"""Tactic-specific mathematical seed solvers for the PhysX inverse search.

The strategy library is intentionally kept as the fast, deployable source of
geometric and calibrated release estimates.  This module makes that boundary
explicit: a :class:`ShotContract` names the intended tactic in ``metadata``;
the corresponding seed solver produces a small set of ``(v, h, w)`` guesses;
and :class:`~local_simulator.curling_solver.search.InverseSolver` subsequently
uses PhysX to select and refine a physically valid release.

No seed is treated as a successful shot.  A seed is only a cheap initial
condition for the forward simulator.
"""

from __future__ import annotations

import contextlib
import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple

from ppo_framework.tactic_targets import (
    bestshot_for_double,
    bestshot_for_relay,
    bestshot_for_target,
    double_relay_geometry_seeds_v2,
    hit_roll_bestshot_for_target,
    peel_guard_geometry_seeds_v2,
    push_in_14_geometry_seeds_v2,
    relay_geometry_seeds_v2,
    tap_back_geometry_seeds_v2,
)
from local_simulator.curling_tactic_search import (
    search_double_hit_geometry,
    search_freeze_geometry_v2,
)

from .contracts import HOUSE_X, ShotContract
from .state import CanonicalState


ROOT = Path(__file__).resolve().parents[2]
TACTICSLIB = ROOT / "tacticslib"
if str(TACTICSLIB) not in sys.path:
    sys.path.insert(0, str(TACTICSLIB))

import strategy_library as strategy


@dataclass(frozen=True)
class ShotSeed:
    """One approximate release and the mathematical tactic that generated it."""

    source: str
    shot: Tuple[float, float, float]


@dataclass(frozen=True)
class SeedContext:
    """Fully specified input for one tactic's seed solver."""

    state: CanonicalState
    objective: ShotContract
    shot_num: int

    @property
    def player_is_first(self) -> bool:
        return int(self.shot_num) % 2 == 0

    @property
    def state_list(self) -> List[List[float]]:
        return [list(point) for point in self.state.positions]


SeedSolver = Callable[[SeedContext], Iterable[ShotSeed]]


def _strategy_seed(name: str, context: SeedContext) -> Optional[ShotSeed]:
    if name == "default_draw":
        return ShotSeed(name, (3.0, 0.0, 0.0))
    function = getattr(strategy, name, None)
    if function is None:
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = function(
                context.state_list,
                0 if context.player_is_first else 1,
                int(context.shot_num),
            )
    except (TypeError, ValueError):
        return None
    if result is None or result == 0 or len(result) < 3:
        return None
    return ShotSeed(name, tuple(float(value) for value in result[:3]))


def _deduplicate(seeds: Iterable[ShotSeed]) -> List[ShotSeed]:
    result: List[ShotSeed] = []
    seen = set()
    for seed in seeds:
        key = tuple(round(value, 5) for value in seed.shot)
        if key not in seen:
            seen.add(key)
            result.append(seed)
    return result


def _formula_draw_seed(
    context: SeedContext,
    desired_point: Tuple[float, float] | None = None,
) -> ShotSeed:
    """Direct draw inversion used even when the route is currently blocked.

    The direct formula is a seed, not a route validation.  A guarded route may
    legitimately fail this straight-line approximation and be recovered by a
    curl seed plus PhysX search.
    """
    x_value, y_value = desired_point or context.objective.landing_points[0]
    return ShotSeed(
        "formula_draw",
        (float(strategy.bl.y2v(float(y_value))), float(x_value - HOUSE_X), 0.0),
    )


def _draw_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    for point_index, point in enumerate(context.objective.landing_points):
        yield ShotSeed(
            "formula_draw" if point_index == 0 else f"formula_draw_slot_{point_index}",
            _formula_draw_seed(context, point).shot,
        )
    if bool(context.objective.metadata.get("final_score_contract", False)):
        # A literal P2 final delivery may need to add a second or third point
        # through guards. The ordinary draw library deliberately starts with
        # straight templates; add calibrated +/-8 button curls only for this
        # strict score-improvement contract and let PhysX reject blocked lanes.
        target_x, target_y = context.objective.landing_points[0]
        for rotation in (-8.0, 8.0):
            h0 = float(target_x) - strategy._calibrated_bypass_x(
                float(target_y), 0.0, rotation,
            )
            h0 += 0.110 if rotation > 0.0 else -0.110
            yield ShotSeed(
                "final_score_curl_%s" % ("left" if rotation < 0.0 else "right"),
                (3.048, h0, rotation),
            )
    for name in ("draw_button", "draw_top4", "draw_back4", "come_around_left", "come_around_right"):
        seed = _strategy_seed(name, context)
        if seed is not None:
            yield seed


def _around_guard_draw_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    side = int(context.objective.metadata.get("side", 0))
    names = (
        ("around_guard_draw_left",)
        if side < 0
        else ("around_guard_draw_right",)
        if side > 0
        else ("around_guard_draw_left", "around_guard_draw_right")
    )
    for name in names:
        seed = _strategy_seed(name, context)
        if seed is not None:
            yield seed
    # The direct formula is valuable as a best-effort candidate when the curl
    # geometry is unavailable, but it cannot displace a valid bypass seed.
    for point_index, point in enumerate(context.objective.landing_points):
        yield ShotSeed(
            "formula_draw" if point_index == 0 else f"formula_draw_slot_{point_index}",
            _formula_draw_seed(context, point).shot,
        )


def _direct_target_seed(context: SeedContext, action_name: str) -> Iterable[ShotSeed]:
    if not context.objective.target_stones:
        return
    shot = bestshot_for_target(
        context.state.as_flat(),
        action_name=action_name,
        player_is_first=context.player_is_first,
        target_index=int(context.objective.target_stones[0]),
        shot_num=int(context.shot_num),
    )
    if shot is not None:
        yield ShotSeed(action_name, tuple(float(value) for value in shot))


def _contact_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    """Legacy tactical release used as the geometric seed for generic hits.

    Some collision tactics have no factorised target head yet.  Their strict
    contract is anchored to the legacy release's first contact, while PhysX
    refines the release locally rather than replacing the tactic with a draw.
    """
    action_name = str(context.objective.metadata.get("action_name", ""))
    seed = _strategy_seed(action_name, context)
    if seed is not None:
        yield seed


def _clear_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    """Seed a clear from the selected delivery-side cluster stone.

    A clear is a high-energy straight collision rather than an opaque old
    template.  The three impact thicknesses and two energy levels are cheap
    analytical entrances; strict PhysX decides whether the whole cluster is
    genuinely dispersed.
    """
    if not context.objective.target_stones:
        return
    entry = int(context.objective.target_stones[0])
    target_x, _target_y = context.state.positions[entry]
    for speed_offset in (-0.20, 0.20):
        for h_offset in (0.0, -0.035, 0.035):
            yield ShotSeed(
                "clear_cluster_geometry_v2",
                (round(6.0 + speed_offset, 6), round(float(target_x - HOUSE_X + h_offset), 6), 0.0),
            )
    legacy = _strategy_seed("clear", context)
    if legacy is not None:
        yield ShotSeed("clear_legacy", legacy.shot)


def _double_relay_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    """Seed outer -> inner -> target relay geometry before retaining legacy."""
    if len(context.objective.target_stones) != 1 or len(context.objective.middle_stones) != 2:
        return
    outer, inner = (int(index) for index in context.objective.middle_stones)
    target = int(context.objective.target_stones[0])
    for rank, shot in enumerate(double_relay_geometry_seeds_v2(
        context.state.as_flat(), outer_index=outer, inner_index=inner, target_index=target,
    )):
        yield ShotSeed("double_relay_geometry_v2_%d" % rank, tuple(float(value) for value in shot))
    legacy = _strategy_seed("double_push_in", context)
    if legacy is not None:
        yield ShotSeed("double_push_in_legacy", legacy.shot)


def _tap_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    if not context.objective.target_stones:
        return
    target_index = int(context.objective.target_stones[0])
    for rank, shot in enumerate(tap_back_geometry_seeds_v2(
        context.state.as_flat(),
        player_is_first=context.player_is_first,
        target_index=target_index,
    )):
        yield ShotSeed("tap_geometry_v2_%d" % rank, tuple(float(value) for value in shot))
    legacy = _strategy_seed("tap_back", context)
    if legacy is not None:
        yield ShotSeed("tap_back_legacy", legacy.shot)


def _takeout_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    action_name = str(context.objective.metadata.get("action_name", "take_out_house"))
    if action_name not in {"take_out", "take_out_house", "take_out_guard", "peel_guard", "hit_and_stay",
                           "around_guard_takeout_left", "around_guard_takeout_right"}:
        action_name = "take_out_house"
    if action_name == "peel_guard" and context.objective.target_stones:
        for rank, shot in enumerate(peel_guard_geometry_seeds_v2(
            context.state.as_flat(),
            player_is_first=context.player_is_first,
            target_index=int(context.objective.target_stones[0]),
        )):
            yield ShotSeed("peel_guard_geometry_v2_%d" % rank, tuple(float(value) for value in shot))
    yield from _direct_target_seed(context, action_name)
    # These are deliberate nearby tactical priors, not arbitrary random
    # releases.  PhysX contract scoring decides whether any is admissible.
    if action_name != "take_out_house":
        yield from _direct_target_seed(context, "take_out_house")
    if action_name != "hit_and_stay":
        yield from _direct_target_seed(context, "hit_and_stay")


def _hit_roll_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    if not context.objective.target_stones:
        return
    action_name = str(context.objective.metadata.get("action_name", "hit_roll"))
    if action_name not in {"hit_roll", "hit_roll_left", "hit_roll_right"}:
        action_name = "hit_roll"
    target_x, _target_y = context.state.positions[int(context.objective.target_stones[0])]
    target_offset = float(target_x - HOUSE_X)
    # With w=0, h translates the inbound line directly.  A hit-and-roll is
    # therefore determined by its signed impact parameter, not a lookup table
    # keyed only on absolute x. Strict PhysX shows a small left/right contact
    # asymmetry for the recovered native stone model, so these values are
    # calibrated independently instead of being forced to be mirror images.
    roll_direction = (
        -1.0 if action_name == "hit_roll_left"
        else 1.0 if action_name == "hit_roll_right"
        else -1.0 if target_offset > 0.0 else 1.0
    )
    direction_matches_target = (
        action_name == "hit_roll"
        or (action_name == "hit_roll_left" and target_offset > 0.0)
        or (action_name == "hit_roll_right" and target_offset < 0.0)
    )
    if direction_matches_target:
        impact_parameter = (
            -0.10
            if roll_direction < 0.0
            else 0.12 + 0.07 * abs(target_offset)
        )
        yield ShotSeed(
            "hit_roll_geometry_v2",
            (10.0, target_offset + impact_parameter, 0.0),
        )
    shot = hit_roll_bestshot_for_target(
        context.state.as_flat(),
        action_name=action_name,
        player_is_first=context.player_is_first,
        target_index=int(context.objective.target_stones[0]),
        shot_num=int(context.shot_num),
    )
    if shot is not None:
        yield ShotSeed(action_name, tuple(float(value) for value in shot))
    yield from _takeout_seeds(context)


def _freeze_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    """Low-energy contact seeds derived from the selected target geometry."""
    if not context.objective.target_stones:
        return
    target_index = int(context.objective.target_stones[0])
    for rank, candidate in enumerate(search_freeze_geometry_v2(
        context.state.as_flat(), target_index=target_index, limit=12,
    )):
        yield ShotSeed("freeze_geometry_v2_%d" % rank, tuple(float(value) for value in candidate.shot))
    # Retain the legacy table only as a comparison seed.  It is not evidence
    # of a freeze outcome and remains masked in normal PPO operation.
    action_name = str(context.objective.metadata.get("action_name", "freeze"))
    if action_name not in {"freeze", "freeze_no1", "freeze_no2"}:
        action_name = "freeze"
    legacy = _strategy_seed(action_name, context)
    if legacy is not None:
        yield ShotSeed("freeze_legacy", legacy.shot)


def _relay_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    if not context.objective.target_stones or len(context.objective.middle_stones) != 1:
        return
    action_name = str(context.objective.metadata.get("action_name", "raise_takeout"))
    if action_name == "push_in_14":
        for rank, shot in enumerate(push_in_14_geometry_seeds_v2(
            context.state.as_flat(),
            player_is_first=context.player_is_first,
            target_index=int(context.objective.target_stones[0]),
            middle_index=int(context.objective.middle_stones[0]),
        )):
            yield ShotSeed("push_in_14_relay_geometry_v2_%d" % rank, tuple(float(value) for value in shot))
        legacy = _strategy_seed("push_in_14", context)
        if legacy is not None:
            yield ShotSeed("push_in_14_legacy", legacy.shot)
        return
    if action_name not in {"raise_takeout", "runback_takeout", "push_in"}:
        action_name = "raise_takeout"
    for rank, shot in enumerate(relay_geometry_seeds_v2(
        context.state.as_flat(),
        action_name=action_name,
        player_is_first=context.player_is_first,
        target_index=int(context.objective.target_stones[0]),
        middle_index=int(context.objective.middle_stones[0]),
    )):
        yield ShotSeed("%s_relay_geometry_v2_%d" % (action_name, rank), tuple(float(value) for value in shot))
    shot = bestshot_for_relay(
        context.state.as_flat(),
        action_name=action_name,
        player_is_first=context.player_is_first,
        target_index=int(context.objective.target_stones[0]),
        middle_index=int(context.objective.middle_stones[0]),
    )
    if shot is not None:
        yield ShotSeed(action_name, tuple(float(value) for value in shot))


def _double_seeds(context: SeedContext) -> Iterable[ShotSeed]:
    if len(context.objective.target_stones) != 2:
        return
    first, second = (int(value) for value in context.objective.target_stones)
    # PPO's target pair is unordered.  Search both contact orders because only
    # one may be reachable from the delivery side or retain two outward exits.
    candidates = []
    for first_index, second_index in ((first, second), (second, first)):
        candidates.extend(search_double_hit_geometry(
            context.state.as_flat(), first_index=first_index, second_index=second_index,
            geometry_samples=144, geometry_limit=6, limit=8,
        ))
    candidates.sort(key=lambda item: item.score)
    for rank, candidate in enumerate(candidates[:12]):
        yield ShotSeed(
            "double_geometry_v2_%d" % rank,
            tuple(float(value) for value in candidate.shot),
        )
    shot = bestshot_for_double(
        context.state.as_flat(), action_name="double_hit",
        player_is_first=context.player_is_first, target_index=first,
        second_target_index=second,
    )
    if shot is not None:
        yield ShotSeed("double_legacy", tuple(float(value) for value in shot))


TACTIC_SEED_SOLVERS: Dict[str, SeedSolver] = {
    "draw": _draw_seeds,
    "freeze": _freeze_seeds,
    "around_guard_draw": _around_guard_draw_seeds,
    "takeout": _takeout_seeds,
    "guard_takeout": _takeout_seeds,
    "hit_roll": _hit_roll_seeds,
    "relay": _relay_seeds,
    "double": _double_seeds,
    "double_hit": _double_seeds,
    "contact": _contact_seeds,
    "clear": _clear_seeds,
    "tap": _tap_seeds,
    "double_relay": _double_relay_seeds,
}


def tactic_name_for_contract(objective: ShotContract) -> str:
    """Resolve the explicit tactic, with stable backward-compatible defaults."""
    tactic = objective.metadata.get("tactic", objective.metadata.get("action_name"))
    if tactic is not None:
        return str(tactic)
    return str(objective.kind)


def generate_strategy_seeds(
    state: CanonicalState,
    objective: ShotContract,
    *,
    shot_num: int,
) -> List[ShotSeed]:
    """Generate mathematical initial guesses for one named tactical contract.

    ``objective.metadata[\"tactic\"]`` selects a registered tactic such as
    ``around_guard_draw``, ``hit_roll`` or ``relay``.  Omitting it preserves
    the historical contract-kind defaults.  The caller must always pass the
    returned seeds to :class:`InverseSolver`; this function never validates a
    shot and deliberately has no PhysX dependency.
    """
    context = SeedContext(state=state, objective=objective, shot_num=int(shot_num))
    tactic_name = tactic_name_for_contract(objective)
    solver = TACTIC_SEED_SOLVERS.get(tactic_name)
    if solver is None:
        # A tactic name should never turn a usable old contract into an empty
        # search.  Falling back to the contract family keeps the interface
        # extensible while making unsupported names visible in diagnostics.
        solver = TACTIC_SEED_SOLVERS.get(str(objective.kind))
    if solver is None:
        return []
    return _deduplicate(solver(context))
