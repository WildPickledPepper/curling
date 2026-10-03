#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在同一批固定严格 PhysX 候选上比较真实 K6 的多个状态机合同。

候选生成只看当前壶面、指定敌壶与粗代理的首撞/攻击拓扑；不读取完整防御、
repair 或交换合同的落点。每条候选只做一次三物理种子严格结算，之后把同一
终局分别交给各合同评分。该脚本仅用于离线比较，不改变生产状态机。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx  # noqa: E402
from local_simulator.examples.train_policy_tree_selfplay import HOUSE_X, HOUSE_Y, STONE_COUNT, StrictCurlingEnd  # noqa: E402
from planning_proxy.analytic_proxy import (  # noqa: E402
    attack_score, calibrate_force_lookup, calibrate_from_recovered_formula,
    make_initial_candidates, refine_candidates, simulate_batch,
)
from planning_proxy.competition_rules import HOUSE_R, STONE_R  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import canonical_board  # noqa: E402
from planning_proxy.first_player_strategy import FirstPlayerPlan, plan_first_player_turn, score_strict_outcome  # noqa: E402
from planning_proxy.strict_refine import Candidate, StrictEvaluation, evaluate_one, is_loss_budget_candidate, make_position, selection_priority  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, action="append", required=True, help="含 game.trace 的真实 K6 续局报告；可重复。")
    parser.add_argument("--shot", type=int, default=11, help="K6 的 trace 投壶编号，默认 11。")
    parser.add_argument("--parents", type=int, default=12, help="合同无关的首撞父拓扑数。")
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument(
        "--stream-contract-gate", action="store_true",
        help="按合同门流式复核：发现完整或 repair 即停止；否则扫描完后才允许仅清。仅测调度，不改生产状态机。",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "planning_proxy" / "runs" / "k6_fixed_candidate_contracts.json")
    return parser.parse_args()


def source_game(source: dict[str, Any]) -> dict[str, Any]:
    if isinstance(source.get("game"), dict):
        return source["game"]
    if isinstance(source.get("games"), list) and source["games"] and isinstance(source["games"][0], dict):
        return source["games"][0]
    raise ValueError("报告缺少 game 或 games[0]")


def state_before(source: dict[str, Any], shot: int) -> list[dict[str, Any]]:
    row = next((item for item in source_game(source).get("trace", []) if int(item.get("shot", -1)) == int(shot)), None)
    if row is None or not isinstance(row.get("stateBefore"), list):
        raise ValueError(f"找不到第 {shot} 手的 stateBefore")
    return row["stateBefore"]


def contract_variants(plan: FirstPlayerPlan) -> dict[str, FirstPlayerPlan]:
    """对应当前 K6 实际会进入的三个语义合同，且不参与候选生成。"""

    return {
        "完整防御": plan,
        "repair": replace(plan, phase="clear_then_repair_outer_house_layer", defence_shapes=()),
        "仅清威胁": replace(plan, phase="pure_clear_fallback", target_points=(), defence_shapes=()),
        "一换一留营": replace(
            plan,
            phase="trade_one_for_one_clear_threat",
            target_points=((HOUSE_X, HOUSE_Y),),
            landing_region_radius_m=HOUSE_R + STONE_R,
            defence_shapes=(),
        ),
    }


def retarget(physical: StrictEvaluation, board: Iterable[Any], active_index: int, plan: FirstPlayerPlan) -> StrictEvaluation:
    """严格物理结束后按另一份合同重算，不再推进 Scene。"""

    scores: list[float] = []
    goals: list[bool] = []
    for final_board in physical.final_boards:
        states: list[dict[str, Any]] = [{"enabled": False} for _ in range(STONE_COUNT)]
        for stone in final_board:
            index = int(stone["index"])
            states[index] = {
                "enabled": bool(stone.get("enabled", False)),
                "x": float(stone["x"]), "y": float(stone["y"]), "yaw": float(stone.get("yaw", 0.0)),
            }
        score, goal = score_strict_outcome(states, board, active_index, plan)
        scores.append(float(score))
        goals.append(bool(goal))
    return replace(physical, tactical_scores=scores, tactical_goal_met=goals)


def choose_parent_rows(coarse: Any, candidates: np.ndarray, target_index: int, count: int) -> list[int]:
    """仅按物理首撞和攻击代理分层选择，不看任何合同落点。"""

    hit_rows = np.flatnonzero(coarse.first_hit_index == int(target_index))
    if not len(hit_rows):
        return []
    attack = attack_score(coarse, protected_opponent_indices=set(), must_clear_index=int(target_index))
    ordered = hit_rows[np.argsort(-attack[hit_rows])]
    selected: list[int] = []
    seen_spin: set[int] = set()
    seen_speed: set[int] = set()
    # 先覆盖不同旋转和速度，避免最容易命中的一个碰撞族占满所有父点。
    for row in ordered:
        speed_bin = int(round(float(candidates[int(row)][0]) * 100.0))
        spin_bin = int(round(float(candidates[int(row)][2]) * 100.0))
        if spin_bin in seen_spin and speed_bin in seen_speed:
            continue
        selected.append(int(row))
        seen_spin.add(spin_bin)
        seen_speed.add(speed_bin)
        if len(selected) >= count:
            return selected
    for row in ordered:
        if int(row) not in selected:
            selected.append(int(row))
        if len(selected) >= count:
            break
    return selected


def evaluate_source(
    source_path: Path, *, shot: int, parents: int, physics_seed_count: int,
    stream_contract_gate: bool = False,
) -> dict[str, Any]:
    source = json.loads(source_path.read_text(encoding="utf-8"))
    states = state_before(source, shot)
    strict_board, proxy_board = canonical_board(states, 0)
    plan = plan_first_player_turn(proxy_board, shot - 1)
    target = plan.target_opponent_index
    if target is None or plan.opponent_action != "physical_clear":
        raise ValueError(f"{source_path.name} 的 K6 不是可比较的 physical_clear 合同")
    match_seed = int(source_game(source).get("seed", source.get("sourceSeed", 0)))
    seeds = [match_seed + (shot - 1) * 7919 + 104729 * offset for offset in range(physics_seed_count)]
    params = calibrate_from_recovered_formula()
    lookup = calibrate_force_lookup()
    coarse_shots = make_initial_candidates(velocity_count=7, lateral_count=41, spin_count=15)
    started = time.perf_counter()
    coarse = simulate_batch(coarse_shots, proxy_board, params, force_lookup=lookup, dt=0.02)
    parent_rows = choose_parent_rows(coarse, coarse_shots, int(target), parents)
    refined = refine_candidates(np.asarray([coarse_shots[row] for row in parent_rows], dtype=np.float32)) if parent_rows else np.empty((0, 3), dtype=np.float32)
    # 局部细分本身只由首撞拓扑父点决定；这里不再按任何合同重排或截断。
    unique: dict[tuple[float, float, float], Candidate] = {}
    for rank, values in enumerate(refined, 1):
        values = np.asarray(values, dtype=np.float64)
        candidate = Candidate(
            float(np.clip(values[0], 1.0, 6.0)),
            float(np.clip(values[1], -2.23, 2.23)),
            float(np.clip(values[2], -15.7, 15.7)),
            rank,
        )
        unique.setdefault((round(candidate.v0, 8), round(candidate.h0, 8), round(candidate.w0, 8)), candidate)
    environment = StrictCurlingEnd(seed=seeds[0], training_fast=True)
    position = make_position(strict_board)
    variants = contract_variants(plan)
    own_count = sum(stone.owner == "self" for stone in strict_board)
    enemy_count = sum(stone.owner == "opponent" for stone in strict_board)

    def loss_budget(variant: FirstPlayerPlan) -> int:
        return (
            int(variant.max_own_cleared)
            if variant.max_own_cleared is not None
            else int(variant.own_throw_number >= 5 and own_count > enemy_count)
        )

    def accepted(physical: StrictEvaluation, variant: FirstPlayerPlan) -> StrictEvaluation | None:
        retargeted = retarget(physical, strict_board, shot - 1, variant)
        if is_loss_budget_candidate(retargeted, loss_budget(variant)) and all(retargeted.tactical_goal_met):
            return retargeted
        return None

    if stream_contract_gate:
        # 这个顺序正是计划中的线上调度语义：只要发现完整或 repair，就立刻
        # 把选择权还给原状态机；不能因为纯清较早出现就提前提交。反之必须
        # 穷尽同一固定批次，才能把“二者均未出现”当作仅清的资格。
        observed: dict[str, list[tuple[int, StrictEvaluation]]] = {name: [] for name in variants}
        stopped = "exhausted_without_full_or_repair"
        evaluated_count = 0
        strict_seconds_total = 0.0
        strict_seconds_max = 0.0
        for ordinal, candidate in enumerate(unique.values(), start=1):
            strict_started = time.perf_counter()
            physical = evaluate_one(
                environment, candidate, strict_board, position, seeds, shot - 1,
                active_index=shot - 1, tactical_plan=None,
            )
            strict_elapsed = time.perf_counter() - strict_started
            strict_seconds_total += strict_elapsed
            strict_seconds_max = max(strict_seconds_max, strict_elapsed)
            evaluated_count = ordinal
            for name, variant in variants.items():
                item = accepted(physical, variant)
                if item is not None:
                    observed[name].append((ordinal, item))
            if observed["完整防御"] or observed["repair"]:
                stopped = "first_full_or_repair_found"
                break
        selected = (
            "仅清威胁"
            if stopped == "exhausted_without_full_or_repair" and observed["仅清威胁"]
            else "保持当前基线"
        )
        elapsed = time.perf_counter() - started
        return {
            "source": str(source_path), "matchSeed": match_seed, "shot": shot,
            "situation": plan.situation_type, "strategy": plan.strategy_type,
            "targetIndex": int(target), "physicsSeeds": seeds,
            "coarseCandidateCount": len(coarse_shots), "targetHitParentCount": int(np.sum(coarse.first_hit_index == int(target))),
            "selectedParentRows": parent_rows, "fixedStrictCandidateCount": len(unique),
            "elapsedSeconds": elapsed,
            "streamContractGate": {
                "stopped": stopped,
                "evaluatedStrictCandidateCount": evaluated_count,
                "selectedContract": selected,
                "observedAcceptedCountBeforeStop": {name: len(items) for name, items in observed.items()},
                "firstAcceptedStrictCandidateOrdinal": {
                    name: (items[0][0] if items else None) for name, items in observed.items()
                },
                "strictEvaluationSecondsTotal": strict_seconds_total,
                "strictEvaluationSecondsMax": strict_seconds_max,
            },
        }
    physical_rows: list[StrictEvaluation] = []
    for candidate in unique.values():
        physical_rows.append(evaluate_one(
            environment, candidate, strict_board, position, seeds, shot - 1,
            active_index=shot - 1, tactical_plan=None,
        ))
    contracts: dict[str, Any] = {}
    for name, variant in variants.items():
        retargeted = [retarget(item, strict_board, shot - 1, variant) for item in physical_rows]
        # ``physical_rows`` 的顺序就是合同无关的首撞拓扑批次顺序。除最终
        # 可行数量外，记录某一合同第一次出现在哪个严格候选：它用来核验
        # 统一批次是否能在平台预算内及早发现“完整/repair 存在”，而不是
        # 把完整枚举耗时误写成一个抽象的有解/无解结论。
        accepted_with_ordinal = [
            (ordinal, item)
            for ordinal, item in enumerate(retargeted, start=1)
            if is_loss_budget_candidate(item, loss_budget(variant)) and all(item.tactical_goal_met)
        ]
        accepted_with_ordinal.sort(key=lambda row: selection_priority(row[1], variant), reverse=True)
        accepted = [item for _ordinal, item in accepted_with_ordinal]
        contracts[name] = {
            "acceptedCount": len(accepted),
            "firstAcceptedStrictCandidateOrdinal": (
                min(ordinal for ordinal, _item in accepted_with_ordinal)
                if accepted_with_ordinal else None
            ),
            "ownLossBudget": loss_budget(variant),
            "best": accepted[0].to_json() if accepted else None,
            "plan": variant.to_json(),
        }
    elapsed = time.perf_counter() - started
    return {
        "source": str(source_path), "matchSeed": match_seed, "shot": shot,
        "situation": plan.situation_type, "strategy": plan.strategy_type,
        "targetIndex": int(target), "physicsSeeds": seeds,
        "coarseCandidateCount": len(coarse_shots), "targetHitParentCount": int(np.sum(coarse.first_hit_index == int(target))),
        "selectedParentRows": parent_rows, "fixedStrictCandidateCount": len(physical_rows),
        "elapsedSeconds": elapsed, "contracts": contracts,
    }


def main() -> None:
    args = parse_args()
    if args.parents < 1 or args.physics_seeds < 1:
        raise SystemExit("--parents 和 --physics-seeds 必须至少为 1")
    install_bundled_pyphysx()
    reports = [
        evaluate_source(
            path, shot=args.shot, parents=args.parents, physics_seed_count=args.physics_seeds,
            stream_contract_gate=bool(args.stream_contract_gate),
        )
        for path in args.source
    ]
    result = {
        "schema": "k6_fixed_contract_independent_candidate_batch_v1",
        "scope": "offline diagnostic only; no production state-machine change",
        "parentSelection": "first-hit target topology + attack score + speed/spin diversity; no contract target points",
        "streamContractGate": bool(args.stream_contract_gate),
        "reports": reports,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "reports": [
        {
            "source": Path(row["source"]).name,
            "elapsedSeconds": row["elapsedSeconds"],
            "contracts": ({
                name: info["acceptedCount"] for name, info in row["contracts"].items()
            } if "contracts" in row else row.get("streamContractGate")),
        } for row in reports
    ]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
