#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K8 高支持“按钮锚后补前红圈壶”历史区域边的端到端反例验证。

选取 ``K7_8_ZONE[control=FIRST;F_house=1;O_house=0]|grid=0,1``：支持度 96，
前置局面为己方已有一颗按钮锚、没有对方营内壶。严格 PhysX 先反解第二颗壶落进
历史圆区，再逐条筛查对手第 16 壶。

该脚本若发现反例，表示此代表候选不能被标为安全终局；它会保留反击证据供难度比较，
不意味着公开比赛中的这个位置动作没有价值，也不推断所有类似局面都不可守。
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

from .execution import SearchAttempt, StrictGoalSolution, accept_bound_goal, solve_strict_goal_with_fallback
from .last_reply import receipt_from_final_defence_reports
from .proposer import propose_goal_states


OWN_SEEDS = (20260811, 20365540, 20470269)


def _as_board_stones(board: list[dict[str, object]]) -> tuple[BoardStone, ...]:
    return tuple(
        BoardStone(
            index=int(stone["index"]), owner=str(stone["owner"]),
            x=float(stone["x"]), y=float(stone["y"]),
            yaw=float(stone.get("yaw", 0.0)), enabled=bool(stone.get("enabled", True)),
        )
        for stone in board if bool(stone.get("enabled", True))
    )


def validate(*, stop_on_first_counterexample: bool = True) -> dict[str, Any]:
    initial = [BoardStone(2, "self", HOUSE_X, HOUSE_Y)]
    proposal_set = propose_goal_states(
        [{"index": 2, "owner": "self", "x": HOUSE_X, "y": HOUSE_Y}],
        8, active_stone_index=14, max_fine=0, max_collision_pairs=0, max_zone=1,
    )
    if len(proposal_set.proposals) != 1:
        raise RuntimeError("K8 按钮锚夹具应只绑定一条最高支持历史区域边。")
    proposal = proposal_set.proposals[0]
    region = proposal.bound_stone_constraints[0].final_region
    if region is None:
        raise RuntimeError("历史区域边缺少 active_delivery 终局圆区。")
    player = ProxyMatchPlayer(physics_seeds=len(OWN_SEEDS), parent_regions=1, decision_budget_seconds=60.0)
    plan = FirstPlayerPlan(
        shot_index=14, own_throw_number=8, phase="k8_anchor_zone_representative",
        target_points=((region.centre_x, region.centre_y),), target_opponent_index=None,
        opponent_action="none", rationale="K8 data-supported zone representative",
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
    common = {
        "schema": "goal_state_k8_anchor_zone_reply_screen_v0",
        "scope": (
            "one data-supported K8 anchor-and-front-house-zone fixture; bounded strict PhysX reply "
            "screen; not continuous-search, match-win, or all-K8 proof"
        ),
        "historical_edge": {
            "transition_id": proposal.goal.transition_id,
            "support": proposal.support,
            "source_state": proposal.goal.source_state,
            "require_last_reply_search": proposal.goal.require_last_reply_search,
            "region": region.to_json(),
        },
    }
    if result is None:
        common["own_candidate"] = {
            "status": "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET",
            "search_budget_seconds": 60.0,
            "elapsed_seconds": elapsed,
            "note": "没有把该结果解释成物理无解。",
        }
        return common
    strict, detail = result
    solution = StrictGoalSolution(
        payload={"bestshot": [strict.candidate.v0, strict.candidate.h0, strict.candidate.w0], "strict_detail": detail},
        final_boards=strict.final_boards,
        rule_legal=strict.rule_legal,
    )
    geometry = accept_bound_goal(
        solution.final_boards, proposal.bound_stone_constraints,
        rule_legal=solution.rule_legal, occupancy_constraints=proposal.goal.occupancy_constraints,
    )
    reply_reports: list[dict[str, Any]] = []
    for index, final_board in enumerate(strict.final_boards):
        fixture = DefenceFixture(
            name=f"K8 按钮锚区域终局种子 {index}", stage="K8 representative",
            description="按钮锚后补历史前红圈圆区的实际严格终局；有限末壶反击筛查。",
            stones=_as_board_stones(final_board),
        )
        reply_reports.append(evaluate_fixture(
            fixture, StrictCurlingEnd(seed=index, training_fast=True),
            direct_count=1, impact_count=1, physics_seeds=(OWN_SEEDS[index],),
            stop_on_first_counterexample=stop_on_first_counterexample,
        ))
    receipt = receipt_from_final_defence_reports(
        strict.final_boards, reply_reports, physics_seeds_per_candidate=1,
        complete_search=not stop_on_first_counterexample,
    )
    executed = solve_strict_goal_with_fallback(
        proposal_set,
        lambda _: SearchAttempt("ACCEPTED", solution),
        screen_last_reply=lambda _proposal, _solution: receipt,
    )
    common.update({
        "own_candidate": {
            "status": "ACCEPTED_BY_OWN_GOAL_GATE_BEFORE_REPLY_SCREEN",
            "bestshot": [strict.candidate.v0, strict.candidate.h0, strict.candidate.w0],
            "rule_legal": strict.rule_legal,
            "elapsed_seconds": elapsed,
            "geometry_accepted": geometry.accepted,
            "geometry_failures_by_seed": geometry.failures_by_seed,
            "strict_detail": detail,
            "final_boards": strict.final_boards,
        },
        "last_reply_screen": {
            "physics_seeds_per_candidate": 1,
            "stop_on_first_counterexample_per_final_seed": stop_on_first_counterexample,
            "counterexample_count_interpretation": (
                "每条终局种子最多记录第一条反例；总数仅为下界，不能用于难度排序。"
                if stop_on_first_counterexample else "完整跑完当前固定候选族；仅可与相同预算、相同候选族的报告比较。"
            ),
            "reports": reply_reports,
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
        },
        "end_to_end_goal_execution": {
            "selected_transition_id": None if executed.selected is None else executed.selected.goal.transition_id,
            "attempted_transition_ids": executed.attempted_transition_ids,
            "attempts": [asdict(item) for item in executed.attempts],
            "conclusion": (
                "该代表候选完成末壶反击筛查且发现反例；不能标为安全终局。"
                if executed.selected is not None else "终局执行未通过搜索完整性或几何门；必须人工复核。"
            ),
        },
    })
    return common


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=None,
    )
    parser.add_argument("--complete-reply-search", action="store_true", help="完整跑完每条终局种子的固定末壶候选族，用于同预算比较。")
    args = parser.parse_args()
    install_bundled_pyphysx()
    report = validate(stop_on_first_counterexample=not args.complete_reply_search)
    output = args.output or (Path(__file__).resolve().parents[1] / "runs" / (
        "goal_state_k8_anchor_zone_reply_screen_full_v0.json" if args.complete_reply_search
        else "goal_state_k8_anchor_zone_reply_screen_v0.json"
    ))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "historical_edge": report["historical_edge"],
        "own_candidate": report["own_candidate"],
        "last_reply_screen": report.get("last_reply_screen", {}).get("receipt"),
        "end_to_end_goal_execution": report.get("end_to_end_goal_execution"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
