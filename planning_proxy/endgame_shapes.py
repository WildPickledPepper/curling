#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""预设残局球形的白盒定义与局面匹配。

这不是一套“摆到固定绝对坐标就算赢”的脚本。它只回答两个问题：

1. 当前静止局面最接近哪种己方三壶结构；
2. 距离该结构还差多少，供后续的候选出手排序使用。

真正决定一手能否提交的仍是 ``strict_refine`` 中的多摩擦序列 PhysX 回放。
本模块刻意不输出 BESTSHOT，也不放宽自由防守区规则。
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


HOUSE_X = 2.375
HOUSE_Y = 4.880
INNER_RING_R = 0.610  # 课程战术库使用的大本营红圈半径
STONE_R = 0.145


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class EndgameShape:
    """三壶残局的几何目标。

    ``guard`` 是己方中线守壶的参考位置；``house_slots`` 是两颗己方红圈壶。
    目标坐标不是硬约束，允许由 ``match_shape`` 用欧氏距离连续评分。
    """

    name: str
    description: str
    guard: Point
    house_slots: tuple[Point, Point]


# 三种刻意错开的候选结构。两颗营内壶均在红圈内，彼此间距也大于两颗壶的直径。
ENDGAME_SHAPES: tuple[EndgameShape, ...] = (
    EndgameShape(
        name="中线锁门",
        description="前方中线守壶遮住直线入口；两颗红圈壶前后错开，避免一条直线带走两颗。",
        guard=Point(HOUSE_X, 7.15),
        house_slots=(Point(1.95, 4.86), Point(2.68, 4.44)),
    ),
    EndgameShape(
        name="左右分离",
        description="前方中线守壶加红圈左右双壶；对手难用一条击打线同时处理两边。",
        guard=Point(HOUSE_X, 7.15),
        house_slots=(Point(1.90, 4.80), Point(2.85, 4.95)),
    ),
    EndgameShape(
        name="斜向夹心",
        description="前方中线守壶加红圈斜对角双壶；保留一侧绕线，同时降低双清碰撞链机会。",
        guard=Point(HOUSE_X, 7.15),
        house_slots=(Point(2.12, 5.20), Point(2.70, 4.43)),
    ),
)


@dataclass(frozen=True)
class ShapeMatch:
    shape: EndgameShape
    own_indices: tuple[int, int, int] | None
    guard_error: float
    house_error: float
    opponent_inner_count: int
    score: float

    @property
    def feasible(self) -> bool:
        """是否已大致摆成目标，而非仅仅“比别的目标更像”。"""

        return (
            self.own_indices is not None
            and self.guard_error <= 0.45
            and self.house_error <= 0.80
            and self.opponent_inner_count == 0
        )


def _distance(a: Point, b: Point) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def _enabled_stones(
    states: Sequence[Mapping[str, object]], owner: str,
) -> list[tuple[int, Point]]:
    result: list[tuple[int, Point]] = []
    for index, state in enumerate(states):
        if not bool(state.get("enabled", False)) or str(state.get("owner", "")) != owner:
            continue
        result.append((index, Point(float(state["x"]), float(state["y"]))))
    return result


def match_shape(
    states: Sequence[Mapping[str, object]],
    shape: EndgameShape,
    *,
    self_owner: str = "self",
    opponent_owner: str = "opponent",
) -> ShapeMatch:
    """将一个含 ``owner`` 的静止棋盘与一种目标球形匹配。

    多余己方壶不处罚；从所有己方壶中选最适合守壶及两个红圈槽位的三颗。
    对手进入红圈会重罚，因为它直接威胁到该残局球形的计分目的。
    """

    own = _enabled_stones(states, self_owner)
    opponents = _enabled_stones(states, opponent_owner)
    opponent_inner_count = sum(
        _distance(point, Point(HOUSE_X, HOUSE_Y)) <= INNER_RING_R + STONE_R
        for _, point in opponents
    )
    if len(own) < 3:
        return ShapeMatch(shape, None, math.inf, math.inf, opponent_inner_count, -math.inf)

    best: tuple[float, tuple[int, int, int], float, float] | None = None
    for (guard_index, guard), (left_index, left), (right_index, right) in itertools.permutations(own, 3):
        guard_error = _distance(guard, shape.guard)
        direct = _distance(left, shape.house_slots[0]) + _distance(right, shape.house_slots[1])
        swapped = _distance(left, shape.house_slots[1]) + _distance(right, shape.house_slots[0])
        house_error = min(direct, swapped)
        # 守壶比单颗营内壶更关键：它决定前五手的规则保护是否仍可利用。
        error = 1.5 * guard_error + house_error
        candidate = (error, (guard_index, left_index, right_index), guard_error, house_error)
        if best is None or candidate[0] < best[0]:
            best = candidate

    assert best is not None
    _, indices, guard_error, house_error = best
    score = 100.0 - 40.0 * guard_error - 25.0 * house_error - 80.0 * opponent_inner_count
    return ShapeMatch(shape, indices, guard_error, house_error, opponent_inner_count, score)


def rank_shapes(
    states: Sequence[Mapping[str, object]],
    shapes: Iterable[EndgameShape] = ENDGAME_SHAPES,
    *,
    self_owner: str = "self",
    opponent_owner: str = "opponent",
) -> list[ShapeMatch]:
    """由最接近到最远返回所有预设球形。"""

    matches = [match_shape(states, shape, self_owner=self_owner, opponent_owner=opponent_owner) for shape in shapes]
    return sorted(matches, key=lambda item: item.score, reverse=True)
