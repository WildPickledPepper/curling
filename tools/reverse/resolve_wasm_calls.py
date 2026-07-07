#!/usr/bin/env python3
"""Resolve WABT decompiled call aliases back to IL2CPP method names.

WABT emits local function names such as `f_kwjc` and comments the definition as
`// func60096`. Unity WebGL's indirect table maps `$f60096` to an IL2CPP method
pointer index, and Il2CppDumper stores that index in ScriptMethod.Address.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEF_RE = re.compile(r"^function\s+(f_[A-Za-z0-9_$]+)\b.*//\s*func(\d+)", re.MULTILINE)
CALL_RE = re.compile(r"\b(f_[A-Za-z0-9_$]+)\(")


def _load_alias_map(decompiled_wasm: Path) -> dict[str, int]:
    text = decompiled_wasm.read_text(encoding="utf-8", errors="replace")
    return {alias: int(func_id) for alias, func_id in DEF_RE.findall(text)}


def _load_method_names(script: dict[str, Any]) -> dict[int, str]:
    names: dict[int, str] = {}
    for entry in script.get("ScriptMethod", []):
        address = entry.get("Address")
        name = entry.get("Name")
        if address is not None and name is not None:
            names[int(address)] = str(name)
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("script_json", type=Path)
    parser.add_argument("wasm_table_map", type=Path)
    parser.add_argument("decompiled_wasm", type=Path)
    parser.add_argument("functions", nargs="+", type=Path)
    args = parser.parse_args()

    script = json.loads(args.script_json.read_text(encoding="utf-8"))
    table_map = json.loads(args.wasm_table_map.read_text(encoding="utf-8"))
    table_by_func = {name: int(index) for index, name in table_map.items()}
    alias_to_func_id = _load_alias_map(args.decompiled_wasm)
    method_names = _load_method_names(script)

    for function_path in args.functions:
        text = function_path.read_text(encoding="utf-8", errors="replace")
        aliases = sorted(set(CALL_RE.findall(text)))
        print(f"== {function_path.name} ==")
        for alias in aliases:
            func_id = alias_to_func_id.get(alias)
            if func_id is None:
                continue
            table_index = table_by_func.get(f"$f{func_id}")
            if table_index is None:
                continue
            method_name = method_names.get(table_index)
            if method_name is None:
                continue
            print(f"  {alias} -> func{func_id} -> table[{table_index}] -> {method_name}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
