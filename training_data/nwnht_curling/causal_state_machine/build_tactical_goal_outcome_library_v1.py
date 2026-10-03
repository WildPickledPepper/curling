#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile outcome-specific GoalStates below each hierarchical action.

The v2 action library deliberately groups together many exact collision and
endpoint realisations under one parent tactical action ``A``.  That is correct
for action support, but it is not sufficient for execution: a solver needs to
know which *whole-board result* ``G`` it is trying to create.

This compiler creates the data object::

    S -> A -> G(post-own anonymous topology + fine endpoint/binding menu)

It does not rank actions, call PhysX, or infer player intent.  Its terminal
labels are descriptive observations only; the following value stage performs
the finite-horizon ranking.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_causal_estimation_panel import FOLDS, fold_for_match
    from .build_double_outcome_goal_contracts_v1 import parse_post_own_topology
except ImportError:  # pragma: no cover - direct invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import FOLDS, fold_for_match  # type: ignore
    from causal_state_machine.build_double_outcome_goal_contracts_v1 import parse_post_own_topology  # type: ignore


MIN_OUTCOME_SUPPORT = 3
MIN_OUTCOME_SUPPORT_PER_FOLD = 1
MAX_FINE_OPTIONS_PER_OUTCOME = 3


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [
        {"value": value, "count": count, "share": round(count / total, 6)}
        for value, count in counter.most_common()
    ] if total else []


def _goal_id(parent_id: str, topology: str) -> str:
    digest = hashlib.sha256((parent_id + "|" + topology).encode("utf-8")).hexdigest()[:12]
    return f"{parent_id}:outcome:{digest}"


def _terminal_evidence(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    records = list(rows)
    margins = [float(row["margin"]) for row in records]
    outcomes = Counter(
        "FIRST_SCORES" if value > 0 else "OPPONENT_SCORES" if value < 0 else "BLANK"
        for value in margins
    )
    return {
        "observed_trajectory_count": len(records),
        "first_end_margin_mean": round(sum(margins) / len(margins), 6) if margins else None,
        "first_end_margin_distribution": _distribution(Counter(str(value) for value in margins)),
        "end_result_distribution": _distribution(outcomes),
        "warning": "Observed historical trajectories conditional on this realised outcome. This is not a causal value or a policy guarantee.",
    }


def build(
    families: Iterable[Mapping[str, Any]], assignments: Iterable[Mapping[str, Any]],
    transition_rows: Iterable[Mapping[str, Any]], *, min_outcome_support: int = MIN_OUTCOME_SUPPORT,
    min_outcome_support_per_fold: int = MIN_OUTCOME_SUPPORT_PER_FOLD,
    max_fine_options_per_outcome: int = MAX_FINE_OPTIONS_PER_OUTCOME,
) -> dict[str, Any]:
    """Build topology-specific G candidates and their historical observations."""

    family_by_id = {str(row["goal_id"]): dict(row) for row in families}
    transition_by_panel = {
        f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transition_rows
    }
    fine_by_parent = {
        parent_id: {str(option["goal_id"]): dict(option) for option in family.get("fine_goal_options", [])}
        for parent_id, family in family_by_id.items()
    }
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    input_assignments = 0
    for assignment in assignments:
        input_assignments += 1
        parent_id = str(assignment["tactical_goal_id"])
        if parent_id not in family_by_id:
            continue
        panel_key = str(assignment["panel_key"])
        source = transition_by_panel.get(panel_key)
        if source is None:
            raise ValueError(f"missing transition row for outcome assignment {panel_key}")
        grouped[(parent_id, str(assignment["post_own_topology"]))].append({
            "assignment": dict(assignment),
            "match_id": int(source["match_id"]),
            "margin": float(source["terminal_end_label"]["first_end_margin"]),
        })

    outcomes: list[dict[str, Any]] = []
    observation_rows: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for (parent_id, topology), rows in sorted(grouped.items()):
        support = len(rows)
        family = family_by_id[parent_id]
        folds = Counter(fold_for_match(int(row["match_id"])) for row in rows)
        fold_support = [int(folds[fold]) for fold in range(FOLDS)]
        if support < int(min_outcome_support):
            rejected.append({"tactical_goal_id": parent_id, "post_own_topology": topology, "reason": "outcome_support_below_gate", "support": support})
            continue
        fine_counts = Counter(str(row["assignment"]["fine_goal_id"]) for row in rows)
        fine_options = [
            {**fine_by_parent[parent_id][fine_id], "outcome_assigned_support": int(count)}
            for fine_id, count in fine_counts.items()
            if fine_id in fine_by_parent[parent_id]
        ]
        fine_options.sort(key=lambda row: (-int(row["outcome_assigned_support"]), str(row["goal_id"])))
        retained = fine_options[:int(max_fine_options_per_outcome)]
        target_id = _goal_id(parent_id, topology)
        status = (
            "CROSS_FOLD_TOPOLOGY_TARGET_CANDIDATE"
            if min(fold_support) >= int(min_outcome_support_per_fold) and retained
            else "TOPOLOGY_RECORDED_NOT_RUNTIME_TARGET"
        )
        outcome = {
            "schema": "nwnht_v2_tactical_goal_outcome_v2",
            "goal_id": target_id,
            "source_state": str(family["source_state"]),
            "K": int(str(family["source_state"])[1:str(family["source_state"]).index("_")]),
            "tactical_goal_id": parent_id,
            # Compatibility fields for the generic finite-horizon value
            # iterator.  The actual endpoint/binding constraints remain in
            # ``fine_goal_options`` because a topology alone is not a shot.
            "observed_template_kind": family["observed_template_kind"],
            "precision": "TOPOLOGY_CONSTRAINED_HIERARCHICAL_GOAL",
            "active_final_region": None,
            "stone_constraints_when_unambiguous": [],
            "dynamic_house_removal_binding_request": None,
            "after_own_occupancy": {"first": {}, "opponent": {}},
            "tactical_target_zone": family.get("tactical_target_zone"),
            "parent_action": {
                "observed_template_kind": family["observed_template_kind"],
                "tactical_target_zone": family.get("tactical_target_zone"),
                "observed_opponent_removed_count": int(family["observed_opponent_removed_count"]),
                "observed_opponent_house_removed_count": int(family["observed_opponent_house_removed_count"]),
            },
            "post_own_topology": topology,
            "terminal_board_predicate": parse_post_own_topology(topology),
            "fine_goal_options": retained,
            "fine_goal_option_count_observed": len(fine_counts),
            "support": support,
            "support_by_match_fold": fold_support,
            "minimum_fold_support": min(fold_support),
            "after_opponent_reply_state_distribution": _distribution(Counter(str(row["assignment"]["after_opponent_reply_state"]) for row in rows)),
            "observed_terminal_evidence": _terminal_evidence(rows),
            "execution_status": status,
            "warning": "The full topology predicate and one selected child endpoint/binding constraint must both be met. Parent action alone and topology alone are not sufficient physical targets.",
        }
        outcomes.append(outcome)
        for row in rows:
            assignment = row["assignment"]
            observation_rows.append({
            "schema": "nwnht_v2_tactical_goal_outcome_observation_v2",
                "panel_key": str(assignment["panel_key"]),
                "match_id": int(row["match_id"]),
                "fold": fold_for_match(int(row["match_id"])),
                "K": int(assignment["K"]),
                "source_state": str(assignment["source_state"]),
                "goal_id": target_id,
                "tactical_goal_id": parent_id,
                "next_state": str(assignment["after_opponent_reply_state"]),
                "post_own_topology": topology,
                "margin": float(row["margin"]),
            })
    outcomes.sort(key=lambda row: (row["source_state"], -int(row["support"]), row["goal_id"]))
    observation_rows.sort(key=lambda row: (row["source_state"], row["goal_id"], row["panel_key"]))
    return {
        "manifest": {
            "schema": "nwnht_v2_tactical_goal_outcome_library_v2",
            "input_assignment_count": input_assignments,
            "outcome_goal_count": len(outcomes),
            "outcome_observation_count": len(observation_rows),
            "rejected_low_support_count": len(rejected),
            "thresholds": {
                "min_outcome_support": min_outcome_support,
                "min_outcome_support_per_fold": min_outcome_support_per_fold,
                "max_fine_options_per_outcome": max_fine_options_per_outcome,
            },
            "prohibition": "This compiles observable outcome targets. It neither ranks their finite-horizon value nor proves an intervention effect or PhysX reachability.",
        },
        "goals": outcomes,
        "rejected": rejected,
        "observations": observation_rows,
    }


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", type=Path, default=root / "nwnht_v2_tactical_action_families_v2.json")
    parser.add_argument("--assignments", type=Path, default=root / "nwnht_v2_tactical_action_assignments_v2.jsonl")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_tactical_goal_outcome_library_v2.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    result = build(
        json.loads(args.families.read_text(encoding="utf-8"))["families"],
        _read_jsonl(args.assignments), _read_jsonl(args.transitions),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
