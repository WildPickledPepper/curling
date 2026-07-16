#!/usr/bin/env python3
"""Fit a small no-sweep endpoint residual correction.

The recovered CurlingMotion formula is kept as the reference physics.  This
script fits only a centimeter-scale endpoint correction for no-sweep,
no-collision samples.  It is meant to remove stable protocol/runtime bias, not
to hide sweep or collision errors.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.infer_unity_sample_residuals import (  # noqa: E402
    Sample,
    has_active_endpoint,
    load_samples,
    percentile,
    rms,
    tail_error,
)


FEATURE_SETS: dict[str, list[str]] = {
    "constant": ["1"],
    "action_linear": ["1", "v0", "h0", "w0", "abs_w0"],
    "action_quadratic_light": ["1", "v0", "h0", "w0", "abs_w0", "v0_w0", "h0_w0"],
    "motion_linear": ["1", "motion_speed", "motion_vx", "motion_w", "abs_motion_w"],
    "motion_quadratic_light": [
        "1",
        "motion_speed",
        "motion_vx",
        "motion_w",
        "abs_motion_w",
        "motion_w2",
        "motion_vx_motion_w",
    ],
}


@dataclass(frozen=True)
class ResidualRow:
    sample: Sample
    dx: float
    dy: float
    error: float


def feature_value(row: ResidualRow, name: str) -> float:
    sample = row.sample
    if name == "1":
        return 1.0
    if name == "v0":
        return sample.v0
    if name == "h0":
        return sample.h0
    if name == "w0":
        return sample.w0
    if name == "abs_w0":
        return abs(sample.w0)
    if name == "v0_w0":
        return sample.v0 * sample.w0
    if name == "h0_w0":
        return sample.h0 * sample.w0
    if name == "motion_speed":
        return math.hypot(sample.motion_vx, sample.motion_vy)
    if name == "motion_vx":
        return sample.motion_vx
    if name == "motion_w":
        return sample.motion_w
    if name == "abs_motion_w":
        return abs(sample.motion_w)
    if name == "motion_w2":
        return sample.motion_w * sample.motion_w
    if name == "motion_vx_motion_w":
        return sample.motion_vx * sample.motion_w
    raise KeyError(name)


def design(rows: list[ResidualRow], features: list[str]) -> np.ndarray:
    return np.array([[feature_value(row, name) for name in features] for row in rows], dtype=float)


def fit_coefficients(rows: list[ResidualRow], features: list[str], *, alpha: float) -> tuple[np.ndarray, np.ndarray]:
    x = design(rows, features)
    yx = np.array([row.dx for row in rows], dtype=float)
    yy = np.array([row.dy for row in rows], dtype=float)
    if alpha <= 0.0:
        bx = np.linalg.lstsq(x, yx, rcond=None)[0]
        by = np.linalg.lstsq(x, yy, rcond=None)[0]
        return bx, by
    lhs = x.T @ x + alpha * np.eye(x.shape[1])
    return np.linalg.solve(lhs, x.T @ yx), np.linalg.solve(lhs, x.T @ yy)


def corrected_errors(rows: list[ResidualRow], features: list[str], bx: np.ndarray, by: np.ndarray) -> list[float]:
    x = design(rows, features)
    pred_x = x @ bx
    pred_y = x @ by
    return [
        math.hypot(row.dx - float(pred_x[index]), row.dy - float(pred_y[index]))
        for index, row in enumerate(rows)
    ]


def metrics(errors: list[float]) -> dict[str, float | int | None]:
    return {
        "n": len(errors),
        "rmse": rms(errors),
        "mae": (sum(errors) / len(errors)) if errors else None,
        "p50": percentile(errors, 0.50),
        "p90": percentile(errors, 0.90),
        "max": max(errors) if errors else None,
    }


def group_key(row: ResidualRow) -> tuple[float, float, float]:
    sample = row.sample
    return (round(sample.v0, 6), round(sample.h0, 6), round(sample.w0, 6))


def grouped_cv(rows: list[ResidualRow], features: list[str], *, alpha: float) -> dict[str, Any]:
    groups: dict[tuple[float, float, float], list[ResidualRow]] = defaultdict(list)
    for row in rows:
        groups[group_key(row)].append(row)
    errors: list[float] = []
    for key, test_rows in groups.items():
        train_rows = [row for other_key, bucket in groups.items() if other_key != key for row in bucket]
        if len(train_rows) < len(features):
            continue
        bx, by = fit_coefficients(train_rows, features, alpha=alpha)
        errors.extend(corrected_errors(test_rows, features, bx, by))
    out = metrics(errors)
    out["groups"] = len(groups)
    return out


def load_residuals(paths: list[Path], *, max_steps: int) -> list[ResidualRow]:
    samples = [
        sample
        for sample in load_samples(paths)
        if not sample.sent_sweep
        and not sample.collision_observed
        and has_active_endpoint(sample)
    ]
    rows: list[ResidualRow] = []
    for sample in samples:
        error = tail_error(sample, max_steps=max_steps)
        rows.append(ResidualRow(sample=sample, dx=float(error["dx"]), dy=float(error["dy"]), error=float(error["error"])))
    return rows


def choose_model(rows: list[ResidualRow], alphas: list[float]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for name, features in FEATURE_SETS.items():
        for alpha in alphas:
            bx, by = fit_coefficients(rows, features, alpha=alpha)
            in_sample = metrics(corrected_errors(rows, features, bx, by))
            cv = grouped_cv(rows, features, alpha=alpha)
            candidates.append(
                {
                    "name": name,
                    "features": features,
                    "alpha": alpha,
                    "coefficients_dx": bx.tolist(),
                    "coefficients_dy": by.tolist(),
                    "in_sample": in_sample,
                    "grouped_cv": cv,
                }
            )
    candidates.sort(
        key=lambda item: (
            float("inf") if item["grouped_cv"]["rmse"] is None else item["grouped_cv"]["rmse"],
            len(item["features"]),
        )
    )
    return {"best": candidates[0], "candidates": candidates}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("config/unity_nosweep_residual_correction.json"))
    parser.add_argument("--report", type=Path, default=Path("data/calibration/unity_nosweep_residual_correction_report.json"))
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--alphas", nargs="+", type=float, default=[0.0, 1e-6, 1e-4, 1e-3, 1e-2, 1e-1])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = load_residuals(args.inputs, max_steps=args.max_steps)
    if not rows:
        raise SystemExit("no usable no-sweep residual rows")
    model = choose_model(rows, args.alphas)
    best = model["best"]
    baseline = metrics([row.error for row in rows])
    report = {
        "inputs": [str(path) for path in args.inputs],
        "rows": len(rows),
        "baseline": baseline,
        "best": best,
        "candidates": model["candidates"],
        "note": (
            "Corrections predict sim_minus_unity residuals. Apply by subtracting "
            "dx/dy from the recovered no-sweep endpoint."
        ),
    }
    config = {
        "mode": "no_sweep_endpoint_residual_correction",
        "source_report": str(args.report),
        "features": best["features"],
        "alpha": best["alpha"],
        "coefficients_dx": best["coefficients_dx"],
        "coefficients_dy": best["coefficients_dy"],
        "baseline_rmse_m": baseline["rmse"],
        "in_sample_rmse_m": best["in_sample"]["rmse"],
        "grouped_cv_rmse_m": best["grouped_cv"]["rmse"],
        "units": "meters",
        "apply": "endpoint_corrected = endpoint_recovered - predicted_residual",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.output.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(config, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
