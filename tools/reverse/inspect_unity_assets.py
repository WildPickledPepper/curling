"""Inspect Unity assets relevant to the curling physics reverse pass.

This script focuses on data that UnityPy can recover reliably from the
WebGL data bundle: tags, global physics settings, stone rigidbodies, and the
runtime-generated ExtendedColliders3D mesh-collider setup.
"""

from __future__ import annotations

import argparse
import os
import struct
from dataclasses import dataclass
from typing import Any, Iterable

import UnityPy


CUSTOM_TAG_BASE = 20000


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


def _fmt_vec3(value: Any) -> str:
    return f"({value.x:g},{value.y:g},{value.z:g})"


def _fmt_component_value(value: Any) -> str:
    if all(hasattr(value, attr) for attr in ("x", "y", "z")):
        return _fmt_vec3(value)
    return str(value)


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


def print_stones(env: Any) -> None:
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
                    f"isKinematic={body.m_IsKinematic} collisionDetection={body.m_CollisionDetection}"
                )
            elif type_name == "MonoBehaviour":
                script = _script_name(component_reader)
                scripts.append(script or "<unknown>")
                if script == "ExtendedColliders3D":
                    props = parse_extended_collider_props(component_reader)
                    world_radius = props.size[0] * scale.x / 2.0
                    world_height = props.size[1] * scale.y
                    shape_key = (
                        props.convex,
                        props.is_trigger,
                        props.material_name,
                        props.collider_type,
                        props.size,
                        props.cylinder_faces,
                        props.cylinder_cap_top,
                        props.cylinder_cap_bottom,
                        round(world_radius, 8),
                        round(world_height, 8),
                    )
                    props_info = (
                        f"ExtendedColliders3D(type={props.collider_type}, convex={props.convex}, "
                        f"isTrigger={props.is_trigger}, material={props.material_name}, "
                        f"size={tuple(round(v, 6) for v in props.size)}, "
                        f"cylinderFaces={props.cylinder_faces}, caps=({props.cylinder_cap_top},"
                        f"{props.cylinder_cap_bottom}), worldRadius={world_radius:.6f}, "
                        f"worldHeight={world_height:.6f})"
                    )
                    seen_shapes.add(shape_key)

        print(
            f"{reader.assets_file.name}:{reader.path_id} {game_object.m_Name} "
            f"tag={tag_names.get(game_object.m_Tag, game_object.m_Tag)} active={game_object.m_IsActive} "
            f"scale=({scale.x:g},{scale.y:g},{scale.z:g}) scripts={scripts} {body_info} {props_info}"
        )

    print("Unique stone collider shapes:")
    for shape in sorted(seen_shapes, key=str):
        print(f"  {shape}")


def print_named_scene_objects(env: Any) -> None:
    interesting_names = {
        "Midline",
        "Hogline1",
        "Hogline2",
        "CameraMid",
        "CameraControl",
        "Broom",
        "Plane",
    }
    interesting_prefixes = ("bound", "tee", "Tee")

    print("Named scene objects:")
    for reader, game_object in iter_game_objects(env):
        name = game_object.m_Name
        if name not in interesting_names and not name.startswith(interesting_prefixes):
            continue

        transform = game_object.m_Transform.read()
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
                "m_Center",
                "m_Size",
                "m_Radius",
                "m_Height",
                "m_Direction",
            ):
                if hasattr(component, field):
                    fields.append(f"{field}={_fmt_component_value(getattr(component, field))}")
            component_infos.append(f"{type_name}({', '.join(fields)})")

        print(
            f"  {reader.assets_file.name}:{reader.path_id} {name} "
            f"active={game_object.m_IsActive} layer={game_object.m_Layer} tag={game_object.m_Tag} "
            f"pos={_fmt_vec3(transform.m_LocalPosition)} "
            f"rot={_fmt_vec3(transform.m_LocalRotation)} "
            f"scale={_fmt_vec3(transform.m_LocalScale)} "
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
    print_global_settings(env)
    print_named_scene_objects(env)
    print_stones(env)


if __name__ == "__main__":
    main()
