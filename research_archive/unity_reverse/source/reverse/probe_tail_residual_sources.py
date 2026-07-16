#!/usr/bin/env python3
"""Probe residual sources for MOTIONINFO -> endpoint tail replay.

This is intentionally a small diagnostic tool. It compares the recovered
CurlingMotion tail replay using mean dry friction against a per-row fitted
constant friction. If a tiny friction adjustment collapses the endpoint error,
the remaining mismatch is more likely missing per-tick Unity friction noise
than a coordinate/timestep/sign bug.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.probe_unity_tail_mapping import read_rows  # noqa: E402
from tools.reverse.recovered_curling_motion import (  # noqa: E402
    BASE_FRICTION,
    STEP,
    SWEEP_FRICTION,
    B2Vec2,
    RecoveredUnityRandom,
    newfrictionstep,
    unity_friction,
)
from tools.reverse.recovered_sweep_window import is_sweeping_at_protocol_y  # noqa: E402


def simulate(
    row: dict,
    friction: float,
    *,
    dt_pos: float,
    max_steps: int,
    unity_seed: int | None = None,
    rng_skip: int = 0,
    sweeping: bool = False,
    sweep_distance: float | None = None,
) -> tuple[float, float, int, float]:
    x = float(row["motion_x"])
    y = float(row["motion_y"])
    vx = float(row["motion_vx"])
    vy = float(row["motion_vy"])
    w = float(row["motion_w"])
    rng = None
    if unity_seed is not None:
        rng = RecoveredUnityRandom.from_seed(unity_seed)
        for _ in range(rng_skip):
            unity_friction(False if sweep_distance is not None else sweeping, rng=rng, noise=None)
    for step in range(max_steps):
        if math.hypot(vx, vy) <= 0.01:
            err = math.hypot(x - float(row["final_x"]), y - float(row["final_y"]))
            return x, y, step, err
        # Unity calls the controller FixedUpdate before the physics step:
        # the script writes the new Rigidbody velocity, then PhysX advances
        # the position over the 0.01 s fixed timestep.
        active_sweep = is_sweeping_at_protocol_y(y, sweep_distance) if sweep_distance is not None else sweeping
        if rng is None:
            step_friction = SWEEP_FRICTION if active_sweep else friction
        else:
            step_friction = unity_friction(active_sweep, rng=rng, noise=None)
        speed = newfrictionstep(step_friction, B2Vec2(vx, vy), w, STEP)
        vx = speed.v.x
        vy = speed.v.y
        w = speed.angle
        x += vx * dt_pos
        y += vy * dt_pos
    err = math.hypot(x - float(row["final_x"]), y - float(row["final_y"]))
    return x, y, max_steps, err


def fit_constant_friction(
    row: dict,
    *,
    dt_pos: float,
    max_steps: int,
    lo: float,
    hi: float,
    iterations: int,
    sweep_distance: float | None = None,
) -> tuple[float, tuple[float, float, int, float]]:
    # Golden-section search is enough here and avoids adding a scipy dependency
    # to a reverse-engineering helper.
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    inv_phi = 1.0 / phi
    left = lo
    right = hi
    c = right - (right - left) * inv_phi
    d = left + (right - left) * inv_phi
    fc = simulate(row, c, dt_pos=dt_pos, max_steps=max_steps, sweep_distance=sweep_distance)
    fd = simulate(row, d, dt_pos=dt_pos, max_steps=max_steps, sweep_distance=sweep_distance)
    for _ in range(iterations):
        if fc[3] <= fd[3]:
            right = d
            d = c
            fd = fc
            c = right - (right - left) * inv_phi
            fc = simulate(row, c, dt_pos=dt_pos, max_steps=max_steps, sweep_distance=sweep_distance)
        else:
            left = c
            c = d
            fc = fd
            d = left + (right - left) * inv_phi
            fd = simulate(row, d, dt_pos=dt_pos, max_steps=max_steps, sweep_distance=sweep_distance)
    friction = (left + right) * 0.5
    return friction, simulate(row, friction, dt_pos=dt_pos, max_steps=max_steps, sweep_distance=sweep_distance)


def row_sweep_distance(row: dict, fixed_distance: float | None, field: str | None) -> float | None:
    if fixed_distance is not None:
        return fixed_distance
    if field is None:
        return None
    if row.get("sent_sweep") is False:
        return None
    value = row.get(field)
    if value in (None, ""):
        return None
    return float(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dt", type=float, default=0.010)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--friction-lo", type=float, default=0.0008)
    parser.add_argument("--friction-hi", type=float, default=0.0012)
    parser.add_argument("--iterations", type=int, default=12)
    parser.add_argument("--unity-seed", type=int, default=None, help="use recovered Unity RNG friction sequence")
    parser.add_argument("--rng-skip", type=int, default=0, help="discard this many Unity friction draws before replay")
    parser.add_argument("--sweeping", action="store_true", help="seeded replay uses sweep base friction")
    parser.add_argument("--sweep-distance", type=float, default=None, help="use recovered sweep window with this distance")
    parser.add_argument("--sweep-field", default=None, help="read recovered sweep window distance from each row field")
    args = parser.parse_args()

    rows = read_rows(args.inputs, args.limit)
    if not rows:
        raise SystemExit("no usable rows")

    base_errors: list[float] = []
    fitted_errors: list[float] = []
    seeded_errors: list[float] = []
    for row in rows:
        sweep_distance = row_sweep_distance(row, args.sweep_distance, args.sweep_field)
        base = simulate(row, BASE_FRICTION, dt_pos=args.dt, max_steps=args.max_steps, sweep_distance=sweep_distance)
        friction, fitted = fit_constant_friction(
            row,
            dt_pos=args.dt,
            max_steps=args.max_steps,
            lo=args.friction_lo,
            hi=args.friction_hi,
            iterations=args.iterations,
            sweep_distance=sweep_distance,
        )
        base_errors.append(base[3])
        fitted_errors.append(fitted[3])
        seeded = None
        if args.unity_seed is not None:
            seeded = simulate(
                row,
                BASE_FRICTION,
                dt_pos=args.dt,
                max_steps=args.max_steps,
                unity_seed=args.unity_seed,
                rng_skip=args.rng_skip,
                sweeping=args.sweeping,
                sweep_distance=sweep_distance,
            )
            seeded_errors.append(seeded[3])
        print(
            (
                "sample={sample_id} base_err={base_err:.6f} fitted_err={fitted_err:.6f} "
                "fitted_friction={friction:.9f} sweep_distance={sweep_distance} "
                "base_steps={base_steps} fitted_steps={fitted_steps}"
                + (
                    " seeded_err={seeded_err:.6f} seeded_steps={seeded_steps} seed={seed} rng_skip={rng_skip}"
                    if seeded is not None
                    else ""
                )
            ).format(
                sample_id=row.get("sample_id", "?"),
                base_err=base[3],
                fitted_err=fitted[3],
                friction=friction,
                sweep_distance=sweep_distance,
                base_steps=base[2],
                fitted_steps=fitted[2],
                seeded_err=seeded[3] if seeded is not None else 0.0,
                seeded_steps=seeded[2] if seeded is not None else 0,
                seed=args.unity_seed,
                rng_skip=args.rng_skip,
            )
        )

    def rmse(values: list[float]) -> float:
        return math.sqrt(sum(value * value for value in values) / len(values))

    summary = f"summary n={len(rows)} base_rmse={rmse(base_errors):.6f} fitted_rmse={rmse(fitted_errors):.6f}"
    if seeded_errors:
        summary += f" seeded_rmse={rmse(seeded_errors):.6f}"
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
