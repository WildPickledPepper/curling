#!/usr/bin/env python3
"""Probe BESTSHOT release constants against MOTIONINFO rows.

The BESTSHOT axis mapping is recovered from Unity code. The remaining practical
constants for full-shot replay are the protocol-space release_x/release_y used
before the stone reaches the Midline trigger, plus the protocol y threshold at
which the trigger sends MOTIONINFO. This helper searches a small grid using the
exact recovered CurlingMotion kernel, so keep limits modest.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.replay_bestshot_seeded import (  # noqa: E402
    DEFAULT_MIDLINE_TRIGGER_PROTOCOL_Y,
    DEFAULT_RELEASE_X,
    DEFAULT_RELEASE_Y,
    Bestshot,
    replay_until_y,
)


REQUIRED_FIELDS = (
    "requested_v0",
    "requested_h0",
    "requested_w0",
    "motion_x",
    "motion_y",
    "motion_vx",
    "motion_vy",
    "motion_w",
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


def frange(start: float, stop: float, step: float) -> list[float]:
    values: list[float] = []
    value = start
    while value <= stop + step * 0.5:
        values.append(round(value, 10))
        value += step
    return values


def evaluate(rows: list[dict], *, release_x: float, release_y: float, stop_y: float, max_steps: int) -> dict:
    pos_errors: list[float] = []
    velocity_errors: list[float] = []
    state_errors: list[float] = []
    step_counts: list[int] = []
    for row in rows:
        state = replay_until_y(
            Bestshot(float(row["requested_v0"]), float(row["requested_h0"]), float(row["requested_w0"])),
            release_x=release_x,
            release_y=release_y,
            stop_y=stop_y,
            max_steps=max_steps,
        )
        dx = state.x - float(row["motion_x"])
        dy = state.y - float(row["motion_y"])
        dvx = state.vx - float(row["motion_vx"])
        dvy = state.vy - float(row["motion_vy"])
        dw = state.w - float(row["motion_w"])
        pos_errors.append(dx * dx + dy * dy)
        velocity_errors.append(dvx * dvx + dvy * dvy + dw * dw)
        state_errors.append(dx * dx + dy * dy + dvx * dvx + dvy * dvy + dw * dw)
        step_counts.append(state.steps)
    n = max(len(rows), 1)
    return {
        "release_x": release_x,
        "release_y": release_y,
        "stop_y": stop_y,
        "n": len(rows),
        "state_rmse": math.sqrt(sum(state_errors) / n),
        "pos_rmse": math.sqrt(sum(pos_errors) / n),
        "velocity_rmse": math.sqrt(sum(velocity_errors) / n),
        "avg_steps": sum(step_counts) / n,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--release-x-min", type=float, default=DEFAULT_RELEASE_X)
    parser.add_argument("--release-x-max", type=float, default=DEFAULT_RELEASE_X)
    parser.add_argument("--release-x-step", type=float, default=0.02)
    parser.add_argument("--release-y-min", type=float, default=DEFAULT_RELEASE_Y - 2.0)
    parser.add_argument("--release-y-max", type=float, default=DEFAULT_RELEASE_Y + 4.0)
    parser.add_argument("--release-y-step", type=float, default=0.5)
    parser.add_argument("--stop-y-min", type=float, default=DEFAULT_MIDLINE_TRIGGER_PROTOCOL_Y)
    parser.add_argument("--stop-y-max", type=float, default=DEFAULT_MIDLINE_TRIGGER_PROTOCOL_Y)
    parser.add_argument("--stop-y-step", type=float, default=0.02)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--top", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_rows(args.inputs, args.limit)
    if not rows:
        raise SystemExit("no usable rows")

    results = []
    for release_x in frange(args.release_x_min, args.release_x_max, args.release_x_step):
        for release_y in frange(args.release_y_min, args.release_y_max, args.release_y_step):
            for stop_y in frange(args.stop_y_min, args.stop_y_max, args.stop_y_step):
                results.append(
                    evaluate(
                        rows,
                        release_x=release_x,
                        release_y=release_y,
                        stop_y=stop_y,
                        max_steps=args.max_steps,
                    )
                )

    for result in sorted(results, key=lambda item: item["state_rmse"])[: args.top]:
        print(
            "state_rmse={state_rmse:.6f} pos_rmse={pos_rmse:.6f} velocity_rmse={velocity_rmse:.6f} "
            "release_x={release_x:.4f} release_y={release_y:.4f} stop_y={stop_y:.4f} "
            "n={n} avg_steps={avg_steps:.1f}".format(
                **result
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
