#!/usr/bin/env python3
"""Compare local production Newfrictionstep setters with Unity's A2 trace."""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.audit_hybrid_p6_endpoint_sixshot import install_pyphysx_extension  # noqa: E402
from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module  # noqa: E402
from tools.reverse.recovered_curling_motion import B2Vec2, STEP, newfrictionstep, unity_friction  # noqa: E402


DEFAULT_EVENTS = (
    ROOT
    / "log"
    / "20260711_a2_static_first_diff_inputs"
    / "unity_runtime_probe_20260711_232310"
    / "events.jsonl"
)
DEFAULT_SAMPLE = ROOT / "data" / "calibration" / "a2_static_first_diff_inputs_14000_20260711.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "calibration" / "a5_bestshot_production_setters_14000_20260712.json"
DEFAULT_EXTENSION = Path(r"D:\esp\tmp\curling_pyphysx_hybrid_build\lib\_pyphysx.cp38-win_amd64.pyd")


def trace_from_events(events: Path) -> list[dict[str, Any]]:
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "a0.angular_write.last_pre_pcm":
            trace = event.get("data", {}).get("a2StaticTrace")
            if isinstance(trace, list) and trace:
                return trace
    raise RuntimeError(f"missing A2 compact trace in {events}")


def max_abs(values: list[float]) -> float:
    return max(abs(float(value)) for value in values)


def f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", float(value)))[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--pyphysx-extension", type=Path, default=DEFAULT_EXTENSION)
    parser.add_argument(
        "--unity-release-p-y",
        action="store_true",
        help="diagnostic only: replace local release P.y with Unity trace row 0 P.y",
    )
    parser.add_argument(
        "--unity-release-pose",
        action="store_true",
        help="diagnostic only: replace the local pre-first-setter pose with Unity A2 row 0 P/Q",
    )
    parser.add_argument(
        "--unity-release-v-y",
        action="store_true",
        help="diagnostic only: replace local release linear Y velocity with Unity trace row 0 Y velocity",
    )
    parser.add_argument(
        "--zero-vertical-setter",
        action="store_true",
        help="diagnostic only: reproduce Unity's captured linear setter y=0 instead of preserving local fall speed",
    )
    parser.add_argument(
        "--no-setactive-refilter",
        action="store_true",
        help="diagnostic only: suppress the local reset_filtering call at release activation",
    )
    parser.add_argument(
        "--preserve-native-angular-z",
        action="store_true",
        help=(
            "diagnostic only: retain the native angular-Z bridge residual while updating Y; "
            "A9 shows Unity's setter does not clear that component."
        ),
    )
    parser.add_argument(
        "--unity-native-angular-setter-tilt-only",
        action="store_true",
        help="diagnostic only: use the A9-backed tilt-only bridge mapping for each angular setter",
    )
    parser.add_argument(
        "--unity-native-angular-setter-transfer",
        action="store_true",
        help="Rotate the custom-sliding angular setter through the current body quaternion.",
    )
    parser.add_argument(
        "--strict-c39-fixture",
        action="store_true",
        help="Use the 16-stone C39/C40 R0 scene setup, including the stationary index-8 target.",
    )
    args = parser.parse_args()

    # The full C39 fixture requires the same scalar hybrid build that owns the
    # PCM multi-cache lifecycle binding.  Import the scene only after loading
    # it, so a host conda package cannot silently change the audit's backend.
    if args.strict_c39_fixture:
        install_pyphysx_extension(args.pyphysx_extension)
    else:
        _install_hybrid_module()
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    unity = trace_from_events(args.events)
    sample = json.loads(args.sample.read_text(encoding="utf-8").splitlines()[0])
    shot = [
        float(sample["requested"]["v0"]),
        float(sample["requested"]["h0"]),
        float(sample["requested"]["w0"]),
    ]
    if args.strict_c39_fixture:
        scene = PersistentPhysxFrontHalfScene(
            stone_count=16,
            ice_mesh_mode="unity-source-once",
            ice_use_fast_midphase=True,
            emulate_unity_native_angular_setter_rotation=True,
            emulate_unity_setactive_no_sim=True,
            restore_active_friction_at_pcm_shell=True,
        )
        scene.reset_positions([0.0] * 32, settle_steps=0)
        scene.activate_stationary(8, 2.375, 5.2)
    else:
        scene = PersistentPhysxFrontHalfScene(
            stone_count=1,
            require_p4_contact_hooks=False,
            enable_stone_stone_contact_friction_override=False,
            emulate_unity_setactive_refilter=not args.no_setactive_refilter,
            emulate_unity_native_angular_setter_rotation=args.unity_native_angular_setter_transfer,
            emulate_unity_native_angular_setter_tilt_only=args.unity_native_angular_setter_tilt_only,
        )
    scene.start_bestshot(0, shot)
    if args.preserve_native_angular_z:
        slot = scene.slots[0]
        initial_w = [float(value) for value in slot.body.get_angular_velocity()]
        initial_w[2] = float(unity[0]["scriptGetter"]["angularVelocity"]["vector"][2])
        slot.body.set_angular_velocity(initial_w)
    if args.unity_release_pose:
        slot = scene.slots[0]
        q = [float(value) for value in unity[0]["q"]]
        slot.body.set_global_pose((
            [float(value) for value in unity[0]["p"]],
            [q[3], q[0], q[1], q[2]],
        ))
    elif args.unity_release_p_y:
        slot = scene.slots[0]
        p, q_wxyz = scene.pyphysx.cast_transformation(slot.body.get_global_pose())
        slot.body.set_global_pose((
            [float(p[0]), float(unity[0]["p"][1]), float(p[2])],
            q_wxyz,
        ))
    if args.unity_release_v_y:
        slot = scene.slots[0]
        velocity = [float(value) for value in slot.body.get_linear_velocity()]
        velocity[1] = float(unity[0]["v"][1])
        slot.body.set_linear_velocity(velocity)

    rows: list[dict[str, Any]] = []
    function_only_rows: list[dict[str, Any]] = []
    for index, expected in enumerate(unity[:-1]):
        local_pre = scene.state(0)
        expected_getter = expected["scriptGetter"]
        expected_pre_v = [float(value) for value in expected_getter["linearVelocity"]["vector"]]
        expected_pre_w = [float(value) for value in expected_getter["angularVelocity"]["vector"]]
        local_pre_v = [float(value) for value in local_pre["physxLinearVelocity"]]
        local_pre_w = [float(value) for value in local_pre["physxAngularVelocity"]]
        direct_speed = newfrictionstep(
            unity_friction(False, noise=float(expected["frictionNoise"])),
            B2Vec2(-expected_pre_v[2], -expected_pre_v[0]),
            expected_pre_w[1],
            STEP,
        )
        direct_setter = [f32(-direct_speed.v.y), 0.0, f32(-direct_speed.v.x)]
        direct_wy = f32(direct_speed.angle)
        function_only_rows.append(
            {
                "trace_index": index,
                "linear_delta": [
                    float(a) - float(b)
                    for a, b in zip(direct_setter, expected["linearSetter"])
                ],
                "angular_delta": direct_wy - float(expected["setterWy"]),
            }
        )
        if args.zero_vertical_setter:
            speed = newfrictionstep(
                unity_friction(False, noise=float(expected["frictionNoise"])),
                B2Vec2(float(local_pre["vx"]), float(local_pre["vy"])),
                float(local_pre["w"]),
                STEP,
            )
            slot = scene.slots[0]
            slot.body.set_linear_velocity(scene._horizontal_velocity(speed.v.x, speed.v.y, 0.0))
            if scene.emulate_unity_native_angular_setter_rotation:
                angular_setter = scene._unity_native_angular_setter_vector(slot, float(speed.angle))
            elif scene.emulate_unity_native_angular_setter_tilt_only:
                angular_setter = scene._unity_native_angular_setter_tilt_vector(slot, float(speed.angle))
            else:
                angular_setter = [
                    0.0,
                    speed.angle,
                    float(local_pre["physxAngularVelocity"][2]) if args.preserve_native_angular_z else 0.0,
                ]
            slot.body.set_angular_velocity(angular_setter)
            actual = scene.state(0)
            scene.scene.simulate(scene.dt)
            scene.scene.get_contact_reports()
        else:
            step = scene.step_custom_sliding(0, float(expected["frictionNoise"]))
            actual = step["beforeScene"]
        actual_v = [float(value) for value in actual["physxLinearVelocity"]]
        expected_v = [float(value) for value in expected["linearSetter"]]
        actual_wy = float(actual["physxAngularVelocity"][1])
        expected_wy = float(expected["setterWy"])
        dv = [float(a) - float(b) for a, b in zip(actual_v, expected_v)]
        dwy = actual_wy - expected_wy
        rows.append(
            {
                "trace_index": index,
                "tick_serial": expected["tickSerial"],
                "linear_setter_delta": dv,
                "linear_setter_max_abs": max_abs(dv),
                "angular_setter_delta": dwy,
                "pre_linear_getter_delta": [
                    float(a) - float(b) for a, b in zip(local_pre_v, expected_pre_v)
                ],
                "pre_angular_getter_delta": [
                    float(a) - float(b) for a, b in zip(local_pre_w, expected_pre_w)
                ],
                "friction_noise": float(expected["frictionNoise"]),
            }
        )

    setter_tolerance = 1.2e-7
    first_setter_difference = next(
        (
            row
            for row in rows
            if row["linear_setter_max_abs"] > setter_tolerance
            or abs(float(row["angular_setter_delta"])) > setter_tolerance
        ),
        None,
    )
    first_pre_angular_difference = next(
        (row for row in rows if max_abs(row["pre_angular_getter_delta"]) > 1.0e-12),
        None,
    )
    first_pre_yaw_difference = next(
        (row for row in rows if abs(float(row["pre_angular_getter_delta"][1])) > 1.0e-12),
        None,
    )
    first_pre_yaw_above_float32_noise = next(
        (row for row in rows if abs(float(row["pre_angular_getter_delta"][1])) > 1.0e-8),
        None,
    )
    first_function_only_difference = next(
        (
            row
            for row in function_only_rows
            if max_abs(row["linear_delta"]) != 0.0 or float(row["angular_delta"]) != 0.0
        ),
        None,
    )
    output = {
        "sample_id": int(sample["sample_id"]),
        "scope": "local start_bestshot plus production step_custom_sliding; same captured Unity friction noises; no Unity mutation",
        "bestshot": shot,
        "unity_release_p_y_override": bool(args.unity_release_p_y),
        "unity_release_pose_override": bool(args.unity_release_pose),
        "unity_release_v_y_override": bool(args.unity_release_v_y),
        "zero_vertical_setter_override": bool(args.zero_vertical_setter),
        "setActiveRefilter": not bool(args.no_setactive_refilter),
        "preserveNativeAngularZ": bool(args.preserve_native_angular_z),
        "unityNativeAngularSetterTiltOnly": bool(args.unity_native_angular_setter_tilt_only),
        "unity_native_angular_setter_transfer": bool(args.unity_native_angular_setter_transfer),
        "strict_c39_fixture": bool(args.strict_c39_fixture),
        "steps": len(rows),
        "setter_tolerance": setter_tolerance,
        "first_setter_difference": first_setter_difference,
        "first_pre_angular_getter_difference": first_pre_angular_difference,
        "first_pre_yaw_getter_difference": first_pre_yaw_difference,
        "first_pre_yaw_getter_difference_above_1e-8": first_pre_yaw_above_float32_noise,
        "last_step": rows[-1],
        "max_angular_setter_delta_row": max(
            rows, key=lambda row: abs(float(row["angular_setter_delta"]))
        ),
        "max_abs_linear_setter_delta": max(row["linear_setter_max_abs"] for row in rows),
        "max_abs_angular_setter_delta": max(abs(float(row["angular_setter_delta"])) for row in rows),
        "unity_getter_to_function_f32": {
            "first_difference": first_function_only_difference,
            "max_abs_linear_delta": max(max_abs(row["linear_delta"]) for row in function_only_rows),
            "max_abs_angular_delta": max(abs(float(row["angular_delta"])) for row in function_only_rows),
        },
        "conclusion": (
            "The function-only subtest isolates the recovered Newfrictionstep calculation: when Unity's captured "
            "getter/noise inputs are used and its output is rounded to float32 as the Rigidbody setter does, the "
            "setter must match exactly. Any production setter difference therefore originates in the local PhysX "
            "getter state fed back into the next script tick."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
