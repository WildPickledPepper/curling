#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replay-check selected semantic G contracts against their observed S->U rows.

This validates the data-to-contract compiler, not counterfactual tactical
quality or PhysX reachability.  Only records whose observed semantic result
equals the MDP's selected primary G for their source S are evaluated.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

# Direct script invocation puts only this directory on sys.path; the contract
# module intentionally lives in the separate tactical package.
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .build_universal_semantic_goal_mdp_v1 import _goal_id, _semantic_key
except ImportError:  # pragma: no cover
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_universal_semantic_goal_mdp_v1 import _goal_id, _semantic_key  # type: ignore

from planning_proxy.tactical_library_strategy.semantic_goal_contract import instantiate_goal_contracts, semantic_transition_met


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _point_covered(point: Mapping[str, Any], contracts: Iterable[Mapping[str, Any]]) -> bool:
    for contract in contracts:
        region = contract.get("active_final_region")
        if not isinstance(region, Mapping):
            continue
        if math.hypot(float(point["x_m"]) - float(region["centre_x_m"]), float(point["y_m"]) - float(region["centre_y_m"])) <= float(region["radius_m"]):
            return True
    return False


def audit(plan: Mapping[str, Any], templates: Iterable[Mapping[str, Any]], transitions: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    transition_by_panel = {f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transitions}
    primary = {str(row["state_id"]): dict(row["primary_goal"]) for row in plan["state_plans"] if row.get("primary_goal")}
    stats: dict[str, Counter[str]] = defaultdict(Counter)
    for raw in templates:
        state = str(raw["source_state"])
        selected = primary.get(state)
        if selected is None or str(selected["goal_id"]) != _goal_id(state, _semantic_key(raw)):
            continue
        source = transition_by_panel.get(str(raw["panel_key"]))
        if source is None:
            raise ValueError(f"missing transition {raw['panel_key']}")
        bound = instantiate_goal_contracts(source["s_before_own"], selected)
        stats[state]["matched_primary_goal_rows"] += 1
        if semantic_transition_met(source["s_before_own"], source["u_after_own"], bound):
            stats[state]["semantic_accept_rows"] += 1
        if bound["contract_status"] == "CONTRACT_READY_FOR_PATH_SEARCH":
            stats[state]["contract_ready_rows"] += 1
        point = raw.get("active_final_point")
        if point is not None:
            stats[state]["observed_active_endpoint_rows"] += 1
            if _point_covered(point, bound["contracts"]):
                stats[state]["active_endpoint_covered_rows"] += 1
    rows = []
    for state in sorted(primary):
        item = stats[state]
        matched = int(item["matched_primary_goal_rows"])
        if not matched:
            raise ValueError(f"selected primary G has no replay rows: {state}")
        rows.append({
            "state_id": state,
            "matched_primary_goal_rows": matched,
            "semantic_accept_rows": int(item["semantic_accept_rows"]),
            "semantic_accept_rate": round(item["semantic_accept_rows"] / matched, 6),
            "contract_ready_rows": int(item["contract_ready_rows"]),
            "contract_ready_rate": round(item["contract_ready_rows"] / matched, 6),
            "observed_active_endpoint_rows": int(item["observed_active_endpoint_rows"]),
            "active_endpoint_covered_rows": int(item["active_endpoint_covered_rows"]),
            "active_endpoint_coverage": None if not item["observed_active_endpoint_rows"] else round(item["active_endpoint_covered_rows"] / item["observed_active_endpoint_rows"], 6),
        })
    total = Counter()
    for row in rows:
        total["matched_primary_goal_rows"] += row["matched_primary_goal_rows"]
        total["semantic_accept_rows"] += row["semantic_accept_rows"]
        total["contract_ready_rows"] += row["contract_ready_rows"]
        total["observed_active_endpoint_rows"] += row["observed_active_endpoint_rows"]
        total["active_endpoint_covered_rows"] += row["active_endpoint_covered_rows"]
    return {
        "manifest": {
            "schema": "nwnht_v2_semantic_goal_contract_replay_audit_v1",
            "scope": "Observed rows that realise each source state's selected full-data primary semantic G.",
            "prohibition": "Replay acceptance checks compiler consistency only; it is not causal validation or PhysX reachability.",
        },
        "summary": {
            **dict(total),
            "semantic_accept_rate": round(total["semantic_accept_rows"] / total["matched_primary_goal_rows"], 6),
            "contract_ready_rate": round(total["contract_ready_rows"] / total["matched_primary_goal_rows"], 6),
            "active_endpoint_coverage": None if not total["observed_active_endpoint_rows"] else round(total["active_endpoint_covered_rows"] / total["observed_active_endpoint_rows"], 6),
        },
        "states": rows,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=root / "nwnht_v2_universal_semantic_goal_mdp_v2.json")
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_semantic_goal_contract_replay_audit_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    result = audit(
        json.loads(args.plan.read_text(encoding="utf-8")), _read_jsonl(args.templates), _read_jsonl(args.transitions),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
