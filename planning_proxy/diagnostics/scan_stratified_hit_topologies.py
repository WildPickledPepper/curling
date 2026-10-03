#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用分层的撞击入口扫描补审计 K8 严格求解的父拓扑覆盖。

先用粗代理从全输入格中取“首撞指定目标”的父格并做局部代理细分；随后不是只取
离目标区最近的少数父格，而是按速度、横移、旋转的进入带分层各取一个候选。每个
入口先记原始严格结果，再做同生产求解器一致的单种子局部轮询，最后才三种子复核。
它是离线覆盖审计，不能证明连续空间无解，也不会改变生产候选顺序或状态机。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path, required=True)
    parser.add_argument("--shot", type=int, default=15)
    parser.add_argument("--max-primary", type=int, default=48)
    parser.add_argument("--starts-per-stratum", type=int, default=1)
    parser.add_argument(
        "--selection-mode", choices=("stratified", "contract_quality"), default="stratified",
        help=(
            "stratified：每个撞击入口分层至少保留一条，用于覆盖审计；"
            "contract_quality：只按粗代理的目标区接近度/攻击分全局取前列，用于给定初值后的局部收敛测试。"
        ),
    )
    parser.add_argument(
        "--strict-preflight-count", type=int, default=0,
        help=(
            "仅 contract_quality：先对粗代理排名前 N 条做一次单种子严格合同接近度预检，"
            "再选前 max-primary 条作为初值；0 表示只用粗代理排序。"
        ),
    )
    parser.add_argument("--strict-local-iterations", type=int, default=6)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def source_game(payload: dict[str, Any]) -> dict[str, Any]:
    game = payload.get("game")
    if isinstance(game, dict):
        return game
    games = payload.get("games")
    if isinstance(games, list) and games and isinstance(games[0], dict):
        return games[0]
    raise ValueError("报告不含 game 或 games[0]")


def make_one_outer_plan(plan: Any, strict_board: Sequence[Any]) -> Any:
    from planning_proxy.first_player_strategy import HOUSE_PAIR_LEFT, HOUSE_PAIR_RIGHT, is_in_house

    own = [stone for stone in strict_board if stone.owner == "self"]
    enemy = [stone for stone in strict_board if stone.owner == "opponent"]
    if not (
        str(plan.situation_type) == "P8_ENEMY_THREAT_ONE_OWN"
        and str(plan.phase) == "clear_then_choose_defence_shape"
        and len(own) == 1 and sum(is_in_house(stone) for stone in own) == 0
        and sum(is_in_house(stone) for stone in enemy) == 1
    ):
        raise ValueError("来源未进入一外场己壶、单敌营内威胁的精确 K8 结构")
    target = next(stone for stone in strict_board if int(stone.index) == int(plan.target_opponent_index))
    pair = HOUSE_PAIR_LEFT if float(target.x) >= 2.375 else HOUSE_PAIR_RIGHT
    return replace(
        plan, phase="clear_then_reclaim_first_inner_anchor",
        strategy_type="CLEAR_THREAT_AND_RECLAIM_FIRST_ANCHOR",
        desired_state_type="P8_FIRST_INNER_ANCHOR_RECLAIMED_FROM_ONE_OUTER",
        target_points=pair, defence_shapes=(), landing_region_radius_m=0.35, max_own_cleared=0,
    )


def region_distance(points: np.ndarray, targets: Sequence[Sequence[float]]) -> np.ndarray:
    return np.asarray([
        min(math.hypot(float(point[0]) - float(x), float(point[1]) - float(y)) for x, y in targets)
        for point in points
    ])


def stratum(values: Sequence[float]) -> tuple[int, int, int, int]:
    v, h, w = (float(value) for value in values)
    # 只覆盖 v>=3 的清壶带：目标距出发线约 6m，低速带在历史严格测时中主要
    # 形成无碰撞长尾，且无法把目标壶清出；范围作为报告的一部分，不作无解证明。
    v_bin = min(2, int((v - 3.0) / 1.0))
    h_bin = 0 if h < 0.0 else 1
    w_sign = 0 if w < 0.0 else 1
    w_bin = min(2, int(abs(w) / 5.25))
    return v_bin, h_bin, w_sign, w_bin


def main() -> int:
    args = parse_args()
    total_started = time.perf_counter()
    if int(args.max_primary) < 1:
        raise SystemExit("--max-primary 必须为正数")
    if int(args.starts_per_stratum) < 1:
        raise SystemExit("--starts-per-stratum 必须为正数")
    if int(args.strict_local_iterations) < 0:
        raise SystemExit("--strict-local-iterations 不能小于 0")
    if int(args.strict_preflight_count) < 0:
        raise SystemExit("--strict-preflight-count 不能小于 0")
    if int(args.strict_preflight_count) and args.selection_mode != "contract_quality":
        raise SystemExit("--strict-preflight-count 只能与 --selection-mode contract_quality 一起使用")
    from local_simulator.runtime_loader import install_bundled_pyphysx

    install_bundled_pyphysx()
    import planning_proxy.evaluate_vs_teammate_ppo as planner
    from planning_proxy.first_player_strategy import INNER_RING_R, STONE_R, is_tactically_dead_position
    from planning_proxy.analytic_proxy import attack_score, make_initial_candidates, refine_candidates, simulate_batch
    from planning_proxy.strict_refine import Candidate, evaluate_one, is_loss_budget_candidate, make_position

    payload = json.loads(args.source_report.read_text(encoding="utf-8"))
    game = source_game(payload)
    row = next(item for item in game["trace"] if int(item.get("shot", -1)) == int(args.shot))
    shot_index = int(args.shot) - 1
    strict_board, proxy_board = planner.canonical_board(row["stateBefore"], 0)
    plan = make_one_outer_plan(planner.plan_first_player_turn(proxy_board, shot_index), strict_board)
    target_index = int(plan.target_opponent_index)
    seed0 = int(game["seed"])
    seeds = [seed0 + shot_index * 7919 + 104729 * index for index in range(int(args.physics_seeds))]
    player = planner.ProxyMatchPlayer(physics_seeds=int(args.physics_seeds), parent_regions=3, decision_budget_seconds=105.0)
    coarse_shots = make_initial_candidates(
        velocity_count=planner.FULL_COARSE_VELOCITY_COUNT,
        lateral_count=planner.FULL_COARSE_LATERAL_COUNT,
        spin_count=planner.FULL_COARSE_SPIN_COUNT,
    )
    coarse_started = time.perf_counter()
    coarse = simulate_batch(coarse_shots, proxy_board, player.params, force_lookup=player.lookup, dt=0.02)
    coarse_seconds = time.perf_counter() - coarse_started
    hit_rows = np.flatnonzero((coarse.first_hit_index == target_index) & (coarse_shots[:, 0] >= 3.0))
    attack = attack_score(coarse, protected_opponent_indices=set(), must_clear_index=target_index)
    distances = region_distance(coarse.stop_points[hit_rows], plan.target_points) if len(hit_rows) else np.asarray([])
    # 只细化最接近落区/最有清壶能力的 384 个父格；其余格不在本审计完成覆盖中。
    ordered = hit_rows[np.lexsort((-attack[hit_rows], distances))] if len(hit_rows) else np.asarray([], dtype=np.int32)
    seed_rows = ordered[:384]
    proxy_refine_started = time.perf_counter()
    refined_shots = refine_candidates(np.asarray([coarse_shots[int(row)] for row in seed_rows], dtype=np.float32))
    refined = simulate_batch(refined_shots, proxy_board, player.params, force_lookup=player.lookup, dt=0.02)
    proxy_refine_seconds = time.perf_counter() - proxy_refine_started
    refined_rows = np.flatnonzero(refined.first_hit_index == target_index)
    refined_rows = refined_rows[refined_shots[refined_rows, 0] >= 3.0]
    refined_distances = region_distance(refined.stop_points[refined_rows], plan.target_points) if len(refined_rows) else np.asarray([])
    refined_attack = attack_score(refined, protected_opponent_indices=set(), must_clear_index=target_index)
    ranked = refined_rows[np.lexsort((-refined_attack[refined_rows], refined_distances))] if len(refined_rows) else np.asarray([], dtype=np.int32)
    # 分层模式先保证每个已发现入口至少有一个严格初值，再以同一代理排序补第二个初值。
    # 不能让高分入口的第二个初值挤掉低分入口的唯一初值，否则“分层覆盖”名不副实。
    # 质量模式的目的不同：它只衡量“已有高质量初值后，局部搜索能否收敛”，因此
    # 必须按代理合同接近度直接全局选取，而不能被每层一个较差入口拉低。
    selected: list[int] = []
    selected_set: set[int] = set()
    selected_per_stratum: dict[tuple[int, int, int, int], int] = {}
    if args.selection_mode == "contract_quality":
        for index in ranked:
            selected.append(int(index))
            selected_set.add(int(index))
            if len(selected) >= int(args.max_primary):
                break
    else:
        for index in ranked:
            key = stratum(refined_shots[int(index)])
            if key in selected_per_stratum:
                continue
            selected_per_stratum[key] = selected_per_stratum.get(key, 0) + 1
            selected.append(int(index))
            selected_set.add(int(index))
            if len(selected) >= int(args.max_primary):
                break
        if len(selected) < int(args.max_primary) and int(args.starts_per_stratum) > 1:
            for index in ranked:
                key = stratum(refined_shots[int(index)])
                if int(index) in selected_set or selected_per_stratum.get(key, 0) >= int(args.starts_per_stratum):
                    continue
                selected_per_stratum[key] = selected_per_stratum.get(key, 0) + 1
                selected.append(int(index))
                selected_set.add(int(index))
                if len(selected) >= int(args.max_primary):
                    break

    def target_neutralized(item: Any) -> bool:
        for board in item.final_boards:
            target = next((stone for stone in board if int(stone["index"]) == target_index), None)
            if target is None or not bool(target.get("enabled", False)):
                continue
            if not is_tactically_dead_position(float(target["x"]), float(target["y"])):
                return False
        return bool(item.final_boards)

    def inner_anchor(item: Any) -> bool:
        for point in item.active_final_positions:
            if point is None or math.hypot(float(point[0]) - 2.375, float(point[1]) - 4.88) > INNER_RING_R + STONE_R:
                return False
        return bool(item.active_final_positions)

    def evaluate(values: np.ndarray, rank: int, seed_set: Sequence[int]) -> Any:
        return evaluate_one(
            player.environment,
            Candidate(float(values[0]), float(values[1]), float(values[2]), rank),
            strict_board,
            make_position(strict_board),
            seed_set,
            shot_index,
            active_index=shot_index,
            tactical_plan=plan,
        )

    def clamp(values: np.ndarray) -> np.ndarray:
        return np.asarray((
            np.clip(float(values[0]), 1.0, 6.0),
            np.clip(float(values[1]), -2.23, 2.23),
            np.clip(float(values[2]), -15.7, 15.7),
        ), dtype=np.float64)

    def local_score(item: Any) -> float:
        """只用严格 PhysX 判分；0 表示本物理种子已满足本轮完整合同。"""

        point = item.active_final_positions[0] if item.active_final_positions else None
        distance = (
            min(math.hypot(float(point[0]) - float(x), float(point[1]) - float(y)) for x, y in plan.target_points)
            if point is not None else float("inf")
        )
        return (
            (100.0 if not target_neutralized(item) else 0.0)
            + (100.0 if not bool(item.rule_legal) else 0.0)
            + (100.0 if not bool(item.tactical_goal_met) or not all(item.tactical_goal_met) else 0.0)
            + (40.0 if not is_loss_budget_candidate(item, 0) else 0.0)
            + (100.0 if not inner_anchor(item) else 0.0)
            + max(0.0, distance - float(plan.landing_region_radius_m))
        )

    # 质量集不能再把 MADS 产物倒灌成初值；但可以独立地以一次严格回放检查
    # 粗代理前列是否至少处在正确合同附近。预检只排序原始粗代理球，不做局部
    # 扰动，因此之后交给 MADS/随机精英的仍是真正的共同初值。
    preflight_scores: dict[int, float] = {}
    preflight_items: dict[int, Any] = {}
    strict_preflight_seconds = 0.0
    if int(args.strict_preflight_count):
        preflight_started = time.perf_counter()
        indexed_scores: list[tuple[float, int, int]] = []
        for proxy_rank, index in enumerate(ranked[: int(args.strict_preflight_count)]):
            value = int(index)
            item = evaluate(refined_shots[value], proxy_rank + 1, [seeds[0]])
            score = local_score(item)
            preflight_scores[value] = float(score)
            preflight_items[value] = item
            indexed_scores.append((float(score), int(proxy_rank), value))
        indexed_scores.sort()
        selected = [index for _score, _proxy_rank, index in indexed_scores[: int(args.max_primary)]]
        selected_set = set(selected)
        strict_preflight_seconds = time.perf_counter() - preflight_started

    def strict_local_poll(start: np.ndarray, rank: int, initial_item: Any) -> tuple[np.ndarray, Any, int, float]:
        """固定、可复现的严格 PhysX 轮询；不跨入口带，也不使用粗代理判定。"""

        started = time.perf_counter()
        current = clamp(start)
        # 原始点已经为报告而严格回放过一次，不重复执行同一个 PhysX 输入。
        current_item = initial_item
        current_score = local_score(current_item)
        evaluations = 1
        mesh = 1.0
        for iteration in range(int(args.strict_local_iterations)):
            if current_score <= 0.0:
                break
            phase = (iteration + 1) * 2.399963229728653
            diagonal = np.asarray((math.cos(phase), math.sin(phase), math.cos(phase * 0.6180339887498948)))
            diagonal /= max(float(np.linalg.norm(diagonal)), 1.0e-12)
            directions = [diagonal, -diagonal]
            for axis in range(3):
                unit = np.zeros(3, dtype=np.float64)
                unit[axis] = 1.0
                directions.extend((unit, -unit))
            best_score, best_values, best_item = current_score, current, current_item
            for direction in directions:
                trial = clamp(current + mesh * np.asarray((0.12, 0.12, 1.6)) * direction)
                item = evaluate(trial, rank, [seeds[0]])
                evaluations += 1
                score = local_score(item)
                if score < best_score:
                    best_score, best_values, best_item = score, trial, item
            if best_score < current_score:
                current, current_score, current_item = best_values, best_score, best_item
                mesh = min(1.0, mesh * 1.5)
            else:
                mesh *= 0.5
                if mesh < 1.0 / 16.0:
                    break
        return current, current_item, evaluations, time.perf_counter() - started

    primary_rows: list[dict[str, Any]] = []
    multi_candidates: list[tuple[int, Any]] = []
    strict_raw_seconds = 0.0
    strict_single_seconds = 0.0
    for rank, index in enumerate(selected, 1):
        action = refined_shots[index]
        if int(index) in preflight_items:
            raw_item = preflight_items[int(index)]
            raw_seconds = 0.0
        else:
            raw_started = time.perf_counter()
            raw_item = evaluate(action, rank, [seeds[0]])
            raw_seconds = time.perf_counter() - raw_started
        strict_raw_seconds += raw_seconds
        local_action, item, local_evaluations, local_seconds = strict_local_poll(action, rank, raw_item)
        strict_single_seconds += local_seconds
        clear = target_neutralized(item)
        inner = inner_anchor(item)
        loss_ok = is_loss_budget_candidate(item, 0)
        one_seed_goal = bool(item.tactical_goal_met) and all(item.tactical_goal_met)
        if clear and inner and loss_ok:
            multi_candidates.append((rank, item))
        primary_rows.append({
            "rank": rank,
            "stratum": list(stratum(action)),
            "rawBestshot": [float(value) for value in action],
            "strictLocalBestshot": [float(value) for value in local_action],
            "strictLocalEvaluationCount": int(local_evaluations),
            "strictRawWallSeconds": float(raw_seconds),
            "strictLocalWallSeconds": float(local_seconds),
            "strictPreflightScore": preflight_scores.get(int(index)),
            "proxyDistanceToTargetM": float(region_distance(np.asarray([refined.stop_points[index]]), plan.target_points)[0]),
            "rawOneSeedContractMet": bool(raw_item.tactical_goal_met) and all(raw_item.tactical_goal_met),
            "ruleLegal": bool(item.rule_legal),
            "targetNeutralized": bool(clear),
            "innerAnchor": bool(inner),
            "lossBudgetOk": bool(loss_ok),
            "oneSeedContractMet": bool(one_seed_goal),
        })
    multi_rows: list[dict[str, Any]] = []
    strict_multi_started = time.perf_counter()
    for rank, primary in multi_candidates:
        item = evaluate_one(
            player.environment, primary.candidate, strict_board, make_position(strict_board), seeds, shot_index,
            active_index=shot_index, tactical_plan=plan,
        )
        multi_rows.append({
            "primaryRank": rank,
            "bestshot": [float(primary.candidate.v0), float(primary.candidate.h0), float(primary.candidate.w0)],
            "ruleLegal": bool(item.rule_legal),
            "targetNeutralized": bool(target_neutralized(item)),
            "innerAnchor": bool(inner_anchor(item)),
            "lossBudgetOk": bool(is_loss_budget_candidate(item, 0)),
            "allSeedContractMet": bool(item.tactical_goal_met) and all(item.tactical_goal_met),
        })
    report = {
        "schema": "stratified_k8_hit_topology_strict_audit_v2",
        "scope": (
            "v∈[3,6] 的首撞目标父拓扑有限审计；覆盖由速度/横移/旋转进入带分层，"
            "严格 PhysX 才认证合同。未命中不代表连续空间无解。"
        ),
        "sourceReport": str(args.source_report),
        "sourceSeed": seed0,
        "shot": int(args.shot),
        "physicsSeeds": seeds,
        "plan": plan.to_json(),
        "coverage": {
            "coarseTotal": int(len(coarse_shots)),
            "coarseTargetHitV3to6": int(len(hit_rows)),
            "coarseParentsRefined": int(len(seed_rows)),
            "refinedTotal": int(len(refined_shots)),
            "refinedTargetHitV3to6": int(len(refined_rows)),
            "strataCovered": int(len(selected_per_stratum)),
            "selectionMode": str(args.selection_mode),
            "strictStartsSelected": int(len(selected)),
            "startsPerStratum": int(args.starts_per_stratum),
            "strataAvailable": int(len({stratum(refined_shots[int(index)]) for index in ranked})),
            "strictLocalIterations": int(args.strict_local_iterations),
            "strictPreflightCount": int(min(len(ranked), int(args.strict_preflight_count))),
            "strictLocalEvaluationCount": int(sum(row["strictLocalEvaluationCount"] for row in primary_rows)),
        },
        "timingSeconds": {
            "coarseProxy": float(coarse_seconds),
            "refinedProxy": float(proxy_refine_seconds),
            "strictRawSingleSeed": float(strict_raw_seconds),
            "strictPreflight": float(strict_preflight_seconds),
            "strictSingleSeedLocal": float(strict_single_seconds),
            "strictMultiSeed": float(time.perf_counter() - strict_multi_started),
            "total": float(time.perf_counter() - total_started),
        },
        "primaryCounts": {
            "targetNeutralized": sum(row["targetNeutralized"] for row in primary_rows),
            "innerAnchor": sum(row["innerAnchor"] for row in primary_rows),
            "clearAndInner": len(multi_candidates),
            "oneSeedContractMet": sum(row["oneSeedContractMet"] for row in primary_rows),
        },
        "primaryRows": primary_rows,
        "multiSeedRows": multi_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"coverage": report["coverage"], "primary": report["primaryCounts"], "multiSeedRows": len(multi_rows)}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
