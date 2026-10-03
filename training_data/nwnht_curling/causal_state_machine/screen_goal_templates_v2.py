#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Holdout descriptive stability screen for frozen v2 endpoint templates.

This screen is intentionally incapable of promoting a template to a causal
policy edge.  A goal family is inferred from the *realised post-shot board*,
so it is a post-treatment endpoint rather than an independently observed
pre-shot intervention.  The code makes that rejection explicit rather than
burying it under a ranking score.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_causal_estimation_panel import fold_for_match
    from .build_goal_library_v2 import _goal_id, _signature
    from .partition_states_v2 import total_variation
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import fold_for_match  # type: ignore
    from causal_state_machine.build_goal_library_v2 import _goal_id, _signature  # type: ignore
    from causal_state_machine.partition_states_v2 import total_variation  # type: ignore


HOLDOUT_FOLD = 4
MIN_DEV_SUPPORT = 25
MIN_HOLDOUT_SUPPORT = 10
MAX_REPLY_TV = 0.35


def _outcome(margin: int) -> str:
    return "FIRST_SCORES" if margin > 0 else "OPPONENT_SCORES" if margin < 0 else "BLANK"


def _summary(item: Mapping[str, Any], split: str) -> dict[str, Any]:
    support = int(item[f"{split}_support"])
    outcomes: Counter[str] = item[f"{split}_outcomes"]
    margins: list[int] = item[f"{split}_margins"]
    return {
        "support": support,
        "observed_mean_first_end_margin": None if not support else round(sum(margins) / support, 6),
        "observed_first_scores_rate": None if not support else round(outcomes["FIRST_SCORES"] / support, 6),
        "observed_outcome_counts": dict(sorted(outcomes.items())),
    }


def build(
    transition_rows: Iterable[Mapping[str, Any]],
    templates: Iterable[Mapping[str, Any]],
    goals: Iterable[Mapping[str, Any]],
    *,
    holdout_fold: int = HOLDOUT_FOLD,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_panel = {f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transition_rows}
    candidates = {str(goal["goal_id"]): goal for goal in goals if bool(goal["runtime_goal_candidate"])}
    grouped: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "dev_support": 0, "holdout_support": 0,
        "dev_margins": [], "holdout_margins": [],
        "dev_outcomes": Counter(), "holdout_outcomes": Counter(),
        "dev_reply": Counter(), "holdout_reply": Counter(),
        "dev_post": Counter(), "holdout_post": Counter(),
    })
    for template in templates:
        goal_id = _goal_id(_signature(template))
        if goal_id not in candidates:
            continue
        raw = by_panel.get(str(template["panel_key"]))
        if raw is None:
            raise ValueError(f"missing transition row for {template['panel_key']}")
        split = "holdout" if fold_for_match(int(raw["match_id"])) == holdout_fold else "dev"
        item = grouped[goal_id]
        item[f"{split}_support"] += 1
        margin = int(raw["terminal_end_label"]["first_end_margin"])
        item[f"{split}_margins"].append(margin)
        item[f"{split}_outcomes"][_outcome(margin)] += 1
        item[f"{split}_reply"][str(template["after_opponent_reply_state"])] += 1
        item[f"{split}_post"][str(template["post_own_topology"])] += 1

    rows: list[dict[str, Any]] = []
    for goal_id, goal in sorted(candidates.items()):
        item = grouped[goal_id]
        dev, holdout = _summary(item, "dev"), _summary(item, "holdout")
        reply_tv = total_variation(item["dev_reply"], item["holdout_reply"])
        post_tv = total_variation(item["dev_post"], item["holdout_post"])
        descriptive_stable = (
            dev["support"] >= MIN_DEV_SUPPORT and holdout["support"] >= MIN_HOLDOUT_SUPPORT
            and reply_tv is not None and post_tv is not None
            and max(reply_tv, post_tv) <= MAX_REPLY_TV
        )
        rows.append({
            "goal_id": goal_id,
            "source_state": goal["source_state"],
            "development": dev,
            "holdout": holdout,
            "post_own_total_variation_dev_vs_holdout": None if post_tv is None else round(post_tv, 6),
            "reply_state_total_variation_dev_vs_holdout": None if reply_tv is None else round(reply_tv, 6),
            "descriptive_stability_pass": descriptive_stable,
            "causal_deployment_status": "REJECTED_POST_TREATMENT_ENDPOINT",
            "causal_rejection_reason": "goal_id is defined by the realised post-shot S->U endpoint. The observational record does not identify a pre-shot attempt to choose this GoalState, so no causal action value or deployable winning edge is estimable from this screen.",
            "selection_leakage_note": "The structural candidate set was selected from the full data before this descriptive split. These holdout values are diagnostics, not an independent policy evaluation.",
        })
    return rows, {
        "schema": "nwnht_v2_goal_template_descriptive_screen_v0",
        "holdout_fold": holdout_fold,
        "candidate_goal_count": len(candidates),
        "descriptive_stability_pass_count": sum(bool(row["descriptive_stability_pass"]) for row in rows),
        "causal_deployable_goal_count": 0,
        "thresholds": {"min_dev_support": MIN_DEV_SUPPORT, "min_holdout_support": MIN_HOLDOUT_SUPPORT, "max_reply_or_post_tv": MAX_REPLY_TV},
        "prohibition": "Do not rank or execute a goal from terminal outcome association in this artifact. A pre-shot target/intent treatment or a controlled intervention dataset is required first.",
    }


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
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_goal_template_descriptive_screen_v0.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    goals = json.loads(args.goals.read_text(encoding="utf-8"))
    rows, manifest = build(_read_jsonl(args.transitions), _read_jsonl(args.templates), goals)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"manifest": manifest, "rows": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **manifest}, ensure_ascii=False))


if __name__ == "__main__":
    main()
