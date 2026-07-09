#!/usr/bin/env python3
"""Dump pyphysx cooked convex hull triangles for the recovered stone mesh.

This is an offline reverse-engineering helper.  The default flags match the
Unity MeshCollider convex path recovered from wasm: eCOMPUTE_CONVEX only,
without eQUANTIZE_INPUT or eGPU_COMPATIBLE.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import numpy as np


Vector3 = Tuple[float, float, float]


def _round_vec(vec: Sequence[float], decimals: int) -> Vector3:
    return tuple(round(float(value), decimals) for value in vec)  # type: ignore[return-value]


def _load_points(path: Path) -> List[Vector3]:
    data = json.loads(path.read_text(encoding="utf-8"))
    points = data["vertices"]
    return [tuple(float(coord) for coord in point) for point in points]  # type: ignore[list-item]


def _radial_stats(points: np.ndarray) -> Dict[str, float]:
    radial = np.sqrt(points[:, 0] * points[:, 0] + points[:, 2] * points[:, 2])
    return {
        "min": float(radial.min()),
        "max": float(radial.max()),
        "mean": float(radial.mean()),
    }


def _scaled(points: np.ndarray, scale: Vector3) -> np.ndarray:
    scale_array = np.array(scale, dtype=np.float32)
    return points * scale_array


def _unique_vertices(triangles: np.ndarray, decimals: int) -> Tuple[List[Vector3], List[List[int]]]:
    mapping: Dict[Vector3, int] = {}
    vertices: List[Vector3] = []
    triangle_indices: List[List[int]] = []

    for triangle in triangles:
        indices: List[int] = []
        for vertex in triangle:
            key = _round_vec(vertex, decimals)
            index = mapping.get(key)
            if index is None:
                index = len(vertices)
                mapping[key] = index
                vertices.append(key)
            indices.append(index)
        triangle_indices.append(indices)

    return vertices, triangle_indices


def _summarize_triangles(
    raw_triangles: np.ndarray,
    *,
    decimals: int,
    world_scale: Vector3,
) -> Dict[str, Any]:
    flat = raw_triangles.reshape(-1, 3)
    unique_vertices, triangle_indices = _unique_vertices(raw_triangles, decimals)
    unique_array = np.array(unique_vertices, dtype=np.float32)
    scaled_unique = _scaled(unique_array, world_scale)

    y_values = np.unique(np.round(unique_array[:, 1], decimals=decimals))
    y_mid = float((unique_array[:, 1].min() + unique_array[:, 1].max()) * 0.5)
    top_count = int(np.count_nonzero(unique_array[:, 1] > y_mid))
    bottom_count = int(np.count_nonzero(unique_array[:, 1] <= y_mid))

    return {
        "triangle_count": int(raw_triangles.shape[0]),
        "unique_vertex_count": len(unique_vertices),
        "top_unique_vertex_count": top_count,
        "bottom_unique_vertex_count": bottom_count,
        "local_bounds": {
            "min": [float(value) for value in flat.min(axis=0)],
            "max": [float(value) for value in flat.max(axis=0)],
        },
        "local_radial_stats_xz": _radial_stats(unique_array),
        "world_scale": list(world_scale),
        "world_bounds": {
            "min": [float(value) for value in _scaled(flat, world_scale).min(axis=0)],
            "max": [float(value) for value in _scaled(flat, world_scale).max(axis=0)],
        },
        "world_radial_stats_xz": _radial_stats(scaled_unique),
        "unique_y_values": [float(value) for value in y_values],
        "unique_vertices": [list(vertex) for vertex in unique_vertices],
        "triangles": triangle_indices,
    }


def _variant_name(quantized_count: int, vertex_limit: int, *, quantize_input: bool, gpu_compatible: bool) -> str:
    qi = 1 if quantize_input else 0
    gpu = 1 if gpu_compatible else 0
    return f"q{quantized_count}_v{vertex_limit}_qi{qi}_gpu{gpu}"


def _probe_variant(
    pyphysx_module: Any,
    points: List[Vector3],
    *,
    quantized_count: int,
    vertex_limit: int,
    quantize_input: bool,
    gpu_compatible: bool,
    decimals: int,
    world_scale: Vector3,
    include_geometry: bool,
    include_raw_convex_data: bool = False,
) -> Dict[str, Any]:
    material = pyphysx_module.Material()
    create_shape = pyphysx_module.Shape.create_convex_mesh_from_points
    try:
        shape = create_shape(
            points,
            material,
            True,
            1.0,
            quantized_count,
            vertex_limit,
            quantize_input,
            gpu_compatible,
        )
        binding_flag_support = True
    except TypeError as exc:
        binding_flag_support = False
        if not (quantize_input and gpu_compatible):
            raise RuntimeError(
                "Installed pyphysx binding does not expose quantize_input/gpu_compatible. "
                "It can only reproduce the binding default flags true/true, not Unity's "
                "recovered false/false convex cooking path."
            ) from None
        shape = create_shape(
            points,
            material,
            True,
            1.0,
            quantized_count,
            vertex_limit,
        )
    shape_data = shape.get_shape_data()
    raw_triangles = np.asarray(shape_data, dtype=np.float32).reshape(-1, 3, 3)
    summary = _summarize_triangles(raw_triangles, decimals=decimals, world_scale=world_scale)
    summary["quantized_count"] = quantized_count
    summary["vertex_limit"] = vertex_limit
    summary["quantize_input"] = quantize_input
    summary["gpu_compatible"] = gpu_compatible
    summary["binding_flag_support"] = binding_flag_support
    summary["shape_data_shape"] = list(shape_data.shape)
    summary["geometry_type"] = str(shape.get_geometry_type())

    if include_raw_convex_data:
        get_raw = getattr(shape, "get_convex_mesh_data", None)
        if get_raw is None:
            summary["raw_convex_mesh_data_error"] = "installed pyphysx Shape has no get_convex_mesh_data()"
        else:
            summary["raw_convex_mesh_data"] = get_raw()

    if not include_geometry:
        summary.pop("unique_vertices")
        summary.pop("triangles")

    return summary


def _parse_ints(values: Iterable[str]) -> List[int]:
    parsed: List[int] = []
    for value in values:
        parsed.extend(int(item) for item in value.split(",") if item)
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(r"D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json"),
        help="Recovered ExtendedColliders3D mesh JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/calibration/pyphysx_cooked_stone_hull_probe_20260708.json"),
    )
    parser.add_argument("--quantized-count", action="append", default=["16,32,64,128,255,512,1024,65535"])
    parser.add_argument("--vertex-limit", action="append", default=["8,16,32,64,128,255,256"])
    parser.add_argument("--detail-quantized-count", type=int, default=255)
    parser.add_argument("--detail-vertex-limit", type=int, default=255)
    parser.add_argument("--round-decimals", type=int, default=6)
    parser.add_argument(
        "--quantize-input",
        action="store_true",
        help="Enable PxConvexFlag::eQUANTIZE_INPUT. Unity's recovered path leaves this off.",
    )
    parser.add_argument(
        "--gpu-compatible",
        action="store_true",
        help="Enable PxConvexFlag::eGPU_COMPATIBLE. Unity's recovered path leaves this off.",
    )
    parser.add_argument(
        "--include-binding-default-control",
        action="store_true",
        help="Also dump one q255/v255 control using pyphysx binding defaults: quantize_input/gpu_compatible on.",
    )
    parser.add_argument(
        "--include-raw-convex-data",
        action="store_true",
        help="Include PhysX PxConvexMesh vertices, polygons, index buffer, bounds, and mass/inertia for the detail variant.",
    )
    parser.add_argument("--world-scale-x", type=float, default=0.1127)
    parser.add_argument("--world-scale-y", type=float, default=0.115)
    parser.add_argument("--world-scale-z", type=float, default=0.1127)
    args = parser.parse_args()

    try:
        import pyphysx  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "pyphysx is required. Use D:\\esp\\tmp\\curling_pyphysx_conda\\python.exe to run this tool."
        ) from exc

    points = _load_points(args.input)
    quantized_counts = _parse_ints(args.quantized_count)
    vertex_limits = _parse_ints(args.vertex_limit)
    world_scale = (args.world_scale_x, args.world_scale_y, args.world_scale_z)

    variants: Dict[str, Any] = {}
    for vertex_limit in vertex_limits:
        name = _variant_name(
            args.detail_quantized_count,
            vertex_limit,
            quantize_input=args.quantize_input,
            gpu_compatible=args.gpu_compatible,
        )
        variants[name] = _probe_variant(
            pyphysx,
            points,
            quantized_count=args.detail_quantized_count,
            vertex_limit=vertex_limit,
            quantize_input=args.quantize_input,
            gpu_compatible=args.gpu_compatible,
            decimals=args.round_decimals,
            world_scale=world_scale,
            include_geometry=False,
        )

    for quantized_count in quantized_counts:
        name = _variant_name(
            quantized_count,
            args.detail_vertex_limit,
            quantize_input=args.quantize_input,
            gpu_compatible=args.gpu_compatible,
        )
        variants[name] = _probe_variant(
            pyphysx,
            points,
            quantized_count=quantized_count,
            vertex_limit=args.detail_vertex_limit,
            quantize_input=args.quantize_input,
            gpu_compatible=args.gpu_compatible,
            decimals=args.round_decimals,
            world_scale=world_scale,
            include_geometry=False,
        )

    if args.include_binding_default_control and not (args.quantize_input and args.gpu_compatible):
        control_name = _variant_name(
            args.detail_quantized_count,
            args.detail_vertex_limit,
            quantize_input=True,
            gpu_compatible=True,
        )
        variants[control_name] = _probe_variant(
            pyphysx,
            points,
            quantized_count=args.detail_quantized_count,
            vertex_limit=args.detail_vertex_limit,
            quantize_input=True,
            gpu_compatible=True,
            decimals=args.round_decimals,
            world_scale=world_scale,
            include_geometry=False,
        )

    detail_name = _variant_name(
        args.detail_quantized_count,
        args.detail_vertex_limit,
        quantize_input=args.quantize_input,
        gpu_compatible=args.gpu_compatible,
    )
    detail = _probe_variant(
        pyphysx,
        points,
        quantized_count=args.detail_quantized_count,
        vertex_limit=args.detail_vertex_limit,
        quantize_input=args.quantize_input,
        gpu_compatible=args.gpu_compatible,
        decimals=args.round_decimals,
        world_scale=world_scale,
        include_geometry=True,
        include_raw_convex_data=args.include_raw_convex_data,
    )

    binding_note = (
        "This pyphysx binding exposes quantize_input/gpu_compatible; runs marked qi0/gpu0 "
        "can exercise Unity's recovered convex cooking flags."
        if detail["binding_flag_support"]
        else (
            "The installed pyphysx binding does not expose quantize_input/gpu_compatible; "
            "requests for false/false fail before cooking. Runs marked qi1/gpu1 are the "
            "binding default/control path and are not Unity's recovered wasm flags."
        )
    )

    report = {
        "tool": "tools/reverse/dump_pyphysx_cooked_convex_hull.py",
        "input": str(args.input),
        "input_vertex_count": len(points),
        "input_local_radial_stats_xz": _radial_stats(np.array(points, dtype=np.float32)),
        "unity_recovered_flags": {
            "compute_convex": True,
            "quantize_input": False,
            "gpu_compatible": False,
            "vertex_limit": 255,
            "quantized_count": 255,
        },
        "selected_flags": {
            "quantize_input": args.quantize_input,
            "gpu_compatible": args.gpu_compatible,
        },
        "binding_note": binding_note,
        "variants": variants,
        "detailed_variant": detail_name,
        "detail": detail,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"wrote {args.output}")
    print(
        "detail %s: %d unique vertices, %d triangles"
        % (detail_name, detail["unique_vertex_count"], detail["triangle_count"])
    )
    print(
        "world radial mean %.6f m"
        % detail["world_radial_stats_xz"]["mean"]
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
