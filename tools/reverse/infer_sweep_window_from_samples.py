#!/usr/bin/env python3
"""Infer effective sweep windows from sampled Unity shots.

The recovered code says a SWEEP message turns on low friction until the moving
stone passes Midline + requested distance, capped by Hogline2.  Socket sampling
adds an extra runtime variable: the SWEEP message arrives after MOTIONINFO, so
the low-friction window may start late.

This helper keeps the recovered CurlingMotion formula fixed and searches only
the sweep-window timing/length implied by endpoint samples.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.infer_unity_sample_residuals import (  # noqa: E402
    Sample,
    has_active_endpoint,
    load_samples,
    percentile,
    rms,
)
from tools.reverse.recovered_curling_motion import (  # noqa: E402
    BASE_FRICTION,
    STEP,
    SWEEP_FRICTION,
    B2Vec2,
    newfrictionstep,
)
from tools.reverse.recovered_sweep_window import (  # noqa: E402
    MAX_SWEEP_DISTANCE,
    MIDLINE_CENTER_PROTOCOL_Y,
)


def simulate(
    sample: Sample,
    *,
    start_lag: float = 0.0,
    effective_distance: float | None = None,
    max_steps: int,
) -> tuple[float, float, int, float]:
    x = sample.motion_x
    y = sample.motion_y
    vx = sample.motion_vx
    vy = sample.motion_vy
    w = sample.motion_w

    requested = sample.sweep_distance or 0.0
    distance = requested if effective_distance is None else effective_distance
    capped = max(0.0, min(distance, MAX_SWEEP_DISTANCE))
    start_y = sample.motion_y - max(0.0, start_lag)
    end_y = MIDLINE_CENTER_PROTOCOL_Y - capped

    for step in range(max_steps):
        if math.hypot(vx, vy) <= 0.01:
            err = math.hypot(x - sample.final_x, y - sample.final_y)
            return x, y, step, err
        active_sweep = y <= start_y and y > end_y
        friction = SWEEP_FRICTION if active_sweep else BASE_FRICTION
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx = speed.v.x
        vy = speed.v.y
        w = speed.angle
        x += vx * 0.01
        y += vy * 0.01
    err = math.hypot(x - sample.final_x, y - sample.final_y)
    return x, y, max_steps, err


def golden_search(
    fn,
    left: float,
    right: float,
    *,
    iterations: int,
) -> tuple[float, float]:
    if right <= left:
        return left, fn(left)
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    inv_phi = 1.0 / phi
    c = right - (right - left) * inv_phi
    d = left + (right - left) * inv_phi
    fc = fn(c)
    fd = fn(d)
    for _ in range(iterations):
        if fc <= fd:
            right = d
            d = c
            fd = fc
            c = right - (right - left) * inv_phi
            fc = fn(c)
        else:
            left = c
            c = d
            fc = fd
            d = left + (right - left) * inv_phi
            fd = fn(d)
    value = (left + right) * 0.5
    return value, fn(value)


def fit_sample(sample: Sample, *, max_steps: int, iterations: int) -> dict[str, Any]:
    requested = float(sample.sweep_distance or 0.0)
    baseline = simulate(sample, start_lag=0.0, effective_distance=None, max_steps=max_steps)

    lag_hi = min(8.0, max(0.0, requested + 0.5))
    best_lag, best_lag_error = golden_search(
        lambda value: simulate(sample, start_lag=value, effective_distance=None, max_steps=max_steps)[3],
        0.0,
        lag_hi,
        iterations=iterations,
    )
    effective_hi = min(MAX_SWEEP_DISTANCE, max(0.0, requested))
    best_effective, best_effective_error = golden_search(
        lambda value: simulate(sample, start_lag=0.0, effective_distance=value, max_steps=max_steps)[3],
        0.0,
        effective_hi,
        iterations=iterations,
    )

    return {
        "sample_id": sample.sample_id,
        "label": sample.label,
        "requested_distance": requested,
        "baseline_error": baseline[3],
        "baseline_steps": baseline[2],
        "best_start_lag_m": best_lag,
        "best_start_lag_error": best_lag_error,
        "best_effective_distance_m": best_effective,
        "best_effective_distance_error": best_effective_error,
        "lost_distance_m": requested - best_effective,
    }


def summarize(values: list[float]) -> dict[str, float | int | None]:
    return {
        "n": len(values),
        "mean": statistics.fmean(values) if values else None,
        "rmse": rms(values),
        "p50": percentile(values, 0.50),
        "p90": percentile(values, 0.90),
        "max": max(values) if values else None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--iterations", type=int, default=7)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    samples = [
        sample
        for sample in load_samples(args.inputs)
        if sample.sent_sweep
        and sample.sweep_distance is not None
        and sample.sweep_distance > 0.0
        and not sample.collision_observed
        and has_active_endpoint(sample)
    ]
    if not samples:
        raise SystemExit("no usable sweep samples")

    rows = [fit_sample(sample, max_steps=args.max_steps, iterations=args.iterations) for sample in samples]
    summary = {
        "inputs": [str(path) for path in args.inputs],
        "n": len(rows),
        "baseline_error": summarize([row["baseline_error"] for row in rows]),
        "start_lag_error": summarize([row["best_start_lag_error"] for row in rows]),
        "effective_distance_error": summarize([row["best_effective_distance_error"] for row in rows]),
        "best_start_lag_m": summarize([row["best_start_lag_m"] for row in rows]),
        "best_effective_distance_m": summarize([row["best_effective_distance_m"] for row in rows]),
        "lost_distance_m": summarize([row["lost_distance_m"] for row in rows]),
        "rows": rows,
    }

    text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
