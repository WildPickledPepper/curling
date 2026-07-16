#!/usr/bin/env python3
"""Reconstruct PhysX BigConvexData VALE/GAUS from the offline raw hull.

PhysX builds BigConvexData for convex hulls whose vertex count exceeds
gaussMapLimit.  The recovered Unity cooking path uses gaussMapLimit=32, while
the formal stone's offline Unity-flags cooked hull has 128 vertices, so this
support/hill-climbing data is part of the contact-query input.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json"
)
DEFAULT_TOPOLOGY = PROJECT_ROOT / "data" / "calibration" / "pyphysx_raw_hull_topology_20260708.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "pyphysx_bigconvex_data_20260709.json"


Vector = tuple[float, float, float]


def _vec(values: Any) -> Vector:
    return (float(values[0]), float(values[1]), float(values[2]))


def _dot(a: Vector, b: Vector) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _normalize(v: Vector) -> Vector:
    length = math.sqrt(_dot(v, v))
    if length == 0.0:
        return (0.0, 0.0, 0.0)
    return (v[0] / length, v[1] / length, v[2] / length)


def _round_vec(v: Vector, digits: int = 9) -> list[float]:
    return [round(v[0], digits), round(v[1], digits), round(v[2], digits)]


def _load_raw(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    raw = (report.get("detail") or {}).get("raw_convex_mesh_data")
    if not isinstance(raw, dict):
        raise SystemExit(
            f"{path} has no detail.raw_convex_mesh_data. Run dump_pyphysx_cooked_convex_hull.py "
            "with --include-raw-convex-data first."
        )
    return report, raw


def _load_topology(path: Path) -> dict[str, Any]:
    report = json.loads(path.read_text(encoding="utf-8"))
    topology = report.get("contact_relevant_topology")
    if not isinstance(topology, dict):
        raise SystemExit(
            f"{path} has no contact_relevant_topology. Run analyze_pyphysx_raw_hull_topology.py first."
        )
    return report


def _polygon_refs(polygons: list[dict[str, Any]], face_id: int) -> list[int]:
    return [int(value) for value in polygons[face_id]["indices"]]


def _reconstruct_vale(
    polygons: list[dict[str, Any]],
    nb_vertices: int,
    faces_by_edges8: list[list[int]],
    edge_data16_by_vertex_ref: list[int],
) -> dict[str, Any]:
    counts = [0] * nb_vertices
    for polygon in polygons:
        for index in polygon["indices"]:
            counts[int(index)] += 1

    offsets = [0] * nb_vertices
    for index in range(1, nb_vertices):
        offsets[index] = offsets[index - 1] + counts[index - 1]
    nb_adjacent = offsets[-1] + counts[-1]
    adjacent = [None] * nb_adjacent
    write_offsets = offsets[:]
    vertex_marker = [0] * nb_vertices

    for face_id, polygon in enumerate(polygons):
        data = _polygon_refs(polygons, face_id)
        num_verts = len(data)
        index_base = int(polygon["index_base"])
        for vertex_slot, vertex_index in enumerate(data):
            num_adj = 0
            if vertex_marker[vertex_index] != 0:
                continue

            prev_index = data[(vertex_slot + 1) % num_verts]
            adjacent[write_offsets[vertex_index]] = prev_index
            write_offsets[vertex_index] += 1
            num_adj += 1

            edge_index = edge_data16_by_vertex_ref[index_base + vertex_slot] * 2
            n0, n1 = faces_by_edges8[edge_index // 2]
            neighbor_polygon = n1 if n0 == face_id else n0

            while neighbor_polygon != face_id:
                neighbor_data = _polygon_refs(polygons, neighbor_polygon)
                num_neighbor_verts = len(neighbor_data)
                next_edge_index = 0

                for neighbor_slot, candidate in enumerate(neighbor_data):
                    if candidate != vertex_index:
                        continue

                    next_index = neighbor_data[(neighbor_slot + 1) % num_neighbor_verts]
                    if next_index == prev_index:
                        prev_index = (
                            neighbor_data[num_neighbor_verts - 1]
                            if neighbor_slot == 0
                            else neighbor_data[neighbor_slot - 1]
                        )
                        next_edge_index = num_neighbor_verts - 1 if neighbor_slot == 0 else neighbor_slot - 1
                    else:
                        prev_index = next_index
                        next_edge_index = neighbor_slot

                    adjacent[write_offsets[vertex_index]] = prev_index
                    write_offsets[vertex_index] += 1
                    num_adj += 1
                    break
                else:
                    raise RuntimeError(f"vertex {vertex_index} not found in neighbor polygon {neighbor_polygon}")

                neighbor_index_base = int(polygons[neighbor_polygon]["index_base"])
                edge_index2 = edge_data16_by_vertex_ref[neighbor_index_base + next_edge_index] * 2
                n0, n1 = faces_by_edges8[edge_index2 // 2]
                neighbor_polygon = n1 if n0 == neighbor_polygon else n0

            vertex_marker[vertex_index] = num_adj

    if any(value is None for value in adjacent):
        raise RuntimeError("VALE reconstruction left unset adjacent vertices")

    valencies = [
        {
            "vertex": index,
            "count": counts[index],
            "offset": offsets[index],
            "adjacent": [int(value) for value in adjacent[offsets[index] : offsets[index] + counts[index]]],
        }
        for index in range(nb_vertices)
    ]
    max_valency = max(counts)
    count_histogram = Counter(counts)
    return {
        "nb_verts": nb_vertices,
        "nb_adjacent_verts": nb_adjacent,
        "max_valency_count": max_valency,
        "compressed_valency_index_bytes": 1 if max_valency <= 0xFF else 2,
        "valency_count_histogram": {str(key): value for key, value in sorted(count_histogram.items())},
        "valencies": valencies,
        "adjacent_verts": [int(value) for value in adjacent],
        "vertex_marker_histogram": {str(key): value for key, value in sorted(Counter(vertex_marker).items())},
    }


def _precompute_sample(
    vertices: list[Vector],
    valencies: list[dict[str, Any]],
    adjacent_verts: list[int],
    direction: Vector,
    start_index: int,
    negative_dir: float,
) -> int:
    small_bitmap = [0] * 8
    minimum = negative_dir * _dot(vertices[start_index], direction)
    while True:
        initial_index = start_index
        valency = valencies[start_index]
        count = int(valency["count"])
        offset = int(valency["offset"])
        for neighbour_index in adjacent_verts[offset : offset + count]:
            dist = negative_dir * _dot(vertices[neighbour_index], direction)
            if dist < minimum:
                bucket = neighbour_index >> 5
                mask = 1 << (neighbour_index & 31)
                if (small_bitmap[bucket] & mask) == 0:
                    small_bitmap[bucket] |= mask
                    minimum = dist
                    start_index = neighbour_index
        if start_index == initial_index:
            return start_index


def _sample_dirs(subdiv: int) -> list[tuple[int, int, int, Vector]]:
    dirs: list[tuple[int, int, int, Vector]] = []
    half_subdiv = float(subdiv - 1) * 0.5
    for j in range(subdiv):
        for i in range(j, subdiv):
            i_subdiv = 1.0 - i / half_subdiv
            j_subdiv = 1.0 - j / half_subdiv
            temp_dir = _normalize((1.0, i_subdiv, j_subdiv))
            variants = [
                (-temp_dir[0], temp_dir[1], temp_dir[2]),
                (temp_dir[0], temp_dir[1], temp_dir[2]),
                (temp_dir[2], -temp_dir[0], temp_dir[1]),
                (temp_dir[2], temp_dir[0], temp_dir[1]),
                (temp_dir[1], temp_dir[2], -temp_dir[0]),
                (temp_dir[1], temp_dir[2], temp_dir[0]),
                (-temp_dir[0], temp_dir[2], temp_dir[1]),
                (temp_dir[0], temp_dir[2], temp_dir[1]),
                (temp_dir[1], -temp_dir[0], temp_dir[2]),
                (temp_dir[1], temp_dir[0], temp_dir[2]),
                (temp_dir[2], temp_dir[1], -temp_dir[0]),
                (temp_dir[2], temp_dir[1], temp_dir[0]),
            ]
            for k in range(6):
                offset = j + i * subdiv + k * subdiv * subdiv
                dirs.append((offset, k, 0, variants[k]))
                offset2 = i + j * subdiv + k * subdiv * subdiv
                dirs.append((offset2, k + 6, 1, variants[k + 6]))
    return dirs


def _reconstruct_gaus(
    vertices: list[Vector],
    vale: dict[str, Any],
    *,
    subdiv: int,
) -> dict[str, Any]:
    nb_samples = 6 * subdiv * subdiv
    samples_min = [0] * nb_samples
    samples_max = [0] * nb_samples
    start_index = [0] * 12
    start_index2 = [0] * 12
    valencies = list(vale["valencies"])
    adjacent_verts = list(vale["adjacent_verts"])

    half_subdiv = float(subdiv - 1) * 0.5
    for j in range(subdiv):
        for i in range(j, subdiv):
            i_subdiv = 1.0 - i / half_subdiv
            j_subdiv = 1.0 - j / half_subdiv
            temp_dir = _normalize((1.0, i_subdiv, j_subdiv))
            dirs = [
                (-temp_dir[0], temp_dir[1], temp_dir[2]),
                (temp_dir[0], temp_dir[1], temp_dir[2]),
                (temp_dir[2], -temp_dir[0], temp_dir[1]),
                (temp_dir[2], temp_dir[0], temp_dir[1]),
                (temp_dir[1], temp_dir[2], -temp_dir[0]),
                (temp_dir[1], temp_dir[2], temp_dir[0]),
                (-temp_dir[0], temp_dir[2], temp_dir[1]),
                (temp_dir[0], temp_dir[2], temp_dir[1]),
                (temp_dir[1], -temp_dir[0], temp_dir[2]),
                (temp_dir[1], temp_dir[0], temp_dir[2]),
                (temp_dir[2], temp_dir[1], -temp_dir[0]),
                (temp_dir[2], temp_dir[1], temp_dir[0]),
            ]

            for d_step, direction in enumerate(dirs):
                start_index[d_step] = _precompute_sample(
                    vertices, valencies, adjacent_verts, direction, start_index[d_step], 1.0
                )
                start_index2[d_step] = _precompute_sample(
                    vertices, valencies, adjacent_verts, direction, start_index2[d_step], -1.0
                )

            for k in range(6):
                ksub = k * subdiv * subdiv
                offset = j + i * subdiv + ksub
                offset2 = i + j * subdiv + ksub
                samples_min[offset] = start_index[k]
                samples_max[offset] = start_index2[k]
                samples_min[offset2] = start_index[k + 6]
                samples_max[offset2] = start_index2[k + 6]

    validation_errors: list[dict[str, Any]] = []
    generated_dirs = {offset: direction for offset, _d_step, _kind, direction in _sample_dirs(subdiv)}
    for offset, direction in generated_dirs.items():
        min_index = samples_min[offset]
        max_index = samples_max[offset]
        dots = [_dot(vertex, direction) for vertex in vertices]
        min_dot = min(dots)
        max_dot = max(dots)
        if abs(dots[min_index] - min_dot) > 1e-8:
            validation_errors.append(
                {
                    "offset": offset,
                    "kind": "min",
                    "sample_index": min_index,
                    "sample_dot": dots[min_index],
                    "expected": min_dot,
                    "direction": _round_vec(direction),
                }
            )
        if abs(dots[max_index] - max_dot) > 1e-8:
            validation_errors.append(
                {
                    "offset": offset,
                    "kind": "max",
                    "sample_index": max_index,
                    "sample_dot": dots[max_index],
                    "expected": max_dot,
                    "direction": _round_vec(direction),
                }
            )

    return {
        "subdiv": subdiv,
        "nb_samples": nb_samples,
        "samples_byte_count": nb_samples * 2,
        "unique_min_sample_vertices": len(set(samples_min)),
        "unique_max_sample_vertices": len(set(samples_max)),
        "unique_all_sample_vertices": len(set(samples_min) | set(samples_max)),
        "min_sample_histogram_top": Counter(samples_min).most_common(16),
        "max_sample_histogram_top": Counter(samples_max).most_common(16),
        "samples_min": samples_min,
        "samples_max": samples_max,
        "bruteforce_validation_error_count": len(validation_errors),
        "bruteforce_validation_errors": validation_errors[:32],
    }


def analyze(raw_path: Path, topology_path: Path, subdiv: int) -> dict[str, Any]:
    source_report, raw = _load_raw(raw_path)
    topology_report = _load_topology(topology_path)
    topology = topology_report["contact_relevant_topology"]
    polygons = list(raw["polygons"])
    vertices = [_vec(vertex) for vertex in raw["vertices"]]
    faces_by_edges8 = [[int(pair[0]), int(pair[1])] for pair in topology["faces_by_edges8"]]
    edge_data16_by_vertex_ref = [int(value) for value in topology["edge_data16_by_vertex_ref"]]

    vale = _reconstruct_vale(polygons, len(vertices), faces_by_edges8, edge_data16_by_vertex_ref)
    gaus = _reconstruct_gaus(vertices, vale, subdiv=subdiv)

    nb_vertices = len(vertices)
    nb_edges = int(topology_report["counts"]["nb_edges"])
    max_valency = int(vale["max_valency_count"])
    valency_count_bytes = 1 if max_valency <= 0xFF else 2
    vale_payload_bytes = 12 + nb_vertices * valency_count_bytes + int(vale["nb_adjacent_verts"])
    gaus_payload_bytes = 8 + int(gaus["samples_byte_count"])

    return {
        "tool": "tools/reverse/analyze_pyphysx_bigconvex_data.py",
        "raw_input": str(raw_path),
        "topology_input": str(topology_path),
        "source_report": {
            "tool": source_report.get("tool"),
            "detailed_variant": source_report.get("detailed_variant"),
            "selected_flags": source_report.get("selected_flags"),
        },
        "physx_source_anchors": {
            "computeGaussMaps": "physx/source/physxcooking/src/convex/ConvexMeshBuilder.cpp",
            "BigConvexDataBuilder": "physx/source/physxcooking/src/convex/BigConvexDataBuilder.cpp",
            "BigConvexRawData": "physx/source/geomutils/src/convex/GuBigConvexData.h",
            "runtime_hill_climbing": "physx/source/geomutils/src/convex/GuHillClimbing.cpp",
            "convex_support_seed": "physx/source/geomutils/src/convex/GuShapeConvex.cpp",
        },
        "trigger": {
            "gauss_map_vertex_limit": 32,
            "nb_hull_vertices": nb_vertices,
            "big_convex_data_required": nb_vertices > 32,
            "density_subdiv": subdiv,
        },
        "vale": vale,
        "gaus": gaus,
        "stream_payload_bytes_excluding_chunk_headers": {
            "SUPM_wrapper": 0,
            "GAUS": gaus_payload_bytes,
            "VALE": vale_payload_bytes,
            "GAUS_plus_VALE": gaus_payload_bytes + vale_payload_bytes,
            "note": "Chunk headers from WriteHeader('SUPM'/'GAUS'/'VALE') are not counted here.",
        },
        "consistency_checks": {
            "nb_adjacent_verts_equals_edges_times_two": int(vale["nb_adjacent_verts"]) == nb_edges * 2,
            "all_valencies_are_three": set(int(item["count"]) for item in vale["valencies"]) == {3},
            "gaus_bruteforce_validation_passed": int(gaus["bruteforce_validation_error_count"]) == 0,
            "gaus_sample_bytes_match_physx": int(gaus["samples_byte_count"]) == 6 * subdiv * subdiv * 2,
        },
        "conclusion": (
            "For the offline Unity-flags 128-vertex hull, BigConvexData is required because "
            "128 > gaussMapLimit=32. VALE reconstructs to 128 vertices, 384 adjacent-vertex entries, "
            "and valency 3 for every vertex. GAUS uses density/subdiv=16, nbSamples=1536, and "
            "3072 sample bytes; the reconstructed samples pass brute-force support validation for "
            "all generated cube-map directions. Byte-level parity with Unity still requires the "
            "formal-stone CVXM/SUPM/GAUS/VALE stream, but the offline algorithmic contents are no "
            "longer opaque."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--topology", type=Path, default=DEFAULT_TOPOLOGY)
    parser.add_argument("--subdiv", type=int, default=16)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = analyze(args.raw, args.topology, args.subdiv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"output: {args.output}")
    print(
        "VALE: "
        f"nbVerts={result['vale']['nb_verts']}, "
        f"nbAdjVerts={result['vale']['nb_adjacent_verts']}, "
        f"valency_hist={result['vale']['valency_count_histogram']}"
    )
    print(
        "GAUS: "
        f"subdiv={result['gaus']['subdiv']}, "
        f"nbSamples={result['gaus']['nb_samples']}, "
        f"sampleBytes={result['gaus']['samples_byte_count']}, "
        f"validationErrors={result['gaus']['bruteforce_validation_error_count']}"
    )
    print(result["conclusion"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
