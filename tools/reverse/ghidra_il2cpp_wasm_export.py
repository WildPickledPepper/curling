# PyGhidra script for Unity WebGL IL2CPP wasm exports.
#
# Usage from analyzeHeadless:
#   pyghidraRun.bat -H <project_dir> <project_name> -process build.wasm \
#     -scriptPath <this_dir>;<ghidra_wasm_plugin_scripts> \
#     -postScript ghidra_il2cpp_wasm_export.py <script.json> <output.md> [table_map.json]
#
# The script labels wasm table functions using Il2CppDumper script.json and
# exports decompiler output plus a compact instruction listing for CurlingMotion.

from __future__ import print_function

import json
import sys

from ghidra.app.decompiler import DecompInterface
from ghidra.program.model.symbol import SourceType
from ghidra.util.task import ConsoleTaskMonitor

from wasm import WasmLoader
from wasm.analysis import WasmAnalysis


TARGET_SUBSTRINGS = [
    "Assets.CurlingMotion$$fdx",
    "Assets.CurlingMotion$$fwx",
    "Assets.CurlingMotion$$fdy",
    "Assets.CurlingMotion$$fwy",
    "Assets.CurlingMotion$$fda",
    "Assets.CurlingMotion$$fwa",
    "Assets.CurlingMotion$$fsimp",
    "Assets.CurlingMotion$$Newfrictionstep",
]


def _as_text(value):
    if value is None:
        return ""
    return str(value)


def _load_table():
    monitor = ConsoleTaskMonitor()
    state = WasmAnalysis.getState(currentProgram)
    WasmLoader.loadElementsToTable(currentProgram, state.module, 0, 0, 0, monitor)


def _find_function_by_wasm_symbol(wasm_symbol):
    if not wasm_symbol:
        return None
    ordinal = wasm_symbol.replace("$f", "").replace("f", "", 1)
    candidate_names = [
        wasm_symbol,
        wasm_symbol.replace("$", ""),
        "unnamed_function_" + ordinal,
        "func_" + ordinal,
    ]
    for candidate in candidate_names:
        try:
            funcs = list(getGlobalFunctions(candidate))
            if funcs:
                return funcs[0]
        except Exception:
            pass
        try:
            symbols = currentProgram.symbolTable.getGlobalSymbols(candidate)
            for symbol in symbols:
                func = getFunctionAt(symbol.address)
                if func is not None:
                    return func
        except Exception:
            pass
    return None


def _next_function_after(func):
    if func is None:
        return None
    found = False
    for candidate in currentProgram.functionManager.getFunctions(True):
        if found:
            return candidate
        if candidate.entryPoint == func.entryPoint:
            found = True
    return None


def _label_script_methods(script_json_path, table_map_path=None):
    with open(script_json_path, "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    table_map = {}
    if table_map_path:
        with open(table_map_path, "rb") as f:
            table_map = json.loads(f.read().decode("utf-8"))

    symbol_table = currentProgram.symbolTable
    user_defined = SourceType.USER_DEFINED
    progspace = currentProgram.addressFactory.getAddressSpace("ram")
    tablespace = currentProgram.addressFactory.getAddressSpace("table")
    renamed = []
    missing = []
    last_ordinal = None
    last_func = None

    for method in data.get("ScriptMethod", []):
        name = method.get("Name", "")
        if "CurlingMotion" not in name:
            continue
        table_index = int(method.get("Address"))
        func = None
        func_addr = None
        wasm_symbol = table_map.get(str(table_index))
        ordinal = None
        if wasm_symbol:
            try:
                ordinal = int(wasm_symbol.replace("$f", ""))
            except Exception:
                ordinal = None
            func = _find_function_by_wasm_symbol(wasm_symbol)
            if func is None and ordinal is not None and last_ordinal is not None and ordinal == last_ordinal + 1:
                func = _next_function_after(last_func)
            if func is not None:
                func_addr = func.entryPoint

        try:
            if func is None:
                func_addr_raw = getInt(tablespace.getAddress(table_index * 4)) & 0xffffffff
                func_addr = progspace.getAddress(func_addr_raw)
                func = getFunctionAt(func_addr)
        except Exception as exc:
            missing.append((name, "table[%d]: %s" % (table_index, exc)))
            continue

        label_name = name.replace(" ", "-")
        createLabel(func_addr, label_name, True, user_defined)
        if func is not None:
            try:
                func.setName(label_name, user_defined)
            except Exception:
                pass
        else:
            try:
                func = createFunction(func_addr, label_name)
            except Exception:
                func = None
        if ordinal is not None:
            last_ordinal = ordinal
            last_func = func
        renamed.append((name, "%s table[%d]" % (wasm_symbol or "", table_index), func_addr))

    return renamed, missing


def _target_functions():
    funcs = []
    for func in currentProgram.functionManager.getFunctions(True):
        name = func.name
        for needle in TARGET_SUBSTRINGS:
            if needle in name:
                funcs.append(func)
                break
    funcs.sort(key=lambda f: str(f.entryPoint))
    return funcs


def _decompile(func):
    ifc = DecompInterface()
    ifc.openProgram(currentProgram)
    result = ifc.decompileFunction(func, 90, monitor)
    if result is None or not result.decompileCompleted():
        return None
    return result.getDecompiledFunction().getC()


def _listing(func, max_insts):
    lines = []
    insts = currentProgram.listing.getInstructions(func.body, True)
    count = 0
    for inst in insts:
        if count >= max_insts:
            lines.append("    ...")
            break
        lines.append("    %s: %s" % (inst.address, inst.toString()))
        count += 1
    return "\n".join(lines)


def _write_export(output_path, renamed, missing):
    funcs = []
    seen = set()
    for name, source, addr in renamed:
        if not any(needle in name for needle in TARGET_SUBSTRINGS):
            continue
        key = str(addr)
        if key in seen:
            continue
        func = getFunctionAt(addr)
        if "Newfrictionstep" in name and func is not None and "ctor" in func.name:
            next_func = _next_function_after(func)
            if next_func is not None:
                func = next_func
                key = str(func.entryPoint)
        if func is not None:
            funcs.append((name, source, func))
            seen.add(key)
    with open(output_path, "wb") as out:
        out.write(("# Ghidra CurlingMotion Export\n\n").encode("utf-8"))
        out.write(("Program: `%s`\n\n" % currentProgram.name).encode("utf-8"))
        out.write(("Renamed CurlingMotion methods: `%d`\n\n" % len(renamed)).encode("utf-8"))
        out.write(("## Method Map\n\n").encode("utf-8"))
        for name, source, addr in renamed:
            out.write(("- `%s` -> `%s` @ `%s`\n" % (_as_text(name), _as_text(source), _as_text(addr))).encode("utf-8"))
        out.write(("\n").encode("utf-8"))
        if missing:
            out.write(("Missing mappings: `%d`\n\n" % len(missing)).encode("utf-8"))
            for name, symbol in missing:
                out.write(("- `%s` expected `%s`\n" % (_as_text(name), _as_text(symbol))).encode("utf-8"))
            out.write(("\n").encode("utf-8"))

        out.write(("Target functions found: `%d`\n\n" % len(funcs)).encode("utf-8"))
        for display_name, source, func in funcs:
            out.write(("## %s @ %s\n\n" % (_as_text(display_name), func.entryPoint)).encode("utf-8"))
            out.write(("Source: `%s`; Ghidra name: `%s`\n\n" % (_as_text(source), _as_text(func.name))).encode("utf-8"))
            c_text = _decompile(func)
            if c_text:
                out.write(("```c\n%s\n```\n\n" % c_text).encode("utf-8"))
            else:
                out.write(("Decompiler did not complete for this function.\n\n").encode("utf-8"))
            out.write(("```asm\n%s\n```\n\n" % _listing(func, 260)).encode("utf-8"))


args = getScriptArgs()
if len(args) < 2:
    print("usage: ghidra_il2cpp_wasm_export.py <script.json> <output.md> [table_map.json]")
    sys.exit(1)

script_json_path = args[0]
output_path = args[1]
table_map_path = args[2] if len(args) > 2 else None

_load_table()
renamed, missing = _label_script_methods(script_json_path, table_map_path)
print("Renamed %d CurlingMotion methods; missing %d" % (len(renamed), len(missing)))
_write_export(output_path, renamed, missing)
print("Wrote " + output_path)
