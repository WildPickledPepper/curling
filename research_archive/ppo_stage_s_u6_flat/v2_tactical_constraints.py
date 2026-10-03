"""Contextual Stage C action constraints based on board geometry, not action priors."""

from __future__ import annotations

from typing import Dict, List, Sequence

from ppo_actions import action_id
from ppo_state_reward import is_house, protected_house_count, summarize_position


def _aligned_front_stone(stone, target, *, tolerance: float = 0.48) -> bool:
    return stone.y > target.y + 0.25 and abs(stone.x - target.x) <= tolerance


def complex_hit_targets(position: Sequence[float], player_is_init: bool) -> Dict[str, bool]:
    summary = summarize_position(position, player_is_init)
    opponent_house = list(summary["opp_house"])
    own_stones = [stone for stone in summary["stones"] if stone.owner == "my"]
    opponent_guards = [
        stone for stone in summary["opp_guards"] if not is_house(stone.x, stone.y)
    ]
    return {
        "raise_takeout": any(
            _aligned_front_stone(stone, target)
            for target in opponent_house
            for stone in own_stones
        ),
        "runback_takeout": any(
            _aligned_front_stone(stone, target)
            for target in opponent_house
            for stone in opponent_guards
        ),
    }


def tactical_context(
    position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    *,
    current_end: int,
    total_ends: int,
    cumulative_score_diff: int,
) -> Dict[str, bool]:
    summary = summarize_position(position, player_is_init)
    fixed_match = total_ends > 0 and current_end > 0
    late_match = fixed_match and current_end >= max(1, total_ends - 1)
    protected_scoring = (
        late_match
        and cumulative_score_diff >= 2
        and int(summary["score_for_my"]) > 0
        and summary["closest_owner"] == "my"
        and protected_house_count(summary["my_house"], summary["my_guards"]) > 0
    )
    final_trailing_build = (
        fixed_match
        and current_end >= total_ends
        and cumulative_score_diff <= -2
        and not player_is_init
        and shot_num >= 8
    )
    return {
        "protect_scoring_structure": bool(protected_scoring),
        "final_trailing_build": bool(final_trailing_build),
    }


def apply_stage_c_action_constraints(
    action_mask: Sequence[bool],
    position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    *,
    current_end: int,
    total_ends: int,
    cumulative_score_diff: int,
    context_mask: bool,
    complex_hit_mask: bool,
) -> List[bool]:
    mask = list(action_mask)
    if complex_hit_mask:
        targets = complex_hit_targets(position, player_is_init)
        for name, viable in targets.items():
            if not viable:
                mask[action_id(name)] = False

    if context_mask:
        context = tactical_context(
            position, player_is_init, shot_num,
            current_end=current_end, total_ends=total_ends,
            cumulative_score_diff=cumulative_score_diff,
        )
        summary = summarize_position(position, player_is_init)
        if context["protect_scoring_structure"]:
            for name in (
                "take_out", "take_out_house", "hit_and_stay",
                "hit_roll", "hit_roll_left", "hit_roll_right",
                "double_hit", "raise_takeout", "runback_takeout",
                "around_guard_takeout_left", "around_guard_takeout_right",
                "push_in_14", "double_push_in",
            ):
                mask[action_id(name)] = False
        if context["final_trailing_build"] and summary["closest_owner"] == "my":
            for name in (
                "take_out_guard", "peel_guard", "clear",
                "raise_takeout", "runback_takeout", "double_hit", "push_in_14",
            ):
                mask[action_id(name)] = False

    if not any(mask):
        mask[action_id("default_draw")] = True
    return mask
