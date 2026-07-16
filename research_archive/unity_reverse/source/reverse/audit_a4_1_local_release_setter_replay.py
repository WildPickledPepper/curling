#!/usr/bin/env python3
"""Replay Unity A2 setters from the unmodified local BESTSHOT release state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unity_front_half_physx import PersistentPhysxFrontHalfScene, UNITY_FIXED_TIMESTEP  # noqa: E402


DEFAULT_EVENTS = (
    ROOT
    / "log"
    / "20260711_a2_static_first_diff_inputs"
    / "unity_runtime_probe_20260711_232310"
    / "events.jsonl"
)
DEFAULT_SAMPLE = ROOT / "data" / "calibration" / "a2_static_first_diff_inputs_14000_20260711.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "calibration" / "a4_1_local_release_setter_replay_14000_20260712.json"


def trace_from_events(events: Path) -> list[dict[str, Any]]:
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "a0.angular_write.last_pre_pcm":
            trace = event.get("data", {}).get("a2StaticTrace")
            if isinstance(trace, list) and trace:
                return trace
    raise RuntimeError(f"missing A2 compact trace in {events}")


def xyzw_from_wxyz(q: list[float]) -> list[float]:
    return [float(q[1]), float(q[2]), float(q[3]), float(q[0])]


def absmax(values: list[float]) -> float:
    return max(abs(float(value)) for value in values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

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
    )
    scene.start_bestshot(0, shot)
    slot = scene.slots[0]
    release_state = scene.state(0)

    rows: list[dict[str, Any]] = []
    for index, current in enumerate(unity[:-1]):
        expected = unity[index + 1]
        slot.body.set_linear_velocity([float(value) for value in current["linearSetter"]])
        slot.body.set_angular_velocity([0.0, float(current["setterWy"]), 0.0])
        scene.scene.simulate(UNITY_FIXED_TIMESTEP)
        scene.scene.get_contact_reports()
        actual_p, actual_q_wxyz = scene.pyphysx.cast_transformation(slot.body.get_global_pose())
        actual_v = [float(value) for value in slot.body.get_linear_velocity()]
        actual_w = [float(value) for value in slot.body.get_angular_velocity()]
        dp = [float(a) - float(b) for a, b in zip(actual_p, expected["p"])]
        actual_q = xyzw_from_wxyz([
            float(getattr(actual_q_wxyz, "w")),
            float(getattr(actual_q_wxyz, "x")),
            float(getattr(actual_q_wxyz, "y")),
            float(getattr(actual_q_wxyz, "z")),
        ])
        dq = [float(a) - float(b) for a, b in zip(actual_q, expected["q"])]
        dv = [float(a) - float(b) for a, b in zip(actual_v, expected["v"])]
        dw = [float(a) - float(b) for a, b in zip(actual_w, expected["w"])]
        rows.append(
            {
                "trace_index": index + 1,
                "tick_serial": expected["tickSerial"],
                "p_max_abs": absmax(dp),
                "q_max_abs": absmax(dq),
                "v_max_abs": absmax(dv),
                "w_max_abs": absmax(dw),
                "dp": dp,
                "dq": dq,
                "dw": dw,
            }
        )

    first_q_above_ulp = next((row for row in rows if row["q_max_abs"] > 1.2e-7), None)
    output = {
        "sample_id": int(sample["sample_id"]),
        "scope": "diagnostic local scalar replay from unmodified local start_bestshot; same Unity setters; no Unity mutation",
        "bestshot": shot,
        "steps": len(rows),
        "release_p_y_delta_m": float(release_state["physxPosition"][1]) - float(unity[0]["p"][1]),
        "first_step": rows[0],
        "first_quaternion_delta_above_float32_ulp": first_q_above_ulp,
        "last_step": rows[-1],
        "max_abs": {
            "p_m": max(row["p_max_abs"] for row in rows),
            "q_component": max(row["q_max_abs"] for row in rows),
            "v_mps": max(row["v_max_abs"] for row in rows),
            "w_rps": max(row["w_max_abs"] for row in rows),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
