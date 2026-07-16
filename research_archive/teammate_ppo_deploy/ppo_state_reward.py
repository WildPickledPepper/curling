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

HIT_CONTEXT_DIM = 12
TACTICAL_CONTEXT_DIM = 16
STATE_DIM = 16 * 5 + 8 + HIT_CONTEXT_DIM + TACTICAL_CONTEXT_DIM
SER_WEIGHT = 0.9
FR_WEIGHT = 0.1
INVALID_ACTION_PENALTY = 1.0
FALLBACK_DRAW_PENALTY = 1.5


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

    return target_features + [
        clamp(max(0, -score_for_my) / 8.0, 0.0, 1.0),
        clamp((my_house - opp_house) / 8.0, -1.0, 1.0),
        clamp((my_guards - opp_guards) / 8.0, -1.0, 1.0),
        1.0 if shot_num >= 12 else 0.0,
        1.0 if urgent_hit else 0.0,
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

    value = ayumu_expected_end_value(summary, player_is_init, shot_num)
    value += my_house * 0.06
    value -= opp_house * 0.07
    if closest_owner == "my":
        value += 0.12
    elif closest_owner == "opp":
        value -= 0.12

    if shot_num <= 6:
        value += my_guards * 0.08
        value -= opp_guards * 0.07
        value += my_center_guards * 0.06
        value -= opp_center_guards * 0.07
    else:
        value += my_guards * 0.03
        value -= opp_guards * 0.04

    if closest_owner == "my":
        value += min(closest_my_protection, 2) * 0.05
    elif closest_owner == "opp":
        value -= min(closest_opp_protection, 2) * 0.06

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
        value += early_weight * (0.07 * my_center_guards + 0.11 * my_corner_guards)
        value -= early_weight * (0.09 * opp_center_guards + 0.08 * opp_corner_guards)
    else:
        value += early_weight * (0.13 * my_center_guards + 0.06 * my_corner_guards)
        value -= early_weight * (0.12 * opp_center_guards + 0.07 * opp_corner_guards)

    value += 0.16 * my_protected_house
    value -= 0.17 * opp_protected_house
    value += min(closest_my_protection, 2) * (0.09 + 0.05 * late_weight)
    value -= min(closest_opp_protection, 2) * (0.10 + 0.05 * late_weight)

    my_freezes = freeze_contact_count(summary, "my")
    opp_freezes = freeze_contact_count(summary, "opp")
    value += min(my_freezes, 2) * (0.11 + 0.05 * late_weight)
    value -= min(opp_freezes, 2) * (0.11 + 0.05 * late_weight)

    if closest_my is not None:
        tee_strength = 1.0 - clamp(closest_my.dist / IN_HOUSE_R, 0.0, 1.0)
        value += (0.08 + 0.08 * late_weight) * tee_strength
    if closest_opp is not None:
        tee_strength = 1.0 - clamp(closest_opp.dist / IN_HOUSE_R, 0.0, 1.0)
        value -= (0.09 + 0.08 * late_weight) * tee_strength

    return clamp(value, -3.0, 3.0)


def delayed_setup_reward(
    before_position: Sequence[float],
    after_own_position: Sequence[float],
    after_response_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    weight: float = 0.25,
    max_abs: float = 0.75,
) -> float:
    before_value = setup_value(before_position, player_is_init, shot_num)
    after_own_value = setup_value(after_own_position, player_is_init, shot_num)
    after_response_value = setup_value(after_response_position, player_is_init, min(15, shot_num + 1))
    survived_gain = after_response_value - before_value
    fragility_penalty = max(0.0, after_own_value - after_response_value)
    reward = weight * (survived_gain - 0.35 * fragility_penalty)
    return clamp(reward, -max_abs, max_abs)


def situation_evaluation_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
) -> float:
    return board_value(after_position, player_is_init, shot_num) - board_value(
        before_position, player_is_init, shot_num
    )


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
    closest_my_before = before["my_house"][0] if before["my_house"] else None

    opp_house_removed = max(0, len(before["opp_house"]) - len(after["opp_house"]))
    my_house_lost = max(0, len(before["my_house"]) - len(after["my_house"]))
    opp_guard_removed = max(0, len(before["opp_guards"]) - len(after["opp_guards"]))
    my_guard_lost = max(0, len(before["my_guards"]) - len(after["my_guards"]))
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

    closest_rank_delta = owner_rank(after["closest_owner"]) - owner_rank(before["closest_owner"])
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

    return {
        "score_delta": float(score_delta(before, after)),
        "opp_house_removed": float(opp_house_removed),
        "my_house_lost": float(my_house_lost),
        "opp_guard_removed": float(opp_guard_removed),
        "my_guard_lost": float(my_guard_lost),
        "my_protected_house_lost": float(my_protected_house_lost),
        "opp_protected_house_removed": float(opp_protected_house_removed),
        "closest_rank_delta": float(closest_rank_delta),
        "opp_shot_removed": opp_shot_removed,
        "my_shot_lost": my_shot_lost,
        "nearest_was_only_guard": 1.0 if nearest_was_only_guard else 0.0,
        "early_shot": 1.0 if shot_num <= 6 else 0.0,
        "target_was_house": 1.0 if target_was_house else 0.0,
        "target_was_center_guard": 1.0 if target_was_center_guard else 0.0,
        "target_was_current_shot": 1.0 if target_was_current_shot else 0.0,
        "target_was_protected": 1.0 if target_protection > 0 else 0.0,
        "target_was_exposed": 1.0 if nearest_opp is not None and target_protection == 0 else 0.0,
    }


def hit_outcome_reward(
    before_position: Sequence[float],
    after_position: Sequence[float],
    player_is_init: bool,
    shot_num: int,
    action_name: str,
) -> float:
    strong_hit_actions = {"take_out", "hit_roll", "double_hit", "clear"}
    soft_hit_actions = {"push_in", "push_in_14", "double_push_in"}
    if action_name not in strong_hit_actions and action_name not in soft_hit_actions:
        return 0.0

    multiplier = 1.0 if action_name in strong_hit_actions else 0.6
    metrics = hit_outcome_metrics(
        before_position=before_position,
        after_position=after_position,
        player_is_init=player_is_init,
        shot_num=shot_num,
    )

    reward = 0.0
    reward += 0.35 * metrics["score_delta"]
    reward += 0.18 * metrics["opp_house_removed"]
    reward += 0.30 * metrics["opp_shot_removed"]
    reward += 0.08 * metrics["opp_protected_house_removed"]
    if metrics["target_was_current_shot"] and metrics["opp_shot_removed"]:
        reward += 0.18
    elif metrics["target_was_house"] and metrics["opp_house_removed"]:
        reward += 0.10
    if metrics["closest_rank_delta"] > 0:
        reward += 0.25
    elif metrics["closest_rank_delta"] < 0:
        reward -= 0.20
    reward -= 0.20 * metrics["my_house_lost"]
    reward -= 0.20 * metrics["my_shot_lost"]
    reward -= 0.15 * metrics["my_protected_house_lost"]

    if metrics["early_shot"] and metrics["score_delta"] <= 0:
        reward -= 0.15 * metrics["my_guard_lost"]
    if metrics["nearest_was_only_guard"] and metrics["score_delta"] <= 0:
        penalty = 0.20 if metrics["target_was_center_guard"] else 0.30
        reward -= penalty
    if (
        not metrics["target_was_house"]
        and metrics["score_delta"] <= 0
        and metrics["closest_rank_delta"] <= 0
        and shot_num < 12
    ):
        reward -= 0.15

    return multiplier * clamp(reward, -2.0, 2.0)


def future_reward(is_end: bool = False, end_score: int = 0) -> float:
    return float(end_score) if is_end else 0.0


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
    return clamp(reward, -5.0, 5.0)
