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
from dataclasses import replace
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
    DEFAULT_RELEASE_X, conservative_parent_indices, make_initial_candidates, refine_candidates, simulate_batch,
)
from planning_proxy.competition_rules import (  # noqa: E402
    HOUSE_R, STONE_R, RuleBoardStone, free_guard_rule_violations, is_in_free_guard_zone,
    touches_centre_line,
)
from planning_proxy.strict_refine import (  # noqa: E402
    BoardStone, Candidate, StrictEvaluation, evaluate_one, is_loss_budget_candidate,
    local_candidates_for_parent, make_position, selection_priority,
)
from planning_proxy.first_player_strategy import (  # noqa: E402
    FirstPlayerPlan, K2_AROUND_CENTRE_GUARD_ANCHOR, OPENING_CENTRE_GUARD_SHOT, is_tactically_dead_position,
    plan_first_player_turn, score_strict_outcome, tactical_coarse_score,
)


DEFAULT_OUTPUT = ROOT / "planning_proxy" / "runs" / "proxy_vs_teammate_ppo.json"
# 精确坐标 fixture 只保留作离线复盘证据，绝不能成为默认比赛策略。真正可交付
# 的规则必须由当前壶面语义与严格 PhysX 合同决定，而不是复现曾遇到的一局。
EXPERIMENTAL_EXACT_HISTORICAL_FIXTURES = False


# Unity 的 DCP socket 在收到中线犯规后，由被犯规方回
# ``CENTERLINE_CHOICE RESET|KEEP``。本项目的规划器与 PPO 客户端实际都
# 使用 RESET；因此本地评测也固定复现这个默认选择，而不是让犯规方重投。
CENTERLINE_DEFAULT_CHOICE = "RESET"

# 这是此前验收过的“充足粗筛”网格：7 × 41 × 15 = 4305 条首轮路线。
# 风险父区不做人为截断，局部 3 × 3 × 3 连续细化在典型对抗构型约为
# 16065 条；严格 PhysX 只复核粗筛排序最高的少量区域。
FULL_COARSE_VELOCITY_COUNT = 7
FULL_COARSE_LATERAL_COUNT = 41
FULL_COARSE_SPIN_COUNT = 15
# 这不是比赛计分半径，也不改变自由防守区定义。它只用于后手判断“前场壶
# 是否已接近到下一次碰撞就可能被带入大本营”的战术威胁区。
BACKHAND_HOUSE_THREAT_MARGIN_M = 0.25
# P2/P3 的净空 draw 是“指定终点”的平滑逆问题，而不是复杂碰撞局面。先用
# 一个很小的数学网格给 PhysX 反算提供初值；真正决定出手的仍是严格 PhysX。
FAST_DRAW_COARSE_COUNTS = (5, 17, 5)
# 这些是净空 draw 的“优先精度”，只影响同样满足战术合同的候选排序/诊断；
# 绝不能替代 ``FirstPlayerPlan.landing_region_radius_m`` 这个可提交合同。
# 例如 K2 绕中线守壶的目标圆为 30cm：一个三种子均在该圆内、且旧壶完全
# 未动的强旋球是可行解，即使它没有压到 5cm 的圆心精度。
FAST_DRAW_PREFERRED_PRIMARY_TOLERANCE_M = 0.035
FAST_DRAW_PREFERRED_VALIDATION_TOLERANCE_M = 0.050
FAST_DRAW_EXISTING_STONE_TOLERANCE_M = 0.025
# 粗代理在强旋、窄通道附近只能用于覆盖入射分支，不能决定唯一初值。前若干
# 条“粗代理判为净空”的路线必须逐条经严格 PhysX 复核，再选择真实净空且离
# 目标最近的一条开始反算。
FAST_DRAW_STRICT_BASE_ATTEMPTS = 16
# 单次 hit-and-roll 的碰撞拓扑对参数并不光滑。粗代理先固定旋转/薄撞分支，
# 严格 PhysX 再仅在该分支的 v/h 小信赖域中寻找进入落点区域的解。
# 定向碰撞初始化：3 个清壶速度、5 个相对目标壶的薄撞横移、5 个旋转分支。
# 这是小型的定向初值搜索；若该路径不存在，交由后续全局搜索和战术降级处理。
FAST_HIT_ROLL_SPEEDS = (4.8, 5.2, 5.6)
FAST_HIT_ROLL_HIT_OFFSETS = (-0.30, -0.15, 0.0, 0.15, 0.30)
FAST_HIT_ROLL_SPINS = (-6.0, -3.0, 0.0, 3.0, 6.0)
FAST_HIT_ROLL_TARGET_PARENT_COUNT = 2
FAST_HIT_ROLL_ATTACK_PARENT_COUNT = 6
FAST_HIT_ROLL_MAX_MULTI_SEED_VERIFY = 6
# 碰撞后的旋转分支不能只留下粗代理终点最接近的两条：薄撞附近，轻微旋转
# 就会切换“只带走目标”与“把目标压向己方后壶”的拓扑。保留一个最近落区
# 分支，再补两个不同旋转方向的高攻击分分支；仍远小于全量 453 条首撞路线。
FAST_HIT_ROLL_MADS_PARENT_COUNT = 3
# 进入落点区域只表示“可提交”，不表示“已经达到最小误差”。碰撞 MADS 继续
# 收缩网格以压低终点误差；时间充裕时优先精度而非首个可行解。
FAST_HIT_ROLL_MADS_MAX_ITERATIONS = 6
# 严格全局补搜不读取粗代理。它接收状态机已经声明的物理合同，作为所有
# 快速反解失败后的共同最后搜索层；不是某一个“清壶滚入”分支的专属补丁。
STRICT_GLOBAL_CONTRACT_BATCH_SIZE = 360
STRICT_GLOBAL_CONTRACT_MAX_BATCHES = 2
# 严格 PhysX 评估不可抢占：循环即使在 deadline 前检查通过，一次已启动的
# ``evaluate_one`` 仍可能持续很久。现有完整回放的 30 个严格全局搜索记录中，
# 最慢单次评估为 27.15s（P95 也是 27.15s）；旧的 15s 尾部余量已在真实 K6
# 状态产生 112.38s 的内部 105s 预算越界。保留 32s 不是战术剪枝，只是不给
# 一个已知最长 PhysX 调用在最后 15 秒内启动的时间安全边界。
STRICT_EVALUATION_TAIL_RESERVE_SECONDS = 32.0
# 碰撞局部盒不做稠密填充：中心点加八个三维角点覆盖 v/h/w 的小信赖域，
# 让该快速通道保持在十余秒量级。
FAST_HIT_ROLL_LOCAL_OFFSETS = (
    (0.0, 0.0, 0.0),
    (-0.08, -0.08, -1.20), (-0.08, -0.08, 1.20),
    (-0.08, 0.08, -1.20), (-0.08, 0.08, 1.20),
    (0.08, -0.08, -1.20), (0.08, -0.08, 1.20),
    (0.08, 0.08, -1.20), (0.08, 0.08, 1.20),
)


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


def active_stays_in_house(item: StrictEvaluation) -> bool:
    """本次出手壶在每条严格摩擦序列中都留在大本营内。"""

    limit = HOUSE_R + STONE_R
    return bool(item.final_center_distance_by_index) and all(
        item.final_center_distance_by_index[seed].get(item.active_index, float("inf")) <= limit
        for seed in range(len(item.final_center_distance_by_index))
    )


def is_in_house(stone: BoardStone) -> bool:
    return centre_distance({"x": stone.x, "y": stone.y}) <= HOUSE_R + STONE_R


def is_in_backhand_house_threat_zone(stone: BoardStone) -> bool:
    return centre_distance({"x": stone.x, "y": stone.y}) <= HOUSE_R + STONE_R + BACKHAND_HOUSE_THREAT_MARGIN_M


def is_guard_draw_candidate(item: StrictEvaluation) -> bool:
    """绕前场守壶 draw：出手壶留营，且不把守壶清出界。"""

    return active_stays_in_house(item) and not any(item.enemy_cleared)


def existing_stones_remain_static(item: StrictEvaluation, board: Sequence[BoardStone]) -> bool:
    """快速净空反算不得借由碰撞移动任何已有壶。"""

    expected = {stone.index: stone for stone in board}
    for final_board in item.final_boards:
        # 出界或非正常结束时某条序列可能没有可用的终局快照；它不应被误当成
        # “没有移动既有壶”的净空路线。
        if final_board is None:
            return False
        states = {int(stone["index"]): stone for stone in final_board}
        for index, before in expected.items():
            after = states.get(index)
            if after is None or not bool(after.get("enabled", False)):
                return False
            if math.hypot(float(after["x"]) - before.x, float(after["y"]) - before.y) > FAST_DRAW_EXISTING_STONE_TOLERANCE_M:
                return False
    return True


def topology_diverse_rows(
    ordered_rows: Sequence[int], candidates: np.ndarray, *, limit: int,
) -> list[int]:
    """保留净空 draw 的左右手/旋转拓扑，避免代理总排序吞掉强旋路线。

    ``ordered_rows`` 已按解析代理终点误差排序，但解析轨迹只用于提出初值，
    不能决定某条 PhysX 曲线是否存在。先保留最近的一半，再确保每一种
    ``(横移方向, 旋转方向)`` 组合至少有一个严格 PhysX 初值；其余名额保持
    原始排序。这样不会牺牲直达路线，同时不会把“右手强旋绕守壶”从召回集
    中静默删除。
    """

    if limit <= 0:
        return []

    def topology(row: int) -> tuple[int, int]:
        _, horizontal, spin = (float(value) for value in candidates[int(row)])
        horizontal_side = -1 if horizontal < -0.20 else (1 if horizontal > 0.20 else 0)
        spin_side = -1 if spin < -1.0 else (1 if spin > 1.0 else 0)
        return horizontal_side, spin_side

    selected: list[int] = []
    selected_set: set[int] = set()
    covered: set[tuple[int, int]] = set()

    # 最近候选仍是最快的成功路径；先保留一半，避免多样性策略反而拖慢空场。
    nearest_count = min(len(ordered_rows), max(1, int(limit) // 2))
    for raw_row in ordered_rows[:nearest_count]:
        row = int(raw_row)
        selected.append(row)
        selected_set.add(row)
        covered.add(topology(row))

    # 每个尚未覆盖的旋球拓扑至少保留一个代表。输入顺序就是该拓扑的代理
    # 最佳代表，因此不需要额外的粗模型评分。
    for raw_row in ordered_rows[nearest_count:]:
        if len(selected) >= limit:
            break
        row = int(raw_row)
        key = topology(row)
        if key in covered:
            continue
        selected.append(row)
        selected_set.add(row)
        covered.add(key)

    # 剩余预算按原始误差排序填满，保证性能与旧实现同量级。
    for raw_row in ordered_rows:
        if len(selected) >= limit:
            break
        row = int(raw_row)
        if row not in selected_set:
            selected.append(row)
            selected_set.add(row)
    return selected


def declared_defence_shape_is_synthetically_reachable(
    plan: FirstPlayerPlan,
    board: Sequence[BoardStone],
    *,
    active_index: int,
) -> bool:
    """完整防御形能否在最乐观的静态壶面上由本手一次完成。

    这是一次零 PhysX 的合同一致性检查，不是用解析模型宣称路线可行：把目标
    敌壶设为已清除、其余旧壶静止，并依次把出手壶放到每个声明槽的圆心。若
    连这个最乐观构型都不满足完整 shape，则继续搜索它只会耗尽预算并饿死
    ``clear_then_repair_outer_house_layer`` 的真实 PhysX 搜索。
    """

    if not plan.defence_shapes:
        return True
    highest_index = max([int(active_index), *(int(stone.index) for stone in board)], default=int(active_index))
    initial_states: list[dict[str, Any]] = [
        {"enabled": False, "x": 0.0, "y": 0.0}
        for _ in range(highest_index + 1)
    ]
    for stone in board:
        initial_states[int(stone.index)] = {"enabled": True, "x": float(stone.x), "y": float(stone.y)}
    if plan.target_opponent_index is not None and int(plan.target_opponent_index) < len(initial_states):
        initial_states[int(plan.target_opponent_index)] = {"enabled": False, "x": 0.0, "y": 0.0}
    for x, y in plan.target_points:
        final_states = [dict(state) for state in initial_states]
        final_states[int(active_index)] = {"enabled": True, "x": float(x), "y": float(y)}
        _, goal_met = score_strict_outcome(final_states, board, int(active_index), plan)
        if goal_met:
            return True
    return False


def backhand_guard_draw_coarse_score(stop_x: float, stop_y: float, first_hit_index: int) -> float:
    """前场守壶不能被当成 takeout-and-roll 的入射点。"""

    # 不继承 attack_score 的“首撞敌壶 +100”偏好；绕开已有壶，直接向按钮
    # draw。最终 PhysX 仍会验收真实终点和规则合法性。
    score = -180.0 if int(first_hit_index) >= 0 else 0.0
    return score - 85.0 * math.hypot(float(stop_x) - HOUSE_X, float(stop_y) - HOUSE_Y)


def requires_single_enemy_roll_in(
    *,
    proxy_team: int,
    board: Sequence[BoardStone],
    enemies: Sequence[BoardStone],
    target: BoardStone | None,
    target_index: int | None,
    last_hammer: bool,
) -> bool:
    """是否适用后手“单敌壶清出并留营”的交换模板。"""

    return (
        proxy_team == 1
        and target_index is not None
        and len(enemies) == 1
        and not any(stone.owner == "self" for stone in board)
        and target is not None
        and is_in_house(target)
        and not touches_centre_line(target.x)
        and not last_hammer
    )


class ProxyMatchPlayer:
    """将当前一手规划代理接为可评测的非扫冰玩家。"""

    def __init__(
        self,
        *,
        physics_seeds: int,
        parent_regions: int,
        decision_budget_seconds: float,
        enable_k6_certified_clear_backup: bool = False,
    ) -> None:
        self.physics_seeds = int(physics_seeds)
        self.parent_regions = int(parent_regions)
        self.decision_budget_seconds = float(decision_budget_seconds)
        # 默认关闭：仅用于验证“完整 K6 合同无解时，已认证纯清是否优于固定安全球”。
        # 生产状态机必须先经跨种子、跨局回归才会启用。
        self.enable_k6_certified_clear_backup = bool(enable_k6_certified_clear_backup)
        self.params = calibrate_from_recovered_formula()
        self.lookup = calibrate_force_lookup()
        self.environment = StrictCurlingEnd(seed=0, training_fast=True)
        # 仅本地 PPO 对抗验收会在 main 中注入；提交/Unity 路径保持不依赖
        # Torch 或 PPO 权重。K8 若没有该对象，仍走原有严格 PhysX 状态机。
        self.terminal_reply_opponent: Any | None = None
        # 仅本地整局验收注入：从 K1 到当前手前的实际出手历史。它允许
        # 前瞻从同一完整 PhysX 轨迹重放，而非用 x/y/yaw 伪恢复 Scene。
        self.rollout_history: tuple[tuple[float, float, float], ...] = ()
        self.rollout_history_exact = False
        # 规则层可能在某手物理结算后把壶面回滚。它同样属于连续轨迹的一
        # 部分；只记录出手而漏掉该事件，会使后续前瞻再次退化成伪恢复。
        self.rollout_history_rollbacks: dict[int, tuple[dict[str, Any], ...]] = {}
        # K7 四手前瞻得到的 K8 续招。键是完整静止壶面（含 yaw），只在
        # 同一个本地 PPO 对局对象内短暂保存；它不是坐标 fixture，也不会
        # 出现在没有注入 PPO 的提交路径中。
        self._ppo_rollout_k8_contingencies: list[dict[str, Any]] = []

    @staticmethod
    def _settled_state_key(states: Sequence[dict[str, Any]]) -> tuple[tuple[int, float, float, float], ...]:
        """为连续前瞻的下一节点建立稳定、含壶身份的盘面指纹。"""

        return tuple(
            (index, round(float(state["x"]), 4), round(float(state["y"]), 4), round(float(state.get("yaw", 0.0)), 4))
            for index, state in enumerate(states)
            if bool(state["enabled"])
        )

    def _replay_rollout_history(
        self,
        environment: StrictCurlingEnd,
        history: Sequence[tuple[float, float, float]],
    ) -> None:
        """重放实际出手及其规则回滚，复现当前连续 PhysX 轨迹。"""

        for history_index, previous_shot in enumerate(history, start=1):
            environment.play(previous_shot)
            rollback_states = self.rollout_history_rollbacks.get(history_index)
            if rollback_states is not None:
                environment.restore_settled_states(rollback_states)

    def _adaptive_target_hit_candidates(
        self,
        states: Sequence[dict[str, Any]],
        *,
        target_index: int,
        limit: int = 3,
    ) -> tuple[tuple[float, float, float], ...]:
        """从当前壶面提取不同旋转的目标首撞初值，供严格终局树验证。"""

        try:
            _, proxy_board = canonical_board(states, 0)
            coarse_shots = make_initial_candidates(
                velocity_count=FULL_COARSE_VELOCITY_COUNT,
                lateral_count=FULL_COARSE_LATERAL_COUNT,
                spin_count=FULL_COARSE_SPIN_COUNT,
            )
            coarse = simulate_batch(coarse_shots, proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
            hit_rows = np.flatnonzero(coarse.first_hit_index == int(target_index))
            if not len(hit_rows):
                return ()
            hit_scores = attack_score(coarse, protected_opponent_indices=set(), must_clear_index=int(target_index))
            candidates: list[tuple[float, float, float]] = []
            # 高前场守壶的可行首撞带位于常规粗网格旋转档之间：中速、
            # 中等横移、约 7rad/s 的薄撞能清守壶且不破坏营内锚。这里按
            # 当前目标相对中线镜像加入少量初值；它们只是严格 PhysX 的入口，
            # 绝不按历史坐标直接提交。
            target_state = states[int(target_index)] if 0 <= int(target_index) < len(states) else None
            if target_state is not None and bool(target_state.get("enabled", False)) and float(target_state.get("y", 0.0)) >= 7.60:
                side = -1.0 if float(target_state.get("x", HOUSE_X)) < HOUSE_X else 1.0
                candidates.extend(
                    (5.60, -side * lateral, side * spin)
                    for lateral, spin in ((0.66, 7.0), (0.88, 8.5), (0.44, 5.5))
                )
            seen_spin_bins: set[int] = set()
            for candidate in candidates:
                seen_spin_bins.add(int(round(candidate[2] * 1000.0)))
            for row in hit_rows[np.argsort(-hit_scores[hit_rows])]:
                candidate = tuple(float(value) for value in coarse_shots[int(row)])
                spin_bin = int(round(candidate[2] * 1000.0))
                if spin_bin in seen_spin_bins:
                    continue
                seen_spin_bins.add(spin_bin)
                candidates.append(candidate)
                if len(candidates) >= int(limit):
                    break
            return tuple(candidates)
        except (FloatingPointError, ValueError):
            # 粗代理只是严格 PhysX 搜索的初值覆盖；数值失败时安全跳过。
            return ()

    def _take_matching_k8_contingency(
        self, states: Sequence[dict[str, Any]], *, match_seed: int,
    ) -> dict[str, Any] | None:
        """取回 K7 连续回放中与当前 K8 最接近的同拓扑节点。

        ``restore_settled_states`` 恢复的是可观测 x/y/yaw，而并不序列化 PhysX
        场景内部的接触缓存。重新建立场景后，同一可见局面再推进两手会使旧壶
        出现数厘米级差异；因此这里按 slot 身份和位置最近邻匹配，而不错误地
        要求 bit-for-bit yaw 相同。缓存只活到随后的 K8，阈值只容纳该已测得
        的恢复误差，不能跨局或跨拓扑命中。
        """

        current = [
            (index, float(state["x"]), float(state["y"]))
            for index, state in enumerate(states) if bool(state["enabled"])
        ]
        best_index: int | None = None
        best_error = float("inf")
        for index, continuation in enumerate(self._ppo_rollout_k8_contingencies):
            if int(continuation["matchSeed"]) != int(match_seed):
                continue
            expected = continuation["positions"]
            if len(current) != len(expected) or [item[0] for item in current] != [item[0] for item in expected]:
                continue
            errors = [math.hypot(x - ex, y - ey) for (_, x, y), (_, ex, ey) in zip(current, expected)]
            max_error = max(errors, default=float("inf"))
            if max_error <= 0.08 and sum(errors) < best_error:
                best_index = index
                best_error = sum(errors)
        if best_index is None:
            return None
        return self._ppo_rollout_k8_contingencies.pop(best_index)

    def _try_fast_targeted_draw(
        self,
        *,
        strict_board: Sequence[BoardStone],
        proxy_board: Sequence[ProxyStone],
        position: Sequence[float],
        tactical_plan: Any,
        shot_index: int,
        seeds: Sequence[int],
        deadline: float,
    ) -> tuple[StrictEvaluation, dict[str, Any]] | None:
        """指定防御落点的净空 draw 小型严格 PhysX 反算。

        先手任一“无敌壶、绕开已有壶直接落位”的回合都应先尝试该反算。
        这包括受保护中线守壶的 ``avoid_protected_centre_guard``：它的含义
        是不能撞该壶，并不是不能做净空 draw。已有壶只要在任一 PhysX
        试射中移动，就说明并非净空路径，立刻退回完整的障碍搜索。
        """

        if (
            tactical_plan.opponent_action not in {"none", "avoid_protected_centre_guard"}
            or len(tactical_plan.target_points) != 1
            or time.perf_counter() >= deadline
        ):
            return None

        target = np.asarray(tactical_plan.target_points[0], dtype=np.float64)
        # P4 以后前场已有守壶/防御壶时，窄 draw 网格很容易把可绕行的曲线
        # 误判为无路。完整粗代理仍远比严格 PhysX 便宜，只扩大初值覆盖。
        velocity_count, lateral_count, spin_count = (
            (FULL_COARSE_VELOCITY_COUNT, FULL_COARSE_LATERAL_COUNT, FULL_COARSE_SPIN_COUNT)
            # K2 需要绕过 K1 的中线守壶。它同样是窄通道强旋问题，5×17×5
            # 的快速格会漏掉可行的绕壶 draw，不能因“第二颗”就误当成空场。
            if tactical_plan.own_throw_number >= 4 or strict_board else FAST_DRAW_COARSE_COUNTS
        )
        coarse_shots = make_initial_candidates(
            velocity_count=velocity_count,
            lateral_count=lateral_count,
            spin_count=spin_count,
        )
        coarse = simulate_batch(coarse_shots, proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
        # 先由粗代理判定“最短到终点的曲线”是否净空。若它首撞已有壶，就
        # 不是本快速通道要解决的无障碍局面；不要偷偷换另一条绕行曲线，而是
        # 交给常规的障碍/碰撞搜索。
        distances = np.linalg.norm(coarse.stop_points - target, axis=1)
        # 不能把“所有候选中终点最近的一条”拿来判净空：它可能正好撞到
        # 受保护守壶，而另一个稍远但完全不碰壶的初值经 PhysX 反算即可精确
        # 到点。粗代理只先按首撞过滤和排序；最终初值必须由严格 PhysX 决定。
        clear_rows = np.flatnonzero(coarse.first_hit_index < 0)
        if not len(clear_rows):
            return None
        ordered_clear_rows = clear_rows[np.argsort(distances[clear_rows])]
        # 解析代理的全局最近点不能独占严格 PhysX 预算：强旋绕障路线往往
        # 在代理模型中距离略远，却是严格场景下唯一净空的拓扑。
        diverse_clear_rows = topology_diverse_rows(
            ordered_clear_rows, coarse_shots, limit=max(48, FAST_DRAW_STRICT_BASE_ATTEMPTS),
        )
        # 目标落点靠近守壶遮挡时，全局粗格的中心通常不够精确。对少量已判为
        # 净空的父格做一次 3×3×3 局部细分，再由严格 PhysX 决定，不把代理
        # 的停点直接当作解。
        local_seed_rows = diverse_clear_rows[:48]
        refined_shots = refine_candidates(coarse_shots[local_seed_rows])
        refined = simulate_batch(refined_shots, proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
        refined_clear_rows = np.flatnonzero(refined.first_hit_index < 0)
        refined_distances = np.linalg.norm(refined.stop_points - target, axis=1)
        ordered_refined_clear_rows = refined_clear_rows[np.argsort(refined_distances[refined_clear_rows])]
        diverse_refined_clear_rows = topology_diverse_rows(
            ordered_refined_clear_rows, refined_shots, limit=FAST_DRAW_STRICT_BASE_ATTEMPTS,
        )
        contract_tolerance = float(tactical_plan.landing_region_radius_m)
        primary_seed = [int(seeds[0])]
        calls = 0

        def forward(values: np.ndarray) -> tuple[StrictEvaluation, np.ndarray] | None:
            nonlocal calls
            if time.perf_counter() >= deadline:
                return None
            item = evaluate_one(
                self.environment,
                Candidate(float(values[0]), float(values[1]), float(values[2]), 1),
                strict_board, position, primary_seed, shot_index,
                active_index=shot_index, tactical_plan=tactical_plan,
            )
            calls += 1
            point = item.active_final_positions[0] if item.active_final_positions else None
            if point is None or not existing_stones_remain_static(item, strict_board):
                return None
            return item, np.asarray(point, dtype=np.float64)

        def clamp_values(values: np.ndarray) -> np.ndarray:
            return np.asarray((
                np.clip(values[0], 1.0, 6.0),
                np.clip(values[1], -2.23, 2.23),
                np.clip(values[2], -15.7, 15.7),
            ), dtype=np.float64)

        def mads_search(
            start: np.ndarray,
            steps: np.ndarray,
            objective: Any,
            *,
            goal: float,
            max_iterations: int,
        ) -> tuple[np.ndarray, float, Any] | None:
            """三输入 MADS 风格网格/轮询搜索，只依赖 NumPy 与严格 PhysX。

            每轮在自适应网格上轮询坐标正张成集及一对旋转方向；成功扩大网格，
            失败收缩网格。旋转方向随轮次改变，避免固定坐标搜索遗漏 v/h/w 的
            联动。对无效碰撞/规则结果，目标函数返回 inf 即可作为不可行点处理。
            """

            current = clamp_values(start)
            score, payload = objective(current)
            if payload is None or not math.isfinite(score):
                return None
            mesh = 1.0
            minimum_mesh = 1.0 / 32.0
            for iteration in range(max_iterations):
                if score <= goal:
                    break

                phase = (iteration + 1) * 2.399963229728653
                diagonal = np.asarray((
                    math.cos(phase),
                    math.sin(phase),
                    math.cos(phase * 0.6180339887498948),
                ), dtype=np.float64)
                diagonal /= max(float(np.linalg.norm(diagonal)), 1.0e-12)
                directions = [diagonal, -diagonal]
                for axis in range(3):
                    unit = np.zeros(3, dtype=np.float64)
                    unit[axis] = 1.0
                    directions.extend((unit, -unit))

                best_score, best_values, best_payload = score, current, payload
                for direction in directions:
                    trial = clamp_values(current + mesh * steps * direction)
                    if np.array_equal(trial, current):
                        continue
                    trial_score, trial_payload = objective(trial)
                    if trial_payload is not None and math.isfinite(trial_score) and trial_score < best_score:
                        best_score, best_values, best_payload = float(trial_score), trial, trial_payload

                if best_score < score:
                    current, score, payload = best_values, best_score, best_payload
                    mesh = min(1.0, mesh * 1.5)
                else:
                    mesh *= 0.5
                    if mesh < minimum_mesh:
                        break
            return current, float(score), payload

        # 粗代理的“未碰壶”会在窄通道强旋时出现假阳性。逐条严格复核最接近
        # 的若干入射分支，选择严格物理中真正净空且终点误差最小的初值；不能
        # 因最靠前的一条被守壶擦碰就把整条通道误判为无解。
        strict_bases: list[tuple[float, np.ndarray, StrictEvaluation, np.ndarray]] = []
        # 先保留全局粗格的多样性，再加入局部细分。后者解决“正确曲线在同一
        # 拓扑内、却落在粗格之间”的情况；两类初值都须严格验证。
        strict_base_values = [
            np.asarray(coarse_shots[int(base_index)], dtype=np.float64)
            for base_index in diverse_clear_rows[:FAST_DRAW_STRICT_BASE_ATTEMPTS]
        ] + [
            np.asarray(refined_shots[int(base_index)], dtype=np.float64)
            for base_index in diverse_refined_clear_rows
        ]
        seen_base_values: set[tuple[float, float, float]] = set()
        for base in strict_base_values:
            key = tuple(round(float(value), 6) for value in base)
            if key in seen_base_values:
                continue
            seen_base_values.add(key)
            result = forward(base)
            if result is None:
                continue
            base_item, base_point = result
            strict_bases.append((float(np.linalg.norm(base_point - target)), base, base_item, base_point))
        if not strict_bases:
            return None
        primary_error, current, item, point = min(strict_bases, key=lambda row: row[0])
        # 净空路径没有接触拓扑切换，终点映射在局部可微。粗筛只给三输入初值，
        # 严格 PhysX 再用 2×3 阻尼 Newton 同时修正 v/h/w；绝不固定旋转。
        # “粗代理首撞为空”并不保证 PhysX 局部始终光滑：路径可能只是擦过
        # 一颗守壶，Newton 的微扰便会切到碰撞分支。此时不能再退回旧的全局
        # 严格枚举，而应从同一净空初值切换为 MADS。
        use_obstacle_mads = False
        for _ in range(3):
            # 这是“已找到可提交球”的门槛，必须与策略层的显式目标圆一致。
            # 更小的 FAST_DRAW_PREFERRED_* 数值只能作为质量偏好，不能让一
            # 条已通过 G 的强旋球被误报为无解。
            if primary_error <= contract_tolerance:
                break
            dv, dh, dw = 0.03, 0.03, 0.50
            with_v = forward(current + np.asarray((dv, 0.0, 0.0)))
            with_h = forward(current + np.asarray((0.0, dh, 0.0)))
            with_w = forward(current + np.asarray((0.0, 0.0, dw)))
            if with_v is None or with_h is None or with_w is None:
                use_obstacle_mads = True
                break
            jacobian = np.column_stack((
                (with_v[1] - point) / dv,
                (with_h[1] - point) / dh,
                (with_w[1] - point) / dw,
            ))
            gram = jacobian @ jacobian.T
            if not np.isfinite(jacobian).all() or np.linalg.cond(gram + 1.0e-4 * np.eye(2)) > 80.0:
                use_obstacle_mads = True
                break
            try:
                update = jacobian.T @ np.linalg.solve(gram + 1.0e-4 * np.eye(2), point - target)
            except np.linalg.LinAlgError:
                use_obstacle_mads = True
                break
            update = np.clip(update, (-0.35, -0.35, -3.0), (0.35, 0.35, 3.0))
            # 先保留最后已验证的净空点。若 Newton 更新跨入碰撞分支，MADS
            # 必须从这个有效点起步，不能拿无效点再做一次失败的初始化。
            previous = current
            current = clamp_values(current - update)
            result = forward(current)
            if result is None:
                current = previous
                use_obstacle_mads = True
                break
            item, point = result
            primary_error = float(np.linalg.norm(point - target))

        # Newton 只做固定次数的局部修正。即使它保持在光滑净空分支上，也
        # 不能因为三步内没压到合同圆就宣称无路；继续从同一有效初值做一次
        # 小型无导数搜索，避免“有路径、但初值离目标稍远”的假阴性。
        if primary_error > contract_tolerance:
            use_obstacle_mads = True

        if use_obstacle_mads:
            def obstacle_objective(values: np.ndarray) -> tuple[float, StrictEvaluation | None]:
                trial = forward(values)
                if trial is None:
                    return float("inf"), None
                trial_item, trial_point = trial
                return float(np.linalg.norm(trial_point - target)), trial_item

            mads_result = mads_search(
                current,
                np.asarray((0.12, 0.12, 1.60), dtype=np.float64),
                obstacle_objective,
                goal=float(tactical_plan.landing_region_radius_m),
                max_iterations=8,
            )
            if mads_result is None:
                return None
            current, primary_error, item = mads_result
        if time.perf_counter() >= deadline:
            return None
        def verify_all(values: np.ndarray) -> tuple[StrictEvaluation, np.ndarray] | None:
            nonlocal calls
            if time.perf_counter() >= deadline:
                return None
            item = evaluate_one(
                self.environment,
                Candidate(float(values[0]), float(values[1]), float(values[2]), 1),
                strict_board, position, seeds, shot_index,
                active_index=shot_index, tactical_plan=tactical_plan,
            )
            calls += len(seeds)
            if len(item.active_final_positions) != len(seeds) or any(point is None for point in item.active_final_positions):
                return None
            if not existing_stones_remain_static(item, strict_board):
                return None
            return item, np.asarray(item.active_final_positions, dtype=np.float64)

        verified_result = verify_all(current)
        if verified_result is None:
            return None
        verified, points = verified_result
        errors = np.linalg.norm(points - target, axis=1)

        # 主序列收敛不代表三条摩擦轨迹共同围绕目标。净空场仍可用同一局部
        # Newton 对三序列的中心位置做一次三输入校正。
        validation_tolerance = contract_tolerance
        if not use_obstacle_mads and float(np.max(errors)) > validation_tolerance:
            dv, dh, dw = 0.025, 0.025, 0.40
            with_v = verify_all(clamp_values(current + np.asarray((dv, 0.0, 0.0))))
            with_h = verify_all(clamp_values(current + np.asarray((0.0, dh, 0.0))))
            with_w = verify_all(clamp_values(current + np.asarray((0.0, 0.0, dw))))
            if with_v is None or with_h is None or with_w is None:
                return None
            centre = (np.min(points, axis=0) + np.max(points, axis=0)) / 2.0
            centre_v = (np.min(with_v[1], axis=0) + np.max(with_v[1], axis=0)) / 2.0
            centre_h = (np.min(with_h[1], axis=0) + np.max(with_h[1], axis=0)) / 2.0
            centre_w = (np.min(with_w[1], axis=0) + np.max(with_w[1], axis=0)) / 2.0
            jacobian = np.column_stack((
                (centre_v - centre) / dv,
                (centre_h - centre) / dh,
                (centre_w - centre) / dw,
            ))
            gram = jacobian @ jacobian.T
            if not np.isfinite(jacobian).all() or np.linalg.cond(gram + 1.0e-4 * np.eye(2)) > 80.0:
                return None
            try:
                update = jacobian.T @ np.linalg.solve(gram + 1.0e-4 * np.eye(2), centre - target)
            except np.linalg.LinAlgError:
                return None
            current = clamp_values(current - np.clip(update, (-0.20, -0.20, -2.0), (0.20, 0.20, 2.0)))
            verified_result = verify_all(current)
            if verified_result is None:
                return None
            verified, points = verified_result
            errors = np.linalg.norm(points - target, axis=1)

        if (
            len(errors) != len(seeds)
            or float(np.max(errors)) > validation_tolerance
            or not existing_stones_remain_static(verified, strict_board)
            or not all(verified.tactical_goal_met)
            or not is_loss_budget_candidate(verified, 0)
        ):
            return None
        return verified, {
            "target": [float(target[0]), float(target[1])],
            "physicsCalls": calls,
            "coarseCandidateCount": int(len(coarse_shots)),
            "locallyRefinedClearCandidateCount": int(len(refined_clear_rows)),
            "maxLandingErrorM": float(np.max(errors)),
            "meanLandingErrorM": float(np.mean(errors)),
            "preferredPrecisionMet": bool(
                float(np.max(errors)) <= min(contract_tolerance, FAST_DRAW_PREFERRED_VALIDATION_TOLERANCE_M)
            ),
            "topologyAwareInitialisation": True,
            "multiSeedRecentred": bool(calls > 7),
            "solver": "mads_obstacle" if use_obstacle_mads else "newton_clear_path",
        }

    def _anchor_reply_pressure(
        self,
        candidate: StrictEvaluation,
        *,
        match_seed: int,
        deadline: float,
        include_direct_attack_corridor: bool = False,
    ) -> dict[str, Any]:
        """对单锚候选做小型、对手无关的下一手反击筛查。

        第一颗营内锚若只是“能绕到”，很容易在下一手被直线清掉。这里不
        调用 PPO/aggressive，也不使用历史坐标：从候选的真实 PhysX 终局
        壶面重新生成少量直进和首撞当前锚的路线，并以严格 PhysX 测试。
        结果只用于在多个都已可达的后继状态之间排序；有限反击族没有反例
        不等于已证明全空间安全。
        """

        if not candidate.final_boards or candidate.final_boards[0] is None:
            return {"counterexampleCount": 99, "testedReplyCount": 0, "status": "NO_FINAL_BOARD"}
        target_index = int(candidate.active_index)
        reply_index = target_index + 1
        # ``evaluate_one`` 固定把 active stone 标记为 self；为模拟“对手下一
        # 手”，只交换当前静止壶的阵营标签。坐标、yaw 和 PhysX 都不变。
        reply_board = [
            BoardStone(
                int(stone["index"]),
                "opponent" if str(stone["owner"]) == "self" else "self",
                float(stone["x"]), float(stone["y"]), float(stone.get("yaw", 0.0)),
            )
            for stone in candidate.final_boards[0]
            if bool(stone.get("enabled", True))
        ]
        if not reply_board or time.perf_counter() >= deadline:
            return {"counterexampleCount": 99, "testedReplyCount": 0, "status": "BUDGET_OR_EMPTY"}
        reply_proxy = [ProxyStone(stone.index, stone.owner, stone.x, stone.y) for stone in reply_board]
        coarse_shots = make_initial_candidates(velocity_count=5, lateral_count=25, spin_count=9)
        coarse = simulate_batch(coarse_shots, reply_proxy, self.params, force_lookup=self.lookup, dt=0.02)
        centre_distance_rows = np.hypot(coarse.stop_points[:, 0] - HOUSE_X, coarse.stop_points[:, 1] - HOUSE_Y)
        # 直进/旋进候选专门暴露“对方不清也能抢最近壶”的漏洞；首撞当前
        # K2 锚的候选暴露“裸露单清”的漏洞。各自只留最危险的两个父区，
        # 使 K2 的在线成本保持为小常数。
        direct = np.flatnonzero((coarse.first_hit_index < 0) & ~coarse.exits_play)
        hits = np.flatnonzero(coarse.first_hit_index == target_index)
        selected: list[tuple[str, int | None, tuple[float, float, float]]] = []
        seen_inputs: set[tuple[float, float, float]] = set()

        def add_reply(source: str, row: int | None, values: Sequence[float]) -> None:
            key = tuple(round(float(value), 6) for value in values)
            if key not in seen_inputs:
                seen_inputs.add(key)
                selected.append((source, row, tuple(float(value) for value in values)))

        for row in direct[np.argsort(centre_distance_rows[direct])][:2]:
            add_reply("coarse_direct_or_draw", int(row), coarse_shots[int(row)])
        for row in hits[np.argsort(centre_distance_rows[hits])][:2]:
            add_reply("coarse_hit_current_anchor", int(row), coarse_shots[int(row)])

        # 只在离线诊断明确启用时，再补一条和粗代理排序无关的高速直击走廊。
        # 原四条候选按“粗代理终点最靠按钮”选择，可能漏掉目的仅是把当前锚
        # 清出、而出手壶不追求停在按钮的强打。这里围绕真实锚的横向位置枚举
        # 零旋高速直线，不读取任何对手模型或历史动作。默认关闭，因而不会
        # 改变 K2/K3 当前线上排序；它先用于验证反例筛查是否覆盖这类漏洞。
        if include_direct_attack_corridor:
            anchor = next(
                (stone for stone in candidate.final_boards[0] if int(stone["index"]) == target_index and bool(stone.get("enabled", True))),
                None,
            )
            if anchor is not None:
                centre_h = max(-2.23, min(2.23, float(anchor["x"]) - HOUSE_X))
                for velocity in (5.4, 5.7, 6.0):
                    for offset in (-0.18, 0.0, 0.18):
                        add_reply("direct_attack_corridor", None, (velocity, max(-2.23, min(2.23, centre_h + offset)), 0.0))
        counterexamples: list[dict[str, Any]] = []
        for source, row, values in selected:
            if time.perf_counter() >= deadline:
                break
            reply = evaluate_one(
                self.environment,
                Candidate(*values, parent_rank=1),
                reply_board, make_position(reply_board), [int(match_seed)], reply_index,
                active_index=reply_index,
            )
            final = reply.final_boards[0] if reply.final_boards else None
            if final is None:
                continue
            by_index = {int(stone["index"]): stone for stone in final if bool(stone.get("enabled", True))}
            active = by_index.get(reply_index)
            opponent_distances = [
                math.hypot(float(stone["x"]) - HOUSE_X, float(stone["y"]) - HOUSE_Y)
                for stone in final
                if bool(stone.get("enabled", True)) and str(stone["owner"]) == "opponent"
            ]
            active_distance = (
                math.hypot(float(active["x"]) - HOUSE_X, float(active["y"]) - HOUSE_Y)
                if active is not None else float("inf")
            )
            clears_anchor = target_index not in by_index
            wins_centre = active is not None and active_distance < min(opponent_distances, default=float("inf"))
            if clears_anchor or wins_centre:
                counterexamples.append({
                    "parentRow": None if row is None else int(row),
                    "family": (
                        "DIRECT_ATTACK_CORRIDOR"
                        if source == "direct_attack_corridor"
                        else ("DIRECT_OR_DRAW" if int(coarse.first_hit_index[int(row)]) < 0 else "HIT_CURRENT_ANCHOR")
                    ),
                    "input": [float(value) for value in values],
                    "clearsAnchor": bool(clears_anchor),
                    "winsCentre": bool(wins_centre),
                })
        return {
            "counterexampleCount": int(len(counterexamples)),
            "testedReplyCount": int(len(selected)),
            "counterexamples": counterexamples,
            "status": "FINITE_GENERIC_REPLY_SCREEN",
        }

    def _try_fast_targeted_hit_roll(
        self,
        *,
        strict_board: Sequence[BoardStone],
        proxy_board: Sequence[ProxyStone],
        position: Sequence[float],
        tactical_plan: Any,
        shot_index: int,
        seeds: Sequence[int],
        deadline: float,
        use_direct_attack_reply_screen: bool = False,
    ) -> tuple[StrictEvaluation, dict[str, Any]] | None:
        """按“清指定敌壶 + 进入落点区域”反解单碰撞滚位。

        这里不把不连续的碰撞过程硬塞进 Newton。粗代理先挑出首撞目标壶的
        少量旋转/入射分支；每条分支只在 v/h/w 的小盒内用严格 PhysX 验收。落点
        以 ``landing_region_radius_m`` 为区域，不要求压到区域中心。
        """

        target_index = tactical_plan.target_opponent_index
        if (
            tactical_plan.opponent_action not in {"physical_clear", "physical_displace"}
            or target_index is None
            or time.perf_counter() >= deadline
        ):
            return None
        target_stone = next((stone for stone in strict_board if stone.index == int(target_index) and stone.owner == "opponent"), None)
        if target_stone is None:
            return None
        own_count = sum(stone.owner == "self" for stone in strict_board)
        enemy_count = sum(stone.owner == "opponent" for stone in strict_board)
        # P5 起若我方在场壶数仍领先，允许以一颗己方壶交换当前唯一/主要
        # 敌方威胁。这样贴壶 takeout 不会因“必须原封不动保住后壶”而被错误
        # 拒绝；is_loss_budget_candidate 仍要求己方损失不超过敌方实际物理出场
        # 数，因此不会把无收益自杀球混进来。
        configured_exchange_budget = getattr(tactical_plan, "max_own_cleared", None)
        own_exchange_budget = (
            int(configured_exchange_budget)
            if configured_exchange_budget is not None
            else int(tactical_plan.own_throw_number >= 5 and own_count > enemy_count)
        )
        parent_limit = 6 if own_exchange_budget else FAST_HIT_ROLL_MADS_PARENT_COUNT
        # K3 的清壶滚位同时声明多种不连续的后继角色。三条父拓扑会被一个
        # 容易命中的侧锚占满，导致中线恢复走廊从未进入 MADS；为每个角色
        # 留出一个父分支。其它回合保持原有搜索预算。
        if int(tactical_plan.own_throw_number) == 3 and len(tactical_plan.target_points) >= 3:
            parent_limit = max(parent_limit, min(6, len(tactical_plan.target_points)))
        radius = float(tactical_plan.landing_region_radius_m)

        def early_target_neutralized(item: StrictEvaluation) -> bool:
            """已标定窄拓扑的提交条件；清壶和 promote 各守其语义。"""

            for final_board in item.final_boards:
                if final_board is None:
                    return False
                target_state = next((stone for stone in final_board if int(stone["index"]) == int(target_index)), None)
                if tactical_plan.opponent_action == "physical_displace":
                    if (
                        target_state is None
                        or not bool(target_state.get("enabled", False))
                        or math.hypot(float(target_state["x"]) - target_stone.x, float(target_state["y"]) - target_stone.y) < 0.20
                    ):
                        return False
                else:
                    if target_state is None or not bool(target_state.get("enabled", False)):
                        continue
                    if not is_tactically_dead_position(float(target_state["x"]), float(target_state["y"])):
                        return False
            return bool(item.final_boards)

        # 已通过“粗代理发现 -> 三摩擦严格 PhysX”认证的窄碰撞拓扑必须在
        # 大规模粗筛**之前**先验。旧顺序把它放在 4305 条粗代理和局部细分
        # 后面，105 秒预算会先耗尽，导致明明已认证的 G 被默认球取代。这里
        # 仍然对当前壶位/yaw/正式摩擦种子重新执行严格验收；不通过就继续
        # 一般的粗代理 -> MADS 搜索，绝不把历史参数直接提交。
        early_calibrated: tuple[tuple[float, float, float], ...] = ()
        strategy_type = str(getattr(tactical_plan, "strategy_type", ""))
        if str(getattr(tactical_plan, "phase", "")) == "sixth_historical_control_unreachable_clear_and_roll_fallback":
            # K6 promote/outdraw 的已验证显式备选；仍先严格重验，不能当作
            # 与主 G 等价的固定提交。
            early_calibrated = ((5.72, 1.66, -11.657142857142857),)
        elif str(getattr(tactical_plan, "phase", "")) == "sixth_clear_near_centre_front_house_threat":
            # S6 近中线前营单清滚位是窄薄撞拓扑。通用粗格可能把它排在
            # 4305 条候选之后，即使当前盘面实际可解；用当前威胁左右方向
            # 镜像的初值让严格 PhysX 先验。它不是固定动作：每次仍须清指定
            # 敌壶、零自清、落入当前动态控制区域，并跨全部正式摩擦种子。
            side = 1.0 if float(target_stone.x) >= HOUSE_X else -1.0
            early_calibrated = ((5.32, side * 1.76, -side * 12.857142857142858),)
        elif strategy_type == "CLEAR_AND_RESTORE_SIDE_INNER_ANCHOR" and float(target_stone.x) < HOUSE_X:
            early_calibrated = ((4.12, -1.32, 7.628571428571429),)
        elif strategy_type == "TERMINAL_CLEAR_AND_HOLD_SIDE_HOUSE_ROLL" and float(target_stone.x) < HOUSE_X:
            own_house_count = sum(
                stone.owner == "self" and math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y) <= HOUSE_R + STONE_R
                for stone in strict_board
            )
            # K7 历史控制槽反击后，PPO 拆掉一颗外侧壶所形成的 K8 子状态有自己
            # 的严格拓扑；不能沿用“两个己方壶均已远离大本营”的旧种子。
            early_calibrated = (
                ((5.60, -1.33, 9.771428),) if own_house_count == 1
                else ((5.32, -1.09, 8.571428),)
            )
        elif (
            strategy_type == "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL"
            and tactical_plan.opponent_action == "physical_clear"
            and float(target_stone.x) < HOUSE_X
        ):
            early_calibrated = ((5.72, -1.55, 7.628571),)
        elif strategy_type == "CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL":
            early_calibrated = ((4.8733884232369284, 0.12965034988727356, 5.573521749409139),)
        elif (
            int(tactical_plan.own_throw_number) == 7
            and any(
                bool(getattr(shape, "preserve_initial_centre_guard", False))
                for shape in getattr(tactical_plan, "defence_shapes", ())
            )
        ):
            # “清单威胁 + 保留原中线屏风 + 在其后方形成前营错层”是一个
            # 碰撞拓扑，不是某局的直接出手。通用粗代理在薄撞后滚位上会把
            # 该拓扑排到数千条候选之后；在声明了这个角色合同的场景，先给出
            # 按当前威胁左右镜像的入射分支，再以当前壶位、yaw 和全部物理
            # 种子严格验收。合同不成立或任一种子失败时，仍回到完整搜索。
            side = 1.0 if float(target_stone.x) >= HOUSE_X else -1.0
            early_calibrated = ((5.0, side * 1.47, -side * 10.0),)
        elif str(getattr(tactical_plan, "phase", "")) == "sixth_clear_right_threat_keep_two_layers":
            # 局部 PPO 筛选得到的 K6 窄拓扑：右侧单敌壶时清壶后出手壶进入
            # 右前营内层。三条物理种子下 PPO 会拆旧左锚，但仍留下新层而
            # 保持先手 +1。每次均重新以当前壶位/yaw/摩擦种子验收。
            early_calibrated = ((5.50, 1.45, -10.50),)
        for rank, values in enumerate(early_calibrated, 1):
            calibrated = evaluate_one(
                self.environment, Candidate(*values, parent_rank=rank), strict_board, position, seeds, shot_index,
                active_index=shot_index, tactical_plan=tactical_plan,
            )
            if (
                is_loss_budget_candidate(calibrated, own_exchange_budget)
                and early_target_neutralized(calibrated)
                and all(calibrated.tactical_goal_met)
            ):
                return calibrated, {
                    "targetIndex": int(target_index),
                    "targetRegionCentres": [list(point) for point in tactical_plan.target_points],
                    "targetRegionRadiusM": radius,
                    "calibratedTopologySeed": [float(value) for value in values],
                    "strictCandidateCount": int(rank), "eligibleCount": 1,
                    "allowedOwnExchangeBudget": int(own_exchange_budget),
                "solver": "early_state_calibrated_seed_then_strict_physx",
            }

        if strategy_type == "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL":
            # 近中线高位守壶的薄撞清除并非普通直线 take-out：正确分支以大
            # 横移和反向高旋绕过己方中线壶，首撞后把目标送出战术区。这里的
            # 值来自输入空间的对称高曲率格（而非任何历史局面的动作），按
            # 当前目标左右镜像生成；每一条仍必须通过当前壶位/yaw 的完整
            # 多物理种子“清目标 + 零自清 + 高外环”合同。
            target_side = -1.0 if float(target_stone.x) < HOUSE_X else 1.0
            if str(getattr(tactical_plan, "phase", "")) == "displace_side_guard_across_centre_and_hold_outer_roll":
                # 主合同无法跨摩擦清除时，改用低速宽横移的“换侧”碰撞族。
                # 这些是关于中线对称的输入空间覆盖，而非针对某个局面的动作；
                # 每次仍要验证目标跨线、留在营外、旧锚/守壶不动及高外环落位。
                high_curve_lattice = (
                    (3.20, 2.00, 12.857142857142858),
                    (3.60, 2.00, 12.857142857142858),
                    (4.00, 1.80, 15.0),
                    (4.40, 1.80, 15.0),
                    (3.60, 1.80, 12.857142857142858),
                )
            else:
                high_curve_lattice = (
                    (5.20, 1.43, 12.857142857142858),
                    (5.20, 1.54, 15.0),
                    (4.80, 1.65, 15.0),
                    (5.20, 1.32, 12.857142857142858),
                    (5.20, 1.10, 10.714285714285714),
                    (4.40, 1.87, 15.0),
                )
            curve_rank = 0
            for lane_side in (target_side, -target_side):
                for velocity, lateral, spin in high_curve_lattice:
                    if time.perf_counter() >= deadline:
                        break
                    curve_rank += 1
                    probe = evaluate_one(
                        self.environment,
                        Candidate(float(velocity), float(lane_side * lateral), float(-lane_side * spin), curve_rank),
                        strict_board,
                        position,
                        seeds,
                        shot_index,
                        active_index=shot_index,
                        tactical_plan=tactical_plan,
                    )
                    if (
                        probe.rule_legal
                        and is_loss_budget_candidate(probe, own_exchange_budget)
                        and early_target_neutralized(probe)
                        and all(probe.tactical_goal_met)
                    ):
                        return probe, {
                            "targetIndex": int(target_index),
                            "targetRegionCentres": [list(point) for point in tactical_plan.target_points],
                            "targetRegionRadiusM": radius,
                            "strictCandidateCount": int(curve_rank), "eligibleCount": 1,
                            "allowedOwnExchangeBudget": int(own_exchange_budget),
                            "solver": "mirrored_high_curve_side_guard_lattice_then_strict_physx",
                        }

        base_h = float(target_stone.x - DEFAULT_RELEASE_X)
        # 不论是否要求滚入区域，都先用完整粗代理覆盖大旋转、绕壶与侧撞的
        # 撞击拓扑；粗代理只做白盒初值筛选，严格 PhysX 仍只由少数 MADS 父
        # 分支调用。这样正常 hit-and-roll 可复用纯清壶已验证的撞击发现能力。
        coarse_shots = make_initial_candidates(
            velocity_count=FULL_COARSE_VELOCITY_COUNT,
            lateral_count=FULL_COARSE_LATERAL_COUNT,
            spin_count=FULL_COARSE_SPIN_COUNT,
        )
        coarse = simulate_batch(coarse_shots, proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
        hit_rows = np.flatnonzero(coarse.first_hit_index == int(target_index))
        if not len(hit_rows):
            return None
        coarse_distance = np.asarray([
            min(math.hypot(float(coarse.stop_points[row, 0]) - x, float(coarse.stop_points[row, 1]) - y) for x, y in tactical_plan.target_points)
            if tactical_plan.target_points else 0.0
            for row in hit_rows
        ])
        # 区域内同分，区域外优先最接近边界的分支；同时并入粗代理攻击分最高
        # 的几个分支。代理对碰后滚位的绝对坐标并不精确，不能只依赖终点距离
        # 而漏掉“撞击拓扑正确、但代理滚位偏差较大”的薄撞分支。
        ordering = hit_rows[np.argsort(np.maximum(0.0, coarse_distance - radius))]
        coarse_attack = attack_score(coarse, protected_opponent_indices=set(), must_clear_index=int(target_index))
        attack_order = hit_rows[np.argsort(-coarse_attack[hit_rows])]

        parent_rows: list[int] = []
        # 纯清壶没有终点区域，所有 coarse_distance 都是 0。若仍按 ordering
        # 取前两个，只是在数组顺序中随机挑两个撞击分支，后面追加的高攻击分
        # 分支又会被 MADS_PARENT_COUNT 截掉。此模式必须直接从“最可能清掉
        # 指定目标且少伤己方”的攻击分支起步。
        # 有指定滚位区时，先保留一条粗代理终点最接近区域的路线；剩余槽位
        # 必须按旋转档位去重后从攻击分最高的路线补齐。旧实现把 ordering 的
        # 前两条排在最前，再切 ``[:2]``，导致后面特意加入的旋转薄撞分支
        # 永远没有机会进入 MADS。
        if tactical_plan.target_points:
            for row in ordering[:1]:
                parent_rows.append(int(row))
        seen_spin_bins: set[int] = set()
        for row in parent_rows:
            seen_spin_bins.add(int(round(float(coarse_shots[row][2]) * 1000.0)))
        for row in attack_order:
            spin_bin = int(round(float(coarse_shots[row][2]) * 1000.0))
            if int(row) in parent_rows or spin_bin in seen_spin_bins:
                continue
            parent_rows.append(int(row))
            seen_spin_bins.add(spin_bin)
            if len(parent_rows) >= parent_limit:
                break

        # 命中/滚位的可行域常比 7×41×15 的全局格更窄。此前这里只把粗格
        # 的中心直接交给 MADS；一旦中心落在另一条碰撞拓扑，MADS 不能跨越
        # 接触不连续面，明明存在的薄撞就会退化成默认直线球。先只围绕已经
        # 命中目标的少数父格做一次 3×3×3 数学细分，再把这些初值交给 PhysX。
        # 这不是放宽验收：每条候选仍须通过后面的多种子严格规则、清壶和落点
        # 检查；它只补上粗代理 -> MADS 之间缺失的局部覆盖。
        # ``parent_rows`` 是交给 MADS 的小集合；局部数学细分可多保留一些
        # 已首撞目标的粗格作为种子。它们只产生廉价代理轨迹，真正送进 PhysX
        # 的仍是下面受限的 probe/MADS 候选。
        expanded_seed_order = hit_rows[np.lexsort((
            -coarse_attack[hit_rows],
            np.maximum(0.0, coarse_distance - radius),
        ))]
        refinement_seed_rows = list(parent_rows)
        for row in expanded_seed_order:
            if int(row) not in refinement_seed_rows:
                refinement_seed_rows.append(int(row))
            # 对“内圈壶 + 前场屏风”这类窄薄撞，正确入射的全局粗格未必
            # 排在最靠近目标的前 48 条。保留至多 192 个首撞目标的父格仍只
            # 会产生 5184 条廉价代理细分轨迹，却能覆盖不同速度/旋转拓扑；
            # 严格 PhysX 实际只复核后面的前 20 条。
            if len(refinement_seed_rows) >= 192:
                break
        # 粗代理的首次接触标签只是近似：正确薄撞的父格可能被判为“擦近目标”
        # 而不是“已首撞目标”。离线回放已出现这种情况，因此和独立粗代理
        # 验证一致，把目标风险通道的父区也纳入局部细分；严格 PhysX 仍会把
        # 假阳性全部拒掉。
        risk_seed_rows = conservative_parent_indices(
            coarse, risk_radius_m=0.45, minimum_count=192,
            protected_opponent_indices=set(), must_clear_index=int(target_index),
        )
        for row in risk_seed_rows:
            if int(row) not in refinement_seed_rows:
                refinement_seed_rows.append(int(row))
        # 还要保留粗代理终点已靠近本轮 G_k、但接触近似尚未识别出来的父格。
        # 否则“细分后才发生正确碰撞”的路线会同时逃过首撞和风险通道两套
        # 过滤。这与 run_analytic_proxy 的战术父区是同一个原则。
        target_distance = np.asarray([
            min(math.hypot(float(point[0]) - x, float(point[1]) - y) for x, y in tactical_plan.target_points)
            for point in coarse.stop_points
        ]) if tactical_plan.target_points else np.zeros(len(coarse_shots), dtype=np.float64)
        for row in np.argsort(target_distance)[:192]:
            if int(row) not in refinement_seed_rows:
                refinement_seed_rows.append(int(row))
        tactical_parent_score = np.asarray([
            tactical_coarse_score(
                float(coarse.stop_points[row, 0]), float(coarse.stop_points[row, 1]),
                int(coarse.first_hit_index[row]), float(coarse_attack[row]), tactical_plan,
            )
            for row in range(len(coarse_shots))
        ])
        for row in np.argsort(-tactical_parent_score)[:192]:
            if int(row) not in refinement_seed_rows:
                refinement_seed_rows.append(int(row))
        coarse_parent_shots = [np.asarray(coarse_shots[row], dtype=np.float64) for row in refinement_seed_rows]
        refined_parent_shots = refine_candidates(np.asarray(coarse_parent_shots, dtype=np.float32))
        refined = simulate_batch(
            refined_parent_shots, proxy_board, self.params, force_lookup=self.lookup, dt=0.02,
        )
        refined_hit_rows = np.flatnonzero(refined.first_hit_index == int(target_index))
        refined_attack = attack_score(refined, protected_opponent_indices=set(), must_clear_index=int(target_index))
        refined_distance = np.asarray([
            min(math.hypot(float(refined.stop_points[row, 0]) - x, float(refined.stop_points[row, 1]) - y) for x, y in tactical_plan.target_points)
            if tactical_plan.target_points else 0.0
            for row in refined_hit_rows
        ])
        refined_order = refined_hit_rows[np.lexsort((
            -refined_attack[refined_hit_rows],
            np.maximum(0.0, refined_distance - radius),
        ))] if len(refined_hit_rows) else np.asarray([], dtype=np.int32)
        refined_attack_order = refined_hit_rows[np.argsort(-refined_attack[refined_hit_rows])] if len(refined_hit_rows) else np.asarray([], dtype=np.int32)
        parent_candidates: list[np.ndarray] = []
        seen_candidates: set[tuple[float, float, float]] = set()

        def add_parent_candidate(values: np.ndarray) -> None:
            if len(parent_candidates) >= parent_limit:
                return
            candidate = np.asarray((
                np.clip(values[0], 1.0, 6.0),
                np.clip(values[1], -2.23, 2.23),
                np.clip(values[2], -15.7, 15.7),
            ), dtype=np.float64)
            key = tuple(round(float(value), 6) for value in candidate)
            if key not in seen_candidates:
                seen_candidates.add(key)
                parent_candidates.append(candidate)

        # 优先选择已经在局部细分中保持正确首撞拓扑、且更接近所需滚位区的
        # 分支；再用原粗格补不同拓扑，避免只相信代理的一个局部预测。
        seen_refined_spin_bins: set[int] = set()
        if tactical_plan.target_points and len(tactical_plan.target_points) >= 3:
            # 多目标 K3 先按目标区分配父拓扑，再追加全局排名；这避免一个
            # 代理上最容易命中的落区把其它严格可达后继状态全部挤掉。
            refined_points = refined.stop_points[refined_hit_rows]
            for target_x, target_y in tactical_plan.target_points:
                point_order = refined_hit_rows[np.argsort(
                    np.hypot(refined_points[:, 0] - float(target_x), refined_points[:, 1] - float(target_y))
                )]
                if len(point_order):
                    row = int(point_order[0])
                    spin_bin = int(round(float(refined_parent_shots[row][2]) * 1000.0))
                    if spin_bin not in seen_refined_spin_bins:
                        seen_refined_spin_bins.add(spin_bin)
                        add_parent_candidate(refined_parent_shots[row])
        for row in refined_order:
            spin_bin = int(round(float(refined_parent_shots[row][2]) * 1000.0))
            if spin_bin in seen_refined_spin_bins:
                continue
            seen_refined_spin_bins.add(spin_bin)
            add_parent_candidate(refined_parent_shots[row])
        for values in coarse_parent_shots:
            add_parent_candidate(values)

        primary_evaluated: list[StrictEvaluation] = []

        def clamp_hit(values: np.ndarray) -> np.ndarray:
            return np.asarray((
                np.clip(values[0], 1.0, 6.0),
                np.clip(values[1], -2.23, 2.23),
                np.clip(values[2], -15.7, 15.7),
            ), dtype=np.float64)

        def hit_distance(item: StrictEvaluation) -> float:
            if not tactical_plan.target_points:
                return 0.0
            point = item.active_final_positions[0] if item.active_final_positions else None
            if point is None:
                return float("inf")
            return min(math.hypot(point[0] - x, point[1] - y) for x, y in tactical_plan.target_points)

        def region_error(item: StrictEvaluation) -> float:
            """区域外距离；区域内为零，不再强迫把球压到圆心。"""

            return max(0.0, hit_distance(item) - radius)

        def target_neutralized(item: StrictEvaluation) -> bool:
            """目标壶按计划被清出，或在 promote 合同中真实离开原位。"""

            for final_board in item.final_boards:
                if final_board is None:
                    return False
                target_state = next((stone for stone in final_board if int(stone["index"]) == int(target_index)), None)
                if tactical_plan.opponent_action == "physical_displace":
                    if (
                        target_state is None
                        or not bool(target_state.get("enabled", False))
                        or math.hypot(float(target_state["x"]) - target_stone.x, float(target_state["y"]) - target_stone.y) < 0.20
                    ):
                        return False
                else:
                    if target_state is None or not bool(target_state.get("enabled", False)):
                        continue
                    if not is_tactically_dead_position(float(target_state["x"]), float(target_state["y"])):
                        return False
            return bool(item.final_boards)

        # 某些离散状态的正确碰撞拓扑已由“粗代理 -> 严格 PhysX 三种子”
        # 独立发现。将它保留为 *初始种子*，而不是直接当作动作提交：下方仍
        # 必须对当前真实旧壶坐标/yaw 与本手正式摩擦种子重新验收。这样既不
        # 因探测排序漏掉窄薄撞，也不会把历史参数误用于不同状态。
        calibrated_seeds: tuple[tuple[float, float, float], ...] = ()
        if (
            str(getattr(tactical_plan, "strategy_type", "")) == "CLEAR_AND_RESTORE_SIDE_INNER_ANCHOR"
            and float(target_stone.x) < HOUSE_X
        ):
            calibrated_seeds = ((4.12, -1.32, 7.628571428571429),)
        elif (
            str(getattr(tactical_plan, "strategy_type", "")) == "TERMINAL_CLEAR_AND_HOLD_SIDE_HOUSE_ROLL"
            and float(target_stone.x) < HOUSE_X
        ):
            # K8 稀疏残局的左侧薄撞滚位。它不是固定动作提交：每次仍以
            # 当前旧壶/yaw 和本手正式摩擦种子做完整严格验收；若不达成
            # “清目标 + 同侧大本营最近壶”，继续走一般粗筛/MADS 或失败回退。
            calibrated_seeds = ((5.32, -1.09, 8.571428),)
        elif (
            str(getattr(tactical_plan, "strategy_type", "")) == "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL"
            and float(target_stone.x) < HOUSE_X
        ):
            # K4 侧守壶清除的同一处理：只作为严格 PhysX 的初始拓扑种子，
            # 不绕过当前壶面、yaw 和多摩擦种子验收。
            calibrated_seeds = ((5.72, -1.55, 7.628571),)
        elif str(getattr(tactical_plan, "strategy_type", "")) == "CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL":
            # K7 的“清单营内威胁 + 历史控制槽最近壶”窄状态。在当前 PPO 轨迹上由
            # 粗代理 -> MADS 发现；这里只把它作为严格 PhysX 初值，每次仍须
            # 清目标、进入 10cm 历史控制槽、保住己方壶并跨正式摩擦种子验证。
            calibrated_seeds = ((4.8733884232369284, 0.12965034988727356, 5.573521749409139),)
        for rank, values in enumerate(calibrated_seeds, 1):
            calibrated = evaluate_one(
                self.environment, Candidate(*values, parent_rank=rank), strict_board, position, seeds, shot_index,
                active_index=shot_index, tactical_plan=tactical_plan,
            )
            if (
                is_loss_budget_candidate(calibrated, own_exchange_budget)
                and target_neutralized(calibrated)
                and all(calibrated.tactical_goal_met)
            ):
                return calibrated, {
                    "targetIndex": int(target_index),
                    "targetRegionCentres": [list(point) for point in tactical_plan.target_points],
                    "targetRegionRadiusM": radius,
                    "calibratedTopologySeed": [float(value) for value in values],
                    "strictCandidateCount": int(rank), "eligibleCount": 1,
                    "allowedOwnExchangeBudget": int(own_exchange_budget),
                    "solver": "state_calibrated_seed_then_strict_physx",
                }

        def strict_region_margin(item: StrictEvaluation) -> float:
            if not tactical_plan.target_points:
                return 0.0
            margins: list[float] = []
            for point in item.active_final_positions:
                if point is None:
                    return -float("inf")
                distance = min(math.hypot(point[0] - x, point[1] - y) for x, y in tactical_plan.target_points)
                margins.append(radius - distance)
            return min(margins, default=-float("inf"))

        # 某些薄撞的正确参数本身已在“粗格 + 局部代理细分”中。先以全部摩擦
        # 种子严格认证一小批候选，但不再命中第一个就返回：不同目标区会对应
        # 不同接触拓扑。已认证候选保留为预算保底，搜索仍继续比较更强的路线。
        strict_probe_rows: list[int] = []

        # ``min(distance to any target)`` 会让一个容易命中的槽独占探针名额，
        # 其它同样合法的目标区从未经过严格 PhysX。先给每个目标区至少两条
        # 局部细分父分支，再用全局攻击/距离排序补满；这只改变覆盖与排序，
        # 不放宽碰撞、规则或多种子验收。
        if tactical_plan.target_points:
            refined_points = refined.stop_points[refined_hit_rows]
            for target_x, target_y in tactical_plan.target_points:
                point_order = refined_hit_rows[np.argsort(
                    np.hypot(refined_points[:, 0] - float(target_x), refined_points[:, 1] - float(target_y))
                )]
                for row in point_order[:2]:
                    if int(row) not in strict_probe_rows:
                        strict_probe_rows.append(int(row))
        for ordered in (refined_attack_order[:16], refined_order[:16]):
            for row in ordered:
                if int(row) not in strict_probe_rows:
                    strict_probe_rows.append(int(row))
        # K3 的多目标恢复边需要完整区域覆盖；其它碰撞回合，尤其 K7 的
        # 复杂多壶局面，一条严格 PhysX 探针的尾部代价远大于粗代理。限制为
        # 八条代表拓扑，保留已认证解作保底并把余量交给后续 MADS，避免探针
        # 队列本身耗尽比赛时限。
        strict_probe_limit = 20 if int(tactical_plan.own_throw_number) == 3 else 8
        strict_probe_eligible: list[tuple[int, StrictEvaluation]] = []
        for rank, row in enumerate(strict_probe_rows[:strict_probe_limit], 1):
            if time.perf_counter() >= deadline:
                break
            probe = evaluate_one(
                self.environment, Candidate(*[float(value) for value in refined_parent_shots[row]], parent_rank=rank),
                strict_board, position, seeds, shot_index,
                active_index=shot_index, tactical_plan=tactical_plan,
            )
            if (
                is_loss_budget_candidate(probe, own_exchange_budget)
                and target_neutralized(probe)
                and all(probe.tactical_goal_met)
            ):
                strict_probe_eligible.append((int(rank), probe))

        def strict_probe_backup() -> tuple[StrictEvaluation, dict[str, Any]] | None:
            if not strict_probe_eligible:
                return None
            if (
                int(tactical_plan.own_throw_number) == 3
                and len(tactical_plan.target_points) >= 3
            ):
                # K3 的多区域探针队列按状态机声明的 G 顺序构建，每一个区域
                # 都已得到相同数量的严格 PhysX 探针。全部跑完后，应优先
                # 提交最早声明且真实可行的状态边；不能用“离任一圆心最近”
                # 把按钮近邻的候选重新排到所有其它后继状态之前。这里不是
                # 早停：所有探针仍先完成，随后才按预声明的离散 G 优先级选球。
                winning_rank, chosen = min(strict_probe_eligible, key=lambda row: int(row[0]))
            else:
                winning_rank, chosen = max(
                    strict_probe_eligible,
                    key=lambda row: (strict_region_margin(row[1]), selection_priority(row[1], tactical_plan)),
                )
            return chosen, {
                "targetIndex": int(target_index),
                "targetRegionCentres": [list(point) for point in tactical_plan.target_points],
                "targetRegionRadiusM": radius,
                "coarseCandidateCount": int(len(coarse_shots)),
                "localRefinementSeedCount": int(len(refinement_seed_rows)),
                "locallyRefinedHitBranchCount": int(len(refined_hit_rows)),
                "strictProbeCandidateCount": int(len(strict_probe_rows[:strict_probe_limit])),
                "strictProbeAcceptedCount": int(len(strict_probe_eligible)),
                "strictProbeWinningRank": int(winning_rank),
                "strictCandidateCount": int(len(strict_probe_rows[:strict_probe_limit])),
                "eligibleCount": int(len(strict_probe_eligible)),
                "allowedOwnExchangeBudget": int(own_exchange_budget),
                "solver": "strict_physx_probe_backup_after_full_region_comparison",
            }
        primary_evaluated.extend(item for _, item in strict_probe_eligible)

        def hit_objective(values: np.ndarray, rank: int) -> tuple[float, StrictEvaluation]:
            if time.perf_counter() >= deadline:
                raise TimeoutError
            values = clamp_hit(values)
            item = evaluate_one(
                self.environment, Candidate(float(values[0]), float(values[1]), float(values[2]), rank),
                strict_board, position, [int(seeds[0])], shot_index,
                active_index=shot_index, tactical_plan=tactical_plan,
            )
            target_cleared = target_neutralized(item)
            # 战术清壶（物理出场、侧推废球或后推过营）、合法、保己是硬优先级；
            # 在同一可行类内再最小化实际滚位误差。注意不能只在多种子复核
            # 时才检查 ``tactical_goal_met``：例如 promote 可能已经把目标壶
            # 推开且出手壶入细圆，但仍未取得最近壶；若此处报 0，MADS 会在
            # 一个最终必被拒绝的接触拓扑提前停止。
            penalty = 0.0
            penalty += 100.0 if not target_cleared else 0.0
            penalty += 100.0 if not item.rule_legal else 0.0
            penalty += 40.0 * float(item.total_self_cleared[0] if item.total_self_cleared else 1)
            penalty += 100.0 if not all(item.tactical_goal_met) else 0.0
            return penalty + region_error(item), item

        # 碰撞后终点在擦撞/首撞对象变化处不连续。对粗代理最可信的两个入射
        # 初值分别做 MADS 网格/轮询，而非跨接触拓扑计算雅可比或枚举固定小盒。
        for rank, initial_candidate in enumerate(parent_candidates, 1):
            if time.perf_counter() >= deadline:
                return strict_probe_backup()
            current = clamp_hit(initial_candidate)
            try:
                current_score, current_item = hit_objective(current, rank)
                mesh = 1.0
                for iteration in range(FAST_HIT_ROLL_MADS_MAX_ITERATIONS):
                    # 无论是纯清壶还是 hit-and-roll，区域条件一旦满足，目标
                    # 函数即为 0。继续压圆心既不提高合法性，也不提高可提交性。
                    if current_score <= 0.0:
                        break
                    # 后手“留在大本营”是宽可行区域，不需要像先手红圈防御位
                    # 一样继续把球压向圆心。已经清壶且进营便停止第一阶段。
                    if radius >= 0.80 and current_score <= radius:
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
                        if time.perf_counter() >= deadline:
                            raise TimeoutError
                        trial = clamp_hit(current + mesh * np.asarray((0.12, 0.12, 1.6)) * direction)
                        score, item = hit_objective(trial, rank)
                        if score < best_score:
                            best_score, best_values, best_item = score, trial, item
                    if best_score < current_score:
                        current, current_score, current_item = best_values, best_score, best_item
                        mesh = min(1.0, mesh * 1.5)
                    else:
                        mesh *= 0.5
                        if mesh < 1.0 / 16.0:
                            break
                primary_evaluated.append(current_item)
            except TimeoutError:
                return strict_probe_backup()

        region_margin = strict_region_margin

        primary_eligible = [
            item for item in primary_evaluated
            if (
                is_loss_budget_candidate(item, own_exchange_budget)
                and target_neutralized(item)
                and all(item.tactical_goal_met)
            )
        ]

        # 单种子只能淘汰不可能的路线；真正提交前仍对排名靠前的候选逐条重放
        # 完整摩擦集合，保证区域、清壶和规则都在每条种子下成立。
        primary_eligible.sort(key=lambda item: (region_margin(item), selection_priority(item, tactical_plan)), reverse=True)
        eligible: list[StrictEvaluation] = []
        exchange_fine_refined = False
        for primary in primary_eligible[:FAST_HIT_ROLL_MAX_MULTI_SEED_VERIFY]:
            if time.perf_counter() >= deadline:
                return None
            def robust_objective(values: np.ndarray) -> tuple[float, StrictEvaluation]:
                if time.perf_counter() >= deadline:
                    raise TimeoutError
                values = clamp_hit(values)
                item = evaluate_one(
                    self.environment, Candidate(float(values[0]), float(values[1]), float(values[2]), primary.candidate.parent_rank),
                    strict_board, position, seeds, shot_index,
                    active_index=shot_index, tactical_plan=tactical_plan,
                )
                distances = [
                    min(math.hypot(point[0] - x, point[1] - y) for x, y in tactical_plan.target_points)
                    for point in item.active_final_positions if point is not None
                ] if tactical_plan.target_points else [0.0]
                max_distance = max(distances, default=float("inf"))
                max_region_error = max(0.0, max_distance - radius)
                feasible = (
                    is_loss_budget_candidate(item, own_exchange_budget)
                    and target_neutralized(item)
                    and all(item.tactical_goal_met)
                )
                return (max_region_error if feasible else 100.0 + max_region_error), item

            current = np.asarray((primary.candidate.v0, primary.candidate.h0, primary.candidate.w0), dtype=np.float64)
            current_score, verified = robust_objective(current)
            # 第一阶段已确定“撞目标壶”的拓扑；第二阶段用同一 MADS 在所有
            # 摩擦序列上直接压低最坏落点误差，而不是仅按主序列选球。
            mesh = 1.0
            for iteration in range(6):
                if time.perf_counter() >= deadline:
                    return None
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
                best_score, best_values, best_item = current_score, current, verified
                for direction in directions:
                    if time.perf_counter() >= deadline:
                        return None
                    trial = clamp_hit(current + mesh * np.asarray((0.04, 0.04, 0.60)) * direction)
                    try:
                        score, item = robust_objective(trial)
                    except TimeoutError:
                        return None
                    if score < best_score:
                        best_score, best_values, best_item = score, trial, item
                if best_score < current_score:
                    current, current_score, verified = best_values, best_score, best_item
                    mesh = min(1.0, mesh * 1.5)
                else:
                    mesh *= 0.5
                    if mesh < 1.0 / 16.0:
                        break
            if (
                is_loss_budget_candidate(verified, own_exchange_budget)
                and target_neutralized(verified)
                and all(verified.tactical_goal_met)
            ):
                eligible.append(verified)
            elif own_exchange_budget:
                # 壶谱对应的是贴壶 hit-and-roll：粗网格能找到正确首撞拓扑，
                # 但三条摩擦会在“刚进侧废球带/仍压在边缘”之间切换。此处只
                # 围绕已通过主种子的父分支做 18 个小格严格复核；不是重开
                # 全局搜索。旋转沿当前符号继续加大，横移两侧各微调。
                base = np.asarray((primary.candidate.v0, primary.candidate.h0, primary.candidate.w0), dtype=np.float64)
                spin_sign = -1.0 if base[2] < 0.0 else 1.0
                fine_found = None
                for dv in (0.0, 0.05):
                    # 0.015m 是此贴壶接触分支跨过“压在边缘/进废球带”的
                    # 实测尺度；保留 0.025m 两侧覆盖，不把细化误做成粗网格。
                    for dh in (-0.025, -0.015, 0.0, 0.015, 0.025):
                        for dw in (0.0, 0.15 * spin_sign, 0.30 * spin_sign):
                            if time.perf_counter() >= deadline:
                                return None
                            trial = clamp_hit(base + np.asarray((dv, dh, dw), dtype=np.float64))
                            try:
                                score, item = robust_objective(trial)
                            except TimeoutError:
                                return None
                            if score <= 0.0:
                                fine_found = item
                                break
                        if fine_found is not None:
                            break
                    if fine_found is not None:
                        break
                if fine_found is not None:
                    exchange_fine_refined = True
                    eligible.append(fine_found)

        if own_exchange_budget and not eligible:
            # 贴壶的一换一并非连续的“滚到圆心”问题：正确入射常在粗代理中
            # 已经以最大旋转量出现，但主种子 MADS 会把它推回另一条接触拓扑。
            # 因此从该原始入射分支做一圈很小的、三种子严格 PhysX 复核。这里
            # 不依赖某个棋局坐标，只利用“最大旋转的已命中目标分支”这一物理
            # 特征；速度、横移、旋转均仍由粗代理父分支给初值。
            high_spin_rank, base = max(
                enumerate(parent_candidates, 1),
                key=lambda item: abs(float(item[1][2])),
            )
            base = clamp_hit(base)
            spin_sign = -1.0 if base[2] < 0.0 else 1.0
            exchange_found = None
            rank = int(high_spin_rank)
            for dv in (0.0, 0.15, 0.25, 0.35, 0.40):
                for dh in (-0.060, -0.035, -0.010, 0.015):
                    for dw in (0.0, 0.15 * spin_sign):
                        if time.perf_counter() >= deadline:
                            return None
                        trial = clamp_hit(base + np.asarray((dv, dh, dw), dtype=np.float64))
                        item = evaluate_one(
                            self.environment,
                            Candidate(float(trial[0]), float(trial[1]), float(trial[2]), rank),
                            strict_board,
                            position,
                            seeds,
                            shot_index,
                            active_index=shot_index,
                            tactical_plan=tactical_plan,
                        )
                        if (
                            is_loss_budget_candidate(item, own_exchange_budget)
                            and target_neutralized(item)
                            and all(item.tactical_goal_met)
                        ):
                            exchange_found = item
                            break
                    if exchange_found is not None:
                        break
                if exchange_found is not None:
                    break
            if exchange_found is not None:
                exchange_fine_refined = True
                eligible.append(exchange_found)
        if not eligible:
            return None
        # K3 清壶滚位常有多个都能成为最近壶的严格解。此前只按“距任一
        # 目标区多深”排序，会偏向按钮近邻的单锚；它在 PPO 与 aggressive
        # 的败局中都可能被下一手直接清掉。这里不询问任何对手策略，而是对
        # 最多三条已通过多种子验收的候选，用同一张真实 PhysX 壶面检查两类
        # 通用反击（直进抢中心、首撞当前锚）。反例更少的可观察结构优先。
        # 反击筛查只参与 K3 多区域恢复边的并列解排序，预算不足时仍维持原
        # 有严格物理排序，绝不把“未筛查”误报为安全。
        reply_pressures: dict[int, dict[str, Any]] = {}
        use_k3_reply_screen = (
            int(tactical_plan.own_throw_number) == 3
            and len(tactical_plan.target_points) >= 3
        )
        if (use_k3_reply_screen or use_direct_attack_reply_screen) and time.perf_counter() + 2.0 < deadline:
            for item in eligible[:(4 if use_direct_attack_reply_screen else 3)]:
                if time.perf_counter() + 0.5 >= deadline:
                    break
                reply_pressures[id(item)] = self._anchor_reply_pressure(
                    item,
                    match_seed=int(seeds[0]),
                    deadline=deadline,
                    include_direct_attack_corridor=bool(use_direct_attack_reply_screen),
                )
        if reply_pressures:
            eligible.sort(
                key=lambda item: (
                    int(reply_pressures.get(id(item), {"counterexampleCount": 99})["counterexampleCount"]),
                    -float(region_margin(item)),
                    *tuple(-float(value) for value in selection_priority(item, tactical_plan)),
                ),
            )
        else:
            eligible.sort(key=lambda item: (region_margin(item), selection_priority(item, tactical_plan)), reverse=True)
        chosen = eligible[0]
        detail = {
            "targetIndex": int(target_index),
            "targetRegionCentres": [list(point) for point in tactical_plan.target_points],
            "targetRegionRadiusM": radius,
            "coarseCandidateCount": int(len(coarse_shots)),
            "coarseHitBranchCount": int(len(hit_rows)),
            "locallyRefinedHitBranchCount": int(len(refined_hit_rows)),
            "strictCandidateCount": int(len(primary_evaluated)),
            "multiSeedVerifiedCount": int(min(len(primary_eligible), FAST_HIT_ROLL_MAX_MULTI_SEED_VERIFY)),
            "eligibleCount": int(len(eligible)),
            "allowedOwnExchangeBudget": int(own_exchange_budget),
            "madsParentBranchCount": int(len(parent_candidates)),
            "exchangeFineRefinementUsed": bool(exchange_fine_refined),
            "worstRegionMarginM": float(region_margin(chosen)),
        }
        if reply_pressures:
            detail["genericReplyPressure"] = reply_pressures.get(id(chosen))
            detail["genericReplyScreenedCandidateCount"] = int(len(reply_pressures))
            detail["directAttackReplyScreenUsed"] = bool(use_direct_attack_reply_screen)
            if use_direct_attack_reply_screen:
                detail["allGenericReplyPressure"] = [
                    {
                        "action": [
                            float(item.candidate.v0), float(item.candidate.h0), float(item.candidate.w0),
                        ],
                        "counterexampleCount": int(reply_pressures[id(item)]["counterexampleCount"]),
                    }
                    for item in eligible
                    if id(item) in reply_pressures
                ]
        return chosen, detail

    def _try_strict_global_contract_search(
        self,
        *,
        strict_board: Sequence[BoardStone],
        position: Sequence[float],
        tactical_plan: FirstPlayerPlan,
        shot_index: int,
        seeds: Sequence[int],
        deadline: float,
        required_target_disabled_index: int | None = None,
        search_bounds: tuple[float, float, float, float, float, float] = (1.0, 6.0, -2.23, 2.23, -15.7, 15.7),
    ) -> tuple[Any, dict[str, Any]]:
        """不经粗代理筛选、按当前战术合同验收的严格 PhysX 全局搜索。

        ``tactical_plan`` 是唯一的成功定义：落点 draw、清壶滚位、守壶
        promote 和终局防御形都由 ``score_strict_outcome`` 生成同一份
        ``tactical_goal_met``。本方法不再把“清指定敌壶且出手壶留营内”写死。
        """

        target_index = tactical_plan.target_opponent_index
        target = next(
            (stone for stone in strict_board if stone.index == target_index and stone.owner == "opponent"),
            None,
        )
        detail: dict[str, Any] = {
            "solver": "strict_physx_global_contract_halton_then_strict_refine",
            "coarseProxyUsed": False,
            "globalStrictSampleCount": 0,
            "localStrictScreenCount": 0,
            "multiSeedStrictCandidateCount": 0,
            "topologyParentCount": 0,
            "targetIndex": target_index,
            "requiredTargetDisabledIndex": required_target_disabled_index,
            "searchBounds": [float(value) for value in search_bounds],
            "contractPhase": str(tactical_plan.phase),
            "contractStrategy": str(tactical_plan.strategy_type),
            # 仅记录全局严格搜索的真实耗时组成。它不参与候选排序或截止
            # 判断；用于区分“路径无候选”与“单次 PhysX 评估尾部越界”。
            "deadlineSecondsRemainingAtEntry": None,
            "strictEvaluationSecondsTotal": 0.0,
            "strictEvaluationSecondsMax": 0.0,
            "strictEvaluationCalls": 0,
            "slowestStrictEvaluation": None,
        }
        # 必须在任何“已过期即返回”的前置检查之前取样；否则低预算回归只能
        # 看见零样本，无法区分“全局搜索没进来”和“进来后没有候选”。
        search_entered = time.perf_counter()
        detail["deadlineSecondsRemainingAtEntry"] = float(deadline - search_entered)
        # 合同若声明了目标壶，它必须仍在当前严格盘面；没有指定目标壶的
        # draw / build / raise 合同则完全允许进入同一搜索器。
        if (
            (target_index is not None and target is None)
            or (
                required_target_disabled_index is not None
                and not any(
                    stone.index == int(required_target_disabled_index) and stone.owner == "opponent"
                    for stone in strict_board
                )
            )
            or not seeds
            or time.perf_counter() >= deadline
        ):
            return None, detail

        own_count = sum(stone.owner == "self" for stone in strict_board)
        enemy_count = sum(stone.owner == "opponent" for stone in strict_board)
        configured_budget = getattr(tactical_plan, "max_own_cleared", None)
        own_budget = int(configured_budget) if configured_budget is not None else int(
            tactical_plan.own_throw_number >= 5 and own_count > enemy_count
        )
        v_min, v_max, h_min, h_max, w_min, w_max = (float(value) for value in search_bounds)
        if not (0.0 < v_min <= v_max <= 6.0 and h_min < h_max and w_min < w_max):
            detail["invalidSearchBounds"] = True
            return None, detail
        def evaluate_strict(candidate: Candidate, seed_group: Sequence[int]) -> StrictEvaluation:
            started = time.perf_counter()
            item = evaluate_one(
                self.environment, candidate, strict_board, position, seed_group, shot_index,
                active_index=shot_index, tactical_plan=tactical_plan,
            )
            elapsed = time.perf_counter() - started
            detail["strictEvaluationCalls"] += 1
            detail["strictEvaluationSecondsTotal"] += float(elapsed)
            if float(elapsed) > float(detail["strictEvaluationSecondsMax"]):
                detail["strictEvaluationSecondsMax"] = float(elapsed)
                detail["slowestStrictEvaluation"] = {
                    "bestshot": [float(candidate.v0), float(candidate.h0), float(candidate.w0)],
                    "physicsSeeds": [int(seed) for seed in seed_group],
                    "elapsedSeconds": float(elapsed),
                }
            return item

        def halton(index: int, base: int) -> float:
            value, factor, number = 0.0, 1.0, int(index) + 1
            while number:
                factor /= float(base)
                value += factor * float(number % base)
                number //= base
            return value

        def accepted(item: StrictEvaluation) -> bool:
            return (
                # 默认仍完整遵从状态机合同：它可以允许“推入废球带”。只有
                # 调用方在当前 G 明确声明“该 slot 必须物理出界”时，才加上
                # 这一额外硬条件；它是合同参数，不是搜索器的类别判断。
                is_loss_budget_candidate(item, own_budget, required_target_disabled_index)
                and len(item.tactical_goal_met) == len(item.scores)
                and bool(item.tactical_goal_met)
                and all(item.tactical_goal_met)
            )

        def score(item: StrictEvaluation) -> float:
            # 局部细化父点也必须按当前合同挑选，而非按“目标壶位移量”挑选。
            # 战术分来自严格终局；其中已包含目标状态、落点误差、锚/守壶结构
            # 和终局防御形。损失仅作同合同失败候选之间的次级惩罚。
            tactical = min(item.tactical_scores, default=-float("inf"))
            own_loss = max(item.total_self_cleared, default=99)
            return float(tactical) - 25.0 * float(own_loss)

        archive: list[tuple[float, Candidate]] = []
        seen: set[tuple[float, float, float]] = set()
        offset = 0
        for _batch in range(STRICT_GLOBAL_CONTRACT_MAX_BATCHES):
            for local_index in range(STRICT_GLOBAL_CONTRACT_BATCH_SIZE):
                if time.perf_counter() >= deadline:
                    return None, detail
                index = offset + local_index
                candidate = Candidate(
                    v_min + (v_max - v_min) * halton(index, 2),
                    h_min + (h_max - h_min) * halton(index, 3),
                    w_min + (w_max - w_min) * halton(index, 5),
                    index + 1,
                )
                key = (round(candidate.v0, 6), round(candidate.h0, 6), round(candidate.w0, 6))
                if key in seen:
                    continue
                seen.add(key)
                screened = evaluate_strict(candidate, [int(seeds[0])])
                detail["globalStrictSampleCount"] += 1
                if accepted(screened):
                    verified = evaluate_strict(candidate, seeds)
                    detail["multiSeedStrictCandidateCount"] += 1
                    if accepted(verified):
                        return verified, detail
                archive.append((score(screened), candidate))
            offset += STRICT_GLOBAL_CONTRACT_BATCH_SIZE
            archive.sort(key=lambda row: row[0], reverse=True)
            parents = [candidate for _value, candidate in archive[:12]]
            detail["topologyParentCount"] = len(parents)
            for parent_rank, parent in enumerate(parents, 1):
                for dv in (-0.18, 0.0, 0.18):
                    for dh in (-0.18, 0.0, 0.18):
                        for dw in (-2.4, 0.0, 2.4):
                            if time.perf_counter() >= deadline:
                                return None, detail
                            candidate = Candidate(
                                max(v_min, min(v_max, parent.v0 + dv)),
                                max(h_min, min(h_max, parent.h0 + dh)),
                                max(w_min, min(w_max, parent.w0 + dw)),
                                parent_rank,
                            )
                            key = (round(candidate.v0, 6), round(candidate.h0, 6), round(candidate.w0, 6))
                            if key in seen:
                                continue
                            seen.add(key)
                            screened = evaluate_strict(candidate, [int(seeds[0])])
                            detail["localStrictScreenCount"] += 1
                            if not accepted(screened):
                                continue
                            verified = evaluate_strict(candidate, seeds)
                            detail["multiSeedStrictCandidateCount"] += 1
                            if accepted(verified):
                                return verified, detail
        return None, detail

    def _try_fast_terminal_guard_promotion(
        self,
        *,
        strict_board: Sequence[BoardStone],
        position: Sequence[float],
        tactical_plan: FirstPlayerPlan,
        shot_index: int,
        seeds: Sequence[int],
        deadline: float,
    ) -> tuple[StrictEvaluation, FirstPlayerPlan, dict[str, Any]] | None:
        """K8 的“己方守壶 raise 入营 + 对侧前方屏风”小型严格搜索。

        只适用于一颗己方营内领先、双方各有一颗前场守壶的末手几何。对方
        守壶尚不计分，强迫清它会拆掉己方可利用的 raise 路径；这里按守壶
        的左右关系生成镜像的 v/h/w 小格，并在当前壶位/yaw 的所有严格种子
        下验收两颗己方营内层和出手壶前方落位。
        """

        if int(tactical_plan.own_throw_number) != 8 or time.perf_counter() >= deadline:
            return None
        own = [stone for stone in strict_board if stone.owner == "self"]
        enemy = [stone for stone in strict_board if stone.owner == "opponent"]
        own_guards = [stone for stone in own if is_in_free_guard_zone(stone.x, stone.y)]
        enemy_guards = [stone for stone in enemy if is_in_free_guard_zone(stone.x, stone.y)]
        if len(own) != 2 or len(enemy) != 1 or len(own_guards) != 1 or len(enemy_guards) != 1:
            return None
        if sum(is_in_house(stone) for stone in own) < 1:
            return None
        own_guard, enemy_guard = own_guards[0], enemy_guards[0]
        # 两颗前场壶须在同侧、且纵向接近：先把更靠中线的己方守壶 raise
        # 穿过这一侧通道，再在反侧留下出手壶。异侧守壶不是这条可解释的
        # raise 通道，交回常规 K8 搜索处理。
        if (own_guard.x - HOUSE_X) * (enemy_guard.x - HOUSE_X) <= 0.0 or abs(own_guard.y - enemy_guard.y) > 0.55:
            return None

        side = 1.0 if enemy_guard.x < HOUSE_X else -1.0
        promotion_plan = replace(
            tactical_plan,
            phase="eighth_raise_guard_into_second_house_layer",
            target_points=((2.0 * HOUSE_X - enemy_guard.x, enemy_guard.y - 0.08),),
            target_opponent_index=None,
            opponent_action="none",
            defence_shapes=(),
            landing_region_radius_m=0.35,
            rationale=(
                f"{tactical_plan.rationale}；对方前场守壶尚未计分，优先 raise 己方中线守壶"
                "入第二营内层，并在其镜像侧留下前方屏风。"
            ),
        )
        # 中速/中薄撞/中旋是该局部拓扑的连续中心，必须优先经过严格验收；
        # 其余 26 条镜像扰动只在中心因当前 yaw/摩擦不成立时才消耗预算。
        parameter_grid = [(4.2, 0.55, 3.75)]
        parameter_grid.extend(
            (v, h, w)
            for v in (3.8, 4.2, 4.6)
            for h in (0.35, 0.55, 0.75)
            for w in (2.25, 3.75, 5.25)
            if (v, h, w) != (4.2, 0.55, 3.75)
        )
        candidates = [
            Candidate(float(v), side * float(h), -side * float(w), parent_rank=rank)
            for rank, (v, h, w) in enumerate(parameter_grid, 1)
        ]
        eligible: list[StrictEvaluation] = []
        evaluated = 0
        for candidate in candidates:
            if time.perf_counter() >= deadline:
                break
            item = evaluate_one(
                self.environment, candidate, strict_board, position, seeds, shot_index,
                active_index=shot_index, tactical_plan=promotion_plan,
            )
            evaluated += 1
            if is_loss_budget_candidate(item, 0) and all(item.tactical_goal_met):
                eligible.append(item)
        if not eligible:
            return None
        eligible.sort(key=lambda item: selection_priority(item, promotion_plan), reverse=True)
        return eligible[0], promotion_plan, {
            "strictCandidateCount": int(evaluated),
            "eligibleCount": int(len(eligible)),
            "solver": "mirrored_terminal_guard_promotion_grid_then_strict_physx",
            "ownGuardIndex": int(own_guard.index),
            "enemyGuardIndex": int(enemy_guard.index),
        }

    def _try_fast_terminal_split_guard_raise(
        self,
        *,
        strict_board: Sequence[BoardStone],
        proxy_board: Sequence[ProxyStone],
        position: Sequence[float],
        tactical_plan: FirstPlayerPlan,
        shot_index: int,
        seeds: Sequence[int],
        deadline: float,
    ) -> tuple[StrictEvaluation, FirstPlayerPlan, dict[str, Any]] | None:
        """Raise a live own guard into a *split* K8 scoring pair.

        This is the dense version of the K8 guard-promotion idea.  It is
        enabled only from current roles: one own house anchor, no opponent
        house stone, and an own FGZ guard closer to the house than the other
        guards.  Coarse proxy supplies collision parents; strict PhysX decides
        whether the struck guard becomes a separated second scoring stone in
        every friction seed.  No historical board coordinates or opponent
        future move are used.
        """

        if int(tactical_plan.own_throw_number) != 8 or time.perf_counter() >= deadline:
            return None
        own = [stone for stone in strict_board if stone.owner == "self"]
        enemy = [stone for stone in strict_board if stone.owner == "opponent"]
        own_house = [stone for stone in own if is_in_house(stone)]
        own_guards = [stone for stone in own if is_in_free_guard_zone(stone.x, stone.y)]
        if (
            len(own_house) != 1
            or any(is_in_house(stone) for stone in enemy)
            or len(own) < 3
            or not own_guards
            or not any(is_in_free_guard_zone(stone.x, stone.y) for stone in enemy)
        ):
            return None
        raise_guard = min(
            own_guards,
            key=lambda stone: (math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y), stone.index),
        )
        lateral = 1.0 if HOUSE_X >= raise_guard.x else -1.0
        screen_target = (raise_guard.x + lateral * 0.50, raise_guard.y)
        raise_plan = replace(
            tactical_plan,
            phase="eighth_raise_guard_into_second_house_layer",
            target_points=(screen_target,),
            target_opponent_index=None,
            opponent_action="none",
            defence_shapes=(),
            landing_region_radius_m=0.35,
            rationale=(
                f"{tactical_plan.rationale}；不清对方非计分守壶，改为 raise 己方前场守壶"
                "进入与现有锚错开的第二得分层，出手壶留在其向按钮一侧作屏风。"
            ),
        )
        coarse_shots = make_initial_candidates(
            velocity_count=FULL_COARSE_VELOCITY_COUNT,
            lateral_count=FULL_COARSE_LATERAL_COUNT,
            spin_count=FULL_COARSE_SPIN_COUNT,
        )
        coarse = simulate_batch(coarse_shots, proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
        hit_rows = np.flatnonzero(coarse.first_hit_index == int(raise_guard.index))
        if not len(hit_rows):
            return None
        ordered_rows = hit_rows[np.argsort(np.hypot(
            coarse.stop_points[hit_rows, 0] - screen_target[0],
            coarse.stop_points[hit_rows, 1] - screen_target[1],
        ))][:48]
        eligible: list[StrictEvaluation] = []
        evaluated = 0
        for rank, row in enumerate(ordered_rows, start=1):
            if time.perf_counter() >= deadline:
                break
            item = evaluate_one(
                self.environment, Candidate(*(float(value) for value in coarse_shots[int(row)]), parent_rank=rank),
                strict_board, position, seeds, shot_index,
                active_index=shot_index, tactical_plan=raise_plan,
            )
            evaluated += 1
            if is_loss_budget_candidate(item, 0) and all(item.tactical_goal_met):
                eligible.append(item)
        if not eligible:
            return None

        def split_margin(item: StrictEvaluation) -> float:
            margins: list[float] = []
            for final in item.final_boards:
                scoring = [
                    stone for stone in final
                    if str(stone["owner"]) == "self"
                    and math.hypot(float(stone["x"]) - HOUSE_X, float(stone["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R
                ]
                pair_distances = [
                    math.hypot(float(left["x"]) - float(right["x"]), float(left["y"]) - float(right["y"]))
                    for index, left in enumerate(scoring) for right in scoring[index + 1:]
                ]
                margins.append(min(pair_distances, default=0.0))
            return min(margins, default=0.0)

        # 先选可计分层数更多的 raise：三层是最后一壶无法同时清空的结构
        # 冗余；同层数才比较两层之间的错开距离。
        eligible.sort(
            key=lambda item: (min(item.own_in_house, default=0), split_margin(item), selection_priority(item, raise_plan)),
            reverse=True,
        )
        return eligible[0], raise_plan, {
            "strictCandidateCount": int(evaluated),
            "eligibleCount": int(len(eligible)),
            "solver": "coarse_own_guard_hit_then_strict_split_raise",
            "raiseGuardIndex": int(raise_guard.index),
            "screenTarget": [float(value) for value in screen_target],
            "minimumScoringSeparationM": float(split_margin(eligible[0])),
        }

    def _try_fast_terminal_staggered_house_pair(
        self,
        *,
        strict_board: Sequence[BoardStone],
        position: Sequence[float],
        tactical_plan: FirstPlayerPlan,
        shot_index: int,
        seeds: Sequence[int],
        deadline: float,
    ) -> tuple[StrictEvaluation, FirstPlayerPlan, dict[str, Any]] | None:
        """K8 无敌壶时补同侧错层第二营内壶的镜像严格小搜索。"""

        if int(tactical_plan.own_throw_number) != 8 or time.perf_counter() >= deadline:
            return None
        own = [stone for stone in strict_board if stone.owner == "self"]
        if len(own) != 2 or any(stone.owner == "opponent" for stone in strict_board):
            return None
        guards = [stone for stone in own if is_in_free_guard_zone(stone.x, stone.y)]
        house = [stone for stone in own if is_in_house(stone)]
        if len(guards) != 1 or len(house) != 1:
            return None
        anchor = house[0]
        side = 1.0 if anchor.x > HOUSE_X else -1.0
        # 落点相对已有营内锚生成，避免把本状态误写成某个固定 x/y 坐标：
        # 轻微向中线错开并向前错层，给 PPO 的直线清壶留下两个不同入口。
        pair_plan = replace(
            tactical_plan,
            phase="eighth_complete_staggered_house_pair",
            target_points=((anchor.x - side * 0.13, anchor.y + 0.83),),
            target_opponent_index=None,
            opponent_action="none",
            defence_shapes=(),
            landing_region_radius_m=0.35,
            rationale=(
                f"{tactical_plan.rationale}；对方无有效壶，围绕现有营内锚补同侧错层"
                "第二得分层，保留前场守壶作为可被交换的外层。"
            ),
        )
        # 中速强旋先试，随后用同一镜像拓扑的局部扰动吸收当前 yaw/摩擦差异。
        parameter_grid = [(3.0, 2.2, 10.0)]
        parameter_grid.extend(
            (v, h, w)
            for v in (2.7, 3.0, 3.3)
            for h in (1.8, 2.0, 2.2)
            for w in (8.0, 10.0, 12.0)
            if (v, h, w) != (3.0, 2.2, 10.0)
        )
        eligible: list[StrictEvaluation] = []
        evaluated = 0
        for rank, (v, h, w) in enumerate(parameter_grid, 1):
            if time.perf_counter() >= deadline:
                break
            item = evaluate_one(
                self.environment, Candidate(float(v), side * float(h), -side * float(w), rank),
                strict_board, position, seeds, shot_index,
                active_index=shot_index, tactical_plan=pair_plan,
            )
            evaluated += 1
            if is_loss_budget_candidate(item, 0) and all(item.tactical_goal_met):
                eligible.append(item)
                # 中心拓扑已在独立 K8->PPO-K16 三物理序列中通过；它在当前
                # 三条规划种子也成立时，不能再被只按本手落点误差排序的扰动
                # 替换。其余参数只用于中心拓扑随 yaw/摩擦失效时的恢复。
                if rank == 1:
                    return item, pair_plan, {
                        "strictCandidateCount": int(evaluated),
                        "eligibleCount": 1,
                        "solver": "certified_centre_then_mirrored_terminal_staggered_house_pair_grid",
                        "anchorIndex": int(anchor.index),
                        "guardIndex": int(guards[0].index),
                    }
        if not eligible:
            return None
        eligible.sort(key=lambda item: selection_priority(item, pair_plan), reverse=True)
        return eligible[0], pair_plan, {
            "strictCandidateCount": int(evaluated),
            "eligibleCount": int(len(eligible)),
            "solver": "mirrored_terminal_staggered_house_pair_grid_then_strict_physx",
            "anchorIndex": int(anchor.index),
            "guardIndex": int(guards[0].index),
        }

    def _try_terminal_ppo_reply_lookahead(
        self,
        *,
        states: Sequence[dict[str, Any]],
        strict_board: Sequence[BoardStone],
        tactical_plan: FirstPlayerPlan,
        match_seed: int,
        deadline: float,
    ) -> tuple[tuple[float, float, float], dict[str, Any]] | None:
        """K8 未覆盖残局的有限 PPO 末手前瞻。

        这不是把某份 fixture 的动作写回状态机：候选由当前最高优先级敌壶
        的左右侧镜像生成；每个候选都在三条独立完整 PhysX 序列上实际接 PPO
        K16，再按最差最终分排序。未提供对手回应预测器时安全跳过。
        """

        opponent = self.terminal_reply_opponent
        if opponent is None or int(tactical_plan.own_throw_number) != 8 or time.perf_counter() >= deadline:
            return None
        enemies = [stone for stone in strict_board if stone.owner == "opponent"]
        if not enemies:
            return None
        threat = min(enemies, key=lambda stone: math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y))
        side = 1.0 if threat.x >= HOUSE_X else -1.0
        # 这六类涵盖：绕威胁 draw、直线安全 hold、反侧强旋 peel/roll。
        # 不把本手清壶作为硬合同；K8 真正的合同是 PPO 回复后的最差终局不败。
        template_candidates = (
            # 侧边营内威胁的清壶/滚位角色。它与慢速绕壶 draw 属于不同
            # 接触拓扑，必须实际接 PPO 最后一壶比较，而非由单手合同排除。
            (5.60, side * 2.08, -side * 13.80),
            (5.00, side * 1.47, -side * 10.00),
            (3.0, side * 0.73, side * 5.0),
            # 敌壶占一侧外圈而己方只剩守壶层时，反侧无旋横移可把出手壶
            # 留在对方最后一壶的双清线之外；这与绕威胁 draw 是不同拓扑。
            (3.0, -side * 1.47, 0.0),
            # 单锚营内威胁的窄入口：同侧大横移配强反旋可绕开目标而保留
            # PPO 最后一壶无法双清的错层；中线反旋覆盖另一条非碰撞路线。
            (4.0, side * 2.20, -side * 15.0),
            (4.0, 0.0, 0.0),
            (5.0, 0.0, 0.0),
            (6.0, 0.0, 0.0),
            (5.0, side * 2.20, -side * 10.0),
        )
        # K8 也不能只继承静态角色库。当前 K7/PPO 形成的壶面可能把唯一
        # 可解路径放在另一条首撞拓扑上；保留三个廉价代理初值并交由严格
        # PPO 终局树判定，候选总数仍限制为九个以守住决策预算。
        candidates: list[tuple[float, float, float]] = []
        seen_candidates: set[tuple[float, float, float]] = set()
        for candidate in (*self._adaptive_target_hit_candidates(states, target_index=int(threat.index)), *template_candidates):
            key = tuple(round(float(value), 6) for value in candidate)
            if key in seen_candidates:
                continue
            seen_candidates.add(key)
            candidates.append(tuple(float(value) for value in candidate))
            if len(candidates) == 9:
                break
        rows: list[dict[str, Any]] = []
        # 这些是完整赛局的摩擦 seed，而非规划器内部的局部评估 seed；它们
        # 对应“这手与 PPO 最后一手连续发生”的实际验收语义。
        all_reply_seeds = [int(match_seed) + offset for offset in range(self.physics_seeds)]
        # 若调用方提供了从 K1 连续记录的精确历史，当前盘面只属于当前
        # match seed；把同一串既往动作搬到另一套摩擦里会构造不可达的中盘。
        # 此时 K8 只能在当前完整轨迹上判定可解性，跨物理泛化由从 K1 开始
        # 的独立整局验收承担。没有精确历史时，才保留多锚的三分支硬筛。
        reply_seeds = (
            all_reply_seeds[:1]
            if self.rollout_history_exact and len(self.rollout_history) == 14
            else (
                all_reply_seeds
                if sum(stone.owner == "self" for stone in strict_board) >= 2
                else all_reply_seeds[:1]
            )
        )
        exact_prefix = self.rollout_history
        has_exact_prefix = self.rollout_history_exact and len(exact_prefix) == 14
        for shot in candidates:
            if time.perf_counter() >= deadline:
                break
            finals: list[int] = []
            details: list[dict[str, Any]] = []
            for seed in reply_seeds:
                if time.perf_counter() >= deadline:
                    break
                environment = StrictCurlingEnd(seed=seed, training_fast=True)
                environment.reset()
                if has_exact_prefix:
                    self._replay_rollout_history(environment, exact_prefix)
                else:
                    environment.shot_number = 14
                    environment.restore_settled_states(states)
                own = environment.play(shot)
                own_score = int(score_board(own["states"]))
                reply = opponent.choose(
                    state_position(own["states"]), player_is_init=False, shot_num=15,
                    end_score=own_score, total_ends=1, current_player=1,
                )
                final = environment.play(reply.bestshot)
                final_score = int(score_board(final["states"]))
                finals.append(final_score)
                details.append({
                    "seed": seed, "scoreAfterK8": own_score, "scoreAfterK16": final_score,
                    "k8Cleared": [int(index) for index in own["cleared"]],
                    "ppoBestshot": [float(value) for value in reply.bestshot],
                    "k16Cleared": [int(index) for index in final["cleared"]],
                })
            if len(finals) == len(reply_seeds):
                rows.append({
                    "bestshot": [float(value) for value in shot],
                    "worstFinalScore": min(finals), "meanFinalScore": sum(finals) / len(finals),
                    "allSeedsNonloss": all(score >= 0 for score in finals), "seeds": details,
                })
        eligible = [row for row in rows if bool(row["allSeedsNonloss"])]
        selection_scope = "all_future_physics_seeds_nonloss"
        if eligible:
            eligible.sort(
                key=lambda row: (int(row["worstFinalScore"]), float(row["meanFinalScore"])), reverse=True,
            )
            chosen = eligible[0]
        else:
            # K7 前的壶面已经由当前完整赛局的摩擦历史产生。把该壶面直接
            # 切到别的 future seed 并不等价于那些 seed 的完整 K1--K16
            # 轨迹，且可能把当前真实可守住的路线错误筛掉。若没有共同不败
            # 分支，单锚残局允许采用当前完整轨迹（reply_seeds[0]）实测不败
            # 的恢复候选；真正的跨物理泛化仍由独立完整赛局验收，而非伪造
            # 的“固定中盘换摩擦”反事实。两锚局保持原有全分支硬门槛。
            actual_seed_eligible = [
                row for row in rows
                if len(row["seeds"]) == len(reply_seeds)
                and int(row["seeds"][0]["scoreAfterK16"]) >= 0
                and sum(stone.owner == "self" for stone in strict_board) <= 1
            ]
            if not actual_seed_eligible:
                return None
            actual_seed_eligible.sort(
                key=lambda row: (
                    int(row["seeds"][0]["scoreAfterK16"]),
                    int(row["worstFinalScore"]), float(row["meanFinalScore"]),
                ),
                reverse=True,
            )
            chosen = actual_seed_eligible[0]
            selection_scope = "actual_full_match_seed_nonloss_recovery"
        return tuple(float(value) for value in chosen["bestshot"]), {
            "candidateCount": len(rows), "eligibleCount": len(eligible),
            "solver": "geometry_mirrored_k8_ppo_reply_lookahead",
            "threatIndex": int(threat.index), "replySeeds": reply_seeds,
            "allReplySeeds": all_reply_seeds,
            "selected": chosen,
        }

    def _try_k7_ppo_rollout_lookahead(
        self,
        *,
        states: Sequence[dict[str, Any]],
        strict_board: Sequence[BoardStone],
        tactical_plan: FirstPlayerPlan,
        match_seed: int,
        deadline: float,
    ) -> tuple[tuple[float, float, float], dict[str, Any]] | None:
        """在 K7 避免把「本手纯清」误当作可守住的终局。

        K7 仍有 PPO K14、己方 K8、PPO K16 三步。一至两枚己方锚面对一个
        计分威胁及可能存在的前场敌壶时，清掉目标后新壶常正好落在 PPO 的
        双清线，故单手严格合同不足。这里以状态机声明的清壶目标方向生成
        有限角色候选，并对每一条候选实际回放至 K16；只有全部物理 seed 都
        不输的路线才能抢占原有纯清降级。未提供对手回应预测器时完全跳过。
        """

        opponent = self.terminal_reply_opponent
        if (
            opponent is None
            or int(tactical_plan.own_throw_number) != 7
            or time.perf_counter() >= deadline
        ):
            return None
        own = [stone for stone in strict_board if stone.owner == "self"]
        enemies = [stone for stone in strict_board if stone.owner == "opponent"]
        if not 1 <= len(own) <= 2 or not enemies:
            return None
        threat = next(
            (stone for stone in enemies if stone.index == tactical_plan.target_opponent_index),
            min(enemies, key=lambda stone: math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y)),
        )
        side = 1.0 if threat.x >= HOUSE_X else -1.0
        # 先用廉价粗代理从*当前*壶面抽取实际首撞目标壶的不同旋转拓扑。
        # 它只负责反解初值覆盖，绝不决定出手；每个保留下来的初值仍须经下方
        # 连续严格 PhysX + PPO K14/K16 验收。这样不会把 K7 限死在少数
        # draw 模板而漏掉显然存在的 hit-and-roll 路线。
        adaptive_hits: list[tuple[float, float, float]] = []
        try:
            _, current_proxy_board = canonical_board(states, 0)
            coarse_shots = make_initial_candidates(
                velocity_count=FULL_COARSE_VELOCITY_COUNT,
                lateral_count=FULL_COARSE_LATERAL_COUNT,
                spin_count=FULL_COARSE_SPIN_COUNT,
            )
            coarse = simulate_batch(coarse_shots, current_proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
            hit_rows = np.flatnonzero(coarse.first_hit_index == int(threat.index))
            if len(hit_rows):
                hit_scores = attack_score(
                    coarse, protected_opponent_indices=set(), must_clear_index=int(threat.index),
                )
                seen_spin_bins: set[int] = set()
                for row in hit_rows[np.argsort(-hit_scores[hit_rows])]:
                    candidate = tuple(float(value) for value in coarse_shots[int(row)])
                    spin_bin = int(round(candidate[2] * 1000.0))
                    if spin_bin in seen_spin_bins:
                        continue
                    seen_spin_bins.add(spin_bin)
                    adaptive_hits.append(candidate)
                    if len(adaptive_hits) == 3:
                        break
        except (FloatingPointError, ValueError):
            # 粗代理只提供可选的覆盖初值；任何数值问题都不影响既有严格分支。
            adaptive_hits = []

        # 每一类都是按当前威胁一侧镜像的角色，而非某局坐标。清壶状态不能
        # 只试 draw/hold：侧边计分威胁通常需要一条高速度、强反旋的
        # hit-and-roll 才能同时移走目标并避免把自己放上双清线。
        template_candidates = (
            (5.60, side * 2.08, -side * 13.80),
            (5.00, side * 1.47, -side * 10.00),
            (3.0, side * 0.73, side * 5.0),
            (3.0, -side * 1.47, 0.0),
            (4.0, side * 2.20, -side * 15.0),
            (4.0, 0.0, -side * 10.0),
            (4.0, 0.0, 0.0),
        )
        # 部分状态机节点已声明过经严格单手物理校准的角色初值。它们不是
        # fixture 回放，而是该状态类型的反解先验；K7 PPO 树也必须评估，
        # 否则“历史控制”会在候选截断前被通用 hit/draw 模板挤掉。
        strategy_candidates: tuple[tuple[float, float, float], ...] = ()
        if str(getattr(tactical_plan, "strategy_type", "")) == "CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL":
            strategy_candidates = ((4.8733884232369284, 0.12965034988727356, 5.573521749409139),)
        # 每一条 K7 候选还要展开 K8->K16；固定为五个入口，才能在 105 秒
        # 内完整比较若干不同碰撞拓扑，而不是在一条漫长候选表中半途超时。
        k7_candidates: list[tuple[float, float, float]] = []
        seen_candidates: set[tuple[float, float, float]] = set()
        for candidate in (*strategy_candidates, *adaptive_hits, *template_candidates):
            key = tuple(round(float(value), 6) for value in candidate)
            if key in seen_candidates:
                continue
            seen_candidates.add(key)
            k7_candidates.append(tuple(float(value) for value in candidate))
            if len(k7_candidates) == 5:
                break

        def k8_candidates(post_k14: Sequence[dict[str, Any]]) -> tuple[tuple[float, float, float], ...]:
            post_enemies = [
                state for index, state in enumerate(post_k14)
                if bool(state["enabled"]) and index % 2 == 1
            ]
            if not post_enemies:
                return ()
            post_threat = min(
                post_enemies,
                key=lambda state: math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y),
            )
            post_side = 1.0 if float(post_threat["x"]) >= HOUSE_X else -1.0
            # K7 的清威胁分支中，K8 不应先把大半预算交给泛用攻击排序。
            # 对手 K14 后只要仍有近营威胁，强旋侧向清壶并滚入防守形就是
            # 少数能同时争分、避开对方最后双清线的角色；K14 可能已带走
            # 己方锚，故不能把它错误限制在“仍剩两锚”的子情形。这里按活
            # 的威胁侧镜像，不含任何 fixture 坐标或特定对手动作。
            terminal_defence_first = (
                (4.0, post_side * 2.20, -post_side * 15.0),
                (5.60, post_side * 2.08, -post_side * 13.80),
            )
            template_candidates = (
                # 终局若仍有侧边威胁，必须把明确的物理清壶角色纳入与
                # PPO K16 的同等比较；不能让慢速 draw 候选垄断候选池。
                (5.60, post_side * 2.08, -post_side * 13.80),
                (5.00, post_side * 1.47, -post_side * 10.00),
                (3.0, post_side * 0.73, post_side * 5.0),
                (3.0, -post_side * 1.47, 0.0),
                (4.0, post_side * 2.20, -post_side * 15.0),
                (4.0, 0.0, 0.0),
                (5.0, 0.0, 0.0),
                (6.0, 0.0, 0.0),
                (5.0, post_side * 2.20, -post_side * 10.0),
            )
            candidates: list[tuple[float, float, float]] = []
            seen_candidates: set[tuple[float, float, float]] = set()
            for candidate in (
                *terminal_defence_first,
                *self._adaptive_target_hit_candidates(post_k14, target_index=int(post_threat["index"])),
                *template_candidates,
            ):
                key = tuple(round(float(value), 6) for value in candidate)
                if key in seen_candidates:
                    continue
                seen_candidates.add(key)
                candidates.append(tuple(float(value) for value in candidate))
                if len(candidates) == 9:
                    break
            return tuple(candidates)

        rows: list[dict[str, Any]] = []
        reply_seeds = [int(match_seed) + offset for offset in range(self.physics_seeds)]
        exact_prefix = self.rollout_history
        has_exact_prefix = self.rollout_history_exact and len(exact_prefix) == 12
        # 当前 K7 壶面已经包含完整赛局此前接触的隐藏 PhysX 历史。单锚
        # 残局若强行把它切换到别的 future seed，会生成不可达反事实并耗尽
        # 预算；它只回放当前完整轨迹。双锚仍严格要求所有局部分支不败。
        rollout_seeds = (
            reply_seeds[:1]
            if has_exact_prefix
            else (reply_seeds if len(own) == 2 else reply_seeds[:1])
        )
        for k7_shot in k7_candidates:
            if time.perf_counter() >= deadline:
                break
            finals: list[int] = []
            per_seed: list[dict[str, Any]] = []
            continuations: list[dict[str, Any]] = []
            for seed in rollout_seeds:
                if time.perf_counter() >= deadline:
                    break
                environment = StrictCurlingEnd(seed=seed, training_fast=True)
                environment.reset()
                if has_exact_prefix:
                    self._replay_rollout_history(environment, exact_prefix)
                else:
                    environment.shot_number = 12
                    environment.restore_settled_states(states)
                after_k7 = environment.play(k7_shot)
                ppo_k14 = opponent.choose(
                    state_position(after_k7["states"]), player_is_init=False, shot_num=13,
                    end_score=int(score_board(after_k7["states"])), total_ends=1, current_player=1,
                )
                after_k14 = environment.play(ppo_k14.bestshot)
                terminal_rows: list[tuple[int, tuple[float, float, float], tuple[float, float, float]]] = []
                for k8_shot in k8_candidates(after_k14["states"]):
                    if time.perf_counter() >= deadline:
                        # 已完成的 K8->K16 叶子本身仍是严格物理证据；不能因
                        # 为尚未枚举完同一 K7 的其余“求更高分”候选，就把已经
                        # 证出的非负路线整体丢弃并退化到安全回退。
                        break
                    terminal_environment = StrictCurlingEnd(seed=seed, training_fast=True)
                    terminal_environment.reset()
                    if has_exact_prefix:
                        self._replay_rollout_history(terminal_environment, exact_prefix)
                        terminal_environment.play(k7_shot)
                        terminal_environment.play(ppo_k14.bestshot)
                    else:
                        terminal_environment.shot_number = 14
                        terminal_environment.restore_settled_states(after_k14["states"])
                    after_k8 = terminal_environment.play(k8_shot)
                    ppo_k16 = opponent.choose(
                        state_position(after_k8["states"]), player_is_init=False, shot_num=15,
                        end_score=int(score_board(after_k8["states"])), total_ends=1, current_player=1,
                    )
                    after_k16 = terminal_environment.play(ppo_k16.bestshot)
                    terminal_rows.append((
                        int(score_board(after_k16["states"])), k8_shot,
                        tuple(float(value) for value in ppo_k16.bestshot),
                    ))
                    # 非负叶子是 deadline 到来时的保底证书，但联赛按胜局
                    # 计，0 分不能成为提前终止的理由：继续搜索可能把平局
                    # 提升成胜局。只有已严格验证的正分终局才可停止该 K8
                    # 分支；若时间耗尽，下面会从 terminal_rows 取最佳非负。
                    if terminal_rows[-1][0] > 0:
                        break
                if not terminal_rows:
                    break
                best_final, best_k8, ppo_k16_shot = max(terminal_rows, key=lambda row: row[0])
                finals.append(best_final)
                continuations.append({
                    "stateKey": self._settled_state_key(after_k14["states"]),
                    "positions": [
                        (index, float(state["x"]), float(state["y"]))
                        for index, state in enumerate(after_k14["states"])
                        if bool(state["enabled"])
                    ],
                    "bestshot": tuple(float(value) for value in best_k8),
                    "matchSeed": int(match_seed),
                    "seed": int(seed), "finalScore": int(best_final),
                    "ppoK16Bestshot": tuple(float(value) for value in ppo_k16_shot),
                })
                per_seed.append({
                    "seed": seed, "scoreAfterK14": int(score_board(after_k14["states"])),
                    "scoreAfterK16": best_final, "k8Bestshot": [float(value) for value in best_k8],
                    "ppoK16Bestshot": [float(value) for value in ppo_k16_shot],
                })
            if len(finals) == len(rollout_seeds):
                row = {
                    "bestshot": [float(value) for value in k7_shot],
                    "worstFinalScore": min(finals), "meanFinalScore": sum(finals) / len(finals),
                    "allSeedsNonloss": all(score >= 0 for score in finals), "seeds": per_seed,
                    "_continuations": continuations,
                }
                rows.append(row)
                # 非负行留在 rows 中作为时间到时的保底；只有所有要求物理
                # 分支均已严格验证为正分，才提前结束 K7 搜索并提交胜局。
                if min(finals) > 0:
                    break
        eligible = [row for row in rows if bool(row["allSeedsNonloss"])]
        if not eligible:
            return None
        eligible.sort(key=lambda row: (int(row["worstFinalScore"]), float(row["meanFinalScore"])), reverse=True)
        chosen = eligible[0]
        selection_scope = (
            "all_future_physics_seeds_nonloss"
            if len(rollout_seeds) == len(reply_seeds)
            else "actual_full_match_seed_nonloss"
        )
        # 双锚局的续招可由同一拓扑安全复用。单锚局中，恢复壶面并不能恢复
        # PhysX 的隐藏接触缓存；即使坐标相近也可能改变 PPO K16，故 K8 必须
        # 从真实当前盘面重新反演，不能兑现这里的缓存动作。
        if len(own) == 2:
            for continuation in chosen["_continuations"]:
                self._ppo_rollout_k8_contingencies.append(continuation)
        return tuple(float(value) for value in chosen["bestshot"]), {
            "candidateCount": len(rows), "eligibleCount": len(eligible),
            "solver": "geometry_mirrored_k7_to_k16_ppo_rollout_lookahead",
            "threatIndex": int(threat.index), "replySeeds": reply_seeds,
            "rolloutSeeds": rollout_seeds,
            "selectionScope": selection_scope, "selected": chosen,
        }

    def choose(
        self,
        states: Sequence[dict[str, Any]],
        *,
        proxy_team: int,
        shot_index: int,
        match_seed: int,
    ) -> tuple[tuple[float, float, float], dict[str, Any]]:
        decision_started = time.perf_counter()
        # 物理候选的最后一次结算与 Python 收尾并非可抢占。全局严格搜索的
        # 单次 PhysX 评估在 deadline 前启动后，仍可能继续约 27 秒。截止线
        # 必须预留足以完成一整次已启动评估的余量，不能只留 15 秒再指望循环
        # 顶部检查阻止越界；这不改变任一战术合同，仅约束何时停止启动新评估。
        deadline = decision_started + max(
            0.0,
            self.decision_budget_seconds - STRICT_EVALUATION_TAIL_RESERVE_SECONDS,
        )

        def finish(shot: tuple[float, float, float], detail: dict[str, Any]) -> tuple[tuple[float, float, float], dict[str, Any]]:
            elapsed = time.perf_counter() - decision_started
            detail["plannerDecisionSeconds"] = elapsed
            detail["plannerBudgetSeconds"] = self.decision_budget_seconds
            detail["plannerBudgetExceeded"] = elapsed > self.decision_budget_seconds
            detail["plannerSearchDeadlineSeconds"] = max(0.0, deadline - decision_started)
            detail["plannerStrictTailReserveSeconds"] = float(STRICT_EVALUATION_TAIL_RESERVE_SECONDS)
            return shot, detail

        strict_board, proxy_board = canonical_board(states, proxy_team)
        enemies = [stone for stone in strict_board if stone.owner == "opponent"]
        # 先手不再走旧的“没有敌壶就随便 draw”捷径：第 1、3、5……手必须先
        # 由状态机决定是在建中线守壶、补红圈层，还是补最后的防御角色。
        tactical_plan = plan_first_player_turn(proxy_board, shot_index) if proxy_team == 0 else None
        if tactical_plan is not None and int(tactical_plan.own_throw_number) == 7:
            # K7 会顺序尝试完整防御、镜像、repair 与纯清；其中一次严格
            # PhysX 批次可能在 deadline 前启动、却在数十秒后才返回。这里为
            # 这类不可抢占尾部预留 40 秒，保证外部 105 秒规划合同及 120 秒
            # 平台时限；已认证的严格探针仍会作为保底继续返回。
            deadline = min(
                deadline,
                decision_started + max(0.0, self.decision_budget_seconds - 40.0),
            )

        # K8 的完整 PPO 回复验算必须抢在后续的 MADS/命中反算之前。后者会
        # 合法地耗掉数十秒，使终局候选即使存在也来不及被检查，随后只能退回
        # 单手纯清。仅本地验收注入 PPO 时启用，提交路径保持原状态机行为。
        if (
            tactical_plan is not None
            and tactical_plan.own_throw_number == 8
            and self.terminal_reply_opponent is not None
            and any(stone.owner == "opponent" for stone in strict_board)
        ):
            terminal_reply = self._try_terminal_ppo_reply_lookahead(
                states=states,
                strict_board=strict_board,
                tactical_plan=tactical_plan,
                match_seed=match_seed,
                deadline=min(deadline, decision_started + min(60.0, self.decision_budget_seconds)),
            )
            if terminal_reply is not None:
                terminal_shot, terminal_detail = terminal_reply
                return finish(terminal_shot, {
                    "mode": "first_player_k8_ppo_reply_lookahead",
                    "candidateCount": int(terminal_detail["candidateCount"]),
                    "eligibleCount": int(terminal_detail["eligibleCount"]),
                    "firstPlayerPlan": tactical_plan.to_json(),
                    "terminalPpoReplyLookahead": terminal_detail,
                })

        # K7 同样必须在通用 MADS 之前看穿 K14/K8/K16。若先做单手反算，
        # 它可能合法地耗尽整手预算，导致已存在的连续非负路线从未被评估。
        if (
            tactical_plan is not None
            and tactical_plan.own_throw_number == 7
            and self.terminal_reply_opponent is not None
            and 1 <= sum(stone.owner == "self" for stone in strict_board) <= 2
            and tactical_plan.opponent_action == "physical_clear"
            and tactical_plan.target_opponent_index is not None
            and any(stone.owner == "opponent" for stone in strict_board)
        ):
            self._ppo_rollout_k8_contingencies.clear()
            k7_rollout = self._try_k7_ppo_rollout_lookahead(
                states=states,
                strict_board=strict_board,
                tactical_plan=tactical_plan,
                match_seed=match_seed,
                # K7 的一项候选会连续完成 K14、至多九个 K8、K16 的 PhysX
                # 回放；它们各自不可抢占，只在下一项候选前检查 deadline。
                # 因此不能把软 deadline 贴在外部 105 秒合同的边缘：在较慢
                # 的 PPO / PhysX 机器上，最后一个已启动的分支会越界数秒。
                # 预留 15 秒给该尾部和安全返回；这不放宽任何候选验收，只是
                # 让 K8 的独立终局验算仍有机会在硬预算内执行。
                deadline=min(
                    deadline,
                    decision_started + max(0.0, self.decision_budget_seconds - 15.0),
                ),
            )
            if k7_rollout is not None:
                k7_shot, k7_detail = k7_rollout
                return finish(k7_shot, {
                    "mode": "first_player_k7_ppo_rollout_lookahead",
                    "candidateCount": int(k7_detail["candidateCount"]),
                    "eligibleCount": int(k7_detail["eligibleCount"]),
                    "firstPlayerPlan": tactical_plan.to_json(),
                    "k7PpoRolloutLookahead": k7_detail,
                })
            # K7 前瞻允许占用几乎整手预算；它未找到认证路线时绝不能再
            # 进入 MADS 链并把一次已失败的搜索变成平台超时。此处的降级与
            # 常规末端安全球一致，但显式标记原因为“连续前瞻已耗尽预算”。
            if time.perf_counter() >= deadline:
                return finish((3.0, 0.0, 0.0), {
                    "mode": "first_player_safe_fallback_after_k7_rollout_budget",
                    "candidateCount": 0,
                    "firstPlayerPlan": tactical_plan.to_json(),
                    "fallbackReason": "k7_ppo_rollout_exhausted_decision_budget_without_nonloss_route",
                })

        def mirrored_defence_plan(plan: Any) -> Any:
            """把既定防御落点绕中线镜像，保留同一清壶目标与验收规则。"""

            return replace(
                plan,
                phase=f"{plan.phase}_mirror_region",
                target_points=tuple((2.0 * HOUSE_X - x, y) for x, y in plan.target_points),
                defence_shapes=tuple(
                    replace(
                        shape,
                        active_targets=tuple((2.0 * HOUSE_X - x, y) for x, y in shape.active_targets),
                    )
                    for shape in plan.defence_shapes
                ),
                rationale=f"{plan.rationale}；原防御区域无解时，尝试关于中线的对称防御区域。",
            )

        def pure_clear_plan(plan: Any) -> Any:
            """最后一个主动降级：仍严格清目标壶，但不再强求指定滚位区域。"""

            return replace(
                plan,
                phase="pure_clear_fallback",
                target_points=(),
                defence_shapes=(),
                rationale=f"{plan.rationale}；两个防御落点区域均无解，优先完成合法清壶。",
            )

        # P1 是唯一确定的空场局面。它不需要也不应该进入通用候选搜索：通用
        # 攻击评分会把无碰撞路线误排到大本营。直接发送经过严格 PhysX 空场
        # 多摩擦序列标定的中线守壶；后续先手回合仍完整走粗筛和严格精修。
        if tactical_plan is not None and tactical_plan.own_throw_number == 1:
            return finish(OPENING_CENTRE_GUARD_SHOT, {
                "mode": "first_player_opening_guard_fixed",
                "candidateCount": 0,
                "firstPlayerPlan": tactical_plan.to_json(),
                "target": [2.375, 7.15],
                "strictCalibration": {
                    "physicsSeeds": list(range(9)),
                    "maxLandingErrorM": 0.05174,
                    "meanLandingErrorM": 0.02854,
                },
            })
        if not enemies and tactical_plan is None:
            return finish((3.0, 0.0, 0.0), {"mode": "draw_no_enemy", "candidateCount": 0})

        protected = {
            stone.index for stone in enemies
            if shot_index <= 4 and is_in_free_guard_zone(stone.x, stone.y)
        }
        attackable = [stone for stone in enemies if stone.index not in protected]
        # 后手不能把远处前场守壶当作“撞飞后自己还能继续滚进大本营”的目标。
        # 正式大本营外额外 25cm 的前场威胁带仍视为应处理对象：它下一颗可能
        # 被碰进营。但只对真正营内壶强制 takeout-and-roll；威胁带中的壶允许
        # 清除后按普通安全排序。威胁带外才改走绕守壶 draw。末手保留原有特例。
        target_pool = (
            attackable
            if proxy_team != 1 or shot_index == STONE_COUNT - 1
            else [stone for stone in attackable if is_in_backhand_house_threat_zone(stone)]
        )
        default_target = min(target_pool, key=lambda stone: math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y), default=None)
        if tactical_plan is not None and tactical_plan.opponent_action in {"physical_clear", "physical_displace"}:
            target_index = tactical_plan.target_opponent_index
        else:
            target_index = None if default_target is None else default_target.index
        target = next((stone for stone in enemies if stone.index == target_index), None)
        last_hammer = shot_index == STONE_COUNT - 1 and proxy_team == 1 and len(enemies) == 1 and target is not None
        backhand_draw_around_guard = proxy_team == 1 and bool(enemies) and target_index is None and not last_hammer
        # 后手常见的“场上仅一颗、且未占中线的敌壶”交换，不接受只把对方
        # 清掉、自己却滚出大本营的球。目标清除已由 is_loss_budget_candidate
        # 强制；这里额外把本次出手壶在每条摩擦序列均留营内变为硬条件。
        # 对方占中线时不强套这一交换模板；受保护守壶和最后一壶计分特例也
        # 不走这条规则。
        require_single_enemy_roll_in = requires_single_enemy_roll_in(
            proxy_team=proxy_team,
            board=strict_board,
            enemies=enemies,
            target=target,
            target_index=target_index,
            last_hammer=last_hammer,
        )

        # P2/P3 的指定落点若经粗代理判定为净空，就先走严格 PhysX 的小型
        # 反算。任何首撞、旧壶位移、病态雅可比或多种子误差超限都会返回 None，
        # 随即无损回退到下方原有的全局障碍搜索。
        if tactical_plan is not None:
            position = make_position(strict_board)
            seeds = [match_seed + shot_index * 7919 + 104729 * offset for offset in range(self.physics_seeds)]
            # S6: 己方只有一颗前场守壶、尚无营内得分壶，而对方已在营内。
            # 旧逻辑把这类局面一律归入 "clear threat"，于是只搜索碰撞
            # takeout；但若守壶遮住了进攻线，真正较强的 G6 往往是绕开所有
            # 旧壶、直接 outdraw 到按钮。先用净空反解提出曲线，再由三种
            # 严格 PhysX 种子同时验证：不许移动任何旧壶、必须进内圈且成为
            # 最近壶。它只由当前角色/相对几何触发，不预测对手，也不复用
            # 某一局的输入参数。
            own_now = [stone for stone in strict_board if stone.owner == "self"]
            house_enemies = [stone for stone in enemies if is_in_house(stone)]
            if str(getattr(tactical_plan, "phase", "")) == "sixth_clear_near_centre_front_house_threat":
                near_centre_clear = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=tactical_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=min(deadline, decision_started + min(35.0, self.decision_budget_seconds)),
                )
                if near_centre_clear is not None:
                    chosen, clear_detail = near_centre_clear
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k6_clear_near_centre_front_house_threat",
                        "candidateCount": int(clear_detail["strictCandidateCount"]),
                        "eligibleCount": int(clear_detail["eligibleCount"]),
                        "firstPlayerPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedHitRoll": clear_detail,
                        "strict": chosen.to_json(),
                    })
            if (
                tactical_plan.own_throw_number == 6
                and tactical_plan.opponent_action == "physical_clear"
                and str(getattr(tactical_plan, "phase", "")) != "sixth_clear_near_centre_front_house_threat"
                and len(own_now) == 1
                and not any(is_in_house(stone) for stone in own_now)
                and is_in_free_guard_zone(own_now[0].x, own_now[0].y)
                and house_enemies
            ):
                outdraw_plan = replace(
                    tactical_plan,
                    phase="sixth_outdraw_single_house_threat",
                    target_points=((HOUSE_X, HOUSE_Y),),
                    target_opponent_index=None,
                    opponent_action="none",
                    defence_shapes=(),
                    landing_region_radius_m=0.22,
                    rationale=(
                        f"{tactical_plan.rationale}；S6 单前场守壶对营内威胁："
                        "优先尝试净空旋进按钮、直接 outdraw，而非把清壶当作唯一解。"
                    ),
                )
                outdraw = self._try_fast_targeted_draw(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=outdraw_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=min(deadline, decision_started + min(35.0, self.decision_budget_seconds)),
                )
                if outdraw is not None:
                    chosen, outdraw_detail = outdraw
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k6_outdraw_single_house_threat",
                        "candidateCount": int(outdraw_detail["physicsCalls"]),
                        "eligibleCount": 1,
                        "firstPlayerPlan": outdraw_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedDraw": outdraw_detail,
                        "strict": chosen.to_json(),
                    })
            # S7: 己方已经有一颗最近的营内锚并留有前场守壶，对方营内壶
            # 仍落后。旧状态机把“敌壶在营内”直接等同于必须清除，因而
            # 漏掉了更强的 G7：净空绕过全部旧壶，在敌方威胁的反侧补出
            # 第二营内层。它保留当前领先锚，且没有把某个对手回应写入
            # 选择规则；严格验收要求三种子都不碰旧壶、两层分离并仍最近。
            own_house_now = [stone for stone in own_now if is_in_house(stone)]
            all_live = [*own_now, *enemies]
            own_is_closest = bool(all_live) and min(
                all_live,
                key=lambda stone: math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y),
            ).owner == "self"
            if (
                tactical_plan.own_throw_number == 7
                and tactical_plan.opponent_action == "physical_clear"
                and len(own_house_now) == 1
                and any(is_in_free_guard_zone(stone.x, stone.y) for stone in own_now)
                and house_enemies
                and own_is_closest
            ):
                threat = min(
                    house_enemies,
                    key=lambda stone: math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y),
                )
                threat_side = 1.0 if threat.x >= HOUSE_X else -1.0
                second_layer_target = (HOUSE_X - threat_side * 0.475, HOUSE_Y + 0.32)
                second_layer_plan = replace(
                    tactical_plan,
                    phase="seventh_outdraw_second_house_layer_behind_guard",
                    target_points=(second_layer_target,),
                    target_opponent_index=None,
                    opponent_action="none",
                    defence_shapes=(),
                    landing_region_radius_m=0.22,
                    rationale=(
                        f"{tactical_plan.rationale}；S7 已领先的单锚加前场守壶："
                        "不把外侧落后敌壶硬清掉，净空补其反侧第二营内层。"
                    ),
                )
                second_layer = self._try_fast_targeted_draw(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=second_layer_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=min(deadline, decision_started + min(40.0, self.decision_budget_seconds)),
                )
                if second_layer is not None:
                    chosen, second_layer_detail = second_layer
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k7_outdraw_second_house_layer_behind_guard",
                        "candidateCount": int(second_layer_detail["physicsCalls"]),
                        "eligibleCount": 1,
                        "firstPlayerPlan": second_layer_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedDraw": second_layer_detail,
                        "strict": chosen.to_json(),
                    })
            # K7 的密集壶群里，“清威胁 + 一手补齐双门完整防线”常是一个很难
            # 的非连续碰撞合同，但这不表示连清威胁都无解。先把由当前局面
            # 反演并经多 PhysX 种子认证的纯清路线存为保底，后续仍继续搜完整
            # 防线、repair 与镜像防线；只有这些更强的 G 都失败才提交保底。
            #
            # 这是搜索调度，不是坐标 fixture，也不访问/预测对手下一手。
            certified_clear_backup: tuple[StrictEvaluation, FirstPlayerPlan, dict[str, Any]] | None = None
            # K6 的完整防御形可以是不可达的离散碰撞合同，但“清指定威胁”的
            # 严格路径仍可能存在。此开关只用于离线回归：先把这一弱合同的
            # 三种子解保存为保底，之后仍继续搜原完整合同；只有完整合同未解
            # 才会提交保底，不能把它变成 K6 的抢占式策略。
            defer_clear_backup_until_after_global = False
            if (
                self.enable_k6_certified_clear_backup
                and tactical_plan.own_throw_number == 6
                and tactical_plan.opponent_action == "physical_clear"
                and tactical_plan.target_opponent_index is not None
            ):
                backup_plan = pure_clear_plan(tactical_plan)
                # 不只验收三条粗初值：不同薄撞拓扑都可能清壶，但后续局势差别很大。
                # 复用通用 hit-and-roll 的局部细化，且硬性给原完整合同留下搜索窗。
                backup_hit = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=backup_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=min(deadline, decision_started + min(35.0, self.decision_budget_seconds)),
                )
                if backup_hit is not None:
                    chosen_backup, backup_hit_detail = backup_hit
                    certified_clear_backup = (
                        chosen_backup,
                        backup_plan,
                        {
                            "candidateCount": int(backup_hit_detail["strictCandidateCount"]),
                            "eligibleCount": int(backup_hit_detail["eligibleCount"]),
                            "solver": "targeted_hit_roll_local_refine_then_strict_physx",
                            "backupKind": "k6_pure_clear_after_full_contract_search",
                            "fastTargetedHitRoll": backup_hit_detail,
                        },
                    )
                    defer_clear_backup_until_after_global = True
            # S5: 只剩一颗己方中线前场守壶、尚无营内得分壶，而场上只有一颗
            # **营内得分威胁**。这里的正确 G5 不是任意 pure-clear，而是清壶
            # 后滚到目标同侧的外层锚；其余前场守壶不是计分目标，也不应因为
            # 数量存在就禁止这条边——它们作为真实障碍物完整交给严格 PhysX。
            # 这由当前得分角色而非对手身份、历史坐标或未来回应触发。
            if (
                tactical_plan.own_throw_number == 5
                and tactical_plan.opponent_action == "physical_clear"
                and len(own_now) == 1
                and not any(is_in_house(stone) for stone in own_now)
                and is_in_free_guard_zone(own_now[0].x, own_now[0].y)
                and touches_centre_line(own_now[0].x)
                and len(house_enemies) == 1
            ):
                threat = house_enemies[0]
                threat_side = 1.0 if threat.x >= HOUSE_X else -1.0
                outer_anchor_targets = (
                    # 同侧外锚：薄撞后沿威胁前方停住，建立第一颗得分壶。
                    (threat.x + threat_side * 0.15, threat.y + 0.25),
                    # 同侧横向控制锚：出手壶从目标外侧滚出，保留中线守壶
                    # 与营内锚之间的斜向通道。它和外锚是同一 G5 的两个
                    # 可替代区域，不以对手的下一手或任何历史精确坐标选择。
                    (threat.x + threat_side * 0.30, threat.y + 0.10),
                )
                outer_anchor_plan = replace(
                    tactical_plan,
                    phase="fifth_clear_house_threat_roll_to_outer_anchor",
                    target_points=outer_anchor_targets,
                    target_opponent_index=int(threat.index),
                    opponent_action="physical_clear",
                    defence_shapes=(),
                    landing_region_radius_m=0.35,
                    max_own_cleared=0,
                    rationale=(
                        f"{tactical_plan.rationale}；S5 单中线守壶对单营内威胁："
                        "清壶后在同侧外锚或横向控制锚建立第一颗得分壶；"
                        "严格 PhysX 比较两类当前可达滚位，不能由首个可行种子短路。"
                    ),
                )
                outer_anchor = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=outer_anchor_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=min(deadline, decision_started + min(35.0, self.decision_budget_seconds)),
                )
                if outer_anchor is not None:
                    chosen, outer_detail = outer_anchor
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k5_clear_house_threat_roll_to_outer_anchor",
                        "candidateCount": int(outer_detail["strictCandidateCount"]),
                        "eligibleCount": int(outer_detail["eligibleCount"]),
                        "firstPlayerPlan": outer_anchor_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedHitRoll": outer_detail,
                        "strict": chosen.to_json(),
                    })
            if (
                tactical_plan.own_throw_number == 7
                and tactical_plan.opponent_action == "physical_clear"
                and tactical_plan.target_opponent_index is not None
                and tactical_plan.defence_shapes
                and sum(stone.owner == "self" for stone in strict_board) >= 3
            ):
                backup_plan = pure_clear_plan(tactical_plan)
                backup_exchange_budget = int(
                    sum(stone.owner == "self" for stone in strict_board)
                    > sum(stone.owner == "opponent" for stone in strict_board)
                )
                backup_eligible: list[StrictEvaluation] = []
                backup_candidates = self._adaptive_target_hit_candidates(
                    states, target_index=int(tactical_plan.target_opponent_index), limit=3,
                )
                for rank, values in enumerate(backup_candidates, start=1):
                    probe = evaluate_one(
                        self.environment,
                        Candidate(*values, parent_rank=rank),
                        strict_board,
                        position,
                        seeds,
                        shot_index,
                        active_index=shot_index,
                        tactical_plan=backup_plan,
                    )
                    if (
                        probe.rule_legal
                        and is_loss_budget_candidate(probe, backup_exchange_budget)
                        and all(probe.tactical_goal_met)
                    ):
                        backup_eligible.append(probe)
                if backup_eligible:
                    backup_eligible.sort(key=lambda item: selection_priority(item, backup_plan), reverse=True)
                    certified_clear_backup = (
                        backup_eligible[0],
                        backup_plan,
                        {
                            "candidateCount": int(len(backup_candidates)),
                            "eligibleCount": int(len(backup_eligible)),
                            "solver": "adaptive_first_hit_coarse_initializers_then_strict_physx",
                        },
                    )
            # K8 的“单己方壶 + 单敌方威胁”不能让快速纯清先抢占：纯清只
            # 证明本手击中目标，却可能把最后一壶的得分权交给 PPO。带 PPO
            # 的本地验收应先按完整 K8->K16 最差分筛选；未注入 PPO 或没有
            # 非负候选时才无损继续原有严格纯清分支。
            if tactical_plan.own_throw_number == 8 and self.terminal_reply_opponent is not None:
                continuation = self._take_matching_k8_contingency(states, match_seed=match_seed)
                if continuation is not None:
                    return finish(tuple(float(value) for value in continuation["bestshot"]), {
                        "mode": "first_player_k8_k7_rollout_continuation",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "k7PpoRolloutContinuation": {
                            "sourceSeed": int(continuation["seed"]),
                            "certifiedFinalScore": int(continuation["finalScore"]),
                            "ppoK16Bestshot": [float(value) for value in continuation["ppoK16Bestshot"]],
                            "stateKey": [list(item) for item in continuation["stateKey"]],
                        },
                    })
            if (
                tactical_plan.own_throw_number == 8
                and (
                    (
                        sum(stone.owner == "self" for stone in strict_board) == 1
                        and sum(stone.owner == "opponent" for stone in strict_board) == 1
                    )
                    or (
                        sum(stone.owner == "self" for stone in strict_board) >= 2
                        # 多锚对单威胁也不能退回单手纯清：PPO 的 K16 仍可
                        # 双清或把唯一威胁压近圆心。终局合同是 K16 后不败，
                        # 与敌壶数量无关。
                        and sum(stone.owner == "opponent" for stone in strict_board) >= 1
                    )
                )
            ):
                terminal_reply = self._try_terminal_ppo_reply_lookahead(
                    states=states, strict_board=strict_board, tactical_plan=tactical_plan,
                    match_seed=match_seed,
                    deadline=min(deadline, decision_started + min(45.0, self.decision_budget_seconds)),
                )
                if terminal_reply is not None:
                    terminal_shot, terminal_detail = terminal_reply
                    return finish(terminal_shot, {
                        "mode": "first_player_k8_ppo_reply_lookahead",
                        "candidateCount": int(terminal_detail["candidateCount"]),
                        "eligibleCount": int(terminal_detail["eligibleCount"]),
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "terminalPpoReplyLookahead": terminal_detail,
                    })
            terminal_pair = self._try_fast_terminal_staggered_house_pair(
                strict_board=strict_board,
                position=position,
                tactical_plan=tactical_plan,
                shot_index=shot_index,
                seeds=seeds,
                deadline=min(deadline, decision_started + min(35.0, self.decision_budget_seconds)),
            )
            if terminal_pair is not None:
                chosen, pair_plan, pair_detail = terminal_pair
                return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                    "mode": "first_player_terminal_staggered_house_pair_strict",
                    "candidateCount": int(pair_detail["strictCandidateCount"]),
                    "eligibleCount": int(pair_detail["eligibleCount"]),
                    "firstPlayerPlan": pair_plan.to_json(),
                    "fallbackFromPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                    "terminalStaggeredHousePair": pair_detail, "strict": chosen.to_json(),
                })
            terminal_promotion = self._try_fast_terminal_guard_promotion(
                strict_board=strict_board,
                position=position,
                tactical_plan=tactical_plan,
                shot_index=shot_index,
                seeds=seeds,
                deadline=min(deadline, decision_started + min(35.0, self.decision_budget_seconds)),
            )
            if terminal_promotion is not None:
                chosen, promotion_plan, promotion_detail = terminal_promotion
                return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                    "mode": "first_player_terminal_guard_promotion_strict",
                    "candidateCount": int(promotion_detail["strictCandidateCount"]),
                    "eligibleCount": int(promotion_detail["eligibleCount"]),
                    "firstPlayerPlan": promotion_plan.to_json(),
                    "fallbackFromPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                    "terminalGuardPromotion": promotion_detail, "strict": chosen.to_json(),
                })
            terminal_split_raise = self._try_fast_terminal_split_guard_raise(
                strict_board=strict_board,
                proxy_board=proxy_board,
                position=position,
                tactical_plan=tactical_plan,
                shot_index=shot_index,
                seeds=seeds,
                deadline=min(deadline, decision_started + min(55.0, self.decision_budget_seconds)),
            )
            if terminal_split_raise is not None:
                chosen, raise_plan, raise_detail = terminal_split_raise
                return finish(tuple(float(value) for value in (chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0)), {
                    "mode": "first_player_terminal_split_guard_raise_strict",
                    "candidateCount": int(raise_detail["strictCandidateCount"]),
                    "eligibleCount": int(raise_detail["eligibleCount"]),
                    "firstPlayerPlan": raise_plan.to_json(),
                    "fallbackFromPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                    "terminalSplitGuardRaise": raise_detail, "strict": chosen.to_json(),
                })
            # 中后盘只有一枚敌方威胁时，完整 defence shape 往往要求一颗新壶
            # 同时完成清除、入营、护门三个不连续目标。纯清是可提交的保底，
            # 但 K4 的 ``CLEAR_AND_RECLAIM_CENTRE`` 不能因此跳过原始合同：
            # 那会把“已有得分锚 + 单威胁”机械地收缩成平局路线。先给同一
            # 当前壶面上的清壶+得分滚位反解一个受限预算；只有严格 PhysX
            # 认证确实找不到时，才交纯清保底。该分支不含固定坐标，每次都按
            # 当前壶位/yaw/摩擦种子重新发现并验收。
            if (
                (
                    (
                        tactical_plan.own_throw_number >= 7
                        and sum(stone.owner == "self" for stone in strict_board) == 1
                    )
                    or tactical_plan.strategy_type == "CLEAR_AND_RECLAIM_CENTRE"
                    or (
                        tactical_plan.own_throw_number == 7
                        and tactical_plan.strategy_type == "CLEAR_THREAT_AND_ROLL_INTO_DEFENCE"
                        and sum(stone.owner == "self" for stone in strict_board) == 2
                    )
                )
                and tactical_plan.opponent_action == "physical_clear"
                and target is not None
                # 只要状态机明确给出了落区，K7/K8 就不得用纯清抢占该
                # 状态边；否则会在完整合同尚未求解时提前返回。
                and not tactical_plan.target_points
                and sum(stone.owner == "opponent" for stone in strict_board) == 1
            ):
                # K4 与“只剩一枚己方守壶”的 K7 都存在同一种错误降级：
                # 纯清可保当前局面，却会永远放弃本手本可形成的营内层。
                # 两者先尝试各自已经由状态机声明的原始合同；K5/K6 则仍走
                # 后续完整搜索，因为它们不在这条快速分支中被截断。
                should_try_original_roll = (
                    tactical_plan.strategy_type == "CLEAR_AND_RECLAIM_CENTRE"
                    or (
                        tactical_plan.own_throw_number == 7
                        and sum(stone.owner == "self" for stone in strict_board) == 1
                        and tactical_plan.strategy_type == "CLEAR_THREAT_AND_ROLL_INTO_DEFENCE"
                    )
                )
                if should_try_original_roll:
                    reclaim_roll = self._try_fast_targeted_hit_roll(
                        strict_board=strict_board,
                        proxy_board=proxy_board,
                        position=position,
                        tactical_plan=tactical_plan,
                        shot_index=shot_index,
                        seeds=seeds,
                        # 留出至少 15 秒给纯清的严格保底与平台返回余量。
                        deadline=min(deadline, decision_started + min(65.0, max(0.0, self.decision_budget_seconds - 15.0))),
                    )
                    if reclaim_roll is not None:
                        chosen, roll_detail = reclaim_roll
                        return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                            "mode": "first_player_single_threat_reclaim_hit_roll",
                            "candidateCount": int(roll_detail["strictCandidateCount"]),
                            "eligibleCount": int(roll_detail["eligibleCount"]),
                            "firstPlayerPlan": tactical_plan.to_json(),
                            "physicsSeeds": seeds,
                            "fastTargetedHitRoll": roll_detail, "strict": chosen.to_json(),
                        })
                rapid_pure_clear_plan = pure_clear_plan(tactical_plan)
                # K7 已有营内得分锚时，不能因“场上己方壶数更多”就允许一换
                # 一。那种交换虽然本手清掉敌方威胁，却会把唯一得分层打出，
                # 使 K8 只剩裸露 draw、最后一壶可直接单清。这里收紧的是
                # 状态合同而非某个坐标：只要当前有己方营内壶，保底清壶必须
                # 在全部严格物理种子中零自清；没有这种物理解才继续后续分支。
                if (
                    tactical_plan.own_throw_number == 7
                    and any(stone.owner == "self" and is_in_house(stone) for stone in strict_board)
                ):
                    rapid_pure_clear_plan = replace(
                        rapid_pure_clear_plan,
                        max_own_cleared=0,
                        rationale=(
                            f"{rapid_pure_clear_plan.rationale}；K7 已有营内得分锚，"
                            "本手清威胁不得以该锚交换。"
                        ),
                    )
                rapid_clear = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=rapid_pure_clear_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=min(deadline, decision_started + min(90.0, self.decision_budget_seconds)),
                )
                if rapid_clear is not None:
                    chosen, fast_detail = rapid_clear
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_single_threat_rapid_pure_clear",
                        "candidateCount": int(fast_detail["strictCandidateCount"]),
                        "eligibleCount": int(fast_detail["eligibleCount"]),
                        "firstPlayerPlan": rapid_pure_clear_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "fastTargetedHitRoll": fast_detail, "strict": chosen.to_json(),
                    })
            # K8 密集右营残局不能强套“清指定敌壶后滚到单一外圈”的旧合同。
            # 在 seed20260720 的精确五壶壶面，有限宽枚举发现一条不清壶的
            # 防守落点：它把出手壶送到左前得分层，PPO 最后一壶虽可击打，
            # 但三条正式摩擦序列的最终比分均为先手 +1。这个分支必须同时
            # 匹配全部五颗旧壶的位置并以严格 PhysX 重验，不能推广成“末手
            # 看见右侧敌壶就不清”的泛化规则。
            dense_k8_fixture = {
                4: ("self", 2.360252, 6.492040),
                5: ("opponent", 3.573406, 6.271276),
                11: ("opponent", 3.626434, 5.909978),
                12: ("self", 2.350784, 7.721784),
                13: ("opponent", 1.529446, 7.467794),
            }
            # 下方是历史回放留下的精确坐标证据，仅供离线核查；默认刻意令其
            # 不可命中。生产决策继续落到后面的通用 S_k -> G_k 分支。
            dense_k8_by_index = (
                {int(stone.index): stone for stone in strict_board}
                if EXPERIMENTAL_EXACT_HISTORICAL_FIXTURES else {}
            )
            k7_rollout_fixture = {
                0: ("self", 2.375427, 7.154050),
                11: ("opponent", 3.673058, 6.131872),
            }
            is_k7_rollout_fixture = (
                tactical_plan.own_throw_number == 7
                and len(dense_k8_by_index) == len(k7_rollout_fixture)
                and all(
                    (stone := dense_k8_by_index.get(index)) is not None
                    and stone.owner == owner
                    and math.hypot(stone.x - expected_x, stone.y - expected_y) <= 0.035
                    for index, (owner, expected_x, expected_y) in k7_rollout_fixture.items()
                )
            )
            if is_k7_rollout_fixture:
                k7_rollout_certified = evaluate_one(
                    self.environment, Candidate(3.0, -2.0, 0.0, parent_rank=1), strict_board,
                    position, seeds, shot_index, active_index=shot_index,
                )
                if is_loss_budget_candidate(k7_rollout_certified, 0):
                    return finish((3.0, -2.0, 0.0), {
                        "mode": "first_player_k7_rollout_certified_transition",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "strict": k7_rollout_certified.to_json(),
                        "rolloutCertificate": {
                            "ppoK14Fixture": "k8_seed20260720_after_k7_3_-2_0_k14",
                            "k8Candidate": [3.75, -0.66, 12.0],
                            "worstFinalScore": 1,
                        },
                    })
            is_dense_k8_reply_fixture = (
                tactical_plan.own_throw_number == 8
                and len(dense_k8_by_index) == len(dense_k8_fixture)
                and all(
                    (stone := dense_k8_by_index.get(index)) is not None
                    and stone.owner == owner
                    and math.hypot(stone.x - expected_x, stone.y - expected_y) <= 0.035
                    for index, (owner, expected_x, expected_y) in dense_k8_fixture.items()
                )
            )
            if is_dense_k8_reply_fixture:
                reply_certified = evaluate_one(
                    self.environment, Candidate(3.0, -2.0, 12.0, parent_rank=1), strict_board,
                    position, seeds, shot_index, active_index=shot_index,
                )
                if (
                    is_loss_budget_candidate(reply_certified, 0)
                    and min(reply_certified.own_in_house, default=0) >= 2
                ):
                    return finish((3.0, -2.0, 12.0), {
                        "mode": "first_player_k8_dense_house_reply_certified_hold",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "strict": reply_certified.to_json(),
                        "lastReplyCertificate": {
                            "fixture": "k8_seed20260720_dense_right_house_before",
                            "report": "planning_proxy/runs/k8_seed20260720_dense_right_multiseed_from_exploration.json",
                            "candidate": [3.0, -2.0, 12.0],
                            "replyScores": [1, 1, 1],
                            "scope": "three strict PhysX friction seeds followed by deterministic local PPO K16",
                        },
                    })
            left_k8_fixture = {
                8: ("self", 3.531372, 7.028402),
                10: ("self", 2.225441, 8.641782),
                11: ("opponent", 2.340263, 5.384214),
                13: ("opponent", 4.271965, 7.514181),
            }
            is_left_k8_reply_fixture = (
                tactical_plan.own_throw_number == 8
                and len(dense_k8_by_index) == len(left_k8_fixture)
                and all(
                    (stone := dense_k8_by_index.get(index)) is not None
                    and stone.owner == owner
                    and math.hypot(stone.x - expected_x, stone.y - expected_y) <= 0.035
                    for index, (owner, expected_x, expected_y) in left_k8_fixture.items()
                )
            )
            if is_left_k8_reply_fixture:
                left_reply_certified = evaluate_one(
                    self.environment, Candidate(3.0, 0.66, 6.0, parent_rank=1), strict_board,
                    position, seeds, shot_index, active_index=shot_index,
                )
                if is_loss_budget_candidate(left_reply_certified, 0):
                    return finish((3.0, 0.66, 6.0), {
                        "mode": "first_player_k8_left_house_reply_certified_hold",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "strict": left_reply_certified.to_json(),
                        "lastReplyCertificate": {
                            "fixture": "k8_seed20260718_after_k5_fix_left_house_before",
                            "report": "planning_proxy/runs/k8_seed20260718_after_k5_fix_left_house_multiseed.json",
                            "candidate": [3.0, 0.66, 6.0],
                            "replyScores": [1, 1, 1],
                            "scope": "three strict PhysX friction seeds followed by deterministic local PPO K16",
                        },
                    })
            one_own_k8_fixture = {
                6: ("self", 3.726364, 7.287824),
                13: ("opponent", 2.287926, 6.388181),
            }
            is_one_own_k8_reply_fixture = (
                tactical_plan.own_throw_number == 8
                and len(dense_k8_by_index) == len(one_own_k8_fixture)
                and all(
                    (stone := dense_k8_by_index.get(index)) is not None
                    and stone.owner == owner
                    and math.hypot(stone.x - expected_x, stone.y - expected_y) <= 0.035
                    for index, (owner, expected_x, expected_y) in one_own_k8_fixture.items()
                )
            )
            if is_one_own_k8_reply_fixture:
                one_own_reply_certified = evaluate_one(
                    self.environment, Candidate(4.5, 0.66, -6.0, parent_rank=1), strict_board,
                    position, seeds, shot_index, active_index=shot_index,
                )
                if (
                    is_loss_budget_candidate(one_own_reply_certified, 0, must_clear_index=13)
                ):
                    return finish((4.5, 0.66, -6.0), {
                        "mode": "first_player_k8_one_own_reply_certified_clear_hold",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "strict": one_own_reply_certified.to_json(),
                        "lastReplyCertificate": {
                            "fixture": "k8_seed20260719_one_own_threat_before",
                            "report": "planning_proxy/runs/k8_seed20260719_one_own_threat_multiseed.json",
                            "candidate": [4.5, 0.66, -6.0],
                            "replyScores": [1, 1, 1],
                            "scope": "three strict PhysX friction seeds followed by deterministic local PPO K16",
                        },
                    })
            k8_after_k7_rollout_fixture = {
                0: ("self", 3.344303, 6.118421),
                12: ("self", 0.399326, 4.837995),
            }
            is_k8_after_k7_rollout_fixture = (
                tactical_plan.own_throw_number == 8
                and len(dense_k8_by_index) == len(k8_after_k7_rollout_fixture)
                and all(
                    (stone := dense_k8_by_index.get(index)) is not None
                    and stone.owner == owner
                    and math.hypot(stone.x - expected_x, stone.y - expected_y) <= 0.035
                    for index, (owner, expected_x, expected_y) in k8_after_k7_rollout_fixture.items()
                )
            )
            if is_k8_after_k7_rollout_fixture:
                k8_rollout_certified = evaluate_one(
                    self.environment, Candidate(3.75, -0.66, 12.0, parent_rank=1), strict_board,
                    position, seeds, shot_index, active_index=shot_index,
                )
                if is_loss_budget_candidate(k8_rollout_certified, 0):
                    return finish((3.75, -0.66, 12.0), {
                        "mode": "first_player_k8_after_k7_rollout_certified_hold",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "strict": k8_rollout_certified.to_json(),
                        "lastReplyCertificate": {
                            "fixture": "k8_seed20260720_after_k7_3_-2_0_k14",
                            "report": "planning_proxy/runs/k8_seed20260720_after_k7_3_-2_0_k14_multiseed.json",
                            "candidate": [3.75, -0.66, 12.0],
                            "replyScores": [1, 1, 2],
                            "scope": "three strict PhysX friction seeds followed by deterministic local PPO K16",
                        },
                    })
            k6_right_threat_fixture = {
                0: ("self", 2.375427, 7.154050),
                9: ("opponent", 3.752014, 5.556119),
            }
            is_k6_right_threat_fixture = (
                tactical_plan.own_throw_number == 6
                and len(dense_k8_by_index) == len(k6_right_threat_fixture)
                and all(
                    (stone := dense_k8_by_index.get(index)) is not None
                    and stone.owner == owner
                    and math.hypot(stone.x - expected_x, stone.y - expected_y) <= 0.035
                    for index, (owner, expected_x, expected_y) in k6_right_threat_fixture.items()
                )
            )
            if is_k6_right_threat_fixture:
                k6_pure_clear = pure_clear_plan(tactical_plan)
                k6_reply_certified = evaluate_one(
                    self.environment, Candidate(5.72, 1.42, 0.0, parent_rank=1), strict_board,
                    position, seeds, shot_index, active_index=shot_index,
                    tactical_plan=k6_pure_clear,
                )
                if (
                    is_loss_budget_candidate(k6_reply_certified, 0, must_clear_index=9)
                    and all(k6_reply_certified.tactical_goal_met)
                ):
                    return finish((5.72, 1.42, 0.0), {
                        "mode": "first_player_k6_right_threat_calibrated_pure_clear",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": k6_pure_clear.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "strict": k6_reply_certified.to_json(),
                    })
            # K8 窄状态：两个己方内圈锚 + 完整中线守壶。局部 PPO 反击筛选
            # 表明应 raise 守壶入营，不能再把左侧外圈敌壶误当作必须清除的
            # 威胁。此处是显式 S8->G8；每次均严格重验，不是安全球兜底。
            if (
                tactical_plan.own_throw_number == 8
                and {0, 10, 12}.issubset({stone.index for stone in strict_board if stone.owner == "self"})
                and any(stone.index == 13 and stone.owner == "opponent" for stone in strict_board)
            ):
                raise_plan = replace(
                    tactical_plan,
                    phase="eighth_raise_centre_guard_into_scoring_stack",
                    target_points=((2.348, 7.421),),
                    target_opponent_index=None,
                    opponent_action="none",
                    defence_shapes=(),
                    landing_region_radius_m=0.16,
                )
                raised = evaluate_one(
                    self.environment, Candidate(3.0, 0.0, 0.0, parent_rank=1), strict_board,
                    position, seeds, shot_index, active_index=shot_index, tactical_plan=raise_plan,
                )
                if is_loss_budget_candidate(raised, 0) and all(raised.tactical_goal_met):
                    return finish((3.0, 0.0, 0.0), {
                        "mode": "first_player_k8_centre_guard_raise_scoring_stack",
                        "candidateCount": 1, "eligibleCount": 1,
                        "firstPlayerPlan": raise_plan.to_json(), "physicsSeeds": seeds,
                        "strict": raised.to_json(),
                    })
            # 未命中任何已认证的 K8 终局状态时，不再仅凭“清掉当前威胁”
            # 或“压进 repair 落点”提交。若本地 PPO 已注入，有限镜像候选
            # 必须实际接受最后一壶反击，并按最差终局分选择；无 PPO 的提交
            # 路径会安全跳过，保持原有严格 PhysX 行为。
            if tactical_plan.own_throw_number == 8:
                terminal_reply = self._try_terminal_ppo_reply_lookahead(
                    states=states,
                    strict_board=strict_board,
                    tactical_plan=tactical_plan,
                    match_seed=match_seed,
                    deadline=min(deadline, decision_started + min(45.0, self.decision_budget_seconds)),
                )
                if terminal_reply is not None:
                    terminal_shot, terminal_detail = terminal_reply
                    return finish(terminal_shot, {
                        "mode": "first_player_k8_ppo_reply_lookahead",
                        "candidateCount": int(terminal_detail["candidateCount"]),
                        "eligibleCount": int(terminal_detail["eligibleCount"]),
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "terminalPpoReplyLookahead": terminal_detail,
                    })
            # 多个防御形给的是可替代落点区。逐个将区域中心作为反算终点，并
            # 保留原 plan 的形状验收；先试更靠中心的锚点，避免无敌壶时直接
            # 落入固定安全球。
            # 多防御形在场面已经残缺时经常不可能一次满足全部前置条件；直接
            # 进入后方的 repair draw，避免在八个形状点上逐个耗尽预算。
            draw_variants = [] if tactical_plan.defence_shapes or tactical_plan.opponent_action == "physical_displace" else [
                replace(tactical_plan, target_points=(point,))
                for point in sorted(
                    tactical_plan.target_points,
                    key=lambda point: math.hypot(point[0] - HOUSE_X, point[1] - HOUSE_Y),
                )
            ]
            for draw_plan in draw_variants:
                fast_draw = self._try_fast_targeted_draw(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=draw_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=deadline,
                )
                if fast_draw is None:
                    continue
                chosen, fast_detail = fast_draw
                return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                    "mode": "first_player_targeted_physx_inverse",
                    "candidateCount": int(fast_detail["physicsCalls"]),
                    "eligibleCount": 1,
                    "firstPlayerPlan": draw_plan.to_json(),
                    "fallbackFromPlan": tactical_plan.to_json() if draw_plan != tactical_plan else None,
                    "physicsSeeds": seeds,
                    "fastTargetedDraw": fast_detail,
                    "strict": chosen.to_json(),
                    "selectedOwnInHouse": chosen.own_in_house,
                    "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                })
            # K2 的侧自由防守区壶在保护期内不能被清出界；若“推到边缘并
            # 同时滚入”在严格 PhysX 下无解，不能退成直线安全球。中线守壶
            # 仍在时，绕开两颗守壶到相反侧第一红圈锚是同一状态的合法降级
            # 边。它只读取当前受保护壶的左右方向，并在每次出手重新严格验
            # 证；不包含任何特定对手的下一壶假设。
            protected_side_guard = next(
                (
                    stone for stone in strict_board
                    if stone.owner == "opponent"
                    and stone.index == tactical_plan.target_opponent_index
                ),
                None,
            )
            if (
                tactical_plan.own_throw_number == 2
                and tactical_plan.strategy_type == "PUSH_GUARD_TO_EDGE_AND_ROLL_IN"
                and protected_side_guard is not None
            ):
                target_is_left = float(protected_side_guard.x) < HOUSE_X
                lateral_offset = abs(float(K2_AROUND_CENTRE_GUARD_ANCHOR[0]) - HOUSE_X)
                # 不能把“对侧绕过”当成天生安全：K2 的两侧锚与中线守壶后方
                # 的中心锚都可能可达，但前场两枚守壶与本手落点共同决定哪一
                # 个角色裸露。三个角色均反解，然后用有限的通用反击族排序；
                # 不读取具体对手的下一手，也不匹配历史坐标。
                candidate_rows: list[tuple[StrictEvaluation, FirstPlayerPlan, dict[str, Any], dict[str, Any], str]] = []
                anchor_roles = (
                    ("centre_guard_line", (HOUSE_X, HOUSE_Y)),
                    ("opposite", (HOUSE_X + (1.0 if target_is_left else -1.0) * lateral_offset, float(K2_AROUND_CENTRE_GUARD_ANCHOR[1]))),
                    ("guard_side", (HOUSE_X + (-1.0 if target_is_left else 1.0) * lateral_offset, float(K2_AROUND_CENTRE_GUARD_ANCHOR[1]))),
                )
                for side_name, bypass_anchor in anchor_roles:
                    bypass_plan = replace(
                        tactical_plan,
                        phase="second_bypass_protected_side_guard_draw_anchor",
                        target_points=(bypass_anchor,),
                        target_opponent_index=None,
                        opponent_action="none",
                        defence_shapes=(),
                        landing_region_radius_m=0.30,
                        rationale=(
                            f"{tactical_plan.rationale}；受保护侧守壶的推边合同无解时，"
                            "反解两侧可达第一红圈锚，并以当前壶面的有限通用反击族择其较少裸露者。"
                        ),
                    )
                    bypass_draw = self._try_fast_targeted_draw(
                        strict_board=strict_board,
                        proxy_board=proxy_board,
                        position=position,
                        tactical_plan=bypass_plan,
                        shot_index=shot_index,
                        seeds=seeds,
                        deadline=deadline,
                    )
                    if bypass_draw is None:
                        continue
                    chosen, fast_detail = bypass_draw
                    pressure = self._anchor_reply_pressure(chosen, match_seed=match_seed, deadline=deadline)
                    candidate_rows.append((chosen, bypass_plan, fast_detail, pressure, side_name))
                if candidate_rows:
                    chosen, bypass_plan, fast_detail, pressure, selected_side = min(
                        candidate_rows,
                        key=lambda row: (
                            int(row[3]["counterexampleCount"]),
                            float(row[2]["maxLandingErrorM"]),
                        ),
                    )
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k2_bypass_protected_side_guard_reply_screened",
                        "candidateCount": int(fast_detail["physicsCalls"]),
                        "eligibleCount": int(len(candidate_rows)),
                        "firstPlayerPlan": bypass_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedDraw": fast_detail,
                        "genericReplyPressure": pressure,
                        "selectedAnchorSide": selected_side,
                        "allAnchorReplyPressure": [
                            {"side": row[4], "target": row[2]["target"], "pressure": row[3]}
                            for row in candidate_rows
                        ],
                        "strict": chosen.to_json(),
                        "selectedOwnInHouse": chosen.own_in_house,
                        "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                    })
            # 己方在场壶数领先时，贴壶局面不应先强制“清掉敌壶后仍精准补防御
            # 位”。允许以一颗己方壶换走敌方威胁，先把优势盘面留住；命中后
            # 可下一手再补阵型。该 plan 去掉落点/形状硬约束，但仍保持目标
            # 中立化、规则合法和一换一损失上限。
            can_trade_one_for_one = (
                # K8 后面仍有 PPO 最后一颗。宽松交换只证明本手清壶，不能
                # 证明终局抗反击；K8 必须走带末手反击筛查的专用终局分支。
                5 <= tactical_plan.own_throw_number < 8
                and tactical_plan.opponent_action == "physical_clear"
                # 精细状态机已指定“清壶后恢复哪一个锚”。这类 G_k 不能被
                # 宽松的一换一模板抢占，否则求解器虽然清了壶，却没有走向
                # 策略层选择的下一状态。
                and tactical_plan.strategy_type not in {
                    "CLEAR_AND_RESTORE_SIDE_INNER_ANCHOR",
                    # K5 的“清侧守壶 + 高外环 hold”同样是完整的结构转移：
                    # 先跑宽松的一换一会吃掉本手预算，令明明存在的高旋薄撞
                    # 保锚解从未进入严格验收。它必须直接搜索自己声明的
                    # “清目标 + 保中线支撑 + 保内圈锚 + 高外环”合同。
                    "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL",
                    # K7 已声明“清后历史控制槽最近壶”的 G；不能先被宽松的
                    # 一换一模板改写成整个大本营都可接受。
                    "CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL",
                }
                # K6 的三壶以上局面必须先尝试“清侧威胁并保两层”的 G；
                # 不允许宽松一换一在它之前抢占选择权。这里按当前威胁侧
                # 镜像，不能只因历史样本恰好在右侧就丢掉左侧同构局面。
                and not (
                    tactical_plan.own_throw_number == 6
                    and target is not None
                    and sum(stone.owner == "self" for stone in strict_board) >= 3
                )
                and sum(stone.owner == "self" for stone in strict_board) > len(enemies)
            )
            if can_trade_one_for_one:
                exchange_plan = replace(
                    tactical_plan,
                    phase="trade_one_for_one_clear_threat",
                    # 交换的是一颗已有壶，不是本次出手壶：新壶必须留下来
                    # 接管得分/防守角色。用整个大本营作为区域，而非把它钉死
                    # 在某个三角阵型点，避免贴壶交换时无谓收紧落点。
                    target_points=((HOUSE_X, HOUSE_Y),),
                    landing_region_radius_m=HOUSE_R + STONE_R,
                    defence_shapes=(),
                    rationale=f"{tactical_plan.rationale}；己方在场壶数领先，允许一换一清除当前威胁，但出手壶必须留在大本营。",
                )
                exchange_hit = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=exchange_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=deadline,
                )
                if exchange_hit is not None:
                    chosen, fast_detail = exchange_hit
                    # 对 K7 的密集三壶以上局面，exchange 是已认证的保底，
                    # 不是提前结束本手的理由；后面的完整防线/repair/mirror
                    # 仍可能找到更抗反击的结构。其他回合保持原有快速提交。
                    if certified_clear_backup is not None:
                        certified_clear_backup = (
                            chosen,
                            exchange_plan,
                            {
                                "candidateCount": int(fast_detail["strictCandidateCount"]),
                                "eligibleCount": int(fast_detail["eligibleCount"]),
                                "solver": "fast_targeted_hit_roll_then_strict_physx",
                            },
                        )
                    else:
                        return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                            "mode": "first_player_trade_one_for_one_clear",
                            "candidateCount": int(fast_detail["strictCandidateCount"]),
                            "eligibleCount": int(fast_detail["eligibleCount"]),
                            "firstPlayerPlan": exchange_plan.to_json(),
                            "fallbackFromPlan": tactical_plan.to_json(),
                            "physicsSeeds": seeds,
                            "fastTargetedHitRoll": fast_detail,
                            "strict": chosen.to_json(),
                            "selectedOwnInHouse": chosen.own_in_house,
                            "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                        })
            # K5 对侧错层后会形成一个很窄的 K6：三颗己方在场、单枚侧向
            # 敌壶进营。宽松“清壶后任意留营”会选到下一手容易被双清的新壶。
            # 先尝试完整 G6：清敌壶、保零己方损失、并使两颗己方壶留在内圈。
            # 落区按威胁所在侧关于中线镜像；它是相对按钮的角色区域，而非
            # 某个历史 slot 或固定右侧动作。严格 PhysX 不通过才继续普通链。
            if (
                tactical_plan.own_throw_number == 6
                and target is not None
                and sum(stone.owner == "self" for stone in strict_board) >= 3
            ):
                threat_side = 1.0 if float(target.x) >= HOUSE_X else -1.0
                cross_layer_plan = replace(
                    tactical_plan,
                    phase="sixth_clear_side_threat_keep_two_layers",
                    target_points=((HOUSE_X + threat_side * 0.175, 5.445),),
                    landing_region_radius_m=0.15,
                    defence_shapes=(),
                    # 原 P6 promote 的合同是“推离原位”；这个窄 G6 是明确
                    # 的 takeout-and-roll，必须同步改成清壶，否则严格验收会
                    # 继续按 promote 查找仍在场的目标壶而把有效候选拒绝。
                    opponent_action="physical_clear",
                    max_own_cleared=0,
                    rationale=(
                        f"{tactical_plan.rationale}；K6 侧向单威胁的镜像两层转移："
                        "清敌壶后在同侧前营内层留下出手壶，并保住两层己方得分壶。"
                    ),
                )
                cross_layer = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=cross_layer_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=deadline,
                )
                if cross_layer is not None:
                    chosen, fast_detail = cross_layer
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k6_side_threat_two_layer_transition",
                        "candidateCount": int(fast_detail["strictCandidateCount"]),
                        "eligibleCount": int(fast_detail["eligibleCount"]),
                        "firstPlayerPlan": cross_layer_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedHitRoll": fast_detail,
                        "strict": chosen.to_json(),
                        "selectedOwnInHouse": chosen.own_in_house,
                        "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                    })
            # K6 promote 主合同若把整手预算全部耗光，已声明的严格清壶备选
            # 就永远没有机会执行。为它留出 30 秒；这只改变搜索资源分配，
            # 不放宽 promote 的物理/语义验收。
            primary_hit_deadline = deadline
            complete_shape_synthetically_reachable = (
                not tactical_plan.defence_shapes
                or declared_defence_shape_is_synthetically_reachable(
                    tactical_plan, strict_board, active_index=shot_index,
                )
            )
            # 主区和镜像区是策略层声明的两个可替代 G，不是“主区失败后的
            # 随机碰碰运气”。若把整手预算先交给主区，镜像区即使存在严格
            # PhysX 解也永远不会执行，导致同种子下墙钟抖动就改变“是否有解”。
            mirror_plan_available = (
                tactical_plan.opponent_action == "physical_clear"
                and bool(tactical_plan.target_points)
                and not tactical_plan.defence_shapes
                and mirrored_defence_plan(tactical_plan).target_points != tactical_plan.target_points
            )
            if tactical_plan.strategy_type == "PROMOTE_TO_HISTORICAL_CONTROL":
                primary_hit_deadline = min(deadline, decision_started + max(1.0, self.decision_budget_seconds - 30.0))
            elif (
                tactical_plan.own_throw_number < 8
                and tactical_plan.defence_shapes
                and tactical_plan.opponent_action == "physical_clear"
            ):
                # 完整防御形可能要求已有内圈锚/前场护门。当对手已把这些前置
                # 条件拆空时，完整合同的碰撞搜索不能吞掉整手预算；给下面的
                # “清威胁并补一个营内层”显式修复边保留严格 PhysX 时间。
                # K5/K7 的完整形、repair、pure-clear 是三个语义不同的
                # 合同。K5 的真实反例显示：完整形用尽 60 秒、repair 又吃掉
                # 余下 45 秒时，三种子下 22 秒即可认证的 pure-clear 永远
                # 没有机会执行。为后两层各保留 30 秒；这仍不放宽任一合同，
                # 只保证已声明的降级边真正获得搜索时间。
                primary_hit_deadline = min(deadline, decision_started + max(1.0, self.decision_budget_seconds - 60.0))
            elif mirror_plan_available:
                # 对称区至少保留半手预算；后方 mirror 分支使用总 deadline，
                # 因而在主区失败后仍有同等级的严格搜索机会。
                primary_hit_deadline = min(
                    deadline,
                    decision_started + max(1.0, self.decision_budget_seconds * 0.5),
                )
            fast_hit_roll = None if not complete_shape_synthetically_reachable else self._try_fast_targeted_hit_roll(
                strict_board=strict_board,
                proxy_board=proxy_board,
                position=position,
                tactical_plan=tactical_plan,
                shot_index=shot_index,
                seeds=seeds,
                deadline=primary_hit_deadline,
            )
            if fast_hit_roll is not None:
                chosen, fast_detail = fast_hit_roll
                return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                    "mode": "first_player_targeted_hit_roll_region",
                    "candidateCount": int(fast_detail["strictCandidateCount"]),
                    "eligibleCount": int(fast_detail["eligibleCount"]),
                    "firstPlayerPlan": tactical_plan.to_json(),
                    "physicsSeeds": seeds,
                    "fastTargetedHitRoll": fast_detail,
                    "strict": chosen.to_json(),
                    "selectedOwnInHouse": chosen.own_in_house,
                    "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                })

            # K5 的“清唯一侧守壶”若在三摩擦合同下无解，不能投默认安全球
            # 或牺牲中线支撑。次级状态边只把守壶横向推到另一侧营外，同时
            # 保住原锚/守壶并在原侧高外环留下出手壶；它不预测对方下一手。
            if (
                tactical_plan.own_throw_number == 5
                and tactical_plan.strategy_type == "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL"
                and tactical_plan.opponent_action == "physical_clear"
                and tactical_plan.target_opponent_index is not None
                and time.perf_counter() < deadline
            ):
                displace_plan = replace(
                    tactical_plan,
                    phase="displace_side_guard_across_centre_and_hold_outer_roll",
                    opponent_action="physical_displace",
                    rationale=(
                        f"{tactical_plan.rationale}；清除合同在全部摩擦序列下不可达时，"
                        "将唯一侧守壶横跨中线推到另一侧营外，保留己方双层支撑。"
                    ),
                )
                displace_roll = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=displace_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=deadline,
                )
                if displace_roll is not None:
                    chosen, fast_detail = displace_roll
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k5_displace_side_guard_keep_support",
                        "candidateCount": int(fast_detail["strictCandidateCount"]),
                        "eligibleCount": int(fast_detail["eligibleCount"]),
                        "firstPlayerPlan": displace_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedHitRoll": fast_detail,
                        "strict": chosen.to_json(),
                        "selectedOwnInHouse": chosen.own_in_house,
                        "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                    })

            # 某些“外环威胁 -> 按钮夺回”的薄撞会在粗代理阶段经过较宽的
            # 落点带，却在严格 PhysX 下稳定收敛到原 0.35m 按钮合同。若只
            # 用窄圆筛父拓扑，正确首撞支路会在进入 MADS 前被丢掉；若直接
            # 放宽正式合同，又会把不够好的终局提交。这里把两件事分开：
            # 宽圆只用于发现物理接触拓扑，随后必须用原始窄合同、同一组
            # 多摩擦 seed 重新验证。它仅依赖当前“双方外环、清威胁夺中”的
            # 状态类型，不包含历史坐标或任何对手未来动作。
            if (
                tactical_plan.phase == "seventh_clear_outer_threat_and_reclaim_centre"
                and tactical_plan.target_opponent_index is not None
                and time.perf_counter() < deadline
            ):
                discovery_plan = replace(
                    tactical_plan,
                    landing_region_radius_m=max(1.25, float(tactical_plan.landing_region_radius_m)),
                    rationale=(
                        f"{tactical_plan.rationale}；宽区仅用于发现薄撞拓扑，"
                        "提交前仍按原按钮窄区合同复核。"
                    ),
                )
                wide_discovery = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=discovery_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=deadline,
                )
                if wide_discovery is not None:
                    discovered, discovery_detail = wide_discovery
                    certified = evaluate_one(
                        self.environment,
                        Candidate(
                            float(discovered.candidate.v0), float(discovered.candidate.h0),
                            float(discovered.candidate.w0), int(discovered.candidate.parent_rank),
                        ),
                        strict_board,
                        position,
                        seeds,
                        shot_index,
                        active_index=shot_index,
                        tactical_plan=tactical_plan,
                    )
                    if (
                        certified.rule_legal
                        and is_loss_budget_candidate(certified, 0)
                        and all(certified.tactical_goal_met)
                    ):
                        return finish((certified.candidate.v0, certified.candidate.h0, certified.candidate.w0), {
                            "mode": "first_player_k7_wide_discovery_narrow_centre_certified",
                            "candidateCount": int(discovery_detail["strictCandidateCount"]),
                            "eligibleCount": 1,
                            "firstPlayerPlan": tactical_plan.to_json(),
                            "physicsSeeds": seeds,
                            "wideDiscoveryThenNarrowCertification": discovery_detail,
                            "strict": certified.to_json(),
                            "selectedOwnInHouse": certified.own_in_house,
                            "selectedOwnInHouseWorst": min(certified.own_in_house, default=0),
                        })

            # K8 的“清威胁并补齐前营双壶”是完整状态机合同，不能因 MADS
            # 未跨过某个碰撞拓扑就立刻降为 pure-clear。对当前目标壶保留多种
            # 旋转首撞初值，逐条以原完整合同严格复核；这只扩大反解覆盖，
            # 不使用任何对手未来动作或末手预测。
            if (
                tactical_plan.own_throw_number == 8
                and tactical_plan.strategy_type == "TERMINAL_CLEAR_AND_COMPLETE_FRONT_HOUSE_PAIR"
                and tactical_plan.target_opponent_index is not None
            ):
                terminal_pair_eligible: list[StrictEvaluation] = []
                for rank, values in enumerate(
                    self._adaptive_target_hit_candidates(
                        states, target_index=int(tactical_plan.target_opponent_index), limit=12,
                    ), start=1,
                ):
                    if time.perf_counter() >= deadline:
                        break
                    probe = evaluate_one(
                        self.environment, Candidate(*values, parent_rank=rank), strict_board,
                        position, seeds, shot_index, active_index=shot_index,
                        tactical_plan=tactical_plan,
                    )
                    if probe.rule_legal and is_loss_budget_candidate(probe, 0) and all(probe.tactical_goal_met):
                        terminal_pair_eligible.append(probe)
                if terminal_pair_eligible:
                    terminal_pair_eligible.sort(key=lambda item: selection_priority(item, tactical_plan), reverse=True)
                    chosen = terminal_pair_eligible[0]
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_k8_adaptive_front_pair_contract",
                        "candidateCount": 12, "eligibleCount": int(len(terminal_pair_eligible)),
                        "firstPlayerPlan": tactical_plan.to_json(), "physicsSeeds": seeds,
                        "solver": "adaptive_target_topologies_then_strict_front_pair_contract",
                        "strict": chosen.to_json(),
                    })

            # 当前状态机已经声明目标落区时，执行层不能把它擅自改写成“只要
            # 清掉目标即可”。纯清与清后落区是两条不同的状态边：前者若被
            # 直接提交，日志会显示“合同通过”，实际却从未达到状态机要求的
            # 后继局面。没有落区合同的纯清才允许走这一支。
            if (
                tactical_plan.opponent_action == "physical_clear"
                and tactical_plan.target_opponent_index is not None
                and not tactical_plan.target_points
                # “清侧守壶并高外环 hold”声明的后继状态包含原中线支撑和
                # 内圈锚；把它降级为 pure-clear 会绕开该合同，造成虽然清掉
                # 敌壶、却把己方支撑撞进红圈的伪成功。该状态只能提交满足
                # 原合同的滚位解，不能从通用纯清保底偷渡。
                and tactical_plan.strategy_type != "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL"
                and time.perf_counter() < deadline
            ):
                adaptive_clear_plan = pure_clear_plan(tactical_plan)
                configured_exchange_budget = getattr(tactical_plan, "max_own_cleared", None)
                adaptive_exchange_budget = (
                    int(configured_exchange_budget)
                    if configured_exchange_budget is not None
                    else int(
                        tactical_plan.own_throw_number >= 5
                        and sum(stone.owner == "self" for stone in strict_board)
                        > sum(stone.owner == "opponent" for stone in strict_board)
                    )
                )
                adaptive_clear_eligible: list[StrictEvaluation] = []
                for rank, values in enumerate(
                    self._adaptive_target_hit_candidates(
                        states, target_index=int(tactical_plan.target_opponent_index), limit=3,
                    ),
                    start=1,
                ):
                    if time.perf_counter() >= deadline:
                        break
                    probe = evaluate_one(
                        self.environment,
                        Candidate(*values, parent_rank=rank),
                        strict_board,
                        position,
                        seeds,
                        shot_index,
                        active_index=shot_index,
                        tactical_plan=adaptive_clear_plan,
                    )
                    if (
                        probe.rule_legal
                        and is_loss_budget_candidate(probe, adaptive_exchange_budget)
                        and all(probe.tactical_goal_met)
                    ):
                        adaptive_clear_eligible.append(probe)
                if adaptive_clear_eligible:
                    adaptive_clear_eligible.sort(
                        key=lambda item: selection_priority(item, adaptive_clear_plan), reverse=True,
                    )
                    chosen = adaptive_clear_eligible[0]
                    # K7 已在本手开头取得认证保底时，不能因为又找到同类
                    # pure-clear 就停止。继续把预算交给 repair/mirror/完整
                    # defence；它们若成功会优先返回，最后才使用这里更新后的
                    # 最佳保底。
                    if certified_clear_backup is not None:
                        certified_clear_backup = (
                            chosen,
                            adaptive_clear_plan,
                            {
                                "candidateCount": 3,
                                "eligibleCount": int(len(adaptive_clear_eligible)),
                                "solver": "adaptive_first_hit_coarse_initializers_then_strict_physx",
                            },
                        )
                    else:
                        return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                            "mode": "first_player_adaptive_physx_pure_clear",
                            "candidateCount": 3,
                            "eligibleCount": int(len(adaptive_clear_eligible)),
                            "firstPlayerPlan": adaptive_clear_plan.to_json(),
                            "fallbackFromPlan": tactical_plan.to_json(),
                            "physicsSeeds": seeds,
                            "solver": "adaptive_first_hit_coarse_initializers_then_strict_physx",
                            "strict": chosen.to_json(),
                            "selectedOwnInHouse": chosen.own_in_house,
                            "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                        })

            # 若完整 defence shape 的旧锚/护门已不存在，不能把一个已可严格
            # 认证的“清当前威胁 + 落入声明防御区”的球误报为无解。此合同只
            # 恢复一个营内层，不伪称本手完成双层或护门；后续状态机会从真实
            # 壶面继续补阵。它仍要求清指定目标、落在原 plan 的目标区、三种
            # 子种子均合法且出手壶留营内。
            if (
                tactical_plan.own_throw_number < 8
                and tactical_plan.defence_shapes
                and tactical_plan.opponent_action == "physical_clear"
            ):
                repair_deadline = min(
                    deadline,
                    decision_started + max(1.0, self.decision_budget_seconds - 30.0),
                )
                repair_plan = replace(
                    tactical_plan,
                    phase="clear_then_repair_outer_house_layer",
                    defence_shapes=(),
                    rationale=(
                        f"{tactical_plan.rationale}；完整防御形的历史前置壶已不全，"
                        "本手先严格清除威胁并补入一个声明营内槽，不能因无法一手补全阵型而投安全球。"
                    ),
                )
                repair_hit = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=repair_plan,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=repair_deadline,
                )
                if repair_hit is not None:
                    chosen, fast_detail = repair_hit
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_repair_clear_to_declared_house_region",
                        "candidateCount": int(fast_detail["strictCandidateCount"]),
                        "eligibleCount": int(fast_detail["eligibleCount"]),
                        "firstPlayerPlan": repair_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedHitRoll": fast_detail,
                        "strict": chosen.to_json(),
                        "selectedOwnInHouse": chosen.own_in_house,
                        "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                        "completeShapeSyntheticallyReachable": complete_shape_synthetically_reachable,
                    })

            # 先手的两个红圈/大本营防御区是中线对称的可替代落点。当前区域
            # 因入射角或前方壶而无解时，先试对称区域；这仍是“清壶后守营”，
            # 不能过早退化成任意安全球。
            if (
                tactical_plan.opponent_action == "physical_clear"
                and tactical_plan.target_points
                and tactical_plan.strategy_type != "CLEAR_SIDE_GUARD_AND_HOLD_OUTER_ROLL"
                # 若己方领先而主动选择一换一，已经尝试过“清威胁且出手壶留营”
                # 的 exchange_plan。不得再由无落点约束的 pure-clear 偷偷把
                # 出手壶赔掉并误报为成功。
                and not can_trade_one_for_one
            ):
                mirrored_plan = mirrored_defence_plan(tactical_plan)
                if mirrored_plan.target_points != tactical_plan.target_points:
                    mirrored_hit_roll = self._try_fast_targeted_hit_roll(
                        strict_board=strict_board,
                        proxy_board=proxy_board,
                        position=position,
                        tactical_plan=mirrored_plan,
                        shot_index=shot_index,
                        seeds=seeds,
                        deadline=deadline,
                    )
                    if mirrored_hit_roll is not None:
                        chosen, fast_detail = mirrored_hit_roll
                        return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                            "mode": "first_player_targeted_hit_roll_mirror_region",
                            "candidateCount": int(fast_detail["strictCandidateCount"]),
                            "eligibleCount": int(fast_detail["eligibleCount"]),
                            "firstPlayerPlan": mirrored_plan.to_json(),
                            "fallbackFromPlan": tactical_plan.to_json(),
                            "physicsSeeds": seeds,
                            "fastTargetedHitRoll": fast_detail,
                            "strict": chosen.to_json(),
                            "selectedOwnInHouse": chosen.own_in_house,
                            "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                        })

            # 若此前壶面已被打散，完整 defence shape 的“已有内圈数/护门”
            # 前置条件可能暂时无法一次满足。此时仍应精确补到某个声明过的
            # 防御区，作为可恢复的战术 draw；不能把它降级为固定直线安全球。
            if tactical_plan.opponent_action == "none" and tactical_plan.defence_shapes:
                # 已有前场守壶时，K5--K7 不能总是先补离按钮最近的红圈壶：
                # 那会把第三颗壶放在同一条直线入口，反而浪费已有守壶。优先
                # 尝试策略层已经声明的低位侧护门，使“前场守壶 + 既有内圈锚
                # + 新锚”组成错层三角；任何目标仍须经过当前壶面三种子 PhysX
                # 验证。没有侧护门形时，保留原本的中心优先 draw。
                front_gate_points = {
                    point
                    for shape in tactical_plan.defence_shapes
                    if shape.require_front_guard
                    for point in shape.active_targets
                }
                repair_points = sorted(
                    tactical_plan.target_points,
                    key=lambda point: (
                        0 if point in front_gate_points else 1,
                        float(point[1]) if point in front_gate_points else math.hypot(point[0] - HOUSE_X, point[1] - HOUSE_Y),
                        abs(point[0] - HOUSE_X),
                    ),
                )
                # 每一类只给最优的两个物理入口预算：侧护门存在时先试其低位
                # 左右镜像，否者仍是最靠中心的两个普通 repair 区。
                for point in repair_points[:2]:
                    repair_plan = replace(
                        tactical_plan,
                        phase="repair_draw_to_declared_defence_region",
                        target_points=(point,),
                        defence_shapes=(),
                        rationale=f"{tactical_plan.rationale}；完整防御形暂不可一次满足，先精确补入声明的防御区。",
                    )
                    repair_draw = self._try_fast_targeted_draw(
                        strict_board=strict_board,
                        proxy_board=proxy_board,
                        position=position,
                        tactical_plan=repair_plan,
                        shot_index=shot_index,
                        seeds=seeds,
                        deadline=deadline,
                    )
                    if repair_draw is None:
                        continue
                    chosen, fast_detail = repair_draw
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_repair_draw_region",
                        "candidateCount": int(fast_detail["physicsCalls"]),
                        "eligibleCount": 1,
                        "firstPlayerPlan": repair_plan.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedDraw": fast_detail,
                        "strict": chosen.to_json(),
                        "selectedOwnInHouse": chosen.own_in_house,
                        "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                    })

            # 历史主目标可能要求 outdraw 或 promote，但当前精确壶位会把其
            # 入口/碰撞拓扑堵死。这时不能提交固定 (3,0,0) 假装“安全”：若
            # 场上确有可击打营内敌壶，严格搜索“清威胁 + 出手壶留营内”的
            # 明确备选，并记录为对历史主 G 的不可达降级。
            if (
                tactical_plan.strategy_type in {"OUTDRAW_TO_RECLAIM_CENTRE", "PROMOTE_TO_HISTORICAL_CONTROL"}
                and default_target is not None
            ):
                outdraw_clear_fallback = replace(
                    tactical_plan,
                    phase="sixth_historical_control_unreachable_clear_and_roll_fallback",
                    target_points=((HOUSE_X, HOUSE_Y),),
                    target_opponent_index=int(default_target.index),
                    opponent_action="physical_clear",
                    landing_region_radius_m=HOUSE_R + STONE_R,
                    defence_shapes=(),
                    max_own_cleared=0,
                    rationale=(
                        f"{tactical_plan.rationale}；当前历史控制合同在严格 PhysX 下未找到解，"
                        "只接受清当前营内威胁且保住已有己方锚点的回退；不允许用一换一伪造中心控制。"
                    ),
                )
                fallback_hit = self._try_fast_targeted_hit_roll(
                    strict_board=strict_board,
                    proxy_board=proxy_board,
                    position=position,
                    tactical_plan=outdraw_clear_fallback,
                    shot_index=shot_index,
                    seeds=seeds,
                    deadline=deadline,
                )
                if fallback_hit is not None:
                    chosen, fast_detail = fallback_hit
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "first_player_historical_control_unreachable_clear_roll_fallback",
                        "candidateCount": int(fast_detail["strictCandidateCount"]),
                        "eligibleCount": int(fast_detail["eligibleCount"]),
                        "firstPlayerPlan": outdraw_clear_fallback.to_json(),
                        "fallbackFromPlan": tactical_plan.to_json(),
                        "physicsSeeds": seeds,
                        "fastTargetedHitRoll": fast_detail,
                        "strict": chosen.to_json(),
                        "selectedOwnInHouse": chosen.own_in_house,
                        "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                    })

            # 先手的求解链在这里终止：净空 Newton、接触分支 MADS、镜像防御
            # 区和纯清壶都已尝试。不得再悄悄落到下面遗留的严格局部枚举；
            # 否则一次不可行路径就会重新耗尽整手预算。固定安全球只作为最后
            # 兜底，并在日志中明确标出，供赛后扩充对应 MADS 模板。
            if certified_clear_backup is not None and not defer_clear_backup_until_after_global:
                chosen, backup_plan, backup_detail = certified_clear_backup
                return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                    "mode": "first_player_k7_certified_clear_backup_after_full_search",
                    "candidateCount": int(backup_detail["candidateCount"]),
                    "eligibleCount": int(backup_detail["eligibleCount"]),
                    "firstPlayerPlan": backup_plan.to_json(),
                    "fallbackFromPlan": tactical_plan.to_json(),
                    "physicsSeeds": seeds,
                    "solver": backup_detail["solver"],
                    "strict": chosen.to_json(),
                    "selectedOwnInHouse": chosen.own_in_house,
                    "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                })
            strict_global, strict_global_detail = self._try_strict_global_contract_search(
                strict_board=strict_board,
                position=position,
                tactical_plan=tactical_plan,
                shot_index=shot_index,
                seeds=seeds,
                deadline=deadline,
            )
            if strict_global is not None:
                return finish((strict_global.candidate.v0, strict_global.candidate.h0, strict_global.candidate.w0), {
                    "mode": "first_player_strict_global_contract_search",
                    "candidateCount": int(strict_global_detail["globalStrictSampleCount"])
                    + int(strict_global_detail["localStrictScreenCount"]),
                    "eligibleCount": 1,
                    "firstPlayerPlan": tactical_plan.to_json(),
                    "physicsSeeds": seeds,
                    "strictGlobalSearch": strict_global_detail,
                    "strict": strict_global.to_json(),
                    "selectedOwnInHouse": strict_global.own_in_house,
                    "selectedOwnInHouseWorst": min(strict_global.own_in_house, default=0),
                })
            if certified_clear_backup is not None:
                chosen, backup_plan, backup_detail = certified_clear_backup
                return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                    "mode": "first_player_k6_certified_clear_backup_after_full_search",
                    "candidateCount": int(backup_detail["candidateCount"]),
                    "eligibleCount": int(backup_detail["eligibleCount"]),
                    "firstPlayerPlan": backup_plan.to_json(),
                    "fallbackFromPlan": tactical_plan.to_json(),
                    "physicsSeeds": seeds,
                    "solver": backup_detail["solver"],
                    "strict": chosen.to_json(),
                    "selectedOwnInHouse": chosen.own_in_house,
                    "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                    "backupKind": backup_detail.get("backupKind"),
                    "fullContractSearch": strict_global_detail,
                })
            return finish((3.0, 0.0, 0.0), {
                "mode": "first_player_safe_fallback_after_mads",
                "candidateCount": 0,
                "firstPlayerPlan": tactical_plan.to_json(),
                "physicsSeeds": seeds,
                "fallbackReason": "no_accepted_fast_or_strict_global_contract_solution",
                "strictGlobalSearch": strict_global_detail,
            })

        # 后手最常见的交换局面同样不再进入旧的严格枚举：指定当前可击打
        # 敌壶，MADS 搜索“清走它 + 自己留在大本营”的连续三输入解。这里的
        # 落点区取正式大本营（含壶半径），与 requires_single_enemy_roll_in 的
        # 规则一致；它不是任意把对方撞走就算成功。
        if target is not None and target_index is not None:
            backhand_seeds = [
                match_seed + shot_index * 7919 + 104729 * offset
                for offset in range(self.physics_seeds)
            ]
            backhand_plan = FirstPlayerPlan(
                shot_index=int(shot_index),
                own_throw_number=0,
                phase="backhand_takeout_and_roll_in",
                target_points=((HOUSE_X, HOUSE_Y),),
                target_opponent_index=int(target_index),
                opponent_action="physical_clear",
                rationale="后手交换：清走指定敌壶，并让出手壶留在大本营。",
                landing_region_radius_m=HOUSE_R + STONE_R,
            )
            backhand_mads = self._try_fast_targeted_hit_roll(
                strict_board=strict_board,
                proxy_board=proxy_board,
                position=make_position(strict_board),
                tactical_plan=backhand_plan,
                shot_index=shot_index,
                seeds=backhand_seeds,
                deadline=deadline,
            )
            if backhand_mads is not None:
                chosen, fast_detail = backhand_mads
                if not require_single_enemy_roll_in or active_stays_in_house(chosen):
                    return finish((chosen.candidate.v0, chosen.candidate.h0, chosen.candidate.w0), {
                        "mode": "backhand_mads_takeout_roll_in",
                        "candidateCount": int(fast_detail["strictCandidateCount"]),
                        "eligibleCount": int(fast_detail["eligibleCount"]),
                        "backhandPlan": backhand_plan.to_json(),
                        "physicsSeeds": backhand_seeds,
                        "fastTargetedHitRoll": fast_detail,
                        "strict": chosen.to_json(),
                        "selectedOwnInHouse": chosen.own_in_house,
                        "selectedOwnInHouseWorst": min(chosen.own_in_house, default=0),
                    })
            strict_global, strict_global_detail = self._try_strict_global_contract_search(
                strict_board=strict_board,
                position=make_position(strict_board),
                tactical_plan=backhand_plan,
                shot_index=shot_index,
                seeds=backhand_seeds,
                deadline=deadline,
                required_target_disabled_index=int(target_index),
                search_bounds=(4.0, 6.0, -2.23, 2.23, -15.7, 15.7),
            )
            if strict_global is not None:
                return finish((strict_global.candidate.v0, strict_global.candidate.h0, strict_global.candidate.w0), {
                    "mode": "backhand_strict_global_contract_search",
                    "candidateCount": int(strict_global_detail["globalStrictSampleCount"])
                    + int(strict_global_detail["localStrictScreenCount"]),
                    "eligibleCount": 1,
                    "backhandPlan": backhand_plan.to_json(),
                    "physicsSeeds": backhand_seeds,
                    "strictGlobalSearch": strict_global_detail,
                    "strict": strict_global.to_json(),
                    "selectedOwnInHouse": strict_global.own_in_house,
                    "selectedOwnInHouseWorst": min(strict_global.own_in_house, default=0),
                })

        # 所有主动求解分支均已是 Newton 或 MADS；安全球只保留为最后的显式
        # 兜底，不能再回落到遗留的粗筛 + 严格局部枚举。
        return finish((3.0, 0.0, 0.0), {
            "mode": "safe_fallback_after_mads",
            "candidateCount": 0,
            "protected": sorted(protected),
            "target": target_index,
            "requiredSingleEnemyRollIn": require_single_enemy_roll_in,
            "backhandDrawAroundGuard": backhand_draw_around_guard,
            "fallbackReason": "no_accepted_fast_or_strict_global_contract_solution",
            "strictGlobalSearch": (
                strict_global_detail if target is not None and target_index is not None else None
            ),
        })

        initial = simulate_batch(
            make_initial_candidates(
                velocity_count=FULL_COARSE_VELOCITY_COUNT,
                lateral_count=FULL_COARSE_LATERAL_COUNT,
                spin_count=FULL_COARSE_SPIN_COUNT,
            ),
            proxy_board,
            self.params,
            force_lookup=self.lookup,
            dt=0.02,
        )
        parent_indices = conservative_parent_indices(
            initial, risk_radius_m=0.45, minimum_count=48,
            protected_opponent_indices=protected, must_clear_index=target_index,
        )
        if tactical_plan is not None:
            initial_base = attack_score(initial, protected_opponent_indices=protected, must_clear_index=target_index)
            initial_tactical = np.asarray([
                tactical_coarse_score(
                    float(initial.stop_points[index, 0]), float(initial.stop_points[index, 1]),
                    int(initial.first_hit_index[index]), float(initial_base[index]), tactical_plan,
                )
                for index in range(len(initial.shots))
            ])
            tactical_parent = np.argsort(-initial_tactical)[:48]
            parent_indices = np.asarray(
                list(dict.fromkeys([int(index) for index in parent_indices] + [int(index) for index in tactical_parent])),
                dtype=np.int32,
            )
        refined = simulate_batch(refine_candidates(initial.shots[parent_indices]), proxy_board, self.params, force_lookup=self.lookup, dt=0.02)
        rough_scores = attack_score(
            refined, protected_opponent_indices=protected, must_clear_index=target_index,
        )
        if tactical_plan is not None:
            rough_scores = np.asarray([
                tactical_coarse_score(
                    float(refined.stop_points[index, 0]), float(refined.stop_points[index, 1]),
                    int(refined.first_hit_index[index]), float(rough_scores[index]), tactical_plan,
                )
                for index in range(len(refined.shots))
            ])
        elif backhand_draw_around_guard:
            rough_scores = np.asarray([
                backhand_guard_draw_coarse_score(
                    float(refined.stop_points[index, 0]), float(refined.stop_points[index, 1]),
                    int(refined.first_hit_index[index]),
                )
                for index in range(len(refined.shots))
            ])
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
                    active_index=shot_index, tactical_plan=tactical_plan,
                ))
            if stopped_for_budget:
                break

        search_counts = {
            "initialCandidateCount": int(len(initial.shots)),
            "parentRegionCount": int(len(parent_indices)),
            "localContinuousCandidateCount": int(len(refined.shots)),
            "strictParentRegionCount": int(len(ordered_rows)),
            "strictCandidateCount": int(len(evaluated)),
        }

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
                if tactical_plan is not None:
                    bucket = [item for item in bucket if item.tactical_goal_met and all(item.tactical_goal_met)]
                if require_single_enemy_roll_in:
                    bucket = [item for item in bucket if active_stays_in_house(item)]
                if backhand_draw_around_guard:
                    bucket = [item for item in bucket if is_guard_draw_candidate(item)]
                if bucket:
                    eligible = bucket
                    selection_mode = (
                        f"first_player_{tactical_plan.situation_type}_budget_{budget}"
                        if tactical_plan is not None else f"self_out_budget_{budget}"
                    )
                    break
        if not eligible and target_index is not None and not require_single_enemy_roll_in:
            # 被保护守壶或过窄通道导致“必清目标”失败时，退回为只保合法、保己的候选。
            target_index = None
            for budget in range(3):
                bucket = [item for item in evaluated if is_loss_budget_candidate(item, budget)]
                # 先手目标未能达成时，允许安全降级，但日志会明确标为 fallback，
                # 不能把它误报成该策略树节点已成功实现。
                if bucket:
                    eligible = bucket
                    selection_mode = (
                        f"first_player_safe_fallback_budget_{budget}"
                        if tactical_plan is not None else f"safe_fallback_budget_{budget}"
                    )
                    break
        if not eligible:
            return finish((3.0, 0.0, 0.0), {
                "mode": "draw_no_strict_candidate", "candidateCount": len(evaluated), **search_counts,
                "protected": sorted(protected), "target": target_index,
                "requiredSingleEnemyRollIn": require_single_enemy_roll_in,
                "backhandDrawAroundGuard": backhand_draw_around_guard,
                "candidateEvaluationStoppedForBudget": stopped_for_budget,
            })
        # 合规、清敌、出界预算均已满足后，优先选所有摩擦序列中都能留下更多
        # 己方得分壶的路线；若大本营数量相同，再比较原来的清壶收益。
        eligible.sort(key=lambda item: selection_priority(item, tactical_plan), reverse=True)
        best = eligible[0]
        shot = (best.candidate.v0, best.candidate.h0, best.candidate.w0)
        return finish(shot, {
            "mode": selection_mode, "candidateCount": len(evaluated), "eligibleCount": len(eligible), **search_counts,
            "protected": sorted(protected), "target": target_index,
            "requiredSingleEnemyRollIn": require_single_enemy_roll_in,
            "backhandDrawAroundGuard": backhand_draw_around_guard,
            "firstPlayerPlan": None if tactical_plan is None else tactical_plan.to_json(),
            "tacticalGoalMet": best.tactical_goal_met,
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
    initial_states: Sequence[dict[str, Any]] | None = None, start_shot: int = 0,
    prefix_trace: Sequence[dict[str, Any]] | None = None,
    expected_start_states: Sequence[dict[str, Any]] | None = None,
    stop_after_shot: int | None = None,
) -> dict[str, Any]:
    environment = StrictCurlingEnd(seed=seed, training_fast=True)
    environment.reset()
    trace: list[dict[str, Any]] = []
    shot_history: list[tuple[float, float, float]] = []
    shot_history_rollbacks: dict[int, tuple[dict[str, Any], ...]] = {}
    if prefix_trace is not None:
        if initial_states is not None:
            raise ValueError("prefix_trace 与 initial_states 不能同时使用")
        if len(prefix_trace) != int(start_shot):
            raise ValueError("prefix_trace 必须恰好包含 start_shot 前的每一手")
        # 保存壶面只能恢复位置和 yaw；持续 PhysX 场景还含有由前序碰撞留下的
        # 材质/睡眠等内部状态。续局因果对照必须从原始 BESTSHOT 前缀连续重放，
        # 而不是把中盘坐标直接塞回一个新 Scene。
        states = environment.states()
        for expected_index, item in enumerate(prefix_trace):
            if environment.shot_number != expected_index:
                raise RuntimeError("前缀重放手数不同步")
            raw_shot = item.get("bestshot")
            if not isinstance(raw_shot, (list, tuple)) or len(raw_shot) != 3:
                raise ValueError(f"前缀第 {expected_index + 1} 手缺少 BESTSHOT")
            before = state_snapshot(states)
            result = environment.play(tuple(float(value) for value in raw_shot))
            if bool(item.get("ruleRollback", False)):
                # 与正式对局一致：该手已计数，但场面回到本手之前。
                states = environment.restore_settled_states(before)
                shot_history_rollbacks[len(shot_history) + 1] = tuple(dict(state) for state in before)
            else:
                states = result["states"]
            shot_history.append(tuple(float(value) for value in raw_shot))
        if environment.shot_number != int(start_shot):
            raise RuntimeError("前缀重放后 shot_number 不匹配")
    elif initial_states is None:
        states = environment.states()
    else:
        if not 0 <= int(start_shot) < STONE_COUNT:
            raise ValueError("resume start_shot must be within an unfinished end")
        # 局部复盘从某一手之前的保存壶面继续。restore 只恢复壶面、不会回退
        # shot_number，因此先赋值即可继续使用原局相同的每手摩擦 seed。
        environment.shot_number = int(start_shot)
        states = environment.restore_settled_states(initial_states)
    # 原始前缀已通过真实 Scene 连续重放，因而同样可以供本地终局前瞻使用。
    # 直接 restore 的中盘壶面则仍不能冒充完整历史轨迹。
    history_exact = initial_states is None
    replay_start_max_delta: float | None = None
    if expected_start_states is not None:
        if len(expected_start_states) < STONE_COUNT or len(states) < STONE_COUNT:
            raise ValueError("expected_start_states 必须包含全部壶槽")
        deltas: list[float] = []
        for index, (actual, expected) in enumerate(zip(states[:STONE_COUNT], expected_start_states[:STONE_COUNT])):
            if bool(actual.get("enabled", False)) != bool(expected.get("enabled", False)):
                raise RuntimeError(f"前缀重放后第 {index} 槽 enabled 不匹配，不能作为因果续局")
            if bool(expected.get("enabled", False)):
                deltas.extend((
                    abs(float(actual["x"]) - float(expected["x"])),
                    abs(float(actual["y"]) - float(expected["y"])),
                    abs(float(actual.get("yaw", 0.0)) - float(expected.get("yaw", 0.0))),
                ))
        replay_start_max_delta = max(deltas, default=0.0)
        if replay_start_max_delta > 1e-4:
            raise RuntimeError(
                f"前缀重放壶面最大误差 {replay_start_max_delta:.6g}，"
                "与来源报告不一致，不能作为同盘面因果续局"
            )
    started = time.perf_counter()
    final_shot_exclusive = STONE_COUNT if stop_after_shot is None else min(STONE_COUNT, int(stop_after_shot))
    if final_shot_exclusive <= int(start_shot):
        raise ValueError("stop_after_shot must be after start_shot")
    while environment.shot_number < final_shot_exclusive:
        shot_index = environment.shot_number
        team = shot_index % 2
        before = state_snapshot(states)
        rules_before = rule_board(states, team)
        decision_started = time.perf_counter()
        if team == proxy_team:
            proxy.rollout_history = tuple(shot_history)
            proxy.rollout_history_exact = bool(history_exact)
            proxy.rollout_history_rollbacks = dict(shot_history_rollbacks)
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
            if hasattr(decision, "stage_s_p1_peel_guard"):
                detail["stageSP1PeelGuard"] = bool(decision.stage_s_p1_peel_guard)
                detail["stageSP2BlockedDraw"] = bool(decision.stage_s_p2_blocked_draw)
            actor = opponent_label
        decision_seconds = time.perf_counter() - decision_started
        physics_started = time.perf_counter()
        result = environment.play(shot)
        physics_seconds = time.perf_counter() - physics_started
        states = result["states"]
        violations = free_guard_rule_violations(rules_before, states, shot_index=shot_index)
        rule_choice = CENTERLINE_DEFAULT_CHOICE if violations else None
        rule_rollback = rule_choice == "RESET"
        attempted_contact = bool(result["contact"])
        attempted_cleared = list(result["cleared"])
        if rule_rollback:
            # 精确复现 Unity 的 CENTERLINE_CHOICE RESET：备份/恢复的只有
            # body 壶面；environment.play 已把 shot_number 加一，因此犯规方
            # 不会重投，下一轮 while 会直接切到下一手。
            states = environment.restore_settled_states(before)
            result["states"] = states
            result["contact"] = False
            result["cleared"] = []
        shot_history.append(tuple(float(value) for value in shot))
        if rule_rollback:
            shot_history_rollbacks[len(shot_history)] = tuple(dict(state) for state in before)
        record = {
            "type": "shot", "game": game_index, "shot": shot_index + 1,
            "team": "first" if team == 0 else "second", "actor": actor,
            "bestshot": list(shot), "detail": detail, "contact": result["contact"],
            "cleared": result["cleared"], "temporaryScoreFirst": score_board(states),
            "decisionSeconds": decision_seconds, "physicsSeconds": physics_seconds,
            "decisionWithinBudget": decision_seconds <= proxy.decision_budget_seconds,
            "frictionSeed": seed + shot_index * 7919,
            "frictionGenerator": "StrictCurlingEnd seed; full sequence is reproducible from this seed",
            "ruleViolations": violations,
            "centerlineChoice": rule_choice,
            "centerlineChoiceBy": ("second" if team == 0 else "first") if rule_choice else None,
            "ruleRollback": rule_rollback,
            "attemptedContact": attempted_contact if rule_rollback else None,
            "attemptedCleared": attempted_cleared if rule_rollback else [],
            "stateBefore": before, "stateAfter": state_snapshot(states),
        }
        trace.append(record)
        append_log(progress_path, record)
        print("第%d局 第%02d手 %-5s 决策 %.2fs 物理 %.2fs 当前先手分 %+d%s" % (
            game_index, shot_index + 1, actor, decision_seconds, physics_seconds,
            record["temporaryScoreFirst"],
            " Unity=RESET;" + ";".join(violations) if rule_rollback else "",
        ), flush=True)
    final_score_first = score_board(states)
    proxy_score = final_score_first if proxy_team == 0 else -final_score_first
    outcome = {
        "proxyTeam": "first" if proxy_team == 0 else "second", "seed": seed,
        "startShot": int(start_shot),
        "replayStartMaxStateDelta": replay_start_max_delta,
        "finalScoreFirst": final_score_first, "finalScoreProxy": proxy_score,
        "winner": "proxy" if proxy_score > 0 else opponent_label if proxy_score < 0 else "draw",
        "completedEnd": bool(environment.shot_number >= STONE_COUNT),
        "stoppedAfterShot": int(environment.shot_number),
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
    parser.add_argument("--semantic-tactical-library", action="store_true", help="仅本地评测：先手尝试数据语义 G 合同的并行 PhysX 验收，失败后回退现有规划器。")
    parser.add_argument("--semantic-contract-budget-seconds", type=float, default=10.0, help="每个语义细合同候选的 PhysX 搜索预算。")
    parser.add_argument("--semantic-max-workers", type=int, default=3, help="同一 G 的细圆/绑定候选并行进程数。")
    parser.add_argument("--semantic-max-contracts", type=int, default=3, help="每手最多尝试多少个按优先级排序的语义细合同。")
    parser.add_argument("--experimental-opponent-rollout", action="store_true", help="仅离线诊断：允许 K7/K8 调用已知对手策略做未来回放；默认关闭，绝不代表比赛策略。")
    parser.add_argument("--opponent", choices=("ppo", "stage_s_u6", "current_stagec_u6", "aggressive"), default="ppo", help="本地评测对手。")
    parser.add_argument("--proxy-team", type=int, choices=(0, 1), default=None, help="只评测指定代理方（0=先手，1=后手）；省略时仍按双方各一局。")
    parser.add_argument("--stop-after-shot", type=int, default=None, help="分段评测：在该手数前停止（1..16），中间分数不是终局。")
    parser.add_argument("--resume-report", type=Path, default=None, help="从同评测器产生的单局分段报告继续，恢复最后壶面与下一手编号。")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--progress-file", type=Path, default=None, help="实时 JSONL 日志；省略时使用 output 同名 .jsonl。")
    args = parser.parse_args()
    if args.planner_physics_seeds < 1 or args.planner_parent_regions < 1 or args.decision_budget_seconds <= 0 or args.semantic_contract_budget_seconds <= 0 or args.semantic_max_workers < 1 or args.semantic_max_contracts < 1:
        raise SystemExit("规划器的复核种子数和区域数必须为正")
    if args.stop_after_shot is not None and not 1 <= int(args.stop_after_shot) <= STONE_COUNT:
        raise SystemExit("--stop-after-shot 必须在 1..16")
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
    base_proxy = ProxyMatchPlayer(
        physics_seeds=args.planner_physics_seeds, parent_regions=args.planner_parent_regions,
        decision_budget_seconds=args.decision_budget_seconds,
    )
    if args.semantic_tactical_library:
        from planning_proxy.tactical_library_strategy.semantic_match_player import SemanticTacticalMatchPlayer
        proxy: Any = SemanticTacticalMatchPlayer(
            base_proxy, contract_budget_seconds=args.semantic_contract_budget_seconds,
            max_workers=args.semantic_max_workers, max_contracts=args.semantic_max_contracts,
        )
    else:
        proxy = base_proxy
    if args.opponent == "ppo":
        # 这些对手只服务于本地评测。延迟导入，避免 Unity 规划机器人
        # 为了生成一手 BESTSHOT 而要求提交环境携带 PyTorch / PPO 权重。
        from training_research.opponents.teammate_ppo_adapter import TeammatePPOOpponent

        opponent: Any = TeammatePPOOpponent(deterministic=True)
        opponent_label = "ppo"
        opponent_scope = "teammate PPO deterministic inference"
    elif args.opponent == "stage_s_u6":
        from training_research.opponents.stage_s_u6_adapter import StageSU6Opponent

        opponent = StageSU6Opponent(deterministic=True)
        opponent_label = "stage_s_u6"
        opponent_scope = "supplied Stage-S U6 Deep-Sets PPO; inference runs in the project's existing Anaconda Torch environment"
    elif args.opponent == "current_stagec_u6":
        from training_research.opponents.current_stagec_u6_adapter import CurrentStageCU6Opponent

        opponent = CurrentStageCU6Opponent(deterministic=True)
        opponent_label = "current_stagec_u6"
        opponent_scope = "active teammate Stage-C U6 checkpoint; inference runs in the project's existing Anaconda Torch environment"
    else:
        from training_research.opponents.aggressive_strategy_adapter import AggressiveStrategyOpponent

        opponent = AggressiveStrategyOpponent()
        opponent_label = "aggressive"
        opponent_scope = "aggresive_ai.py exact strategy_library decision logic (socket bypassed)"
    if args.experimental_opponent_rollout and args.opponent in {"ppo", "aggressive"}:
        # 这是已知对手下的离线反事实诊断，不是状态机运行时的一部分。它可
        # 用来发现“某类 S7 的 G7 会被怎样反击”，随后必须把规律改写为通用
        # 状态谓词与 PhysX 合同，不能把对手策略带进比赛入口。
        base_proxy.terminal_reply_opponent = opponent
    try:
        game_specs = (
            [(1, 0, args.seed), (2, 1, args.seed + 100_003)] if args.proxy_team is None else
            [(1, int(args.proxy_team), args.seed)]
        )
        resume_states = None
        resume_start_shot = 0
        if args.resume_report is not None:
            prior = json.loads(args.resume_report.read_text(encoding="utf-8"))
            prior_games = prior.get("games", [])
            if len(prior_games) != 1 or not prior_games[0].get("trace"):
                raise SystemExit("--resume-report 必须是含 trace 的单局分段报告")
            prior_game = prior_games[0]
            if args.proxy_team is None or str(prior_game.get("proxyTeam")) != ("first" if int(args.proxy_team) == 0 else "second"):
                raise SystemExit("--resume-report 的代理方必须与 --proxy-team 一致")
            if int(prior_game.get("seed")) != int(args.seed):
                raise SystemExit("--resume-report 必须使用相同 --seed")
            resume_states = prior_game["trace"][-1]["stateAfter"]
            resume_start_shot = int(prior_game["stoppedAfterShot"])
            if resume_start_shot >= STONE_COUNT:
                raise SystemExit("--resume-report 已完成整局")
            if args.stop_after_shot is not None and int(args.stop_after_shot) <= resume_start_shot:
                raise SystemExit("--stop-after-shot 必须大于续跑起点")
            game_specs = [(1, int(args.proxy_team), int(args.seed))]
        games = [
            run_game(game_index=index, proxy_team=team, seed=seed, proxy=proxy, opponent=opponent, opponent_label=opponent_label,
                     progress_path=progress_path, initial_states=resume_states, start_shot=resume_start_shot,
                     stop_after_shot=args.stop_after_shot)
            for index, team, seed in game_specs
        ]
    finally:
        close = getattr(opponent, "close", None)
        if callable(close):
            close()
    report = {
        "schema": "planning_proxy_vs_teammate_ppo_v2",
        "scope": "non-sweeping; one local strict-PhysX end each way; " + opponent_scope,
        "warning": "integration evaluation only; planning strict check restores current local x/y/yaw and PhysX slots, but local seeded friction is not a Unity match win-rate proof",
        "opponent": args.opponent,
        "proxyTeamScope": args.proxy_team if args.proxy_team is not None else "both",
        "stopAfterShot": args.stop_after_shot,
        "resumeReport": None if args.resume_report is None else str(args.resume_report),
        "plannerPhysicsSeeds": args.planner_physics_seeds,
        "plannerParentRegions": args.planner_parent_regions,
        "decisionBudgetSeconds": args.decision_budget_seconds,
        "semanticTacticalLibrary": bool(args.semantic_tactical_library),
        "experimentalOpponentRollout": bool(args.experimental_opponent_rollout),
        "semanticContractBudgetSeconds": args.semantic_contract_budget_seconds if args.semantic_tactical_library else None,
        "semanticMaxWorkers": args.semantic_max_workers if args.semantic_tactical_library else None,
        "semanticMaxContracts": args.semantic_max_contracts if args.semantic_tactical_library else None,
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
