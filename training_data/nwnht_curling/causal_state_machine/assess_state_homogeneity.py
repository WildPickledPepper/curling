#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Screen whether candidate CORE states hide stable fine-board differences.

For each observed (CORE state, own board-effect) cell, compare the opponent's
reply-effect distribution between its FINE substates.  Comparisons are split
by match, so a fine-board difference must recur in both train and holdout to
be labelled ``STABLE_HETEROGENEITY_SPLIT``.

This is a state-abstraction screen, not a causal effect estimate: own board
effects are observed post-shot labels and neither team strength nor other
confounding is adjusted here.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    from .build_causal_state_abstraction import (
        MIN_ACTION_HOLDOUT_SUPPORT,
        MIN_ACTION_TRAIN_SUPPORT,
        MIN_STATE_SUPPORT,
        _opponent_reply_effect,
        _split_for_match,
        _total_variation,
        read_jsonl,
        state_key,
    )
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_state_abstraction import (  # type: ignore
        MIN_ACTION_HOLDOUT_SUPPORT,
        MIN_ACTION_TRAIN_SUPPORT,
        MIN_STATE_SUPPORT,
        _opponent_reply_effect,
        _split_for_match,
        _total_variation,
        read_jsonl,
        state_key,
    )


MIN_FINE_TRAIN_SUPPORT = 25
MIN_FINE_HOLDOUT_SUPPORT = 10
HETEROGENEITY_TOTAL_VARIATION_THRESHOLD = 0.25


def _counter_without(total: Counter[str], part: Counter[str]) -> Counter[str]:
    return Counter({key: total[key] - part.get(key, 0) for key in total if total[key] > part.get(key, 0)})


def assess(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    state_count: Counter[str] = Counter()
    # (core, action) -> split -> fine -> reply distribution
    replies: dict[tuple[str, str], dict[str, dict[str, Counter[str]]]] = defaultdict(
        lambda: {"train": defaultdict(Counter), "holdout": defaultdict(Counter)}
    )
    for row in rows:
        k = int(row["own_throw_number"])
        core = state_key(k, list(row["s_before_own"]))
        fine = state_key(k, list(row["s_before_own"]), fine=True)
        action = str(row["observed_own_board_effect"]["primary_effect"])
        reply = _opponent_reply_effect(list(row["u_after_own"]), list(row["s_after_opponent_reply"]))
        split = _split_for_match(int(row["match_id"]))
        state_count[core] += 1
        replies[(core, action)][split][fine][reply] += 1

    diagnostics: list[dict[str, Any]] = []
    for (core, action), by_split in sorted(replies.items()):
        train_total = sum(sum(counter.values()) for counter in by_split["train"].values())
        holdout_total = sum(sum(counter.values()) for counter in by_split["holdout"].values())
        if (
            state_count[core] < MIN_STATE_SUPPORT
            or train_total < MIN_ACTION_TRAIN_SUPPORT
            or holdout_total < MIN_ACTION_HOLDOUT_SUPPORT
        ):
            continue
        fine_ids = sorted(set(by_split["train"]) | set(by_split["holdout"]))
        fine_reports: list[dict[str, Any]] = []
        stable_splits = 0
        for fine in fine_ids:
            child_train = by_split["train"].get(fine, Counter())
            child_holdout = by_split["holdout"].get(fine, Counter())
            all_train = sum((counter for counter in by_split["train"].values()), Counter())
            all_holdout = sum((counter for counter in by_split["holdout"].values()), Counter())
            rest_train = _counter_without(all_train, child_train)
            rest_holdout = _counter_without(all_holdout, child_holdout)
            train_tv = _total_variation(child_train, rest_train)
            holdout_tv = _total_variation(child_holdout, rest_holdout)
            eligible = (
                sum(child_train.values()) >= MIN_FINE_TRAIN_SUPPORT
                and sum(child_holdout.values()) >= MIN_FINE_HOLDOUT_SUPPORT
                and sum(rest_train.values()) >= MIN_FINE_TRAIN_SUPPORT
                and sum(rest_holdout.values()) >= MIN_FINE_HOLDOUT_SUPPORT
            )
            stable = bool(
                eligible
                and train_tv is not None
                and holdout_tv is not None
                and train_tv >= HETEROGENEITY_TOTAL_VARIATION_THRESHOLD
                and holdout_tv >= HETEROGENEITY_TOTAL_VARIATION_THRESHOLD
            )
            stable_splits += int(stable)
            fine_reports.append(
                {
                    "fine_state": fine,
                    "train_support": sum(child_train.values()),
                    "holdout_support": sum(child_holdout.values()),
                    "reply_tv_vs_other_fine_train": train_tv,
                    "reply_tv_vs_other_fine_holdout": holdout_tv,
                    "eligible_for_split_test": eligible,
                    "stable_heterogeneity": stable,
                }
            )
        status = (
            "STABLE_HETEROGENEITY_SPLIT"
            if stable_splits
            else "NO_STABLE_HETEROGENEITY_DETECTED"
            if any(item["eligible_for_split_test"] for item in fine_reports)
            else "INSUFFICIENT_FINE_SUPPORT"
        )
        diagnostics.append(
            {
                "core_state": core,
                "observed_own_effect": action,
                "core_state_support": state_count[core],
                "action_train_support": train_total,
                "action_holdout_support": holdout_total,
                "fine_substates_observed": len(fine_ids),
                "fine_substates_testable": sum(item["eligible_for_split_test"] for item in fine_reports),
                "stable_heterogeneous_fine_substates": stable_splits,
                "abstraction_status": status,
                "fine_diagnostics": fine_reports,
            }
        )

    return {
        "schema": "nwnht_first_player_state_homogeneity_screen_v0",
        "purpose": "Grouped-holdout screen for stable reply-distribution heterogeneity within candidate CORE states; not causal identification.",
        "thresholds": {
            "min_core_state_support": MIN_STATE_SUPPORT,
            "min_core_action_train_support": MIN_ACTION_TRAIN_SUPPORT,
            "min_core_action_holdout_support": MIN_ACTION_HOLDOUT_SUPPORT,
            "min_fine_train_support": MIN_FINE_TRAIN_SUPPORT,
            "min_fine_holdout_support": MIN_FINE_HOLDOUT_SUPPORT,
            "stable_heterogeneity_total_variation_threshold": HETEROGENEITY_TOTAL_VARIATION_THRESHOLD,
        },
        "summary": {
            "screened_core_action_cells": len(diagnostics),
            "stable_heterogeneity_split_cells": sum(item["abstraction_status"] == "STABLE_HETEROGENEITY_SPLIT" for item in diagnostics),
            "no_stable_heterogeneity_detected_cells": sum(item["abstraction_status"] == "NO_STABLE_HETEROGENEITY_DETECTED" for item in diagnostics),
            "insufficient_fine_support_cells": sum(item["abstraction_status"] == "INSUFFICIENT_FINE_SUPPORT" for item in diagnostics),
        },
        "diagnostics": diagnostics,
        "limits": [
            "No stable detected difference is not proof that fine boards are equivalent.",
            "A stable split says only that reply distributions differ observationally; it does not identify why.",
            "Terminal end outcome is intentionally not used in this homogeneity decision because it needs later confounding adjustment.",
        ],
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_state_homogeneity_screen_v0.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new path deliberately.")
    result = assess(read_jsonl(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
