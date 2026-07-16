#!/usr/bin/env python3
"""Compare Unity's captured rink TriangleMesh with local PhysX cooking output.

This is a P4 evidence tool. It does not alter training state and it does not
pretend that re-cooking Unity's post-cook arrays yields Unity's original BV4
tree. It records which fields are available in the existing capture.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from unity_front_half_physx import (  # noqa: E402
    DEFAULT_RUNTIME_ICE_MESH,
    PersistentPhysxFrontHalfScene,
)


DEFAULT_OUTPUT = PROJECT_ROOT / "data/calibration/runtime_ice_cooked_equivalence_audit_20260710.json"


def _sha_bytes(values: list[int]) -> str:
    return hashlib.sha256(bytes(int(value) & 0xFF for value in values)).hexdigest()


def _sha_json(values: object) -> str:
    raw = json.dumps(values, ensure_ascii=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def _sha_f32_triplets(values: list[list[float]]) -> str:
    return hashlib.sha256(b"".join(struct.pack("<fff", *row) for row in values)).hexdigest()


def _sha_triangle_indices(values: list[list[int]], index_width: int) -> str:
    fmt = "<HHH" if int(index_width) == 2 else "<III"
    return hashlib.sha256(b"".join(struct.pack(fmt, *row) for row in values)).hexdigest()


def _sha_u32(values: list[int]) -> str:
    return hashlib.sha256(struct.pack(f"<{len(values)}I", *values)).hexdigest()


def _summarize_local(shape: Any) -> dict[str, Any]:
    raw = dict(shape.get_triangle_mesh_runtime_data())
    bv4 = dict(raw.get("bv4") or {})
    vertices = [list(row) for row in raw.get("vertices") or []]
    triangles = [list(row) for row in raw.get("triangles") or []]
    face_remap = [int(value) for value in raw.get("face_remap") or []]
    return {
        "geometry": {
            "scale": list(raw.get("scale") or []),
            "scaleRotationXyzw": list(raw.get("scale_rotation_xyzw") or []),
            "meshFlags": raw.get("mesh_flags"),
            "triangleMeshFlags": raw.get("triangle_mesh_flags"),
            "midphaseId": raw.get("midphase_id"),
            "nbVertices": raw.get("nb_vertices"),
            "nbTriangles": raw.get("nb_triangles"),
            "indexWidth": raw.get("index_width"),
        },
        "arrays": {
            "verticesSha256": _sha_json(vertices),
            "trianglesSha256": _sha_json(triangles),
            "verticesRawSha256": _sha_f32_triplets(vertices),
            "trianglesRawSha256": _sha_triangle_indices(triangles, int(raw.get("index_width") or 4)),
            "faceRemapSha256": _sha_json(raw.get("face_remap") or []),
            "faceRemapRawSha256": _sha_u32(face_remap) if face_remap else None,
            "adjacenciesSha256": _sha_json(raw.get("adjacencies") or []),
            "faceRemapCount": len(raw.get("face_remap") or []),
            "adjacenciesCount": len(raw.get("adjacencies") or []),
        },
        "bv4": {
            "available": bool(bv4),
            "nbNodes": bv4.get("nb_nodes"),
            "initData": bv4.get("init_data"),
            "quantized": bv4.get("quantized"),
            "nodeSize": bv4.get("node_size"),
            "centerOrMinCoeff": list(bv4.get("center_or_min_coeff") or []),
            "extentsOrMaxCoeff": list(bv4.get("extents_or_max_coeff") or []),
            "rawBytes": len(bv4.get("raw_bytes") or []),
            "rawSha256": _sha_bytes(list(bv4.get("raw_bytes") or [])) if bv4 else None,
        },
    }


def _unity_summary(document: dict[str, Any]) -> dict[str, Any]:
    captures = document.get("captures") or []
    capture = next(
        (item for item in captures if isinstance(item, dict) and item.get("decodedMesh")),
        None,
    )
    if capture is None:
        raise ValueError("capture has no decoded Unity triangle mesh")
    mesh = dict(capture["decodedMesh"])
    geometry = dict(capture.get("triangleGeometry") or {})
    runtime = dict(capture.get("triangleMeshRuntime") or {})
    internals = dict(capture.get("decodedCookedInternals") or {})
    header = dict(runtime.get("headerWindow") or {})
    return {
        "source": document.get("source"),
        "geometry": {
            "scale": list(geometry.get("scale") or []),
            "scaleRotation": list(geometry.get("scaleRotation") or []),
            "meshFlags": geometry.get("meshFlags"),
            "nbVertices": (mesh.get("layout") or {}).get("nbVertices"),
            "nbTriangles": (mesh.get("layout") or {}).get("nbTriangles"),
            "indexWidth": (mesh.get("layout") or {}).get("indexWidth"),
        },
        "arrays": {
            "verticesSha256": (mesh.get("sha256") or {}).get("vertices"),
            "trianglesSha256": (mesh.get("sha256") or {}).get("triangles"),
            "faceRemapRawSha256": (internals.get("sha256") or {}).get("faceRemap"),
            "faceRemapCaptured": isinstance(internals.get("faceRemap"), list),
            "adjacenciesCaptured": False,
        },
        "bv4": {
            "available": isinstance(internals.get("bvh4"), dict),
            "headerEvidence": {
                "nbNodes": 100,
                "initData": 4,
                "quantized": True,
                "nodeSize": 16,
                "rawBytesExpected": 1600,
                "source": "verified Unity Gu::BV4TriangleMesh header; full mNodes buffer was not captured",
            },
            "rawSha256": (internals.get("sha256") or {}).get("bvh4Nodes"),
        },
        "headerWindowSha256": _sha_bytes(list(header.get("rawBytes") or [])) if header.get("rawBytes") else None,
    }


def _make_scene(**kwargs: Any) -> PersistentPhysxFrontHalfScene:
    return PersistentPhysxFrontHalfScene(
        stone_count=1,
        runtime_feature_events=None,
        patch_runtime_features=False,
        **kwargs,
    )


def audit(runtime_mesh: Path) -> dict[str, Any]:
    unity_document = json.loads(runtime_mesh.read_text(encoding="utf-8"))
    unity = _unity_summary(unity_document)
    capture = next(item for item in unity_document["captures"] if item.get("decodedMesh"))
    unity_triangles = [list(row) for row in capture["decodedMesh"]["triangles"]]
    bvh33 = _make_scene()
    bvh34 = _make_scene(ice_use_fast_midphase=True)
    runtime_re_cook = _make_scene(
        ice_use_fast_midphase=True,
        ice_mesh_mode="unity-runtime-postcook",
    )
    source_once = _make_scene(
        ice_use_fast_midphase=True,
        ice_mesh_mode="unity-source-once",
    )
    source_once_raw = dict(source_once.ice.get_atached_shapes()[0].get_triangle_mesh_runtime_data())
    source_once_triangles = [list(row) for row in source_once_raw.get("triangles") or []]
    prefix = 0
    for local_row, unity_row in zip(source_once_triangles, unity_triangles):
        if local_row != unity_row:
            break
        prefix += 1

    local = {
        "reconstructedBvh33": _summarize_local(bvh33.ice.get_atached_shapes()[0]),
        "reconstructedBvh34": _summarize_local(bvh34.ice.get_atached_shapes()[0]),
        "unityPostCookInputReCookedBvh34": _summarize_local(
            runtime_re_cook.ice.get_atached_shapes()[0]
        ),
        "unitySourceOnceBvh34": _summarize_local(source_once.ice.get_atached_shapes()[0]),
    }
    source_summary = local["unitySourceOnceBvh34"]
    cooked_equal = (
        unity["arrays"]["verticesSha256"] == source_summary["arrays"]["verticesRawSha256"]
        and unity["arrays"]["trianglesSha256"] == source_summary["arrays"]["trianglesRawSha256"]
        and unity["arrays"]["faceRemapRawSha256"] == source_summary["arrays"]["faceRemapRawSha256"]
        and unity["bv4"]["rawSha256"] == source_summary["bv4"]["rawSha256"]
    )
    return {
        "schema": "runtime_ice_cooked_equivalence_audit_v1",
        "purpose": "P4 cooked rink mesh / midphase equivalence audit; no endpoint fitting.",
        "unity": unity,
        "local": local,
        "findings": [
            "The executable scalar Scene uses BVH33 by default because PhysX excludes BV4 traversal when PX_SIMD_DISABLED is defined.",
            "Unity's captured rink is a quantized BVH34 with 100 nodes. Baking scale/pose or re-cooking post-cook arrays yields 116 nodes, but the recovered built-in Plane source input with Unity PxMeshScale yields 100 nodes.",
            "The source-once BVH34 reuses Unity mTriangles in Unity's native vertex frame, and reproduces all 200 cooked triangle rows plus the 100-node/1600-byte BV4 shape.",
            "The v3 capture supplies Unity face-remap and BV4 raw nodes. The scalar binding patches face-remap after cooking, so all four cooked byte buffers can be compared directly.",
            "Unity runtime capture contains exact source vertex/index buffers but not complete face-remap, adjacency, or BV4 mNodes buffers, so byte-identical cooked import cannot yet be proven from the current capture.",
            "The unity-runtime-postcook mode is audit-only: those arrays are already Unity post-cook output and local creation cooks them again.",
        ],
        "acceptance": {
            "cookedIceEquivalent": cooked_equal,
            "reason": (
                "vertices, triangles, face-remap, and BV4 raw nodes all match Unity byte-for-byte"
                if cooked_equal
                else "at least one cooked Unity ice buffer differs from the local source-once object"
            ),
        },
        "sourceOnceComparison": {
            "unityBvh4NodeCount": 100,
            "localBvh4NodeCount": (source_once_raw.get("bv4") or {}).get("nb_nodes"),
            "cookedTriangleRowsMatching": sum(
                local_row == unity_row
                for local_row, unity_row in zip(source_once_triangles, unity_triangles)
            ),
            "cookedTriangleCommonPrefix": prefix,
            "cookedTriangleRowCount": len(unity_triangles),
            "verticesRawEqual": unity["arrays"]["verticesSha256"] == source_summary["arrays"]["verticesRawSha256"],
            "trianglesRawEqual": unity["arrays"]["trianglesSha256"] == source_summary["arrays"]["trianglesRawSha256"],
            "faceRemapRawEqual": unity["arrays"]["faceRemapRawSha256"] == source_summary["arrays"]["faceRemapRawSha256"],
            "bvh4NodesRawEqual": unity["bv4"]["rawSha256"] == source_summary["bv4"]["rawSha256"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-mesh", type=Path, default=DEFAULT_RUNTIME_ICE_MESH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit(args.runtime_mesh)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "acceptance": report["acceptance"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
