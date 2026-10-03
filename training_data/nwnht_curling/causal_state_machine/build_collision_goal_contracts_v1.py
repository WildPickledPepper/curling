#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile v2 removal actions into executable *collision goal contracts*.

This is deliberately below the parent tactical action layer.  A parent says
"remove one opponent house stone and roll to this tactical zone"; a contract
adds the only target identity that NWNHT can support at runtime: a geometric
role such as "closest opponent in the house".  It never invents a persistent
historical stone id.

The output is not a new policy and does not bypass cross-fold action ranking.
It is an execution contract available only when a selected v2 removal action
has a sufficiently dominant, dynamically bindable target-role specification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_runtime_state_plan_v1 import semantic_region
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_runtime_state_plan_v1 import semantic_region  # type: ignore


MIN_PARENT_SUPPORT = 30
MIN_BINDING_SHARE = 0.80


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _normalise_binding(fine: Mapping[str, Any]) -> dict[str, Any] | None:
    """Prefer dynamic house role binding; fall back to unambiguous selectors."""

    dynamic = fine.get("dynamic_house_removal_binding_request")
    if isinstance(dynamic, Mapping):
        if (
            str(dynamic.get("binding_kind")) == "OPPONENT_HOUSE_SET"
            and str(dynamic.get("owner")) == "opponent"
            and str(dynamic.get("source_region")) == "house"
            and str(dynamic.get("required_disposition")) == "OUT_OF_PLAY"
            and int(dynamic.get("choose_count", 0)) >= 1
        ):
            return {
                "binding_mode": "DYNAMIC_OPPONENT_HOUSE_SET",
                "owner": "opponent",
                "source_region": "house",
                "choose_count": int(dynamic["choose_count"]),
                "required_disposition": "OUT_OF_PLAY",
                "runtime_selection": "enumerate current opponent-house combinations; prioritise one containing closest-to-button opponent",
                "identity_note": "Historical same-colour IDs are unavailable; targets bind by current geometry only.",
            }
    selectors = fine.get("stone_constraints_when_unambiguous")
    if not isinstance(selectors, list) or not selectors:
        return None
    normalised: list[dict[str, Any]] = []
    for selector in selectors:
        if not isinstance(selector, Mapping):
            return None
        if str(selector.get("owner")) != "opponent" or str(selector.get("required_disposition")) != "OUT_OF_PLAY":
            return None
        if str(selector.get("source_region")) not in {"house", "visible"}:
            return None
        if str(selector.get("rank_by")) not in {"closest_to_button", "frontmost", "backmost", "leftmost", "rightmost"}:
            return None
        normalised.append({
            "owner": "opponent", "source_region": str(selector["source_region"]),
            "rank_by": str(selector["rank_by"]), "rank": int(selector["rank"]),
            "required_disposition": "OUT_OF_PLAY",
        })
    return {
        "binding_mode": "UNAMBIGUOUS_SELECTOR_SET",
        "selectors": sorted(normalised, key=_canonical),
        "choose_count": len(normalised),
        "identity_note": "Selectors bind by current geometry, not historical stone IDs.",
    }


def _contract_id(parent_id: str, binding: Mapping[str, Any]) -> str:
    digest = hashlib.sha256((parent_id + "|" + _canonical(binding)).encode("utf-8")).hexdigest()[:12]
    return f"{parent_id}:collision:{digest}"


def build(
    families: Iterable[Mapping[str, Any]],
    *,
    min_parent_support: int = MIN_PARENT_SUPPORT,
    min_binding_share: float = MIN_BINDING_SHARE,
) -> dict[str, Any]:
    """Return contracts plus a transparent rejection audit."""

    if min_parent_support < 1 or not 0.0 < float(min_binding_share) <= 1.0:
        raise ValueError("invalid support or binding-share threshold")
    contracts: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    removal_parent_count = 0
    for family in families:
        kind = str(family.get("observed_template_kind"))
        if kind not in {"SINGLE_OPPONENT_REMOVAL", "DOUBLE_OR_MULTI_OPPONENT_REMOVAL"}:
            continue
        removal_parent_count += 1
        parent_id = str(family["goal_id"])
        support = int(family.get("support", 0))
        if support < min_parent_support:
            rejected.append({"tactical_goal_id": parent_id, "reason": "parent_support_below_gate", "parent_support": support})
            continue
        region = semantic_region(str(family.get("tactical_target_zone")))
        if region is None:
            rejected.append({"tactical_goal_id": parent_id, "reason": "no_executable_active_target_region", "target_zone": family.get("tactical_target_zone")})
            continue
        weighted: dict[str, dict[str, Any]] = defaultdict(lambda: {"support": 0, "fine_goal_ids": []})
        represented_support = 0
        for fine in family.get("fine_goal_options", []):
            if not isinstance(fine, Mapping):
                continue
            weight = int(fine.get("assigned_support", 0))
            represented_support += weight
            binding = _normalise_binding(fine)
            if binding is None:
                continue
            key = _canonical(binding)
            weighted[key]["support"] += weight
            weighted[key]["binding"] = binding
            weighted[key]["fine_goal_ids"].append(str(fine.get("goal_id")))
        if not weighted:
            rejected.append({"tactical_goal_id": parent_id, "reason": "no_bindable_fine_goal"})
            continue
        _, winner = max(weighted.items(), key=lambda item: (int(item[1]["support"]), item[0]))
        binding_support = int(winner["support"])
        binding_share = 0.0 if represented_support == 0 else binding_support / represented_support
        if binding_share < min_binding_share:
            rejected.append({
                "tactical_goal_id": parent_id, "reason": "binding_not_dominant_in_retained_fine_goals",
                "binding_share": round(binding_share, 6), "represented_fine_support": represented_support,
            })
            continue
        binding = dict(winner["binding"])
        expected_removed = int(family.get("observed_opponent_removed_count", 0))
        if int(binding["choose_count"]) != expected_removed:
            rejected.append({
                "tactical_goal_id": parent_id, "reason": "binding_count_disagrees_with_parent_removal_count",
                "binding_count": int(binding["choose_count"]), "parent_removed_count": expected_removed,
            })
            continue
        contracts.append({
            "schema": "nwnht_v2_collision_goal_contract_v1",
            "collision_goal_id": _contract_id(parent_id, binding),
            "tactical_goal_id": parent_id,
            "source_state": str(family["source_state"]),
            "observed_template_kind": kind,
            "parent_support": support,
            "required_opponent_removed_count": expected_removed,
            "required_opponent_house_removed_count": int(family.get("observed_opponent_house_removed_count", 0)),
            "target_binding": binding,
            "active_target_region": region,
            "expected_next_state_distribution": family.get("after_opponent_reply_state_distribution", []),
            "binding_support_in_retained_fine_goals": binding_support,
            "represented_fine_support": represented_support,
            "binding_share_in_retained_fine_goals": round(binding_share, 6),
            "fine_goal_examples": sorted(winner["fine_goal_ids"])[:5],
            "execution_status": "REQUIRES_PARENT_ACTION_VALUE_GATE_AND_STRICT_PHYSX",
            "warning": "This is a target-role/terminal-region contract, not a proof that the parent action is cross-fold stable, physically reachable, or winning.",
        })
    contracts.sort(key=lambda row: (row["source_state"], row["tactical_goal_id"], row["collision_goal_id"]))
    rejected.sort(key=lambda row: (str(row["reason"]), str(row["tactical_goal_id"])))
    return {
        "manifest": {
            "schema": "nwnht_v2_collision_goal_contract_library_v1",
            "input_removal_parent_count": removal_parent_count,
            "contract_count": len(contracts),
            "rejected_parent_count": len(rejected),
            "gates": {"min_parent_support": min_parent_support, "min_binding_share": min_binding_share},
            "warning": "Contracts compile only target semantics. Runtime use still requires cross-fold action selection, local FGZ checks, strict PhysX and K8 reply search.",
        },
        "contracts": contracts,
        "rejected_parents": rejected,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", type=Path, default=root / "nwnht_v2_tactical_action_families_v2.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_collision_goal_contracts_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    families = json.loads(args.families.read_text(encoding="utf-8"))["families"]
    result = build(families)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
