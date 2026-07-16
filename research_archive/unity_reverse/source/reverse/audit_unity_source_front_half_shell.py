#!/usr/bin/env python3
"""Audit Unity-source ice motion through the pre-stone-contact PCM shell.

The target stone's simulation shape is disabled only after its recorded reset
state has settled. It remains a pose/distance boundary, while the active stone
continues to use the real triangle-mesh ice. This deliberately stops before
the pyphysx dynamic-dynamic Scene path; scalar direct PCM is audited elsewhere.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.audit_persistent_scene_sequence import (  # noqa: E402
    DEFAULT_EVENTS,
    DEFAULT_SAMPLES,
    DEFAULT_TRUTH,
    _load_jsonl,
)
from tools.reverse.front_half_pcm_replay import (  # noqa: E402
    FIRST_PCM_CENTER_DISTANCE,
    event_shot_groups,
    load_jsonl,
)
from unity_front_half_physx import PersistentPhysxFrontHalfScene  # noqa: E402


DEFAULT_OUTPUT = PROJECT_ROOT / "data/calibration/unity_source_front_half_shell_audit_20260710.json"


def _norm(values: Iterable[float]) -> float:
    return math.sqrt(sum(float(value) * float(value) for value in values))


def _unity_wxyz(native_q: list[float]) -> list[float]:
    return [float(native_q[3]), float(native_q[0]), float(native_q[1]), float(native_q[2])]


def _quaternion_delta(local_wxyz: list[float], unity_xyzw: list[float]) -> float:
    target = _unity_wxyz(unity_xyzw)
    return min(
        _norm(a - b for a, b in zip(local_wxyz, target)),
        _norm(a + b for a, b in zip(local_wxyz, target)),
    )


def _yaw_delta(left: float, right: float) -> float:
    value = float(left) - float(right)
    while value > math.pi:
        value -= 2.0 * math.pi
    while value <= -math.pi:
        value += 2.0 * math.pi
    return value


def _run_to_shell_without_target_pair(
    scene: PersistentPhysxFrontHalfScene,
    active_index: int,
    shot: list[float],
    noises: list[float],
    targets: list[int],
) -> dict[str, Any]:
    """Advance the active stone only, stopping before the disabled stone pair."""
    scene.start_bestshot(active_index, shot)
    for step_index, noise in enumerate(noises, 1):
        step = scene.step_custom_sliding(active_index, noise)
        active = step["afterScene"]
        target_states = {str(index): scene.state(index) for index in targets}
        distances = {
            str(index): math.hypot(
                float(active["x"]) - float(target_states[str(index)]["x"]),
                float(active["y"]) - float(target_states[str(index)]["y"]),
            )
            for index in targets
        }
        hit_targets = [index for index in targets if distances[str(index)] <= FIRST_PCM_CENTER_DISTANCE]
        if hit_targets:
            return {
                "reachedPcmShell": True,
                "steps": step_index,
                "targetDistances": distances,
                "entranceState": active,
                "targetEntranceStates": target_states,
                "targetIndices": hit_targets,
            }
    return {"reachedPcmShell": False, "steps": len(noises)}


def audit(
    samples: list[dict[str, Any]],
    groups: list[dict[str, Any]],
    truth_rows: list[dict[str, Any]],
    *,
    progress_path: Path | None = None,
) -> dict[str, Any]:
    if not (len(samples) == len(groups) == len(truth_rows)):
        raise ValueError("sample, event, and truth counts must agree")
    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        # Scalar PhysX cannot execute BVH34 traversal. The audit preserves the
        # Unity cooking input but uses its executable BVH33 fallback for motion.
        ice_use_fast_midphase=False,
    )
    rows: list[dict[str, Any]] = []
    for seq, (sample, group, truth) in enumerate(zip(samples, groups, truth_rows)):
        active_index = int(sample["active_shot_num"])
        targets = [int(value) for value in sample.get("target_indices") or []]
        scene.reset_positions(sample["reset_position"], settle_steps=1)
        for index in targets:
            target_slot = scene.slots[index]
            target_slot.shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, False)
            target_slot.body.disable_gravity()
            target_slot.body.set_linear_velocity([0.0, 0.0, 0.0])
            target_slot.body.set_angular_velocity([0.0, 0.0, 0.0])
            target_slot.body.put_to_sleep()
        replay = _run_to_shell_without_target_pair(
            scene,
            active_index,
            [float(group["v0"]), float(group["h0"]), float(group["w0"])],
            [float(item["noise"]) for item in group.get("friction") or []],
            targets,
        )
        row: dict[str, Any] = {
            "seq": seq,
            "sampleId": sample.get("sample_id"),
            "activeIndex": active_index,
            "targetIndices": targets,
            "reachedPcmShell": bool(replay.get("reachedPcmShell")),
            "pcmShellStep": replay.get("steps"),
            "targetDistances": replay.get("targetDistances"),
        }
        if replay.get("reachedPcmShell"):
            local_active = replay["entranceState"]
            local_target = replay["targetEntranceStates"][str(targets[0])]
            unity = truth["unity_entrance_state"]
            unity_active = unity["active"]
            unity_target = unity["target"]
            row["shellState"] = {
                "localActive": local_active,
                "localTarget": local_target,
                "positionDeltaM": {
                    "active": _norm(
                        local_active["physxPosition"][i] - unity_active["nativeP"][i]
                        for i in range(3)
                    ),
                    "target": _norm(
                        local_target["physxPosition"][i] - unity_target["nativeP"][i]
                        for i in range(3)
                    ),
                },
                "quaternionDelta": {
                    "active": _quaternion_delta(local_active["quaternionWxyz"], unity_active["nativeQ"]),
                    "target": _quaternion_delta(local_target["quaternionWxyz"], unity_target["nativeQ"]),
                },
                "yawDeltaRad": {
                    "active": _yaw_delta(local_active["yaw"], unity_active["yaw"]),
                    "target": _yaw_delta(local_target["yaw"], unity_target["yaw"]),
                },
            }
        rows.append(row)
        if progress_path is not None:
            with progress_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    reached = [row for row in rows if row["reachedPcmShell"]]
    return {
        "schema": "unity_source_front_half_shell_audit_v1",
        "purpose": "P4 pre-contact motion audit with Unity mTriangles/PxMeshScale/static pose; no endpoint fitting.",
        "configuration": {
            "iceMeshMode": "unity-source-once",
            "iceMidphase": "BVH33 fallback; Unity source cooking semantics retained",
            "targetPairPolicy": "target shape disabled after recorded reset; active stone remains on triangle-mesh ice",
            "boundary": "first post-step distance <= FIRST_PCM_CENTER_DISTANCE",
            "shellThreshold": FIRST_PCM_CENTER_DISTANCE,
            "handoff": "scalar direct PCM, separately verified against Unity with exact native inputs",
        },
        "aggregate": {
            "rowCount": len(rows),
            "reachedPcmShellCount": len(reached),
            "maxActivePositionDeltaM": max(
                (row["shellState"]["positionDeltaM"]["active"] for row in reached), default=None
            ),
        },
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    truth = json.loads(DEFAULT_TRUTH.read_text(encoding="utf-8"))
    progress_path = args.output.with_suffix(".progress.jsonl")
    progress_path.unlink(missing_ok=True)
    report = audit(
        _load_jsonl(DEFAULT_SAMPLES),
        event_shot_groups(load_jsonl(DEFAULT_EVENTS)),
        truth.get("rows") or [],
        progress_path=progress_path,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "aggregate": report["aggregate"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
