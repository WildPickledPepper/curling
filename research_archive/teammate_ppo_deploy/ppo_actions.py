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
    raise KeyError(f"Unknown tactic action: {name}")
