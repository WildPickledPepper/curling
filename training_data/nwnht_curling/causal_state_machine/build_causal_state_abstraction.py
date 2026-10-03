#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an auditable, runtime-safe *candidate* state abstraction.

This stage deliberately does not learn a policy.  It converts each first-side
pre-shot board S_K into a deterministic topology key that can also be computed
at runtime from K and stone coordinates.  Score, end number, team, event,
called-shot text and terminal result are excluded from the state key.

The output is a diagnostic for the next causal-estimation stage:

    state S_K + observed own board effect A_K
      -> own post-shot topology U_K
      -> observed opponent board effect B_K
      -> next first-side topology S_(K+1), end margin Y

It reports grouped-match holdout stability and support.  Neither historical
frequencies nor this abstraction are a recommendation or causal proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    from .derive_action_effects import action_effect, board_facts
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.derive_action_effects import action_effect, board_facts  # type: ignore


MIN_STATE_SUPPORT = 100
MIN_ACTION_TRAIN_SUPPORT = 25
MIN_ACTION_HOLDOUT_SUPPORT = 10
STABILITY_TV_THRESHOLD = 0.35


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def _bin(value: int, maximum_singleton: int = 1) -> str:
    if value <= maximum_singleton:
        return str(value)
    return f"{maximum_singleton + 1}P"


def _protected_house_count(board: list[dict[str, Any]], owner: str) -> int:
    """Count own in-house stones with a same-owner guard plausibly in front.

    This is a transparent topology proxy, not a claim that the stone is
    physically untouchable.  It is intentionally the same geometric notion
    used only as a feature in the earlier state-graph exploration.
    """
    protected = 0
    for stone in board:
        if stone["owner"] != owner:
            continue
        x, y = float(stone["x_m"]), float(stone["y_m"])
        if x * x + y * y > 1.8288 ** 2:
            continue
        if any(
            other["owner"] == owner
            and 1.8288 < float(other["y_m"]) <= 6.45
            and float(other["y_m"]) > y
            and abs(float(other["x_m"]) - x) <= 0.42
            for other in board
        ):
            protected += 1
    return protected


def topology_features(board: list[dict[str, Any]]) -> dict[str, str]:
    """Return finite categorical features derived only from board coordinates."""
    facts = board_facts(board)
    result: dict[str, str] = {
        "control": {None: "NONE_OR_UNCERTAIN", "first": "FIRST", "opponent": "OPPONENT"}[facts["scoring_owner"]],
    }
    for owner, prefix in (("first", "F"), ("opponent", "O")):
        visible = int(facts[f"{owner}_visible"])
        house = int(facts[f"{owner}_in_house"])
        guards = int(facts[f"{owner}_guards"])
        centre_guards = int(facts[f"{owner}_centre_guards"])
        result[f"{prefix}_visible"] = _bin(visible, 2)
        result[f"{prefix}_house"] = _bin(house, 1)
        result[f"{prefix}_centre_guard"] = _bin(centre_guards, 1)
        result[f"{prefix}_wing_guard"] = _bin(max(guards - centre_guards, 0), 1)
        result[f"{prefix}_protected_house"] = _bin(_protected_house_count(board, owner), 1)
    return result


CORE_FEATURES = (
    "control",
    "F_house",
    "O_house",
    "F_centre_guard",
    "O_centre_guard",
    "F_wing_guard",
    "O_wing_guard",
)
FINE_ONLY_FEATURES = ("F_visible", "O_visible", "F_protected_house", "O_protected_house")


def state_key(k: int, board: list[dict[str, Any]], *, fine: bool = False) -> str:
    features = topology_features(board)
    names = CORE_FEATURES + (FINE_ONLY_FEATURES if fine else ())
    level = "FINE" if fine else "CORE"
    payload = ";".join(f"{name}={features[name]}" for name in names)
    return f"K{k}_{level}[{payload}]"


def _opponent_reply_effect(after_own: list[dict[str, Any]], after_reply: list[dict[str, Any]]) -> str:
    """Describe B_K by swapping perspectives before applying the S->U taxonomy."""
    def swap(board: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{**stone, "owner": "opponent" if stone["owner"] == "first" else "first"} for stone in board]

    own_view = action_effect(swap(after_own), swap(after_reply))["primary_effect"]
    rename = {
        "GAIN_OWN_SCORING_CONTROL": "OPPONENT_GAINS_SCORING_CONTROL",
        "REDUCE_OPPONENT_HOUSE_LAYER": "OPPONENT_REDUCES_FIRST_HOUSE_LAYER",
        "ADD_OWN_HOUSE_LAYER": "OPPONENT_ADDS_HOUSE_LAYER",
        "ADD_PRESSURE_GUARD": "OPPONENT_ADDS_PRESSURE_GUARD",
        "REDUCE_STONE_COUNT_WITHOUT_CONTROL": "OPPONENT_REDUCES_STONE_COUNT_WITHOUT_CONTROL",
        "NO_CLASSIFIABLE_MACRO_EFFECT": "OPPONENT_NO_CLASSIFIABLE_MACRO_EFFECT",
    }
    return rename[str(own_view)]


def _split_for_match(match_id: int) -> str:
    """Stable grouped split; no rows from one match appear on both sides."""
    digest = hashlib.sha256(f"nwnht-state-abstraction:{match_id}".encode("ascii")).digest()
    return "holdout" if digest[0] % 5 == 0 else "train"


def _distribution(counter: Counter[str]) -> dict[str, float]:
    total = sum(counter.values())
    return {} if total == 0 else {key: round(value / total, 6) for key, value in sorted(counter.items())}


def _total_variation(left: Counter[str], right: Counter[str]) -> float | None:
    if not left or not right:
        return None
    left_total, right_total = sum(left.values()), sum(right.values())
    keys = set(left) | set(right)
    return round(0.5 * sum(abs(left.get(key, 0) / left_total - right.get(key, 0) / right_total) for key in keys), 6)


def build(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    state_counts: Counter[str] = Counter()
    fine_counts: Counter[str] = Counter()
    fine_substates_by_core: dict[str, Counter[str]] = defaultdict(Counter)
    state_features: dict[str, dict[str, str]] = {}
    edge_data: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "all": Counter(), "train": Counter(), "holdout": Counter(),
            "reply_all": Counter(), "reply_train": Counter(), "reply_holdout": Counter(),
            "next_all": Counter(), "next_train": Counter(), "next_holdout": Counter(),
            "u_all": Counter(), "margin_sum_all": 0, "margin_count_all": 0,
            "examples": [],
        }
    )
    row_count = 0
    match_splits: Counter[str] = Counter()
    seen_matches: set[int] = set()

    for row in rows:
        row_count += 1
        k = int(row["own_throw_number"])
        before = list(row["s_before_own"])
        after_own = list(row["u_after_own"])
        after_reply = list(row["s_after_opponent_reply"])
        state = state_key(k, before)
        fine_state = state_key(k, before, fine=True)
        state_counts[state] += 1
        fine_counts[fine_state] += 1
        fine_substates_by_core[state][fine_state] += 1
        state_features.setdefault(state, topology_features(before))
        action = str(row["observed_own_board_effect"]["primary_effect"])
        reply = _opponent_reply_effect(after_own, after_reply)
        u_key = state_key(k, after_own)
        next_key = "END" if k == 8 else state_key(k + 1, after_reply)
        split = _split_for_match(int(row["match_id"]))
        if int(row["match_id"]) not in seen_matches:
            seen_matches.add(int(row["match_id"]))
            match_splits[split] += 1
        item = edge_data[(state, action)]
        item["all"][action] += 1
        item[split][action] += 1
        item["reply_all"][reply] += 1
        item[f"reply_{split}"][reply] += 1
        item["next_all"][next_key] += 1
        item[f"next_{split}"][next_key] += 1
        item["u_all"][u_key] += 1
        item["margin_sum_all"] += int(row["terminal_end_label"]["first_end_margin"])
        item["margin_count_all"] += 1
        if len(item["examples"]) < 3:
            item["examples"].append(f"{row['end_id']}:{row['own_global_shot_number']}")

    states = [
        {
            "state_id": state,
            "sample_count": count,
            "runtime_features": state_features[state],
            "fine_substate_count": len(fine_substates_by_core[state]),
            "fine_sample_count": sum(fine_substates_by_core[state].values()),
            "eligible_for_later_estimation": count >= MIN_STATE_SUPPORT,
        }
        for state, count in sorted(state_counts.items(), key=lambda item: (int(item[0].split("_")[0][1:]), -item[1], item[0]))
    ]
    edges: list[dict[str, Any]] = []
    for (state, action), item in sorted(edge_data.items()):
        train_support = sum(item["train"].values())
        holdout_support = sum(item["holdout"].values())
        reply_tv = _total_variation(item["reply_train"], item["reply_holdout"])
        next_tv = _total_variation(item["next_train"], item["next_holdout"])
        support_ok = (
            state_counts[state] >= MIN_STATE_SUPPORT
            and train_support >= MIN_ACTION_TRAIN_SUPPORT
            and holdout_support >= MIN_ACTION_HOLDOUT_SUPPORT
        )
        stable = support_ok and reply_tv is not None and next_tv is not None and max(reply_tv, next_tv) <= STABILITY_TV_THRESHOLD
        edges.append(
            {
                "from_state": state,
                "observed_own_effect": action,
                "support_all": sum(item["all"].values()),
                "support_train": train_support,
                "support_holdout": holdout_support,
                "mean_terminal_end_margin_observed": round(item["margin_sum_all"] / item["margin_count_all"], 4),
                "own_post_shot_topology_distribution": _distribution(item["u_all"]),
                "opponent_reply_distribution": _distribution(item["reply_all"]),
                "next_state_distribution": _distribution(item["next_all"]),
                "holdout_reply_total_variation": reply_tv,
                "holdout_next_state_total_variation": next_tv,
                "estimation_support_ok": support_ok,
                "distribution_stable_at_threshold": stable,
                "examples": item["examples"],
            }
        )

    edge_support_ok = sum(1 for edge in edges if edge["estimation_support_ok"])
    edge_stable = sum(1 for edge in edges if edge["distribution_stable_at_threshold"])
    return {
        "schema": "nwnht_first_player_causal_state_abstraction_v1",
        "purpose": "Runtime-safe candidate state cells and observational transition diagnostics; not a policy and not a causal estimate.",
        "runtime_input_contract": "K (1..8) plus current stone coordinates/owners only. No score, end number, match, team, event, called-shot or terminal label enters state_id.",
        "feature_definition": {
            "core_features": list(CORE_FEATURES),
            "fine_only_features": list(FINE_ONLY_FEATURES),
            "control_rule": "FIRST/OPPONENT only when v2 scoring control is certain; NONE_OR_UNCERTAIN otherwise.",
            "protection_rule": "same-owner guard in front within 0.42m lateral distance; a topology proxy, not an untouchable-shell claim.",
        },
        "thresholds": {
            "min_state_support": MIN_STATE_SUPPORT,
            "min_action_train_support": MIN_ACTION_TRAIN_SUPPORT,
            "min_action_holdout_support": MIN_ACTION_HOLDOUT_SUPPORT,
            "stability_total_variation_threshold": STABILITY_TV_THRESHOLD,
        },
        "source": {"row_count": row_count, "match_split_counts": dict(sorted(match_splits.items()))},
        "summary": {
            "core_state_count": len(states),
            "fine_state_count": len(fine_counts),
            "core_states_with_minimum_support": sum(1 for state in states if state["eligible_for_later_estimation"]),
            "state_action_edges": len(edges),
            "edges_with_minimum_train_holdout_support": edge_support_ok,
            "edges_with_support_and_distribution_stability": edge_stable,
        },
        "states": states,
        "state_action_diagnostics": edges,
        "limits": [
            "Observed own effect is a post-shot board label, not a randomized treatment.",
            "Observed end margin is descriptive only; it is not adjusted for team/event or unobserved tactical context.",
            "A stable grouped holdout distribution is a screening condition, not causal identification or policy validation.",
            "Fine states are retained only to quantify within-core heterogeneity; no automated state merge is claimed in v0.",
        ],
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_causal_state_abstraction_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new path deliberately.")
    result = build(read_jsonl(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
