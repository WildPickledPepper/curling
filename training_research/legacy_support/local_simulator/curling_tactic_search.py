"""Offline trajectory search for curl-dependent tactical shots.

The legacy tactic library emits fixed curl parameters.  This module is a
calibration tool: it first traces the recovered pre-contact CurlingMotion path
and then asks the strict PhysX simulator to validate only the strongest
candidates.  It must not be used to unmask actions until a scenario corpus
shows that their outcome contracts are reliable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, List, Sequence, Tuple

from local_simulator.runtime_support.tools.reverse.front_half_pcm_replay import (
    local_initial_state,
)
from local_simulator.runtime_support.tools.reverse.recovered_curling_motion import (
    B2Vec2,
    STEP,
    newfrictionstep,
    unity_friction,
)
from local_simulator.double_geometry import DoubleGeometry, double_collision_geometries


_NATIVE_MOTION_STEP = None
_NATIVE_MOTION_RESOLVED = False


HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
RELEASE_Y = 32.4768
PATH_CLEARANCE = 2.0 * STONE_R + 0.025
TAKEOUT_CENTERLINE_TOLERANCE = 0.10
BESTSHOT_MAX_VELOCITY = 6.0
BESTSHOT_MAX_OFFSET = 2.23


@dataclass(frozen=True)
class TrajectoryPoint:
    x: float
    y: float
    vx: float
    vy: float
    w: float


@dataclass(frozen=True)
class CurlCandidate:
    shot: Tuple[float, float, float]
    score: float
    target_distance: float
    blocker_clearance: float
    guard_side_margin: float


@dataclass(frozen=True)
class DoubleCurlCandidate:
    """A collision-derived double seed filtered by recovered free flight."""

    shot: Tuple[float, float, float]
    score: float
    geometry: DoubleGeometry
    inbound_alignment: float
    contact_speed: float
    blocker_clearance: float


def _motion_step(friction: float, vx: float, vy: float, w: float) -> Tuple[float, float, float]:
    """Use the packaged native kernel when possible, with formula fallback."""
    global _NATIVE_MOTION_RESOLVED, _NATIVE_MOTION_STEP
    if not _NATIVE_MOTION_RESOLVED:
        _NATIVE_MOTION_RESOLVED = True
        try:
            from local_simulator.runtime_loader import install_bundled_pyphysx

            _NATIVE_MOTION_STEP = getattr(
                install_bundled_pyphysx(), "curling_new_friction_step", None
            )
        except RuntimeError:
            # The formula path remains useful in documentation or a non-Windows
            # Python environment, just much slower for a full candidate grid.
            _NATIVE_MOTION_STEP = None
    if _NATIVE_MOTION_STEP is not None:
        next_state = _NATIVE_MOTION_STEP(friction, vx, vy, w, STEP)
        return float(next_state[0]), float(next_state[1]), float(next_state[2])
    stepped = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
    return stepped.v.x, stepped.v.y, stepped.angle


def trace_free_flight(
    shot: Sequence[float],
    *,
    friction_noise: float = 0.0,
    max_steps: int = 5000,
) -> List[TrajectoryPoint]:
    """Trace first-contact-free motion with the recovered Unity equations."""
    velocity, horizontal_offset, rotation = (float(value) for value in shot[:3])
    base = _relative_free_flight(velocity, rotation, float(friction_noise), int(max_steps))
    return [
        TrajectoryPoint(point.x + horizontal_offset, point.y, point.vx, point.vy, point.w)
        for point in base
    ]


@lru_cache(maxsize=256)
def _relative_free_flight(
    velocity: float,
    rotation: float,
    friction_noise: float,
    max_steps: int,
) -> Tuple[TrajectoryPoint, ...]:
    """Cached h=0 trace; the recovered dynamics are translation invariant."""
    release = local_initial_state(velocity, 0.0, rotation)
    x, y, vx, vy, w = release.x, release.y, release.vx, release.vy, release.w
    friction = unity_friction(sweeping=False, noise=float(friction_noise))
    points = [TrajectoryPoint(x, y, vx, vy, w)]
    for _ in range(max_steps):
        if math.hypot(vx, vy) <= 0.01:
            break
        vx, vy, w = _motion_step(friction, vx, vy, w)
        x += vx * 0.01
        y += vy * 0.01
        points.append(TrajectoryPoint(x, y, vx, vy, w))
    return tuple(points)


def _distance_to_segment(point: Tuple[float, float], a: TrajectoryPoint, b: TrajectoryPoint) -> float:
    dx, dy = b.x - a.x, b.y - a.y
    length_sq = dx * dx + dy * dy
    if length_sq <= 1e-12:
        return math.hypot(point[0] - a.x, point[1] - a.y)
    ratio = ((point[0] - a.x) * dx + (point[1] - a.y) * dy) / length_sq
    ratio = max(0.0, min(1.0, ratio))
    return math.hypot(point[0] - (a.x + ratio * dx), point[1] - (a.y + ratio * dy))


def minimum_path_distance(path: Sequence[TrajectoryPoint], point: Tuple[float, float]) -> float:
    if len(path) < 2:
        return math.inf
    return min(_distance_to_segment(point, start, end) for start, end in zip(path, path[1:]))


def x_at_y(path: Sequence[TrajectoryPoint], y_value: float) -> float | None:
    """Interpolate the inbound path at a rink y coordinate."""
    for start, end in zip(path, path[1:]):
        if (start.y >= y_value >= end.y) or (start.y <= y_value <= end.y):
            if abs(end.y - start.y) <= 1e-12:
                return start.x
            ratio = (y_value - start.y) / (end.y - start.y)
            return start.x + ratio * (end.x - start.x)
    return None


def _state_at_y(path: Sequence[TrajectoryPoint], y_value: float) -> TrajectoryPoint | None:
    """Interpolate position and velocity at an inbound protocol y coordinate."""
    for start, end in zip(path, path[1:]):
        if (start.y >= y_value >= end.y) or (start.y <= y_value <= end.y):
            if abs(end.y - start.y) <= 1e-12:
                return start
            ratio = (y_value - start.y) / (end.y - start.y)
            return TrajectoryPoint(
                start.x + ratio * (end.x - start.x),
                y_value,
                start.vx + ratio * (end.vx - start.vx),
                start.vy + ratio * (end.vy - start.vy),
                start.w + ratio * (end.w - start.w),
            )
    return None


def _path_until_y(path: Sequence[TrajectoryPoint], y_value: float) -> Sequence[TrajectoryPoint]:
    for index, (start, end) in enumerate(zip(path, path[1:])):
        if (start.y >= y_value >= end.y) or (start.y <= y_value <= end.y):
            state = _state_at_y((start, end), y_value)
            return tuple(path[:index + 1]) + ((state,) if state is not None else ())
    return ()


def _closest_path_point(
    path: Sequence[TrajectoryPoint],
    point: Tuple[float, float],
) -> TrajectoryPoint:
    return min(path, key=lambda item: math.hypot(item.x - point[0], item.y - point[1]))


def _active_points(position: Sequence[float], excluded: Iterable[int]) -> List[Tuple[float, float]]:
    excluded_set = {int(index) for index in excluded}
    points = []
    for index in range(min(16, len(position) // 2)):
        if index in excluded_set:
            continue
        x, y = float(position[index * 2]), float(position[index * 2 + 1])
        if x != 0.0 or y != 0.0:
            points.append((x, y))
    return points


def search_double_hit_geometry(
    position: Sequence[float],
    *,
    first_index: int,
    second_index: int,
    velocities: Sequence[float] = (5.0, 5.3, 5.6, 5.8, 6.0),
    rotations: Sequence[float] = (-9.0, -7.0, -5.0, -3.0, 0.0, 3.0, 5.0, 7.0, 9.0),
    geometry_samples: int = 144,
    geometry_limit: int = 6,
    limit: int = 10,
) -> List[DoubleCurlCandidate]:
    """Map analytical double-contact geometry to a small free-flight seed set.

    The free-flight trace is used only until the delivery reaches the virtual
    contact point behind ``first_index``.  All stone-to-stone contacts after
    that point remain unmodelled here and must be verified by strict PhysX.
    """
    if first_index == second_index or limit < 1:
        return []
    first = float(position[first_index * 2]), float(position[first_index * 2 + 1])
    second = float(position[second_index * 2]), float(position[second_index * 2 + 1])
    if first == (0.0, 0.0) or second == (0.0, 0.0):
        return []
    geometries = double_collision_geometries(
        first, second, samples=geometry_samples, limit=geometry_limit,
    )
    blockers = _active_points(position, (first_index, second_index))
    candidates: List[DoubleCurlCandidate] = []
    for geometry in geometries:
        aim_x, aim_y = geometry.virtual_aim_point
        for velocity in _grid(velocities):
            if not 0.0001 <= velocity <= BESTSHOT_MAX_VELOCITY:
                continue
            for rotation in _grid(rotations):
                path = _relative_free_flight(velocity, rotation, 0.0, 5000)
                contact = _state_at_y(path, aim_y)
                if contact is None:
                    continue
                offset = aim_x - contact.x
                if abs(offset) > BESTSHOT_MAX_OFFSET:
                    continue
                speed = math.hypot(contact.vx, contact.vy)
                if speed <= 1e-8:
                    continue
                inbound = contact.vx / speed, contact.vy / speed
                # The first contact can be a controlled glancing hit.  The
                # selected first target leaves that collision along its contact
                # normal (the analytical ``pre_second_direction``); the
                # delivery need only supply a positive normal component, not
                # travel parallel to that normal itself.
                alignment = inbound[0] * geometry.pre_second_direction[0] + inbound[1] * geometry.pre_second_direction[1]
                if alignment < 0.35:
                    continue
                inbound_path = _path_until_y(path, aim_y)
                if len(inbound_path) < 2:
                    continue
                blocker_clearance = min(
                    (minimum_path_distance(inbound_path, (point[0] - offset, point[1])) for point in blockers),
                    default=math.inf,
                )
                if blocker_clearance < PATH_CLEARANCE:
                    continue
                # The post-collision range remains a proxy.  It only rejects
                # candidates that clearly lack energy before PhysX is called.
                required_range = max(
                    geometry.first_exit_distance / max(geometry.tangential_transfer, 1e-6),
                    geometry.second_exit_distance / max(geometry.normal_transfer, 1e-6),
                )
                range_proxy = (speed * alignment) * (speed * alignment)
                if range_proxy < 0.55 * required_range:
                    continue
                score = (
                    -geometry.score
                    + 0.18 * (1.0 - alignment)
                    - 0.025 * min(blocker_clearance, 1.0)
                    - 0.008 * speed
                )
                candidates.append(DoubleCurlCandidate(
                    shot=(velocity, offset, rotation),
                    score=score,
                    geometry=geometry,
                    inbound_alignment=alignment,
                    contact_speed=speed,
                    blocker_clearance=blocker_clearance,
                ))
    candidates.sort(key=lambda item: item.score)
    unique: List[DoubleCurlCandidate] = []
    seen = set()
    for candidate in candidates:
        key = tuple(round(value, 4) for value in candidate.shot)
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
        if len(unique) >= int(limit):
            break
    return unique


def _grid(values: Sequence[float]) -> Tuple[float, ...]:
    return tuple(float(value) for value in values)


def search_around_guard_takeout(
    position: Sequence[float],
    *,
    target_index: int,
    guard_index: int,
    side: int,
    velocities: Sequence[float] = (4.5, 4.8, 5.1, 5.4, 5.7, 6.0),
    offsets: Sequence[float] = (-1.50, -1.20, -0.90, -0.60, -0.30, 0.0, 0.30, 0.60, 0.90, 1.20, 1.50),
    rotations: Sequence[float] = (-9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.14, -2.0, 2.0, 3.14, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0),
    limit: int = 24,
) -> List[CurlCandidate]:
    """Find free-flight candidates that pass one guard before hitting a target.

    The returned candidates have *not* been collision-validated.  The strict
    validator must still prove that the target is hit/removed and the guard is
    retained after PhysX resolves the contact.
    """
    if side not in (-1, 1):
        raise ValueError("side must be -1 (left) or 1 (right)")
    target = (float(position[target_index * 2]), float(position[target_index * 2 + 1]))
    guard = (float(position[guard_index * 2]), float(position[guard_index * 2 + 1]))
    if target == (0.0, 0.0) or guard == (0.0, 0.0):
        return []
    blockers = _active_points(position, (target_index, guard_index))
    candidates: List[CurlCandidate] = []
    for velocity in _grid(velocities):
        if not 0.0001 <= velocity <= BESTSHOT_MAX_VELOCITY:
            continue
        for rotation in _grid(rotations):
            path = _relative_free_flight(velocity, rotation, 0.0, 5000)
            target_x = x_at_y(path, target[1])
            if target_x is None:
                continue
            # `h` only translates the trajectory. Align the curve at the
            # target height, then probe a small impact-normal band around it.
            # This avoids mistaking a coarse-grid graze for a true takeout.
            aligned_offset = target[0] - target_x
            adaptive_offsets = set(_grid(offsets))
            adaptive_offsets.update(
                aligned_offset + delta
                for delta in (-0.12, -0.08, -0.04, 0.0, 0.04, 0.08, 0.12)
            )
            for offset in sorted(adaptive_offsets):
                if abs(offset) > BESTSHOT_MAX_OFFSET:
                    continue
                target_relative = (target[0] - offset, target[1])
                guard_relative = (guard[0] - offset, guard[1])
                target_distance = minimum_path_distance(path, target_relative)
                # A bypass takeout must enter a near-centre impact line. A
                # wider collision envelope admits grazing contacts which can
                # leave a centred house target untouched after PhysX resolves.
                if target_distance > TAKEOUT_CENTERLINE_TOLERANCE:
                    continue
                guard_x = x_at_y(path, guard[1])
                if guard_x is None:
                    continue
                guard_side_margin = side * (guard_x + offset - guard[0]) - PATH_CLEARANCE
                if guard_side_margin < 0.0:
                    continue
                guard_clearance = minimum_path_distance(path, guard_relative)
                if guard_clearance < PATH_CLEARANCE:
                    continue
                blocker_clearance = min(
                    (minimum_path_distance(path, (blocker[0] - offset, blocker[1])) for blocker in blockers),
                    default=math.inf,
                )
                if blocker_clearance < PATH_CLEARANCE:
                    continue
                # A takeout needs both a near-centre contact line and enough
                # delivered speed to dislodge the target. Guard clearance is
                # still a hard contract, not a reward for a wider detour.
                score = (
                    3.0 * target_distance
                    - 0.12 * min(guard_side_margin, 0.6)
                    - 0.05 * min(blocker_clearance, 1.0)
                    - 0.015 * velocity
                )
                candidates.append(CurlCandidate(
                    shot=(velocity, offset, rotation),
                    score=score,
                    target_distance=target_distance,
                    blocker_clearance=blocker_clearance,
                    guard_side_margin=guard_side_margin,
                ))
    return sorted(candidates, key=lambda candidate: candidate.score)[:max(1, int(limit))]


def search_around_guard_draw(
    position: Sequence[float],
    *,
    guard_index: int,
    side: int,
    target: Tuple[float, float] | None = None,
    velocities: Sequence[float] = (2.7, 2.9, 3.1, 3.3, 3.5, 3.7),
    offsets: Sequence[float] = (-1.35, -1.05, -0.75, -0.45, -0.15, 0.15, 0.45, 0.75, 1.05, 1.35),
    rotations: Sequence[float] = (-8.0, -6.0, -4.0, -3.14, 3.14, 4.0, 6.0, 8.0),
    limit: int = 24,
) -> List[CurlCandidate]:
    """Find a draw path which passes the named guard and stops in the house."""
    if side not in (-1, 1):
        raise ValueError("side must be -1 (left) or 1 (right)")
    guard = (float(position[guard_index * 2]), float(position[guard_index * 2 + 1]))
    if guard == (0.0, 0.0):
        return []
    # A last-stone bypass draw is valuable only when it is a scoring attempt,
    # so default to the button instead of merely occupying the open side.
    desired = target or (HOUSE_X, HOUSE_Y)
    blockers = _active_points(position, (guard_index,))
    candidates: List[CurlCandidate] = []
    for velocity in _grid(velocities):
        for rotation in _grid(rotations):
            path = _relative_free_flight(velocity, rotation, 0.0, 5000)
            for offset in _grid(offsets):
                end = path[-1]
                end_distance = math.hypot(end.x + offset - desired[0], end.y - desired[1])
                if end_distance > 0.52 or math.hypot(end.x + offset - HOUSE_X, end.y - HOUSE_Y) > HOUSE_R:
                    continue
                guard_x = x_at_y(path, guard[1])
                if guard_x is None:
                    continue
                guard_side_margin = side * (guard_x + offset - guard[0]) - PATH_CLEARANCE
                guard_clearance = minimum_path_distance(path, (guard[0] - offset, guard[1]))
                if guard_side_margin < 0.0 or guard_clearance < PATH_CLEARANCE:
                    continue
                blocker_clearance = min(
                    (minimum_path_distance(path, (blocker[0] - offset, blocker[1])) for blocker in blockers),
                    default=math.inf,
                )
                if blocker_clearance < PATH_CLEARANCE:
                    continue
                score = end_distance - 0.20 * min(guard_side_margin, 0.6)
                candidates.append(CurlCandidate(
                    shot=(velocity, offset, rotation),
                    score=score,
                    target_distance=end_distance,
                    blocker_clearance=blocker_clearance,
                    guard_side_margin=guard_side_margin,
                ))
    return sorted(candidates, key=lambda candidate: candidate.score)[:max(1, int(limit))]


def search_freeze(
    position: Sequence[float],
    *,
    target_index: int,
    velocities: Sequence[float] = (2.90, 2.91, 2.92, 2.93, 2.94, 2.95),
    rotations: Sequence[float] = (-6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0),
    limit: int = 24,
) -> List[CurlCandidate]:
    """Find low-speed contact candidates for a selected house stone.

    The free-flight path is aligned at the incoming contact band above the
    target. Strict PhysX must still prove final touching geometry; this method
    only narrows the set to low-speed, obstruction-free approaches.
    """
    target = (float(position[target_index * 2]), float(position[target_index * 2 + 1]))
    if target == (0.0, 0.0):
        return []
    blockers = _active_points(position, (target_index,))
    candidates: List[CurlCandidate] = []
    contact_y = target[1] + 2.0 * STONE_R
    for velocity in _grid(velocities):
        if not 0.0001 <= velocity <= BESTSHOT_MAX_VELOCITY:
            continue
        for rotation in _grid(rotations):
            path = _relative_free_flight(velocity, rotation, 0.0, 5000)
            contact_x = x_at_y(path, contact_y)
            if contact_x is None:
                continue
            aligned_offset = target[0] - contact_x
            direct_offset = target[0] - HOUSE_X
            candidate_offsets = {
                aligned_offset + delta
                for delta in (-0.18, -0.14, -0.10, -0.06, -0.02, 0.02, 0.06, 0.10, 0.14, 0.18)
            }
            candidate_offsets.update(
                direct_offset + delta
                for delta in (-0.18, -0.14, -0.10, -0.06, -0.02, 0.02, 0.06, 0.10, 0.14, 0.18)
            )
            for offset in sorted(candidate_offsets):
                if abs(offset) > BESTSHOT_MAX_OFFSET:
                    continue
                target_relative = (target[0] - offset, target[1])
                target_distance = minimum_path_distance(path, target_relative)
                if target_distance > 2.0 * STONE_R + 0.035:
                    continue
                blocker_clearance = min(
                    (minimum_path_distance(path, (blocker[0] - offset, blocker[1])) for blocker in blockers),
                    default=math.inf,
                )
                if blocker_clearance < PATH_CLEARANCE:
                    continue
                closest = _closest_path_point(path, target_relative)
                impact_speed = math.hypot(closest.vx, closest.vy)
                # A freeze favours just-enough contact energy. Final touching
                # remains a strict collision outcome, not a free-flight proxy.
                score = (
                    target_distance
                    + 0.30 * impact_speed
                    + 0.010 * abs(rotation)
                    - 0.04 * min(blocker_clearance, 1.0)
                )
                candidates.append(CurlCandidate(
                    shot=(velocity, offset, rotation),
                    score=score,
                    target_distance=target_distance,
                    blocker_clearance=blocker_clearance,
                    guard_side_margin=math.inf,
                ))
    return sorted(candidates, key=lambda candidate: candidate.score)[:max(1, int(limit))]


def _velocity_for_stop_y(
    target_y: float,
    rotation: float,
    *,
    low: float = 2.45,
    high: float = 3.35,
    iterations: int = 18,
) -> float | None:
    """Invert recovered free flight for the release whose rest y matches target.

    With the delivery travelling from high y to low y, final y decreases
    monotonically with release speed in this low-speed interval.  Bisection
    produces a physical speed initialisation rather than a fixed freeze table.
    """
    low_end = _relative_free_flight(low, rotation, 0.0, 5000)[-1].y
    high_end = _relative_free_flight(high, rotation, 0.0, 5000)[-1].y
    if not high_end <= float(target_y) <= low_end:
        return None
    for _ in range(int(iterations)):
        middle = 0.5 * (low + high)
        end_y = _relative_free_flight(middle, rotation, 0.0, 5000)[-1].y
        if end_y > target_y:
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def search_freeze_geometry_v2(
    position: Sequence[float],
    *,
    target_index: int,
    contact_angles: Sequence[float] = (-0.20, -0.10, 0.0, 0.10, 0.20),
    rotations: Sequence[float] = (-2.0, 0.0, 2.0),
    contact_overshoot: float = 0.200,
    limit: int = 12,
) -> List[CurlCandidate]:
    """Generate geometry-derived low-energy freeze initial conditions.

    Let ``n=(sin(a), cos(a))`` point from the target toward the delivered
    stone. A proper freeze approaches the contact centre
    ``target + 2*STONE_R*n`` from upstream.  The recovered free-flight model
    is inverted so the unimpeded stone would finish about 0.20m beyond that point;
    this supplies enough normal impulse to establish contact without turning
    the freeze into a takeout. Strict PhysX remains the collision authority.
    """
    if not 0 <= int(target_index) < len(position) // 2:
        return []
    target = (float(position[target_index * 2]), float(position[target_index * 2 + 1]))
    if target == (0.0, 0.0):
        return []
    blockers = _active_points(position, (target_index,))
    candidates: List[CurlCandidate] = []
    for angle in contact_angles:
        normal = math.sin(float(angle)), math.cos(float(angle))
        contact_x = target[0] + 2.0 * STONE_R * normal[0]
        contact_y = target[1] + 2.0 * STONE_R * normal[1]
        # The delivery must approach from the release end, not from below the
        # target.  This also prevents a side-on candidate becoming a roll.
        if normal[1] <= 0.80 or not 0.545 < contact_x < 4.205:
            continue
        for rotation in rotations:
            velocity = _velocity_for_stop_y(contact_y - float(contact_overshoot), float(rotation))
            if velocity is None or not 0.0001 <= velocity <= BESTSHOT_MAX_VELOCITY:
                continue
            path = _relative_free_flight(velocity, float(rotation), 0.0, 5000)
            arrival = _state_at_y(path, contact_y)
            if arrival is None:
                continue
            offset = contact_x - arrival.x
            if abs(offset) > BESTSHOT_MAX_OFFSET:
                continue
            inbound = _path_until_y(path, contact_y)
            if len(inbound) < 2:
                continue
            blocker_clearance = min(
                (minimum_path_distance(inbound, (point[0] - offset, point[1])) for point in blockers),
                default=math.inf,
            )
            if blocker_clearance < PATH_CLEARANCE:
                continue
            impact_speed = math.hypot(arrival.vx, arrival.vy)
            # Prefer axial, low-energy contacts, while retaining enough room
            # around unrelated stones for the strict PhysX rollout.
            score = (
                0.18 * abs(float(angle))
                + 0.35 * impact_speed
                + 0.012 * abs(float(rotation))
                - 0.035 * min(blocker_clearance, 1.0)
            )
            candidates.append(CurlCandidate(
                shot=(float(velocity), float(offset), float(rotation)),
                score=float(score),
                target_distance=0.0,
                blocker_clearance=float(blocker_clearance),
                guard_side_margin=math.inf,
            ))
    return sorted(candidates, key=lambda candidate: candidate.score)[:max(1, int(limit))]
