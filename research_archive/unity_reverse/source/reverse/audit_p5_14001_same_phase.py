#!/usr/bin/env python3
"""Compare the first same-phase 14001 finalizer without Unity re-sampling."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module


SAMPLES = PROJECT_ROOT / "data/calibration/front_half_pcm_samples_20260710_012534.jsonl"
EVENTS = PROJECT_ROOT / "log/unity_runtime_probe_20260710_012403/events.jsonl"
UNITY_SOLVER = PROJECT_ROOT / "data/calibration/front_half_pcm_solver_state_20260710.json"
OUTPUT = PROJECT_ROOT / "data/calibration/p5_14001_same_phase_audit_20260711.json"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _yaw_from_xyzw(quaternion: dict[str, float] | list[float]) -> float:
    if isinstance(quaternion, dict):
        return 2.0 * math.atan2(float(quaternion["y"]), float(quaternion["w"]))
    return 2.0 * math.atan2(float(quaternion[1]), float(quaternion[3]))


def _distance_sq(left: list[float], right: list[float]) -> float:
    return sum((float(a) - float(b)) ** 2 for a, b in zip(left, right))


def _phase_score(local: dict[str, Any], unity: dict[str, Any]) -> float:
    local_frames = [local["body_frame0"]["p"], local["body_frame1"]["p"]]
    desc = unity["contactDesc"]
    unity_frames = [desc["bodyFrame0"]["p"], desc["bodyFrame1"]["p"]]
    forward = _distance_sq(local_frames[0], unity_frames[0]) + _distance_sq(local_frames[1], unity_frames[1])
    reverse = _distance_sq(local_frames[0], unity_frames[1]) + _distance_sq(local_frames[1], unity_frames[0])
    return min(forward, reverse)


def _first_unity_friction_row(row: dict[str, Any]) -> dict[str, Any]:
    for extra in row.get("extraConstraintDumps") or []:
        decoded = extra.get("decodedConstraint") or {}
        rows = decoded.get("frictionRows") or []
        if rows:
            return dict(rows[0])
    raise ValueError("matched Unity finalizer has no decoded friction row")


def main() -> int:
    _install_hybrid_module()
    from tools.reverse import audit_persistent_scene_sequence as sequence
    from tools.reverse.audit_hybrid_p6_endpoint_sixshot import _settle
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    samples = _load_jsonl(SAMPLES)
    groups = event_shot_groups(load_jsonl(EVENTS))
    unity_rows = json.loads(UNITY_SOLVER.read_text(encoding="utf-8"))["stoneStoneRows"]
    if int(samples[1]["sample_id"]) != 14001:
        raise ValueError("expected sample 14001 at sequence 1")

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
    )
    local_finalizers: list[dict[str, Any]] = []
    local_writebacks: list[dict[str, Any]] = []
    for seq in (0, 1):
        sample, group = samples[seq], groups[seq]
        active_index = int(sample["active_shot_num"])
        target_index = int((sample.get("target_indices") or [])[0])
        scene.reset_positions(sample["reset_position"], settle_steps=1)
        if seq == 1:
            scene.pyphysx.clear_scene_finalizer_trace()
            scene.pyphysx.clear_scene_solve_writeback_trace()
            scene.pyphysx.set_scene_finalizer_trace_enabled(True)
            scene.pyphysx.set_scene_solve_writeback_trace_enabled(True)
        replay = scene.run_bestshot_to_first_contact(
            active_index,
            [float(group["v0"]), float(group["h0"]), float(group["w0"])],
            [float(item["noise"]) for item in group["friction"]],
            target_indices=[target_index],
            max_steps=len(group["friction"]),
        )
        scene.scene.simulate(scene.dt)
        scene.scene.get_contact_reports()
        if seq == 0:
            _settle(scene)
        else:
            local_finalizers = list(scene.pyphysx.get_scene_finalizer_trace(True))
            local_writebacks = list(scene.pyphysx.get_scene_solve_writeback_trace(True))
            scene.pyphysx.set_scene_finalizer_trace_enabled(False)
            scene.pyphysx.set_scene_solve_writeback_trace_enabled(False)

    candidates = [row for row in local_finalizers if int(row.get("contact_count") or 0) >= 2]
    if not candidates:
        raise RuntimeError("14001 replay produced no two-contact local finalizer")
    local = min(candidates, key=lambda row: min(_phase_score(row, unity) for unity in unity_rows))
    unity = min(unity_rows, key=lambda row: _phase_score(local, row))
    desc = unity["contactDesc"]

    # Local finalizer is target/body0 then active/body1; Unity is active/body0 then target/body1.
    local_target, local_active = local["data0"], local["data1"]
    unity_active, unity_target = desc["bodyFrame0"], desc["bodyFrame1"]
    unity_friction = _first_unity_friction_row(unity)
    local_friction = (local.get("friction_rows") or [None])[0]
    phase_score = _phase_score(local, unity)
    report = {
        "schema": "p5_14001_same_phase_audit_v1",
        "purpose": "Locate the earliest 14001 friction/writeback mismatch using existing Unity raw state.",
        "policy": "no Unity re-sampling; no pose/cache/post-collision oracle injection",
        "match": {
            "unityStoneStoneRowIndex": unity_rows.index(unity),
            "unityTimestamp": unity.get("t"),
            "unityPhase": unity.get("phase"),
            "localFinalizerSequence": local.get("sequence"),
            "framePositionSquaredError": phase_score,
        },
        "entranceBeforeSolver": {
            "activeYaw": {
                "unity": _yaw_from_xyzw(unity_active["q"]),
                "local": _yaw_from_xyzw(local_active["body2world"]["q"]),
            },
            "targetYaw": {
                "unity": _yaw_from_xyzw(unity_target["q"]),
                "local": _yaw_from_xyzw(local_target["body2world"]["q"]),
            },
        },
        "contact": {
            "unity": (unity.get("contactBuffer") or {}).get("candidate", {}).get("contactsPreview"),
            "local": local.get("contacts"),
        },
        "firstFrictionRow": {
            "unity": unity_friction,
            "local": local_friction,
            "targetVelocityDelta": None
            if local_friction is None
            else float(local_friction["target_velocity"]) - float(unity_friction["targetVel"]),
        },
        "localWritebacks": [
            row for row in local_writebacks if int(row.get("normal_constraint_count") or 0) >= 2
        ],
    }
    for role in ("activeYaw", "targetYaw"):
        values = report["entranceBeforeSolver"][role]
        values["delta"] = float(values["local"]) - float(values["unity"])
    report["conclusion"] = (
        "The first nonzero yaw delta at this same-phase boundary is an input to contact/friction "
        "generation. A friction-row delta observed after it must not be called an independent solver defect."
    )
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT),
        "match": report["match"],
        "yaw": report["entranceBeforeSolver"],
        "frictionTargetVelocityDelta": report["firstFrictionRow"]["targetVelocityDelta"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
