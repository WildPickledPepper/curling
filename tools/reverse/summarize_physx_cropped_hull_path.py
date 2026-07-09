#!/usr/bin/env python3
"""Summarize the Unity wasm -> PhysX cropped convex-hull cooking path.

This is a small evidence printer for the curling stone MeshCollider path.  It
does not export the final cooked hull; it proves the branch chain we must
reproduce or hook next:

  createConvexHull -> expandHullOBB -> mCropedConvexHull -> cropped desc fill
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_DECOMPILE = Path(r"D:\esp\tmp\curling_reverse_il2cpp\build.dcmp")
DEFAULT_PHYSX_ROOT = Path(r"D:\esp\tmp\curling_physx_41\physx")


@dataclass(frozen=True)
class FunctionBody:
    marker: str
    name: str
    start_line: int
    lines: tuple[str, ...]


@dataclass(frozen=True)
class Hit:
    line: int
    text: str


FUNC_RE = re.compile(r"^function\s+([A-Za-z0-9_]+)\(.*//\s+(func\d+)")


def _load_functions(path: Path, markers: Iterable[str]) -> dict[str, FunctionBody]:
    wanted = set(markers)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    headers: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = FUNC_RE.match(line)
        if match:
            headers.append((index, match.group(1), match.group(2)))

    result: dict[str, FunctionBody] = {}
    for pos, (start, name, marker) in enumerate(headers):
        if marker not in wanted:
            continue
        end = headers[pos + 1][0] if pos + 1 < len(headers) else len(lines)
        result[marker] = FunctionBody(
            marker=marker,
            name=name,
            start_line=start + 1,
            lines=tuple(lines[start:end]),
        )

    missing = sorted(wanted - set(result))
    if missing:
        raise SystemExit(f"missing functions in {path}: {', '.join(missing)}")
    return result


def _find(body: FunctionBody, needle: str, limit: int | None = None) -> list[Hit]:
    hits: list[Hit] = []
    for offset, line in enumerate(body.lines):
        if needle in line:
            hits.append(Hit(body.start_line + offset, line.strip()))
            if limit is not None and len(hits) >= limit:
                break
    return hits


def _find_any(body: FunctionBody, needles: Iterable[str]) -> dict[str, list[Hit]]:
    return {needle: _find(body, needle) for needle in needles}


def _source_hits(path: Path, patterns: Iterable[str]) -> dict[str, list[Hit]]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    result: dict[str, list[Hit]] = {}
    for pattern in patterns:
        result[pattern] = [
            Hit(index + 1, line.strip())
            for index, line in enumerate(lines)
            if pattern in line
        ]
    return result


def _format_hits(hits: list[Hit]) -> list[str]:
    return [f"L{hit.line}: {hit.text}" for hit in hits]


def _has_hits(report: dict) -> bool:
    required = [
        report["wasm"]["func72908_createConvexHull"]["hits"]["f_gvcd(a)"],
        report["wasm"]["func72910_expandHullOBB"]["hits"]["f_jvcd(a, n + 16)"],
        report["wasm"]["func72910_expandHullOBB"]["hits"]["k = select_if(i, 256"],
        report["wasm"]["func72910_expandHullOBB"]["hits"]["c[1]:int > (d = a[1]:int)[19]:ushort"],
        report["wasm"]["func72910_expandHullOBB"]["hits"]["a[9]:int = c"],
        report["wasm"]["func72915_fillConvexMeshDesc"]["hits"]["if (a[9]:int)"],
        report["wasm"]["func72915_fillConvexMeshDesc"]["hits"]["f_jvcd(a, b)"],
    ]
    return all(required)


def build_report(decompile: Path, physx_root: Path, convex_flags: int, vertex_limit: int) -> dict:
    funcs = _load_functions(
        decompile,
        ["func72908", "func72910", "func72915", "func72926", "func72927"],
    )

    quick_hull_cpp = physx_root / "source" / "physxcooking" / "src" / "convex" / "QuickHullConvexHullLib.cpp"
    hull_utils_cpp = physx_root / "source" / "physxcooking" / "src" / "convex" / "ConvexHullUtils.cpp"
    cooking_cpp = physx_root / "source" / "physxcooking" / "src" / "Cooking.cpp"

    flag_bits = {
        "eCOMPUTE_CONVEX": 0x02,
        "ePLANE_SHIFTING": 0x20,
        "eGPU_COMPATIBLE": 0x80,
    }

    wasm = {
        "func72908_createConvexHull": {
            "symbol": funcs["func72908"].name,
            "start_line": funcs["func72908"].start_line,
            "line_count": len(funcs["func72908"].lines),
            "hits": _find_any(
                funcs["func72908"],
                [
                    "(a[8]:int)[7]:int <= (b = a[1]:int)[19]:ushort",
                    "(a[1]:int)[36]:ubyte & 32",
                    "f_fvcd(a)",
                    "f_gvcd(a)",
                    "if (a[9]:int) goto B_xb",
                    "(a[1]:int)[36]:ubyte & 128",
                ],
            ),
        },
        "func72910_expandHullOBB": {
            "symbol": funcs["func72910"].name,
            "start_line": funcs["func72910"].start_line,
            "line_count": len(funcs["func72910"].lines),
            "hits": _find_any(
                funcs["func72910"],
                [
                    "f_hvcd(n + 112, c)",
                    "f_jvcd(a, n + 16)",
                    "n[26]:short = (a[1]:int)[18]:ushort",
                    "k = select_if(i, 256",
                    "c = select_if(l, -1, ka > oa)",
                    "var h:int = g_a - 7968",
                    "c[1]:int > (d = a[1]:int)[19]:ushort",
                    "d[36]:ubyte & 128",
                    "a[9]:int = c",
                ],
            ),
        },
        "func72915_fillConvexMeshDesc": {
            "symbol": funcs["func72915"].name,
            "start_line": funcs["func72915"].start_line,
            "line_count": len(funcs["func72915"].lines),
            "hits": _find_any(
                funcs["func72915"],
                [
                    "if (a[9]:int)",
                    "m = e[4]:int",
                    "n = e[7]:int",
                    "k = e[1]:int",
                    "b.g = 4",
                    "b.a = 12",
                    "b.d = 20",
                    "f_jvcd(a, b)",
                ],
            ),
        },
        "func72926_cookConvexMeshInternal": {
            "symbol": funcs["func72926"].name,
            "start_line": funcs["func72926"].start_line,
            "line_count": len(funcs["func72926"].lines),
        },
        "func72927_convexMeshBuilderSave": {
            "symbol": funcs["func72927"].name,
            "start_line": funcs["func72927"].start_line,
            "line_count": len(funcs["func72927"].lines),
        },
    }

    source = {
        "Cooking.cpp": _source_hits(
            cooking_cpp,
            [
                "hullLib->createConvexHull()",
                "hullLib->fillConvexMeshDesc(desc)",
                "desc.points.count >= 256",
            ],
        ),
        "QuickHullConvexHullLib.cpp": _source_hits(
            quick_hull_cpp,
            [
                "res = expandHull()",
                "res = expandHullOBB()",
                "fillConvexMeshDescFromQuickHull(convexDesc)",
                "computeOBBFromConvex(convexDesc",
                "PxU32 maxplanes = PxMin(PxU32(256)",
                "c->findCandidatePlane(planeTolerance, epsilon)",
                "c = convexHullCrop(*tmp",
                "c->getVertices().size() > mConvexMeshDesc.vertexLimit",
                "c->maxNumVertsPerFace() > gpuMaxVertsPerFace",
                "mCropedConvexHull = c",
                "fillConvexMeshDescFromCroppedHull(desc)",
            ],
        ),
        "ConvexHullUtils.cpp": _source_hits(
            hull_utils_cpp,
            [
                "ConvexHull::findCandidatePlane",
                "return (md > epsilon) ? p : -1",
                "bool ConvexHull::assertIntact",
                "convexHullCrop(const ConvexHull& convex",
            ],
        ),
    }

    report = {
        "decompile": str(decompile),
        "physx_root": str(physx_root),
        "stone_convex_desc_assumption": {
            "flags": convex_flags,
            "flags_hex": f"0x{convex_flags:04x}",
            "vertexLimit": vertex_limit,
            "eCOMPUTE_CONVEX": bool(convex_flags & flag_bits["eCOMPUTE_CONVEX"]),
            "ePLANE_SHIFTING": bool(convex_flags & flag_bits["ePLANE_SHIFTING"]),
            "eGPU_COMPATIBLE": bool(convex_flags & flag_bits["eGPU_COMPATIBLE"]),
            "expected_expand_path": "f_fvcd/expandHull"
            if convex_flags & flag_bits["ePLANE_SHIFTING"]
            else "f_gvcd/expandHullOBB",
        },
        "wasm": wasm,
        "physx_source": source,
    }
    report["evidence_chain_complete"] = _has_hits(report)
    return report


def _print_section(title: str) -> None:
    print(title)
    print("-" * len(title))


def print_report(report: dict) -> None:
    desc = report["stone_convex_desc_assumption"]
    _print_section("Stone convex desc assumption")
    print(f"flags={desc['flags_hex']} vertexLimit={desc['vertexLimit']}")
    print(f"eCOMPUTE_CONVEX={desc['eCOMPUTE_CONVEX']}")
    print(f"ePLANE_SHIFTING={desc['ePLANE_SHIFTING']}")
    print(f"eGPU_COMPATIBLE={desc['eGPU_COMPATIBLE']}")
    print(f"expected expand path: {desc['expected_expand_path']}")
    print()

    _print_section("Unity wasm evidence")
    for title, data in report["wasm"].items():
        print(f"{title}: {data['symbol']} @ L{data['start_line']} ({data['line_count']} lines)")
        hits = data.get("hits", {})
        for needle, found in hits.items():
            status = "yes" if found else "no"
            print(f"  {status:3} {needle}")
            for line in _format_hits(found[:4]):
                print(f"      {line}")
        print()

    _print_section("PhysX 4.1 source evidence")
    for filename, patterns in report["physx_source"].items():
        print(filename)
        for pattern, hits in patterns.items():
            status = "yes" if hits else "no"
            print(f"  {status:3} {pattern}")
            for line in _format_hits(hits[:3]):
                print(f"      {line}")
        print()

    _print_section("Conclusion")
    if report["evidence_chain_complete"]:
        print(
            "The wasm and PhysX source evidence support the cropped-hull branch: "
            "createConvexHull -> f_gvcd/expandHullOBB -> a[9]/mCropedConvexHull -> "
            "fillConvexMeshDesc cropped path."
        )
    else:
        print("The expected evidence chain is incomplete; inspect missing hits above.")


def _json_default(value: object) -> object:
    if is_dataclass(value):
        return asdict(value)
    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decompile", type=Path, default=DEFAULT_DECOMPILE)
    parser.add_argument("--physx-root", type=Path, default=DEFAULT_PHYSX_ROOT)
    parser.add_argument(
        "--convex-flags",
        type=lambda value: int(value, 0),
        default=0x02,
        help="PxConvexMeshDesc.flags for the stone runtime path; default is eCOMPUTE_CONVEX.",
    )
    parser.add_argument("--vertex-limit", type=int, default=255)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    report = build_report(args.decompile, args.physx_root, args.convex_flags, args.vertex_limit)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, default=_json_default))
    else:
        print_report(report)
    return 0 if report["evidence_chain_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
