#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证手工构造的接触类测试样本本身确实有稳定的正向解。

这里故意只回放数据集中预先记录的 ``oracle_witness``。它是造数据时的
正向证明，不是求解器输入；本脚本不衡量反解器召回率。
"""
from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import canonical_board  # noqa: E402
from planning_proxy.first_player_strategy import FirstPlayerPlan, is_tactically_dead_position  # noqa: E402
from planning_proxy.strict_refine import Candidate, evaluate_one, make_position  # noqa: E402
from planning_proxy.solver_benchmark.run_draw_recall_benchmark import states_from_board  # noqa: E402

DEFAULT_DATASET = ROOT / "planning_proxy" / "solver_benchmark" / "manual_realistic_contact_v1.json"


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
        rationale="基准合同：清指定威胁、保住已在场己方壶并滚入任一允许区域。",
        landing_region_radius_m=float(contract["landing_region_radius_m"]),
        max_own_cleared=0,
    )


def validate(sample: dict[str, Any], environment: StrictCurlingEnd) -> dict[str, Any]:
    plan = plan_for(sample)
    strict_board, _ = canonical_board(states_from_board(sample["board"]), proxy_team=0)
    witness = [float(value) for value in sample["oracle_witness"]["bestshot"]]
    evaluation = evaluate_one(
        environment,
        Candidate(*witness, parent_rank=0),
        strict_board,
        make_position(strict_board),
        [int(seed) for seed in sample["goal_contract"]["required_physics_seeds"]],
        shot_index=plan.shot_index,
        active_index=plan.shot_index,
        tactical_plan=plan,
    )
    target_index = int(sample["target_opponent_index"])
    target_cleared_or_dead = []
    for final_board in evaluation.final_boards:
        target = next((stone for stone in final_board if int(stone["index"]) == target_index), None)
        target_cleared_or_dead.append(
            target is None or not bool(target.get("enabled", True))
            or is_tactically_dead_position(float(target["x"]), float(target["y"]))
        )
    passed = bool(
        evaluation.rule_legal
        and evaluation.preserves_all_own
        and all(target_cleared_or_dead)
        and len(evaluation.tactical_goal_met) == len(sample["goal_contract"]["required_physics_seeds"])
        and all(evaluation.tactical_goal_met)
    )
    return {
        "id": sample["id"],
        "passed": passed,
        "oracle_witness": witness,
        "tactical_goal_met": evaluation.tactical_goal_met,
        "target_cleared_or_dead": target_cleared_or_dead,
        "rule_legal": evaluation.rule_legal,
        "own_cleared": evaluation.own_cleared,
        "active_final_positions": [None if point is None else list(point) for point in evaluation.active_final_positions],
        "target_region_count": len(plan.target_points),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="正向验证手工接触测试样本的 witness，不运行反解器。")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    dataset = args.dataset if args.dataset.is_absolute() else ROOT / args.dataset
    output = args.output or dataset.with_name(dataset.stem + "_witness_validation.json")
    if not output.is_absolute():
        output = ROOT / output
    data = json.loads(dataset.read_text(encoding="utf-8"))
    environment = StrictCurlingEnd(seed=0, training_fast=True)
    rows = [validate(sample, environment) for sample in data["samples"]]
    report = {
        "schema": "planning_proxy_manual_realistic_contact_witness_validation_v1",
        "dataset": dataset.name,
        "purpose": "只验证测试样本有正向稳定解；不使用 oracle 评估反解器。",
        "all_passed": all(row["passed"] for row in rows),
        "samples": rows,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "all_passed": report["all_passed"], "samples": len(rows)}, ensure_ascii=False))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
