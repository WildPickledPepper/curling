#!/usr/bin/env python3
"""Replay a complete Unity collision session with its per-shot friction stream.

Unlike the one-shot manifest replay, this runner intentionally keeps the local
scene alive across rows.  That reproduces Unity's normal RESETPOSITION contract:
positions and velocities reset, while each stone's orientation remains part of
the persistent physics state.  No Unity P/Q/v/w or contact state is injected.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module
from tools.reverse.front_half_pcm_replay import BESTSHOT_RE, text_preview
from tools.reverse.sample_local_collision_distribution import (
    _after_position,
    _effective_sweep,
    _load_sweep_effect_manifest,
    _run_to_first_contact,
    _settle,
)


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _friction_by_shot(events: Path) -> list[list[float]]:
    shots: list[list[float]] = []
    current = -1
    for line in events.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if BESTSHOT_RE.search(text_preview(event)):
            shots.append([])
            current += 1
            continue
        if current >= 0 and event.get("type") == "sliding.random_range.friction":
            shots[current].append(float((event.get("data") or {})["value"]))
    return shots


def _xy(values: list[float], index: int) -> list[float]:
    return [float(values[2 * index]), float(values[2 * index + 1])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True, help="Unity controlled-sampler JSONL")
    parser.add_argument("--events", type=Path, required=True, help="Unity runtime events JSONL with friction events")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-settle-steps", type=int, default=6000)
    parser.add_argument(
        "--sweep-start-delay-m", type=float, default=0.0,
        help="Protocol-distance delay before a SWEEP command becomes active; diagnostic only.",
    )
    parser.add_argument("--sweep-effect-manifest", type=Path)
    parser.add_argument(
        "--sweep-request-policy", choices=("protocol-late", "assume-effective"), default="protocol-late",
    )
    parser.add_argument(
        "--reset-all-stone-rotations",
        action="store_true",
        help="diagnostic fresh-state A/B; production replay preserves persistent orientation",
    )
    args = parser.parse_args()

    samples = _rows(args.samples)
    sweep_effects = _load_sweep_effect_manifest(args.sweep_effect_manifest)
    friction = _friction_by_shot(args.events)
    if len(friction) < len(samples):
        raise ValueError(f"friction stream has {len(friction)} BESTSHOT sections for {len(samples)} samples")
    if any(not values for values in friction[:len(samples)]):
        raise ValueError("at least one selected BESTSHOT has no friction values")

    _install_hybrid_module()
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_tilt_only=True,
        emulate_unity_setactive_refilter=True,
    )
    rows: list[dict[str, Any]] = []
    for ordinal, sample in enumerate(samples):
        active = int(sample["active_shot_num"])
        targets = [int(value) for value in sample.get("target_indices") or []]
        if not targets:
            raise ValueError(f"{sample.get('label')}: no target indices")
        scene.reset_positions(
            [float(value) for value in sample["reset_position"]],
            yaw_overrides=({index: 0.0 for index in range(16)} if args.reset_all_stone_rotations else None),
            settle_steps=1,
        )
        requested = sample["requested"]
        sweep_row = dict(requested)
        sweep_row["label"] = sample.get("label")
        effective_sweep, effective_delay_m, sweep_effect_source = _effective_sweep(
            sweep_row, sweep_effects, float(args.sweep_start_delay_m),
            args.sweep_request_policy == "assume-effective",
        )
        contact = _run_to_first_contact(
            scene,
            active,
            [float(requested[key]) for key in ("v0", "h0", "w0")],
            targets,
            friction[ordinal],
            effective_sweep,
            effective_delay_m,
            bool(args.reset_all_stone_rotations),
        )
        settle = _settle(scene, int(args.max_settle_steps)) if contact["reached"] else None
        if settle and settle["settled"]:
            scene.clear_out_of_play_stones()
        local_after = _after_position(scene)
        unity_after = [float(value) for value in sample["after_position"]]
        active_error = 1000.0 * math.dist(_xy(local_after, active), _xy(unity_after, active))
        target_errors = {
            str(target): 1000.0 * math.dist(_xy(local_after, target), _xy(unity_after, target))
            for target in targets
        }
        rows.append({
            "ordinal": ordinal,
            "label": sample.get("label"),
            "frictionDrawCount": len(friction[ordinal]),
            "sweep": {
                "requested": float(requested.get("sweep") or 0.0),
                "effective": effective_sweep,
                "startDelayM": effective_delay_m,
                "source": sweep_effect_source,
            },
            "firstContact": {"reached": bool(contact["reached"]), "steps": contact["steps"], "hitTargets": contact["hitTargets"]},
            "unity": {"active": _xy(unity_after, active), "targets": {str(target): _xy(unity_after, target) for target in targets}},
            "local": {"active": _xy(local_after, active), "targets": {str(target): _xy(local_after, target) for target in targets}},
            "errorMm": {"active": active_error, "targets": target_errors},
            "branch": {"unityFar": _xy(unity_after, active)[0] < 1.3, "localFar": _xy(local_after, active)[0] < 1.3},
        })

    result = {
        "schema": "manifest_collision_session_replay_v1",
        "policy": "friction values are replayed; local scene persists its own orientation between protocol resets; no Unity P/Q/v/w/contact state is injected",
        "input": {
            "samples": str(args.samples), "events": str(args.events),
            "resetAllStoneRotations": bool(args.reset_all_stone_rotations),
            "sweepStartDelayM": max(0.0, float(args.sweep_start_delay_m)),
            "sweepEffectManifest": None if args.sweep_effect_manifest is None else str(args.sweep_effect_manifest),
            "sweepRequestPolicy": args.sweep_request_policy,
        },
        "rows": rows,
        "summary": {
            "samples": len(rows),
            "branchMatches": sum(item["branch"]["unityFar"] == item["branch"]["localFar"] for item in rows),
            "unityFar": sum(item["branch"]["unityFar"] for item in rows),
            "localFar": sum(item["branch"]["localFar"] for item in rows),
            "meanActiveErrorMm": sum(item["errorMm"]["active"] for item in rows) / len(rows),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "summary": result["summary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
