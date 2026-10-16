"""Analytical two-target collision geometry for double takeouts.

This module deliberately contains no simulator, tactic-library, or PhysX
dependency.  It narrows an unordered target pair to the collision geometries
which can plausibly send both targets out of the house.  A later free-flight
inversion maps the virtual first-contact point to ``(v, h, w)``; strict PhysX
then remains responsible for accepting the collision chain.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple


HOUSE_X = 2.375
HOUSE_Y = 4.880
HOUSE_EXIT_R = 1.830 + 0.145
STONE_R = 0.145


@dataclass(frozen=True)
class DoubleGeometry:
    """One ordered, off-centre two-target collision candidate."""

    first_point: Tuple[float, float]
    second_point: Tuple[float, float]
    phi: float
    contact_normal: Tuple[float, float]
    second_contact_point: Tuple[float, float]
    pre_second_direction: Tuple[float, float]
    virtual_aim_point: Tuple[float, float]
    first_exit_direction: Tuple[float, float]
    second_exit_direction: Tuple[float, float]
    first_exit_distance: float
    second_exit_distance: float
    normal_transfer: float
    tangential_transfer: float
    first_escape_margin: float
    second_escape_margin: float
    score: float


def _dot(left: Tuple[float, float], right: Tuple[float, float]) -> float:
    return left[0] * right[0] + left[1] * right[1]


def _norm(point: Tuple[float, float]) -> float:
    return math.hypot(point[0], point[1])


def _unit(point: Tuple[float, float]) -> Tuple[float, float] | None:
    length = _norm(point)
    if length <= 1e-10:
        return None
    return point[0] / length, point[1] / length


def _exit_distance(point: Tuple[float, float], direction: Tuple[float, float]) -> float | None:
    """Distance for a live stone center to leave the house along ``direction``."""
    rho = point[0] - HOUSE_X, point[1] - HOUSE_Y
    projected = _dot(rho, direction)
    discriminant = projected * projected + HOUSE_EXIT_R * HOUSE_EXIT_R - _dot(rho, rho)
    if discriminant < -1e-9:
        return None
    return max(0.0, -projected + math.sqrt(max(0.0, discriminant)))


def double_collision_geometries(
    first_point: Sequence[float],
    second_point: Sequence[float],
    *,
    samples: int = 72,
    limit: int = 4,
) -> List[DoubleGeometry]:
    """Return ranked physically meaningful double-hit contact geometries.

    ``first_point`` is the target hit by the delivery stone.  ``second_point``
    is hit by the first target.  The solver samples only the one-dimensional
    circle of possible second contacts, rejects non-outward energy splits, and
    returns a small ranked set.  It does not claim a collision will occur in
    PhysX and should never be used as a terminal success test.
    """
    if samples < 8 or limit < 1:
        raise ValueError("double geometry requires at least 8 samples and positive limit")
    first = float(first_point[0]), float(first_point[1])
    second = float(second_point[0]), float(second_point[1])
    if _norm((second[0] - first[0], second[1] - first[1])) <= 2.0 * STONE_R + 1e-6:
        return []

    candidates: List[DoubleGeometry] = []
    for index in range(int(samples)):
        phi = -math.pi + 2.0 * math.pi * index / float(samples)
        normal = math.cos(phi), math.sin(phi)
        contact = second[0] - 2.0 * STONE_R * normal[0], second[1] - 2.0 * STONE_R * normal[1]
        direction = _unit((contact[0] - first[0], contact[1] - first[1]))
        if direction is None or direction[1] >= -0.04:
            continue

        normal_transfer = _dot(direction, normal)
        tangential = (
            direction[0] - normal_transfer * normal[0],
            direction[1] - normal_transfer * normal[1],
        )
        tangential_transfer = _norm(tangential)
        # A double needs energy in both post-second-contact target paths.  A
        # nearly centre-on-centre second hit stops the first target instead.
        if normal_transfer < 0.28 or tangential_transfer < 0.25:
            continue

        first_exit_direction = _unit(tangential)
        second_exit_direction = normal
        first_radial = _unit((contact[0] - HOUSE_X, contact[1] - HOUSE_Y))
        second_radial = _unit((second[0] - HOUSE_X, second[1] - HOUSE_Y))
        if first_exit_direction is None or first_radial is None or second_radial is None:
            continue
        first_margin = _dot(first_exit_direction, first_radial)
        second_margin = _dot(second_exit_direction, second_radial)
        if first_margin <= 0.08 or second_margin <= 0.08:
            continue

        first_exit = _exit_distance(contact, first_exit_direction)
        second_exit = _exit_distance(second, second_exit_direction)
        if first_exit is None or second_exit is None:
            continue
        # The delivery must reach the upstream side of the first target before
        # it transfers its motion along ``direction``.
        aim = first[0] - 2.0 * STONE_R * direction[0], first[1] - 2.0 * STONE_R * direction[1]
        if aim[1] <= first[1]:
            continue

        score = (
            min(first_margin * tangential_transfer, second_margin * normal_transfer)
            + 0.12 * min(normal_transfer, tangential_transfer)
            - 0.035 * max(first_exit, second_exit)
        )
        candidates.append(DoubleGeometry(
            first_point=first,
            second_point=second,
            phi=phi,
            contact_normal=normal,
            second_contact_point=contact,
            pre_second_direction=direction,
            virtual_aim_point=aim,
            first_exit_direction=first_exit_direction,
            second_exit_direction=second_exit_direction,
            first_exit_distance=first_exit,
            second_exit_distance=second_exit,
            normal_transfer=normal_transfer,
            tangential_transfer=tangential_transfer,
            first_escape_margin=first_margin,
            second_escape_margin=second_margin,
            score=score,
        ))

    candidates.sort(key=lambda item: item.score, reverse=True)
    # Keep distinct second-impact families.  Adjacent phi samples otherwise
    # spend the entire seed budget on nearly identical collision normals.
    selected: List[DoubleGeometry] = []
    for candidate in candidates:
        if all(abs(math.atan2(math.sin(candidate.phi - other.phi), math.cos(candidate.phi - other.phi))) >= 0.18
               for other in selected):
            selected.append(candidate)
        if len(selected) >= int(limit):
            break
    return selected
