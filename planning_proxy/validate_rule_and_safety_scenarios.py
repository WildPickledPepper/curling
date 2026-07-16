#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""12 个规则/安全构型的端到端回归：粗筛 -> 严格 PhysX -> 规则过滤。"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd  # noqa: E402
from local_simulator.runtime_loader import install_bundled_pyphysx  # noqa: E402
from planning_proxy.analytic_proxy import (  # noqa: E402
    ProxyStone, attack_score, calibrate_force_lookup, calibrate_from_recovered_formula,
    conservative_parent_indices, make_initial_candidates, refine_candidates, simulate_batch,
)
from planning_proxy.competition_rules import is_in_free_guard_zone  # noqa: E402
from planning_proxy.strict_refine import (  # noqa: E402
    BoardStone, Candidate, evaluate_one, local_candidates_for_parent, make_position,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture", type=Path,
        default=ROOT / "planning_proxy" / "fixtures" / "rule_and_safety_scenarios_v1.json",
    )
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--max-parent-regions", type=int, default=3)
    parser.add_argument("--top-parent-rows", type=int, default=16)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "planning_proxy" / "runs" / "rule_and_safety_scenarios_v1.json",
    )
    return parser.parse_args()


def scenario_board(raw: list[dict[str, Any]]) -> tuple[list[BoardStone], list[ProxyStone]]:
    strict = [BoardStone(int(item["index"]), str(item["owner"]), float(item["x"]), float(item["y"])) for item in raw]
    proxy = [ProxyStone(item.index, item.owner, item.x, item.y) for item in strict]
    return strict, proxy


def run_one(
    scenario: dict[str, Any], *, params, lookup, environment: StrictCurlingEnd,
    physics_seeds: list[int], max_parent_regions: int, top_parent_rows: int,
) -> dict[str, Any]:
    strict_board, proxy_board = scenario_board(scenario["board"])
    shot_index = int(scenario["shotIndex"])
    protected = {
        stone.index for stone in strict_board
        if shot_index <= 4 and stone.owner == "opponent" and is_in_free_guard_zone(stone.x, stone.y)
    }
    started = time.perf_counter()
    initial = simulate_batch(make_initial_candidates(), proxy_board, params, force_lookup=lookup, dt=0.02)
    parents = conservative_parent_indices(
        initial, risk_radius_m=0.45, minimum_count=48,
        protected_opponent_indices=protected,
    )
    refined = simulate_batch(refine_candidates(initial.shots[parents]), proxy_board, params, force_lookup=lookup, dt=0.02)
    score = attack_score(refined, protected_opponent_indices=protected)
    ordered = np.argsort(-score)[:top_parent_rows]
    rows = [{"bestshot": [float(value) for value in refined.shots[index]]} for index in ordered]
    top_protected_hits = int(sum(int(refined.first_hit_index[index]) in protected for index in ordered))

    position = make_position(strict_board)
    evaluated = []
    seen: set[tuple[float, float, float]] = set()
    regions_used = 0
    # 安全回归只需找到一条合法且全保的路线；若第一个局部区域没有，再扩到最多 3 个。
    for rank, row in enumerate(rows[:max_parent_regions], 1):
        batch = list(local_candidates_for_parent(row, rank, seen))
        if not batch:
            continue
        regions_used += 1
        evaluated.extend(evaluate_one(environment, candidate, strict_board, position, physics_seeds, shot_index) for candidate in batch)
        if any(item.preserves_all_own and item.rule_legal for item in evaluated):
            break
    safe = [item for item in evaluated if item.preserves_all_own and item.rule_legal]
    safe.sort(key=lambda item: (item.worst_score, item.mean_score), reverse=True)
    chosen = safe[0] if safe else None
    return {
        "id": scenario["id"], "category": scenario["category"], "shotIndex": shot_index,
        "stoneCountBeforeThrow": len(strict_board), "protectedOpponentFreeGuardIndices": sorted(protected),
        "coarseTopProtectedFirstHitCount": top_protected_hits,
        "regionsUsed": regions_used, "strictCandidateCount": len(evaluated),
        "safeCandidateCount": len(safe), "hasSafeCandidate": chosen is not None,
        "elapsedSeconds": time.perf_counter() - started,
        "selected": None if chosen is None else chosen.to_json(),
    }


def main() -> int:
    args = parse_args()
    if args.physics_seeds < 1 or args.max_parent_regions < 1 or args.top_parent_rows < 1:
        raise SystemExit("physics-seeds、max-parent-regions、top-parent-rows 必须为正")
    document = json.loads(args.fixture.read_text(encoding="utf-8"))
    if document.get("schema") != "planning_proxy_rule_and_safety_scenarios_v1":
        raise SystemExit("fixture schema 不匹配")
    install_bundled_pyphysx()
    params = calibrate_from_recovered_formula()
    lookup = calibrate_force_lookup()
    seeds = [int(args.seed) + 7919 * index for index in range(args.physics_seeds)]
    environment = StrictCurlingEnd(seed=seeds[0], training_fast=True)
    rows = []
    for scenario in document["scenarios"]:
        row = run_one(
            scenario, params=params, lookup=lookup, environment=environment,
            physics_seeds=seeds, max_parent_regions=args.max_parent_regions,
            top_parent_rows=args.top_parent_rows,
        )
        rows.append(row)
        print(
            "%s | 壶=%d | 受保护=%s | 安全候选=%d | %.2fs" % (
                row["id"], row["stoneCountBeforeThrow"], row["protectedOpponentFreeGuardIndices"],
                row["safeCandidateCount"], row["elapsedSeconds"],
            ), flush=True,
        )
    report = {
        "schema": "planning_proxy_rule_and_safety_validation_v1",
        "scope": "non-sweeping; strict PhysX; each selected action must preserve all own stones and active stone and be free-guard-rule legal on every tested friction seed",
        "fixture": str(args.fixture),
        "physicsSeeds": seeds, "maxParentRegions": args.max_parent_regions,
        "scenarioCount": len(rows), "safeScenarioCount": sum(bool(row["hasSafeCandidate"]) for row in rows),
        "allSafe": all(bool(row["hasSafeCandidate"]) for row in rows), "scenarios": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("安全构型通过 %d/%d | report=%s" % (report["safeScenarioCount"], report["scenarioCount"], args.output))
    return 0 if report["allSafe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
