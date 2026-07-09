#!/usr/bin/env python3
"""Finite-difference sensitivity of target early velocity to replay inputs.

This diagnostic asks whether the target stone's missing 0.02s velocity can be
explained by a single global perturbation in handoff state, target placement,
yaw, radius, contact offset, or center height.  If the least-squares fit needs
implausibly large perturbations or still leaves a large residual, the mismatch
is more likely inside contact manifold/solver state than in a simple global
initial-condition offset.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse import probe_physx_collision_alignment as probe
from tools.reverse.analyze_collision_impulse_residual import _norm, _vec2


DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "unity_unique_role_collision_samples_20260708_r00.jsonl"
DEFAULT_PROBE = PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_current_best_20260708.json"
DEFAULT_IMPULSE = PROJECT_ROOT / "data" / "calibration" / "unity_collision_impulse_residual_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_early_velocity_sensitivity_20260709.json"


PARAMETERS = [
    {
        "name": "active_handoff_x_offset",
        "step": 0.001,
        "plausible_abs": 0.01,
        "description": "protocol x offset applied to active handoff pose",
    },
    {
        "name": "active_handoff_y_offset",
        "step": 0.001,
        "plausible_abs": 0.01,
        "description": "protocol y offset applied to active handoff pose",
    },
    {
        "name": "active_handoff_vx_offset",
        "step": 0.01,
        "plausible_abs": 0.05,
        "description": "protocol vx offset applied to active handoff velocity",
    },
    {
        "name": "active_handoff_vy_offset",
        "step": 0.01,
        "plausible_abs": 0.05,
        "description": "protocol vy offset applied to active handoff velocity",
    },
    {
        "name": "active_handoff_w_offset",
        "step": 0.01,
        "plausible_abs": 0.10,
        "description": "angular velocity offset applied to active handoff",
    },
    {
        "name": "target_x_offset",
        "step": 0.001,
        "plausible_abs": 0.01,
        "description": "protocol x offset applied to target reset position",
    },
    {
        "name": "target_y_offset",
        "step": 0.001,
        "plausible_abs": 0.01,
        "description": "protocol y offset applied to target reset position",
    },
    {
        "name": "active_yaw",
        "step": 0.001,
        "plausible_abs": 0.05,
        "description": "active initial yaw around vertical axis",
    },
    {
        "name": "target_yaw",
        "step": 0.001,
        "plausible_abs": 0.05,
        "description": "target initial yaw around vertical axis",
    },
    {
        "name": "radius",
        "step": 0.001,
        "plausible_abs": 0.01,
        "description": "stone convex radius, with explicit handoff held fixed",
    },
    {
        "name": "contact_offset",
        "step": 0.001,
        "plausible_abs": 0.005,
        "description": "shape contact offset",
    },
    {
        "name": "center_height",
        "step": 0.001,
        "plausible_abs": 0.01,
        "description": "actor center height",
    },
]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_samples(path: Path) -> Dict[int, Dict[str, Any]]:
    rows: Dict[int, Dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            sample = json.loads(line)
            rows[int(sample["sample_id"])] = sample
    return rows


def _best_result_set(payload: Dict[str, Any], result_index: Optional[int]) -> Dict[str, Any]:
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        raise ValueError("probe has no result_sets")
    if result_index is not None:
        return result_sets[result_index]
    return min(
        result_sets,
        key=lambda result_set: float("inf")
        if (result_set.get("summary") or {}).get("combined_rmse_m") is None
        else float((result_set.get("summary") or {})["combined_rmse_m"]),
    )


def _impulse_rows(path: Path) -> Dict[int, Dict[str, Any]]:
    payload = _read_json(path)
    current = None
    for result in payload.get("results", []):
        if result.get("label") == "unique_role_current_best":
            current = result
            break
    if current is None:
        results = payload.get("results", [])
        if not results:
            raise ValueError("impulse report has no results")
        current = results[0]
    return {
        int(row["sample_id"]): row
        for row in current.get("rows", [])
        if row.get("status") == "ok" and row.get("delta_v_required_mps") is not None
    }


def _float_config(config: Dict[str, Any], key: str, default: float) -> float:
    value = config.get(key)
    return default if value is None else float(value)


def _string_config(config: Dict[str, Any], key: str, default: str) -> str:
    value = config.get(key)
    return default if value is None else str(value)


def _bool_config(config: Dict[str, Any], key: str, default: bool = False) -> bool:
    value = config.get(key)
    return default if value is None else bool(value)


def _sample_with_explicit_handoff(
    base_sample: Dict[str, Any],
    base_row: Dict[str, Any],
    offsets: Dict[str, float],
) -> Dict[str, Any]:
    sample = copy.deepcopy(base_sample)
    handoff = copy.deepcopy(base_row["handoff"])
    handoff["x"] = float(handoff["x"]) + offsets.get("active_handoff_x_offset", 0.0)
    handoff["y"] = float(handoff["y"]) + offsets.get("active_handoff_y_offset", 0.0)
    handoff["vx"] = float(handoff["vx"]) + offsets.get("active_handoff_vx_offset", 0.0)
    handoff["vy"] = float(handoff["vy"]) + offsets.get("active_handoff_vy_offset", 0.0)
    handoff["w"] = float(handoff["w"]) + offsets.get("active_handoff_w_offset", 0.0)
    handoff["source"] = "sensitivity_explicit_handoff"
    sample["handoff_state"] = handoff

    target_index = int(sample["target_indices"][0])
    reset_position = list(sample["reset_position"])
    reset_position[2 * target_index] = float(reset_position[2 * target_index]) + offsets.get("target_x_offset", 0.0)
    reset_position[2 * target_index + 1] = float(reset_position[2 * target_index + 1]) + offsets.get("target_y_offset", 0.0)
    sample["reset_position"] = reset_position
    return sample


def _simulate_target_velocity(
    sample: Dict[str, Any],
    config: Dict[str, Any],
    offsets: Dict[str, float],
) -> Tuple[float, float]:
    scene_flag_names = config.get("scene_flags") or []
    if isinstance(scene_flag_names, str):
        scene_flag_names = [scene_flag_names]
    scene_flags = probe._scene_flags_from_names(scene_flag_names)
    combine_mode_name = _string_config(config, "combine_mode", "multiply")
    row = probe._simulate_one(
        sample,
        handoff_extra=_float_config(config, "handoff_extra", 0.0),
        ice_friction=_float_config(config, "ice_friction", 0.02),
        stone_friction=_float_config(config, "stone_friction", 0.6),
        stone_restitution=_float_config(config, "stone_restitution", 1.0),
        pre_collision_dynamic_friction=config.get("pre_collision_dynamic_friction"),
        pre_collision_static_friction=config.get("pre_collision_static_friction"),
        pre_collision_friction_scope=_string_config(config, "pre_collision_friction_scope", "both"),
        material_switch_mode=_string_config(config, "material_switch_mode", "post-step-distance"),
        radius=_float_config(config, "radius", probe.RADIUS) + offsets.get("radius", 0.0),
        height=_float_config(config, "height", probe.HEIGHT),
        stone_faces=int(config.get("stone_faces") or 256),
        inertia_model=_string_config(config, "inertia_model", "solid-cylinder"),
        inertia_radial=config.get("inertia_radial"),
        inertia_vertical=config.get("inertia_vertical"),
        active_yaw=_float_config(config, "active_yaw", 0.0) + offsets.get("active_yaw", 0.0),
        target_yaw=_float_config(config, "target_yaw", 0.0) + offsets.get("target_yaw", 0.0),
        center_height=_float_config(config, "center_height", probe.HEIGHT / 2.0) + offsets.get("center_height", 0.0),
        scene_flags=scene_flags,
        scene_flag_names=scene_flag_names,
        combine_mode=probe._combine_mode_from_name(combine_mode_name),
        combine_mode_name=combine_mode_name,
        contact_offset=_float_config(config, "contact_offset", 0.01) + offsets.get("contact_offset", 0.0),
        rest_offset=_float_config(config, "rest_offset", 0.0),
        shape_local_x=_float_config(config, "shape_local_x", 0.0),
        shape_local_y=_float_config(config, "shape_local_y", 0.0),
        shape_local_z=_float_config(config, "shape_local_z", 0.0),
        shape_local_yaw=_float_config(config, "shape_local_yaw", 0.0),
        convex_quantized_count=int(config.get("convex_quantized_count") or 255),
        convex_vertex_limit=int(config.get("convex_vertex_limit") or 255),
        quantize_input=_bool_config(config, "quantize_input", False),
        gpu_compatible=_bool_config(config, "gpu_compatible", False),
        solver_position_iterations=int(config.get("solver_position_iterations") or 6),
        solver_velocity_iterations=int(config.get("solver_velocity_iterations") or 1),
        max_depenetration_velocity=_float_config(config, "max_depenetration_velocity", 10.0),
        lock_upright=_bool_config(config, "lock_upright", False),
        disable_stone_gravity=_bool_config(config, "disable_stone_gravity", False),
        disable_strong_friction=_bool_config(config, "disable_strong_friction", False),
        improved_patch_friction=_bool_config(config, "improved_patch_friction", False),
        rink_geometry=_string_config(config, "rink_geometry", "plane"),
        rink_mesh_center_x=_float_config(config, "rink_mesh_center_x", probe.UNITY_PLANE_MESH_CENTER_X_M),
        rink_mesh_center_y=_float_config(config, "rink_mesh_center_y", probe.UNITY_PLANE_MESH_CENTER_Y_M),
        rink_mesh_width=_float_config(config, "rink_mesh_width", probe.UNITY_PLANE_MESH_WIDTH_M),
        rink_mesh_length=_float_config(config, "rink_mesh_length", probe.UNITY_PLANE_MESH_LENGTH_M),
        rink_mesh_subdivisions=int(config.get("rink_mesh_subdivisions") or probe.UNITY_PLANE_MESH_SUBDIVISIONS),
        use_unity_frame=_bool_config(config, "use_unity_frame", True),
        friction_offset_threshold=config.get("friction_offset_threshold"),
        dt=_float_config(config, "dt", 0.01),
        max_time=0.03,
        stop_speed=0.0,
        stop_frames=999999,
        snapshot_times=[0.02],
        handoff_friction=_float_config(config, "handoff_friction", probe.BASE_FRICTION),
        handoff_v_scale=_float_config(config, "handoff_v_scale", 1.0),
        angular_sign=_float_config(config, "angular_sign", 1.0),
        handoff_x_offset=0.0,
        handoff_y_offset=0.0,
    )
    return _vec2(row["snapshots"]["0.020000"]["target"]["linear_velocity"])


def _rmse_from_matrix(values: np.ndarray) -> float:
    if values.size == 0:
        return float("nan")
    return float(math.sqrt(float(np.mean(values * values))))


def build_report(
    samples_path: Path,
    probe_path: Path,
    impulse_path: Path,
    result_index: Optional[int],
) -> Dict[str, Any]:
    samples = _read_samples(samples_path)
    result_set = _best_result_set(_read_json(probe_path), result_index)
    config = result_set.get("config") or {}
    impulse_rows = _impulse_rows(impulse_path)

    baseline_rows = [row for row in result_set.get("rows", []) if int(row["sample_id"]) in impulse_rows]
    sample_ids = [int(row["sample_id"]) for row in baseline_rows]
    if not sample_ids:
        raise ValueError("no overlapping in-play target rows")

    baseline_velocities: List[Vector] = []
    desired_velocities: List[Vector] = []
    saved_velocities: List[Vector] = []
    per_sample: List[Dict[str, Any]] = []
    for row in baseline_rows:
        sample_id = int(row["sample_id"])
        sample = _sample_with_explicit_handoff(samples[sample_id], row, {})
        baseline_velocity = _simulate_target_velocity(sample, config, {})
        saved_velocity = _vec2(row["snapshots"]["0.020000"]["target"]["linear_velocity"])
        required_delta = _vec2(impulse_rows[sample_id]["delta_v_required_mps"])
        desired_velocity = (saved_velocity[0] + required_delta[0], saved_velocity[1] + required_delta[1])
        baseline_velocities.append(baseline_velocity)
        saved_velocities.append(saved_velocity)
        desired_velocities.append(desired_velocity)
        per_sample.append(
            {
                "sample_id": sample_id,
                "label": row.get("label"),
                "saved_target_velocity_0p02_mps": list(saved_velocity),
                "rerun_baseline_target_velocity_0p02_mps": list(baseline_velocity),
                "baseline_rerun_delta_norm_mps": float(_norm((baseline_velocity[0] - saved_velocity[0], baseline_velocity[1] - saved_velocity[1]))),
                "desired_target_velocity_0p02_mps": list(desired_velocity),
                "required_delta_v_mps": list(required_delta),
                "required_delta_v_norm_mps": float(_norm(required_delta)),
            }
        )

    y = np.asarray(
        [
            component
            for desired, baseline in zip(desired_velocities, baseline_velocities)
            for component in (desired[0] - baseline[0], desired[1] - baseline[1])
        ],
        dtype=float,
    )

    columns: List[np.ndarray] = []
    parameter_reports: List[Dict[str, Any]] = []
    for spec in PARAMETERS:
        name = spec["name"]
        step = float(spec["step"])
        perturbed: List[Vector] = []
        for row in baseline_rows:
            sample_id = int(row["sample_id"])
            offsets = {name: step}
            sample = _sample_with_explicit_handoff(samples[sample_id], row, offsets)
            velocity = _simulate_target_velocity(sample, config, offsets)
            perturbed.append(velocity)
        derivative = np.asarray(
            [
                component
                for pert, base in zip(perturbed, baseline_velocities)
                for component in ((pert[0] - base[0]) / step, (pert[1] - base[1]) / step)
            ],
            dtype=float,
        )
        columns.append(derivative)
        parameter_reports.append(
            {
                "name": name,
                "finite_difference_step": step,
                "plausible_abs": spec["plausible_abs"],
                "description": spec["description"],
                "sensitivity_norm_per_unit": float(np.linalg.norm(derivative)),
            }
        )

    sensitivity = np.column_stack(columns)
    solution, residuals, rank, singular_values = np.linalg.lstsq(sensitivity, y, rcond=None)
    fitted = sensitivity @ solution
    residual = y - fitted
    baseline_rmse = _rmse_from_matrix(y)
    fitted_rmse = _rmse_from_matrix(residual)
    plausible_bounds = np.asarray([float(spec["plausible_abs"]) for spec in PARAMETERS], dtype=float)
    clipped_solution = np.clip(solution, -plausible_bounds, plausible_bounds)
    clipped_fitted = sensitivity @ clipped_solution
    clipped_residual = y - clipped_fitted
    clipped_rmse = _rmse_from_matrix(clipped_residual)

    for index, spec in enumerate(PARAMETERS):
        plausible = float(spec["plausible_abs"])
        value = float(solution[index])
        parameter_reports[index]["least_squares_value"] = value
        parameter_reports[index]["abs_over_plausible"] = None if plausible <= 0.0 else abs(value) / plausible
        parameter_reports[index]["plausible_clipped_value"] = float(clipped_solution[index])

    for sample_index, item in enumerate(per_sample):
        base_delta = y[2 * sample_index : 2 * sample_index + 2]
        fit_delta = fitted[2 * sample_index : 2 * sample_index + 2]
        rem_delta = residual[2 * sample_index : 2 * sample_index + 2]
        item["least_squares_fit_delta_v_mps"] = [float(fit_delta[0]), float(fit_delta[1])]
        item["least_squares_residual_delta_v_mps"] = [float(rem_delta[0]), float(rem_delta[1])]
        item["least_squares_residual_norm_mps"] = float(np.linalg.norm(rem_delta))
        item["baseline_delta_norm_from_rerun_mps"] = float(np.linalg.norm(base_delta))
        clipped_fit_delta = clipped_fitted[2 * sample_index : 2 * sample_index + 2]
        clipped_rem_delta = clipped_residual[2 * sample_index : 2 * sample_index + 2]
        item["plausible_clipped_fit_delta_v_mps"] = [float(clipped_fit_delta[0]), float(clipped_fit_delta[1])]
        item["plausible_clipped_residual_delta_v_mps"] = [float(clipped_rem_delta[0]), float(clipped_rem_delta[1])]
        item["plausible_clipped_residual_norm_mps"] = float(np.linalg.norm(clipped_rem_delta))

    return {
        "samples": str(samples_path.relative_to(PROJECT_ROOT)),
        "probe": str(probe_path.relative_to(PROJECT_ROOT)),
        "impulse_report": str(impulse_path.relative_to(PROJECT_ROOT)),
        "sample_count": len(sample_ids),
        "sample_ids": sample_ids,
        "target": "target linear velocity at t=0.02s",
        "baseline_required_delta_rmse_mps": baseline_rmse,
        "least_squares_residual_rmse_mps": fitted_rmse,
        "plausible_clipped_residual_rmse_mps": clipped_rmse,
        "least_squares_rank": int(rank),
        "singular_values": [float(value) for value in singular_values],
        "parameters": parameter_reports,
        "per_sample": per_sample,
        "interpretation": [
            "This fit is intentionally linearized around the current-best replay and uses explicit baseline handoff so radius sensitivity is isolated from handoff-threshold changes.",
            "Large abs_over_plausible values mean a simple global initial-state or geometry offset would need to be unrealistically large.",
            "A poor residual after this fit points back to per-contact runtime state: manifold/cache/solver rows/cooked stream rather than one global scalar.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--impulse", type=Path, default=DEFAULT_IMPULSE)
    parser.add_argument("--result-index", type=int, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    samples_path = args.samples if args.samples.is_absolute() else PROJECT_ROOT / args.samples
    probe_path = args.probe if args.probe.is_absolute() else PROJECT_ROOT / args.probe
    impulse_path = args.impulse if args.impulse.is_absolute() else PROJECT_ROOT / args.impulse
    output = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    report = build_report(samples_path, probe_path, impulse_path, args.result_index)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {output.relative_to(PROJECT_ROOT)}")
    print(f"sample_count={report['sample_count']}")
    print(f"baseline_required_delta_rmse_mps={report['baseline_required_delta_rmse_mps']:.6f}")
    print(f"least_squares_residual_rmse_mps={report['least_squares_residual_rmse_mps']:.6f}")
    print(f"plausible_clipped_residual_rmse_mps={report['plausible_clipped_residual_rmse_mps']:.6f}")
    print("largest parameters:")
    for item in sorted(report["parameters"], key=lambda row: abs(row["least_squares_value"]), reverse=True)[:5]:
        print(
            f"- {item['name']}={item['least_squares_value']:.6g} "
            f"(abs/plausible={item['abs_over_plausible']:.3f})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
