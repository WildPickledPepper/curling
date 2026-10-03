"""用当前先手状态机复验 K7 历史困难壶面。

输入来自 ``build_k7_historical_transition_fixture_set.py``。每个壶面独立注入当前
规划器；它不是完整对局，也不把旧终局分数当作当前表现。用途是记录当前的
``S7 -> G7`` 是否找到三物理种子严格合同、是否安全回退及耗时，为下一步完整对局
筛出值得研究的状态簇。
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from evaluate_vs_teammate_ppo import ProxyMatchPlayer, canonical_board
from first_player_strategy import plan_first_player_turn


def concise_detail(detail: dict[str, Any], wall_seconds: float) -> dict[str, Any]:
    strict = detail.get("strict") or {}
    plan = detail.get("firstPlayerPlan") or {}
    return {
        "mode": detail.get("mode"),
        "wallSeconds": float(wall_seconds),
        "plannerDecisionSeconds": detail.get("plannerDecisionSeconds"),
        "plannerBudgetExceeded": detail.get("plannerBudgetExceeded"),
        "candidateCount": detail.get("candidateCount"),
        "eligibleCount": detail.get("eligibleCount"),
        "fallbackReason": detail.get("fallbackReason"),
        "plannedPhase": plan.get("phase"),
        "plannedSituation": plan.get("situation_type"),
        "strictGoalMetByPhysicsSeed": strict.get("tactical_goal_met"),
        "strictEnemyClearedByPhysicsSeed": strict.get("enemy_cleared"),
        "strictOwnClearedByPhysicsSeed": strict.get("own_cleared"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fixture-id", action="append", default=[])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    args = parser.parse_args()

    fixture_set = json.loads(args.fixtures.read_text(encoding="utf-8"))
    fixtures = list(fixture_set["fixtures"])
    requested = {str(item) for item in args.fixture_id}
    if requested:
        fixtures = [item for item in fixtures if str(item["fixtureId"]) in requested]
    if args.limit is not None:
        fixtures = fixtures[: max(0, int(args.limit))]

    result: dict[str, Any] = {
        "schema": "k7_current_planner_fixture_evaluation_v1",
        "scope": "独立 K7 状态注入；不是完整对局胜率。",
        "currentPlanner": {
            "decisionBudgetSeconds": float(args.decision_budget_seconds),
            "physicsSeeds": int(args.physics_seeds),
            "parentRegions": int(args.parent_regions),
        },
        "fixtureSource": str(args.fixtures),
        "results": [],
    }
    for fixture in fixtures:
        strict_board, proxy_board = canonical_board(fixture["stateBefore"], 0)
        planned = plan_first_player_turn(proxy_board, 12)
        match_seed = int(fixture["historicalMatchSeeds"][0])
        player = ProxyMatchPlayer(
            physics_seeds=int(args.physics_seeds),
            parent_regions=int(args.parent_regions),
            decision_budget_seconds=float(args.decision_budget_seconds),
        )
        started = time.perf_counter()
        action, detail = player.choose(
            fixture["stateBefore"],
            proxy_team=0,
            shot_index=12,
            match_seed=match_seed,
        )
        row = {
            "fixtureId": fixture["fixtureId"],
            "historicalRecordCount": fixture["historicalRecordCount"],
            "historicalOutcomeCount": fixture["historicalOutcomeCount"],
            "historicalMatchSeed": match_seed,
            "liveStoneSummary": fixture["liveStoneSummary"],
            "stateMachinePlanBeforeSolve": planned.to_json(),
            "action": [float(value) for value in action],
            "result": concise_detail(detail, time.perf_counter() - started),
        }
        result["results"].append(row)
        print(
            f"{fixture['fixtureId']} mode={row['result']['mode']} "
            f"seconds={row['result']['wallSeconds']:.3f}",
            flush=True,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
