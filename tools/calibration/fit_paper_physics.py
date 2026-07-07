# -*- coding: utf-8 -*-
"""Fit and evaluate the reduced paper-inspired curling dynamics."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
from scipy.optimize import least_squares

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from fit_physics_calibration import (
    design_matrix,
    load_rows,
    metric_dict,
    split_indices,
    targets,
    usable_rows,
)
from paper_curling_sim import PaperPhysicsParams, simulate_tail_batch


MOTION_FIELDS = ["motion_x", "motion_y", "motion_vx", "motion_vy", "motion_w"]
FEATURE_NAMES = [
    "1", "v", "h", "w", "abs_w", "tanh_w",
    "v2", "h2", "w2", "v_h", "v_w", "h_w",
]


def rows_with_motion(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [
        row
        for row in usable_rows(rows)
        if all(row.get(field) is not None for field in MOTION_FIELDS)
    ]


def all_rows_with_motion(
    rows: Sequence[Dict[str, object]]
) -> List[Dict[str, object]]:
    return [
        row
        for row in rows
        if all(row.get(field) is not None for field in MOTION_FIELDS)
    ]


def motion_targets(rows: Sequence[Dict[str, object]]) -> np.ndarray:
    return np.asarray(
        [[float(row[field]) for field in MOTION_FIELDS] for row in rows],
        dtype=float,
    )


def fit_middle_mapping(
    x: np.ndarray, middle: np.ndarray, train_idx: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    coefficients, *_ = np.linalg.lstsq(x[train_idx], middle[train_idx], rcond=None)
    return coefficients, x @ coefficients


def fit_tail_params(
    middle: np.ndarray,
    final: np.ndarray,
    train_idx: np.ndarray,
    *,
    dt: float,
    max_nfev: int,
    initial: PaperPhysicsParams | None = None,
) -> Tuple[PaperPhysicsParams, object]:
    initial_values = (initial or PaperPhysicsParams()).to_array()
    lower = np.array(
        [0.005, 0.0, 0.5, 0.0, 0.0, 0.2, 0.04, 0.0, 0.0], dtype=float
    )
    upper = np.array(
        [0.20, 0.08, 3.5, 0.05, 30.0, 2.0, 0.8, 0.3, 0.2], dtype=float
    )
    train_middle = middle[train_idx]
    train_final = final[train_idx]

    def residual(values: np.ndarray) -> np.ndarray:
        params = PaperPhysicsParams.from_sequence(values)
        prediction, _ = simulate_tail_batch(train_middle, params, dt=dt)
        return (prediction - train_final).ravel()

    result = least_squares(
        residual,
        initial_values,
        bounds=(lower, upper),
        max_nfev=max_nfev,
        verbose=1,
        x_scale="jac",
        diff_step=2e-3,
    )
    return PaperPhysicsParams.from_sequence(result.x), result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--output", type=Path, default=Path("config/paper_physics_calibration.json")
    )
    parser.add_argument("--dt", type=float, default=0.025)
    parser.add_argument("--max-nfev", type=int, default=250)
    parser.add_argument(
        "--fit-all",
        action="store_true",
        help="refit deployment coefficients using every usable observation",
    )
    parser.add_argument(
        "--initial-config",
        type=Path,
        help="start ODE optimization from an existing fitted configuration",
    )
    args = parser.parse_args()

    rows_total = load_rows(args.input)
    rows = rows_with_motion(rows_total)
    motion_rows = all_rows_with_motion(rows_total)
    if len(rows) < 30:
        raise SystemExit(f"not enough usable MOTIONINFO rows: {len(rows)}")

    x = design_matrix(rows)
    final = targets(rows)
    middle = motion_targets(rows)
    train_idx, val_idx = split_indices(rows)

    if args.fit_all:
        motion_x = design_matrix(motion_rows)
        motion_middle = motion_targets(motion_rows)
        motion_idx = np.arange(len(motion_rows), dtype=int)
        middle_coef, _ = fit_middle_mapping(
            motion_x, motion_middle, motion_idx
        )
        middle_pred = x @ middle_coef
        fit_idx = np.arange(len(rows), dtype=int)
    else:
        middle_coef, middle_pred = fit_middle_mapping(x, middle, train_idx)
        fit_idx = train_idx

    initial_params = None
    if args.initial_config:
        initial_payload = json.loads(
            args.initial_config.read_text(encoding="utf-8")
        )
        initial_params = PaperPhysicsParams(
            **initial_payload["params"]
        )
    params, optimizer = fit_tail_params(
        middle,
        final,
        fit_idx,
        dt=args.dt,
        max_nfev=args.max_nfev,
        initial=initial_params,
    )

    oracle_pred, oracle_time = simulate_tail_batch(middle, params, dt=args.dt)
    full_pred, full_time = simulate_tail_batch(middle_pred, params, dt=args.dt)

    # Fit the endpoint baseline on exactly the same training partition.
    landing_coef, *_ = np.linalg.lstsq(x[fit_idx], final[fit_idx], rcond=None)
    landing_pred = x @ landing_coef
    hybrid_pred = np.column_stack([landing_pred[:, 0], full_pred[:, 1]])

    report = {
        "schema": "paper_curling_physics_v1",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_file": str(args.input),
        "n_total": len(rows_total),
        "n_motion_used": len(motion_rows),
        "n_landing_used": len(rows),
        "n_out_of_play": len(rows_total) - len(rows),
        "fit_mode": "all_data_deployment" if args.fit_all else "train_validation",
        "dt": float(args.dt),
        "model_scope": "single-rock, no-collision, no-sweep",
        "params": params.to_dict(),
        "middle_feature_names": FEATURE_NAMES,
        "middle_target_names": MOTION_FIELDS,
        "middle_coefficients": middle_coef.tolist(),
        "direct_landing_coefficients": landing_coef.tolist(),
        "optimizer": {
            "success": bool(optimizer.success),
            "status": int(optimizer.status),
            "message": str(optimizer.message),
            "nfev": int(optimizer.nfev),
            "cost": float(optimizer.cost),
        },
        "metrics": {},
        "stop_time_seconds": {
            "oracle_mean": float(np.mean(oracle_time)),
            "oracle_min": float(np.min(oracle_time)),
            "oracle_max": float(np.max(oracle_time)),
            "full_mean": float(np.mean(full_time)),
        },
    }

    if args.fit_all:
        report["metrics"] = {
            "oracle_middle_all_fit": metric_dict(
                oracle_pred, final, fit_idx
            ),
            "full_pipeline_all_fit": metric_dict(full_pred, final, fit_idx),
            "direct_polynomial_all_fit": metric_dict(
                landing_pred, final, fit_idx
            ),
            "hybrid_all_fit": metric_dict(hybrid_pred, final, fit_idx),
        }
    else:
        report["metrics"] = {
            "oracle_middle_train": metric_dict(oracle_pred, final, train_idx),
            "oracle_middle_val": metric_dict(oracle_pred, final, val_idx),
            "full_pipeline_train": metric_dict(full_pred, final, train_idx),
            "full_pipeline_val": metric_dict(full_pred, final, val_idx),
            "direct_polynomial_train": metric_dict(
                landing_pred, final, train_idx
            ),
            "direct_polynomial_val": metric_dict(
                landing_pred, final, val_idx
            ),
            "hybrid_train": metric_dict(hybrid_pred, final, train_idx),
            "hybrid_val": metric_dict(hybrid_pred, final, val_idx),
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report["params"], indent=2), flush=True)
    print(json.dumps(report["metrics"], indent=2), flush=True)
    print(f"wrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
