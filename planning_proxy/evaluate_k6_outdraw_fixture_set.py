"""在真实 K6 outdraw 历史壶面上运行当前规划器的单手基线。"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from evaluate_vs_teammate_ppo import ProxyMatchPlayer, canonical_board
from first_player_strategy import plan_first_player_turn


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    args = parser.parse_args()
    fixture_set = json.loads(args.fixtures.read_text(encoding="utf-8"))
    result: dict[str, Any] = {
        "schema": "k6_current_planner_fixture_evaluation_v1",
        "scope": "独立 K6 状态注入；不是完整对局胜率。",
        "currentPlanner": {
            "decisionBudgetSeconds": float(args.decision_budget_seconds),
            "physicsSeeds": int(args.physics_seeds),
            "parentRegions": int(args.parent_regions),
        },
        "results": [],
    }
    for fixture in fixture_set["fixtures"]:
        strict_board, proxy_board = canonical_board(fixture["stateBefore"], 0)
        planned = plan_first_player_turn(proxy_board, 10)
        seed = int(fixture["historicalMatchSeeds"][0])
        player = ProxyMatchPlayer(
            physics_seeds=int(args.physics_seeds),
            parent_regions=int(args.parent_regions),
            decision_budget_seconds=float(args.decision_budget_seconds),
        )
        started = time.perf_counter()
        action, detail = player.choose(fixture["stateBefore"], proxy_team=0, shot_index=10, match_seed=seed)
        strict = detail.get("strict") or {}
        plan = detail.get("firstPlayerPlan") or {}
        row = {
            "fixtureId": fixture["fixtureId"],
            "historicalRecordCount": fixture["historicalRecordCount"],
            "historicalOutcomeCount": fixture["historicalOutcomeCount"],
            "historicalMatchSeed": seed,
            "liveStoneSummary": fixture["liveStoneSummary"],
            "stateMachinePlanBeforeSolve": planned.to_json(),
            "action": [float(value) for value in action],
            "result": {
                "mode": detail.get("mode"),
                "wallSeconds": time.perf_counter() - started,
                "plannerDecisionSeconds": detail.get("plannerDecisionSeconds"),
                "plannerBudgetExceeded": detail.get("plannerBudgetExceeded"),
                "candidateCount": detail.get("candidateCount"),
                "eligibleCount": detail.get("eligibleCount"),
                "fallbackReason": detail.get("fallbackReason"),
                "plannedPhase": plan.get("phase"),
                "fallbackFromPhase": (detail.get("fallbackFromPlan") or {}).get("phase"),
                "strictGoalMetByPhysicsSeed": strict.get("tactical_goal_met"),
                "strictEnemyClearedByPhysicsSeed": strict.get("enemy_cleared"),
                "strictOwnClearedByPhysicsSeed": strict.get("own_cleared"),
                "activeFinalPositions": strict.get("active_final_positions"),
            },
        }
        result["results"].append(row)
        print(
            f"{fixture['fixtureId']} mode={row['result']['mode']} seconds={row['result']['wallSeconds']:.3f}",
            flush=True,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
