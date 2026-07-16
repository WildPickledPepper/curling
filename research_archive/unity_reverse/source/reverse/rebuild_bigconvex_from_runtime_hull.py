#!/usr/bin/env python3
"""Rebuild PhysX BigConvexRawData arrays from a runtime ConvexHullData buffer.

The Unity WebGL dump gives us the in-memory Gu::ConvexHullData feature buffer,
but older captures did not include the pointed BigConvexRawData arrays.  This
tool reconstructs those arrays from the runtime hull topology and first checks
the reconstruction against local pyphysx native bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260709_171257" / "events.jsonl"
DEFAULT_LOCAL_NATIVE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_native_runtime_20260709.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_runtime_bigconvex_rebuild_20260709.json"


def _sha16(values: list[int] | bytes) -> str:
    raw = values if isinstance(values, bytes) else bytes(int(value) & 0xFF for value in values)
    return hashlib.sha256(raw).hexdigest()[:16]


def _first_diff(a: list[int], b: list[int]) -> dict[str, Any] | None:
    limit = min(len(a), len(b))
    for index in range(limit):
        if int(a[index]) != int(b[index]):
            return {"offset": index, "a": int(a[index]), "b": int(b[index])}
    if len(a) != len(b):
        return {"offset": limit, "a_len": len(a), "b_len": len(b)}
    return None


def _byte_diff_count(a: list[int], b: list[int]) -> int:
    return sum(int(x) != int(y) for x, y in zip(a, b)) + abs(len(a) - len(b))


def _infer_layout(raw_len: int, nb_polygons: int, nb_vertices: int, nb_edges: int, vertex_ref_count: int) -> dict[str, Any]:
    offset = 0
    layout: dict[str, Any] = {}
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


def _slice(raw: bytes, layout: dict[str, Any], key: str) -> bytes:
    item = layout[key]
    start = int(item["offset"])
    return raw[start : start + int(item["bytes"])]


def _decode_polygons(raw: bytes, count: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(count):
        plane0, plane1, plane2, plane3, vref, nb_vertices, min_index = struct.unpack_from(
            "<ffffHBB", raw, index * 20
        )
        rows.append(
            {
                "index": index,
                "plane": [plane0, plane1, plane2, plane3],
                "mVRef8": vref,
                "mNbVerts": nb_vertices,
                "mMinIndex": min_index,
            }
        )
    return rows


def _decode_vertices(raw: bytes, count: int) -> list[tuple[float, float, float]]:
    return [struct.unpack_from("<fff", raw, index * 12) for index in range(count)]


def _decode_faces_by_edges(raw: bytes, count: int) -> list[tuple[int, int]]:
    return [(raw[index * 2], raw[index * 2 + 1]) for index in range(count)]


def _decode_u16_pairs(raw: bytes, count: int) -> list[tuple[int, int]]:
    return [struct.unpack_from("<HH", raw, index * 4) for index in range(count)]


def _read_local_native(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    runtime = payload["detail"]["raw_convex_mesh_runtime_hull_data"]
    big = runtime["big_convex_raw_data"]
    return {
        "path": str(path),
        "raw": bytes(int(value) & 0xFF for value in runtime["raw_bytes"]),
        "layout": runtime.get("byte_layout"),
        "nb_polygons": int(runtime["nb_polygons"]),
        "nb_vertices": int(runtime["nb_hull_vertices"]),
        "nb_edges": int(runtime["nb_edges"]),
        "vertex_ref_count": int(runtime["byte_layout"]["vertexData8"]["bytes"]),
        "has_grb_edges": bool(runtime.get("has_grb_edges")),
        "expected": {
            "samples": [int(value) & 0xFF for value in big["samples_raw_bytes"]],
            "valencies": [int(value) & 0xFF for value in big["valencies_raw_bytes"]],
            "adjacent_vertices": [int(value) & 0xFF for value in big["adjacent_vertices_raw_bytes"]],
        },
    }


def _read_unity_runtime_hull(events_path: Path, line_number: int | None) -> dict[str, Any]:
    with events_path.open("r", encoding="utf-8") as handle:
        for current, line in enumerate(handle, start=1):
            if line_number is not None and current != line_number:
                continue
            if "PxcPCMContactConvexConvex" not in line or "hullRuntime" not in line:
                continue
            event = json.loads(line)
            extras = event.get("data", {}).get("extraDumps", [])
            for extra in extras:
                if not isinstance(extra, dict):
                    continue
                shape = extra.get("shape0") if isinstance(extra.get("shape0"), dict) else {}
                runtime = shape.get("hullRuntime") if isinstance(shape.get("hullRuntime"), dict) else {}
                window = (
                    runtime.get("runtimeBufferWindow")
                    if isinstance(runtime.get("runtimeBufferWindow"), dict)
                    else {}
                )
                raw_bytes = window.get("rawBytes")
                if not isinstance(raw_bytes, list):
                    continue
                layout = runtime.get("byteLayout")
                hull_data = shape.get("hullData") if isinstance(shape.get("hullData"), dict) else {}
                vertex_ref_count = int(runtime.get("vertexRefCount") or 384)
                return {
                    "path": str(events_path),
                    "line_number": current,
                    "raw": bytes(int(value) & 0xFF for value in raw_bytes),
                    "layout": layout,
                    "nb_polygons": int(hull_data.get("nbPolygons") or 66),
                    "nb_vertices": int(hull_data.get("nbHullVertices") or 128),
                    "nb_edges": int(hull_data.get("nbEdges") or 192),
                    "vertex_ref_count": vertex_ref_count,
                    "has_grb_edges": False,
                }
    raise ValueError(f"no runtime hull found in {events_path}")


def _edge_data_from_vertex_refs(
    polygons: list[dict[str, Any]],
    vertex_data: bytes,
    faces_by_edges: list[tuple[int, int]],
    vertices_by_edges16: list[tuple[int, int]] | None,
) -> tuple[list[int], dict[str, Any]]:
    occurrences: dict[tuple[int, int], list[dict[str, int]]] = defaultdict(list)
    edge_data = [0] * len(vertex_data)

    for face_id, polygon in enumerate(polygons):
        vref = int(polygon["mVRef8"])
        count = int(polygon["mNbVerts"])
        refs = [int(vertex_data[vref + slot]) for slot in range(count)]
        for slot, a in enumerate(refs):
            b = refs[(slot + 1) % count]
            key = (a, b) if a <= b else (b, a)
            occurrences[key].append({"face": face_id, "slot": slot, "a": a, "b": b})

    edge_ids_by_face_pair: dict[frozenset[int], int] = {}
    duplicate_face_pairs: list[dict[str, Any]] = []
    for edge_id, pair in enumerate(faces_by_edges):
        face_pair = frozenset((int(pair[0]), int(pair[1])))
        if face_pair in edge_ids_by_face_pair:
            duplicate_face_pairs.append(
                {"face_pair": sorted(face_pair), "first": edge_ids_by_face_pair[face_pair], "second": edge_id}
            )
        edge_ids_by_face_pair[face_pair] = edge_id

    sorted_keys = sorted(occurrences)
    edge_pair_mismatches: list[dict[str, Any]] = []
    vertex_pair_mismatches: list[dict[str, Any]] = []
    non_manifold: list[dict[str, Any]] = []
    missing_face_pair_edges: list[dict[str, Any]] = []
    for sorted_edge_id, key in enumerate(sorted_keys):
        rows = occurrences[key]
        if len(rows) != 2:
            non_manifold.append({"sorted_edge_id": sorted_edge_id, "key": list(key), "occurrence_count": len(rows)})
            edge_id = sorted_edge_id
        else:
            actual_faces = frozenset(int(row["face"]) for row in rows)
            edge_id = edge_ids_by_face_pair.get(actual_faces, sorted_edge_id)
            if actual_faces not in edge_ids_by_face_pair:
                missing_face_pair_edges.append(
                    {"sorted_edge_id": sorted_edge_id, "key": list(key), "actual_faces": sorted(actual_faces)}
                )
        for row in rows:
            edge_data[int(polygons[row["face"]]["mVRef8"]) + row["slot"]] = edge_id

        expected_faces = set(faces_by_edges[edge_id]) if edge_id < len(faces_by_edges) else set()
        actual_faces = {int(row["face"]) for row in rows}
        if expected_faces != actual_faces:
            edge_pair_mismatches.append(
                {
                    "edge_id": edge_id,
                    "key": list(key),
                    "faces_by_edges": list(faces_by_edges[edge_id]) if edge_id < len(faces_by_edges) else None,
                    "actual_faces": sorted(actual_faces),
                }
            )
        if vertices_by_edges16 is not None:
            actual_pair = tuple(vertices_by_edges16[edge_id])
            if actual_pair != key and actual_pair != (key[1], key[0]):
                vertex_pair_mismatches.append(
                    {
                        "edge_id": edge_id,
                        "sorted_key": list(key),
                        "vertices_by_edges16": list(actual_pair),
                    }
                )

    return edge_data, {
        "edge_count_from_refs": len(sorted_keys),
        "duplicate_faces_by_edges_pair_count": len(duplicate_face_pairs),
        "duplicate_faces_by_edges_pair_preview": duplicate_face_pairs[:8],
        "missing_face_pair_edge_count": len(missing_face_pair_edges),
        "missing_face_pair_edge_preview": missing_face_pair_edges[:8],
        "non_manifold_count": len(non_manifold),
        "non_manifold_preview": non_manifold[:8],
        "faces_by_edges_set_mismatch_count": len(edge_pair_mismatches),
        "faces_by_edges_set_mismatch_preview": edge_pair_mismatches[:8],
        "vertices_by_edges16_pair_mismatch_count": len(vertex_pair_mismatches),
        "vertices_by_edges16_pair_mismatch_preview": vertex_pair_mismatches[:8],
    }


def _reconstruct_valencies(
    polygons: list[dict[str, Any]],
    nb_vertices: int,
    faces_by_edges: list[tuple[int, int]],
    edge_data: list[int],
    vertex_data: bytes,
) -> dict[str, Any]:
    counts = [0] * nb_vertices
    for polygon in polygons:
        vref = int(polygon["mVRef8"])
        for slot in range(int(polygon["mNbVerts"])):
            counts[int(vertex_data[vref + slot])] += 1

    offsets = [0] * nb_vertices
    for index in range(1, nb_vertices):
        offsets[index] = offsets[index - 1] + counts[index - 1]
    adjacent = [None] * (offsets[-1] + counts[-1])
    write_offsets = offsets[:]
    vertex_marker = [0] * nb_vertices

    for face_id, polygon in enumerate(polygons):
        vref = int(polygon["mVRef8"])
        count = int(polygon["mNbVerts"])
        data = [int(vertex_data[vref + slot]) for slot in range(count)]
        for slot, vertex_index in enumerate(data):
            if vertex_marker[vertex_index] != 0:
                continue
            num_adj = 0
            prev_index = data[(slot + 1) % count]
            adjacent[write_offsets[vertex_index]] = prev_index
            write_offsets[vertex_index] += 1
            num_adj += 1

            edge_index = edge_data[vref + slot]
            n0, n1 = faces_by_edges[edge_index]
            neighbor_polygon = n1 if n0 == face_id else n0

            while neighbor_polygon != face_id:
                neighbor = polygons[neighbor_polygon]
                neighbor_vref = int(neighbor["mVRef8"])
                neighbor_count = int(neighbor["mNbVerts"])
                neighbor_data = [
                    int(vertex_data[neighbor_vref + neighbor_slot]) for neighbor_slot in range(neighbor_count)
                ]
                next_edge_slot = 0
                found = False
                for neighbor_slot, candidate in enumerate(neighbor_data):
                    if candidate != vertex_index:
                        continue
                    next_index = neighbor_data[(neighbor_slot + 1) % neighbor_count]
                    if next_index == prev_index:
                        prev_index = neighbor_data[neighbor_count - 1] if neighbor_slot == 0 else neighbor_data[neighbor_slot - 1]
                        next_edge_slot = neighbor_count - 1 if neighbor_slot == 0 else neighbor_slot - 1
                    else:
                        prev_index = next_index
                        next_edge_slot = neighbor_slot
                    adjacent[write_offsets[vertex_index]] = prev_index
                    write_offsets[vertex_index] += 1
                    num_adj += 1
                    found = True
                    break
                if not found:
                    raise RuntimeError(f"vertex {vertex_index} not found in polygon {neighbor_polygon}")

                next_edge_index = edge_data[neighbor_vref + next_edge_slot]
                n0, n1 = faces_by_edges[next_edge_index]
                neighbor_polygon = n1 if n0 == neighbor_polygon else n0

            vertex_marker[vertex_index] = num_adj

    if any(value is None for value in adjacent):
        raise RuntimeError("adjacent vertex reconstruction left holes")

    valencies = [{"count": counts[index], "offset": offsets[index]} for index in range(nb_vertices)]
    valencies_raw: list[int] = []
    for row in valencies:
        valencies_raw.extend(struct.pack("<HH", int(row["count"]), int(row["offset"])))

    return {
        "valencies": valencies,
        "adjacent_vertices": [int(value) for value in adjacent],
        "valencies_raw_bytes": valencies_raw,
        "adjacent_vertices_raw_bytes": [int(value) for value in adjacent],
        "count_histogram": {str(key): value for key, value in sorted(Counter(counts).items())},
        "vertex_marker_histogram": {str(key): value for key, value in sorted(Counter(vertex_marker).items())},
    }


def _f32(value: Any) -> np.float32:
    return np.float32(value)


def _dot_f32(a: tuple[float, float, float], b: tuple[np.float32, np.float32, np.float32]) -> np.float32:
    return _f32(_f32(a[0]) * b[0] + _f32(a[1]) * b[1] + _f32(a[2]) * b[2])


def _normalize_f32(v: tuple[np.float32, np.float32, np.float32]) -> tuple[np.float32, np.float32, np.float32]:
    length = _f32(np.sqrt(_f32(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])))
    if float(length) == 0.0:
        return (_f32(0.0), _f32(0.0), _f32(0.0))
    return (_f32(v[0] / length), _f32(v[1] / length), _f32(v[2] / length))


def _precompute_sample(
    vertices: list[tuple[float, float, float]],
    valencies: list[dict[str, int]],
    adjacent_vertices: list[int],
    direction: tuple[np.float32, np.float32, np.float32],
    start_index: int,
    negative_dir: float,
) -> int:
    small_bitmap = [0] * 8
    neg = _f32(negative_dir)
    minimum = _f32(neg * _dot_f32(vertices[start_index], direction))
    while True:
        initial_index = start_index
        row = valencies[start_index]
        for neighbor_index in adjacent_vertices[int(row["offset"]) : int(row["offset"]) + int(row["count"])]:
            dist = _f32(neg * _dot_f32(vertices[neighbor_index], direction))
            if dist < minimum:
                bucket = neighbor_index >> 5
                mask = 1 << (neighbor_index & 31)
                if (small_bitmap[bucket] & mask) == 0:
                    small_bitmap[bucket] |= mask
                    minimum = dist
                    start_index = neighbor_index
        if start_index == initial_index:
            return start_index


def _reconstruct_samples(
    vertices: list[tuple[float, float, float]],
    valencies: list[dict[str, int]],
    adjacent_vertices: list[int],
    subdiv: int,
) -> dict[str, Any]:
    nb_samples = 6 * subdiv * subdiv
    samples_min = [0] * nb_samples
    samples_max = [0] * nb_samples
    start_index = [0] * 12
    start_index2 = [0] * 12
    half_subdiv = _f32(_f32(subdiv - 1) * _f32(0.5))

    for j in range(subdiv):
        for i in range(j, subdiv):
            i_subdiv = _f32(_f32(1.0) - _f32(i) / half_subdiv)
            j_subdiv = _f32(_f32(1.0) - _f32(j) / half_subdiv)
            temp = _normalize_f32((_f32(1.0), i_subdiv, j_subdiv))
            dirs = [
                (_f32(-temp[0]), temp[1], temp[2]),
                (temp[0], temp[1], temp[2]),
                (temp[2], _f32(-temp[0]), temp[1]),
                (temp[2], temp[0], temp[1]),
                (temp[1], temp[2], _f32(-temp[0])),
                (temp[1], temp[2], temp[0]),
                (_f32(-temp[0]), temp[2], temp[1]),
                (temp[0], temp[2], temp[1]),
                (temp[1], _f32(-temp[0]), temp[2]),
                (temp[1], temp[0], temp[2]),
                (temp[2], temp[1], _f32(-temp[0])),
                (temp[2], temp[1], temp[0]),
            ]
            for d_step, direction in enumerate(dirs):
                start_index[d_step] = _precompute_sample(
                    vertices, valencies, adjacent_vertices, direction, start_index[d_step], 1.0
                )
                start_index2[d_step] = _precompute_sample(
                    vertices, valencies, adjacent_vertices, direction, start_index2[d_step], -1.0
                )
            for k in range(6):
                ksub = k * subdiv * subdiv
                offset = j + i * subdiv + ksub
                offset2 = i + j * subdiv + ksub
                samples_min[offset] = start_index[k]
                samples_max[offset] = start_index2[k]
                samples_min[offset2] = start_index[k + 6]
                samples_max[offset2] = start_index2[k + 6]

    samples_raw = [int(value) for value in samples_min + samples_max]
    return {
        "subdiv": subdiv,
        "nb_samples": nb_samples,
        "samples_min": samples_min,
        "samples_max": samples_max,
        "samples_raw_bytes": samples_raw,
        "unique_sample_vertices": len(set(samples_raw)),
    }


def _rebuild_from_runtime_hull(source: dict[str, Any], subdiv: int) -> dict[str, Any]:
    raw = source["raw"]
    layout = source.get("layout") or _infer_layout(
        len(raw), source["nb_polygons"], source["nb_vertices"], source["nb_edges"], source["vertex_ref_count"]
    )
    polygons = _decode_polygons(_slice(raw, layout, "polygons"), source["nb_polygons"])
    vertices = _decode_vertices(_slice(raw, layout, "hullVertices"), source["nb_vertices"])
    faces_by_edges = _decode_faces_by_edges(_slice(raw, layout, "facesByEdges8"), source["nb_edges"])
    vertex_data = _slice(raw, layout, "vertexData8")
    vertices_by_edges16 = None
    if "verticesByEdges16" in layout:
        vertices_by_edges16 = _decode_u16_pairs(_slice(raw, layout, "verticesByEdges16"), source["nb_edges"])

    edge_data, edge_checks = _edge_data_from_vertex_refs(polygons, vertex_data, faces_by_edges, vertices_by_edges16)
    vale = _reconstruct_valencies(polygons, source["nb_vertices"], faces_by_edges, edge_data, vertex_data)
    gaus = _reconstruct_samples(vertices, vale["valencies"], vale["adjacent_vertices"], subdiv)

    return {
        "source": {
            "raw_byte_count": len(raw),
            "raw_sha16": _sha16(raw),
            "layout": layout,
            "nb_polygons": source["nb_polygons"],
            "nb_vertices": source["nb_vertices"],
            "nb_edges": source["nb_edges"],
            "has_grb_edges": source.get("has_grb_edges"),
        },
        "edge_checks": edge_checks,
        "big_convex": {
            "samples_raw_bytes": gaus["samples_raw_bytes"],
            "valencies_raw_bytes": vale["valencies_raw_bytes"],
            "adjacent_vertices_raw_bytes": vale["adjacent_vertices_raw_bytes"],
            "samples_sha16": _sha16(gaus["samples_raw_bytes"]),
            "valencies_sha16": _sha16(vale["valencies_raw_bytes"]),
            "adjacent_vertices_sha16": _sha16(vale["adjacent_vertices_raw_bytes"]),
            "lengths": {
                "samples": len(gaus["samples_raw_bytes"]),
                "valencies": len(vale["valencies_raw_bytes"]),
                "adjacent_vertices": len(vale["adjacent_vertices_raw_bytes"]),
            },
        },
        "vale_summary": {
            "count_histogram": vale["count_histogram"],
            "vertex_marker_histogram": vale["vertex_marker_histogram"],
        },
        "gaus_summary": {
            "subdiv": subdiv,
            "nb_samples": gaus["nb_samples"],
            "unique_sample_vertices": gaus["unique_sample_vertices"],
        },
    }


def _compare_rebuild(name: str, rebuilt: dict[str, Any], expected: dict[str, list[int]]) -> dict[str, Any]:
    actual = rebuilt["big_convex"]
    rows: dict[str, Any] = {}
    for key in ("samples", "valencies", "adjacent_vertices"):
        actual_values = actual[f"{key}_raw_bytes"]
        expected_values = expected[key]
        rows[key] = {
            "actual_len": len(actual_values),
            "expected_len": len(expected_values),
            "byte_diff_count": _byte_diff_count(actual_values, expected_values),
            "first_diff": _first_diff(actual_values, expected_values),
            "actual_sha16": _sha16(actual_values),
            "expected_sha16": _sha16(expected_values),
        }
    return {
        "name": name,
        "all_byte_equal": all(row["byte_diff_count"] == 0 for row in rows.values()),
        "fields": rows,
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    local = _read_local_native(args.local_native)
    unity = _read_unity_runtime_hull(args.events, args.event_line)
    local_rebuilt = _rebuild_from_runtime_hull(local, args.subdiv)
    unity_rebuilt = _rebuild_from_runtime_hull(unity, args.subdiv)
    local_compare = _compare_rebuild("local_native_rebuild_vs_pyphysx_native", local_rebuilt, local["expected"])

    if local_compare["all_byte_equal"]:
        answer = (
            "The runtime-hull BigConvex rebuild byte-matches local pyphysx native arrays. "
            "The Unity 4008-byte hull can now be paired with synthetic BigConvex arrays for contact A/B."
        )
    else:
        answer = (
            "The runtime-hull BigConvex rebuild does not yet byte-match local pyphysx native arrays; "
            "do not trust the Unity synthetic arrays until the local self-check is fixed."
        )

    return {
        "question": "Can BigConvexRawData be rebuilt from a runtime Gu::ConvexHullData buffer?",
        "answer": answer,
        "inputs": {
            "local_native": str(args.local_native),
            "unity_events": str(args.events),
            "unity_event_line": unity.get("line_number"),
            "subdiv": args.subdiv,
        },
        "local_rebuilt": local_rebuilt,
        "local_self_check": local_compare,
        "unity_rebuilt": unity_rebuilt,
        "next_step": (
            "If local_self_check.all_byte_equal is true, feed unity_rebuilt.big_convex arrays into "
            "probe_unity_runtime_hull_patch_contacts.py as the synthetic BigConvex patch."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--event-line", type=int, default=221)
    parser.add_argument("--local-native", type=Path, default=DEFAULT_LOCAL_NATIVE)
    parser.add_argument("--subdiv", type=int, default=16)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {args.output.relative_to(PROJECT_ROOT)}")
    print(report["answer"])
    check = report["local_self_check"]
    print(f"local byte equal: {check['all_byte_equal']}")
    for key, row in check["fields"].items():
        print(f"{key}: diff={row['byte_diff_count']} actual={row['actual_sha16']} expected={row['expected_sha16']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
