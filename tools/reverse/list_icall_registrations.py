#!/usr/bin/env python3
"""List Unity internal-call registrations recovered from wasm-decompile output.

Unity's WebGL player registers engine internal calls through a helper that
decompiles as ``f_vvrd(name_address, function_pointer)`` in this build. This
script resolves the string addresses through the WAT data segments and prints a
searchable table.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from extract_wat_data_string import _load_segments, _read_c_string


CALL_RE = re.compile(r"\bf_vvrd\((\d+),\s*(\d+)\);")


def iter_registrations(decompile_text: str) -> list[tuple[int, int]]:
    return [(int(match.group(1)), int(match.group(2))) for match in CALL_RE.finditer(decompile_text)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wat", type=Path)
    parser.add_argument("decompile", type=Path)
    parser.add_argument("--grep", help="case-insensitive substring filter")
    parser.add_argument("--max-bytes", type=int, default=256)
    args = parser.parse_args()

    segments = _load_segments(args.wat.read_text(encoding="utf-8", errors="replace"))
    registrations = iter_registrations(args.decompile.read_text(encoding="utf-8", errors="ignore"))
    needle = args.grep.casefold() if args.grep else None

    for name_address, function_pointer in registrations:
        raw = _read_c_string(segments, name_address, args.max_bytes)
        if raw is None:
            text = "<string not found>"
        else:
            text = raw.decode("utf-8", errors="replace")
        if needle and needle not in text.casefold():
            continue
        print(f"{name_address}\t{function_pointer}\t{text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
