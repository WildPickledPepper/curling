#!/usr/bin/env python3
"""Replay one local stone-ice tick from adjacent Unity solver-body snapshots."""

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

from unity_front_half_physx import PersistentPhysxFrontHalfScene, UNITY_FIXED_TIMESTEP
from tools.reverse.recovered_curling_motion import B2Vec2, STEP, newfrictionstep, unity_friction


DEFAULT_EVENTS = (
    ROOT
    / "log"
    / "a0_static_bodydata_20260711_clean"
    / "unity_runtime_probe_20260711_212959"
    / "events.jsonl"
)
DEFAULT_OUTPUT = ROOT / "data" / "calibration" / "a1_local_one_tick_static_integration_14000_20260711.json"


def read_first_event(path: Path, event_type: str) -> dict[str, Any]:
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("type") == event_type:
            return row
    raise RuntimeError(f"missing event {event_type!r} in {path}")


def yaw(q: list[float]) -> float:
    return 2.0 * math.atan2(float(q[1]), float(q[3]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--from-row", type=int, default=-2)
    parser.add_argument(
        "--input-stage",
        choices=("prewrite", "postwrite"),
        default="postwrite",
        help="Use the Rigidbody getter state or Newfrictionstep setter state as local simulate input.",
    )
    args = parser.parse_args()

    flush = read_first_event(args.events, "a0.angular_write.before_first_stone_task")
    rows = flush["data"]["precedingStaticWritebacks"]
    source = rows[args.from_row]
    target = rows[args.from_row + 1]
    source_body = source["bodyDataBefore"][0]["bodyA"]
    target_body = target["bodyDataBefore"][0]["bodyA"]

    # The adjacent static snapshots bracket the next script tick: source pre-w
    # is the Rigidbody getter input, then Newfrictionstep writes the target-tick
    # setter value before the scene advances to target pose.
    writes = flush["data"]["lastTwoAngularWrites"]
    noises = flush["data"]["lastTwoFrictionNoises"]
    source_w = float(source_body["angularVelocity"][1])
    write = next(
        row
        for row in writes
        if abs(float(row["scriptInputs"]["angularVelocity"]["vector"][1]) - source_w) < 1e-7
    )
    noise = next(row for row in noises if row["tickSerial"] == write["tickSerial"])
    script_v = [float(value) for value in write["scriptInputs"]["linearVelocity"]["vector"]]
    script_w = [float(value) for value in write["scriptInputs"]["angularVelocity"]["vector"]]
    speed = newfrictionstep(
        unity_friction(False, noise=float(noise["value"])),
        B2Vec2(-script_v[2], -script_v[0]),
        script_w[1],
        STEP,
    )

    # SolverBodyData linear y already contains gravity for this solve phase.
    # Seed the actor's pre-sim velocity instead; simulate() applies the same gravity.
    p = [float(value) for value in source_body["body2World"]["p"]]
    q = [float(value) for value in source_body["body2World"]["q"]]
    postwrite_v = [-float(speed.v.y), 0.0, -float(speed.v.x)]
    postwrite_w = [0.0, float(speed.angle), 0.0]
    prewrite_v = [script_v[0], 0.0, script_v[2]]
    prewrite_w = [0.0, script_w[1], 0.0]
    v, w = (prewrite_v, prewrite_w) if args.input_stage == "prewrite" else (postwrite_v, postwrite_w)

    scene = PersistentPhysxFrontHalfScene(
        stone_count=1,
        require_p4_contact_hooks=False,
        enable_stone_stone_contact_friction_override=False,
    )
    slot = scene.slots[0]
    slot.shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, True)
    slot.body.set_global_pose((p, [q[3], q[0], q[1], q[2]]))
    slot.body.set_linear_velocity([v[0], 0.0, v[2]])
    slot.body.set_angular_velocity([0.0, w[1], 0.0])
    # CurlingStoneNew/Start and the recovered sliding path keep the moving
    # stone frictionless against ice until the stone-stone PCM shell.
    slot.material.set_static_friction(0.0)
    slot.material.set_dynamic_friction(0.0)
    slot.body.enable_gravity()
    slot.body.wake_up()
    slot.enabled = True
    local_pre_v = [float(value) for value in slot.body.get_linear_velocity()]
    local_pre_w = [float(value) for value in slot.body.get_angular_velocity()]
    scene.scene.simulate(UNITY_FIXED_TIMESTEP)
    scene.scene.get_contact_reports()

    local_p, local_q_wxyz = slot.body.get_global_pose()
    local_post_v = [float(value) for value in slot.body.get_linear_velocity()]
    local_post_w = [float(value) for value in slot.body.get_angular_velocity()]
    local_q = [
        float(local_q_wxyz.x),
        float(local_q_wxyz.y),
        float(local_q_wxyz.z),
        float(local_q_wxyz.w),
    ]
    expected_q = [float(value) for value in target_body["body2World"]["q"]]
    expected_p = [float(value) for value in target_body["body2World"]["p"]]
    output = {
        "purpose": "diagnostic only: local one-tick stone-ice static solve plus pose integration",
        "unityRows": {"fromTick": source["tickSerial"], "toTick": target["tickSerial"]},
        "localInputStage": args.input_stage,
        "unityEntry": {
            "p": p,
            "q": q,
            "scriptGetterV": script_v,
            "scriptGetterW": script_w,
            "frictionNoise": float(noise["value"]),
            "scriptSetterV": postwrite_v,
            "scriptSetterW": postwrite_w,
            "capturedSetterW": write["vector"],
        },
        "unityExpectedNext": {"p": expected_p, "q": expected_q, "yaw": yaw(expected_q)},
        "localNext": {
            "p": [float(value) for value in local_p],
            "q": local_q,
            "yaw": yaw(local_q),
            "preV": local_pre_v,
            "preW": local_pre_w,
            "postV": local_post_v,
            "postW": local_post_w,
        },
        "delta": {
            "position": [float(local_p[i]) - expected_p[i] for i in range(3)],
            "quaternion": [local_q[i] - expected_q[i] for i in range(4)],
            "yaw": yaw(local_q) - yaw(expected_q),
        },
        "scope": "No Unity memory write and no production simulator change. The source pose is an oracle diagnostic fixture.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
