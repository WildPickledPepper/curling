#!/usr/bin/env python3
"""Persist tick progress for the P4 Unity-source scalar Scene diagnostic."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse import audit_persistent_scene_sequence as audit
from tools.reverse.front_half_pcm_replay import FIRST_PCM_CENTER_DISTANCE, event_shot_groups, load_jsonl
from unity_front_half_physx import PersistentPhysxFrontHalfScene


OUTPUT = PROJECT_ROOT / "data/calibration/scalar_source_scene_progress_14000_20260710.jsonl"


def main() -> int:
    sample = audit._load_jsonl(audit.DEFAULT_SAMPLES)[0]
    group = event_shot_groups(load_jsonl(audit.DEFAULT_EVENTS))[0]
    with OUTPUT.open("w", encoding="utf-8") as handle:
        def emit(row: dict[str, object]) -> None:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()

        emit({"phase": "start"})
        scene = PersistentPhysxFrontHalfScene(
            stone_count=16,
            ice_mesh_mode="unity-source-once",
            ice_use_fast_midphase=False,
        )
        emit({"phase": "scene-created"})
        scene.reset_positions(sample["reset_position"], settle_steps=1)
        emit({"phase": "reset"})
        target_index = int((sample.get("target_indices") or [8])[0])
        target_slot = scene.slots[target_index]
        target_slot.shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, False)
        target_slot.body.disable_gravity()
        target_slot.body.set_linear_velocity([0.0, 0.0, 0.0])
        target_slot.body.set_angular_velocity([0.0, 0.0, 0.0])
        target_slot.body.put_to_sleep()
        emit({"phase": "target-shape-disabled", "targetIndex": target_index})
        scene.start_bestshot(
            int(sample["active_shot_num"]),
            [float(group["v0"]), float(group["h0"]), float(group["w0"])],
        )
        emit({"phase": "motion-started"})
        for step, item in enumerate(group["friction"], 1):
            row = scene.step_custom_sliding(int(sample["active_shot_num"]), float(item["noise"]))
            active = row["afterScene"]
            target = scene.state(target_index)
            distance = (
                (float(active["x"]) - float(target["x"])) ** 2
                + (float(active["y"]) - float(target["y"])) ** 2
            ) ** 0.5
            if step % 25 == 0:
                emit({
                    "phase": "tick",
                    "step": step,
                    "distance": distance,
                    "active": [
                        active["x"], active["y"], active["yaw"],
                        active["vx"], active["vy"], active["w"],
                    ],
                })
            if distance <= FIRST_PCM_CENTER_DISTANCE:
                emit({
                    "phase": "pcm-shell",
                    "step": step,
                    "distance": distance,
                    "active": active,
                    "target": target,
                })
                break
        else:
            emit({"phase": "completed-without-shell", "steps": len(group["friction"])})
    print(json.dumps({"output": str(OUTPUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
