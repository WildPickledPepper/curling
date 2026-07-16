# -*- coding: utf-8 -*-
"""Fit fast-simulator landing calibration from Unity JSONL samples."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import numpy as np


FEATURE_NAMES = [
    "1",
    "v",
    "h",
    "w",
    "sweep",
    "abs_w",
    "tanh_w",
    "v2",
    "h2",
    "w2",
    "sweep2",
    "v_h",
    "v_w",
    "h_w",
    "v_sweep",
    "h_sweep",
    "w_sweep",
]


def read_jsonl(paths: Sequence[Path]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                text = line.strip()
                if not text:
                    continue
                try:
                    row = json.loads(text)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_no}: invalid json") from exc
                row["_source_file"] = str(path)
                rows.append(row)
    return rows


def normalize_row(row: Dict[str, Any]) -> Dict[str, Any] | None:
    if "shot" in row:
        shot = row["shot"]
        final = row.get("final_xy")
        if final is None:
            return None
        return {
            "v0": float(shot["v0"]),
            "h0": float(shot["h0"]),
            "w0": float(shot["w0"]),
            "sweep": float(shot.get("sweep", 0.0)),
            "final_x": float(final[0]),
            "final_y": float(final[1]),
            "collision_free": bool(row.get("collision_free", False)),
            "in_play": bool(final[0] or final[1]),
            "motioninfo": row.get("motioninfo"),
            "source_file": row.get("_source_file", ""),
        }

    if "requested_v0" in row:
        sweep = row.get("requested_sweep_distance", row.get("requested_sweep", 0.0))
        return {
            "v0": float(row["requested_v0"]),
            "h0": float(row["requested_h0"]),
            "w0": float(row["requested_w0"]),
            "sweep": float(sweep or 0.0),
            "final_x": float(row.get("final_x", 0.0) or 0.0),
            "final_y": float(row.get("final_y", 0.0) or 0.0),
            "collision_free": True,
            "in_play": bool(row.get("in_play", False)),
            "motioninfo": [
                row.get("motion_x"),
                row.get("motion_y"),
                row.get("motion_vx"),
                row.get("motion_vy"),
                row.get("motion_w"),
            ],
            "source_file": row.get("_source_file", ""),
        }
    return None


def usable_rows(rows: Iterable[Dict[str, Any]], collision_free_only: bool) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for raw in rows:
        row = normalize_row(raw)
        if row is None:
            continue
        if not row["in_play"]:
            continue
        if collision_free_only and not row["collision_free"]:
            continue
        if not all(math.isfinite(float(row[name])) for name in ("v0", "h0", "w0", "sweep", "final_x", "final_y")):
            continue
        out.append(row)
    return out


def feature_row(row: Dict[str, Any]) -> List[float]:
    v = float(row["v0"])
    h = float(row["h0"])
    w = float(row["w0"])
    s = float(row["sweep"])
    return [
        1.0,
        v,
        h,
        w,
        s,
        abs(w),
        math.tanh(w),
        v * v,
        h * h,
        w * w,
        s * s,
        v * h,
        v * w,
        h * w,
        v * s,
        h * s,
        w * s,
    ]


def design_matrix(rows: Sequence[Dict[str, Any]]) -> np.ndarray:
    return np.array([feature_row(row) for row in rows], dtype=np.float64)


def targets(rows: Sequence[Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray]:
    return (
        np.array([float(row["final_x"]) for row in rows], dtype=np.float64),
        np.array([float(row["final_y"]) for row in rows], dtype=np.float64),
    )


def ridge_fit(x: np.ndarray, y: np.ndarray, alpha: float) -> np.ndarray:
    reg = alpha * np.eye(x.shape[1], dtype=np.float64)
    reg[0, 0] = 0.0
    return np.linalg.solve(x.T @ x + reg, x.T @ y)


def predict(rows: Sequence[Dict[str, Any]], coef_x: Sequence[float], coef_y: Sequence[float]) -> Tuple[np.ndarray, np.ndarray]:
    x = design_matrix(rows)
    return x @ np.array(coef_x), x @ np.array(coef_y)


def metrics(rows: Sequence[Dict[str, Any]], coef_x: Sequence[float], coef_y: Sequence[float]) -> Dict[str, float]:
    if not rows:
        return {"n": 0}
    tx, ty = targets(rows)
    px, py = predict(rows, coef_x, coef_y)
    dx = px - tx
    dy = py - ty
    total = np.sqrt(dx * dx + dy * dy)
    return {
        "n": len(rows),
        "rmse_x": float(np.sqrt(np.mean(dx * dx))),
        "rmse_y": float(np.sqrt(np.mean(dy * dy))),
        "rmse_total": float(np.sqrt(np.mean(total * total))),
        "mae_x": float(np.mean(np.abs(dx))),
        "mae_y": float(np.mean(np.abs(dy))),
        "p90_total": float(np.percentile(total, 90)),
        "max_total": float(np.max(total)),
    }


def split_rows(rows: Sequence[Dict[str, Any]], seed: int, val_fraction: float) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    items = list(rows)
    rng.shuffle(items)
    val_n = max(1, int(round(len(items) * val_fraction))) if len(items) >= 5 else 0
    return items[val_n:], items[:val_n]


def ranges(rows: Sequence[Dict[str, Any]]) -> Dict[str, List[float]]:
    result: Dict[str, List[float]] = {}
    for key in ("v0", "h0", "w0", "sweep"):
        values = [float(row[key]) for row in rows]
        result[key] = [min(values), max(values)] if values else [0.0, 0.0]
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("config/unity_physics_calibration.json"))
    parser.add_argument("--eval-output", type=Path, default=Path("config/unity_physics_evaluation.json"))
    parser.add_argument("--min-fit-samples", type=int, default=80)
    parser.add_argument("--alpha", type=float, default=1e-5)
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--val-fraction", type=float, default=0.2)
    parser.add_argument("--include-collisions", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_rows = read_jsonl(args.inputs)
    rows = usable_rows(raw_rows, collision_free_only=not args.include_collisions)
    train_rows, val_rows = split_rows(rows, args.seed, args.val_fraction)

    report: Dict[str, Any] = {
        "schema": "unity_landing_v2",
        "enabled": False,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_files": [str(path) for path in args.inputs],
        "n_raw": len(raw_rows),
        "n_used": len(rows),
        "collision_free_only": not args.include_collisions,
        "feature_names": FEATURE_NAMES,
        "input_ranges": ranges(rows),
        "support_margin": 0.10,
        "min_fit_samples": args.min_fit_samples,
    }

    if len(rows) < args.min_fit_samples or len(train_rows) < len(FEATURE_NAMES):
        report["status"] = "insufficient_samples"
        report["metrics"] = {"all": {"n": len(rows)}}
        args.eval_output.parent.mkdir(parents=True, exist_ok=True)
        args.eval_output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
        return

    x_train = design_matrix(train_rows)
    tx, ty = targets(train_rows)
    coef_x = ridge_fit(x_train, tx, args.alpha)
    coef_y = ridge_fit(x_train, ty, args.alpha)

    report.update(
        {
            "enabled": True,
            "status": "fit",
            "coef_x": coef_x.tolist(),
            "coef_y": coef_y.tolist(),
            "residual_std_x": metrics(rows, coef_x, coef_y)["rmse_x"],
            "residual_std_y": metrics(rows, coef_x, coef_y)["rmse_y"],
            "metrics": {
                "train": metrics(train_rows, coef_x, coef_y),
                "val": metrics(val_rows, coef_x, coef_y),
                "all": metrics(rows, coef_x, coef_y),
            },
        }
    )
    args.eval_output.parent.mkdir(parents=True, exist_ok=True)
    args.eval_output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
