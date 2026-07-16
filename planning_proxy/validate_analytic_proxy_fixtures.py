#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在 24 个固定残局构型上审计连续白盒粗代理的“别漏路”能力。

对照物是已经恢复的逐 0.01 秒自由滑行公式（不是碰后终局）。本脚本只回答：
若该公式认为一条路线会先碰到敌方壶，粗代理是否至少把它列为“需要交给
严格 PhysX 复核”的近敌路线。它不把粗代理当作碰撞结果，也不替代严格验证。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.analytic_proxy import (  # noqa: E402
    ProxyStone,
    calibrate_force_lookup,
    calibrate_from_recovered_formula,
    conservative_parent_indices,
    simulate_batch,
)
from planning_proxy.whitebox_proxy import Shot, Stone, predict_free_slide  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario-file", type=Path,
        default=ROOT / "training_research" / "fixtures" / "p0_representative_late_end_scenarios_v1.json",
    )
    parser.add_argument("--samples-per-board", type=int, default=60)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--proxy-dt", type=float, default=0.05, help="粗代理的公式积分步长（秒）")
    parser.add_argument("--risk-radii", type=float, nargs="+", default=(0.45, 0.55, 0.65))
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "planning_proxy" / "runs" / "analytic_proxy_fixture_audit.json",
    )
    return parser.parse_args()


def board_from_scenario(scenario: dict[str, Any]) -> tuple[list[Stone], list[ProxyStone]]:
    """按当前出手方重标记己方/对方；偶号壶=先手，奇号壶=后手。"""

    team = int(scenario["targetShot"]) % 2
    exact: list[Stone] = []
    rough: list[ProxyStone] = []
    for item in scenario["stones"]:
        index = int(item["id"])
        owner = "self" if index % 2 == team else "opponent"
        values = (index, owner, float(item["x"]), float(item["y"]))
        exact.append(Stone(*values))
        rough.append(ProxyStone(*values))
    return exact, rough


def sampled_shots(count: int, seed: int) -> np.ndarray:
    """固定随机样本；连续参数而非离散路径表。"""

    rng = np.random.default_rng(seed)
    return np.column_stack((
        rng.uniform(3.2, 5.8, size=count),
        rng.uniform(-2.2, 2.2, size=count),
        rng.uniform(-15.0, 15.0, size=count),
    )).astype(np.float32)


def summary(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(rows)
    actual = sum(int(row["actualEnemyFirstHits"]) for row in rows)
    kept = sum(int(row["keptActualEnemyFirstHits"]) for row in rows)
    selected = sum(int(row["selectedForStrictReview"]) for row in rows)
    own = sum(int(row["selectedOwnFirstHits"]) for row in rows)
    return {
        "scenarioCount": len(rows),
        "actualEnemyFirstHits": actual,
        "keptActualEnemyFirstHits": kept,
        "enemyRecall": None if actual == 0 else kept / actual,
        "selectedForStrictReview": selected,
        "selectedOwnFirstHits": own,
        "selectionRate": 0.0 if not rows else selected / sum(int(row["samples"]) for row in rows),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.samples_per_board < 1:
        raise ValueError("samples-per-board 必须为正数")
    document = json.loads(args.scenario_file.read_text(encoding="utf-8"))
    if document.get("schema") != "p0_fixed_representative_late_end_scenarios_v1":
        raise ValueError("不是预期的 24 构型 fixture")
    params = calibrate_from_recovered_formula()
    force_lookup = calibrate_force_lookup()
    started = time.perf_counter()
    outputs: dict[float, list[dict[str, Any]]] = {float(radius): [] for radius in args.risk_radii}

    for scenario_index, scenario in enumerate(document["scenarios"]):
        exact_board, rough_board = board_from_scenario(scenario)
        if not exact_board or not any(stone.owner == "opponent" for stone in exact_board):
            continue
        shots = sampled_shots(args.samples_per_board, int(args.seed) + scenario_index * 100_003)
        # 对照：恢复公式逐 tick 推进到首撞；碰撞发生后立即停止，不伪造终局。
        exact = [predict_free_slide(Shot(*map(float, row)), exact_board) for row in shots]
        labels_enemy = np.asarray([item.first_hit_owner == "opponent" for item in exact], dtype=bool)
        labels_own = np.asarray([item.first_hit_owner == "self" for item in exact], dtype=bool)
        rough = simulate_batch(shots, rough_board, params, force_lookup=force_lookup, dt=float(args.proxy_dt))
        for radius in args.risk_radii:
            chosen = conservative_parent_indices(rough, risk_radius_m=float(radius), minimum_count=0)
            mask = np.zeros(len(shots), dtype=bool)
            mask[chosen] = True
            row = {
                "scenario": str(scenario["id"]),
                "category": str(scenario["category"]),
                "targetShot": int(scenario["targetShot"]),
                "samples": len(shots),
                "actualEnemyFirstHits": int(np.sum(labels_enemy)),
                "keptActualEnemyFirstHits": int(np.sum(labels_enemy & mask)),
                "enemyRecall": None if not np.any(labels_enemy) else float(np.sum(labels_enemy & mask) / np.sum(labels_enemy)),
                "selectedForStrictReview": int(np.sum(mask)),
                "selectedOwnFirstHits": int(np.sum(labels_own & mask)),
                "missedEnemyExampleActions": [
                    [round(float(value), 4) for value in shots[index]]
                    for index in np.flatnonzero(labels_enemy & ~mask)[:5]
                ],
            }
            outputs[float(radius)].append(row)
        print(
            f"{scenario['id']} | 真实首撞敌方 {int(np.sum(labels_enemy)):2d}/{len(shots)} | "
            f"0.45m 保留 {outputs[float(args.risk_radii[0])][-1]['keptActualEnemyFirstHits']:2d}",
            flush=True,
        )

    by_radius: dict[str, Any] = {}
    for radius, rows in outputs.items():
        categories: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            categories[row["category"]].append(row)
        by_radius[f"{radius:.2f}"] = {
            "all": summary(rows),
            "byCategory": {category: summary(category_rows) for category, category_rows in sorted(categories.items())},
            "scenarios": rows,
        }
    report = {
        "schema": "continuous_math_proxy_fixture_free_slide_audit_v1",
        "scope": (
            "non-sweeping; 24 fixed late-end boards; exact recovered free-slide formula versus "
            "continuous coarse proxy; first-contact screening only, not strict PhysX collision/end-state validation"
        ),
        "configuration": {
            "samplesPerNonEmptyBoard": int(args.samples_per_board), "seed": int(args.seed),
            "proxyDtSeconds": float(args.proxy_dt),
            "riskRadiiM": [float(radius) for radius in args.risk_radii],
            "calibration": params.__dict__,
            "forceLookup": force_lookup.metadata(),
        },
        "elapsedSeconds": time.perf_counter() - started,
        "byRiskRadius": by_radius,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    args = parse_args()
    report = run(args)
    for radius, content in report["byRiskRadius"].items():
        all_rows = content["all"]
        print(
            f"风险半径 {radius}m | 召回 {all_rows['keptActualEnemyFirstHits']}/{all_rows['actualEnemyFirstHits']} "
            f"= {all_rows['enemyRecall']!s} | 送严格复核 {all_rows['selectedForStrictReview']}",
            flush=True,
        )
    print(f"报告: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
