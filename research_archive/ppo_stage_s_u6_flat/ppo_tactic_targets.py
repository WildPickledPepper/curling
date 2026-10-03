"""Target-conditioned execution for the reliable direct-hit tactic families.

The legacy tactic library selects the nearest target internally.  This module
exposes the same direct-hit geometry behind an explicit stone-slot target so a
future factorised PPO actor can choose both a tactic family and a target.
Only actions with an unambiguous, validated direct-hit contract belong here.
"""

from __future__ import annotations

import sys
import math
from pathlib import Path
from typing import List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parent
TACTICSLIB = ROOT / "tacticslib"
if str(TACTICSLIB) not in sys.path:
    sys.path.insert(0, str(TACTICSLIB))

import strategy_library as strategy


TARGETED_DIRECT_HIT_ACTIONS = frozenset({
    "take_out",
    "take_out_house",
    "take_out_guard",
    "peel_guard",
    "hit_and_stay",
    "around_guard_takeout_left",
    "around_guard_takeout_right",
})

# These families require a target and a distinct middle stone. They are not
# wired into PPO sampling yet; this module first makes every chosen pair
# physically executable and auditable in the local simulator.
TARGETED_RELAY_ACTIONS = frozenset({
    "raise_takeout",
    "runback_takeout",
    "push_in",
})

TARGETED_DOUBLE_ACTIONS = frozenset({"double_hit"})

HIT_ROLL_TARGET_ACTIONS = frozenset({
    "hit_roll", "hit_roll_left", "hit_roll_right",
})


def position_to_state_list(position: Sequence[float]) -> List[List[float]]:
    if len(position) < 32:
        raise ValueError("target-conditioned tactics require 16 stone slots")
    return [
        [float(position[index * 2]), float(position[index * 2 + 1])]
        for index in range(16)
    ]


def _is_active(stone: Sequence[float]) -> bool:
    return float(stone[0]) != 0.0 or float(stone[1]) != 0.0


def _owner_is_opponent(index: int, player_is_first: bool) -> bool:
    own_parity = 0 if player_is_first else 1
    return index % 2 != own_parity


def target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Return the exact selectable target slots for a direct-hit family."""
    if action_name not in TARGETED_DIRECT_HIT_ACTIONS:
        return [False] * 16
    state = position_to_state_list(position)
    mask: List[bool] = []
    for index, stone in enumerate(state):
        eligible = _owner_is_opponent(index, player_is_first) and _is_active(stone)
        if action_name in {
            "take_out", "take_out_house", "hit_and_stay",
            "around_guard_takeout_left", "around_guard_takeout_right",
        }:
            eligible = eligible and bool(strategy.bl.House(stone))
        else:
            eligible = eligible and bool(strategy._is_guard(stone))
        mask.append(bool(eligible))
    return mask


def bestshot_for_target(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    shot_num: int = 14,
) -> Optional[Tuple[float, float, float]]:
    """Resolve a validated direct-hit action against one physical stone slot."""
    if action_name in HIT_ROLL_TARGET_ACTIONS:
        return hit_roll_bestshot_for_target(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            shot_num=shot_num,
            target_index=target_index,
        )
    if action_name not in TARGETED_DIRECT_HIT_ACTIONS:
        return None
    if not 0 <= int(target_index) < 16:
        return None
    mask = target_mask(
        position,
        action_name=action_name,
        player_is_first=player_is_first,
    )
    if not mask[int(target_index)]:
        return None
    state = position_to_state_list(position)
    is_init = 0 if player_is_first else 1
    _, state_me = strategy._split_stones(state, is_init)
    if action_name.startswith("around_guard_takeout_"):
        side = -1 if action_name.endswith("left") else 1
        result = strategy.bypass_takeout_for_target(
            state, is_init, state[int(target_index)], side, shot_num=14,
        )
    else:
        velocity = 8.0 if action_name == "peel_guard" else 5.7 if action_name == "hit_and_stay" else 6.0
        result = strategy._direct_hit_target(
            state,
            state_me,
            state[int(target_index)],
            velocity=velocity,
        )
    if result is None or result == 0 or len(result) < 3:
        return None
    return tuple(float(value) for value in result[:3])


def executable_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Keep only eligible target slots with a direct, executable BESTSHOT."""
    eligible = target_mask(
        position,
        action_name=action_name,
        player_is_first=player_is_first,
    )
    return [
        bool(enabled) and bestshot_for_target(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            target_index=index,
        ) is not None
        for index, enabled in enumerate(eligible)
    ]


def hit_roll_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Opponent slots eligible for a target-conditioned hit-and-roll probe."""
    if action_name not in HIT_ROLL_TARGET_ACTIONS:
        return [False] * 16
    state = position_to_state_list(position)
    return [
        bool(_owner_is_opponent(index, player_is_first) and _is_active(stone))
        for index, stone in enumerate(state)
    ]


def hit_roll_bestshot_for_target(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    shot_num: int,
    target_index: int,
) -> Optional[Tuple[float, float, float]]:
    """Resolve one legacy hit-roll geometry against an explicit stone slot.

    The legacy function retains every stone as a path/collision constraint and
    only restricts its candidate-selection loop to ``target_index``.  With no
    explicit target the legacy action remains unchanged.
    """
    if action_name not in HIT_ROLL_TARGET_ACTIONS or not 0 <= int(target_index) < 16:
        return None
    if not hit_roll_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )[int(target_index)]:
        return None
    state = position_to_state_list(position)
    result = strategy.hit_roll(
        state,
        0 if player_is_first else 1,
        int(shot_num),
        target_stone=state[int(target_index)],
    )
    if result is None or result == 0 or len(result) < 3:
        return None
    result = [float(value) for value in result[:3]]
    if action_name == "hit_roll_left":
        result[1] -= 0.08
    elif action_name == "hit_roll_right":
        result[1] += 0.08
    return tuple(result)


def executable_hit_roll_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    shot_num: int,
) -> List[bool]:
    """Keep only slots for which the target-conditioned hit-roll is routable."""
    eligible = hit_roll_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )
    return [
        bool(enabled) and hit_roll_bestshot_for_target(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            shot_num=shot_num,
            target_index=index,
        ) is not None
        for index, enabled in enumerate(eligible)
    ]


def legacy_hit_roll_target_index(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    shot_num: int,
) -> Optional[int]:
    """Return the slot selected by the unchanged legacy hit-roll tactic.

    Each explicit-target candidate uses the same legacy geometric code with
    the target loop restricted to one stone. Matching its BESTSHOT against
    the unrestricted legacy result gives an exact deterministic prior without
    removing any blockers from the board.
    """
    if action_name not in HIT_ROLL_TARGET_ACTIONS:
        return None
    state = position_to_state_list(position)
    legacy = strategy.hit_roll(state, 0 if player_is_first else 1, int(shot_num))
    if legacy is None or legacy == 0 or len(legacy) < 3:
        return None
    legacy = [float(value) for value in legacy[:3]]
    if action_name == "hit_roll_left":
        legacy[1] -= 0.08
    elif action_name == "hit_roll_right":
        legacy[1] += 0.08
    candidates = executable_hit_roll_target_mask(
        position,
        action_name=action_name,
        player_is_first=player_is_first,
        shot_num=shot_num,
    )
    best_index = None
    best_error = float("inf")
    for index, enabled in enumerate(candidates):
        if not enabled:
            continue
        shot = hit_roll_bestshot_for_target(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            shot_num=shot_num,
            target_index=index,
        )
        error = sum(abs(float(left) - float(right)) for left, right in zip(shot, legacy))
        if error < best_error:
            best_error = error
            best_index = index
    return best_index if best_error < 1e-6 else None


def relay_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Eligible opposing house targets for an explicit relay delivery."""
    if action_name not in TARGETED_RELAY_ACTIONS:
        return [False] * 16
    state = position_to_state_list(position)
    return [
        bool(_owner_is_opponent(index, player_is_first) and _is_active(stone) and strategy.bl.House(stone))
        for index, stone in enumerate(state)
    ]


def _relay_middle_eligible(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    middle_index: int,
) -> bool:
    state = position_to_state_list(position)
    if not (0 <= int(target_index) < 16 and 0 <= int(middle_index) < 16):
        return False
    if not relay_target_mask(position, action_name=action_name, player_is_first=player_is_first)[int(target_index)]:
        return False
    if int(middle_index) == int(target_index) or not _is_active(state[int(middle_index)]):
        return False
    middle_is_opponent = _owner_is_opponent(int(middle_index), player_is_first)
    if action_name == "runback_takeout":
        if not middle_is_opponent:
            return False
    elif middle_is_opponent:
        return False
    target = state[int(target_index)]
    middle = state[int(middle_index)]
    return bool(middle[1] > target[1] + 2.0 * strategy.Stone_R and 0.545 < middle[0] < 4.205)


def bestshot_for_relay(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    middle_index: int,
) -> Optional[Tuple[float, float, float]]:
    """Resolve an explicitly selected target-middle relay pair.

    This is the pair-conditioned form of the geometric route used by the
    legacy raise/runback implementation. It rejects a blocked or shallow pair
    so callers can use it directly as a legal-pair mask.
    """
    if action_name not in TARGETED_RELAY_ACTIONS or not _relay_middle_eligible(
        position, action_name=action_name, player_is_first=player_is_first,
        target_index=target_index, middle_index=middle_index,
    ):
        return None
    state = position_to_state_list(position)
    target = state[int(target_index)]
    middle = state[int(middle_index)]
    dx = target[0] - middle[0]
    dy = target[1] - middle[1]
    norm = math.hypot(dx, dy)
    if norm < 1e-8 or dy >= -0.1:
        return None
    angle = math.atan2(abs(dy), max(abs(dx), 1e-8))
    if angle < math.radians(35):
        return None
    contact_x = middle[0] - 2.0 * strategy.Stone_R * dx / norm
    contact_y = middle[1] - 2.0 * strategy.Stone_R * dy / norm
    if not 0.545 < contact_x < 4.205:
        return None
    active = [stone for stone in state if _is_active(stone)]
    without_pair = [
        stone for index, stone in enumerate(state)
        if _is_active(stone) and index not in {int(target_index), int(middle_index)}
    ]
    if not strategy.bl.Roadjudge(middle, target, without_pair):
        return None
    if not strategy.bl.Roadjudge([contact_x, contact_y], [contact_x, 10.61], active):
        return None
    correction = 0.033 if dx > 0 else 0.017
    return (6.0, float(contact_x - 2.375 + correction), 0.0)


def executable_relay_middle_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
) -> List[bool]:
    """Selectable middle-stone slots for one explicitly selected target."""
    return [
        bestshot_for_relay(
            position, action_name=action_name, player_is_first=player_is_first,
            target_index=target_index, middle_index=index,
        ) is not None
        for index in range(16)
    ]


def executable_relay_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Keep only relay targets that have at least one routable middle stone."""
    eligible = relay_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )
    return [
        bool(enabled) and any(executable_relay_middle_mask(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            target_index=index,
        ))
        for index, enabled in enumerate(eligible)
    ]


def double_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Opponent house stones eligible to participate in an explicit double."""
    if action_name not in TARGETED_DOUBLE_ACTIONS:
        return [False] * 16
    state = position_to_state_list(position)
    return [
        bool(_owner_is_opponent(index, player_is_first) and _is_active(stone) and strategy.bl.House(stone))
        for index, stone in enumerate(state)
    ]


def _double_bestshot_order(
    state: Sequence[Sequence[float]],
    first_index: int,
    second_index: int,
) -> Optional[Tuple[float, float, float]]:
    """Legacy double geometry with an explicitly supplied ordered pair."""
    first = state[first_index]
    second = state[second_index]
    distance = float(strategy.bl.Dist(first, second))
    if distance < 1e-8 or float(strategy.bl.DistH(first)) >= 1.22:
        return None
    if not (
        second[1] > first[1]
        or (second[1] > 4.88 - 1.22 and float(strategy.bl.DistH(first)) < 1.83 + 1.8 * strategy.Stone_R)
    ):
        return None
    dx = second[0] - first[0]
    dy = second[1] - first[1]
    if abs(dx) < 1e-8:
        return None
    if distance > 2.0 * math.sqrt(2.0) * strategy.Stone_R:
        separation = math.sqrt(distance ** 2 - (2.0 * strategy.Stone_R) ** 2)
        theta = math.asin(2.0 * strategy.Stone_R / distance)
        alpha = math.acos(max(-1.0, min(1.0, dx / distance)))
        angle = theta + alpha
        delta_x = separation * math.cos(angle)
        delta_y = separation * math.sin(angle)
    else:
        theta = math.acos(distance / (4.0 * strategy.Stone_R))
        alpha = math.acos(max(-1.0, min(1.0, dx / distance)))
        angle = theta + alpha
        delta_x = 2.0 * strategy.Stone_R * math.cos(angle)
        delta_y = 2.0 * strategy.Stone_R * math.sin(angle)
    if angle < math.radians(25) and distance > 1.22:
        return None
    if distance > 2.6 and angle < math.radians(50):
        return None
    if distance > 1.22 + 1.83 and math.radians(50) <= angle < math.radians(75):
        return None
    if angle > math.radians(75):
        return None
    if dx > 0 and dy > 0:
        point = [first[0] + delta_x, first[1] + delta_y]
    elif dx > 0 and dy < 0:
        point = [second[0] - delta_x, first[1] + delta_y]
    elif dx < 0 and dy > 0:
        point = [first[0] - delta_x, first[1] + delta_y]
    else:
        point = [second[0] + delta_x, second[1] + delta_y]
    if not (strategy.bl.Roadjudge(point, first, state) and strategy.bl.Roadjudge(point, [point[0], 10.61], state)):
        return None
    correction = 0.017 if point[0] - second[0] > 0 else 0.033
    return (6.0, float(point[0] - 2.375 + correction), 0.0)


def bestshot_for_double(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    second_target_index: int,
) -> Optional[Tuple[float, float, float]]:
    """Resolve a selected unordered pair of opponent stones as a double hit."""
    if action_name not in TARGETED_DOUBLE_ACTIONS:
        return None
    if not (0 <= int(target_index) < 16 and 0 <= int(second_target_index) < 16):
        return None
    if int(target_index) == int(second_target_index):
        return None
    mask = double_target_mask(position, action_name=action_name, player_is_first=player_is_first)
    if not (mask[int(target_index)] and mask[int(second_target_index)]):
        return None
    state = position_to_state_list(position)
    # The pair is unordered from PPO's perspective. Try both physical orders;
    # the first valid route determines which stone is contacted first.
    for first_index, second_index in (
        (int(target_index), int(second_target_index)),
        (int(second_target_index), int(target_index)),
    ):
        result = _double_bestshot_order(state, first_index, second_index)
        if result is not None:
            return result
    return None


def executable_double_second_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
) -> List[bool]:
    """Legal second-target slots for one selected double pair endpoint."""
    return [
        bestshot_for_double(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            target_index=target_index,
            second_target_index=index,
        ) is not None
        for index in range(16)
    ]


def executable_double_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Keep only first selected endpoints that have a routable pair partner."""
    eligible = double_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )
    return [
        bool(enabled) and any(executable_double_second_mask(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            target_index=index,
        ))
        for index, enabled in enumerate(eligible)
    ]


def double_outcome(
    before_position: Sequence[float],
    after_position: Sequence[float],
    *,
    action_name: str,
    target_index: Optional[int],
    second_target_index: Optional[int],
) -> dict:
    """Label success only when both explicitly selected targets leave house."""
    if action_name not in TARGETED_DOUBLE_ACTIONS or target_index is None or second_target_index is None:
        return {"evaluable": False, "success": False}
    if not (0 <= int(target_index) < 16 and 0 <= int(second_target_index) < 16):
        return {"evaluable": False, "success": False}
    before = position_to_state_list(before_position)
    after = position_to_state_list(after_position)
    success = bool(
        strategy.bl.House(before[int(target_index)])
        and strategy.bl.House(before[int(second_target_index)])
        and not strategy.bl.House(after[int(target_index)])
        and not strategy.bl.House(after[int(second_target_index)])
    )
    return {"evaluable": True, "success": success}


def relay_outcome(
    before_position: Sequence[float],
    after_position: Sequence[float],
    *,
    action_name: str,
    target_index: Optional[int],
    middle_index: Optional[int],
) -> dict:
    """Label whether an explicitly selected relay pair met its contract."""
    if action_name not in TARGETED_RELAY_ACTIONS or target_index is None or middle_index is None:
        return {"evaluable": False, "success": False}
    if not (0 <= int(target_index) < 16 and 0 <= int(middle_index) < 16):
        return {"evaluable": False, "success": False}
    before = position_to_state_list(before_position)
    after = position_to_state_list(after_position)
    target_before = before[int(target_index)]
    target_after = after[int(target_index)]
    middle_before = before[int(middle_index)]
    middle_after = after[int(middle_index)]
    middle_motion = math.dist(middle_before, middle_after)
    success = bool(
        strategy.bl.House(target_before)
        and not strategy.bl.House(target_after)
        and middle_motion >= strategy.Stone_R
    )
    return {"evaluable": True, "success": success, "middle_motion": middle_motion}


def target_outcome(
    before_position: Sequence[float],
    after_position: Sequence[float],
    *,
    action_name: str,
    target_index: Optional[int],
    candidate_index: Optional[int] = None,
) -> dict:
    """Return a target-specific outcome label without assigning reward.

    The caller chooses whether and how to weight this evidence. Keeping the
    semantic label separate from reward avoids silently turning a new metric
    into a new shaping term during a diagnostic rollout.
    """
    if action_name not in TARGETED_DIRECT_HIT_ACTIONS or target_index is None:
        return {"evaluable": False, "success": False}
    if not 0 <= int(target_index) < 16:
        return {"evaluable": False, "success": False}
    before = position_to_state_list(before_position)
    after = position_to_state_list(after_position)
    target_before = before[int(target_index)]
    target_after = after[int(target_index)]
    if action_name in {"take_out", "take_out_house"}:
        success = bool(strategy.bl.House(target_before) and not strategy.bl.House(target_after))
    elif action_name in {"take_out_guard", "peel_guard"}:
        success = bool(strategy._is_guard(target_before) and not strategy._is_guard(target_after))
    else:
        candidate_ok = False
        if candidate_index is not None and 0 <= int(candidate_index) < 16:
            candidate_ok = bool(strategy.bl.House(after[int(candidate_index)]))
        success = bool(
            strategy.bl.House(target_before)
            and not strategy.bl.House(target_after)
            and candidate_ok
        )
    return {"evaluable": True, "success": success}
