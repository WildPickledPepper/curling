#!/usr/bin/env python3
"""Fit a small empirical BESTSHOT -> MOTIONINFO probe.

This is not meant to replace the recovered Unity physics. It is a quick
diagnostic for how much of the release-to-middle-line mapping can be explained
from official calibration rows before deeper Unity release-state recovery.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


TARGETS = (
    "motion_x",
    "motion_y",
    "motion_vx",
    "motion_vy",
    "motion_w",
    "final_x",
    "final_y",
)


def features(v0: float, h0: float, w0: float) -> list[float]:
    return [
        1.0,
        v0,
        h0,
        w0,
        v0 * w0,
        h0 * w0,
        w0 * w0,
        v0 * v0,
        h0 * h0,
    ]


def read_rows(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if not row.get("in_play"):
                continue
            if not all(row.get(name) is not None for name in TARGETS):
                continue
            rows.append(row)
    return rows


def fit_target(matrix: np.ndarray, values: np.ndarray) -> tuple[np.ndarray, float, float]:
    coefficients, *_ = np.linalg.lstsq(matrix, values, rcond=None)
    prediction = matrix @ coefficients
    errors = prediction - values
    rmse = math.sqrt(float(np.mean(errors * errors)))
    mae = float(np.mean(np.abs(errors)))
    return coefficients, rmse, mae


def describe_ratio(name: str, values: list[float]) -> None:
    array = np.array(values, dtype=float)
    print(
        f"{name}: mean={array.mean():.6f} std={array.std():.6f} "
        f"min={array.min():.6f} max={array.max():.6f}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_rows(args.input)
    if not rows:
        raise SystemExit("no usable rows")

    matrix = np.array(
        [
            features(
                float(row["requested_v0"]),
                float(row["requested_h0"]),
                float(row["requested_w0"]),
            )
            for row in rows
        ],
        dtype=float,
    )

    print(f"rows={len(rows)}")
    print("features=1,v0,h0,w0,v0*w0,h0*w0,w0*w0,v0*v0,h0*h0")
    for target in TARGETS:
        values = np.array([float(row[target]) for row in rows], dtype=float)
        coefficients, rmse, mae = fit_target(matrix, values)
        shown = ",".join(f"{value:.6g}" for value in coefficients[:5])
        print(f"{target}: rmse={rmse:.6f} mae={mae:.6f} coef_prefix={shown}")

    describe_ratio("motion_x_minus_h0", [row["motion_x"] - row["requested_h0"] for row in rows])
    describe_ratio(
        "motion_vx_over_w0",
        [
            row["motion_vx"] / row["requested_w0"]
            for row in rows
            if abs(row["requested_w0"]) > 1e-9
        ],
    )
    describe_ratio(
        "motion_w_over_w0",
        [
            row["motion_w"] / row["requested_w0"]
            for row in rows
            if abs(row["requested_w0"]) > 1e-9
        ],
    )
    describe_ratio("motion_vy_over_v0", [row["motion_vy"] / row["requested_v0"] for row in rows])


if __name__ == "__main__":
    main()
