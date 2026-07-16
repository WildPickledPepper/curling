#!/usr/bin/env python3
"""Find wasm-decompile function markers that contain specific line numbers."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FUNCTION_RE = re.compile(r"^function\s+(\S+).*//\s+(func\d+)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("decompile", type=Path)
    parser.add_argument("lines", nargs="+", type=int)
    args = parser.parse_args()

    wanted = sorted(args.lines)
    next_wanted = 0
    current_name = "<before first function>"
    current_marker = "<none>"
    current_start = 0

    with args.decompile.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_no, line in enumerate(handle, 1):
            match = FUNCTION_RE.match(line)
            if match:
                current_name, current_marker = match.groups()
                current_start = line_no
            while next_wanted < len(wanted) and wanted[next_wanted] == line_no:
                print(f"{line_no}\t{current_marker}\t{current_name}\tstarts_at={current_start}")
                next_wanted += 1
            if next_wanted >= len(wanted):
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
