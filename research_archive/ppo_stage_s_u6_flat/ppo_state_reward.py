"""State extraction, board evaluation, and reward shaping for curling PPO."""

import json
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
IN_HOUSE_R = HOUSE_R + STONE_R

FGZ_X_MIN = 0.545
FGZ_X_MAX = 4.205
FGZ_Y_MIN = 6.71
FGZ_Y_MAX = 9.74
CENTER_GUARD_HALF_WIDTH = 0.45
PROTECTION_LANE_WIDTH = 0.55
FREEZE_CONTACT_DIST = STONE_R * 2.6
CORNER_GUARD_MIN_OFFSET = 0.65

HIT_CONTEXT_DIM = 20
TACTICAL_CONTEXT_DIM = 16
STATE_DIM = 16 * 5 + 8 + HIT_CONTEXT_DIM + TACTICAL_CONTEXT_DIM
SER_WEIGHT = 0.9
FR_WEIGHT = 0.1
INVALID_ACTION_PENALTY = 1.0
FALLBACK_DRAW_PENALTY = 1.5

HOUSE_HIT_ACTIONS = frozenset({
    "take_out",
    "take_out_house",
    "hit_and_stay",
    "hit_roll",
    "hit_roll_left",
    "hit_roll_right",
    "double_hit",
    "raise_takeout",
    "runback_takeout",
    "around_guard_takeout_left",
    "around_guard_takeout_right",
})
GUARD_HIT_ACTIONS = frozenset({
    "take_out_guard",
    "peel_guard",
    "clear",
})
SOFT_DISPLACEMENT_ACTIONS = frozenset({
    "push_in",
    "push_in_14",
    "double_push_in",
    "tap_back",
})
SETUP_ACTIONS = frozenset({
    "occupy",
    "middle_in_center",
    "defense",
    "defense_push_in",
    "freeze",
    "freeze_no1",
    "freeze_no2",
    "default_draw",
    "draw_button",
    "draw_top4",
    "draw_back4",
    "center_guard",
    "center_guard_high",
    "center_guard_low",
    "corner_guard_left",
    "corner_guard_right",
    "corner_guard_left_high",
    "corner_guard_right_high",
    "guard_my_shot",
    "come_around_left",
    "come_around_right",
    "around_guard_draw_left",
    "around_guard_draw_right",
})
HIT_ACTIONS = HOUSE_HIT_ACTIONS | GUARD_HIT_ACTIONS | SOFT_DISPLACEMENT_ACTIONS


@dataclass(frozen=True)
class Stone:
    index: int
    x: float
    y: float
    owner: str
    dist: float


def dist_house(x_value: float, y_value: float) -> float:
    return math.sqrt((x_value - HOUSE_X) ** 2 + (y_value - HOUSE_Y) ** 2)


def is_played(x_value: float, y_value: float) -> bool:
    return x_value != 0 or y_value != 0


def is_house(x_value: float, y_value: float) -> bool:
    return dist_house(x_value, y_value) < IN_HOUSE_R


def is_guard_zone(x_value: float, y_value: float) -> bool:
    return FGZ_Y_MIN < y_value < FGZ_Y_MAX and FGZ_X_MIN < x_value < FGZ_X_MAX


def is_center_guard(x_value: float, y_value: float) -> bool:
    return is_guard_zone(x_value, y_value) and abs(x_value - HOUSE_X) <= CENTER_GUARD_HALF_WIDTH


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def owner_for_index(index: int, player_is_init: bool) -> str:
    stone_is_init = index % 2 == 0
    return "my" if stone_is_init == player_is_init else "opp"


def parse_position_json(value: str) -> List[float]:
    if not value:
        return [0.0] * 32
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [0.0] * 32
    values = [float(item) for item in parsed[:32]]
    values.extend([0.0] * (32 - len(values)))
    return values[:32]


def stones_from_position(position: Sequence[float], player_is_init: bool) -> List[Stone]:
    stones: List[Stone] = []
    for index in range(16):
        raw_index = index * 2
        if raw_index + 1 >= len(position):
            break
        x_value = float(position[raw_index])
        y_value = float(position[raw_index + 1])
        if not is_played(x_value, y_value):
            continue
        stones.append(
            Stone(
                index=index,
                x=x_value,
                y=y_value,
                owner=owner_for_index(index, player_is_init),
                dist=dist_house(x_value, y_value),
            )
        )
    return stones


def score_from_house(house_stones: Sequence[Stone]) -> int:
    if not house_stones:
        return 0
    sorted_stones = sorted(house_stones, key=lambda stone: stone.dist)
    closest_owner = sorted_stones[0].owner
    score = 0
    for stone in sorted_stones:
        if stone.owner != closest_owner:
            break
        score += 1 if closest_owner == "my" else -1
    return score


def summarize_position(position: Sequence[float], player_is_init: bool) -> Dict[str, object]:
    stones = stones_from_position(position, player_is_init)
    house_stones = [stone for stone in stones if is_house(stone.x, stone.y)]
    house_stones.sort(key=lambda stone: stone.dist)
    my_house = [stone for stone in house_stones if stone.owner == "my"]
    opp_house = [stone for stone in house_stones if stone.owner == "opp"]
    my_guards = [stone for stone in stones if stone.owner == "my" and is_guard_zone(stone.x, stone.y)]
    opp_guards = [stone for stone in stones if stone.owner == "opp" and is_guard_zone(stone.x, stone.y)]
    closest_owner: Optional[str] = house_stones[0].owner if house_stones else None

    return {
        "stones": stones,
        "house_stones": house_stones,
        "my_house": my_house,
        "opp_house": opp_house,
        "my_guards": my_guards,
        "opp_guards": opp_guards,
        "closest_owner": closest_owner,
        "score_for_my": score_from_house(house_stones),
    }


def stone_by_index(summary: Dict[str, object], index: int) -> Optional[Stone]:
    for stone in summary["stones"]:
        if stone.index == index:
            return stone
    return None


def nearest_opponent_stone(summary: Dict[str, object]) -> Optional[Stone]:
    opp_stones = [stone for stone in summary["stones"] if stone.owner == "opp"]
    if not opp_stones:
        return None
    return min(opp_stones, key=lambda stone: stone.dist)


def blocked_house_threat(summary: Dict[str, object]) -> Tuple[Optional[Stone], List[Stone]]:
    """Find the highest-value opponent house target protected by front guards."""
    for target in summary["opp_house"]:
        blockers = [
            guard for guard in summary["my_guards"] + summary["opp_guards"]
            if guard.y > target.y and abs(guard.x - target.x) <= 0.52
        ]
        if blockers:
            return target, blockers
    return None, []


def bypass_lane_open(
    summary: Dict[str, object],
    target: Optional[Stone],
    blockers: Sequence[Stone],
    side: int,
) -> bool:
    """Approximate whether the calibrated curl entry lane is clear on one side."""
    if target is None or not blockers:
        return False
    front_guard = max(blockers, key=lambda stone: stone.y)
    lane_x = front_guard.x + side * 0.78
    if not 0.30 < lane_x < 4.45:
        return False
    return not any(
        stone.index != target.index
        and stone.y >= front_guard.y
        and abs(stone.x - lane_x) <= 2.0 * STONE_R
        for stone in summary["stones"]
    )


def owner_rank(owner: Optional[str]) -> int:
    if owner == "my":
        return 1
    if owner == "opp":
        return -1
    return 0


def guard_protects_stone(guard: Stone, stone: Stone) -> bool:
    return (
        guard.y > stone.y
        and is_guard_zone(guard.x, guard.y)
        and abs(guard.x - stone.x) <= PROTECTION_LANE_WIDTH
    )


def protection_count(stone: Optional[Stone], guards: Sequence[Stone]) -> int:
    if stone is None:
        return 0
    return sum(1 for guard in guards if guard_protects_stone(guard, stone))


def protected_house_count(house_stones: Sequence[Stone], guards: Sequence[Stone]) -> int:
    return sum(1 for stone in house_stones if protection_count(stone, guards) > 0)


def stone_distance(first: Stone, second: Stone) -> float:
    return math.sqrt((first.x - second.x) ** 2 + (first.y - second.y) ** 2)


def freeze_contact_count(summary: Dict[str, object], owner: str) -> int:
    owner_stones = [
        stone for stone in summary["stones"]
        if stone.owner == owner and (is_house(stone.x, stone.y) or stone.y <= FGZ_Y_MIN)
    ]
    other_owner = "opp" if owner == "my" else "my"
    other_house = [
        stone for stone in summary["house_stones"]
        if stone.owner == other_owner
    ]
    count = 0
    for stone in owner_stones:
        if any(stone_distance(stone, other) <= FREEZE_CONTACT_DIST for other in other_house):
            count += 1
    return count


def corner_guard_count(guards: Sequence[Stone]) -> int:
    return sum(
        1 for guard in guards
        if abs(guard.x - HOUSE_X) >= CORNER_GUARD_MIN_OFFSET
    )


def first_opposite_after_scoring_group(house_stones: Sequence[Stone]) -> Optional[Stone]:
    if not house_stones:
        return None
    closest_owner = house_stones[0].owner
    for stone in house_stones:
        if stone.owner != closest_owner:
            return stone
    return None


def ayumu_expected_end_value(
    summary: Dict[str, object],
    player_is_init: bool,
    shot_num: int,
) -> float:
    """Approximate Ayumu's end-score reward table with interpretable features."""
    house_stones = summary["house_stones"]
    has_hammer = not player_is_init
    phase = clamp(float(shot_num) / 15.0, 0.0, 1.0)

    if not house_stones:
        return 0.08 if has_hammer else -0.04

    score = float(summary["score_for_my"])
    no1 = house_stones[0]
    no1_sign = float(owner_rank(no1.owner))
    no1_tee_strength = 1.0 - clamp(no1.dist / IN_HOUSE_R, 0.0, 1.0)
    score_weight = 0.45 + 0.55 * phase

    value = score * score_weight
    value += no1_sign * (0.18 + 0.10 * phase) * no1_tee_strength

    next_stone = first_opposite_after_scoring_group(house_stones)
    if next_stone is not None:
        no2_strength = 1.0 - clamp(next_stone.dist / IN_HOUSE_R, 0.0, 1.0)
        if no1.owner == "my" and next_stone.owner == "opp":
            value -= (0.08 + 0.08 * phase) * no2_strength
        elif no1.owner == "opp" and next_stone.owner == "my":
            value += (0.08 + 0.08 * phase) * no2_strength

    no1_guards = protection_count(
        no1,
        summary["my_guards"] if no1.owner == "my" else summary["opp_guards"],
    )
    value += no1_sign * min(no1_guards, 2) * (0.06 + 0.08 * phase)

    if has_hammer and score == 1.0 and shot_num < 12:
        value -= 0.08
    elif has_hammer and score <= -1.0 and shot_num >= 10:
        value -= 0.10

    return value


def tactical_context_features(
    summary: Dict[str, object],
    player_is_init: bool,
    shot_num: int,
    end_score: int,
    total_ends: int,
    current_player: int,
) -> List[float]:
    my_center_guards = [
        stone for stone in summary["my_guards"]
        if is_center_guard(stone.x, stone.y)
    ]
    opp_center_guards = [
        stone for stone in summary["opp_guards"]
        if is_center_guard(stone.x, stone.y)
    ]
    closest_my = summary["my_house"][0] if summary["my_house"] else None
    closest_opp = summary["opp_house"][0] if summary["opp_house"] else None
    my_protected_house = protected_house_count(summary["my_house"], summary["my_guards"])
    opp_protected_house = protected_house_count(summary["opp_house"], summary["opp_guards"])

    closest_my_protection = protection_count(closest_my, summary["my_guards"])
    closest_opp_protection = protection_count(closest_opp, summary["opp_guards"])
    score_for_my = int(summary["score_for_my"])
    first_five = shot_num <= 4
    late_pressure = shot_num >= 12 and (score_for_my < 0 or summary["closest_owner"] == "opp")
    guard_clear_risky = (
        first_five
        and score_for_my >= 0
        and len(opp_center_guards) + len(summary["opp_guards"]) > 0
    )

    return [
        clamp((16.0 - float(shot_num)) / 16.0, 0.0, 1.0),
        0.0 if player_is_init else 1.0,
        clamp(float(end_score) / 8.0, -1.0, 1.0),
        clamp(float(total_ends) / 10.0, -1.0, 1.0) if total_ends >= 0 else -1.0,
        clamp((float(current_player) - 1.5) / 1.5, -1.0, 1.0),
        clamp(len(my_center_guards) / 4.0, 0.0, 1.0),
        clamp(len(opp_center_guards) / 4.0, 0.0, 1.0),
        clamp((len(my_center_guards) - len(opp_center_guards)) / 4.0, -1.0, 1.0),
        clamp(my_protected_house / 4.0, 0.0, 1.0),
        clamp(opp_protected_house / 4.0, 0.0, 1.0),
        1.0 if closest_my is not None and closest_my_protection > 0 else 0.0,
        1.0 if closest_opp is not None and closest_opp_protection > 0 else 0.0,
        1.0 if closest_opp is not None and closest_opp_protection == 0 else 0.0,
        1.0 if closest_my is not None and closest_my_protection == 0 else 0.0,
        1.0 if guard_clear_risky else 0.0,
        1.0 if late_pressure else 0.0,
    ]


def hit_context_features(
    summary: Dict[str, object],
    shot_num: int,
) -> List[float]:
    nearest_opp = nearest_opponent_stone(summary)
    score_for_my = int(summary["score_for_my"])
    closest_house = summary["house_stones"][0] if summary["house_stones"] else None

    if nearest_opp is None:
        target_features = [0.0] * 7
    else:
        target_features = [
            1.0,
            1.0 if is_house(nearest_opp.x, nearest_opp.y) else 0.0,
            1.0 if is_guard_zone(nearest_opp.x, nearest_opp.y) else 0.0,
            1.0
            if closest_house is not None
            and closest_house.owner == "opp"
            and closest_house.index == nearest_opp.index
            else 0.0,
            clamp(nearest_opp.dist / 6.0, 0.0, 1.0),
            clamp((nearest_opp.x - HOUSE_X) / HOUSE_R, -1.0, 1.0),
            clamp((nearest_opp.y - HOUSE_Y) / 5.0, -1.0, 1.0),
        ]

    my_house = len(summary["my_house"])
    opp_house = len(summary["opp_house"])
    my_guards = len(summary["my_guards"])
    opp_guards = len(summary["opp_guards"])
    urgent_hit = shot_num >= 10 and (score_for_my < 0 or summary["closest_owner"] == "opp")

    blocked_target, blocking_guards = blocked_house_threat(summary)
    left_open = bypass_lane_open(summary, blocked_target, blocking_guards, side=-1)
    right_open = bypass_lane_open(summary, blocked_target, blocking_guards, side=1)
    multi_stone_threat = (
        shot_num >= 12
        and score_for_my < 0
        and len(summary["opp_house"]) >= 2
        and bool(blocking_guards)
    )

    return target_features + [
        clamp(max(0, -score_for_my) / 8.0, 0.0, 1.0),
        clamp((my_house - opp_house) / 8.0, -1.0, 1.0),
        clamp((my_guards - opp_guards) / 8.0, -1.0, 1.0),
        1.0 if shot_num >= 12 else 0.0,
        1.0 if urgent_hit else 0.0,
        1.0 if blocked_target is not None else 0.0,
        clamp(len(blocking_guards) / 3.0, 0.0, 1.0),
        1.0 if left_open else 0.0,
        1.0 if right_open else 0.0,
        clamp((blocked_target.x - HOUSE_X) / HOUSE_R, -1.0, 1.0) if blocked_target else 0.0,
        clamp(len(summary["opp_house"]) / 4.0, 0.0, 1.0),
        clamp(max(0, -score_for_my) / 4.0, 0.0, 1.0),
        1.0 if multi_stone_threat else 0.0,
    ]


def stone_features(position: Sequence[float], player_is_init: bool) -> List[float]:
    features: List[Tuple[float, float, float, float, float]] = []
    for index in range(16):
        raw_index = index * 2
        x_value = float(position[raw_index]) if raw_index < len(position) else 0.0
        y_value = float(position[raw_index + 1]) if raw_index + 1 < len(position) else 0.0
        if is_played(x_value, y_value):
            owner = 1.0 if owner_for_index(index, player_is_init) == "my" else -1.0
            in_score_zone = 1.0 if is_house(x_value, y_value) else 0.0
            features.append((x_value, y_value, dist_house(x_value, y_value), owner, in_score_zone))
        else:
            features.append((0.0, 0.0, 0.0, 0.0, 0.0))

    features.sort(key=lambda item: item[2] if item[2] > 0 else 99.0)
    flat: List[float] = []
    for item in features:
        flat.extend(item)
    return flat


def build_state(
    position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    end_score: int = 0,
    total_ends: int = -1,
    current_player: int = 0,
) -> List[float]:
    summary = summarize_position(position, player_is_init)
    flat = stone_features(position, player_is_init)

    shot_progress = max(0.0, min(1.0, float(shot_num) / 16.0))
    extra = [
        shot_progress,
        1.0 if player_is_init else 0.0,
        float(summary["score_for_my"]) / 8.0,
        len(summary["my_house"]) / 8.0,
        len(summary["opp_house"]) / 8.0,
        len(summary["my_guards"]) / 8.0,
        len(summary["opp_guards"]) / 8.0,
        1.0 if shot_num <= 4 else 0.0,
    ]
    extra.extend(hit_context_features(summary, shot_num))
    extra.extend(
        tactical_context_features(
            summary=summary,
            player_is_init=player_is_init,
            shot_num=shot_num,
            end_score=end_score,
            total_ends=total_ends,
            current_player=current_player,
        )
    )
    state = flat + extra
    if len(state) != STATE_DIM:
        raise ValueError(f"Unexpected state length {len(state)}; expected {STATE_DIM}")
    return state


def board_value(position: Sequence[float], player_is_init: bool, shot_num: int) -> float:
    summary = summarize_position(position, player_is_init)
    my_house = len(summary["my_house"])
    opp_house = len(summary["opp_house"])
    my_guards = len(summary["my_guards"])
    opp_guards = len(summary["opp_guards"])
    closest_owner = summary["closest_owner"]
    closest_my = summary["my_house"][0] if summary["my_house"] else None
    closest_opp = summary["opp_house"][0] if summary["opp_house"] else None
    my_center_guards = sum(1 for stone in summary["my_guards"] if is_center_guard(stone.x, stone.y))
    opp_center_guards = sum(1 for stone in summary["opp_guards"] if is_center_guard(stone.x, stone.y))
    closest_my_protection = protection_count(closest_my, summary["my_guards"])
    closest_opp_protection = protection_count(closest_opp, summary["opp_guards"])
    my_protected_house = protected_house_count(summary["my_house"], summary["my_guards"])
    opp_protected_house = protected_house_count(summary["opp_house"], summary["opp_guards"])

    value = ayumu_expected_end_value(summary, player_is_init, shot_num)
    value += my_house * 0.07
    value -= opp_house * 0.075
    if closest_owner == "my":
        value += 0.12
    elif closest_owner == "opp":
        value -= 0.12

    if shot_num <= 6:
        value += my_guards * 0.12
        value -= opp_guards * 0.09
        value += my_center_guards * 0.10
        value -= opp_center_guards * 0.08
    else:
        value += my_guards * 0.05
        value -= opp_guards * 0.05

    value += my_protected_house * 0.07
    value -= opp_protected_house * 0.07

    if closest_owner == "my":
        value += min(closest_my_protection, 2) * 0.09
    elif closest_owner == "opp":
        value -= min(closest_opp_protection, 2) * 0.08

    return value


def setup_value(position: Sequence[float], player_is_init: bool, shot_num: int) -> float:
    """Estimate tactical structures whose value often appears after later stones."""
    summary = summarize_position(position, player_is_init)
    has_hammer = not player_is_init
    phase = clamp(float(shot_num) / 15.0, 0.0, 1.0)
    early_weight = 1.0 - phase
    late_weight = phase

    closest_my = summary["my_house"][0] if summary["my_house"] else None
    closest_opp = summary["opp_house"][0] if summary["opp_house"] else None
    my_center_guards = sum(1 for stone in summary["my_guards"] if is_center_guard(stone.x, stone.y))
    opp_center_guards = sum(1 for stone in summary["opp_guards"] if is_center_guard(stone.x, stone.y))
    my_corner_guards = corner_guard_count(summary["my_guards"])
    opp_corner_guards = corner_guard_count(summary["opp_guards"])
    my_protected_house = protected_house_count(summary["my_house"], summary["my_guards"])
    opp_protected_house = protected_house_count(summary["opp_house"], summary["opp_guards"])
    closest_my_protection = protection_count(closest_my, summary["my_guards"])
    closest_opp_protection = protection_count(closest_opp, summary["opp_guards"])

    value = 0.0
    if has_hammer:
        value += early_weight * (0.09 * my_center_guards + 0.16 * my_corner_guards)
        value -= early_weight * (0.12 * opp_center_guards + 0.10 * opp_corner_guards)
    else:
        value += early_weight * (0.18 * my_center_guards + 0.09 * my_corner_guards)
        value -= early_weight * (0.16 * opp_center_guards + 0.10 * opp_corner_guards)

    protection_scale = 0.55 + 0.45 * early_weight
    value += (0.17 + 0.14 * early_weight) * my_protected_house
    value -= (0.15 + 0.10 * early_weight) * opp_protected_house
    value += min(closest_my_protection, 2) * (0.09 + 0.11 * protection_scale)
    value -= min(closest_opp_protection, 2) * (0.08 + 0.10 * protection_scale)

    my_freezes = freeze_contact_count(summary, "my")
    opp_freezes = freeze_contact_count(summary, "opp")
    value += min(my_freezes, 2) * (0.19 + 0.07 * late_weight)
    value -= min(opp_freezes, 2) * (0.15 + 0.06 * late_weight)

    if closest_my is not None:
        tee_strength = 1.0 - clamp(closest_my.dist / IN_HOUSE_R, 0.0, 1.0)
        value += (0.10 + 0.09 * late_weight) * tee_strength
    if closest_opp is not None:
        tee_strength = 1.0 - clamp(closest_opp.dist / IN_HOUSE_R, 0.0, 1.0)
        value -= (0.11 + 0.09 * late_weight) * tee_strength

    return clamp(value, -3.0, 3.0)


def delayed_setup_reward(
    before_position: Sequence[float],
    after_own_position: Sequence[float],
    after_response_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    weight: float = 0.45,
    max_abs: float = 1.2,
) -> float:
    phase = clamp(float(shot_num) / 15.0, 0.0, 1.0)
    late_decay = max(0.25, 1.0 - 0.75 * phase)
    before_value = setup_value(before_position, player_is_init, shot_num)
    after_own_value = setup_value(after_own_position, player_is_init, shot_num)
    after_response_value = setup_value(after_response_position, player_is_init, min(15, shot_num + 1))
    survived_gain = after_response_value - before_value
    fragility_penalty = max(0.0, after_own_value - after_response_value)
    reward = weight * late_decay * (survived_gain - 0.45 * fragility_penalty)
    return clamp(reward, -max_abs, max_abs)


def setup_outcome_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    action_name: str,
) -> float:
    if action_name not in SETUP_ACTIONS:
        return 0.0

    before = summarize_position(before_position, player_is_init)
    after = summarize_position(after_position, player_is_init)
    phase = clamp(float(shot_num) / 15.0, 0.0, 1.0)
    setup_scale = max(0.08, 1.0 - 0.92 * phase)
    late_pressure = shot_num >= 10 and (
        int(before["score_for_my"]) < 0 or before["closest_owner"] == "opp"
    )
    endgame_pressure = shot_num >= 12 and (
        int(before["score_for_my"]) <= 0 or before["closest_owner"] == "opp"
    )

    setup_delta = setup_value(after_position, player_is_init, shot_num) - setup_value(
        before_position, player_is_init, shot_num
    )
    reward = 0.20 * setup_delta * setup_scale

    before_my_center = sum(1 for stone in before["my_guards"] if is_center_guard(stone.x, stone.y))
    after_my_center = sum(1 for stone in after["my_guards"] if is_center_guard(stone.x, stone.y))
    before_my_corner = corner_guard_count(before["my_guards"])
    after_my_corner = corner_guard_count(after["my_guards"])
    my_guard_gain = max(0, len(after["my_guards"]) - len(before["my_guards"]))
    my_house_gain = max(0, len(after["my_house"]) - len(before["my_house"]))
    protected_gain = max(
        0,
        protected_house_count(after["my_house"], after["my_guards"])
        - protected_house_count(before["my_house"], before["my_guards"]),
    )
    freeze_gain = max(
        0,
        freeze_contact_count(after, "my") - freeze_contact_count(before, "my"),
    )
    closest_rank_delta = owner_rank(after["closest_owner"]) - owner_rank(before["closest_owner"])
    score_gain = score_delta(before, after)
    before_score = int(before["score_for_my"])

    guard_actions = {
        "center_guard",
        "center_guard_high",
        "center_guard_low",
        "corner_guard_left",
        "corner_guard_right",
        "corner_guard_left_high",
        "corner_guard_right_high",
        "guard_my_shot",
        "defense",
        "defense_push_in",
    }
    draw_actions = {
        "occupy",
        "middle_in_center",
        "default_draw",
        "draw_button",
        "draw_top4",
        "draw_back4",
        "come_around_left",
        "come_around_right",
        "around_guard_draw_left",
        "around_guard_draw_right",
    }
    freeze_actions = {"freeze", "freeze_no1", "freeze_no2"}

    if action_name in guard_actions:
        reward += setup_scale * 0.17 * my_guard_gain
        reward += setup_scale * 0.14 * max(0, after_my_center - before_my_center)
        reward += setup_scale * 0.12 * max(0, after_my_corner - before_my_corner)
        reward += setup_scale * 0.20 * protected_gain
        if action_name == "guard_my_shot":
            reward += setup_scale * 0.16 * protected_gain
        if shot_num <= 8 and my_guard_gain == 0 and protected_gain == 0 and score_gain <= 0:
            reward -= 0.10

    if action_name in freeze_actions:
        freeze_scale = 0.65 + 0.35 * (1.0 - phase)
        reward += freeze_scale * 0.24 * freeze_gain
        if closest_rank_delta > 0:
            reward += 0.14
        if freeze_gain == 0 and score_gain <= 0 and closest_rank_delta <= 0:
            reward -= 0.08

    if action_name in draw_actions:
        reward += setup_scale * 0.12 * my_house_gain
        if closest_rank_delta > 0:
            reward += 0.16
        if action_name in {
            "come_around_left",
            "come_around_right",
            "around_guard_draw_left",
            "around_guard_draw_right",
        } and protected_gain > 0:
            reward += setup_scale * 0.10 * protected_gain
        if shot_num >= 12 and score_gain <= 0 and closest_rank_delta <= 0:
            reward -= 0.14

    if late_pressure and action_name in guard_actions.union(draw_actions):
        if score_gain <= 0 and closest_rank_delta <= 0:
            pressure_penalty = 0.28 + 0.07 * max(0, -before_score)
            if endgame_pressure:
                pressure_penalty += 0.16
            if action_name in guard_actions:
                pressure_penalty += 0.08
            if action_name in {
                "come_around_left",
                "come_around_right",
                "around_guard_draw_left",
                "around_guard_draw_right",
            }:
                pressure_penalty += 0.06
            if action_name in {"middle_in_center", "draw_back4", "draw_top4", "draw_button"}:
                pressure_penalty += 0.04
            reward -= pressure_penalty
        else:
            reward += 0.08 + (0.05 if endgame_pressure else 0.0)

    if (
        shot_num >= 12
        and action_name in guard_actions
        and my_guard_gain > 0
        and score_gain <= 0
        and closest_rank_delta <= 0
    ):
        reward -= 0.18

    if (
        shot_num >= 12
        and action_name in draw_actions
        and before["closest_owner"] == "opp"
        and score_gain <= 0
        and closest_rank_delta <= 0
    ):
        reward -= 0.16

    return clamp(reward, -1.3, 1.35)


def situation_evaluation_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
) -> float:
    return board_value(after_position, player_is_init, shot_num) - board_value(
        before_position, player_is_init, shot_num
    )


def strategic_match_context_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    action_name: str,
    *,
    current_end: int,
    total_ends: int,
    cumulative_score_diff: int,
) -> float:
    """Outcome reward for two match contexts missing from generic board shaping."""
    if total_ends <= 0 or current_end <= 0:
        return 0.0
    before = summarize_position(before_position, player_is_init)
    after = summarize_position(after_position, player_is_init)
    reward = 0.0

    late_match = current_end >= max(1, total_ends - 1)
    before_protected = protected_house_count(before["my_house"], before["my_guards"])
    after_protected = protected_house_count(after["my_house"], after["my_guards"])
    protect_context = (
        late_match
        and cumulative_score_diff >= 2
        and int(before["score_for_my"]) > 0
        and before["closest_owner"] == "my"
        and before_protected > 0
    )
    if protect_context:
        reward += 0.55 * (after_protected - before_protected)
        reward += 0.28 * (len(after["my_house"]) - len(before["my_house"]))
        reward += 0.18 * score_delta(before, after)
        if (
            action_name in {"raise_takeout", "runback_takeout", "double_hit", "push_in_14"}
            and (after_protected < before_protected or int(after["score_for_my"]) < int(before["score_for_my"]))
        ):
            reward -= 0.35

    build_context = (
        current_end >= total_ends
        and cumulative_score_diff <= -2
        and not player_is_init
        and shot_num >= 8
    )
    if build_context:
        required = min(4, max(2, -int(cumulative_score_diff)))
        before_capacity = min(required, len(before["my_house"]))
        after_capacity = min(required, len(after["my_house"]))
        opponent_removed = max(0, len(before["opp_house"]) - len(after["opp_house"]))
        score_gain = score_delta(before, after)
        reward += 0.38 * (after_capacity - before_capacity)
        reward += 0.22 * score_gain
        reward -= 0.30 * max(0, len(before["my_house"]) - len(after["my_house"]))
        if action_name in HIT_ACTIONS and opponent_removed == 0 and score_gain <= 0 and after_capacity <= before_capacity:
            reward -= 0.28
        if action_name in GUARD_HIT_ACTIONS and opponent_removed == 0:
            reward -= 0.18

    # A late end with multiple opponent counters is a tactical emergency even
    # outside the final match end.  Clearing a front guard without changing
    # that scoring cluster is often the exact failure mode we want to avoid.
    # Keep this outcome-based: a hit remains valid when it actually reduces
    # the house threat or improves the current score.
    late_end_multi_stone_threat = (
        shot_num >= 12
        and int(before["score_for_my"]) < 0
        and len(before["opp_house"]) >= 2
    )
    if late_end_multi_stone_threat and action_name in HIT_ACTIONS:
        house_reduced = max(0, len(before["opp_house"]) - len(after["opp_house"]))
        score_improved = int(after["score_for_my"]) > int(before["score_for_my"])
        if house_reduced > 0 or score_improved:
            reward += 0.30 + 0.12 * min(house_reduced, 2)
            if score_improved:
                reward += 0.10
        else:
            reward -= 0.42
            if action_name in GUARD_HIT_ACTIONS:
                reward -= 0.28

    return clamp(reward, -1.2, 1.2)


def score_delta(before_summary: Dict[str, object], after_summary: Dict[str, object]) -> int:
    return int(after_summary["score_for_my"]) - int(before_summary["score_for_my"])


def hit_outcome_metrics(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
) -> Dict[str, float]:
    before = summarize_position(before_position, player_is_init)
    after = summarize_position(after_position, player_is_init)
    before_closest = before["house_stones"][0] if before["house_stones"] else None
    after_closest = after["house_stones"][0] if after["house_stones"] else None
    nearest_opp = nearest_opponent_stone(before)
    blocked_threat_target, blocked_threat_guards = blocked_house_threat(before)
    closest_my_before = before["my_house"][0] if before["my_house"] else None

    before_house_count = len(before["house_stones"])
    after_house_count = len(after["house_stones"])
    before_my_stones = sum(1 for stone in before["stones"] if stone.owner == "my")
    after_my_stones = sum(1 for stone in after["stones"] if stone.owner == "my")
    before_opp_stones = sum(1 for stone in before["stones"] if stone.owner == "opp")
    after_opp_stones = sum(1 for stone in after["stones"] if stone.owner == "opp")
    opp_house_removed = max(0, len(before["opp_house"]) - len(after["opp_house"]))
    my_house_lost = max(0, len(before["my_house"]) - len(after["my_house"]))
    my_house_added = max(0, len(after["my_house"]) - len(before["my_house"]))
    opp_house_added = max(0, len(after["opp_house"]) - len(before["opp_house"]))
    opp_guard_removed = max(0, len(before["opp_guards"]) - len(after["opp_guards"]))
    my_guard_lost = max(0, len(before["my_guards"]) - len(after["my_guards"]))
    opp_stones_removed = max(0, before_opp_stones - after_opp_stones)
    my_stones_lost = max(0, before_my_stones - after_my_stones)
    my_protected_house_lost = max(
        0,
        protected_house_count(before["my_house"], before["my_guards"])
        - protected_house_count(after["my_house"], after["my_guards"]),
    )
    opp_protected_house_removed = max(
        0,
        protected_house_count(before["opp_house"], before["opp_guards"])
        - protected_house_count(after["opp_house"], after["opp_guards"]),
    )
    before_my_structure = (
        len(before["my_guards"])
        + protected_house_count(before["my_house"], before["my_guards"])
        + freeze_contact_count(before, "my")
    )
    after_my_structure = (
        len(after["my_guards"])
        + protected_house_count(after["my_house"], after["my_guards"])
        + freeze_contact_count(after, "my")
    )
    before_opp_structure = (
        len(before["opp_guards"])
        + protected_house_count(before["opp_house"], before["opp_guards"])
        + freeze_contact_count(before, "opp")
    )
    after_opp_structure = (
        len(after["opp_guards"])
        + protected_house_count(after["opp_house"], after["opp_guards"])
        + freeze_contact_count(after, "opp")
    )

    closest_rank_delta = owner_rank(after["closest_owner"]) - owner_rank(before["closest_owner"])
    score_change = score_delta(before, after)
    opp_shot_removed = 0.0
    if before_closest is not None and before_closest.owner == "opp":
        same_after = stone_by_index(after, before_closest.index)
        if same_after is None or not is_house(same_after.x, same_after.y):
            opp_shot_removed = 1.0
        elif after_closest is None or after_closest.owner != "opp":
            opp_shot_removed = 1.0

    my_shot_lost = 0.0
    if closest_my_before is not None:
        same_after = stone_by_index(after, closest_my_before.index)
        if same_after is None or not is_house(same_after.x, same_after.y):
            my_shot_lost = 1.0
        elif after_closest is None or after_closest.owner != "my":
            my_shot_lost = 1.0

    nearest_was_only_guard = (
        nearest_opp is not None
        and is_guard_zone(nearest_opp.x, nearest_opp.y)
        and not is_house(nearest_opp.x, nearest_opp.y)
        and opp_guard_removed > 0
        and opp_house_removed == 0
    )
    target_was_house = nearest_opp is not None and is_house(nearest_opp.x, nearest_opp.y)
    target_was_center_guard = nearest_opp is not None and is_center_guard(nearest_opp.x, nearest_opp.y)
    target_protection = protection_count(nearest_opp, before["opp_guards"]) if nearest_opp else 0
    target_was_current_shot = (
        nearest_opp is not None
        and before_closest is not None
        and before_closest.owner == "opp"
        and before_closest.index == nearest_opp.index
    )
    before_score_for_my = int(before["score_for_my"])
    after_score_for_my = int(after["score_for_my"])
    urgent_hit = shot_num >= 10 and (
        before_score_for_my < 0 or before["closest_owner"] == "opp"
    )
    blocked_multi_stone_threat = (
        shot_num >= 12
        and before_score_for_my < 0
        and len(before["opp_house"]) >= 2
        and blocked_threat_target is not None
        and bool(blocked_threat_guards)
    )

    return {
        "board_delta": float(
            board_value(after_position, player_is_init, shot_num)
            - board_value(before_position, player_is_init, shot_num)
        ),
        "score_delta": float(score_change),
        "before_score_for_my": float(before_score_for_my),
        "after_score_for_my": float(after_score_for_my),
        "opp_score_threat": float(max(0, -before_score_for_my)),
        "before_house_count": float(before_house_count),
        "after_house_count": float(after_house_count),
        "house_cleared": 1.0 if before_house_count > 0 and after_house_count == 0 else 0.0,
        "after_house_empty": 1.0 if after_house_count == 0 else 0.0,
        "opp_stones_removed": float(opp_stones_removed),
        "my_stones_lost": float(my_stones_lost),
        "opp_house_removed": float(opp_house_removed),
        "my_house_lost": float(my_house_lost),
        "my_house_added": float(my_house_added),
        "opp_house_added": float(opp_house_added),
        "opp_guard_removed": float(opp_guard_removed),
        "my_guard_lost": float(my_guard_lost),
        "my_protected_house_lost": float(my_protected_house_lost),
        "opp_protected_house_removed": float(opp_protected_house_removed),
        "my_structure_lost": float(max(0, before_my_structure - after_my_structure)),
        "opp_structure_removed": float(max(0, before_opp_structure - after_opp_structure)),
        "closest_rank_delta": float(closest_rank_delta),
        "opp_shot_removed": opp_shot_removed,
        "my_shot_lost": my_shot_lost,
        "nearest_was_only_guard": 1.0 if nearest_was_only_guard else 0.0,
        "early_shot": 1.0 if shot_num <= 6 else 0.0,
        "mid_or_early_shot": 1.0 if shot_num < 12 else 0.0,
        "late_shot": 1.0 if shot_num >= 10 else 0.0,
        "endgame_shot": 1.0 if shot_num >= 12 else 0.0,
        "urgent_hit": 1.0 if urgent_hit else 0.0,
        "target_was_house": 1.0 if target_was_house else 0.0,
        "target_was_center_guard": 1.0 if target_was_center_guard else 0.0,
        "target_was_current_shot": 1.0 if target_was_current_shot else 0.0,
        "target_was_protected": 1.0 if target_protection > 0 else 0.0,
        "target_was_exposed": 1.0 if nearest_opp is not None and target_protection == 0 else 0.0,
        "blocked_house_threat": 1.0 if blocked_threat_target is not None else 0.0,
        "blocked_multi_stone_threat": 1.0 if blocked_multi_stone_threat else 0.0,
        "threat_house_reduced": 1.0 if len(after["opp_house"]) < len(before["opp_house"]) else 0.0,
    }


def hit_outcome_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    action_name: str,
) -> float:
    if action_name not in HIT_ACTIONS:
        return 0.0

    is_house_hit = action_name in HOUSE_HIT_ACTIONS
    is_guard_hit = action_name in GUARD_HIT_ACTIONS
    is_soft_displacement = action_name in SOFT_DISPLACEMENT_ACTIONS
    has_hammer = not player_is_init
    multiplier = 1.0
    if is_guard_hit:
        multiplier = 0.85
    elif is_soft_displacement:
        multiplier = 0.82

    metrics = hit_outcome_metrics(
        before_position=before_position,
        after_position=after_position,
        player_is_init=player_is_init,
        shot_num=shot_num,
    )

    reward = 0.0
    score_weight = 0.46 + 0.12 * metrics["urgent_hit"] + 0.09 * metrics["endgame_shot"]
    reward += score_weight * metrics["score_delta"]
    if metrics["closest_rank_delta"] > 0:
        reward += 0.46 + 0.14 * metrics["late_shot"]
    elif metrics["closest_rank_delta"] < 0:
        reward -= 0.40 + 0.14 * metrics["endgame_shot"]

    if is_house_hit:
        reward += 0.20 * metrics["opp_house_removed"]
        reward += 0.60 * metrics["opp_shot_removed"]
        reward += 0.08 * metrics["opp_stones_removed"]
        reward += 0.18 * metrics["opp_protected_house_removed"]
        if metrics["target_was_current_shot"] and metrics["opp_shot_removed"]:
            reward += 0.38 + 0.18 * metrics["urgent_hit"]
        elif metrics["target_was_house"] and metrics["opp_house_removed"]:
            reward += 0.18
        if action_name == "double_hit" and metrics["opp_house_removed"] >= 2.0:
            reward += 0.22
        if action_name in {"hit_roll", "hit_roll_left", "hit_roll_right", "hit_and_stay"} and metrics["my_house_added"] > 0:
            reward += 0.18
        if action_name in {"raise_takeout", "runback_takeout"} and metrics["closest_rank_delta"] > 0:
            reward += 0.16

    if is_guard_hit:
        reward += 0.07 * metrics["opp_guard_removed"]
        reward += 0.17 * metrics["opp_protected_house_removed"]
        if metrics["target_was_center_guard"] and (shot_num >= 8 or metrics["urgent_hit"]):
            reward += 0.08
        if metrics["nearest_was_only_guard"] and metrics["score_delta"] <= 0:
            penalty = 0.13 if metrics["target_was_center_guard"] else 0.22
            if metrics["early_shot"] and not metrics["urgent_hit"]:
                penalty += 0.10
            reward -= penalty

    if is_soft_displacement:
        reward += 0.18 * metrics["opp_house_removed"]
        if metrics["score_delta"] > 0 or metrics["closest_rank_delta"] > 0:
            reward += 0.22 + 0.10 * metrics["late_shot"]
        if metrics["my_house_added"] > 0 and metrics["my_house_lost"] == 0:
            reward += 0.12
        if action_name == "double_push_in" and metrics["score_delta"] > 0:
            reward += 0.13
        if action_name == "tap_back" and metrics["my_house_added"] > 0:
            reward += 0.16

    reward -= (0.32 + 0.10 * metrics["endgame_shot"]) * metrics["my_house_lost"]
    reward -= (0.45 + 0.16 * metrics["endgame_shot"]) * metrics["my_shot_lost"]
    reward -= 0.34 * metrics["my_protected_house_lost"]
    reward -= (0.09 if not is_soft_displacement else 0.05) * metrics["my_stones_lost"]

    if metrics["early_shot"] and metrics["score_delta"] <= 0:
        guard_loss_weight = 0.28 if is_guard_hit else 0.20
        reward -= guard_loss_weight * metrics["my_guard_lost"]
    if is_guard_hit and metrics["my_structure_lost"] > 0:
        reward -= 0.10 * metrics["my_structure_lost"]

    productive_hit = (
        metrics["score_delta"] > 0
        or metrics["closest_rank_delta"] > 0
        or metrics["opp_shot_removed"] > 0
        or metrics["opp_house_removed"] > 0
        or metrics["opp_protected_house_removed"] > 0
    )
    decisive_hit = (
        metrics["score_delta"] > 0
        or metrics["closest_rank_delta"] > 0
        or metrics["opp_shot_removed"] > 0
        or metrics["opp_protected_house_removed"] > 0
    )
    if is_house_hit and decisive_hit and (metrics["late_shot"] or metrics["urgent_hit"]):
        reward += 0.20 + 0.07 * min(metrics["opp_score_threat"], 3.0)
        if metrics["target_was_house"]:
            reward += 0.10
        if metrics["score_delta"] > 0 and metrics["my_shot_lost"] == 0:
            reward += 0.14
        if metrics["before_score_for_my"] < 0.0 and metrics["after_score_for_my"] >= 0.0:
            reward += 0.22
    if (
        is_house_hit
        and metrics["target_was_house"]
        and not productive_hit
        and metrics["score_delta"] <= 0
    ):
        reward -= 0.30 + 0.10 * metrics["late_shot"]
    if (
        metrics["urgent_hit"]
        and (is_house_hit or is_soft_displacement)
        and not productive_hit
    ):
        reward -= 0.32 + 0.08 * min(metrics["opp_score_threat"], 3.0)

    # In the final stones, a central guard may hide several opponent scoring
    # stones. Reward a real reduction of that threat, but penalize a shot that
    # only clears the guard and leaves the scoring cluster intact.
    if metrics["blocked_multi_stone_threat"]:
        if metrics["threat_house_reduced"]:
            reward += 0.28 + 0.10 * min(metrics["opp_house_removed"], 2.0)
            if metrics["score_delta"] > 0:
                reward += 0.18
        elif metrics["opp_guard_removed"] > 0 and metrics["score_delta"] <= 0:
            reward -= 1.00
    if (
        not productive_hit
        and metrics["mid_or_early_shot"]
        and not metrics["urgent_hit"]
        and (is_house_hit or is_guard_hit)
    ):
        penalty = 0.24
        if is_guard_hit or not metrics["target_was_house"]:
            penalty += 0.07
        if metrics["early_shot"] and metrics["target_was_exposed"]:
            penalty += 0.06
        reward -= penalty

    if (
        is_house_hit
        and metrics["mid_or_early_shot"]
        and not metrics["urgent_hit"]
        and not decisive_hit
    ):
        penalty = 0.12 + 0.08 * metrics["early_shot"]
        if not metrics["target_was_protected"]:
            penalty += 0.06
        if metrics["target_was_exposed"]:
            penalty += 0.04
        reward -= penalty

    if (
        (is_house_hit or is_guard_hit)
        and metrics["house_cleared"]
        and metrics["score_delta"] <= 0
    ):
        penalty = 0.20 if has_hammer and shot_num < 10 else 0.34
        if metrics["my_structure_lost"] > 0:
            penalty += 0.06
        reward -= penalty

    if (
        (is_house_hit or is_guard_hit)
        and metrics["after_house_empty"]
        and metrics["before_house_count"] == 0
        and metrics["opp_guard_removed"] > 0
        and metrics["score_delta"] <= 0
        and metrics["mid_or_early_shot"]
        and not metrics["urgent_hit"]
    ):
        reward -= 0.18

    scaled_reward = multiplier * reward
    if (
        metrics["blocked_multi_stone_threat"]
        and not metrics["threat_house_reduced"]
        and metrics["opp_guard_removed"] > 0
        and metrics["score_delta"] <= 0
    ):
        combined_reward = SER_WEIGHT * metrics["board_delta"] + scaled_reward
        if combined_reward > -0.15:
            scaled_reward -= combined_reward + 0.15

    return clamp(scaled_reward, -2.6, 2.4)


def terminal_score_reward(end_score: int = 0) -> float:
    score = float(end_score)
    if score < 0.0:
        return score - 0.35 * max(0.0, -score - 1.0)
    if score > 1.0:
        return score + 0.12 * min(score - 1.0, 2.0)
    return score


def future_reward(is_end: bool = False, end_score: int = 0) -> float:
    return terminal_score_reward(end_score) if is_end else 0.0


def shaped_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    is_end: bool = False,
    end_score: int = 0,
    invalid_action: bool = False,
    fallback_draw: bool = False,
    ser_weight: float = SER_WEIGHT,
    fr_weight: float = FR_WEIGHT,
    invalid_action_penalty: float = INVALID_ACTION_PENALTY,
    fallback_draw_penalty: float = FALLBACK_DRAW_PENALTY,
) -> float:
    ser = situation_evaluation_reward(
        before_position=before_position,
        after_position=after_position,
        player_is_init=player_is_init,
        shot_num=shot_num,
    )
    fr = future_reward(is_end=is_end, end_score=end_score)
    reward = ser_weight * ser + fr_weight * fr
    if invalid_action:
        reward -= invalid_action_penalty
    if fallback_draw:
        reward -= fallback_draw_penalty
    return max(-5.0, min(5.0, reward))


def row_player_is_init(row: Dict[str, str]) -> bool:
    # In this local setup player1 starts first in infinite mode; this matches
    # how our current parser labels tactics data.
    return row.get("player_label") == "player1"


def state_from_row(row: Dict[str, str], use_after: bool = False) -> List[float]:
    key = "position_after_json" if use_after else "position_before_json"
    position = parse_position_json(row.get(key, ""))
    return build_state(
        position=position,
        player_is_init=row_player_is_init(row),
        shot_num=int(float(row.get("state_shot") or 0)),
        end_score=int(float(row.get("state_score") or 0)),
        total_ends=int(float(row.get("state_total_ends") or -1)),
        current_player=int(float(row.get("state_current_player") or 0)),
    )


def reward_from_row(row: Dict[str, str]) -> float:
    before_position = parse_position_json(row.get("position_before_json", ""))
    after_position = parse_position_json(row.get("position_after_json", ""))
    round_score_raw = row.get("round_score_points_for_player")
    is_end = round_score_raw not in ("", None)
    end_score = int(float(round_score_raw)) if is_end else 0
    reward = shaped_reward(
        before_position=before_position,
        after_position=after_position,
        player_is_init=row_player_is_init(row),
        shot_num=int(float(row.get("state_shot") or 0)),
        is_end=is_end,
        end_score=end_score,
    )
    reward += hit_outcome_reward(
        before_position=before_position,
        after_position=after_position,
        player_is_init=row_player_is_init(row),
        shot_num=int(float(row.get("state_shot") or 0)),
        action_name=row.get("selected_tactic") or "",
    )
    reward += setup_outcome_reward(
        before_position=before_position,
        after_position=after_position,
        player_is_init=row_player_is_init(row),
        shot_num=int(float(row.get("state_shot") or 0)),
        action_name=row.get("selected_tactic") or "",
    )
    return clamp(reward, -5.0, 5.0)
