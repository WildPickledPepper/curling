#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K8 高支持“单清”边的端到端严格 PhysX 反例验证。

选择的历史边是：
``K8_COLLISION[control=OPPONENT;F_house=0;O_house=1;F_guards=N;O_guards=N]|remove=1``，
支持度 797。夹具刻意极简：对方一颗按钮壶，我方第 8 壶直进单清。它验证的是模块
是否会在“我方单清已成功、但对方末壶仍有反例”时记录该反击而不伪造安全声明；这
不是证明所有 K8 单清都失败，更不是整库胜率评测。
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd, install_bundled_pyphysx
from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.strict_refine import BoardStone, Candidate, evaluate_one, make_position
from planning_proxy.validate_final_defence import DefenceFixture, evaluate_fixture

from .execution import SearchAttempt, StrictGoalSolution, accept_bound_goal, solve_strict_goal_with_fallback
from .last_reply import receipt_from_final_defence_reports
from .proposer import propose_goal_states


OWN_SEEDS = (20260801, 20260801 + 104729, 20260801 + 2 * 104729)


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
    initial = [BoardStone(1, "opponent", HOUSE_X, HOUSE_Y)]
    proposal_set = propose_goal_states(
        [{"index": 1, "owner": "opponent", "x": HOUSE_X, "y": HOUSE_Y}],
        8, active_stone_index=14, max_fine=0, max_zone=0,
    )
    if len(proposal_set.proposals) != 1:
        raise RuntimeError("K8 单壶夹具应只绑定一条历史单清目标。")
    proposal = proposal_set.proposals[0]
    environment = StrictCurlingEnd(seed=0, training_fast=True)
    # 这是直进单清的已知工作候选；不把它包装成通用 K8 反解器。
    strict = evaluate_one(
        environment, Candidate(5.6, 0.0, 0.0, 1), initial, make_position(initial), OWN_SEEDS,
        shot_index=14, active_index=14,
    )
    solution = StrictGoalSolution(
        payload={"bestshot": [5.6, 0.0, 0.0], "kind": "fixed_representative_candidate"},
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
            name=f"K8 单清后终局种子 {index}", stage="K8 representative",
            description="我方单清后的实际严格终局；只用于有限末壶反击筛查。",
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
    return {
        "schema": "goal_state_k8_single_clear_reply_screen_v0",
        "scope": (
            "one data-supported K8 single-clear fixture; bounded strict PhysX reply screen; "
            "not continuous-search, match-win, or all-K8 proof"
        ),
        "historical_edge": {
            "transition_id": proposal.goal.transition_id,
            "support": proposal.support,
            "source_state": proposal.goal.source_state,
            "require_last_reply_search": proposal.goal.require_last_reply_search,
        },
        "own_candidate": {
            "bestshot": [5.6, 0.0, 0.0],
            "rule_legal": strict.rule_legal,
            "enemy_cleared_indices_by_seed": strict.enemy_cleared_indices,
            "goal_geometry_accepted_before_reply_screen": geometry.accepted,
            "goal_geometry_failures_by_seed": geometry.failures_by_seed,
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
                "该代表候选完成末壶反击筛查且发现反例；可作为战术候选，但不能标为安全终局。"
                if executed.selected is not None else "终局执行未通过搜索完整性或几何门；必须人工复核。"
            ),
        },
    }


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
        "goal_state_k8_single_clear_reply_screen_full_v0.json" if args.complete_reply_search
        else "goal_state_k8_single_clear_reply_screen_v0.json"
    ))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "historical_edge": report["historical_edge"],
        "reply_receipt": report["last_reply_screen"]["receipt"],
        "end_to_end_goal_execution": report["end_to_end_goal_execution"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
