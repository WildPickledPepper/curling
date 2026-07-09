#!/usr/bin/env python3
"""Measure the best possible collision error inside existing probe grids.

This is an offline diagnostic. It does not fit new parameters and does not run
Unity/PhysX. Instead, it asks a narrower question: among the probe results we
have already generated, could any already-tested parameter set explain each
unique-role collision sample to the 2 cm level?
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GLOB = "unity_physx_collision_probe_unique_role*.json"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_parameter_oracle_floor_20260709.json"
)
THRESHOLD_M = 0.02

SUMMARY_RMSE_KEYS = (
    "combined_rmse_m",
    "target_in_play_rmse_m",
    "target_rmse_m",
    "active_rmse_m",
)
ROW_PARAM_KEYS = (
    "handoff_friction",
    "handoff_v_scale",
    "handoff_x_offset",
    "handoff_y_offset",
    "combine_mode",
    "friction_offset_threshold",
    "pre_collision_dynamic_friction",
    "pre_collision_static_friction",
    "pre_collision_friction_scope",
    "ice_friction",
    "stone_friction",
    "stone_restitution",
    "radius",
    "height",
    "stone_faces",
    "inertia_model",
    "inertia_radial",
    "inertia_vertical",
    "active_yaw",
    "target_yaw",
    "center_height",
    "shape_local_x",
    "shape_local_y",
    "shape_local_z",
    "shape_local_yaw",
    "scene_flags",
    "solver_position_iterations",
    "solver_velocity_iterations",
    "max_depenetration_velocity",
    "convex_quantized_count",
    "convex_vertex_limit",
    "contact_offset",
    "rest_offset",
    "lock_upright",
    "disable_stone_gravity",
    "disable_strong_friction",
    "improved_patch_friction",
    "rink_geometry",
    "rink_mesh_center_x",
    "rink_mesh_center_y",
    "rink_mesh_width",
    "rink_mesh_length",
    "rink_mesh_subdivisions",
    "material_switch_time",
    "material_switch_distance",
)


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _score_summary(summary: Dict[str, Any]) -> float:
    for key in SUMMARY_RMSE_KEYS:
        value = summary.get(key)
        if value is not None:
            return float(value)
    return float("inf")


def _rmse(values: Sequence[float]) -> Optional[float]:
    if not values:
        return None
    return math.sqrt(sum(value * value for value in values) / len(values))


def _mean(values: Sequence[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    return float(value)


def _row_config(result_set: Dict[str, Any], row: Dict[str, Any]) -> Dict[str, Any]:
    config = dict(result_set.get("config") or {})
    for key in ROW_PARAM_KEYS:
        if key in row and key not in config:
            config[key] = row[key]
    return config


def _compact_config(config: Dict[str, Any]) -> Dict[str, Any]:
    # Keep the report readable while still showing which hypothesis won.
    keys = [
        "handoff_extra",
        "handoff_friction",
        "handoff_v_scale",
        "handoff_x_offset",
        "handoff_y_offset",
        "ice_friction",
        "stone_friction",
        "stone_restitution",
        "radius",
        "height",
        "stone_faces",
        "inertia_model",
        "inertia_radial",
        "inertia_vertical",
        "active_yaw",
        "target_yaw",
        "center_height",
        "shape_local_x",
        "shape_local_y",
        "shape_local_z",
        "shape_local_yaw",
        "combine_mode",
        "contact_offset",
        "rest_offset",
        "solver_position_iterations",
        "solver_velocity_iterations",
        "lock_upright",
        "disable_stone_gravity",
        "rink_geometry",
        "rink_mesh_center_x",
        "rink_mesh_center_y",
        "rink_mesh_width",
        "rink_mesh_length",
        "rink_mesh_subdivisions",
        "convex_quantized_count",
        "convex_vertex_limit",
        "scene_flags",
        "use_unity_frame",
        "dt",
    ]
    return {key: config.get(key) for key in keys if key in config}


def _row_error_pair(row: Dict[str, Any]) -> Optional[float]:
    active_error = _safe_float(row.get("active_error"))
    target_error = _safe_float(row.get("target_error"))
    if active_error is None or target_error is None:
        return None
    return math.sqrt((active_error * active_error + target_error * target_error) / 2.0)


def _is_probe_payload(payload: Dict[str, Any]) -> bool:
    result_sets = payload.get("result_sets")
    return isinstance(result_sets, list) and bool(result_sets)


def _iter_probe_paths(calibration_dir: Path, patterns: Sequence[str], explicit_paths: Sequence[Path]) -> List[Path]:
    paths: Dict[Path, None] = {}
    for pattern in patterns:
        for path in calibration_dir.glob(pattern):
            if path.is_file():
                paths[path.resolve()] = None
    for path in explicit_paths:
        if path.is_file():
            paths[path.resolve()] = None
    return sorted(paths)


def _sample_metadata_from_payload(payload: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    metadata: Dict[int, Dict[str, Any]] = {}
    for sample in payload.get("samples") or []:
        try:
            sample_id = int(sample["sample_id"])
        except (KeyError, TypeError, ValueError):
            continue
        plan_metadata = sample.get("plan_metadata") or {}
        metadata[sample_id] = {
            "sample_id": sample_id,
            "label": sample.get("label"),
            "category": sample.get("category"),
            "source_sample_id": plan_metadata.get("source_sample_id"),
            "active_index": (sample.get("active_move") or {}).get("index"),
            "target_indices": sample.get("target_indices"),
        }
    return metadata


def _better_target(candidate: Dict[str, Any], current: Optional[Dict[str, Any]]) -> bool:
    if current is None:
        return True
    return float(candidate["target_error_m"]) < float(current["target_error_m"])


def _better_pair(candidate: Dict[str, Any], current: Optional[Dict[str, Any]]) -> bool:
    if current is None:
        return True
    return float(candidate["pair_rmse_m"]) < float(current["pair_rmse_m"])


def analyze(paths: Sequence[Path]) -> Dict[str, Any]:
    sample_metadata: Dict[int, Dict[str, Any]] = {}
    file_reports: List[Dict[str, Any]] = []
    best_target_by_sample: Dict[int, Dict[str, Any]] = {}
    best_pair_by_sample: Dict[int, Dict[str, Any]] = {}
    global_result_sets: List[Dict[str, Any]] = []
    total_result_sets = 0
    total_rows = 0

    for path in paths:
        payload = _read_json(path)
        if not _is_probe_payload(payload):
            continue
        sample_metadata.update(_sample_metadata_from_payload(payload))
        result_sets = payload.get("result_sets") or []
        total_result_sets += len(result_sets)
        best_for_file: Optional[Dict[str, Any]] = None
        file_target_rows = 0
        file_pair_rows = 0

        for result_index, result_set in enumerate(result_sets):
            rows = result_set.get("rows") or []
            total_rows += len(rows)
            summary = result_set.get("summary") or {}
            score = _score_summary(summary)
            candidate_global = {
                "file": str(path.relative_to(PROJECT_ROOT)),
                "result_index": result_index,
                "score": score,
                "summary": summary,
                "config": _compact_config(result_set.get("config") or {}),
            }
            global_result_sets.append(candidate_global)
            if best_for_file is None or score < float(best_for_file["score"]):
                best_for_file = candidate_global

            for row in rows:
                try:
                    sample_id = int(row["sample_id"])
                except (KeyError, TypeError, ValueError):
                    continue
                config = _compact_config(_row_config(result_set, row))
                active_error = _safe_float(row.get("active_error"))
                target_error = _safe_float(row.get("target_error"))
                if target_error is not None:
                    file_target_rows += 1
                    candidate = {
                        "sample_id": sample_id,
                        "label": row.get("label"),
                        "target_index": row.get("target_index"),
                        "target_error_m": target_error,
                        "active_error_m": active_error,
                        "file": str(path.relative_to(PROJECT_ROOT)),
                        "result_index": result_index,
                        "config": config,
                        "sim_target": row.get("sim_target"),
                        "unity_target": row.get("unity_target"),
                        "sim_active": row.get("sim_active"),
                        "unity_active": row.get("unity_active"),
                    }
                    if _better_target(candidate, best_target_by_sample.get(sample_id)):
                        best_target_by_sample[sample_id] = candidate
                pair_rmse = _row_error_pair(row)
                if pair_rmse is not None:
                    file_pair_rows += 1
                    candidate_pair = {
                        "sample_id": sample_id,
                        "label": row.get("label"),
                        "target_index": row.get("target_index"),
                        "pair_rmse_m": pair_rmse,
                        "target_error_m": target_error,
                        "active_error_m": active_error,
                        "file": str(path.relative_to(PROJECT_ROOT)),
                        "result_index": result_index,
                        "config": config,
                    }
                    if _better_pair(candidate_pair, best_pair_by_sample.get(sample_id)):
                        best_pair_by_sample[sample_id] = candidate_pair

        file_reports.append(
            {
                "file": str(path.relative_to(PROJECT_ROOT)),
                "result_set_count": len(result_sets),
                "target_row_count": file_target_rows,
                "pair_row_count": file_pair_rows,
                "best_global": best_for_file,
            }
        )

    best_target_rows = [
        {**sample_metadata.get(sample_id, {}), **row}
        for sample_id, row in sorted(best_target_by_sample.items())
    ]
    best_pair_rows = [
        {**sample_metadata.get(sample_id, {}), **row}
        for sample_id, row in sorted(best_pair_by_sample.items())
    ]
    target_values = [float(row["target_error_m"]) for row in best_target_rows]
    pair_values = [float(row["pair_rmse_m"]) for row in best_pair_rows]
    over_target = [row for row in best_target_rows if float(row["target_error_m"]) > THRESHOLD_M]
    over_pair = [row for row in best_pair_rows if float(row["pair_rmse_m"]) > THRESHOLD_M]
    both_within = [
        row
        for row in best_pair_rows
        if float(row["pair_rmse_m"]) <= THRESHOLD_M
        and float(row["target_error_m"]) <= THRESHOLD_M
        and float(row["active_error_m"]) <= THRESHOLD_M
    ]

    global_result_sets.sort(key=lambda item: float(item["score"]))
    file_reports.sort(
        key=lambda item: float((item.get("best_global") or {}).get("score", float("inf")))
    )

    return {
        "probe_files": [str(path.relative_to(PROJECT_ROOT)) for path in paths],
        "threshold_m": THRESHOLD_M,
        "processed_probe_file_count": len(file_reports),
        "processed_result_set_count": total_result_sets,
        "processed_row_count": total_rows,
        "best_global_result_sets": global_result_sets[:20],
        "file_reports": file_reports,
        "target_only_oracle": {
            "sample_count": len(best_target_rows),
            "rmse_m": _rmse(target_values),
            "mean_m": _mean(target_values),
            "max_m": max(target_values) if target_values else None,
            "within_2cm_count": len(best_target_rows) - len(over_target),
            "over_2cm_count": len(over_target),
            "over_2cm_sample_ids": [row["sample_id"] for row in over_target],
            "per_sample_best": best_target_rows,
        },
        "active_and_target_pair_oracle": {
            "sample_count": len(best_pair_rows),
            "pair_rmse_floor_m": _rmse(pair_values),
            "pair_mean_m": _mean(pair_values),
            "pair_max_m": max(pair_values) if pair_values else None,
            "pair_within_2cm_count": len(best_pair_rows) - len(over_pair),
            "pair_over_2cm_count": len(over_pair),
            "pair_over_2cm_sample_ids": [row["sample_id"] for row in over_pair],
            "both_active_and_target_individually_within_2cm_count": len(both_within),
            "per_sample_best": best_pair_rows,
        },
        "interpretation": {
            "target": (
                "If target_only_oracle still has many rows over 2 cm, the current probe grids "
                "cannot explain Unity target endpoints even with per-sample parameter choice."
            ),
            "pair": (
                "If pair oracle is worse than target-only oracle, tuning one stone endpoint is "
                "trading off the other; that points to a missing state/contact-model detail, "
                "not a single global scalar."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--calibration-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "calibration",
    )
    parser.add_argument(
        "--glob",
        action="append",
        default=[DEFAULT_GLOB],
        help="Probe file glob relative to --calibration-dir. Can be repeated.",
    )
    parser.add_argument(
        "--probe",
        action="append",
        type=Path,
        default=[],
        help="Explicit probe JSON path. Can be repeated.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    paths = _iter_probe_paths(args.calibration_dir, args.glob, args.probe)
    if not paths:
        raise SystemExit("no probe files found")

    report = analyze(paths)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    target = report["target_only_oracle"]
    pair = report["active_and_target_pair_oracle"]
    print(f"processed probe files: {report['processed_probe_file_count']}")
    print(f"processed result sets: {report['processed_result_set_count']}")
    print(
        "target-only oracle: "
        f"rmse={target['rmse_m']:.6f} m, "
        f"over_2cm={target['over_2cm_count']}/{target['sample_count']}"
    )
    print(
        "active+target pair oracle: "
        f"rmse_floor={pair['pair_rmse_floor_m']:.6f} m, "
        f"pair_over_2cm={pair['pair_over_2cm_count']}/{pair['sample_count']}, "
        "both_individual_within_2cm="
        f"{pair['both_active_and_target_individually_within_2cm_count']}/{pair['sample_count']}"
    )
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
