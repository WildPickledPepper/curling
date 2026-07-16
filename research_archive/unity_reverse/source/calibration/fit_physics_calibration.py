# -*- coding: utf-8 -*-
"""Fit official-server no-sweep landing calibration from JSONL samples."""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


FEATURES = [
    "1",
    "v",
    "h",
    "w",
    "abs_w",
    "tanh_w",
    "v2",
    "h2",
    "w2",
    "v_h",
    "v_w",
    "h_w",
]


def load_rows(path: Path) -> List[Dict[str, object]]:
    rows = []
    for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_num}: invalid JSON: {exc}") from exc
    return rows


def usable_rows(rows: Iterable[Dict[str, object]], include_out_of_play: bool = False) -> List[Dict[str, object]]:
    usable = []
    for row in rows:
        final_x = float(row.get("final_x") or 0.0)
        final_y = float(row.get("final_y") or 0.0)
        if include_out_of_play or (bool(row.get("in_play")) and final_x > 0.0 and final_y > 0.0):
            usable.append(row)
    return usable


def feature_vector(v: float, h: float, w: float) -> List[float]:
    return [
        1.0,
        v,
        h,
        w,
        abs(w),
        math.tanh(w),
        v * v,
        h * h,
        w * w,
        v * h,
        v * w,
        h * w,
    ]


def design_matrix(rows: Sequence[Dict[str, object]]) -> np.ndarray:
    return np.array(
        [
            feature_vector(
                float(row["requested_v0"]),
                float(row["requested_h0"]),
                float(row["requested_w0"]),
            )
            for row in rows
        ],
        dtype=float,
    )


def targets(rows: Sequence[Dict[str, object]]) -> np.ndarray:
    return np.array([[float(row["final_x"]), float(row["final_y"])] for row in rows], dtype=float)


def split_indices(rows: Sequence[Dict[str, object]]) -> Tuple[np.ndarray, np.ndarray]:
    train = []
    val = []
    for idx, row in enumerate(rows):
        sample_id = int(row.get("sample_id", idx))
        if sample_id % 5 == 0:
            val.append(idx)
        else:
            train.append(idx)
    if not val:
        val = train[: max(1, len(train) // 5)]
        train = train[len(val) :]
    return np.array(train, dtype=int), np.array(val, dtype=int)


def fit_coefficients(x: np.ndarray, y: np.ndarray, fit_indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    coefs = []
    preds = np.zeros_like(y)
    for target_idx in range(2):
        beta, *_ = np.linalg.lstsq(x[fit_indices], y[fit_indices, target_idx], rcond=None)
        coefs.append(beta)
        preds[:, target_idx] = x @ beta
    return np.array(coefs), preds


def metric_dict(pred: np.ndarray, y: np.ndarray, indices: np.ndarray) -> Dict[str, float]:
    err = pred[indices] - y[indices]
    total = np.sqrt(np.sum(err * err, axis=1))
    return {
        "n": int(len(indices)),
        "rmse_x": float(np.sqrt(np.mean(err[:, 0] ** 2))),
        "rmse_y": float(np.sqrt(np.mean(err[:, 1] ** 2))),
        "rmse_total": float(np.sqrt(np.mean(total * total))),
        "mae_x": float(np.mean(np.abs(err[:, 0]))),
        "mae_y": float(np.mean(np.abs(err[:, 1]))),
        "p90_total": float(np.percentile(total, 90)),
        "max_total": float(np.max(total)),
    }


def current_mock_predictions(rows: Sequence[Dict[str, object]]) -> np.ndarray:
    pred = []
    for row in rows:
        v = float(row["requested_v0"])
        h = float(row["requested_h0"])
        w = float(row["requested_w0"])
        x = 2.375 + h * 0.88 + math.tanh(w / 5.0) * 0.55
        y = 8.0 - max(0.0, min(6.0, v)) * 1.02 + abs(w) * 0.05
        pred.append([x, y])
    return np.array(pred, dtype=float)


def input_ranges(rows: Sequence[Dict[str, object]]) -> Dict[str, List[float]]:
    result = {}
    for src, dst in [
        ("requested_v0", "v0"),
        ("requested_h0", "h0"),
        ("requested_w0", "w0"),
    ]:
        values = [float(row[src]) for row in rows]
        result[dst] = [float(min(values)), float(max(values))]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Fit no-sweep official physics calibration")
    parser.add_argument("input", type=Path, help="JSONL file from dual_calibration_collector.py")
    parser.add_argument("--output", type=Path, default=Path("config/physics_calibration.json"))
    parser.add_argument("--include-out-of-play", action="store_true")
    parser.add_argument("--support-margin", type=float, default=0.15)
    args = parser.parse_args()

    rows_total = load_rows(args.input)
    rows = usable_rows(rows_total, include_out_of_play=args.include_out_of_play)
    if len(rows) < len(FEATURES) * 2:
        raise SystemExit(f"not enough usable rows: {len(rows)}")

    x = design_matrix(rows)
    y = targets(rows)
    train_idx, val_idx = split_indices(rows)

    split_coefs, split_pred = fit_coefficients(x, y, train_idx)
    all_idx = np.arange(len(rows), dtype=int)
    all_coefs, all_pred = fit_coefficients(x, y, all_idx)
    mock_pred = current_mock_predictions(rows)
    residuals = all_pred - y

    report = {
        "schema": "official_no_sweep_landing_v1",
        "enabled": True,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_file": str(args.input),
        "n_total": len(rows_total),
        "n_used": len(rows),
        "n_filtered": len(rows_total) - len(rows),
        "feature_names": FEATURES,
        "coef_x": [float(v) for v in all_coefs[0]],
        "coef_y": [float(v) for v in all_coefs[1]],
        "residual_std_x": float(np.std(residuals[:, 0])),
        "residual_std_y": float(np.std(residuals[:, 1])),
        "input_ranges": input_ranges(rows),
        "support_margin": float(args.support_margin),
        "metrics": {
            "current_mock_all": metric_dict(mock_pred, y, all_idx),
            "calibrated_train_split_train": metric_dict(split_pred, y, train_idx),
            "calibrated_train_split_val": metric_dict(split_pred, y, val_idx),
            "calibrated_all_fit_all": metric_dict(all_pred, y, all_idx),
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report["metrics"], indent=2, ensure_ascii=False), flush=True)
    print(f"wrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
