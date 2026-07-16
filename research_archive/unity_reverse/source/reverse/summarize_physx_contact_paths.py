#!/usr/bin/env python3
"""Summarize Unity WebGL PhysX contact paths relevant to curling stones."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, Tuple

from extract_wat_data_string import _load_segments


GEOMETRIES = ("SPHERE", "PLANE", "CAPSULE", "BOX", "CONVEXMESH", "TRIANGLEMESH", "HEIGHTFIELD")

TABLES = {
    "legacy_contact": 4117760,
    "pcm_contact": 4117968,
    "material": 4118208,
}

CURLING_PAIRS = {
    "stone_vs_stone": ("CONVEXMESH", "CONVEXMESH"),
    "stone_vs_rink_mesh": ("CONVEXMESH", "TRIANGLEMESH"),
    "stone_vs_wall_box": ("BOX", "CONVEXMESH"),
}

FUNC_RE = re.compile(r"\$f(\d+)")


def _memory_from_wat(wat: Path) -> Dict[int, int]:
    segments = _load_segments(wat.read_text(encoding="utf-8", errors="replace"))
    memory: Dict[int, int] = {}
    for start, _end, data in segments:
        for index, byte in enumerate(data):
            memory[start + index] = byte
    return memory


def _read_u32(memory: Dict[int, int], address: int) -> int:
    return sum(memory.get(address + index, 0) << (index * 8) for index in range(4))


def _geometry_index(name: str) -> int:
    return GEOMETRIES.index(name)


def _table_entry(memory: Dict[int, int], table_base: int, pair: Tuple[str, str]) -> int:
    row = _geometry_index(pair[0])
    col = _geometry_index(pair[1])
    return _read_u32(memory, table_base + row * 7 * 4 + col * 4)


def _format_entry(word: int, table_map: Dict[str, str]) -> str:
    if word == 0:
        return "0"
    marker = table_map.get(str(word))
    if marker is None:
        return str(word)
    match = FUNC_RE.fullmatch(marker)
    if match:
        return f"{word} {marker} func{match.group(1)}"
    return f"{word} {marker}"


def _iter_rows(memory: Dict[int, int], table_base: int) -> Iterable[Tuple[str, list[int]]]:
    for row, name in enumerate(GEOMETRIES):
        yield name, [_read_u32(memory, table_base + (row * 7 + col) * 4) for col in range(7)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wat",
        type=Path,
        default=Path(r"D:\esp\tmp\curling_reverse_il2cpp\build.wat"),
    )
    parser.add_argument(
        "--table-map",
        type=Path,
        default=Path(r"D:\esp\tmp\curling_reverse_il2cpp\wasm_table_map.json"),
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--full-tables", action="store_true", help="Also include all 7x7 rows.")
    args = parser.parse_args()

    memory = _memory_from_wat(args.wat)
    table_map: Dict[str, str] = json.loads(args.table_map.read_text(encoding="utf-8"))

    report = {
        "wat": str(args.wat),
        "table_map": str(args.table_map),
        "geometry_order": GEOMETRIES,
        "tables": {},
        "curling_pairs": {},
        "unity_relevant_choice": {
            "contactsGeneration": 1,
            "selected_contact_table": "pcm_contact",
            "frictionType": 0,
            "selected_friction_model": "patch",
        },
    }

    for table_name, table_base in TABLES.items():
        report["tables"][table_name] = {"base": table_base}
        if args.full_tables:
            report["tables"][table_name]["rows"] = {
                row_name: [_format_entry(word, table_map) for word in row_words]
                for row_name, row_words in _iter_rows(memory, table_base)
            }

    for pair_name, pair in CURLING_PAIRS.items():
        report["curling_pairs"][pair_name] = {
            "geometry_pair": pair,
            "legacy_contact": _format_entry(_table_entry(memory, TABLES["legacy_contact"], pair), table_map),
            "pcm_contact": _format_entry(_table_entry(memory, TABLES["pcm_contact"], pair), table_map),
            "material": _format_entry(_table_entry(memory, TABLES["material"], pair), table_map),
        }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print("Unity relevant choice:")
    choice = report["unity_relevant_choice"]
    print(f"  contactsGeneration={choice['contactsGeneration']} -> {choice['selected_contact_table']}")
    print(f"  frictionType={choice['frictionType']} -> {choice['selected_friction_model']}")
    print()
    for pair_name, data in report["curling_pairs"].items():
        print(pair_name)
        print(f"  geometry_pair: {data['geometry_pair'][0]} x {data['geometry_pair'][1]}")
        print(f"  pcm_contact:   {data['pcm_contact']}")
        print(f"  legacy_contact:{data['legacy_contact']}")
        print(f"  material:      {data['material']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
