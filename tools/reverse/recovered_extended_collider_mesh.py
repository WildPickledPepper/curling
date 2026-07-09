#!/usr/bin/env python3
"""Recover ExtendedColliders3D mesh generation for the curling stone cylinder."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path


Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class CylinderMesh:
    vertices: list[Vector3]
    triangles: list[int]

    @property
    def triangle_count(self) -> int:
        return len(self.triangles) // 3


def _triangulate_cap(indices: list[int], top: bool) -> list[int]:
    remaining = list(indices)
    center = len(remaining) >> 1
    toggle = 0
    triangles: list[int] = []

    while len(remaining) >= 3:
        prev_index = remaining[(center - 1 + len(remaining)) % len(remaining)]
        center_index = remaining[center]
        next_index = remaining[(center + 1) % len(remaining)]
        if top:
            triangles.extend([prev_index, center_index, next_index])
        else:
            triangles.extend([prev_index, next_index, center_index])

        old_prev = center - 1
        del remaining[center]
        if len(remaining) <= 2:
            break
        if toggle & 1:
            center = (len(remaining) + old_prev) % len(remaining)
        toggle ^= 1

    return triangles


def _flip_triangles(triangles: list[int]) -> None:
    for index in range(0, len(triangles), 3):
        triangles[index], triangles[index + 1] = triangles[index + 1], triangles[index]


def generate_cylinder_mesh(
    *,
    faces: int = 256,
    cap_top: bool = True,
    cap_bottom: bool = True,
    taper_top: tuple[float, float] = (1.0, 1.0),
    taper_bottom: tuple[float, float] = (1.0, 1.0),
    size: Vector3 = (2.5, 2.0, 2.5),
    centre: Vector3 = (0.0, 0.0, 0.0),
    flip_faces: bool = True,
) -> CylinderMesh:
    """Generate the same local cylinder mesh as ExtendedColliders3D for stones."""

    vertices: list[Vector3] = []
    for index in range(faces):
        angle = (index / faces) * math.pi * 2.0
        x = math.cos(angle) * 0.5
        z = math.sin(angle) * 0.5
        vertices.append(
            (
                centre[0] + x * taper_top[0] * size[0],
                centre[1] + 0.5 * size[1],
                centre[2] + z * taper_top[1] * size[2],
            )
        )
        vertices.append(
            (
                centre[0] + x * taper_bottom[0] * size[0],
                centre[1] - 0.5 * size[1],
                centre[2] + z * taper_bottom[1] * size[2],
            )
        )

    # The wasm stores the first ring contiguously, then the second ring.
    ordered_vertices = vertices[0::2] + vertices[1::2]

    triangles: list[int] = []
    for index in range(faces):
        top = index
        bottom = index + faces
        next_top = 0 if index + 1 == faces else index + 1
        next_bottom = faces if index + 1 == faces else faces + index + 1
        triangles.extend([top, bottom, next_top, next_top, bottom, next_bottom])

    if cap_top:
        triangles.extend(_triangulate_cap(list(range(faces)), top=True))
    if cap_bottom:
        triangles.extend(_triangulate_cap(list(range(faces, faces * 2)), top=False))

    if flip_faces:
        _flip_triangles(triangles)

    return CylinderMesh(vertices=ordered_vertices, triangles=triangles)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--faces", type=int, default=256)
    parser.add_argument("--no-top-cap", action="store_true")
    parser.add_argument("--no-bottom-cap", action="store_true")
    parser.add_argument("--no-flip-faces", action="store_true")
    parser.add_argument("--json", type=Path, help="Optional path to write vertices/triangles.")
    args = parser.parse_args()

    mesh = generate_cylinder_mesh(
        faces=args.faces,
        cap_top=not args.no_top_cap,
        cap_bottom=not args.no_bottom_cap,
        flip_faces=not args.no_flip_faces,
    )

    print(f"vertices={len(mesh.vertices)}")
    print(f"indices={len(mesh.triangles)}")
    print(f"triangles={mesh.triangle_count}")
    print(f"first_vertices={mesh.vertices[:4]}")
    print(f"first_triangles={mesh.triangles[:18]}")
    print(f"last_triangles={mesh.triangles[-18:]}")

    if args.json:
        args.json.write_text(
            json.dumps({"vertices": mesh.vertices, "triangles": mesh.triangles}, indent=2),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
