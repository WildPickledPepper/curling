#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运行连续数学粗代理，并输出严格 PhysX 的局部精修候选。

它只负责把连续参数空间压缩为少量“可能撞敌/接近敌方”的区域。严格 PhysX
随后处理真实碰撞、连锁、出界和随机摩擦。当前固定非扫冰。
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Optional, Sequence

import numpy as np

from analytic_proxy import (
    ProxyStone, attack_score, calibrate_force_lookup, calibrate_from_recovered_formula, conservative_parent_indices,
    make_initial_candidates, refine_candidates, simulate_batch,
)
from planning_proxy.competition_rules import is_in_free_guard_zone  # noqa: E402
from planning_proxy.first_player_strategy import plan_first_player_turn, tactical_coarse_score  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOARD = (
    ProxyStone(2, "self", 2.05, 7.25),
    ProxyStone(1, "opponent", 2.55, 5.45),
    ProxyStone(3, "opponent", 2.75, 4.72),
)


def load_board(path: Optional[Path]) -> Sequence[ProxyStone]:
    if path is None:
        return DEFAULT_BOARD
    raw = json.loads(path.read_text(encoding="utf-8"))
    return tuple(
        ProxyStone(int(row["index"]), str(row["owner"]), float(row["x"]), float(row["y"]))
        for row in raw if row.get("enabled", True)
    )


def report_rows(prediction, score, count: int, protected_opponent_indices: set[int]):
    result = []
    for index in np.argsort(-score)[:count]:
        result.append({
            "bestshot": [float(value) for value in prediction.shots[index]],
            "proxyScore": float(score[index]),
            "firstHitIndex": int(prediction.first_hit_index[index]),
            "firstHitOwner": str(prediction.first_hit_owner[index]),
            "nearestEnemyM": float(prediction.nearest_enemy[index]),
            "nearestOwnM": float(prediction.nearest_own[index]),
            "exitsPlay": bool(prediction.exits_play[index]),
            "proxyFirstHitsProtectedGuard": bool(int(prediction.first_hit_index[index]) in protected_opponent_indices),
        })
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", type=Path, default=None)
    parser.add_argument("--shot-index", type=int, required=True, help="当前投壶序号（零基 0..15）；用于自由防守区规则。")
    parser.add_argument("--must-clear-index", type=int, default=None, help="必须真正清出界的对方壶 slot；粗代理会提升直撞及经紧邻己方壶的连锁路线。")
    parser.add_argument("--must-neutralize-index", type=int, dest="must_clear_index", help=argparse.SUPPRESS)
    parser.add_argument("--risk-radius", type=float, default=0.45, help="敌方风险通道半径（米）。")
    parser.add_argument("--minimum-parents", type=int, default=48)
    parser.add_argument("--top-k", type=int, default=16)
    parser.add_argument("--proxy-dt", type=float, default=0.02, help="粗代理受力表积分步长（秒）。")
    parser.add_argument("--first-player", action="store_true", help="启用先手中线控场状态机；仅可用于我方偶数 shot-index。")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "planning_proxy" / "runs" / "analytic_proxy.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.risk_radius <= 0 or args.minimum_parents < 1 or args.top_k < 1 or args.proxy_dt <= 0 or not 0 <= args.shot_index < 16:
        raise SystemExit("风险半径、父区域数量、top-k 都必须为正")
    board = load_board(args.board)
    tactical_plan = None
    if args.first_player:
        try:
            tactical_plan = plan_first_player_turn(board, args.shot_index)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
    target_index = args.must_clear_index
    if target_index is None and tactical_plan is not None and tactical_plan.opponent_action == "physical_clear":
        target_index = tactical_plan.target_opponent_index
    target = None if target_index is None else next((stone for stone in board if stone.index == target_index), None)
    if target_index is not None and (target is None or target.owner != "opponent"):
        raise SystemExit("--must-clear-index 必须是场上已有的对方壶 slot")
    # 细则：第 1--5 次投壶保护对方自由防守区壶。粗代理据此降低首撞这些壶的
    # 路线优先级；严格层会在每个真实终局上做最终的硬合法性裁决。
    protected_opponent_indices = {
        stone.index for stone in board
        if args.shot_index <= 4 and stone.owner == "opponent" and is_in_free_guard_zone(stone.x, stone.y)
    }
    chain_entry_indices = set()
    if target is not None:
        # 从出手端朝大本营推进时，位于目标上游、且与目标足够接近的己方壶可形成
        # 一撞传力链；这里只是保留搜索种子，真实连锁仍由严格 PhysX 判定。
        chain_entry_indices = {
            stone.index for stone in board if stone.owner == "self" and stone.y > target.y
            and ((stone.x - target.x) ** 2 + (stone.y - target.y) ** 2) ** 0.5 <= 0.85
        }
    started = time.perf_counter()
    params = calibrate_from_recovered_formula()
    force_lookup = calibrate_force_lookup()
    initial = simulate_batch(make_initial_candidates(), board, params, force_lookup=force_lookup, dt=args.proxy_dt)
    parent_indices = conservative_parent_indices(
        initial, risk_radius_m=args.risk_radius, minimum_count=args.minimum_parents,
        protected_opponent_indices=protected_opponent_indices,
        must_clear_index=target_index, chain_entry_indices=chain_entry_indices,
    )
    if tactical_plan is not None:
        # 无敌壶的首颗守壶、以及“推到边缘而不能清出界”的第二颗，不能只靠
        # 原先的“贴近敌壶”筛选。把最靠近本轮策略目标的区域并入严格候选。
        initial_base = attack_score(
            initial, protected_opponent_indices=protected_opponent_indices,
            must_clear_index=target_index, chain_entry_indices=chain_entry_indices,
        )
        initial_tactical = np.asarray([
            tactical_coarse_score(
                float(initial.stop_points[index, 0]), float(initial.stop_points[index, 1]),
                int(initial.first_hit_index[index]), float(initial_base[index]), tactical_plan,
            )
            for index in range(len(initial.shots))
        ])
        tactical_parent = np.argsort(-initial_tactical)[:args.minimum_parents]
        parent_indices = np.asarray(list(dict.fromkeys([int(index) for index in parent_indices] + [int(index) for index in tactical_parent])), dtype=np.int32)
    refined = simulate_batch(refine_candidates(initial.shots[parent_indices]), board, params, force_lookup=force_lookup, dt=args.proxy_dt)
    score = attack_score(
        refined, protected_opponent_indices=protected_opponent_indices,
        must_clear_index=target_index, chain_entry_indices=chain_entry_indices,
    )
    if tactical_plan is not None:
        score = np.asarray([
            tactical_coarse_score(
                float(refined.stop_points[index, 0]), float(refined.stop_points[index, 1]),
                int(refined.first_hit_index[index]), float(score[index]), tactical_plan,
            )
            for index in range(len(refined.shots))
        ])
    elapsed = time.perf_counter() - started
    top = report_rows(refined, score, args.top_k, protected_opponent_indices)
    print(
        "数学粗代理：首轮 %d，风险父区 %d，局部 %d，总耗时 %.3fs"
        % (len(initial.shots), len(parent_indices), len(refined.shots), elapsed)
    )
    for rank, row in enumerate(top, 1):
        v0, h0, w0 = row["bestshot"]
        print("%2d. BESTSHOT %.3f %.3f %.3f | %.1f | first=%s/%s | enemy=%.3fm" % (
            rank, v0, h0, w0, row["proxyScore"], row["firstHitOwner"], row["firstHitIndex"], row["nearestEnemyM"],
        ))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "schema": "continuous_math_coarse_proxy_v1",
        "scope": "non-sweeping; formula-only free slide; strict PhysX required for final choice",
        "riskRadiusM": args.risk_radius,
        "shotIndex": args.shot_index,
        "protectedOpponentFreeGuardIndices": sorted(protected_opponent_indices),
        "mustClearIndex": target_index,
        "firstPlayerPlan": None if tactical_plan is None else tactical_plan.to_json(),
        "chainEntryIndices": sorted(chain_entry_indices),
        "parameters": params.__dict__,
        "forceLookup": force_lookup.metadata(),
        "proxyDtSeconds": args.proxy_dt,
        "board": [stone.__dict__ for stone in board],
        "initialCandidateCount": int(len(initial.shots)),
        "parentRegionCount": int(len(parent_indices)),
        "refinedCandidateCount": int(len(refined.shots)),
        "elapsedSeconds": elapsed,
        "top": top,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("report=%s" % args.output)


if __name__ == "__main__":
    main()
