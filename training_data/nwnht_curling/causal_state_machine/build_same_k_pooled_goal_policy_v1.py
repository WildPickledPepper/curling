#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prototype same-K pooled semantic GoalState ranking.

An exact endpoint is state-specific, but a post-own tactical *template* can be
shared by several states at the same K.  This module keeps values conditional
on S while shrinking sparse ``Q(S,T)`` estimates toward (1) the same-K
template mean and (2) the same-state baseline.  It never pools a K3 template
with K4, and it is an audit prototype rather than a deployable policy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping


MIN_TEMPLATE_SUPPORT = 30
TEMPLATE_PRIOR_WEIGHT = 20.0
STATE_PRIOR_WEIGHT = 10.0
MAX_CANDIDATES = 5


def _template_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    delta = row["observed_delta"]
    return (
        int(row["K"]), str(row["observed_template_kind"]),
        int(delta["opponent_removed_count"]), int(delta["opponent_house_removed_count"]),
        str(row["post_own_topology"]),
    )


def _template_id(key: tuple[Any, ...]) -> str:
    return "nwnht_v2_same_k_semantic_goal_" + hashlib.sha256(repr(key).encode("utf-8")).hexdigest()[:16]


def _mean(values: Iterable[float], default: float = 0.0) -> float:
    values = list(values)
    return sum(values) / len(values) if values else default


def _compatible_with_state_macro(macro: str | None, prototype: Mapping[str, Any]) -> bool:
    """Reject only removals that a macro state proves impossible.

    This is deliberately a minimum safety screen, not a reachability oracle.
    The runtime board still has to check the exact target count before asking
    a planner to bind a removal goal.
    """

    removed = int(prototype.get("observed_opponent_house_removed_count", 0))
    if removed == 0 or macro is None:
        return True
    return str(macro) not in {"EMPTY", "GUARD_EXCHANGE"}


def collect(
    templates: Iterable[Mapping[str, Any]], transitions: Iterable[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Join raw realised endpoints to terminal labels without using intent."""

    by_panel = {
        f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transitions
    }
    rows: list[dict[str, Any]] = []
    prototypes: dict[str, dict[str, Any]] = {}
    for raw in templates:
        panel = str(raw["panel_key"])
        source = by_panel.get(panel)
        if source is None:
            raise ValueError(f"missing transition for template {panel}")
        key = _template_key(raw)
        template_id = _template_id(key)
        if template_id not in prototypes:
            k, kind, removed, house_removed, topology = key
            prototypes[template_id] = {
                "template_id": template_id, "K": k,
                "observed_template_kind": kind,
                "observed_opponent_removed_count": removed,
                "observed_opponent_house_removed_count": house_removed,
                "post_own_topology": topology,
                "runtime_preconditions": (
                    [] if house_removed == 0 else [f"current opponent house count >= {house_removed}"]
                ),
                "warning": "Shared semantic template only. It must be instantiated against the current board; it is not a transferable fixed endpoint.",
            }
        rows.append({
            "K": int(raw["K"]), "source_state": str(raw["source_state"]),
            "template_id": template_id, "next_state": str(raw["after_opponent_reply_state"]),
            "margin": float(source["terminal_end_label"]["first_end_margin"]),
        })
    return rows, prototypes


def build(
    rows: Iterable[Mapping[str, Any]], prototypes: Mapping[str, Mapping[str, Any]], state_k: Mapping[str, int], *,
    state_macro: Mapping[str, str] | None = None,
    min_template_support: int = MIN_TEMPLATE_SUPPORT,
    template_prior_weight: float = TEMPLATE_PRIOR_WEIGHT,
    state_prior_weight: float = STATE_PRIOR_WEIGHT,
    max_candidates: int = MAX_CANDIDATES,
) -> dict[str, Any]:
    """Run K8->K1 value backup with same-K partial pooling."""

    all_rows = [dict(row) for row in rows]
    template_support = Counter(str(row["template_id"]) for row in all_rows)
    allowed = {
        template_id for template_id, support in template_support.items()
        if support >= int(min_template_support)
    }
    rows_by_k: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in all_rows:
        rows_by_k[int(row["K"])].append(row)

    values: dict[str, float] = {}
    plans: list[dict[str, Any]] = []
    for k in range(8, 0, -1):
        current = rows_by_k[k]
        by_state: dict[str, list[dict[str, Any]]] = defaultdict(list)
        by_template: dict[str, list[dict[str, Any]]] = defaultdict(list)
        by_pair: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in current:
            continuation = float(row["margin"]) if k == 8 else values.get(str(row["next_state"]), float(row["margin"]))
            row = {**row, "continuation": continuation}
            by_state[str(row["source_state"])].append(row)
            if str(row["template_id"]) in allowed:
                by_template[str(row["template_id"])].append(row)
                by_pair[(str(row["source_state"]), str(row["template_id"]))].append(row)
        global_mean = _mean((float(row["continuation"]) for rows in by_state.values() for row in rows))
        template_mean = {
            template_id: _mean(float(row["continuation"]) for row in template_rows)
            for template_id, template_rows in by_template.items()
        }
        state_mean = {
            state: _mean((float(row["continuation"]) for row in state_rows), global_mean)
            for state, state_rows in by_state.items()
        }
        templates_at_k = sorted(template_mean)
        for state, state_k_value in state_k.items():
            if int(state_k_value) != k:
                continue
            baseline = state_mean.get(state, global_mean)
            candidates: list[dict[str, Any]] = []
            for template_id in templates_at_k:
                if not _compatible_with_state_macro(
                    None if state_macro is None else state_macro.get(state), prototypes[template_id]
                ):
                    continue
                direct_rows = by_pair.get((state, template_id), [])
                direct_support = len(direct_rows)
                direct_mean = _mean((float(row["continuation"]) for row in direct_rows), template_mean[template_id])
                q = (
                    direct_support * direct_mean
                    + float(template_prior_weight) * template_mean[template_id]
                    + float(state_prior_weight) * baseline
                ) / (direct_support + float(template_prior_weight) + float(state_prior_weight))
                candidates.append({
                    "template_id": template_id,
                    "pooled_backed_up_value": round(q, 6),
                    "direct_support_in_this_state": direct_support,
                    "same_k_template_support": int(template_support[template_id]),
                    "evidence_status": "DIRECT_PLUS_SAME_K_POOL" if direct_support else "SAME_K_POOLED_NO_DIRECT_REALISATION",
                    "goal_template": dict(prototypes[template_id]),
                })
            candidates.sort(key=lambda item: (-float(item["pooled_backed_up_value"]), -int(item["direct_support_in_this_state"]), item["template_id"]))
            chosen = candidates[:int(max_candidates)]
            values[state] = float(chosen[0]["pooled_backed_up_value"]) if chosen else baseline
            plans.append({
                "state_id": state, "K": k,
                "recommendation_status": "POOLED_SEMANTIC_GOAL_CANDIDATES_NOT_DEPLOYED",
                "primary_goal": chosen[0] if chosen else None,
                "fallback_goals": chosen[1:],
                "state_baseline_continuation_value": round(baseline, 6),
                "warning": "This fills sparse candidate sets by same-K partial pooling. It is not five-fold validated and must not replace the direct-evidence runtime plan.",
            })
    plans.sort(key=lambda item: (int(item["K"]), str(item["state_id"])))
    return {
        "manifest": {
            "schema": "nwnht_v2_same_k_pooled_semantic_goal_policy_v2",
            "purpose": "Coverage audit for same-K shared semantic GoalState templates; not a deployment policy.",
            "template_count": len(allowed), "state_plan_count": len(plans),
            "thresholds": {
                "min_template_support": min_template_support,
                "template_prior_weight": template_prior_weight,
                "state_prior_weight": state_prior_weight,
                "max_candidates": max_candidates,
            },
            "prohibition": "Do not treat pooled values as direct causal evidence, five-fold consensus, PhysX feasibility, or a guaranteed move.",
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
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_same_k_pooled_semantic_goal_policy_v2.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    rows, prototypes = collect(_read_jsonl(args.templates), _read_jsonl(args.transitions))
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    state_k = {str(row["state_id"]): int(row["K"]) for row in partition["states"]}
    state_macro = {str(row["state_id"]): str(row["macro_state"]) for row in partition["states"]}
    result = build(rows, prototypes, state_k, state_macro=state_macro)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
