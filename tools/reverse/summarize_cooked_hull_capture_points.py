#!/usr/bin/env python3
"""Print the wasm capture points for Unity's cooked convex hull data.

This does not decode live memory.  It documents the exact places where a runtime
probe or wasm patch should read memory to get the final Unity cooked hull:

  1. func72915/f_lvcd writes PxConvexMeshDesc points/polygons/indices.
  2. func72926/f_wvcd checks desc.points.count < 256 and builds ConvexMeshBuilder.
  3. func72927/f_xvcd serializes CVXM/CLHL cooked stream.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_DECOMPILE = Path(r"D:\esp\tmp\curling_reverse_il2cpp\build.dcmp")


FUNC_RE = re.compile(r"^function\s+([A-Za-z0-9_]+)\(.*//\s+(func\d+)")


@dataclass(frozen=True)
class FunctionBody:
    marker: str
    symbol: str
    start_line: int
    lines: tuple[str, ...]


def _load_functions(path: Path, markers: Iterable[str]) -> dict[str, FunctionBody]:
    wanted = set(markers)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    headers: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = FUNC_RE.match(line)
        if match:
            headers.append((index, match.group(1), match.group(2)))

    result: dict[str, FunctionBody] = {}
    for position, (start, symbol, marker) in enumerate(headers):
        if marker not in wanted:
            continue
        end = headers[position + 1][0] if position + 1 < len(headers) else len(lines)
        result[marker] = FunctionBody(marker, symbol, start + 1, tuple(lines[start:end]))

    missing = sorted(wanted - set(result))
    if missing:
        raise SystemExit(f"missing functions in {path}: {', '.join(missing)}")
    return result


def _find(body: FunctionBody, needle: str) -> list[str]:
    hits: list[str] = []
    for offset, line in enumerate(body.lines):
        if needle in line:
            hits.append(f"L{body.start_line + offset}: {line.strip()}")
    return hits


def _print_hits(title: str, body: FunctionBody, needles: Iterable[str]) -> None:
    print(title)
    print(f"  {body.marker} / {body.symbol} @ L{body.start_line}, {len(body.lines)} lines")
    for needle in needles:
        hits = _find(body, needle)
        print(f"  {'yes' if hits else 'no ':3} {needle}")
        for hit in hits[:5]:
            print(f"      {hit}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decompile", type=Path, default=DEFAULT_DECOMPILE)
    args = parser.parse_args()

    funcs = _load_functions(args.decompile, ["func72915", "func72926", "func72927"])

    print("Capture target 1: PxConvexMeshDesc after cropped fill")
    print("-----------------------------------------------------")
    print("Hook table index 122108 after func72915/f_lvcd returns, or at its final branch exit.")
    print("Read the desc pointer passed as the second argument:")
    print()
    print("  +0  u32 points.stride    = 12")
    print("  +4  u32 points.data      = vertsOut")
    print("  +8  u32 points.count     = numVertices")
    print("  +12 u32 polygons.stride  = 20")
    print("  +16 u32 polygons.data    = polygonsOut")
    print("  +20 u32 polygons.count   = numPolygons")
    print("  +24 u32 indices.stride   = 4")
    print("  +28 u32 indices.data     = indicesOut")
    print("  +32 u32 indices.count    = numIndices")
    print()
    print("Read arrays using:")
    print("  points.data    -> points.count * 12 bytes of PxVec3")
    print("  polygons.data  -> polygons.count * 20 bytes of PxHullPolygon")
    print("  indices.data   -> indices.count * 4 bytes of PxU32")
    print()

    _print_hits(
        "func72915 evidence",
        funcs["func72915"],
        [
            "if (a[9]:int)",
            "m = e[4]:int",
            "n = e[7]:int",
            "k = e[1]:int",
            "b.g = 4",
            "b.c = k",
            "b.b = o",
            "b.a = 12",
            "b.d = 20",
            "b.h = h",
            "b.i = m",
            "b.f = n",
            "b.e = l",
            "f_jvcd(a, b)",
        ],
    )

    print("Capture target 2: caller check/build boundary")
    print("---------------------------------------------")
    print("func72926/f_wvcd copies the input desc to stack `f`, calls hullLib,")
    print("then checks `f[2] >= 256` before ConvexMeshBuilder::build.")
    print("This makes `f` another useful desc pointer after the indirect fill call.")
    print()
    _print_hits(
        "func72926 evidence",
        funcs["func72926"],
        [
            "call_indirect(d, f, (d[0])[3]:int)",
            "if (f[2]:int >= 256)",
            "b = f_aucd(c, f, a[12]:int, 0, d)",
        ],
    )

    print("Capture target 3: cooked stream serialization")
    print("---------------------------------------------")
    print("func72927/f_xvcd calls f_wvcd and then writes CVXM/CLHL. This is")
    print("later than target 1, but it can capture the exact cooked stream.")
    print()
    _print_hits(
        "func72927 evidence",
        funcs["func72927"],
        [
            "eqz(f_wvcd(a, p + 160",
            "f_wazc(67, 86, 88, 77",
            "f_xazc(67, 76, 72, 76",
            "f_razc(a[38]:ubyte",
            "f_razc((g & 32767)",
            "f_razc((f[7]:int)[39]:ubyte",
            "f_uazc(f[0]:int, (f[7]:int)[38]:ubyte * 3",
            "call_indirect(c, f[2]:int + a, 1",
            "call_indirect(c, f[3]:int, a[18]:ushort << 1",
            "call_indirect(c, f[4]:int, (f[7]:int)[38]:ubyte * 3",
            "f_uazc(f + 116, 9",
            "f_uazc(f + 68, 3",
        ],
    )

    print("Practical conclusion")
    print("--------------------")
    print("The shortest runtime probe is target 1: hook func72915 after it fills")
    print("the desc and dump three bounded arrays. That gives the exact final")
    print("vertices, polygons/planes, and indices for Unity's cooked stone hull.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
