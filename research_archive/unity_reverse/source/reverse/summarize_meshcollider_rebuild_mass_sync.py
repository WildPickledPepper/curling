#!/usr/bin/env python3
"""Summarize MeshCollider rebuild -> Rigidbody mass-property sync evidence."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from extract_wat_data_string import _load_segments


DEFAULT_REVERSE_DIR = Path(r"D:\esp\tmp\curling_reverse_il2cpp")
MESH_COLLIDER_VTABLE = 3_221_476


def _load_memory(wat: Path) -> list[tuple[int, int, bytes]]:
    return _load_segments(wat.read_text(encoding="utf-8", errors="replace"))


def _read_u32(segments: list[tuple[int, int, bytes]], address: int) -> int | None:
    for start, end, data in segments:
        if start <= address <= end - 4:
            return struct.unpack_from("<I", data, address - start)[0]
    return None


def _func_id(marker: str | None) -> str:
    if not marker:
        return ""
    match = re.fullmatch(r"\$f(\d+)", marker)
    return f"func{match.group(1)}" if match else marker


def _has(text: str, pattern: str) -> str:
    return "yes" if pattern in text else "no"


def _extract_function(text: str, alias: str) -> str:
    pattern = re.compile(rf"^function {re.escape(alias)}\b.*?(?=^function |\Z)", re.M | re.S)
    match = pattern.search(text)
    return match.group(0) if match else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reverse-dir", type=Path, default=DEFAULT_REVERSE_DIR)
    args = parser.parse_args()

    reverse_dir = args.reverse_dir
    wat = reverse_dir / "build.wat"
    dcmp = reverse_dir / "build.dcmp"
    table_map_path = reverse_dir / "wasm_table_map.json"

    segments = _load_memory(wat)
    table_map = json.loads(table_map_path.read_text(encoding="utf-8"))
    text = dcmp.read_text(encoding="utf-8", errors="replace")

    print("MeshCollider native vtable:")
    for slot in (37, 38, 42):
        address = MESH_COLLIDER_VTABLE + slot * 4
        word = _read_u32(segments, address)
        marker = table_map.get(str(word)) if word is not None else None
        print(f"- slot[{slot}] @{address:#x}: table={word} {marker or ''} {_func_id(marker)}")

    func82533 = _extract_function(text, "f_jbrd")
    func72947 = _extract_function(text, "f_rwcd")
    func72951 = _extract_function(text, "f_vwcd")
    func73283 = _extract_function(text, "f_pjdd")
    func73284 = _extract_function(text, "f_qjdd")
    func73060 = _extract_function(text, "f_abdd")

    print("\nSetter/rebuild checks:")
    print(f"- MeshCollider.set_sharedMesh func82533 calls slot[37]: {_has(func82533, '(a[0]:int)[37]:int')}")
    print(f"- MeshCollider.set_convex helper func72947 calls slot[37]: {_has(func72947, '(a[0]:int)[37]:int')}")
    print(f"- rebuild func72951 clears old shape through slot[38]: {_has(func72951, '(a[0]:int)[38]:int')}")
    print(f"- rebuild func72951 convex path calls f_pjdd: {_has(func72951, 'f_pjdd(a, e + 8, d)')}")
    print(f"- shape attach func73283 searches Rigidbody via f_qjdd: {_has(func73283, 'f_qjdd(a, c)')}")
    print(f"- f_qjdd references native component id 4128948: {_has(func73284, '4128948')}")
    print(f"- shape attach func73283 calls f_abdd(e): {_has(func73283, 'f_abdd(e)')}")
    print(f"- f_abdd gates PxRigidBodyExt sync on m_Implicit flags: {_has(func73060, 'a[100]:ubyte | a[85]:ubyte')}")
    print(f"- f_abdd calls f_eqcd/setMassAndUpdateInertia: {_has(func73060, 'f_eqcd(')}")

    print("\nConclusion:")
    print(
        "runtime MeshCollider sharedMesh/convex rebuild reaches func72951; "
        "for convex stone shapes it reaches func73283 and calls f_abdd on the attached Rigidbody. "
        "With m_ImplicitTensor=true, f_abdd can recompute solver inertia from the rebuilt PhysX shapes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
