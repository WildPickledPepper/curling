#!/usr/bin/env python3
"""Scan Unity WebGL WAT data segments for runs of wasm table function pointers."""

from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path

from extract_wat_data_string import _load_segments


FUNC_RE = re.compile(r"\$f(\d+)")


def _func_id(marker: str | None) -> int | None:
    if marker is None:
        return None
    match = FUNC_RE.fullmatch(marker)
    if not match:
        return None
    return int(match.group(1))


def _format_func(table_value: str | None) -> str:
    func_id = _func_id(table_value)
    if func_id is None:
        return table_value or ""
    return f"{table_value}/func{func_id}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wat", type=Path)
    parser.add_argument("table_map", type=Path)
    parser.add_argument("--min-run", type=int, default=4)
    parser.add_argument("--min-func", type=int, default=0)
    parser.add_argument("--max-func", type=int, default=10**9)
    parser.add_argument("--context", type=int, default=8)
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    segments = _load_segments(args.wat.read_text(encoding="utf-8", errors="replace"))
    table_map = json.loads(args.table_map.read_text(encoding="utf-8"))

    printed = 0
    for start, _end, data in segments:
        run: list[tuple[int, int, str]] = []
        usable = len(data) - (len(data) % 4)
        for offset in range(0, usable, 4):
            word = struct.unpack_from("<I", data, offset)[0]
            table_value = table_map.get(str(word))
            func_id = _func_id(table_value)
            if func_id is not None and args.min_func <= func_id <= args.max_func:
                run.append((start + offset, word, table_value))
                continue

            if len(run) >= args.min_run:
                print(f"address {run[0][0]} ({run[0][0]:#x}) run={len(run)}")
                for address, value, marker in run[: args.context]:
                    print(f"  {address:#x}: {value} {_format_func(marker)}")
                if len(run) > args.context:
                    print("  ...")
                print()
                printed += 1
                if printed >= args.limit:
                    return 0
            run = []

        if len(run) >= args.min_run:
            print(f"address {run[0][0]} ({run[0][0]:#x}) run={len(run)}")
            for address, value, marker in run[: args.context]:
                print(f"  {address:#x}: {value} {_format_func(marker)}")
            if len(run) > args.context:
                print("  ...")
            print()
            printed += 1
            if printed >= args.limit:
                return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
