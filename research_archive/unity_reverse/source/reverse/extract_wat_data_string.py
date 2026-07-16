#!/usr/bin/env python3
"""Extract null-terminated strings from WAT data segments by linear memory address."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DATA_RE = re.compile(r'\(data(?: \$[^ ]+)? \(i32\.const (\d+)\) "', re.MULTILINE)


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wat", type=Path)
    parser.add_argument("addresses", nargs="+", type=lambda value: int(value, 0))
    parser.add_argument("--max-bytes", type=int, default=256)
    args = parser.parse_args()

    segments = _load_segments(args.wat.read_text(encoding="utf-8", errors="replace"))
    for address in args.addresses:
        raw = _read_c_string(segments, address, args.max_bytes)
        if raw is None:
            print(f"{address}: <not found>")
            continue
        text = raw.decode("utf-8", errors="replace")
        print(f"{address}: {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
