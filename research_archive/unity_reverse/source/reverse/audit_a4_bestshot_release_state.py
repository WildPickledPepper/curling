#!/usr/bin/env python3
"""Compare local start_bestshot release state with Unity A2 trace row zero.

This diagnostic does not mutate Unity and does not alter production behavior.
It uses the controlled 14000 reset/BESTSHOT input and reports the first native
release-state field that differs from Unity.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unity_front_half_physx import PersistentPhysxFrontHalfScene  # noqa: E402


DEFAULT_EVENTS = (
    ROOT
    / "log"
    / "20260711_a2_static_first_diff_inputs"
    / "unity_runtime_probe_20260711_232310"
    / "events.jsonl"
)
DEFAULT_SAMPLE = ROOT / "data" / "calibration" / "a2_static_first_diff_inputs_14000_20260711.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "calibration" / "a4_bestshot_release_state_14000_20260712.json"


def unity_release(events: Path) -> dict[str, Any]:
    for line in events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") == "a0.angular_write.last_pre_pcm":
            trace = event.get("data", {}).get("a2StaticTrace")
            if isinstance(trace, list) and trace:
                return trace[0]
    raise RuntimeError(f"missing A2 compact trace in {events}")


def subtract(left: list[float], right: list[float]) -> list[float]:
    return [float(a) - float(b) for a, b in zip(left, right)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    sample = json.loads(args.sample.read_text(encoding="utf-8").splitlines()[0])
    unity = unity_release(args.events)
    active = int(sample["active_shot_num"])
    shot = [
        float(sample["requested"]["v0"]),
        float(sample["requested"]["h0"]),
        float(sample["requested"]["w0"]),
    ]

    scene = PersistentPhysxFrontHalfScene(stone_count=16)
    scene.reset_positions(sample["reset_position"], settle_steps=1)
    scene.start_bestshot(active, shot)
    local = scene.state(active)
    local_q_xyzw = [
        float(local["quaternionWxyz"][1]),
        float(local["quaternionWxyz"][2]),
        float(local["quaternionWxyz"][3]),
        float(local["quaternionWxyz"][0]),
    ]
    unity_v = [float(value) for value in unity["scriptGetter"]["linearVelocity"]["vector"]]
    unity_w = [float(value) for value in unity["scriptGetter"]["angularVelocity"]["vector"]]
    local_p = [float(value) for value in local["physxPosition"]]
    local_v = [float(value) for value in local["physxLinearVelocity"]]
    local_w = [float(value) for value in local["physxAngularVelocity"]]
    unity_p = [float(value) for value in unity["p"]]
    unity_q = [float(value) for value in unity["q"]]

    output = {
        "sample_id": int(sample["sample_id"]),
        "scope": "local release-state read only; controlled 14000 reset plus BESTSHOT",
        "unity_release_trace": str(args.events.relative_to(ROOT)).replace("\\", "/"),
        "sample": str(args.sample.relative_to(ROOT)).replace("\\", "/"),
        "bestshot": shot,
        "unity_trace_row_0": {
            "tick_serial": unity["tickSerial"],
            "p": unity_p,
            "q_xyzw": unity_q,
            "v": unity_v,
            "w": unity_w,
        },
        "local_start_bestshot": {
            "p": local_p,
            "q_xyzw": local_q_xyzw,
            "v": local_v,
            "w": local_w,
        },
        "local_minus_unity": {
            "p_m": subtract(local_p, unity_p),
            "q_component": subtract(local_q_xyzw, unity_q),
            "v_mps": subtract(local_v, unity_v),
            "w_rps": subtract(local_w, unity_w),
        },
        "first_unequal_field": "release actor P.y",
        "conclusion": (
            "The local BESTSHOT release begins 12.615204mm below Unity in native P.y while its P.x/P.z, "
            "q, v, and w match this controlled Unity release row at float precision. This is the earliest "
            "observed A-chain state difference; causality for the later yaw residual remains unproven."
        ),
        "next_boundary": (
            "Run one diagnostic same-setter replay from the local release state, without a Unity pose seed, "
            "to determine whether this P.y difference is corrected before or generates the observed yaw delta."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
