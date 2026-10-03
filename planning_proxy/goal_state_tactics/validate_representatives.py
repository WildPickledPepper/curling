#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三个 GoalState 代表性严格 PhysX 验证夹具。

范围刻意很小：

* K1 历史精细守壶圆区能否跨三条摩擦种子进入；
* K6 固定直进候选不满足双飞终局门时，是否由同一数据状态的单清回退接管。

这不是全战术库胜率评测，也不是连续空间证明。它只验证模块边界、严格终局
验收和回退控制流可在本地 PhysX 中实际联通。
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd, install_bundled_pyphysx
from planning_proxy.analytic_proxy import ProxyStone
from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer
from planning_proxy.first_player_strategy import FirstPlayerPlan
from planning_proxy.strict_refine import BoardStone, Candidate, evaluate_one, make_position

from .execution import SearchAttempt, accept_bound_goal, solve_with_fallback
from .proposer import propose_goal_states


SEEDS = (20260731, 20260731 + 104729, 20260731 + 2 * 104729)


def validate_k1_fine_region() -> dict[str, Any]:
    proposal_set = propose_goal_states([], 1, active_stone_index=0)
    proposal = next((item for item in proposal_set.proposals if item.proposal_kind == "FINE_TERMINAL_REGION"), None)
    if proposal is None or not proposal.bound_stone_constraints or proposal.bound_stone_constraints[0].final_region is None:
        return {"status": "NO_FINE_GOAL_PROPOSED"}
    region = proposal.bound_stone_constraints[0].final_region
    player = ProxyMatchPlayer(physics_seeds=len(SEEDS), parent_regions=1, decision_budget_seconds=60.0)
    plan = FirstPlayerPlan(
        shot_index=0, own_throw_number=1, phase="open_centre_guard",
        target_points=((region.centre_x, region.centre_y),), target_opponent_index=None,
        opponent_action="none", rationale="GoalState K1 representative strict validation",
        landing_region_radius_m=region.radius_m,
    )
    started = time.perf_counter()
    result = player._try_fast_targeted_draw(
        strict_board=[], proxy_board=[], position=make_position([]), tactical_plan=plan,
        shot_index=0, seeds=SEEDS, deadline=time.perf_counter() + 60.0,
    )
    if result is None:
        return {
            "status": "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET",
            "transition_id": proposal.goal.transition_id,
            "search_budget_seconds": 60.0,
            "note": "仅表示本次目标 draw 搜索未找到；不构成物理无解证明。",
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        }
    item, detail = result
    acceptance = accept_bound_goal(
        item.final_boards, proposal.bound_stone_constraints, rule_legal=item.rule_legal,
        occupancy_constraints=proposal.goal.occupancy_constraints,
    )
    return {
        "status": "ACCEPTED" if acceptance.accepted else "REJECTED_BY_GOAL_GATE",
        "transition_id": proposal.goal.transition_id,
        "bestshot": [item.candidate.v0, item.candidate.h0, item.candidate.w0],
        "acceptance": {"accepted": acceptance.accepted, "failures_by_seed": acceptance.failures_by_seed},
        "strict_detail": detail,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
    }


def validate_k6_double_fallback() -> dict[str, Any]:
    board = [
        BoardStone(1, "opponent", HOUSE_X, HOUSE_Y + 0.58),
        BoardStone(3, "opponent", HOUSE_X, HOUSE_Y + 0.28),
    ]
    proposal_set = propose_goal_states(
        [{"index": stone.index, "owner": stone.owner, "x": stone.x, "y": stone.y} for stone in board],
        6, active_stone_index=10, max_collision_pairs=3,
    )
    environment = StrictCurlingEnd(seed=0, training_fast=True)
    # 这是本夹具中已严格复核过的直进候选；本验证测试的是 GoalState 终局门和
    # 回退选择，不把它误称为一般双飞求解器。
    item = evaluate_one(
        environment, Candidate(5.6, 0.0, 0.0, 1), board, make_position(board), SEEDS,
        shot_index=10, active_index=10,
    )

    def attempt(proposal):
        verdict = accept_bound_goal(
            item.final_boards, proposal.bound_stone_constraints, rule_legal=item.rule_legal,
            occupancy_constraints=proposal.goal.occupancy_constraints,
        )
        if verdict.accepted:
            return SearchAttempt("ACCEPTED", {"bestshot": [5.6, 0.0, 0.0], "acceptance": verdict})
        return SearchAttempt(
            "REJECTED_BY_GOAL_GATE",
            detail="固定候选的严格终局不满足该 GoalState；本夹具没有调用双飞反解搜索。",
        )

    chosen = solve_with_fallback(proposal_set, attempt)
    return {
        "status": "FALLBACK_ACCEPTED" if chosen.selected is not None else "NO_FALLBACK_ACCEPTED",
        "candidate_enemy_cleared_indices": item.enemy_cleared_indices,
        "attempted_transition_ids": chosen.attempted_transition_ids,
        "attempts": [
            {"status": record.status, "detail": record.detail}
            for record in chosen.attempts
        ],
        "selected_transition_id": None if chosen.selected is None else chosen.selected.goal.transition_id,
        "selected_out_slots": None if chosen.selected is None else [
            constraint.stone_index for constraint in chosen.selected.bound_stone_constraints
            if constraint.disposition == "OUT_OF_PLAY"
        ],
    }


def validate_k5_zone_fallback() -> dict[str, Any]:
    board = [BoardStone(2, "self", HOUSE_X, HOUSE_Y)]
    proposal_set = propose_goal_states(
        [{"index": 2, "owner": "self", "x": HOUSE_X, "y": HOUSE_Y}],
        5, active_stone_index=8,
    )
    zone_proposals = [item for item in proposal_set.proposals if item.proposal_kind == "HISTORICAL_ZONE_FALLBACK"]
    if not zone_proposals:
        return {"status": "NO_ZONE_FALLBACK_PROPOSED"}
    player = ProxyMatchPlayer(physics_seeds=len(SEEDS), parent_regions=1, decision_budget_seconds=60.0)
    started = time.perf_counter()
    attempts: list[dict[str, Any]] = []
    selected: dict[str, Any] | None = None
    for proposal in zone_proposals:
        region = proposal.bound_stone_constraints[0].final_region
        if region is None:
            continue
        plan = FirstPlayerPlan(
            shot_index=8, own_throw_number=5, phase="open_centre_guard",
            target_points=((region.centre_x, region.centre_y),), target_opponent_index=None,
            opponent_action="none", rationale="GoalState K5 zone-fallback strict validation",
            landing_region_radius_m=region.radius_m,
        )
        result = player._try_fast_targeted_draw(
            strict_board=board, proxy_board=[ProxyStone(2, "self", HOUSE_X, HOUSE_Y)], position=make_position(board),
            tactical_plan=plan, shot_index=8, seeds=SEEDS, deadline=time.perf_counter() + 30.0,
        )
        if result is None:
            attempts.append({
                "transition_id": proposal.goal.transition_id,
                "status": "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET",
                "search_budget_seconds": 30.0,
                "note": "仅表示本次目标 draw 搜索未找到；不构成物理无解证明。",
            })
            continue
        item, detail = result
        acceptance = accept_bound_goal(
            item.final_boards, proposal.bound_stone_constraints, rule_legal=item.rule_legal,
            occupancy_constraints=proposal.goal.occupancy_constraints,
        )
        attempts.append({"transition_id": proposal.goal.transition_id, "status": "ACCEPTED" if acceptance.accepted else "REJECTED_BY_GOAL_GATE"})
        if acceptance.accepted:
            selected = {
                "transition_id": proposal.goal.transition_id,
                "bestshot": [item.candidate.v0, item.candidate.h0, item.candidate.w0],
                "acceptance": {"accepted": acceptance.accepted, "failures_by_seed": acceptance.failures_by_seed},
                "strict_detail": detail,
            }
            break
    if selected is None:
        return {
            "status": "NO_ZONE_FALLBACK_ACCEPTED_WITHIN_CURRENT_SEARCH_BUDGET",
            "attempts": attempts,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        }
    return {
        "status": "FALLBACK_ACCEPTED",
        "attempts": attempts,
        "selected": selected,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "runs" / "goal_state_representative_physx_v0.json",
    )
    args = parser.parse_args()
    install_bundled_pyphysx()
    report = {
        "schema": "goal_state_representative_physx_v0",
        "scope": "three bounded local strict-PhysX fixtures; no sweeping; not a match win-rate or continuous-search proof. NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET never means physical impossibility.",
        "physics_seeds": list(SEEDS),
        "k1_fine_region": validate_k1_fine_region(),
        "k5_zone_fallback": validate_k5_zone_fallback(),
        "k6_double_fallback": validate_k6_double_fallback(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
