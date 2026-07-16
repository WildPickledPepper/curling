#!/usr/bin/env python3
"""Diagnose one C03 dynamic-dynamic solve from the captured Unity pre-state.

This is deliberately an oracle *diagnostic*: the Unity rigid-core P/Q/v/w
immediately before its first dynamic-dynamic solver setup is injected into a
fresh local identity-preserving pair.  It does not alter production simulation.
The discriminator is narrow:

* matching post-step states mean the remaining reusable-state error is before
  this solver call (pair/history preparation);
* a post-step mismatch with matching input means the dynamic consume/writeback
  or integration boundary is still different.
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

from tools.reverse.audit_hybrid_p6_endpoint_sixshot import install_pyphysx_extension  # noqa: E402


DEFAULT_EVENTS = (
    ROOT
    / "log/c03_first_writeback_20260712/unity_runtime_probe_20260712_193902/events.jsonl"
)
DEFAULT_EXTENSION = Path(r"D:\esp\tmp\curling_pyphysx_hybrid_build\lib\_pyphysx.cp38-win_amd64.pyd")
DEFAULT_OUTPUT = ROOT / "data/calibration/c03_same_run_dynamic_writeback_14000_20260712.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--pyphysx-extension", type=Path, default=DEFAULT_EXTENSION)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--active-friction",
        type=float,
        default=0.6,
        help="diagnostic material value for active during this one Scene step",
    )
    parser.add_argument(
        "--c04-window",
        action="store_true",
        help="Compare a post-contact local multi-step tail to C04 dynamic-solver frame exits in --events.",
    )
    parser.add_argument(
        "--c05-window",
        action="store_true",
        help="Replay the Unity C05 PCM-call count and export local persistent PCM cache states.",
    )
    parser.add_argument(
        "--pcm-trace",
        action="store_true",
        help="Export local Scene PCM calls from this diagnostic replay without requiring C05 Unity events.",
    )
    parser.add_argument(
        "--empty-target-multi-payload",
        action="store_true",
        help="Diagnostic only: clear convex-mesh multi-manifold payload/cache size before each Scene PCM call.",
    )
    parser.add_argument(
        "--empty-multi-cache-at-narrowphase",
        action="store_true",
        help="Diagnostic only: present an empty task-local multi-manifold at the PxcDiscreteNarrowPhasePCM boundary.",
    )
    parser.add_argument(
        "--narrowphase-trace",
        action="store_true",
        help="Read-only: export parent narrowphase cache headers without enabling any diagnostic cache mutation.",
    )
    parser.add_argument(
        "--c28-solver-setup-trace",
        action="store_true",
        help="Read-only: export outer local solverSetupSolve entry/exit snapshots for phase mapping.",
    )
    parser.add_argument(
        "--c29-phase4-active-q-oracle",
        action="store_true",
        help="Diagnostic only: replace active quaternion with Unity phase-4 entry immediately before local frame 3.",
    )
    parser.add_argument(
        "--truth-fill-q-entry-indices",
        default="",
        help="Diagnostic only: comma-separated aligned C04 entry indices where active0 q is set to same-run Unity truth.",
    )
    parser.add_argument(
        "--truth-fill-full-entry-indices",
        default="",
        help="Diagnostic only: comma-separated aligned C04 entry indices where both stones receive same-run Unity P/Q/v/w truth.",
    )
    parser.add_argument(
        "--truth-fill-active-w-entry-indices",
        default="",
        help=(
            "Diagnostic only: comma-separated aligned C04 entry indices where only "
            "active0 angular velocity is set to same-run Unity truth. Unlike the full "
            "P/Q/v/w oracle this preserves the local pose, linear velocity, and contact cache."
        ),
    )
    parser.add_argument(
        "--truth-fill-target-w-entry-indices",
        default="",
        help=(
            "Diagnostic only: comma-separated aligned C04 entry indices where only "
            "target8 angular velocity is set to same-run Unity truth."
        ),
    )
    parser.add_argument(
        "--continue-after-c04-to-settle",
        action="store_true",
        help=(
            "Diagnostic only: after the C04 replay, advance the same isolated pair until quiet; "
            "used only to measure an oracle/no-oracle local endpoint delta."
        ),
    )
    parser.add_argument(
        "--settle-max-steps",
        type=int,
        default=6000,
        help="Maximum post-C04 diagnostic settle steps (default: 6000).",
    )
    parser.add_argument(
        "--clear-physx-angular-locks",
        action="store_true",
        help="Diagnostic: clear local PhysX X/Z lock flags while retaining the Unity setter projection and inertia tensor.",
    )
    parser.add_argument(
        "--unity-target-velocity-normal",
        action="store_true",
        help="Diagnostic: enable the recovered stone-stone contact-modify callback (0.36 friction plus targetVelocity=normal).",
    )
    parser.add_argument(
        "--disable-strong-friction",
        action="store_true",
        help="Diagnostic: set eDISABLE_STRONG_FRICTION on both dynamic stone materials to test friction-patch reuse.",
    )
    return parser.parse_args()


def _event(events: Path) -> dict[str, Any]:
    for line in events.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("type") == "c03.first_dynamic_writeback":
            return row["data"]
    raise RuntimeError(f"c03.first_dynamic_writeback not found in {events}")


def _core(data: dict[str, Any], index: int, phase: str) -> dict[str, Any]:
    values = data["manager"][phase]
    try:
        return values[index]["decodedCandidate"]
    except (IndexError, KeyError, TypeError) as exc:
        raise RuntimeError(f"missing manager {phase} core {index}") from exc


def _delta(left: list[float], right: list[float]) -> dict[str, Any]:
    components = [float(a) - float(b) for a, b in zip(left, right)]
    return {"components": components, "maxAbs": max(abs(value) for value in components)}


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


def _f32_bits(value: float) -> int:
    return struct.unpack("<I", struct.pack("<f", _f32(value)))[0]


def _normalize_quaternion_f32(quaternion: list[float]) -> dict[str, Any]:
    q = [_f32(value) for value in quaternion]
    length_sq = _f32(0.0)
    for value in q:
        length_sq = _f32(length_sq + _f32(value * value))
    inverse_length = _f32(1.0 / _f32(math.sqrt(length_sq)))
    normalized = [_f32(value * inverse_length) for value in q]
    return {
        "lengthSquared": length_sq,
        "inverseLength": inverse_length,
        "q": normalized,
        "bits": [_f32_bits(value) for value in normalized],
    }


def _pose(body: Any) -> dict[str, list[float]]:
    position, quaternion = body.get_global_pose()
    return {
        "p": [float(value) for value in position],
        "q": [
            float(getattr(quaternion, "x")),
            float(getattr(quaternion, "y")),
            float(getattr(quaternion, "z")),
            float(getattr(quaternion, "w")),
        ],
    }


def _body_state(body: Any) -> dict[str, list[float]]:
    pose = _pose(body)
    return {
        **pose,
        "v": [float(value) for value in body.get_linear_velocity()],
        "w": [float(value) for value in body.get_angular_velocity()],
    }


def _unity_state(core: dict[str, Any]) -> dict[str, list[float]]:
    return {
        "p": [float(value) for value in core["p"]],
        "q": [float(value) for value in core["q"]],
        "v": [float(value) for value in core["linearVelocity"]],
        "w": [float(value) for value in core["angularVelocity"]],
    }


def _compare(local: dict[str, list[float]], unity: dict[str, list[float]]) -> dict[str, Any]:
    return {field: _delta(local[field], unity[field]) for field in ("p", "q", "v", "w")}


def _settle_isolated_pair(scene: Any, *, max_steps: int) -> dict[str, Any]:
    """Advance only this diagnostic fixture; never used by production paths."""
    quiet = 0
    moving: list[int] = []
    for step in range(1, max_steps + 1):
        scene.scene.simulate(scene.dt)
        scene.scene.get_contact_reports()
        moving = []
        for slot_index in (0, 8):
            state = _body_state(scene.slots[slot_index].body)
            linear = math.sqrt(sum(value * value for value in state["v"]))
            angular = math.sqrt(sum(value * value for value in state["w"]))
            if linear > 0.01 or angular > 0.01:
                moving.append(slot_index)
        quiet = quiet + 1 if not moving else 0
        if quiet >= 20:
            return {
                "settled": True,
                "steps": step,
                "movingIndices": [],
                "final": [_body_state(scene.slots[index].body) for index in (0, 8)],
            }
    return {
        "settled": False,
        "steps": max_steps,
        "movingIndices": moving,
        "final": [_body_state(scene.slots[index].body) for index in (0, 8)],
    }


def _c04_windows(events: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in events.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("type") != "c04.dynamic_solver_frame":
            continue
        data = row.get("data") or {}
        exits = data.get("exitCores") or []
        entries = data.get("entryCores") or []
        if len(entries) < 2 or len(exits) < 2:
            continue
        rows.append({
            "frameIndex": int(data.get("frameIndex") or 0),
            "entry": [_unity_state(item["decodedCandidate"]) for item in entries[:2]],
            "exit": [_unity_state(item["decodedCandidate"]) for item in exits[:2]],
        })
    return sorted(rows, key=lambda item: item["frameIndex"])


def _max_state_error(left: dict[str, list[float]], right: dict[str, list[float]]) -> float:
    return max(
        abs(float(value_left) - float(value_right))
        for field in ("p", "q", "v", "w")
        for value_left, value_right in zip(left[field], right[field])
    )


def _parse_indices(value: str) -> set[int]:
    if not value.strip():
        return set()
    try:
        indices = {int(item.strip()) for item in value.split(",") if item.strip()}
    except ValueError as exc:
        raise RuntimeError("truth-fill indices must be comma-separated integers") from exc
    if any(index < 0 for index in indices):
        raise RuntimeError("truth-fill indices must be non-negative")
    return indices


def _c05_call_count(events: Path) -> int:
    return sum(
        1
        for line in events.read_text(encoding="utf-8").splitlines()
        if json.loads(line).get("type") == "c05.persistent_pcm_call"
    )


def main() -> int:
    args = parse_args()
    if args.continue_after_c04_to_settle and not args.c04_window:
        raise RuntimeError("--continue-after-c04-to-settle requires --c04-window")
    truth_fill_q_indices = _parse_indices(args.truth_fill_q_entry_indices)
    truth_fill_full_indices = _parse_indices(args.truth_fill_full_entry_indices)
    truth_fill_active_w_indices = _parse_indices(args.truth_fill_active_w_entry_indices)
    truth_fill_target_w_indices = _parse_indices(args.truth_fill_target_w_entry_indices)
    if (truth_fill_q_indices or truth_fill_full_indices or truth_fill_active_w_indices or truth_fill_target_w_indices) and not args.c04_window:
        raise RuntimeError("truth-fill entry indices require --c04-window")
    captured = _event(args.events)
    unity_before = [_unity_state(_core(captured, index, "coresBeforeSolve")) for index in range(2)]
    unity_after = [_unity_state(_core(captured, index, "coresAfterSolverSetup")) for index in range(2)]

    install_pyphysx_extension(args.pyphysx_extension)
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_rotation=True,
        emulate_unity_setactive_no_sim=True,
        restore_active_friction_at_pcm_shell=True,
        enable_stone_stone_contact_friction_override=args.unity_target_velocity_normal,
    )
    if args.clear_physx_angular_locks:
        for slot in scene.slots:
            slot.body.set_rigid_dynamic_lock_flag(
                scene.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_X, False
            )
            slot.body.set_rigid_dynamic_lock_flag(
                scene.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_Z, False
            )
    scene.pyphysx.clear_scene_finalizer_trace()
    scene.pyphysx.clear_scene_solve_writeback_trace()
    scene.pyphysx.clear_scene_solve_block_trace()
    if args.c28_solver_setup_trace:
        scene.pyphysx.clear_scene_solver_setup_trace()
        scene.pyphysx.set_scene_solver_setup_trace_enabled(True)
    scene.pyphysx.set_scene_finalizer_trace_enabled(True)
    scene.pyphysx.set_scene_solve_writeback_trace_enabled(True)
    scene.pyphysx.set_scene_solve_block_trace_enabled(True)
    if args.c05_window or args.pcm_trace:
        scene.pyphysx.clear_scene_pcm_trace()
        scene.pyphysx.set_scene_pcm_trace_enabled(True)
    if args.empty_target_multi_payload:
        scene.pyphysx.set_scene_pcm_empty_multi_payload_diagnostic(True)
    if args.empty_multi_cache_at_narrowphase or args.narrowphase_trace:
        scene.pyphysx.clear_scene_narrowphase_trace()
        scene.pyphysx.set_scene_narrowphase_trace_enabled(True)
    if args.empty_multi_cache_at_narrowphase:
        scene.pyphysx.set_scene_narrowphase_empty_multi_cache_diagnostic(True)

    # Preserve Unity's role creation: target is made live first, then active.
    scene.reset_positions([0.0] * 32, settle_steps=0)
    scene.activate_stationary(8, 0.0, 0.0)
    scene.start_bestshot(0, [3.4, 0.0, 0.0])
    for slot_index, expected in zip((0, 8), unity_before):
        body = scene.slots[slot_index].body
        # Runtime probe transforms are xyzw; this pyphysx binding accepts
        # quaternion constructor lists in wxyz order.
        qx, qy, qz, qw = expected["q"]
        body.set_global_pose((expected["p"], [qw, qx, qy, qz]))
        body.set_linear_velocity(expected["v"])
        body.set_angular_velocity(expected["w"])
        body.wake_up()
    for slot_index, friction in ((0, float(args.active_friction)), (8, 0.6)):
        material = scene.slots[slot_index].material
        material.set_static_friction(friction)
        material.set_dynamic_friction(friction)
        if args.disable_strong_friction:
            material.set_flag(scene.pyphysx.MaterialFlag.DISABLE_STRONG_FRICTION, True)

    local_before = [_body_state(scene.slots[index].body) for index in (0, 8)]
    scene.scene.simulate(scene.dt)
    local_reports = scene._stone_reports(scene.scene.get_contact_reports())
    local_after = [_body_state(scene.slots[index].body) for index in (0, 8)]

    c04_comparison: list[dict[str, Any]] | None = None
    truth_fill_events: list[dict[str, Any]] = []
    c29_phase4_oracle: dict[str, Any] | None = None
    settle_tail: dict[str, Any] | None = None
    if args.c04_window:
        c04_windows = _c04_windows(args.events)
        if not c04_windows:
            raise RuntimeError("--c04-window requested but no c04.dynamic_solver_frame events exist")
        expected_frames = [window["exit"] for window in c04_windows]
        expected_entries = [window["entry"] for window in c04_windows]
        local_frames = [local_after]
        # Production restores the active material only after the first
        # dynamic-dynamic Scene step has completed.
        active_material = scene.slots[0].material
        active_material.set_static_friction(0.6)
        active_material.set_dynamic_friction(0.6)
        if args.c29_phase4_active_q_oracle and len(expected_entries) < 4:
            raise RuntimeError("--c29-phase4-active-q-oracle requires four C04 entry frames")
        for index in range(1, len(expected_frames)):
            if args.c29_phase4_active_q_oracle and index == 3:
                active = scene.slots[0].body
                oracle_q = expected_entries[3][0]["q"]
                oracle_position, _current_q = active.get_global_pose()
                qx, qy, qz, qw = oracle_q
                c29_phase4_oracle = {
                    "before": _body_state(active),
                    "unityEntry": expected_entries[3][0],
                }
                c29_phase4_oracle["f32NormalizeBeforeQuaternion"] = _normalize_quaternion_f32(
                    c29_phase4_oracle["before"]["q"]
                )
                c29_phase4_oracle["unityEntryQuaternionBits"] = [
                    _f32_bits(value) for value in oracle_q
                ]
                active.set_global_pose((oracle_position, [qw, qx, qy, qz]))
                c29_phase4_oracle["afterQuaternionSet"] = _body_state(active)
            if index in truth_fill_q_indices:
                active = scene.slots[0].body
                position, _quaternion = active.get_global_pose()
                qx, qy, qz, qw = expected_entries[index][0]["q"]
                active.set_global_pose((position, [qw, qx, qy, qz]))
                truth_fill_events.append({"entryIndex": index, "kind": "active0_q"})
            if index in truth_fill_full_indices:
                for slot_index, expected in zip((0, 8), expected_entries[index]):
                    body = scene.slots[slot_index].body
                    qx, qy, qz, qw = expected["q"]
                    body.set_global_pose((expected["p"], [qw, qx, qy, qz]))
                    body.set_linear_velocity(expected["v"])
                    body.set_angular_velocity(expected["w"])
                    body.wake_up()
                truth_fill_events.append({"entryIndex": index, "kind": "both_full_pqvw"})
            if index in truth_fill_active_w_indices:
                scene.slots[0].body.set_angular_velocity(expected_entries[index][0]["w"])
                scene.slots[0].body.wake_up()
                truth_fill_events.append({"entryIndex": index, "kind": "active0_w"})
            if index in truth_fill_target_w_indices:
                scene.slots[8].body.set_angular_velocity(expected_entries[index][1]["w"])
                scene.slots[8].body.wake_up()
                truth_fill_events.append({"entryIndex": index, "kind": "target8_w"})
            scene.scene.simulate(scene.dt)
            scene.scene.get_contact_reports()
            local_frames.append([_body_state(scene.slots[index].body) for index in (0, 8)])
            if c29_phase4_oracle is not None and index == 3:
                c29_phase4_oracle["postPhase"] = local_frames[-1][0]
                c29_phase4_oracle["postPhaseComparison"] = _compare(
                    local_frames[-1][0], expected_frames[index][0]
                )
        c04_comparison = [
            {
                "frameIndex": index,
                "active": _compare(local_frames[index][0], expected_frames[index][0]),
                "target": _compare(local_frames[index][1], expected_frames[index][1]),
            }
            for index in range(len(expected_frames))
        ]
        if args.continue_after_c04_to_settle:
            settle_tail = _settle_isolated_pair(scene, max_steps=int(args.settle_max_steps))

    c05_trace: list[dict[str, Any]] | None = None
    if args.c05_window:
        call_count = _c05_call_count(args.events)
        if call_count <= 0:
            raise RuntimeError("--c05-window requested but no c05.persistent_pcm_call events exist")
        active_material = scene.slots[0].material
        active_material.set_static_friction(0.6)
        active_material.set_dynamic_friction(0.6)
        for _ in range(1, call_count):
            scene.scene.simulate(scene.dt)
            scene.scene.get_contact_reports()
    if args.c05_window or args.pcm_trace:
        c05_trace = list(scene.pyphysx.get_scene_pcm_trace(True))

    report = {
        "schema": "c03_same_run_dynamic_writeback_v1",
        "scope": (
            "diagnostic_only: Unity first dynamic-dynamic rigid-core pre-state is injected into a fresh local "
            "identity-preserving pair. This must not be used by production simulation."
        ),
        "diagnosticActiveFriction": float(args.active_friction),
        "diagnosticClearPhysxAngularLocks": bool(args.clear_physx_angular_locks),
        "diagnosticUnityTargetVelocityNormal": bool(args.unity_target_velocity_normal),
        "diagnosticDisableStrongFriction": bool(args.disable_strong_friction),
        "diagnosticPcmTrace": bool(args.pcm_trace),
        "diagnosticC28SolverSetupTrace": bool(args.c28_solver_setup_trace),
        "diagnosticC29Phase4ActiveQuaternionOracle": bool(args.c29_phase4_active_q_oracle),
        "diagnosticTruthFillQEntryIndices": sorted(truth_fill_q_indices),
        "diagnosticTruthFillFullEntryIndices": sorted(truth_fill_full_indices),
        "diagnosticTruthFillActiveWEntryIndices": sorted(truth_fill_active_w_indices),
        "diagnosticTruthFillTargetWEntryIndices": sorted(truth_fill_target_w_indices),
        "diagnosticContinueAfterC04ToSettle": bool(args.continue_after_c04_to_settle),
        "diagnosticEmptyTargetMultiPayload": bool(args.empty_target_multi_payload),
        "diagnosticEmptyMultiCacheAtNarrowphase": bool(args.empty_multi_cache_at_narrowphase),
        "unityCapture": {
            "events": str(args.events),
            "tickSerial": int(captured["tickSerial"]),
            "angularWriteSerial": int(captured["angularWriteSerial"]),
            "before": unity_before,
            "afterSolverSetup": unity_after,
        },
        "hybrid": {
            "before": local_before,
            "afterOneSceneStep": local_after,
            "reports": local_reports,
            "finalizerTrace": list(scene.pyphysx.get_scene_finalizer_trace(True)),
            "solveWritebackTrace": list(scene.pyphysx.get_scene_solve_writeback_trace(True)),
            "solveBlockTrace": list(scene.pyphysx.get_scene_solve_block_trace(True)),
            "solverSetupTrace": (
                list(scene.pyphysx.get_scene_solver_setup_trace(True))
                if args.c28_solver_setup_trace
                else None
            ),
            "narrowphaseTrace": (
                list(scene.pyphysx.get_scene_narrowphase_trace(True))
                if args.empty_multi_cache_at_narrowphase or args.narrowphase_trace
                else None
            ),
        },
        "comparison": {
            "input": [_compare(local_before[index], unity_before[index]) for index in range(2)],
            "postStep": [_compare(local_after[index], unity_after[index]) for index in range(2)],
            "c04Window": c04_comparison,
            "truthFillEvents": truth_fill_events,
            "endpointState": {
                "active": scene.state(0),
                "target": scene.state(8),
            },
            "c29Phase4ActiveQuaternionOracle": c29_phase4_oracle,
            "settleTail": settle_tail,
            "c05LocalPcmTrace": c05_trace,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "input": report["comparison"]["input"],
        "postStep": report["comparison"]["postStep"],
        "c04Window": c04_comparison,
        "settleTail": settle_tail,
        "c05LocalPcmTraceCount": None if c05_trace is None else len(c05_trace),
        "contacts": [
            {"pair": [row.get("stoneIndex0"), row.get("stoneIndex1")], "count": row.get("contact_count")}
            for row in local_reports
        ],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
