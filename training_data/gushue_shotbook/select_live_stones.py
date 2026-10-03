"""Choose live CurlIT stones from one end's image candidates.

The scorebook has two visual facts that cannot be safely decided in isolation:
solid non-blue components are normal live-stone drawings, while royal-blue
marked components may be either a live stone or chart history.  This module
keeps the image extractor deliberately agnostic and makes the decision over a
complete end instead.

For each of the 16 panels it enumerates the blue-marked candidates as optional
and keeps ordinary coloured components.  It then finds the lowest-blue-mark
solution satisfying curling's one-delivery transition invariant:

* only the team that throws this shot may gain a stone;
* that team may gain at most one stone;
* the other team cannot gain a stone.

This is a conservative *selection* rule, not a physics reconstruction: rocks
may move or leave on a collision, so no artificial displacement limit is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Selection:
    stones: tuple[dict[str, object], ...]
    optional_blue_count: int
    red_count: int
    yellow_count: int


def _options(candidates: Sequence[dict[str, object]], red_team: str, yellow_team: str) -> list[Selection]:
    normal = [candidate for candidate in candidates if not bool(candidate["has_royal_blue_mark"])]
    optional = [candidate for candidate in candidates if bool(candidate["has_royal_blue_mark"])]
    choices: list[Selection] = []
    for size in range(len(optional) + 1):
        for extra in combinations(optional, size):
            stones = tuple(normal + list(extra))
            choices.append(
                Selection(
                    stones=stones,
                    optional_blue_count=size,
                    red_count=sum(stone["team"] == red_team for stone in stones),
                    yellow_count=sum(stone["team"] == yellow_team for stone in stones),
                )
            )
    return choices


def _valid_transition(previous: Selection | None, current: Selection, throwing_team: str, red_team: str, yellow_team: str) -> bool:
    previous_red = 0 if previous is None else previous.red_count
    previous_yellow = 0 if previous is None else previous.yellow_count
    return (
        current.red_count <= previous_red + int(throwing_team == red_team)
        and current.yellow_count <= previous_yellow + int(throwing_team == yellow_team)
    )


def select_end_live_stones(
    candidate_states: Sequence[Sequence[dict[str, object]]],
    throwing_teams: Sequence[str],
    red_team: str,
    yellow_team: str,
) -> list[list[dict[str, object]]]:
    """Select a globally consistent state for every shot in one end.

    Tie-breaking is deterministic: first use fewer optional blue components,
    then the earlier candidate order from the image.  If no legal sequence is
    available, fail closed rather than silently emit a corrupt coordinate set.
    """
    if len(candidate_states) != len(throwing_teams):
        raise ValueError("candidate state and throwing-team counts differ")
    layers = [_options(state, red_team, yellow_team) for state in candidate_states]
    # (cumulative optional-blue count, option index) -> predecessor option index.
    costs: list[dict[int, tuple[int, int | None]]] = []
    for shot_index, options in enumerate(layers):
        current_costs: dict[int, tuple[int, int | None]] = {}
        previous_costs = costs[-1] if costs else {0: (0, None)}
        previous_options: list[tuple[int, Selection | None]]
        if shot_index == 0:
            previous_options = [(0, None)]
        else:
            # This must be materialised: every current candidate needs to be
            # compared against every feasible previous candidate.  A generator
            # here would be consumed by the first comparison only.
            previous_options = [(index, layers[shot_index - 1][index]) for index in previous_costs]
        for current_index, current in enumerate(options):
            best: tuple[int, int | None] | None = None
            for previous_index, previous in previous_options:
                if not _valid_transition(previous, current, throwing_teams[shot_index], red_team, yellow_team):
                    continue
                previous_cost = 0 if previous is None else previous_costs[previous_index][0]
                proposal = (previous_cost + current.optional_blue_count, None if previous is None else previous_index)
                if best is None or proposal[0] < best[0] or (proposal[0] == best[0] and proposal[1] < best[1]):
                    best = proposal
            if best is not None:
                current_costs[current_index] = best
        if not current_costs:
            raise ValueError(f"No legal live-stone selection at shot {shot_index + 1}")
        costs.append(current_costs)
    final_index = min(costs[-1], key=lambda index: (costs[-1][index][0], index))
    selected: list[list[dict[str, object]]] = []
    for shot_index in range(len(layers) - 1, -1, -1):
        selected.append(list(layers[shot_index][final_index].stones))
        predecessor = costs[shot_index][final_index][1]
        if predecessor is None:
            break
        final_index = predecessor
    selected.reverse()
    if len(selected) != len(layers):
        raise AssertionError("selector backtracking did not reach first shot")
    return selected
