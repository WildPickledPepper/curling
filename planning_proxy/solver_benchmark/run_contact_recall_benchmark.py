#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""盲测接触反解器：只给壶面和合同，绝不向求解器提供 witness。"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer, canonical_board  # noqa: E402
from planning_proxy.first_player_strategy import FirstPlayerPlan, is_tactically_dead_position  # noqa: E402
from planning_proxy.strict_refine import make_position  # noqa: E402
from planning_proxy.solver_benchmark.run_draw_recall_benchmark import states_from_board  # noqa: E402

DEFAULT_DATASETS = (ROOT / "planning_proxy" / "solver_benchmark" / "manual_realistic_contact_v1.json",)


def plan_for(sample: dict[str, Any]) -> FirstPlayerPlan:
    contract = sample["goal_contract"]
    active_index = int(sample["active_index"])
    return FirstPlayerPlan(
        shot_index=active_index,
        own_throw_number=active_index // 2 + 1,
        phase="benchmark_contact_clear",
        target_points=tuple((float(x), float(y)) for x, y in contract["target_points"]),
        target_opponent_index=int(sample["target_opponent_index"]),
        opponent_action=str(contract["kind"]),
        rationale="盲测合同：清指定敌壶、保己方壶、进入任一允许滚位区。",
        landing_region_radius_m=float(contract["landing_region_radius_m"]),
        max_own_cleared=0,
    )


def run_one(player: ProxyMatchPlayer, sample: dict[str, Any], budget_seconds: float) -> dict[str, Any]:
    # 注意：函数内完全不读取 sample["oracle_witness"]。
    plan = plan_for(sample)
    strict_board, proxy_board = canonical_board(states_from_board(sample["board"]), proxy_team=0)
    seeds = [int(seed) for seed in sample["goal_contract"]["required_physics_seeds"]]
    started = time.perf_counter()
    result = player._try_fast_targeted_hit_roll(
        strict_board=strict_board,
        proxy_board=proxy_board,
        position=make_position(strict_board),
        tactical_plan=plan,
        shot_index=plan.shot_index,
        seeds=seeds,
        deadline=started + float(budget_seconds),
    )
    elapsed = time.perf_counter() - started
    if result is None:
        return {
            "id": sample["id"], "found": False, "within_budget": elapsed <= budget_seconds,
            "elapsed_seconds": elapsed, "target_region_count": len(plan.target_points),
        }
    evaluation, detail = result
    target_index = int(sample["target_opponent_index"])
    target_cleared_or_dead = []
    for final_board in evaluation.final_boards:
        target = next((stone for stone in final_board if int(stone["index"]) == target_index), None)
        target_cleared_or_dead.append(
            target is None or not bool(target.get("enabled", True))
            or is_tactically_dead_position(float(target["x"]), float(target["y"]))
        )
    passed = bool(
        evaluation.rule_legal and evaluation.preserves_all_own
        and all(target_cleared_or_dead) and all(evaluation.tactical_goal_met)
    )
    return {
        "id": sample["id"], "found": passed, "within_budget": elapsed <= budget_seconds,
        "elapsed_seconds": elapsed, "target_region_count": len(plan.target_points),
        "bestshot": [evaluation.candidate.v0, evaluation.candidate.h0, evaluation.candidate.w0],
        "tactical_goal_met": evaluation.tactical_goal_met,
        "target_cleared_or_dead": target_cleared_or_dead,
        "rule_legal": evaluation.rule_legal,
        "own_cleared": evaluation.own_cleared,
        "solver_detail": detail,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="接触反解器盲测。")
    parser.add_argument("--dataset", action="append", type=Path, default=[])
    parser.add_argument("--budget-seconds", type=float, default=105.0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    datasets = tuple(args.dataset) if args.dataset else DEFAULT_DATASETS
    player = ProxyMatchPlayer(physics_seeds=3, parent_regions=3, decision_budget_seconds=float(args.budget_seconds))
    rows: list[dict[str, Any]] = []
    for path in datasets:
        dataset = path if path.is_absolute() else ROOT / path
        data = json.loads(dataset.read_text(encoding="utf-8"))
        for sample in data["samples"]:
            row = run_one(player, sample, float(args.budget_seconds))
            row["dataset"] = dataset.name
            rows.append(row)
            print(json.dumps({key: row[key] for key in ("id", "found", "within_budget", "elapsed_seconds")}, ensure_ascii=False))
    report = {
        "schema": "planning_proxy_contact_recall_benchmark_v1",
        "purpose": "反解器盲测；oracle_witness 不传入求解器。",
        "budget_seconds": float(args.budget_seconds),
        "sample_count": len(rows),
        "found_count": sum(bool(row["found"]) for row in rows),
        "within_budget_count": sum(bool(row["within_budget"]) for row in rows),
        "samples": rows,
    }
    output = args.output or ROOT / "planning_proxy" / "solver_benchmark" / "contact_recall_v1.json"
    if not output.is_absolute():
        output = ROOT / output
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "found": report["found_count"], "samples": report["sample_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
