#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成净空粗代理的严格 PhysX 终点残差表。

表只适用于“未撞壶、未出界”的低速 draw 区间。它以空场严格 PhysX 为标定
真值，记录当前白盒受力表代理的终点偏差；运行时仅用于校正净空路线的排序，
绝不拿来推断碰撞后的滚位。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd  # noqa: E402
from planning_proxy.analytic_proxy import (  # noqa: E402
    calibrate_force_lookup,
    calibrate_from_recovered_formula,
    simulate_batch,
)


DEFAULT_OUTPUT = ROOT / "planning_proxy" / "assets" / "free_slide_endpoint_residual_v1.npz"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dt", type=float, default=0.02, help="必须与比赛时粗代理步长一致")
    parser.add_argument("--physics-seed", type=int, default=20260720)
    parser.add_argument("--active-index", type=int, default=12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    # 这个区间内空场严格回放均保留出手壶；超过它的高速球会出界，不能把
    # “已移除”的零位置错误当作一个可插值终点。
    speed_nodes = np.asarray((2.70, 2.80, 2.90, 3.00, 3.10), dtype=np.float32)
    # 不放精确 0，避免恢复公式的零旋特例；运行时在 -0.01/+0.01 间插值。
    spin_nodes = np.asarray(
        (-14.0, -12.0, -9.0, -6.0, -3.0, -1.0, -0.01, 0.01, 1.0, 3.0, 6.0, 9.0, 12.0, 14.0),
        dtype=np.float32,
    )
    params = calibrate_from_recovered_formula()
    force_lookup = calibrate_force_lookup()
    active = int(args.active_index)
    environment = StrictCurlingEnd(seed=int(args.physics_seed) - active * 7919, training_fast=True)
    residual = np.empty((len(speed_nodes), len(spin_nodes), 2), dtype=np.float32)

    for speed_index, speed in enumerate(speed_nodes):
        for spin_index, spin in enumerate(spin_nodes):
            environment.reset()
            environment.seed = int(args.physics_seed) - active * 7919
            environment.shot_number = active
            state = environment.play((float(speed), 0.0, float(spin)))["states"][active]
            if not bool(state["enabled"]):
                raise RuntimeError(f"标定点出界：v={speed}, w={spin}")
            proxy = simulate_batch(
                np.asarray(((speed, 0.0, spin),), dtype=np.float32), (), params,
                force_lookup=force_lookup, dt=float(args.dt),
            )
            residual[speed_index, spin_index] = (
                float(state["x"]) - float(proxy.stop_points[0, 0]),
                float(state["y"]) - float(proxy.stop_points[0, 1]),
            )

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output,
        speed_nodes=speed_nodes,
        spin_nodes=spin_nodes,
        residual_xy=residual,
        dt=np.asarray((float(args.dt),), dtype=np.float32),
        physics_seed=np.asarray((int(args.physics_seed),), dtype=np.int64),
        active_index=np.asarray((active,), dtype=np.int32),
    )
    print({
        "output": str(output), "dt": float(args.dt),
        "shape": list(residual.shape), "min": residual.min(axis=(0, 1)).tolist(),
        "max": residual.max(axis=(0, 1)).tolist(),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
