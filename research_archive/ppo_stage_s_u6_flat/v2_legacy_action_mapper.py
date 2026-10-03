"""Reversible mapping between legacy tactic IDs and Stage D1 semantics."""

from __future__ import annotations

from dataclasses import replace
from typing import Dict, Iterable, Mapping, Optional, Union

from ppo_actions import ACTION_NAMES, TACTIC_ACTIONS, action_id, action_name
from v2_action_space import ActionFamily, StructuredAction


_FAMILY_BY_PRESET: Mapping[str, ActionFamily] = {
    "occupy": ActionFamily.GUARD,
    "middle_in_center": ActionFamily.PUSH_TAP,
    "defense": ActionFamily.GUARD,
    "defense_push_in": ActionFamily.GUARD,
    "take_out": ActionFamily.TAKEOUT,
    "hit_roll": ActionFamily.HIT_ROLL,
    "push_in": ActionFamily.PUSH_TAP,
    "push_in_14": ActionFamily.PUSH_TAP,
    "freeze": ActionFamily.FREEZE,
    "clear": ActionFamily.PEEL,
    "double_hit": ActionFamily.DOUBLE,
    "double_push_in": ActionFamily.RAISE_RUNBACK,
    "default_draw": ActionFamily.DRAW,
    "draw_button": ActionFamily.DRAW,
    "draw_top4": ActionFamily.DRAW,
    "draw_back4": ActionFamily.DRAW,
    "center_guard": ActionFamily.GUARD,
    "corner_guard_left": ActionFamily.GUARD,
    "corner_guard_right": ActionFamily.GUARD,
    "come_around_left": ActionFamily.COME_AROUND,
    "come_around_right": ActionFamily.COME_AROUND,
    "take_out_house": ActionFamily.TAKEOUT,
    "take_out_guard": ActionFamily.TAKEOUT,
    "hit_and_stay": ActionFamily.HIT_STAY,
    "peel_guard": ActionFamily.PEEL,
    "hit_roll_left": ActionFamily.HIT_ROLL,
    "hit_roll_right": ActionFamily.HIT_ROLL,
    "freeze_no1": ActionFamily.FREEZE,
    "freeze_no2": ActionFamily.FREEZE,
    "guard_my_shot": ActionFamily.GUARD,
    "center_guard_high": ActionFamily.GUARD,
    "center_guard_low": ActionFamily.GUARD,
    "corner_guard_left_high": ActionFamily.GUARD,
    "corner_guard_right_high": ActionFamily.GUARD,
    "tap_back": ActionFamily.PUSH_TAP,
    "raise_takeout": ActionFamily.RAISE_RUNBACK,
    "runback_takeout": ActionFamily.RAISE_RUNBACK,
    "around_guard_takeout_left": ActionFamily.BYPASS,
    "around_guard_takeout_right": ActionFamily.BYPASS,
    "around_guard_draw_left": ActionFamily.BYPASS,
    "around_guard_draw_right": ActionFamily.BYPASS,
}


def _side(name: str) -> str:
    if name.endswith("_left"):
        return "left"
    if name.endswith("_right"):
        return "right"
    return "none"


def _derived_labels(preset: str) -> Dict[str, str]:
    family = _FAMILY_BY_PRESET[preset]
    labels = {
        "spin": _side(preset),
        "strength": "preset",
        "length": "preset",
        "contact_offset": "preset",
        "landing_zone": "preset",
    }
    if family in (ActionFamily.DRAW, ActionFamily.GUARD, ActionFamily.COME_AROUND):
        labels["strength"] = "draw"
    elif family == ActionFamily.PEEL:
        labels["strength"] = "peel"
    elif family == ActionFamily.HIT_STAY:
        labels["strength"] = "stay"
    elif family in (ActionFamily.TAKEOUT, ActionFamily.HIT_ROLL, ActionFamily.DOUBLE):
        labels["strength"] = "hit"
    if preset in ("draw_button", "middle_in_center"):
        labels["landing_zone"] = "button"
    elif preset == "draw_top4":
        labels["landing_zone"] = "top4"
    elif preset == "draw_back4":
        labels["landing_zone"] = "back4"
    elif "guard" in preset or preset in ("occupy", "defense", "defense_push_in"):
        labels["landing_zone"] = "guard"
    elif "come_around" in preset:
        labels["landing_zone"] = "house_cover"
    return labels


def legacy_to_structured(
    legacy: Union[int, str],
    *,
    primary_target: Optional[int] = None,
    middle_target: Optional[int] = None,
    second_target: Optional[int] = None,
) -> StructuredAction:
    """Convert a legacy action ID/name to a reversible D1 action."""
    preset = action_name(legacy) if isinstance(legacy, int) else str(legacy)
    if preset not in _FAMILY_BY_PRESET:
        raise KeyError("Unknown legacy tactic preset: %s" % preset)
    return StructuredAction(
        family=_FAMILY_BY_PRESET[preset],
        preset=preset,
        primary_target=primary_target,
        middle_target=middle_target,
        second_target=second_target,
        **_derived_labels(preset)
    )


def structured_to_legacy_name(action: StructuredAction) -> str:
    """Return the exact legacy preset while verifying the semantic mapping."""
    expected = _FAMILY_BY_PRESET.get(action.preset)
    if expected is None:
        raise KeyError("Unknown legacy tactic preset: %s" % action.preset)
    if action.family != expected:
        raise ValueError(
            "preset %s belongs to %s, not %s" % (action.preset, expected.value, action.family.value)
        )
    return action.preset


def structured_to_legacy_id(action: StructuredAction) -> int:
    return action_id(structured_to_legacy_name(action))


def action_mapping() -> Mapping[str, ActionFamily]:
    """Expose the immutable logical mapping used by docs and coverage tests."""
    return dict(_FAMILY_BY_PRESET)


def actions_for_family(family: ActionFamily) -> Iterable[str]:
    return tuple(name for name in ACTION_NAMES if _FAMILY_BY_PRESET[name] == family)


def with_targets(
    action: StructuredAction,
    *,
    primary_target: Optional[int] = None,
    middle_target: Optional[int] = None,
    second_target: Optional[int] = None,
) -> StructuredAction:
    """Return an immutable action with D1 target slots populated."""
    return replace(
        action,
        primary_target=primary_target,
        middle_target=middle_target,
        second_target=second_target,
    )


if set(_FAMILY_BY_PRESET) != set(ACTION_NAMES) or len(TACTIC_ACTIONS) != len(ACTION_NAMES):
    raise RuntimeError("D1 action mapping must cover every legacy action exactly once")
