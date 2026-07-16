#!/usr/bin/env python3
"""Probe Unity collision samples with a local PhysX reproduction.

Run this script with the Python environment that has ``pyphysx`` installed,
for example:

    D:\\esp\\tmp\\curling_pyphysx_conda\\python.exe tools\\reverse\\probe_physx_collision_alignment.py

The script intentionally focuses on no-sweep, one-target controlled collision
samples. Cleared stones whose Unity endpoint is ``(0, 0)`` are reported but not
included in endpoint RMSE because wall/removal behavior is not modeled here.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import struct
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import pyphysx
except ImportError as exc:  # pragma: no cover - depends on external env.
    raise SystemExit("pyphysx is required; run with the pyphysx conda Python") from exc

from tools.reverse.recovered_curling_motion import BASE_FRICTION, STEP, B2Vec2, newfrictionstep


DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "unity_controlled_samples_20260707.jsonl"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe.json"
DEFAULT_FORMAL_STONE_MESH = Path(r"D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json")
DEFAULT_RELEASE_X = 2.3506
DEFAULT_RELEASE_Y = 32.4768

RADIUS = 0.140875
HEIGHT = 0.23
MASS = 19.1
UNITY_TARGET_EPS = 1e-9
PYPHYSX_CONVEX_COOKING_CAVEAT = (
    "The rebuilt pyphysx binding exposes quantize_input/gpu_compatible. "
    "The default probe path passes Unity's recovered quantize_input=false / "
    "gpu_compatible=false flags; use --quantize-input/--gpu-compatible only "
    "for old binding/default-control comparisons."
)
PYPHYSX_SCENE_NOTE = (
    "pyphysx.Scene starts from PhysX PxSceneDesc defaults; PhysX 4.1 defaults "
    "include PxSceneFlag::eENABLE_PCM. Empty scene_flags does not disable PCM."
)
MATERIAL_SWITCH_MODES = ("post-step-distance", "pre-step-distance", "never")
RINK_GEOMETRY_MODES = ("plane", "unity-plane-mesh")
STONE_GEOMETRY_MODES = ("ring", "formal-recovered")
ACTIVE_YAW_SOURCES = ("constant", "integrated-precontact", "sample")
TARGET_YAW_SOURCES = ("constant", "sample")
UNITY_PLANE_MESH_WIDTH_M = 9.9568
UNITY_PLANE_MESH_LENGTH_M = 49.98
UNITY_PLANE_MESH_CENTER_X_M = 2.375
UNITY_PLANE_MESH_CENTER_Y_M = 14.0
UNITY_PLANE_MESH_SUBDIVISIONS = 10


def _parse_float_list(value: str) -> List[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def _pyphysx_z_yaw_quat(yaw: float) -> List[float]:
    half_yaw = 0.5 * yaw
    return [math.cos(half_yaw), 0.0, 0.0, math.sin(half_yaw)]


def _read_samples(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            sample = json.loads(line)
            if not sample.get("collision_observed"):
                continue
            if sample.get("sent_sweep") is not False:
                continue
            if not str(sample.get("category", "")).startswith("collision"):
                continue
            if len(sample.get("target_indices") or []) != 1:
                continue
            rows.append(sample)
    return rows


def _xy_from_position(position: Sequence[float], index: int) -> Tuple[float, float]:
    return float(position[2 * index]), float(position[2 * index + 1])


def _is_unity_in_play(xy: Tuple[float, float]) -> bool:
    return abs(xy[0]) > UNITY_TARGET_EPS or abs(xy[1]) > UNITY_TARGET_EPS


def _stone_points(radius: float = RADIUS, height: float = HEIGHT, faces: int = 256) -> np.ndarray:
    rows = []
    for index in range(faces):
        angle = 2.0 * math.pi * index / faces
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        rows.append([x, y, height / 2.0])
        rows.append([x, y, -height / 2.0])
    return np.asarray(rows, dtype=np.float32)


STONE_POINTS = _stone_points()


def _formal_stone_points(path: Path) -> np.ndarray:
    """Load recovered Unity x/y/z mesh vertices into the z-up PhysX shape frame, unscaled."""
    data = json.loads(path.read_text(encoding="utf-8"))
    points = []
    for vertex in data["vertices"]:
        unity_x = float(vertex[0])
        unity_y = float(vertex[1])
        unity_z = float(vertex[2])
        points.append([unity_x, unity_z, unity_y])
    return np.asarray(points, dtype=np.float32)


def _sha16_bytes(values: Sequence[int]) -> str:
    raw = bytes(int(value) & 0xFF for value in values)
    return hashlib.sha256(raw).hexdigest()[:16]


def _runtime_hull_counts_from_layout(
    layout: Optional[Dict[str, Any]],
    vertex_ref_count: Optional[int],
) -> Tuple[int, int, int, int]:
    if not isinstance(layout, dict):
        return 66, 128, 192, int(vertex_ref_count or 384)

    def bytes_for(key: str, fallback: int) -> int:
        row = layout.get(key)
        if isinstance(row, dict) and row.get("bytes") is not None:
            return int(row["bytes"])
        return fallback

    nb_polygons = bytes_for("polygons", 66 * 20) // 20
    nb_vertices = bytes_for("hullVertices", 128 * 12) // 12
    nb_edges = bytes_for("facesByEdges8", 192 * 2) // 2
    refs = vertex_ref_count
    if refs is None:
        refs = bytes_for("vertexData8", 384)
    return nb_polygons, nb_vertices, nb_edges, int(refs)


def _infer_runtime_hull_layout(
    raw_len: int,
    *,
    nb_polygons: int,
    nb_vertices: int,
    nb_edges: int,
    vertex_ref_count: int,
) -> Dict[str, Dict[str, int]]:
    offset = 0
    layout: Dict[str, Dict[str, int]] = {}
    layout["polygons"] = {"offset": offset, "bytes": nb_polygons * 20}
    offset += layout["polygons"]["bytes"]
    layout["hullVertices"] = {"offset": offset, "bytes": nb_vertices * 12}
    offset += layout["hullVertices"]["bytes"]
    layout["facesByEdges8"] = {"offset": offset, "bytes": nb_edges * 2}
    offset += layout["facesByEdges8"]["bytes"]
    layout["facesByVertices8"] = {"offset": offset, "bytes": nb_vertices * 3}
    offset += layout["facesByVertices8"]["bytes"]
    no_grb_size = offset + vertex_ref_count
    grb_size = offset + nb_edges * 2 * 2 + vertex_ref_count
    if raw_len == grb_size:
        layout["verticesByEdges16"] = {"offset": offset, "bytes": nb_edges * 2 * 2}
        offset += layout["verticesByEdges16"]["bytes"]
    elif raw_len != no_grb_size:
        raise ValueError(f"cannot infer ConvexHullData layout for {raw_len} bytes")
    layout["vertexData8"] = {"offset": offset, "bytes": vertex_ref_count}
    return layout


def _runtime_hull_source_from_bundle(
    raw_bytes: Sequence[int],
    unity_bundle: Dict[str, Any],
) -> Dict[str, Any]:
    raw = bytes(int(value) & 0xFF for value in raw_bytes)
    layout = unity_bundle.get("byte_layout")
    vertex_ref_count_value = unity_bundle.get("vertex_ref_count")
    vertex_ref_count = int(vertex_ref_count_value) if vertex_ref_count_value is not None else None
    nb_polygons, nb_vertices, nb_edges, vertex_ref_count = _runtime_hull_counts_from_layout(
        layout if isinstance(layout, dict) else None,
        vertex_ref_count,
    )
    if not isinstance(layout, dict):
        layout = _infer_runtime_hull_layout(
            len(raw),
            nb_polygons=nb_polygons,
            nb_vertices=nb_vertices,
            nb_edges=nb_edges,
            vertex_ref_count=vertex_ref_count,
        )
    return {
        "raw": raw,
        "layout": layout,
        "nb_polygons": nb_polygons,
        "nb_vertices": nb_vertices,
        "nb_edges": nb_edges,
        "vertex_ref_count": vertex_ref_count,
        "has_grb_edges": "verticesByEdges16" in layout,
    }


def _swap_yz_f32_inplace(raw: bytearray, offset: int) -> None:
    y = struct.unpack_from("<f", raw, offset + 4)[0]
    z = struct.unpack_from("<f", raw, offset + 8)[0]
    struct.pack_into("<f", raw, offset + 4, z)
    struct.pack_into("<f", raw, offset + 8, y)


def _transform_runtime_hull_raw_unity_xyz_to_pyphysx_xzy(
    raw_bytes: Sequence[int],
    *,
    layout: Dict[str, Any],
    nb_polygons: int,
    nb_vertices: int,
) -> List[int]:
    """Transform Unity y-up ConvexHullData coordinates into the z-up local shape frame.

    Only coordinate-bearing fields are touched. Topology/index streams stay byte-identical.
    """
    raw = bytearray(int(value) & 0xFF for value in raw_bytes)
    polygons = layout["polygons"]
    polygon_offset = int(polygons["offset"])
    for index in range(nb_polygons):
        _swap_yz_f32_inplace(raw, polygon_offset + index * 20)

    vertices = layout["hullVertices"]
    vertex_offset = int(vertices["offset"])
    for index in range(nb_vertices):
        _swap_yz_f32_inplace(raw, vertex_offset + index * 12)
    return list(raw)


def _bigconvex_arrays_from_rebuild(rebuilt: Dict[str, Any]) -> Dict[str, List[int]]:
    big = rebuilt["big_convex"]
    return {
        "samples_raw_bytes": [int(value) & 0xFF for value in big["samples_raw_bytes"]],
        "valencies_raw_bytes": [int(value) & 0xFF for value in big["valencies_raw_bytes"]],
        "adjacent_vertices_raw_bytes": [
            int(value) & 0xFF for value in big["adjacent_vertices_raw_bytes"]
        ],
    }


def _solid_cylinder_inertia(*, mass: float, radius: float, height: float) -> Tuple[float, float, float]:
    radial = mass * (3.0 * radius * radius + height * height) / 12.0
    vertical = 0.5 * mass * radius * radius
    return radial, radial, vertical


def _thin_shell_cylinder_inertia(*, mass: float, radius: float, height: float) -> Tuple[float, float, float]:
    radial = mass * (6.0 * radius * radius + height * height) / 12.0
    vertical = mass * radius * radius
    return radial, radial, vertical


def _resolve_inertia_tensor(
    *,
    model: str,
    mass: float,
    radius: float,
    height: float,
    inertia_radial: Optional[float],
    inertia_vertical: Optional[float],
) -> Optional[Tuple[float, float, float]]:
    if model == "pyphysx-default":
        return None
    if model == "solid-cylinder":
        return _solid_cylinder_inertia(mass=mass, radius=radius, height=height)
    if model == "thin-shell":
        return _thin_shell_cylinder_inertia(mass=mass, radius=radius, height=height)
    if model == "custom":
        if inertia_radial is None or inertia_vertical is None:
            raise ValueError("--inertia-model custom requires --inertia-radial and --inertia-vertical")
        return inertia_radial, inertia_radial, inertia_vertical
    raise ValueError(f"unsupported inertia model: {model}")


def _vec3(value: Any) -> np.ndarray:
    return np.asarray(value, dtype=float)


def _pose_xy(actor: Any) -> np.ndarray:
    position, _quat = pyphysx.cast_transformation(actor.get_global_pose())
    return np.asarray(position, dtype=float)[:2]


def _protocol_to_unity_frame_xy(x: float, y: float) -> Tuple[float, float]:
    return -y, -x


def _unity_frame_to_protocol_xy(x: float, y: float) -> Tuple[float, float]:
    return -y, -x


def _to_physx_xy(x: float, y: float, use_unity_frame: bool) -> Tuple[float, float]:
    if use_unity_frame:
        return _protocol_to_unity_frame_xy(x, y)
    return x, y


def _from_physx_xy(x: float, y: float, use_unity_frame: bool) -> Tuple[float, float]:
    if use_unity_frame:
        return _unity_frame_to_protocol_xy(x, y)
    return x, y


def _unity_plane_mesh(
    *,
    center_x: float,
    center_y: float,
    width: float,
    length: float,
    subdivisions: int,
    use_unity_frame: bool,
) -> Tuple[np.ndarray, np.ndarray]:
    if subdivisions <= 0:
        raise ValueError("--rink-mesh-subdivisions must be positive")
    vertices: List[List[float]] = []
    for iy in range(subdivisions + 1):
        protocol_y = center_y - 0.5 * length + length * iy / subdivisions
        for ix in range(subdivisions + 1):
            protocol_x = center_x - 0.5 * width + width * ix / subdivisions
            physx_x, physx_y = _to_physx_xy(protocol_x, protocol_y, use_unity_frame)
            vertices.append([physx_x, physx_y, 0.0])

    triangles: List[List[int]] = []
    row_width = subdivisions + 1
    for iy in range(subdivisions):
        for ix in range(subdivisions):
            v00 = iy * row_width + ix
            v10 = v00 + 1
            v01 = v00 + row_width
            v11 = v01 + 1
            if use_unity_frame:
                triangles.append([v00, v01, v10])
                triangles.append([v01, v11, v10])
            else:
                triangles.append([v00, v10, v01])
                triangles.append([v01, v10, v11])

    return np.asarray(vertices, dtype=np.float32), np.asarray(triangles, dtype=np.int32)


def _linear_velocity(actor: Any) -> np.ndarray:
    return _vec3(actor.get_linear_velocity())


def _angular_velocity(actor: Any) -> np.ndarray:
    return _vec3(actor.get_angular_velocity())


def _actor_address(actor: Any) -> int:
    return int(actor.get_physx_address())


def _contact_point_to_dict(point: Any) -> Dict[str, Any]:
    return {
        "position": [float(value) for value in point.get("position", [])],
        "normal": [float(value) for value in point.get("normal", [])],
        "impulse": [float(value) for value in point.get("impulse", [])],
        "separation": float(point.get("separation")),
        "internal_face_index0": int(point.get("internal_face_index0")),
        "internal_face_index1": int(point.get("internal_face_index1")),
    }


def _stone_stone_contact_reports(
    scene: Any,
    *,
    active_address: int,
    target_address: int,
    current_time: float,
) -> List[Dict[str, Any]]:
    reports: List[Dict[str, Any]] = []
    pair_addresses = {active_address, target_address}
    for report in scene.get_contact_reports():
        actor0 = int(report.get("actor0"))
        actor1 = int(report.get("actor1"))
        if {actor0, actor1} != pair_addresses:
            continue
        reports.append(
            {
                "time": current_time,
                "actor0": actor0,
                "actor1": actor1,
                "active_is_actor0": actor0 == active_address,
                "events": int(report.get("events")),
                "flags": int(report.get("flags")),
                "contact_count": int(report.get("contact_count")),
                "points": [_contact_point_to_dict(point) for point in report.get("points", [])],
            }
        )
    return reports


def _combine_mode_from_name(name: str) -> Any:
    key = name.strip().lower().replace("-", "_")
    mapping = {
        "average": pyphysx.CombineMode.AVERAGE,
        "avg": pyphysx.CombineMode.AVERAGE,
        "multiply": pyphysx.CombineMode.MULTIPLY,
        "mul": pyphysx.CombineMode.MULTIPLY,
        "minimum": pyphysx.CombineMode.MIN,
        "min": pyphysx.CombineMode.MIN,
        "maximum": pyphysx.CombineMode.MAX,
        "max": pyphysx.CombineMode.MAX,
    }
    try:
        return mapping[key]
    except KeyError as exc:
        raise argparse.ArgumentTypeError(f"unsupported combine mode: {name}") from exc


def _scene_flags_from_names(names: Sequence[str]) -> List[Any]:
    mapping = {
        "enable_pcm": pyphysx.SceneFlag.ENABLE_PCM,
        "pcm": pyphysx.SceneFlag.ENABLE_PCM,
        "disable_contact_cache": pyphysx.SceneFlag.DISABLE_CONTACT_CACHE,
        "enable_stabilization": pyphysx.SceneFlag.ENABLE_STABILIZATION,
        "enable_average_point": pyphysx.SceneFlag.ENABLE_AVERAGE_POINT,
        "enable_friction_every_iteration": pyphysx.SceneFlag.ENABLE_FRICTION_EVERY_ITERATION,
        "enable_enhanced_determinism": pyphysx.SceneFlag.ENABLE_ENHANCED_DETERMINISM,
    }
    flags: List[Any] = []
    for name in names:
        key = name.strip().lower().replace("-", "_")
        if not key:
            continue
        try:
            flags.append(mapping[key])
        except KeyError as exc:
            raise argparse.ArgumentTypeError(f"unsupported scene flag: {name}") from exc
    return flags


def _make_material(
    static_friction: float,
    dynamic_friction: float,
    restitution: float,
    combine_mode: Any,
    disable_strong_friction: bool,
    improved_patch_friction: bool,
) -> Any:
    material = pyphysx.Material(static_friction, dynamic_friction, restitution)
    material.set_friction_combine_mode(combine_mode)
    material.set_restitution_combine_mode(combine_mode)
    if disable_strong_friction:
        material.set_flag(pyphysx.MaterialFlag.DISABLE_STRONG_FRICTION, True)
    if improved_patch_friction:
        material.set_flag(pyphysx.MaterialFlag.IMPROVED_PATCH_FRICTION, True)
    return material


def _patch_runtime_stone_shape(
    shape: Any,
    *,
    runtime_hull_raw_bytes: Optional[List[int]],
    runtime_big_convex_arrays: Optional[Dict[str, List[int]]],
) -> Dict[str, Any]:
    patch: Dict[str, Any] = {
        "runtime_hull_raw_bytes": len(runtime_hull_raw_bytes) if isinstance(runtime_hull_raw_bytes, list) else None,
        "runtime_big_convex_raw_bytes": None,
        "hull_patch": None,
        "big_convex_patch": None,
    }
    if runtime_hull_raw_bytes is not None:
        patch["hull_patch"] = shape.patch_convex_mesh_runtime_hull_data_for_unity(
            runtime_hull_raw_bytes,
            True,
        )
    if runtime_big_convex_arrays is not None:
        samples = runtime_big_convex_arrays["samples_raw_bytes"]
        valencies = runtime_big_convex_arrays["valencies_raw_bytes"]
        adjacent = runtime_big_convex_arrays["adjacent_vertices_raw_bytes"]
        patch["runtime_big_convex_raw_bytes"] = {
            "samples": len(samples),
            "valencies": len(valencies),
            "adjacent_vertices": len(adjacent),
        }
        patch["big_convex_patch"] = shape.patch_convex_mesh_big_convex_raw_data_for_unity(
            samples,
            valencies,
            adjacent,
        )
    return patch


def _make_stone(
    x: float,
    y: float,
    vx: float,
    vy: float,
    w: float,
    yaw: float,
    *,
    vz: float = 0.0,
    wx: float = 0.0,
    wy: float = 0.0,
    stone_points: np.ndarray,
    radius: float,
    height: float,
    stone_faces: int,
    inertia_model: str,
    inertia_radial: Optional[float],
    inertia_vertical: Optional[float],
    center_height: float,
    stone_friction: float,
    static_friction: float,
    dynamic_friction: float,
    stone_restitution: float,
    combine_mode: Any,
    contact_offset: float,
    rest_offset: float,
    shape_local_x: float,
    shape_local_y: float,
    shape_local_z: float,
    shape_local_yaw: float,
    convex_quantized_count: int,
    convex_vertex_limit: int,
    convex_mesh_scale: Optional[Sequence[float]],
    quantize_input: bool,
    gpu_compatible: bool,
    runtime_hull_raw_bytes: Optional[List[int]],
    runtime_big_convex_arrays: Optional[Dict[str, List[int]]],
    solver_position_iterations: int,
    solver_velocity_iterations: int,
    max_depenetration_velocity: float,
    lock_upright: bool,
    disable_stone_gravity: bool,
    disable_strong_friction: bool,
    improved_patch_friction: bool,
) -> Tuple[Any, Any, Any, Dict[str, Any]]:
    material = _make_material(
        static_friction,
        dynamic_friction,
        stone_restitution,
        combine_mode=combine_mode,
        disable_strong_friction=disable_strong_friction,
        improved_patch_friction=improved_patch_friction,
    )
    if convex_mesh_scale is not None:
        shape = pyphysx.Shape.create_convex_mesh_from_points_with_scale(
            stone_points,
            material,
            True,
            [float(value) for value in convex_mesh_scale],
            convex_quantized_count,
            convex_vertex_limit,
            quantize_input,
            gpu_compatible,
        )
    else:
        shape = pyphysx.Shape.create_convex_mesh_from_points(
            stone_points,
            material,
            True,
            1.0,
            convex_quantized_count,
            convex_vertex_limit,
            quantize_input,
            gpu_compatible,
        )
    runtime_patch = _patch_runtime_stone_shape(
        shape,
        runtime_hull_raw_bytes=runtime_hull_raw_bytes,
        runtime_big_convex_arrays=runtime_big_convex_arrays,
    )
    shape.set_contact_offset(contact_offset)
    shape.set_rest_offset(rest_offset)
    if (
        abs(shape_local_x) > 1e-12
        or abs(shape_local_y) > 1e-12
        or abs(shape_local_z) > 1e-12
        or abs(shape_local_yaw) > 1e-12
    ):
        shape.set_local_pose(
            (
                [shape_local_x, shape_local_y, shape_local_z],
                _pyphysx_z_yaw_quat(shape_local_yaw),
            )
        )

    body = pyphysx.RigidDynamic()
    body.attach_shape(shape)
    body.set_mass(MASS)
    # CurlingStoneNew.Start explicitly calls Rigidbody.set_centerOfMass(Vector3.zero).
    # The cooked convex hull has a tiny nonzero mass centroid, so leave no implicit
    # cooker-derived COM state in the local rigid body.
    body.set_center_of_mass_local_pose(([0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]))
    inertia_tensor = _resolve_inertia_tensor(
        model=inertia_model,
        mass=MASS,
        radius=radius,
        height=height,
        inertia_radial=inertia_radial,
        inertia_vertical=inertia_vertical,
    )
    if inertia_tensor is not None:
        body.set_mass_space_inertia_tensor(inertia_tensor)
    body.set_linear_damping(0.0)
    body.set_angular_damping(0.05)
    body.set_solver_iteration_counts(solver_position_iterations, solver_velocity_iterations)
    body.set_max_depenetration_velocity(max_depenetration_velocity)
    if disable_stone_gravity:
        body.disable_gravity()
    if lock_upright:
        body.set_rigid_dynamic_lock_flag(pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_X, True)
        body.set_rigid_dynamic_lock_flag(pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_Y, True)
    body.set_global_pose(([x, y, center_height], _pyphysx_z_yaw_quat(yaw)))
    body.set_linear_velocity([vx, vy, vz])
    body.set_angular_velocity([wx, wy, w])
    return body, shape, material, runtime_patch


def _handoff_state(
    sample: Dict[str, Any],
    target_xy: Tuple[float, float],
    threshold: float,
    handoff_friction: float,
    target_distance: Optional[float] = None,
) -> Dict[str, float]:
    x, y, vx, vy, w = [float(value) for value in sample["motioninfo"]]
    tx, ty = target_xy
    best_distance = float("inf")
    best_step = 0
    previous: Optional[Dict[str, float]] = None
    for step_index in range(6000):
        distance = math.hypot(x - tx, y - ty)
        if distance < best_distance:
            best_distance = distance
            best_step = step_index
        if target_distance is not None and previous is not None:
            previous_delta = float(previous["distance"]) - target_distance
            current_delta = distance - target_distance
            if previous_delta == 0.0 or previous_delta * current_delta <= 0.0:
                denom = distance - float(previous["distance"])
                alpha = 0.0 if abs(denom) < 1e-12 else (target_distance - float(previous["distance"])) / denom
                alpha = max(0.0, min(1.0, alpha))
                return {
                    "step": float(previous["step"]) + alpha,
                    "x": float(previous["x"]) + (x - float(previous["x"])) * alpha,
                    "y": float(previous["y"]) + (y - float(previous["y"])) * alpha,
                    "vx": float(previous["vx"]) + (vx - float(previous["vx"])) * alpha,
                    "vy": float(previous["vy"]) + (vy - float(previous["vy"])) * alpha,
                    "w": float(previous["w"]) + (w - float(previous["w"])) * alpha,
                    "distance": target_distance,
                    "threshold": threshold,
                    "source": "interpolated_center_distance",
                    "target_distance": target_distance,
                    "interpolation_alpha": alpha,
                }
        if target_distance is None and distance <= threshold:
            return {
                "step": step_index,
                "x": x,
                "y": y,
                "vx": vx,
                "vy": vy,
                "w": w,
                "distance": distance,
                "threshold": threshold,
            }
        previous = {
            "step": float(step_index),
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "w": w,
            "distance": distance,
        }
        speed = newfrictionstep(handoff_friction, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        x += vx * 0.01
        y += vy * 0.01
        if math.hypot(vx, vy) < 1e-5:
            break
    return {
        "step": best_step,
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "w": w,
        "distance": best_distance,
        "threshold": threshold,
        "target_distance": target_distance,
        "missed_threshold": True,
    }


def _bestshot_state_yaw_to_motioninfo(
    sample: Dict[str, Any],
    *,
    friction: float,
    release_x: float = DEFAULT_RELEASE_X,
    release_y: float = DEFAULT_RELEASE_Y,
) -> Dict[str, Any]:
    requested = sample.get("requested") or {}
    motioninfo = sample.get("motioninfo") or []
    if len(motioninfo) < 5:
        return {"yaw": 0.0, "steps": 0, "status": "missing_motioninfo"}

    x = release_x + float(requested.get("h0", 0.0))
    y = release_y
    vx = 0.0
    vy = -float(requested.get("v0", 0.0))
    w = float(requested.get("w0", 0.0))
    stop_y = float(motioninfo[1])
    yaw = 0.0
    for step_index in range(5000):
        if math.hypot(vx, vy) <= 0.01 or y <= stop_y:
            return {"yaw": yaw, "steps": step_index, "status": "ok"}
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        yaw += w * 0.01
        x += vx * 0.01
        y += vy * 0.01
    return {"yaw": yaw, "steps": 5000, "status": "max_steps"}


def _motioninfo_yaw_to_handoff(
    sample: Dict[str, Any],
    target_xy: Tuple[float, float],
    threshold: float,
    *,
    friction: float,
) -> Dict[str, Any]:
    x, y, vx, vy, w = [float(value) for value in sample["motioninfo"]]
    tx, ty = target_xy
    yaw = 0.0
    for step_index in range(6000):
        if math.hypot(x - tx, y - ty) <= threshold:
            return {"yaw": yaw, "steps": step_index, "status": "ok"}
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        yaw += w * 0.01
        x += vx * 0.01
        y += vy * 0.01
        if math.hypot(vx, vy) < 1e-5:
            break
    return {"yaw": yaw, "steps": step_index, "status": "missed_threshold"}


def _integrated_precontact_yaw(
    sample: Dict[str, Any],
    target_xy: Tuple[float, float],
    threshold: float,
    *,
    friction: float,
) -> Dict[str, Any]:
    release_to_motioninfo = _bestshot_state_yaw_to_motioninfo(sample, friction=friction)
    motioninfo_to_handoff = _motioninfo_yaw_to_handoff(
        sample,
        target_xy,
        threshold,
        friction=friction,
    )
    total_yaw = float(release_to_motioninfo["yaw"]) + float(motioninfo_to_handoff["yaw"])
    return {
        "yaw": total_yaw,
        "yaw_deg": math.degrees(total_yaw),
        "release_to_motioninfo_yaw": release_to_motioninfo["yaw"],
        "release_to_motioninfo_yaw_deg": math.degrees(float(release_to_motioninfo["yaw"])),
        "release_to_motioninfo_steps": release_to_motioninfo["steps"],
        "release_to_motioninfo_status": release_to_motioninfo["status"],
        "motioninfo_to_handoff_yaw": motioninfo_to_handoff["yaw"],
        "motioninfo_to_handoff_yaw_deg": math.degrees(float(motioninfo_to_handoff["yaw"])),
        "motioninfo_to_handoff_steps": motioninfo_to_handoff["steps"],
        "motioninfo_to_handoff_status": motioninfo_to_handoff["status"],
    }


def _explicit_handoff_state(sample: Dict[str, Any]) -> Optional[Dict[str, float]]:
    handoff_state = sample.get("handoff_state")
    if not isinstance(handoff_state, dict):
        return None
    required = ("x", "y", "vx", "vy", "w")
    missing = [name for name in required if name not in handoff_state]
    if missing:
        raise ValueError(f"handoff_state missing fields: {', '.join(missing)}")
    return {
        "step": int(handoff_state.get("step", -1)),
        "x": float(handoff_state["x"]),
        "y": float(handoff_state["y"]),
        "vx": float(handoff_state["vx"]),
        "vy": float(handoff_state["vy"]),
        "vz": float(handoff_state.get("vz", 0.0)),
        "wx": float(handoff_state.get("wx", 0.0)),
        "wy": float(handoff_state.get("wy", 0.0)),
        "w": float(handoff_state["w"]),
        "distance": float(handoff_state.get("distance", 0.0)),
        "threshold": float(handoff_state.get("threshold", 0.0)),
        "source": str(handoff_state.get("source", "explicit")),
        "velocity_source": str(handoff_state.get("velocity_source", "")),
    }


def _explicit_target_handoff_state(sample: Dict[str, Any]) -> Dict[str, float]:
    state = sample.get("target_handoff_state")
    if not isinstance(state, dict):
        state = {}
    return {
        "vx": float(state.get("vx", 0.0)),
        "vy": float(state.get("vy", 0.0)),
        "vz": float(state.get("vz", 0.0)),
        "wx": float(state.get("wx", 0.0)),
        "wy": float(state.get("wy", 0.0)),
        "w": float(state.get("w", 0.0)),
        "source": str(state.get("source", "")),
        "velocity_source": str(state.get("velocity_source", "")),
    }


def _sample_yaw(sample: Dict[str, Any], key: str, default: float) -> float:
    value = sample.get(key)
    if value is not None:
        return float(value)
    handoff_state = sample.get("handoff_state")
    if isinstance(handoff_state, dict):
        handoff_key = "yaw" if key == "active_yaw" else key
        if handoff_key in handoff_state:
            return float(handoff_state[handoff_key])
    return default


def _actor_snapshot(actor: Any, use_unity_frame: bool) -> Dict[str, Any]:
    position, quaternion = pyphysx.cast_transformation(actor.get_global_pose())
    physx_position = np.asarray(position, dtype=float)
    physx_quaternion = [
        float(getattr(quaternion, "x")),
        float(getattr(quaternion, "y")),
        float(getattr(quaternion, "z")),
        float(getattr(quaternion, "w")),
    ]
    pyphysx_quaternion_wxyz = [
        physx_quaternion[3],
        physx_quaternion[0],
        physx_quaternion[1],
        physx_quaternion[2],
    ]
    xy = physx_position[:2]
    velocity = _linear_velocity(actor)
    angular = _angular_velocity(actor)
    px, py = _from_physx_xy(float(xy[0]), float(xy[1]), use_unity_frame)
    vx, vy = _from_physx_xy(float(velocity[0]), float(velocity[1]), use_unity_frame)
    return {
        "position": [px, py],
        "linear_velocity": [vx, vy],
        "linear_speed": math.hypot(vx, vy),
        "angular_velocity": float(angular[2]),
        "physx_position": [float(value) for value in physx_position],
        "physx_linear_velocity": [float(value) for value in velocity],
        "physx_angular_velocity": [float(value) for value in angular],
        "physx_quaternion": physx_quaternion,
        "physx_quaternion_order": "xyzw",
        "pyphysx_quaternion_wxyz": pyphysx_quaternion_wxyz,
    }


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return [_jsonable(item) for item in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def _immediate_contact_probe(
    *,
    active: Any,
    active_shape: Any,
    target: Any,
    target_shape: Any,
    stage: str,
    step_index: int,
    current_time: float,
    contact_distance: float,
    mesh_contact_margin: float,
    tolerance_length: float,
    use_unity_frame: bool,
) -> Dict[str, Any]:
    active_xy = _pose_xy(active)
    target_xy = _pose_xy(target)
    item: Dict[str, Any] = {
        "stage": stage,
        "step_index": step_index,
        "time": current_time,
        "center_distance": float(np.linalg.norm(active_xy - target_xy)),
        "active": _actor_snapshot(active, use_unity_frame),
        "target": _actor_snapshot(target, use_unity_frame),
    }
    if not hasattr(pyphysx, "generate_contacts_between"):
        item["ok"] = False
        item["error"] = "pyphysx.generate_contacts_between is not available"
        return item
    try:
        result = pyphysx.generate_contacts_between(
            active,
            active_shape,
            target,
            target_shape,
            contact_distance,
            mesh_contact_margin,
            tolerance_length,
        )
    except Exception as exc:  # pragma: no cover - native probe failure path.
        item["ok"] = False
        item["error"] = repr(exc)
        return item
    item["ok"] = True
    item["result"] = _jsonable(result)
    return item


def _set_pose_xy_yaw(actor: Any, x: float, y: float, z: float, yaw: float) -> None:
    actor.set_global_pose(([x, y, z], _pyphysx_z_yaw_quat(yaw)))


def _actor_z(actor: Any) -> float:
    position, _quat = pyphysx.cast_transformation(actor.get_global_pose())
    return float(np.asarray(position, dtype=float)[2])


def _settle_scene(scene: Any, dt: float, settle_time: float) -> None:
    steps = max(0, int(round(settle_time / dt)))
    for _ in range(steps):
        scene.simulate(dt)


def _zero_actor_velocity(actor: Any) -> None:
    actor.set_linear_velocity([0.0, 0.0, 0.0])
    actor.set_angular_velocity([0.0, 0.0, 0.0])


def _simulate_one(
    sample: Dict[str, Any],
    *,
    handoff_extra: float,
    ice_friction: float,
    stone_friction: float,
    stone_restitution: float,
    pre_collision_dynamic_friction: Optional[float],
    pre_collision_static_friction: Optional[float],
    pre_collision_friction_scope: str,
    material_switch_mode: str,
    stone_points: np.ndarray,
    radius: float,
    height: float,
    stone_faces: int,
    inertia_model: str,
    inertia_radial: Optional[float],
    inertia_vertical: Optional[float],
    active_yaw: float,
    active_yaw_source: str,
    active_yaw_integral_sign: float,
    target_yaw: float,
    target_yaw_source: str,
    center_height: float,
    scene_flags: Sequence[Any],
    scene_flag_names: Sequence[str],
    combine_mode: Any,
    combine_mode_name: str,
    contact_offset: float,
    rest_offset: float,
    shape_local_x: float,
    shape_local_y: float,
    shape_local_z: float,
    shape_local_yaw: float,
    convex_quantized_count: int,
    convex_vertex_limit: int,
    convex_mesh_scale: Optional[Sequence[float]],
    quantize_input: bool,
    gpu_compatible: bool,
    runtime_hull_raw_bytes: Optional[List[int]],
    runtime_big_convex_arrays: Optional[Dict[str, List[int]]],
    runtime_feature_source: Optional[str],
    solver_position_iterations: int,
    solver_velocity_iterations: int,
    max_depenetration_velocity: float,
    lock_upright: bool,
    disable_stone_gravity: bool,
    disable_strong_friction: bool,
    improved_patch_friction: bool,
    rink_geometry: str,
    rink_mesh_center_x: float,
    rink_mesh_center_y: float,
    rink_mesh_width: float,
    rink_mesh_length: float,
    rink_mesh_subdivisions: int,
    use_unity_frame: bool,
    friction_offset_threshold: Optional[float],
    dt: float,
    max_time: float,
    stop_speed: float,
    stop_frames: int,
    snapshot_times: Sequence[float],
    enable_contact_report: bool,
    max_contact_reports: int,
    enable_immediate_contact_probe: bool,
    max_immediate_contact_probes: int,
    immediate_contact_distance: float,
    immediate_mesh_contact_margin: float,
    immediate_tolerance_length: float,
    handoff_friction: float,
    handoff_center_distance: Optional[float],
    handoff_v_scale: float,
    handoff_vx_offset: float,
    handoff_vy_offset: float,
    handoff_w_offset: float,
    angular_sign: float,
    handoff_x_offset: float,
    handoff_y_offset: float,
    target_x_offset: float,
    target_y_offset: float,
    target_settle_time: float,
    active_settle_time: float,
    active_settle_backoff: float,
) -> Dict[str, Any]:
    target_index = int(sample["target_indices"][0])
    active_index = int(sample["active_shot_num"])
    target_before = _xy_from_position(sample["reset_position"], target_index)
    target_physics_before = (
        target_before[0] + target_x_offset,
        target_before[1] + target_y_offset,
    )
    unity_active = _xy_from_position(sample["after_position"], active_index)
    unity_target = _xy_from_position(sample["after_position"], target_index)
    threshold = 2.0 * radius + handoff_extra
    handoff = _explicit_handoff_state(sample)
    if handoff is None:
        handoff = _handoff_state(
            sample,
            target_physics_before,
            threshold,
            handoff_friction,
            target_distance=handoff_center_distance,
        )
    integrated_yaw = _integrated_precontact_yaw(
        sample,
        target_physics_before,
        threshold,
        friction=handoff_friction,
    )
    effective_active_yaw = active_yaw
    if active_yaw_source == "integrated-precontact":
        effective_active_yaw = active_yaw + active_yaw_integral_sign * float(integrated_yaw["yaw"])
    elif active_yaw_source == "sample":
        effective_active_yaw = _sample_yaw(sample, "active_yaw", active_yaw)
    effective_target_yaw = target_yaw
    if target_yaw_source == "sample":
        effective_target_yaw = _sample_yaw(sample, "target_yaw", target_yaw)

    scene_kwargs = {"bounce_threshold_velocity": 0.05}
    if friction_offset_threshold is not None:
        scene_kwargs["friction_offset_threshold"] = friction_offset_threshold
    if enable_contact_report:
        scene_kwargs["enable_contact_report"] = True
    scene = pyphysx.Scene(scene_flags=list(scene_flags), **scene_kwargs)
    ice_material = _make_material(
        ice_friction,
        ice_friction,
        0.0,
        combine_mode=combine_mode,
        disable_strong_friction=disable_strong_friction,
        improved_patch_friction=improved_patch_friction,
    )
    if rink_geometry == "plane":
        ice = pyphysx.RigidStatic.create_plane(ice_material, 0.0, 0.0, 1.0, 0.0)
    elif rink_geometry == "unity-plane-mesh":
        points, triangles = _unity_plane_mesh(
            center_x=rink_mesh_center_x,
            center_y=rink_mesh_center_y,
            width=rink_mesh_width,
            length=rink_mesh_length,
            subdivisions=rink_mesh_subdivisions,
            use_unity_frame=use_unity_frame,
        )
        ice_shape = pyphysx.Shape.create_triangle_mesh_from_points(
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
        ice = pyphysx.RigidStatic()
        ice.attach_shape(ice_shape)
    else:
        raise ValueError(f"unsupported rink geometry: {rink_geometry}")
    # The pyphysx plane helper and newly cooked triangle mesh leave shape offsets
    # at PhysX defaults; Unity's recovered PhysicsManager uses 0.01m globally.
    for shape in ice.get_atached_shapes():
        shape.set_contact_offset(contact_offset)
        shape.set_rest_offset(rest_offset)
    scene.add_actor(ice)

    active_x, active_y = _to_physx_xy(
        handoff["x"] + handoff_x_offset,
        handoff["y"] + handoff_y_offset,
        use_unity_frame,
    )
    active_vx, active_vy = _to_physx_xy(
        handoff["vx"] * handoff_v_scale + handoff_vx_offset,
        handoff["vy"] * handoff_v_scale + handoff_vy_offset,
        use_unity_frame,
    )
    active_w = handoff["w"] * angular_sign + handoff_w_offset
    active_vz = float(handoff.get("vz", 0.0))
    active_wx = float(handoff.get("wx", 0.0))
    active_wy = float(handoff.get("wy", 0.0))
    target_handoff = _explicit_target_handoff_state(sample)
    target_vx, target_vy = _to_physx_xy(
        float(target_handoff.get("vx", 0.0)),
        float(target_handoff.get("vy", 0.0)),
        use_unity_frame,
    )
    target_vz = float(target_handoff.get("vz", 0.0))
    target_w = float(target_handoff.get("w", 0.0))
    target_wx = float(target_handoff.get("wx", 0.0))
    target_wy = float(target_handoff.get("wy", 0.0))
    target_x, target_y = _to_physx_xy(target_physics_before[0], target_physics_before[1], use_unity_frame)

    apply_pre_active = pre_collision_friction_scope in {"active", "both"}
    apply_pre_target = pre_collision_friction_scope in {"target", "both"}
    active, _active_shape, _active_material, active_runtime_patch = _make_stone(
        active_x,
        active_y,
        active_vx,
        active_vy,
        active_w,
        effective_active_yaw,
        vz=active_vz,
        wx=active_wx,
        wy=active_wy,
        stone_points=stone_points,
        radius=radius,
        height=height,
        stone_faces=stone_faces,
        inertia_model=inertia_model,
        inertia_radial=inertia_radial,
        inertia_vertical=inertia_vertical,
        center_height=center_height,
        stone_friction=stone_friction,
        static_friction=pre_collision_static_friction
        if apply_pre_active and pre_collision_static_friction is not None
        else stone_friction,
        dynamic_friction=pre_collision_dynamic_friction
        if apply_pre_active and pre_collision_dynamic_friction is not None
        else stone_friction,
        stone_restitution=stone_restitution,
        combine_mode=combine_mode,
        contact_offset=contact_offset,
        rest_offset=rest_offset,
        shape_local_x=shape_local_x,
        shape_local_y=shape_local_y,
        shape_local_z=shape_local_z,
        shape_local_yaw=shape_local_yaw,
        convex_quantized_count=convex_quantized_count,
        convex_vertex_limit=convex_vertex_limit,
        convex_mesh_scale=convex_mesh_scale,
        quantize_input=quantize_input,
        gpu_compatible=gpu_compatible,
        runtime_hull_raw_bytes=runtime_hull_raw_bytes,
        runtime_big_convex_arrays=runtime_big_convex_arrays,
        solver_position_iterations=solver_position_iterations,
        solver_velocity_iterations=solver_velocity_iterations,
        max_depenetration_velocity=max_depenetration_velocity,
        lock_upright=lock_upright,
        disable_stone_gravity=disable_stone_gravity,
        disable_strong_friction=disable_strong_friction,
        improved_patch_friction=improved_patch_friction,
    )
    target, _target_shape, _target_material, target_runtime_patch = _make_stone(
        target_x,
        target_y,
        target_vx,
        target_vy,
        target_w,
        effective_target_yaw,
        vz=target_vz,
        wx=target_wx,
        wy=target_wy,
        stone_points=stone_points,
        radius=radius,
        height=height,
        stone_faces=stone_faces,
        inertia_model=inertia_model,
        inertia_radial=inertia_radial,
        inertia_vertical=inertia_vertical,
        center_height=center_height,
        stone_friction=stone_friction,
        static_friction=pre_collision_static_friction
        if apply_pre_target and pre_collision_static_friction is not None
        else stone_friction,
        dynamic_friction=pre_collision_dynamic_friction
        if apply_pre_target and pre_collision_dynamic_friction is not None
        else stone_friction,
        stone_restitution=stone_restitution,
        combine_mode=combine_mode,
        contact_offset=contact_offset,
        rest_offset=rest_offset,
        shape_local_x=shape_local_x,
        shape_local_y=shape_local_y,
        shape_local_z=shape_local_z,
        shape_local_yaw=shape_local_yaw,
        convex_quantized_count=convex_quantized_count,
        convex_vertex_limit=convex_vertex_limit,
        convex_mesh_scale=convex_mesh_scale,
        quantize_input=quantize_input,
        gpu_compatible=gpu_compatible,
        runtime_hull_raw_bytes=runtime_hull_raw_bytes,
        runtime_big_convex_arrays=runtime_big_convex_arrays,
        solver_position_iterations=solver_position_iterations,
        solver_velocity_iterations=solver_velocity_iterations,
        max_depenetration_velocity=max_depenetration_velocity,
        lock_upright=lock_upright,
        disable_stone_gravity=disable_stone_gravity,
        disable_strong_friction=disable_strong_friction,
        improved_patch_friction=improved_patch_friction,
    )
    active_added = False
    target_added = False
    if target_settle_time > 0.0:
        scene.add_actor(target)
        target_added = True
        _settle_scene(scene, dt, target_settle_time)
        _zero_actor_velocity(target)
        target.set_linear_velocity([target_vx, target_vy, target_vz])
        target.set_angular_velocity([target_wx, target_wy, target_w])

    if active_settle_time > 0.0:
        horizontal_speed = math.hypot(active_vx, active_vy)
        if horizontal_speed > 1e-9 and active_settle_backoff != 0.0:
            settle_x = active_x - active_settle_backoff * active_vx / horizontal_speed
            settle_y = active_y - active_settle_backoff * active_vy / horizontal_speed
        else:
            settle_x = active_x
            settle_y = active_y
        _set_pose_xy_yaw(active, settle_x, settle_y, center_height, effective_active_yaw)
        _zero_actor_velocity(active)
        scene.add_actor(active)
        active_added = True
        _settle_scene(scene, dt, active_settle_time)
        _set_pose_xy_yaw(active, active_x, active_y, _actor_z(active), effective_active_yaw)
        active.set_linear_velocity([active_vx, active_vy, active_vz])
        active.set_angular_velocity([active_wx, active_wy, active_w])
        if target_added:
            _zero_actor_velocity(target)
            target.set_linear_velocity([target_vx, target_vy, target_vz])
            target.set_angular_velocity([target_wx, target_wy, target_w])

    if not active_added:
        scene.add_actor(active)
        active_added = True
    if not target_added:
        scene.add_actor(target)
        target_added = True

    active_address = _actor_address(active)
    target_address = _actor_address(target)
    stone_stone_reports: List[Dict[str, Any]] = []
    immediate_contact_probes: List[Dict[str, Any]] = []

    def capture_immediate_contact(stage: str, step_index: int, current_time: float) -> None:
        if not enable_immediate_contact_probe:
            return
        if len(immediate_contact_probes) >= max_immediate_contact_probes:
            return
        immediate_contact_probes.append(
            _immediate_contact_probe(
                active=active,
                active_shape=_active_shape,
                target=target,
                target_shape=_target_shape,
                stage=stage,
                step_index=step_index,
                current_time=current_time,
                contact_distance=immediate_contact_distance,
                mesh_contact_margin=immediate_mesh_contact_margin,
                tolerance_length=immediate_tolerance_length,
                use_unity_frame=use_unity_frame,
            )
        )

    still_count = 0
    steps = int(max_time / dt)
    elapsed = max_time
    material_switch_materials = []
    if apply_pre_active and (
        pre_collision_dynamic_friction is not None or pre_collision_static_friction is not None
    ):
        material_switch_materials.append(_active_material)
    if apply_pre_target and (
        pre_collision_dynamic_friction is not None or pre_collision_static_friction is not None
    ):
        material_switch_materials.append(_target_material)
    material_switched = not material_switch_materials
    material_switch_time: Optional[float] = None
    material_switch_distance: Optional[float] = None

    def switch_materials_if_close(time_value: float) -> bool:
        nonlocal material_switched, material_switch_time, material_switch_distance
        if material_switched or material_switch_mode == "never":
            return False
        active_xy = _pose_xy(active)
        target_xy = _pose_xy(target)
        center_distance = float(np.linalg.norm(active_xy - target_xy))
        if center_distance <= (2.0 * radius + 2.0 * contact_offset + 1e-6):
            for material in material_switch_materials:
                material.set_dynamic_friction(stone_friction)
                material.set_static_friction(stone_friction)
            material_switched = True
            material_switch_time = time_value
            material_switch_distance = center_distance
            return True
        return False

    snapshots: Dict[str, Any] = {
        "0.000000": {
            "active": _actor_snapshot(active, use_unity_frame),
            "target": _actor_snapshot(target, use_unity_frame),
        }
    }
    pending_snapshots = sorted({round(time_value, 9) for time_value in snapshot_times if time_value > 0.0})
    next_snapshot_index = 0
    for step_index in range(steps):
        capture_immediate_contact("pre_step", step_index, step_index * dt)
        if material_switch_mode == "pre-step-distance":
            switch_materials_if_close(step_index * dt)
        scene.simulate(dt)
        current_time = (step_index + 1) * dt
        capture_immediate_contact("post_step", step_index, current_time)
        if enable_contact_report and len(stone_stone_reports) < max_contact_reports:
            new_reports = _stone_stone_contact_reports(
                scene,
                active_address=active_address,
                target_address=target_address,
                current_time=current_time,
            )
            if new_reports:
                remaining = max_contact_reports - len(stone_stone_reports)
                stone_stone_reports.extend(new_reports[:remaining])
        if material_switch_mode == "post-step-distance":
            switch_materials_if_close(current_time)
        while (
            next_snapshot_index < len(pending_snapshots)
            and current_time + 1e-12 >= pending_snapshots[next_snapshot_index]
        ):
            snapshot_time = pending_snapshots[next_snapshot_index]
            snapshots[f"{snapshot_time:.6f}"] = {
                "active": _actor_snapshot(active, use_unity_frame),
                "target": _actor_snapshot(target, use_unity_frame),
            }
            next_snapshot_index += 1
        active_speed = float(np.linalg.norm(_linear_velocity(active)[:2]))
        target_speed = float(np.linalg.norm(_linear_velocity(target)[:2]))
        active_w = abs(float(_angular_velocity(active)[2]))
        target_w = abs(float(_angular_velocity(target)[2]))
        if active_speed < stop_speed and target_speed < stop_speed and active_w < 0.05 and target_w < 0.05:
            still_count += 1
            if still_count >= stop_frames:
                elapsed = (step_index + 1) * dt
                break
        else:
            still_count = 0

    sim_active_arr = _pose_xy(active)
    sim_target_arr = _pose_xy(target)
    sim_active = _from_physx_xy(float(sim_active_arr[0]), float(sim_active_arr[1]), use_unity_frame)
    sim_target = _from_physx_xy(float(sim_target_arr[0]), float(sim_target_arr[1]), use_unity_frame)
    unity_active_in_play = _is_unity_in_play(unity_active)
    unity_target_in_play = _is_unity_in_play(unity_target)

    row: Dict[str, Any] = {
        "sample_id": sample["sample_id"],
        "label": sample.get("label"),
        "active_index": active_index,
        "target_index": target_index,
        "handoff": handoff,
        "target_handoff": target_handoff,
        "handoff_friction": handoff_friction,
        "handoff_center_distance": handoff_center_distance,
        "handoff_v_scale": handoff_v_scale,
        "handoff_vx_offset": handoff_vx_offset,
        "handoff_vy_offset": handoff_vy_offset,
        "handoff_w_offset": handoff_w_offset,
        "angular_sign": angular_sign,
        "handoff_x_offset": handoff_x_offset,
        "handoff_y_offset": handoff_y_offset,
        "target_x_offset": target_x_offset,
        "target_y_offset": target_y_offset,
        "target_settle_time": target_settle_time,
        "active_settle_time": active_settle_time,
        "active_settle_backoff": active_settle_backoff,
        "unity_active": unity_active,
        "unity_target": unity_target,
        "unity_active_in_play": unity_active_in_play,
        "unity_target_in_play": unity_target_in_play,
        "sim_active": sim_active,
        "sim_target": sim_target,
        "elapsed": elapsed,
        "combine_mode": combine_mode_name,
        "friction_offset_threshold": friction_offset_threshold,
        "pre_collision_dynamic_friction": pre_collision_dynamic_friction,
        "pre_collision_static_friction": pre_collision_static_friction,
        "pre_collision_friction_scope": pre_collision_friction_scope,
        "material_switch_mode": material_switch_mode,
        "radius": radius,
        "height": height,
        "stone_faces": stone_faces,
        "inertia_model": inertia_model,
        "inertia_radial": inertia_radial,
        "inertia_vertical": inertia_vertical,
        "active_yaw": active_yaw,
        "active_yaw_source": active_yaw_source,
        "active_yaw_integral_sign": active_yaw_integral_sign,
        "integrated_precontact_yaw": integrated_yaw,
        "effective_active_yaw": effective_active_yaw,
        "effective_active_yaw_deg": math.degrees(effective_active_yaw),
        "target_yaw": target_yaw,
        "target_yaw_source": target_yaw_source,
        "effective_target_yaw": effective_target_yaw,
        "effective_target_yaw_deg": math.degrees(effective_target_yaw),
        "center_height": center_height,
        "shape_local_x": shape_local_x,
        "shape_local_y": shape_local_y,
        "shape_local_z": shape_local_z,
        "shape_local_yaw": shape_local_yaw,
        "scene_flags": list(scene_flag_names),
        "solver_position_iterations": solver_position_iterations,
        "solver_velocity_iterations": solver_velocity_iterations,
        "max_depenetration_velocity": max_depenetration_velocity,
        "disable_stone_gravity": disable_stone_gravity,
        "rink_geometry": rink_geometry,
        "rink_mesh_center_x": rink_mesh_center_x,
        "rink_mesh_center_y": rink_mesh_center_y,
        "rink_mesh_width": rink_mesh_width,
        "rink_mesh_length": rink_mesh_length,
        "rink_mesh_subdivisions": rink_mesh_subdivisions,
        "convex_quantized_count": convex_quantized_count,
        "convex_vertex_limit": convex_vertex_limit,
        "convex_mesh_scale": list(convex_mesh_scale) if convex_mesh_scale is not None else None,
        "quantize_input": quantize_input,
        "gpu_compatible": gpu_compatible,
        "runtime_feature_source": runtime_feature_source,
        "active_runtime_patch": active_runtime_patch,
        "target_runtime_patch": target_runtime_patch,
        "material_switch_time": material_switch_time,
        "material_switch_distance": material_switch_distance,
        "contact_report_enabled": enable_contact_report,
        "active_physx_address": active_address,
        "target_physx_address": target_address,
        "stone_stone_contact_report_count": len(stone_stone_reports),
        "first_stone_stone_contact_time": stone_stone_reports[0]["time"] if stone_stone_reports else None,
        "stone_stone_contact_reports": stone_stone_reports,
        "immediate_contact_probe_enabled": enable_immediate_contact_probe,
        "immediate_contact_probe_count": len(immediate_contact_probes),
        "immediate_contact_probes": immediate_contact_probes,
        "snapshots": snapshots,
    }
    if unity_active_in_play:
        row["active_error"] = math.hypot(sim_active[0] - unity_active[0], sim_active[1] - unity_active[1])
    if unity_target_in_play:
        row["target_error"] = math.hypot(sim_target[0] - unity_target[0], sim_target[1] - unity_target[1])
    return row


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    active_errors = [float(row["active_error"]) for row in rows if "active_error" in row]
    target_errors = [float(row["target_error"]) for row in rows if "target_error" in row]
    all_errors = active_errors + target_errors
    return {
        "sample_count": len(rows),
        "active_error_count": len(active_errors),
        "target_in_play_error_count": len(target_errors),
        "target_cleared_count": sum(1 for row in rows if not row["unity_target_in_play"]),
        "active_rmse_m": _rmse(active_errors),
        "target_in_play_rmse_m": _rmse(target_errors),
        "combined_rmse_m": _rmse(all_errors),
        "active_mean_m": (sum(active_errors) / len(active_errors)) if active_errors else None,
        "target_in_play_mean_m": (sum(target_errors) / len(target_errors)) if target_errors else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sample-id", type=int, action="append", default=[])
    parser.add_argument("--handoff-extra", default="0.0")
    parser.add_argument(
        "--handoff-friction",
        default=str(BASE_FRICTION),
        help=(
            "Comma list for the Newfrictionstep friction used between MOTIONINFO "
            "and the PhysX handoff. Unity samples draw 0.001 +/- 0.0002 per tick."
        ),
    )
    parser.add_argument(
        "--handoff-center-distance",
        default="",
        help=(
            "Comma list. Optional diagnostic center distance for MOTIONINFO -> handoff interpolation. "
            "Empty keeps the historical first distance <= 2R + handoff_extra switch."
        ),
    )
    parser.add_argument("--handoff-v-scale", default="1.0", help="Comma list scaling handoff linear velocity.")
    parser.add_argument(
        "--handoff-vx-offset",
        default="0.0",
        help="Comma list protocol-x velocity offsets added to the active stone at PhysX handoff.",
    )
    parser.add_argument(
        "--handoff-vy-offset",
        default="0.0",
        help="Comma list protocol-y velocity offsets added to the active stone at PhysX handoff.",
    )
    parser.add_argument(
        "--handoff-w-offset",
        default="0.0",
        help="Comma list angular-velocity offsets added to the active stone at PhysX handoff.",
    )
    parser.add_argument(
        "--angular-sign",
        default="1.0",
        help="Comma list scaling the handoff angular velocity sign/magnitude after protocol-to-PhysX mapping.",
    )
    parser.add_argument("--handoff-x-offset", default="0.0", help="Comma list protocol-x offsets added at PhysX handoff.")
    parser.add_argument("--handoff-y-offset", default="0.0", help="Comma list protocol-y offsets added at PhysX handoff.")
    parser.add_argument(
        "--target-settle-time",
        default="0.0",
        help="Comma list. Diagnostic seconds to pre-settle the target stone on the rink before adding the active stone.",
    )
    parser.add_argument(
        "--active-settle-time",
        default="0.0",
        help="Comma list. Diagnostic seconds to pre-settle the active stone on the rink before teleporting it to handoff.",
    )
    parser.add_argument(
        "--active-settle-backoff",
        default="0.5",
        help="Comma list. Backoff distance in meters for active pre-settle, opposite the handoff velocity direction.",
    )
    parser.add_argument("--ice-friction", default="0.02")
    parser.add_argument("--stone-friction", default="0.6")
    parser.add_argument("--stone-restitution", default="1.0")
    parser.add_argument("--radius", default=str(RADIUS))
    parser.add_argument("--height", default=str(HEIGHT))
    parser.add_argument("--stone-faces", default="256", help="Comma list for cylinder faces before convex cooking.")
    parser.add_argument(
        "--stone-geometry",
        choices=STONE_GEOMETRY_MODES,
        default="ring",
        help=(
            "ring preserves the historical generated top/bottom ring points. "
            "formal-recovered uses the recovered ExtendedColliders3D 512-vertex mesh directly."
        ),
    )
    parser.add_argument("--formal-stone-mesh", type=Path, default=DEFAULT_FORMAL_STONE_MESH)
    parser.add_argument("--formal-stone-scale-x", type=float, default=0.1127)
    parser.add_argument("--formal-stone-scale-y", type=float, default=0.115)
    parser.add_argument("--formal-stone-scale-z", type=float, default=0.1127)
    parser.add_argument(
        "--unity-runtime-feature-mode",
        choices=("none", "hull", "hull-bigconvex"),
        default="none",
        help=(
            "Patch pyphysx convex meshes with Unity runtime PhysX feature data captured from "
            "PxcPCMContactConvexConvex: hull uses the 4008-byte ConvexHullData runtime buffer; "
            "hull-bigconvex also patches BigConvexRawData support-map arrays."
        ),
    )
    parser.add_argument(
        "--unity-runtime-feature-events",
        type=Path,
        default=None,
        help="events.jsonl containing a native PxcPCMContactConvexConvex dump with hullRuntime raw bytes.",
    )
    parser.add_argument(
        "--unity-runtime-feature-line",
        type=int,
        default=221,
        help="1-based JSONL line containing the runtime feature dump.",
    )
    parser.add_argument(
        "--unity-runtime-feature-coordinate",
        choices=("pyphysx-zup", "unity-native"),
        default="pyphysx-zup",
        help=(
            "Coordinate interpretation for the captured Unity ConvexHullData raw buffer. "
            "pyphysx-zup swaps y/z coordinate-bearing hull fields before patching the z-up local Scene; "
            "unity-native preserves old byte-for-byte behavior for A/B diagnostics."
        ),
    )
    parser.add_argument(
        "--no-rebuild-bigconvex-from-runtime-hull",
        action="store_true",
        help=(
            "Do not rebuild BigConvexRawData from the possibly coordinate-transformed runtime hull. "
            "Only use this for old A/B checks; the z-up Scene path normally needs rebuilt support-map arrays."
        ),
    )
    parser.add_argument(
        "--synthetic-bigconvex",
        type=Path,
        default=None,
        help=(
            "Optional rebuild_bigconvex_from_runtime_hull.py output. Used only when "
            "--unity-runtime-feature-mode=hull-bigconvex and the capture lacks real arrays."
        ),
    )
    parser.add_argument(
        "--inertia-model",
        default="solid-cylinder",
        help="Comma list: solid-cylinder, thin-shell, pyphysx-default, or custom.",
    )
    parser.add_argument(
        "--inertia-radial",
        default="",
        help="Comma list used only with --inertia-model custom. Applies to horizontal mass-space axes.",
    )
    parser.add_argument(
        "--inertia-vertical",
        default="",
        help="Comma list used only with --inertia-model custom. Applies to the vertical mass-space axis.",
    )
    parser.add_argument(
        "--pre-collision-dynamic-friction",
        default="",
        help=(
            "Comma list. Empty keeps stone dynamic friction equal to --stone-friction from t=0. "
            "Use 0.0 to mimic CurlingStoneNew.Start before OnCollisionEnter resets it to 0.6."
        ),
    )
    parser.add_argument(
        "--pre-collision-static-friction",
        default="",
        help=(
            "Comma list. Empty keeps stone static friction equal to --stone-friction from t=0. "
            "Use 0.0 with --pre-collision-dynamic-friction=0.0 to test formal shot material candidates."
        ),
    )
    parser.add_argument(
        "--pre-collision-friction-scope",
        choices=("active", "target", "both"),
        default="both",
        help="Which stone materials receive the pre-collision friction override.",
    )
    parser.add_argument(
        "--material-switch-mode",
        choices=MATERIAL_SWITCH_MODES,
        default="post-step-distance",
        help=(
            "When pre-collision friction is set, choose when it is restored to --stone-friction. "
            "post-step-distance preserves the historical probe behavior."
        ),
    )
    parser.add_argument("--active-yaw", default="0.0", help="Comma list, radians around the vertical axis.")
    parser.add_argument(
        "--active-yaw-source",
        choices=ACTIVE_YAW_SOURCES,
        default="constant",
        help="constant uses --active-yaw directly; integrated-precontact adds BESTSHOT->handoff yaw estimated from recovered motion.",
    )
    parser.add_argument(
        "--active-yaw-integral-sign",
        default="1.0",
        help="Comma list. Sign/magnitude applied to integrated pre-contact yaw before adding --active-yaw.",
    )
    parser.add_argument("--target-yaw", default="0.0", help="Comma list, radians around the vertical axis.")
    parser.add_argument(
        "--target-yaw-source",
        choices=TARGET_YAW_SOURCES,
        default="constant",
        help="constant uses --target-yaw directly; sample reads per-row target_yaw from the sample file.",
    )
    parser.add_argument("--center-height", default=str(HEIGHT / 2.0))
    parser.add_argument(
        "--scene-flags",
        default="",
        help=(
            "Comma list: enable_pcm, disable_contact_cache, enable_stabilization, "
            "enable_average_point, enable_friction_every_iteration, enable_enhanced_determinism."
        ),
    )
    parser.add_argument(
        "--combine-mode",
        choices=("average", "multiply", "minimum", "maximum"),
        default="multiply",
        help=(
            "Recovered serialized asset value 2 behaves like PhysX Multiply in the alignment probes; "
            "Minimum is also available for checking the managed enum interpretation."
        ),
    )
    parser.add_argument("--contact-offset", default="0.01")
    parser.add_argument("--rest-offset", default="0.0")
    parser.add_argument(
        "--shape-local-x",
        default="0.0",
        help="Comma list of PxShape local x offsets in the PhysX actor frame.",
    )
    parser.add_argument(
        "--shape-local-y",
        default="0.0",
        help="Comma list of PxShape local y offsets in the PhysX actor frame.",
    )
    parser.add_argument(
        "--shape-local-z",
        default="0.0",
        help="Comma list of PxShape local z offsets in the PhysX actor frame.",
    )
    parser.add_argument(
        "--shape-local-yaw",
        default="0.0",
        help="Comma list of PxShape local yaw rotations around the PhysX vertical axis.",
    )
    parser.add_argument(
        "--target-x-offset",
        default="0.0",
        help=(
            "Diagnostic comma list. Protocol x offset applied to the target stone's reset pose before "
            "handoff reconstruction and PhysX placement."
        ),
    )
    parser.add_argument(
        "--target-y-offset",
        default="0.0",
        help=(
            "Diagnostic comma list. Protocol y offset applied to the target stone's reset pose before "
            "handoff reconstruction and PhysX placement."
        ),
    )
    parser.add_argument("--convex-quantized-count", default="255")
    parser.add_argument("--convex-vertex-limit", default="255")
    parser.add_argument(
        "--quantize-input",
        action="store_true",
        help="Enable PxConvexFlag::eQUANTIZE_INPUT. Unity's recovered formal-stone path leaves this off.",
    )
    parser.add_argument(
        "--gpu-compatible",
        action="store_true",
        help="Enable PxConvexFlag::eGPU_COMPATIBLE. Unity's recovered formal-stone path leaves this off.",
    )
    parser.add_argument("--solver-position-iterations", default="6")
    parser.add_argument("--solver-velocity-iterations", default="1")
    parser.add_argument("--max-depenetration-velocity", default="10.0")
    parser.add_argument("--lock-upright", action="store_true")
    parser.add_argument(
        "--disable-stone-gravity",
        action="store_true",
        help="Diagnostic only. Unity formal stones use gravity; this tests whether rink contact coupling is the mismatch.",
    )
    parser.add_argument("--disable-strong-friction", action="store_true")
    parser.add_argument("--improved-patch-friction", action="store_true")
    parser.add_argument(
        "--rink-geometry",
        choices=RINK_GEOMETRY_MODES,
        default="plane",
        help=(
            "plane preserves the historical PxPlane probe. unity-plane-mesh uses a "
            "10x10 triangle grid matching Unity's built-in Plane structure."
        ),
    )
    parser.add_argument("--rink-mesh-center-x", type=float, default=UNITY_PLANE_MESH_CENTER_X_M)
    parser.add_argument("--rink-mesh-center-y", type=float, default=UNITY_PLANE_MESH_CENTER_Y_M)
    parser.add_argument("--rink-mesh-width", type=float, default=UNITY_PLANE_MESH_WIDTH_M)
    parser.add_argument("--rink-mesh-length", type=float, default=UNITY_PLANE_MESH_LENGTH_M)
    parser.add_argument("--rink-mesh-subdivisions", type=int, default=UNITY_PLANE_MESH_SUBDIVISIONS)
    parser.add_argument(
        "--friction-offset-threshold",
        default="",
        help="Comma list. Empty keeps PhysX default (currently 0.04 in pyphysx).",
    )
    parser.add_argument(
        "--use-unity-frame",
        action="store_true",
        help="Run PhysX in Unity horizontal axes and convert protocol coordinates at the boundary.",
    )
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--max-time", type=float, default=20.0)
    parser.add_argument("--stop-speed", type=float, default=0.003)
    parser.add_argument("--stop-frames", type=int, default=500)
    parser.add_argument("--snapshot-times", default="0,0.02,0.05,0.1,0.2,0.5,1.0,2.0")
    parser.add_argument(
        "--enable-contact-report",
        action="store_true",
        help="Enable pyphysx PxSimulationEventCallback contact reports and keep active-target reports in each row.",
    )
    parser.add_argument(
        "--max-contact-reports",
        type=int,
        default=8,
        help="Maximum active-target contact report entries stored per sample when --enable-contact-report is set.",
    )
    parser.add_argument(
        "--enable-immediate-contact-probe",
        action="store_true",
        help=(
            "Call pyphysx.generate_contacts_between around each simulation step to dump "
            "local immediate-mode ContactBuffer-like fields."
        ),
    )
    parser.add_argument(
        "--max-immediate-contact-probes",
        type=int,
        default=8,
        help="Maximum pre/post step immediate contact probe entries stored per sample.",
    )
    parser.add_argument(
        "--immediate-contact-distance",
        type=float,
        default=-1.0,
        help="PxGenerateContacts contactDistance. Negative uses shape0+shape1 contact offsets.",
    )
    parser.add_argument(
        "--immediate-mesh-contact-margin",
        type=float,
        default=-1.0,
        help="PxGenerateContacts meshContactMargin. Negative uses 0.01m.",
    )
    parser.add_argument(
        "--immediate-tolerance-length",
        type=float,
        default=-1.0,
        help="PxGenerateContacts toleranceLength. Negative uses Physics tolerances scale.",
    )
    args = parser.parse_args()

    samples = _read_samples(args.samples)
    if args.sample_id:
        allowed = set(args.sample_id)
        samples = [sample for sample in samples if int(sample["sample_id"]) in allowed]
    if not samples:
        raise SystemExit("no matching collision samples")

    formal_points: Optional[np.ndarray] = None
    if args.unity_runtime_feature_mode != "none" and args.stone_geometry != "formal-recovered":
        raise SystemExit("--unity-runtime-feature-mode requires --stone-geometry formal-recovered")
    if args.stone_geometry == "formal-recovered":
        formal_points = _formal_stone_points(args.formal_stone_mesh)

    runtime_hull_raw_bytes: Optional[List[int]] = None
    runtime_big_convex_arrays: Optional[Dict[str, List[int]]] = None
    runtime_feature_source: Optional[str] = None
    runtime_feature_meta: Dict[str, Any] = {"mode": args.unity_runtime_feature_mode}
    if args.unity_runtime_feature_mode != "none":
        from tools.reverse.probe_unity_runtime_hull_patch_contacts import (
            _load_synthetic_bigconvex,
            _load_unity_runtime_feature_bundle,
        )

        if args.unity_runtime_feature_events is None:
            raise SystemExit("--unity-runtime-feature-events is required when runtime feature mode is enabled")
        unity_bundle = _load_unity_runtime_feature_bundle(
            args.unity_runtime_feature_events,
            args.unity_runtime_feature_line,
        )
        runtime_hull_raw_bytes = [int(value) & 0xFF for value in unity_bundle["hull_raw_bytes"]]
        runtime_feature_source = (
            f"runtime_capture:{args.unity_runtime_feature_events}:{args.unity_runtime_feature_line}"
        )
        runtime_hull_source = _runtime_hull_source_from_bundle(runtime_hull_raw_bytes, unity_bundle)
        original_hull_sha16 = _sha16_bytes(runtime_hull_raw_bytes)
        hull_transform = "none"
        if args.unity_runtime_feature_coordinate == "pyphysx-zup":
            runtime_hull_raw_bytes = _transform_runtime_hull_raw_unity_xyz_to_pyphysx_xzy(
                runtime_hull_raw_bytes,
                layout=runtime_hull_source["layout"],
                nb_polygons=int(runtime_hull_source["nb_polygons"]),
                nb_vertices=int(runtime_hull_source["nb_vertices"]),
            )
            runtime_hull_source = dict(runtime_hull_source)
            runtime_hull_source["raw"] = bytes(int(value) & 0xFF for value in runtime_hull_raw_bytes)
            hull_transform = "unity_xyz_to_pyphysx_xzy"
        runtime_feature_meta.update(
            {
                "source": runtime_feature_source,
                "coordinate_mode": args.unity_runtime_feature_coordinate,
                "hull_transform": hull_transform,
                "hull_raw_bytes": len(runtime_hull_raw_bytes),
                "hull_raw_sha16_original": original_hull_sha16,
                "hull_raw_sha16_patched": _sha16_bytes(runtime_hull_raw_bytes),
                "hull_counts": {
                    "nb_polygons": int(runtime_hull_source["nb_polygons"]),
                    "nb_vertices": int(runtime_hull_source["nb_vertices"]),
                    "nb_edges": int(runtime_hull_source["nb_edges"]),
                    "vertex_ref_count": int(runtime_hull_source["vertex_ref_count"]),
                    "has_grb_edges": bool(runtime_hull_source.get("has_grb_edges")),
                },
                "big_convex_decoded": unity_bundle.get("big_convex"),
                "big_convex_arrays_complete": bool(unity_bundle.get("big_convex_arrays_complete")),
                "big_convex_lengths": {
                    "samples": len(unity_bundle["samples_raw_bytes"])
                    if isinstance(unity_bundle.get("samples_raw_bytes"), list)
                    else None,
                    "samples_expected": unity_bundle.get("samples_expected_bytes"),
                    "valencies": len(unity_bundle["valencies_raw_bytes"])
                    if isinstance(unity_bundle.get("valencies_raw_bytes"), list)
                    else None,
                    "valencies_expected": unity_bundle.get("valencies_expected_bytes"),
                    "adjacent_vertices": len(unity_bundle["adjacent_vertices_raw_bytes"])
                    if isinstance(unity_bundle.get("adjacent_vertices_raw_bytes"), list)
                    else None,
                    "adjacent_vertices_expected": unity_bundle.get("adjacent_vertices_expected_bytes"),
                },
            }
        )
        if args.unity_runtime_feature_mode == "hull-bigconvex":
            should_rebuild_bigconvex = not args.no_rebuild_bigconvex_from_runtime_hull
            if should_rebuild_bigconvex:
                from tools.reverse.rebuild_bigconvex_from_runtime_hull import _rebuild_from_runtime_hull

                rebuilt_bigconvex = _rebuild_from_runtime_hull(runtime_hull_source, 16)
                runtime_big_convex_arrays = _bigconvex_arrays_from_rebuild(rebuilt_bigconvex)
                runtime_feature_meta["big_convex_source"] = (
                    f"rebuilt_from_runtime_hull:{args.unity_runtime_feature_coordinate}:subdiv16"
                )
                runtime_feature_meta["big_convex_rebuild"] = {
                    "source_raw_sha16": rebuilt_bigconvex["source"]["raw_sha16"],
                    "lengths": rebuilt_bigconvex["big_convex"]["lengths"],
                    "samples_sha16": rebuilt_bigconvex["big_convex"]["samples_sha16"],
                    "valencies_sha16": rebuilt_bigconvex["big_convex"]["valencies_sha16"],
                    "adjacent_vertices_sha16": rebuilt_bigconvex["big_convex"]["adjacent_vertices_sha16"],
                    "edge_checks": rebuilt_bigconvex["edge_checks"],
                }
            elif unity_bundle.get("big_convex_arrays_complete"):
                runtime_big_convex_arrays = {
                    "samples_raw_bytes": [int(value) & 0xFF for value in unity_bundle["samples_raw_bytes"]],
                    "valencies_raw_bytes": [int(value) & 0xFF for value in unity_bundle["valencies_raw_bytes"]],
                    "adjacent_vertices_raw_bytes": [
                        int(value) & 0xFF for value in unity_bundle["adjacent_vertices_raw_bytes"]
                    ],
                }
                runtime_feature_meta["big_convex_source"] = "runtime_capture"
            elif args.synthetic_bigconvex is not None:
                runtime_big_convex_arrays = _load_synthetic_bigconvex(args.synthetic_bigconvex)
                runtime_feature_meta["big_convex_source"] = f"synthetic_rebuild:{args.synthetic_bigconvex}"
                runtime_feature_meta["synthetic_bigconvex"] = str(args.synthetic_bigconvex)
            else:
                raise SystemExit(
                    "runtime capture lacks complete BigConvex arrays; rerun Unity sampling with nested raw "
                    "or pass --synthetic-bigconvex explicitly"
                )

    result_sets = []
    combine_mode = _combine_mode_from_name(args.combine_mode)
    scene_flag_names = [part.strip() for part in args.scene_flags.split(",") if part.strip()]
    scene_flags = _scene_flags_from_names(scene_flag_names)
    snapshot_times = _parse_float_list(args.snapshot_times)
    friction_offset_thresholds: List[Optional[float]]
    if args.friction_offset_threshold.strip():
        friction_offset_thresholds = [float(value) for value in _parse_float_list(args.friction_offset_threshold)]
    else:
        friction_offset_thresholds = [None]
    pre_collision_dynamic_frictions: List[Optional[float]]
    if args.pre_collision_dynamic_friction.strip():
        pre_collision_dynamic_frictions = [
            float(value) for value in _parse_float_list(args.pre_collision_dynamic_friction)
        ]
    else:
        pre_collision_dynamic_frictions = [None]
    pre_collision_static_frictions: List[Optional[float]]
    if args.pre_collision_static_friction.strip():
        pre_collision_static_frictions = [
            float(value) for value in _parse_float_list(args.pre_collision_static_friction)
        ]
    else:
        pre_collision_static_frictions = [None]
    inertia_models = [part.strip() for part in args.inertia_model.split(",") if part.strip()]
    inertia_radials: List[Optional[float]]
    inertia_verticals: List[Optional[float]]
    inertia_radials = _parse_float_list(args.inertia_radial) if args.inertia_radial.strip() else [None]
    inertia_verticals = _parse_float_list(args.inertia_vertical) if args.inertia_vertical.strip() else [None]
    handoff_center_distances: List[Optional[float]]
    if args.handoff_center_distance.strip():
        handoff_center_distances = [float(value) for value in _parse_float_list(args.handoff_center_distance)]
    else:
        handoff_center_distances = [None]
    for (
        handoff_extra,
        handoff_friction,
        handoff_center_distance,
        handoff_v_scale,
        handoff_vx_offset,
        handoff_vy_offset,
        handoff_w_offset,
        angular_sign,
        handoff_x_offset,
        handoff_y_offset,
        target_x_offset,
        target_y_offset,
        target_settle_time,
        active_settle_time,
        active_settle_backoff,
        ice_friction,
        stone_friction,
        stone_restitution,
        radius,
        height,
        stone_faces,
        inertia_model,
        inertia_radial,
        inertia_vertical,
        contact_offset,
        rest_offset,
        shape_local_x,
        shape_local_y,
        shape_local_z,
        shape_local_yaw,
        active_yaw,
        active_yaw_integral_sign,
        target_yaw,
        center_height,
        convex_quantized_count,
        convex_vertex_limit,
        solver_position_iterations,
        solver_velocity_iterations,
        max_depenetration_velocity,
        friction_offset_threshold,
        pre_collision_dynamic_friction,
        pre_collision_static_friction,
    ) in itertools.product(
        _parse_float_list(args.handoff_extra),
        _parse_float_list(args.handoff_friction),
        handoff_center_distances,
        _parse_float_list(args.handoff_v_scale),
        _parse_float_list(args.handoff_vx_offset),
        _parse_float_list(args.handoff_vy_offset),
        _parse_float_list(args.handoff_w_offset),
        _parse_float_list(args.angular_sign),
        _parse_float_list(args.handoff_x_offset),
        _parse_float_list(args.handoff_y_offset),
        _parse_float_list(args.target_x_offset),
        _parse_float_list(args.target_y_offset),
        _parse_float_list(args.target_settle_time),
        _parse_float_list(args.active_settle_time),
        _parse_float_list(args.active_settle_backoff),
        _parse_float_list(args.ice_friction),
        _parse_float_list(args.stone_friction),
        _parse_float_list(args.stone_restitution),
        _parse_float_list(args.radius),
        _parse_float_list(args.height),
        [int(value) for value in _parse_float_list(args.stone_faces)],
        inertia_models,
        inertia_radials,
        inertia_verticals,
        _parse_float_list(args.contact_offset),
        _parse_float_list(args.rest_offset),
        _parse_float_list(args.shape_local_x),
        _parse_float_list(args.shape_local_y),
        _parse_float_list(args.shape_local_z),
        _parse_float_list(args.shape_local_yaw),
        _parse_float_list(args.active_yaw),
        _parse_float_list(args.active_yaw_integral_sign),
        _parse_float_list(args.target_yaw),
        _parse_float_list(args.center_height),
        [int(value) for value in _parse_float_list(args.convex_quantized_count)],
        [int(value) for value in _parse_float_list(args.convex_vertex_limit)],
        [int(value) for value in _parse_float_list(args.solver_position_iterations)],
        [int(value) for value in _parse_float_list(args.solver_velocity_iterations)],
        _parse_float_list(args.max_depenetration_velocity),
        friction_offset_thresholds,
        pre_collision_dynamic_frictions,
        pre_collision_static_frictions,
    ):
        if args.stone_geometry == "formal-recovered":
            assert formal_points is not None
            stone_points = formal_points
            convex_mesh_scale: Optional[List[float]] = [
                args.formal_stone_scale_x,
                args.formal_stone_scale_z,
                args.formal_stone_scale_y,
            ]
        else:
            stone_points = _stone_points(radius=radius, height=height, faces=stone_faces)
            convex_mesh_scale = None
        rows = [
            _simulate_one(
                sample,
                handoff_extra=handoff_extra,
                handoff_friction=handoff_friction,
                handoff_center_distance=handoff_center_distance,
                handoff_v_scale=handoff_v_scale,
                handoff_vx_offset=handoff_vx_offset,
                handoff_vy_offset=handoff_vy_offset,
                handoff_w_offset=handoff_w_offset,
                angular_sign=angular_sign,
                handoff_x_offset=handoff_x_offset,
                handoff_y_offset=handoff_y_offset,
                target_x_offset=target_x_offset,
                target_y_offset=target_y_offset,
                ice_friction=ice_friction,
                stone_friction=stone_friction,
                stone_restitution=stone_restitution,
                pre_collision_dynamic_friction=pre_collision_dynamic_friction,
                pre_collision_static_friction=pre_collision_static_friction,
                pre_collision_friction_scope=args.pre_collision_friction_scope,
                material_switch_mode=args.material_switch_mode,
                stone_points=stone_points,
                radius=radius,
                height=height,
                stone_faces=stone_faces,
                inertia_model=inertia_model,
                inertia_radial=inertia_radial,
                inertia_vertical=inertia_vertical,
                active_yaw=active_yaw,
                active_yaw_source=args.active_yaw_source,
                active_yaw_integral_sign=active_yaw_integral_sign,
                target_yaw=target_yaw,
                target_yaw_source=args.target_yaw_source,
                center_height=center_height,
                scene_flags=scene_flags,
                scene_flag_names=scene_flag_names,
                combine_mode=combine_mode,
                combine_mode_name=args.combine_mode,
                contact_offset=contact_offset,
                rest_offset=rest_offset,
                shape_local_x=shape_local_x,
                shape_local_y=shape_local_y,
                shape_local_z=shape_local_z,
                shape_local_yaw=shape_local_yaw,
                convex_quantized_count=convex_quantized_count,
                convex_vertex_limit=convex_vertex_limit,
                convex_mesh_scale=convex_mesh_scale,
                quantize_input=args.quantize_input,
                gpu_compatible=args.gpu_compatible,
                runtime_hull_raw_bytes=runtime_hull_raw_bytes,
                runtime_big_convex_arrays=runtime_big_convex_arrays,
                runtime_feature_source=runtime_feature_source,
                solver_position_iterations=solver_position_iterations,
                solver_velocity_iterations=solver_velocity_iterations,
                max_depenetration_velocity=max_depenetration_velocity,
                lock_upright=args.lock_upright,
                disable_stone_gravity=args.disable_stone_gravity,
                disable_strong_friction=args.disable_strong_friction,
                improved_patch_friction=args.improved_patch_friction,
                rink_geometry=args.rink_geometry,
                rink_mesh_center_x=args.rink_mesh_center_x,
                rink_mesh_center_y=args.rink_mesh_center_y,
                rink_mesh_width=args.rink_mesh_width,
                rink_mesh_length=args.rink_mesh_length,
                rink_mesh_subdivisions=args.rink_mesh_subdivisions,
                use_unity_frame=args.use_unity_frame,
                friction_offset_threshold=friction_offset_threshold,
                dt=args.dt,
                max_time=args.max_time,
                stop_speed=args.stop_speed,
                stop_frames=args.stop_frames,
                snapshot_times=snapshot_times,
                enable_contact_report=args.enable_contact_report,
                max_contact_reports=args.max_contact_reports,
                enable_immediate_contact_probe=args.enable_immediate_contact_probe,
                max_immediate_contact_probes=args.max_immediate_contact_probes,
                immediate_contact_distance=args.immediate_contact_distance,
                immediate_mesh_contact_margin=args.immediate_mesh_contact_margin,
                immediate_tolerance_length=args.immediate_tolerance_length,
                target_settle_time=target_settle_time,
                active_settle_time=active_settle_time,
                active_settle_backoff=active_settle_backoff,
            )
            for sample in samples
        ]
        config = {
            "handoff_extra": handoff_extra,
            "handoff_friction": handoff_friction,
            "handoff_center_distance": handoff_center_distance,
            "handoff_v_scale": handoff_v_scale,
            "handoff_vx_offset": handoff_vx_offset,
            "handoff_vy_offset": handoff_vy_offset,
            "handoff_w_offset": handoff_w_offset,
            "angular_sign": angular_sign,
            "handoff_x_offset": handoff_x_offset,
            "handoff_y_offset": handoff_y_offset,
            "target_x_offset": target_x_offset,
            "target_y_offset": target_y_offset,
            "target_settle_time": target_settle_time,
            "active_settle_time": active_settle_time,
            "active_settle_backoff": active_settle_backoff,
            "ice_friction": ice_friction,
            "stone_friction": stone_friction,
            "stone_restitution": stone_restitution,
            "pre_collision_dynamic_friction": pre_collision_dynamic_friction,
            "pre_collision_static_friction": pre_collision_static_friction,
            "pre_collision_friction_scope": args.pre_collision_friction_scope,
            "material_switch_mode": args.material_switch_mode,
            "stone_geometry": args.stone_geometry,
            "formal_stone_mesh": str(args.formal_stone_mesh) if args.stone_geometry == "formal-recovered" else None,
            "formal_stone_scale": [
                args.formal_stone_scale_x,
                args.formal_stone_scale_y,
                args.formal_stone_scale_z,
            ]
            if args.stone_geometry == "formal-recovered"
            else None,
            "radius": radius,
            "height": height,
            "stone_faces": stone_faces,
            "inertia_model": inertia_model,
            "inertia_radial": inertia_radial,
            "inertia_vertical": inertia_vertical,
            "active_yaw": active_yaw,
            "active_yaw_source": args.active_yaw_source,
            "active_yaw_integral_sign": active_yaw_integral_sign,
            "target_yaw": target_yaw,
            "target_yaw_source": args.target_yaw_source,
            "center_height": center_height,
            "scene_flags": scene_flag_names,
            "combine_mode": args.combine_mode,
            "contact_offset": contact_offset,
            "rest_offset": rest_offset,
            "shape_local_x": shape_local_x,
            "shape_local_y": shape_local_y,
            "shape_local_z": shape_local_z,
            "shape_local_yaw": shape_local_yaw,
            "convex_quantized_count": convex_quantized_count,
            "convex_vertex_limit": convex_vertex_limit,
            "convex_mesh_scale": convex_mesh_scale,
            "quantize_input": args.quantize_input,
            "gpu_compatible": args.gpu_compatible,
            "unity_runtime_feature": runtime_feature_meta,
            "solver_position_iterations": solver_position_iterations,
            "solver_velocity_iterations": solver_velocity_iterations,
            "max_depenetration_velocity": max_depenetration_velocity,
            "lock_upright": args.lock_upright,
            "disable_stone_gravity": args.disable_stone_gravity,
            "disable_strong_friction": args.disable_strong_friction,
            "improved_patch_friction": args.improved_patch_friction,
            "rink_geometry": args.rink_geometry,
            "rink_mesh_center_x": args.rink_mesh_center_x,
            "rink_mesh_center_y": args.rink_mesh_center_y,
            "rink_mesh_width": args.rink_mesh_width,
            "rink_mesh_length": args.rink_mesh_length,
            "rink_mesh_subdivisions": args.rink_mesh_subdivisions,
            "friction_offset_threshold": friction_offset_threshold,
            "use_unity_frame": args.use_unity_frame,
            "dt": args.dt,
            "max_time": args.max_time,
            "enable_contact_report": args.enable_contact_report,
            "max_contact_reports": args.max_contact_reports,
            "enable_immediate_contact_probe": args.enable_immediate_contact_probe,
            "max_immediate_contact_probes": args.max_immediate_contact_probes,
            "immediate_contact_distance": args.immediate_contact_distance,
            "immediate_mesh_contact_margin": args.immediate_mesh_contact_margin,
            "immediate_tolerance_length": args.immediate_tolerance_length,
            "pyphysx_scene_note": PYPHYSX_SCENE_NOTE,
            "pyphysx_convex_cooking_caveat": PYPHYSX_CONVEX_COOKING_CAVEAT,
        }
        result_sets.append({"config": config, "summary": _summarize(rows), "rows": rows})

    payload = {"samples": str(args.samples), "result_sets": result_sets}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    best = min(
        result_sets,
        key=lambda item: float("inf")
        if item["summary"]["combined_rmse_m"] is None
        else item["summary"]["combined_rmse_m"],
    )
    print(json.dumps({"output": str(args.output), "best": best["config"], "summary": best["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
