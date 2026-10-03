#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""记录快速“撞目标壶并滚入区域”流程的严格候选覆盖。

该工具不改状态机。它把既有快速流程实际调用的 ``evaluate_one`` 全部记录下来，
用于区分：没有生成撞击入口、生成入口但严格清壶失败、清壶成功但落区失败、
以及多物理种子失败。粗代理不据此认证可行性，报告中的合同结果均来自严格 PhysX。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path, required=True)
    parser.add_argument("--shot", type=int, default=15)
    parser.add_argument("--contract", choices=("current", "one_outer_reclaim"), default="current")
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--budget-seconds", type=float, default=105.0)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def source_game(report: dict[str, Any]) -> dict[str, Any]:
    game = report.get("game")
    if isinstance(game, dict):
        return game
    games = report.get("games")
    if isinstance(games, list) and games and isinstance(games[0], dict):
        return games[0]
    raise ValueError("报告不含 game 或 games[0]")


def neutralized(item: Any, target_index: int, dead_predicate: Any) -> bool:
    if not item.final_boards:
        return False
    for board in item.final_boards:
        target = next((stone for stone in board if int(stone["index"]) == int(target_index)), None)
        if target is None or not bool(target.get("enabled", False)):
            continue
        if not dead_predicate(float(target["x"]), float(target["y"])):
            return False
    return True


def worst_region_error(item: Any, points: Sequence[Sequence[float]], radius: float) -> float:
    if not item.active_final_positions:
        return float("inf")
    distances = []
    for position in item.active_final_positions:
        if position is None:
            return float("inf")
        distances.append(min(math.hypot(float(position[0]) - float(x), float(position[1]) - float(y)) for x, y in points))
    return max(0.0, max(distances, default=float("inf")) - float(radius))


def main() -> int:
    args = parse_args()
    from local_simulator.runtime_loader import install_bundled_pyphysx

    install_bundled_pyphysx()
    import planning_proxy.evaluate_vs_teammate_ppo as planner
    from planning_proxy.first_player_strategy import HOUSE_PAIR_LEFT, HOUSE_PAIR_RIGHT, is_in_house, is_tactically_dead_position
    from planning_proxy.strict_refine import is_loss_budget_candidate, make_position

    payload = json.loads(args.source_report.read_text(encoding="utf-8"))
    game = source_game(payload)
    row = next(item for item in game["trace"] if int(item.get("shot", -1)) == int(args.shot))
    shot_index = int(args.shot) - 1
    strict_board, proxy_board = planner.canonical_board(row["stateBefore"], 0)
    plan = planner.plan_first_player_turn(proxy_board, shot_index)
    if args.contract == "one_outer_reclaim":
        own = [stone for stone in strict_board if stone.owner == "self"]
        enemy = [stone for stone in strict_board if stone.owner == "opponent"]
        if not (
            str(plan.situation_type) == "P8_ENEMY_THREAT_ONE_OWN"
            and str(plan.phase) == "clear_then_choose_defence_shape"
            and len(own) == 1 and sum(is_in_house(stone) for stone in own) == 0
            and sum(is_in_house(stone) for stone in enemy) == 1
        ):
            raise SystemExit("来源未进入一外场己壶、单敌营内威胁的精确合同")
        target = next(stone for stone in strict_board if int(stone.index) == int(plan.target_opponent_index))
        pair = HOUSE_PAIR_LEFT if float(target.x) >= 2.375 else HOUSE_PAIR_RIGHT
        plan = replace(
            plan, phase="clear_then_reclaim_first_inner_anchor",
            strategy_type="CLEAR_THREAT_AND_RECLAIM_FIRST_ANCHOR",
            desired_state_type="P8_FIRST_INNER_ANCHOR_RECLAIMED_FROM_ONE_OUTER",
            target_points=pair, defence_shapes=(), landing_region_radius_m=0.35,
            max_own_cleared=0,
        )
    if plan.target_opponent_index is None:
        raise SystemExit("合同没有物理清壶目标")
    seed0 = int(game["seed"])
    seeds = [seed0 + shot_index * 7919 + 104729 * index for index in range(int(args.physics_seeds))]
    player = planner.ProxyMatchPlayer(
        physics_seeds=int(args.physics_seeds), parent_regions=3, decision_budget_seconds=float(args.budget_seconds),
    )
    original_evaluate = planner.evaluate_one
    calls: list[dict[str, Any]] = []
    target_index = int(plan.target_opponent_index)

    def observed_evaluate(*call_args: Any, **call_kwargs: Any) -> Any:
        item = original_evaluate(*call_args, **call_kwargs)
        error = worst_region_error(item, plan.target_points, float(plan.landing_region_radius_m))
        cleared = neutralized(item, target_index, is_tactically_dead_position)
        loss_ok = is_loss_budget_candidate(item, int(plan.max_own_cleared or 0))
        calls.append({
            "bestshot": [float(item.candidate.v0), float(item.candidate.h0), float(item.candidate.w0)],
            "physicsSeedCount": len(item.final_boards),
            "ruleLegal": bool(item.rule_legal),
            "targetNeutralized": bool(cleared),
            "lossBudgetOk": bool(loss_ok),
            "allTacticalGoalMet": bool(item.tactical_goal_met) and all(item.tactical_goal_met),
            "worstRegionErrorM": None if not math.isfinite(error) else float(error),
            "enemyCleared": [int(value) for value in item.enemy_cleared],
            "selfCleared": [int(value) for value in item.total_self_cleared],
        })
        return item

    planner.evaluate_one = observed_evaluate
    started = time.perf_counter()
    try:
        found = player._try_fast_targeted_hit_roll(
            strict_board=strict_board,
            proxy_board=proxy_board,
            position=make_position(strict_board),
            tactical_plan=plan,
            shot_index=shot_index,
            seeds=seeds,
            deadline=started + max(0.0, float(args.budget_seconds) - planner.STRICT_EVALUATION_TAIL_RESERVE_SECONDS),
        )
    finally:
        planner.evaluate_one = original_evaluate
    elapsed = time.perf_counter() - started
    def count(predicate: Any) -> int:
        return sum(bool(predicate(call)) for call in calls)
    accepted = [
        call for call in calls
        if call["ruleLegal"] and call["targetNeutralized"] and call["lossBudgetOk"] and call["allTacticalGoalMet"]
    ]
    finite_errors = [float(call["worstRegionErrorM"]) for call in calls if call["worstRegionErrorM"] is not None]
    result = {
        "schema": "fast_targeted_hit_roll_strict_coverage_profile_v1",
        "scope": "诊断既有快速撞击滚位的严格调用覆盖；不运行完整对局、不修改生产状态机。",
        "sourceReport": str(args.source_report),
        "sourceSeed": seed0,
        "shot": int(args.shot),
        "contract": str(args.contract),
        "physicsSeeds": seeds,
        "plan": plan.to_json(),
        "elapsedSeconds": elapsed,
        "returnedCandidate": None if found is None else found[0].to_json(),
        "counts": {
            "strictEvaluateCalls": len(calls),
            "singleSeedCalls": count(lambda call: int(call["physicsSeedCount"]) == 1),
            "multiSeedCalls": count(lambda call: int(call["physicsSeedCount"]) == len(seeds)),
            "ruleLegal": count(lambda call: call["ruleLegal"]),
            "targetNeutralized": count(lambda call: call["targetNeutralized"]),
            "targetNeutralizedAndLegal": count(lambda call: call["targetNeutralized"] and call["ruleLegal"]),
            "allTacticalGoal": count(lambda call: call["allTacticalGoalMet"]),
            "accepted": len(accepted),
        },
        "bestObserved": {
            "minimumWorstRegionErrorM": min(finite_errors) if finite_errors else None,
            "accepted": accepted[:8],
        },
        "calls": calls,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "elapsedSeconds": elapsed, "returned": found is not None, "counts": result["counts"],
        "minimumWorstRegionErrorM": result["bestObserved"]["minimumWorstRegionErrorM"],
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
