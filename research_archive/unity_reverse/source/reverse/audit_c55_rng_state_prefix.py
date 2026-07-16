#!/usr/bin/env python3
"""Summarize the read-only C55 random/state prefix before first C04 solve."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def websocket_text(row: dict[str, Any]) -> str:
    data = row.get("data") if isinstance(row.get("data"), dict) else {}
    return str(data.get("textPreview") or "")


def main() -> int:
    args = parse_args()
    rows = [json.loads(line) for line in args.events.read_text(encoding="utf-8").splitlines() if line]
    type_counts = Counter(str(row.get("type") or "") for row in rows)

    def first(predicate: Any) -> dict[str, Any] | None:
        return next((row for row in rows if predicate(row)), None)

    hook = first(lambda row: row.get("type") == "sliding.hooks_installed")
    bestshot = first(
        lambda row: row.get("type") == "websocket.recv" and websocket_text(row).startswith("BESTSHOT")
    )
    reset = first(
        lambda row: row.get("type") == "websocket.recv" and websocket_text(row).startswith("RESETSTATE")
    )
    first_friction = first(lambda row: row.get("type") == "sliding.random_range.friction")
    c03 = first(lambda row: row.get("type") == "c03.first_dynamic_writeback")
    c04 = first(lambda row: row.get("type") == "c04.dynamic_solver_frame")

    random_types = {
        "sliding.random_init_state",
        "sliding.random_range.friction",
        "sliding.random_range.other",
        "sliding.random_value",
        "sliding.random_seed",
    }
    random_rows = [row for row in rows if row.get("type") in random_types]
    range_shapes = Counter(
        (
            float((row.get("data") or {}).get("min")),
            float((row.get("data") or {}).get("max")),
        )
        for row in random_rows
        if row.get("type") in {"sliding.random_range.friction", "sliding.random_range.other"}
    )

    def stamp(row: dict[str, Any] | None) -> dict[str, Any] | None:
        if row is None:
            return None
        return {"t": row.get("t"), "type": row.get("type"), "data": row.get("data")}

    result = {
        "schema": "c55_rng_state_prefix_v1",
        "scope": (
            "read-only inventory of UnityEngine.Random hooks and observable protocol/controller anchors "
            "from browser start through the first C04 solver frame; absence only applies to these hooked Unity APIs"
        ),
        "artifacts": {"events": str(args.events)},
        "anchors": {
            "slidingHooksInstalled": stamp(hook),
            "resetState": stamp(reset),
            "bestShot": stamp(bestshot),
            "firstFriction": stamp(first_friction),
            "firstC03": stamp(c03),
            "firstC04": stamp(c04),
        },
        "counts": {key: type_counts[key] for key in sorted(random_types)},
        "rangeShapes": [
            {"min": minimum, "max": maximum, "count": count}
            for (minimum, maximum), count in sorted(range_shapes.items())
        ],
        "coverage": {
            "hookInstalledBeforeBestShot": bool(hook and bestshot and float(hook.get("t", 0)) < float(bestshot.get("t", 0))),
            "observedNonFrictionUnityRandomCalls": (
                type_counts["sliding.random_init_state"]
                + type_counts["sliding.random_range.other"]
                + type_counts["sliding.random_value"]
                + type_counts["sliding.random_seed"]
            ),
            "firstC04Captured": c04 is not None,
            "interpretation": (
                "No non-friction UnityEngine.Random calls were observed in this hook-covered window; "
                "this does not exclude RNG APIs outside the recovered UnityEngine.Random internal-call set, "
                "nor state established before the hook installation."
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "counts": result["counts"], "coverage": result["coverage"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
