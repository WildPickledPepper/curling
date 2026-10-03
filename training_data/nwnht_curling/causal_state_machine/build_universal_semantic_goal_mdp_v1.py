#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the complete same-K semantic MDP: S_k -> G_k -> S_(k+1).

``G_k`` exists independently of whether an exact endpoint circle is stable.
It is a tactical post-own objective: K, change in house occupancy, anonymous
removal/placement effect, and desired control/macro topology.  Exact complete
post-own layouts, narrow endpoint circles and dynamic stone bindings are
children of that semantic target, retained as execution evidence only.

The model is historical and finite-horizon.  It does not infer player intent,
call PhysX, or claim that an observational edge causes its recorded outcome.
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
    from .build_goal_library_v2 import _active_region, _canonical, _grid_key
except ImportError:  # pragma: no cover
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import FOLDS, fold_for_match  # type: ignore
    from causal_state_machine.build_double_outcome_goal_contracts_v1 import parse_post_own_topology  # type: ignore
    from causal_state_machine.build_goal_library_v2 import _active_region, _canonical, _grid_key  # type: ignore


SHRINKAGE_PSEUDOCOUNT = 5.0
MAX_GOALS_PER_STATE = 3
MAX_FINE_OPTIONS_PER_GOAL = 3


def physically_admissible_own_shot_observation(row: Mapping[str, Any]) -> bool:
    """Reject impossible opponent-stone creation before learning a semantic G.

    During our own delivery an opponent stone may move into/out of the house,
    but no new opponent stone can appear.  Negative total removals therefore
    signal a frame/panel alignment anomaly in a historical record, not a
    feasible action outcome in the local rules or PhysX simulator.
    """

    return int(row["observed_delta"]["opponent_removed_count"]) >= 0


def _semantic_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    """A compact G key: same K tactical effect, never an endpoint point."""

    delta = row["observed_delta"]
    predicate = parse_post_own_topology(str(row["post_own_topology"]))
    return (
        int(row["K"]),
        str(row["observed_template_kind"]),
        int(delta["first_house"]),
        int(delta["opponent_house"]),
        int(delta["opponent_removed_count"]),
        int(delta["opponent_house_removed_count"]),
        str(predicate["control"]),
        str(predicate["macro"]),
    )


def _goal_id(source_state: str, key: tuple[Any, ...]) -> str:
    digest = hashlib.sha256((source_state + "|" + repr(key)).encode("utf-8")).hexdigest()[:16]
    return f"nwnht_v2_semantic_goal_{digest}"


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [
        {"value": value, "count": count, "share": round(count / total, 6)}
        for value, count in counter.most_common()
    ] if total else []


def _fine_signature(row: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        str(row["precision"]),
        _grid_key(row.get("active_final_point")),
        _canonical(row.get("stone_constraints_when_unambiguous", [])),
        _canonical(row.get("dynamic_house_removal_binding_request")),
        _canonical(row.get("after_own_occupancy", {})),
    )


def _fine_options(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[_fine_signature(row)].append(row)
    options: list[dict[str, Any]] = []
    for signature, members in grouped.items():
        precision, _, selectors_json, binding_json, occupancy_json = signature
        points = [
            (float(row["active_final_point"]["x_m"]), float(row["active_final_point"]["y_m"]))
            for row in members if row.get("active_final_point") is not None
        ]
        region = _active_region(points)
        selectors = json.loads(selectors_json)
        binding = json.loads(binding_json)
        # A semantic G may be valid even without a fine child.  Do not emit a
        # fake execution target for no-observable-change records.
        if region is None and not selectors and binding is None:
            continue
        options.append({
            "precision": precision,
            "active_final_region": region,
            "stone_constraints_when_unambiguous": selectors,
            "dynamic_house_removal_binding_request": binding,
            "after_own_occupancy": json.loads(occupancy_json),
            "historical_support": len(members),
            "post_own_topology_distribution": _distribution(Counter(str(row["post_own_topology"]) for row in members)),
            "examples": [str(row["panel_key"]) for row in members[:5]],
            "warning": "A historical implementation child, not a guarantee that this current board is physically reachable.",
        })
    options.sort(key=lambda item: (-int(item["historical_support"]), _canonical(item)))
    return options[:MAX_FINE_OPTIONS_PER_GOAL]


def collect(
    template_rows: Iterable[Mapping[str, Any]], transitions: Iterable[Mapping[str, Any]],
    state_k: Mapping[str, int],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Compile all observed semantic edges without any fine-support gate."""

    transition_by_panel = {f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transitions}
    grouped: dict[tuple[str, tuple[Any, ...]], list[dict[str, Any]]] = defaultdict(list)
    rejected_impossible = 0
    for raw in template_rows:
        if not physically_admissible_own_shot_observation(raw):
            rejected_impossible += 1
            continue
        source_state = str(raw["source_state"])
        k = int(raw["K"])
        if state_k.get(source_state) != k:
            raise ValueError(f"source K mismatch: {source_state} / {k}")
        next_state = str(raw["after_opponent_reply_state"])
        if k == 8:
            if next_state != "END":
                raise ValueError(f"K8 must lead to END, got {next_state}")
        elif state_k.get(next_state) != k + 1:
            raise ValueError(f"bad next-state K: {source_state} -> {next_state}")
        transition = transition_by_panel.get(str(raw["panel_key"]))
        if transition is None:
            raise ValueError(f"missing transition: {raw['panel_key']}")
        grouped[(source_state, _semantic_key(raw))].append({
            **dict(raw),
            "match_id": int(transition["match_id"]),
            "fold": fold_for_match(int(transition["match_id"])),
            "next_state": next_state,
            "margin": float(transition["terminal_end_label"]["first_end_margin"]),
        })

    goals: dict[str, dict[str, Any]] = {}
    observations: list[dict[str, Any]] = []
    for (state, key), rows in grouped.items():
        k, kind, first_house_delta, opponent_house_delta, removed, house_removed, control, macro = key
        goal_id = _goal_id(state, key)
        topology_distribution = _distribution(Counter(str(row["post_own_topology"]) for row in rows))
        fine_options = _fine_options(rows)
        goals[goal_id] = {
            "goal_id": goal_id,
            "source_state": state,
            "K": k,
            "semantic_effect": {
                "observed_template_kind": kind,
                "first_house_delta": first_house_delta,
                "opponent_house_delta": opponent_house_delta,
                "opponent_removed_count": removed,
                "opponent_house_removed_count": house_removed,
            },
            "semantic_terminal_predicate": {"control": control, "macro": macro},
            "post_own_topology_distribution": topology_distribution,
            "historical_direct_support": len(rows),
            "fine_goal_options": fine_options,
            "fine_execution_status": "HAS_HISTORICAL_FINE_IMPLEMENTATION" if fine_options else "NO_HISTORICAL_BINDABLE_FINE_IMPLEMENTATION",
            "warning": "This is an observable same-K tactical target. Exact post-own layouts and fine children are optional execution evidence, not part of semantic target existence.",
        }
        observations.extend({
            "source_state": state, "goal_id": goal_id, "K": k,
            "match_id": int(row["match_id"]), "fold": int(row["fold"]),
            "next_state": str(row["next_state"]), "margin": float(row["margin"]),
        } for row in rows)
    # The public return shape stays compatible; the count is attached to each
    # observation only through the generated manifest below via ``build``.
    # Keep it on the function for the CLI audit without changing callers.
    collect.last_rejected_impossible_observations = rejected_impossible  # type: ignore[attr-defined]
    return goals, observations


def _estimate(observations: Iterable[Mapping[str, Any]], state_k: Mapping[str, int]) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, float]]:
    rows = list(observations)
    by_state: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    by_edge: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    by_k: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_state[str(row["source_state"])].append(row)
        by_edge[(str(row["source_state"]), str(row["goal_id"]))].append(row)
        by_k[int(row["K"])].append(row)
    global_mean = {
        k: (sum(float(row["margin"]) for row in by_k[k]) / len(by_k[k]) if by_k[k] else 0.0)
        for k in range(1, 9)
    }
    baseline = {
        state: (sum(float(row["margin"]) for row in items) + SHRINKAGE_PSEUDOCOUNT * global_mean[state_k[state]]) / (len(items) + SHRINKAGE_PSEUDOCOUNT)
        for state, items in by_state.items()
    }
    values: dict[str, float] = {}
    edges: dict[tuple[str, str], dict[str, Any]] = {}
    for k in range(8, 0, -1):
        state_candidates: dict[str, list[float]] = defaultdict(list)
        for (state, goal_id), items in by_edge.items():
            if int(items[0]["K"]) != k:
                continue
            continuation = [
                float(row["margin"]) if k == 8 else values.get(str(row["next_state"]), baseline.get(str(row["next_state"]), global_mean[k + 1]))
                for row in items
            ]
            raw_mean = sum(continuation) / len(continuation)
            q = (len(items) * raw_mean + SHRINKAGE_PSEUDOCOUNT * baseline[state]) / (len(items) + SHRINKAGE_PSEUDOCOUNT)
            replies = Counter(str(row["next_state"]) for row in items)
            edges[(state, goal_id)] = {
                "source_state": state, "goal_id": goal_id, "K": k,
                "direct_support": len(items),
                "backed_up_value_mean": round(q, 6),
                "raw_continuation_mean": round(raw_mean, 6),
                "after_opponent_reply_state_distribution": _distribution(replies),
                "dominant_next_state": _distribution(replies)[0]["value"],
            }
            state_candidates[state].append(q)
        for state, candidates in state_candidates.items():
            values[state] = max(candidates)
    # Every state has at least one raw edge; this only protects malformed test input.
    for state in state_k:
        values.setdefault(state, baseline.get(state, global_mean[state_k[state]]))
    return edges, values


def _rank(edges: Mapping[tuple[str, str], Mapping[str, Any]], state: str) -> list[dict[str, Any]]:
    ranked = [dict(edge) for (source, _), edge in edges.items() if source == state]
    ranked.sort(key=lambda item: (-float(item["backed_up_value_mean"]), -int(item["direct_support"]), str(item["goal_id"])))
    return ranked[:MAX_GOALS_PER_STATE]


def build(goals: Mapping[str, Mapping[str, Any]], observations: Iterable[Mapping[str, Any]], state_k: Mapping[str, int]) -> dict[str, Any]:
    """Return a primary semantic G and its S_(k+1) transition for every S."""

    all_rows = [dict(row) for row in observations]
    full_edges, _ = _estimate(all_rows, state_k)
    fold_primary: dict[str, Counter[str]] = defaultdict(Counter)
    fold_available: dict[str, int] = Counter()
    for holdout in range(FOLDS):
        train_edges, _ = _estimate([row for row in all_rows if int(row["fold"]) != holdout], state_k)
        for state in state_k:
            ranked = _rank(train_edges, state)
            if ranked:
                fold_available[state] += 1
                fold_primary[state][str(ranked[0]["goal_id"])] += 1

    plans: list[dict[str, Any]] = []
    for state, k in sorted(state_k.items(), key=lambda item: (item[1], item[0])):
        ranked = _rank(full_edges, state)
        if not ranked:
            raise ValueError(f"universal semantic model lost all goals for {state}")
        rendered = []
        for edge in ranked:
            goal = dict(goals[str(edge["goal_id"])])
            if int(goal["K"]) != k:
                raise ValueError(f"goal K mismatch for {state}")
            rendered.append({**edge, "goal_state": goal})
        primary = rendered[0]
        votes = fold_primary[state]
        primary_votes = int(votes.get(str(primary["goal_id"]), 0))
        evidence = (
            "SEMANTIC_GOAL_FIVE_FOLD_PRIMARY_CONSENSUS" if primary_votes >= 4 else
            "SEMANTIC_GOAL_PARTIAL_CROSS_FOLD_SUPPORT" if primary_votes else
            "SEMANTIC_GOAL_FULL_DATA_ONLY_LOW_SUPPORT"
        )
        plans.append({
            "state_id": state, "K": k,
            "recommendation_status": "SEMANTIC_GOAL_AVAILABLE",
            "evidence_status": evidence,
            "primary_goal": primary,
            "fallback_goals": rendered[1:],
            "folds_with_any_semantic_goal": int(fold_available[state]),
            "primary_goal_id_distribution": dict(votes.most_common()),
            "runtime_contract": "G.K equals S.K. After opponent response, observe the actual board and classify it as S_(K+1); the stored distribution is a prediction, not a forced successor.",
        })
    return {
        "manifest": {
            "schema": "nwnht_v2_universal_semantic_goal_mdp_v2",
            "decision_chain": "S_k -> G_k (same K semantic terminal predicate) -> P(S_(k+1) | S_k,G_k)",
            "state_count": len(state_k), "goal_count": len(goals), "observation_count": len(all_rows),
            "rejected_physically_impossible_observation_count": int(getattr(collect, "last_rejected_impossible_observations", 0)),
            "guarantee": "Every recognised S_k has at least one observed same-K semantic G_k in this artifact.",
            "prohibition": "A semantic goal is not automatically a solver-ready endpoint, a causal intervention result, a rule validation, or a win guarantee.",
        },
        "state_plans": plans,
    }


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--partition", type=Path, default=root / "nwnht_first_player_state_partition_v2.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_universal_semantic_goal_mdp_v2.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    state_k = {str(row["state_id"]): int(row["K"]) for row in partition["states"]}
    goals, observations = collect(_read_jsonl(args.templates), _read_jsonl(args.transitions), state_k)
    result = build(goals, observations, state_k)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
