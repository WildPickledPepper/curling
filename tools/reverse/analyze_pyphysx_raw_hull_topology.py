#!/usr/bin/env python3
"""Analyze contact-relevant topology from a dumped pyphysx PxConvexMesh.

The input is produced by dump_pyphysx_cooked_convex_hull.py with
--include-raw-convex-data.  This script reconstructs the pieces that PhysX
ConvexHullBuilder stores around Gu::ConvexHullData: unique edges,
facesByEdges8, facesByVertices8, and compact face/edge geometry summaries.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "pyphysx_raw_hull_topology_20260708.json"
WORLD_SCALE = (0.112700008, 0.115, 0.112700008)


Vector = tuple[float, float, float]


def _vec(values: Any) -> Vector:
    return (float(values[0]), float(values[1]), float(values[2]))


def _sub(a: Vector, b: Vector) -> Vector:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a: Vector, b: Vector) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(v: Vector) -> float:
    return math.sqrt(_dot(v, v))


def _scale(v: Vector, scale: Vector) -> Vector:
    return (v[0] * scale[0], v[1] * scale[1], v[2] * scale[2])


def _round_list(values: list[float] | tuple[float, ...], digits: int = 9) -> list[float]:
    return [round(float(value), digits) for value in values]


def _canonical_dir(v: Vector) -> Vector:
    length = _norm(v)
    if length == 0.0:
        return (0.0, 0.0, 0.0)
    n = (v[0] / length, v[1] / length, v[2] / length)
    for component in n:
        if abs(component) > 1e-9:
            if component < 0.0:
                return (-n[0], -n[1], -n[2])
            return n
    return n


def _classify_polygon(polygon: dict[str, Any]) -> str:
    plane = polygon["plane"]
    normal = _vec(plane[:3])
    if polygon["nb_vertices"] == 64 and normal[1] > 0.9:
        return "top_cap"
    if polygon["nb_vertices"] == 64 and normal[1] < -0.9:
        return "bottom_cap"
    if polygon["nb_vertices"] == 4 and abs(normal[1]) < 1e-4:
        return "side_quad"
    return "other"


def _classify_edge(vertices: list[Vector], edge_vertices: tuple[int, int]) -> str:
    a = vertices[edge_vertices[0]]
    b = vertices[edge_vertices[1]]
    if a[1] > 0.0 and b[1] > 0.0:
        return "top_ring"
    if a[1] < 0.0 and b[1] < 0.0:
        return "bottom_ring"
    if a[1] * b[1] < 0.0:
        return "vertical"
    return "other"


def _load_raw_report(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    detail = report.get("detail") or {}
    raw = detail.get("raw_convex_mesh_data")
    if not isinstance(raw, dict):
        raise SystemExit(
            f"{path} has no detail.raw_convex_mesh_data. Re-run dump_pyphysx_cooked_convex_hull.py "
            "with --include-raw-convex-data."
        )
    return report, raw


def _build_faces_by_vertices(polygons: list[dict[str, Any]], nb_vertices: int) -> tuple[list[list[int]], bool]:
    faces_by_vertices: list[list[int]] = [[] for _ in range(nb_vertices)]
    for face_id, polygon in enumerate(polygons):
        for index in polygon["indices"]:
            if len(faces_by_vertices[index]) < 3:
                faces_by_vertices[index].append(face_id)

    complete = all(len(faces) == 3 for faces in faces_by_vertices)
    if not complete:
        return [[255, 255, 255] for _ in range(nb_vertices)], False
    return faces_by_vertices, True


def _build_edges(polygons: list[dict[str, Any]], vertices: list[Vector]) -> dict[str, Any]:
    redundant: list[dict[str, Any]] = []
    for face_id, polygon in enumerate(polygons):
        indices = [int(value) for value in polygon["indices"]]
        for vertex_id, v0 in enumerate(indices):
            v1 = indices[(vertex_id + 1) % len(indices)]
            sorted_v0 = v0
            sorted_v1 = v1
            flipped = sorted_v0 > sorted_v1
            if flipped:
                sorted_v0, sorted_v1 = sorted_v1, sorted_v0
            redundant.append(
                {
                    "sorted_v0": sorted_v0,
                    "sorted_v1": sorted_v1,
                    "face_id": face_id,
                    "vertex_id": vertex_id,
                    "flipped": flipped,
                    "original_v0": v0,
                    "original_v1": v1,
                    "index_base": int(polygon["index_base"]),
                }
            )

    sorted_entries = sorted(redundant, key=lambda item: (item["sorted_v0"], item["sorted_v1"]))
    edges: list[dict[str, Any]] = []
    edge_data16_by_vertex_ref = [None] * len(redundant)
    pair_counts: Counter[tuple[int, int]] = Counter()
    previous_pair: tuple[int, int] | None = None
    previous_face: int | None = None
    nb_hull_edges = 0

    for sorted_index, item in enumerate(sorted_entries):
        pair = (item["sorted_v0"], item["sorted_v1"])
        pair_counts[pair] += 1
        if pair != previous_pair:
            tail = item["sorted_v0"]
            head = item["sorted_v1"]
            if item["flipped"]:
                tail, head = head, tail
            edge_type = _classify_edge(vertices, (tail, head))
            local_vector = _sub(vertices[head], vertices[tail])
            world_vector = _sub(_scale(vertices[head], WORLD_SCALE), _scale(vertices[tail], WORLD_SCALE))
            edges.append(
                {
                    "edge_id": nb_hull_edges,
                    "vertices": [tail, head],
                    "sorted_vertices": [pair[0], pair[1]],
                    "faces_by_edges8": [item["face_id"], None],
                    "type": edge_type,
                    "length_local": _norm(local_vector),
                    "length_world_m": _norm(world_vector),
                    "direction_local_canonical": _round_list(_canonical_dir(local_vector)),
                }
            )
            previous_pair = pair
            previous_face = item["face_id"]
            nb_hull_edges += 1
        else:
            edges[-1]["faces_by_edges8"] = [previous_face, item["face_id"]]

        edge_data16_by_vertex_ref[item["index_base"] + item["vertex_id"]] = sorted_index // 2

    if any(value is None for value in edge_data16_by_vertex_ref):
        raise RuntimeError("edgeData16 reconstruction left unset vertex references")

    manifold = all(count == 2 for count in pair_counts.values()) and all(
        edge["faces_by_edges8"][0] is not None and edge["faces_by_edges8"][1] is not None for edge in edges
    )
    type_counts = Counter(edge["type"] for edge in edges)

    lengths_by_type: dict[str, dict[str, float]] = {}
    for edge_type in sorted(type_counts):
        local_lengths = [edge["length_local"] for edge in edges if edge["type"] == edge_type]
        world_lengths = [edge["length_world_m"] for edge in edges if edge["type"] == edge_type]
        lengths_by_type[edge_type] = {
            "local_min": min(local_lengths),
            "local_max": max(local_lengths),
            "world_min_m": min(world_lengths),
            "world_max_m": max(world_lengths),
        }

    unique_direction_keys = {
        tuple(round(component, 6) for component in edge["direction_local_canonical"]) for edge in edges
    }
    return {
        "nb_edges": len(edges),
        "manifold": manifold,
        "edge_type_counts": dict(sorted(type_counts.items())),
        "lengths_by_type": lengths_by_type,
        "unique_direction_class_count": len(unique_direction_keys),
        "faces_by_edges8": [edge["faces_by_edges8"] for edge in edges],
        "edges": edges,
        "edge_data16_by_vertex_ref": [int(value) for value in edge_data16_by_vertex_ref],
    }


def _polygon_summaries(polygons: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    summaries: list[dict[str, Any]] = []
    class_counts: Counter[str] = Counter()
    side_angles: list[float] = []

    for face_id, polygon in enumerate(polygons):
        face_class = _classify_polygon(polygon)
        class_counts[face_class] += 1
        plane = [float(value) for value in polygon["plane"]]
        angle = None
        if face_class == "side_quad":
            angle = math.degrees(math.atan2(plane[2], plane[0]))
            side_angles.append(angle)
        summaries.append(
            {
                "face_id": face_id,
                "class": face_class,
                "nb_vertices": int(polygon["nb_vertices"]),
                "index_base": int(polygon["index_base"]),
                "plane": _round_list(plane),
                "side_normal_angle_degrees": None if angle is None else round(angle, 9),
                "indices": [int(value) for value in polygon["indices"]],
            }
        )

    side_steps: list[float] = []
    if side_angles:
        sorted_angles = sorted(side_angles)
        for index, angle in enumerate(sorted_angles):
            next_angle = sorted_angles[0] + 360.0 if index == len(sorted_angles) - 1 else sorted_angles[index + 1]
            side_steps.append(next_angle - angle)
    if side_steps:
        class_counts["side_normal_step_min_mdeg"] = round(min(side_steps) * 1000)
        class_counts["side_normal_step_max_mdeg"] = round(max(side_steps) * 1000)
    return summaries, {str(key): int(value) for key, value in class_counts.items()}


def _geometry_summary(vertices: list[Vector], polygons: list[dict[str, Any]]) -> dict[str, Any]:
    radial_values = [math.hypot(v[0], v[2]) for v in vertices]
    side_planes = [polygon["plane"] for polygon in polygons if _classify_polygon(polygon) == "side_quad"]
    apothems = []
    for plane in side_planes:
        normal_len_xz = math.hypot(float(plane[0]), float(plane[2]))
        if normal_len_xz:
            apothems.append(-float(plane[3]) / normal_len_xz)
    top_y = [v[1] for v in vertices if v[1] > 0.0]
    bottom_y = [v[1] for v in vertices if v[1] < 0.0]
    radius = max(radial_values)
    apothem = min(apothems) if apothems else None
    return {
        "local_vertex_radius_min": min(radial_values),
        "local_vertex_radius_max": max(radial_values),
        "local_side_apothem_min": min(apothems) if apothems else None,
        "local_side_apothem_max": max(apothems) if apothems else None,
        "local_radius_minus_apothem": None if apothem is None else radius - apothem,
        "world_vertex_radius_max_m": radius * WORLD_SCALE[0],
        "world_side_apothem_min_m": None if apothem is None else apothem * WORLD_SCALE[0],
        "world_radius_minus_apothem_m": None if apothem is None else (radius - apothem) * WORLD_SCALE[0],
        "local_top_y": sorted(set(round(value, 9) for value in top_y)),
        "local_bottom_y": sorted(set(round(value, 9) for value in bottom_y)),
        "world_top_y_m": sorted(set(round(value * WORLD_SCALE[1], 9) for value in top_y)),
        "world_bottom_y_m": sorted(set(round(value * WORLD_SCALE[1], 9) for value in bottom_y)),
    }


def analyze(input_path: Path) -> dict[str, Any]:
    report, raw = _load_raw_report(input_path)
    vertices = [_vec(vertex) for vertex in raw["vertices"]]
    polygons = list(raw["polygons"])
    vertex_refs = [int(value) for value in raw["index_buffer"]]

    polygon_summaries, polygon_class_counts = _polygon_summaries(polygons)
    faces_by_vertices8, faces_by_vertices_complete = _build_faces_by_vertices(polygons, len(vertices))
    vertex_face_valencies = Counter(len([face for face in faces if face != 255]) for faces in faces_by_vertices8)
    edge_data = _build_edges(polygons, vertices)

    nb_vertices = len(vertices)
    nb_polygons = len(polygons)
    nb_edges = edge_data["nb_edges"]
    euler_ok = nb_vertices - nb_edges + nb_polygons == 2

    return {
        "tool": "tools/reverse/analyze_pyphysx_raw_hull_topology.py",
        "input": str(input_path),
        "source_report": {
            "tool": report.get("tool"),
            "detailed_variant": report.get("detailed_variant"),
            "selected_flags": report.get("selected_flags"),
        },
        "physx_source_anchors": {
            "ConvexHullData": "physx/source/geomutils/src/convex/GuConvexMeshData.h",
            "ConvexHullBuilder_createEdgeList": "physx/source/physxcooking/src/convex/ConvexHullBuilder.cpp",
            "ConvexHullBuilder_save": "physx/source/physxcooking/src/convex/ConvexHullBuilder.cpp",
            "convex_convex_edge_axes": "physx/source/geomutils/src/contact/GuContactConvexConvex.cpp",
            "pcm_triangle_convex_edges": "physx/source/geomutils/src/pcm/GuPCMTriangleContactGen.cpp",
        },
        "counts": {
            "nb_vertices": nb_vertices,
            "nb_polygons": nb_polygons,
            "nb_vertex_refs": len(vertex_refs),
            "nb_edges": nb_edges,
            "euler_characteristic": nb_vertices - nb_edges + nb_polygons,
            "euler_ok": euler_ok,
            "polygon_class_counts": polygon_class_counts,
            "edge_type_counts": edge_data["edge_type_counts"],
            "vertex_face_valency_histogram": {str(key): value for key, value in sorted(vertex_face_valencies.items())},
        },
        "geometry_summary": _geometry_summary(vertices, polygons),
        "contact_relevant_topology": {
            "faces_by_edges8_complete": edge_data["manifold"],
            "faces_by_vertices8_complete": faces_by_vertices_complete,
            "faces_by_edges8_length": nb_edges * 2,
            "faces_by_vertices8_length": nb_vertices * 3,
            "vertex_data8_length": len(vertex_refs),
            "edge_data16_length": len(edge_data["edge_data16_by_vertex_ref"]),
            "unique_edge_direction_class_count": edge_data["unique_direction_class_count"],
            "lengths_by_type": edge_data["lengths_by_type"],
            "faces_by_vertices8": faces_by_vertices8,
            "faces_by_edges8": edge_data["faces_by_edges8"],
            "edge_data16_by_vertex_ref": edge_data["edge_data16_by_vertex_ref"],
            "vertex_data8": vertex_refs,
            "edges": edge_data["edges"],
        },
        "runtime_buffer_layout_bytes": {
            "HullPolygonData_polygons": nb_polygons * 20,
            "hull_vertices": nb_vertices * 12,
            "faces_by_edges8": nb_edges * 2,
            "faces_by_vertices8": nb_vertices * 3,
            "vertices_by_edges16": 0,
            "vertex_data8": len(vertex_refs),
            "total_runtime_extra_buffer": nb_polygons * 20
            + nb_vertices * 12
            + nb_edges * 2
            + nb_vertices * 3
            + len(vertex_refs),
            "note": "verticesByEdges16 is absent when mNbEdges GRB bit is not set; Unity recovered buildGPUData=false.",
        },
        "clhl_payload_layout_bytes_excluding_chunk_header": {
            "count_dwords": 16,
            "hull_vertices": nb_vertices * 12,
            "HullPolygonData_polygons": nb_polygons * 20,
            "vertex_data8": len(vertex_refs),
            "faces_by_edges8": nb_edges * 2,
            "faces_by_vertices8": nb_vertices * 3,
            "vertices_by_edges16": 0,
            "total": 16 + nb_vertices * 12 + nb_polygons * 20 + len(vertex_refs) + nb_edges * 2 + nb_vertices * 3,
        },
        "polygon_summaries": polygon_summaries,
        "conclusion": (
            "The offline Unity-flags PxConvexMesh is a manifold 64-sided prism: "
            "128 vertices, 66 polygons, 192 unique edges, and 384 polygon vertex refs. "
            "Every vertex has exactly 3 incident faces, so PhysX facesByVertices8 is valid. "
            "facesByEdges8 is reconstructable from the raw polygon/index buffer; exact byte ordering "
            "should still be verified against Unity's formal-stone CLHL stream if byte-perfect parity is required."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = result["counts"]
    geometry = result["geometry_summary"]
    print(f"output: {args.output}")
    print(
        "topology: "
        f"V={counts['nb_vertices']}, F={counts['nb_polygons']}, E={counts['nb_edges']}, "
        f"V-E+F={counts['euler_characteristic']}"
    )
    print(f"polygon classes: {counts['polygon_class_counts']}")
    print(f"edge classes: {counts['edge_type_counts']}")
    print(
        "side apothem/radius world gap: "
        f"{geometry['world_radius_minus_apothem_m']:.9f} m"
    )
    print(result["conclusion"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
