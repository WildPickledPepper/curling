"""Extract winner-only trajectories and win-associated edges from full data.

States are never re-clustered here.  The full trajectory dataset supplies the
state vocabulary; game_result=FIRST_WINS only filters evidence about which
historical transitions co-occurred with eventual wins.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


def wilson_lower(successes: int, total: int, z: float = 1.96) -> float:
    """Conservative 95% lower bound for an observed proportion."""
    if total <= 0:
        return 0.0
    p = successes / total
    denom = 1.0 + z * z / total
    centre = p + z * z / (2 * total)
    radius = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total)
    return max(0.0, (centre - radius) / denom)


def load_rows(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def build(rows: list[dict[str, Any]], min_edge_support: int) -> dict[str, Any]:
    game_counts = Counter(str(row["game_result"]) for row in rows)
    baseline_win_rate = game_counts["FIRST_WINS"] / len(rows) if rows else 0.0
    state_counts: dict[str, Counter[str]] = defaultdict(Counter)
    action_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    edge_counts: dict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    edge_end_counts: dict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    for row in rows:
        state = str(row["state_id"])
        action = str(row["observed_own_action"])
        edge = (state, action, str(row["observed_opponent_reply"]), str(row["next_state_id"]))
        result = str(row["game_result"])
        state_counts[state][result] += 1
        action_counts[(state, action)][result] += 1
        edge_counts[edge][result] += 1
        edge_end_counts[edge][str(row["end_result"])] += 1

    state_summary = []
    for state, counts in sorted(state_counts.items()):
        total = sum(counts.values())
        wins = counts["FIRST_WINS"]
        state_summary.append(
            {
                "state_id": state,
                "total_count": total,
                "game_result_counts": dict(counts),
                "observed_win_rate": round(wins / total, 6),
                "win_rate_lower_95": round(wilson_lower(wins, total), 6),
            }
        )
    state_win_rate = {row["state_id"]: row["observed_win_rate"] for row in state_summary}

    action_summary = []
    for (state, action), counts in sorted(action_counts.items()):
        total = sum(counts.values())
        wins = counts["FIRST_WINS"]
        action_summary.append(
            {
                "state_id": state,
                "observed_own_action": action,
                "total_count": total,
                "game_result_counts": dict(counts),
                "observed_win_rate": round(wins / total, 6),
                "win_rate_lower_95": round(wilson_lower(wins, total), 6),
                "state_observed_win_rate": state_win_rate[state],
                "association_delta_vs_state": round(wins / total - state_win_rate[state], 6),
            }
        )

    edge_summary = []
    for edge, counts in edge_counts.items():
        total = sum(counts.values())
        wins = counts["FIRST_WINS"]
        edge_summary.append(
            {
                "from": edge[0],
                "observed_own_action": edge[1],
                "observed_opponent_reply": edge[2],
                "to": edge[3],
                "total_count": total,
                "game_result_counts": dict(counts),
                "end_result_counts": dict(edge_end_counts[edge]),
                "observed_win_rate": round(wins / total, 6),
                "win_rate_lower_95": round(wilson_lower(wins, total), 6),
                "source_state_observed_win_rate": state_win_rate[edge[0]],
                "association_delta_vs_source_state": round(wins / total - state_win_rate[edge[0]], 6),
            }
        )
    edge_summary.sort(key=lambda row: (-row["total_count"], row["from"], row["observed_own_action"]))
    promising = [
        row for row in edge_summary
        if row["total_count"] >= min_edge_support
        and row["win_rate_lower_95"] > baseline_win_rate
        and row["association_delta_vs_source_state"] > 0
    ]
    return {
        "schema": "nwnht_first_player_success_subgraph_v0",
        "row_count": len(rows),
        "baseline_first_wins_rate": round(baseline_win_rate, 6),
        "minimum_edge_support": min_edge_support,
        "state_summary": state_summary,
        "state_action_summary": action_summary,
        "edge_summary": edge_summary,
        "promising_win_associated_edges": promising,
        "warning": "Win rates are observational associations. They do not prove an action caused a win; selection bias, team strength and prior game state remain confounders.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent / "artifacts"
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_macro_trajectories_v0.jsonl")
    parser.add_argument("--winner-output", type=Path, default=root / "nwnht_first_player_macro_winning_trajectories_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_success_subgraph_v0.json")
    parser.add_argument("--min-edge-support", type=int, default=20)
    args = parser.parse_args()
    if args.min_edge_support < 1:
        raise SystemExit("--min-edge-support must be positive")
    if not args.input.is_file():
        raise SystemExit(f"Input trajectory dataset not found: {args.input}")
    for path in (args.winner_output, args.output):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}; choose a new path deliberately.")
    rows = list(load_rows(args.input))
    winners = [row for row in rows if row["game_result"] == "FIRST_WINS"]
    args.winner_output.parent.mkdir(parents=True, exist_ok=True)
    with args.winner_output.open("w", encoding="utf-8") as handle:
        for row in winners:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    result = build(rows, args.min_edge_support)
    result["winner_only_row_count"] = len(winners)
    result["winner_only_definition"] = "Rows whose end-first team ultimately won the full match; state vocabulary remains full-data vocabulary."
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"winner_rows": len(winners), "output": str(args.output), "promising_edges": len(result["promising_win_associated_edges"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
