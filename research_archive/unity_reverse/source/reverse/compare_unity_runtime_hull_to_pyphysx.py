#!/usr/bin/env python3
"""Compare Unity runtime ConvexHullData buffers with local pyphysx cooked hull data."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260709_171257" / "events.jsonl"
DEFAULT_LOCAL_RAW = (
    PROJECT_ROOT / "data" / "calibration" / "pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_runtime_hull_vs_pyphysx_diff_20260709_171257.json"


def _sha16(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()[:16]


def _pack_f32(value: float) -> bytes:
    return struct.pack("<f", float(value))


def _first_diff(a: bytes, b: bytes) -> dict[str, Any] | None:
    limit = min(len(a), len(b))
    for index in range(limit):
        if a[index] != b[index]:
            return {
                "offset": index,
                "unityByte": a[index],
                "localByte": b[index],
                "unityHex": f"{a[index]:02x}",
                "localHex": f"{b[index]:02x}",
            }
    if len(a) != len(b):
        return {"offset": limit, "unityLength": len(a), "localLength": len(b)}
    return None


def _byte_diff_count(a: bytes, b: bytes) -> int:
    return sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b))


def _read_runtime_hulls(events_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with events_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if "PxcPCMContactConvexConvex" not in line or "hullRuntime" not in line:
                continue
            event = json.loads(line)
            data = event.get("data") if isinstance(event.get("data"), dict) else {}
            extras = data.get("extraDumps") if isinstance(data.get("extraDumps"), list) else []
            for extra in extras:
                if not isinstance(extra, dict) or not str(extra.get("label") or "").endswith(".pcmInputs"):
                    continue
                for shape_name in ("shape0", "shape1"):
                    shape = extra.get(shape_name) if isinstance(extra.get(shape_name), dict) else {}
                    runtime = shape.get("hullRuntime") if isinstance(shape.get("hullRuntime"), dict) else {}
                    window = (
                        runtime.get("runtimeBufferWindow")
                        if isinstance(runtime.get("runtimeBufferWindow"), dict)
                        else {}
                    )
                    raw_bytes = window.get("rawBytes")
                    if not isinstance(raw_bytes, list):
                        continue
                    rows.append(
                        {
                            "lineNumber": line_number,
                            "eventType": event.get("type"),
                            "t": event.get("t"),
                            "phase": data.get("phase"),
                            "shape": shape_name,
                            "geometry": shape.get("decoded"),
                            "hullData": shape.get("hullData"),
                            "runtime": {
                                "vertexRefCount": runtime.get("vertexRefCount"),
                                "byteLayout": runtime.get("byteLayout"),
                                "ptr": window.get("ptr"),
                                "byteLength": window.get("byteLength"),
                                "sha256_16": _sha16(bytes(int(x) & 0xFF for x in raw_bytes)),
                            },
                            "raw": bytes(int(x) & 0xFF for x in raw_bytes),
                        }
                    )
    return rows


def _load_local_raw(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    detail = (payload.get("detail") or {})
    raw = ((detail.get("raw_convex_mesh_data")) or {})
    if not raw:
        raise ValueError(f"{path} has no detail.raw_convex_mesh_data")
    runtime = detail.get("raw_convex_mesh_runtime_hull_data")
    if isinstance(runtime, dict):
        raw = dict(raw)
        raw["raw_convex_mesh_runtime_hull_data"] = runtime
    return raw


def _build_local_runtime_buffer(raw: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    native = raw.get("raw_convex_mesh_runtime_hull_data") if isinstance(raw.get("raw_convex_mesh_runtime_hull_data"), dict) else {}
    native_raw = native.get("raw_bytes") if isinstance(native.get("raw_bytes"), list) else None
    native_layout = native.get("byte_layout") if isinstance(native.get("byte_layout"), dict) else None
    if native_raw is not None and native_layout is not None:
        return bytes(int(value) & 0xFF for value in native_raw), native_layout

    vertices = raw.get("vertices") or []
    polygons = raw.get("polygons") or []
    index_buffer = raw.get("index_buffer") or []

    polygon_bytes = bytearray()
    for polygon in polygons:
        plane = [float(value) for value in polygon["plane"]]
        indices = [int(value) for value in polygon["indices"]]
        nb_vertices = int(polygon["nb_vertices"])
        index_base = int(polygon["index_base"])
        min_index = 0
        min_dot = math.inf
        for vertex_index, vertex in enumerate(vertices):
            dot = float(vertex[0]) * plane[0] + float(vertex[1]) * plane[1] + float(vertex[2]) * plane[2]
            if dot < min_dot:
                min_dot = dot
                min_index = vertex_index
        polygon_bytes.extend(struct.pack("<ffffHBB", plane[0], plane[1], plane[2], plane[3], index_base, nb_vertices, min_index))

    vertex_bytes = bytearray()
    for vertex in vertices:
        vertex_bytes.extend(_pack_f32(vertex[0]))
        vertex_bytes.extend(_pack_f32(vertex[1]))
        vertex_bytes.extend(_pack_f32(vertex[2]))

    topology_path = PROJECT_ROOT / "data" / "calibration" / "pyphysx_raw_hull_topology_20260708.json"
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    contact = topology["contact_relevant_topology"]
    faces_by_edges = bytes(int(value) & 0xFF for pair in contact["faces_by_edges8"] for value in pair)
    faces_by_vertices = bytes(int(value) & 0xFF for triple in contact["faces_by_vertices8"] for value in triple)
    vertex_data = bytes(int(value) & 0xFF for value in index_buffer)

    layout = {
        "polygons": {"offset": 0, "bytes": len(polygon_bytes)},
        "hullVertices": {"offset": len(polygon_bytes), "bytes": len(vertex_bytes)},
        "facesByEdges8": {
            "offset": len(polygon_bytes) + len(vertex_bytes),
            "bytes": len(faces_by_edges),
        },
        "facesByVertices8": {
            "offset": len(polygon_bytes) + len(vertex_bytes) + len(faces_by_edges),
            "bytes": len(faces_by_vertices),
        },
        "vertexData8": {
            "offset": len(polygon_bytes) + len(vertex_bytes) + len(faces_by_edges) + len(faces_by_vertices),
            "bytes": len(vertex_data),
        },
    }
    runtime = bytes(polygon_bytes) + bytes(vertex_bytes) + faces_by_edges + faces_by_vertices + vertex_data
    return runtime, layout


def _slice(raw: bytes, layout: dict[str, Any], key: str) -> bytes:
    item = layout[key]
    start = int(item["offset"])
    return raw[start : start + int(item["bytes"])]


def _decode_polygons(raw: bytes, count: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(count):
        offset = index * 20
        plane0, plane1, plane2, plane3, vref, nb_vertices, min_index = struct.unpack_from("<ffffHBB", raw, offset)
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


def _decode_vertices(raw: bytes, count: int) -> list[list[float]]:
    return [list(struct.unpack_from("<fff", raw, index * 12)) for index in range(count)]


def _round_key(vec: list[float], ndigits: int = 6) -> tuple[float, ...]:
    return tuple(round(float(value), ndigits) for value in vec)


def _set_overlap(unity_vertices: list[list[float]], local_vertices: list[list[float]]) -> dict[str, Any]:
    unity_set = {_round_key(vertex) for vertex in unity_vertices}
    local_set = {_round_key(vertex) for vertex in local_vertices}
    return {
        "unityCount": len(unity_set),
        "localCount": len(local_set),
        "intersectionCount": len(unity_set & local_set),
        "unityOnlyPreview": [list(item) for item in sorted(unity_set - local_set)[:8]],
        "localOnlyPreview": [list(item) for item in sorted(local_set - unity_set)[:8]],
    }


def _nearest_vertex_metrics(unity_vertices: list[list[float]], local_vertices: list[list[float]]) -> dict[str, Any]:
    distances: list[float] = []
    worst: dict[str, Any] | None = None
    for unity_vertex in unity_vertices:
        best_distance = math.inf
        best_local: list[float] | None = None
        for local_vertex in local_vertices:
            distance = math.dist(unity_vertex, local_vertex)
            if distance < best_distance:
                best_distance = distance
                best_local = local_vertex
        distances.append(best_distance)
        if worst is None or best_distance > worst["distance"]:
            worst = {
                "distance": best_distance,
                "unityVertex": unity_vertex,
                "nearestLocalVertex": best_local,
            }
    rms = math.sqrt(sum(distance * distance for distance in distances) / len(distances)) if distances else None
    return {
        "count": len(distances),
        "maxDistanceLocalUnits": max(distances) if distances else None,
        "rmsDistanceLocalUnits": rms,
        "worstPair": worst,
    }


def _norm_angle_deg(value: float) -> float:
    value = float(value) % 360.0
    return value + 360.0 if value < 0 else value


def _angle_delta_deg(a: float, b: float) -> float:
    return ((_norm_angle_deg(a) - _norm_angle_deg(b) + 180.0) % 360.0) - 180.0


def _side_plane_angle_alignment(
    unity_polygons: list[dict[str, Any]], local_polygons: list[dict[str, Any]]
) -> dict[str, Any]:
    unity_angles = sorted(
        _norm_angle_deg(math.degrees(math.atan2(float(row["plane"][2]), float(row["plane"][0]))))
        for row in unity_polygons
        if int(row.get("mNbVerts") or 0) == 4
    )
    local_angles = sorted(
        _norm_angle_deg(math.degrees(math.atan2(float(row["plane"][2]), float(row["plane"][0]))))
        for row in local_polygons
        if int(row.get("mNbVerts") or 0) == 4
    )
    if not unity_angles or len(unity_angles) != len(local_angles):
        return {
            "unitySideCount": len(unity_angles),
            "localSideCount": len(local_angles),
            "comparable": False,
        }

    best: dict[str, Any] | None = None
    count = len(unity_angles)
    for shift in range(count):
        rotation = _angle_delta_deg(unity_angles[0], local_angles[shift])
        errors = [
            _angle_delta_deg(unity_angles[index], local_angles[(index + shift) % count] + rotation)
            for index in range(count)
        ]
        score = max(abs(error) for error in errors)
        candidate = {
            "shift": shift,
            "rotationDeg": rotation,
            "maxAbsErrorDeg": score,
            "rmsErrorDeg": math.sqrt(sum(error * error for error in errors) / count),
            "firstErrorsDeg": errors[:8],
        }
        if best is None or candidate["maxAbsErrorDeg"] < best["maxAbsErrorDeg"]:
            best = candidate

    return {
        "unitySideCount": len(unity_angles),
        "localSideCount": len(local_angles),
        "comparable": True,
        "best": best,
        "unitySortedPreviewDeg": unity_angles[:8],
        "localSortedPreviewDeg": local_angles[:8],
    }


def _segment_report(unity: bytes, local: bytes) -> dict[str, Any]:
    return {
        "unityBytes": len(unity),
        "localBytes": len(local),
        "unitySha256_16": _sha16(unity),
        "localSha256_16": _sha16(local),
        "byteEqual": unity == local,
        "byteDiffCount": _byte_diff_count(unity, local),
        "firstDiff": _first_diff(unity, local),
    }


def analyze(events_path: Path, local_raw_path: Path) -> dict[str, Any]:
    unity_rows = _read_runtime_hulls(events_path)
    if not unity_rows:
        raise ValueError(f"no PxcPCMContactConvexConvex hullRuntime rows found in {events_path}")

    local_raw = _load_local_raw(local_raw_path)
    local_runtime, local_layout = _build_local_runtime_buffer(local_raw)
    local_runtime_source = (
        "native Gu::ConvexHullData runtime buffer"
        if isinstance(local_raw.get("raw_convex_mesh_runtime_hull_data"), dict)
        else "python rebuilt buffer from public PxConvexMesh data"
    )
    first = unity_rows[0]
    unity_raw = first["raw"]
    unity_layout = first["runtime"]["byteLayout"]

    segment_keys = ["polygons", "hullVertices", "facesByEdges8", "facesByVertices8", "vertexData8"]
    segments = {
        key: _segment_report(_slice(unity_raw, unity_layout, key), _slice(local_runtime, local_layout, key))
        for key in segment_keys
        if key in unity_layout and key in local_layout
    }
    extra_local_segments = {
        key: _segment_report(b"", _slice(local_runtime, local_layout, key))
        for key in sorted(local_layout)
        if key not in unity_layout
    }

    nb_polygons = int((first.get("hullData") or {}).get("nbPolygons") or local_raw.get("nb_polygons") or 0)
    nb_vertices = int((first.get("hullData") or {}).get("nbHullVertices") or local_raw.get("nb_vertices") or 0)
    unity_polygons = _decode_polygons(_slice(unity_raw, unity_layout, "polygons"), nb_polygons)
    local_polygons = _decode_polygons(_slice(local_runtime, local_layout, "polygons"), nb_polygons)
    first_polygon_diff = None
    for up, lp in zip(unity_polygons, local_polygons):
        if up != lp:
            first_polygon_diff = {"unity": up, "local": lp}
            break

    unity_vertices = _decode_vertices(_slice(unity_raw, unity_layout, "hullVertices"), nb_vertices)
    local_vertices = _decode_vertices(_slice(local_runtime, local_layout, "hullVertices"), nb_vertices)

    all_unity_hashes = {}
    for row in unity_rows:
        key = f"{row['shape']}:{row['phase']}:{row['eventType']}"
        all_unity_hashes.setdefault(key, set()).add(row["runtime"]["sha256_16"])

    return {
        "source": {
            "unityEvents": str(events_path),
            "localRaw": str(local_raw_path),
        },
        "selectedUnityRuntimeHull": {
            key: value
            for key, value in first.items()
            if key not in {"raw"}
        },
        "unityRuntimeHullHashGroups": {key: sorted(values) for key, values in sorted(all_unity_hashes.items())},
        "localRuntime": {
            "bytes": len(local_runtime),
            "sha256_16": _sha16(local_runtime),
            "layout": local_layout,
            "source": local_runtime_source,
        },
        "overall": _segment_report(unity_raw, local_runtime),
        "segments": segments,
        "extraLocalSegments": extra_local_segments,
        "firstPolygonDiff": first_polygon_diff,
        "vertexSetOverlapRounded1e6": _set_overlap(unity_vertices, local_vertices),
        "nearestVertexMetrics": _nearest_vertex_metrics(unity_vertices, local_vertices),
        "sidePlaneAngleAlignment": _side_plane_angle_alignment(unity_polygons, local_polygons),
        "conclusion": (
            f"Unity runtime cooked hull buffer is byte-identical to the local pyphysx {local_runtime_source}."
            if unity_raw == local_runtime
            else (
                f"Unity runtime cooked hull buffer differs from the local pyphysx {local_runtime_source}; "
                "see first differing segment."
            )
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--local-raw", type=Path, default=DEFAULT_LOCAL_RAW)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = analyze(args.events, args.local_raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "overall": report["overall"],
                "localRuntime": report["localRuntime"],
                "segments": report["segments"],
                "extraLocalSegments": report["extraLocalSegments"],
                "firstPolygonDiff": report["firstPolygonDiff"],
                "vertexSetOverlapRounded1e6": report["vertexSetOverlapRounded1e6"],
                "nearestVertexMetrics": report["nearestVertexMetrics"],
                "sidePlaneAngleAlignment": report["sidePlaneAngleAlignment"],
                "conclusion": report["conclusion"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
