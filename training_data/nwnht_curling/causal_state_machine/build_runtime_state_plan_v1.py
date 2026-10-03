#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialise a conservative runtime StatePlan from cross-fold action evidence.

The artifact is deliberately pre-PhysX.  It returns a tactical action and an
evidence-appropriate endpoint contract, never a launch parameter.  A plan is
only emitted when the same parent action is primary in at least four of five
match-grouped folds.  Exact narrow children are used only when their own
cross-fold screen passed; otherwise a placement action may expose a semantic
region predicate, while removal actions without a bindable fine child remain
``SEARCH_REQUIRED``.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping


MIN_PRIMARY_MODE_SHARE = 0.80
MIN_ACTION_FOLD_COVERAGE = 4
MAX_FALLBACKS = 2


def semantic_region(zone: str) -> dict[str, Any] | None:
    """Coordinate predicates in the canonical button-centred frame."""

    zones = {
        "BUTTON": {"kind": "CIRCLE", "centre_x_m": 0.0, "centre_y_m": 0.0, "max_radius_m": 0.6096},
        "HOUSE_FRONT_LEFT": {"kind": "HOUSE_SECTOR", "min_radius_m": 0.6096, "max_radius_m": 1.8288, "y_relation": ">=0", "x_relation": "<0"},
        "HOUSE_FRONT_RIGHT": {"kind": "HOUSE_SECTOR", "min_radius_m": 0.6096, "max_radius_m": 1.8288, "y_relation": ">=0", "x_relation": ">=0"},
        "HOUSE_BACK_LEFT": {"kind": "HOUSE_SECTOR", "min_radius_m": 0.6096, "max_radius_m": 1.8288, "y_relation": "<0", "x_relation": "<0"},
        "HOUSE_BACK_RIGHT": {"kind": "HOUSE_SECTOR", "min_radius_m": 0.6096, "max_radius_m": 1.8288, "y_relation": "<0", "x_relation": ">=0"},
        "CENTRE_GUARD_NEAR": {"kind": "GUARD_LANE", "abs_x_max_m": 0.38, "y_min_exclusive_m": 1.8288, "y_max_inclusive_m": 4.14},
        "CENTRE_GUARD_FAR": {"kind": "GUARD_LANE", "abs_x_max_m": 0.38, "y_min_exclusive_m": 4.14, "y_max_inclusive_m": 6.45},
        "WING_GUARD_NEAR_LEFT": {"kind": "WING_GUARD", "x_relation": "<-0.38", "y_min_exclusive_m": 1.8288, "y_max_inclusive_m": 4.14},
        "WING_GUARD_FAR_LEFT": {"kind": "WING_GUARD", "x_relation": "<-0.38", "y_min_exclusive_m": 4.14, "y_max_inclusive_m": 6.45},
        "WING_GUARD_NEAR_RIGHT": {"kind": "WING_GUARD", "x_relation": ">0.38", "y_min_exclusive_m": 1.8288, "y_max_inclusive_m": 4.14},
        "WING_GUARD_FAR_RIGHT": {"kind": "WING_GUARD", "x_relation": ">0.38", "y_min_exclusive_m": 4.14, "y_max_inclusive_m": 6.45},
    }
    return zones.get(zone)


def _result_key(family: Mapping[str, Any]) -> tuple[Any, ...]:
    post = family.get("post_own_topology_distribution", [])
    return (
        family.get("observed_template_kind"), family.get("tactical_target_zone"),
        family.get("observed_opponent_removed_count"), family.get("observed_opponent_house_removed_count"),
        post[0]["value"] if post else None,
    )


def _option(family: Mapping[str, Any], screen: Mapping[str, Any] | None) -> dict[str, Any] | None:
    narrow = [] if screen is None else list(screen.get("representative_execution_options", []))
    base = {
        "tactical_goal_id": str(family["goal_id"]),
        "observed_template_kind": family["observed_template_kind"],
        "tactical_target_zone": family.get("tactical_target_zone"),
        "observed_opponent_removed_count": family["observed_opponent_removed_count"],
        "observed_opponent_house_removed_count": family["observed_opponent_house_removed_count"],
        "expected_next_state_distribution": family.get("after_opponent_reply_state_distribution", []),
        "canonical_coordinate_note": "If runtime state classification mirrored the board, reflect every x-coordinate and left/right predicate before execution.",
    }
    if narrow:
        return {
            **base,
            "precision_level": "NARROW_CROSS_FOLD_GOAL",
            "fine_goal_options": narrow,
            "evidence_note": "Each listed narrow GoalState recurred at least ten times in every match-grouped fold; order is recurrence stability, not a finer terminal-value claim.",
        }
    region = semantic_region(str(family.get("tactical_target_zone")))
    if str(family.get("observed_template_kind")) == "ACTIVE_STONE_PLACEMENT" and region is not None:
        return {
            **base,
            "precision_level": "SEMANTIC_REGION_GOAL",
            "target_region": region,
            "evidence_note": "No cross-fold-supported fixed narrow endpoint exists. This is the narrowest region abstraction supported by the data; later path search must optimise within it.",
        }
    return None


def _action_rank_stats(fold_results: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    stats: dict[str, dict[str, dict[str, Any]]] = defaultdict(lambda: defaultdict(lambda: {"ranks": [], "values": []}))
    for result in fold_results:
        by_state: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
        for item in result["candidate_values"]:
            if item.get("eligible_for_empirical_ranking"):
                by_state[str(item["source_state"])].append(item)
        for state, values in by_state.items():
            values.sort(key=lambda item: (-float(item["backed_up_value_mean"]), str(item["goal_id"])))
            for rank, item in enumerate(values, start=1):
                slot = stats[state][str(item["goal_id"])]
                slot["ranks"].append(rank)
                slot["values"].append(float(item["backed_up_value_mean"]))
    return stats


def build(
    partition: Mapping[str, Any],
    families: Iterable[Mapping[str, Any]],
    fine_screen: Mapping[str, Any],
    outer_summary: Mapping[str, Any],
    fold_results: Iterable[Mapping[str, Any]],
    *,
    min_primary_mode_share: float = MIN_PRIMARY_MODE_SHARE,
    min_action_fold_coverage: int = MIN_ACTION_FOLD_COVERAGE,
    max_fallbacks: int = MAX_FALLBACKS,
) -> dict[str, Any]:
    family_by_id = {str(row["goal_id"]): dict(row) for row in families}
    screen_by_id = {str(row["tactical_goal_id"]): row for row in fine_screen["parents"]}
    summary_by_state = {str(row["state_id"]): row for row in outer_summary["states"]}
    stats = _action_rank_stats(fold_results)
    plans: list[dict[str, Any]] = []
    for state in sorted(partition["states"], key=lambda row: (int(row["K"]), str(row["state_id"]))):
        state_id = str(state["state_id"])
        summary = summary_by_state.get(state_id, {})
        primary_id = summary.get("primary_mode_goal_id")
        mode_share = summary.get("primary_mode_share")
        coverage = 0 if primary_id is None else len(stats[state_id].get(str(primary_id), {}).get("ranks", []))
        primary_family = None if primary_id is None else family_by_id.get(str(primary_id))
        primary = None if primary_family is None else _option(primary_family, screen_by_id.get(str(primary_id)))
        if not bool(state["eligible_for_next_goal_stage"]):
            status, reason = "SEARCH_REQUIRED_INSUFFICIENT_STATE_SUPPORT", "state_partition_support_gate"
        elif primary_family is None:
            status, reason = "SEARCH_REQUIRED_NO_CROSS_FOLD_ACTION", "no_parent_action_ranked_in_outer_folds"
        elif mode_share is None or float(mode_share) < min_primary_mode_share or coverage < min_action_fold_coverage:
            status, reason = "SEARCH_REQUIRED_ACTION_UNSTABLE", "primary_parent_action_lacks_cross_fold_consensus"
        elif primary is None:
            status, reason = "SEARCH_REQUIRED_NO_BINDABLE_TARGET", "action_has_no_narrow_child_or_supported_placement_region"
        else:
            status, reason = "EMPIRICAL_ACTION_CONSENSUS", None

        fallbacks: list[dict[str, Any]] = []
        if status == "EMPIRICAL_ACTION_CONSENSUS" and primary_family is not None:
            primary_key = _result_key(primary_family)
            candidates = []
            for goal_id, record in stats[state_id].items():
                if goal_id == str(primary_id) or len(record["ranks"]) < min_action_fold_coverage:
                    continue
                family = family_by_id.get(goal_id)
                if family is None or _result_key(family) == primary_key:
                    continue
                option = _option(family, screen_by_id.get(goal_id))
                if option is None:
                    continue
                candidates.append((sum(record["ranks"]) / len(record["ranks"]), goal_id, option, record))
            for _, goal_id, option, record in sorted(candidates)[:max_fallbacks]:
                fallbacks.append({
                    **option,
                    "cross_fold_rank_mean": round(sum(record["ranks"]) / len(record["ranks"]), 6),
                    "cross_fold_coverage": len(record["ranks"]),
                })
        plans.append({
            "state_id": state_id,
            "K": int(state["K"]),
            "recommendation_status": status,
            "search_reason": reason,
            "primary_action": None if primary is None else {
                **primary,
                "cross_fold_primary_mode_share": mode_share,
                "cross_fold_coverage": coverage,
                "cross_fold_rank_mean": None if primary_id is None else round(sum(stats[state_id][str(primary_id)]["ranks"]) / coverage, 6),
            },
            "fallback_actions": fallbacks,
            "runtime_contract": "Tactical module outputs endpoint constraints only. Local legality and PhysX inverse planning are separate later stages.",
        })
    return {
        "manifest": {
            "schema": "nwnht_first_player_runtime_state_plan_v1",
            "runtime_input": "K plus current board owner/coordinates only",
            "selection_gate": {"min_primary_mode_share": min_primary_mode_share, "min_action_fold_coverage": min_action_fold_coverage},
            "precision_levels": ["NARROW_CROSS_FOLD_GOAL", "SEMANTIC_REGION_GOAL", "SEARCH_REQUIRED"],
            "summary": {
                "state_count": len(plans),
                "empirical_action_consensus_count": sum(row["recommendation_status"] == "EMPIRICAL_ACTION_CONSENSUS" for row in plans),
                "narrow_goal_plan_count": sum(row["primary_action"] is not None and row["primary_action"]["precision_level"] == "NARROW_CROSS_FOLD_GOAL" and row["recommendation_status"] == "EMPIRICAL_ACTION_CONSENSUS" for row in plans),
                "semantic_region_plan_count": sum(row["primary_action"] is not None and row["primary_action"]["precision_level"] == "SEMANTIC_REGION_GOAL" and row["recommendation_status"] == "EMPIRICAL_ACTION_CONSENSUS" for row in plans),
            },
            "warning": "This is a data-derived tactical plan, not a causal proof or a PhysX-feasibility certificate. A semantic region is intentionally not presented as a fixed narrow coordinate.",
        },
        "state_plans": plans,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--partition", type=Path, default=root / "nwnht_first_player_state_partition_v2.json")
    parser.add_argument("--families", type=Path, default=root / "nwnht_v2_tactical_action_families_v2.json")
    parser.add_argument("--fine-screen", type=Path, default=root / "nwnht_v2_tactical_action_fine_option_screen_v2.json")
    parser.add_argument("--outer-summary", type=Path, default=root / "nwnht_v2_tactical_action_outer_fold_summary_v2.json")
    parser.add_argument("--fold-results", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_runtime_state_plan_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    families = json.loads(args.families.read_text(encoding="utf-8"))["families"]
    fine_screen = json.loads(args.fine_screen.read_text(encoding="utf-8"))
    outer_summary = json.loads(args.outer_summary.read_text(encoding="utf-8"))
    fold_results = [json.loads(path.read_text(encoding="utf-8")) for path in args.fold_results]
    result = build(partition, families, fine_screen, outer_summary, fold_results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
