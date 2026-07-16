#!/usr/bin/env python3
"""Check whether the entrance-state oracle corrections look generalizable."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse import probe_physx_collision_alignment as probe


CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_SAMPLES = CALIBRATION / "unity_unique_role_collision_samples_20260708_r00.jsonl"
ORACLE_REPORT = CALIBRATION / "unity_collision_handoff_xy_oracle_20260709.json"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_oracle_generalization_20260709.json"


TARGET_KEYS = [
    "handoff_x_offset",
    "handoff_y_offset",
    "handoff_v_scale_delta",
    "target_x_offset",
    "target_y_offset",
    "handoff_w_offset",
]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_samples(path: Path) -> Dict[str, Dict[str, Any]]:
    rows: Dict[str, Dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            rows[str(row["sample_id"])] = row
    return rows


def _xy_from_position(position: Sequence[float], index: int) -> Tuple[float, float]:
    return float(position[2 * index]), float(position[2 * index + 1])


def _feature_row(sample: Dict[str, Any], oracle: Dict[str, Any]) -> Dict[str, Any]:
    target_index = int(sample["target_indices"][0])
    active_index = int(sample["active_shot_num"])
    target_before = _xy_from_position(sample["reset_position"], target_index)
    motion_x, motion_y, motion_vx, motion_vy, motion_w = [float(value) for value in sample["motioninfo"]]
    handoff = oracle.get("handoff") or {}
    config = oracle.get("config") or {}
    active_speed = math.hypot(motion_vx, motion_vy)
    label = str(sample.get("label") or "")
    requested = sample.get("requested") or {}
    target_x_offset = float(config.get("target_x_offset") or 0.0)
    target_y_offset = float(config.get("target_y_offset") or 0.0)
    handoff_x_offset = float(config.get("handoff_x_offset") or 0.0)
    handoff_y_offset = float(config.get("handoff_y_offset") or 0.0)
    handoff_v_scale = float(config.get("handoff_v_scale") or 1.0)
    handoff_w_offset = float(config.get("handoff_w_offset") or 0.0)
    handoff_speed = math.hypot(float(handoff.get("vx") or 0.0), float(handoff.get("vy") or 0.0))
    dx = float(handoff.get("x") or motion_x) - target_before[0]
    dy = float(handoff.get("y") or motion_y) - target_before[1]
    distance = math.hypot(dx, dy)
    if distance > 1e-12:
        normal_x, normal_y = dx / distance, dy / distance
        tangent_x, tangent_y = -normal_y, normal_x
    else:
        normal_x, normal_y, tangent_x, tangent_y = 0.0, -1.0, 1.0, 0.0
    return {
        "sample_id": int(sample["sample_id"]),
        "label": label,
        "category": str(sample.get("category") or ""),
        "is_glance": 1.0 if "glance" in label else 0.0,
        "is_right": 1.0 if "right" in label else 0.0,
        "target_before_x": target_before[0],
        "target_before_y": target_before[1],
        "requested_v0": float(requested.get("v0", active_speed)),
        "requested_w0": float(requested.get("w0", 0.0)),
        "motion_vx": motion_vx,
        "motion_vy": motion_vy,
        "motion_w": motion_w,
        "motion_speed": active_speed,
        "handoff_x": float(handoff.get("x") or 0.0),
        "handoff_y": float(handoff.get("y") or 0.0),
        "handoff_vx": float(handoff.get("vx") or 0.0),
        "handoff_vy": float(handoff.get("vy") or 0.0),
        "handoff_w": float(handoff.get("w") or 0.0),
        "handoff_speed": handoff_speed,
        "approach_normal_x": normal_x,
        "approach_normal_y": normal_y,
        "approach_tangent_x": tangent_x,
        "approach_tangent_y": tangent_y,
        "active_error_m": oracle.get("active_error_m"),
        "target_error_m": oracle.get("target_error_m"),
        "max_endpoint_error_m": oracle.get("max_endpoint_error_m"),
        "handoff_x_offset": handoff_x_offset,
        "handoff_y_offset": handoff_y_offset,
        "handoff_v_scale_delta": handoff_v_scale - 1.0,
        "target_x_offset": target_x_offset,
        "target_y_offset": target_y_offset,
        "handoff_w_offset": handoff_w_offset,
    }


def _matrix(rows: List[Dict[str, Any]], feature_names: Sequence[str]) -> np.ndarray:
    return np.asarray([[1.0] + [float(row[name]) for name in feature_names] for row in rows], dtype=float)


def _target(rows: List[Dict[str, Any]], key: str) -> np.ndarray:
    return np.asarray([float(row[key]) for row in rows], dtype=float)


def _fit_predict_loo(rows: List[Dict[str, Any]], feature_names: Sequence[str]) -> List[Dict[str, Any]]:
    predictions: List[Dict[str, Any]] = []
    for holdout_index, holdout in enumerate(rows):
        train = [row for index, row in enumerate(rows) if index != holdout_index]
        design = _matrix(train, feature_names)
        holdout_design = _matrix([holdout], feature_names)
        prediction: Dict[str, Any] = {"sample_id": holdout["sample_id"]}
        for key in TARGET_KEYS:
            y = _target(train, key)
            coef, *_ = np.linalg.lstsq(design, y, rcond=None)
            predicted = float(holdout_design @ coef)
            prediction[key] = predicted
            prediction[key + "_true"] = float(holdout[key])
            prediction[key + "_abs_error"] = abs(predicted - float(holdout[key]))
        predictions.append(prediction)
    return predictions


def _loo_summary(predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {"sample_count": len(predictions)}
    for key in TARGET_KEYS:
        errors = [float(row[key + "_abs_error"]) for row in predictions]
        summary[key + "_mae"] = float(np.mean(errors)) if errors else None
        summary[key + "_max_abs_error"] = float(np.max(errors)) if errors else None
    return summary


def _build_sim_config(row: Dict[str, Any], prediction: Dict[str, Any]) -> Dict[str, float]:
    return {
        "handoff_extra": 0.0,
        "handoff_friction": probe.BASE_FRICTION,
        "handoff_v_scale": 1.0 + float(prediction.get("handoff_v_scale_delta", 0.0)),
        "handoff_vx_offset": 0.0,
        "handoff_vy_offset": 0.0,
        "handoff_w_offset": float(prediction.get("handoff_w_offset", 0.0)),
        "angular_sign": 1.0,
        "handoff_x_offset": float(prediction.get("handoff_x_offset", 0.0)),
        "handoff_y_offset": float(prediction.get("handoff_y_offset", 0.0)),
        "target_x_offset": float(prediction.get("target_x_offset", 0.0)),
        "target_y_offset": float(prediction.get("target_y_offset", 0.0)),
    }


def _simulate_predictions(
    samples: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
    predictions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    scene_flags: List[Any] = []
    combine_mode = probe._combine_mode_from_name("multiply")
    stone_points = probe._stone_points(radius=0.146, height=0.23, faces=256)
    sim_rows = []
    for row, prediction in zip(rows, predictions):
        sample = samples[str(row["sample_id"])]
        cfg = _build_sim_config(row, prediction)
        result = probe._simulate_one(
            sample,
            **cfg,
            ice_friction=0.02,
            stone_friction=0.6,
            stone_restitution=1.0,
            pre_collision_dynamic_friction=None,
            pre_collision_static_friction=None,
            pre_collision_friction_scope="both",
            material_switch_mode="post-step-distance",
            stone_points=stone_points,
            radius=0.146,
            height=0.23,
            stone_faces=256,
            inertia_model="solid-cylinder",
            inertia_radial=None,
            inertia_vertical=None,
            active_yaw=0.0,
            active_yaw_source="constant",
            active_yaw_integral_sign=1.0,
            target_yaw=0.0,
            center_height=0.1276,
            scene_flags=scene_flags,
            scene_flag_names=[],
            combine_mode=combine_mode,
            combine_mode_name="multiply",
            contact_offset=0.01,
            rest_offset=0.0,
            shape_local_x=0.0,
            shape_local_y=0.0,
            shape_local_z=0.0,
            shape_local_yaw=0.0,
            convex_quantized_count=255,
            convex_vertex_limit=255,
            quantize_input=False,
            gpu_compatible=False,
            solver_position_iterations=6,
            solver_velocity_iterations=1,
            max_depenetration_velocity=10.0,
            lock_upright=False,
            disable_stone_gravity=False,
            disable_strong_friction=False,
            improved_patch_friction=False,
            rink_geometry="plane",
            rink_mesh_center_x=probe.UNITY_PLANE_MESH_CENTER_X_M,
            rink_mesh_center_y=probe.UNITY_PLANE_MESH_CENTER_Y_M,
            rink_mesh_width=probe.UNITY_PLANE_MESH_WIDTH_M,
            rink_mesh_length=probe.UNITY_PLANE_MESH_LENGTH_M,
            rink_mesh_subdivisions=probe.UNITY_PLANE_MESH_SUBDIVISIONS,
            use_unity_frame=True,
            friction_offset_threshold=None,
            dt=0.01,
            max_time=20.0,
            stop_speed=0.003,
            stop_frames=500,
            snapshot_times=[],
            enable_contact_report=False,
            max_contact_reports=0,
            target_settle_time=0.0,
            active_settle_time=0.0,
            active_settle_backoff=0.5,
        )
        sim_rows.append(
            {
                "sample_id": row["sample_id"],
                "predicted_config": cfg,
                "active_error_m": result.get("active_error"),
                "target_error_m": result.get("target_error"),
                "max_endpoint_error_m": max(
                    float(result.get("active_error") or 0.0),
                    float(result.get("target_error") or 0.0),
                )
                if result.get("target_error") is not None
                else result.get("active_error"),
                "sim_active": result.get("sim_active"),
                "sim_target": result.get("sim_target"),
                "unity_active": result.get("unity_active"),
                "unity_target": result.get("unity_target"),
            }
        )
    return sim_rows


def _endpoint_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    in_play = [row for row in rows if row.get("target_error_m") is not None]
    active_errors = [float(row["active_error_m"]) for row in rows if row.get("active_error_m") is not None]
    target_errors = [float(row["target_error_m"]) for row in in_play]
    both_under = [
        int(row["sample_id"])
        for row in in_play
        if float(row["active_error_m"]) <= 0.02 and float(row["target_error_m"]) <= 0.02
    ]
    return {
        "sample_count": len(rows),
        "in_play_pair_count": len(in_play),
        "active_rmse_m": math.sqrt(sum(value * value for value in active_errors) / len(active_errors))
        if active_errors
        else None,
        "target_in_play_rmse_m": math.sqrt(sum(value * value for value in target_errors) / len(target_errors))
        if target_errors
        else None,
        "both_endpoints_within_2cm_count": len(both_under),
        "both_endpoints_within_2cm_sample_ids": both_under,
        "bottlenecks_over_2cm": [
            {
                "sample_id": row["sample_id"],
                "active_error_m": row.get("active_error_m"),
                "target_error_m": row.get("target_error_m"),
                "max_endpoint_error_m": row.get("max_endpoint_error_m"),
            }
            for row in in_play
            if float(row["active_error_m"]) > 0.02 or float(row["target_error_m"]) > 0.02
        ],
    }


def build_report() -> Dict[str, Any]:
    samples = _read_samples(DEFAULT_SAMPLES)
    oracle = _read_json(ORACLE_REPORT)
    oracle_by_sample = oracle.get("handoff_xy_oracle_by_sample") or {}
    rows = [
        _feature_row(samples[sample_id], oracle_row)
        for sample_id, oracle_row in sorted(oracle_by_sample.items(), key=lambda item: int(item[0]))
        if (oracle_row.get("target_error_m") is not None and samples.get(sample_id) is not None)
    ]
    feature_sets = {
        "headon_linear": ["target_before_y", "requested_v0"],
        "headon_plus_glance": ["target_before_y", "requested_v0", "is_glance", "is_right"],
        "approach_geometry": [
            "target_before_y",
            "requested_v0",
            "handoff_speed",
            "approach_normal_x",
            "approach_normal_y",
            "approach_tangent_x",
            "approach_tangent_y",
            "is_glance",
            "is_right",
        ],
    }
    models = []
    for name, features in feature_sets.items():
        predictions = _fit_predict_loo(rows, features)
        sim_rows = _simulate_predictions(samples, rows, predictions)
        models.append(
            {
                "name": name,
                "features": features,
                "loo_parameter_error_summary": _loo_summary(predictions),
                "endpoint_summary": _endpoint_summary(sim_rows),
                "predictions": predictions,
                "sim_rows": sim_rows,
            }
        )
    best_model = min(
        models,
        key=lambda item: float(item["endpoint_summary"].get("target_in_play_rmse_m") or float("inf")),
    )
    return {
        "question": "Can visible pre-collision features predict the per-sample entrance-state oracle well enough to keep collisions under 2cm?",
        "samples": str(DEFAULT_SAMPLES.relative_to(PROJECT_ROOT)),
        "oracle_source": str(ORACLE_REPORT.relative_to(PROJECT_ROOT)),
        "oracle_feature_rows": rows,
        "models": models,
        "best_model_by_target_rmse": {
            "name": best_model["name"],
            "endpoint_summary": best_model["endpoint_summary"],
        },
        "interpretation": [
            "This is intentionally a tiny-data leave-one-out audit, not a production correction model.",
            "If simple visible features cannot predict the oracle corrections, the current 2cm result remains a per-sample native-state proxy rather than a general simulator formula.",
            "The next trustworthy route would be either runtime contact/solver state capture or a larger controlled sample set for correction-model validation.",
        ],
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["best_model_by_target_rmse"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
