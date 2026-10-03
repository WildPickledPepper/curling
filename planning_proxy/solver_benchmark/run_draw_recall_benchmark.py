#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测量当前净空反解器对手工正向正样本集的 105 秒召回率。

输入样本中的 oracle_witness 绝不读取；运行器只交给当前求解器：
  1. 手工摆出的盘面；
  2. 目标区域与保护旧壶合同；
  3. 多物理种子。

输出的“成功”还会重新用严格 PhysX 验证，不信任求解器自己的声明。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import STONE_COUNT, StrictCurlingEnd  # noqa: E402
from planning_proxy.competition_rules import RuleBoardStone, free_guard_rule_violations  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer, canonical_board  # noqa: E402
from planning_proxy.first_player_strategy import FirstPlayerPlan  # noqa: E402
from planning_proxy.strict_refine import make_position  # noqa: E402


DEFAULT_DATASET = ROOT / "planning_proxy" / "solver_benchmark" / "manual_forward_draw_v0.json"
DEFAULT_OUTPUT = ROOT / "planning_proxy" / "solver_benchmark" / "manual_forward_draw_v0_recall.json"


def states_from_board(board: list[dict[str, Any]]) -> list[dict[str, Any]]:
    states = [{"enabled": False, "x": 0.0, "y": 0.0, "yaw": 0.0} for _ in range(STONE_COUNT)]
    for stone in board:
        index = int(stone["index"])
        states[index] = {
            "enabled": True, "x": float(stone["x"]), "y": float(stone["y"]),
            "yaw": float(stone.get("yaw", 0.0)),
        }
    return states


def reset_data(states: list[dict[str, Any]]) -> tuple[list[float], dict[int, float]]:
    position = [0.0] * (STONE_COUNT * 2)
    yaws = {index: 0.0 for index in range(STONE_COUNT)}
    for index, state in enumerate(states):
        if bool(state["enabled"]):
            position[2 * index] = float(state["x"])
            position[2 * index + 1] = float(state["y"])
            yaws[index] = float(state.get("yaw", 0.0))
    return position, yaws


def contract_plan(sample: dict[str, Any]) -> FirstPlayerPlan:
    contract = sample["goal_contract"]
    target = contract["active_target_region"]
    active_index = int(contract["active_index"])
    return FirstPlayerPlan(
        shot_index=active_index,
        own_throw_number=active_index // 2 + 1,
        phase="benchmark_net_draw",
        target_points=((float(target["center"][0]), float(target["center"][1])),),
        target_opponent_index=None,
        opponent_action="none",
        rationale="基准测试：绕开所有旧壶，进入给定目标区域。",
        landing_region_radius_m=float(target["radius_m"]),
    )


def validate_contract(sample: dict[str, Any], shot: tuple[float, float, float]) -> dict[str, Any]:
    """不用 oracle，独立验证候选是否满足数据集写入的合同。"""

    contract = sample["goal_contract"]
    active_index = int(contract["active_index"])
    states = states_from_board(sample["board"])
    position, yaws = reset_data(states)
    old_positions = {
        int(stone["index"]): (float(stone["x"]), float(stone["y"]))
        for stone in sample["board"]
    }
    radius = float(contract["active_target_region"]["radius_m"])
    centre = tuple(float(value) for value in contract["active_target_region"]["center"])
    tolerance = float(contract["old_stone_position_tolerance_m"])
    environment = StrictCurlingEnd(seed=0, training_fast=True)
    rows: list[dict[str, Any]] = []
    passed = True
    for seed in contract["required_physics_seeds"]:
        environment.seed = int(seed) - active_index * 7919
        environment.scene.reset_positions(position, yaw_overrides=yaws)
        environment.shot_number = active_index
        result = environment.play(shot)
        final = result["states"]
        rule_board = [
            RuleBoardStone(int(stone["index"]), str(stone["owner"]), float(stone["x"]), float(stone["y"]), True)
            for stone in sample["board"]
        ]
        active = final[active_index]
        active_point = (float(active["x"]), float(active["y"])) if bool(active.get("enabled", False)) else None
        landing_error = math.inf if active_point is None else math.hypot(active_point[0] - centre[0], active_point[1] - centre[1])
        old_static = True
        for index, start in old_positions.items():
            state = final[index]
            old_static = old_static and bool(state.get("enabled", False)) and math.hypot(
                float(state["x"]) - start[0], float(state["y"]) - start[1]
            ) <= tolerance
        violations = free_guard_rule_violations(rule_board, final, shot_index=active_index)
        row_passed = (
            not bool(result.get("contact", False)) and not violations and old_static
            and active_point is not None and landing_error <= radius
        )
        passed = passed and row_passed
        rows.append({
            "physics_seed": int(seed), "passed": row_passed,
            "contact": bool(result.get("contact", False)), "rule_violations": violations,
            "old_stones_static": old_static, "landing_error_m": landing_error,
            "active_final": None if active_point is None else list(active_point),
        })
    return {"passed": passed, "per_seed": rows}


def run_sample(player: ProxyMatchPlayer, sample: dict[str, Any], deadline_seconds: float) -> dict[str, Any]:
    states = states_from_board(sample["board"])
    plan = contract_plan(sample)
    strict_board, proxy_board = canonical_board(states, proxy_team=0)
    started = time.perf_counter()
    result = player._try_fast_targeted_draw(
        strict_board=strict_board,
        proxy_board=proxy_board,
        position=make_position(strict_board),
        tactical_plan=plan,
        shot_index=plan.shot_index,
        seeds=[int(seed) for seed in sample["goal_contract"]["required_physics_seeds"]],
        deadline=started + float(deadline_seconds),
    )
    elapsed = time.perf_counter() - started
    if result is None:
        return {"id": sample["id"], "found": False, "elapsed_seconds": elapsed, "verified": None}
    evaluation, detail = result
    shot = (float(evaluation.candidate.v0), float(evaluation.candidate.h0), float(evaluation.candidate.w0))
    verified = validate_contract(sample, shot)
    return {
        "id": sample["id"], "found": bool(verified["passed"]), "elapsed_seconds": elapsed,
        "bestshot": list(shot), "solver_detail": detail, "verified": verified,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dataset = json.loads(args.dataset.read_text(encoding="utf-8"))
    accepted_schemas = {
        "planning_proxy_manual_forward_fixture_set_v0",
        "planning_proxy_historical_recovery_draw_set_v1",
        "planning_proxy_historical_targeted_draw_bulk_v2",
        "planning_proxy_historical_targeted_draw_variants_v3",
        "planning_proxy_actual_fallback_restore_draw_v1",
        "planning_proxy_manual_complex_draw_v1",
    }
    if dataset.get("schema") not in accepted_schemas:
        raise SystemExit("dataset 不是受支持的净空反解正样本集")
    samples = list(dataset["samples"])
    if args.limit is not None:
        samples = samples[:int(args.limit)]
    player = ProxyMatchPlayer(physics_seeds=3, parent_regions=3, decision_budget_seconds=float(args.decision_budget_seconds))
    rows = []
    for sample in samples:
        row = run_sample(player, sample, float(args.decision_budget_seconds))
        rows.append(row)
        print(json.dumps({"id": row["id"], "found": row["found"], "seconds": round(row["elapsed_seconds"], 3)}, ensure_ascii=False), flush=True)
    solved = sum(bool(row["found"]) for row in rows)
    payload = {
        "schema": "planning_proxy_draw_recall_benchmark_v0",
        "dataset": str(args.dataset), "decision_budget_seconds": float(args.decision_budget_seconds),
        "sample_count": len(rows), "solved_count": solved,
        "recall": None if not rows else solved / len(rows), "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "solved": solved, "total": len(rows), "recall": payload["recall"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
