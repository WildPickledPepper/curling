#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rank v2 GoalState candidates with a finite-horizon empirical MDP.

This is deliberately a *historical trajectory model*, not a causal estimator:
``G`` is a realised, observable terminal-board template.  The program answers
which recorded continuations had the strongest backed-up end result after a
given recognised state.  It never calls PhysX, never adds match context to the
runtime state, and never claims that a historical association is a guaranteed
intervention effect.

The value recursion is evaluated from K8 to K1.  For K<8 the observed opponent
reply is folded into ``P(S_(k+1) | S_k, G_k)``.  A state without a supported
candidate uses its development-set state baseline as a continuation value;
this preserves the finite horizon without inventing a target for that state.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_causal_estimation_panel import fold_for_match
    from .build_goal_library_v2 import _goal_id, _signature
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import fold_for_match  # type: ignore
    from causal_state_machine.build_goal_library_v2 import _goal_id, _signature  # type: ignore


HOLDOUT_FOLD = 4
MIN_DEVELOPMENT_SUPPORT = 20
MIN_HOLDOUT_SUPPORT = 5
SHRINKAGE_PSEUDOCOUNT = 5.0
DEFAULT_BOOTSTRAP_REPLICATES = 100
BOOTSTRAP_LOWER_QUANTILE = 0.10
BOOTSTRAP_SEED = 20260717


def _outcome(margin: float) -> str:
    return "FIRST_SCORES" if margin > 0 else "OPPONENT_SCORES" if margin < 0 else "BLANK"


def _quantile(values: Iterable[float], q: float) -> float | None:
    ordered = sorted(values)
    if not ordered:
        return None
    index = min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))
    return ordered[index]


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    if not total:
        return []
    return [
        {"value": value, "count": count, "share": round(count / total, 6)}
        for value, count in counter.most_common()
    ]


def _weighted_mean(values: Iterable[tuple[float, int]], default: float) -> float:
    numerator = denominator = 0.0
    for value, weight in values:
        numerator += value * weight
        denominator += weight
    return default if denominator <= 0 else numerator / denominator


def _state_k_from_partition(partition: Mapping[str, Any]) -> dict[str, int]:
    return {str(row["state_id"]): int(row["K"]) for row in partition["states"]}


def collect_observations(
    transition_rows: Iterable[Mapping[str, Any]],
    templates: Iterable[Mapping[str, Any]],
    goals: Iterable[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Join candidate endpoint templates to their match-grouped trajectories."""

    by_panel = {
        f"{row['end_id']}:{row['own_global_shot_number']}": row
        for row in transition_rows
    }
    goal_by_id = {
        str(goal["goal_id"]): dict(goal)
        for goal in goals
        if bool(goal.get("runtime_goal_candidate"))
    }
    observations: list[dict[str, Any]] = []
    for template in templates:
        goal_id = _goal_id(_signature(template))
        if goal_id not in goal_by_id:
            continue
        source = by_panel.get(str(template["panel_key"]))
        if source is None:
            raise ValueError(f"missing transition row for candidate template {template['panel_key']}")
        observations.append({
            "match_id": int(source["match_id"]),
            "fold": fold_for_match(int(source["match_id"])),
            "K": int(template["K"]),
            "source_state": str(template["source_state"]),
            "goal_id": goal_id,
            "next_state": str(template["after_opponent_reply_state"]),
            "post_own_topology": str(template["post_own_topology"]),
            "margin": float(source["terminal_end_label"]["first_end_margin"]),
        })
    if not observations:
        raise ValueError("no candidate GoalState observations were collected")
    return observations, goal_by_id


def _estimate_values(
    observations: Iterable[Mapping[str, Any]],
    state_k: Mapping[str, int],
    *,
    min_development_support: int,
    shrinkage_pseudocount: float,
    match_weights: Mapping[int, int] | None = None,
) -> dict[str, Any]:
    """One development-sample K8->K1 backward pass.

    ``match_weights`` implements a match-cluster bootstrap without materialising
    a repeated row list.  A zero weight means that the match is absent in that
    bootstrap replicate.
    """

    rows = list(observations)
    if match_weights is not None:
        rows = [row for row in rows if int(match_weights.get(int(row["match_id"]), 0)) > 0]

    by_state: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    by_edge: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    by_k: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        weight = 1 if match_weights is None else int(match_weights[int(row["match_id"])])
        if weight <= 0:
            continue
        weighted = dict(row)
        weighted["_weight"] = weight
        by_state[str(row["source_state"])].append(weighted)
        by_edge[(str(row["source_state"]), str(row["goal_id"]))].append(weighted)
        by_k[int(row["K"])].append(weighted)

    global_by_k: dict[int, float] = {}
    for k in range(1, 9):
        global_by_k[k] = _weighted_mean(
            ((float(row["margin"]), int(row["_weight"])) for row in by_k[k]), 0.0
        )
    baseline: dict[str, float] = {}
    for state, state_rows in by_state.items():
        k = int(state_k.get(state, state_rows[0]["K"]))
        raw_count = sum(int(row["_weight"]) for row in state_rows)
        raw_sum = sum(float(row["margin"]) * int(row["_weight"]) for row in state_rows)
        baseline[state] = (raw_sum + shrinkage_pseudocount * global_by_k[k]) / (raw_count + shrinkage_pseudocount)

    edge_values: dict[tuple[str, str], dict[str, Any]] = {}
    value_by_state: dict[str, float] = {}
    for k in range(8, 0, -1):
        current_edges = [key for key, edge_rows in by_edge.items() if int(edge_rows[0]["K"]) == k]
        current_state_values: dict[str, list[float]] = defaultdict(list)
        for state, goal_id in current_edges:
            edge_rows = by_edge[(state, goal_id)]
            support = sum(int(row["_weight"]) for row in edge_rows)
            if k == 8:
                continuation_values = [float(row["margin"]) for row in edge_rows]
            else:
                continuation_values = [
                    value_by_state.get(str(row["next_state"]), baseline.get(str(row["next_state"]), global_by_k[k + 1]))
                    for row in edge_rows
                ]
            raw_mean = _weighted_mean(
                ((value, int(row["_weight"])) for value, row in zip(continuation_values, edge_rows)),
                baseline.get(state, global_by_k[k]),
            )
            state_prior = baseline.get(state, global_by_k[k])
            q_mean = (raw_mean * support + shrinkage_pseudocount * state_prior) / (support + shrinkage_pseudocount)
            reply = Counter()
            post_own = Counter()
            for row in edge_rows:
                weight = int(row["_weight"])
                reply[str(row["next_state"])] += weight
                post_own[str(row["post_own_topology"])] += weight
            edge_values[(state, goal_id)] = {
                "source_state": state,
                "goal_id": goal_id,
                "K": k,
                "development_support": support,
                "backed_up_value_mean": q_mean,
                "raw_continuation_mean": raw_mean,
                "dominant_next_state": _distribution(reply)[0]["value"] if reply else None,
                "after_opponent_reply_state_distribution": _distribution(reply),
                "dominant_post_own_topology": _distribution(post_own)[0]["value"] if post_own else None,
                "post_own_topology_distribution": _distribution(post_own),
            }
            if support >= min_development_support:
                current_state_values[state].append(q_mean)
        for state, values in current_state_values.items():
            value_by_state[state] = max(values)
        # States that have observations but no support-cleared candidate remain
        # at their empirical baseline for earlier continuation estimates.
        for state in (name for name, state_rows in by_state.items() if int(state_rows[0]["K"]) == k):
            value_by_state.setdefault(state, baseline[state])
    return {"edges": edge_values, "baseline": baseline, "global_by_k": global_by_k}


def _holdout_summary(observations: Iterable[Mapping[str, Any]], holdout_fold: int) -> dict[tuple[str, str], dict[str, Any]]:
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for row in observations:
        if int(row["fold"]) == holdout_fold:
            grouped[(str(row["source_state"]), str(row["goal_id"]))].append(row)
    summary: dict[tuple[str, str], dict[str, Any]] = {}
    for key, rows in grouped.items():
        outcomes = Counter(_outcome(float(row["margin"])) for row in rows)
        summary[key] = {
            "support": len(rows),
            "observed_mean_first_end_margin": round(sum(float(row["margin"]) for row in rows) / len(rows), 6),
            "observed_outcome_counts": dict(sorted(outcomes.items())),
            "observed_first_scores_rate": round(outcomes["FIRST_SCORES"] / len(rows), 6),
        }
    return summary


def _cluster_bootstrap(
    development_observations: list[Mapping[str, Any]],
    state_k: Mapping[str, int],
    *,
    min_development_support: int,
    shrinkage_pseudocount: float,
    replicates: int,
    seed: int,
) -> dict[tuple[str, str], list[float]]:
    if replicates <= 0:
        return {}
    match_ids = sorted({int(row["match_id"]) for row in development_observations})
    if not match_ids:
        return {}
    rng = random.Random(seed)
    values: dict[tuple[str, str], list[float]] = defaultdict(list)
    for _ in range(replicates):
        weights = Counter(rng.choice(match_ids) for _ in range(len(match_ids)))
        estimate = _estimate_values(
            development_observations, state_k,
            min_development_support=min_development_support,
            shrinkage_pseudocount=shrinkage_pseudocount,
            match_weights=weights,
        )
        for key, item in estimate["edges"].items():
            if int(item["development_support"]) >= min_development_support:
                values[key].append(float(item["backed_up_value_mean"]))
    return values


def _goal_payload(goal: Mapping[str, Any]) -> dict[str, Any]:
    """The terminal constraints the later execution layer must receive."""

    payload = {
        "goal_id": str(goal["goal_id"]),
        "observed_template_kind": goal["observed_template_kind"],
        "precision": goal["precision"],
        "active_final_region": goal["active_final_region"],
        "stone_constraints_when_unambiguous": goal["stone_constraints_when_unambiguous"],
        "dynamic_house_removal_binding_request": goal["dynamic_house_removal_binding_request"],
        "after_own_occupancy": goal["after_own_occupancy"],
    }
    # Tactical parent actions retain a small menu of original narrow endpoint
    # constraints.  Plain v2 fine goals simply do not carry these fields.
    if "tactical_target_zone" in goal:
        payload["tactical_target_zone"] = goal["tactical_target_zone"]
    if "fine_goal_options" in goal:
        payload["fine_goal_options"] = goal["fine_goal_options"]
    # A topology-constrained hierarchical goal is executable only if the
    # later planner satisfies both this anonymous board predicate and one
    # child endpoint/binding constraint.  Preserve this information instead
    # of flattening it back into an action label during value ranking.
    for optional in (
        "tactical_goal_id", "parent_action", "post_own_topology",
        "terminal_board_predicate", "execution_status",
    ):
        if optional in goal:
            payload[optional] = goal[optional]
    return payload


def _choose_primary_and_fallbacks(ranked: list[dict[str, Any]], maximum: int = 3) -> list[dict[str, Any]]:
    """Keep alternatives that aim for a materially different observed result."""

    selected: list[dict[str, Any]] = []
    seen_results: set[tuple[str | None, str | None]] = set()
    for item in ranked:
        result_key = (item["dominant_post_own_topology"], item["dominant_next_state"])
        if selected and result_key in seen_results:
            continue
        selected.append(item)
        seen_results.add(result_key)
        if len(selected) >= maximum:
            break
    return selected


def _spearman_rank_correlation(points: list[tuple[float, float]]) -> float | None:
    """Small dependency-free rank correlation for a descriptive holdout check."""

    if len(points) < 3:
        return None
    # Deterministic distinct ranks are enough here: value ties are already
    # broken by goal id in the caller before points are formed.
    left_order = {index: rank for rank, index in enumerate(sorted(range(len(points)), key=lambda i: points[i][0]))}
    right_order = {index: rank for rank, index in enumerate(sorted(range(len(points)), key=lambda i: points[i][1]))}
    xs = [float(left_order[index]) for index in range(len(points))]
    ys = [float(right_order[index]) for index in range(len(points))]
    mean_x, mean_y = sum(xs) / len(xs), sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = math.sqrt(sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys))
    return None if denominator == 0 else numerator / denominator


def build(
    observations: Iterable[Mapping[str, Any]],
    goals: Mapping[str, Mapping[str, Any]],
    state_k: Mapping[str, int],
    *,
    holdout_fold: int = HOLDOUT_FOLD,
    min_development_support: int = MIN_DEVELOPMENT_SUPPORT,
    min_holdout_support: int = MIN_HOLDOUT_SUPPORT,
    shrinkage_pseudocount: float = SHRINKAGE_PSEUDOCOUNT,
    bootstrap_replicates: int = 0,
    bootstrap_seed: int = BOOTSTRAP_SEED,
) -> dict[str, Any]:
    """Return ranked edges and one primary/two result-different fallbacks per state."""

    all_rows = list(observations)
    dev_rows = [row for row in all_rows if int(row["fold"]) != holdout_fold]
    holdout = _holdout_summary(all_rows, holdout_fold)
    point_estimate = _estimate_values(
        dev_rows, state_k,
        min_development_support=min_development_support,
        shrinkage_pseudocount=shrinkage_pseudocount,
    )
    # This separate pass never feeds the development rank.  It is only a
    # descriptive answer to "does the held-out trajectory ordering resemble
    # the development ordering?"  Candidate-set selection leakage is still
    # documented in the manifest below.
    holdout_estimate = _estimate_values(
        [row for row in all_rows if int(row["fold"]) == holdout_fold], state_k,
        min_development_support=0,
        shrinkage_pseudocount=shrinkage_pseudocount,
    )
    bootstrap = _cluster_bootstrap(
        dev_rows, state_k,
        min_development_support=min_development_support,
        shrinkage_pseudocount=shrinkage_pseudocount,
        replicates=bootstrap_replicates,
        seed=bootstrap_seed,
    )
    candidate_values: list[dict[str, Any]] = []
    for key, estimate in sorted(point_estimate["edges"].items()):
        state, goal_id = key
        holdout_item = holdout.get(key, {"support": 0, "observed_mean_first_end_margin": None, "observed_outcome_counts": {}, "observed_first_scores_rate": None})
        boot_values = bootstrap.get(key, [])
        holdout_value = holdout_estimate["edges"].get(key)
        lcb = _quantile(boot_values, BOOTSTRAP_LOWER_QUANTILE) if boot_values else float(estimate["backed_up_value_mean"])
        ucb = _quantile(boot_values, 1.0 - BOOTSTRAP_LOWER_QUANTILE) if boot_values else float(estimate["backed_up_value_mean"])
        development_ok = int(estimate["development_support"]) >= min_development_support
        holdout_ok = int(holdout_item["support"]) >= min_holdout_support
        candidate_values.append({
            **estimate,
            "backed_up_value_lcb": None if lcb is None else round(lcb, 6),
            "backed_up_value_ucb": None if ucb is None else round(ucb, 6),
            "bootstrap_replicate_count": len(boot_values),
            "holdout": holdout_item,
            "holdout_backed_up_value_mean": None if holdout_value is None else round(float(holdout_value["backed_up_value_mean"]), 6),
            "eligible_for_empirical_ranking": development_ok and holdout_ok,
            "eligibility_reasons": [] if development_ok and holdout_ok else [
                *([] if development_ok else ["development_support_below_minimum"]),
                *([] if holdout_ok else ["holdout_support_below_minimum"]),
            ],
            "goal_state": _goal_payload(goals[goal_id]),
            "evidence_status": "EMPIRICAL_TRAJECTORY_VALUE_NOT_CAUSAL_PROOF",
            "warning": "Rank is a finite-horizon historical-continuation estimate. It is not a proof that issuing this GoalState causes the same result against every opponent.",
        })
    by_state: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in candidate_values:
        by_state[str(item["source_state"])].append(item)
    plans: list[dict[str, Any]] = []
    for state, k in sorted(state_k.items(), key=lambda pair: (pair[1], pair[0])):
        eligible = [item for item in by_state.get(state, []) if item["eligible_for_empirical_ranking"]]
        # Q mean answers the tactical question "which continuation is best in
        # the historical model?"  The bootstrap LCB remains a visible
        # confidence/risk guard; using it as the sole objective would instead
        # select the least-variable action, even when its estimated and
        # held-out expected value are worse.
        eligible.sort(key=lambda item: (
            -float(item["backed_up_value_mean"]), -float(item["backed_up_value_lcb"]),
            -int(item["development_support"]), str(item["goal_id"]),
        ))
        chosen = _choose_primary_and_fallbacks(eligible)
        comparable = [
            item for item in eligible
            if item["holdout_backed_up_value_mean"] is not None and int(item["holdout"]["support"]) >= min_holdout_support
        ]
        heldout_ranked = sorted(
            comparable,
            key=lambda item: (-float(item["holdout_backed_up_value_mean"]), str(item["goal_id"])),
        )
        holdout_rank = {item["goal_id"]: index + 1 for index, item in enumerate(heldout_ranked)}
        primary_holdout_rank = None if not chosen else holdout_rank.get(chosen[0]["goal_id"])
        correlation = _spearman_rank_correlation([
            (float(item["backed_up_value_mean"]), float(item["holdout_backed_up_value_mean"]))
            for item in comparable
        ])
        plans.append({
            "state_id": state,
            "K": k,
            "recommendation_status": "EMPIRICAL_RANKED_GOALS" if chosen else "SEARCH_REQUIRED_NO_SUPPORTED_GOAL",
            "primary_goal": chosen[0] if chosen else None,
            "fallback_goals": chosen[1:],
            "eligible_goal_count": len(eligible),
            "candidate_goal_count": len(by_state.get(state, [])),
            "descriptive_holdout_rank_diagnostic": {
                "comparable_goal_count": len(comparable),
                "development_vs_holdout_spearman": None if correlation is None else round(correlation, 6),
                "primary_goal_holdout_rank": primary_holdout_rank,
                "primary_goal_is_holdout_top3": None if primary_holdout_rank is None else primary_holdout_rank <= 3,
                "warning": "Diagnostic only. It does not remove candidate-set selection leakage and is not a causal policy evaluation.",
            },
            "runtime_note": "Give the selected GoalState constraints to the later local-rule/PhysX execution layer. A current solver-budget miss is not a physical-impossibility conclusion.",
        })
    manifest = {
        "schema": "nwnht_v2_empirical_finite_horizon_mdp_value_v0",
        "decision_model": "first-player finite-horizon empirical MDP; historical opponent reply is an observed transition distribution",
        "runtime_inputs": "K plus current board coordinates only",
        "excluded_runtime_inputs": ["score", "end_number", "team", "event", "called_shot", "PhysX parameters"],
        "development_holdout_split": {
            "kind": "deterministic SHA-256 grouped by match_id via fold_for_match",
            "holdout_fold": holdout_fold,
            "development_rows": len(dev_rows),
            "holdout_rows": len(all_rows) - len(dev_rows),
        },
        "recursion": "K8 terminal margin; K1-K7 expected value of the next first-player state after observed opponent reply; unsupported next state uses development state baseline.",
        "ranking_rule": "Rank eligible candidates by backed_up_value_mean (the empirical Q estimate). Report bootstrap LCB/UCB as uncertainty and risk diagnostics, not as a substitute objective.",
        "thresholds": {
            "min_development_support": min_development_support,
            "min_holdout_support": min_holdout_support,
            "shrinkage_pseudocount": shrinkage_pseudocount,
            "bootstrap_replicates": bootstrap_replicates,
            "bootstrap_lcb_quantile": BOOTSTRAP_LOWER_QUANTILE,
        },
        "summary": {
            "candidate_goal_value_count": len(candidate_values),
            "states_with_ranked_goal": sum(bool(plan["primary_goal"]) for plan in plans),
            "ranked_goal_count": sum(int(plan["eligible_goal_count"]) for plan in plans),
            "states_with_comparable_holdout_goal_ranks": sum(
                int(plan["descriptive_holdout_rank_diagnostic"]["comparable_goal_count"]) >= 3 for plan in plans
            ),
        },
        "selection_leakage_note": "The present state partition and structural GoalState candidate set were learned before this split from the full corpus. Holdout rows here test rank stability descriptively; they are not an independent causal policy evaluation.",
        "prohibition": "Do not interpret high backed-up value as a causal guarantee or a complete playing strategy. PhysX reachability and local-rule legality are deliberately outside this artifact.",
    }
    return {"manifest": manifest, "candidate_values": candidate_values, "state_plans": plans}


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--goals", type=Path, default=root / "nwnht_v2_goal_template_families_v0.json")
    parser.add_argument("--partition", type=Path, default=root / "nwnht_first_player_state_partition_v2.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_empirical_mdp_value_v0.json")
    parser.add_argument("--bootstrap-replicates", type=int, default=DEFAULT_BOOTSTRAP_REPLICATES)
    parser.add_argument("--holdout-fold", type=int, default=HOLDOUT_FOLD)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    observations, goals = collect_observations(_read_jsonl(args.transitions), _read_jsonl(args.templates), json.loads(args.goals.read_text(encoding="utf-8")))
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    result = build(
        observations, goals, _state_k_from_partition(partition),
        holdout_fold=args.holdout_fold,
        bootstrap_replicates=args.bootstrap_replicates,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
