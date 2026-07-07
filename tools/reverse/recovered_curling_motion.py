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
from dataclasses import dataclass
from typing import Protocol

try:
    from tools.reverse.recovered_unity_random import RecoveredUnityRandom
except ModuleNotFoundError:  # Allows running this file directly from tools/reverse.
    from recovered_unity_random import RecoveredUnityRandom


PI = 3.1416
R = 0.125
DR = 0.006
K = 0.2
MASS = 19.0
INERTIA = 0.399475
UNITY_FIXED_TIMESTEP = 0.01
NEWFRICTIONSTEP_PARAM = 0.001
STEP = NEWFRICTIONSTEP_PARAM
EPS = 1e-5
BASE_FRICTION = 0.001
SWEEP_FRICTION = BASE_FRICTION * (1.0 - 0.4)
FRICTION_NOISE = 0.0002


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


def _atan_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0.0:
        if numerator == 0.0:
            return math.atan(float("nan"))
        return math.atan(math.copysign(math.inf, numerator))
    return math.atan(numerator / denominator)


def _local(x: float, p: MyParams, radius: float, numerator_mode: str, denom_sign: float):
    s = math.sin(x)
    c = math.cos(x)
    if numerator_mode == "plus":
        a = p.vx + s * p.w * radius
    elif numerator_mode == "minus":
        a = s * p.w * radius - p.vx
    else:
        raise ValueError(numerator_mode)
    b = p.vy + denom_sign * c * p.w * radius
    theta = _atan_ratio(a, b)
    speed_sq = a * a + b * b
    return a, b, theta, speed_sq


def integrand(type_: int, i: int, x: float, p: MyParams) -> float:
    if type_ == 1:
        if i == 1:
            return math.sin(_local(x, p, p.r2, "plus", 1.0)[2]) + math.sin(
                _local(x, p, p.r2, "plus", -1.0)[2]
            )
        if i == 2:
            return math.sin(_local(x, p, p.r1, "minus", 1.0)[2]) + math.sin(
                _local(x, p, p.r1, "minus", -1.0)[2]
            )
        if i == 3:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", 1.0)
            return speed_sq * math.sin(theta)
        if i == 4:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", -1.0)
            return speed_sq * math.sin(theta)
        if i == 5:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", 1.0)
            return speed_sq * math.sin(theta)
        if i == 6:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", -1.0)
            return speed_sq * math.sin(theta)
        if i == 7:
            return math.sin(_local(x, p, p.r2, "plus", -1.0)[2])

    if type_ == 2:
        if i == 1:
            return math.cos(_local(x, p, p.r2, "plus", 1.0)[2]) + math.cos(
                _local(x, p, p.r2, "plus", -1.0)[2]
            )
        if i == 2:
            return math.cos(_local(x, p, p.r1, "minus", 1.0)[2]) + math.cos(
                _local(x, p, p.r1, "minus", -1.0)[2]
            )
        if i == 3:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", 1.0)
            return speed_sq * math.cos(theta)
        if i == 4:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", -1.0)
            return speed_sq * math.cos(theta)
        if i == 5:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", 1.0)
            return speed_sq * math.cos(theta)
        if i == 6:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", -1.0)
            return speed_sq * math.cos(theta)
        if i == 7:
            return math.cos(_local(x, p, p.r2, "plus", -1.0)[2])

    if type_ == 3:
        if i == 1:
            theta = _local(x, p, p.r2, "plus", 1.0)[2]
            return math.sin(x + PI / 2.0 - theta)
        if i == 2:
            theta = _local(x, p, p.r2, "plus", -1.0)[2]
            return math.sin(x + PI / 2.0 + theta)
        if i == 3:
            theta = _local(x, p, p.r1, "minus", 1.0)[2]
            return math.sin(PI / 2.0 - x + theta)
        if i == 4:
            theta = _local(x, p, p.r1, "minus", -1.0)[2]
            return math.sin(PI / 2.0 - x - theta)
        if i == 5:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", 1.0)
            return speed_sq * math.sin(x + PI / 2.0 - theta)
        if i == 6:
            _, _, theta, speed_sq = _local(x, p, p.r1, "plus", -1.0)
            return speed_sq * math.sin(x + PI / 2.0 + theta)
        if i == 7:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", 1.0)
            return speed_sq * math.sin(PI / 2.0 - x + theta)
        if i == 8:
            _, _, theta, speed_sq = _local(x, p, p.r2, "minus", -1.0)
            return speed_sq * math.sin(PI / 2.0 - x - theta)

    raise ValueError(f"unsupported integrand type={type_} i={i}")


def fsimp(
    a: float,
    b: float,
    eps: float,
    p: MyParams,
    type_: int,
    i: int,
    max_iterations: int = 24,
) -> float:
    step = b - a
    trap = step * (integrand(type_, i, a, p) + integrand(type_, i, b, p)) * 0.5
    simpson = trap
    intervals = 1

    for _ in range(max_iterations):
        previous = simpson
        old_trap = trap
        midpoint_sum = 0.0
        for index in range(intervals):
            midpoint_sum += integrand(type_, i, a + step * (index + 0.5), p)
        trap = (old_trap + step * midpoint_sum) * 0.5
        simpson = (4.0 * trap - old_trap) / 3.0
        step *= 0.5
        intervals <<= 1
        if abs(simpson - previous) < eps:
            return simpson
    return simpson


def _i(p: MyParams, type_: int, index: int) -> float:
    return fsimp(0.0, PI / 2.0, EPS, p, type_, index)


def newfrictionstep(friction: float, vec: B2Vec2, angle: float, steptime: float) -> Speed:
    angle_input = 0.01 if abs(angle) <= 1e-6 else angle
    speed = math.hypot(vec.x, vec.y)
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
        ax_base = K / MASS * (i15 + i16)
        ay = f2 * i21 + K / MASS * (i25 + i26)
        if positive_spin:
            ax = ax_base - f2 * i11
            torque = t2 * R * (i32 - i31) + K * R * (i38 - i37)
        else:
            ax = f2 * i11 - ax_base
            torque = t2 * R * (i31 - i32) + K * R * (i37 - i38)

    elif speed >= 1.0:
        r1 = R - DR / 2.0
        r2 = R + DR / 2.0
        p = MyParams(vx, vy, w, r1, r2)
        values = {
            **{(1, idx): _i(p, 1, idx) for idx in range(1, 7)},
            **{(2, idx): _i(p, 2, idx) for idx in range(1, 7)},
            **{(3, idx): _i(p, 3, idx) for idx in range(1, 9)},
        }
        ax_wet_low = 0.1 / MASS * (values[1, 3] + values[1, 4])
        ax_wet_high = 0.1 / MASS * (values[1, 5] + values[1, 6])
        ay = (
            f4 * (values[2, 1] + values[2, 2])
            + 0.1 / MASS * (values[2, 3] + values[2, 4])
            + 0.1 / MASS * (values[2, 5] + values[2, 6])
        )
        if positive_spin:
            ax = f4 * (values[1, 2] - values[1, 1]) + ax_wet_high - ax_wet_low
            torque = (
                t4 * (r2 * (values[3, 2] - values[3, 1]) + r1 * (values[3, 4] - values[3, 3]))
                + K * r1 * (values[3, 6] - values[3, 5])
                + K * r2 * (values[3, 8] - values[3, 7])
            )
        else:
            ax = f4 * (values[1, 1] - values[1, 2]) + ax_wet_low - ax_wet_high
            torque = (
                t4 * (r2 * (values[3, 1] - values[3, 2]) + r1 * (values[3, 3] - values[3, 4]))
                + K * r1 * (values[3, 5] - values[3, 6])
                + K * r2 * (values[3, 7] - values[3, 8])
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
        ay = K / MASS * i23 + f2 * (i22 + i27)
        if positive_spin:
            ax = f2 * (i12 - i17) - K / MASS * i13
            torque = t2 * R * (i32 - i33 + i34) - K * R * i35
        else:
            ax = K / MASS * i13 + f2 * (i17 - i12)
            torque = K * R * i35 + t2 * R * (i33 - i32 - i34)

    return Speed(
        B2Vec2(vec.x + steptime * 10.0 * ax, vec.y + steptime * 10.0 * ay),
        angle_input + steptime * 20.0 * torque / INERTIA,
    )


def unity_friction_noise(rng: UnityRangeFloatRng | random.Random | None = None) -> float:
    if rng is not None and hasattr(rng, "range_float"):
        return float(rng.range_float(-FRICTION_NOISE, FRICTION_NOISE))
    rng = rng or random
    return float(rng.uniform(-FRICTION_NOISE, FRICTION_NOISE))


def unity_friction(
    sweeping: bool,
    rng: UnityRangeFloatRng | random.Random | None = None,
    noise: float | None = 0.0,
) -> float:
    base = SWEEP_FRICTION if sweeping else BASE_FRICTION
    if noise is None:
        noise = unity_friction_noise(rng)
    return base + noise


def recovered_unity_friction_from_seed(seed: int, sweeping: bool, count: int) -> list[float]:
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
