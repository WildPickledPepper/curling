"""Print PhysX 4.1 convex-hull layouts for Unity WebGL/wasm.

Unity's WebGL build is a 32-bit target, so pointers in the native PhysX data
structures are 4 bytes.  This script mirrors the relevant structures with
``ctypes`` using 32-bit pointer placeholders, then prints offsets that can be
checked against decompiled wasm such as ``func72915`` and ``func72927``.
"""

from __future__ import annotations

import argparse
import ctypes
import json
from dataclasses import dataclass
from typing import Iterable


class PxVec3(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
    ]


class PxMat33(ctypes.Structure):
    _fields_ = [
        ("column0", PxVec3),
        ("column1", PxVec3),
        ("column2", PxVec3),
    ]


class PxPlane(ctypes.Structure):
    _fields_ = [
        ("nx", ctypes.c_float),
        ("ny", ctypes.c_float),
        ("nz", ctypes.c_float),
        ("d", ctypes.c_float),
    ]


class PxStridedData32(ctypes.Structure):
    _fields_ = [
        ("stride", ctypes.c_uint32),
        ("data", ctypes.c_uint32),
    ]


class PxBoundedData32(ctypes.Structure):
    _fields_ = [
        ("stride", ctypes.c_uint32),
        ("data", ctypes.c_uint32),
        ("count", ctypes.c_uint32),
    ]


class PxConvexMeshDesc32(ctypes.Structure):
    _fields_ = [
        ("points", PxBoundedData32),
        ("polygons", PxBoundedData32),
        ("indices", PxBoundedData32),
        ("flags", ctypes.c_uint16),
        ("vertexLimit", ctypes.c_uint16),
        ("quantizedCount", ctypes.c_uint16),
    ]


class PxHullPolygon(ctypes.Structure):
    _fields_ = [
        ("mPlane0", ctypes.c_float),
        ("mPlane1", ctypes.c_float),
        ("mPlane2", ctypes.c_float),
        ("mPlane3", ctypes.c_float),
        ("mNbVerts", ctypes.c_uint16),
        ("mIndexBase", ctypes.c_uint16),
    ]


class HullPolygonData(ctypes.Structure):
    _fields_ = [
        ("plane", PxPlane),
        ("mVRef8", ctypes.c_uint16),
        ("mNbVerts", ctypes.c_uint8),
        ("mMinIndex", ctypes.c_uint8),
    ]


class InternalObjectsData(ctypes.Structure):
    _fields_ = [
        ("mRadius", ctypes.c_float),
        ("mExtents0", ctypes.c_float),
        ("mExtents1", ctypes.c_float),
        ("mExtents2", ctypes.c_float),
    ]


class CenterExtents(ctypes.Structure):
    _fields_ = [
        ("mCenter", PxVec3),
        ("mExtents", PxVec3),
    ]


class ConvexHullData32(ctypes.Structure):
    _fields_ = [
        ("mAABB", CenterExtents),
        ("mCenterOfMass", PxVec3),
        ("mNbEdges", ctypes.c_uint16),
        ("mNbHullVertices", ctypes.c_uint8),
        ("mNbPolygons", ctypes.c_uint8),
        ("mPolygons", ctypes.c_uint32),
        ("mBigConvexRawData", ctypes.c_uint32),
        ("mInternal", InternalObjectsData),
    ]


class ConvexHullBuilder32(ctypes.Structure):
    _fields_ = [
        ("mHullDataHullVertices", ctypes.c_uint32),
        ("mHullDataPolygons", ctypes.c_uint32),
        ("mHullDataVertexData8", ctypes.c_uint32),
        ("mHullDataFacesByEdges8", ctypes.c_uint32),
        ("mHullDataFacesByVertices8", ctypes.c_uint32),
        ("mEdgeData16", ctypes.c_uint32),
        ("mEdges", ctypes.c_uint32),
        ("mHull", ctypes.c_uint32),
        ("mBuildGRBData", ctypes.c_uint8),
    ]


class ConvexPolygonsBuilder32(ctypes.Structure):
    _fields_ = [
        ("base", ConvexHullBuilder32),
        ("mNbHullFaces", ctypes.c_uint32),
        ("mFaces", ctypes.c_uint32),
    ]


class ConvexMeshBuilder32(ctypes.Structure):
    _fields_ = [
        ("hullBuilder", ConvexPolygonsBuilder32),
        ("mHullData", ConvexHullData32),
        ("mBigConvexData", ctypes.c_uint32),
        ("mMass", ctypes.c_float),
        ("mInertia", PxMat33),
    ]


class ConvexHullInitData32(ctypes.Structure):
    _fields_ = [
        ("mHullData", ConvexHullData32),
        ("mNb", ctypes.c_uint32),
        ("mMass", ctypes.c_float),
        ("mInertia", PxMat33),
        ("mBigConvexData", ctypes.c_uint32),
    ]


class Valency(ctypes.Structure):
    _fields_ = [
        ("mCount", ctypes.c_uint16),
        ("mOffset", ctypes.c_uint16),
    ]


class BigConvexRawData32(ctypes.Structure):
    _fields_ = [
        ("mSubdiv", ctypes.c_uint16),
        ("mNbSamples", ctypes.c_uint16),
        ("mSamples", ctypes.c_uint32),
        ("mNbVerts", ctypes.c_uint32),
        ("mNbAdjVerts", ctypes.c_uint32),
        ("mValencies", ctypes.c_uint32),
        ("mAdjacentVerts", ctypes.c_uint32),
    ]


@dataclass(frozen=True)
class FieldOffset:
    name: str
    offset: int
    size: int


def field_offsets(struct_type: type[ctypes.Structure]) -> list[FieldOffset]:
    rows: list[FieldOffset] = []
    for name, _ctype in struct_type._fields_:  # type: ignore[attr-defined]
        descriptor = getattr(struct_type, name)
        rows.append(FieldOffset(name, int(descriptor.offset), int(descriptor.size)))
    return rows


def nested_offsets() -> dict[str, int]:
    return {
        "PxConvexMeshDesc32.points.stride": PxConvexMeshDesc32.points.offset
        + PxBoundedData32.stride.offset,
        "PxConvexMeshDesc32.points.data": PxConvexMeshDesc32.points.offset
        + PxBoundedData32.data.offset,
        "PxConvexMeshDesc32.points.count": PxConvexMeshDesc32.points.offset
        + PxBoundedData32.count.offset,
        "PxConvexMeshDesc32.polygons.stride": PxConvexMeshDesc32.polygons.offset
        + PxBoundedData32.stride.offset,
        "PxConvexMeshDesc32.polygons.data": PxConvexMeshDesc32.polygons.offset
        + PxBoundedData32.data.offset,
        "PxConvexMeshDesc32.polygons.count": PxConvexMeshDesc32.polygons.offset
        + PxBoundedData32.count.offset,
        "PxConvexMeshDesc32.indices.stride": PxConvexMeshDesc32.indices.offset
        + PxBoundedData32.stride.offset,
        "PxConvexMeshDesc32.indices.data": PxConvexMeshDesc32.indices.offset
        + PxBoundedData32.data.offset,
        "PxConvexMeshDesc32.indices.count": PxConvexMeshDesc32.indices.offset
        + PxBoundedData32.count.offset,
        "PxHullPolygon.mPlane": PxHullPolygon.mPlane0.offset,
        "PxHullPolygon.mNbVerts": PxHullPolygon.mNbVerts.offset,
        "PxHullPolygon.mIndexBase": PxHullPolygon.mIndexBase.offset,
        "ConvexHullData32.mNbEdges": ConvexHullData32.mNbEdges.offset,
        "ConvexHullData32.mNbHullVertices": ConvexHullData32.mNbHullVertices.offset,
        "ConvexHullData32.mNbPolygons": ConvexHullData32.mNbPolygons.offset,
        "ConvexHullBuilder32.mHull": ConvexHullBuilder32.mHull.offset,
        "ConvexHullBuilder32.mBuildGRBData": ConvexHullBuilder32.mBuildGRBData.offset,
        "ConvexPolygonsBuilder32.mNbHullFaces": ConvexPolygonsBuilder32.mNbHullFaces.offset,
        "ConvexPolygonsBuilder32.mFaces": ConvexPolygonsBuilder32.mFaces.offset,
        "ConvexMeshBuilder32.mHullData": ConvexMeshBuilder32.mHullData.offset,
        "ConvexMeshBuilder32.mBigConvexData": ConvexMeshBuilder32.mBigConvexData.offset,
        "ConvexMeshBuilder32.mMass": ConvexMeshBuilder32.mMass.offset,
        "ConvexMeshBuilder32.mInertia": ConvexMeshBuilder32.mInertia.offset,
        "HullPolygonData.mPlane": HullPolygonData.plane.offset,
        "HullPolygonData.mVRef8": HullPolygonData.mVRef8.offset,
        "HullPolygonData.mNbVerts": HullPolygonData.mNbVerts.offset,
        "HullPolygonData.mMinIndex": HullPolygonData.mMinIndex.offset,
        "BigConvexRawData32.mSubdiv": BigConvexRawData32.mSubdiv.offset,
        "BigConvexRawData32.mNbSamples": BigConvexRawData32.mNbSamples.offset,
        "BigConvexRawData32.mSamples": BigConvexRawData32.mSamples.offset,
        "BigConvexRawData32.mNbVerts": BigConvexRawData32.mNbVerts.offset,
        "BigConvexRawData32.mNbAdjVerts": BigConvexRawData32.mNbAdjVerts.offset,
        "BigConvexRawData32.mValencies": BigConvexRawData32.mValencies.offset,
        "BigConvexRawData32.mAdjacentVerts": BigConvexRawData32.mAdjacentVerts.offset,
    }


def runtime_buffer_layout(
    nb_polygons: int,
    nb_vertices: int,
    nb_edges: int,
    nb_vertex_refs: int,
    has_grb_data: bool,
) -> list[FieldOffset]:
    offset = 0
    rows: list[FieldOffset] = []

    def add(name: str, size: int) -> None:
        nonlocal offset
        rows.append(FieldOffset(name, offset, size))
        offset += size

    add("mPolygons[nbPolygons]", 20 * nb_polygons)
    add("hullVertices[nbHullVertices]", 12 * nb_vertices)
    add("facesByEdges8[nbEdges * 2]", 2 * nb_edges)
    add("facesByVertices8[nbHullVertices * 3]", 3 * nb_vertices)
    if has_grb_data:
        add("verticesByEdges16[nbEdges * 2]", 4 * nb_edges)
    add("vertexData8[sum polygon vertex counts]", nb_vertex_refs)
    return rows


def clhl_stream_layout(
    nb_polygons: int,
    nb_vertices: int,
    nb_edges: int,
    nb_vertex_refs: int,
    has_grb_data: bool,
) -> list[FieldOffset]:
    offset = 0
    rows: list[FieldOffset] = []

    def add(name: str, size: int) -> None:
        nonlocal offset
        rows.append(FieldOffset(name, offset, size))
        offset += size

    add("u32 nbHullVertices", 4)
    add("u32 nbEdgesWithGrbBit", 4)
    add("u32 nbPolygons", 4)
    add("u32 nbVertexRefs", 4)
    add("float hullVertices[nbHullVertices * 3]", 12 * nb_vertices)
    add("HullPolygonData polygons[nbPolygons]", 20 * nb_polygons)
    add("u8 vertexData8[nbVertexRefs]", nb_vertex_refs)
    add("u8 facesByEdges8[nbEdges * 2]", 2 * nb_edges)
    add("u8 facesByVertices8[nbHullVertices * 3]", 3 * nb_vertices)
    if has_grb_data:
        add("u16 verticesByEdges16[nbEdges * 2]", 4 * nb_edges)
    return rows


def cvxm_stream_layout(
    nb_polygons: int,
    nb_vertices: int,
    nb_edges: int,
    nb_vertex_refs: int,
    has_grb_data: bool,
    has_gauss: bool,
    gauss_samples: int,
    gauss_nb_verts: int,
    gauss_adj_verts: int,
    gauss_valency_index_bytes: int,
) -> list[FieldOffset]:
    offset = 0
    rows: list[FieldOffset] = []

    def add(name: str, size: int) -> None:
        nonlocal offset
        rows.append(FieldOffset(name, offset, size))
        offset += size

    add("CVXM chunk header (not counted)", 0)
    add("u32 serialFlags", 4)
    clhl_rows = clhl_stream_layout(nb_polygons, nb_vertices, nb_edges, nb_vertex_refs, has_grb_data)
    clhl_size = 0
    if clhl_rows:
        last = clhl_rows[-1]
        clhl_size = last.offset + last.size
    add("CLHL chunk payload (chunk header not counted)", clhl_size)
    add("float geomEpsilon_or_zero", 4)
    add("float boundsMin[3]", 12)
    add("float boundsMax[3]", 12)
    add("float mass", 4)
    add("float inertia[9]", 36)
    add("float centerOfMass[3]", 12)
    add("float gaussMapFlag", 4)
    if has_gauss:
        add("SUPM/GAUS chunk headers (not counted)", 0)
        add("GAUS: u32 subdiv", 4)
        add("GAUS: u32 nbSamples", 4)
        add("GAUS: u8 samples[nbSamples * 2]", gauss_samples * 2)
        add("VALE chunk header (not counted)", 0)
        add("VALE: u32 nbVerts", 4)
        add("VALE: u32 nbAdjVerts", 4)
        add("VALE: u32 maxValencyCount", 4)
        add(
            f"VALE: compressed valency counts[{gauss_valency_index_bytes} byte each]",
            compressed_index_bytes(gauss_nb_verts, gauss_valency_index_bytes),
        )
        add("VALE: u8 adjacentVerts[nbAdjVerts]", gauss_adj_verts)
    add("float internal.radius", 4)
    add("float internal.extents[3]", 12)
    return rows


def compressed_index_bytes(count: int, index_bytes: int) -> int:
    # StoreIndices chooses 8-bit or 16-bit elements from the maximum index.
    # Valency counts are usually small, but expose the width so this sketch can
    # represent either branch.
    return count * index_bytes


def table(struct_type: type[ctypes.Structure]) -> dict[str, object]:
    return {
        "size": ctypes.sizeof(struct_type),
        "alignment": ctypes.alignment(struct_type),
        "fields": [row.__dict__ for row in field_offsets(struct_type)],
    }


def rows_to_dict(rows: Iterable[FieldOffset]) -> list[dict[str, int | str]]:
    return [row.__dict__ for row in rows]


def build_payload(args: argparse.Namespace) -> dict[str, object]:
    return {
        "target": "Unity WebGL / wasm32 PhysX 4.1",
        "structures": {
            "PxBoundedData32": table(PxBoundedData32),
            "PxConvexMeshDesc32": table(PxConvexMeshDesc32),
            "PxHullPolygon": table(PxHullPolygon),
            "HullPolygonData": table(HullPolygonData),
            "InternalObjectsData": table(InternalObjectsData),
            "CenterExtents": table(CenterExtents),
            "ConvexHullData32": table(ConvexHullData32),
            "ConvexHullBuilder32": table(ConvexHullBuilder32),
            "ConvexPolygonsBuilder32": table(ConvexPolygonsBuilder32),
            "ConvexMeshBuilder32": table(ConvexMeshBuilder32),
            "PxMat33": table(PxMat33),
            "ConvexHullInitData32": table(ConvexHullInitData32),
            "Valency": table(Valency),
            "BigConvexRawData32": table(BigConvexRawData32),
        },
        "nested_offsets": nested_offsets(),
        "runtime_buffer_layout": rows_to_dict(
            runtime_buffer_layout(
                args.polygons,
                args.vertices,
                args.edges,
                args.vertex_refs,
                args.grb,
            )
        ),
        "clhl_stream_layout": rows_to_dict(
            clhl_stream_layout(
                args.polygons,
                args.vertices,
                args.edges,
                args.vertex_refs,
                args.grb,
            )
        ),
        "cvxm_stream_layout": rows_to_dict(
            cvxm_stream_layout(
                args.polygons,
                args.vertices,
                args.edges,
                args.vertex_refs,
                args.grb,
                args.gauss,
                args.gauss_samples,
                args.gauss_nb_verts,
                args.gauss_adj_verts,
                args.gauss_valency_index_bytes,
            )
        ),
        "decompiled_cross_checks": {
            "func72915_b_g_equals_4": "PxConvexMeshDesc.indices.stride, not flags",
            "func72927_a_18_ushort": "ConvexHullData32.mNbEdges at byte offset 36",
            "func72927_a_38_ubyte": "ConvexHullData32.mNbHullVertices at byte offset 38",
            "func72927_a_39_ubyte": "ConvexHullData32.mNbPolygons at byte offset 39",
            "func72927_gaus_header": "BigConvexRawData32 starts with u16 mSubdiv, u16 mNbSamples",
            "func72876_f_ytcd": "ConvexMeshBuilder32.hullBuilder.mHull is initialized to builder + 44",
            "func72927_f_7": "ConvexMeshBuilder32.hullBuilder.mHull pointer at offset 28 points to ConvexMeshBuilder32.mHullData",
            "func72927_f_27": "ConvexMeshBuilder32.mBigConvexData pointer at offset 108",
            "func72927_f_28": "ConvexMeshBuilder32.mMass at offset 112 followed by inertia matrix at offset 116",
            "convex_builder_copy": "ConvexHullInitData32 holds copied hull, vertex-ref count mNb, mass, inertia, and optional BigConvexData pointer",
        },
    }


def print_text(payload: dict[str, object]) -> None:
    print(payload["target"])
    print()
    structures = payload["structures"]
    assert isinstance(structures, dict)
    for name, info in structures.items():
        assert isinstance(info, dict)
        print(f"{name}: size={info['size']} align={info['alignment']}")
        fields = info["fields"]
        assert isinstance(fields, list)
        for row in fields:
            assert isinstance(row, dict)
            print(f"  {row['offset']:>3} +{row['size']:<2} {row['name']}")
        print()

    print("Nested offsets:")
    nested = payload["nested_offsets"]
    assert isinstance(nested, dict)
    for name, offset in nested.items():
        print(f"  {offset:>3} {name}")
    print()

    print("Runtime ConvexHullData extra buffer order:")
    for row in payload["runtime_buffer_layout"]:  # type: ignore[index]
        print(f"  {row['offset']:>4} +{row['size']:<4} {row['name']}")
    print()

    print("CLHL cooked stream order:")
    for row in payload["clhl_stream_layout"]:  # type: ignore[index]
        print(f"  {row['offset']:>4} +{row['size']:<4} {row['name']}")
    print()

    print("CVXM cooked stream order, payload-level sketch:")
    for row in payload["cvxm_stream_layout"]:  # type: ignore[index]
        print(f"  {row['offset']:>4} +{row['size']:<4} {row['name']}")
    print()

    print("Decompiler cross-checks:")
    checks = payload["decompiled_cross_checks"]
    assert isinstance(checks, dict)
    for name, meaning in checks.items():
        print(f"  {name}: {meaning}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=64)
    parser.add_argument("--polygons", type=int, default=124)
    parser.add_argument("--edges", type=int, default=186)
    parser.add_argument("--vertex-refs", type=int, default=372)
    parser.add_argument("--grb", action="store_true", help="Include GRB verticesByEdges16 data.")
    parser.add_argument("--gauss", action="store_true", help="Include a SUPM/GAUS/VALE sketch.")
    parser.add_argument("--gauss-samples", type=int, default=6 * 16 * 16)
    parser.add_argument("--gauss-nb-verts", type=int, default=64)
    parser.add_argument("--gauss-adj-verts", type=int, default=372)
    parser.add_argument("--gauss-valency-index-bytes", type=int, choices=(1, 2), default=1)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = build_payload(args)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
