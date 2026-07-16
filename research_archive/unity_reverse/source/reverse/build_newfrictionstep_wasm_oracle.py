#!/usr/bin/env python3
"""Build standalone Wasm exports for Unity func59955 and func59956."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

try:
    from tools.reverse.build_fsimp_wasm_oracle import extract_function
except ModuleNotFoundError:  # Allows running this file directly.
    from build_fsimp_wasm_oracle import extract_function


DEFAULT_SOURCE = Path(r"D:\esp\tmp\curling_reverse_il2cpp\curlingmotion_real_funcs.wat")
DEFAULT_WAT = Path(r"D:\esp\tmp\curling_reverse_il2cpp\newfrictionstep_oracle.wat")
DEFAULT_WASM = Path(r"D:\esp\tmp\curling_reverse_il2cpp\newfrictionstep_oracle.wasm")
DEFAULT_WAT2WASM = Path(r"D:\esp\tmp\curling_wabt_tools\wabt-1.0.41\bin\wat2wasm.exe")


HELPERS = r"""
  (func $f61037 (param $p0 i32) (param $p1 f64) (param $p2 f64) (param $p3 i32)
    local.get $p0 local.get $p2 f64.store offset=8
    local.get $p0 local.get $p1 f64.store)
  (func $f61040 (param $p0 i32) (param $p1 i32) (result f64)
    local.get $p0 f64.load
    local.get $p0 f64.load
    f64.mul
    local.get $p0 f64.load offset=8
    local.get $p0 f64.load offset=8
    f64.mul
    f64.add
    f64.sqrt)
  (func $f61046 (param $p0 i32) (param $p1 f64) (param $p2 f64) (param $p3 f64) (param $p4 f64) (param $p5 f64) (param $p6 i32)
    local.get $p0 local.get $p5 f64.store offset=32
    local.get $p0 local.get $p4 f64.store offset=24
    local.get $p0 local.get $p3 f64.store offset=16
    local.get $p0 local.get $p2 f64.store offset=8
    local.get $p0 local.get $p1 f64.store)
"""


def module_text(fsimp: str, newfrictionstep: str) -> str:
    return "\n".join(
        [
            "(module",
            "  (type $t393 (func (param f64 f64 f64 i32 i32 i32 i32) (result f64)))",
            "  (type $t394 (func (param i32 f64 i32 f64 f64 i32)))",
            '  (import "env" "cos" (func $f5979 (param f64) (result f64)))',
            '  (import "env" "sin" (func $f5980 (param f64) (result f64)))',
            '  (import "env" "atan" (func $f54019 (param f64) (result f64)))',
            '  (import "env" "pow" (func $f56754 (param f64 f64 i32) (result f64)))',
            "  (func $f1661 (param i32))",
            "  (func $f65192 (param i32))",
            '  (memory (export "memory") 80)',
            "  (global $g0 (mut i32) (i32.const 5200000))",
            HELPERS,
            fsimp,
            newfrictionstep,
            '  (export "fsimp" (func $f59955))',
            '  (export "newfrictionstep" (func $f59956))',
            ")",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--wat", type=Path, default=DEFAULT_WAT)
    parser.add_argument("--wasm", type=Path, default=DEFAULT_WASM)
    parser.add_argument("--wat2wasm", type=Path, default=DEFAULT_WAT2WASM)
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    fsimp = extract_function(source, "f59955")
    newfrictionstep = extract_function(source, "f59956")
    args.wat.write_text(module_text(fsimp, newfrictionstep), encoding="utf-8")
    subprocess.run([str(args.wat2wasm), str(args.wat), "-o", str(args.wasm)], check=True)
    print(f"wrote {args.wat}")
    print(f"wrote {args.wasm}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
