#!/usr/bin/env python3
"""Trace direct callers in a WABT WAT dump.

The Unity WebGL build keeps stable numeric wasm labels such as ``$f71035``.
This helper scans the large ``build.wat`` once, records direct ``call $fNNNN``
edges, and walks the reverse call graph back to table-exported functions.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


FUNC_DEF_RE = re.compile(r"^\s*\(func\s+\$f(\d+)\b")
CALL_RE = re.compile(r"\bcall\s+\$f(\d+)\b")


def load_table_map(path: Path) -> dict[int, list[int]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    by_func: dict[int, list[int]] = defaultdict(list)
    for table_index, marker in raw.items():
        match = re.fullmatch(r"\$f(\d+)", str(marker))
        if match:
            by_func[int(match.group(1))].append(int(table_index))
    return {func: sorted(indices) for func, indices in by_func.items()}


def scan_wat(path: Path) -> tuple[dict[int, set[int]], dict[int, dict[str, Any]]]:
    calls: dict[int, set[int]] = defaultdict(set)
    meta: dict[int, dict[str, Any]] = {}
    current: int | None = None

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_no, line in enumerate(handle, 1):
            match = FUNC_DEF_RE.match(line)
            if match:
                current = int(match.group(1))
                meta[current] = {"line": line_no, "header": line.rstrip()}
            if current is None:
                continue
            for callee in CALL_RE.findall(line):
                calls[current].add(int(callee))
    return calls, meta


def reverse_edges(calls: dict[int, set[int]]) -> dict[int, set[int]]:
    callers: dict[int, set[int]] = defaultdict(set)
    for caller, callees in calls.items():
        for callee in callees:
            callers[callee].add(caller)
    return callers


def walk_callers(
    target: int,
    callers: dict[int, set[int]],
    table_by_func: dict[int, list[int]],
    max_depth: int,
) -> list[dict[str, Any]]:
    seen = {target}
    queue: deque[tuple[int, list[int]]] = deque([(target, [target])])
    rows: list[dict[str, Any]] = []

    while queue:
        func, path = queue.popleft()
        depth = len(path) - 1
        if depth >= max_depth:
            continue
        for caller in sorted(callers.get(func, ())):
            next_path = path + [caller]
            rows.append(
                {
                    "target": target,
                    "callee": func,
                    "caller": caller,
                    "depth": depth + 1,
                    "path_from_target": next_path,
                    "caller_table_indices": table_by_func.get(caller, []),
                }
            )
            if caller not in seen:
                seen.add(caller)
                queue.append((caller, next_path))
    return rows


def print_report(
    targets: list[int],
    rows_by_target: dict[int, list[dict[str, Any]]],
    table_by_func: dict[int, list[int]],
    meta: dict[int, dict[str, Any]],
) -> None:
    for target in targets:
        print(f"func{target}")
        target_tables = table_by_func.get(target, [])
        if target_tables:
            print(f"  table: {target_tables}")
        rows = rows_by_target[target]
        if not rows:
            print("  no direct callers found")
            continue
        for row in rows:
            caller = row["caller"]
            tables = row["caller_table_indices"]
            path = " <- ".join(f"func{x}" for x in row["path_from_target"])
            table_suffix = f" table={tables}" if tables else ""
            line = meta.get(caller, {}).get("line")
            line_suffix = f" line={line}" if line else ""
            print(f"  d{row['depth']}: {path}{table_suffix}{line_suffix}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wat", type=Path)
    parser.add_argument("table_map", type=Path)
    parser.add_argument("targets", nargs="+", type=int, help="Wasm function IDs, e.g. 71035")
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    calls, meta = scan_wat(args.wat)
    callers = reverse_edges(calls)
    table_by_func = load_table_map(args.table_map)

    rows_by_target = {
        target: walk_callers(target, callers, table_by_func, args.max_depth)
        for target in args.targets
    }
    print_report(args.targets, rows_by_target, table_by_func, meta)

    if args.output:
        payload = {
            "wat": str(args.wat),
            "table_map": str(args.table_map),
            "targets": args.targets,
            "max_depth": args.max_depth,
            "rowsByTarget": rows_by_target,
            "targetTables": {str(t): table_by_func.get(t, []) for t in args.targets},
            "functionMeta": {
                str(func): {"table": table_by_func.get(func, []), **info}
                for func, info in meta.items()
                if func in set(args.targets)
                or any(row["caller"] == func for rows in rows_by_target.values() for row in rows)
            },
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"wrote {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
