#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将白盒粗筛出的少数路线交给严格 PhysX 做局部密搜。

这是“全部创飞”规划的第二层：连续数学粗代理只负责挑出少数可能先
撞敌方、且传力方向可能朝边线的路线；本脚本在每条种子周围扰动 v0/h0/w0，
用项目交付的严格 PhysX 真正计算碰撞、连撞、出界和静止。

示例：

    python planning_proxy\\run_whitebox_proxy.py --output planning_proxy\\runs\\p1.json
    python planning_proxy\\strict_refine.py --proxy-report planning_proxy\\runs\\p1.json

最终报告中的 BESTSHOT 才是可提交候选。当前版本固定非扫冰，且只针对一手
“尽量清敌、尽量保己”的攻击评分；真正上线前仍建议把最终前几名按更多随机
摩擦种子复核。
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_R, HOUSE_X, HOUSE_Y, STONE_COUNT, STONE_R, StrictCurlingEnd,
)
from local_simulator.runtime_loader import install_bundled_pyphysx  # noqa: E402
from planning_proxy.competition_rules import RuleBoardStone, free_guard_rule_violations  # noqa: E402


@dataclass(frozen=True)
class BoardStone:
    index: int
    owner: str
    x: float
    y: float
    enabled: bool = True
    # 多手对局中，发生过碰撞的静止壶可能已有非零朝向；这是严格回放输入的一部分。
    yaw: float = 0.0


@dataclass(frozen=True)
class Candidate:
    v0: float
    h0: float
    w0: float
    parent_rank: int


@dataclass
class StrictEvaluation:
    candidate: Candidate
    active_index: int
    scores: List[float]
    enemy_cleared: List[int]
    own_cleared: List[int]
    active_cleared: List[bool]
    total_self_cleared: List[int]
    own_in_house: List[int]
    preserves_all_own: bool
    rule_legal: bool
    rule_violations: List[List[str]]
    enemy_cleared_indices: List[List[int]]
    final_center_distance_by_index: List[Dict[int, float]]
    mean_score: float
    worst_score: float

    def to_json(self) -> dict:
        data = asdict(self)
        data["bestshot"] = [self.candidate.v0, self.candidate.h0, self.candidate.w0]
        return data


def selection_priority(item: StrictEvaluation) -> tuple[float, float, float, float]:
    """合规候选的最终排序键：先尽量多留己方得分壶，再比较清壶收益。

    这是在 ``is_loss_budget_candidate`` 已经完成规则、目标清除和己方出界
    安全筛选之后使用的目标函数。因此它不会为了多留一颗壶而接受违规、漏清
    目标或更高的己方损失；只会在同一安全档的可提交路线中选择更有得分潜力者。
    """

    return (
        float(min(item.own_in_house, default=0)),
        float(statistics.mean(item.own_in_house)) if item.own_in_house else 0.0,
        item.worst_score,
        item.mean_score,
    )


def is_loss_budget_candidate(
    item: StrictEvaluation,
    own_out_budget: int,
    must_clear_index: int | None = None,
    allow_last_hammer_closer_win: bool = False,
) -> bool:
    """检查“允许原有己方壶出界数”的一档可提交约束。

    ``enemy_cleared`` 只由严格终局的 ``enabled=false`` 得出；撞到但仍在
    场内不算清出界。所有己方壶（包括本次出手壶）都只按最终是否出界计数；
    自由防守区规则始终是硬约束。
    """

    if own_out_budget < 0 or not item.rule_legal:
        return False
    if must_clear_index is not None:
        if allow_last_hammer_closer_win:
            return is_last_hammer_target_beaten(item, int(must_clear_index))
        elif not all(int(must_clear_index) in row for row in item.enemy_cleared_indices):
            return False
    for enemy_out, self_out in zip(item.enemy_cleared, item.total_self_cleared):
        if self_out > own_out_budget or self_out > enemy_out:
            return False
        # 进入牺牲己方壶的档位时，每条摩擦序列都至少要实际清掉一颗敌壶。
        if own_out_budget > 0 and enemy_out < 1:
            return False
    return True


def is_last_hammer_target_beaten(item: StrictEvaluation, target_index: int) -> bool:
    """最后一局后手的专用终局条件。

    调用端验证开局只有 ``target_index`` 这一颗敌壶。每条摩擦序列都要求：
    最终在场己方壶数严格大于敌方壶数；若敌壶仍在场，它还必须比己方最近壶
    更远离中心。出手壶按最终是否在场计数，不另设硬约束。
    """

    for final_distances in item.final_center_distance_by_index:
        target_distance = final_distances.get(int(target_index))
        enemy_count = 0 if target_distance is None else 1
        self_distances = [distance for index, distance in final_distances.items() if int(index) == item.active_index or int(index) not in {int(target_index)}]
        # 这里只有一个敌方壶，因此除目标外所有在场壶均为己方（含本次出手壶）。
        if len(self_distances) <= enemy_count:
            return False
        if target_distance is not None and min(self_distances) >= target_distance:
            return False
    return True


def is_full_preserve_candidate(item: StrictEvaluation) -> bool:
    """兼容旧调用：默认档为零原有己方壶出界。"""

    return is_loss_budget_candidate(item, 0)


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def parse_board(raw: Sequence[dict]) -> Tuple[BoardStone, ...]:
    board = tuple(
        BoardStone(
            index=int(item["index"]), owner=str(item["owner"]), x=float(item["x"]), y=float(item["y"]),
            enabled=bool(item.get("enabled", True)), yaw=float(item.get("yaw", 0.0)),
        )
        for item in raw
        if bool(item.get("enabled", True))
    )
    if any(stone.owner not in {"self", "opponent"} for stone in board):
        raise ValueError("board 中 owner 必须是 self 或 opponent")
    if any(stone.index <= 0 or stone.index >= STONE_COUNT for stone in board):
        raise ValueError("当前一手规划保留 slot 0 为出手壶；静止壶 index 必须在 1..15")
    if len({stone.index for stone in board}) != len(board):
        raise ValueError("board 中 stone index 不能重复")
    return board


def make_position(board: Sequence[BoardStone]) -> List[float]:
    position = [0.0] * (STONE_COUNT * 2)
    for stone in board:
        position[2 * stone.index] = stone.x
        position[2 * stone.index + 1] = stone.y
    return position


def local_candidates_for_parent(row: dict, rank: int, seen: set) -> Iterable[Candidate]:
    """单个粗筛区域的 3×3×3 严格小盒；跨区域去重由调用方维护。"""

    values = row.get("bestshot")
    if not isinstance(values, list) or len(values) < 3:
        return
    base_v, base_h, base_w = (float(values[0]), float(values[1]), float(values[2]))
    for dv in (-0.12, 0.0, 0.12):
        for dh in (-0.12, 0.0, 0.12):
            for dw in (-1.5, 0.0, 1.5):
                candidate = Candidate(
                    v0=clamp(base_v + dv, 1.0, 6.0),
                    h0=clamp(base_h + dh, -2.23, 2.23),
                    w0=clamp(base_w + dw, -15.7, 15.7),
                    parent_rank=rank,
                )
                key = (round(candidate.v0, 8), round(candidate.h0, 8), round(candidate.w0, 8))
                if key not in seen:
                    seen.add(key)
                    yield candidate


def evaluate_one(
    environment: StrictCurlingEnd,
    candidate: Candidate,
    board: Sequence[BoardStone],
    position: Sequence[float],
    physics_seeds: Sequence[int],
    shot_index: int,
    active_index: int = 0,
) -> StrictEvaluation:
    scores: List[float] = []
    enemy_counts: List[int] = []
    own_counts: List[int] = []
    active_out: List[bool] = []
    rule_violations: List[List[str]] = []
    enemy_out_indices: List[List[int]] = []
    final_center_distances: List[Dict[int, float]] = []
    own_in_house: List[int] = []
    enemy_indices = {stone.index for stone in board if stone.owner == "opponent"}
    own_indices = {stone.index for stone in board if stone.owner == "self"}
    if not 0 <= int(active_index) < STONE_COUNT:
        raise ValueError("active_index 必须在 0..15")
    # 本次出手壶必须从 factory yaw=0 起步；其他在场壶原样恢复其真实 yaw。
    # 对未启用 slot 也显式写 0，防止上一条候选残留的 PhysX 姿态渗入下一条回放。
    yaw_overrides = {index: 0.0 for index in range(STONE_COUNT)}
    yaw_overrides.update({stone.index: float(stone.yaw) for stone in board if stone.enabled})

    for physics_seed in physics_seeds:
        # ``physics_seed`` 表示这一手实际消耗的摩擦序列种子。若复核的是
        # 多手对局的真实 slot，StrictCurlingEnd 仍要用真实 shot_number 才会
        # 激活同一颗 PhysX 壶，因此将 base seed 反推回去，保证两者相加后
        # 仍精确得到 physics_seed。
        environment.seed = int(physics_seed) - int(active_index) * 7919
        # 每个候选和每条摩擦序列都从完全相同的位置、真实旧壶朝向开始。
        environment.scene.reset_positions(position, yaw_overrides=yaw_overrides)
        environment.shot_number = int(active_index)
        result = environment.play((candidate.v0, candidate.h0, candidate.w0))
        states = result["states"]
        now_enabled = {index for index, state in enumerate(states) if bool(state["enabled"])}
        enemies_out = len(enemy_indices - now_enabled)
        own_out = len(own_indices - now_enabled)
        throw_out = int(active_index) not in now_enabled
        # 敌壶每清走一颗 +100；任一己方壶（含出手壶）出界 -140。
        # 出手壶不再拥有独立的安全地位。
        score = 100.0 * enemies_out - 140.0 * (own_out + float(throw_out))
        scores.append(score)
        enemy_counts.append(enemies_out)
        enemy_out_indices.append(sorted(enemy_indices - now_enabled))
        final_distances = {
            index: ((float(state["x"]) - HOUSE_X) ** 2 + (float(state["y"]) - HOUSE_Y) ** 2) ** 0.5
            for index, state in enumerate(states)
            if bool(state["enabled"]) and (index == int(active_index) or index in enemy_indices or index in own_indices)
        }
        final_center_distances.append(final_distances)
        own_in_house.append(sum(
            1 for index, distance in final_distances.items()
            if (index == int(active_index) or index in own_indices) and distance <= HOUSE_R + STONE_R
        ))
        own_counts.append(own_out)
        active_out.append(throw_out)
        rule_violations.append(
            free_guard_rule_violations(
                [RuleBoardStone(stone.index, stone.owner, stone.x, stone.y, stone.enabled) for stone in board],
                states,
                shot_index=shot_index,
            )
        )

    return StrictEvaluation(
        candidate=candidate,
        active_index=int(active_index),
        scores=scores,
        enemy_cleared=enemy_counts,
        own_cleared=own_counts,
        active_cleared=active_out,
        total_self_cleared=[own + int(active) for own, active in zip(own_counts, active_out)],
        own_in_house=own_in_house,
        # 所有已有己方壶、以及本次出手壶，都必须在每条摩擦序列中留下。
        preserves_all_own=not any(own_counts) and not any(active_out),
        rule_legal=not any(rule_violations),
        rule_violations=rule_violations,
        enemy_cleared_indices=enemy_out_indices,
        final_center_distance_by_index=final_center_distances,
        mean_score=statistics.mean(scores),
        worst_score=min(scores),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proxy-report", type=Path, required=True, help="run_whitebox_proxy.py 输出的 JSON 报告。")
    parser.add_argument("--parent-count", type=int, default=3, help="最多对白盒前几条路线做严格局部密搜。")
    parser.add_argument("--physics-seeds", type=int, default=3, help="每条候选用几条摩擦随机序列复核。")
    parser.add_argument("--seed", type=int, default=20260715, help="第一条 PhysX 摩擦序列种子。")
    parser.add_argument(
        "--shot-index", type=int, default=None,
        help="当前是本局第几次投壶，零基 0..15；省略时读取粗代理报告中的 shotIndex。",
    )
    parser.add_argument(
        "--must-clear-index", type=int, default=None,
        help="必须真正清出界的对方壶 slot；目标在每条摩擦序列的最终状态中均须 enabled=false。",
    )
    # 保留旧命令一版兼容，语义已收紧为“真正出界”。
    parser.add_argument("--must-neutralize-index", type=int, dest="must_clear_index", help=argparse.SUPPRESS)
    parser.add_argument(
        "--last-end-hammer-closer-win", action="store_true",
        help="仅最后一局后手、且场上仅有 --must-clear-index 这一颗敌壶时可用：目标不必出界，但每条摩擦序列都必须比任一己方在场壶更远离中心。",
    )
    parser.add_argument("--max-own-out", type=int, default=2, choices=(0, 1, 2), help="找不到零己方出界路线时，最多逐档放宽到几颗原有己方壶出界。")
    parser.add_argument("--top-k", type=int, default=10, help="报告严格结果前几名。")
    parser.add_argument(
        "--no-stop-on-perfect", action="store_true",
        help="即使已在全部摩擦序列下清空敌壶且零己方/出手损失，也继续搜索所有区域。",
    )
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "planning_proxy" / "runs" / "strict_refine.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.parent_count < 1 or args.physics_seeds < 1 or args.top_k < 1:
        raise SystemExit("--parent-count、--physics-seeds 和 --top-k 都必须至少为 1")
    source = json.loads(args.proxy_report.read_text(encoding="utf-8"))
    if source.get("schema") not in {"whitebox_attack_proxy_p1_v1", "continuous_math_coarse_proxy_v1"}:
        raise SystemExit("--proxy-report 不是可识别的白盒/数学粗代理报告")
    board = parse_board(source.get("board") or [])
    shot_index_raw = args.shot_index if args.shot_index is not None else source.get("shotIndex")
    if shot_index_raw is None or not 0 <= int(shot_index_raw) < STONE_COUNT:
        raise SystemExit("必须提供正确的 --shot-index（零基 0..15），才能安全执行自由防守区规则过滤")
    shot_index = int(shot_index_raw)
    target_index = args.must_clear_index
    if target_index is not None:
        target_index = int(target_index)
        target = next((stone for stone in board if stone.index == target_index), None)
        if target is None or target.owner != "opponent":
            raise SystemExit("--must-clear-index 必须是场上已有的对方壶 slot")
    if args.last_end_hammer_closer_win:
        opponents = [stone.index for stone in board if stone.owner == "opponent"]
        if target_index is None:
            raise SystemExit("--last-end-hammer-closer-win 必须同时指定 --must-clear-index <唯一敌方壶 slot>")
        if opponents != [target_index]:
            raise SystemExit("最后一局后手放宽只适用于场上恰有这一颗敌方壶；当前敌方 slot=%s" % opponents)
    parents = source.get("top") or []
    seeds = [args.seed + 7919 * index for index in range(args.physics_seeds)]

    install_bundled_pyphysx()
    environment = StrictCurlingEnd(seed=seeds[0], training_fast=True)
    position = make_position(board)
    start = time.perf_counter()
    evaluated: List[StrictEvaluation] = []
    seen = set()
    parents_evaluated = 0
    stopped_early_perfect = False
    # “全部创飞且全保”的理论上限。一个候选若在所有摩擦序列下达到它，后续
    # 区域不可能产生更高分，直接停止以保住单核时间预算。
    perfect_score = 100.0 * sum(stone.owner == "opponent" for stone in board)
    for rank, row in enumerate(parents[:args.parent_count], 1):
        batch = list(local_candidates_for_parent(row, rank, seen))
        if not batch:
            continue
        parents_evaluated += 1
        evaluated.extend(evaluate_one(environment, candidate, board, position, seeds, shot_index) for candidate in batch)
        if not args.no_stop_on_perfect and any(
            is_loss_budget_candidate(item, 0, target_index, args.last_end_hammer_closer_win)
            and item.worst_score >= perfect_score
            for item in evaluated
        ):
            stopped_early_perfect = True
            break
    if not evaluated:
        raise SystemExit("白盒报告中没有可精修的候选")
    elapsed = time.perf_counter() - start
    # 普通局面按 0 -> 1 -> 2 逐档放宽，且每条摩擦序列要求已有己方实际出界数
    # 不超过敌方实际出界数。最后一局后手的专用模式则改用最终数量和中心距离，
    # 不再把“交换出界数”作为约束。
    by_budget = {
        budget: [item for item in evaluated if is_loss_budget_candidate(item, budget, target_index, args.last_end_hammer_closer_win)]
        for budget in range(args.max_own_out + 1)
    }
    # 失败时要能分清是“最终比分没翻过来”，还是物理/出界安全约束卡住。
    by_budget_without_target_goal = {
        budget: [item for item in evaluated if is_loss_budget_candidate(item, budget)]
        for budget in range(args.max_own_out + 1)
    }
    last_hammer_target_beaten_count = (
        sum(is_last_hammer_target_beaten(item, target_index) for item in evaluated)
        if args.last_end_hammer_closer_win and target_index is not None else None
    )
    for candidates in by_budget.values():
        candidates.sort(key=selection_priority, reverse=True)
    if args.last_end_hammer_closer_win:
        last_hammer_candidates = by_budget[0]
        selected_budget = None
        selected = last_hammer_candidates[: args.top_k]
        selection_mode = "last_end_hammer_closer_win" if selected else "no_submit_candidate"
    else:
        selected_budget = next((budget for budget, candidates in by_budget.items() if candidates), None)
        selected = [] if selected_budget is None else by_budget[selected_budget][: args.top_k]
        selection_mode = (
            "no_submit_candidate" if selected_budget is None
            else ("full_preserve" if selected_budget == 0 else f"{selected_budget}_own_out_trade")
        )

    print("严格 PhysX 精修：%d 个区域、%d 条候选 × %d 条摩擦序列，%.3f 秒%s。" % (
        parents_evaluated, len(evaluated), len(seeds), elapsed,
        "（已达全清全保，提前停止）" if stopped_early_perfect else "",
    ))
    if not selected:
        print("严格 PhysX 未找到满足当前目标与安全约束的候选；不输出可提交 BESTSHOT。")
    elif args.last_end_hammer_closer_win:
        print("最后一局后手模式：按终局剩余己方壶数 > 敌方壶数，且敌壶更远离中心选择。")
    elif selected_budget and selected_budget > 0:
        print("未找到更低损失档，启用 %d 颗己方原有壶出界档；每条摩擦序列仍要求己方出界数不超过敌方实际出界数。" % selected_budget)
    for rank, item in enumerate(selected, 1):
        candidate = item.candidate
        print(
            "%2d. BESTSHOT %.3f %.3f %.3f | 大本营己方=%s | worst=%.0f mean=%.1f | 清敌=%s 己方总出界=%s（原有=%s，出手=%s）"
            % (
                rank, candidate.v0, candidate.h0, candidate.w0, item.own_in_house, item.worst_score, item.mean_score,
                item.enemy_cleared, item.total_self_cleared, item.own_cleared, item.active_cleared,
            )
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {
                "schema": "whitebox_then_strict_physx_attack_v1",
                "scope": "non-sweeping; strict PhysX is final evaluator",
                "warning": "该评分只覆盖一手清敌保己；最终上线仍应按比赛局面价值重新评分。",
                "sourceProxyReport": str(args.proxy_report),
                "board": [asdict(stone) for stone in board],
                "shotIndex": shot_index,
                "mustClearIndex": target_index,
                "lastEndHammerCloserWin": bool(args.last_end_hammer_closer_win),
                "parentCountCap": args.parent_count,
                "parentsEvaluated": parents_evaluated,
                "candidateCount": len(evaluated),
                "candidateCountsByOwnOutBudget": {str(budget): len(candidates) for budget, candidates in by_budget.items()},
                "candidateCountsByOwnOutBudgetWithoutTargetGoal": {str(budget): len(candidates) for budget, candidates in by_budget_without_target_goal.items()},
                "lastHammerTargetBeatenCandidateCount": last_hammer_target_beaten_count,
                "hasSafeCandidate": bool(by_budget_without_target_goal[0]),
                "hasSubmitCandidate": bool(selected),
                "selectionMode": selection_mode,
                "selectedOwnOutBudget": selected_budget,
                "selectionConstraint": "normal mode: stage 0/1/2 counts every self stone actually out, including the active shot; total self out must not exceed opponent stones actually out on every seed, free-guard-zone rule is hard, and mustClearIndex is actually out. Explicit last-end-hammer-closer-win mode: one initial opponent only; on every seed remaining self count must be strictly greater than remaining opponent count and, if target remains, closest self must be strictly closer to house centre",
                "physicsSeeds": seeds,
                "perfectScore": perfect_score,
                "stoppedEarlyPerfect": stopped_early_perfect,
                "elapsedSeconds": elapsed,
                "top": [item.to_json() for item in selected],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("report=%s" % args.output)


if __name__ == "__main__":
    main()
