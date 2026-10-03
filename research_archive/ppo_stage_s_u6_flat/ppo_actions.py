"""High-level tactic action space used by the first PPO version."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TacticAction:
    action_id: int
    name: str


TACTIC_ACTIONS: List[TacticAction] = [
    TacticAction(0, "occupy"),
    TacticAction(1, "middle_in_center"),
    TacticAction(2, "defense"),
    TacticAction(3, "defense_push_in"),
    TacticAction(4, "take_out"),
    TacticAction(5, "hit_roll"),
    TacticAction(6, "push_in"),
    TacticAction(7, "push_in_14"),
    TacticAction(8, "freeze"),
    TacticAction(9, "clear"),
    TacticAction(10, "double_hit"),
    TacticAction(11, "double_push_in"),
    TacticAction(12, "default_draw"),
    TacticAction(13, "draw_button"),
    TacticAction(14, "draw_top4"),
    TacticAction(15, "draw_back4"),
    TacticAction(16, "center_guard"),
    TacticAction(17, "corner_guard_left"),
    TacticAction(18, "corner_guard_right"),
    TacticAction(19, "come_around_left"),
    TacticAction(20, "come_around_right"),
    TacticAction(21, "take_out_house"),
    TacticAction(22, "take_out_guard"),
    TacticAction(23, "hit_and_stay"),
    TacticAction(24, "peel_guard"),
    TacticAction(25, "hit_roll_left"),
    TacticAction(26, "hit_roll_right"),
    TacticAction(27, "freeze_no1"),
    TacticAction(28, "freeze_no2"),
    TacticAction(29, "guard_my_shot"),
    TacticAction(30, "center_guard_high"),
    TacticAction(31, "center_guard_low"),
    TacticAction(32, "corner_guard_left_high"),
    TacticAction(33, "corner_guard_right_high"),
    TacticAction(34, "tap_back"),
    TacticAction(35, "raise_takeout"),
    TacticAction(36, "runback_takeout"),
    TacticAction(37, "around_guard_takeout_left"),
    TacticAction(38, "around_guard_takeout_right"),
    TacticAction(39, "around_guard_draw_left"),
    TacticAction(40, "around_guard_draw_right"),
]

ACTION_NAMES = [action.name for action in TACTIC_ACTIONS]
ACTION_NAME_TO_ID = {action.name: action.action_id for action in TACTIC_ACTIONS}
N_ACTIONS = len(TACTIC_ACTIONS)


def action_name(action_id: int) -> str:
    return ACTION_NAMES[int(action_id)]


def action_id(name: str) -> int:
    if name in ACTION_NAME_TO_ID:
        return ACTION_NAME_TO_ID[name]
    if name in ("double_hit_init", "double_hit_gote", "double_hit_last"):
        return ACTION_NAME_TO_ID["double_hit"]
    if name in ("double_push_in_center",):
        return ACTION_NAME_TO_ID["double_push_in"]
    if name in ("draw_center", "draw_button"):
        return ACTION_NAME_TO_ID["draw_button"]
    if name in ("guard_center",):
        return ACTION_NAME_TO_ID["center_guard"]
    if name in ("peel", "clear_guard"):
        return ACTION_NAME_TO_ID["peel_guard"]
    if name in ("freeze_no1", "freeze_first"):
        return ACTION_NAME_TO_ID["freeze_no1"]
    if name in ("freeze_no2", "freeze_second"):
        return ACTION_NAME_TO_ID["freeze_no2"]
    if name in ("raise",):
        return ACTION_NAME_TO_ID["raise_takeout"]
    if name in ("runback",):
        return ACTION_NAME_TO_ID["runback_takeout"]
    raise KeyError(f"Unknown tactic action: {name}")
