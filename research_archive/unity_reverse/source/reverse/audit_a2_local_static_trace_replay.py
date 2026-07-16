#!/usr/bin/env python3
"""Replay the compact Unity A2 stone-ice trace through one local scalar Scene.

This is a diagnostic boundary test.  It seeds the local actor once from the
first Unity solver-body pose, then feeds only Unity's captured script velocity
setters.  It never writes Unity state and is not a production replay path.
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

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module  # noqa: E402
from unity_front_half_physx import PersistentPhysxFrontHalfScene, UNITY_FIXED_TIMESTEP  # noqa: E402


DEFAULT_EVENTS = (
    ROOT
    / "log"
    / "20260711_a2_static_first_diff_inputs"
    / "unity_runtime_probe_20260711_232310"
    / "events.jsonl"
)
DEFAULT_OUTPUT = ROOT / "data" / "calibration" / "a2_local_static_trace_replay_14000_20260711.json"


def _first_pcm_trace(events: Path) -> list[dict[str, Any]]:
    for line in events.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("type") == "a0.angular_write.last_pre_pcm":
            trace = row.get("data", {}).get("a2StaticTrace")
            if isinstance(trace, list) and trace:
                return trace
    raise RuntimeError(f"missing compact A2 trace in {events}")


def _wxyz_from_xyzw(q: list[float]) -> list[float]:
    return [float(q[3]), float(q[0]), float(q[1]), float(q[2])]


def _xyzw_from_wxyz(q: list[float]) -> list[float]:
    return [float(q[1]), float(q[2]), float(q[3]), float(q[0])]


def _max_abs(values: list[float]) -> float:
    return max((abs(float(value)) for value in values), default=0.0)


def _as_vector(value: Any, label: str) -> list[float]:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be a 3-vector")
    return [float(item) for item in value]


def _as_quaternion(value: Any, label: str) -> list[float]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{label} must be a 4-vector")
    return [float(item) for item in value]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--position-tolerance", type=float, default=1e-7)
    parser.add_argument("--quaternion-tolerance", type=float, default=1e-7)
    parser.add_argument("--velocity-tolerance", type=float, default=1e-7)
    args = parser.parse_args()
    args.events = args.events.resolve()
    args.output = args.output.resolve()

    # Keep this diagnostic on the same scalar-PCM/BVH4 production binding as
    # endpoint replay.  Importing a generic site-package pyphysx here omits
    # the SetActive/reset-filtering APIs required by the persistent scene.
    _install_hybrid_module()

    unity = _first_pcm_trace(args.events)
    if len(unity) < 2:
        raise RuntimeError("A2 trace needs at least two ticks")

    first = unity[0]
    scene = PersistentPhysxFrontHalfScene(
        stone_count=1,
        require_p4_contact_hooks=False,
        enable_stone_stone_contact_friction_override=False,
    )
    slot = scene.slots[0]
    slot.shape.set_flag(scene.pyphysx.ShapeFlag.SIMULATION_SHAPE, True)
    slot.body.set_global_pose((
        _as_vector(first["p"], "first.p"),
        _wxyz_from_xyzw(_as_quaternion(first["q"], "first.q")),
    ))
    slot.body.set_linear_velocity(_as_vector(first["v"], "first.v"))
    slot.body.set_angular_velocity(_as_vector(first["w"], "first.w"))
    slot.material.set_static_friction(0.0)
    slot.material.set_dynamic_friction(0.0)
    slot.body.enable_gravity()
    slot.body.wake_up()
    slot.enabled = True

    rows: list[dict[str, Any]] = []
    first_divergence: dict[str, Any] | None = None
    for index, current in enumerate(unity[:-1]):
        expected = unity[index + 1]
        linear_setter = _as_vector(current["linearSetter"], f"row {index}.linearSetter")
        setter_wy = float(current["setterWy"])
        slot.body.set_linear_velocity(linear_setter)
        slot.body.set_angular_velocity([0.0, setter_wy, 0.0])
        scene.scene.simulate(UNITY_FIXED_TIMESTEP)
        scene.scene.get_contact_reports()

        actual_p, actual_q_wxyz = scene.pyphysx.cast_transformation(slot.body.get_global_pose())
        actual_v = [float(value) for value in slot.body.get_linear_velocity()]
        actual_w = [float(value) for value in slot.body.get_angular_velocity()]
        expected_p = _as_vector(expected["p"], f"row {index + 1}.p")
        expected_q = _as_quaternion(expected["q"], f"row {index + 1}.q")
        expected_getter = expected.get("scriptGetter") or {}
        expected_v = _as_vector((expected_getter.get("linearVelocity") or {}).get("vector"), "expected getter v")
        expected_w = _as_vector((expected_getter.get("angularVelocity") or {}).get("vector"), "expected getter w")
        actual_q = _xyzw_from_wxyz([
            float(getattr(actual_q_wxyz, "w")),
            float(getattr(actual_q_wxyz, "x")),
            float(getattr(actual_q_wxyz, "y")),
            float(getattr(actual_q_wxyz, "z")),
        ])
        delta = {
            "p": [float(actual_p[i]) - expected_p[i] for i in range(3)],
            "q": [actual_q[i] - expected_q[i] for i in range(4)],
            "v": [actual_v[i] - expected_v[i] for i in range(3)],
            "w": [actual_w[i] - expected_w[i] for i in range(3)],
        }
        row = {
            "step": index + 1,
            "fromTick": int(current["tickSerial"]),
            "toTick": int(expected["tickSerial"]),
            "unitySetter": {"v": linear_setter, "wy": setter_wy},
            "delta": delta,
            "maxAbs": {key: _max_abs(value) for key, value in delta.items()},
        }
        rows.append(row)
        diverged = (
            row["maxAbs"]["p"] > args.position_tolerance
            or row["maxAbs"]["q"] > args.quaternion_tolerance
            or row["maxAbs"]["v"] > args.velocity_tolerance
            or row["maxAbs"]["w"] > args.velocity_tolerance
        )
        if diverged and first_divergence is None:
            first_divergence = row

    output = {
        "purpose": "A2 diagnostic: first local scalar stone-ice divergence under same-tick Unity script setters.",
        "scope": "Unity first pose is a diagnostic seed only; no Unity state is written and this is not a production path.",
        "unityEvents": str(args.events.relative_to(ROOT)),
        "traceTicks": {"first": int(unity[0]["tickSerial"]), "last": int(unity[-1]["tickSerial"]), "count": len(unity)},
        "tolerances": {
            "position": args.position_tolerance,
            "quaternion": args.quaternion_tolerance,
            "velocity": args.velocity_tolerance,
        },
        "firstDivergence": first_divergence,
        "lastRow": rows[-1] if rows else None,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({
        "traceTicks": output["traceTicks"],
        "firstDivergence": first_divergence,
        "lastRow": output["lastRow"],
    }, indent=2))


if __name__ == "__main__":
    main()
