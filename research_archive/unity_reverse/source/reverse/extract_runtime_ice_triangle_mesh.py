#!/usr/bin/env python3
"""Extract the runtime ice PxTriangleMesh header from probe JSONL events."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path
from typing import Any, Iterator


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "data/calibration/unity_runtime_ice_triangle_mesh.json"


def _events(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                item = json.loads(line)
                if isinstance(item, dict):
                    yield item


def _triangle_shape(pcm: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    for name in ("shape0", "shape1"):
        shape = pcm.get(name)
        if not isinstance(shape, dict):
            continue
        decoded = shape.get("decoded")
        if isinstance(decoded, dict) and int(decoded.get("geometryType") or -1) == 5:
            return name, shape
    return None


def _raw_bytes(window: object) -> bytes | None:
    if not isinstance(window, dict):
        return None
    values = window.get("rawBytes")
    if not isinstance(values, list):
        return None
    try:
        return bytes(values)
    except ValueError:
        return None


def _decode_verified_mesh(runtime: object) -> dict[str, Any] | None:
    """Decode only the explicitly verified 32-bit Gu::TriangleMesh fields."""
    if not isinstance(runtime, dict):
        return None
    layout = runtime.get("verifiedLayout")
    vertex_raw = _raw_bytes(runtime.get("vertexBuffer"))
    triangle_raw = _raw_bytes(runtime.get("triangleBuffer"))
    if not isinstance(layout, dict) or vertex_raw is None or triangle_raw is None:
        return None

    try:
        nb_vertices = int(layout["nbVertices"])
        nb_triangles = int(layout["nbTriangles"])
        index_width = int(layout["indexWidth"])
    except (KeyError, TypeError, ValueError):
        return None
    vertex_bytes = nb_vertices * 12
    triangle_bytes = nb_triangles * 3 * index_width
    if index_width not in {2, 4} or len(vertex_raw) != vertex_bytes or len(triangle_raw) != triangle_bytes:
        return None

    vertices = [
        list(struct.unpack_from("<fff", vertex_raw, index * 12))
        for index in range(nb_vertices)
    ]
    index_format = "H" if index_width == 2 else "I"
    flat_indices = list(struct.unpack(f"<{nb_triangles * 3}{index_format}", triangle_raw))
    if any(index < 0 or index >= nb_vertices for index in flat_indices):
        return None
    return {
        "layout": {
            "nbVertices": nb_vertices,
            "nbTriangles": nb_triangles,
            "verticesPtr": int(layout["verticesPtr"]),
            "trianglesPtr": int(layout["trianglesPtr"]),
            "meshFlags": int(layout["meshFlags"]),
            "indexWidth": index_width,
        },
        "sha256": {
            "vertices": hashlib.sha256(vertex_raw).hexdigest(),
            "triangles": hashlib.sha256(triangle_raw).hexdigest(),
        },
        "vertices": vertices,
        "triangles": [
            flat_indices[index : index + 3]
            for index in range(0, len(flat_indices), 3)
        ],
    }


def _decode_cooked_internals(runtime: object) -> dict[str, Any] | None:
    """Decode optional face-remap/BV4 buffers emitted by the v3 runtime probe."""
    if not isinstance(runtime, dict):
        return None
    layout = runtime.get("verifiedLayout")
    if not isinstance(layout, dict):
        return None
    try:
        nb_triangles = int(layout["nbTriangles"])
    except (KeyError, TypeError, ValueError):
        return None
    result: dict[str, Any] = {}
    face_raw = _raw_bytes(runtime.get("faceRemapBuffer"))
    if face_raw is not None and len(face_raw) == nb_triangles * 4:
        result["faceRemap"] = list(struct.unpack(f"<{nb_triangles}I", face_raw))
        result.setdefault("sha256", {})["faceRemap"] = hashlib.sha256(face_raw).hexdigest()
    bvh4 = runtime.get("bvh4")
    if isinstance(bvh4, dict):
        node_raw = _raw_bytes(bvh4.get("nodeBuffer"))
        try:
            nb_nodes = int(bvh4["nbNodes"])
            node_size = int(bvh4["nodeSize"])
        except (KeyError, TypeError, ValueError):
            nb_nodes = node_size = 0
        if node_raw is not None and len(node_raw) == nb_nodes * node_size:
            result["bvh4"] = {
                "nbNodes": nb_nodes,
                "initData": bvh4.get("initData"),
                "nodeSize": node_size,
                "rawBytes": list(node_raw),
            }
            result.setdefault("sha256", {})["bvh4Nodes"] = hashlib.sha256(node_raw).hexdigest()
    return result or None


def extract(path: Path) -> dict[str, Any]:
    captures: list[dict[str, Any]] = []
    for event in _events(path):
        if event.get("type") not in {"physx.native.before", "physx.native.after"}:
            continue
        data = event.get("data")
        if not isinstance(data, dict) or (data.get("hook") or {}).get("name") != "PxcPCMContactConvexMesh":
            continue
        for pcm in data.get("extraDumps") or []:
            if not isinstance(pcm, dict):
                continue
            found = _triangle_shape(pcm)
            if found is None:
                continue
            name, shape = found
            decoded = shape["decoded"]
            runtime = shape.get("triangleMeshRuntime")
            captures.append(
                {
                    "eventTime": event.get("t"),
                    "phase": data.get("phase"),
                    "dumpId": data.get("dumpId"),
                    "callIndex": data.get("callIndex"),
                    "triangleShape": name,
                    "triangleGeometry": decoded,
                    "triangleMeshRuntime": runtime,
                    "decodedMesh": _decode_verified_mesh(runtime),
                    "decodedCookedInternals": _decode_cooked_internals(runtime),
                    "transform0": ((pcm.get("transform0") or {}).get("decoded")),
                    "transform1": ((pcm.get("transform1") or {}).get("decoded")),
                    "narrowPhaseParams": ((pcm.get("narrowPhaseParams") or {}).get("decoded")),
                }
            )
    return {
        "schema": "unity_runtime_ice_triangle_mesh_v3",
        "source": str(path),
        "captureCount": len(captures),
        "captures": captures,
        "interpretation": (
            "A capture is useful only when triangleMeshRuntime is present. "
            "decodedMesh uses verified Gu::TriangleMesh fields: counts at +16/+20, pointers at +24/+28, "
            "and index width at +64. v3 captures also decode faceRemap (+72) and the verified BV4Tree "
            "node buffer (mNbNodes +144, mNodes +148)."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = extract(args.events)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "captureCount": report["captureCount"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
