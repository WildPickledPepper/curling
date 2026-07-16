#!/usr/bin/env python3
"""Sample the local physics model for the 20 collision configurations.

This is deliberately standalone: it reads only the requested shot/stone
configuration.  Friction noise is generated locally with the recovered
UnityEngine.Random algorithm; no Unity endpoint, pose, per-frame noise, or
post-collision state is consumed.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.calibration.controlled_scene_sampler import EMPTY_POSITION, set_stone_xy
from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module
from tools.reverse.recovered_curling_motion import B2Vec2, STEP, newfrictionstep, unity_friction
from tools.reverse.recovered_sweep_window import sweep_window
from tools.reverse.recovered_unity_random import RecoveredUnityRandom


def _load_plan(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not value:
        raise ValueError("plan must be a non-empty JSON list")
    return value


def _load_sweep_effect_manifest(path: Path | None) -> dict[str, dict[str, Any]]:
    """Load Unity-observed SWEEP dispatch outcomes keyed by exact plan label.

    A protocol request and a physics-effective sweep are intentionally distinct:
    in the WebGL runtime a socket message can be received by JavaScript while
    its Unity handler is deferred until after the current slide has stopped.
    Such a request must not be modelled as an immediately active ice change.
    """

    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    entries = raw.get("entries") if isinstance(raw, dict) else raw
    if not isinstance(entries, list):
        raise ValueError("sweep effect manifest must be a list or an object with an entries list")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("label"), str):
            raise ValueError("each sweep effect manifest entry needs an exact string label")
        label = entry["label"]
        if label in result:
            raise ValueError(f"duplicate sweep effect manifest label: {label}")
        result[label] = entry
    return result


def _effective_sweep(
    row: dict[str, Any],
    effects: dict[str, dict[str, Any]],
    default_delay_m: float,
    request_default_effective: bool,
) -> tuple[float, float, str]:
    """Return effective distance, activation delay and auditable decision source."""

    requested = float(row.get("sweep") or 0.0)
    entry = effects.get(str(row.get("label") or ""))
    if entry is None:
        if request_default_effective:
            return requested, max(0.0, float(default_delay_m)), "assume_requested_effective"
        return 0.0, 0.0, "protocol_request_not_yet_effective"
    effective = bool(entry.get("effective", True))
    if not effective:
        return 0.0, 0.0, "unity_observed_not_effective"
    distance = float(entry.get("effective_distance", requested))
    delay = max(0.0, float(entry.get("start_delay_m", default_delay_m)))
    return distance, delay, "unity_observed_effective"


def _reset_position(row: dict[str, Any], active_index: int) -> tuple[list[float], list[int]]:
    position = list(EMPTY_POSITION)
    target_indices: list[int] = []
    for offset, stone in enumerate(row.get("stones") or []):
        target = stone.get("index")
        if target is None:
            target = active_index + 2 + offset * 2
        target = int(target)
        if target == active_index:
            raise ValueError(f"{row.get('label')}: target conflicts with active stone")
        set_stone_xy(position, target, float(stone["x"]), float(stone["y"]))
        target_indices.append(target)
    if not target_indices:
        raise ValueError(f"{row.get('label')}: no target stones")
    return position, target_indices


def _noise_stream(seed: int, count: int) -> Iterable[float]:
    rng = RecoveredUnityRandom.from_seed(seed)
    for _ in range(count):
        yield rng.range_float(-0.0002, 0.0002)


def _run_to_first_contact(
    scene: Any,
    active_index: int,
    shot: list[float],
    target_indices: list[int],
    noises: Iterable[float],
    sweep_distance: float,
    sweep_start_delay_m: float,
    reset_all_stone_rotations: bool,
) -> dict[str, Any]:
    """Run local front-half with an independently generated friction stream."""

    # Unity's RESETPOSITION writes positions and velocities, not every stone's
    # quaternion.  Preserving the scene's accumulated orientation is therefore
    # the production protocol path.  The explicit reset mode is only for an
    # isolated/fresh-scene diagnostic.
    scene.start_bestshot(active_index, shot, yaw=0.0 if reset_all_stone_rotations else None)
    wanted = set(target_indices)
    # In the socket game, SWEEP is received after MOTIONINFO rather than at
    # the mathematical Midline trigger.  Keep the recovered end boundary,
    # but make the arrival delay an explicit diagnostic input instead of
    # silently assuming a zero-latency command.
    window = sweep_window(
        sweep_distance,
        start_y=sweep_window(sweep_distance).start_y - max(0.0, sweep_start_delay_m),
    )
    for step_index, noise in enumerate(noises, 1):
        current = scene.state(active_index)
        sweeping = bool(sweep_distance > 0.0 and window.active_at(current["y"]))
        speed = newfrictionstep(
            unity_friction(sweeping, noise=float(noise)),
            B2Vec2(float(current["vx"]), float(current["vy"])),
            float(current["w"]),
            STEP,
        )
        step = scene.step_custom_sliding(
            active_index,
            float(noise),
            motion_override=[speed.v.x, speed.v.y, speed.angle],
        )
        hit: set[int] = set()
        for report in step["stoneReports"]:
            pair = {int(report["stoneIndex0"]), int(report["stoneIndex1"])}
            if active_index not in pair or int(report.get("contact_count") or 0) <= 0:
                continue
            other = next(index for index in pair if index != active_index)
            if other in wanted:
                hit.add(other)
        if hit:
            scene.slots[active_index].material.set_static_friction(0.6)
            scene.slots[active_index].material.set_dynamic_friction(0.6)
            scene._custom_sliding_index = None
            return {
                "reached": True,
                "steps": step_index,
                "hitTargets": sorted(hit),
                # These are local diagnostic fields, not Unity handoff data.
                # They make the first impulse and the later free-slide tail
                # separately observable for sweep and multi-stone cases.
                "preContact": {
                    "active": step["beforeScene"],
                    "targets": step["targetsBeforeScene"],
                },
                "postContact": {
                    "active": step["afterScene"],
                    "targets": step["targetsAfterScene"],
                },
                "stoneReports": step["stoneReports"],
            }
    return {
        "reached": False,
        "steps": step_index if "step_index" in locals() else 0,
        "hitTargets": [],
        "preContact": None,
        "postContact": None,
        "stoneReports": [],
    }


def _settle(
    scene: Any,
    max_steps: int,
    *,
    capture_tail_steps: int = 0,
) -> dict[str, Any]:
    quiet = 0
    moving: list[int] = []
    post_contact_tail: list[dict[str, Any]] = []
    for step in range(1, max_steps + 1):
        scene.scene.simulate(scene.dt)
        reports = scene.scene.get_contact_reports()
        if step <= capture_tail_steps:
            post_contact_tail.append(
                {
                    "step": step,
                    "states": {
                        str(slot.index): scene.state(slot.index)
                        for slot in scene.slots
                        if slot.enabled
                    },
                    "stone_reports": scene._stone_reports(reports),
                }
            )
        moving = []
        for slot in scene.slots:
            if not slot.enabled:
                continue
            state = scene.state(slot.index)
            linear = math.sqrt(state["vx"] ** 2 + state["vy"] ** 2 + state["vz"] ** 2)
            angular = math.sqrt(state["wx"] ** 2 + state["wy"] ** 2 + state["w"] ** 2)
            if linear > 0.01 or angular > 0.01:
                moving.append(slot.index)
        quiet = quiet + 1 if not moving else 0
        if quiet >= 20:
            return {
                "settled": True,
                "steps": step,
                "movingIndices": [],
                "post_contact_tail": post_contact_tail,
            }
    return {
        "settled": False,
        "steps": max_steps,
        "movingIndices": moving,
        "post_contact_tail": post_contact_tail,
    }


def _after_position(scene: Any) -> list[float]:
    values = [0.0] * 32
    for slot in scene.slots:
        if not slot.enabled:
            continue
        state = scene.state(slot.index)
        values[2 * slot.index] = float(state["x"])
        values[2 * slot.index + 1] = float(state["y"])
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-file", type=Path, required=True)
    parser.add_argument("--output-file", type=Path, required=True)
    parser.add_argument("--seed-base", type=int, default=20260714)
    parser.add_argument("--max-friction-steps", type=int, default=2500)
    parser.add_argument("--max-settle-steps", type=int, default=6000)
    parser.add_argument(
        "--sweep-start-delay-m",
        type=float,
        default=0.0,
        help="diagnostic protocol-y delay before SWEEP becomes active; default preserves the old zero-delay model",
    )
    parser.add_argument(
        "--sweep-effect-manifest",
        type=Path,
        help="optional Unity-observed sweep dispatch manifest; distinguishes requested from physics-effective sweep",
    )
    parser.add_argument(
        "--sweep-request-policy",
        choices=("protocol-late", "assume-effective"),
        default="protocol-late",
        help="without an observed manifest, socket SWEEP is late for the current slide (default); use assume-effective only for a direct/native sweep API",
    )
    parser.add_argument(
        "--contact-tail-capture-steps",
        type=int,
        default=0,
        help="record this many ordinary PhysX frames immediately after first contact (diagnostic only)",
    )
    parser.add_argument(
        "--compact-training-output",
        action="store_true",
        help="omit pointer-bearing contact snapshots; keeps endpoint/training fields byte-stable across worker processes",
    )
    parser.add_argument(
        "--wake-target-at-current-pcm-shell",
        action="store_true",
        help="diagnostic A/B: wake target on the current PCM-shell frame instead of the next frame",
    )
    parser.add_argument(
        "--emulate-unity-setactive-no-sim",
        action="store_true",
        help="diagnostic A/B: recreate the Unity SetActive no-simulation lifecycle for body ordering",
    )
    parser.add_argument(
        "--reset-all-stone-rotations",
        action="store_true",
        help="diagnostic fresh-scene mode: reset every stone yaw on every RESETPOSITION instead of preserving Unity's protocol state",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="zero-based inclusive plan index for a disjoint worker shard",
    )
    parser.add_argument(
        "--end-index",
        type=int,
        help="zero-based exclusive plan index for a disjoint worker shard (default: end of plan)",
    )
    parser.add_argument(
        "--labels",
        help=(
            "optional comma-separated configuration label prefixes; preserves the original plan "
            "ordinal so diagnostic reruns use the same local seed as the full batch"
        ),
    )
    args = parser.parse_args()

    _install_hybrid_module()
    from unity_front_half_physx import (
        PersistentPhysxFrontHalfScene,
        UNITY_RETAINED_PROTOCOL_X,
        UNITY_RETAINED_PROTOCOL_Y,
    )

    plan = _load_plan(args.plan_file)
    sweep_effects = _load_sweep_effect_manifest(args.sweep_effect_manifest)
    start_index = int(args.start_index)
    end_index = len(plan) if args.end_index is None else int(args.end_index)
    if start_index < 0 or end_index < start_index or end_index > len(plan):
        raise ValueError(f"invalid shard [{start_index}, {end_index}) for plan length {len(plan)}")
    requested_labels = (
        {item.strip() for item in args.labels.split(",") if item.strip()}
        if args.labels
        else None
    )
    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_tilt_only=True,
        emulate_unity_setactive_refilter=True,
        wake_target_at_current_pcm_shell=bool(args.wake_target_at_current_pcm_shell),
        emulate_unity_setactive_no_sim=bool(args.emulate_unity_setactive_no_sim),
    )
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    with args.output_file.open("w", encoding="utf-8") as out:
        for plan_index in range(start_index, end_index):
            row = plan[plan_index]
            base_label = str(row.get("label") or "").rsplit("_r", 1)[0]
            logical_label = base_label[:-5] if base_label.endswith("_dist") else base_label
            if requested_labels is not None and not ({base_label, logical_label} & requested_labels):
                continue
            ordinal = plan_index + 1
            active_index = (ordinal - 1) % 2
            reset_position, target_indices = _reset_position(row, active_index)
            # Production protocol parity: RESETPOSITION preserves each body's
            # quaternion.  Do not inject Unity state; this is the local scene's
            # own persistent orientation history.  The old all-yaw-zero behavior
            # remains available only as an explicit fresh-scene diagnostic.
            scene.reset_positions(
                reset_position,
                yaw_overrides=({index: 0.0 for index in range(16)} if args.reset_all_stone_rotations else None),
                settle_steps=1,
            )
            seed = int(args.seed_base) + ordinal
            effective_sweep, effective_delay_m, sweep_effect_source = _effective_sweep(
                row, sweep_effects, float(args.sweep_start_delay_m),
                args.sweep_request_policy == "assume-effective",
            )
            contact = _run_to_first_contact(
                scene,
                active_index,
                [float(row["v0"]), float(row["h0"]), float(row["w0"])],
                target_indices,
                _noise_stream(seed, args.max_friction_steps),
                effective_sweep,
                effective_delay_m,
                bool(args.reset_all_stone_rotations),
            )
            settle = (
                _settle(
                    scene,
                    args.max_settle_steps,
                    capture_tail_steps=max(0, int(args.contact_tail_capture_steps)),
                )
                if contact["reached"]
                else None
            )
            cleared_indices = (
                scene.clear_out_of_play_stones()
                if settle is not None and settle["settled"]
                else []
            )
            after = _after_position(scene)
            output = {
                "sample_id": int(row.get("sample_id", ordinal)),
                "label": row.get("label"),
                "category": row.get("category"),
                "plan_metadata": {
                    "source_sample_id": row.get("source_sample_id"),
                    "config_index": row.get("config_index"),
                    "repeat_index": row.get("repeat_index"),
                },
                "random_source": {
                    "algorithm": "recovered UnityEngine.Random",
                    "seed": seed,
                    "unity_state_or_endpoint_injected": False,
                },
                "local_contact_lifecycle": {
                    "wake_target_at_current_pcm_shell": bool(args.wake_target_at_current_pcm_shell),
                    "emulate_unity_setactive_no_sim": bool(args.emulate_unity_setactive_no_sim),
                    "sweep_start_delay_m": effective_delay_m,
                    "requested_sweep": float(row.get("sweep") or 0.0),
                    "effective_sweep": effective_sweep,
                    "sweep_effect_source": sweep_effect_source,
                    "sweep_request_policy": args.sweep_request_policy,
                    "reset_all_stone_rotations": bool(args.reset_all_stone_rotations),
                    "compact_training_output": bool(args.compact_training_output),
                },
                "active_shot_num": active_index,
                "target_indices": target_indices,
                "requested": {key: row.get(key) for key in ("v0", "h0", "w0", "sweep", "stones")},
                "reset_position": reset_position,
                "collision_observed": contact["reached"],
                "first_contact_steps": contact["steps"],
                "hit_target_indices": contact["hitTargets"],
                "first_contact": (
                    None if args.compact_training_output else {
                        "pre": contact["preContact"],
                        "post": contact["postContact"],
                        "stone_reports": contact["stoneReports"],
                    }
                ),
                "settle": settle,
                "out_of_play": {
                    "applied": settle is not None and settle["settled"],
                    "retained_protocol_bounds": {
                        "x": list(UNITY_RETAINED_PROTOCOL_X),
                        "y": list(UNITY_RETAINED_PROTOCOL_Y),
                    },
                    "cleared_indices": cleared_indices,
                },
                "after_position": after,
                "final_xy": [after[2 * active_index], after[2 * active_index + 1]],
            }
            out.write(json.dumps(output, ensure_ascii=False) + "\n")
            shard_ordinal = plan_index - start_index + 1
            shard_total = end_index - start_index
            if shard_ordinal % 50 == 0 or shard_ordinal == shard_total:
                print(f"local shard [{start_index},{end_index}) {shard_ordinal}/{shard_total}", flush=True)


if __name__ == "__main__":
    main()
