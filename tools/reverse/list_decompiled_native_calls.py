#!/usr/bin/env python3
"""List native wasm-decompile helper calls with funcNNNN ids."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FUNC_HEADER_RE = re.compile(r"^(?:\d+:\s*)?function\s+(f_[A-Za-z0-9_]+)\([^)]*\).*//\s*(func\d+)", re.MULTILINE)
CALL_RE = re.compile(r"\b(f_[A-Za-z0-9_]+)\(")


def load_aliases(decompile: Path) -> dict[str, str]:
    text = decompile.read_text(encoding="utf-8", errors="replace")
    return {alias: func_id for alias, func_id in FUNC_HEADER_RE.findall(text)}


def list_calls(alias_map: dict[str, str], function_path: Path) -> list[tuple[str, str, int]]:
    text = function_path.read_text(encoding="utf-8", errors="replace")
    header = FUNC_HEADER_RE.search(text)
    self_alias = header.group(1) if header else None
    counts: dict[str, int] = {}
    for alias in CALL_RE.findall(text):
        if alias == self_alias or alias not in alias_map:
            continue
        counts[alias] = counts.get(alias, 0) + 1
    return sorted(
        ((alias, alias_map[alias], count) for alias, count in counts.items()),
        key=lambda item: (int(item[1][4:]), item[0]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("decompile", type=Path, help="Full wasm-decompile output, e.g. build.dcmp")
    parser.add_argument("functions", type=Path, nargs="+", help="Extracted function .dcmp files")
    args = parser.parse_args()

    alias_map = load_aliases(args.decompile)
    for function_path in args.functions:
        print(f"== {function_path.name} ==")
        for alias, func_id, count in list_calls(alias_map, function_path):
            suffix = "" if count == 1 else f" x{count}"
            print(f"{func_id} {alias}{suffix}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
