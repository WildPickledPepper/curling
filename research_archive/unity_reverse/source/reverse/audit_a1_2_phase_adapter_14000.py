#!/usr/bin/env python3
"""Diagnostic no-oracle 14000 replay for Unity's split pose/solver velocity phase."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
from tools.reverse.recovered_curling_motion import B2Vec2, STEP, newfrictionstep, unity_friction
from unity_front_half_physx import PersistentPhysxFrontHalfScene


SAMPLES = ROOT / "data/calibration/front_half_pcm_samples_20260710_012534.jsonl"
EVENTS = ROOT / "log/unity_runtime_probe_20260710_012403/events.jsonl"
TRUTH = ROOT / "data/calibration/front_half_pcm_entrance_truth_20260710.json"
OUTPUT = ROOT / "data/calibration/a1_2_phase_adapter_14000_20260711.json"


def norm(values: list[float]) -> float:
    return math.sqrt(sum(float(value) * float(value) for value in values))


def yaw_delta(local: float, unity: float) -> float:
    delta = float(local) - float(unity)
    while delta > math.pi:
        delta -= 2.0 * math.pi
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    return delta


def set_raw_state(scene: PersistentPhysxFrontHalfScene, index: int, source: PersistentPhysxFrontHalfScene, source_index: int) -> None:
    src = source.slots[source_index].body
    dst = scene.slots[index].body
    position, quaternion = src.get_global_pose()
    dst.set_global_pose((list(position), [quaternion.w, quaternion.x, quaternion.y, quaternion.z]))
    dst.set_linear_velocity(list(src.get_linear_velocity()))
    dst.set_angular_velocity(list(src.get_angular_velocity()))
    dst.enable_gravity()
    dst.wake_up()


def set_postwrite_velocity(scene: PersistentPhysxFrontHalfScene, index: int, current: dict[str, Any], noise: float) -> None:
    speed = newfrictionstep(
        unity_friction(False, noise=float(noise)),
        B2Vec2(float(current["vx"]), float(current["vy"])),
        float(current["w"]),
        STEP,
    )
    slot = scene.slots[index]
    slot.body.set_linear_velocity(scene._horizontal_velocity(speed.v.x, speed.v.y, float(current["vz"])))
    slot.body.set_angular_velocity([0.0, speed.angle, 0.0])


def main() -> None:
    samples = [json.loads(line) for line in SAMPLES.read_text(encoding="utf-8").splitlines() if line.strip()]
    sample = next(row for row in samples if int(row["sample_id"]) == 14000)
    # Runtime friction groups are ordered to the controlled sample stream but
    # do not themselves carry sample_id. This is the same positional join used
    # by audit_persistent_scene_sequence.py.
    sample_index = samples.index(sample)
    group = event_shot_groups(load_jsonl(EVENTS))[sample_index]
    truth = next(row for row in json.loads(TRUTH.read_text(encoding="utf-8"))["rows"] if int(row["sample_id"]) == 14000)
    active = int(sample["active_shot_num"])
    target = int(sample["target_indices"][0])
    noises = [float(row["noise"]) for row in group["friction"]]
    shot = [float(group["v0"]), float(group["h0"]), float(group["w0"])]

    primary = PersistentPhysxFrontHalfScene(stone_count=16)
    shadow = PersistentPhysxFrontHalfScene(stone_count=1, require_p4_contact_hooks=False, enable_stone_stone_contact_friction_override=False)
    primary.reset_positions(sample["reset_position"], settle_steps=1)
    primary.start_bestshot(active, shot)
    shadow.start_bestshot(0, shot)

    first: dict[str, Any] | None = None
    for step, noise in enumerate(noises, 1):
        pre = primary.state(active)
        # Shadow starts from the same actor state, but carries no target: it is
        # only the ice solver/writeback branch for the post-write velocity.
        set_raw_state(shadow, 0, primary, active)
        shadow.slots[0].material.set_static_friction(0.0)
        shadow.slots[0].material.set_dynamic_friction(0.0)
        set_postwrite_velocity(shadow, 0, pre, noise)

        # Primary advances pose/PCM from pre-write actor velocity, matching the
        # Unity P/Q consumer phase observed in A1.1.
        primary.scene.simulate(primary.dt)
        reports = primary._stone_reports(primary.scene.get_contact_reports())
        post_pose = primary.state(active)
        shadow.scene.simulate(shadow.dt)
        shadow.scene.get_contact_reports()

        stone_reports = [
            report
            for report in reports
            if {int(report["stoneIndex0"]), int(report["stoneIndex1"])} == {active, target}
        ]
        if stone_reports:
            first = {
                "step": step,
                "prePose": pre,
                "pcmPose": post_pose,
                "reports": stone_reports,
                "shadowPost": shadow.state(0),
                "velocityTransferred": False,
            }
            break

        # Preserve primary P/Q for the next PCM pass but carry the separately
        # solved post-write velocity into the next script getter state.
        primary.slots[active].body.set_linear_velocity(list(shadow.slots[0].body.get_linear_velocity()))
        primary.slots[active].body.set_angular_velocity(list(shadow.slots[0].body.get_angular_velocity()))

    if first is None:
        raise RuntimeError("phase-adapter replay did not reach a stone-stone report")
    unity = truth["unity_entrance_state"]["active"]
    local = first["pcmPose"]
    output = {
        "purpose": "diagnostic-only no-oracle phase adapter; old v/w drives pose, new v/w drives ice solver state",
        "sampleId": 14000,
        "firstContact": first,
        "unityEntrance": unity,
        "delta": {
            "positionM": [float(local["physxPosition"][i]) - float(unity["nativeP"][i]) for i in range(3)],
            "positionNormM": norm([float(local["physxPosition"][i]) - float(unity["nativeP"][i]) for i in range(3)]),
            "yawRad": yaw_delta(float(local["yaw"]), float(unity["yaw"])),
        },
        "scope": "No Unity state injection. Shadow scene is a diagnostic adapter only and is not production code.",
    }
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
