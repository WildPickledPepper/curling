"""Build the deployable macro-state graph for the first player.

Unlike the exploratory flat k-means graphs, this is intentionally two-layer:
the discrete layer classifies only a stable, explainable tactical topology;
fine geometry (gates, exact cover, raise/runback contact chains) is retained in
the board and must be decided by the local PhysX planner.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

try:
    from .discover_first_player_state_graph import FirstDecision, first_decisions
    from .discover_state_graph import DEFAULT_DB, DEFAULT_MATCH_TYPES, _iter_end_records
except ImportError:  # pragma: no cover - direct script invocation
    from discover_first_player_state_graph import FirstDecision, first_decisions
    from discover_state_graph import DEFAULT_DB, DEFAULT_MATCH_TYPES, _iter_end_records


def macro_type(features: dict[str, float]) -> str:
    """Classify an observable board relationship in priority order.

    This is not a move selector.  The ordering makes high-complexity and
    protected structures explicit before generic current-house control.
    """
    own_visible = features["first_visible"]
    opponent_visible = features["opponent_visible"]
    total_visible = own_visible + opponent_visible
    own_house = features["first_in_house"]
    opponent_house = features["opponent_in_house"]
    own_centre_guard = features["first_centre_guards"]
    opponent_centre_guard = features["opponent_centre_guards"]
    own_scoring = features["first_currently_scoring"] > 0.5
    opponent_scoring = features["opponent_currently_scoring"] > 0.5

    if total_visible == 0:
        return "EMPTY"
    # A crowded house has too many contact/raise/runback variants for a
    # durable discrete micro-state; preserve it as one explicit PhysX branch.
    if total_visible >= 5 and own_house + opponent_house >= 3:
        return "CROWDED_HOUSE_SEARCH_REQUIRED"
    if opponent_centre_guard >= 1 and opponent_house >= 1:
        return "OPPONENT_CENTRE_SHELL"
    if own_centre_guard >= 1 and own_house >= 1:
        return "OWN_CENTRE_SHELL"
    if opponent_scoring and opponent_house >= 1:
        return "OPPONENT_HOUSE_THREAT"
    if own_scoring and own_house >= 1:
        return "OWN_HOUSE_CONTROL"
    if own_house + opponent_house == 0 and features["first_guards"] + features["opponent_guards"] >= 1:
        return "GUARD_EXCHANGE"
    if total_visible <= 2:
        return "SPARSE_OPEN"
    return "MIXED_CONTESTED"


def medoid(group: list[FirstDecision], feature_names: list[str]) -> FirstDecision:
    means = {name: float(np.mean([item.features[name] for item in group])) for name in feature_names}
    return min(group, key=lambda item: sum((item.features[name] - means[name]) ** 2 for name in feature_names))


def build(decisions_by_end: list[list[FirstDecision]], min_support: int) -> dict[str, Any]:
    feature_names = sorted(decisions_by_end[0][0].features)
    raw_counts: Counter[tuple[int, str]] = Counter()
    for end in decisions_by_end:
        for decision in end:
            raw_counts[(decision.own_throw_number, macro_type(decision.features))] += 1
    groups: dict[str, list[FirstDecision]] = defaultdict(list)
    for end in decisions_by_end:
        for decision in end:
            raw_macro = macro_type(decision.features)
            decision.macro_state = raw_macro if raw_counts[(decision.own_throw_number, raw_macro)] >= min_support else "LOW_SUPPORT_SEARCH_REQUIRED"  # dynamic field; input is local only
            state_id = f"FIRST_K{decision.own_throw_number}_{decision.macro_state}"
            groups[state_id].append(decision)

    states: list[dict[str, Any]] = []
    for state_id, group in sorted(groups.items()):
        example = medoid(group, feature_names)
        macro = getattr(example, "macro_state")
        states.append(
            {
                "id": state_id,
                "own_throw_number": example.own_throw_number,
                "macro_state": macro,
                "sample_count": len(group),
                "observed_own_actions": dict(Counter(item.own_action for item in group).most_common()),
                "observed_opponent_replies": dict(Counter(item.opponent_reply for item in group).most_common()),
                "feature_means": {name: round(float(np.mean([item.features[name] for item in group])), 4) for name in feature_names},
                "physx_detail_required": macro in {"CROWDED_HOUSE_SEARCH_REQUIRED", "OPPONENT_CENTRE_SHELL", "OWN_CENTRE_SHELL", "LOW_SUPPORT_SEARCH_REQUIRED"},
                "medoid_example": {
                    "sample_uid": example.uid,
                    "match_id": example.match_id,
                    "visible_board": example.visible_board,
                },
            }
        )

    edges: Counter[tuple[str, str, str, str]] = Counter()
    examples: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    for end in decisions_by_end:
        for index, item in enumerate(end):
            source = f"FIRST_K{item.own_throw_number}_{getattr(item, 'macro_state')}"
            if index == 7:
                target = "TERMINAL_AFTER_OPPONENT_REPLY"
            else:
                next_item = end[index + 1]
                target = f"FIRST_K{next_item.own_throw_number}_{getattr(next_item, 'macro_state')}"
            key = (source, item.own_action, item.opponent_reply, target)
            edges[key] += 1
            if len(examples[key]) < 3:
                examples[key].append(item.uid)
    transitions = [
        {
            "from": source,
            "observed_own_action": own_action,
            "observed_opponent_reply": opponent_reply,
            "to": target,
            "count": count,
            "example_samples": examples[(source, own_action, opponent_reply, target)],
        }
        for (source, own_action, opponent_reply, target), count in sorted(edges.items(), key=lambda item: (-item[1], item[0]))
    ]
    return {"feature_names": feature_names, "states": states, "transitions": transitions, "sample_count": sum(len(end) for end in decisions_by_end)}


def run(database: Path, match_types: tuple[str, ...], min_support: int) -> dict[str, Any]:
    connection = sqlite3.connect(f"file:{database.resolve().as_posix()}?mode=ro", uri=True)
    accepted: list[list[FirstDecision]] = []
    examined = rejected = 0
    try:
        for record in _iter_end_records(connection, match_types):
            examined += 1
            decisions = first_decisions(record)
            if decisions is None:
                rejected += 1
            else:
                accepted.append(decisions)
    finally:
        connection.close()
    if not accepted:
        raise ValueError("No complete first-player decision chains were available.")
    graph = build(accepted, min_support=min_support)
    graph.update(
        {
            "schema": "nwnht_first_player_macro_state_graph_v0",
            "state_definition": "(first player's own throw number 1..8, explainable macro board topology)",
            "excluded_from_state_features": ["score", "end number", "game/end result", "hammer/control strategy", "external rule profile"],
            "local_rule_boundary": "The local simulator, not this graph, enforces legality from the own throw number.",
            "macro_classifier": {
                "EMPTY": "no visible stones",
                "CROWDED_HOUSE_SEARCH_REQUIRED": "at least five visible stones and at least three in the house",
                "OPPONENT_CENTRE_SHELL": "opponent has a centre guard and an in-house stone",
                "OWN_CENTRE_SHELL": "first player has a centre guard and an in-house stone",
                "OPPONENT_HOUSE_THREAT": "opponent currently has the closest in-house stone",
                "OWN_HOUSE_CONTROL": "first player currently has the closest in-house stone",
                "GUARD_EXCHANGE": "no in-house stones but at least one guard",
                "SPARSE_OPEN": "at most two visible stones after the above cases",
                "MIXED_CONTESTED": "remaining mixed topology",
                "LOW_SUPPORT_SEARCH_REQUIRED": f"a Kk × raw macro combination with fewer than {min_support} observations",
            },
            "minimum_state_support": min_support,
            "evidence_level": "NWNHT automatic board detection and recorded calls: macro-state/transition evidence only; no policy or PhysX proof.",
            "source": {"database": str(database), "match_types": list(match_types), "ends_examined": examined, "ends_accepted": len(accepted), "ends_rejected": rejected},
        }
    )
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "artifacts" / "nwnht_first_player_macro_state_graph_v1_supported.json")
    parser.add_argument("--match-types", default=",".join(DEFAULT_MATCH_TYPES))
    parser.add_argument("--min-support", type=int, default=250)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new --output deliberately.")
    if not args.database.is_file():
        raise SystemExit(f"Database not found: {args.database}")
    if args.min_support < 1:
        raise SystemExit("--min-support must be positive")
    graph = run(args.database, tuple(item.strip() for item in args.match_types.split(",") if item.strip()), args.min_support)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "accepted_ends": graph["source"]["ends_accepted"], "states": len(graph["states"]), "transitions": len(graph["transitions"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
