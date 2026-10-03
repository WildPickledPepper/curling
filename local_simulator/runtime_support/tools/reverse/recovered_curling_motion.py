#!/usr/bin/env python3
"""Recovered Unity CurlingMotion model prototype.

This is a direct Python translation of the formulas recovered from the Unity
WebGL IL2CPP wasm functions:

- func59955: Assets.CurlingMotion.fsimp
- func59956: Assets.CurlingMotion.Newfrictionstep

It is intentionally standalone and not wired into training yet. The purpose is
to validate the reverse-engineered equations against Unity traces first.
"""

from __future__ import annotations

import argparse
import math
import random
import struct
from dataclasses import dataclass
from typing import List, Optional, Protocol, Union

try:
    from tools.reverse.recovered_unity_random import RecoveredUnityRandom
except ModuleNotFoundError:  # Allows running this file directly from tools/reverse.
    from recovered_unity_random import RecoveredUnityRandom


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", float(value)))[0]


# C# float literals are promoted to f64 at the recovered method boundary.
PI = float.fromhex("0x1.921ff2p+1")
R = 0.125
DR = 0.006
R1 = float.fromhex("0x1.f3b646p-4")
R2 = float.fromhex("0x1.0624dep-3")
K = float.fromhex("0x1.99999ap-3")
WET_K = float.fromhex("0x1.99999ap-4")
MASS = 19.0
INERTIA = 0.399475
UNITY_FIXED_TIMESTEP = 0.01
NEWFRICTIONSTEP_PARAM = float.fromhex("0x1.0624dep-10")
STEP = NEWFRICTIONSTEP_PARAM
EPS = 1e-5
BASE_FRICTION = float.fromhex("0x1.0624dep-10")
SWEEP_FRICTION = float.fromhex("0x1.3a92a4p-11")
FRICTION_NOISE = _f32(0.0002)
ANGLE_FALLBACK = float.fromhex("0x1.47ae14p-7")
ANGLE_EPS = float.fromhex("0x1.0c6f7ap-20")
FSIMP_SAFETY_MAX_ITERATIONS = 24
_sin = math.sin
_cos = math.cos
_atan = math.atan
SUPPORTED_KERNELS = tuple(
    [(1, index) for index in range(1, 8)]
    + [(2, index) for index in range(1, 8)]
    + [(3, index) for index in range(1, 9)]
)


class UnityRangeFloatRng(Protocol):
    def range_float(self, min_inclusive: float, max_inclusive: float) -> float: ...


@dataclass(frozen=True)
class B2Vec2:
    x: float
    y: float


@dataclass(frozen=True)
class Speed:
    v: B2Vec2
    angle: float


@dataclass(frozen=True)
class MyParams:
    vx: float
    vy: float
    w: float
    r1: float
    r2: float


@dataclass(frozen=True)
class FsimpDiagnostics:
    value: float
    iterations: int
    converged: bool


def _atan_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0.0:
        if numerator == 0.0:
            return _atan(float("nan"))
        return _atan(math.copysign(math.inf, numerator))
    return _atan(numerator / denominator)


def _local(x: float, p: MyParams, radius: float, numerator_mode: str, denom_sign: float):
    s = _sin(x)
    c = _cos(x)
    spin_radius = p.w * radius
    sin_term = s * spin_radius
    cos_term = c * spin_radius
    if numerator_mode == "plus":
        a = p.vx + sin_term
    elif numerator_mode == "minus":
        a = sin_term - p.vx
    else:
        raise ValueError(numerator_mode)
    b = p.vy + denom_sign * cos_term
    theta = _atan_ratio(a, b)
    speed_sq = a * a + b * b
    return a, b, theta, speed_sq


def integrand(type_: int, i: int, x: float, p: MyParams) -> float:
    if type_ == 1:
        if i == 1:
            return _sin(_local(x, p, p.r2, "plus", 1.0)[2]) + _sin(
                _local(x, p, p.r2, "plus", -1.0)[2]
            )
        if i == 2:
            return _sin(_local(x, p, p.r1, "minus", 1.0)[2]) + _sin(
                _local(x, p, p.r1, "minus", -1.0)[2]
            )
        if i == 3:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", 1.0)
            return speed_sq * _sin(theta)
        if i == 4:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", -1.0)
            return speed_sq * _sin(theta)
        if i == 5:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", 1.0)
            return speed_sq * _sin(theta)
        if i == 6:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", -1.0)
            return speed_sq * _sin(theta)
        if i == 7:
            return _sin(_local(x, p, p.r2, "plus", -1.0)[2])

    if type_ == 2:
        if i == 1:
            return _cos(_local(x, p, p.r2, "plus", 1.0)[2]) + _cos(
                _local(x, p, p.r2, "plus", -1.0)[2]
            )
        if i == 2:
            return _cos(_local(x, p, p.r1, "minus", 1.0)[2]) + _cos(
                _local(x, p, p.r1, "minus", -1.0)[2]
            )
        if i == 3:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", 1.0)
            return speed_sq * _cos(theta)
        if i == 4:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", -1.0)
            return speed_sq * _cos(theta)
        if i == 5:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", 1.0)
            return speed_sq * _cos(theta)
        if i == 6:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", -1.0)
            return speed_sq * _cos(theta)
        if i == 7:
            return _cos(_local(x, p, p.r2, "plus", -1.0)[2])

    if type_ == 3:
        if i == 1:
            theta = _local(x, p, p.r2, "plus", 1.0)[2]
            return _sin(x + PI / 2.0 - theta)
        if i == 2:
            theta = _local(x, p, p.r2, "plus", -1.0)[2]
            return _sin(x + PI / 2.0 + theta)
        if i == 3:
            theta = _local(x, p, p.r1, "minus", 1.0)[2]
            return _sin(PI / 2.0 - x + theta)
        if i == 4:
            theta = _local(x, p, p.r1, "minus", -1.0)[2]
            return _sin(PI / 2.0 - x - theta)
        if i == 5:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", 1.0)
            return speed_sq * _sin(x + PI / 2.0 - theta)
        if i == 6:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", -1.0)
            return speed_sq * _sin(x + PI / 2.0 + theta)
        if i == 7:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", 1.0)
            return speed_sq * _sin(PI / 2.0 - x + theta)
        if i == 8:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", -1.0)
            return speed_sq * _sin(PI / 2.0 - x - theta)

    raise ValueError(f"unsupported integrand type={type_} i={i}")


def integrand_direct_trig(type_: int, i: int, x: float, p: MyParams) -> float:
    """Fast algebraic form of :func:`integrand` used by the native batch kernel.

    ``theta`` in the recovered formula is ``atan(a / b)`` and is only consumed
    by ``sin`` or ``cos``.  The native hot path therefore derives those values
    from ``a / b`` directly.  This reference form exists solely for numerical
    regression tests; the recovered, literal form above remains authoritative.
    """

    sine = _sin(x)
    cosine = _cos(x)
    half_pi_sine = _sin(PI / 2.0)
    half_pi_cosine = _cos(PI / 2.0)

    def local(radius: float, numerator_mode: str, denom_sign: float):
        spin_radius = p.w * radius
        if numerator_mode == "plus":
            a = p.vx + sine * spin_radius
        elif numerator_mode == "minus":
            a = sine * spin_radius - p.vx
        else:
            raise ValueError(f"unsupported numerator mode={numerator_mode!r}")
        b = p.vy + denom_sign * cosine * spin_radius
        speed_sq = a * a + b * b
        if b == 0.0:
            if a == 0.0:
                return float("nan"), float("nan"), speed_sq
            return math.copysign(1.0, a), 0.0, speed_sq
        ratio = a / b
        cos_theta = 1.0 / math.sqrt(1.0 + ratio * ratio)
        return ratio * cos_theta, cos_theta, speed_sq

    def minus_theta_forward(value):
        sin_theta, cos_theta, _ = value
        angle_sine = sine * cos_theta - cosine * sin_theta
        angle_cosine = cosine * cos_theta + sine * sin_theta
        return half_pi_sine * angle_cosine + half_pi_cosine * angle_sine

    def plus_theta_forward(value):
        sin_theta, cos_theta, _ = value
        angle_sine = sine * cos_theta + cosine * sin_theta
        angle_cosine = cosine * cos_theta - sine * sin_theta
        return half_pi_sine * angle_cosine + half_pi_cosine * angle_sine

    def minus_theta_reverse(value):
        sin_theta, cos_theta, _ = value
        angle_sine = sine * cos_theta - cosine * sin_theta
        angle_cosine = cosine * cos_theta + sine * sin_theta
        return half_pi_sine * angle_cosine - half_pi_cosine * angle_sine

    def plus_theta_reverse(value):
        sin_theta, cos_theta, _ = value
        angle_sine = sine * cos_theta + cosine * sin_theta
        angle_cosine = cosine * cos_theta - sine * sin_theta
        return half_pi_sine * angle_cosine - half_pi_cosine * angle_sine

    if type_ == 1:
        if i == 1:
            return local(p.r2, "plus", 1.0)[0] + local(p.r2, "plus", -1.0)[0]
        if i == 2:
            return local(p.r1, "minus", 1.0)[0] + local(p.r1, "minus", -1.0)[0]
        radial = {
            3: (p.r1, "plus", 1.0),
            4: (p.r1, "plus", -1.0),
            5: (p.r2, "minus", 1.0),
            6: (p.r2, "minus", -1.0),
            7: (p.r2, "plus", -1.0),
        }
        value = local(*radial[i])
        return value[0] if i == 7 else value[2] * value[0]

    if type_ == 2:
        if i == 1:
            return local(p.r2, "plus", 1.0)[1] + local(p.r2, "plus", -1.0)[1]
        if i == 2:
            return local(p.r1, "minus", 1.0)[1] + local(p.r1, "minus", -1.0)[1]
        radial = {
            3: (p.r1, "plus", 1.0),
            4: (p.r1, "plus", -1.0),
            5: (p.r2, "minus", 1.0),
            6: (p.r2, "minus", -1.0),
            7: (p.r2, "plus", -1.0),
        }
        value = local(*radial[i])
        return value[1] if i == 7 else value[2] * value[1]

    if type_ == 3:
        angular = {
            1: (p.r2, "plus", 1.0, minus_theta_forward),
            2: (p.r2, "plus", -1.0, plus_theta_forward),
            3: (p.r1, "minus", 1.0, minus_theta_reverse),
            4: (p.r1, "minus", -1.0, plus_theta_reverse),
            5: (p.r1, "plus", 1.0, minus_theta_forward),
            6: (p.r1, "plus", -1.0, plus_theta_forward),
            7: (p.r2, "minus", 1.0, minus_theta_reverse),
            8: (p.r2, "minus", -1.0, plus_theta_reverse),
        }
        radius, numerator_mode, denom_sign, transform = angular[i]
        value = local(radius, numerator_mode, denom_sign)
        result = transform(value)
        return result if i < 5 else value[2] * result

    raise ValueError(f"unsupported integrand type={type_} i={i}")


def fsimp_diagnostics(
    a: float,
    b: float,
    eps: float,
    p: MyParams,
    type_: int,
    i: int,
    max_iterations: Optional[int] = FSIMP_SAFETY_MAX_ITERATIONS,
) -> FsimpDiagnostics:
    step = b - a
    trap = step * (integrand(type_, i, a, p) + integrand(type_, i, b, p)) * 0.5
    simpson = trap
    intervals = 1
    iterations = 0

    while max_iterations is None or iterations < max_iterations:
        previous = simpson
        old_trap = trap
        midpoint_sum = 0.0
        for index in range(intervals):
            midpoint_sum += integrand(type_, i, a + step * (index + 0.5), p)
        trap = (old_trap + step * midpoint_sum) * 0.5
        simpson = (4.0 * trap - old_trap) / 3.0
        step *= 0.5
        intervals <<= 1
        iterations += 1
        if abs(simpson - previous) < eps:
            return FsimpDiagnostics(simpson, iterations, True)
    return FsimpDiagnostics(simpson, iterations, False)


def fsimp(
    a: float,
    b: float,
    eps: float,
    p: MyParams,
    type_: int,
    i: int,
    max_iterations: Optional[int] = FSIMP_SAFETY_MAX_ITERATIONS,
) -> float:
    return fsimp_diagnostics(a, b, eps, p, type_, i, max_iterations=max_iterations).value


def _i(p: MyParams, type_: int, index: int) -> float:
    return fsimp(0.0, PI / 2.0, EPS, p, type_, index)


def newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
    angle_input = ANGLE_FALLBACK if abs(angle) <= ANGLE_EPS else angle
    speed = math.sqrt(vec.x * vec.x + vec.y * vec.y)
    if speed <= 0.01:
        return Speed(B2Vec2(0.0, 0.0), 0.0)

    vx = abs(vec.x)
    vy = abs(vec.y)
    w = abs(angle_input)
    positive_spin = angle_input > 0.0

    f2 = friction * 100.0 / (2.0 * PI)
    f4 = friction * 100.0 / (4.0 * PI)
    t2 = friction * 1900.0 / (2.0 * PI)
    t4 = friction * 1900.0 / (4.0 * PI)

    if speed >= 1.5:
        p = MyParams(vx, vy, w, R, R)
        i11 = _i(p, 1, 1)
        i15 = _i(p, 1, 5)
        i16 = _i(p, 1, 6)
        i21 = _i(p, 2, 1)
        i25 = _i(p, 2, 5)
        i26 = _i(p, 2, 6)
        i31 = _i(p, 3, 1)
        i32 = _i(p, 3, 2)
        i37 = _i(p, 3, 7)
        i38 = _i(p, 3, 8)
        ax_base = (i15 + i16) * K / MASS
        ay = f2 * i21 + (i25 + i26) * K / MASS
        if positive_spin:
            ax = ax_base - f2 * i11
            torque = t2 * R * (i32 - i31) + K * R * (i38 - i37)
        else:
            ax = f2 * i11 - ax_base
            torque = t2 * R * (i31 - i32) + K * R * (i37 - i38)

    elif speed >= 1.0:
        r1 = R1
        r2 = R2
        p = MyParams(vx, vy, w, r1, r2)
        values = {
            **{(1, idx): _i(p, 1, idx) for idx in range(1, 7)},
            **{(2, idx): _i(p, 2, idx) for idx in range(1, 7)},
            **{(3, idx): _i(p, 3, idx) for idx in range(1, 9)},
        }
        ax_wet_low = (values[1, 3] + values[1, 4]) * WET_K / MASS
        ax_wet_high = (values[1, 5] + values[1, 6]) * WET_K / MASS
        ay = (
            f4 * values[2, 1]
            + f4 * values[2, 2]
            + (values[2, 3] + values[2, 4]) * WET_K / MASS
            + (values[2, 5] + values[2, 6]) * WET_K / MASS
        )
        if positive_spin:
            ax = f4 * values[1, 2] - f4 * values[1, 1] + ax_wet_high - ax_wet_low
            torque = (
                t4 * r2 * (values[3, 2] - values[3, 1])
                + t4 * r1 * (values[3, 4] - values[3, 3])
                + (values[3, 6] - values[3, 5]) * (K * r1)
                + (values[3, 8] - values[3, 7]) * (K * r2)
            )
        else:
            ax = f4 * values[1, 1] - f4 * values[1, 2] + ax_wet_low - ax_wet_high
            torque = (
                t4 * r2 * (values[3, 1] - values[3, 2])
                + t4 * r1 * (values[3, 3] - values[3, 4])
                + (values[3, 5] - values[3, 6]) * (K * r1)
                + (values[3, 7] - values[3, 8]) * (K * r2)
            )

    else:
        p = MyParams(vx, vy, w, R, R)
        i12 = _i(p, 1, 2)
        i13 = _i(p, 1, 3)
        i17 = _i(p, 1, 7)
        i22 = _i(p, 2, 2)
        i23 = _i(p, 2, 3)
        i27 = _i(p, 2, 7)
        i32 = _i(p, 3, 2)
        i33 = _i(p, 3, 3)
        i34 = _i(p, 3, 4)
        i35 = _i(p, 3, 5)
        ay = i23 * K / MASS + f2 * (i22 + i27)
        if positive_spin:
            ax = f2 * (i12 - i17) - i13 * K / MASS
            torque = t2 * R * (i32 - i33 + i34) - K * R * i35
        else:
            ax = i13 * K / MASS + f2 * (i17 - i12)
            torque = K * R * i35 + t2 * R * (i33 - i32 - i34)

    velocity_step = steptime * 10.0
    angular_step = steptime * 20.0
    return Speed(
        B2Vec2(vec.x + velocity_step * ax, velocity_step * ay + vec.y),
        angle_input + angular_step * (torque / INERTIA),
    )


def unity_friction_noise(rng: Optional[Union[UnityRangeFloatRng, random.Random]] = None) -> float:
    if rng is not None and hasattr(rng, "range_float"):
        return float(rng.range_float(-FRICTION_NOISE, FRICTION_NOISE))
    rng = rng or random
    return float(rng.uniform(-FRICTION_NOISE, FRICTION_NOISE))


def unity_friction(
    sweeping: bool,
    rng: Optional[Union[UnityRangeFloatRng, random.Random]] = None,
    noise: Optional[float] = 0.0,
) -> float:
    base = SWEEP_FRICTION if sweeping else BASE_FRICTION
    if noise is None:
        noise = unity_friction_noise(rng)
    return _f32(_f32(base) + _f32(noise))


def recovered_unity_friction_from_seed(seed: int, sweeping: bool, count: int) -> List[float]:
    rng = RecoveredUnityRandom.from_seed(seed)
    return [unity_friction(sweeping, rng=rng, noise=None) for _ in range(count)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vx", type=float, default=1.0)
    parser.add_argument("--vy", type=float, default=2.0)
    parser.add_argument("--angle", type=float, default=5.0)
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--noise", type=float, default=0.0)
    parser.add_argument("--unity-seed", type=int, default=None)
    args = parser.parse_args()

    if args.unity_seed is None:
        friction = unity_friction(args.sweep, noise=args.noise)
    else:
        friction = unity_friction(args.sweep, rng=RecoveredUnityRandom.from_seed(args.unity_seed), noise=None)
    result = newfrictionstep(friction, B2Vec2(args.vx, args.vy), args.angle, STEP)
    print(f"friction={friction:.8f}")
    print(f"unity_fixed_timestep={UNITY_FIXED_TIMESTEP:.8f}")
    print(f"newfrictionstep_param={STEP:.8f}")
    print(f"vx={result.v.x:.12f}")
    print(f"vy={result.v.y:.12f}")
    print(f"angle={result.angle:.12f}")


if __name__ == "__main__":
    main()
