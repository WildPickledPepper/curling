#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""比赛细则中会改变单手合法性的规则检查。

依据仓库根目录 ``比赛细则.md``：第 6 次投壶之前（零基 shotIndex 为 0..4），
对方自由防守区壶不得被直接或间接送到无效位置；其中触及中线的对方守壶也
不得被撞离中线或撞离自由防守区。这里的输出用于规划器的保守过滤。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence


HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
# 本地严格模拟器采用的可比赛区域上边界，也是本比赛端的前掷线侧边界。
FRONT_HOG_Y = 10.525
FREE_GUARD_PROTECTED_LAST_SHOT_INDEX = 4
EPS = 1e-6


@dataclass(frozen=True)
class RuleBoardStone:
    index: int
    owner: str
    x: float
    y: float
    enabled: bool = True


def is_in_free_guard_zone(x: float, y: float) -> bool:
    """是否在 T 线至前掷线之间，且整颗壶不触及大本营。"""

    return (
        HOUSE_Y - EPS <= float(y) <= FRONT_HOG_Y + EPS
        and math.hypot(float(x) - HOUSE_X, float(y) - HOUSE_Y) > HOUSE_R + STONE_R + EPS
    )


def touches_centre_line(x: float) -> bool:
    """石头圆盘与 x=HOUSE_X 的中线相交或相切。"""

    return abs(float(x) - HOUSE_X) <= STONE_R + EPS


def free_guard_rule_violations(
    initial_board: Sequence[RuleBoardStone],
    final_states: Sequence[Mapping[str, object]],
    *,
    shot_index: int,
) -> list[str]:
    """返回该摩擦序列下可由对手主张恢复场面的违规原因。

    只检查细则明确给出的最终位置/是否有效条件。若比赛端额外暴露逐 tick
    规则事件，应以比赛端事件为准；当前严格 PhysX 层不伪造该裁判状态。
    """

    if not 0 <= int(shot_index) <= FREE_GUARD_PROTECTED_LAST_SHOT_INDEX:
        return []
    violations: list[str] = []
    for stone in initial_board:
        if stone.owner != "opponent" or not stone.enabled or not is_in_free_guard_zone(stone.x, stone.y):
            continue
        if stone.index >= len(final_states):
            violations.append("对方自由防守区壶 %d 的终局状态缺失" % stone.index)
            continue
        state = final_states[stone.index]
        if not bool(state.get("enabled", False)):
            violations.append("对方自由防守区壶 %d 被移至无效位置" % stone.index)
            continue
        final_x, final_y = float(state["x"]), float(state["y"])
        if touches_centre_line(stone.x):
            if not is_in_free_guard_zone(final_x, final_y):
                violations.append("对方中线自由防守区壶 %d 被撞离自由防守区" % stone.index)
            elif not touches_centre_line(final_x):
                violations.append("对方中线自由防守区壶 %d 被撞离中线" % stone.index)
    return violations
