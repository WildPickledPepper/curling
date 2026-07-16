#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""规划代理与队友 PPO 的本地严格 PhysX 一局对局评测。

每个评测组包含两局 16 手单 end：规划代理分别作为先手和后手。PPO 通过
``training_research/opponents/teammate_ppo_adapter.py`` 调用队友保留的
``latest.pt``，不连接 Unity 或 socket。

此脚本是当前一手攻击规划器的集成冒烟评测，不是 Unity 实战胜率：严格复核会
带入场上旧壶的真实 yaw，摩擦仍使用可复现的本地种子。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_X, HOUSE_Y, STONE_COUNT, StrictCurlingEnd, install_bundled_pyphysx, score_board,
)
from planning_proxy.analytic_proxy import (  # noqa: E402
    ProxyStone, attack_score, calibrate_force_lookup, calibrate_from_recovered_formula,
    conservative_parent_indices, make_initial_candidates, refine_candidates, simulate_batch,
)
from planning_proxy.competition_rules import (  # noqa: E402
    RuleBoardStone, free_guard_rule_violations, is_in_free_guard_zone,
)
from planning_proxy.strict_refine import (  # noqa: E402
    BoardStone, Candidate, StrictEvaluation, evaluate_one, is_loss_budget_candidate,
    local_candidates_for_parent, make_position, selection_priority,
)
from training_research.opponents.teammate_ppo_adapter import TeammatePPOOpponent  # noqa: E402
from training_research.opponents.aggressive_strategy_adapter import AggressiveStrategyOpponent  # noqa: E402


DEFAULT_OUTPUT = ROOT / "planning_proxy" / "runs" / "proxy_vs_teammate_ppo.json"


def centre_distance(state: dict[str, Any]) -> float:
    return math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y)


def canonical_board(states: Sequence[dict[str, Any]], proxy_team: int) -> tuple[list[BoardStone], list[ProxyStone]]:
    """读取真实 PhysX slot 的棋盘；不重编号，避免丢失壶身份与历史姿态。"""

    strict: list[BoardStone] = []
    proxy: list[ProxyStone] = []
    for actual_index, state in enumerate(states):
        if not bool(state["enabled"]):
            continue
        owner = "self" if actual_index % 2 == proxy_team else "opponent"
        stone = BoardStone(
            actual_index, owner, float(state["x"]), float(state["y"]),
            yaw=float(state.get("yaw", 0.0)),
        )
        strict.append(stone)
        proxy.append(ProxyStone(actual_index, owner, stone.x, stone.y))
    return strict, proxy


class ProxyMatchPlayer:
    """将当前一手规划代理接为可评测的非扫冰玩家。"""

    def __init__(self, *, physics_seeds: int, parent_regions: int, decision_budget_seconds: float) -> None:
        self.physics_seeds = int(physics_seeds)
        self.parent_regions = int(parent_regions)
        self.decision_budget_seconds = float(decision_budget_seconds)
        self.params = calibrate_from_recovered_formula()
        self.lookup = calibrate_force_lookup()
        self.environment = StrictCurlingEnd(seed=0, training_fast=True)

    def choose(
        self,
        states: Sequence[dict[str, Any]],
        *,
        proxy_team: int,
        shot_index: int,
        match_seed: int,
    ) -> tuple[tuple[float, float, float], dict[str, Any]]:
        decision_started = time.perf_counter()
        deadline = decision_started + self.decision_budget_seconds

        def finish(shot: tuple[float, float, float], detail: dict[str, Any]) -> tuple[tuple[float, float, float], dict[str, Any]]:
            elapsed = time.perf_counter() - decision_started
            detail["plannerDecisionSeconds"] = elapsed
            detail["plannerBudgetSeconds"] = self.decision_budget_seconds
            detail["plannerBudgetExceeded"] = elapsed > self.decision_budget_seconds
            return shot, detail

        strict_board, proxy_board = canonical_board(states, proxy_team)
        enemies = [stone for stone in strict_board if stone.owner == "opponent"]
        if not enemies:
            return finish((3.0, 0.0, 0.0), {"mode": "draw_no_enemy", "candidateCount": 0})

        protected = {
            stone.index for stone in enemies
            if shot_index <= 4 and is_in_free_guard_zone(stone.x, stone.y)
        }
        attackable = [stone for stone in enemies if stone.index not in protected]
        target = min(attackable, key=lambda stone: math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y), default=None)
        target_index = None if target is None else target.index
        last_hammer = shot_index == STONE_COUNT - 1 and proxy_team == 1 and len(enemies) == 1 and target is not None

        initial = simulate_batch(make_initial_candidates(), proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
        parent_indices = conservative_parent_indices(
            initial, risk_radius_m=0.45, minimum_count=48,
            protected_opponent_indices=protected, must_clear_index=target_index,
        )
        refined = simulate_batch(refine_candidates(initial.shots[parent_indices]), proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
        rough_scores = attack_score(
            refined, protected_opponent_indices=protected, must_clear_index=target_index,
        )
        ordered_rows = [
            {"bestshot": [float(value) for value in refined.shots[index]]}
            for index in np.argsort(-rough_scores)[: self.parent_regions]
        ]

        position = make_position(strict_board)
        seeds = [match_seed + shot_index * 7919 + 104729 * offset for offset in range(self.physics_seeds)]
        evaluated: list[StrictEvaluation] = []
        seen: set[tuple[float, float, float]] = set()
        stopped_for_budget = False
        for rank, row in enumerate(ordered_rows, 1):
            for candidate in local_candidates_for_parent(row, rank, seen):
                if time.perf_counter() >= deadline:
                    stopped_for_budget = True
                    break
                evaluated.append(evaluate_one(
                    self.environment, candidate, strict_board, position, seeds, shot_index,
                    active_index=shot_index,
                ))
            if stopped_for_budget:
                break

        if last_hammer:
            eligible = [
                item for item in evaluated
                if is_loss_budget_candidate(item, 0, target_index, allow_last_hammer_closer_win=True)
            ]
            selection_mode = "last_end_hammer"
        else:
            eligible = []
            selection_mode = "no_submit"
            for budget in range(3):
                bucket = [item for item in evaluated if is_loss_budget_candidate(item, budget, target_index)]
                if bucket:
                    eligible = bucket
                    selection_mode = f"self_out_budget_{budget}"
                    break
        if not eligible and target_index is not None:
            # 被保护守壶或过窄通道导致“必清目标”失败时，退回为只保合法、保己的候选。
            target_index = None
            for budget in range(3):
                bucket = [item for item in evaluated if is_loss_budget_candidate(item, budget)]
                if bucket:
                    eligible = bucket
                    selection_mode = f"safe_fallback_budget_{budget}"
                    break
        if not eligible:
            return finish((3.0, 0.0, 0.0), {
                "mode": "draw_no_strict_candidate", "candidateCount": len(evaluated),
                "protected": sorted(protected), "target": target_index,
                "candidateEvaluationStoppedForBudget": stopped_for_budget,
            })
        # 合规、清敌、出界预算均已满足后，优先选所有摩擦序列中都能留下更多
        # 己方得分壶的路线；若大本营数量相同，再比较原来的清壶收益。
        eligible.sort(key=selection_priority, reverse=True)
        best = eligible[0]
        shot = (best.candidate.v0, best.candidate.h0, best.candidate.w0)
        return finish(shot, {
            "mode": selection_mode, "candidateCount": len(evaluated), "eligibleCount": len(eligible),
            "protected": sorted(protected), "target": target_index,
            "physicsSeeds": seeds, "strict": best.to_json(),
            "selectedOwnInHouse": best.own_in_house,
            "selectedOwnInHouseWorst": min(best.own_in_house, default=0),
            "candidateEvaluationStoppedForBudget": stopped_for_budget,
        })


def state_position(states: Sequence[dict[str, Any]]) -> list[float]:
    position = [0.0] * (STONE_COUNT * 2)
    for index, state in enumerate(states):
        if bool(state["enabled"]):
            position[2 * index] = float(state["x"])
            position[2 * index + 1] = float(state["y"])
    return position


def state_snapshot(states: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """把当前场面压成稳定、可实时写入 JSONL 的记录。"""

    fields = ("x", "y", "yaw", "vx", "vy", "w")
    rows: list[dict[str, Any]] = []
    for index, state in enumerate(states):
        row: dict[str, Any] = {"index": index, "enabled": bool(state.get("enabled", False))}
        for field in fields:
            if field in state:
                row[field] = float(state[field])
        rows.append(row)
    return rows


def rule_board(states: Sequence[dict[str, Any]], acting_team: int) -> list[RuleBoardStone]:
    """以当前出手方为 self，构造自由防守区规则所需的场面。"""

    return [
        RuleBoardStone(
            index=index,
            owner="self" if index % 2 == acting_team else "opponent",
            x=float(state["x"]), y=float(state["y"]), enabled=bool(state.get("enabled", False)),
        )
        for index, state in enumerate(states)
        if bool(state.get("enabled", False))
    ]


def append_log(path: Path, record: dict[str, Any]) -> None:
    """每一手完成即落盘并 flush，便于长对局实时查看。"""

    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        handle.flush()


def run_game(
    *, game_index: int, proxy_team: int, seed: int, proxy: ProxyMatchPlayer,
    opponent: Any, opponent_label: str, progress_path: Path,
) -> dict[str, Any]:
    environment = StrictCurlingEnd(seed=seed, training_fast=True)
    states = environment.reset()
    trace: list[dict[str, Any]] = []
    started = time.perf_counter()
    while environment.shot_number < STONE_COUNT:
        shot_index = environment.shot_number
        team = shot_index % 2
        before = state_snapshot(states)
        rules_before = rule_board(states, team)
        decision_started = time.perf_counter()
        if team == proxy_team:
            shot, detail = proxy.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=seed)
            actor = "proxy"
        else:
            decision = opponent.choose(
                state_position(states), player_is_init=(team == 0), shot_num=shot_index,
                end_score=score_board(states), total_ends=1, current_player=team,
            )
            shot = decision.bestshot
            detail = {
                "tactic": decision.tactic, "actionId": decision.action_id,
                "policyProbability": decision.policy_probability, "value": decision.value,
                "fallback": decision.fallback,
            }
            actor = opponent_label
        decision_seconds = time.perf_counter() - decision_started
        physics_started = time.perf_counter()
        result = environment.play(shot)
        physics_seconds = time.perf_counter() - physics_started
        states = result["states"]
        violations = free_guard_rule_violations(rules_before, states, shot_index=shot_index)
        record = {
            "type": "shot", "game": game_index, "shot": shot_index + 1,
            "team": "first" if team == 0 else "second", "actor": actor,
            "bestshot": list(shot), "detail": detail, "contact": result["contact"],
            "cleared": result["cleared"], "temporaryScoreFirst": score_board(states),
            "decisionSeconds": decision_seconds, "physicsSeconds": physics_seconds,
            "decisionWithinBudget": decision_seconds <= proxy.decision_budget_seconds,
            "frictionSeed": seed + shot_index * 7919,
            "frictionGenerator": "StrictCurlingEnd seed; full sequence is reproducible from this seed",
            "ruleViolations": violations, "stateBefore": before, "stateAfter": state_snapshot(states),
        }
        trace.append(record)
        append_log(progress_path, record)
        print("第%d局 第%02d手 %-5s 决策 %.2fs 物理 %.2fs 当前先手分 %+d%s" % (
            game_index, shot_index + 1, actor, decision_seconds, physics_seconds,
            record["temporaryScoreFirst"], " 规则警告=" + ";".join(violations) if violations else "",
        ), flush=True)
    final_score_first = score_board(states)
    proxy_score = final_score_first if proxy_team == 0 else -final_score_first
    outcome = {
        "proxyTeam": "first" if proxy_team == 0 else "second", "seed": seed,
        "finalScoreFirst": final_score_first, "finalScoreProxy": proxy_score,
        "winner": "proxy" if proxy_score > 0 else opponent_label if proxy_score < 0 else "draw",
        "elapsedSeconds": time.perf_counter() - started, "trace": trace,
    }
    append_log(progress_path, {"type": "game_end", "game": game_index, **{key: value for key, value in outcome.items() if key != "trace"}})
    return outcome


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument("--planner-physics-seeds", type=int, default=3, help="规划器每手严格复核的摩擦序列数；正式评测默认 3。")
    parser.add_argument("--planner-parent-regions", type=int, default=3)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0, help="每手规划硬预算；默认给 2 分钟平台限制留 15 秒余量。")
    parser.add_argument("--opponent", choices=("ppo", "aggressive"), default="ppo", help="本地评测对手。")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--progress-file", type=Path, default=None, help="实时 JSONL 日志；省略时使用 output 同名 .jsonl。")
    args = parser.parse_args()
    if args.planner_physics_seeds < 1 or args.planner_parent_regions < 1 or args.decision_budget_seconds <= 0:
        raise SystemExit("规划器的复核种子数和区域数必须为正")
    progress_path = args.progress_file or args.output.with_suffix(".jsonl")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if progress_path.exists():
        progress_path.unlink()
    append_log(progress_path, {
        "type": "match_start", "schema": "planning_proxy_vs_teammate_ppo_live_v2",
        "seed": args.seed, "plannerPhysicsSeeds": args.planner_physics_seeds,
        "plannerParentRegions": args.planner_parent_regions,
        "decisionBudgetSeconds": args.decision_budget_seconds,
    })
    install_bundled_pyphysx()
    proxy = ProxyMatchPlayer(
        physics_seeds=args.planner_physics_seeds, parent_regions=args.planner_parent_regions,
        decision_budget_seconds=args.decision_budget_seconds,
    )
    if args.opponent == "ppo":
        opponent: Any = TeammatePPOOpponent(deterministic=True)
        opponent_label = "ppo"
        opponent_scope = "teammate PPO deterministic inference"
    else:
        opponent = AggressiveStrategyOpponent()
        opponent_label = "aggressive"
        opponent_scope = "aggresive_ai.py exact strategy_library decision logic (socket bypassed)"
    games = [
        run_game(game_index=1, proxy_team=0, seed=args.seed, proxy=proxy, opponent=opponent, opponent_label=opponent_label, progress_path=progress_path),
        run_game(game_index=2, proxy_team=1, seed=args.seed + 100_003, proxy=proxy, opponent=opponent, opponent_label=opponent_label, progress_path=progress_path),
    ]
    report = {
        "schema": "planning_proxy_vs_teammate_ppo_v2",
        "scope": "non-sweeping; one local strict-PhysX end each way; " + opponent_scope,
        "warning": "integration evaluation only; planning strict check restores current local x/y/yaw and PhysX slots, but local seeded friction is not a Unity match win-rate proof",
        "opponent": args.opponent,
        "plannerPhysicsSeeds": args.planner_physics_seeds,
        "plannerParentRegions": args.planner_parent_regions,
        "decisionBudgetSeconds": args.decision_budget_seconds,
        "liveProgressFile": str(progress_path),
        "games": games,
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    append_log(progress_path, {"type": "match_end", "report": str(args.output)})
    for game in games:
        print("规划代理%s | 先手分=%+d | 规划方分=%+d | 胜方=%s | %.1fs" % (
            "先手" if game["proxyTeam"] == "first" else "后手", game["finalScoreFirst"],
            game["finalScoreProxy"], game["winner"], game["elapsedSeconds"],
        ))
    print("report=%s" % args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
