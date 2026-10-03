"""Export complete first-player macro-state trajectories from NWNHT.

One row is one first-player decision in one end:

    S_k -> observed own action -> observed opponent reply -> S_(k+1)

End and game outcomes are labels only.  They are intentionally not fed into
the state recogniser, which remains (own throw number, board topology).
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from planning_proxy.first_player_macro_state import LOW_SUPPORT_RAW_BY_K, raw_macro_type
    from .discover_first_player_state_graph import FirstDecision, first_decisions
    from .discover_state_graph import DEFAULT_DB, DEFAULT_MATCH_TYPES, _iter_end_records
except ImportError:  # pragma: no cover - direct script invocation
    from planning_proxy.first_player_macro_state import LOW_SUPPORT_RAW_BY_K, raw_macro_type
    from discover_first_player_state_graph import FirstDecision, first_decisions
    from discover_state_graph import DEFAULT_DB, DEFAULT_MATCH_TYPES, _iter_end_records


def state_id(decision: FirstDecision) -> tuple[str, str]:
    raw = raw_macro_type(decision.features)
    macro = "LOW_SUPPORT_SEARCH_REQUIRED" if raw in LOW_SUPPORT_RAW_BY_K[decision.own_throw_number] else raw
    return f"FIRST_K{decision.own_throw_number}_{macro}", raw


def outcome_labels(record: Any) -> dict[str, Any]:
    first_team = str(record.frames[1].throwing_team)
    opponent_team = str(record.frames[2].throwing_team)
    first_end_points = int(record.score_after[first_team]) - int(record.score_before[first_team])
    opponent_end_points = int(record.score_after[opponent_team]) - int(record.score_before[opponent_team])
    if first_end_points > opponent_end_points:
        end_result = "FIRST_SCORES"
    elif first_end_points < opponent_end_points:
        end_result = "OPPONENT_SCORES"
    else:
        end_result = "BLANK"
    first_game_score = int(record.final_score[first_team])
    opponent_game_score = int(record.final_score[opponent_team])
    if first_game_score > opponent_game_score:
        game_result = "FIRST_WINS"
    elif first_game_score < opponent_game_score:
        game_result = "FIRST_LOSES"
    else:
        game_result = "GAME_DRAW"
    return {
        "first_team": first_team,
        "opponent_team": opponent_team,
        "end_points": {"first": first_end_points, "opponent": opponent_end_points},
        "end_result": end_result,
        "final_game_score": {"first": first_game_score, "opponent": opponent_game_score},
        "game_result": game_result,
    }


def build_rows(database: Path, match_types: tuple[str, ...]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    connection = sqlite3.connect(f"file:{database.resolve().as_posix()}?mode=ro", uri=True)
    rows: list[dict[str, Any]] = []
    examined = rejected = accepted = 0
    try:
        for record in _iter_end_records(connection, match_types):
            examined += 1
            decisions = first_decisions(record)
            if decisions is None:
                rejected += 1
                continue
            accepted += 1
            labels = outcome_labels(record)
            ids = [state_id(decision) for decision in decisions]
            for index, decision in enumerate(decisions):
                current_id, raw_macro = ids[index]
                next_id = ids[index + 1][0] if index < 7 else "TERMINAL_AFTER_OPPONENT_REPLY"
                rows.append(
                    {
                        "schema": "nwnht_first_player_trajectory_row_v0",
                        "match_id": record.match_id,
                        "end_id": record.end_id,
                        "end_number": record.end_number,
                        "first_team": labels["first_team"],
                        "opponent_team": labels["opponent_team"],
                        "own_throw_number": decision.own_throw_number,
                        "global_shot_number": decision.own_throw_number * 2 - 1,
                        "state_id": current_id,
                        "raw_macro_state": raw_macro,
                        "observed_own_action": decision.own_action,
                        "observed_opponent_reply": decision.opponent_reply,
                        "next_state_id": next_id,
                        "board_before_own_shot": decision.visible_board,
                        # Labels below are deliberately outside state_id/features.
                        "end_points": labels["end_points"],
                        "end_result": labels["end_result"],
                        "final_game_score": labels["final_game_score"],
                        "game_result": labels["game_result"],
                    }
                )
    finally:
        connection.close()
    manifest = {
        "schema": "nwnht_first_player_trajectory_manifest_v0",
        "source": {"database": str(database), "match_types": list(match_types), "ends_examined": examined, "ends_accepted": accepted, "ends_rejected": rejected},
        "row_count": len(rows),
        "trajectory_definition": "One end has eight ordered rows, K1..K8. Rows retain the first-player perspective throughout the end.",
        "outcome_boundary": "end_result, end_points, final_game_score and game_result are labels only; they are not state features.",
    }
    return rows, manifest


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Provide label distributions for audit; never interprets them as causal values."""
    state_labels: dict[str, Counter[str]] = defaultdict(Counter)
    transition_labels: dict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    for row in rows:
        state_labels[str(row["state_id"])][str(row["game_result"])] += 1
        key = (str(row["state_id"]), str(row["observed_own_action"]), str(row["observed_opponent_reply"]), str(row["next_state_id"]))
        transition_labels[key][str(row["end_result"])] += 1
    return {
        "state_game_label_counts": {state: dict(counts) for state, counts in sorted(state_labels.items())},
        "transition_end_label_counts": [
            {"from": key[0], "observed_own_action": key[1], "observed_opponent_reply": key[2], "to": key[3], "end_result_counts": dict(counts)}
            for key, counts in sorted(transition_labels.items())
        ],
        "warning": "These are observational label distributions, not causal action values or policy recommendations.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent / "artifacts"
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_macro_trajectories_v0.jsonl")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_first_player_macro_trajectories_v0_manifest.json")
    parser.add_argument("--aggregate", type=Path, default=root / "nwnht_first_player_macro_trajectories_v0_aggregate.json")
    parser.add_argument("--match-types", default=",".join(DEFAULT_MATCH_TYPES))
    args = parser.parse_args()
    for path in (args.output, args.manifest, args.aggregate):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}; choose a new path deliberately.")
    rows, manifest = build_rows(args.database, tuple(item.strip() for item in args.match_types.split(",") if item.strip()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    args.aggregate.write_text(json.dumps(aggregate(rows), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "manifest": str(args.manifest), "aggregate": str(args.aggregate)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
