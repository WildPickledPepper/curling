"""Turn full trajectories into auditable, non-causal action-intent candidates.

Output is a lookup table:
    state -> candidate historical action intents -> opponent reply branches -> next states

It deliberately leaves v/h/w and exact path construction to the local PhysX
planner and labels every ranking as observational.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    from .build_first_player_success_subgraph import wilson_lower
except ImportError:  # pragma: no cover - direct script invocation
    from build_first_player_success_subgraph import wilson_lower


NON_EXECUTABLE_ACTIONS = {"UNCLASSIFIED", "NOT_PLAYED"}


def load_rows(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def build(rows: list[dict[str, Any]], state_metadata: dict[str, dict[str, Any]], min_action_support: int, max_actions: int) -> dict[str, Any]:
    total_wins = sum(row["game_result"] == "FIRST_WINS" for row in rows)
    global_win_rate = total_wins / len(rows) if rows else 0.0
    state_results: dict[str, Counter[str]] = defaultdict(Counter)
    action_results: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    branch_results: dict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    branch_end: dict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    state_end_margin: dict[str, int] = defaultdict(int)
    action_end_margin: dict[tuple[str, str], int] = defaultdict(int)
    branch_end_margin: dict[tuple[str, str, str, str], int] = defaultdict(int)
    target_counts: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in rows:
        state, action = str(row["state_id"]), str(row["observed_own_action"])
        reply, target = str(row["observed_opponent_reply"]), str(row["next_state_id"])
        result = str(row["game_result"])
        state_results[state][result] += 1
        action_results[(state, action)][result] += 1
        branch_results[(state, action, reply, target)][result] += 1
        branch_end[(state, action, reply, target)][str(row["end_result"])] += 1
        margin = int(row["end_points"]["first"]) - int(row["end_points"]["opponent"])
        state_end_margin[state] += margin
        action_end_margin[(state, action)] += margin
        branch_end_margin[(state, action, reply, target)] += margin
        target_counts[(state, action, target)] += 1

    policy_states = []
    for state, state_counter in sorted(state_results.items()):
        state_total = sum(state_counter.values())
        state_wins = state_counter["FIRST_WINS"]
        state_rate = state_wins / state_total
        state_margin = state_end_margin[state] / state_total
        actions = []
        for (source, action), counter in action_results.items():
            if source != state:
                continue
            total = sum(counter.values())
            wins = counter["FIRST_WINS"]
            rate = wins / total
            branches = []
            for (branch_source, branch_action, reply, target), results in branch_results.items():
                if (branch_source, branch_action) != (state, action):
                    continue
                branch_total = sum(results.values())
                branch_wins = results["FIRST_WINS"]
                branches.append(
                    {
                        "observed_opponent_reply": reply,
                        "next_state_id": target,
                        "count": branch_total,
                        "conditional_probability_given_action": round(branch_total / total, 6),
                        "observed_win_rate": round(branch_wins / branch_total, 6),
                        "win_rate_lower_95": round(wilson_lower(branch_wins, branch_total), 6),
                        "mean_end_point_margin": round(branch_end_margin[(branch_source, branch_action, reply, target)] / branch_total, 6),
                        "end_result_counts": dict(branch_end[(branch_source, branch_action, reply, target)]),
                    }
                )
            branches.sort(key=lambda item: (-item["count"], item["observed_opponent_reply"], item["next_state_id"]))
            targets = [
                {"next_state_id": target, "count": count, "probability": round(count / total, 6)}
                for (source2, action2, target), count in target_counts.items()
                if (source2, action2) == (state, action)
            ]
            targets.sort(key=lambda item: (-item["count"], item["next_state_id"]))
            end_margin = action_end_margin[(state, action)] / total
            actions.append(
                {
                    "observed_action_intent": action,
                    "total_count": total,
                    "observed_win_rate": round(rate, 6),
                    "win_rate_lower_95": round(wilson_lower(wins, total), 6),
                    "association_delta_vs_state": round(rate - state_rate, 6),
                    "mean_end_point_margin": round(end_margin, 6),
                    "association_delta_end_margin_vs_state": round(end_margin - state_margin, 6),
                    "eligible_win_associated_candidate": action not in NON_EXECUTABLE_ACTIONS and total >= min_action_support and wilson_lower(wins, total) > global_win_rate and rate > state_rate and end_margin >= state_margin,
                    "next_state_distribution": targets,
                    "opponent_reply_branches": branches,
                }
            )
        actions.sort(key=lambda item: (-item["win_rate_lower_95"], -item["total_count"], item["observed_action_intent"]))
        candidates = [item for item in actions if item["eligible_win_associated_candidate"]][:max_actions]
        fallback = max(actions, key=lambda item: (item["total_count"], item["observed_action_intent"])) if actions else None
        meta = state_metadata.get(state, {})
        policy_states.append(
            {
                "state_id": state,
                "physx_detail_required": bool(meta.get("physx_detail_required", True)),
                "state_total_count": state_total,
                "state_observed_win_rate": round(state_rate, 6),
                "state_mean_end_point_margin": round(state_margin, 6),
                "candidate_action_intents": candidates,
                "reference_fallback_most_observed_action": None if fallback is None else fallback["observed_action_intent"],
                "reference_fallback_count": None if fallback is None else fallback["total_count"],
                "no_eligible_candidate": not candidates,
            }
        )
    return {
        "schema": "nwnht_first_player_candidate_policy_v0",
        "source_row_count": len(rows),
        "global_observed_first_wins_rate": round(global_win_rate, 6),
        "minimum_action_support": min_action_support,
        "max_candidates_per_state": max_actions,
        "policy_states": policy_states,
        "warning": "Candidate action intents are historical win associations, not causal estimates or executable shots. Enforce local rules and validate every target through PhysX before use.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent / "artifacts"
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_macro_trajectories_v0.jsonl")
    parser.add_argument("--states", type=Path, default=root / "nwnht_first_player_macro_state_graph_v1_supported.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_candidate_policy_v2_game_and_end.json")
    parser.add_argument("--min-action-support", type=int, default=50)
    parser.add_argument("--max-actions", type=int, default=2)
    args = parser.parse_args()
    if args.min_action_support < 1 or args.max_actions < 1:
        raise SystemExit("--min-action-support and --max-actions must be positive")
    if not args.input.is_file() or not args.states.is_file():
        raise SystemExit("Trajectory input or macro-state artifact is missing")
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new path deliberately.")
    rows = list(load_rows(args.input))
    artifact = json.loads(args.states.read_text(encoding="utf-8"))
    metadata = {str(state["id"]): state for state in artifact["states"]}
    result = build(rows, metadata, args.min_action_support, args.max_actions)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    candidate_count = sum(len(state["candidate_action_intents"]) for state in result["policy_states"])
    print(json.dumps({"output": str(args.output), "states": len(result["policy_states"]), "candidate_actions": candidate_count}, ensure_ascii=False))


if __name__ == "__main__":
    main()
