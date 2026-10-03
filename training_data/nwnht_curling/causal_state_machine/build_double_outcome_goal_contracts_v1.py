#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build anonymous whole-board terminal contracts for observed double clears.

NWNHT has no persistent identity for same-colour stones.  After a double
collision it is often impossible to state which surviving first stone was the
delivered stone.  That is an identity limitation, not permission to ignore the
delivered stone's strategic consequence.  This builder therefore uses the
observable anonymous post-own topology as the terminal constraint:

    two dynamically bound opponent house stones out
    + exact anonymous post-own topology of the whole board

Every topology branch retains grouped-match support and its observed opponent
reply distribution.  It is an execution target only after a separate action
value gate and a future multi-target strict-PhysX solver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_causal_estimation_panel import FOLDS, fold_for_match
    from .build_collision_goal_contracts_v1 import _normalise_binding
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_estimation_panel import FOLDS, fold_for_match  # type: ignore
    from causal_state_machine.build_collision_goal_contracts_v1 import _normalise_binding  # type: ignore


MIN_PARENT_SUPPORT = 30
MIN_OUTCOME_SUPPORT = 3
MIN_OUTCOME_FOLD_SUPPORT = 1
MIN_BINDING_SHARE = 0.80


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [{"value": value, "count": count, "share": round(count / total, 6)} for value, count in counter.most_common()]


def _terminal_evidence(labels: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Keep observed end outcomes separate from tactical/causal value claims."""

    rows = [dict(label) for label in labels]
    margins = [int(row["first_end_margin"]) for row in rows if "first_end_margin" in row]
    outcomes = Counter(str(row.get("end_result", "UNKNOWN")) for row in rows)
    return {
        "observed_trajectory_count": len(rows),
        "first_end_margin_mean": round(sum(margins) / len(margins), 6) if margins else None,
        "first_end_margin_distribution": _distribution(Counter(str(value) for value in margins)),
        "end_result_distribution": _distribution(outcomes),
        "warning": "Observed terminal labels on historical trajectories conditional on this branch. They are descriptive evidence, not a causal branch value or a deployment rank.",
    }


def parse_post_own_topology(value: str) -> dict[str, str]:
    """Extract the anonymous whole-board feature predicate from a topology key."""

    prefix, separator, rest = str(value).partition("[")
    if not separator or not rest.endswith("]") or not prefix.startswith("K"):
        raise ValueError(f"invalid post-own topology {value!r}")
    values: dict[str, str] = {}
    for item in rest[:-1].split(";"):
        key, equals, raw = item.partition("=")
        if not equals:
            raise ValueError(f"invalid topology token {item!r}")
        values[key] = raw
    expected = {
        "control", "F_BUTTON", "F_HOUSE_FRONT_LEFT", "F_HOUSE_FRONT_RIGHT", "F_HOUSE_BACK_LEFT",
        "F_HOUSE_BACK_RIGHT", "O_BUTTON", "O_HOUSE_FRONT_LEFT", "O_HOUSE_FRONT_RIGHT",
        "O_HOUSE_BACK_LEFT", "O_HOUSE_BACK_RIGHT", "F_protected_house", "O_protected_house", "macro",
    }
    if set(values) != expected:
        raise ValueError(f"topology feature set changed: {set(values) ^ expected}")
    return values


def _dominant_binding(family: Mapping[str, Any]) -> tuple[dict[str, Any] | None, float]:
    weighted: dict[str, tuple[dict[str, Any], int]] = {}
    total = 0
    for fine in family.get("fine_goal_options", []):
        if not isinstance(fine, Mapping):
            continue
        weight = int(fine.get("assigned_support", 0))
        total += weight
        binding = _normalise_binding(fine)
        if binding is None:
            continue
        key = _canonical(binding)
        old = weighted.get(key)
        weighted[key] = (binding, weight + (0 if old is None else old[1]))
    if not weighted or total == 0:
        return None, 0.0
    binding, count = max(weighted.values(), key=lambda row: (row[1], _canonical(row[0])))
    return binding, count / total


def build(
    families: Iterable[Mapping[str, Any]],
    assignments: Iterable[Mapping[str, Any]],
    transition_rows: Iterable[Mapping[str, Any]],
    *,
    min_parent_support: int = MIN_PARENT_SUPPORT,
    min_outcome_support: int = MIN_OUTCOME_SUPPORT,
    min_outcome_fold_support: int = MIN_OUTCOME_FOLD_SUPPORT,
    min_binding_share: float = MIN_BINDING_SHARE,
) -> dict[str, Any]:
    """Compile all sufficiently supported double-clear topology branches."""

    family_by_id = {
        str(family["goal_id"]): dict(family)
        for family in families
        if str(family.get("observed_template_kind")) == "DOUBLE_OR_MULTI_OPPONENT_REMOVAL"
    }
    relevant_assignments = [row for row in assignments if str(row.get("tactical_goal_id")) in family_by_id]
    wanted_panels = {str(row["panel_key"]) for row in relevant_assignments}
    transition_by_panel = {
        f"{row['end_id']}:{row['own_global_shot_number']}": row
        for row in transition_rows
        if f"{row['end_id']}:{row['own_global_shot_number']}" in wanted_panels
    }
    missing = wanted_panels - set(transition_by_panel)
    if missing:
        raise ValueError(f"missing match identity for {len(missing)} double-action assignment rows")

    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for row in relevant_assignments:
        grouped[(str(row["tactical_goal_id"]), str(row["post_own_topology"]))].append(row)

    contracts: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for parent_id, family in sorted(family_by_id.items()):
        parent_support = int(family.get("support", 0))
        if parent_support < min_parent_support:
            rejected.append({"tactical_goal_id": parent_id, "reason": "parent_support_below_gate"})
            continue
        binding, binding_share = _dominant_binding(family)
        if binding is None or binding_share < min_binding_share:
            rejected.append({"tactical_goal_id": parent_id, "reason": "no_dominant_dynamic_target_binding"})
            continue
        if int(binding.get("choose_count", 0)) != int(family.get("observed_opponent_removed_count", 0)):
            rejected.append({"tactical_goal_id": parent_id, "reason": "binding_count_disagrees_with_removal_count"})
            continue
        for (goal_id, topology), rows in grouped.items():
            if goal_id != parent_id:
                continue
            support = len(rows)
            if support < min_outcome_support:
                continue
            folds = Counter(fold_for_match(int(transition_by_panel[str(row["panel_key"])]["match_id"])) for row in rows)
            fold_support = [int(folds[fold]) for fold in range(FOLDS)]
            reply = Counter(str(row["after_opponent_reply_state"]) for row in rows)
            labels = [
                transition_by_panel[str(row["panel_key"])].get("terminal_end_label", {})
                for row in rows
            ]
            predicate = parse_post_own_topology(topology)
            digest = hashlib.sha256((parent_id + "|" + topology).encode("utf-8")).hexdigest()[:12]
            contracts.append({
                "schema": "nwnht_v2_double_outcome_goal_contract_v1",
                "double_goal_id": f"{parent_id}:double-outcome:{digest}",
                "tactical_goal_id": parent_id,
                "source_state": str(family["source_state"]),
                "parent_support": parent_support,
                "required_opponent_removed_count": int(family["observed_opponent_removed_count"]),
                "required_opponent_house_removed_count": int(family["observed_opponent_house_removed_count"]),
                "target_binding": binding,
                "anonymous_post_own_topology": topology,
                "terminal_board_predicate": predicate,
                "active_delivery_identity_status": "UNRESOLVED_FROM_ANONYMOUS_SAME_COLOUR_SNAPSHOTS",
                "outcome_support": support,
                "support_by_match_fold": fold_support,
                "minimum_fold_support": min(fold_support),
                "expected_after_opponent_reply_distribution": _distribution(reply),
                "observed_terminal_evidence": _terminal_evidence(
                    label for label in labels if isinstance(label, Mapping)
                ),
                "execution_status": (
                    "CROSS_FOLD_TOPOLOGY_CANDIDATE_REQUIRES_MULTI_TARGET_PHYSX"
                    if min(fold_support) >= min_outcome_fold_support
                    else "LOW_CROSS_FOLD_TOPOLOGY_SUPPORT"
                ),
                "warning": "Whole-board anonymous topology is the terminal requirement; it does not assert an unobserved active-stone identity or a fixed active-stone point.",
            })
    contracts.sort(key=lambda row: (row["source_state"], -row["outcome_support"], row["double_goal_id"]))
    rejected.sort(key=lambda row: row["tactical_goal_id"])
    return {
        "manifest": {
            "schema": "nwnht_v2_double_outcome_goal_contract_library_v2",
            "input_double_parent_count": len(family_by_id),
            "contract_count": len(contracts),
            "rejected_parent_count": len(rejected),
            "gates": {
                "min_parent_support": min_parent_support, "min_outcome_support": min_outcome_support,
                "min_outcome_fold_support": min_outcome_fold_support, "min_binding_share": min_binding_share,
            },
            "warning": "A double topology contract and its observed terminal evidence are not a parent action causal-value proof or a multi-target PhysX feasibility result.",
        },
        "contracts": contracts,
        "rejected_parents": rejected,
    }


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", type=Path, default=root / "nwnht_v2_tactical_action_families_v2.json")
    parser.add_argument("--assignments", type=Path, default=root / "nwnht_v2_tactical_action_assignments_v2.jsonl")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_board_effects_v2.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_double_outcome_goal_contracts_v2.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    payload = json.loads(args.families.read_text(encoding="utf-8"))
    result = build(payload["families"], _read_jsonl(args.assignments), _read_jsonl(args.transitions))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
