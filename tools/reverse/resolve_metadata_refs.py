#!/usr/bin/env python3
"""Resolve IL2CPP metadata/string references in WABT-decompiled functions.

The generated wasm uses `f_xkb(address)` to lazily initialize metadata usage
slots. After initialization, the decompiled code reads those slots as
`d_[index]`. In this build the relation is:

    address = 3705984 + 4 * index

This helper maps both forms back to names from il2cppdumper's script.json.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FXKB_RE = re.compile(r"f_xkb\((\d+)\)")
DREF_RE = re.compile(r"d_[a-zA-Z0-9_$]*\[(\d+)\]:")


def _iter_named_entries(script: dict[str, Any]):
    for group in (
        "ScriptString",
        "ScriptMetadata",
        "ScriptMetadataMethod",
        "ScriptMethod",
    ):
        for entry in script.get(group, []):
            address = entry.get("Address")
            name = entry.get("Name") if group != "ScriptString" else entry.get("Value")
            if address is None or name is None:
                continue
            yield int(address), group, str(name)


def _format_ref(address: int, entries: dict[int, tuple[str, str]]) -> str:
    hit = entries.get(address)
    if hit is None:
        return f"{address} 0x{address:x} <unresolved>"
    group, name = hit
    return f"{address} 0x{address:x} {group} {name}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("script_json", type=Path)
    parser.add_argument("functions", nargs="+", type=Path)
    parser.add_argument(
        "--base",
        type=int,
        default=3_705_984,
        help="base address for d_[index] metadata slots",
    )
    args = parser.parse_args()

    with args.script_json.open("r", encoding="utf-8") as f:
        script = json.load(f)

    entries = {address: (group, name) for address, group, name in _iter_named_entries(script)}

    for function_path in args.functions:
        text = function_path.read_text(encoding="utf-8", errors="replace")
        fxkb_addresses = sorted({int(m.group(1)) for m in FXKB_RE.finditer(text)})
        d_indices = sorted({int(m.group(1)) for m in DREF_RE.finditer(text)})

        print(f"== {function_path.name} ==")
        print("f_xkb initializers:")
        for address in fxkb_addresses:
            print("  " + _format_ref(address, entries))

        print("d_ metadata reads:")
        for index in d_indices:
            address = args.base + index * 4
            print(f"  d_[{index}] -> " + _format_ref(address, entries))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
