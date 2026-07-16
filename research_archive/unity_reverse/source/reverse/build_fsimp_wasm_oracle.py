#!/usr/bin/env python3
"""Build a standalone Wasm oracle from Unity's original func59955 body."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


DEFAULT_SOURCE = Path(r"D:\esp\tmp\curling_reverse_il2cpp\curlingmotion_real_funcs.wat")
DEFAULT_WAT = Path(r"D:\esp\tmp\curling_reverse_il2cpp\fsimp_oracle.wat")
DEFAULT_WASM = Path(r"D:\esp\tmp\curling_reverse_il2cpp\fsimp_oracle.wasm")
DEFAULT_WAT2WASM = Path(r"D:\esp\tmp\curling_wabt_tools\wabt-1.0.41\bin\wat2wasm.exe")


def extract_function(source: str, name: str) -> str:
    marker = f"  (func ${name} "
    start = source.index(marker)
    depth = 0
    for offset, char in enumerate(source[start:], start):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[start : offset + 1]
    raise ValueError(f"unterminated Wasm function {name}")


def module_text(function: str) -> str:
    return "\n".join(
        [
            "(module",
            "  (type $t393 (func (param f64 f64 f64 i32 i32 i32 i32) (result f64)))",
            '  (import "env" "cos" (func $f5979 (param f64) (result f64)))',
            '  (import "env" "sin" (func $f5980 (param f64) (result f64)))',
            '  (import "env" "atan" (func $f54019 (param f64) (result f64)))',
            '  (import "env" "pow" (func $f56754 (param f64 f64 i32) (result f64)))',
            "  (func $f1661 (param i32))",
            "  (func $f65192 (param i32))",
            '  (memory (export "memory") 80)',
            function,
            '  (export "fsimp" (func $f59955))',
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
    function = extract_function(source, "f59955")
    args.wat.write_text(module_text(function), encoding="utf-8")
    subprocess.run(
        [str(args.wat2wasm), str(args.wat), "-o", str(args.wasm)],
        check=True,
    )
    print(f"wrote {args.wat}")
    print(f"wrote {args.wasm}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
