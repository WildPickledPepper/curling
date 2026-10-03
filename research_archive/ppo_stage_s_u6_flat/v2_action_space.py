"""Stage D1 semantic action contract.

Stage C checkpoints emit one of the legacy 41 tactic IDs.  D1 gives each ID
an explicit tactical family and optional stone slots without making any of
those fields independently learnable yet.  Keeping ``preset`` mandatory makes
the conversion reversible and preserves the frozen Stage C policy exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


STONE_SLOT_COUNT = 16


class ActionFamily(str, Enum):
    DRAW = "draw"
    GUARD = "guard"
    COME_AROUND = "come_around"
    FREEZE = "freeze"
    TAKEOUT = "takeout"
    HIT_STAY = "hit_stay"
    HIT_ROLL = "hit_roll"
    PEEL = "peel"
    PUSH_TAP = "push_tap"
    RAISE_RUNBACK = "raise_runback"
    DOUBLE = "double"
    BYPASS = "bypass"


def _validate_slot(name: str, value: Optional[int]) -> None:
    if value is not None and not 0 <= int(value) < STONE_SLOT_COUNT:
        raise ValueError("%s must be in [0, %d), got %r" % (name, STONE_SLOT_COUNT, value))


@dataclass(frozen=True)
class StructuredAction:
    """A semantic action with a legacy-compatible delivery preset.

    Only ``family``, ``preset`` and selected stone slots affect D1 execution.
    Delivery descriptors are labels derived from the preset; later D stages may
    turn them into independently sampled controls after their contracts exist.
    """

    family: ActionFamily
    preset: str
    primary_target: Optional[int] = None
    middle_target: Optional[int] = None
    second_target: Optional[int] = None
    spin: str = "none"
    strength: str = "preset"
    length: str = "preset"
    contact_offset: str = "preset"
    landing_zone: str = "preset"

    def __post_init__(self) -> None:
        if not self.preset:
            raise ValueError("StructuredAction.preset is required for D1 compatibility")
        _validate_slot("primary_target", self.primary_target)
        _validate_slot("middle_target", self.middle_target)
        _validate_slot("second_target", self.second_target)
        if self.primary_target is not None and self.primary_target == self.middle_target:
            raise ValueError("primary_target and middle_target must be distinct")
        if self.primary_target is not None and self.primary_target == self.second_target:
            raise ValueError("primary_target and second_target must be distinct")

    @property
    def has_selected_targets(self) -> bool:
        return any(
            slot is not None
            for slot in (self.primary_target, self.middle_target, self.second_target)
        )
