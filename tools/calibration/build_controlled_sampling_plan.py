#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a broad controlled Unity sampling plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CENTER_X = 2.375


def shot(
    rows: list[dict[str, Any]],
    label: str,
    category: str,
    v0: float,
    h0: float,
    w0: float,
    sweep: float = 0.0,
    stones: list[dict[str, float | int]] | None = None,
    notes: str = "",
) -> None:
    rows.append(
        {
            "sample_id": len(rows),
            "label": label,
            "category": category,
            "v0": v0,
            "h0": h0,
            "w0": w0,
            "sweep": sweep,
            "stones": stones or [],
            "notes": notes,
        }
    )


def build_plan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for idx in range(6):
        shot(rows, f"repeat_no_sweep_center_{idx:02d}", "repeat", 3.0, 0.0, 0.0)
    for idx in range(4):
        shot(rows, f"repeat_curl_neg_{idx:02d}", "repeat", 2.55, -1.2, -3.14)

    for v0 in (2.55, 2.85, 3.15, 3.45):
        for h0 in (-1.2, 0.0, 1.2):
            for w0 in (-3.14, 0.0, 3.14):
                label = f"free_v{v0:g}_h{h0:g}_w{w0:g}".replace("-", "m").replace(".", "p")
                shot(rows, label, "no_collision", v0, h0, w0)

    sweep_distances = (0.0, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0)
    sweep_bases = (
        ("straight", 3.0, 0.0, 0.0),
        ("negcurl", 2.55, -1.2, -3.14),
        ("poscurl", 2.55, 1.2, 3.14),
    )
    for base_label, v0, h0, w0 in sweep_bases:
        for distance in sweep_distances:
            label = f"sweep_{base_label}_s{distance:g}".replace(".", "p")
            shot(rows, label, "sweep_window", v0, h0, w0, sweep=distance)

    boundary_cases = (
        ("fast_center", 5.5, 0.0, 0.0),
        ("fast_left_neg", 4.2, -2.0, -6.0),
        ("fast_right_pos", 4.2, 2.0, 6.0),
        ("clamp_hi", 6.5, 3.0, 20.0),
        ("clamp_lo", 0.0, 0.0, 0.0),
        ("wall_left", 4.8, -3.0, 0.0),
        ("wall_right", 4.8, 3.0, 0.0),
        ("slow_curl", 1.5, 0.0, 6.0),
    )
    for label, v0, h0, w0 in boundary_cases:
        shot(rows, f"boundary_{label}", "boundary", v0, h0, w0)

    for target_y in (5.2, 6.2, 8.0):
        for v0 in (3.4, 4.0):
            shot(
                rows,
                f"collision_headon_y{target_y:g}_v{v0:g}".replace(".", "p"),
                "collision_headon",
                v0,
                0.0,
                0.0,
                stones=[{"x": CENTER_X, "y": target_y}],
            )

    glancing_cases = (
        ("left_target", CENTER_X - 0.18, 6.2, 3.6, 0.0, 0.0),
        ("right_target", CENTER_X + 0.18, 6.2, 3.6, 0.0, 0.0),
        ("left_curl_in", CENTER_X - 0.28, 6.8, 3.4, -0.2, -1.57),
        ("right_curl_in", CENTER_X + 0.28, 6.8, 3.4, 0.2, 1.57),
        ("wide_left", CENTER_X - 0.42, 5.7, 3.9, -0.35, 0.0),
        ("wide_right", CENTER_X + 0.42, 5.7, 3.9, 0.35, 0.0),
    )
    for label, tx, ty, v0, h0, w0 in glancing_cases:
        shot(rows, f"collision_glance_{label}", "collision_glancing", v0, h0, w0, stones=[{"x": tx, "y": ty}])

    double_cases = (
        ("line_two", [{"x": CENTER_X, "y": 6.2}, {"x": CENTER_X, "y": 4.9}], 4.1, 0.0, 0.0),
        ("split_left", [{"x": CENTER_X - 0.16, "y": 6.1}, {"x": CENTER_X + 0.16, "y": 5.0}], 4.2, 0.0, 0.0),
        ("split_right", [{"x": CENTER_X + 0.16, "y": 6.1}, {"x": CENTER_X - 0.16, "y": 5.0}], 4.2, 0.0, 0.0),
        ("curl_double", [{"x": CENTER_X - 0.2, "y": 6.4}, {"x": CENTER_X - 0.42, "y": 5.3}], 3.9, -0.2, -1.57),
    )
    for label, stones, v0, h0, w0 in double_cases:
        shot(rows, f"collision_double_{label}", "collision_double", v0, h0, w0, stones=stones)

    sweep_collision = (
        ("sweep_to_guard_s2", 3.0, 0.0, 0.0, 2.0, CENTER_X, 8.0),
        ("sweep_to_guard_s6", 3.0, 0.0, 0.0, 6.0, CENTER_X, 8.0),
        ("sweep_glance_s4", 3.3, -0.15, -1.57, 4.0, CENTER_X - 0.24, 6.8),
        ("sweep_glance_s8", 3.3, -0.15, -1.57, 8.0, CENTER_X - 0.24, 6.8),
    )
    for label, v0, h0, w0, sweep, tx, ty in sweep_collision:
        shot(rows, label, "collision_with_sweep", v0, h0, w0, sweep=sweep, stones=[{"x": tx, "y": ty}])

    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("config/unity_controlled_sampling_plan_20260707.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = build_plan()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} controlled samples -> {args.output}")
    print("categories", sorted({row["category"] for row in rows}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
