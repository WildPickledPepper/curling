#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用恢复公式的逐 0.01 秒版本检查数学粗代理是否漏掉敌方通道。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from analytic_proxy import (
    ProxyStone, calibrate_from_recovered_formula, conservative_parent_indices, simulate_batch,
)
from whitebox_proxy import Shot, Stone, predict_free_slide


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--risk-radius", type=float, default=0.45)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "planning_proxy" / "runs" / "analytic_proxy_validation.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = np.random.RandomState(args.seed)
    shots = np.column_stack((
        rng.uniform(3.2, 5.8, args.samples), rng.uniform(-2.2, 2.2, args.samples), rng.uniform(-15.0, 15.0, args.samples),
    )).astype(np.float32)
    exact_board = [Stone(2, "self", 2.05, 7.25), Stone(1, "opponent", 2.55, 5.45), Stone(3, "opponent", 2.75, 4.72)]
    proxy_board = [ProxyStone(2, "self", 2.05, 7.25), ProxyStone(1, "opponent", 2.55, 5.45), ProxyStone(3, "opponent", 2.75, 4.72)]
    truth = np.asarray([
        predict_free_slide(Shot(float(v0), float(h0), float(w0)), exact_board).first_hit_owner or "none"
        for v0, h0, w0 in shots
    ], dtype=object)
    proxy = simulate_batch(shots, proxy_board, calibrate_from_recovered_formula())
    selected = np.zeros(args.samples, dtype=bool)
    selected[conservative_parent_indices(proxy, risk_radius_m=args.risk_radius, minimum_count=0)] = True
    enemy_truth = truth == "opponent"
    own_truth = truth == "self"
    report = {
        "schema": "analytic_proxy_vs_recovered_formula_v1",
        "samples": int(args.samples), "riskRadiusM": args.risk_radius,
        "actualEnemyHits": int(np.sum(enemy_truth)),
        "keptForPhysx": int(np.sum(selected)),
        "enemyRecall": float(np.sum(enemy_truth & selected) / max(1, np.sum(enemy_truth))),
        "ownPathsPassed": int(np.sum(own_truth & selected)),
        "missedEnemy": int(np.sum(enemy_truth & ~selected)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
