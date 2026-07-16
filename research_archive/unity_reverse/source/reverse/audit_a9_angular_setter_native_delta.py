#!/usr/bin/env python3
"""Summarize observable native Rigidbody mutations made by A9 setter hooks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def matches_setter(value: Any, setter: float) -> bool:
    return isinstance(value, (int, float)) and abs(float(value) - setter) <= 1.0e-9


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    for line in args.events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") != "a9.angular_setter_native_delta":
            continue
        data = event["data"]
        setter_wy = float(data["setterWy"])
        ranges = data.get("changedRanges") or []
        target_deltas = data.get("targetDeltas") or []
        target_setter_matches = [
            {"ptr": target.get("ptr"), "offset": item.get("f32WordOffset")}
            for target in target_deltas
            for item in target.get("changedRanges", [])
            if matches_setter(item.get("afterF32"), setter_wy)
        ]
        rows.append(
            {
                "tick_serial": data.get("tickSerial"),
                "angular_write_serial": data.get("angularWriteSerial"),
                "setter_wy": setter_wy,
                "body_native_ptr": data.get("bodyNativePtr"),
                "changed_range_count": len(ranges),
                "ranges": ranges,
                "target_delta_count": len(target_deltas),
                "target_deltas": target_deltas,
                "target_changed_word_equal_to_setter_wy": target_setter_matches,
                "changed_word_equal_to_setter_wy": [
                    item["f32WordOffset"]
                    for item in ranges
                    if matches_setter(item.get("afterF32"), setter_wy)
                ],
            }
        )

    result = {
        "events": str(args.events),
        "window_count": len(rows),
        "acceptance": {
            "setter_native_deltas_captured": bool(rows),
            "all_calls_mutated_observable_native_window": bool(rows)
            and all(
                row["changed_range_count"] > 0 or row["target_delta_count"] > 0
                for row in rows
            ),
            "any_pointer_target_mutated": any(row["target_delta_count"] > 0 for row in rows),
            "any_pointer_target_word_equals_setter_wy": any(
                row["target_changed_word_equal_to_setter_wy"] for row in rows
            ),
            "any_changed_word_equals_setter_wy": any(
                row["changed_word_equal_to_setter_wy"] for row in rows
            ),
        },
        "rows": rows,
        "scope": (
            "This is a byte-delta audit of Unity's native Rigidbody object during the actual "
            "set_angularVelocity call. It intentionally does not infer a PxsBodyCore layout or "
            "claim that any changed offset is the solver body."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["acceptance"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
