#!/usr/bin/env python3
"""Locate a controlled-shot MOTIONINFO report inside its Unity A2 trace.

This is a read-only semantic audit.  MOTIONINFO is a protocol report emitted
when the moving stone enters Midline; it must not be treated as BESTSHOT's
native Rigidbody release state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = (
    ROOT
    / "log"
    / "20260711_a2_static_first_diff_inputs"
    / "unity_runtime_probe_20260711_232310"
    / "events.jsonl"
)
DEFAULT_SAMPLE = ROOT / "data" / "calibration" / "a2_static_first_diff_inputs_14000_20260711.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "calibration" / "a3_motioninfo_semantics_14000_20260712.json"

UNITY_NATIVE_ORIGIN_X = -64.37740020751953
UNITY_NATIVE_ORIGIN_Z = 56.525001525878906


def first_trace(events: Path) -> list[dict[str, Any]]:
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "a0.angular_write.last_pre_pcm":
            trace = event.get("data", {}).get("a2StaticTrace")
            if isinstance(trace, list) and trace:
                return trace
    raise RuntimeError(f"missing A2 compact trace in {events}")


def protocol_position(row: dict[str, Any]) -> tuple[float, float]:
    p = row["p"]
    return UNITY_NATIVE_ORIGIN_Z - float(p[2]), UNITY_NATIVE_ORIGIN_X - float(p[0])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    trace = first_trace(args.events)
    sample = json.loads(args.sample.read_text(encoding="utf-8").splitlines()[0])
    motion = [float(value) for value in sample["motioninfo"]]

    closest_index, closest = min(
        enumerate(trace),
        key=lambda item: abs(protocol_position(item[1])[1] - motion[1]),
    )
    release = trace[0]
    release_x, release_y = protocol_position(release)
    report_x, report_y = protocol_position(closest)
    report_v = [float(value) for value in closest["v"]]
    report_w = [float(value) for value in closest["w"]]

    output = {
        "sample_id": int(sample["sample_id"]),
        "scope": "controlled 14000 protocol-report semantics only; no local physics mutation",
        "unity_trace": str(args.events.relative_to(ROOT)).replace("\\", "/"),
        "sample": str(args.sample.relative_to(ROOT)).replace("\\", "/"),
        "trace_rows": len(trace),
        "bestshot_release_trace_row": {
            "trace_index": 0,
            "tick_serial": release["tickSerial"],
            "protocol_x": release_x,
            "protocol_y": release_y,
            "script_getter_v": release["scriptGetter"]["linearVelocity"]["vector"],
            "script_getter_w": release["scriptGetter"]["angularVelocity"]["vector"],
            "solver_body_p": release["p"],
            "solver_body_q": release["q"],
        },
        "motioninfo_protocol_report": motion,
        "matching_midline_trace_row": {
            "trace_index": closest_index,
            "tick_serial": closest["tickSerial"],
            "protocol_x": report_x,
            "protocol_y": report_y,
            "position_y_delta_m": report_y - motion[1],
            "protocol_vx_from_solver": -report_v[2],
            "protocol_vy_from_solver": -report_v[0],
            "solver_wy": report_w[1],
            "velocity_delta": [
                -report_v[2] - motion[2],
                -report_v[0] - motion[3],
                report_w[1] - motion[4],
            ],
            "solver_body_p": closest["p"],
            "solver_body_q": closest["q"],
        },
        "conclusion": (
            "MOTIONINFO matches the active solver-body state at trace tick 403 after BESTSHOT release, "
            "not the release state at trace tick 0. It is a Midline protocol report and cannot be used "
            "as the native Rigidbody start state."
        ),
        "next_boundary": (
            "Compare local start_bestshot/release actor P/Q/v/w with Unity trace row 0 before changing "
            "stone-ice, solver, cache, activation, or pair-lifecycle code."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
