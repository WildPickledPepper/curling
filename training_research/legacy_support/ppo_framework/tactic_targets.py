"""Target-conditioned execution for the reliable direct-hit tactic families.

The legacy tactic library selects the nearest target internally.  This module
exposes the same direct-hit geometry behind an explicit stone-slot target so a
future factorised PPO actor can choose both a tactic family and a target.
Only actions with an unambiguous, validated direct-hit contract belong here.
"""

from __future__ import annotations

import sys
import math
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
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

HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
# Strict PhysX calibration corpus ``relay_takeout_v1``: the 24 successful
# raise pairs had middle-to-target gaps in [0.714m, 0.824m].  A raise chain
# with a much shorter or longer gap is usually a direct-hit or a dead relay,
# not a useful candidate for local search.  Runback has different geometry and
# intentionally retains the broader legacy window.
RAISE_RELAY_MIN_GAP_M = 0.60
RAISE_RELAY_MAX_GAP_M = 1.15
# Strict three-seed teacher telemetry, not a generic physics assumption:
# - The sampled runback failures all had a nearly vertical 1.63--1.65m pair.
#   Nearby pairs with meaningful lateral transfer were feasible.
# - The sampled push-in pairs at 1.25--2.20m all failed the relay contract or
#   loss budget, while compact and long relays were feasible.
# Keep these exclusions at the pair gate so PPO does not spend a Top-K slot
# or a 48-replay PhysX solve on a known unsuitable geometry.
RUNBACK_NEAR_VERTICAL_GAP_MIN_M = 1.58
RUNBACK_NEAR_VERTICAL_GAP_MAX_M = 1.70
RUNBACK_NEAR_VERTICAL_MAX_LATERAL_M = 0.05
PUSH_IN_UNSUPPORTED_GAP_MIN_M = 1.25
PUSH_IN_UNSUPPORTED_GAP_MAX_M = 2.20
# Strict PhysX direct-seed calibration (2026-07-18).  The directional
# hit-roll h biases are only reliable in these target regions.  Generic
# hit_roll retains the legacy selector and is intentionally not narrowed.
HIT_ROLL_DIRECTIONAL_MIN_Y = {
    "hit_roll_left": 5.10,
    "hit_roll_right": 4.80,
}

# A legacy hit-roll is only useful when the struck opponent stone is a real
# near-button scoring threat and there is an unoccupied landing shoulder for
# the shooter.  This is deliberately a cheap geometry screen: strict PhysX
# still decides whether an eligible release can actually satisfy its contract.
HIT_ROLL_TARGET_RADIUS_M = 1.20
HIT_ROLL_LANDING_LATERAL_M = 0.42
HIT_ROLL_LANDING_BACK_M = 0.12
HIT_ROLL_CLEARANCE_M = 2.0 * STONE_R + 0.06
HIT_ROLL_DIRECT_LANE_HALF_WIDTH_M = 2.0 * STONE_R + 0.08
TAP_MIN_BUTTON_DISTANCE_M = 0.42
TAP_MAX_BUTTON_DISTANCE_M = 1.15
TAP_MIN_REAR_OFFSET_M = 0.35
TAP_MAX_REAR_OFFSET_M = 1.35
TAP_MAX_LATERAL_SLOPE = 0.65
PEEL_DELIVERY_CLEARANCE_M = 2.0 * STONE_R + 0.06
PEEL_OWN_DOWNSTREAM_CLEARANCE_M = 2.0 * STONE_R + 0.10
PEEL_DOWNSTREAM_RISK_DEPTH_M = 1.25


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


def has_viable_hit_roll_geometry(
    position: Sequence[float],
    *,
    player_is_first: bool,
) -> bool:
    """Return whether an opponent scoring stone has a usable hit-roll lane.

    The old legacy family was selectable against any opponent stone, including
    high guards and crowded shoulders where a roll cannot plausibly finish in
    the button area.  A viable target must be near the button, have no direct
    blocker immediately upstream, and leave at least one side landing pocket
    free.  Directional releases intentionally share this screen: their names
    describe release bias, not a guarantee of the target's x-side.
    """
    state = position_to_state_list(position)
    active = [
        (index, float(stone[0]), float(stone[1]))
        for index, stone in enumerate(state)
        if _is_active(stone)
    ]
    for target_index, target_x, target_y in active:
        if not _owner_is_opponent(target_index, player_is_first):
            continue
        if math.hypot(target_x - HOUSE_X, target_y - HOUSE_Y) > HIT_ROLL_TARGET_RADIUS_M:
            continue
        blocked_upstream = any(
            index != target_index
            and other_y > target_y + STONE_R
            and abs(other_x - target_x) <= HIT_ROLL_DIRECT_LANE_HALF_WIDTH_M
            for index, other_x, other_y in active
        )
        if blocked_upstream:
            continue
        for side in (-1.0, 1.0):
            landing_x = target_x + side * HIT_ROLL_LANDING_LATERAL_M
            landing_y = target_y - HIT_ROLL_LANDING_BACK_M
            if math.hypot(landing_x - HOUSE_X, landing_y - HOUSE_Y) > HIT_ROLL_TARGET_RADIUS_M:
                continue
            landing_clear = all(
                index == target_index
                or math.hypot(other_x - landing_x, other_y - landing_y) > HIT_ROLL_CLEARANCE_M
                for index, other_x, other_y in active
            )
            if landing_clear:
                return True
    return False


def tap_back_geometry_seeds_v2(
    position: Sequence[float],
    *,
    player_is_first: bool,
    target_index: int,
) -> List[Tuple[float, float, float]]:
    """Return button-directed analytical seeds for a narrow tap-back cone.

    The delivery contacts the target on the side opposite the button, rather
    than vertically through its centre. It deliberately returns no seed for
    sideways or shallow targets; such cases should be a draw/guard decision,
    not an attempted tap.
    """
    if not 0 <= int(target_index) < 16:
        return []
    state = position_to_state_list(position)
    target = state[int(target_index)]
    own_parity = 0 if player_is_first else 1
    if int(target_index) % 2 != own_parity or not _is_active(target):
        return []
    dx = float(target[0] - HOUSE_X)
    dy = float(target[1] - HOUSE_Y)
    distance = math.hypot(dx, dy)
    if not (
        TAP_MIN_BUTTON_DISTANCE_M <= distance <= TAP_MAX_BUTTON_DISTANCE_M
        and TAP_MIN_REAR_OFFSET_M <= dy <= TAP_MAX_REAR_OFFSET_M
        and abs(dx) / max(dy, 1e-8) <= TAP_MAX_LATERAL_SLOPE
    ):
        return []
    contact_x = float(target[0] + 2.0 * STONE_R * dx / distance)
    contact_y = float(target[1] + 2.0 * STONE_R * dy / distance)
    if not 0.545 < contact_x < 4.205:
        return []
    without_target = [
        stone for index, stone in enumerate(state)
        if _is_active(stone) and index != int(target_index)
    ]
    if not strategy.bl.Roadjudge(target, [HOUSE_X, HOUSE_Y], without_target):
        return []
    if not strategy.bl.Roadjudge([contact_x, contact_y], [contact_x, 10.61], without_target):
        return []
    base_velocity = max(
        2.9,
        min(3.45, 0.251899 * float(target[1]) + 1.734523 - 0.08 * abs(dx) / distance),
    )
    # Two energy levels and three impact thicknesses cover the local PhysX
    # search basin without treating a tap as an unrestricted collision shot.
    return [
        (round(base_velocity + speed_delta, 6), round(contact_x - HOUSE_X + h_delta, 6), 0.0)
        for speed_delta in (-0.10, 0.10)
        for h_delta in (0.0, -0.025, 0.025)
    ]


def peel_guard_geometry_seeds_v2(
    position: Sequence[float],
    *,
    player_is_first: bool,
    target_index: int,
) -> List[Tuple[float, float, float]]:
    """Return three straight-peel impact seeds when the exchange is viable.

    A guard peel is only meaningful when the incoming lane is clear and an
    own stone is not waiting immediately downstream of the opponent guard.
    The latter screen keeps the action from consuming PPO mass in positions
    where a nominally successful hit simply transfers the guard into our own
    house anchor.
    """
    if not 0 <= int(target_index) < 16:
        return []
    state = position_to_state_list(position)
    target = state[int(target_index)]
    if not (_owner_is_opponent(int(target_index), player_is_first) and _is_active(target)):
        return []
    if not bool(strategy._is_guard(target)):
        return []
    target_x, target_y = float(target[0]), float(target[1])
    own_parity = 0 if player_is_first else 1
    for index, stone in enumerate(state):
        if index == int(target_index) or not _is_active(stone):
            continue
        stone_x, stone_y = float(stone[0]), float(stone[1])
        # Any upstream obstruction changes the first collision and invalidates
        # a direct peel. The target itself is intentionally excluded above.
        if stone_y > target_y + 0.04 and abs(stone_x - target_x) <= PEEL_DELIVERY_CLEARANCE_M:
            return []
        # Do not drive an opponent guard into an own anchor/house stone in the
        # direct exit corridor. Opponent stones remain admissible: clearing two
        # opponent guards is not an exchange loss.
        if (
            index % 2 == own_parity
            and target_y - PEEL_DOWNSTREAM_RISK_DEPTH_M <= stone_y < target_y + 0.04
            and abs(stone_x - target_x) <= PEEL_OWN_DOWNSTREAM_CLEARANCE_M
        ):
            return []
    center_h = target_x - HOUSE_X
    return [
        (8.0, round(center_h + impact, 6), 0.0)
        for impact in (-0.045, 0.0, 0.045)
    ]


def has_executable_push_in_14_relay(
    position: Sequence[float],
    *,
    player_is_first: bool,
    shot_num: int,
) -> bool:
    """Whether legacy ``push_in_14`` will take its actual relay branch.

    The legacy tactic intentionally returns a direct takeout when the target's
    lane is clear.  That is a valid shot, but it is not a push-in contract and
    must not receive the PPO probability mass of a selected relay action.
    This screen mirrors the tactic's late-shot geometry: an own upstream
    middle has to block the vertical target lane, be reachable from delivery,
    and have a clear middle-to-target contact route.
    """
    if int(shot_num) not in (14, 15):
        return False
    state = position_to_state_list(position)
    active = [stone for stone in state if _is_active(stone)]
    for target_index, target in enumerate(state):
        if not (_owner_is_opponent(target_index, player_is_first) and _is_active(target)):
            continue
        if not bool(strategy.bl.House(target)) or not (0.545 < target[0] < 4.205) or target[1] > 6.71:
            continue
        for middle_index, middle in enumerate(state):
            if _owner_is_opponent(middle_index, player_is_first) or not _is_active(middle):
                continue
            if not (0.545 < middle[0] < 4.205 and middle[1] > target[1]):
                continue
            # Match Roadjudge's vertical corridor tolerance. This is the
            # condition that prevents the legacy function's early direct-hit
            # return and opens its relay branch.
            blocks_direct_lane = (
                target[1] <= middle[1] <= 10.61
                and abs(middle[0] - target[0]) <= 2.0 * strategy.Stone_R
            )
            if not blocks_direct_lane:
                continue
            dx = target[0] - middle[0]
            dy = target[1] - middle[1]
            norm = math.hypot(dx, dy)
            if norm <= 1e-8 or norm > 2.0 * 1.83:
                continue
            if math.atan2(abs(dy), max(abs(dx), 1e-8)) < math.radians(35):
                continue
            contact_x = middle[0] - 2.0 * strategy.Stone_R * dx / norm
            contact_y = middle[1] - 2.0 * strategy.Stone_R * dy / norm
            if not 0.545 < contact_x < 4.205:
                continue
            target_contact_x = target[0] + 0.61 * dx / norm
            target_contact_y = target[1] + 0.61 * dy / norm
            without_target = [
                stone for index, stone in enumerate(state)
                if _is_active(stone) and index != target_index
            ]
            if not strategy.bl.Roadjudge(middle, [target_contact_x, target_contact_y], without_target):
                continue
            if not strategy.bl.Roadjudge([contact_x, contact_y], [contact_x, 10.61], active):
                continue
            return True
    return False


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
        if eligible and action_name == "peel_guard":
            eligible = bool(peel_guard_geometry_seeds_v2(
                position, player_is_first=player_is_first, target_index=index,
            ))
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
    mask: List[bool] = []
    for index, stone in enumerate(state):
        eligible = _owner_is_opponent(index, player_is_first) and _is_active(stone)
        if action_name == "hit_roll_left":
            eligible = eligible and float(stone[0]) > HOUSE_X and float(stone[1]) >= HIT_ROLL_DIRECTIONAL_MIN_Y[action_name]
        elif action_name == "hit_roll_right":
            eligible = eligible and float(stone[0]) < HOUSE_X and float(stone[1]) >= HIT_ROLL_DIRECTIONAL_MIN_Y[action_name]
        mask.append(bool(eligible))
    return mask


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
    if action_name == "hit_roll_left":
        # Strict local PhysX calibration: the left roll is reliably described
        # by a signed 0.10m impact parameter, unlike the legacy x-only table.
        return (10.0, float(state[int(target_index)][0]) - HOUSE_X - 0.10, 0.0)
    result = strategy.hit_roll(
        state,
        0 if player_is_first else 1,
        int(shot_num),
        target_stone=state[int(target_index)],
    )
    if result is None or result == 0 or len(result) < 3:
        return None
    result = [float(value) for value in result[:3]]
    if action_name == "hit_roll_right":
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
    if not bool(middle[1] > target[1] + 2.0 * strategy.Stone_R and 0.545 < middle[0] < 4.205):
        return False
    gap = math.dist(middle, target)
    if action_name == "raise_takeout" and not RAISE_RELAY_MIN_GAP_M <= gap <= RAISE_RELAY_MAX_GAP_M:
        return False
    lateral = abs(float(middle[0]) - float(target[0]))
    if (
        action_name == "runback_takeout"
        and RUNBACK_NEAR_VERTICAL_GAP_MIN_M <= gap <= RUNBACK_NEAR_VERTICAL_GAP_MAX_M
        and lateral <= RUNBACK_NEAR_VERTICAL_MAX_LATERAL_M
    ):
        return False
    if (
        action_name == "push_in"
        and PUSH_IN_UNSUPPORTED_GAP_MIN_M <= gap <= PUSH_IN_UNSUPPORTED_GAP_MAX_M
    ):
        return False
    return True


def relay_geometry_seeds_v2(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    middle_index: int,
) -> List[Tuple[float, float, float]]:
    """Return six geometric releases for a routable relay pair.

    The delivery aims at the contact point behind the middle stone along the
    middle-to-target line.  Speed is conditioned on the relay gap, then each
    of three impact thicknesses is tried at two nearby energy levels.  This is
    a mathematical seed generator, not a substitute for strict PhysX.
    """
    if action_name not in TARGETED_RELAY_ACTIONS or not _relay_middle_eligible(
        position,
        action_name=action_name,
        player_is_first=player_is_first,
        target_index=target_index,
        middle_index=middle_index,
    ):
        return []
    state = position_to_state_list(position)
    target = state[int(target_index)]
    middle = state[int(middle_index)]
    dx = target[0] - middle[0]
    dy = target[1] - middle[1]
    gap = math.hypot(dx, dy)
    if gap < 1e-8:
        return []
    contact_x = middle[0] - 2.0 * strategy.Stone_R * dx / gap
    contact_y = middle[1] - 2.0 * strategy.Stone_R * dy / gap
    active = [stone for stone in state if _is_active(stone)]
    without_pair = [
        stone for index, stone in enumerate(state)
        if _is_active(stone) and index not in {int(target_index), int(middle_index)}
    ]
    if not (
        0.545 < contact_x < 4.205
        and strategy.bl.Roadjudge(middle, target, without_pair)
        and strategy.bl.Roadjudge([contact_x, contact_y], [contact_x, 10.61], active)
    ):
        return []
    correction = 0.033 if dx > 0.0 else 0.017
    base_h = contact_x - HOUSE_X + correction
    if action_name == "raise_takeout":
        # Calibrated around the 0.76m corpus mean. Longer raise gaps need a
        # little more residual energy after the first collision.
        base_v = max(5.70, min(6.35, 6.00 + 0.95 * (gap - 0.76)))
        speed_offsets = (-0.16, 0.16)
    elif action_name == "runback_takeout":
        # A runback transfers through an opposing guard, so its viable gap is
        # materially longer than a raise.  The legacy fixed v=6 seed leaves
        # long pairs short; use gap-scaled energy and let PhysX reject any
        # contact chain that is still not strict.
        base_v = max(5.85, min(8.60, 6.05 + 1.00 * (gap - 1.15)))
        speed_offsets = (-0.24, 0.24)
    else:  # push_in
        # Push-in pairs span both compact house relays and longer blockers.
        # Keep its seed broad but bounded rather than treating every pair as
        # the fixed-speed legacy contact.
        base_v = max(5.70, min(8.50, 5.95 + 0.90 * (gap - 0.85)))
        speed_offsets = (-0.24, 0.24)
    shots = []
    for h_offset in (0.0, -0.032, 0.032):
        for v_offset in speed_offsets:
            shots.append((base_v + v_offset, base_h + h_offset, 0.0))
    return shots


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
    if action_name == "raise_takeout":
        seeds = relay_geometry_seeds_v2(
            position,
            action_name=action_name,
            player_is_first=player_is_first,
            target_index=target_index,
            middle_index=middle_index,
        )
        if seeds:
            # The centered low-energy seed remains the direct template. Strict
            # PhysX receives all six variants through ``_relay_seeds``.
            return seeds[0]
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


def select_clear_cluster(
    position: Sequence[float],
) -> Optional[Tuple[int, Tuple[int, ...]]]:
    """Choose the delivery-side stone of a compact three-stone cluster.

    ``clear`` used to obtain this information by first simulating its old
    template and treating that template's first collision as the definition of
    the tactic.  That made the contract and its initial seed circular.  The
    cluster itself is fully observable from the board, so select it directly:
    each active stone proposes a narrow x-column, and the upstream member is
    the intended first collision.

    The result is only a geometric intent.  The strict contract still decides
    whether a release actually clears the cluster safely.
    """
    state = position_to_state_list(position)
    active = [index for index, stone in enumerate(state) if _is_active(stone)]
    best: Optional[Tuple[Tuple[float, ...], int, Tuple[int, ...]]] = None
    for anchor in active:
        anchor_x, anchor_y = state[anchor]
        cluster = tuple(sorted(
            index for index in active
            if abs(float(state[index][0]) - float(anchor_x)) < 2.0 * STONE_R
            and abs(float(state[index][1]) - float(anchor_y)) < 1.45
        ))
        if len(cluster) < 3:
            continue
        entry = max(cluster, key=lambda index: float(state[index][1]))
        x_span = max(float(state[index][0]) for index in cluster) - min(
            float(state[index][0]) for index in cluster
        )
        # Prefer clearing more stones, then the tighter and more upstream
        # column.  The final index makes ties deterministic.
        rank = (-float(len(cluster)), float(x_span), -float(state[entry][1]), float(entry))
        candidate = (rank, int(entry), cluster)
        if best is None or candidate[0] < best[0]:
            best = candidate
    return None if best is None else (best[1], best[2])


def select_push_in_14_relay(
    position: Sequence[float],
    *,
    player_is_first: bool,
) -> Optional[Tuple[int, int]]:
    """Select a routable late-end push-in pair without a physics probe.

    This intentionally does *not* reuse the ordinary ``push_in`` gap gate.
    A real late-end log contains a useful 1.97m relay which ordinary push-in
    excludes; ``push_in_14`` has its own historical geometry and must retain
    that wider late-shot corridor.
    """
    state = position_to_state_list(position)
    candidates = []
    for target_index, target in enumerate(state):
        if not (_owner_is_opponent(target_index, player_is_first) and _is_active(target)):
            continue
        for middle_index, middle in enumerate(state):
            if not _push_in_14_pair_geometry(
                position,
                player_is_first=player_is_first,
                target_index=target_index,
                middle_index=middle_index,
            ):
                continue
            gap = math.dist(target, middle)
            candidates.append((
                math.dist(target, (HOUSE_X, HOUSE_Y)), gap,
                abs(float(target[0]) - HOUSE_X), int(target_index), int(middle_index),
            ))
    if not candidates:
        return None
    _, _, _, target_index, middle_index = min(candidates)
    return target_index, middle_index


def _push_in_14_pair_geometry(
    position: Sequence[float],
    *,
    player_is_first: bool,
    target_index: int,
    middle_index: int,
) -> Optional[Tuple[float, float, float]]:
    """Return the late-push contact point and pair gap, or ``None``.

    This is the slot-aware form of the old ``push_in_14`` mathematics.  It is
    deliberately pure geometry: it checks roads and angles, never simulates a
    release.  Keeping it separate from ordinary push-in preserves the late
    tactic's historically wider, valid relay interval.
    """
    if not (0 <= int(target_index) < 16 and 0 <= int(middle_index) < 16):
        return None
    state = position_to_state_list(position)
    target, middle = state[int(target_index)], state[int(middle_index)]
    if not (
        _owner_is_opponent(int(target_index), player_is_first)
        and not _owner_is_opponent(int(middle_index), player_is_first)
        and _is_active(target) and _is_active(middle)
        and 0.545 < float(target[0]) < 4.205 and float(target[1]) <= 6.71
        and 0.545 < float(middle[0]) < 4.205 and float(middle[1]) > float(target[1])
    ):
        return None
    dx = float(target[0] - middle[0])
    dy = float(target[1] - middle[1])
    gap = math.hypot(dx, dy)
    if gap <= 1e-8 or gap > 2.0 * HOUSE_R:
        return None
    if math.atan2(abs(dy), max(abs(dx), 1e-8)) < math.radians(35):
        return None
    target_contact = (target[0] + 0.61 * dx / gap, target[1] + 0.61 * dy / gap)
    middle_contact = (middle[0] - 2.0 * STONE_R * dx / gap, middle[1] - 2.0 * STONE_R * dy / gap)
    without_target = [
        stone for index, stone in enumerate(state)
        if _is_active(stone) and index != int(target_index)
    ]
    active = [stone for stone in state if _is_active(stone)]
    if not (
        0.545 < middle_contact[0] < 4.205
        and strategy.bl.Roadjudge(middle, target_contact, without_target)
        and strategy.bl.Roadjudge([middle_contact[0], middle_contact[1]], [middle_contact[0], 10.61], active)
    ):
        return None
    return float(middle_contact[0]), float(middle_contact[1]), float(gap)


def push_in_14_geometry_seeds_v2(
    position: Sequence[float],
    *,
    player_is_first: bool,
    target_index: int,
    middle_index: int,
) -> List[Tuple[float, float, float]]:
    """Return six late-push seeds, with the old template centre retained."""
    geometry = _push_in_14_pair_geometry(
        position,
        player_is_first=player_is_first,
        target_index=target_index,
        middle_index=middle_index,
    )
    if geometry is None:
        return []
    contact_x, _contact_y, _gap = geometry
    state = position_to_state_list(position)
    dx = float(state[int(target_index)][0] - state[int(middle_index)][0])
    correction = 0.033 if dx > 0.0 else 0.017
    base_h = float(contact_x - HOUSE_X + correction)
    # (6.0, base_h, 0) is exactly the old late-push centre release.  It stays
    # first so a new six-seed entrance cannot evict a known historical route.
    return [
        (round(base_v, 6), round(base_h + h_offset, 6), 0.0)
        for base_v in (6.0, 6.24)
        for h_offset in (0.0, -0.032, 0.032)
    ]


def select_double_push_in_chain(
    position: Sequence[float],
    *,
    player_is_first: bool,
    shot_num: int,
) -> Optional[Tuple[int, int, int]]:
    """Infer ``outer -> own inner -> opponent target`` from board geometry.

    This ports the useful *geometric* gates of the legacy double-push tactic,
    but returns stone slots rather than an opaque release.  No PhysX call is
    made here; strict replay later checks the complete collision sequence.
    """
    state = position_to_state_list(position)
    active = [index for index, stone in enumerate(state) if _is_active(stone)]
    opponents = [
        index for index in active
        if _owner_is_opponent(index, player_is_first)
        and float(state[index][1]) >= HOUSE_Y - 0.61
    ]
    if int(shot_num) in (14, 15) and opponents:
        nearest = min(math.dist(state[index], (HOUSE_X, HOUSE_Y)) for index in opponents)
        opponents = [
            index for index in opponents
            if math.dist(state[index], (HOUSE_X, HOUSE_Y)) <= nearest + 1.7 * STONE_R
        ]
    own = [index for index in active if not _owner_is_opponent(index, player_is_first)]
    candidates = []
    for target in opponents:
        for inner in own:
            if float(state[inner][1]) <= float(state[target][1]):
                continue
            dx1 = float(state[target][0] - state[inner][0])
            dy1 = float(state[target][1] - state[inner][1])
            gap1 = math.hypot(dx1, dy1)
            if gap1 <= 1e-8 or math.atan2(abs(dy1), max(abs(dx1), 1e-8)) < math.radians(30):
                continue
            contact_inner = (
                float(state[inner][0] - 2.0 * STONE_R * dx1 / gap1),
                float(state[inner][1] - 2.0 * STONE_R * dy1 / gap1),
            )
            if not strategy.bl.Roadjudge(state[inner], state[target], state):
                continue
            for outer in active:
                if outer in {target, inner} or float(state[outer][1]) <= float(state[inner][1]):
                    continue
                dx2 = contact_inner[0] - float(state[outer][0])
                dy2 = contact_inner[1] - float(state[outer][1])
                gap2 = math.hypot(dx2, dy2)
                if gap2 <= 1e-8:
                    continue
                angle2 = math.atan2(abs(dy2), max(abs(dx2), 1e-8))
                angle1 = math.atan2(abs(dy1), max(abs(dx1), 1e-8))
                if dx2 * dx1 < 0.0 or angle2 > math.radians(80) or angle2 < angle1:
                    continue
                contact_outer = (
                    float(state[outer][0] - 2.0 * STONE_R * dx2 / gap2),
                    float(state[outer][1] - 2.0 * STONE_R * dy2 / gap2),
                )
                if not (
                    0.545 < contact_outer[0] < 4.205
                    and strategy.bl.Roadjudge(state[outer], contact_inner, state)
                    and strategy.bl.Roadjudge([contact_outer[0], contact_outer[1]], [contact_outer[0], 10.61], state)
                ):
                    continue
                candidates.append((
                    math.dist(state[target], (HOUSE_X, HOUSE_Y)), gap1 + gap2,
                    int(target), int(inner), int(outer),
                ))
    if not candidates:
        return None
    _, _, target, inner, outer = min(candidates)
    return outer, inner, target


def double_relay_geometry_seeds_v2(
    position: Sequence[float],
    *,
    outer_index: int,
    inner_index: int,
    target_index: int,
) -> List[Tuple[float, float, float]]:
    """Make six contact-point seeds for a selected double-relay chain."""
    state = position_to_state_list(position)
    if len({int(outer_index), int(inner_index), int(target_index)}) != 3:
        return []
    if not all(0 <= int(index) < 16 and _is_active(state[int(index)]) for index in (outer_index, inner_index, target_index)):
        return []
    outer, inner, target = (state[int(index)] for index in (outer_index, inner_index, target_index))
    dx1, dy1 = float(target[0] - inner[0]), float(target[1] - inner[1])
    gap1 = math.hypot(dx1, dy1)
    if gap1 <= 1e-8:
        return []
    inner_contact = (inner[0] - 2.0 * STONE_R * dx1 / gap1, inner[1] - 2.0 * STONE_R * dy1 / gap1)
    dx2, dy2 = float(inner_contact[0] - outer[0]), float(inner_contact[1] - outer[1])
    gap2 = math.hypot(dx2, dy2)
    if gap2 <= 1e-8:
        return []
    outer_contact_x = float(outer[0] - 2.0 * STONE_R * dx2 / gap2)
    if not 0.545 < outer_contact_x < 4.205:
        return []
    correction = 0.033 if dx2 > 0.0 else 0.017
    base_v = max(5.80, min(7.20, 6.0 + 0.20 * (gap1 - 1.0) + 0.24 * (gap2 - 1.0)))
    return [
        (round(base_v + speed_offset, 6), round(outer_contact_x - HOUSE_X + correction + h_offset, 6), 0.0)
        for speed_offset in (-0.20, 0.20)
        for h_offset in (0.0, -0.028, 0.028)
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


def _v2_double_geometry_available(
    position: Sequence[float],
    *,
    first_index: int,
    second_index: int,
) -> bool:
    """Cheap analytical screen before the free-flight V2 seed search.

    This is deliberately only an availability screen.  It proves that the
    ordered pair admits an outward two-target collision geometry; the slower
    curl/free-flight inversion in :func:`bestshot_for_double_v2` still decides
    whether a release seed exists.
    """
    from local_simulator.double_geometry import double_collision_geometries

    state = position_to_state_list(position)
    return bool(double_collision_geometries(
        state[int(first_index)], state[int(second_index)], samples=72, limit=1,
    ))


@lru_cache(maxsize=512)
def _cached_v2_double_shots(
    position: Tuple[float, ...],
    target_index: int,
    second_target_index: int,
) -> Tuple[Tuple[float, float, float], ...]:
    """Return bounded V2 free-flight seeds for an unordered target pair.

    A factorised actor asks the target and partner masks separately.  Caching
    prevents that bookkeeping from repeating the same recovered-curl search
    for an unchanged board snapshot.
    """
    from local_simulator.curling_tactic_search import search_double_hit_geometry

    candidates = []
    for first_index, second_index in (
        (int(target_index), int(second_target_index)),
        (int(second_target_index), int(target_index)),
    ):
        candidates.extend(search_double_hit_geometry(
            position,
            first_index=first_index,
            second_index=second_index,
            geometry_samples=144,
            geometry_limit=6,
            limit=8,
        ))
    candidates.sort(key=lambda item: item.score)
    shots = []
    seen = set()
    for candidate in candidates:
        shot = tuple(float(value) for value in candidate.shot)
        key = tuple(round(value, 5) for value in shot)
        if key not in seen:
            seen.add(key)
            shots.append(shot)
        if len(shots) >= 12:
            break
    return tuple(shots)


def bestshot_for_double_v2(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    second_target_index: int,
) -> Optional[Tuple[float, float, float]]:
    """Resolve a selected double with the collision-derived V2 seed solver.

    The returned release is a mathematical initial condition for strict PhysX,
    not a claim that the double contract has succeeded.  PPO can select this
    action only in the local PhysX environment, which supplies the actual
    outcome label and reward after execution.
    """
    if action_name not in TARGETED_DOUBLE_ACTIONS:
        return None
    if not (0 <= int(target_index) < 16 and 0 <= int(second_target_index) < 16):
        return None
    if int(target_index) == int(second_target_index):
        return None
    mask = double_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )
    if not (mask[int(target_index)] and mask[int(second_target_index)]):
        return None
    # Avoid invoking the curl search for a pair with no physical double
    # geometry in either contact order.
    if not any(_v2_double_geometry_available(
        position, first_index=first_index, second_index=second_index,
    ) for first_index, second_index in (
        (int(target_index), int(second_target_index)),
        (int(second_target_index), int(target_index)),
    )):
        return None
    shots = v2_double_seed_candidates(
        position,
        action_name=action_name,
        player_is_first=player_is_first,
        target_index=target_index,
        second_target_index=second_target_index,
    )
    return shots[0] if shots else None


def v2_double_seed_candidates(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    second_target_index: int,
) -> Tuple[Tuple[float, float, float], ...]:
    """Return the bounded V2 seed set for one legal unordered target pair."""
    if action_name not in TARGETED_DOUBLE_ACTIONS:
        return ()
    if not (0 <= int(target_index) < 16 and 0 <= int(second_target_index) < 16):
        return ()
    if int(target_index) == int(second_target_index):
        return ()
    mask = double_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )
    if not (mask[int(target_index)] and mask[int(second_target_index)]):
        return ()
    if not any(_v2_double_geometry_available(
        position, first_index=first_index, second_index=second_index,
    ) for first_index, second_index in (
        (int(target_index), int(second_target_index)),
        (int(second_target_index), int(target_index)),
    )):
        return ()
    return _cached_v2_double_shots(
        tuple(float(value) for value in position[:32]),
        int(target_index),
        int(second_target_index),
    )


def v2_double_geometry_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> List[bool]:
    """Fast V2-geometry action screen for PPO family availability.

    The exact free-flight solver is intentionally deferred until PPO chooses
    ``double_hit``.  Otherwise every decision would evaluate every pair's
    expensive curl inversion even though double-hit is rarely selected.
    """
    eligible = double_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )
    result = [False] * 16
    for first_index, enabled in enumerate(eligible):
        if not enabled:
            continue
        result[first_index] = any(
            second_index != first_index
            and eligible[second_index]
            and any(_v2_double_geometry_available(
                position, first_index=left, second_index=right,
            ) for left, right in (
                (first_index, second_index), (second_index, first_index),
            ))
            for second_index in range(16)
        )
    return result


def has_executable_double_v2(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
) -> bool:
    """Return whether any selected pair has an actual V2 release seed.

    This stops at the first executable pair for the family-level PPO mask.
    Full 16-slot masks are computed later only if PPO samples double-hit.
    """
    eligible = double_target_mask(
        position, action_name=action_name, player_is_first=player_is_first,
    )
    for target_index, enabled in enumerate(eligible):
        if not enabled:
            continue
        for second_target_index, partner_enabled in enumerate(eligible):
            if not partner_enabled or second_target_index == target_index:
                continue
            if not any(_v2_double_geometry_available(
                position, first_index=left, second_index=right,
            ) for left, right in (
                (target_index, second_target_index),
                (second_target_index, target_index),
            )):
                continue
            if bestshot_for_double_v2(
                position,
                action_name=action_name,
                player_is_first=player_is_first,
                target_index=target_index,
                second_target_index=second_target_index,
            ) is not None:
                return True
    return False


def executable_double_second_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    target_index: int,
    use_v2: bool = False,
) -> List[bool]:
    """Legal second-target slots for one selected double pair endpoint."""
    return [
        (bestshot_for_double_v2 if use_v2 else bestshot_for_double)(
            position, action_name=action_name, player_is_first=player_is_first,
            target_index=target_index, second_target_index=index,
        ) is not None
        for index in range(16)
    ]


def executable_double_target_mask(
    position: Sequence[float],
    *,
    action_name: str,
    player_is_first: bool,
    use_v2: bool = False,
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
            use_v2=use_v2,
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
    first_contact_indices: Sequence[int] = (),
    collision_events: Sequence[Dict[str, object]] = (),
) -> dict:
    """Label a relay only when its physical collision chain is observed.

    Terminal displacement alone cannot prove a raise/runback: the delivered
    stone must first hit the named middle stone, and PhysX must report that
    middle stone colliding with the named target.  Missing collision telemetry
    therefore never becomes a successful relay label.
    """
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
    first_contacts = {int(value) for value in first_contact_indices}
    first_contact_middle = bool(first_contacts) and (
        int(middle_index) in first_contacts and int(target_index) not in first_contacts
    )
    middle_target_contact = any(
        {int(value) for value in event.get("stone_indices", ())}
        == {int(middle_index), int(target_index)}
        for event in collision_events
    )
    success = bool(
        strategy.bl.House(target_before)
        and not strategy.bl.House(target_after)
        and middle_motion >= strategy.Stone_R
        and first_contact_middle
        and middle_target_contact
    )
    return {
        "evaluable": True,
        "success": success,
        "middle_motion": middle_motion,
        "first_contact_is_middle": bool(first_contact_middle),
        "middle_target_contact": bool(middle_target_contact),
        "collision_chain_evaluable": bool(first_contact_indices or collision_events),
    }


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
