#!/usr/bin/env python3
"""Bit-oriented translations of the libm routines embedded in Unity WebGL.

The Unity build's f5975/f5978/f5979/f5980/f54019 functions are musl's
double-precision cos kernel, sin kernel, cos, sin, and atan respectively.
These translations keep the Wasm operation order used by the recovered build.
The argument reducer covers the range used by CurlingMotion.fsimp.
"""

from __future__ import annotations

import math
import struct


_PIO4 = float.fromhex("0x1.921fb54442d18p-1")
_INVPIO2 = float.fromhex("0x1.45f306dc9c883p-1")
_PIO2_1 = float.fromhex("0x1.921fb544p+0")
_PIO2_1T = float.fromhex("0x1.0b4611a626331p-34")
_PIO2_2 = float.fromhex("0x1.0b4611a6p-34")
_PIO2_2T = float.fromhex("0x1.3198a2e037073p-69")
_PIO2_3 = float.fromhex("0x1.3198a2ep-69")
_PIO2_3T = float.fromhex("0x1.b839a252049c1p-104")
_TOINT = float.fromhex("0x1.8p+52")

_S1 = float.fromhex("-0x1.5555555555549p-3")
_S2 = float.fromhex("0x1.111111110f8a6p-7")
_S3 = float.fromhex("-0x1.a01a019c161d5p-13")
_S4 = float.fromhex("0x1.71de357b1fe7dp-19")
_S5 = float.fromhex("-0x1.ae5e68a2b9cebp-26")
_S6 = float.fromhex("0x1.5d93a5acfd57cp-33")

_C1 = float.fromhex("0x1.555555555554cp-5")
_C2 = float.fromhex("-0x1.6c16c16c15177p-10")
_C3 = float.fromhex("0x1.a01a019cb159p-16")
_C4 = float.fromhex("-0x1.27e4f809c52adp-22")
_C5 = float.fromhex("0x1.1ee9ebdb4b1c4p-29")
_C6 = float.fromhex("-0x1.8fae9be8838d4p-37")

_ATAN_HI = (
    float.fromhex("0x1.dac670561bb4fp-2"),
    float.fromhex("0x1.921fb54442d18p-1"),
    float.fromhex("0x1.f730bd281f69bp-1"),
    float.fromhex("0x1.921fb54442d18p+0"),
)
_ATAN_LO = (
    float.fromhex("0x1.a2b7f222f65e2p-56"),
    float.fromhex("0x1.1a62633145c07p-55"),
    float.fromhex("0x1.007887af0cbbdp-56"),
    float.fromhex("0x1.1a62633145c07p-54"),
)
_AT = (
    float.fromhex("0x1.555555555550dp-2"),
    float.fromhex("-0x1.999999998ebc4p-3"),
    float.fromhex("0x1.24924920083ffp-3"),
    float.fromhex("-0x1.c71c6fe231671p-4"),
    float.fromhex("0x1.745cdc54c206ep-4"),
    float.fromhex("-0x1.3b0f2af749a6dp-4"),
    float.fromhex("0x1.10d66a0d03d51p-4"),
    float.fromhex("-0x1.dde2d52defd9ap-5"),
    float.fromhex("0x1.97b4b24760debp-5"),
    float.fromhex("-0x1.2b4442c6a6c2fp-5"),
    float.fromhex("0x1.0ad3ae322da11p-6"),
)


def _bits(value: float) -> int:
    return struct.unpack("<Q", struct.pack("<d", value))[0]


def _high_abs(value: float) -> int:
    return (_bits(value) >> 32) & 0x7FFFFFFF


def _kernel_sin(x: float, y: float, tail_nonzero: bool) -> float:
    z = x * x
    w = z * z
    r_left = _S3 + z * _S4
    r_left = _S2 + z * r_left
    r_right = _S5 + z * _S6
    r = r_left + z * w * r_right
    v = z * x
    if not tail_nonzero:
        return x + v * (_S1 + z * r)
    correction = 0.5 * y - v * r
    correction = z * correction - y
    correction = correction - v * _S1
    return x - correction


def _kernel_cos(x: float, y: float) -> float:
    z = x * x
    left = _C2 + z * _C3
    left = _C1 + z * left
    left = z * left
    right = _C5 + z * _C6
    right = _C4 + z * right
    zz = z * z
    right = zz * zz * right
    r = left + right
    hz = 0.5 * z
    w = 1.0 - hz
    correction = (1.0 - w) - hz
    correction = correction + (z * r - x * y)
    return w + correction


def _rem_pio2_curling(x: float) -> tuple[int, float, float]:
    """Return n,y0,y1 for the bounded angles used by fsimp."""
    ix = _high_abs(x)
    sign = _bits(x) >> 63

    if ix <= 0x400F6A7A and (ix & 0xFFFFF) != 0x921FB:
        if ix <= 0x4002D97C:
            if not sign:
                z = x - _PIO2_1
                y0 = z - _PIO2_1T
                y1 = (z - y0) - _PIO2_1T
                return 1, y0, y1
            z = x + _PIO2_1
            y0 = z + _PIO2_1T
            y1 = (z - y0) + _PIO2_1T
            return -1, y0, y1
        if not sign:
            z = x - 2.0 * _PIO2_1
            y0 = z - 2.0 * _PIO2_1T
            y1 = (z - y0) - 2.0 * _PIO2_1T
            return 2, y0, y1
        z = x + 2.0 * _PIO2_1
        y0 = z + 2.0 * _PIO2_1T
        y1 = (z - y0) + 2.0 * _PIO2_1T
        return -2, y0, y1

    if ix >= 0x413921FB:
        raise ValueError("Unity fsimp angle exceeded the audited libm range")

    fn = x * _INVPIO2
    fn = (fn + _TOINT) - _TOINT
    n = int(fn)
    r = x - fn * _PIO2_1
    w = fn * _PIO2_1T
    reduced = r - w
    if reduced < -_PIO4:
        n -= 1
        fn -= 1.0
        r = x - fn * _PIO2_1
        w = fn * _PIO2_1T
    elif reduced > _PIO4:
        n += 1
        fn += 1.0
        r = x - fn * _PIO2_1
        w = fn * _PIO2_1T

    y0 = r - w
    ey = (_bits(y0) >> 52) & 0x7FF
    ex = ix >> 20
    if ex - ey > 16:
        t = r
        w = fn * _PIO2_2
        r = t - w
        w = fn * _PIO2_2T - ((t - r) - w)
        y0 = r - w
        ey = (_bits(y0) >> 52) & 0x7FF
        if ex - ey > 49:
            t = r
            w = fn * _PIO2_3
            r = t - w
            w = fn * _PIO2_3T - ((t - r) - w)
            y0 = r - w
    y1 = (r - y0) - w
    return n, y0, y1


def sin(x: float) -> float:
    ix = _high_abs(x)
    if ix <= 0x3FE921FB:
        if ix < 0x3E500000:
            return x
        return _kernel_sin(x, 0.0, False)
    if ix >= 0x7FF00000:
        return x - x
    n, y0, y1 = _rem_pio2_curling(x)
    quadrant = n & 3
    if quadrant == 0:
        return _kernel_sin(y0, y1, True)
    if quadrant == 1:
        return _kernel_cos(y0, y1)
    if quadrant == 2:
        return -_kernel_sin(y0, y1, True)
    return -_kernel_cos(y0, y1)


def cos(x: float) -> float:
    ix = _high_abs(x)
    if ix <= 0x3FE921FB:
        if ix < 0x3E46A09E:
            return 1.0
        return _kernel_cos(x, 0.0)
    if ix >= 0x7FF00000:
        return x - x
    n, y0, y1 = _rem_pio2_curling(x)
    quadrant = n & 3
    if quadrant == 0:
        return _kernel_cos(y0, y1)
    if quadrant == 1:
        return -_kernel_sin(y0, y1, True)
    if quadrant == 2:
        return -_kernel_cos(y0, y1)
    return _kernel_sin(y0, y1, True)


def atan(x: float) -> float:
    bits = _bits(x)
    ix = (bits >> 32) & 0x7FFFFFFF
    negative = bool(bits >> 63)
    if ix >= 0x44100000:
        if math.isnan(x):
            return x
        return math.copysign(_ATAN_HI[3], x)

    if ix < 0x3FDC0000:
        if ix < 0x3E400000:
            return x
        ident = -1
    else:
        x = abs(x)
        if ix < 0x3FF30000:
            if ix < 0x3FE60000:
                ident = 0
                x = (2.0 * x - 1.0) / (2.0 + x)
            else:
                ident = 1
                x = (x - 1.0) / (x + 1.0)
        elif ix < 0x40038000:
            ident = 2
            x = (x - 1.5) / (1.0 + 1.5 * x)
        else:
            ident = 3
            x = -1.0 / x

    z = x * x
    w = z * z
    s2 = _AT[9] * w + _AT[7]
    s2 = s2 * w + _AT[5]
    s2 = s2 * w + _AT[3]
    s2 = s2 * w + _AT[1]
    s2 = w * s2
    s1 = _AT[10] * w + _AT[8]
    s1 = s1 * w + _AT[6]
    s1 = s1 * w + _AT[4]
    s1 = s1 * w + _AT[2]
    s1 = s1 * w + _AT[0]
    s1 = z * s1
    poly = s1 + s2
    if ident < 0:
        return x - x * poly
    result = x * poly
    result = result - _ATAN_LO[ident]
    result = result - x
    result = _ATAN_HI[ident] - result
    return -result if negative else result

