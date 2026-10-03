#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把战术库意图展开为少量、可解释的候选目标区域。

此模块位于“离散战术”与“连续 PhysX”之间：它不计算出手路径、不验证碰撞，
只给后续搜索器一组小而明确的目标。

候选分两类：

* ``STOP_REGION``：本次出手壶最终应停入的圆形区域；
* ``STONE_CONTACT``：应首先接触的现有壶附近的瞄准圆区。它不是承诺撞击后
  的停点，PhysX 仍须决定入射角、速度、旋转和最终滚位。
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Iterable, Mapping

from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R
from planning_proxy.tactical_library_strategy.strategy import (
    TacticalLibraryPlan,
    plan_first_player_from_tactical_library,
)


# 这些是“区域中心”，并非固定必达坐标。两侧红圈层故意前后错开，避免将
# 己方壶排成一条直接 double 的线；外翼 draw 给中线壳留下绕行空间。
HOUSE_LAYER_SLOTS: tuple[tuple[str, float, float], ...] = (
    ("left_front_house_layer", HOUSE_X - 0.42, HOUSE_Y + 0.30),
    ("right_back_house_layer", HOUSE_X + 0.42, HOUSE_Y - 0.30),
    ("right_front_house_layer", HOUSE_X + 0.42, HOUSE_Y + 0.30),
    ("left_back_house_layer", HOUSE_X - 0.42, HOUSE_Y - 0.30),
)
WING_DRAW_SLOTS: tuple[tuple[str, float, float], ...] = (
    ("left_wing_draw", HOUSE_X - 1.05, HOUSE_Y + 0.22),
    ("right_wing_draw", HOUSE_X + 1.05, HOUSE_Y + 0.22),
)
FRONT_GUARD_SLOTS: tuple[tuple[str, float, float], ...] = (
    ("left_front_guard", HOUSE_X - 0.52, HOUSE_Y + 1.30),
    ("right_front_guard", HOUSE_X + 0.52, HOUSE_Y + 1.30),
)
STOP_REGION_RADIUS_M = 0.24
CONTACT_REGION_RADIUS_M = 0.07
MIN_FREE_CENTRE_DISTANCE_M = 2.0 * STONE_R + 0.04


@dataclass(frozen=True)
class CandidateTargetRegion:
    """一条供后续粗代理/PhysX 尝试的候选目标。

    ``centre`` 对 ``STONE_CONTACT`` 是入射瞄准区域，而非静止壶应停的位置。
    """

    region_id: str
    target_kind: str
    centre: tuple[float, float]
    radius_m: float
    tactical_role: str
    intended_intent: str
    target_stone_index: int | None = None
    acceptance_hint: str = ""

    def to_json(self) -> dict:
        result = asdict(self)
        result["centre"] = list(self.centre)
        return result


@dataclass(frozen=True)
class TacticalTargetRegionPlan:
    """一份战术计划及其几何候选区域。"""

    tactical_plan: TacticalLibraryPlan
    regions: tuple[CandidateTargetRegion, ...]

    def to_json(self) -> dict:
        return {
            "tactical_plan": self.tactical_plan.to_json(),
            "candidate_target_regions": [region.to_json() for region in self.regions],
            "warning": "区域仅是离散目标；必须先过本地规则，再由 PhysX 验证可达性、终局与反击。",
        }


def _stones(board: Iterable[object]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for item in board:
        if isinstance(item, Mapping):
            get = item.get
        else:
            get = lambda name, default=None: getattr(item, name, default)
        if not bool(get("enabled", True)):
            continue
        result.append({
            "index": int(get("index")),
            "owner": str(get("owner")),
            "x": float(get("x")),
            "y": float(get("y")),
        })
    return result


def _is_free_stop_centre(x: float, y: float, stones: list[dict[str, object]]) -> bool:
    """排除明显与静止壶重叠的落位区中心；不代替路径可达性检查。"""

    return all(math.hypot(x - float(stone["x"]), y - float(stone["y"])) >= MIN_FREE_CENTRE_DISTANCE_M for stone in stones)


def _stop_regions(
    slots: tuple[tuple[str, float, float], ...],
    stones: list[dict[str, object]],
    *,
    role: str,
    intent: str,
) -> list[CandidateTargetRegion]:
    return [
        CandidateTargetRegion(
            region_id=name,
            target_kind="STOP_REGION",
            centre=(x, y),
            radius_m=STOP_REGION_RADIUS_M,
            tactical_role=role,
            intended_intent=intent,
            acceptance_hint="出手壶终局停入该圆区，且不得与现有静止壶重叠。",
        )
        for name, x, y in slots
        if _is_free_stop_centre(x, y, stones)
    ]


def _contact_regions(
    target: dict[str, object],
    *,
    include_rolls: bool,
    intended_intent: str,
    role: str,
) -> list[CandidateTargetRegion]:
    """为指定目标壶生成正撞和左右薄撞瞄准区。

    本地赛道的出手方向从大 y 朝小 y；故 ``front`` 位于目标壶的 +y 侧。
    左右薄撞只定义接触位置的几何类别，不预断 roll 的精确终点。
    """

    x, y, index = float(target["x"]), float(target["y"]), int(target["index"])
    result = [
        CandidateTargetRegion(
            region_id=f"stone_{index}_front_contact",
            target_kind="STONE_CONTACT",
            centre=(x, y + STONE_R),
            radius_m=CONTACT_REGION_RADIUS_M,
            tactical_role=role,
            intended_intent=intended_intent,
            target_stone_index=index,
            acceptance_hint="优先首撞该壶；严格层再验证能否中立化目标且不超己方损失预算。",
        )
    ]
    if include_rolls:
        for side, dx in (("left", -0.10), ("right", 0.10)):
            result.append(CandidateTargetRegion(
                region_id=f"stone_{index}_{side}_thin_contact",
                target_kind="STONE_CONTACT",
                centre=(x + dx, y + 0.10),
                radius_m=CONTACT_REGION_RADIUS_M,
                tactical_role=f"{role}_{side}_roll",
                intended_intent="HIT_AND_ROLL",
                target_stone_index=index,
                acceptance_hint="薄撞滚位候选；必须由 PhysX 验证出手壶终局和目标壶状态。",
            ))
    return result


def _target_stone(stones: list[dict[str, object]], target_index: int | None) -> dict[str, object] | None:
    return next((stone for stone in stones if int(stone["index"]) == target_index), None)


def candidate_target_regions(
    board: Iterable[object],
    own_throw_number: int,
) -> TacticalTargetRegionPlan:
    """根据战术库计划生成候选落位/撞击目标区域。

    该函数的输出刻意控制在 2--8 个区域，避免把连续空间离散得过细。若所有
    标准落位区均被占据，仍保留撞击区或返回空列表，交给上层标记
    ``SEARCH_REQUIRED``，而不是擅自塞进重叠坐标。
    """

    stones = _stones(board)
    plan = plan_first_player_from_tactical_library(stones, own_throw_number)
    target = _target_stone(stones, plan.target_opponent_index)
    regions: list[CandidateTargetRegion] = []

    # 保护期的规则约束覆盖一般战术意图。中线守壶只给绕守壶/两翼落位；普通
    # 侧守壶可给“推到边缘”的接触区，但最终是否合法仍由规则层裁定。
    if plan.primary_intent == "DRAW_AROUND_PROTECTED_CENTRE_GUARD":
        regions.extend(_stop_regions(HOUSE_LAYER_SLOTS + WING_DRAW_SLOTS, stones, role="绕开受保护中线守壶建层", intent="DRAW"))
    elif plan.primary_intent == "PUSH_SIDE_GUARD_TO_EDGE_DEAD_OR_DRAW_AROUND":
        if target is not None:
            regions.extend(_contact_regions(target, include_rolls=False, intended_intent="PUSH_TO_EDGE_DEAD", role="推普通FGZ侧守壶"))
        regions.extend(_stop_regions(WING_DRAW_SLOTS + HOUSE_LAYER_SLOTS[:2], stones, role="绕开普通FGZ侧守壶", intent="DRAW"))
    elif plan.primary_intent in {"BUILD_OWN_HOUSE_LAYER", "PRESERVE_OR_THICKEN_OWN_CONTROL"}:
        regions.extend(_stop_regions(HOUSE_LAYER_SLOTS, stones, role="己方营内得分层", intent="DRAW"))
        regions.extend(_stop_regions(FRONT_GUARD_SLOTS, stones, role="前场压力壶", intent="GUARD"))
        if target is not None:
            regions.extend(_contact_regions(target, include_rolls=True, intended_intent="TAKEOUT", role="选择性处理营内威胁"))
    elif plan.primary_intent == "CHANGE_OPPONENT_SCORING_STONE":
        if target is not None:
            regions.extend(_contact_regions(target, include_rolls=True, intended_intent="TAKEOUT", role="改变对方最近营内占分"))
        regions.extend(_stop_regions(WING_DRAW_SLOTS, stones, role="穿门反超候选", intent="DRAW_THROUGH_PORT"))
    elif plan.primary_intent in {"COMPARE_SHELL_ROUTES", "PHYSX_COMPARE_WING_ROLL_RAISE"}:
        regions.extend(_stop_regions(WING_DRAW_SLOTS, stones, role="两翼绕壳", intent="WING_DRAW"))
        if target is not None:
            regions.extend(_contact_regions(target, include_rolls=True, intended_intent="CLEARING", role="壳内/营内处理候选"))
    elif plan.primary_intent == "COMPARE_CROWDED_HOUSE_ROUTES":
        if target is not None:
            regions.extend(_contact_regions(target, include_rolls=True, intended_intent="TAKEOUT", role="拥挤营内首要威胁"))
        regions.extend(_stop_regions(HOUSE_LAYER_SLOTS, stones, role="拥挤营内保己方层", intent="DRAW"))
    else:  # LOW_SUPPORT 与混合局面：有限、对称的保层/两翼候选。
        regions.extend(_stop_regions(HOUSE_LAYER_SLOTS + WING_DRAW_SLOTS + FRONT_GUARD_SLOTS, stones, role="搜索用压力/保层候选", intent="SEARCH_REQUIRED"))
        if target is not None:
            regions.extend(_contact_regions(target, include_rolls=True, intended_intent="TAKEOUT", role="搜索用威胁处理候选"))

    # 同一 region_id 不重复；上游按 role/intended_intent 选少数父区域，不应
    # 将这里的全部候选都无差别交给昂贵的严格搜索。
    unique = {region.region_id: region for region in regions}
    return TacticalTargetRegionPlan(plan, tuple(unique.values()))
