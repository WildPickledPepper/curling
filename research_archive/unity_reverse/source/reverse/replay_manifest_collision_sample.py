#!/usr/bin/env python3
"""Replay one captured collision with its recorded Unity friction sequence.

The Unity endpoint in the sampler record is used only for the final comparison.
The local Scene receives just reset positions, BESTSHOT input, and the recorded
per-tick ``Random.Range`` friction values.  In particular, no Unity pose,
velocity, contact manifold, or post-contact state is injected.
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

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module  # noqa: E402


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        key: state[key]
        for key in ("x", "y", "vx", "vy", "w", "yaw", "physxPosition", "physxLinearVelocity", "physxAngularVelocity")
    }


def _settle(scene: Any, *, max_steps: int) -> int:
    quiet = 0
    for step in range(1, max_steps + 1):
        scene.scene.simulate(scene.dt)
        scene.scene.get_contact_reports()
        moving = False
        for slot in scene.slots:
            if not slot.enabled:
                continue
            state = scene.state(slot.index)
            if math.hypot(float(state["vx"]), float(state["vy"])) > 0.01 or abs(float(state["w"])) > 0.01:
                moving = True
                break
        quiet = 0 if moving else quiet + 1
        if quiet >= 20:
            return step
    return max_steps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, required=True, help="Unity sampler JSONL containing the selected shot")
    parser.add_argument("--manifest", type=Path, required=True, help="JSONL of captured sliding.random_range.friction events")
    parser.add_argument("--label", help="Exact sampler label; required when --sample has more than one row")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-settle-steps", type=int, default=6000)
    args = parser.parse_args()

    samples = _rows(args.sample)
    if args.label:
        samples = [row for row in samples if row.get("label") == args.label]
    if len(samples) != 1:
        raise ValueError("select exactly one sampler row with --label")
    sample = samples[0]
    targets = [int(index) for index in sample.get("target_indices") or []]
    if not targets:
        raise ValueError("sample has no target indices")
    active = int(sample["active_shot_num"])
    manifest = _rows(args.manifest)
    noise = [float((row.get("data") or {})["value"]) for row in manifest]
    if not noise:
        raise ValueError("friction manifest is empty")

    _install_hybrid_module()
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_tilt_only=True,
        emulate_unity_setactive_refilter=True,
    )
    scene.reset_positions(
        [float(value) for value in sample["reset_position"]],
        yaw_overrides={index: 0.0 for index in range(16)},
        settle_steps=1,
    )
    requested = sample["requested"]
    replay = scene.run_bestshot_to_first_contact(
        active,
        [float(requested[key]) for key in ("v0", "h0", "w0")],
        noise,
        target_indices=targets,
        yaw=0.0,
        max_steps=len(noise),
    )
    result: dict[str, Any] = {
        "schema": "manifest_collision_replay_v2",
        "policy": "recorded friction only; no Unity state is injected into the local Scene",
        "input": {"sample": str(args.sample), "manifest": str(args.manifest), "label": sample.get("label")},
        "frictionDrawCount": len(noise),
        "firstContact": {
            "reached": bool(replay.get("reachedFirstContact")),
            "step": replay.get("steps"),
            "contactCounts": [int(row.get("contact_count") or 0) for row in replay.get("firstContactReports") or []],
        },
    }
    if not replay.get("reachedFirstContact"):
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 2

    result["firstContact"].update(
        {
            "activeBefore": _state(replay["beforeScene"]),
            "targetsBefore": {
                str(target): _state(replay["targetsBeforeScene"][str(target)])
                for target in targets
            },
            "activeAfter": _state(replay["afterScene"]),
            "targetsAfter": {
                str(target): _state(replay["targetsAfterScene"][str(target)])
                for target in targets
            },
        }
    )
    settle_steps = _settle(scene, max_steps=int(args.max_settle_steps))
    local_active = scene.state(active)
    unity_position = [float(value) for value in sample["after_position"]]
    unity_active = unity_position[2 * active : 2 * active + 2]
    local_targets = {str(target): scene.state(target) for target in targets}
    unity_targets = {
        str(target): unity_position[2 * target : 2 * target + 2]
        for target in targets
    }
    local_target_xy = {
        target: [state["x"], state["y"]]
        for target, state in local_targets.items()
    }
    target_error_mm = {
        target: 1000.0 * math.hypot(
            local_target_xy[target][0] - unity_targets[target][0],
            local_target_xy[target][1] - unity_targets[target][1],
        )
        for target in local_target_xy
    }
    result["endpoint"] = {
        "settleSteps": settle_steps,
        "unity": {"active": unity_active, "targets": unity_targets},
        "local": {"active": [local_active["x"], local_active["y"]], "targets": local_target_xy},
        "errorMm": {
            "active": 1000.0 * math.hypot(local_active["x"] - unity_active[0], local_active["y"] - unity_active[1]),
            "targets": target_error_mm,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "firstContact": result["firstContact"], "endpointErrorMm": result["endpoint"]["errorMm"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
