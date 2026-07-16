"""Extract a wasm table-index map from a wasm2wat text dump.

The Unity WebGL IL2CPP method pointers in Il2CppDumper's script.json are table
indices. This helper turns the huge WAT element segment into a compact JSON map:

    python tools/reverse/extract_wasm_table_map.py build.wat wasm_table_map.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def extract_table_map(wat_path: Path) -> dict[str, str]:
    elem_line = None
    with wat_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if line.lstrip().startswith("(elem "):
                elem_line = line.strip()
                break
    if elem_line is None:
        raise ValueError("No WAT element segment found")

    match = re.search(r"\(i32\.const\s+(\d+)\)\s+(.+)\)$", elem_line)
    if match is None:
        raise ValueError("Could not parse WAT element segment")

    start = int(match.group(1))
    funcs = re.findall(r"\$[\w.$]+", match.group(2))
    return {str(start + i): func for i, func in enumerate(funcs)}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: extract_wasm_table_map.py <build.wat> <out.json>", file=sys.stderr)
        return 2
    wat_path = Path(argv[1])
    out_path = Path(argv[2])
    table_map = extract_table_map(wat_path)
    out_path.write_text(json.dumps(table_map, indent=2), encoding="utf-8")
    print(f"wrote {len(table_map)} table entries to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
