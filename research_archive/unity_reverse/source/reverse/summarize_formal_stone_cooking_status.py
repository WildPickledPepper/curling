#!/usr/bin/env python3
"""Summarize the offline status of formal curling-stone convex cooking."""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MESH = Path(r"D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json")
DEFAULT_WAITING_HULL_IDENTITY = (
    PROJECT_ROOT / "data" / "calibration" / "unity_cooked_hull_identity_20260708_225950.json"
)
DEFAULT_PYPHYSX_CONTROL = (
    PROJECT_ROOT / "data" / "calibration" / "pyphysx_cooked_stone_hull_probe_binding_default_refresh_20260708.json"
)
DEFAULT_PYPHYSX_UNITY_FLAGS = (
    PROJECT_ROOT / "data" / "calibration" / "pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_20260708.json"
)
DEFAULT_PYPHYSX_UNITY_FLAGS_RAW = (
    PROJECT_ROOT / "data" / "calibration" / "pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json"
)
DEFAULT_PYPHYSX_TOPOLOGY = PROJECT_ROOT / "data" / "calibration" / "pyphysx_raw_hull_topology_20260708.json"
DEFAULT_PYPHYSX_BIGCONVEX = PROJECT_ROOT / "data" / "calibration" / "pyphysx_bigconvex_data_20260709.json"
DEFAULT_PYPHYSX_SCALED_MASS = (
    PROJECT_ROOT / "data" / "calibration" / "pyphysx_scaled_mass_properties_20260709.json"
)
DEFAULT_COLLISION_UNITY_FLAGS_CURRENT_BEST = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_current_best_rebuilt_unityflags_20260708.json"
)
DEFAULT_COLLISION_FORMAL_GEOMETRY = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_formal_geometry_rebuilt_unityflags_handoff292_20260708.json"
)
DEFAULT_COLLISION_FORMAL_GEOMETRY_COOKED_INERTIA = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_formal_geometry_cooked_inertia_20260709.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "formal_stone_cooking_status_20260708.json"

WORLD_SCALE = (0.112700008, 0.115, 0.112700008)
UNITY_VERTEX_LIMIT = 255


def _load_mesh(path: Path) -> tuple[list[tuple[float, float, float]], list[int]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    vertices = [tuple(float(coord) for coord in vertex) for vertex in data["vertices"]]
    triangles = [int(index) for index in data["triangles"]]
    return vertices, triangles


def _bounds(vertices: list[tuple[float, float, float]]) -> dict[str, list[float]]:
    mins = [min(vertex[i] for vertex in vertices) for i in range(3)]
    maxs = [max(vertex[i] for vertex in vertices) for i in range(3)]
    extents = [maxs[i] - mins[i] for i in range(3)]
    return {"min": mins, "max": maxs, "extents": extents, "sorted_extents": sorted(extents)}


def _scale_vertices(
    vertices: list[tuple[float, float, float]], scale: tuple[float, float, float]
) -> list[tuple[float, float, float]]:
    return [tuple(vertex[i] * scale[i] for i in range(3)) for vertex in vertices]


def _unique_vertices(
    vertices: list[tuple[float, float, float]], ndigits: int = 10
) -> list[tuple[float, float, float]]:
    seen: dict[tuple[float, float, float], tuple[float, float, float]] = {}
    for vertex in vertices:
        key = tuple(round(value, ndigits) for value in vertex)
        seen.setdefault(key, vertex)
    return list(seen.values())


def _support_extreme_count(vertices: list[tuple[float, float, float]]) -> int:
    extreme = 0
    eps_y = 1e-3
    tolerance = 1e-9
    for vx, vy, vz in vertices:
        radius = math.hypot(vx, vz)
        if radius == 0.0:
            continue
        dx = vx / radius
        dy = eps_y if vy >= 0.0 else -eps_y
        dz = vz / radius
        scores = [x * dx + y * dy + z * dz for x, y, z in vertices]
        best = max(scores)
        winners = sum(1 for score in scores if abs(score - best) <= tolerance)
        score = vx * dx + vy * dy + vz * dz
        if winners == 1 and abs(score - best) <= tolerance:
            extreme += 1
    return extreme


def _read_json_if_exists(path: Path) -> Any | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _pyphysx_detail(path: Path) -> dict[str, Any] | None:
    report = _read_json_if_exists(path)
    if not report:
        return None
    detail = report.get("detail") or report.get("detailed_variant")
    if not isinstance(detail, dict):
        return None
    result = {
        "path": str(path),
        "detailed_variant": report.get("detailed_variant"),
        "binding_note": report.get("binding_note"),
        "unique_vertex_count": detail.get("unique_vertex_count"),
        "triangle_count": detail.get("triangle_count"),
        "quantize_input": detail.get("quantize_input"),
        "gpu_compatible": detail.get("gpu_compatible"),
        "binding_flag_support": detail.get("binding_flag_support"),
        "local_bounds": detail.get("local_bounds"),
        "world_bounds": detail.get("world_bounds"),
        "world_radial_stats_xz": detail.get("world_radial_stats_xz"),
    }
    raw = detail.get("raw_convex_mesh_data")
    if isinstance(raw, dict):
        polygon_histogram: dict[str, int] = {}
        for polygon in raw.get("polygons") or []:
            key = str(polygon.get("nb_vertices"))
            polygon_histogram[key] = polygon_histogram.get(key, 0) + 1
        vertices = raw.get("vertices") or []
        top_vertices = [vertex for vertex in vertices if len(vertex) >= 3 and vertex[1] > 0.0]
        bottom_vertices = [vertex for vertex in vertices if len(vertex) >= 3 and vertex[1] < 0.0]
        radial_values = [math.hypot(vertex[0], vertex[2]) for vertex in vertices if len(vertex) >= 3]
        angle_steps_degrees: list[float] = []
        if len(top_vertices) > 1:
            angles = sorted(math.atan2(vertex[2], vertex[0]) for vertex in top_vertices)
            for index, angle in enumerate(angles):
                next_angle = angles[0] + 2.0 * math.pi if index == len(angles) - 1 else angles[index + 1]
                angle_steps_degrees.append((next_angle - angle) * 180.0 / math.pi)
        result["raw_convex_mesh_data"] = {
            "nb_vertices": raw.get("nb_vertices"),
            "nb_polygons": raw.get("nb_polygons"),
            "index_count": raw.get("index_count"),
            "polygon_vertex_count_histogram": polygon_histogram,
            "top_vertex_count": len(top_vertices),
            "bottom_vertex_count": len(bottom_vertices),
            "local_radial_min": min(radial_values) if radial_values else None,
            "local_radial_max": max(radial_values) if radial_values else None,
            "top_angle_step_degrees_min": min(angle_steps_degrees) if angle_steps_degrees else None,
            "top_angle_step_degrees_max": max(angle_steps_degrees) if angle_steps_degrees else None,
            "scale": raw.get("scale"),
            "scale_rotation_xyzw": raw.get("scale_rotation_xyzw"),
            "scale_is_identity": raw.get("scale_is_identity"),
            "is_gpu_compatible": raw.get("is_gpu_compatible"),
            "local_bounds": raw.get("local_bounds"),
            "mass_information": raw.get("mass_information"),
        }
    return result


def _collision_summary(path: Path) -> dict[str, Any] | None:
    report = _read_json_if_exists(path)
    if not report:
        return None
    result_sets = report.get("result_sets") or []
    if not result_sets:
        return None
    first = result_sets[0]
    config = first.get("config", {})
    summary = first.get("summary", {})
    return {
        "path": str(path),
        "radius": config.get("radius"),
        "center_height": config.get("center_height"),
        "handoff_extra": config.get("handoff_extra"),
        "quantize_input": config.get("quantize_input"),
        "gpu_compatible": config.get("gpu_compatible"),
        "active_rmse_m": summary.get("active_rmse_m"),
        "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
        "combined_rmse_m": summary.get("combined_rmse_m"),
    }


def _topology_summary(path: Path) -> dict[str, Any] | None:
    report = _read_json_if_exists(path)
    if not report:
        return None
    counts = report.get("counts", {})
    geometry = report.get("geometry_summary", {})
    topology = report.get("contact_relevant_topology", {})
    return {
        "path": str(path),
        "nb_vertices": counts.get("nb_vertices"),
        "nb_polygons": counts.get("nb_polygons"),
        "nb_edges": counts.get("nb_edges"),
        "euler_characteristic": counts.get("euler_characteristic"),
        "polygon_class_counts": counts.get("polygon_class_counts"),
        "edge_type_counts": counts.get("edge_type_counts"),
        "vertex_face_valency_histogram": counts.get("vertex_face_valency_histogram"),
        "faces_by_edges8_complete": topology.get("faces_by_edges8_complete"),
        "faces_by_vertices8_complete": topology.get("faces_by_vertices8_complete"),
        "unique_edge_direction_class_count": topology.get("unique_edge_direction_class_count"),
        "world_radius_minus_apothem_m": geometry.get("world_radius_minus_apothem_m"),
        "runtime_extra_buffer_bytes": (report.get("runtime_buffer_layout_bytes") or {}).get(
            "total_runtime_extra_buffer"
        ),
        "clhl_payload_bytes": (report.get("clhl_payload_layout_bytes_excluding_chunk_header") or {}).get("total"),
        "conclusion": report.get("conclusion"),
    }


def _bigconvex_summary(path: Path) -> dict[str, Any] | None:
    report = _read_json_if_exists(path)
    if not report:
        return None
    trigger = report.get("trigger", {})
    vale = report.get("vale", {})
    gaus = report.get("gaus", {})
    payload = report.get("stream_payload_bytes_excluding_chunk_headers", {})
    checks = report.get("consistency_checks", {})
    return {
        "path": str(path),
        "big_convex_data_required": trigger.get("big_convex_data_required"),
        "gauss_map_vertex_limit": trigger.get("gauss_map_vertex_limit"),
        "density_subdiv": trigger.get("density_subdiv"),
        "vale_nb_verts": vale.get("nb_verts"),
        "vale_nb_adjacent_verts": vale.get("nb_adjacent_verts"),
        "vale_max_valency_count": vale.get("max_valency_count"),
        "vale_valency_count_histogram": vale.get("valency_count_histogram"),
        "gaus_nb_samples": gaus.get("nb_samples"),
        "gaus_samples_byte_count": gaus.get("samples_byte_count"),
        "gaus_unique_all_sample_vertices": gaus.get("unique_all_sample_vertices"),
        "gaus_bruteforce_validation_error_count": gaus.get("bruteforce_validation_error_count"),
        "payload_bytes_excluding_chunk_headers": payload,
        "consistency_checks": checks,
        "conclusion": report.get("conclusion"),
    }


def _scaled_mass_summary(path: Path) -> dict[str, Any] | None:
    report = _read_json_if_exists(path)
    if not report:
        return None
    candidates = report.get("candidates") or []
    recommended = report.get("recommended_for_collision_probe") or {}
    candidate_name = recommended.get("candidate")
    selected = None
    for candidate in candidates:
        if candidate.get("name") == candidate_name:
            selected = candidate
            break
    selected = selected or (candidates[-1] if candidates else {})
    args = selected.get("probe_z_up_custom_args") or {}
    return {
        "path": str(path),
        "rigidbody_mass": report.get("rigidbody_mass"),
        "candidate": selected.get("name"),
        "scale": selected.get("scale"),
        "scaled_bounds": selected.get("scaled_bounds"),
        "unit_density_scaled_mass": selected.get("unit_density_scaled_mass"),
        "density_scale_to_rigidbody_mass_19p1": selected.get(
            "density_scale_to_rigidbody_mass_19p1"
        ),
        "rigidbody_mass_scaled_inertia_diag_xyz": selected.get(
            "rigidbody_mass_scaled_inertia_diag_xyz"
        ),
        "probe_z_up_custom_args": args,
        "comparison": selected.get("comparison"),
        "command_fragment": recommended.get("command_fragment"),
        "conclusion": report.get("conclusion"),
    }


def summarize(
    mesh_path: Path,
    waiting_identity_path: Path,
    pyphysx_control_path: Path,
    pyphysx_unity_flags_path: Path,
    pyphysx_unity_flags_raw_path: Path,
    pyphysx_topology_path: Path,
    pyphysx_bigconvex_path: Path,
    pyphysx_scaled_mass_path: Path,
    collision_current_best_path: Path,
    collision_formal_geometry_path: Path,
    collision_formal_cooked_inertia_path: Path,
) -> dict[str, Any]:
    vertices, triangles = _load_mesh(mesh_path)
    unique = _unique_vertices(vertices)
    world_vertices = _scale_vertices(unique, WORLD_SCALE)
    local_bounds = _bounds(unique)
    world_bounds = _bounds(world_vertices)
    support_extreme_count = _support_extreme_count(unique)

    waiting_identity = _read_json_if_exists(waiting_identity_path)
    pyphysx_control_detail = _pyphysx_detail(pyphysx_control_path)
    pyphysx_unity_flags_detail = _pyphysx_detail(pyphysx_unity_flags_path)
    pyphysx_unity_flags_raw_detail = _pyphysx_detail(pyphysx_unity_flags_raw_path)
    pyphysx_topology = _topology_summary(pyphysx_topology_path)
    pyphysx_bigconvex = _bigconvex_summary(pyphysx_bigconvex_path)
    pyphysx_scaled_mass = _scaled_mass_summary(pyphysx_scaled_mass_path)
    collision_current_best = _collision_summary(collision_current_best_path)
    collision_formal_geometry = _collision_summary(collision_formal_geometry_path)
    collision_formal_cooked_inertia = _collision_summary(collision_formal_cooked_inertia_path)

    forced_crop = support_extreme_count > UNITY_VERTEX_LIMIT
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "formal_stone_mesh": {
            "path": str(mesh_path),
            "raw_vertices": len(vertices),
            "unique_vertices": len(unique),
            "indices": len(triangles),
            "triangles": len(triangles) // 3,
            "local_bounds": local_bounds,
            "world_scale": list(WORLD_SCALE),
            "world_bounds": world_bounds,
            "support_extreme_vertices": support_extreme_count,
        },
        "unity_recovered_convex_desc": {
            "flags": ["eCOMPUTE_CONVEX"],
            "quantize_input": False,
            "gpu_compatible": False,
            "plane_shifting": False,
            "vertex_limit": UNITY_VERTEX_LIMIT,
            "quantized_count": 255,
            "build_gpu_data": False,
            "expected_physx_path": "createConvexHull -> expandHullOBB -> mCropedConvexHull -> fillConvexMeshDescFromCroppedHull",
            "forced_crop_by_vertex_count": forced_crop,
            "reason": (
                f"{support_extreme_count} support-extreme vertices exceed vertexLimit={UNITY_VERTEX_LIMIT}"
                if forced_crop
                else "support-extreme vertex count does not exceed vertexLimit"
            ),
        },
        "waiting_page_hull_identity": {
            "path": str(waiting_identity_path),
            "any_extent_match_5pct": waiting_identity.get("any_extent_match_5pct") if waiting_identity else None,
            "best_candidate": waiting_identity.get("best_candidate") if waiting_identity else None,
            "conclusion": waiting_identity.get("conclusion") if waiting_identity else "missing",
        },
        "pyphysx_control": {
            "path": str(pyphysx_control_path),
            "detail": pyphysx_control_detail,
            "role": "binding-default qi1/gpu1 control; not Unity flags",
        },
        "pyphysx_unity_flags_rebuilt": {
            "path": str(pyphysx_unity_flags_path),
            "detail": pyphysx_unity_flags_detail,
            "role": "rebuilt binding, Unity recovered qi0/gpu0 flags",
        },
        "pyphysx_unity_flags_rebuilt_raw": {
            "path": str(pyphysx_unity_flags_raw_path),
            "detail": pyphysx_unity_flags_raw_detail,
            "role": "rebuilt binding with PxConvexMesh raw vertices/polygons/index buffer/mass information",
        },
        "pyphysx_raw_hull_topology": {
            "path": str(pyphysx_topology_path),
            "detail": pyphysx_topology,
            "role": "contact-relevant topology reconstructed from raw PxConvexMesh data",
        },
        "pyphysx_bigconvex_data": {
            "path": str(pyphysx_bigconvex_path),
            "detail": pyphysx_bigconvex,
            "role": "offline reconstruction of PhysX BigConvexData VALE/GAUS support data",
        },
        "pyphysx_scaled_mass_properties": {
            "path": str(pyphysx_scaled_mass_path),
            "detail": pyphysx_scaled_mass,
            "role": "PhysX scaleInertia mass-property reconstruction for Unity-scale cooked hull",
        },
        "collision_probe_checks": {
            "current_best_geometry_with_unity_flags": collision_current_best,
            "formal_geometry_with_unity_flags": collision_formal_geometry,
            "formal_geometry_with_cooked_hull_inertia": collision_formal_cooked_inertia,
        },
        "current_blocker": (
            "The C++ toolchain and rebuilt pyphysx binding now run Unity's recovered "
            "quantize_input=false/gpu_compatible=false convex cooking path. The offline "
            "pyphysx dump for the formal source mesh is 128 vertices / 66 convex polygons / "
            "384 polygon indices / 252 rendered triangles under the recovered Unity flags; "
            "the raw polygon histogram is 2 caps with 64 vertices plus 64 side quads. "
            "The reconstructed contact topology has 192 unique edges, complete "
            "facesByEdges8/facesByVertices8, and BigConvexData VALE/GAUS contents that pass "
            "brute-force support validation. The world-scale cooked-hull mass properties now give "
            "probe custom inertia radial=0.178810612362 and vertical=0.189222883199 kg*m^2 "
            "from PhysX scaleInertia rather than fitting. A targeted replay with that inertia still gives "
            "unique-role target RMSE about 12.65cm, so the inertia formula alone is not the missing piece. "
            "However, plugging formal radius 0.140875m into the existing collision probe still worsens "
            "unique-role target RMSE to the 12cm class, while the older 0.146m compensated geometry stays "
            "near 11cm. The remaining blocker is no longer the binding; it is the exact Unity runtime "
            "shape scale/local pose/contact handoff and whether Unity's formal-stone runtime cooked stream "
            "is byte-level identical to this offline PhysX 4.1 reconstruction."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh", type=Path, default=DEFAULT_MESH)
    parser.add_argument("--waiting-identity", type=Path, default=DEFAULT_WAITING_HULL_IDENTITY)
    parser.add_argument("--pyphysx-control", type=Path, default=DEFAULT_PYPHYSX_CONTROL)
    parser.add_argument("--pyphysx-unity-flags", type=Path, default=DEFAULT_PYPHYSX_UNITY_FLAGS)
    parser.add_argument("--pyphysx-unity-flags-raw", type=Path, default=DEFAULT_PYPHYSX_UNITY_FLAGS_RAW)
    parser.add_argument("--pyphysx-topology", type=Path, default=DEFAULT_PYPHYSX_TOPOLOGY)
    parser.add_argument("--pyphysx-bigconvex", type=Path, default=DEFAULT_PYPHYSX_BIGCONVEX)
    parser.add_argument("--pyphysx-scaled-mass", type=Path, default=DEFAULT_PYPHYSX_SCALED_MASS)
    parser.add_argument(
        "--collision-current-best",
        type=Path,
        default=DEFAULT_COLLISION_UNITY_FLAGS_CURRENT_BEST,
    )
    parser.add_argument("--collision-formal", type=Path, default=DEFAULT_COLLISION_FORMAL_GEOMETRY)
    parser.add_argument(
        "--collision-formal-cooked-inertia",
        type=Path,
        default=DEFAULT_COLLISION_FORMAL_GEOMETRY_COOKED_INERTIA,
    )
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = summarize(
        args.mesh,
        args.waiting_identity,
        args.pyphysx_control,
        args.pyphysx_unity_flags,
        args.pyphysx_unity_flags_raw,
        args.pyphysx_topology,
        args.pyphysx_bigconvex,
        args.pyphysx_scaled_mass,
        args.collision_current_best,
        args.collision_formal,
        args.collision_formal_cooked_inertia,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    mesh = result["formal_stone_mesh"]
    desc = result["unity_recovered_convex_desc"]
    waiting = result["waiting_page_hull_identity"]
    print(f"output: {args.output}")
    print(f"formal mesh: {mesh['unique_vertices']} unique vertices, {mesh['triangles']} triangles")
    print(
        "formal world sorted extents: "
        + ", ".join(f"{value:.6f}" for value in mesh["world_bounds"]["sorted_extents"])
    )
    print(f"support-extreme vertices: {mesh['support_extreme_vertices']}")
    print(f"forced cropped path: {desc['forced_crop_by_vertex_count']} ({desc['reason']})")
    print(f"waiting-page hull extent match: {waiting['any_extent_match_5pct']}")
    unity_flags = result["pyphysx_unity_flags_rebuilt"]["detail"] or {}
    print(
        "rebuilt pyphysx qi0/gpu0 detail: "
        f"{unity_flags.get('unique_vertex_count')} unique vertices, "
        f"{unity_flags.get('triangle_count')} triangles"
    )
    unity_flags_raw = result["pyphysx_unity_flags_rebuilt_raw"]["detail"] or {}
    raw = unity_flags_raw.get("raw_convex_mesh_data") or {}
    if raw:
        print(
            "raw PxConvexMesh: "
            f"{raw.get('nb_vertices')} vertices, "
            f"{raw.get('nb_polygons')} polygons, "
            f"{raw.get('index_count')} polygon indices"
        )
        print(
            "raw hull prism summary: "
            f"{raw.get('top_vertex_count')} top + {raw.get('bottom_vertex_count')} bottom vertices, "
            f"angle step {raw.get('top_angle_step_degrees_min'):.6f}.."
            f"{raw.get('top_angle_step_degrees_max'):.6f} deg"
        )
    topology = result["pyphysx_raw_hull_topology"]["detail"] or {}
    if topology:
        print(
            "raw hull contact topology: "
            f"E={topology.get('nb_edges')}, "
            f"facesByEdges8={topology.get('faces_by_edges8_complete')}, "
            f"facesByVertices8={topology.get('faces_by_vertices8_complete')}"
        )
    bigconvex = result["pyphysx_bigconvex_data"]["detail"] or {}
    if bigconvex:
        print(
            "raw hull BigConvexData: "
            f"VALE adj={bigconvex.get('vale_nb_adjacent_verts')}, "
            f"GAUS samples={bigconvex.get('gaus_nb_samples')}, "
            f"validation errors={bigconvex.get('gaus_bruteforce_validation_error_count')}"
        )
    scaled_mass = result["pyphysx_scaled_mass_properties"]["detail"] or {}
    scaled_args = scaled_mass.get("probe_z_up_custom_args") or {}
    if scaled_mass:
        print(
            "world-scale cooked-hull inertia: "
            f"radial={scaled_args.get('inertia_radial')}, "
            f"vertical={scaled_args.get('inertia_vertical')}"
        )
    formal_cooked_inertia = result["collision_probe_checks"]["formal_geometry_with_cooked_hull_inertia"]
    if formal_cooked_inertia:
        print(
            "formal geometry + cooked inertia replay: "
            f"active RMSE={formal_cooked_inertia.get('active_rmse_m')}, "
            f"target RMSE={formal_cooked_inertia.get('target_in_play_rmse_m')}"
        )
    print(result["current_blocker"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
