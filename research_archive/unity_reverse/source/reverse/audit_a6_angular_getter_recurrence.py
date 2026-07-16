#!/usr/bin/env python3
"""Compare Unity and local angular getter recurrence just after BESTSHOT release."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_EVENTS = (
    ROOT
    / "log"
    / "20260711_a2_static_first_diff_inputs"
    / "unity_runtime_probe_20260711_232310"
    / "events.jsonl"
)
DEFAULT_SAMPLE = ROOT / "data" / "calibration" / "a2_static_first_diff_inputs_14000_20260711.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "calibration" / "a6_angular_getter_recurrence_14000_20260712.json"


def install_pyphysx_extension(extension: Path) -> None:
    """Load an isolated pyphysx build without touching the production package."""

    resolved = extension.resolve()
    if not resolved.is_file():
        raise RuntimeError(f"pyphysx extension does not exist: {resolved}")
    package = types.ModuleType("pyphysx")
    package.__path__ = []
    sys.modules["pyphysx"] = package
    spec = importlib.util.spec_from_file_location("pyphysx._pyphysx", resolved)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pyphysx extension: {resolved}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pyphysx._pyphysx"] = module
    spec.loader.exec_module(module)
    for name in dir(module):
        if not name.startswith("_"):
            setattr(package, name, getattr(module, name))


def trace_from_events(events: Path) -> list[dict[str, Any]]:
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "a0.angular_write.last_pre_pcm":
            trace = event.get("data", {}).get("a2StaticTrace")
            if isinstance(trace, list) and trace:
                return trace
    raise RuntimeError(f"missing A2 compact trace in {events}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--unity-native-angular-setter-transfer",
        action="store_true",
        help="Rotate each captured setter Vector3 through the local body quaternion before writing it.",
    )
    parser.add_argument(
        "--pyphysx-extension",
        type=Path,
        help="isolated _pyphysx.pyd to load for an A/B backend audit",
    )
    args = parser.parse_args()

    if args.pyphysx_extension is not None:
        install_pyphysx_extension(args.pyphysx_extension)
    from unity_front_half_physx import PersistentPhysxFrontHalfScene, UNITY_FIXED_TIMESTEP

    unity = trace_from_events(args.events)
    sample = json.loads(args.sample.read_text(encoding="utf-8").splitlines()[0])
    shot = [
        float(sample["requested"]["v0"]),
        float(sample["requested"]["h0"]),
        float(sample["requested"]["w0"]),
    ]
    scene = PersistentPhysxFrontHalfScene(
        stone_count=1,
        require_p4_contact_hooks=False,
        enable_stone_stone_contact_friction_override=False,
        emulate_unity_native_angular_setter_rotation=args.unity_native_angular_setter_transfer,
    )
    scene.start_bestshot(0, shot)
    slot = scene.slots[0]
    p, q_wxyz = scene.pyphysx.cast_transformation(slot.body.get_global_pose())
    slot.body.set_global_pose((
        [float(p[0]), float(unity[0]["p"][1]), float(p[2])],
        q_wxyz,
    ))

    rows: list[dict[str, Any]] = []
    for index, current in enumerate(unity[: max(0, int(args.steps))]):
        expected_next = unity[index + 1]
        slot.body.set_linear_velocity([float(value) for value in current["linearSetter"]])
        setter_wy = float(current["setterWy"])
        slot.body.set_angular_velocity(
            scene._unity_native_angular_setter_vector(slot, setter_wy)
            if args.unity_native_angular_setter_transfer
            else [0.0, setter_wy, 0.0]
        )
        scene.scene.simulate(UNITY_FIXED_TIMESTEP)
        scene.scene.get_contact_reports()
        local_wy = float(slot.body.get_angular_velocity()[1])
        unity_wy = float(expected_next["scriptGetter"]["angularVelocity"]["vector"][1])
        rows.append(
            {
                "setter_tick_serial": current["tickSerial"],
                "next_getter_tick_serial": expected_next["tickSerial"],
                "setter_wy": float(current["setterWy"]),
                "unity_next_getter_wy": unity_wy,
                "local_next_getter_wy": local_wy,
                "local_minus_unity_wy": local_wy - unity_wy,
            }
        )

    output = {
        "sample_id": int(sample["sample_id"]),
        "scope": "same Unity release P.y and same captured setters; local scalar read-only recurrence diagnostic",
        "local_angular_damping": float(slot.body.get_angular_damping()),
        "local_linear_damping": float(slot.body.get_linear_damping()),
        "unity_angular_drag": 0.05,
        "unity_native_angular_setter_transfer": bool(args.unity_native_angular_setter_transfer),
        "pyphysx_extension": (
            str(args.pyphysx_extension.resolve()) if args.pyphysx_extension is not None else "production"
        ),
        "rows": rows,
        "first_nonzero_delta": next(
            (row for row in rows if float(row["local_minus_unity_wy"]) != 0.0),
            None,
        ),
        "conclusion": (
            "If damping fields are equal but the first nonzero recurrence delta remains, the observed boundary is "
            "native integration/damping rounding rather than a missing actor/cache refresh."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
