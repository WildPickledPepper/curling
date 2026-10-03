#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit fine endpoint/binding constraints for audited same-K semantic goals.

For a semantic template borrowed within the same K and macro state, this stage
does not invent a point.  It gathers only historical implementations of that
same semantic result, conditionally weights them by pre-shot geometry, and
requires the leading fine constraint signature to recur across grouped match
folds.  The result remains observational evidence until its runtime adapter is
added and locally validated.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_causal_estimation_panel import FOLDS, fold_for_match
    from .build_goal_library_v2 import _active_region, _canonical, _grid_key
    from .conditional_same_k_goal_audit_v1 import KERNEL_GAMMA, _similarity, _template_id, _template_key
    from .partition_states_v2 import SPLIT_FEATURES
    from .state_features_v2 import state_features
except ImportError:  # pragma: no cover
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import FOLDS, fold_for_match  # type: ignore
    from causal_state_machine.build_goal_library_v2 import _active_region, _canonical, _grid_key  # type: ignore
    from causal_state_machine.conditional_same_k_goal_audit_v1 import KERNEL_GAMMA, _similarity, _template_id, _template_key  # type: ignore
    from causal_state_machine.partition_states_v2 import SPLIT_FEATURES  # type: ignore
    from causal_state_machine.state_features_v2 import state_features  # type: ignore


MIN_FINE_TRAIN_SUPPORT = 5
MIN_PRIMARY_FOLD_CONSENSUS = 4
MIN_TOTAL_HELDOUT_DIRECT_SUPPORT = 3
MAX_FINE_OPTIONS = 3


def _profiles(rows: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, str]]:
    counts: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    for row in rows:
        for name, value in row["features"].items():
            counts[str(row["source_state"])][str(name)][str(value)] += 1
    return {
        state: {name: values.most_common(1)[0][0] for name, values in fields.items()}
        for state, fields in counts.items()
    }


def _fine_signature(row: Mapping[str, Any]) -> tuple[Any, ...]:
    """Fine signature is an endpoint grid plus only safe anonymous bindings."""

    point = row.get("active_final_point")
    return (
        str(row.get("precision")),
        _grid_key(point),
        _canonical(row.get("stone_constraints_when_unambiguous", [])),
        _canonical(row.get("dynamic_house_removal_binding_request")),
        _canonical(row.get("after_own_occupancy", {})),
    )


def _signature_key(signature: tuple[Any, ...]) -> str:
    return _canonical(list(signature))


def _fine_goal(signature: tuple[Any, ...], rows: list[Mapping[str, Any]], weighted_support: float) -> dict[str, Any]:
    precision, _, selectors_json, binding_json, occupancy_json = signature
    points = [
        (float(row["active_final_point"]["x_m"]), float(row["active_final_point"]["y_m"]))
        for row in rows if row.get("active_final_point") is not None
    ]
    return {
        "fine_signature_key": _signature_key(signature),
        "precision": precision,
        "active_final_region": _active_region(points),
        "stone_constraints_when_unambiguous": json.loads(selectors_json),
        "dynamic_house_removal_binding_request": json.loads(binding_json),
        "after_own_occupancy": json.loads(occupancy_json),
        "train_raw_support": len(rows),
        "train_similarity_weighted_support": round(weighted_support, 6),
        "examples": [str(row["panel_key"]) for row in rows[:5]],
    }


def collect(template_rows: Iterable[Mapping[str, Any]], transitions: Iterable[Mapping[str, Any]], state_meta: Mapping[str, tuple[int, str]], *, wanted_template_ids: set[str] | None = None) -> list[dict[str, Any]]:
    transition_by_panel = {f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transitions}
    records: list[dict[str, Any]] = []
    for raw in template_rows:
        template_id = _template_id(_template_key(raw))
        if wanted_template_ids is not None and template_id not in wanted_template_ids:
            continue
        state = str(raw["source_state"])
        if state not in state_meta:
            continue
        source = transition_by_panel.get(str(raw["panel_key"]))
        if source is None:
            raise ValueError(f"missing transition {raw['panel_key']}")
        k, macro = state_meta[state]
        if int(raw["K"]) != k:
            raise ValueError(f"K mismatch in raw template {raw['panel_key']}")
        records.append({
            **dict(raw),
            "macro": macro,
            "template_id": template_id,
            "fine_signature": _fine_signature(raw),
            "fold": fold_for_match(int(source["match_id"])),
            "features": {name: str(state_features(k, source["s_before_own"])[name]) for name in SPLIT_FEATURES},
        })
    return records


def _rank_for_state(records: list[Mapping[str, Any]], state: str, *, min_train_support: int = MIN_FINE_TRAIN_SUPPORT) -> list[dict[str, Any]]:
    profiles = _profiles(records)
    target = profiles.get(state)
    if not target:
        return []
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    weighted: dict[tuple[Any, ...], float] = defaultdict(float)
    for row in records:
        signature = row["fine_signature"]
        grouped[signature].append(row)
        weighted[signature] += math.exp(KERNEL_GAMMA * _similarity(target, profiles.get(str(row["source_state"]), {})))
    candidates = []
    for signature, rows in grouped.items():
        if len(rows) < min_train_support:
            continue
        candidate = _fine_goal(signature, rows, weighted[signature])
        # A semantic post-own predicate alone is not a fine goal.  At least
        # one endpoint region or safe dynamic/identity binding must remain.
        if (
            candidate["active_final_region"] is None
            and not candidate["stone_constraints_when_unambiguous"]
            and candidate["dynamic_house_removal_binding_request"] is None
        ):
            continue
        candidates.append(candidate)
    candidates.sort(key=lambda row: (-float(row["train_similarity_weighted_support"]), -int(row["train_raw_support"]), _canonical(row)))
    return candidates[:MAX_FINE_OPTIONS]


def build(records: Iterable[Mapping[str, Any]], registry: Mapping[str, Any]) -> dict[str, Any]:
    """Run fold-isolated fine compilation only for semantic-only registry rows."""

    records = [dict(row) for row in records]
    pending = [
        dict(row) for row in registry["state_plans"]
        if row["recommendation_status"] == "CONDITIONAL_SEMANTIC_GOAL_CONSENSUS_PENDING_FINE_COMPILATION"
    ]
    plans: list[dict[str, Any]] = []
    for plan in pending:
        state, k = str(plan["state_id"]), int(plan["K"])
        semantic = plan["primary_goal"]["goal_template"]
        template_id = str(plan["primary_goal"]["template_id"])
        # The semantic topology includes its macro state, so a matching
        # template id already implies same K and same macro; never infer a
        # macro by parsing a human-readable state id.
        base = [row for row in records if int(row["K"]) == k and str(row["template_id"]) == template_id]
        if not base:
            plans.append({"state_id": state, "K": k, "recommendation_status": "NO_FINE_IMPLEMENTATION_RECORDS", "primary_goal": None})
            continue
        fold_primary: list[dict[str, Any]] = []
        for holdout in range(FOLDS):
            train = [row for row in base if int(row["fold"]) != holdout]
            options = _rank_for_state(train, state)
            if not options:
                continue
            primary = dict(options[0])
            signature = str(primary["fine_signature_key"])
            heldout = [
                row for row in base if int(row["fold"]) == holdout and _signature_key(row["fine_signature"]) == signature and str(row["source_state"]) == state
            ]
            primary.update({"holdout_fold": holdout, "holdout_direct_source_support": len(heldout)})
            fold_primary.append(primary)
        votes = Counter(str(row["fine_signature_key"]) for row in fold_primary)
        if not votes:
            plans.append({"state_id": state, "K": k, "recommendation_status": "NO_FINE_CONSENSUS", "primary_goal": None, "fold_choices": []})
            continue
        selected_key, vote_count = votes.most_common(1)[0]
        selected = [row for row in fold_primary if str(row["fine_signature_key"]) == selected_key]
        support = sum(int(row["holdout_direct_source_support"]) for row in selected)
        status = (
            "CONDITIONAL_FINE_GOAL_CONSENSUS"
            if vote_count >= MIN_PRIMARY_FOLD_CONSENSUS and support >= MIN_TOTAL_HELDOUT_DIRECT_SUPPORT
            else "CONDITIONAL_FINE_GOAL_AUDIT_ONLY"
        )
        representative = dict(selected[0])
        representative.pop("holdout_fold", None)
        representative.pop("holdout_direct_source_support", None)
        plans.append({
            "state_id": state, "K": k, "recommendation_status": status,
            "semantic_goal_template": semantic,
            "primary_goal": representative,
            "primary_fold_count": vote_count,
            "total_direct_source_holdout_support": support,
            "fold_choices": selected,
            "warning": "Fine constraint is conditionally borrowed from same-K historical implementations; it is observational and requires later runtime/physics validation.",
        })
    return {
        "manifest": {
            "schema": "nwnht_v2_conditional_fine_goal_audit_v1",
            "input_pending_semantic_state_count": len(pending),
            "thresholds": {"min_fine_train_support": MIN_FINE_TRAIN_SUPPORT, "min_primary_fold_consensus": MIN_PRIMARY_FOLD_CONSENSUS, "min_total_heldout_direct_source_support": MIN_TOTAL_HELDOUT_DIRECT_SUPPORT},
            "prohibition": "Audit only. Do not deploy a compiled conditional fine goal before adding source-board runtime conditioning and local rule/PhysX checks.",
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
    parser.add_argument("--registry", type=Path, default=root / "nwnht_v2_goal_evidence_registry_v1.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_conditional_fine_goal_audit_v3.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    wanted = {
        str(row["primary_goal"]["template_id"])
        for row in registry["state_plans"]
        if row["recommendation_status"] == "CONDITIONAL_SEMANTIC_GOAL_CONSENSUS_PENDING_FINE_COMPILATION"
    }
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    meta = {str(row["state_id"]): (int(row["K"]), str(row["macro_state"])) for row in partition["states"]}
    records = collect(_read_jsonl(args.templates), _read_jsonl(args.transitions), meta, wanted_template_ids=wanted)
    result = build(records, registry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "status_counts": dict(Counter(row["recommendation_status"] for row in result["state_plans"]))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
