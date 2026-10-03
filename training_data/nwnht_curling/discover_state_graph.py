"""Discover an auditable discrete state graph from NWNHT four-player curling.

This is deliberately an *offline evidence pipeline*, not a shot planner.  It
turns each usable NWNHT end into:

    board before shot -> observed call -> board before next shot -> end outcome

The graph keeps the first-playing team's point of view throughout an end.  A
node therefore says both whose turn it is (first side/opponent) and which
shot-phase it belongs to.  The clusters are only topology candidates: their
names are neutral IDs, not tactical claims and not PhysX validation.

The original SQLite DB is opened read-only.  The script never parses PDFs and
refuses to overwrite an existing output file.
"""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import numpy as np


HOUSE_RADIUS_M = 1.8288
CENTER_LANE_M = 0.38
DEFAULT_DB = (
    Path(__file__).resolve().parents[2]
    / "external_research"
    / "NWNHT_curling"
    / "curling-main"
    / "src"
    / "world_curling_ss.db"
)
DEFAULT_MATCH_TYPES = ("Mens_Teams", "Womens_Teams", "Mixed_Teams")


@dataclass
class Frame:
    throwing_team: str | None = None
    call: str | None = None
    rating: int | None = None
    stones: list[tuple[str, float, float]] = field(default_factory=list)


@dataclass
class EndRecord:
    end_id: int
    match_id: int
    end_number: int
    match_type: str
    teams: tuple[str, str]
    score_before: dict[str, int]
    score_after: dict[str, int]
    final_score: dict[str, int]
    frames: dict[int, Frame] = field(default_factory=dict)


@dataclass
class Sample:
    uid: str
    end_id: int
    match_id: int
    end_number: int
    shot: int
    role: str
    phase: str
    action: str
    rating: int | None
    score_bucket: str
    end_outcome: str
    game_outcome: str
    features: dict[str, float]
    board: list[dict[str, float | str]]
    state_id: str | None = None


def normalize_action(call: str | None) -> str:
    """Map upstream call labels to a small observed-action alphabet."""
    text = (call or "").strip().casefold()
    mapping = {
        "draw": "DRAW",
        "take-out": "TAKEOUT",
        "double take-out": "DOUBLE_TAKEOUT",
        "clearing": "CLEARING",
        "front": "FRONT",
        "guard": "GUARD",
        "hit and roll": "HIT_AND_ROLL",
        "raise": "RAISE",
        "promotion take-out": "PROMOTION_TAKEOUT",
        "wick / soft peeling": "WICK_OR_SOFT_PEEL",
        "freeze": "FREEZE",
        "through": "THROUGH",
        "no statistics": "UNCLASSIFIED",
        "not played": "NOT_PLAYED",
    }
    return mapping.get(text, "UNCLASSIFIED")


def shot_phase(shot: int) -> str:
    if shot <= 5:
        return "FGZ_1_5"
    if shot <= 10:
        return "BUILD_6_10"
    if shot <= 14:
        return "RESOLUTION_11_14"
    return "LAST_15_16"


def score_bucket(diff: int) -> str:
    if diff <= -2:
        return "TRAIL_2_PLUS"
    if diff < 0:
        return "TRAIL"
    if diff == 0:
        return "TIED"
    if diff == 1:
        return "LEAD"
    return "LEAD_2_PLUS"


def signed_outcome(value: int) -> str:
    return "FIRST_SCORES" if value > 0 else "OPPONENT_SCORES" if value < 0 else "BLANK"


def signed_game(value: int) -> str:
    return "FIRST_WINS" if value > 0 else "FIRST_LOSES" if value < 0 else "DRAW"


def _stone_features(stones: list[dict[str, float | str]], owner: str, prefix: str) -> dict[str, float]:
    owned = [stone for stone in stones if stone["owner"] == owner]
    result: dict[str, float] = {
        f"{prefix}_visible": float(len(owned)),
        f"{prefix}_in_house": 0.0,
        f"{prefix}_guards": 0.0,
        f"{prefix}_centre_guards": 0.0,
        f"{prefix}_centre_house": 0.0,
        f"{prefix}_protected_house": 0.0,
    }
    for row in owned:
        x, y = float(row["x_m"]), float(row["y_m"])
        radius = math.hypot(x, y)
        in_house = radius <= HOUSE_RADIUS_M
        guard = HOUSE_RADIUS_M < y <= 6.45
        centre = abs(x) <= CENTER_LANE_M
        result[f"{prefix}_in_house"] += float(in_house)
        result[f"{prefix}_guards"] += float(guard)
        result[f"{prefix}_centre_guards"] += float(guard and centre)
        result[f"{prefix}_centre_house"] += float(in_house and centre)
        if in_house and any(
            HOUSE_RADIUS_M < float(other["y_m"]) <= 6.45
            and float(other["y_m"]) > y
            and abs(float(other["x_m"]) - x) <= 0.42
            for other in owned
        ):
            result[f"{prefix}_protected_house"] += 1.0
    return result


def board_features(board: list[dict[str, float | str]], score_diff: int, end_number: int, shot: int) -> dict[str, float]:
    """Return transparent topology features, not raw 16-stone coordinates.

    X/Y bins retain centre versus wing and guard/front/button/back structure.
    Their counts are robust to a missing overlapped stone in a way that a raw
    coordinate vector is not.  ``first`` is always the team that threw shot 1.
    """
    features: dict[str, float] = {
        "score_diff_first_clipped": float(max(-4, min(4, score_diff))),
        "end_number_clipped": float(min(end_number, 12)),
        # Shot phase is a hard partition; exact hand number still matters
        # inside it (e.g. first, third and fifth shots have different future
        # stone budgets and legal options), so retain it explicitly.
        "shot_in_end": float(shot),
    }
    features.update(_stone_features(board, "first", "first"))
    features.update(_stone_features(board, "opponent", "opponent"))

    x_bins = (("left", lambda x: x < -CENTER_LANE_M), ("centre", lambda x: abs(x) <= CENTER_LANE_M), ("right", lambda x: x > CENTER_LANE_M))
    y_bins = (
        ("guard", lambda y: HOUSE_RADIUS_M < y <= 6.45),
        ("front_house", lambda y: 0.55 < y <= HOUSE_RADIUS_M),
        ("button", lambda y: -0.55 <= y <= 0.55),
        ("back_house", lambda y: -HOUSE_RADIUS_M <= y < -0.55),
    )
    for owner in ("first", "opponent"):
        for y_name, y_test in y_bins:
            for x_name, x_test in x_bins:
                key = f"{owner}_{y_name}_{x_name}"
                features[key] = float(
                    sum(
                        stone["owner"] == owner
                        and y_test(float(stone["y_m"]))
                        and x_test(float(stone["x_m"]))
                        for stone in board
                    )
                )

    in_house = sorted(
        (math.hypot(float(stone["x_m"]), float(stone["y_m"])), str(stone["owner"]))
        for stone in board
        if math.hypot(float(stone["x_m"]), float(stone["y_m"])) <= HOUSE_RADIUS_M
    )
    features["first_currently_scoring"] = float(bool(in_house) and in_house[0][1] == "first")
    features["opponent_currently_scoring"] = float(bool(in_house) and in_house[0][1] == "opponent")
    scoring_count = 0
    if in_house:
        current = in_house[0][1]
        for _, owner in in_house:
            if owner != current:
                break
            scoring_count += 1
    features["current_scoring_count"] = float(scoring_count)
    for owner in ("first", "opponent"):
        distances = [
            math.hypot(float(stone["x_m"]), float(stone["y_m"]))
            for stone in board
            if stone["owner"] == owner and math.hypot(float(stone["x_m"]), float(stone["y_m"])) <= HOUSE_RADIUS_M
        ]
        features[f"{owner}_nearest_house_distance"] = min(distances, default=2.5)
    return features


def infer_colour_owners(frames: dict[int, Frame], teams: tuple[str, str]) -> dict[str, str] | None:
    """Use retained-stone additions to infer red/yellow ownership conservatively."""
    mapping: dict[str, str] = {}
    previous: Counter[str] = Counter()
    for shot in range(1, 17):
        frame = frames[shot]
        current = Counter(colour for colour, _, _ in frame.stones)
        increased = [colour for colour in ("red", "yellow") if current[colour] == previous[colour] + 1]
        if len(increased) == 1 and frame.throwing_team:
            colour = increased[0]
            old = mapping.get(colour)
            if old is not None and old != frame.throwing_team:
                return None
            mapping[colour] = frame.throwing_team
        previous = current
    if len(mapping) == 1:
        colour, owner = next(iter(mapping.items()))
        other_colour = "yellow" if colour == "red" else "red"
        other_team = next((team for team in teams if team != owner), None)
        if other_team:
            mapping[other_colour] = other_team
    if set(mapping) != {"red", "yellow"} or set(mapping.values()) != set(teams):
        return None
    return mapping


def make_samples(record: EndRecord) -> list[Sample] | None:
    if set(record.frames) != set(range(17)):
        return None
    if any(record.frames[shot].throwing_team is None for shot in range(1, 17)):
        return None
    first_team = record.frames[1].throwing_team
    opponent_team = record.frames[2].throwing_team
    if not first_team or not opponent_team or first_team == opponent_team:
        return None
    if any(record.frames[shot].throwing_team != (first_team if shot % 2 else opponent_team) for shot in range(1, 17)):
        return None
    owners = infer_colour_owners(record.frames, record.teams)
    if owners is None:
        return None

    score_diff = record.score_before[first_team] - record.score_before[opponent_team]
    end_diff = (record.score_after[first_team] - record.score_before[first_team]) - (
        record.score_after[opponent_team] - record.score_before[opponent_team]
    )
    game_diff = record.final_score[first_team] - record.final_score[opponent_team]
    samples: list[Sample] = []
    for shot in range(1, 17):
        board = [
            {"owner": "first" if owners[colour] == first_team else "opponent", "x_m": x, "y_m": y}
            for colour, x, y in record.frames[shot - 1].stones
            if colour in owners
        ]
        role = "FIRST_TO_THROW" if shot % 2 else "OPPONENT_TO_THROW"
        frame = record.frames[shot]
        samples.append(
            Sample(
                uid=f"{record.end_id}:{shot}",
                end_id=record.end_id,
                match_id=record.match_id,
                end_number=record.end_number,
                shot=shot,
                role=role,
                phase=shot_phase(shot),
                action=normalize_action(frame.call),
                rating=frame.rating,
                score_bucket=score_bucket(score_diff),
                end_outcome=signed_outcome(end_diff),
                game_outcome=signed_game(game_diff),
                features=board_features(board, score_diff, record.end_number, shot),
                board=board,
            )
        )
    return samples


def _iter_end_records(connection: sqlite3.Connection, allowed_types: tuple[str, ...]) -> Iterable[EndRecord]:
    """Stream DB records end-by-end so the 1M-stone table is never held at once."""
    placeholders = ",".join("?" for _ in allowed_types)
    meta_rows = connection.execute(
        f"""
        SELECT e.end_id,e.match_id,e.num,m.type,m.team_1,m.team_2,
               e.team_1_final_score,e.team_2_final_score,
               m.team_1_final_score AS final_1,m.team_2_final_score AS final_2
        FROM End e JOIN Match m ON m.match_id=e.match_id
        WHERE m.type IN ({placeholders})
        ORDER BY e.match_id,e.num,e.end_id
        """,
        allowed_types,
    ).fetchall()
    meta: dict[int, EndRecord] = {}
    previous_scores: dict[int, dict[str, int]] = {}
    last_match: int | None = None
    prior: dict[str, int] = {}
    for row in meta_rows:
        end_id, match_id, _, _, team_1, team_2, score_1, score_2, final_1, final_2 = row
        teams = (str(team_1), str(team_2))
        if match_id != last_match:
            prior = {teams[0]: 0, teams[1]: 0}
            last_match = match_id
        previous_scores[int(end_id)] = dict(prior)
        record = EndRecord(
            end_id=int(end_id), match_id=int(match_id), end_number=int(row[2]), match_type=str(row[3]), teams=teams,
            score_before=dict(prior), score_after={teams[0]: int(score_1), teams[1]: int(score_2)},
            final_score={teams[0]: int(final_1), teams[1]: int(final_2)},
        )
        meta[record.end_id] = record
        prior = dict(record.score_after)

    cursor = connection.execute(
        f"""
        SELECT e.end_id,pos.frame_num,t.type,t.rating,pl.team,s.colour,s.x,s.y
        FROM End e JOIN Match m ON m.match_id=e.match_id
        JOIN Position pos ON pos.end_id=e.end_id
        LEFT JOIN Throw t ON t.end_id=e.end_id AND t.throw_num=pos.frame_num
        LEFT JOIN Player pl ON pl.player_id=t.player_id
        LEFT JOIN Stone s ON s.position_id=pos.position_id
        WHERE m.type IN ({placeholders}) AND pos.frame_num BETWEEN 0 AND 16
        ORDER BY e.end_id,pos.frame_num,s.stone_id
        """,
        allowed_types,
    )
    current_id: int | None = None
    record: EndRecord | None = None
    for row in cursor:
        end_id = int(row[0])
        if end_id != current_id:
            if record is not None:
                yield record
            current_id = end_id
            record = meta.get(end_id)
            if record is None:
                continue
        assert record is not None
        frame_number = int(row[1])
        frame = record.frames.setdefault(frame_number, Frame())
        if frame_number and frame.throwing_team is None:
            frame.throwing_team = str(row[4]) if row[4] is not None else None
            frame.call = str(row[2]) if row[2] is not None else None
            frame.rating = int(row[3]) if row[3] is not None else None
        if row[5] is not None:
            frame.stones.append((str(row[5]), float(row[6]), float(row[7])))
    if record is not None:
        yield record


def _fit_kmeans(features: np.ndarray, k: int, seed: int, max_iterations: int = 35) -> tuple[np.ndarray, np.ndarray, float]:
    rng = np.random.default_rng(seed)
    centers = features[rng.choice(features.shape[0], size=k, replace=False)].copy()
    labels = np.zeros(features.shape[0], dtype=np.int32)
    for _ in range(max_iterations):
        squared = ((features[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        updated = squared.argmin(axis=1)
        new_centers = centers.copy()
        for index in range(k):
            members = features[updated == index]
            if len(members):
                new_centers[index] = members.mean(axis=0)
            else:
                new_centers[index] = features[rng.integers(features.shape[0])]
        if np.array_equal(updated, labels) and np.allclose(new_centers, centers, atol=1e-7):
            labels = updated
            centers = new_centers
            break
        labels, centers = updated, new_centers
    sse = float(((features - centers[labels]) ** 2).sum())
    return labels, centers, sse


def _choose_clusters(matrix: np.ndarray, maximum: int, min_cluster_size: int, seed: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Choose k by a conservative spherical-Gaussian BIC, then return labels."""
    n, dimension = matrix.shape
    maximum = min(maximum, max(1, n // max(1, min_cluster_size)))
    best: tuple[float, np.ndarray, np.ndarray, int] | None = None
    for k in range(1, maximum + 1):
        labels, centers, sse = _fit_kmeans(matrix, k, seed + k, max_iterations=15)
        counts = np.bincount(labels, minlength=k)
        if counts.min() < min_cluster_size:
            continue
        variance = max(sse / max(n * dimension, 1), 1e-12)
        parameters = k * dimension + k
        bic = n * dimension * (math.log(2 * math.pi * variance) + 1.0) + parameters * math.log(n)
        if best is None or bic < best[0]:
            best = (bic, labels, centers, k)
    if best is None:
        labels, centers, _ = _fit_kmeans(matrix, 1, seed, max_iterations=15)
        return labels, centers, 1
    return best[1], best[2], best[3]


def _assign_and_refine(matrix: np.ndarray, centers: np.ndarray, rounds: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """Assign every row, then perform a few full-data Lloyd refinements."""
    labels = np.zeros(matrix.shape[0], dtype=np.int32)
    for _ in range(rounds):
        squared = ((matrix[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = squared.argmin(axis=1)
        updated = centers.copy()
        for index in range(centers.shape[0]):
            members = matrix[labels == index]
            if len(members):
                updated[index] = members.mean(axis=0)
        if np.allclose(updated, centers, atol=1e-7):
            centers = updated
            break
        centers = updated
    squared = ((matrix[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    return squared.argmin(axis=1), centers


def discover(samples_by_end: list[list[Sample]], max_clusters: int, min_cluster_size: int, seed: int) -> dict[str, Any]:
    samples = [sample for end in samples_by_end for sample in end]
    feature_names = sorted(samples[0].features)
    partitions: dict[tuple[str, str], list[Sample]] = defaultdict(list)
    for sample in samples:
        partitions[(sample.role, sample.phase)].append(sample)

    state_samples: dict[str, list[Sample]] = defaultdict(list)
    partition_meta: list[dict[str, Any]] = []
    for (role, phase), group in sorted(partitions.items()):
        raw = np.asarray([[sample.features[name] for name in feature_names] for sample in group], dtype=np.float64)
        mean, std = raw.mean(axis=0), raw.std(axis=0)
        std[std < 1e-8] = 1.0
        normalized = (raw - mean) / std
        # Candidate-k fitting is intentionally capped.  Every sample is still
        # assigned and counted below; the cap only avoids fitting k=1..6 over
        # the same 100k+ rows repeatedly.  Evenly spaced indices cover the
        # chronological source rather than favouring a single event.
        fit_limit = 2500
        if len(normalized) > fit_limit:
            fit_indices = np.linspace(0, len(normalized) - 1, num=fit_limit, dtype=np.int64)
            fit_matrix = normalized[fit_indices]
            scaled_minimum = max(10, math.ceil(min_cluster_size * fit_limit / len(normalized)))
        else:
            fit_matrix = normalized
            scaled_minimum = min_cluster_size
        _, centers, selected_k = _choose_clusters(fit_matrix, max_clusters, scaled_minimum, seed)
        labels, centers = _assign_and_refine(normalized, centers)
        # Relabel by medoid provenance for deterministic human-readable IDs.
        medoid_indices = [int(np.argmin(((normalized - centers[index]) ** 2).sum(axis=1))) for index in range(selected_k)]
        order = sorted(range(selected_k), key=lambda index: (group[medoid_indices[index]].end_id, group[medoid_indices[index]].shot))
        remap = {old: new + 1 for new, old in enumerate(order)}
        for sample, label in zip(group, labels):
            sample.state_id = f"{role}_{phase}_C{remap[int(label)]:02d}"
            state_samples[sample.state_id].append(sample)
        partition_meta.append({"role": role, "phase": phase, "samples": len(group), "selected_clusters": selected_k})

    states: list[dict[str, Any]] = []
    for state_id, group in sorted(state_samples.items()):
        action_counts = Counter(sample.action for sample in group)
        end_counts = Counter(sample.end_outcome for sample in group)
        game_counts = Counter(sample.game_outcome for sample in group)
        feature_means = {name: round(float(np.mean([sample.features[name] for sample in group])), 4) for name in feature_names}
        medoid = min(
            group,
            key=lambda sample: sum((sample.features[name] - feature_means[name]) ** 2 for name in feature_names),
        )
        states.append(
            {
                "id": state_id,
                "sample_count": len(group),
                "observed_actions": dict(action_counts.most_common()),
                "end_outcomes_observed": dict(end_counts),
                "game_outcomes_observed": dict(game_counts),
                "feature_means": feature_means,
                "medoid_example": {
                    "sample_uid": medoid.uid,
                    "match_id": medoid.match_id,
                    "end_number": medoid.end_number,
                    "shot": medoid.shot,
                    "score_bucket": medoid.score_bucket,
                    "observed_action": medoid.action,
                    "visible_board": medoid.board,
                },
            }
        )

    edges: Counter[tuple[str, str, str]] = Counter()
    edge_examples: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for end in samples_by_end:
        for index, sample in enumerate(end):
            assert sample.state_id is not None
            target = end[index + 1].state_id if index + 1 < len(end) else f"END_{sample.end_outcome}"
            assert target is not None
            key = (sample.state_id, sample.action, target)
            edges[key] += 1
            if len(edge_examples[key]) < 3:
                edge_examples[key].append(sample.uid)
    transitions = [
        {
            "from": source,
            "observed_action": action,
            "to": target,
            "count": count,
            "example_samples": edge_examples[(source, action, target)],
        }
        for (source, action, target), count in sorted(edges.items(), key=lambda item: (-item[1], item[0]))
    ]
    return {
        "feature_names": feature_names,
        "partitions": partition_meta,
        "states": states,
        "transitions": transitions,
        "sample_count": len(samples),
    }


def run(database: Path, allowed_types: tuple[str, ...], max_clusters: int, min_cluster_size: int, seed: int, limit_ends: int | None = None) -> dict[str, Any]:
    connection = sqlite3.connect(f"file:{database.resolve().as_posix()}?mode=ro", uri=True)
    usable: list[list[Sample]] = []
    total = rejected = 0
    try:
        for record in _iter_end_records(connection, allowed_types):
            total += 1
            samples = make_samples(record)
            if samples is None:
                rejected += 1
                continue
            usable.append(samples)
            if limit_ends is not None and len(usable) >= limit_ends:
                break
    finally:
        connection.close()
    if not usable:
        raise ValueError("No usable complete four-player ends after continuity and colour-ownership checks.")
    graph = discover(usable, max_clusters=max_clusters, min_cluster_size=min_cluster_size, seed=seed)
    graph.update(
        {
            "schema": "nwnht_discrete_state_graph_v0",
            "evidence_level": "公开历史壶谱的自动检测坐标；不是 PhysX 轨迹验证，也不是因果胜率证明。",
            "source": {
                "database": str(database),
                "match_types": list(allowed_types),
                "ends_examined": total,
                "ends_accepted": len(usable),
                "ends_rejected": rejected,
                "acceptance_rule": "17 个帧完整、投手严格交替、红黄壶色可由连续新增壶唯一反推且无冲突。",
            },
            "clustering": {
                "algorithm": "per (turn role, shot phase) standardized k-means; k/initial centres selected by spherical-Gaussian BIC on at most 2,500 evenly spaced rows (15 candidate-fit iterations), then every accepted row is assigned and refined on full data",
                "max_clusters_per_partition": max_clusters,
                "min_cluster_size": min_cluster_size,
                "seed": seed,
                "state_semantics": "节点是候选局面类型；observed_actions 是历史选择频数，不是推荐动作。",
            },
        }
    )
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "artifacts" / "nwnht_four_player_state_graph_v1_exact_shot.json")
    parser.add_argument("--match-types", default=",".join(DEFAULT_MATCH_TYPES), help="Comma-separated Match.type values; mixed doubles is excluded by default.")
    parser.add_argument("--max-clusters", type=int, default=6)
    parser.add_argument("--min-cluster-size", type=int, default=250)
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument("--limit-ends", type=int, default=None, help="For a quick smoke run only; omitted means all eligible ends.")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new --output deliberately.")
    if not args.database.is_file():
        raise SystemExit(f"Database not found: {args.database}")
    if args.max_clusters < 1 or args.min_cluster_size < 1:
        raise SystemExit("--max-clusters and --min-cluster-size must be positive")
    graph = run(
        database=args.database,
        allowed_types=tuple(item.strip() for item in args.match_types.split(",") if item.strip()),
        max_clusters=args.max_clusters,
        min_cluster_size=args.min_cluster_size,
        seed=args.seed,
        limit_ends=args.limit_ends,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "accepted_ends": graph["source"]["ends_accepted"], "states": len(graph["states"]), "transitions": len(graph["transitions"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
