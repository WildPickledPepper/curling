"""Normalized, permutation-friendly board representation for PPO Stage C."""

from __future__ import annotations

from typing import List, Sequence, Tuple

import torch

from ppo_state_reward import (
    HOUSE_R,
    HOUSE_X,
    HOUSE_Y,
    blocked_house_threat,
    clamp,
    dist_house,
    is_center_guard,
    is_guard_zone,
    is_house,
    is_played,
    owner_for_index,
    protected_house_count,
    protection_count,
    summarize_position,
)

STONE_COUNT = 16
STONE_FEATURE_DIM = 12
LEGACY_GLOBAL_FEATURE_DIM = 20
GLOBAL_FEATURE_DIM = 28
STAGE_C_STATE_DIM = STONE_COUNT * STONE_FEATURE_DIM + GLOBAL_FEATURE_DIM
HAMMER_GLOBAL_INDEX = 3


def _lane_blocking_flags(position: Sequence[float], index: int) -> Tuple[float, float]:
    raw_index = index * 2
    x_value = float(position[raw_index])
    y_value = float(position[raw_index + 1])
    if not is_played(x_value, y_value):
        return 0.0, 0.0
    blocked_left = False
    blocked_right = False
    for other_index in range(STONE_COUNT):
        if other_index == index:
            continue
        other_raw = other_index * 2
        other_x = float(position[other_raw])
        other_y = float(position[other_raw + 1])
        if not is_played(other_x, other_y):
            continue
        # Stones with larger y are encountered first by a delivered stone.
        if other_y <= y_value + 0.20 or abs(other_x - x_value) > 0.65:
            continue
        if other_x <= x_value + 0.12:
            blocked_left = True
        if other_x >= x_value - 0.12:
            blocked_right = True
    return float(blocked_left), float(blocked_right)


def encode_stones(position: Sequence[float], player_is_init: bool) -> List[List[float]]:
    """Encode all physical stone slots without sorting them by tee distance."""
    summary = summarize_position(position, player_is_init)
    guards = list(summary["my_guards"]) + list(summary["opp_guards"])
    stones_by_index = {stone.index: stone for stone in summary["stones"]}
    encoded: List[List[float]] = []
    for index in range(STONE_COUNT):
        raw_index = index * 2
        x_value = float(position[raw_index]) if raw_index < len(position) else 0.0
        y_value = float(position[raw_index + 1]) if raw_index + 1 < len(position) else 0.0
        played = is_played(x_value, y_value)
        owner = 0.0
        if played:
            owner = 1.0 if owner_for_index(index, player_is_init) == "my" else -1.0
        stone = stones_by_index.get(index)
        protected = protection_count(stone, guards) if stone is not None and is_house(x_value, y_value) else 0
        blocked_left, blocked_right = _lane_blocking_flags(position, index)
        encoded.append([
            float(played),
            clamp((x_value - HOUSE_X) / max(HOUSE_X, 1e-6), -1.0, 1.0) if played else 0.0,
            clamp((y_value - HOUSE_Y) / 5.0, -1.0, 1.0) if played else 0.0,
            owner,
            clamp(dist_house(x_value, y_value) / 6.0, 0.0, 1.0) if played else 0.0,
            float(played and is_house(x_value, y_value)),
            float(played and is_guard_zone(x_value, y_value)),
            float(played and is_center_guard(x_value, y_value)),
            clamp(float(protected) / 4.0, 0.0, 1.0),
            blocked_left,
            blocked_right,
            float(index) / float(STONE_COUNT - 1),
        ])
    return encoded


def encode_globals(
    position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    end_score: int = 0,
    total_ends: int = -1,
    current_player: int = 0,
    current_end: int = 0,
    cumulative_score_diff: int = 0,
) -> List[float]:
    summary = summarize_position(position, player_is_init)
    played_my = sum(stone.owner == "my" for stone in summary["stones"])
    played_opp = sum(stone.owner == "opp" for stone in summary["stones"])
    closest_owner = summary["closest_owner"]
    blocked_target, blocking_guards = blocked_house_threat(summary)
    my_protected = protected_house_count(summary["my_house"], summary["my_guards"])
    opp_protected = protected_house_count(summary["opp_house"], summary["opp_guards"])
    fixed_match = total_ends > 0
    end_number = max(0, int(current_end))
    ends_remaining = max(0, int(total_ends) - end_number) if fixed_match else -1
    score_diff = int(cumulative_score_diff)
    return [
        clamp(float(shot_num) / 16.0, 0.0, 1.0),
        clamp(float(8 - played_my) / 8.0, 0.0, 1.0),
        clamp(float(8 - played_opp) / 8.0, 0.0, 1.0),
        0.0 if player_is_init else 1.0,
        1.0 if player_is_init else 0.0,
        clamp(float(end_score) / 8.0, -1.0, 1.0),
        clamp(float(total_ends) / 10.0, -1.0, 1.0) if total_ends >= 0 else -1.0,
        clamp((float(current_player) - 1.5) / 1.5, -1.0, 1.0),
        clamp(float(summary["score_for_my"]) / 8.0, -1.0, 1.0),
        clamp(len(summary["my_house"]) / 8.0, 0.0, 1.0),
        clamp(len(summary["opp_house"]) / 8.0, 0.0, 1.0),
        clamp(len(summary["my_guards"]) / 8.0, 0.0, 1.0),
        clamp(len(summary["opp_guards"]) / 8.0, 0.0, 1.0),
        float(shot_num <= 4),
        float(shot_num >= 15),
        1.0 if closest_owner == "my" else -1.0 if closest_owner == "opp" else 0.0,
        float(shot_num >= 12 and len(summary["opp_house"]) >= 2),
        float(blocked_target is not None and bool(blocking_guards)),
        clamp(float(my_protected) / 4.0, 0.0, 1.0),
        clamp(float(opp_protected) / 4.0, 0.0, 1.0),
        clamp(float(end_number) / float(total_ends), 0.0, 1.0) if fixed_match else -1.0,
        clamp(float(ends_remaining) / float(total_ends), 0.0, 1.0) if fixed_match else -1.0,
        clamp(float(score_diff) / 16.0, -1.0, 1.0),
        float(score_diff > 0),
        float(score_diff == 0),
        float(score_diff < 0),
        float(fixed_match and end_number >= total_ends),
        float(fixed_match and end_number >= max(1, total_ends - 1)),
    ]


def build_stage_c_state(
    position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    end_score: int = 0,
    total_ends: int = -1,
    current_player: int = 0,
    current_end: int = 0,
    cumulative_score_diff: int = 0,
) -> List[float]:
    stones = encode_stones(position, player_is_init)
    globals_ = encode_globals(
        position, player_is_init, shot_num,
        end_score=end_score, total_ends=total_ends, current_player=current_player,
        current_end=current_end, cumulative_score_diff=cumulative_score_diff,
    )
    flat = [feature for stone in stones for feature in stone] + globals_
    if len(flat) != STAGE_C_STATE_DIM:
        raise ValueError(f"Unexpected Stage C state length {len(flat)}; expected {STAGE_C_STATE_DIM}")
    return flat


def split_stage_c_tensor(states: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    if states.shape[-1] != STAGE_C_STATE_DIM:
        raise ValueError(
            f"Unexpected Stage C tensor width {states.shape[-1]}; expected {STAGE_C_STATE_DIM}"
        )
    stone_width = STONE_COUNT * STONE_FEATURE_DIM
    stones = states[..., :stone_width].reshape(*states.shape[:-1], STONE_COUNT, STONE_FEATURE_DIM)
    globals_ = states[..., stone_width:]
    valid_mask = stones[..., 0] > 0.5
    return stones, globals_, valid_mask
