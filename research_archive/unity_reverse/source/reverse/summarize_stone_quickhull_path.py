#!/usr/bin/env python3
"""Summarize why the recovered stone mesh should trigger PhysX cropped QuickHull."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


DEFAULT_MESH = Path(r"D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json")
UNITY_VERTEX_LIMIT = 255


def _load_vertices(path: Path) -> list[tuple[float, float, float]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [tuple(map(float, vertex)) for vertex in data["vertices"]]


def _unique_vertices(vertices: list[tuple[float, float, float]], ndigits: int = 10) -> list[tuple[float, float, float]]:
    seen: dict[tuple[float, float, float], tuple[float, float, float]] = {}
    for vertex in vertices:
        key = tuple(round(value, ndigits) for value in vertex)
        seen.setdefault(key, vertex)
    return list(seen.values())


def _support_extreme_count(vertices: list[tuple[float, float, float]]) -> int:
    """Count vertices that are unique supports for a direction near their radial angle.

    The stone mesh is a two-ring prism.  A direction (radial_x, +/-eps, radial_z)
    distinguishes top and bottom points, while the radial component distinguishes
    the angular sample on the polygon.
    """

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
        if winners == 1 and abs((vx * dx + vy * dy + vz * dz) - best) <= tolerance:
            extreme += 1
    return extreme


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh", type=Path, default=DEFAULT_MESH)
    parser.add_argument("--vertex-limit", type=int, default=UNITY_VERTEX_LIMIT)
    args = parser.parse_args()

    vertices = _load_vertices(args.mesh)
    unique = _unique_vertices(vertices)
    y_levels = sorted({round(vertex[1], 10) for vertex in unique})
    radii = [math.hypot(vertex[0], vertex[2]) for vertex in unique]
    extreme_count = _support_extreme_count(unique)

    print("Recovered stone ExtendedColliders3D mesh:")
    print(f"- mesh: {args.mesh}")
    print(f"- raw vertices: {len(vertices)}")
    print(f"- unique vertices: {len(unique)}")
    print(f"- y levels: {y_levels}")
    print(f"- radius range: {min(radii):.12g} .. {max(radii):.12g}")
    print(f"- support-extreme vertices: {extreme_count}")
    print(f"- Unity/PhysX PxConvexMeshDesc.vertexLimit: {args.vertex_limit}")
    print()
    print("Static path implication:")
    if extreme_count > args.vertex_limit:
        print(
            "- The recovered two-ring 256-sided prism has more extreme vertices than "
            "the PhysX vertex limit."
        )
        print(
            "- With Unity flags eCOMPUTE_CONVEX only, no eQUANTIZE_INPUT and no "
            "eGPU_COMPATIBLE, QuickHull must reduce this hull before cooking can "
            "satisfy desc.points.count < 256."
        )
        print(
            "- In PhysX 4.1 / Unity wasm this reduction is the non-plane-shifting "
            "OBB cropped hull path: createConvexHull -> expandHullOBB -> "
            "mCropedConvexHull -> fillConvexMeshDescFromCroppedHull."
        )
    else:
        print("- This mesh does not force the cropped path by vertex count alone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
