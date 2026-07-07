#!/usr/bin/env python3
"""Resolve PhysX metadata/vtable/function-table blocks from Unity WebGL WAT data.

The PhysX task names in this build point at metadata blocks, not plain string
starts. The first words in those blocks are indirect-function table indices.
The same representation is also used by small native function tables such as
the contact finalization method arrays. This helper decodes those words and maps
them back to wasm function ids.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path

from extract_wat_data_string import _load_segments


PRINTABLE_RE = re.compile(rb"[ -~]{6,}")


def _read_bytes(segments: list[tuple[int, int, bytes]], address: int, size: int) -> bytes:
    for start, end, data in segments:
        if start <= address < end:
            offset = address - start
            return data[offset : min(offset + size, len(data))]
    raise ValueError(f"address range not found in data segments: {address:#x}+{size}")


def _func_marker(table_value: str | None) -> str:
    if not table_value:
        return ""
    match = re.fullmatch(r"\$f(\d+)", table_value)
    if not match:
        return table_value
    return f"func{match.group(1)}"


def _strings(blob: bytes) -> list[str]:
    found: list[str] = []
    for match in PRINTABLE_RE.finditer(blob):
        text = match.group(0).decode("ascii", errors="replace")
        if text not in found:
            found.append(text)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wat", type=Path)
    parser.add_argument("table_map", type=Path)
    parser.add_argument("addresses", nargs="+", type=lambda value: int(value, 0))
    parser.add_argument("--bytes", type=int, default=256)
    parser.add_argument("--words", type=int, default=12)
    args = parser.parse_args()

    segments = _load_segments(args.wat.read_text(encoding="utf-8", errors="replace"))
    table_map = json.loads(args.table_map.read_text(encoding="utf-8"))

    for address in args.addresses:
        print(f"address {address} ({address:#x})")
        try:
            blob = _read_bytes(segments, address, args.bytes)
        except ValueError as exc:
            print(f"  {exc}")
            print()
            continue

        word_count = min(args.words, len(blob) // 4)
        words = struct.unpack("<" + "I" * word_count, blob[: word_count * 4])
        for index, word in enumerate(words):
            table_value = table_map.get(str(word))
            marker = _func_marker(table_value)
            mapped = f" {table_value} {marker}".rstrip() if table_value else ""
            print(f"  [{index:02d}] {word}{mapped}")
        strings = _strings(blob)
        if strings:
            print("  strings:")
            for text in strings[:12]:
                print(f"    {text}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
