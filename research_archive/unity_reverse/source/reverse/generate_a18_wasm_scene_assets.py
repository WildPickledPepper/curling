#!/usr/bin/env python3
"""Generate a C++ header from already-captured Unity geometry assets.

This is a mechanical export only: it neither cooks geometry nor contacts Unity.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STONE = Path(r"D:\esp\tmp\curling_reverse_il2cpp\stone_extendedcollider_mesh_256.json")
ICE = ROOT / "data/calibration/unity_runtime_ice_triangle_mesh_20260710_213035_v3.json"
OUTPUT = ROOT / "tools/reverse/a18_wasm_scene_assets.generated.h"
RUNTIME_HULL_EVENTS = ROOT / "log/unity_runtime_probe_20260709_171257/events.jsonl"
RUNTIME_HULL_LINE = 221
RELEASE_TRACE_EVENTS = (
    ROOT / "log/20260711_a2_static_first_diff_inputs/"
    "unity_runtime_probe_20260711_232310/events.jsonl"
)


def floats(rows: list[list[float]]) -> str:
    def literal(value: float) -> str:
        text = f"{float(value):.9g}"
        if "." not in text and "e" not in text.lower():
            text += ".0"
        return text + "f"

    return ",\n    ".join(
        "{" + ", ".join(literal(value) for value in row) + "}" for row in rows
    )


def ints(rows: list[list[int]]) -> str:
    return ",\n    ".join("{" + ", ".join(str(int(value)) for value in row) + "}" for row in rows)


def bytes_literal(values: list[int]) -> str:
    return ",\n    ".join(
        ", ".join(str(int(value) & 0xFF) for value in values[offset : offset + 16])
        for offset in range(0, len(values), 16)
    )


def runtime_features() -> tuple[list[int], dict[str, list[int]]]:
    # Reuse the production audit's deterministic native-Y-up rebuild path.
    sys.path.insert(0, str(ROOT))
    from tools.reverse.probe_physx_collision_alignment import _runtime_hull_source_from_bundle
    from tools.reverse.probe_unity_runtime_hull_patch_contacts import (
        _load_unity_runtime_feature_bundle,
    )
    from tools.reverse.rebuild_bigconvex_from_runtime_hull import _rebuild_from_runtime_hull

    bundle = _load_unity_runtime_feature_bundle(RUNTIME_HULL_EVENTS, RUNTIME_HULL_LINE)
    hull = [int(value) & 0xFF for value in bundle["hull_raw_bytes"]]
    source = _runtime_hull_source_from_bundle(hull, bundle)
    source["raw"] = bytes(hull)
    rebuilt = _rebuild_from_runtime_hull(source, 16)["big_convex"]
    return hull, {
        "samples": [int(value) & 0xFF for value in rebuilt["samples_raw_bytes"]],
        "valencies": [int(value) & 0xFF for value in rebuilt["valencies_raw_bytes"]],
        "adjacent": [int(value) & 0xFF for value in rebuilt["adjacent_vertices_raw_bytes"]],
    }


def release_trace() -> list[list[float]]:
    for line in RELEASE_TRACE_EVENTS.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") != "a0.angular_write.last_pre_pcm":
            continue
        rows = event.get("data", {}).get("a2StaticTrace")
        if not isinstance(rows, list):
            continue
        output = []
        for row in rows:
            linear = row["linearSetter"]
            output.append([
                float(linear[0]), float(linear[1]), float(linear[2]), float(row["setterWy"]),
                *(float(value) for value in row["p"]),
                *(float(value) for value in row["q"]),
                *(float(value) for value in row["w"]),
            ])
        if len(output) != 1560:
            raise ValueError(f"unexpected controlled 14000 trace length: {len(output)}")
        return output
    raise ValueError("controlled 14000 A2 release trace is missing")


def main() -> int:
    stone = json.loads(STONE.read_text(encoding="utf-8"))
    ice_doc = json.loads(ICE.read_text(encoding="utf-8"))
    mesh = next(item["decodedMesh"] for item in ice_doc["captures"] if "decodedMesh" in item)
    stone_vertices = stone["vertices"]
    ice_vertices = mesh["vertices"]
    ice_triangles = mesh["triangles"]
    runtime_hull, runtime_big_convex = runtime_features()
    trace = release_trace()
    if len(stone_vertices) != 512 or len(ice_vertices) != 121 or len(ice_triangles) != 200:
        raise ValueError("captured geometry cardinality changed")
    if len(runtime_hull) != 4008:
        raise ValueError(f"unexpected Unity runtime hull byte count: {len(runtime_hull)}")
    OUTPUT.write_text(
        "// Generated from existing Unity capture assets. Do not edit manually.\n"
        "#pragma once\n"
        "#include <cstdint>\n\n"
        "struct A18Vec3 { float x, y, z; };\n"
        "struct A18Tri { uint32_t a, b, c; };\n\n"
        "struct A18ReleaseTrace { float vx, vy, vz, wy, px, py, pz, qx, qy, qz, qw, wx, wyPost, wz; };\n\n"
        f"static const A18Vec3 kA18StoneVertices[{len(stone_vertices)}] = {{\n    {floats(stone_vertices)}\n}};\n\n"
        f"static const A18Vec3 kA18IceVertices[{len(ice_vertices)}] = {{\n    {floats(ice_vertices)}\n}};\n\n"
        f"static const A18Tri kA18IceTriangles[{len(ice_triangles)}] = {{\n    {ints(ice_triangles)}\n}};\n"
        f"\nstatic const uint8_t kA18RuntimeHull[{len(runtime_hull)}] = {{\n    {bytes_literal(runtime_hull)}\n}};\n\n"
        f"static const uint8_t kA18BigConvexSamples[{len(runtime_big_convex['samples'])}] = {{\n    {bytes_literal(runtime_big_convex['samples'])}\n}};\n\n"
        f"static const uint8_t kA18BigConvexValencies[{len(runtime_big_convex['valencies'])}] = {{\n    {bytes_literal(runtime_big_convex['valencies'])}\n}};\n\n"
        f"static const uint8_t kA18BigConvexAdjacent[{len(runtime_big_convex['adjacent'])}] = {{\n    {bytes_literal(runtime_big_convex['adjacent'])}\n}};\n"
        f"\nstatic const A18ReleaseTrace kA18ReleaseTrace[{len(trace)}] = {{\n    {floats(trace)}\n}};\n",
        encoding="ascii",
    )
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
