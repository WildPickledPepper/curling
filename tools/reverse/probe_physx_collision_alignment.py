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
import itertools
import json
import math
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
ACTIVE_YAW_SOURCES = ("constant", "integrated-precontact")
UNITY_PLANE_MESH_WIDTH_M = 9.9568
UNITY_PLANE_MESH_LENGTH_M = 49.98
UNITY_PLANE_MESH_CENTER_X_M = 2.375
UNITY_PLANE_MESH_CENTER_Y_M = 14.0
UNITY_PLANE_MESH_SUBDIVISIONS = 10


def _parse_float_list(value: str) -> List[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


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


def _formal_stone_points(
    path: Path,
    *,
    scale_x: float,
    scale_y: float,
    scale_z: float,
) -> np.ndarray:
    """Load recovered Unity x/y/z mesh vertices into the z-up PhysX shape frame."""
    data = json.loads(path.read_text(encoding="utf-8"))
    points = []
    for vertex in data["vertices"]:
        unity_x = float(vertex[0]) * scale_x
        unity_y = float(vertex[1]) * scale_y
        unity_z = float(vertex[2]) * scale_z
        points.append([unity_x, unity_z, unity_y])
    return np.asarray(points, dtype=np.float32)


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


def _make_stone(
    x: float,
    y: float,
    vx: float,
    vy: float,
    w: float,
    yaw: float,
    *,
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
    quantize_input: bool,
    gpu_compatible: bool,
    solver_position_iterations: int,
    solver_velocity_iterations: int,
    max_depenetration_velocity: float,
    lock_upright: bool,
    disable_stone_gravity: bool,
    disable_strong_friction: bool,
    improved_patch_friction: bool,
) -> Tuple[Any, Any, Any]:
    material = _make_material(
        static_friction,
        dynamic_friction,
        stone_restitution,
        combine_mode=combine_mode,
        disable_strong_friction=disable_strong_friction,
        improved_patch_friction=improved_patch_friction,
    )
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
                [0.0, 0.0, math.sin(0.5 * shape_local_yaw), math.cos(0.5 * shape_local_yaw)],
            )
        )

    body = pyphysx.RigidDynamic()
    body.attach_shape(shape)
    body.set_mass(MASS)
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
    body.set_global_pose(([x, y, center_height], [0.0, 0.0, math.sin(0.5 * yaw), math.cos(0.5 * yaw)]))
    body.set_linear_velocity([vx, vy, 0.0])
    body.set_angular_velocity([0.0, 0.0, w])
    return body, shape, material


def _handoff_state(
    sample: Dict[str, Any],
    target_xy: Tuple[float, float],
    threshold: float,
    handoff_friction: float,
) -> Dict[str, float]:
    x, y, vx, vy, w = [float(value) for value in sample["motioninfo"]]
    tx, ty = target_xy
    best_distance = float("inf")
    best_step = 0
    for step_index in range(6000):
        distance = math.hypot(x - tx, y - ty)
        if distance < best_distance:
            best_distance = distance
            best_step = step_index
        if distance <= threshold:
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
        "w": float(handoff_state["w"]),
        "distance": float(handoff_state.get("distance", 0.0)),
        "threshold": float(handoff_state.get("threshold", 0.0)),
        "source": str(handoff_state.get("source", "explicit")),
    }


def _actor_snapshot(actor: Any, use_unity_frame: bool) -> Dict[str, Any]:
    position, quaternion = pyphysx.cast_transformation(actor.get_global_pose())
    physx_position = np.asarray(position, dtype=float)
    physx_quaternion = [
        float(getattr(quaternion, "x")),
        float(getattr(quaternion, "y")),
        float(getattr(quaternion, "z")),
        float(getattr(quaternion, "w")),
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
    }


def _set_pose_xy_yaw(actor: Any, x: float, y: float, z: float, yaw: float) -> None:
    actor.set_global_pose(([x, y, z], [0.0, 0.0, math.sin(0.5 * yaw), math.cos(0.5 * yaw)]))


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
    quantize_input: bool,
    gpu_compatible: bool,
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
    handoff_friction: float,
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
        handoff = _handoff_state(sample, target_physics_before, threshold, handoff_friction)
    integrated_yaw = _integrated_precontact_yaw(
        sample,
        target_physics_before,
        threshold,
        friction=handoff_friction,
    )
    effective_active_yaw = active_yaw
    if active_yaw_source == "integrated-precontact":
        effective_active_yaw = active_yaw + active_yaw_integral_sign * float(integrated_yaw["yaw"])

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
    target_x, target_y = _to_physx_xy(target_physics_before[0], target_physics_before[1], use_unity_frame)

    apply_pre_active = pre_collision_friction_scope in {"active", "both"}
    apply_pre_target = pre_collision_friction_scope in {"target", "both"}
    active, _active_shape, _active_material = _make_stone(
        active_x,
        active_y,
        active_vx,
        active_vy,
        active_w,
        effective_active_yaw,
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
        quantize_input=quantize_input,
        gpu_compatible=gpu_compatible,
        solver_position_iterations=solver_position_iterations,
        solver_velocity_iterations=solver_velocity_iterations,
        max_depenetration_velocity=max_depenetration_velocity,
        lock_upright=lock_upright,
        disable_stone_gravity=disable_stone_gravity,
        disable_strong_friction=disable_strong_friction,
        improved_patch_friction=improved_patch_friction,
    )
    target, _target_shape, _target_material = _make_stone(
        target_x,
        target_y,
        0.0,
        0.0,
        0.0,
        target_yaw,
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
        quantize_input=quantize_input,
        gpu_compatible=gpu_compatible,
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
        active.set_linear_velocity([active_vx, active_vy, 0.0])
        active.set_angular_velocity([0.0, 0.0, active_w])
        if target_added:
            _zero_actor_velocity(target)

    if not active_added:
        scene.add_actor(active)
        active_added = True
    if not target_added:
        scene.add_actor(target)
        target_added = True

    active_address = _actor_address(active)
    target_address = _actor_address(target)
    stone_stone_reports: List[Dict[str, Any]] = []

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
        if material_switch_mode == "pre-step-distance":
            switch_materials_if_close(step_index * dt)
        scene.simulate(dt)
        current_time = (step_index + 1) * dt
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
        "handoff_friction": handoff_friction,
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
        "quantize_input": quantize_input,
        "gpu_compatible": gpu_compatible,
        "material_switch_time": material_switch_time,
        "material_switch_distance": material_switch_distance,
        "contact_report_enabled": enable_contact_report,
        "active_physx_address": active_address,
        "target_physx_address": target_address,
        "stone_stone_contact_report_count": len(stone_stone_reports),
        "first_stone_stone_contact_time": stone_stone_reports[0]["time"] if stone_stone_reports else None,
        "stone_stone_contact_reports": stone_stone_reports,
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
    args = parser.parse_args()

    samples = _read_samples(args.samples)
    if args.sample_id:
        allowed = set(args.sample_id)
        samples = [sample for sample in samples if int(sample["sample_id"]) in allowed]
    if not samples:
        raise SystemExit("no matching collision samples")

    formal_points: Optional[np.ndarray] = None
    if args.stone_geometry == "formal-recovered":
        formal_points = _formal_stone_points(
            args.formal_stone_mesh,
            scale_x=args.formal_stone_scale_x,
            scale_y=args.formal_stone_scale_y,
            scale_z=args.formal_stone_scale_z,
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
    for (
        handoff_extra,
        handoff_friction,
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
        else:
            stone_points = _stone_points(radius=radius, height=height, faces=stone_faces)
        rows = [
            _simulate_one(
                sample,
                handoff_extra=handoff_extra,
                handoff_friction=handoff_friction,
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
                quantize_input=args.quantize_input,
                gpu_compatible=args.gpu_compatible,
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
                target_settle_time=target_settle_time,
                active_settle_time=active_settle_time,
                active_settle_backoff=active_settle_backoff,
            )
            for sample in samples
        ]
        config = {
            "handoff_extra": handoff_extra,
            "handoff_friction": handoff_friction,
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
            "quantize_input": args.quantize_input,
            "gpu_compatible": args.gpu_compatible,
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
