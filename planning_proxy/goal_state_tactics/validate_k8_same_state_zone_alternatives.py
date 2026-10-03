#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""同一 K8 按钮锚局面的多个历史区域候选：反解、末壶筛查与压力排序。

初始局面固定为：己方一颗按钮锚、无对方营内壶。历史区域库在这一**同一当前状态**
给出三个高支持候选（前红圈、按钮附近、较前守壶带）。脚本先分别反解到终局圆区，
再对每条我方 PhysX 终局调用同一末壶筛查器。

默认“找到首条反例即停”，只用于快速确认每条边已被搜索；传入
``--complete-reply-search`` 才完整枚举当前固定反击候选族，并启用同状态压力排序。
这不是连续空间或胜率评测。
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd, install_bundled_pyphysx
from planning_proxy.analytic_proxy import ProxyStone
from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer
from planning_proxy.first_player_strategy import FirstPlayerPlan
from planning_proxy.strict_refine import BoardStone, make_position
from planning_proxy.validate_final_defence import DefenceFixture, evaluate_fixture

from .execution import (
    SearchAttempt,
    StrictGoalSolution,
    rank_k8_proposal_set_by_reply_pressure,
    screen_all_strict_goals,
)
from .last_reply import receipt_from_final_defence_reports
from .proposer import ProposedGoal, propose_goal_states


OWN_SEEDS = (20260911, 20365640, 20470369)


def _as_board_stones(board: list[dict[str, object]]) -> tuple[BoardStone, ...]:
    return tuple(
        BoardStone(
            index=int(stone["index"]), owner=str(stone["owner"]),
            x=float(stone["x"]), y=float(stone["y"]),
            yaw=float(stone.get("yaw", 0.0)), enabled=bool(stone.get("enabled", True)),
        )
        for stone in board if bool(stone.get("enabled", True))
    )


def validate(*, complete_reply_search: bool = False) -> dict[str, Any]:
    initial = [BoardStone(2, "self", HOUSE_X, HOUSE_Y)]
    proposal_set = propose_goal_states(
        [{"index": 2, "owner": "self", "x": HOUSE_X, "y": HOUSE_Y}],
        8, active_stone_index=14, max_fine=0, max_collision_pairs=0, max_zone=3,
    )
    player = ProxyMatchPlayer(physics_seeds=len(OWN_SEEDS), parent_regions=1, decision_budget_seconds=60.0)
    resolved: dict[str, StrictGoalSolution] = {}
    attempt_metadata: dict[str, dict[str, Any]] = {}

    def attempt(proposal: ProposedGoal) -> SearchAttempt:
        region = proposal.bound_stone_constraints[0].final_region
        if region is None:
            return SearchAttempt("SEARCH_ERROR", detail="区域候选缺少 active_delivery 终局圆区。")
        plan = FirstPlayerPlan(
            shot_index=14, own_throw_number=8, phase="k8_same_state_zone_alternatives",
            target_points=((region.centre_x, region.centre_y),), target_opponent_index=None,
            opponent_action="none", rationale="same-state historical zone alternative",
            landing_region_radius_m=region.radius_m,
        )
        started = time.perf_counter()
        result = player._try_fast_targeted_draw(
            strict_board=initial,
            proxy_board=[ProxyStone(2, "self", HOUSE_X, HOUSE_Y)],
            position=make_position(initial), tactical_plan=plan, shot_index=14,
            seeds=OWN_SEEDS, deadline=time.perf_counter() + 60.0,
        )
        elapsed = round(time.perf_counter() - started, 3)
        if result is None:
            attempt_metadata[proposal.goal.transition_id] = {
                "status": "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET",
                "search_budget_seconds": 60.0,
                "elapsed_seconds": elapsed,
            }
            return SearchAttempt("NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET")
        strict, detail = result
        solution = StrictGoalSolution(
            payload={"bestshot": [strict.candidate.v0, strict.candidate.h0, strict.candidate.w0], "strict_detail": detail},
            final_boards=strict.final_boards, rule_legal=strict.rule_legal,
        )
        resolved[proposal.goal.transition_id] = solution
        attempt_metadata[proposal.goal.transition_id] = {
            "status": "ACCEPTED_BY_OWN_GOAL_GATE_BEFORE_REPLY_SCREEN",
            "bestshot": solution.payload["bestshot"],
            "rule_legal": strict.rule_legal,
            "elapsed_seconds": elapsed,
            "strict_detail": detail,
        }
        return SearchAttempt("ACCEPTED", solution)

    reply_metadata: dict[str, dict[str, Any]] = {}

    def screen_last_reply(proposal: ProposedGoal, solution: StrictGoalSolution):
        reports: list[dict[str, Any]] = []
        for index, final_board in enumerate(solution.final_boards):
            fixture = DefenceFixture(
                name=f"{proposal.goal.transition_id} / own-seed-{index}",
                stage="K8 same-state zone alternative",
                description="同一按钮锚局面的历史区域候选；末壶反击筛查。",
                stones=_as_board_stones(final_board),
            )
            reports.append(evaluate_fixture(
                fixture, StrictCurlingEnd(seed=index, training_fast=True),
                direct_count=1, impact_count=1, physics_seeds=(OWN_SEEDS[index],),
                stop_on_first_counterexample=not complete_reply_search,
            ))
        receipt = receipt_from_final_defence_reports(
            solution.final_boards, reports, physics_seeds_per_candidate=1,
            complete_search=complete_reply_search,
        )
        reply_metadata[proposal.goal.transition_id] = {
            "stop_on_first_counterexample_per_final_seed": not complete_reply_search,
            "reports": reports,
            "receipt": {
                "status": receipt.status,
                "strict_candidate_count": receipt.strict_candidate_count,
                "counterexample_count": receipt.counterexample_count,
                "stable_counterexample_count": receipt.stable_counterexample_count,
                "button_counterexample_count": receipt.button_counterexample_count,
                "direct_counterexample_count": receipt.direct_counterexample_count,
                "impact_counterexample_count": receipt.impact_counterexample_count,
                "complete_search": receipt.complete_search,
                "counterexample_rate": receipt.counterexample_rate,
                "detail": receipt.detail,
            },
        }
        return receipt

    screened = screen_all_strict_goals(
        proposal_set, attempt, screen_last_reply=screen_last_reply,
    )
    ranking: list[dict[str, Any]] = []
    ranking_note = "早停筛查不允许压力排序。"
    if complete_reply_search:
        ranking = [
            {
                "transition_id": item.proposal.goal.transition_id,
                "proposal_kind": item.proposal.proposal_kind,
                "support": item.proposal.support,
                "pressure_key": list(item.pressure_key),
            }
            for item in rank_k8_proposal_set_by_reply_pressure(proposal_set, screened)
        ]
        ranking_note = "仅同一 GoalProposalSet、同一完整反击预算内的局部压力排序；不是胜率或跨状态排名。"
    return {
        "schema": "goal_state_k8_same_state_zone_alternatives_v0",
        "scope": (
            "one canonical K8 button-anchor board with three historical zone alternatives; "
            "bounded strict PhysX search; not continuous-space or match-win proof"
        ),
        "runtime_state": {
            "runtime_core_state": proposal_set.runtime_core_state,
            "runtime_zone_state": proposal_set.runtime_zone_state,
            "own_throw_number": proposal_set.own_throw_number,
        },
        "complete_reply_search": complete_reply_search,
        "candidates": [
            {
                "transition_id": item.goal.transition_id,
                "proposal_kind": item.proposal_kind,
                "support": item.support,
                "region": item.bound_stone_constraints[0].final_region.to_json(),
                "attempt": attempt_metadata.get(item.goal.transition_id),
                "last_reply": reply_metadata.get(item.goal.transition_id),
                "screen_result": asdict(next(row.attempt for row in screened if row.proposal is item)),
            }
            for item in proposal_set.proposals
        ],
        "pressure_ranking": ranking,
        "pressure_ranking_note": ranking_note,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete-reply-search", action="store_true", help="完整跑完每条终局种子的固定末壶候选族，并输出局部压力排序。")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    install_bundled_pyphysx()
    report = validate(complete_reply_search=args.complete_reply_search)
    suffix = "full_v0" if args.complete_reply_search else "v0"
    output = args.output or (Path(__file__).resolve().parents[1] / "runs" / f"goal_state_k8_same_state_zone_alternatives_{suffix}.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "runtime_state": report["runtime_state"],
        "complete_reply_search": report["complete_reply_search"],
        "pressure_ranking": report["pressure_ranking"],
        "pressure_ranking_note": report["pressure_ranking_note"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
