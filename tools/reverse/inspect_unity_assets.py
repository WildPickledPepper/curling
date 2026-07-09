"""Inspect Unity assets relevant to the curling physics reverse pass.

This script focuses on data that UnityPy can recover reliably from the
WebGL data bundle: tags, global physics settings, stone rigidbodies, and the
runtime-generated ExtendedColliders3D mesh-collider setup.
"""

from __future__ import annotations

import argparse
import os
import re
import struct
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Iterable

import UnityPy


CUSTOM_TAG_BASE = 20000

INTERESTING_SCENE_SCRIPTS = {
    "AIBattleController",
    "AutoDCP",
    "DCP",
    "DCP_HumanVSAI",
    "FastDCP",
    "HumanInputController",
    "MotionTest",
    "MotionTestStone",
    "ScenesController",
    "UrlParamReader",
    "WaitMenuControl",
}

INTERESTING_SCENE_OBJECTS = {
    "BtnDebug Contest",
    "BtnFastGame",
    "BtnFinalContest",
    "BtnHumanVsAI",
    "BtnMotionTest",
    "BtnNoLimit Contest",
    "BtnPreliminary Contest",
    "DCP",
    "DCP_HumanVSAI",
    "FastDCP",
    "AutoDCP",
    "ReadRecord",
    "SceneControl",
    "SendIsReady",
    "StartGame",
    "StartHisGame",
    "UrlParamReader",
    "btnStartAI",
}


@dataclass
class ExtendedColliderProps:
    convex: bool
    is_trigger: bool
    material_file_id: int
    material_path_id: int
    material_name: str
    collider_type: int
    centre: tuple[float, float, float]
    rotation: tuple[float, float, float]
    size: tuple[float, float, float]
    flip_faces: bool
    circle_vertices: int
    circle_two_sided: bool
    cone_faces: int
    cylinder_faces: int
    cylinder_cap_top: bool
    cylinder_cap_bottom: bool
    cylinder_taper_top: tuple[float, float]
    cylinder_taper_bottom: tuple[float, float]
    sphere_stacks: int
    sphere_slices: int


def _read_vec3(raw: bytes, offset: int) -> tuple[tuple[float, float, float], int]:
    return struct.unpack_from("<fff", raw, offset), offset + 12


def _read_vec2(raw: bytes, offset: int) -> tuple[tuple[float, float], int]:
    return struct.unpack_from("<ff", raw, offset), offset + 8


def _safe_name(reader_or_obj: Any) -> str:
    try:
        obj = reader_or_obj.read() if hasattr(reader_or_obj, "read") else reader_or_obj
        return getattr(obj, "m_Name", "") or getattr(obj, "name", "") or ""
    except Exception:
        return ""


def _read_aligned_string(raw: bytes, offset: int) -> tuple[str, int]:
    length = struct.unpack_from("<i", raw, offset)[0]
    offset += 4
    value = raw[offset : offset + length].decode("utf-8", errors="replace")
    offset += length
    offset = (offset + 3) & ~3
    return value, offset


def _script_name(reader: Any) -> str:
    try:
        head = reader.parse_monobehaviour_head()
        return head.m_Script.read().m_Name
    except Exception:
        return ""


def _resolve_external_name(assets_file: Any, file_id: int, path_id: int) -> str:
    if file_id == 0:
        reader = assets_file.objects.get(path_id)
    else:
        externals = getattr(assets_file, "externals", [])
        if file_id - 1 >= len(externals):
            return ""
        external_name = externals[file_id - 1].name
        env = assets_file.environment
        external_file = None
        for object_reader in env.objects:
            candidate = object_reader.assets_file
            if getattr(candidate, "name", None) == external_name:
                external_file = candidate
                break
        if external_file is None:
            return external_name
        reader = external_file.objects.get(path_id)
    if reader is None:
        return ""
    name = _safe_name(reader)
    return name or reader.type.name


def _describe_pptr(assets_file: Any, pointer: Any) -> str:
    file_id = getattr(pointer, "m_FileID", 0)
    path_id = getattr(pointer, "m_PathID", 0)
    if path_id == 0:
        return "None"

    if file_id == 0:
        reader = assets_file.objects.get(path_id)
        if reader is None:
            return f"local:{path_id} (unresolved)"
        name = _safe_name(reader)
        return f"local:{path_id} {reader.type.name} {name}".rstrip()

    externals = getattr(assets_file, "externals", [])
    external_name = "<external>"
    if file_id - 1 < len(externals):
        external_name = externals[file_id - 1].name

    external_file = None
    env = assets_file.environment
    for object_reader in env.objects:
        candidate = object_reader.assets_file
        if getattr(candidate, "name", None) == external_name:
            external_file = candidate
            break

    if external_file is None:
        return f"{external_name}:{path_id} (unresolved)"

    reader = external_file.objects.get(path_id)
    if reader is None:
        return f"{external_name}:{path_id} (unresolved)"
    name = _safe_name(reader)
    return f"{external_name}:{path_id} {reader.type.name} {name}".rstrip()


def parse_extended_collider_props(reader: Any) -> ExtendedColliderProps:
    raw = reader.get_raw_data()

    # MonoBehaviour header is 32 bytes here. The serializable properties object
    # starts immediately after it. Unity aligns serialized bool fields to four
    # bytes in this typetree, which is why consecutive bools advance by four.
    offset = 32
    convex = bool(raw[offset])
    offset += 4
    is_trigger = bool(raw[offset])
    offset += 4

    material_file_id = struct.unpack_from("<i", raw, offset)[0]
    material_path_id = struct.unpack_from("<q", raw, offset + 4)[0]
    material_name = _resolve_external_name(reader.assets_file, material_file_id, material_path_id)
    offset += 12

    collider_type = struct.unpack_from("<i", raw, offset)[0]
    offset += 4
    centre, offset = _read_vec3(raw, offset)
    rotation, offset = _read_vec3(raw, offset)
    size, offset = _read_vec3(raw, offset)

    flip_faces = bool(raw[offset])
    offset += 4
    circle_vertices = struct.unpack_from("<i", raw, offset)[0]
    offset += 4
    circle_two_sided = bool(raw[offset])
    offset += 4
    cone_faces = struct.unpack_from("<i", raw, offset)[0]
    offset += 4

    # Cone and cube face flags are serialized as aligned bools.
    offset += 4  # coneCap
    offset += 4  # coneHalfCapFlatEnd
    offset += 4  # cubeTopFace
    offset += 4  # cubeBottomFace
    offset += 4  # cubeLeftFace
    offset += 4  # cubeRightFace
    offset += 4  # cubeForwardFace
    offset += 4  # cubeBackFace

    cylinder_faces = struct.unpack_from("<i", raw, offset)[0]
    offset += 4
    cylinder_cap_top = bool(raw[offset])
    offset += 4
    cylinder_cap_bottom = bool(raw[offset])
    offset += 4
    cylinder_taper_top, offset = _read_vec2(raw, offset)
    cylinder_taper_bottom, offset = _read_vec2(raw, offset)

    # cylinderHalfCapFlatEnd, quadTwoSided, triangleTwoSided.
    offset += 4
    offset += 4
    offset += 4
    sphere_stacks = struct.unpack_from("<i", raw, offset)[0]
    offset += 4
    sphere_slices = struct.unpack_from("<i", raw, offset)[0]

    return ExtendedColliderProps(
        convex=convex,
        is_trigger=is_trigger,
        material_file_id=material_file_id,
        material_path_id=material_path_id,
        material_name=material_name,
        collider_type=collider_type,
        centre=centre,
        rotation=rotation,
        size=size,
        flip_faces=flip_faces,
        circle_vertices=circle_vertices,
        circle_two_sided=circle_two_sided,
        cone_faces=cone_faces,
        cylinder_faces=cylinder_faces,
        cylinder_cap_top=cylinder_cap_top,
        cylinder_cap_bottom=cylinder_cap_bottom,
        cylinder_taper_top=cylinder_taper_top,
        cylinder_taper_bottom=cylinder_taper_bottom,
        sphere_stacks=sphere_stacks,
        sphere_slices=sphere_slices,
    )


def iter_game_objects(env: Any) -> Iterable[tuple[Any, Any]]:
    for reader in env.objects:
        if reader.type.name != "GameObject":
            continue
        try:
            yield reader, reader.read()
        except Exception:
            continue


def component_readers(game_object: Any) -> Iterable[Any]:
    for pair in game_object.m_Component:
        pointer = pair.component
        reader = pointer.assetsfile.objects.get(pointer.m_PathID)
        if reader is not None:
            yield reader


def _game_object_scripts(game_object: Any) -> list[str]:
    scripts: list[str] = []
    for component_reader in component_readers(game_object):
        if component_reader.type.name == "MonoBehaviour":
            script = _script_name(component_reader)
            scripts.append(script or "<unknown>")
    return scripts


def _printable_strings(raw: bytes) -> list[str]:
    return [match.decode("latin1") for match in re.findall(rb"[\x20-\x7e]{3,}", raw)]


def _button_click_summary(game_object: Any) -> str:
    for component_reader in component_readers(game_object):
        if component_reader.type.name != "MonoBehaviour" or _script_name(component_reader) != "Button":
            continue
        strings = _printable_strings(component_reader.get_raw_data())
        if "mLoadScence" in strings:
            index = strings.index("mLoadScence")
            args = [
                value
                for value in strings[index + 1 :]
                if value not in {"UnityEngine.Object, UnityEngine", "Normal", "Highlighted", "Pressed", "Selected", "Disabled"}
            ]
            if args:
                return f"onClick=mLoadScence({args[-1]!r})"
            return "onClick=mLoadScence(?)"
        if "set_enabled" in strings:
            return "onClick=set_enabled(...)"
    return ""


def _fmt_vec3(value: Any) -> str:
    return f"({value.x:g},{value.y:g},{value.z:g})"


def _fmt_quat(value: Any) -> str:
    return f"({value.x:g},{value.y:g},{value.z:g},{value.w:g})"


def _fmt_vec3_tuple(value: tuple[float, float, float]) -> str:
    return f"({value[0]:g},{value[1]:g},{value[2]:g})"


def _fmt_component_value(value: Any) -> str:
    if all(hasattr(value, attr) for attr in ("x", "y", "z")):
        return _fmt_vec3(value)
    return str(value)


def _matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [sum(left[row][k] * right[k][col] for k in range(4)) for col in range(4)]
        for row in range(4)
    ]


def _quat_to_mat3(rotation: Any) -> list[list[float]]:
    x, y, z, w = rotation.x, rotation.y, rotation.z, rotation.w
    norm = x * x + y * y + z * z + w * w
    if norm <= 1e-12:
        return [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    scale = 2.0 / norm
    xx, yy, zz = x * x * scale, y * y * scale, z * z * scale
    xy, xz, yz = x * y * scale, x * z * scale, y * z * scale
    wx, wy, wz = w * x * scale, w * y * scale, w * z * scale
    return [
        [1.0 - yy - zz, xy - wz, xz + wy],
        [xy + wz, 1.0 - xx - zz, yz - wx],
        [xz - wy, yz + wx, 1.0 - xx - yy],
    ]


def _local_transform_matrix(transform: Any) -> list[list[float]]:
    position = transform.m_LocalPosition
    scale = transform.m_LocalScale
    rotation = _quat_to_mat3(transform.m_LocalRotation)
    matrix = [[0.0, 0.0, 0.0, 0.0] for _ in range(4)]
    scales = (scale.x, scale.y, scale.z)
    for row in range(3):
        for col in range(3):
            matrix[row][col] = rotation[row][col] * scales[col]
    matrix[0][3] = position.x
    matrix[1][3] = position.y
    matrix[2][3] = position.z
    matrix[3][3] = 1.0
    return matrix


def _transform_key(pointer: Any) -> tuple[str, int] | None:
    path_id = getattr(pointer, "m_PathID", 0)
    assets_file = getattr(pointer, "assetsfile", None)
    if not path_id or assets_file is None:
        return None
    return (assets_file.name, path_id)


def _build_transform_world_matrices(env: Any) -> dict[tuple[str, int], list[list[float]]]:
    transforms: dict[tuple[str, int], tuple[Any, Any]] = {}
    for reader in env.objects:
        if reader.type.name != "Transform":
            continue
        try:
            transforms[(reader.assets_file.name, reader.path_id)] = (reader, reader.read())
        except Exception:
            continue

    cache: dict[tuple[str, int], list[list[float]]] = {}

    def world_matrix(key: tuple[str, int]) -> list[list[float]]:
        if key in cache:
            return cache[key]
        reader, transform = transforms[key]
        local = _local_transform_matrix(transform)
        parent_key = _transform_key(transform.m_Father)
        if parent_key in transforms:
            matrix = _matmul(world_matrix(parent_key), local)
        else:
            matrix = local
        cache[key] = matrix
        return matrix

    for key in transforms:
        world_matrix(key)
    return cache


def _build_game_object_paths(env: Any) -> dict[tuple[str, int], str]:
    transform_to_game_object: dict[tuple[str, int], tuple[str, bool]] = {}
    transform_parents: dict[tuple[str, int], tuple[str, int] | None] = {}

    for reader, game_object in iter_game_objects(env):
        transform_key = _transform_key(game_object.m_Transform)
        if transform_key is not None:
            transform_to_game_object[transform_key] = (game_object.m_Name, bool(game_object.m_IsActive))

    for reader in env.objects:
        if reader.type.name not in {"Transform", "RectTransform"}:
            continue
        try:
            transform = reader.read()
        except Exception:
            continue
        key = (reader.assets_file.name, reader.path_id)
        transform_parents[key] = _transform_key(transform.m_Father)

    cache: dict[tuple[str, int], str] = {}

    def object_path(transform_key: tuple[str, int]) -> str:
        if transform_key in cache:
            return cache[transform_key]
        name = transform_to_game_object.get(transform_key, ("<unnamed>", True))[0]
        parent_key = transform_parents.get(transform_key)
        if parent_key in transform_to_game_object:
            path = f"{object_path(parent_key)}/{name}"
        else:
            path = name
        cache[transform_key] = path
        return path

    paths: dict[tuple[str, int], str] = {}
    for reader, game_object in iter_game_objects(env):
        transform_key = _transform_key(game_object.m_Transform)
        if transform_key is None:
            continue
        paths[(reader.assets_file.name, reader.path_id)] = object_path(transform_key)
    return paths


def _parse_build_scenes(reader: Any) -> list[str]:
    raw = reader.get_raw_data()
    if len(raw) < 4:
        return []
    count = struct.unpack_from("<i", raw, 0)[0]
    offset = 4
    scenes: list[str] = []
    for _ in range(count):
        scene, offset = _read_aligned_string(raw, offset)
        scenes.append(scene)
    return scenes


def print_build_settings(env: Any) -> None:
    for reader in env.objects:
        if reader.type.name != "BuildSettings":
            continue
        print("Build scenes:")
        try:
            scenes = _parse_build_scenes(reader)
        except Exception as exc:
            print(f"  <unreadable: {type(exc).__name__}: {exc}>")
            return
        for index, scene in enumerate(scenes):
            print(f"  {index}: {scene} ({PurePosixPath(scene).stem})")
        if not any(PurePosixPath(scene).stem == "AutoGame" for scene in scenes):
            print("  AutoGame: not present in BuildSettings")
        if not any(PurePosixPath(scene).stem == "FastGame" for scene in scenes):
            print("  FastGame: not present in BuildSettings")
        return
    print("Build scenes: <BuildSettings not found>")


def print_controller_inventory(env: Any) -> None:
    paths = _build_game_object_paths(env)
    script_counts: dict[str, Counter[str]] = defaultdict(Counter)
    inventory: list[tuple[str, int, str, bool, list[str]]] = []

    for reader, game_object in iter_game_objects(env):
        scripts = _game_object_scripts(game_object)
        asset_name = reader.assets_file.name
        for script in scripts:
            if script in INTERESTING_SCENE_SCRIPTS:
                script_counts[asset_name][script] += 1

        if (
            game_object.m_Name in INTERESTING_SCENE_OBJECTS
            or any(script in INTERESTING_SCENE_SCRIPTS for script in scripts)
        ):
            path = paths.get((asset_name, reader.path_id), game_object.m_Name)
            inventory.append((asset_name, reader.path_id, path, bool(game_object.m_IsActive), scripts))

    print("Interesting script counts:")
    for asset_name in sorted(script_counts):
        pairs = ", ".join(f"{name}={count}" for name, count in sorted(script_counts[asset_name].items()))
        print(f"  {asset_name}: {pairs}")

    print("Controller/UI inventory:")
    for asset_name, path_id, path, active, scripts in sorted(inventory):
        click_summary = ""
        reader = next(
            (
                candidate
                for candidate in env.objects
                if candidate.assets_file.name == asset_name
                and candidate.path_id == path_id
                and candidate.type.name == "GameObject"
            ),
            None,
        )
        if reader is not None:
            try:
                click_summary = _button_click_summary(reader.read())
            except Exception:
                click_summary = ""
        suffix = f" {click_summary}" if click_summary else ""
        print(f"  {asset_name}:{path_id} {path} active={active} scripts={scripts}{suffix}")


def _matrix_position(matrix: list[list[float]]) -> tuple[float, float, float]:
    return (matrix[0][3], matrix[1][3], matrix[2][3])


def _matrix_axis_lengths(matrix: list[list[float]]) -> tuple[float, float, float]:
    lengths = []
    for col in range(3):
        lengths.append(sum(matrix[row][col] * matrix[row][col] for row in range(3)) ** 0.5)
    return (lengths[0], lengths[1], lengths[2])


def print_global_settings(env: Any) -> None:
    for reader in env.objects:
        if reader.type.name == "TagManager":
            tag_manager = reader.read()
            print("Tags:", ", ".join(tag_manager.tags))
            print("Layers:", ", ".join(layer or "<empty>" for layer in tag_manager.layers))
        elif reader.type.name == "TimeManager":
            time_manager = reader.read()
            print("Time:")
            for field in (
                "Fixed_Timestep",
                "Maximum_Allowed_Timestep",
                "Maximum_Particle_Timestep",
                "m_TimeScale",
            ):
                print(f"  {field}: {getattr(time_manager, field, None)}")
        elif reader.type.name == "PhysicsManager":
            physics = reader.read()
            print("Physics:")
            for field in (
                "m_Gravity",
                "m_BounceThreshold",
                "m_DefaultContactOffset",
                "m_DefaultSolverIterations",
                "m_DefaultSolverVelocityIterations",
                "m_SleepThreshold",
                "m_DefaultMaxAngularSpeed",
                "m_DefaultMaxDepenetrationVelocity",
                "m_FrictionType",
                "m_SolverType",
                "m_BroadphaseType",
                "m_ContactsGeneration",
                "m_ContactPairsMode",
                "m_AutoSyncTransforms",
                "m_SimulationMode",
                "m_EnableAdaptiveForce",
                "m_EnableEnhancedDeterminism",
                "m_ImprovedPatchFriction",
                "m_EnableUnifiedHeightmaps",
                "m_QueriesHitBackfaces",
                "m_QueriesHitTriggers",
                "m_FastMotionThreshold",
                "m_WorldSubdivisions",
                "m_InvokeCollisionCallbacks",
                "m_ReuseCollisionCallbacks",
            ):
                print(f"  {field}: {getattr(physics, field, None)}")
            default_material = getattr(physics, "m_DefaultMaterial", None)
            if default_material is not None:
                material_reader = default_material.assetsfile.objects.get(default_material.m_PathID)
                print(f"  m_DefaultMaterial: {_safe_name(material_reader) if material_reader else None}")
        elif reader.type.name == "PhysicMaterial":
            material = reader.read()
            print(
                "PhysicMaterial:",
                material.m_Name,
                f"dynamic={material.dynamicFriction:g}",
                f"static={material.staticFriction:g}",
                f"bounciness={material.bounciness:g}",
                f"frictionCombine={material.frictionCombine}",
                f"bounceCombine={material.bounceCombine}",
            )


def print_stones(env: Any, world_matrices: dict[tuple[str, int], list[list[float]]]) -> None:
    tag_names: dict[int, str] = {}
    for reader in env.objects:
        if reader.type.name == "TagManager":
            tags = reader.read().tags
            tag_names = {CUSTOM_TAG_BASE + index: tag for index, tag in enumerate(tags)}
            break

    seen_shapes: set[tuple[Any, ...]] = set()
    for reader, game_object in iter_game_objects(env):
        if game_object.m_Tag != CUSTOM_TAG_BASE + 2:
            continue
        if not game_object.m_Name.startswith("Curling stone"):
            continue

        transform = game_object.m_Transform.read()
        scale = transform.m_LocalScale
        transform_key = _transform_key(game_object.m_Transform)
        world_matrix = world_matrices.get(transform_key) if transform_key else None
        world_info = ""
        if world_matrix is not None:
            world_info = (
                f"worldPos={_fmt_vec3_tuple(_matrix_position(world_matrix))} "
                f"worldScale={_fmt_vec3_tuple(_matrix_axis_lengths(world_matrix))} "
            )
        body_info = ""
        props_info = ""
        scripts: list[str] = []
        for component_reader in component_readers(game_object):
            type_name = component_reader.type.name
            if type_name == "Rigidbody":
                body = component_reader.read()
                body_info = (
                    f"mass={body.m_Mass:g} drag={body.m_Drag:g} "
                    f"angularDrag={body.m_AngularDrag:g} useGravity={body.m_UseGravity} "
                    f"isKinematic={body.m_IsKinematic} collisionDetection={body.m_CollisionDetection} "
                    f"constraints={getattr(body, 'm_Constraints', None)} "
                    f"implicitCom={getattr(body, 'm_ImplicitCom', None)} "
                    f"implicitTensor={getattr(body, 'm_ImplicitTensor', None)} "
                    f"centerOfMass={_fmt_component_value(getattr(body, 'm_CenterOfMass', 'None'))} "
                    f"inertiaTensor={_fmt_component_value(getattr(body, 'm_InertiaTensor', 'None'))} "
                    f"inertiaRotation={_fmt_component_value(getattr(body, 'm_InertiaRotation', 'None'))}"
                )
            elif type_name == "MonoBehaviour":
                script = _script_name(component_reader)
                scripts.append(script or "<unknown>")
                if script == "ExtendedColliders3D":
                    props = parse_extended_collider_props(component_reader)
                    local_radius = props.size[0] * scale.x / 2.0
                    local_height = props.size[1] * scale.y
                    world_radius = local_radius
                    world_height = local_height
                    if world_matrix is not None:
                        world_scale = _matrix_axis_lengths(world_matrix)
                        world_radius = max(
                            props.size[0] * world_scale[0] / 2.0,
                            props.size[2] * world_scale[2] / 2.0,
                        )
                        world_height = props.size[1] * world_scale[1]
                    shape_key = (
                        props.convex,
                        props.is_trigger,
                        props.material_name,
                        props.collider_type,
                        props.size,
                        props.cylinder_faces,
                        props.cylinder_cap_top,
                        props.cylinder_cap_bottom,
                        round(local_radius, 8),
                        round(local_height, 8),
                        round(world_radius, 8),
                        round(world_height, 8),
                    )
                    props_info = (
                        f"ExtendedColliders3D(type={props.collider_type}, convex={props.convex}, "
                        f"isTrigger={props.is_trigger}, material={props.material_name}, "
                        f"size={tuple(round(v, 6) for v in props.size)}, "
                        f"cylinderFaces={props.cylinder_faces}, caps=({props.cylinder_cap_top},"
                        f"{props.cylinder_cap_bottom}), taperTop={props.cylinder_taper_top}, "
                        f"taperBottom={props.cylinder_taper_bottom}, flipFaces={props.flip_faces}, "
                        f"localRadius={local_radius:.6f}, localHeight={local_height:.6f}, "
                        f"worldRadius={world_radius:.6f}, worldHeight={world_height:.6f})"
                    )
                    seen_shapes.add(shape_key)

        print(
            f"{reader.assets_file.name}:{reader.path_id} {game_object.m_Name} "
            f"tag={tag_names.get(game_object.m_Tag, game_object.m_Tag)} active={game_object.m_IsActive} "
            f"localPos={_fmt_vec3(transform.m_LocalPosition)} "
            f"localRot={_fmt_quat(transform.m_LocalRotation)} "
            f"scale=({scale.x:g},{scale.y:g},{scale.z:g}) {world_info}scripts={scripts} "
            f"{body_info} {props_info}"
        )

    print("Unique stone collider shapes:")
    for shape in sorted(seen_shapes, key=str):
        print(f"  {shape}")


def print_named_scene_objects(env: Any, world_matrices: dict[tuple[str, int], list[list[float]]]) -> None:
    interesting_names = {
        "Midline",
        "Hogline1",
        "Hogline2",
        "CameraMid",
        "CameraHouse",
        "CameraControl",
        "Broom",
        "Plane",
        "Terminal",
    }
    interesting_prefixes = ("bound", "tee", "Tee")

    print("Named scene objects:")
    for reader, game_object in iter_game_objects(env):
        name = game_object.m_Name
        if name not in interesting_names and not name.startswith(interesting_prefixes):
            continue

        transform = game_object.m_Transform.read()
        transform_key = _transform_key(game_object.m_Transform)
        world_matrix = world_matrices.get(transform_key) if transform_key else None
        world_pos = _matrix_position(world_matrix) if world_matrix is not None else None
        world_scale = _matrix_axis_lengths(world_matrix) if world_matrix is not None else None
        component_infos: list[str] = []
        scripts: list[str] = []
        for component_reader in component_readers(game_object):
            type_name = component_reader.type.name
            if type_name == "MonoBehaviour":
                script = _script_name(component_reader)
                if script:
                    scripts.append(script)
                continue
            if not type_name.endswith("Collider"):
                continue
            try:
                component = component_reader.read()
            except Exception:
                component_infos.append(f"{type_name}(unreadable)")
                continue

            fields: list[str] = []
            for field in (
                "m_Enabled",
                "m_IsTrigger",
                "m_Convex",
                "m_CookingOptions",
                "m_Center",
                "m_Size",
                "m_Radius",
                "m_Height",
                "m_Direction",
            ):
                if hasattr(component, field):
                    fields.append(f"{field}={_fmt_component_value(getattr(component, field))}")
            if hasattr(component, "m_Material"):
                material = component.m_Material
                material_name = _resolve_external_name(
                    component_reader.assets_file,
                    getattr(material, "m_FileID", 0),
                    getattr(material, "m_PathID", 0),
                )
                fields.append(f"m_Material={material_name or _describe_pptr(component_reader.assets_file, material)}")
            if hasattr(component, "m_Mesh"):
                fields.append(f"m_Mesh={_describe_pptr(component_reader.assets_file, component.m_Mesh)}")
            component_infos.append(f"{type_name}({', '.join(fields)})")

        print(
            f"  {reader.assets_file.name}:{reader.path_id} {name} "
            f"active={game_object.m_IsActive} layer={game_object.m_Layer} tag={game_object.m_Tag} "
            f"pos={_fmt_vec3(transform.m_LocalPosition)} "
            f"rot={_fmt_vec3(transform.m_LocalRotation)} "
            f"scale={_fmt_vec3(transform.m_LocalScale)} "
            f"worldPos={_fmt_vec3_tuple(world_pos) if world_pos else None} "
            f"worldScale={_fmt_vec3_tuple(world_scale) if world_scale else None} "
            f"scripts={scripts} components={component_infos}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data_unity3d",
        nargs="?",
        default=os.path.join(os.environ.get("TEMP", "."), "curling_reverse_il2cpp", "data.unity3d"),
    )
    args = parser.parse_args()
    env = UnityPy.load(args.data_unity3d)
    world_matrices = _build_transform_world_matrices(env)
    print_build_settings(env)
    print_controller_inventory(env)
    print_global_settings(env)
    print_named_scene_objects(env, world_matrices)
    print_stones(env, world_matrices)


if __name__ == "__main__":
    main()
