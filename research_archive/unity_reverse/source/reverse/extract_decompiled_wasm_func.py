#!/usr/bin/env python3
"""Extract named wasm-decompile functions from a large decompiler output.

WABT's wasm-decompile keeps the original numeric wasm function id in comments
such as ``// func59956`` even when it renames the function symbol. This helper
cuts those functions into smaller files for manual reverse engineering.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def extract_function(lines: list[str], marker: str) -> list[str]:
    start = None
    for index, line in enumerate(lines):
        if marker in line and line.startswith("function "):
            start = index
            break
    if start is None:
        raise SystemExit(f"could not find function marker: {marker}")

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("function "):
            end = index
            break
    return lines[start:end]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("decompile", type=Path, help="wasm-decompile output")
    parser.add_argument("out_dir", type=Path, help="directory for extracted files")
    parser.add_argument("markers", nargs="+", help="markers like func59955")
    args = parser.parse_args()

    lines = args.decompile.read_text(encoding="utf-8", errors="ignore").splitlines()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for marker in args.markers:
        body = extract_function(lines, marker)
        output = args.out_dir / f"{marker}.dcmp"
        output.write_text(
            "\n".join(f"{line_no}: {line}" for line_no, line in enumerate(body, 1))
            + "\n",
            encoding="utf-8",
        )
        print(f"wrote {len(body)} lines to {output}")


if __name__ == "__main__":
    main()
