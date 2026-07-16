#!/usr/bin/env python3
"""Resolve wasm linear-memory string references in WABT-decompiled functions.

WABT's wasm-decompile output often contains calls such as ``f_vkb(309480)``
and ``f_xkb(3830976)``. In this Unity WebGL build ``f_vkb`` usually points to
null-terminated strings in wasm linear-memory data segments, while ``f_xkb``
commonly points to IL2CPP managed string literal addresses. This helper
extracts those names for one or more small decompiled function files.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DATA_RE = re.compile(r'\(data(?: \$[^ ]+)? \(i32\.const (\d+)\) "', re.MULTILINE)
STRING_REF_RE = re.compile(r"\bf_[vx]kb\((\d+)\)")


def _decode_wat_bytes(source: str) -> tuple[bytes, int]:
    out = bytearray()
    i = 0
    while i < len(source):
        ch = source[i]
        if ch == '"':
            break
        if ch == "\\":
            if i + 2 < len(source) and all(c in "0123456789abcdefABCDEF" for c in source[i + 1 : i + 3]):
                out.append(int(source[i + 1 : i + 3], 16))
                i += 3
                continue
            if i + 1 < len(source):
                escapes = {"n": 10, "t": 9, "r": 13, '"': 34, "'": 39, "\\": 92}
                out.append(escapes.get(source[i + 1], ord(source[i + 1])))
                i += 2
                continue
        out.extend(ch.encode("utf-8"))
        i += 1
    return bytes(out), i


def _load_segments(wat_text: str) -> list[tuple[int, int, bytes]]:
    segments: list[tuple[int, int, bytes]] = []
    for match in DATA_RE.finditer(wat_text):
        start_address = int(match.group(1))
        data, _ = _decode_wat_bytes(wat_text[match.end() :])
        segments.append((start_address, start_address + len(data), data))
    return segments


def _read_c_string(segments: list[tuple[int, int, bytes]], address: int, max_bytes: int) -> bytes | None:
    for start, end, data in segments:
        if start <= address < end:
            offset = address - start
            terminator = data.find(b"\0", offset)
            if terminator < 0:
                terminator = min(len(data), offset + max_bytes)
            return data[offset:terminator]
    return None


def _default_script_json(wat_path: Path) -> Path | None:
    candidates = [
        wat_path.parent / "il2cpp_out" / "script.json",
        wat_path.parent / "script.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _load_script_strings(script_json_path: Path | None) -> dict[int, str]:
    if script_json_path is None:
        return {}
    data = json.loads(script_json_path.read_text(encoding="utf-8", errors="replace"))
    return {
        int(item["Address"]): str(item["Value"])
        for item in data.get("ScriptString", [])
        if "Address" in item and "Value" in item
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wat", type=Path, help="build.wat")
    parser.add_argument("functions", nargs="+", type=Path, help="decompiled function snippets")
    parser.add_argument("--script-json", type=Path, default=None, help="optional Il2CppDumper script.json")
    parser.add_argument("--max-bytes", type=int, default=256)
    args = parser.parse_args()

    segments = _load_segments(args.wat.read_text(encoding="utf-8", errors="replace"))
    script_strings = _load_script_strings(args.script_json or _default_script_json(args.wat))

    for function_path in args.functions:
        text = function_path.read_text(encoding="utf-8", errors="replace")
        addresses = sorted({int(match.group(1)) for match in STRING_REF_RE.finditer(text)})
        print(f"== {function_path.name} ==")
        if not addresses:
            print("  <no f_vkb/f_xkb string refs>")
            continue
        for address in addresses:
            if address in script_strings:
                print(f"  {address}: {script_strings[address]}")
                continue
            raw = _read_c_string(segments, address, args.max_bytes)
            if raw is None:
                print(f"  {address}: <not found>")
                continue
            print(f"  {address}: {raw.decode('utf-8', errors='replace')}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
