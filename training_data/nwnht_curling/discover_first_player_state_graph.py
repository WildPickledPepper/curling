"""Cluster only the first player's eight decision points from NWNHT boards.

This script implements the deliberately narrow state definition agreed for the
local AI:

    state = (first player's own throw number k=1..8, tactical board topology)

Scores, end number, winner, hammer strategy and real-world rule variants are
not features.  The local simulator owns legality.  NWNHT is used only to find
repeated board topologies and observed action/reply/next-topology transitions.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

try:  # Supports both `python file.py` and package imports in tests.
    from .discover_state_graph import (
        DEFAULT_DB,
        DEFAULT_MATCH_TYPES,
        EndRecord,
        _assign_and_refine,
        _fit_kmeans,
        _iter_end_records,
        board_features,
        infer_colour_owners,
        normalize_action,
    )
except ImportError:  # pragma: no cover - direct-script path
    from discover_state_graph import (
        DEFAULT_DB,
        DEFAULT_MATCH_TYPES,
        EndRecord,
        _assign_and_refine,
        _fit_kmeans,
        _iter_end_records,
        board_features,
        infer_colour_owners,
        normalize_action,
    )


CONTEXT_FEATURES = {"score_diff_first_clipped", "end_number_clipped", "shot_in_end"}


@dataclass
class FirstDecision:
    uid: str
    end_id: int
    match_id: int
    own_throw_number: int
    own_action: str
    opponent_reply: str
    features: dict[str, float]
    visible_board: list[dict[str, float | str]]
    state_id: str | None = None


def _nearest_labels(matrix: np.ndarray, centers: np.ndarray) -> np.ndarray:
    return ((matrix[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)


def select_k_by_heldout_action_stability(group: list[FirstDecision], feature_names: list[str], maximum: int, min_cluster_size: int, seed: int) -> tuple[int, list[dict[str, float | int]]]:
    """Choose the smallest geometrical partition that predicts held-out calls.

    Matches, rather than individual shots, are held out.  A state partition
    that only exists because it memorised one match should not predict calls
    in unseen matches.  This does *not* make historical calls a recommendation:
    it is only a test of whether a proposed geometrical split is reproducible
    as a decision distinction.
    """
    raw = np.asarray([[item.features[name] for name in feature_names] for item in group], dtype=np.float64)
    validation_mask = np.asarray([item.match_id % 5 == 0 for item in group], dtype=bool)
    if validation_mask.sum() < max(100, len(group) // 10):
        validation_mask = np.asarray([item.match_id % 4 == 0 for item in group], dtype=bool)
    train_mask = ~validation_mask
    train, validation = raw[train_mask], raw[validation_mask]
    train_items = [item for item, included in zip(group, train_mask) if included]
    validation_items = [item for item, included in zip(group, validation_mask) if included]
    if not len(train) or not len(validation):
        return 1, []
    mean, std = train.mean(axis=0), train.std(axis=0)
    std[std < 1e-8] = 1.0
    train, validation = (train - mean) / std, (validation - mean) / std
    action_names = sorted({item.own_action for item in group})
    action_index = {action: index for index, action in enumerate(action_names)}
    train_actions = np.asarray([action_index[item.own_action] for item in train_items], dtype=np.int32)
    validation_actions = np.asarray([action_index[item.own_action] for item in validation_items], dtype=np.int32)
    fit_limit = min(1200, len(train))
    fit_indices = np.linspace(0, len(train) - 1, fit_limit, dtype=np.int64)
    fit_train = train[fit_indices]
    metrics: list[dict[str, float | int]] = []
    for k in range(1, min(maximum, len(train) // max(1, min_cluster_size)) + 1):
        _, centers, _ = _fit_kmeans(fit_train, k, seed + k, max_iterations=15)
        train_labels, centers = _assign_and_refine(train, centers, rounds=2)
        counts = np.bincount(train_labels, minlength=k)
        if counts.min() < min_cluster_size:
            continue
        validation_labels = _nearest_labels(validation, centers)
        action_counts = np.ones((k, len(action_names)), dtype=np.float64)  # Laplace smoothing
        for label, action in zip(train_labels, train_actions):
            action_counts[int(label), int(action)] += 1.0
        probabilities = action_counts / action_counts.sum(axis=1, keepdims=True)
        losses = -np.log(probabilities[validation_labels, validation_actions])
        metrics.append(
            {
                "k": k,
                "heldout_action_nll": round(float(losses.mean()), 6),
                "heldout_action_se": round(float(losses.std(ddof=1) / math.sqrt(len(losses))), 6),
                "minimum_train_cluster": int(counts.min()),
            }
        )
    if not metrics:
        return 1, []
    best = min(metrics, key=lambda item: float(item["heldout_action_nll"]))
    threshold = float(best["heldout_action_nll"]) + float(best["heldout_action_se"])
    selected = min((item for item in metrics if float(item["heldout_action_nll"]) <= threshold), key=lambda item: int(item["k"]))
    return int(selected["k"]), metrics


def topology_features(board: list[dict[str, float | str]]) -> dict[str, float]:
    """Make the board mirror-invariant and remove all score/time context.

    A left/right reflection should not create a new discrete tactical state:
    the later PhysX search can choose the corresponding physical side.  We
    calculate the existing auditable geometry features for both orientations
    and retain the lexicographically smaller one as a canonical description.
    """
    def describe(candidate: list[dict[str, float | str]]) -> dict[str, float]:
        raw = board_features(candidate, score_diff=0, end_number=0, shot=0)
        return {name: value for name, value in raw.items() if name not in CONTEXT_FEATURES}

    original = describe(board)
    mirrored = describe(
        [{"owner": stone["owner"], "x_m": -float(stone["x_m"]), "y_m": float(stone["y_m"])} for stone in board]
    )
    names = sorted(original)
    return mirrored if tuple(mirrored[name] for name in names) < tuple(original[name] for name in names) else original


def first_decisions(record: EndRecord) -> list[FirstDecision] | None:
    """Extract eight pre-shot boards from one strictly usable four-player end."""
    if set(record.frames) != set(range(17)):
        return None
    if any(record.frames[shot].throwing_team is None for shot in range(1, 17)):
        return None
    first_team, opponent_team = record.frames[1].throwing_team, record.frames[2].throwing_team
    if not first_team or not opponent_team or first_team == opponent_team:
        return None
    if any(record.frames[shot].throwing_team != (first_team if shot % 2 else opponent_team) for shot in range(1, 17)):
        return None
    owners = infer_colour_owners(record.frames, record.teams)
    if owners is None:
        return None

    result: list[FirstDecision] = []
    for own_throw_number in range(1, 9):
        shot = own_throw_number * 2 - 1
        board = [
            {"owner": "first" if owners[colour] == first_team else "opponent", "x_m": x, "y_m": y}
            for colour, x, y in record.frames[shot - 1].stones
            if colour in owners
        ]
        result.append(
            FirstDecision(
                uid=f"{record.end_id}:{shot}",
                end_id=record.end_id,
                match_id=record.match_id,
                own_throw_number=own_throw_number,
                own_action=normalize_action(record.frames[shot].call),
                opponent_reply=normalize_action(record.frames[shot + 1].call),
                features=topology_features(board),
                visible_board=board,
            )
        )
    return result


def discover(decisions_by_end: list[list[FirstDecision]], max_clusters: int, min_cluster_size: int, seed: int) -> dict[str, Any]:
    all_decisions = [item for end in decisions_by_end for item in end]
    feature_names = sorted(all_decisions[0].features)
    by_throw: dict[int, list[FirstDecision]] = defaultdict(list)
    for decision in all_decisions:
        by_throw[decision.own_throw_number].append(decision)

    state_members: dict[str, list[FirstDecision]] = defaultdict(list)
    partitions: list[dict[str, int]] = []
    for own_throw_number, group in sorted(by_throw.items()):
        raw = np.asarray([[item.features[name] for name in feature_names] for item in group], dtype=np.float64)
        mean, std = raw.mean(axis=0), raw.std(axis=0)
        std[std < 1e-8] = 1.0
        normalized = (raw - mean) / std
        selected_k, selection_metrics = select_k_by_heldout_action_stability(
            group, feature_names, max_clusters, min_cluster_size, seed + own_throw_number
        )
        fit_limit = 2500
        if len(normalized) > fit_limit:
            indices = np.linspace(0, len(normalized) - 1, fit_limit, dtype=np.int64)
            fit_matrix = normalized[indices]
        else:
            fit_matrix = normalized
        _, centers, _ = _fit_kmeans(fit_matrix, selected_k, seed + own_throw_number, max_iterations=25)
        labels, centers = _assign_and_refine(normalized, centers)
        medoid_indices = [int(np.argmin(((normalized - centers[index]) ** 2).sum(axis=1))) for index in range(selected_k)]
        order = sorted(range(selected_k), key=lambda index: (group[medoid_indices[index]].end_id, group[medoid_indices[index]].uid))
        remap = {old: new + 1 for new, old in enumerate(order)}
        for item, label in zip(group, labels):
            item.state_id = f"FIRST_K{own_throw_number}_C{remap[int(label)]:02d}"
            state_members[item.state_id].append(item)
        partitions.append(
            {
                "own_throw_number": own_throw_number,
                "samples": len(group),
                "selected_clusters": selected_k,
                "selection_metrics": selection_metrics,
            }
        )

    states: list[dict[str, Any]] = []
    for state_id, group in sorted(state_members.items()):
        means = {name: round(float(np.mean([item.features[name] for item in group])), 4) for name in feature_names}
        medoid = min(group, key=lambda item: sum((item.features[name] - means[name]) ** 2 for name in feature_names))
        states.append(
            {
                "id": state_id,
                "sample_count": len(group),
                "observed_own_actions": dict(Counter(item.own_action for item in group).most_common()),
                "observed_opponent_replies": dict(Counter(item.opponent_reply for item in group).most_common()),
                "feature_means": means,
                "medoid_example": {
                    "sample_uid": medoid.uid,
                    "match_id": medoid.match_id,
                    "own_action": medoid.own_action,
                    "opponent_reply": medoid.opponent_reply,
                    "visible_board": medoid.visible_board,
                },
            }
        )

    edges: Counter[tuple[str, str, str, str]] = Counter()
    examples: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    for end in decisions_by_end:
        for index, item in enumerate(end):
            assert item.state_id
            target = end[index + 1].state_id if index < 7 else "TERMINAL_AFTER_OPPONENT_REPLY"
            assert target
            key = (item.state_id, item.own_action, item.opponent_reply, target)
            edges[key] += 1
            if len(examples[key]) < 3:
                examples[key].append(item.uid)
    transitions = [
        {
            "from": source,
            "observed_own_action": own_action,
            "observed_opponent_reply": reply,
            "to": target,
            "count": count,
            "example_samples": examples[(source, own_action, reply, target)],
        }
        for (source, own_action, reply, target), count in sorted(edges.items(), key=lambda row: (-row[1], row[0]))
    ]
    return {"feature_names": feature_names, "partitions": partitions, "states": states, "transitions": transitions, "sample_count": len(all_decisions)}


def run(database: Path, match_types: tuple[str, ...], max_clusters: int, min_cluster_size: int, seed: int) -> dict[str, Any]:
    import sqlite3

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
    graph = discover(accepted, max_clusters, min_cluster_size, seed)
    graph.update(
        {
            "schema": "nwnht_first_player_state_graph_v0",
            "state_definition": "(first player's own throw number 1..8, mirror-canonical tactical board topology)",
            "excluded_from_state_features": ["score", "end number", "game/end result", "hammer/control strategy", "external rule profile"],
            "local_rule_boundary": "The local simulator enforces legality from the own throw number.  NWNHT does not define legality for this graph.",
            "evidence_level": "NWNHT automatic board detection and recorded calls: candidate topology/transition evidence only; not a policy recommendation or PhysX proof.",
            "source": {"database": str(database), "match_types": list(match_types), "ends_examined": examined, "ends_accepted": len(accepted), "ends_rejected": rejected},
            "clustering": {
                "per_partition": "one partition for each first-player own throw number",
                "maximum_clusters": max_clusters,
                "minimum_cluster_size": min_cluster_size,
                "candidate_fit": "k-means geometry fit on at most 2,500 evenly spaced rows; all accepted rows are assigned and refined",
                "selection": "match-held-out historical-call NLL; choose the smallest k within one standard error of the best held-out NLL",
                "seed": seed,
            },
        }
    )
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "artifacts" / "nwnht_first_player_state_graph_v1_heldout_action.json")
    parser.add_argument("--match-types", default=",".join(DEFAULT_MATCH_TYPES))
    parser.add_argument("--max-clusters", type=int, default=10)
    parser.add_argument("--min-cluster-size", type=int, default=250)
    parser.add_argument("--seed", type=int, default=20260716)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new --output deliberately.")
    if not args.database.is_file():
        raise SystemExit(f"Database not found: {args.database}")
    graph = run(args.database, tuple(item.strip() for item in args.match_types.split(",") if item.strip()), args.max_clusters, args.min_cluster_size, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "accepted_ends": graph["source"]["ends_accepted"], "states": len(graph["states"]), "transitions": len(graph["transitions"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
