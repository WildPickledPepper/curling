#!/usr/bin/env python3
"""Replay the eight A12 setter ticks and compare local pose to Unity bridge pose.

This is deliberately narrow: it seeds only the first Unity solver-body pose,
uses the captured per-tick horizontal velocity and angular setter value, then
checks whether local pose integration produces the next Unity body2World.
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

from unity_front_half_physx import PersistentPhysxFrontHalfScene, UNITY_FIXED_TIMESTEP


def yaw(q: list[float]) -> float:
    return 2.0 * math.atan2(float(q[1]), float(q[3]))


def body_a(data: dict[str, Any]) -> dict[str, Any]:
    snapshots = data.get("bodyDataBefore") or []
    if not snapshots:
        raise RuntimeError("A8 event is missing bodyDataBefore")
    return snapshots[0]["bodyA"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--unity-native-angular-setter-transfer",
        action="store_true",
        help="Use the local diagnostic mirror of Unity's native setter rotation.",
    )
    args = parser.parse_args()

    unity_rows: list[dict[str, Any]] = []
    for line in args.events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "a8.static_contact_window":
            unity_rows.append(event["data"])
    unity_rows.sort(key=lambda row: int(row["tickSerial"]))
    if len(unity_rows) < 2:
        raise RuntimeError("need at least two A8 static-window rows")

    first = body_a(unity_rows[0])
    first_pose = first["body2World"]
    scene = PersistentPhysxFrontHalfScene(
        stone_count=1,
        require_p4_contact_hooks=False,
        enable_stone_stone_contact_friction_override=False,
        emulate_unity_native_angular_setter_rotation=args.unity_native_angular_setter_transfer,
    )
    slot = scene.slots[0]
    slot.shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, True)
    q = [float(value) for value in first_pose["q"]]
    p = [float(value) for value in first_pose["p"]]
    slot.body.set_global_pose((p, [q[3], q[0], q[1], q[2]]))
    slot.material.set_static_friction(0.0)
    slot.material.set_dynamic_friction(0.0)
    slot.body.enable_gravity()
    slot.body.wake_up()
    slot.enabled = True

    rows: list[dict[str, Any]] = []
    for current, expected_row in zip(unity_rows[:-1], unity_rows[1:]):
        source_body = body_a(current)
        expected_body = body_a(expected_row)
        source_linear = [float(value) for value in source_body["linearVelocity"]]
        setter_wy = float(current["setterWy"])
        _before_p, before_q = scene.pyphysx.cast_transformation(slot.body.get_global_pose())
        local_q_before_setter = [
            float(before_q.x),
            float(before_q.y),
            float(before_q.z),
            float(before_q.w),
        ]
        slot.body.set_linear_velocity([source_linear[0], 0.0, source_linear[2]])
        vector = (
            scene._unity_native_angular_setter_vector(slot, setter_wy)
            if args.unity_native_angular_setter_transfer
            else [0.0, setter_wy, 0.0]
        )
        slot.body.set_angular_velocity(vector)
        scene.scene.simulate(UNITY_FIXED_TIMESTEP)
        scene.scene.get_contact_reports()
        local_p, local_q = scene.pyphysx.cast_transformation(slot.body.get_global_pose())
        local_v = [float(value) for value in slot.body.get_linear_velocity()]
        local_w = [float(value) for value in slot.body.get_angular_velocity()]
        local_q_xyzw = [float(local_q.x), float(local_q.y), float(local_q.z), float(local_q.w)]
        local_p_xyz = [float(value) for value in local_p]
        expected_pose = expected_body["body2World"]
        expected_q = [float(value) for value in expected_pose["q"]]
        expected_p = [float(value) for value in expected_pose["p"]]
        rows.append(
            {
                "from_tick": int(current["tickSerial"]),
                "to_tick": int(expected_row["tickSerial"]),
                "setter_wy": setter_wy,
                "setter_vector": vector,
                "local_q_before_setter": local_q_before_setter,
                "unity_q_before_setter": [float(value) for value in source_body["body2World"]["q"]],
                "local_q": local_q_xyzw,
                "unity_q": expected_q,
                "local_minus_unity_q": [local_q_xyzw[i] - expected_q[i] for i in range(4)],
                "local_yaw_minus_unity": yaw(local_q_xyzw) - yaw(expected_q),
                "local_p": local_p_xyz,
                "unity_p": expected_p,
                "local_minus_unity_p": [local_p_xyz[i] - expected_p[i] for i in range(3)],
                "local_v": local_v,
                "unity_v": [float(value) for value in expected_body["linearVelocity"]],
                "local_minus_unity_v": [
                    local_v[i] - float(expected_body["linearVelocity"][i]) for i in range(3)
                ],
                "local_w": local_w,
                "unity_w": [float(value) for value in expected_body["angularVelocity"]],
                "local_minus_unity_w": [
                    local_w[i] - float(expected_body["angularVelocity"][i]) for i in range(3)
                ],
            }
        )

    first_q_difference = next((row for row in rows if any(value != 0.0 for value in row["local_minus_unity_q"])), None)
    output = {
        "events": str(args.events),
        "unity_native_angular_setter_transfer": bool(args.unity_native_angular_setter_transfer),
        "first_q_difference": first_q_difference,
        "rows": rows,
        "scope": (
            "The first Unity body2World is a diagnostic seed. This tests whether the local scene's next pose "
            "matches the next captured Unity body2World when both use the observed release-tick setters."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"first_q_difference": first_q_difference}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
