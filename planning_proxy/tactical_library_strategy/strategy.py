#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""独立的先手战术库策略层。

这个模块**不替换** ``first_player_strategy.py``，也不输出 ``v/h/w``。它把
当前壶面压成宏观状态后，输出一条可交给粗代理和严格 PhysX 的离散指令：

``状态 -> 本手目标 -> 候选战术意图 -> 希望的后继状态 -> 验收门``。

其中的历史候选来自 NWNHT 的双标签筛选（整场胜利关联 + 本局得分差），但
观察数据不能证明因果。因此中线壳、拥挤营内、低支持状态只会输出
``PHYSX_SEARCH_REQUIRED``，绝不会伪造固定撞击路线或“安全终局”。
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping

from planning_proxy.competition_rules import (
    HOUSE_R,
    HOUSE_X,
    HOUSE_Y,
    STONE_R,
    is_in_free_guard_zone,
    touches_centre_line,
)
from planning_proxy.first_player_macro_state import FirstPlayerMacroState, classify_first_player_macro_state


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_ARTIFACT = (
    PROJECT_ROOT
    / "training_data"
    / "nwnht_curling"
    / "artifacts"
    / "nwnht_first_player_candidate_policy_v2_game_and_end.json"
)

# 打包运行时不携带训练数据工件时的最小可用回退。它只含通过双标签门槛的
# 候选，不把 33 个无候选状态硬凑成历史策略。
FALLBACK_HISTORICAL_INTENTS: dict[str, tuple[str, ...]] = {
    "FIRST_K1_EMPTY": ("DRAW",),
    "FIRST_K2_OWN_HOUSE_CONTROL": ("DRAW", "TAKEOUT"),
    "FIRST_K3_OWN_CENTRE_SHELL": ("CLEARING",),
    "FIRST_K4_CROWDED_HOUSE_SEARCH_REQUIRED": ("CLEARING", "TAKEOUT"),
    "FIRST_K4_OWN_CENTRE_SHELL": ("CLEARING",),
    "FIRST_K6_CROWDED_HOUSE_SEARCH_REQUIRED": ("CLEARING",),
    "FIRST_K7_CROWDED_HOUSE_SEARCH_REQUIRED": ("GUARD",),
    "FIRST_K8_CROWDED_HOUSE_SEARCH_REQUIRED": ("GUARD", "CLEARING"),
    "FIRST_K8_OWN_CENTRE_SHELL": ("GUARD",),
    "FIRST_K8_OPPONENT_HOUSE_THREAT": ("CLEARING",),
}

# 在胜局记录里出现过、却会把局面留在同一或更差状态的动作。它们不能作
# 默认主策略；仍可由 PhysX 在明确比较其他路线后作为一个处理候选。
ANTI_DEFAULT_CLEAR: frozenset[str] = frozenset({
    "FIRST_K3_OPPONENT_CENTRE_SHELL",
    "FIRST_K6_GUARD_EXCHANGE",
    "FIRST_K7_GUARD_EXCHANGE",
    "FIRST_K7_OPPONENT_HOUSE_THREAT",
})


@dataclass(frozen=True)
class TacticalLibraryPlan:
    """战术库输出；连续规划器只能把它当约束，不能当已验证出手。"""

    own_throw_number: int
    state_id: str
    raw_macro_state: str
    policy_status: str
    current_goal: str
    desired_next_state: str
    primary_intent: str
    alternative_intents: tuple[str, ...]
    target_opponent_index: int | None
    rule_constraint: str
    require_strict_physx: bool
    require_last_reply_search: bool
    historical_candidate_intents: tuple[str, ...]
    rationale: str

    def to_json(self) -> dict:
        result = asdict(self)
        result["alternative_intents"] = list(self.alternative_intents)
        result["historical_candidate_intents"] = list(self.historical_candidate_intents)
        return result


def _stones(board: Iterable[object]) -> list[dict[str, object]]:
    """接受 Mapping 或现有策略模块的 stone 对象，统一为最小字典。"""

    result: list[dict[str, object]] = []
    for item in board:
        if isinstance(item, Mapping):
            raw = item
            get = raw.get
        else:
            get = lambda name, default=None: getattr(item, name, default)
        if not bool(get("enabled", True)):
            continue
        result.append({
            "index": int(get("index")),
            "owner": str(get("owner")),
            "x": float(get("x")),
            "y": float(get("y")),
            "enabled": True,
        })
    return result


def _historical_intents(state_id: str) -> tuple[str, ...]:
    """读取本地统计工件；部署包中没有工件时使用版本化内置表。"""

    try:
        raw = json.loads(POLICY_ARTIFACT.read_text(encoding="utf-8"))
        for row in raw.get("policy_states", []):
            if row.get("state_id") == state_id:
                return tuple(
                    str(candidate["observed_action_intent"])
                    for candidate in row.get("candidate_action_intents", [])
                    if candidate.get("eligible_win_associated_candidate")
                )
    except (OSError, ValueError, TypeError, KeyError):
        # 战术库仍可独立打包执行；工件缺失不应让比赛端崩溃。
        pass
    return FALLBACK_HISTORICAL_INTENTS.get(state_id, ())


def _closest_opponent_in_house(stones: list[dict[str, object]]) -> dict[str, object] | None:
    opponents = [stone for stone in stones if stone["owner"] == "opponent"]
    inside = [
        stone for stone in opponents
        if math.hypot(float(stone["x"]) - HOUSE_X, float(stone["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R
    ]
    return min(
        inside,
        key=lambda stone: math.hypot(float(stone["x"]) - HOUSE_X, float(stone["y"]) - HOUSE_Y),
        default=None,
    )


def _rule_relevant_opponent(
    stones: list[dict[str, object]],
    scoring_target: dict[str, object] | None,
) -> dict[str, object] | None:
    """规则检查优先看营内威胁；若没有，再看任一自由防守区守壶。"""

    if scoring_target is not None:
        return scoring_target
    guards = [
        stone for stone in stones
        if stone["owner"] == "opponent" and is_in_free_guard_zone(float(stone["x"]), float(stone["y"]))
    ]
    return min(
        guards,
        key=lambda stone: (abs(float(stone["x"]) - HOUSE_X), float(stone["y"])),
        default=None,
    )


def _protected_guard_constraint(
    own_throw_number: int,
    target: dict[str, object] | None,
) -> tuple[str, str | None, int | None]:
    """返回规则说明、必要时的强制主意图和可指定目标。

    本地保护期按全局第 1--5 手，即先手 K1--K3。中线守壶不能离中线；普通
    自由防守区守壶不能出界，允许被推去边缘废球带。
    """

    if own_throw_number > 3 or target is None:
        return "FGZ_NOT_ACTIVE_OR_NO_TARGET", None, None if target is None else int(target["index"])
    x, y = float(target["x"]), float(target["y"])
    if not is_in_free_guard_zone(x, y):
        return "FGZ_ACTIVE_TARGET_NOT_GUARD", None, int(target["index"])
    if touches_centre_line(x):
        return (
            "FGZ_ACTIVE_CENTRE_GUARD_MUST_REMAIN_ON_CENTRE_LINE_AND_IN_FGZ",
            "DRAW_AROUND_PROTECTED_CENTRE_GUARD",
            None,
        )
    return (
        "FGZ_ACTIVE_SIDE_GUARD_MUST_NOT_LEAVE_PLAY",
        "PUSH_SIDE_GUARD_TO_EDGE_DEAD_OR_DRAW_AROUND",
        int(target["index"]),
    )


def _next_state(own_throw_number: int, raw_macro_state: str) -> str:
    if own_throw_number >= 8:
        return "TERMINAL_REPLY_SEARCH_REQUIRED"
    return f"FIRST_K{own_throw_number + 1}_{raw_macro_state}"


def plan_first_player_from_tactical_library(board: Iterable[object], own_throw_number: int) -> TacticalLibraryPlan:
    """从当前静止壶面给出一条独立的先手战术库指令。

    ``own_throw_number`` 是先手自己的 K1..K8，不接受全局 shot index，以免
    与旧策略模块的接口混淆。
    """

    if not 1 <= int(own_throw_number) <= 8:
        raise ValueError("own_throw_number must be in 1..8")
    stones = _stones(board)
    state: FirstPlayerMacroState = classify_first_player_macro_state(int(own_throw_number), stones)
    historical = _historical_intents(state.state_id)
    target = _closest_opponent_in_house(stones)
    rule_target = _rule_relevant_opponent(stones, target)
    rule_constraint, forced_intent, guarded_target_index = _protected_guard_constraint(int(own_throw_number), rule_target)
    target_index = None if target is None else int(target["index"])

    # 规则的强制限制先于任何统计或人类战术。尤其不能把“有清壶历史样本”
    # 解读为可以在保护期把对方守壶打出界。
    if forced_intent is not None:
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, state.raw_macro_state,
            "RULE_CONSTRAINED_PHYSX_SEARCH",
            "在不触犯本地自由防守区规则的前提下建立己方得分层或压力壶。",
            _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
            forced_intent,
            ("DRAW_TO_OWN_HOUSE_LAYER", "WING_DRAW"),
            guarded_target_index, rule_constraint, True, int(own_throw_number) == 8,
            historical,
            "规则优先：中线守壶不可离中线；普通自由防守区守壶不可被打出界。",
        )

    raw = state.raw_macro_state
    if state.macro_state == "LOW_SUPPORT_SEARCH_REQUIRED":
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, raw, "LOW_SUPPORT_SEARCH_REQUIRED",
            "不复用少样本叫球；先保留己方可计分层并避免送出直接入口。",
            _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
            "SEARCH_REQUIRED",
            ("DRAW", "WING_DRAW", "HIT_AND_ROLL", "TAKEOUT"),
            target_index, rule_constraint, True, int(own_throw_number) == 8, historical,
            "该 K 与该壶形的样本不足；由 PhysX 比较合法可达终局，不能将历史频率硬编码。",
        )

    if state.state_id in ANTI_DEFAULT_CLEAR:
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, raw, "ANTI_DEFAULT_CLEAR",
            "不把交换局面或受保护壳误写成默认清场；寻找可保层、两翼或滚位的处理。",
            _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
            "PHYSX_COMPARE_WING_ROLL_RAISE",
            ("WING_DRAW", "HIT_AND_ROLL", "RAISE", "PROMOTE", "CLEARING"),
            target_index, rule_constraint, True, int(own_throw_number) == 8, historical,
            "统计反证显示默认 CLEARING 常把后继留在对方营内威胁或中线壳；清壶只能作为比较候选。",
        )

    if raw == "EMPTY":
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, raw, "DATA_SUPPORTED_CANDIDATE",
            "建立首个可继续施压的己方层，而非把空场当作清场局面。",
            _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
            "BUILD_OWN_HOUSE_LAYER",
            ("DRAW", "FRONT_GUARD"), None, rule_constraint, True, int(own_throw_number) == 8, historical,
            "历史候选叫球为 DRAW；具体是营内壶还是前场压力壶，应以本地 PhysX 的后继壶形验收，不把人类叫球名当坐标。",
        )

    if raw == "OWN_HOUSE_CONTROL":
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, raw, "DATA_SUPPORTED_OR_PHYSX_SEARCH",
            "维持己方最近营内壶，并加厚得分层或提高直线处理难度。",
            _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
            "PRESERVE_OR_THICKEN_OWN_CONTROL",
            ("DRAW", "TAKEOUT", "HIT_AND_ROLL"), target_index, rule_constraint, True, int(own_throw_number) == 8, historical,
            "若对方没有直接改变最近壶的威胁，优先保层；若有威胁，才让 PhysX 比较 takeout 与 hit-and-roll。",
        )

    if raw == "OPPONENT_HOUSE_THREAT":
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, raw, "PHYSX_SEARCH_REQUIRED",
            "先改变对方当前最近营内壶占分这一几何事实，而不是见壶就高速清。",
            _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
            "CHANGE_OPPONENT_SCORING_STONE",
            ("TAKEOUT", "HIT_AND_ROLL", "RAISE", "DRAW_THROUGH_PORT"), target_index,
            rule_constraint, True, int(own_throw_number) == 8, historical,
            "目标是对方最近营内壶；严格 PhysX 必须比较清出、滚位、raise 与穿门 draw 的终局和己方损失。",
        )

    if raw in {"OPPONENT_CENTRE_SHELL", "OWN_CENTRE_SHELL"}:
        goal = "打破对方中线壳并重新取得入口。" if raw.startswith("OPPONENT") else "保住己方营内层，同时避免把中线壳误当无敌盾。"
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, raw, "PHYSX_SEARCH_REQUIRED",
            goal, _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
            "COMPARE_SHELL_ROUTES",
            ("WING_DRAW", "HIT_AND_ROLL", "RAISE", "PROMOTE", "CLEARING"), target_index,
            rule_constraint, True, int(own_throw_number) == 8, historical,
            "中线壳必须比较两翼、soft hit-and-roll、raise/promote 与清守壶；不承诺单条直线清壶可行。",
        )

    if raw == "CROWDED_HOUSE_SEARCH_REQUIRED":
        return TacticalLibraryPlan(
            int(own_throw_number), state.state_id, raw, "PHYSX_SEARCH_REQUIRED",
            "在拥挤营内削弱对方得分层、保留己方层，并提高对方下一手反击难度。",
            _next_state(int(own_throw_number), "CROWDED_HOUSE_SEARCH_REQUIRED"),
            "COMPARE_CROWDED_HOUSE_ROUTES",
            ("TAKEOUT", "DOUBLE_TAKEOUT", "HIT_AND_ROLL", "RAISE", "DRAW", "GUARD"), target_index,
            rule_constraint, True, int(own_throw_number) == 8, historical,
            "复杂营内不按叫球名判成败；每条候选都须以实际终局的对方得分层、己方存活层和反击入口评分。",
        )

    # GUARD_EXCHANGE 与 MIXED_CONTESTED：没有稳定历史处方，但仍输出明确的
    # 搜索目标，避免旧式“找到敌壶就清”。
    return TacticalLibraryPlan(
        int(own_throw_number), state.state_id, raw, "PHYSX_SEARCH_REQUIRED",
        "建立己方可继续施压的层，或处理真正阻断入口的壶；不默认清场。",
        _next_state(int(own_throw_number), "OWN_HOUSE_CONTROL"),
        "COMPARE_PRESSURE_AND_WING_OPTIONS",
        ("DRAW", "GUARD", "WING_DRAW", "HIT_AND_ROLL", "CLEARING"), target_index,
        rule_constraint, True, int(own_throw_number) == 8, historical,
        "守壶交换/混合局面缺乏单一稳健动作；让 PhysX 在压力壶、两翼和必要处理之间比较。",
    )
