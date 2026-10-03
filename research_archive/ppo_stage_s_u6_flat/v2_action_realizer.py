"""D1 adapter from :class:`StructuredAction` to legacy ``BESTSHOT`` tuples.

This module is deliberately deployable: it depends on tacticslib and the
existing target-conditioned helpers, but never on the local PhysX simulator.
"""

from __future__ import annotations

import contextlib
import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from ppo_actions import ACTION_NAMES, action_id
from ppo_robot_flat_v2 import TRAINING_MASKED_ACTIONS
from ppo_tactic_targets import (
    TARGETED_DIRECT_HIT_ACTIONS,
    TARGETED_DOUBLE_ACTIONS,
    TARGETED_RELAY_ACTIONS,
    bestshot_for_double,
    bestshot_for_relay,
    bestshot_for_target,
)
from v2_action_space import ActionFamily, StructuredAction
from v2_legacy_action_mapper import legacy_to_structured, structured_to_legacy_name


ROOT = Path(__file__).resolve().parents[2]
TACTICSLIB = ROOT / "tacticslib"
if str(TACTICSLIB) not in sys.path:
    sys.path.insert(0, str(TACTICSLIB))

import strategy_library as strategy


BestShot = Tuple[float, float, float]
DEFAULT_DRAW: BestShot = (3.0, 0.0, 0.0)


@dataclass(frozen=True)
class RealizedStructuredAction:
    """An auditable D2 decision after the legacy-compatible realization."""

    action: StructuredAction
    bestshot: Optional[BestShot]


def _state_list(position: Sequence[float]) -> List[List[float]]:
    if len(position) < 32:
        raise ValueError("D1 action realization requires 16 stone slots")
    return [[float(position[index * 2]), float(position[index * 2 + 1])] for index in range(16)]


def legacy_bestshot(
    preset: str,
    position: Sequence[float],
    *,
    player_is_first: bool,
    shot_num: int,
) -> Optional[BestShot]:
    """Resolve one legacy action exactly as the existing robot path does."""
    if preset == "default_draw":
        return DEFAULT_DRAW
    function_name = preset
    if preset == "double_hit":
        function_name = "double_hit_init" if player_is_first else "double_hit_gote"
    function = getattr(strategy, function_name, None)
    if function is None:
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = function(_state_list(position), 0 if player_is_first else 1, int(shot_num))
    except TypeError:
        return None
    if result is None or result == 0 or len(result) < 3:
        return None
    return tuple(float(value) for value in result[:3])


def realize_structured_action(
    action: StructuredAction,
    position: Sequence[float],
    *,
    player_is_first: bool,
    shot_num: int,
    allow_unvalidated_actions: bool = False,
) -> Optional[BestShot]:
    """Realize D1 semantics using the unchanged legacy/conditional routes."""
    preset = structured_to_legacy_name(action)
    if not allow_unvalidated_actions and preset in TRAINING_MASKED_ACTIONS:
        return None
    if action.primary_target is None:
        if action.middle_target is not None or action.second_target is not None:
            raise ValueError("middle/second target requires primary_target")
        return legacy_bestshot(
            preset, position, player_is_first=player_is_first, shot_num=shot_num,
        )
    if action.second_target is not None:
        if preset not in TARGETED_DOUBLE_ACTIONS or action.middle_target is not None:
            raise ValueError("second_target is only valid for a double action")
        return bestshot_for_double(
            position,
            action_name=preset,
            player_is_first=player_is_first,
            target_index=action.primary_target,
            second_target_index=action.second_target,
        )
    if action.middle_target is not None:
        if preset not in TARGETED_RELAY_ACTIONS:
            raise ValueError("middle_target is only valid for a relay action")
        return bestshot_for_relay(
            position,
            action_name=preset,
            player_is_first=player_is_first,
            target_index=action.primary_target,
            middle_index=action.middle_target,
        )
    if preset not in TARGETED_DIRECT_HIT_ACTIONS:
        raise ValueError("primary_target is not supported by legacy preset %s" % preset)
    return bestshot_for_target(
        position,
        action_name=preset,
        player_is_first=player_is_first,
        target_index=action.primary_target,
        shot_num=shot_num,
    )


def realize_legacy_selection(
    legacy_action: int,
    position: Sequence[float],
    *,
    player_is_first: bool,
    shot_num: int,
    primary_target: Optional[int] = None,
    middle_target: Optional[int] = None,
    second_target: Optional[int] = None,
    allow_unvalidated_actions: bool = False,
) -> RealizedStructuredAction:
    """Build and realize the D2 form of one sampled legacy decision."""
    action = legacy_to_structured(
        legacy_action,
        primary_target=primary_target,
        middle_target=middle_target,
        second_target=second_target,
    )
    return RealizedStructuredAction(
        action=action,
        bestshot=realize_structured_action(
            action,
            position,
            player_is_first=player_is_first,
            shot_num=shot_num,
            allow_unvalidated_actions=allow_unvalidated_actions,
        ),
    )


def legacy_compatibility_mask(
    position: Sequence[float],
    *,
    player_is_first: bool,
    shot_num: int,
    allow_unvalidated_actions: bool = False,
) -> List[bool]:
    """Return the old 41-way legal mask through the D1 realizer.

    The default draw remains a fallback: it is enabled only when no tactical
    preset is executable, matching ``PPOTacticsRobot.legal_action_mask``.
    """
    default_id = action_id("default_draw")
    mask: List[bool] = []
    for index, name in enumerate(ACTION_NAMES):
        action = legacy_to_structured(index)
        legal = (
            index != default_id
            and realize_structured_action(
                action,
                position,
                player_is_first=player_is_first,
                shot_num=shot_num,
                allow_unvalidated_actions=allow_unvalidated_actions,
            ) is not None
        )
        mask.append(bool(legal))
    if not any(mask):
        mask[default_id] = True
    return mask


def family_availability(mask: Sequence[bool]) -> Dict[ActionFamily, bool]:
    """A family is legal exactly when one of its legacy presets is legal."""
    if len(mask) != len(ACTION_NAMES):
        raise ValueError("expected one mask entry per legacy action")
    result = {family: False for family in ActionFamily}
    for enabled, name in zip(mask, ACTION_NAMES):
        if enabled:
            result[legacy_to_structured(name).family] = True
    return result
