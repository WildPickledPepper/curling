#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Five-fold audit of conditional same-K semantic GoalState templates.

Templates are shared only within the same K and macro state.  Their values are
estimated conditionally on S by a deterministic kernel over runtime geometry
features; no score, team, call text, or post-shot value enters the kernel.
The output is evidence for a later model choice, never a deployed policy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_causal_estimation_panel import FOLDS, fold_for_match
    from .partition_states_v2 import SPLIT_FEATURES
    from .state_features_v2 import state_features
except ImportError:  # pragma: no cover
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import FOLDS, fold_for_match  # type: ignore
    from causal_state_machine.partition_states_v2 import SPLIT_FEATURES  # type: ignore
    from causal_state_machine.state_features_v2 import state_features  # type: ignore


MIN_TRAIN_TEMPLATE_SUPPORT = 10
KERNEL_GAMMA = 4.0
MAX_CANDIDATES = 3
MIN_PRIMARY_FOLD_CONSENSUS = 4
MIN_TOTAL_HELDOUT_DIRECT_SUPPORT = 5


def _template_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    delta = row["observed_delta"]
    return (int(row["K"]), str(row["observed_template_kind"]), int(delta["opponent_removed_count"]), int(delta["opponent_house_removed_count"]), str(row["post_own_topology"]))


def _template_id(key: tuple[Any, ...]) -> str:
    return "nwnht_v2_conditional_same_k_goal_" + hashlib.sha256(repr(key).encode("utf-8")).hexdigest()[:16]


def _mean(values: Iterable[float], default: float = 0.0) -> float:
    values = list(values)
    return sum(values) / len(values) if values else default


def collect(templates: Iterable[Mapping[str, Any]], transitions: Iterable[Mapping[str, Any]], state_meta: Mapping[str, tuple[int, str]]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    by_panel = {f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transitions}
    rows: list[dict[str, Any]] = []
    prototype: dict[str, dict[str, Any]] = {}
    for raw in templates:
        source = by_panel.get(str(raw["panel_key"]))
        if source is None:
            raise ValueError(f"missing transition {raw['panel_key']}")
        state = str(raw["source_state"])
        if state not in state_meta:
            continue
        key = _template_key(raw)
        template_id = _template_id(key)
        k, kind, removed, house_removed, topology = key
        prototype.setdefault(template_id, {
            "template_id": template_id, "K": k, "observed_template_kind": kind,
            "observed_opponent_removed_count": removed, "observed_opponent_house_removed_count": house_removed,
            "post_own_topology": topology,
        })
        features = state_features(k, source["s_before_own"])
        rows.append({
            "K": k, "source_state": state, "macro": state_meta[state][1], "template_id": template_id,
            "next_state": str(raw["after_opponent_reply_state"]),
            "margin": float(source["terminal_end_label"]["first_end_margin"]),
            "fold": fold_for_match(int(source["match_id"])),
            "features": {name: str(features[name]) for name in SPLIT_FEATURES},
        })
    return rows, prototype


def _profiles(rows: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, str]]:
    counts: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    for row in rows:
        for name, value in row["features"].items():
            counts[str(row["source_state"])][str(name)][str(value)] += 1
    return {state: {name: counter.most_common(1)[0][0] for name, counter in fields.items()} for state, fields in counts.items()}


def _similarity(left: Mapping[str, str], right: Mapping[str, str]) -> float:
    if not left or not right:
        return 0.0
    names = set(left) & set(right)
    return sum(left[name] == right[name] for name in names) / len(names) if names else 0.0


def fit(train_rows: Iterable[Mapping[str, Any]], state_meta: Mapping[str, tuple[int, str]], *, min_template_support: int = MIN_TRAIN_TEMPLATE_SUPPORT, gamma: float = KERNEL_GAMMA, max_candidates: int = MAX_CANDIDATES) -> dict[str, list[dict[str, Any]]]:
    rows = [dict(row) for row in train_rows]
    profiles = _profiles(rows)
    templates_by_macro: dict[tuple[int, str], Counter[str]] = defaultdict(Counter)
    for row in rows:
        templates_by_macro[(int(row["K"]), str(row["macro"]))][str(row["template_id"])] += 1
    allowed = {key: {template for template, support in counter.items() if support >= min_template_support} for key, counter in templates_by_macro.items()}
    values: dict[str, float] = {}
    result: dict[str, list[dict[str, Any]]] = {}
    for k in range(8, 0, -1):
        current = [row for row in rows if int(row["K"]) == k]
        pair: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in current:
            continuation = float(row["margin"]) if k == 8 else values.get(str(row["next_state"]), float(row["margin"]))
            pair[(str(row["source_state"]), str(row["template_id"]))].append(continuation)
        states = [state for state, (state_k, _) in state_meta.items() if state_k == k]
        for state in states:
            macro = state_meta[state][1]
            candidates: list[dict[str, Any]] = []
            for template in allowed.get((k, macro), set()):
                numerator = denominator = 0.0
                direct_support = len(pair.get((state, template), []))
                for other in states:
                    observed = pair.get((other, template), [])
                    if not observed:
                        continue
                    weight = math.exp(float(gamma) * _similarity(profiles.get(state, {}), profiles.get(other, {})))
                    numerator += weight * sum(observed)
                    denominator += weight * len(observed)
                if denominator:
                    candidates.append({
                        "template_id": template,
                        "conditional_backed_up_value": round(numerator / denominator, 6),
                        "train_direct_support": direct_support,
                        "train_same_macro_template_support": int(templates_by_macro[(k, macro)][template]),
                    })
            candidates.sort(key=lambda item: (-float(item["conditional_backed_up_value"]), -int(item["train_direct_support"]), item["template_id"]))
            result[state] = candidates[:max_candidates]
            if candidates:
                values[state] = float(candidates[0]["conditional_backed_up_value"])
    return result


def build(rows: Iterable[Mapping[str, Any]], prototypes: Mapping[str, Mapping[str, Any]], state_meta: Mapping[str, tuple[int, str]]) -> dict[str, Any]:
    rows = [dict(row) for row in rows]
    fold_choices: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for holdout in range(FOLDS):
        train = [row for row in rows if int(row["fold"]) != holdout]
        test = [row for row in rows if int(row["fold"]) == holdout]
        fitted = fit(train, state_meta)
        heldout_pairs: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in test:
            heldout_pairs[(str(row["source_state"]), str(row["template_id"]))].append(float(row["margin"]))
        for state, candidates in fitted.items():
            if not candidates:
                continue
            primary = dict(candidates[0])
            observed = heldout_pairs.get((state, str(primary["template_id"])), [])
            primary.update({
                "holdout_fold": holdout, "holdout_direct_support": len(observed),
                "holdout_direct_margin_mean": None if not observed else round(_mean(observed), 6),
            })
            fold_choices[state].append(primary)
    plans: list[dict[str, Any]] = []
    for state, (k, macro) in sorted(state_meta.items(), key=lambda item: (item[1][0], item[0])):
        choices = fold_choices.get(state, [])
        votes = Counter(str(choice["template_id"]) for choice in choices)
        if not votes:
            plans.append({"state_id": state, "K": k, "recommendation_status": "NO_CONDITIONAL_TEMPLATE_CANDIDATE", "primary_goal": None, "fold_choices": []})
            continue
        template_id, vote_count = votes.most_common(1)[0]
        selected = [choice for choice in choices if str(choice["template_id"]) == template_id]
        heldout_support = sum(int(choice["holdout_direct_support"]) for choice in selected)
        status = (
            "CONDITIONAL_TEMPLATE_CONSENSUS_WITH_DIRECT_HOLDOUT_EVIDENCE"
            if vote_count >= MIN_PRIMARY_FOLD_CONSENSUS and heldout_support >= MIN_TOTAL_HELDOUT_DIRECT_SUPPORT
            else "CONDITIONAL_TEMPLATE_AUDIT_ONLY"
        )
        plans.append({
            "state_id": state, "K": k, "macro_state": macro, "recommendation_status": status,
            "primary_goal": {
                "template_id": template_id, "goal_template": dict(prototypes[template_id]),
                "primary_fold_count": vote_count,
                "selected_fold_count": len(selected),
                "mean_conditional_backed_up_value": round(_mean(float(choice["conditional_backed_up_value"]) for choice in selected), 6),
                "total_direct_holdout_support": heldout_support,
            },
            "fold_template_distribution": dict(votes.most_common()),
            "fold_choices": selected,
            "warning": "Conditional same-K template estimator. It is an observational audit and not a causal or PhysX-valid policy.",
        })
    return {
        "manifest": {
            "schema": "nwnht_v2_conditional_same_k_goal_audit_v1",
            "purpose": "Five-fold audit of conditional same-K shared semantic templates.",
            "thresholds": {"min_train_template_support": MIN_TRAIN_TEMPLATE_SUPPORT, "kernel_gamma": KERNEL_GAMMA, "min_primary_fold_consensus": MIN_PRIMARY_FOLD_CONSENSUS, "min_total_heldout_direct_support": MIN_TOTAL_HELDOUT_DIRECT_SUPPORT},
            "prohibition": "Audit only. Do not wire this artifact into runtime until comparison against direct-evidence policy and rule/PhysX checks are complete.",
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
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_conditional_same_k_goal_audit_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    state_meta = {str(row["state_id"]): (int(row["K"]), str(row["macro_state"])) for row in partition["states"]}
    rows, prototypes = collect(_read_jsonl(args.templates), _read_jsonl(args.transitions), state_meta)
    result = build(rows, prototypes, state_meta)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = Counter(row["recommendation_status"] for row in result["state_plans"])
    print(json.dumps({"output": str(args.output), "state_count": len(result["state_plans"]), "status_counts": dict(summary)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
