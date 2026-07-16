#!/usr/bin/env python3
"""Compare a Wasm PhysX damping kernel with the captured Unity A6 window."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from audit_a6_angular_getter_recurrence import DEFAULT_EVENTS, trace_from_events


ROOT = Path(__file__).resolve().parents[2]
WASM = ROOT / "data" / "calibration" / "a7_wasm_angular_damping.wasm"
RUNNER = ROOT / "tools" / "reverse" / "run_a7_wasm_angular_damping.js"
OUTPUT = ROOT / "data" / "calibration" / "a7_wasm_angular_damping_14000_20260712.json"


def main() -> None:
    if not WASM.is_file():
        raise RuntimeError(f"missing Wasm kernel: {WASM}")
    unity = trace_from_events(DEFAULT_EVENTS)
    payload = {
        "angularDamping": 0.05,
        "dt": 0.01,
        "rows": [
            {"tickSerial": row["tickSerial"], "setterWy": float(row["setterWy"])}
            for row in unity[:8]
        ],
    }
    completed = subprocess.run(
        ["node", str(RUNNER), str(WASM)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    wasm_rows = json.loads(completed.stdout)["rows"]
    rows = []
    for current, expected_next, wasm_row in zip(unity[:8], unity[1:9], wasm_rows):
        unity_wy = float(expected_next["scriptGetter"]["angularVelocity"]["vector"][1])
        wasm_wy = float(wasm_row["wasmGetterWy"])
        rows.append(
            {
                "setter_tick_serial": current["tickSerial"],
                "next_getter_tick_serial": expected_next["tickSerial"],
                "setter_wy": float(current["setterWy"]),
                "unity_next_getter_wy": unity_wy,
                "wasm_next_getter_wy": wasm_wy,
                "wasm_minus_unity_wy": wasm_wy - unity_wy,
            }
        )
    result = {
        "scope": "Wasm-only reproduction of the native PhysX angular-damping kernel",
        "wasm": str(WASM),
        "rows": rows,
        "first_nonzero_delta": next(
            (row for row in rows if float(row["wasm_minus_unity_wy"]) != 0.0), None
        ),
        "interpretation": (
            "A match only validates the damping expression's Wasm rounding. "
            "It does not validate complete PhysX static solve or pose integration."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
