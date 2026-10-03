"""Instrument selected *direct* Wasm calls without rewriting arithmetic.

Each selected function's byte-identical original body is appended as a new
function. Its old index becomes an argument/return forwarding thunk through a
new table slot. The runtime probe can hook that slot, including calls which
never went through Unity's original function table. Original indices/slots,
memory, globals, data and unselected bodies are preserved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEFAULT_FUNCTIONS = [70030, 70031, 70485, 70494, 69939, 69978, 69979,
                     70050, 70051, 70054, 70056, 69975, 69976, 70052,
                     70055, 70057, 70058, 70059, 70060, 70061, 70062,
                     70179, 69896, 69972, 69977, 70053]


def uleb(value: int) -> bytes:
    out = bytearray()
    while True:
        part = value & 127
        value >>= 7
        out.append(part | (128 if value else 0))
        if not value:
            return bytes(out)


def sleb(value: int) -> bytes:
    out = bytearray()
    while True:
        part = value & 127
        value >>= 7
        done = (value == 0 and not part & 64) or (value == -1 and part & 64)
        out.append(part | (0 if done else 128))
        if done:
            return bytes(out)


class Reader:
    def __init__(self, data: bytes):
        self.data, self.pos = data, 0

    def byte(self) -> int:
        value = self.data[self.pos]
        self.pos += 1
        return value

    def uint(self) -> int:
        value = shift = 0
        while True:
            part = self.byte()
            value |= (part & 127) << shift
            if part < 128:
                return value
            shift += 7

    def take(self, length: int) -> bytes:
        value = self.data[self.pos:self.pos + length]
        self.pos += length
        if len(value) != length:
            raise ValueError("truncated Wasm")
        return value

    def name(self) -> bytes:
        return self.take(self.uint())


def sections(data: bytes) -> list[tuple[int, bytes]]:
    if data[:8] != b"\0asm\x01\0\0\0":
        raise ValueError("not a Wasm v1 module")
    reader = Reader(data)
    reader.pos = 8
    out = []
    while reader.pos < len(data):
        kind, length = reader.byte(), reader.uint()
        out.append((kind, reader.take(length)))
    return out


def instrument(data: bytes, function_ids: list[int]) -> tuple[bytes, dict]:
    if len(set(function_ids)) != len(function_ids):
        raise ValueError("duplicate function index")
    original = sections(data)
    by_id = {kind: payload for kind, payload in original if kind}
    types_reader = Reader(by_id[1])
    types = []
    for _ in range(types_reader.uint()):
        if types_reader.byte() != 0x60:
            raise ValueError("non-function type unsupported")
        params = list(types_reader.take(types_reader.uint()))
        results = list(types_reader.take(types_reader.uint()))
        types.append((params, results))
    import_reader = Reader(by_id[2])
    imported_functions = 0
    for _ in range(import_reader.uint()):
        import_reader.name()
        import_reader.name()
        kind = import_reader.byte()
        if kind == 0:
            import_reader.uint()
            imported_functions += 1
        else:
            raise ValueError("this instrumenter requires function-only imports")
    function_reader = Reader(by_id[3])
    type_ids = [function_reader.uint() for _ in range(function_reader.uint())]
    code_reader = Reader(by_id[10])
    bodies = [code_reader.take(code_reader.uint()) for _ in range(code_reader.uint())]
    if len(bodies) != len(type_ids):
        raise ValueError("function/code length mismatch")
    table_reader = Reader(by_id[4])
    if table_reader.uint() != 1 or table_reader.byte() != 0x70:
        raise ValueError("requires one funcref table")
    limits_flags = table_reader.uint()
    table_min = table_reader.uint()
    table_max = table_reader.uint() if limits_flags == 1 else None
    if limits_flags not in (0, 1) or table_reader.pos != len(table_reader.data):
        raise ValueError("unsupported table limits")
    elem_reader = Reader(by_id[9])
    old_elem_count = elem_reader.uint()
    elem_remainder = elem_reader.data[elem_reader.pos:]
    count = len(function_ids)
    appended_bodies, appended_types, records = [], [], []
    alphabet = {0x7f: "i", 0x7e: "j", 0x7d: "f", 0x7c: "d"}
    original_function_count = imported_functions + len(type_ids)
    for offset, fid in enumerate(function_ids):
        body_index = fid - imported_functions
        if not 0 <= body_index < len(bodies):
            raise ValueError(f"function {fid} out of range")
        type_id = type_ids[body_index]
        params, results = types[type_id]
        if len(results) > 1:
            raise ValueError("multiple return values unsupported")
        signature = (alphabet[results[0]] if results else "v") + "".join(alphabet[p] for p in params)
        slot = table_min + offset
        raw_index = original_function_count + offset
        body = bodies[body_index]
        appended_bodies.append(body)
        appended_types.append(type_id)
        # zero local declarations; forward every parameter; indirect call; end.
        thunk = bytearray(b"\0")
        for parameter in range(len(params)):
            thunk += b"\x20" + uleb(parameter)
        thunk += b"\x41" + sleb(slot) + b"\x11" + uleb(type_id) + b"\0\x0b"
        bodies[body_index] = bytes(thunk)
        records.append({"functionIndex": fid, "rawFunctionIndex": raw_index,
                        "tableIndex": slot, "typeIndex": type_id, "signature": signature,
                        "originalBodySha256": hashlib.sha256(body).hexdigest(),
                        "originalBodyBytes": len(body)})
    new_table = uleb(1) + b"\x70" + uleb(limits_flags) + uleb(table_min + count)
    if table_max is not None:
        new_table += uleb(table_max + count)
    new_elem = (uleb(old_elem_count + 1) + elem_remainder + b"\0\x41" + sleb(table_min)
                + b"\x0b" + uleb(count)
                + b"".join(uleb(r["rawFunctionIndex"]) for r in records))
    all_bodies = bodies + appended_bodies
    replacements = {
        3: uleb(len(type_ids) + count) + b"".join(uleb(i) for i in type_ids + appended_types),
        4: new_table,
        9: new_elem,
        10: uleb(len(all_bodies)) + b"".join(uleb(len(b)) + b for b in all_bodies),
    }
    patched = data[:8] + b"".join(bytes([kind]) + uleb(len(replacements.get(kind, payload)))
                                   + replacements.get(kind, payload) for kind, payload in original)
    return patched, {"sourceSha256": hashlib.sha256(data).hexdigest(),
                     "patchedSha256": hashlib.sha256(patched).hexdigest(),
                     "importedFunctions": imported_functions,
                     "originalTableSize": table_min, "functions": records,
                     "method": "byte-identical relocated body with argument/return table thunk"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("analysis_input/unity_20260930.wasm"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--functions", type=int, nargs="+", default=DEFAULT_FUNCTIONS)
    args = parser.parse_args()
    if args.output.exists() or args.output.with_suffix(".json").exists():
        raise FileExistsError(args.output)
    patched, manifest = instrument(args.source.read_bytes(), args.functions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(patched)
    manifest.update(source=str(args.source.resolve()), patched=str(args.output.resolve()))
    args.output.with_suffix(".json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
