#!/usr/bin/env python3
"""Summarize Unity Rigidbody mass/COM/inertia writes in a WebGL IL2CPP build.

The Il2CppDumper ``ScriptMethod.Address`` values in this Unity WebGL build are
wasm table indices, not ``d_[index]`` metadata slots.  This tool resolves those
indices through ``wasm_table_map.json`` and then scans ``wasm-decompile`` output
for actual calls to the resolved wrapper functions.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FUNC_HEADER_RE = re.compile(r"^function\s+(f_[A-Za-z0-9_]+)\([^)]*\).*//\s*(func\d+)")
CALL_RE = re.compile(r"\b(f_[A-Za-z0-9_]+)\(")

TARGET_RIGIDBODY_METHODS = {
    "UnityEngine.Rigidbody$$set_mass",
    "UnityEngine.Rigidbody$$set_centerOfMass",
    "UnityEngine.Rigidbody$$set_inertiaTensorRotation",
    "UnityEngine.Rigidbody$$set_inertiaTensor",
    "UnityEngine.Rigidbody$$ResetCenterOfMass",
    "UnityEngine.Rigidbody$$ResetInertiaTensor",
    "UnityEngine.Rigidbody$$set_centerOfMass_Injected",
    "UnityEngine.Rigidbody$$set_inertiaTensorRotation_Injected",
    "UnityEngine.Rigidbody$$set_inertiaTensor_Injected",
}


@dataclass(frozen=True)
class MethodRef:
    address: int
    name: str
    signature: str
    func_id: str | None
    alias: str | None


@dataclass(frozen=True)
class CallSite:
    line: int
    api_names: tuple[str, ...]
    api_func_id: str
    api_alias: str
    caller_func_id: str
    caller_alias: str
    caller_methods: tuple[str, ...]
    source: str


def load_script_methods(script_json: Path) -> dict[int, dict[str, Any]]:
    script = json.loads(script_json.read_text(encoding="utf-8", errors="replace"))
    out: dict[int, dict[str, Any]] = {}
    for entry in script.get("ScriptMethod", []):
        address = entry.get("Address")
        if address is None:
            continue
        out[int(address)] = entry
    return out


def load_table_map(table_map: Path) -> dict[int, str]:
    data = json.loads(table_map.read_text(encoding="utf-8", errors="replace"))
    out: dict[int, str] = {}
    for index, alias in data.items():
        normalized = str(alias).lstrip("$")
        if normalized.startswith("f") and normalized[1:].isdigit():
            normalized = "func" + normalized[1:]
        out[int(index)] = normalized
    return out


def load_decompile_aliases(decompile: Path) -> tuple[dict[str, str], dict[str, str]]:
    alias_to_func: dict[str, str] = {}
    func_to_alias: dict[str, str] = {}
    with decompile.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            match = FUNC_HEADER_RE.match(line)
            if not match:
                continue
            alias, func_id = match.groups()
            alias_to_func[alias] = func_id
            func_to_alias[func_id] = alias
    return alias_to_func, func_to_alias


def resolve_methods(
    script_methods: dict[int, dict[str, Any]],
    table_map: dict[int, str],
    func_to_alias: dict[str, str],
    target_names: set[str],
) -> list[MethodRef]:
    refs: list[MethodRef] = []
    for address, entry in sorted(script_methods.items()):
        name = str(entry.get("Name", ""))
        if name not in target_names:
            continue
        func_id = table_map.get(address)
        alias = func_to_alias.get(func_id) if func_id else None
        refs.append(
            MethodRef(
                address=address,
                name=name,
                signature=str(entry.get("Signature", "")),
                func_id=func_id,
                alias=alias,
            )
        )
    return refs


def build_func_method_index(
    script_methods: dict[int, dict[str, Any]],
    table_map: dict[int, str],
) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for address, entry in script_methods.items():
        func_id = table_map.get(address)
        if not func_id:
            continue
        out.setdefault(func_id, []).append(str(entry.get("Name", "")))
    for names in out.values():
        names.sort()
    return out


def scan_calls(
    decompile: Path,
    alias_to_func: dict[str, str],
    func_to_methods: dict[str, list[str]],
    target_refs: list[MethodRef],
) -> list[CallSite]:
    alias_to_api_names: dict[str, list[str]] = {}
    alias_to_api_func: dict[str, str] = {}
    for ref in target_refs:
        if not ref.alias or not ref.func_id:
            continue
        alias_to_api_names.setdefault(ref.alias, []).append(ref.name)
        alias_to_api_func[ref.alias] = ref.func_id

    callsites: list[CallSite] = []
    current_alias = "<none>"
    current_func_id = "<none>"
    with decompile.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_no, line in enumerate(handle, 1):
            header = FUNC_HEADER_RE.match(line)
            if header:
                current_alias, current_func_id = header.groups()
                continue
            for alias in CALL_RE.findall(line):
                if alias not in alias_to_api_names:
                    continue
                if alias == current_alias:
                    continue
                caller_methods = tuple(func_to_methods.get(current_func_id, []))
                callsites.append(
                    CallSite(
                        line=line_no,
                        api_names=tuple(sorted(alias_to_api_names[alias])),
                        api_func_id=alias_to_api_func[alias],
                        api_alias=alias,
                        caller_func_id=current_func_id,
                        caller_alias=current_alias,
                        caller_methods=caller_methods,
                        source=line.strip(),
                    )
                )
    return callsites


def classify_callsite(site: CallSite) -> str:
    joined = " ".join(site.caller_methods)
    if "CurlingStoneNew" in joined:
        return "formal_stone"
    if "CrossLineEvent" in joined or "GameControll" in joined or "GameController" in joined:
        return "formal_game"
    if "RosSharp.Urdf" in joined:
        return "urdf_unrelated"
    if "MotionTest" in joined or "DragRigidbody" in joined:
        return "dev_or_demo"
    if site.caller_methods:
        return "other_managed"
    return "unknown_native_or_helper"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--script-json",
        type=Path,
        default=Path(r"D:\esp\tmp\curling_reverse_il2cpp\il2cpp_out\script.json"),
    )
    parser.add_argument(
        "--table-map",
        type=Path,
        default=Path(r"D:\esp\tmp\curling_reverse_il2cpp\wasm_table_map.json"),
    )
    parser.add_argument(
        "--decompile",
        type=Path,
        default=Path(r"D:\esp\tmp\curling_reverse_il2cpp\build.dcmp"),
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    script_methods = load_script_methods(args.script_json)
    table_map = load_table_map(args.table_map)
    alias_to_func, func_to_alias = load_decompile_aliases(args.decompile)
    target_refs = resolve_methods(script_methods, table_map, func_to_alias, TARGET_RIGIDBODY_METHODS)
    func_to_methods = build_func_method_index(script_methods, table_map)
    callsites = scan_calls(args.decompile, alias_to_func, func_to_methods, target_refs)

    if args.json:
        print(
            json.dumps(
                {
                    "targets": [ref.__dict__ for ref in target_refs],
                    "callsites": [
                        {
                            **site.__dict__,
                            "api_names": list(site.api_names),
                            "caller_methods": list(site.caller_methods),
                            "category": classify_callsite(site),
                        }
                        for site in callsites
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print("Resolved Rigidbody mass/COM/inertia APIs:")
    for ref in target_refs:
        print(f"- {ref.name}: table={ref.address} wasm={ref.func_id} alias={ref.alias}")

    print("\nCall sites:")
    for site in callsites:
        methods = ", ".join(site.caller_methods) if site.caller_methods else "<unmapped>"
        api_names = " / ".join(site.api_names)
        print(
            f"- line {site.line}: {api_names} via {site.api_func_id}/{site.api_alias} "
            f"from {site.caller_func_id}/{site.caller_alias} [{classify_callsite(site)}]"
        )
        print(f"  caller: {methods}")
        print(f"  source: {site.source}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
