#!/usr/bin/env python3
"""严格回放粗代理候选本身，供定位某个状态机分支为何退化。"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
from local_simulator.runtime_loader import install_bundled_pyphysx
from planning_proxy.analytic_proxy import ProxyStone
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer
from planning_proxy.first_player_strategy import FirstPlayerPlan
from planning_proxy.strict_refine import BoardStone, Candidate, evaluate_one, make_position


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--yaw-board", type=Path, help="可选：用含 yaw 的局面 JSON 覆盖严格回放的旧壶朝向。")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260718)
    parser.add_argument("--try-hit-target", nargs=2, type=float, metavar=("X", "Y"))
    parser.add_argument("--try-draw-target", nargs=2, type=float, metavar=("X", "Y"))
    parser.add_argument("--max-own-cleared", type=int, default=None, help="可选：将本次碰撞合同限制为至多清掉几颗己方壶。")
    parser.add_argument("--hit-radius", type=float, default=0.10, help="--try-hit-target 的出手壶终点圆区半径（米）。")
    parser.add_argument("--hit-budget-seconds", type=float, default=20.0)
    args = parser.parse_args()
    raw = json.loads(args.report.read_text(encoding="utf-8"))
    yaw_by_index: dict[int, float] = {}
    if args.yaw_board is not None:
        yaw_by_index = {
            int(stone["index"]): float(stone.get("yaw", 0.0))
            for stone in json.loads(args.yaw_board.read_text(encoding="utf-8"))
        }
    board = tuple(
        BoardStone(
            int(stone["index"]), str(stone["owner"]), float(stone["x"]), float(stone["y"]),
            yaw=float(yaw_by_index.get(int(stone["index"]), stone.get("yaw", 0.0))),
        )
        for stone in raw["board"]
    )
    shot_index = int(raw["shotIndex"])
    seeds = [int(args.seed) + 7919 * offset for offset in range(int(args.physics_seeds))]
    install_bundled_pyphysx()
    environment = StrictCurlingEnd(seed=seeds[0], training_fast=True)
    position = make_position(board)
    for rank, row in enumerate(raw["top"][:int(args.count)], 1):
        v0, h0, w0 = (float(value) for value in row["bestshot"])
        outcome = evaluate_one(
            environment, Candidate(v0, h0, w0, rank), board, position, seeds,
            shot_index=shot_index, active_index=shot_index,
        )
        print(json.dumps({
            "rank": rank, "bestshot": [v0, h0, w0], "ruleLegal": outcome.rule_legal,
            "enemyClearedIndices": outcome.enemy_cleared_indices,
            "selfCleared": outcome.total_self_cleared,
            "activeFinalPositions": outcome.active_final_positions,
            "worstScore": outcome.worst_score,
        }, ensure_ascii=False))
    if args.try_hit_target is not None:
        target_index = raw.get("mustClearIndex")
        if target_index is None:
            raise SystemExit("report must contain mustClearIndex for --try-hit-target")
        target = (float(args.try_hit_target[0]), float(args.try_hit_target[1]))
        plan = FirstPlayerPlan(
            shot_index=shot_index, own_throw_number=shot_index // 2 + 1,
            phase="diagnostic_clear_hold", target_points=(target,), target_opponent_index=int(target_index),
            opponent_action="physical_clear", rationale="diagnostic only", landing_region_radius_m=float(args.hit_radius),
            max_own_cleared=args.max_own_cleared,
        )
        first_v0, first_h0, first_w0 = (float(value) for value in raw["top"][0]["bestshot"])
        direct = evaluate_one(
            environment, Candidate(first_v0, first_h0, first_w0, 1), board, position, seeds,
            shot_index=shot_index, active_index=shot_index, tactical_plan=plan,
        )
        print(json.dumps({
            "target": target, "topCoarseDirectWithGoal": {
                "tacticalGoalMet": direct.tactical_goal_met,
                "enemyClearedIndices": direct.enemy_cleared_indices,
                "selfCleared": direct.total_self_cleared,
                "ruleLegal": direct.rule_legal,
            },
        }, ensure_ascii=False))
        player = ProxyMatchPlayer(
            physics_seeds=int(args.physics_seeds), parent_regions=2,
            decision_budget_seconds=float(args.hit_budget_seconds),
        )
        result = player._try_fast_targeted_hit_roll(
            strict_board=board,
            proxy_board=tuple(ProxyStone(stone.index, stone.owner, stone.x, stone.y) for stone in board),
            position=position, tactical_plan=plan, shot_index=shot_index, seeds=seeds,
            deadline=time.perf_counter() + float(args.hit_budget_seconds),
        )
        if result is None:
            print(json.dumps({"target": target, "fastHitRoll": "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET"}, ensure_ascii=False))
        else:
            evaluation, detail = result
            print(json.dumps({
                "target": target, "fastHitRoll": "CERTIFIED", "bestshot": evaluation.to_json()["bestshot"],
                "detail": detail,
            }, ensure_ascii=False))
    if args.try_draw_target is not None:
        target = (float(args.try_draw_target[0]), float(args.try_draw_target[1]))
        plan = FirstPlayerPlan(
            shot_index=shot_index, own_throw_number=shot_index // 2 + 1,
            phase="diagnostic_draw", target_points=(target,), target_opponent_index=None,
            opponent_action="none", rationale="diagnostic only", landing_region_radius_m=0.10,
        )
        player = ProxyMatchPlayer(
            physics_seeds=int(args.physics_seeds), parent_regions=2,
            decision_budget_seconds=float(args.hit_budget_seconds),
        )
        result = player._try_fast_targeted_draw(
            strict_board=board,
            proxy_board=tuple(ProxyStone(stone.index, stone.owner, stone.x, stone.y) for stone in board),
            position=position, tactical_plan=plan, shot_index=shot_index, seeds=seeds,
            deadline=time.perf_counter() + float(args.hit_budget_seconds),
        )
        if result is None:
            print(json.dumps({"target": target, "fastDraw": "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET"}, ensure_ascii=False))
        else:
            evaluation, detail = result
            print(json.dumps({
                "target": target, "fastDraw": "CERTIFIED", "bestshot": evaluation.to_json()["bestshot"],
                "detail": detail,
            }, ensure_ascii=False))


if __name__ == "__main__":
    main()
