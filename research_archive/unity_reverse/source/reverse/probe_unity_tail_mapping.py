#!/usr/bin/env python3
"""Probe protocol MOTIONINFO -> recovered CurlingMotion tail mapping.

The recovered wasm formulas are intentionally exact-ish and slow in Python.
This helper runs a small number of official calibration rows to infer coarse
runtime conventions, especially position integration timestep and sign mapping.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.recovered_curling_motion import (  # noqa: E402
    BASE_FRICTION,
    STEP,
    B2Vec2,
    newfrictionstep,
)


REQUIRED_FIELDS = (
    "motion_x",
    "motion_y",
    "motion_vx",
    "motion_vy",
    "motion_w",
    "final_x",
    "final_y",
)


def read_rows(paths: list[Path], limit: int) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                if not row.get("in_play"):
                    continue
                if not all(row.get(field) is not None for field in REQUIRED_FIELDS):
                    continue
                rows.append(row)
                if len(rows) >= limit:
                    return rows
    return rows


def simulate_tail(
    row: dict,
    *,
    dt_pos: float,
    sx: int,
    sy: int,
    sw: int,
    max_steps: int,
    x_bound: float,
    y_min: float,
    y_max: float,
    speed_bound: float,
    direction_precheck: bool,
) -> tuple[float, float, int]:
    x = float(row["motion_x"])
    y = float(row["motion_y"])
    vx = sx * float(row["motion_vx"])
    vy = sy * float(row["motion_vy"])
    w = sw * float(row["motion_w"])
    if direction_precheck:
        dx = float(row["final_x"]) - x
        dy = float(row["final_y"]) - y
        if vx * dx + vy * dy <= 0.0:
            return x, y, 0

    for step in range(max_steps):
        if math.hypot(vx, vy) <= 0.01:
            return x, y, step
        # Match Unity's order: controller FixedUpdate updates velocity first,
        # then the physics step advances Rigidbody.position.
        speed = newfrictionstep(BASE_FRICTION, B2Vec2(vx, vy), w, STEP)
        vx = speed.v.x
        vy = speed.v.y
        w = speed.angle
        x += vx * dt_pos
        y += vy * dt_pos
        if (
            not math.isfinite(x)
            or not math.isfinite(y)
            or abs(x) > x_bound
            or y < y_min
            or y > y_max
        ):
            return x, y, step + 1
        if not all(math.isfinite(value) for value in (vx, vy, w)):
            return x, y, step + 1
        if math.hypot(vx, vy) > speed_bound:
            return x, y, step + 1
    return x, y, max_steps


def evaluate(
    rows: list[dict],
    dt_pos: float,
    sx: int,
    sy: int,
    sw: int,
    max_steps: int,
    x_bound: float,
    y_min: float,
    y_max: float,
    speed_bound: float,
    direction_precheck: bool,
) -> dict:
    errors: list[float] = []
    steps: list[int] = []
    for row in rows:
        x, y, step_count = simulate_tail(
            row,
            dt_pos=dt_pos,
            sx=sx,
            sy=sy,
            sw=sw,
            max_steps=max_steps,
            x_bound=x_bound,
            y_min=y_min,
            y_max=y_max,
            speed_bound=speed_bound,
            direction_precheck=direction_precheck,
        )
        errors.append(math.hypot(x - float(row["final_x"]), y - float(row["final_y"])))
        steps.append(step_count)
    rmse = math.sqrt(sum(error * error for error in errors) / max(len(errors), 1))
    return {
        "dt_pos": dt_pos,
        "sx": sx,
        "sy": sy,
        "sw": sw,
        "n": len(rows),
        "rmse": rmse,
        "mae": sum(errors) / max(len(errors), 1),
        "max": max(errors) if errors else 0.0,
        "avg_steps": sum(steps) / max(len(steps), 1),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--dt", nargs="+", type=float, default=[0.008, 0.009, 0.010, 0.011, 0.012])
    parser.add_argument("--search-signs", action="store_true")
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--x-bound", type=float, default=10.0)
    parser.add_argument("--y-min", type=float, default=-10.0)
    parser.add_argument("--y-max", type=float, default=30.0)
    parser.add_argument("--speed-bound", type=float, default=10.0)
    parser.add_argument("--direction-precheck", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_rows(args.inputs, args.limit)
    if not rows:
        raise SystemExit("no usable rows")

    sign_options = list(itertools.product([1, -1], repeat=3)) if args.search_signs else [(1, 1, 1)]
    results = []
    for dt_pos in args.dt:
        for sx, sy, sw in sign_options:
            results.append(
                evaluate(
                    rows,
                    dt_pos,
                    sx,
                    sy,
                    sw,
                    args.max_steps,
                    args.x_bound,
                    args.y_min,
                    args.y_max,
                    args.speed_bound,
                    args.direction_precheck,
                )
            )

    for result in sorted(results, key=lambda item: item["rmse"]):
        print(
            "rmse={rmse:.4f} mae={mae:.4f} max={max:.4f} "
            "dt={dt_pos:.4f} sx={sx:+d} sy={sy:+d} sw={sw:+d} avg_steps={avg_steps:.1f}".format(
                **result
            )
        )


if __name__ == "__main__":
    main()
