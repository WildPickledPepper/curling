#!/usr/bin/env python3
"""Fit simple global solver-row correction models and evaluate endpoints.

The per-sample tail oracle tells us what normal/tangent impulse correction would
make each endpoint match Unity.  This script asks whether a single global row
model can reproduce those corrections.  Every candidate is evaluated by running
the corrected target velocity through the actual pyphysx tail replay, so the
reported metric is endpoint RMSE, not only an algebraic impulse residual.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse import analyze_collision_tail_replay_oracle as tail


DEFAULT_PROBE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_current_best_step_snapshots_20260709.json"
)
DEFAULT_ROW_DELTA = PROJECT_ROOT / "data" / "calibration" / "unity_collision_solver_row_delta_from_tail_oracle_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_row_correction_models_20260709.json"
MASS_KG = 19.1


Array = np.ndarray


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rmse(values: Iterable[float]) -> Optional[float]:
    vals = [float(value) for value in values if value is not None]
    if not vals:
        return None
    return math.sqrt(sum(value * value for value in vals) / len(vals))


def _mean(values: Iterable[float]) -> Optional[float]:
    vals = [float(value) for value in values if value is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


def _result_set(payload: Dict[str, Any], index: int) -> Dict[str, Any]:
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        raise ValueError("probe has no result_sets")
    return result_sets[index]


def _complex_from_components(values: Array) -> Array:
    return values[:, 0] + 1j * values[:, 1]


def _components_from_complex(values: Array) -> Array:
    return np.column_stack([values.real, values.imag])


def _fit_models(local: Array, implied: Array) -> Dict[str, Tuple[Dict[str, Any], Callable[[Array], Array]]]:
    models: Dict[str, Tuple[Dict[str, Any], Callable[[Array], Array]]] = {}
    delta = implied - local

    models["no_correction"] = ({}, lambda x: x.copy())
    models["per_sample_oracle"] = ({}, lambda x: implied.copy())

    denom_n = float(np.dot(local[:, 0], local[:, 0]))
    s_n = 1.0 if denom_n <= 1e-12 else float(np.dot(local[:, 0], implied[:, 0]) / denom_n)
    models["global_normal_scale_only"] = (
        {"normal_scale": s_n},
        lambda x, s=s_n: np.column_stack([s * x[:, 0], x[:, 1]]),
    )

    denom_t = float(np.dot(local[:, 1], local[:, 1]))
    s_t = 1.0 if denom_t <= 1e-12 else float(np.dot(local[:, 1], implied[:, 1]) / denom_t)
    models["global_tangent_scale_only"] = (
        {"tangent_scale": s_t},
        lambda x, s=s_t: np.column_stack([x[:, 0], s * x[:, 1]]),
    )

    denom = float(np.sum(local * local))
    s = 1.0 if denom <= 1e-12 else float(np.sum(local * implied) / denom)
    models["global_uniform_scale"] = ({"scale": s}, lambda x, scale=s: scale * x)

    models["global_nt_scale"] = (
        {"normal_scale": s_n, "tangent_scale": s_t},
        lambda x, sn=s_n, st=s_t: np.column_stack([sn * x[:, 0], st * x[:, 1]]),
    )

    z_local = _complex_from_components(local)
    z_implied = _complex_from_components(implied)
    cross = np.sum(z_implied * np.conj(z_local))
    theta = float(np.angle(cross))
    rot = complex(math.cos(theta), math.sin(theta))
    models["global_rotation_only"] = (
        {"theta_deg": math.degrees(theta)},
        lambda x, r=rot: _components_from_complex(_complex_from_components(x) * r),
    )

    alpha = 1.0 + 0.0j if denom <= 1e-12 else cross / denom
    models["global_uniform_scale_rotation"] = (
        {"scale": abs(alpha), "theta_deg": math.degrees(float(np.angle(alpha)))},
        lambda x, a=alpha: _components_from_complex(_complex_from_components(x) * a),
    )

    # yN = a*N - b*T, yT = b*N + c*T.  This is still a single global
    # transform, but allows normal/tangent scales plus one rotation-like term.
    a_rows: List[List[float]] = []
    b_vals: List[float] = []
    for (n, t), (yn, yt) in zip(local, implied):
        a_rows.append([float(n), float(-t), 0.0])
        b_vals.append(float(yn))
        a_rows.append([0.0, float(n), float(t)])
        b_vals.append(float(yt))
    params_3, *_ = np.linalg.lstsq(np.asarray(a_rows), np.asarray(b_vals), rcond=None)
    a, b, c = [float(value) for value in params_3]
    models["global_nt_scale_plus_rotation_term"] = (
        {"normal_scale_like": a, "rotation_term": b, "tangent_scale_like": c},
        lambda x, aa=a, bb=b, cc=c: np.column_stack([aa * x[:, 0] - bb * x[:, 1], bb * x[:, 0] + cc * x[:, 1]]),
    )

    # Fully general global 2x2 linear map in the contact frame.  This is an
    # intentionally generous baseline; if it fails, a simple global correction is untenable.
    matrix_t, *_ = np.linalg.lstsq(local, implied, rcond=None)
    matrix = matrix_t.T
    models["global_full_2x2_linear"] = (
        {"matrix": matrix.tolist()},
        lambda x, m=matrix: x @ m.T,
    )

    # Constant tangent/normal offsets test whether a hidden fixed row bias exists.
    offset = np.mean(delta, axis=0)
    models["global_constant_impulse_offset"] = (
        {"normal_offset_Ns": float(offset[0]), "tangent_offset_Ns": float(offset[1])},
        lambda x, off=offset: x + off,
    )

    return models


def _protocol_delta(row: Dict[str, Any], delta_components: Array) -> List[float]:
    normal = np.asarray(row["contact_normal"], dtype=float)
    tangent_vec = np.asarray(row["contact_tangent"], dtype=float)
    delta_v = (normal * delta_components[0] + tangent_vec * delta_components[1]) / MASS_KG
    return [float(delta_v[0]), float(delta_v[1])]


def _evaluate_model(
    *,
    model_name: str,
    params: Dict[str, Any],
    predicted_implied: Array,
    local: Array,
    implied: Array,
    row_delta_rows: List[Dict[str, Any]],
    probe_rows_by_id: Dict[int, Dict[str, Any]],
    config: Dict[str, Any],
    snapshot_key: str,
    dt: float,
    max_time: float,
    stop_speed: float,
    stop_frames: int,
) -> Dict[str, Any]:
    rows = []
    residuals = predicted_implied - implied
    predicted_deltas = predicted_implied - local
    for index, row_delta in enumerate(row_delta_rows):
        sample_id = int(row_delta["sample_id"])
        probe_row = probe_rows_by_id[sample_id]
        snapshot = (probe_row.get("snapshots") or {})[snapshot_key]["target"]
        base_v = np.asarray(snapshot["linear_velocity"], dtype=float)
        delta_v = np.asarray(_protocol_delta(row_delta, predicted_deltas[index]), dtype=float)
        corrected_velocity = base_v + delta_v
        tail_result = tail._simulate_tail(
            snapshot,
            config,
            corrected_velocity_protocol=corrected_velocity,
            dt=dt,
            max_time=max_time,
            stop_speed=stop_speed,
            stop_frames=stop_frames,
        )
        unity_target = probe_row["unity_target"]
        endpoint_error = tail._dist(tail_result["endpoint"], unity_target)
        rows.append(
            {
                "sample_id": sample_id,
                "label": row_delta.get("label"),
                "endpoint_error_m": endpoint_error,
                "predicted_delta_impulse_normal_Ns": float(predicted_deltas[index, 0]),
                "predicted_delta_impulse_tangent_Ns": float(predicted_deltas[index, 1]),
                "oracle_delta_impulse_normal_Ns": float(implied[index, 0] - local[index, 0]),
                "oracle_delta_impulse_tangent_Ns": float(implied[index, 1] - local[index, 1]),
                "residual_impulse_normal_Ns": float(residuals[index, 0]),
                "residual_impulse_tangent_Ns": float(residuals[index, 1]),
                "residual_impulse_norm_Ns": float(np.linalg.norm(residuals[index])),
                "endpoint": tail_result["endpoint"],
                "unity_target": unity_target,
            }
        )
    endpoint_errors = [float(row["endpoint_error_m"]) for row in rows]
    residual_norms = [float(row["residual_impulse_norm_Ns"]) for row in rows]
    return {
        "model": model_name,
        "params": params,
        "summary": {
            "endpoint_rmse_m": _rmse(endpoint_errors),
            "endpoint_mean_m": _mean(endpoint_errors),
            "endpoint_over_2cm_count": sum(1 for value in endpoint_errors if value > 0.02),
            "endpoint_max_m": max(endpoint_errors) if endpoint_errors else None,
            "impulse_residual_rmse_Ns": _rmse(residual_norms),
            "impulse_residual_mean_Ns": _mean(residual_norms),
            "impulse_residual_max_Ns": max(residual_norms) if residual_norms else None,
        },
        "worst_rows": sorted(rows, key=lambda row: row["endpoint_error_m"], reverse=True)[:5],
        "rows": rows,
    }


def build_report(
    probe_path: Path,
    row_delta_path: Path,
    *,
    snapshot_key: str,
    result_index: int,
    dt: float,
    max_time: float,
    stop_speed: float,
    stop_frames: int,
) -> Dict[str, Any]:
    probe_payload = _read_json(probe_path)
    result_set = _result_set(probe_payload, result_index)
    config = result_set.get("config") or {}
    probe_rows_by_id = {int(row["sample_id"]): row for row in result_set.get("rows") or []}

    row_delta_payload = _read_json(row_delta_path)
    row_delta_rows = [row for row in row_delta_payload.get("rows", []) if row.get("status") == "ok"]
    local = np.asarray(
        [[float(row["local_target_impulse_normal_Ns"]), float(row["local_target_impulse_tangent_Ns"])] for row in row_delta_rows],
        dtype=float,
    )
    implied = np.asarray(
        [
            [
                float(row["unity_implied_target_impulse_normal_Ns"]),
                float(row["unity_implied_target_impulse_tangent_Ns"]),
            ]
            for row in row_delta_rows
        ],
        dtype=float,
    )

    model_reports = []
    for model_name, (params, predict) in _fit_models(local, implied).items():
        predicted = predict(local)
        model_reports.append(
            _evaluate_model(
                model_name=model_name,
                params=params,
                predicted_implied=predicted,
                local=local,
                implied=implied,
                row_delta_rows=row_delta_rows,
                probe_rows_by_id=probe_rows_by_id,
                config=config,
                snapshot_key=snapshot_key,
                dt=dt,
                max_time=max_time,
                stop_speed=stop_speed,
                stop_frames=stop_frames,
            )
        )
    model_reports.sort(key=lambda item: float(item["summary"]["endpoint_rmse_m"] or float("inf")))

    return {
        "probe": str(probe_path.relative_to(PROJECT_ROOT)),
        "row_delta": str(row_delta_path.relative_to(PROJECT_ROOT)),
        "snapshot_key": snapshot_key,
        "summary": {
            "best_model": model_reports[0]["model"] if model_reports else None,
            "best_endpoint_rmse_m": (model_reports[0]["summary"]["endpoint_rmse_m"] if model_reports else None),
            "best_endpoint_over_2cm_count": (
                model_reports[0]["summary"]["endpoint_over_2cm_count"] if model_reports else None
            ),
            "model_count": len(model_reports),
        },
        "models": model_reports,
        "interpretation": [
            "Low-dimensional global models correspond to tuning one or two solver parameters; failure to reach 2cm means the residual is sample/contact-instance specific.",
            "per_sample_oracle is included as a sanity check and should be near the tail-oracle report.",
            "global_full_2x2_linear is intentionally generous; if it still leaves >2cm endpoints, a single global contact-frame transform is not enough.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--row-delta", type=Path, default=DEFAULT_ROW_DELTA)
    parser.add_argument("--snapshot-key", default="0.020000")
    parser.add_argument("--result-index", type=int, default=0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--max-time", type=float, default=20.0)
    parser.add_argument("--stop-speed", type=float, default=0.003)
    parser.add_argument("--stop-frames", type=int, default=500)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    probe_path = args.probe if args.probe.is_absolute() else PROJECT_ROOT / args.probe
    row_delta_path = args.row_delta if args.row_delta.is_absolute() else PROJECT_ROOT / args.row_delta
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    report = build_report(
        probe_path,
        row_delta_path,
        snapshot_key=args.snapshot_key,
        result_index=args.result_index,
        dt=args.dt,
        max_time=args.max_time,
        stop_speed=args.stop_speed,
        stop_frames=args.stop_frames,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output_path.relative_to(PROJECT_ROOT)}")
    for model in report["models"]:
        summary = model["summary"]
        print(
            f"{model['model']}: rmse={summary['endpoint_rmse_m']:.6f} "
            f"over2cm={summary['endpoint_over_2cm_count']} "
            f"impulse_resid={summary['impulse_residual_rmse_Ns']:.6f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
