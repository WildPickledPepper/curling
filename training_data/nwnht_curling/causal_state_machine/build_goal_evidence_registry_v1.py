#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge direct GoalState evidence with conditional same-K template evidence.

This is deliberately an *evidence registry*, not a new value estimator.  A
direct, cross-fold GoalState remains the only executable record because it
contains both a terminal-board predicate and retained fine endpoint/binding
options.  A conditional template can complement a state only when it passes
its independent five-fold audit, and is explicitly marked pending until a
separate compiler derives fine constraints.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping


DIRECT = "EMPIRICAL_GOAL_OUTCOME_CONSENSUS"
CONDITIONAL = "CONDITIONAL_TEMPLATE_CONSENSUS_WITH_DIRECT_HOLDOUT_EVIDENCE"


def _by_state(artifact: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in artifact["state_plans"]:
        state = str(row["state_id"])
        if state in result:
            raise ValueError(f"duplicate state in artifact: {state}")
        result[state] = dict(row)
    return result


def build(direct_artifact: Mapping[str, Any], conditional_artifact: Mapping[str, Any]) -> dict[str, Any]:
    """Give each S exactly one highest-evidence status without cross-K reuse."""

    direct = _by_state(direct_artifact)
    conditional = _by_state(conditional_artifact)
    if set(direct) != set(conditional):
        raise ValueError("direct and conditional artifacts must cover the same states")

    plans: list[dict[str, Any]] = []
    for state in sorted(direct, key=lambda name: (int(direct[name]["K"]), name)):
        exact = direct[state]
        semantic = conditional[state]
        k = int(exact["K"])
        if int(semantic["K"]) != k:
            raise ValueError(f"K mismatch for {state}")

        if exact.get("recommendation_status") == DIRECT:
            plans.append({
                "state_id": state,
                "K": k,
                "recommendation_status": "DIRECT_FINE_GOAL_CONSENSUS",
                "primary_goal": exact.get("primary_goal"),
                "conditional_template_audit": semantic.get("primary_goal"),
                "execution_status": "EXECUTABLE_GOAL_CONSTRAINT_CANDIDATE",
                "warning": "Historical cross-fold evidence, not a causal or PhysX reachability proof.",
            })
            continue

        if semantic.get("recommendation_status") == CONDITIONAL:
            primary = semantic.get("primary_goal")
            if not isinstance(primary, Mapping) or int(primary["goal_template"]["K"]) != k:
                raise ValueError(f"conditional template does not preserve K for {state}")
            plans.append({
                "state_id": state,
                "K": k,
                "recommendation_status": "CONDITIONAL_SEMANTIC_GOAL_CONSENSUS_PENDING_FINE_COMPILATION",
                "primary_goal": dict(primary),
                "execution_status": "NOT_RUNTIME_EXECUTABLE_NO_FINE_ENDPOINT_OR_BINDING",
                "warning": "This shared same-K semantic target has independent five-fold and direct-heldout support, but has no source-specific fine endpoint/binding constraint yet.",
            })
            continue

        plans.append({
            "state_id": state,
            "K": k,
            "recommendation_status": "SEARCH_REQUIRED_NO_HIGH_CONFIDENCE_GOAL",
            "primary_goal": None,
            "execution_status": "NO_GOAL_TO_SEND_TO_SOLVER",
        })

    counts = Counter(str(row["recommendation_status"]) for row in plans)
    return {
        "manifest": {
            "schema": "nwnht_v2_goal_evidence_registry_v1",
            "purpose": "Prefer exact direct GoalStates; retain only independently audited same-K semantic complements.",
            "priority": ["DIRECT_FINE_GOAL_CONSENSUS", "CONDITIONAL_SEMANTIC_GOAL_CONSENSUS_PENDING_FINE_COMPILATION", "SEARCH_REQUIRED_NO_HIGH_CONFIDENCE_GOAL"],
            "prohibition": "Conditional semantic entries must not be passed to a path solver until source-specific fine endpoint/binding constraints are compiled and separately checked.",
        },
        "summary": dict(counts),
        "state_plans": plans,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--direct", type=Path, default=root / "nwnht_v2_tactical_goal_outcome_value_v1.json")
    parser.add_argument("--conditional", type=Path, default=root / "nwnht_v2_conditional_same_k_goal_audit_v1.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_goal_evidence_registry_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    result = build(
        json.loads(args.direct.read_text(encoding="utf-8")),
        json.loads(args.conditional.read_text(encoding="utf-8")),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
