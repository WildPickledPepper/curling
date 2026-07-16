#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""先手中线控场策略的状态机。

这个模块只定义“这一颗壶要修复什么局面”，不自己假装计算碰撞。真正的
BESTSHOT 仍由白盒粗筛和严格 PhysX 产生。这样第七、第八颗不会变成写死的
坐标，而是根据对方刚刚拆掉的层来选择目标。

``shot_index`` 是全局零基投壶序号；本模块仅接受先手方自己的偶数序号
``0, 2, ..., 14``。
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping, Sequence

from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R, is_in_free_guard_zone, touches_centre_line


INNER_RING_R = 0.610
GUARD_TARGET = (HOUSE_X, 7.15)
# 前后、左右都错开的一对红圈得分槽。镜像版本用于一侧被挡住时。
HOUSE_PAIR_LEFT = ((2.28, 4.70), (2.67, 5.18))
HOUSE_PAIR_RIGHT = ((2.47, 4.70), (2.08, 5.18))
# 第六/第七/第八颗用于保护直线入口的前方偏侧位置。
FRONT_GUARD_LEFT = (1.86, 6.18)
FRONT_GUARD_RIGHT = (2.89, 6.18)
EDGE_DEAD_LEFT = (0.195, 0.435)
EDGE_DEAD_RIGHT = (4.315, 4.555)


@dataclass(frozen=True)
class StrategyStone:
    index: int
    owner: str
    x: float
    y: float
    enabled: bool = True


@dataclass(frozen=True)
class FirstPlayerPlan:
    """一颗先手壶的战术目标。

    ``target_opponent_index`` 是需要重点处理的对方壶；它不是一律要求物理
    出界：前五次投壶中的普通自由防守区守壶只能被推到边缘废球带。
    """

    shot_index: int
    own_throw_number: int
    phase: str
    target_points: tuple[tuple[float, float], ...]
    target_opponent_index: int | None
    opponent_action: str
    rationale: str

    def to_json(self) -> dict:
        result = asdict(self)
        result["target_points"] = [list(point) for point in self.target_points]
        return result

    @classmethod
    def from_json(cls, raw: Mapping[str, object]) -> "FirstPlayerPlan":
        points = tuple((float(point[0]), float(point[1])) for point in raw.get("target_points", []) if isinstance(point, (list, tuple)) and len(point) == 2)
        return cls(
            shot_index=int(raw["shot_index"]),
            own_throw_number=int(raw["own_throw_number"]),
            phase=str(raw["phase"]),
            target_points=points,
            target_opponent_index=None if raw.get("target_opponent_index") is None else int(raw["target_opponent_index"]),
            opponent_action=str(raw["opponent_action"]),
            rationale=str(raw["rationale"]),
        )


def _as_stones(board: Iterable[object]) -> list[StrategyStone]:
    result: list[StrategyStone] = []
    for item in board:
        if isinstance(item, Mapping):
            result.append(StrategyStone(int(item["index"]), str(item["owner"]), float(item["x"]), float(item["y"]), bool(item.get("enabled", True))))
        else:
            result.append(StrategyStone(int(getattr(item, "index")), str(getattr(item, "owner")), float(getattr(item, "x")), float(getattr(item, "y")), bool(getattr(item, "enabled", True))))
    return [stone for stone in result if stone.enabled]


def distance_to_house(stone: StrategyStone) -> float:
    return math.hypot(stone.x - HOUSE_X, stone.y - HOUSE_Y)


def is_in_inner_ring(stone: StrategyStone) -> bool:
    return distance_to_house(stone) <= INNER_RING_R + STONE_R


def is_in_house(stone: StrategyStone) -> bool:
    return distance_to_house(stone) <= HOUSE_R + STONE_R


def is_edge_dead(stone: StrategyStone) -> bool:
    return (EDGE_DEAD_LEFT[0] <= stone.x <= EDGE_DEAD_LEFT[1]) or (EDGE_DEAD_RIGHT[0] <= stone.x <= EDGE_DEAD_RIGHT[1])


def _target_pair(stones: Sequence[StrategyStone]) -> tuple[tuple[float, float], tuple[float, float]]:
    """根据当前障碍选择左右镜像红圈布局。"""

    left_pressure = sum(1 for stone in stones if stone.owner == "opponent" and stone.x < HOUSE_X and not is_edge_dead(stone))
    right_pressure = sum(1 for stone in stones if stone.owner == "opponent" and stone.x > HOUSE_X and not is_edge_dead(stone))
    return HOUSE_PAIR_RIGHT if left_pressure > right_pressure else HOUSE_PAIR_LEFT


def _front_guard_target(stones: Sequence[StrategyStone]) -> tuple[float, float]:
    """保护壶落在与主要得分壶相反的一侧，避免三个己方壶排成一线。"""

    own_house = [stone for stone in stones if stone.owner == "self" and is_in_inner_ring(stone)]
    if own_house:
        mean_x = sum(stone.x for stone in own_house) / len(own_house)
        return FRONT_GUARD_RIGHT if mean_x <= HOUSE_X else FRONT_GUARD_LEFT
    return FRONT_GUARD_LEFT


def _priority_opponent(stones: Sequence[StrategyStone]) -> StrategyStone | None:
    """先处理红圈/大本营威胁；边缘废球不是当前主要目标。"""

    enemies = [stone for stone in stones if stone.owner == "opponent" and not is_edge_dead(stone)]
    if not enemies:
        return None
    return min(
        enemies,
        key=lambda stone: (
            0 if is_in_inner_ring(stone) else 1 if is_in_house(stone) else 2 if is_in_free_guard_zone(stone.x, stone.y) else 3,
            distance_to_house(stone),
        ),
    )


def _opponent_action(target: StrategyStone | None, shot_index: int) -> str:
    if target is None:
        return "none"
    if shot_index <= 4 and is_in_free_guard_zone(target.x, target.y):
        # 中线守壶在保护期内不能被撞离中线；普通守壶可被推到边缘，但不能出界。
        return "avoid_protected_centre_guard" if touches_centre_line(target.x) else "push_to_edge_dead"
    return "physical_clear"


def _has_front_guard(stones: Sequence[StrategyStone]) -> bool:
    return any(
        stone.owner == "self"
        and abs(stone.y - GUARD_TARGET[1]) <= 1.25
        and abs(stone.x - HOUSE_X) >= 0.20
        for stone in stones
    )


def _own_inner_count(stones: Sequence[StrategyStone]) -> int:
    return sum(1 for stone in stones if stone.owner == "self" and is_in_inner_ring(stone))


def _self_is_closest(stones: Sequence[StrategyStone]) -> bool:
    in_house = [stone for stone in stones if is_in_house(stone)]
    return bool(in_house) and min(in_house, key=distance_to_house).owner == "self"


def plan_first_player_turn(board: Iterable[object], shot_index: int) -> FirstPlayerPlan:
    """为先手方的下一颗壶生成可执行的战术意图。

    它处理的是“该补什么层”，不是直接输出物理输入。调用端将
    ``target_points`` 和 ``target_opponent_index`` 交给粗筛/严格 PhysX。
    """

    if not 0 <= int(shot_index) <= 14 or int(shot_index) % 2:
        raise ValueError("先手策略只接受我方的偶数全局投壶序号 0,2,...,14")
    stones = _as_stones(board)
    own_throw = int(shot_index) // 2 + 1
    target = _priority_opponent(stones)
    opponent_action = _opponent_action(target, int(shot_index))
    pair = _target_pair(stones)

    if own_throw == 1:
        return FirstPlayerPlan(int(shot_index), own_throw, "open_centre_guard", (GUARD_TARGET,), None, "none", "第一颗占中线守壶；之后的保护规则才有可利用的支点。")

    if own_throw == 2:
        target_point = pair[0]
        if opponent_action == "physical_clear":
            text = "对方第一颗已进大本营：优先物理清出，同时让出手壶尽量滚入第一红圈槽。"
        elif opponent_action == "push_to_edge_dead":
            text = "对方第一颗是受保护的普通自由防守区守壶：推入边缘废球带，不可打出界；出手壶争取第一红圈槽。"
        else:
            text = "对方中线守壶仍受保护，避免把它撞离中线；直接建立第一红圈得分壶。"
        return FirstPlayerPlan(int(shot_index), own_throw, "process_first_enemy_and_score", (target_point,), None if opponent_action == "avoid_protected_centre_guard" else (target.index if target else None), opponent_action, text)

    if own_throw == 3:
        return FirstPlayerPlan(int(shot_index), own_throw, "complete_staggered_house_pair", (pair[1],), target.index if target and opponent_action != "avoid_protected_centre_guard" else None, opponent_action, "保护期的最后一颗：优先补第二红圈壶，并与第一颗前后、左右错开；只有明显敌方得分威胁才顺带处理。")

    if own_throw in (4, 5):
        if target is not None and is_in_inner_ring(target):
            return FirstPlayerPlan(int(shot_index), own_throw, "reclaim_centre_or_clear_threat", (pair[0], pair[1]), target.index, "physical_clear", "对方已占红圈：能稳定清出则清出；否则先投得比它更靠中心。")
        if _own_inner_count(stones) < 2:
            return FirstPlayerPlan(int(shot_index), own_throw, "restore_second_scoring_stone", (pair[1],), None, "none", "己方红圈壶不足两颗，补另一侧得分层，不把壶堆在同一条直线上。")
        return FirstPlayerPlan(int(shot_index), own_throw, "maintain_centre_advantage", (pair[0],), None, "none", "当前中心层仍完整；用更靠中心或轻微错层的壶维持优势。")

    if own_throw == 6:
        return FirstPlayerPlan(int(shot_index), own_throw, "sixth_hit_and_roll_defence", (_front_guard_target(stones),), target.index if target else None, "physical_clear" if target else "none", "第六颗先处理对方第五颗，再让出手壶滚到前方偏侧保护位，形成防御三角。")

    # 第七、第八颗：不贪清场，而是按“最近壶、第二红圈壶、前方保护壶”的顺序修复。
    if not _self_is_closest(stones):
        return FirstPlayerPlan(int(shot_index), own_throw, "repair_closest_scoring_anchor", (pair[0],), target.index if target and is_in_inner_ring(target) else None, "physical_clear" if target and is_in_inner_ring(target) else "none", "对方已抢到最近壶；先重新取得最近壶，不能为了清无关壶放弃计分锚点。")
    if _own_inner_count(stones) < 2:
        return FirstPlayerPlan(int(shot_index), own_throw, "repair_second_inner_stone", (pair[1],), None, "none", "最近壶仍在，但第二红圈层被拆；在另一侧补回，避免一杆连锁双清。")
    if not _has_front_guard(stones):
        return FirstPlayerPlan(int(shot_index), own_throw, "repair_front_protector", (_front_guard_target(stones),), None, "none", "两颗得分壶仍在，但前方保护层缺失；优先堵住对方最后的直线击打。")
    return FirstPlayerPlan(int(shot_index), own_throw, "reinforce_final_defence", (_front_guard_target(stones),), target.index if target and is_in_inner_ring(target) else None, "physical_clear" if target and is_in_inner_ring(target) else "none", "三层仍完整；第八颗只加固最容易被直线击打的一侧，不为边缘废球浪费机会。")


def tactical_coarse_score(stop_x: float, stop_y: float, first_hit_index: int, base_score: float, plan: FirstPlayerPlan) -> float:
    """给粗筛的轻量加分；严格 PhysX 仍负责真正的碰撞与终局排序。"""

    score = float(base_score)
    if plan.target_opponent_index is not None and int(first_hit_index) == plan.target_opponent_index:
        score += 250.0
    if plan.target_points:
        landing_error = min(math.hypot(stop_x - x, stop_y - y) for x, y in plan.target_points)
        score -= 45.0 * landing_error
    return score


def score_strict_outcome(
    final_states: Sequence[Mapping[str, object]],
    initial_board: Iterable[object],
    active_index: int,
    plan: FirstPlayerPlan,
) -> tuple[float, bool]:
    """给严格 PhysX 终局打先手战术分。

    分数只用于在已经合法、满足同一己方损失档的候选之间排序；它不放宽
    ``strict_refine`` 的自由防守区和出界安全约束。返回的布尔值是本轮主要
    目标是否在该摩擦序列下实现，供多种子取最差值。
    """

    initial = _as_stones(initial_board)
    owners = {stone.index: stone.owner for stone in initial}
    owners[int(active_index)] = "self"
    final: list[StrategyStone] = []
    for index, state in enumerate(final_states):
        if bool(state.get("enabled", False)):
            final.append(StrategyStone(index, owners.get(index, "unknown"), float(state["x"]), float(state["y"])))

    own = [stone for stone in final if stone.owner == "self"]
    enemy = [stone for stone in final if stone.owner == "opponent"]
    own_inner = sum(is_in_inner_ring(stone) for stone in own)
    own_closest = bool(own) and (not enemy or min(own + enemy, key=distance_to_house).owner == "self")
    guard_present = _has_front_guard(final)
    active = next((stone for stone in final if stone.index == int(active_index)), None)
    landing_error = math.inf if active is None or not plan.target_points else min(
        math.hypot(active.x - point[0], active.y - point[1]) for point in plan.target_points
    )

    target_ok = True
    if plan.target_opponent_index is not None:
        target = next((stone for stone in final if stone.index == plan.target_opponent_index), None)
        if plan.opponent_action == "physical_clear":
            target_ok = target is None
        elif plan.opponent_action == "push_to_edge_dead":
            target_ok = target is not None and is_edge_dead(target)

    landing_ok = not plan.target_points or (active is not None and landing_error <= 0.70)
    if plan.phase == "open_centre_guard":
        goal_met = landing_ok
    elif plan.phase in {"process_first_enemy_and_score", "sixth_hit_and_roll_defence"}:
        goal_met = target_ok and landing_ok
    elif plan.phase in {"repair_closest_scoring_anchor", "reclaim_centre_or_clear_threat"}:
        goal_met = own_closest and landing_ok
    elif plan.phase in {"repair_second_inner_stone", "restore_second_scoring_stone", "complete_staggered_house_pair"}:
        goal_met = own_inner >= 2 and landing_ok
    elif plan.phase in {"repair_front_protector", "reinforce_final_defence"}:
        goal_met = own_closest and own_inner >= 2 and guard_present and landing_ok
    else:
        goal_met = landing_ok

    score = 0.0
    score += 240.0 if target_ok else -240.0
    score += 120.0 if own_closest else -120.0
    score += 55.0 * min(2, own_inner)
    score += 45.0 if guard_present else 0.0
    if math.isfinite(landing_error):
        score -= 70.0 * landing_error
    else:
        score -= 200.0
    return score, bool(goal_met)
