#!/usr/bin/env python3
"""Audit the A8 solver-body snapshot recurrence before static contact solve."""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path
from typing import Any


def f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


def angular_y(snapshot: list[dict[str, Any]]) -> float:
    return float(snapshot[0]["bodyA"]["angularVelocity"][1])


def bridge_y(data: dict[str, Any], key: str) -> float | None:
    slots = data.get(key) or []
    if not slots:
        return None
    xyz = slots[0].get("xyz")
    if not isinstance(xyz, list) or len(xyz) < 2:
        return None
    return float(xyz[1])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    for line in args.events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") != "a8.static_contact_window":
            continue
        data = event["data"]
        setter = float(data["setterWy"])
        unity_before = angular_y(data["bodyDataBefore"])
        unity_after = angular_y(data["bodyDataAfter"])
        bridge_after_setter = bridge_y(data, "bridgeAfterSetter")
        bridge_at_static_entry = bridge_y(data, "bridgeAtStaticEntry")
        local_raw = f32(f32(setter) * f32(1.0 - f32(0.05) * f32(0.01)))
        rows.append(
            {
                "tick_serial": data["tickSerial"],
                "setter_wy": setter,
                "bridge_wy_after_setter": bridge_after_setter,
                "bridge_wy_at_static_entry": bridge_at_static_entry,
                "unity_solver_body_data_wy_before_static": unity_before,
                "unity_solver_body_data_wy_after_static": unity_after,
                "local_raw_damping_wy": local_raw,
                "local_minus_unity_wy": local_raw - unity_before,
                "solver_body_data_static_delta_wy": unity_after - unity_before,
            }
        )

    first_difference = next((row for row in rows if row["local_minus_unity_wy"] != 0.0), None)
    tick_serials = [row["tick_serial"] for row in rows]
    contiguous = tick_serials == list(range(tick_serials[0], tick_serials[0] + len(tick_serials))) if tick_serials else False
    result = {
        "events": str(args.events),
        "window_count": len(rows),
        "tick_serials": tick_serials,
        "acceptance": {
            "eight_contiguous_static_windows": len(rows) == 8 and contiguous,
            "first_snapshot_difference_observed": first_difference is not None,
            "solver_body_data_unchanged_across_static_call": all(
                row["solver_body_data_static_delta_wy"] == 0.0 for row in rows
            ),
            "bridge_observed_after_setter_and_at_static_entry": bool(rows)
            and all(
                row["bridge_wy_after_setter"] is not None
                and row["bridge_wy_at_static_entry"] is not None
                for row in rows
            ),
        },
        "first_snapshot_difference": first_difference,
        "rows": rows,
        "scope": (
            "PxSolverBodyData is a pre-solver snapshot. Its before/after equality does not by itself "
            "prove that no PxSolverBody angularState changed; A0.6 remains the evidence for the tiny "
            "static writeback delta. When A9 is enabled in the same run, bridge_wy_after_setter and "
            "bridge_wy_at_static_entry delimit whether the mismatch first appears in the native bridge "
            "state itself or only while constructing the solver-body snapshot."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["acceptance"], ensure_ascii=False))
    if first_difference:
        print(json.dumps(first_difference, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
