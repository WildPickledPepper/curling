#!/usr/bin/env python3
"""Replay the post-collision tail from local snapshots with optional velocity correction.

This is a diagnostic, not a simulator patch.  It asks whether the current
endpoint residual can be explained by the target stone's early post-collision
velocity alone.  For each sample it starts a fresh pyphysx scene from an
existing local snapshot, first with the snapshot velocity unchanged and then
with the target linear velocity replaced by the Unity-implied velocity from
``analyze_collision_impulse_residual``.
"""

from __future__ import annotations

import argparse
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
from tools.reverse.analyze_collision_impulse_residual import _row_residual


DEFAULT_PROBE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_current_best_step_snapshots_20260709.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_tail_replay_oracle_20260709.json"


Vec2 = Tuple[float, float]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _vec2(values: Sequence[float]) -> Vec2:
    return (float(values[0]), float(values[1]))


def _dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1]))


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return float(a[0]) * float(b[0]) + float(a[1]) * float(b[1])


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = [float(value) for value in values if value is not None]
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _mean(values: Iterable[float]) -> Optional[float]:
    rows = [float(value) for value in values if value is not None]
    if not rows:
        return None
    return sum(rows) / len(rows)


def _result_set(payload: Dict[str, Any], result_index: int) -> Dict[str, Any]:
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        raise ValueError("probe has no result_sets")
    return result_sets[result_index]


def _scene_flags(config: Dict[str, Any]) -> List[Any]:
    return probe._scene_flags_from_names(config.get("scene_flags") or [])


def _combine(config: Dict[str, Any]) -> Any:
    return probe._combine_mode_from_name(str(config.get("combine_mode") or "multiply"))


def _stone_points_from_config(config: Dict[str, Any]) -> np.ndarray:
    radius = float(config.get("radius", probe.RADIUS))
    height = float(config.get("height", probe.HEIGHT))
    stone_faces = int(config.get("stone_faces", 256))
    if str(config.get("stone_geometry") or "ring") == "formal-recovered":
        mesh_path_value = config.get("formal_stone_mesh") or probe.DEFAULT_FORMAL_STONE_MESH
        mesh_path = Path(mesh_path_value)
        if not mesh_path.is_absolute():
            mesh_path = PROJECT_ROOT / mesh_path
        scale = config.get("formal_stone_scale") or [1.0, 1.0, 1.0]
        return probe._formal_stone_points(
            mesh_path,
            scale_x=float(scale[0]),
            scale_y=float(scale[1]),
            scale_z=float(scale[2]),
        )
    return probe._stone_points(radius=radius, height=height, faces=stone_faces)


def _add_ice(scene: Any, config: Dict[str, Any], combine_mode: Any) -> None:
    ice_material = probe._make_material(
        float(config.get("ice_friction", 0.02)),
        float(config.get("ice_friction", 0.02)),
        0.0,
        combine_mode=combine_mode,
        disable_strong_friction=bool(config.get("disable_strong_friction", False)),
        improved_patch_friction=bool(config.get("improved_patch_friction", False)),
    )
    rink_geometry = str(config.get("rink_geometry") or "plane")
    use_unity_frame = bool(config.get("use_unity_frame", True))
    if rink_geometry == "plane":
        ice = probe.pyphysx.RigidStatic.create_plane(ice_material, 0.0, 0.0, 1.0, 0.0)
    elif rink_geometry == "unity-plane-mesh":
        points, triangles = probe._unity_plane_mesh(
            center_x=float(config.get("rink_mesh_center_x", probe.UNITY_PLANE_MESH_CENTER_X_M)),
            center_y=float(config.get("rink_mesh_center_y", probe.UNITY_PLANE_MESH_CENTER_Y_M)),
            width=float(config.get("rink_mesh_width", probe.UNITY_PLANE_MESH_WIDTH_M)),
            length=float(config.get("rink_mesh_length", probe.UNITY_PLANE_MESH_LENGTH_M)),
            subdivisions=int(config.get("rink_mesh_subdivisions", probe.UNITY_PLANE_MESH_SUBDIVISIONS)),
            use_unity_frame=use_unity_frame,
        )
        ice_shape = probe.pyphysx.Shape.create_triangle_mesh_from_points(
            points,
            triangles,
            ice_material,
            True,
            1.0,
            True,
            False,
            False,
            False,
            True,
            False,
        )
        ice = probe.pyphysx.RigidStatic()
        ice.attach_shape(ice_shape)
    else:
        raise ValueError(f"unsupported rink geometry: {rink_geometry}")

    for shape in ice.get_atached_shapes():
        shape.set_contact_offset(float(config.get("contact_offset", 0.01)))
        shape.set_rest_offset(float(config.get("rest_offset", 0.0)))
    scene.add_actor(ice)


def _make_target_from_snapshot(
    snapshot: Dict[str, Any],
    config: Dict[str, Any],
    *,
    corrected_velocity_protocol: Optional[Sequence[float]],
    combine_mode: Any,
) -> Any:
    use_unity_frame = bool(config.get("use_unity_frame", True))
    physx_position = [float(value) for value in snapshot["physx_position"]]
    physx_quaternion = [float(value) for value in snapshot["physx_quaternion"]]
    physx_velocity = [float(value) for value in snapshot["physx_linear_velocity"]]
    physx_angular = [float(value) for value in snapshot["physx_angular_velocity"]]
    if corrected_velocity_protocol is not None:
        vx, vy = probe._to_physx_xy(
            float(corrected_velocity_protocol[0]),
            float(corrected_velocity_protocol[1]),
            use_unity_frame,
        )
        physx_velocity[0] = vx
        physx_velocity[1] = vy

    stone_points = _stone_points_from_config(config)
    actor, _shape, _material = probe._make_stone(
        physx_position[0],
        physx_position[1],
        physx_velocity[0],
        physx_velocity[1],
        physx_angular[2],
        0.0,
        stone_points=stone_points,
        radius=float(config.get("radius", probe.RADIUS)),
        height=float(config.get("height", probe.HEIGHT)),
        stone_faces=int(config.get("stone_faces", 256)),
        inertia_model=str(config.get("inertia_model") or "solid-cylinder"),
        inertia_radial=config.get("inertia_radial"),
        inertia_vertical=config.get("inertia_vertical"),
        center_height=physx_position[2],
        stone_friction=float(config.get("stone_friction", 0.6)),
        static_friction=float(config.get("stone_friction", 0.6)),
        dynamic_friction=float(config.get("stone_friction", 0.6)),
        stone_restitution=float(config.get("stone_restitution", 1.0)),
        combine_mode=combine_mode,
        contact_offset=float(config.get("contact_offset", 0.01)),
        rest_offset=float(config.get("rest_offset", 0.0)),
        shape_local_x=float(config.get("shape_local_x", 0.0)),
        shape_local_y=float(config.get("shape_local_y", 0.0)),
        shape_local_z=float(config.get("shape_local_z", 0.0)),
        shape_local_yaw=float(config.get("shape_local_yaw", 0.0)),
        convex_quantized_count=int(config.get("convex_quantized_count", 255)),
        convex_vertex_limit=int(config.get("convex_vertex_limit", 255)),
        quantize_input=bool(config.get("quantize_input", False)),
        gpu_compatible=bool(config.get("gpu_compatible", False)),
        solver_position_iterations=int(config.get("solver_position_iterations", 6)),
        solver_velocity_iterations=int(config.get("solver_velocity_iterations", 1)),
        max_depenetration_velocity=float(config.get("max_depenetration_velocity", 10.0)),
        lock_upright=bool(config.get("lock_upright", False)),
        disable_stone_gravity=bool(config.get("disable_stone_gravity", False)),
        disable_strong_friction=bool(config.get("disable_strong_friction", False)),
        improved_patch_friction=bool(config.get("improved_patch_friction", False)),
    )
    actor.set_global_pose((physx_position, physx_quaternion))
    actor.set_linear_velocity(physx_velocity)
    actor.set_angular_velocity(physx_angular)
    return actor


def _simulate_tail(
    snapshot: Dict[str, Any],
    config: Dict[str, Any],
    *,
    corrected_velocity_protocol: Optional[Sequence[float]],
    dt: float,
    max_time: float,
    stop_speed: float,
    stop_frames: int,
) -> Dict[str, Any]:
    scene_kwargs = {"bounce_threshold_velocity": 0.05}
    if config.get("friction_offset_threshold") is not None:
        scene_kwargs["friction_offset_threshold"] = float(config["friction_offset_threshold"])
    scene = probe.pyphysx.Scene(scene_flags=_scene_flags(config), **scene_kwargs)
    combine_mode = _combine(config)
    _add_ice(scene, config, combine_mode)
    target = _make_target_from_snapshot(
        snapshot,
        config,
        corrected_velocity_protocol=corrected_velocity_protocol,
        combine_mode=combine_mode,
    )
    scene.add_actor(target)

    still_count = 0
    elapsed = max_time
    for step_index in range(int(max_time / dt)):
        scene.simulate(dt)
        speed = float(np.linalg.norm(probe._linear_velocity(target)[:2]))
        angular_z = abs(float(probe._angular_velocity(target)[2]))
        if speed < stop_speed and angular_z < 0.05:
            still_count += 1
            if still_count >= stop_frames:
                elapsed = (step_index + 1) * dt
                break
        else:
            still_count = 0

    xy = probe._pose_xy(target)
    endpoint = probe._from_physx_xy(float(xy[0]), float(xy[1]), bool(config.get("use_unity_frame", True)))
    final_snapshot = probe._actor_snapshot(target, bool(config.get("use_unity_frame", True)))
    return {
        "endpoint": list(endpoint),
        "elapsed_s": elapsed,
        "final_linear_speed": final_snapshot["linear_speed"],
        "final_angular_velocity": final_snapshot["angular_velocity"],
    }


def _velocity_oracle(
    snapshot: Dict[str, Any],
    config: Dict[str, Any],
    *,
    unity_target: Sequence[float],
    initial_velocity_protocol: Sequence[float],
    dt: float,
    max_time: float,
    stop_speed: float,
    stop_frames: int,
    max_iterations: int,
    finite_diff_eps: float,
) -> Dict[str, Any]:
    velocity = np.asarray(initial_velocity_protocol, dtype=float)
    initial = velocity.copy()
    best = _simulate_tail(
        snapshot,
        config,
        corrected_velocity_protocol=velocity,
        dt=dt,
        max_time=max_time,
        stop_speed=stop_speed,
        stop_frames=stop_frames,
    )
    best_error = _dist(best["endpoint"], unity_target)
    iterations = []

    for iteration in range(max_iterations):
        base_endpoint = np.asarray(best["endpoint"], dtype=float)
        residual = np.asarray(unity_target, dtype=float) - base_endpoint
        if float(np.linalg.norm(residual)) <= 0.002:
            break

        jacobian = np.zeros((2, 2), dtype=float)
        eps = max(finite_diff_eps, 0.0025 * max(1.0, float(np.linalg.norm(velocity))))
        for axis in range(2):
            trial_velocity = velocity.copy()
            trial_velocity[axis] += eps
            trial = _simulate_tail(
                snapshot,
                config,
                corrected_velocity_protocol=trial_velocity,
                dt=dt,
                max_time=max_time,
                stop_speed=stop_speed,
                stop_frames=stop_frames,
            )
            jacobian[:, axis] = (np.asarray(trial["endpoint"], dtype=float) - base_endpoint) / eps

        try:
            delta, *_ = np.linalg.lstsq(jacobian, residual, rcond=None)
        except np.linalg.LinAlgError:
            break
        delta_norm = float(np.linalg.norm(delta))
        if not math.isfinite(delta_norm) or delta_norm <= 1e-12:
            break
        if delta_norm > 0.25:
            delta *= 0.25 / delta_norm

        chosen = None
        for damping in (1.0, 0.5, 0.25, 0.1):
            trial_velocity = velocity + damping * delta
            trial = _simulate_tail(
                snapshot,
                config,
                corrected_velocity_protocol=trial_velocity,
                dt=dt,
                max_time=max_time,
                stop_speed=stop_speed,
                stop_frames=stop_frames,
            )
            trial_error = _dist(trial["endpoint"], unity_target)
            if chosen is None or trial_error < chosen["error_m"]:
                chosen = {
                    "velocity": trial_velocity,
                    "endpoint": trial,
                    "error_m": trial_error,
                    "damping": damping,
                }

        iterations.append(
            {
                "iteration": iteration,
                "error_before_m": best_error,
                "delta_v_mps": [float(value) for value in delta],
                "jacobian": jacobian.tolist(),
                "chosen_damping": None if chosen is None else chosen["damping"],
                "error_after_m": None if chosen is None else chosen["error_m"],
            }
        )
        if chosen is None or chosen["error_m"] >= best_error - 1e-6:
            break
        velocity = np.asarray(chosen["velocity"], dtype=float)
        best = chosen["endpoint"]
        best_error = float(chosen["error_m"])

    return {
        "endpoint": best["endpoint"],
        "error_m": best_error,
        "velocity_protocol": [float(value) for value in velocity],
        "delta_v_from_snapshot_mps": [float(value) for value in (velocity - initial)],
        "delta_v_norm_from_snapshot_mps": float(np.linalg.norm(velocity - initial)),
        "iterations": iterations,
    }


def _row_report(
    row: Dict[str, Any],
    config: Dict[str, Any],
    *,
    snapshot_time: float,
    dt: float,
    max_time: float,
    stop_speed: float,
    stop_frames: int,
) -> Dict[str, Any]:
    residual = _row_residual(row, snapshot_time)
    if residual.get("status") != "ok":
        return {"sample_id": row.get("sample_id"), "status": residual.get("status"), "residual": residual}
    snapshot_key = str(residual["snapshot_key"])
    snapshot = (row.get("snapshots") or {})[snapshot_key]["target"]
    unity_target = _vec2(row["unity_target"])
    local_target = _vec2(row["sim_target"])

    baseline = _simulate_tail(
        snapshot,
        config,
        corrected_velocity_protocol=None,
        dt=dt,
        max_time=max_time,
        stop_speed=stop_speed,
        stop_frames=stop_frames,
    )
    corrected = _simulate_tail(
        snapshot,
        config,
        corrected_velocity_protocol=residual.get("required_early_velocity"),
        dt=dt,
        max_time=max_time,
        stop_speed=stop_speed,
        stop_frames=stop_frames,
    )
    oracle = _velocity_oracle(
        snapshot,
        config,
        unity_target=unity_target,
        initial_velocity_protocol=snapshot["linear_velocity"],
        dt=dt,
        max_time=max_time,
        stop_speed=stop_speed,
        stop_frames=stop_frames,
        max_iterations=5,
        finite_diff_eps=0.005,
    )
    contact_normal = residual.get("contact_normal") or [0.0, -1.0]
    contact_tangent = residual.get("contact_tangent") or [1.0, 0.0]
    oracle_delta = oracle["delta_v_from_snapshot_mps"]
    oracle_delta_normal = _dot(oracle_delta, contact_normal)
    oracle_delta_tangent = _dot(oracle_delta, contact_tangent)
    if abs(oracle_delta_tangent) > 1.25 * abs(oracle_delta_normal):
        oracle_component = "tangent"
    elif abs(oracle_delta_normal) > 1.25 * abs(oracle_delta_tangent):
        oracle_component = "normal"
    else:
        oracle_component = "mixed"

    return {
        "sample_id": int(row["sample_id"]),
        "label": row.get("label"),
        "status": "ok",
        "snapshot_key": snapshot_key,
        "unity_target": list(unity_target),
        "local_full_replay_target": list(local_target),
        "baseline_tail_endpoint": baseline["endpoint"],
        "corrected_tail_endpoint": corrected["endpoint"],
        "oracle_linear_tail_endpoint": oracle["endpoint"],
        "baseline_tail_vs_local_full_m": _dist(baseline["endpoint"], local_target),
        "baseline_tail_vs_unity_m": _dist(baseline["endpoint"], unity_target),
        "local_full_vs_unity_m": _dist(local_target, unity_target),
        "corrected_tail_vs_unity_m": _dist(corrected["endpoint"], unity_target),
        "oracle_linear_tail_vs_unity_m": oracle["error_m"],
        "corrected_tail_vs_local_full_m": _dist(corrected["endpoint"], local_target),
        "oracle_linear_delta_v_from_snapshot_mps": oracle["delta_v_from_snapshot_mps"],
        "oracle_linear_delta_v_norm_from_snapshot_mps": oracle["delta_v_norm_from_snapshot_mps"],
        "oracle_linear_delta_v_normal_mps": oracle_delta_normal,
        "oracle_linear_delta_v_tangent_mps": oracle_delta_tangent,
        "oracle_linear_delta_v_component": oracle_component,
        "oracle_linear_impulse_normal_Ns": oracle_delta_normal * probe.MASS,
        "oracle_linear_impulse_tangent_Ns": oracle_delta_tangent * probe.MASS,
        "oracle_linear_velocity_protocol": oracle["velocity_protocol"],
        "required_early_velocity": residual.get("required_early_velocity"),
        "delta_v_required_mps": residual.get("delta_v_required_mps"),
        "tail_distance_scale_required": residual.get("tail_distance_scale_required"),
        "tail_direction_delta_deg_required": residual.get("tail_direction_delta_deg_required"),
        "baseline_tail": baseline,
        "corrected_tail": corrected,
        "oracle_linear_tail": oracle,
    }


def _summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    ok = [row for row in rows if row.get("status") == "ok"]

    def vals(key: str) -> List[float]:
        return [float(row[key]) for row in ok if row.get(key) is not None]

    return {
        "row_count": len(rows),
        "ok_count": len(ok),
        "baseline_tail_vs_local_full_rmse_m": _rmse(vals("baseline_tail_vs_local_full_m")),
        "baseline_tail_vs_unity_rmse_m": _rmse(vals("baseline_tail_vs_unity_m")),
        "local_full_vs_unity_rmse_m": _rmse(vals("local_full_vs_unity_m")),
        "corrected_tail_vs_unity_rmse_m": _rmse(vals("corrected_tail_vs_unity_m")),
        "corrected_tail_vs_unity_mean_m": _mean(vals("corrected_tail_vs_unity_m")),
        "corrected_tail_over_2cm_count": sum(1 for value in vals("corrected_tail_vs_unity_m") if value > 0.02),
        "oracle_linear_tail_vs_unity_rmse_m": _rmse(vals("oracle_linear_tail_vs_unity_m")),
        "oracle_linear_tail_vs_unity_mean_m": _mean(vals("oracle_linear_tail_vs_unity_m")),
        "oracle_linear_tail_over_2cm_count": sum(
            1 for value in vals("oracle_linear_tail_vs_unity_m") if value > 0.02
        ),
        "oracle_linear_delta_v_norm_mean_mps": _mean(vals("oracle_linear_delta_v_norm_from_snapshot_mps")),
        "oracle_linear_delta_v_norm_rmse_mps": _rmse(vals("oracle_linear_delta_v_norm_from_snapshot_mps")),
        "oracle_linear_delta_v_normal_rmse_mps": _rmse(vals("oracle_linear_delta_v_normal_mps")),
        "oracle_linear_delta_v_tangent_rmse_mps": _rmse(vals("oracle_linear_delta_v_tangent_mps")),
        "oracle_linear_delta_v_component_counts": {
            component: sum(1 for row in ok if row.get("oracle_linear_delta_v_component") == component)
            for component in ("normal", "tangent", "mixed")
        },
        "baseline_tail_vs_local_full_mean_m": _mean(vals("baseline_tail_vs_local_full_m")),
    }


def build_report(
    probe_path: Path,
    *,
    snapshot_time: float,
    result_index: int,
    dt: float,
    max_time: float,
    stop_speed: float,
    stop_frames: int,
) -> Dict[str, Any]:
    payload = _read_json(probe_path)
    result_set = _result_set(payload, result_index)
    config = result_set.get("config") or {}
    rows = [
        _row_report(
            row,
            config,
            snapshot_time=snapshot_time,
            dt=dt,
            max_time=max_time,
            stop_speed=stop_speed,
            stop_frames=stop_frames,
        )
        for row in result_set.get("rows") or []
        if row.get("unity_target_in_play")
    ]
    return {
        "probe": str(probe_path.relative_to(PROJECT_ROOT)),
        "snapshot_time_s": snapshot_time,
        "result_index": result_index,
        "summary": _summarize(rows),
        "rows": rows,
        "interpretation": [
            "baseline_tail_vs_local_full checks whether a fresh target-only scene can reproduce the original local full replay from the chosen snapshot.",
            "corrected_tail_vs_unity checks whether replacing only the target's horizontal velocity by the Unity-implied velocity is enough to land near Unity's endpoint.",
            "oracle_linear_tail_vs_unity uses finite differences through the actual pyphysx tail replay to find the best local target vx/vy correction.",
            "If baseline_tail_vs_local_full is small and corrected_tail_vs_unity is around 2cm, the tail physics is not the main mismatch; the missing state is before the chosen snapshot, i.e. contact/solver output.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--snapshot-time", type=float, default=0.2)
    parser.add_argument("--result-index", type=int, default=0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--max-time", type=float, default=20.0)
    parser.add_argument("--stop-speed", type=float, default=0.003)
    parser.add_argument("--stop-frames", type=int, default=500)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    probe_path = args.probe if args.probe.is_absolute() else PROJECT_ROOT / args.probe
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    report = build_report(
        probe_path,
        snapshot_time=args.snapshot_time,
        result_index=args.result_index,
        dt=args.dt,
        max_time=args.max_time,
        stop_speed=args.stop_speed,
        stop_frames=args.stop_frames,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output_path.relative_to(PROJECT_ROOT)}")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
