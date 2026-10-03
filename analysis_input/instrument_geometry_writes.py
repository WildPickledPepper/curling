"""Watch actual writes to a live convex geometry, reporting the writer function.

All numeric store instructions retain their original value/address semantics.
Small typed Wasm helpers perform the store then report only addresses inside
two explicitly armed globals. No guesses about the scale producer are needed.
"""
import argparse
import hashlib
import json
from pathlib import Path

from instrument_pcm_calls import Reader, sections, uleb, sleb, instrument

STORE_TYPES = {0x36: 0x7f, 0x37: 0x7e, 0x38: 0x7d, 0x39: 0x7c,
               0x3a: 0x7f, 0x3b: 0x7f, 0x3c: 0x7e, 0x3d: 0x7e, 0x3e: 0x7e}
ALIGNMENTS = {0x36: 2, 0x37: 3, 0x38: 2, 0x39: 3,
              0x3a: 0, 0x3b: 1, 0x3c: 0, 0x3d: 1, 0x3e: 2}


def instruction(reader):
    opcode = reader.byte()
    operand = None
    if opcode in (2, 3, 4, 0xd0, 0x41, 0x42):
        reader.uint()  # signed LEBs have identical byte boundaries
    elif opcode in (0x0c, 0x0d, 0x10, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x3f, 0x40, 0xd2):
        reader.uint()
    elif opcode == 0x0e:
        for _ in range(reader.uint() + 1):
            reader.uint()
    elif opcode == 0x11:
        reader.uint()
        reader.uint()
    elif opcode == 0x1c:
        reader.take(reader.uint())
    elif 0x28 <= opcode <= 0x3e:
        operand = (reader.uint(), reader.uint())
    elif opcode == 0x43:
        reader.take(4)
    elif opcode == 0x44:
        reader.take(8)
    elif opcode == 0xfc:
        sub = reader.uint()
        arity = {8: 2, 9: 1, 10: 2, 11: 1, 12: 2, 13: 1, 14: 2, 15: 1, 16: 1, 17: 1}
        if sub > 7 and sub not in arity:
            raise ValueError(f"unsupported bulk opcode {sub}")
        for _ in range(arity.get(sub, 0)):
            reader.uint()
    elif not (opcode in (0, 1, 5, 0x0b, 0x0f, 0x1a, 0x1b, 0xd1) or 0x45 <= opcode <= 0xc4):
        raise ValueError(f"unsupported opcode 0x{opcode:x}")
    return opcode, operand


def vec_append(payload, entries):
    reader = Reader(payload)
    count = reader.uint()
    return uleb(count + len(entries)) + payload[reader.pos:] + b"".join(entries)


def build(source):
    src_sections = sections(source)
    sec = dict(src_sections)
    import_reader = Reader(sec[2])
    import_count = import_reader.uint()
    for _ in range(import_count):
        import_reader.name(); import_reader.name()
        if import_reader.byte() != 0:
            raise ValueError("requires function-only imports")
        import_reader.uint()
    function_reader = Reader(sec[3])
    function_count = function_reader.uint()
    first_new_function = import_count + function_count
    old_type_count = Reader(sec[1]).uint()
    old_global_count = Reader(sec[6]).uint()
    if old_global_count != 1:
        raise ValueError("this instrumenter expects Unity's one internal global")
    start_global, end_global, caller_global = old_global_count, old_global_count + 1, old_global_count + 2
    table_reader = Reader(sec[4])
    if table_reader.uint() != 1 or table_reader.byte() != 0x70 or table_reader.uint() != 1:
        raise ValueError("requires one fixed-size funcref table")
    table_min, table_max = table_reader.uint(), table_reader.uint()
    helper_types, callback_types, type_entries = {}, {}, []
    for value_type in (0x7f, 0x7e, 0x7d, 0x7c):
        helper_types[value_type] = old_type_count + len(type_entries)
        type_entries.append(bytes([0x60, 4, 0x7f, value_type, 0x7f, 0x7f, 0]))
        callback_types[value_type] = old_type_count + len(type_entries)
        type_entries.append(bytes([0x60, 4, 0x7f, 0x7f, value_type, 0x7f, 0]))
    store_helpers, records, extra_bodies, extra_function_types = {}, [], [], []
    for ordinal, (opcode, value_type) in enumerate(STORE_TYPES.items()):
        helper_index = first_new_function + ordinal
        slot = table_min + ordinal
        store_helpers[opcode] = helper_index
        # One i32 local for the effective address.
        code = bytearray(b"\x01\x01\x7f")
        code += b"\x20\0\x20\x02\x6a\x22\x04\x20\x01"
        code += bytes([opcode]) + uleb(ALIGNMENTS[opcode]) + b"\0"
        code += b"\x20\x04\x23" + uleb(start_global) + b"\x4f"
        code += b"\x20\x04\x23" + uleb(end_global) + b"\x49\x71\x04\x40"
        code += b"\x20\x03\x20\x04\x20\x01\x41" + sleb(opcode)
        code += b"\x41" + sleb(slot) + b"\x11" + uleb(callback_types[value_type]) + b"\0\x0b\x0b"
        extra_bodies.append(bytes(code))
        extra_function_types.append(helper_types[value_type])
        char = {0x7f: "i", 0x7e: "j", 0x7d: "f", 0x7c: "d"}[value_type]
        records.append({"storeOpcode": opcode, "tableIndex": slot,
                        "signature": "vii" + char + "i", "helperFunctionIndex": helper_index})
    # Default callbacks are empty; JS replaces these table slots when armed.
    for opcode, value_type in STORE_TYPES.items():
        extra_bodies.append(b"\0\x0b")
        extra_function_types.append(callback_types[value_type])
    code_reader = Reader(sec[10])
    count = code_reader.uint()
    if count != function_count:
        raise ValueError("function/code count mismatch")
    bodies, store_count = [], 0
    for body_index in range(count):
        body = code_reader.take(code_reader.uint())
        reader = Reader(body)
        for _ in range(reader.uint()):
            reader.uint(); reader.byte()
        output = bytearray(body[:reader.pos])
        while reader.pos < len(body):
            begin = reader.pos
            opcode, operand = instruction(reader)
            if opcode in store_helpers:
                offset = operand[1]
                output += b"\x41" + sleb(offset) + b"\x41" + sleb(import_count + body_index)
                output += b"\x10" + uleb(store_helpers[opcode])
                store_count += 1
            else:
                if opcode in (0x10, 0x11):
                    output += b"\x41" + sleb(import_count + body_index) + b"\x24" + uleb(caller_global)
                output += body[begin:reader.pos]
        bodies.append(bytes(output))
    element_reader = Reader(sec[9])
    element_count = element_reader.uint()
    element_new = (b"\0\x41" + sleb(table_min) + b"\x0b" + uleb(len(records))
                   + b"".join(uleb(first_new_function + len(records) + i) for i in range(len(records))))
    export_entries = []
    for name, gid in (("probe_geometry_watch_start", start_global), ("probe_geometry_watch_end", end_global),
                      ("probe_last_call_caller", caller_global)):
        raw_name = name.encode()
        export_entries.append(uleb(len(raw_name)) + raw_name + b"\x03" + uleb(gid))
    all_bodies = bodies + extra_bodies
    replacement = {
        1: vec_append(sec[1], type_entries),
        3: vec_append(sec[3], [uleb(t) for t in extra_function_types]),
        4: b"\x01\x70\x01" + uleb(table_min + len(records)) + uleb(table_max + len(records)),
        6: vec_append(sec[6], [b"\x7f\x01\x41\0\x0b"] * 3),
        7: vec_append(sec[7], export_entries),
        9: uleb(element_count + 1) + sec[9][element_reader.pos:] + element_new,
        10: uleb(len(all_bodies)) + b"".join(uleb(len(b)) + b for b in all_bodies),
    }
    patched = source[:8] + b"".join(bytes([kind]) + uleb(len(replacement.get(kind, data)))
                                     + replacement.get(kind, data) for kind, data in src_sections)
    return patched, {"sourceSha256": hashlib.sha256(source).hexdigest(),
                     "patchedSha256": hashlib.sha256(patched).hexdigest(),
                     "functions": [], "writeHooks": records, "storeInstructions": store_count,
                     "method": "typed original numeric stores with guarded writer-index observation"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("analysis_input/unity_20260930.wasm"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace-functions", nargs="+", type=int)
    parser.add_argument("--geometry-root-functions", nargs="+", type=int,
                        help="Only enter function tracing through these construction roots")
    args = parser.parse_args()
    if args.output.exists() or args.output.with_suffix(".json").exists():
        raise FileExistsError(args.output)
    result, manifest = build(args.source.read_bytes())
    if args.trace_functions:
        result, function_manifest = instrument(result, args.trace_functions)
        manifest["functions"] = function_manifest["functions"]
        manifest["patchedSha256"] = hashlib.sha256(result).hexdigest()
        manifest["scope"] = "geometry-construction"
        if args.geometry_root_functions:
            manifest["geometryRootFunctions"] = args.geometry_root_functions
    args.output.write_bytes(result)
    manifest.update(source=str(args.source.resolve()), patched=str(args.output.resolve()))
    args.output.with_suffix(".json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k != "writeHooks"}))


if __name__ == "__main__":
    main()
