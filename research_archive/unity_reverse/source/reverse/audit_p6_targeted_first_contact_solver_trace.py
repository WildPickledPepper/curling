#!/usr/bin/env python3
"""Capture the local solver trace for one recorded P6 first-contact step.

Unlike an isolated truth-filled pair, this replays all earlier shots in the
same persistent local Scene, resets only recorded x/y positions, and enables
the native trace immediately before the selected shot's already-known
first-contact step.  It is therefore the local counterpart to a targeted C04
window without injecting Unity P/Q/v/w.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module
from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl


def samples(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def settle(scene: Any, limit: int = 6000) -> None:
    quiet = 0
    for _ in range(limit):
        scene.scene.simulate(scene.dt)
        scene.scene.get_contact_reports()
        moving = False
        for slot in scene.slots:
            if not slot.enabled:
                continue
            state = scene.state(slot.index)
            if math.sqrt(sum(float(state[key]) ** 2 for key in ("vx", "vy", "vz", "wx", "wy", "w"))) > 0.01:
                moving = True
                break
        quiet = 0 if moving else quiet + 1
        if quiet >= 20:
            return
    raise RuntimeError("local Scene did not settle before the next recorded reset")


def offset_f32_ulp(value: float, ulps: int) -> float:
    """Move one scalar float32 value by signed ULPs, preserving its sign ordering."""
    if ulps == 0:
        return float(value)
    bits = struct.unpack("<I", struct.pack("<f", float(value)))[0]
    if bits & 0x80000000:
        bits -= int(ulps)
    else:
        bits += int(ulps)
    return struct.unpack("<f", struct.pack("<I", bits & 0xFFFFFFFF))[0]


def offset_stationary_target_x(scene: Any, target_indices: list[int], ulps: int) -> None:
    """Diagnostic-only stationary-target pose perturbation after ResetState."""
    if ulps == 0:
        return
    for index in target_indices:
        position, quaternion = scene._pose(index)
        position[0] = offset_f32_ulp(position[0], ulps)
        scene.slots[index].body.set_global_pose((position, quaternion))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--endpoint-audit", type=Path, required=True, help="Matching P6 endpoint audit that records firstContactStep.")
    parser.add_argument("--label", required=True)
    parser.add_argument(
        "--active-yaw-override",
        type=float,
        help=(
            "Diagnostic-only: replace the selected active stone's yaw immediately before "
            "the traced first-contact tick. This is never a production replay input."
        ),
    )
    parser.add_argument(
        "--stationary-physx-x-f32-ulp",
        type=int,
        default=0,
        help=(
            "Diagnostic-only signed float32-ULP offset applied to each recorded stationary "
            "target immediately after ResetState; never a production replay input."
        ),
    )
    parser.add_argument(
        "--post-first-active-quaternion-w-f32-ulp",
        type=int,
        default=0,
        help=(
            "Diagnostic-only signed float32-ULP adjustment to the active quaternion W "
            "after the traced first-contact step and before the tail; never a production input."
        ),
    )
    parser.add_argument(
        "--post-contact-tail-steps",
        type=int,
        default=0,
        help="After the traced first-contact Scene step, record this many read-only local physics tail steps.",
    )
    parser.add_argument(
        "--post-contact-tail-trace-steps",
        type=int,
        default=0,
        help="Replace the exported solver trace with this many immediately following post-contact physics steps.",
    )
    parser.add_argument(
        "--reset-settle-steps",
        type=int,
        default=1,
        help=(
            "Diagnostic-only replacement for the production replay reset settle count. "
            "Use only to locate activation/support timing; default 1 preserves the replay."
        ),
    )
    parser.add_argument(
        "--reset-no-force-sleep",
        action="store_true",
        help=(
            "Diagnostic-only: do not force stationary bodies to sleep after each reset. "
            "Never a production replay input."
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = samples(args.samples)
    groups = event_shot_groups(load_jsonl(args.events))
    if len(rows) != len(groups):
        raise ValueError(f"sample/event count mismatch: {len(rows)} != {len(groups)}")
    audit_rows = json.loads(args.endpoint_audit.read_text(encoding="utf-8")).get("rows") or []
    target_seq = next((index for index, row in enumerate(rows) if row.get("label") == args.label), None)
    audit_row = next((row for row in audit_rows if row.get("label") == args.label), None)
    if target_seq is None or audit_row is None:
        raise ValueError(f"label not found: {args.label}")
    contact_step = int(audit_row.get("firstContactStep") or 0)
    if contact_step < 1:
        raise ValueError("target audit has no firstContactStep")
    if args.reset_settle_steps < 0:
        raise ValueError("--reset-settle-steps must be non-negative")

    _install_hybrid_module()
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
    )
    target_step: dict[str, Any] | None = None
    for seq, (sample, group) in enumerate(zip(rows, groups)):
        active = int(sample["active_shot_num"])
        target_indices = [int(value) for value in sample.get("target_indices") or []]
        scene.reset_positions(
            sample["reset_position"],
            settle_steps=int(args.reset_settle_steps),
            force_sleep_after_reset=not bool(args.reset_no_force_sleep),
        )
        offset_stationary_target_x(
            scene, target_indices, int(args.stationary_physx_x_f32_ulp)
        )
        noises = [float(item["noise"]) for item in group["friction"]]
        shot = [float(group["v0"]), float(group["h0"]), float(group["w0"])]
        if seq != target_seq:
            replay = scene.run_bestshot_to_first_contact(active, shot, noises, target_indices=target_indices, max_steps=len(noises))
            if not replay.get("reachedFirstContact"):
                raise RuntimeError(f"prior shot {sample['label']} did not reach local contact")
            scene.scene.simulate(scene.dt)
            scene.scene.get_contact_reports()
            settle(scene)
            continue

        if contact_step > len(noises):
            raise ValueError(f"contact step {contact_step} exceeds recorded friction count {len(noises)}")
        scene.start_bestshot(active, shot)
        for noise in noises[: contact_step - 1]:
            scene.step_custom_sliding(active, noise)
        if args.active_yaw_override is not None:
            current = scene.state(active)
            scene._set_pose(active, current["x"], current["y"], float(args.active_yaw_override))
        scene.pyphysx.clear_scene_finalizer_trace()
        scene.pyphysx.clear_scene_solve_writeback_trace()
        scene.pyphysx.clear_scene_solve_block_trace()
        scene.pyphysx.set_scene_finalizer_trace_enabled(True)
        scene.pyphysx.set_scene_solve_writeback_trace_enabled(True)
        scene.pyphysx.set_scene_solve_block_trace_enabled(True)
        target_step = scene.step_custom_sliding(active, noises[contact_step - 1])
        scene.pyphysx.set_scene_finalizer_trace_enabled(False)
        scene.pyphysx.set_scene_solve_writeback_trace_enabled(False)
        scene.pyphysx.set_scene_solve_block_trace_enabled(False)
        break

    if target_step is None:
        raise RuntimeError("target shot was not replayed")
    if args.post_contact_tail_steps < 0:
        raise ValueError("--post-contact-tail-steps must be non-negative")
    if args.post_contact_tail_trace_steps < 0 or args.post_contact_tail_trace_steps > args.post_contact_tail_steps:
        raise ValueError("--post-contact-tail-trace-steps must be between zero and --post-contact-tail-steps")
    post_contact_tail: list[dict[str, Any]] = []
    if args.post_contact_tail_steps:
        # ``_run_to_first_contact`` restores the active stone's regular ice
        # material immediately after the matching report.  This targeted
        # collector invokes ``step_custom_sliding`` directly so it must mirror
        # that production handoff before observing any post-contact tail.
        scene.slots[active].material.set_static_friction(0.6)
        scene.slots[active].material.set_dynamic_friction(0.6)
        active_quaternion_w_ulp = int(args.post_first_active_quaternion_w_f32_ulp)
        if active_quaternion_w_ulp:
            position, quaternion = scene._pose(active)
            quaternion[0] = offset_f32_ulp(quaternion[0], active_quaternion_w_ulp)
            scene.slots[active].body.set_global_pose((position, quaternion))
        watched_targets = [int(index) for index in target_indices]
        if args.post_contact_tail_trace_steps:
            scene.pyphysx.clear_scene_finalizer_trace()
            scene.pyphysx.clear_scene_solve_writeback_trace()
            scene.pyphysx.clear_scene_solve_block_trace()
            scene.pyphysx.clear_scene_pcm_trace()
            scene.pyphysx.set_scene_finalizer_trace_enabled(True)
            scene.pyphysx.set_scene_solve_writeback_trace_enabled(True)
            scene.pyphysx.set_scene_solve_block_trace_enabled(True)
            # Read-only capture of the PCM geometry used to rebuild the
            # second-tick pair constraint.  The production cache-lifecycle
            # wrapper is already installed; this only retains its inputs and
            # outputs for the diagnostic report.
            scene.pyphysx.set_scene_pcm_trace_enabled(True)
        post_contact_tail.append({
            "tailStep": 0,
            "active": scene.state(active),
            "targets": {str(index): scene.state(index) for index in watched_targets},
        })
        for tail_step in range(1, args.post_contact_tail_steps + 1):
            scene.scene.simulate(scene.dt)
            scene.scene.get_contact_reports()
            post_contact_tail.append({
                "tailStep": tail_step,
                "active": scene.state(active),
                "targets": {str(index): scene.state(index) for index in watched_targets},
            })
            if args.post_contact_tail_trace_steps and tail_step == args.post_contact_tail_trace_steps:
                scene.pyphysx.set_scene_finalizer_trace_enabled(False)
                scene.pyphysx.set_scene_solve_writeback_trace_enabled(False)
                scene.pyphysx.set_scene_solve_block_trace_enabled(False)
                scene.pyphysx.set_scene_pcm_trace_enabled(False)
    report = {
        "schema": "p6_targeted_first_contact_solver_trace_v1",
        "scope": "read-only no-oracle persistent-scene replay; native tracing begins only on the recorded first-contact step",
        "label": args.label,
        "firstContactStep": contact_step,
        "diagnosticActiveYawOverride": args.active_yaw_override,
        "diagnosticStationaryPhysxXF32Ulp": int(args.stationary_physx_x_f32_ulp),
        "diagnosticPostFirstActiveQuaternionWF32Ulp": int(
            args.post_first_active_quaternion_w_f32_ulp
        ),
        "diagnosticResetSettleSteps": int(args.reset_settle_steps),
        "diagnosticResetNoForceSleep": bool(args.reset_no_force_sleep),
        "traceScope": "post-contact-tail" if args.post_contact_tail_trace_steps else "first-contact",
        "firstStep": target_step,
        "finalizerTrace": list(scene.pyphysx.get_scene_finalizer_trace(True)),
        "solveBlockTrace": list(scene.pyphysx.get_scene_solve_block_trace(True)),
        "solveWritebackTrace": list(scene.pyphysx.get_scene_solve_writeback_trace(True)),
        "postContactPcmTrace": list(scene.pyphysx.get_scene_pcm_trace(True)),
        "postContactTail": post_contact_tail,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "label": args.label, "firstContactStep": contact_step, "traceCounts": {key: len(report[key]) for key in ("finalizerTrace", "solveBlockTrace", "solveWritebackTrace")}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
