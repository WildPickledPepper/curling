#!/usr/bin/env python3
"""Audit the first same-phase 14000 ContactBuffer against Unity raw state."""

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
OUTPUT = PROJECT_ROOT / "data/calibration/p5_14000_contactbuffer_audit_20260711.json"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _yaw(quaternion: dict[str, float] | list[float]) -> float:
    if isinstance(quaternion, dict):
        return 2.0 * math.atan2(float(quaternion["y"]), float(quaternion["w"]))
    return 2.0 * math.atan2(float(quaternion[1]), float(quaternion[3]))


def _sq(left: list[float], right: list[float]) -> float:
    return sum((float(a) - float(b)) ** 2 for a, b in zip(left, right))


def _score(local: dict[str, Any], unity: dict[str, Any]) -> float:
    local_frames = [local["body_frame0"]["p"], local["body_frame1"]["p"]]
    desc = unity["contactDesc"]
    unity_frames = [desc["bodyFrame0"]["p"], desc["bodyFrame1"]["p"]]
    return min(
        _sq(local_frames[0], unity_frames[0]) + _sq(local_frames[1], unity_frames[1]),
        _sq(local_frames[0], unity_frames[1]) + _sq(local_frames[1], unity_frames[0]),
    )


def _first_unity_friction(row: dict[str, Any]) -> dict[str, Any]:
    for extra in row.get("extraConstraintDumps") or []:
        rows = (extra.get("decodedConstraint") or {}).get("frictionRows") or []
        if rows:
            return dict(rows[0])
    raise ValueError("missing decoded Unity friction row")


def _best_contact_pairs(
    unity: list[dict[str, Any]], local: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    remaining = set(range(len(local)))
    pairs = []
    for unity_point in unity:
        index = min(
            remaining,
            key=lambda candidate: _sq(unity_point["point"], local[candidate]["point"]),
        )
        remaining.remove(index)
        local_point = local[index]
        pairs.append(
            {
                "unityPoint": unity_point["point"],
                "localPoint": local_point["point"],
                "delta": [
                    float(local_point["point"][axis]) - float(unity_point["point"][axis])
                    for axis in range(3)
                ],
                "unitySeparation": unity_point["separation"],
                "localSeparation": local_point["separation"],
            }
        )
    return pairs


def main() -> int:
    _install_hybrid_module()
    from tools.reverse import audit_persistent_scene_sequence as sequence
    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    sample = _load_jsonl(SAMPLES)[0]
    group = event_shot_groups(load_jsonl(EVENTS))[0]
    unity_rows = json.loads(UNITY_SOLVER.read_text(encoding="utf-8"))["stoneStoneRows"]
    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
    )
    scene.pyphysx.clear_scene_finalizer_trace()
    scene.pyphysx.set_scene_finalizer_trace_enabled(True)
    scene.reset_positions(sample["reset_position"], settle_steps=1)
    scene.run_bestshot_to_first_contact(
        int(sample["active_shot_num"]),
        [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        [float(item["noise"]) for item in group["friction"]],
        target_indices=[int((sample.get("target_indices") or [])[0])],
        max_steps=len(group["friction"]),
    )
    scene.scene.simulate(scene.dt)
    scene.scene.get_contact_reports()
    local_rows = list(scene.pyphysx.get_scene_finalizer_trace(True))
    scene.pyphysx.set_scene_finalizer_trace_enabled(False)
    local = min(
        (row for row in local_rows if int(row.get("contact_count") or 0) == 2),
        key=lambda row: min(_score(row, unity) for unity in unity_rows),
    )
    unity = min(unity_rows, key=lambda row: _score(local, row))
    desc = unity["contactDesc"]
    unity_contacts = (unity.get("contactBuffer") or {}).get("candidate", {}).get("contactsPreview") or []
    local_contacts = local.get("contacts") or []
    unity_friction = _first_unity_friction(unity)
    local_friction = (local.get("friction_rows") or [None])[0]
    report = {
        "schema": "p5_14000_contactbuffer_audit_v1",
        "purpose": "Prove whether the 14000 tangent difference exists before solver writeback.",
        "policy": "no Unity re-sampling; no pose/cache/post-collision oracle injection",
        "match": {
            "unityStoneStoneRowIndex": unity_rows.index(unity),
            "unityTimestamp": unity.get("t"),
            "localFinalizerSequence": local.get("sequence"),
            "framePositionSquaredError": _score(local, unity),
        },
        "entranceYaw": {
            "unityActive": _yaw(desc["bodyFrame0"]["q"]),
            "localActive": _yaw(local["data1"]["body2world"]["q"]),
            "unityTarget": _yaw(desc["bodyFrame1"]["q"]),
            "localTarget": _yaw(local["data0"]["body2world"]["q"]),
        },
        "contactPairs": _best_contact_pairs(unity_contacts, local_contacts),
        "firstFrictionRow": {
            "unity": unity_friction,
            "local": local_friction,
            "targetVelocityDelta": None
            if local_friction is None
            else float(local_friction["target_velocity"]) - float(unity_friction["targetVel"]),
        },
    }
    report["entranceYaw"]["activeDelta"] = report["entranceYaw"]["localActive"] - report["entranceYaw"]["unityActive"]
    report["entranceYaw"]["targetDelta"] = report["entranceYaw"]["localTarget"] - report["entranceYaw"]["unityTarget"]
    report["conclusion"] = (
        "If position is equal while contact points differ, the mismatch is generated before "
        "Dy::SolverContactFriction and cannot be repaired by friction or writeback tuning."
    )
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT),
        "match": report["match"],
        "entranceYaw": report["entranceYaw"],
        "contactPairs": report["contactPairs"],
        "frictionTargetVelocityDelta": report["firstFrictionRow"]["targetVelocityDelta"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
