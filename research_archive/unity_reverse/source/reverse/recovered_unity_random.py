#!/usr/bin/env python3
"""Recovered UnityEngine.Random implementation from the WebGL build.

The competition player registers these native internal calls:

    UnityEngine.Random::InitState -> func82199
    UnityEngine.Random::Range     -> func82200
    UnityEngine.Random::get_value -> func82202
    UnityEngine.Random::get_seed  -> func82203

This module mirrors the recovered wasm logic closely enough for deterministic
simulation and sample analysis.
"""

from __future__ import annotations

import argparse
import struct
from dataclasses import dataclass


UINT32_MASK = 0xFFFFFFFF
RANDOM_MASK = 0x7FFFFF
RANDOM_SCALE = 1.0 / RANDOM_MASK
INIT_MULTIPLIER = 1812433253


def _u32(value: int) -> int:
    return value & UINT32_MASK


def _i32(value: int) -> int:
    value &= UINT32_MASK
    if value & 0x80000000:
        return value - 0x100000000
    return value


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", float(value)))[0]


@dataclass
class RecoveredUnityRandom:
    """Four-word xorshift-style UnityEngine.Random state recovered from wasm."""

    s0: int
    s1: int
    s2: int
    s3: int

    @classmethod
    def from_seed(cls, seed: int) -> "RecoveredUnityRandom":
        s0 = _u32(seed)
        s1 = _u32(_i32(s0) * INIT_MULTIPLIER + 1)
        s2 = _u32(_i32(s1) * INIT_MULTIPLIER + 1)
        s3 = _u32(_i32(s2) * INIT_MULTIPLIER + 1)
        return cls(s0, s1, s2, s3)

    def next_u32(self) -> int:
        old0 = self.s0
        old3 = self.s3
        self.s0, self.s1, self.s2 = self.s1, self.s2, self.s3

        x = _u32(old0 ^ _u32(old0 << 11))
        new3 = _u32(old3 ^ ((x >> 8) ^ x) ^ (old3 >> 19))
        self.s3 = new3
        return new3

    def value(self) -> float:
        return _f32(_f32(float(self.next_u32() & RANDOM_MASK)) * _f32(RANDOM_SCALE))

    def range_float(self, min_inclusive: float, max_inclusive: float) -> float:
        t = self.value()
        # The wasm evaluates min * t + (1 - t) * max. For symmetric noise this
        # is distribution-equivalent to min + t * (max - min), but not bitwise
        # identical for asymmetric ranges.
        return _f32(_f32(_f32(min_inclusive) * t) + _f32(_f32(1.0 - t) * _f32(max_inclusive)))

    def range_int(self, min_inclusive: int, max_exclusive: int) -> int:
        if min_inclusive < max_exclusive:
            return int(self.next_u32() % (max_exclusive - min_inclusive) + min_inclusive)
        if min_inclusive > max_exclusive:
            return int(min_inclusive - self.next_u32() % (min_inclusive - max_exclusive))
        return int(min_inclusive)

    def get_seed(self) -> int:
        return _i32(self.s0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seed", type=lambda value: int(value, 0))
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--min", type=float, default=-0.0002)
    parser.add_argument("--max", type=float, default=0.0002)
    args = parser.parse_args()

    rng = RecoveredUnityRandom.from_seed(args.seed)
    print(f"initial_state={rng.s0:#010x},{rng.s1:#010x},{rng.s2:#010x},{rng.s3:#010x}")
    for _ in range(args.count):
        print(rng.range_float(args.min, args.max))
    print(f"final_state={rng.s0:#010x},{rng.s1:#010x},{rng.s2:#010x},{rng.s3:#010x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
