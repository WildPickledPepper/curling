#!/usr/bin/env python3
"""Fit and cross-check a collision endpoint residual correction.

This is a diagnostic layer for the current Unity-vs-pyphysx collision gap.  It
does not replace the reverse-engineered physics; it asks whether the remaining
target endpoint residual is stable enough to correct from the local PhysX
replay outputs and handoff geometry, using existing samples only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "unity_unique_target_collision_samples_20260708.jsonl"
DEFAULT_PROBE = (
    PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_target_current_best_20260708.json"
)
DEFAULT_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_endpoint_residual_correction_20260709.json"
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "unity_collision_endpoint_residual_correction.json"


FEATURE_SETS: dict[str, list[str]] = {
    "constant": ["1"],
    "sim_endpoint_linear": ["1", "sim_dx", "sim_dy", "sim_distance", "sim_angle"],
    "handoff_geometry_linear": [
        "1",
        "v0",
        "target_x",
        "target_y",
        "rel_x",
        "rel_y",
        "handoff_speed",
        "handoff_w",
        "sim_dx",
        "sim_dy",
    ],
    "handoff_geometry_quadratic_light": [
        "1",
        "v0",
        "target_x",
        "target_y",
        "rel_x",
        "rel_y",
        "handoff_speed",
        "handoff_w",
        "sim_dx",
        "sim_dy",
        "sim_distance",
        "rel_x_handoff_speed",
        "rel_y_handoff_speed",
        "sim_dx_sim_dy",
    ],
}


@dataclass(frozen=True)
class Row:
    sample_id: int
    source_case_id: int
    repeat_index: int
    category: str
    v0: float
    h0: float
    w0: float
    target_x: float
    target_y: float
    handoff_x: float
    handoff_y: float
    handoff_vx: float
    handoff_vy: float
    handoff_w: float
    sim_target_x: float
    sim_target_y: float
    unity_target_x: float
    unity_target_y: float

    @property
    def sim_residual_x(self) -> float:
        return self.sim_target_x - self.unity_target_x

    @property
    def sim_residual_y(self) -> float:
        return self.sim_target_y - self.unity_target_y

    @property
    def baseline_error(self) -> float:
        return math.hypot(self.sim_residual_x, self.sim_residual_y)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _best_result_set(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        raise SystemExit(f"{path} has no result_sets")
    return min(
        result_sets,
        key=lambda item: float("inf")
        if (item.get("summary") or {}).get("combined_rmse_m") is None
        else float((item.get("summary") or {})["combined_rmse_m"]),
    )


def _sample_target_xy(sample: dict[str, Any]) -> tuple[float, float] | None:
    stones = (sample.get("requested") or {}).get("stones") or []
    if not stones:
        return None
    return float(stones[0]["x"]), float(stones[0]["y"])


def load_rows(samples_path: Path, probe_path: Path) -> list[Row]:
    samples = {int(row["sample_id"]): row for row in _read_jsonl(samples_path)}
    result_set = _best_result_set(probe_path)
    rows: list[Row] = []
    for probe_row in result_set.get("rows") or []:
        sample_id = int(probe_row["sample_id"])
        sample = samples.get(sample_id)
        if sample is None or not probe_row.get("unity_target_in_play"):
            continue
        target_xy = _sample_target_xy(sample)
        if target_xy is None:
            continue
        metadata = sample.get("plan_metadata") or {}
        handoff = probe_row.get("handoff") or {}
        requested = sample.get("requested") or {}
        rows.append(
            Row(
                sample_id=sample_id,
                source_case_id=int(metadata.get("source_sample_id", sample_id)),
                repeat_index=int(metadata.get("batch_repeat_index", 0)),
                category=str(sample.get("category")),
                v0=float(requested.get("v0", 0.0)),
                h0=float(requested.get("h0", 0.0)),
                w0=float(requested.get("w0", 0.0)),
                target_x=target_xy[0],
                target_y=target_xy[1],
                handoff_x=float(handoff["x"]),
                handoff_y=float(handoff["y"]),
                handoff_vx=float(handoff["vx"]),
                handoff_vy=float(handoff["vy"]),
                handoff_w=float(handoff["w"]),
                sim_target_x=float(probe_row["sim_target"][0]),
                sim_target_y=float(probe_row["sim_target"][1]),
                unity_target_x=float(probe_row["unity_target"][0]),
                unity_target_y=float(probe_row["unity_target"][1]),
            )
        )
    return rows


def feature_value(row: Row, name: str) -> float:
    if name.startswith("case_"):
        return 1.0 if row.source_case_id == int(name[5:]) else 0.0
    if name.startswith("category_"):
        return 1.0 if row.category == name[9:] else 0.0
    rel_x = row.handoff_x - row.target_x
    rel_y = row.handoff_y - row.target_y
    sim_dx = row.sim_target_x - row.target_x
    sim_dy = row.sim_target_y - row.target_y
    sim_distance = math.hypot(sim_dx, sim_dy)
    handoff_speed = math.hypot(row.handoff_vx, row.handoff_vy)
    if name == "1":
        return 1.0
    if name == "v0":
        return row.v0
    if name == "h0":
        return row.h0
    if name == "w0":
        return row.w0
    if name == "target_x":
        return row.target_x
    if name == "target_y":
        return row.target_y
    if name == "rel_x":
        return rel_x
    if name == "rel_y":
        return rel_y
    if name == "handoff_speed":
        return handoff_speed
    if name == "handoff_w":
        return row.handoff_w
    if name == "sim_dx":
        return sim_dx
    if name == "sim_dy":
        return sim_dy
    if name == "sim_distance":
        return sim_distance
    if name == "sim_angle":
        return math.atan2(sim_dy, sim_dx)
    if name == "rel_x_handoff_speed":
        return rel_x * handoff_speed
    if name == "rel_y_handoff_speed":
        return rel_y * handoff_speed
    if name == "sim_dx_sim_dy":
        return sim_dx * sim_dy
    raise KeyError(name)


def design(rows: list[Row], features: list[str]) -> np.ndarray:
    return np.asarray([[feature_value(row, name) for name in features] for row in rows], dtype=float)


def fit(rows: list[Row], features: list[str], alpha: float) -> tuple[np.ndarray, np.ndarray]:
    x = design(rows, features)
    yx = np.asarray([row.sim_residual_x for row in rows], dtype=float)
    yy = np.asarray([row.sim_residual_y for row in rows], dtype=float)
    if alpha <= 0.0:
        return np.linalg.lstsq(x, yx, rcond=None)[0], np.linalg.lstsq(x, yy, rcond=None)[0]
    lhs = x.T @ x + alpha * np.eye(x.shape[1])
    return np.linalg.solve(lhs, x.T @ yx), np.linalg.solve(lhs, x.T @ yy)


def corrected_errors(rows: list[Row], features: list[str], bx: np.ndarray, by: np.ndarray) -> list[float]:
    x = design(rows, features)
    pred_x = x @ bx
    pred_y = x @ by
    return [
        math.hypot(row.sim_residual_x - float(pred_x[index]), row.sim_residual_y - float(pred_y[index]))
        for index, row in enumerate(rows)
    ]


def _percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    rows = sorted(values)
    pos = (len(rows) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return rows[lo]
    return rows[lo] * (hi - pos) + rows[hi] * (pos - lo)


def metrics(errors: list[float]) -> dict[str, Any]:
    return {
        "n": len(errors),
        "rmse_m": None if not errors else math.sqrt(sum(value * value for value in errors) / len(errors)),
        "mae_m": None if not errors else sum(errors) / len(errors),
        "p50_m": _percentile(errors, 0.50),
        "p90_m": _percentile(errors, 0.90),
        "max_m": None if not errors else max(errors),
        "within_2cm": sum(1 for value in errors if value <= 0.02),
    }


def grouped_cv(rows: list[Row], features: list[str], alpha: float, key: str) -> dict[str, Any]:
    groups: dict[Any, list[Row]] = defaultdict(list)
    for row in rows:
        groups[getattr(row, key)].append(row)
    errors: list[float] = []
    fold_details = []
    for group_value, test_rows in sorted(groups.items(), key=lambda item: item[0]):
        train_rows = [row for other, bucket in groups.items() if other != group_value for row in bucket]
        if len(train_rows) < len(features):
            continue
        bx, by = fit(train_rows, features, alpha)
        fold_errors = corrected_errors(test_rows, features, bx, by)
        errors.extend(fold_errors)
        fold_details.append({"held_out": group_value, **metrics(fold_errors)})
    return {"group_count": len(groups), "overall": metrics(errors), "folds": fold_details}


def choose_model(rows: list[Row], alphas: list[float]) -> dict[str, Any]:
    source_case_features = [f"case_{case_id}" for case_id in sorted({row.source_case_id for row in rows})]
    category_features = [f"category_{category}" for category in sorted({row.category for row in rows})]
    feature_sets = {
        **FEATURE_SETS,
        "category_onehot_plus_sim": ["1", *category_features, "sim_dx", "sim_dy", "sim_distance", "sim_angle"],
        "source_case_onehot": ["1", *source_case_features],
        "source_case_onehot_plus_sim": [
            "1",
            *source_case_features,
            "sim_dx",
            "sim_dy",
            "sim_distance",
            "sim_angle",
        ],
    }
    candidates = []
    for name, features in feature_sets.items():
        for alpha in alphas:
            bx, by = fit(rows, features, alpha)
            in_sample = metrics(corrected_errors(rows, features, bx, by))
            leave_repeat = grouped_cv(rows, features, alpha, "repeat_index")
            leave_source = grouped_cv(rows, features, alpha, "source_case_id")
            candidates.append(
                {
                    "name": name,
                    "features": features,
                    "alpha": alpha,
                    "coefficients_dx": bx.tolist(),
                    "coefficients_dy": by.tolist(),
                    "in_sample": in_sample,
                    "leave_repeat_out": leave_repeat,
                    "leave_source_case_out": leave_source,
                }
            )
    candidates.sort(
        key=lambda item: (
            float("inf")
            if item["leave_repeat_out"]["overall"]["rmse_m"] is None
            else item["leave_repeat_out"]["overall"]["rmse_m"],
            len(item["features"]),
        )
    )
    return {"best_by_leave_repeat": candidates[0], "candidates": candidates}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--alphas", nargs="+", type=float, default=[0.0, 1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 1e-1])
    args = parser.parse_args()

    rows = load_rows(args.samples, args.probe)
    if not rows:
        raise SystemExit("no in-play target rows")
    model = choose_model(rows, args.alphas)
    best = model["best_by_leave_repeat"]
    baseline = metrics([row.baseline_error for row in rows])
    report = {
        "samples": str(args.samples),
        "probe": str(args.probe),
        "row_count": len(rows),
        "baseline_target": baseline,
        "best_by_leave_repeat": best,
        "candidates": model["candidates"],
        "rows": [
            {
                "sample_id": row.sample_id,
                "source_case_id": row.source_case_id,
                "repeat_index": row.repeat_index,
                "category": row.category,
                "baseline_error_m": row.baseline_error,
                "residual": [row.sim_residual_x, row.sim_residual_y],
            }
            for row in rows
        ],
        "interpretation": (
            "If leave-repeat-out is near 2cm while leave-source-case-out remains much worse, "
            "the residual is stable for repeated planned collision cases but not yet a general "
            "physics replacement for unseen contacts. That identifies a deterministic Unity-vs-pyphysx "
            "contact residual, not random sampling noise."
        ),
    }
    config = {
        "mode": "collision_endpoint_residual_correction",
        "source_report": str(args.report),
        "features": best["features"],
        "alpha": best["alpha"],
        "coefficients_dx": best["coefficients_dx"],
        "coefficients_dy": best["coefficients_dy"],
        "baseline_target_rmse_m": baseline["rmse_m"],
        "in_sample_rmse_m": best["in_sample"]["rmse_m"],
        "leave_repeat_out_rmse_m": best["leave_repeat_out"]["overall"]["rmse_m"],
        "leave_source_case_out_rmse_m": best["leave_source_case_out"]["overall"]["rmse_m"],
        "units": "meters",
        "apply": "corrected_target_endpoint = pyphysx_target_endpoint - predicted_residual",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.config.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.config.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
