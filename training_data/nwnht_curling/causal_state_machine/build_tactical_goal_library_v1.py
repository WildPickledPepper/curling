#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the action layer A between v2 board states and fine GoalStates.

The v2 library deliberately stores narrow endpoint constraints (roughly
0.20 m grid cells).  Those are appropriate instructions for a later inverse
planner, but treating every cell as an independent tactical action produces a
thin and unstable action space.  This module builds a *parent tactical goal*:

    S_k -> A_k (structural result + semantic target zone) -> fine GoalState(s)

It does not merge board states and it does not widen a fine GoalState.  A
parent keeps its original narrow child GoalStates as ordered execution options.
The parent is what the finite-horizon value model ranks; a child is what the
future local-rule/PhysX executor will try to realise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_goal_library_v2 import _goal_id, _signature
    from .extract_anonymous_goal_templates import zone_of
    from .state_features_v2 import GUARD_NEAR_FAR_SPLIT_M
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_goal_library_v2 import _goal_id, _signature  # type: ignore
    from causal_state_machine.extract_anonymous_goal_templates import zone_of  # type: ignore
    from causal_state_machine.state_features_v2 import GUARD_NEAR_FAR_SPLIT_M  # type: ignore


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def tactical_target_zone(point: Mapping[str, Any] | None) -> str:
    """Semantic action-zone, deliberately coarser than a 0.20 m child cell."""

    if point is None:
        return "NO_ACTIVE_FINAL_POINT"
    base = zone_of(dict(point))
    if base == "centre_guard":
        return "CENTRE_GUARD_NEAR" if float(point["y_m"]) <= GUARD_NEAR_FAR_SPLIT_M else "CENTRE_GUARD_FAR"
    if base == "wing_guard_left":
        return "WING_GUARD_NEAR_LEFT" if float(point["y_m"]) <= GUARD_NEAR_FAR_SPLIT_M else "WING_GUARD_FAR_LEFT"
    if base == "wing_guard_right":
        return "WING_GUARD_NEAR_RIGHT" if float(point["y_m"]) <= GUARD_NEAR_FAR_SPLIT_M else "WING_GUARD_FAR_RIGHT"
    return base.upper()


def _parent_signature(template: Mapping[str, Any]) -> tuple[Any, ...]:
    """Keep collision/removal/occupancy semantics; replace only fine grid cell."""

    delta = template["observed_delta"]
    return (
        str(template["source_state"]), str(template["observed_template_kind"]), str(template["precision"]),
        int(delta["opponent_removed_count"]), int(delta["opponent_house_removed_count"]),
        _canonical(template["stone_constraints_when_unambiguous"]),
        _canonical(template["dynamic_house_removal_binding_request"]),
        _canonical(template["after_own_occupancy"]), tactical_target_zone(template.get("active_final_point")),
    )


def _parent_id(signature: tuple[Any, ...]) -> str:
    return "nwnht_v2_tactical_goal_" + hashlib.sha256(repr(signature).encode("utf-8")).hexdigest()[:16]


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [
        {"value": value, "count": count, "share": round(count / total, 6)}
        for value, count in counter.most_common()
    ] if total else []


def _fine_option(goal: Mapping[str, Any], assigned_support: int) -> dict[str, Any]:
    """Exact terminal constraints retained below the tactical action layer."""

    return {
        "goal_id": str(goal["goal_id"]),
        "assigned_support": assigned_support,
        "observed_template_kind": goal["observed_template_kind"],
        "precision": goal["precision"],
        "active_final_region": goal["active_final_region"],
        "stone_constraints_when_unambiguous": goal["stone_constraints_when_unambiguous"],
        "dynamic_house_removal_binding_request": goal["dynamic_house_removal_binding_request"],
        "after_own_occupancy": goal["after_own_occupancy"],
    }


def build(
    templates: Iterable[Mapping[str, Any]],
    fine_goals: Iterable[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Return parent action families and one compact assignment per observation."""

    child_by_id = {
        str(goal["goal_id"]): dict(goal)
        for goal in fine_goals
        if bool(goal.get("runtime_goal_candidate"))
    }
    grouped: dict[tuple[Any, ...], dict[str, Any]] = defaultdict(lambda: {
        "count": 0, "children": Counter(), "post": Counter(), "reply": Counter(), "examples": [],
    })
    assignments: list[dict[str, Any]] = []
    candidate_template_rows = 0
    for template in templates:
        child_id = _goal_id(_signature(template))
        if child_id not in child_by_id:
            continue
        candidate_template_rows += 1
        signature = _parent_signature(template)
        parent_id = _parent_id(signature)
        item = grouped[signature]
        item["count"] += 1
        item["children"][child_id] += 1
        item["post"][str(template["post_own_topology"])] += 1
        item["reply"][str(template["after_opponent_reply_state"])] += 1
        if len(item["examples"]) < 5:
            item["examples"].append(str(template["panel_key"]))
        assignments.append({
            "schema": "nwnht_v2_tactical_goal_assignment_v1",
            "panel_key": str(template["panel_key"]),
            "K": int(template["K"]),
            "source_state": str(template["source_state"]),
            "tactical_goal_id": parent_id,
            "fine_goal_id": child_id,
            "post_own_topology": str(template["post_own_topology"]),
            "after_opponent_reply_state": str(template["after_opponent_reply_state"]),
        })
    if not assignments:
        raise ValueError("no v2 runtime candidate templates were assigned to a tactical action")

    parents: list[dict[str, Any]] = []
    for signature, item in grouped.items():
        (
            source_state, kind, precision, removed, house_removed,
            selectors_json, binding_json, occupancy_json, target_zone,
        ) = signature
        child_options = [
            _fine_option(child_by_id[child_id], support)
            for child_id, support in item["children"].most_common()
        ]
        parents.append({
            "schema": "nwnht_v2_tactical_goal_family_v1",
            "goal_id": _parent_id(signature),
            "source_state": source_state,
            "observed_template_kind": kind,
            "precision": precision,
            "tactical_target_zone": target_zone,
            "observed_opponent_removed_count": removed,
            "observed_opponent_house_removed_count": house_removed,
            "stone_constraints_when_unambiguous": json.loads(selectors_json),
            "dynamic_house_removal_binding_request": json.loads(binding_json),
            "after_own_occupancy": json.loads(occupancy_json),
            "active_final_region": None,
            "fine_goal_options": child_options,
            "support": item["count"],
            "fine_goal_count": len(child_options),
            "post_own_topology_distribution": _distribution(item["post"]),
            "after_opponent_reply_state_distribution": _distribution(item["reply"]),
            "runtime_goal_candidate": True,
            "examples": item["examples"],
            "evidence_status": "HIERARCHICAL_EMPIRICAL_TACTICAL_ACTION",
            "warning": "This parent is a tactical action category, not a widened physical target. Execute only one listed fine_goal_option after later value ranking and local-rule/PhysX screening.",
        })
    parents.sort(key=lambda row: (str(row["source_state"]), -int(row["support"]), str(row["goal_id"])))
    assignments.sort(key=lambda row: (str(row["source_state"]), str(row["tactical_goal_id"]), str(row["panel_key"])))
    manifest = {
        "schema": "nwnht_v2_tactical_goal_library_manifest_v1",
        "purpose": "Hierarchical action layer: rank parent tactical actions while retaining narrow GoalState children for execution.",
        "input_runtime_fine_goal_count": len(child_by_id),
        "candidate_template_rows": candidate_template_rows,
        "tactical_action_count": len(parents),
        "action_zone_rule": "Existing semantic zones; guards retain the existing near/far split rather than an arbitrary new distance boundary.",
        "warning": "Parents are historical action abstractions. They are not causal guarantees and do not replace local rule or PhysX validation.",
    }
    return parents, assignments, manifest


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--fine-goals", type=Path, default=root / "nwnht_v2_goal_template_families_v0.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_tactical_goal_families_v1.json")
    parser.add_argument("--assignments", type=Path, default=root / "nwnht_v2_tactical_goal_assignments_v1.jsonl")
    args = parser.parse_args()
    if args.output.exists() or args.assignments.exists():
        raise SystemExit("Refusing to overwrite tactical goal artifacts; choose new output paths.")
    parents, assignments, manifest = build(_read_jsonl(args.templates), json.loads(args.fine_goals.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"manifest": manifest, "families": parents}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with args.assignments.open("w", encoding="utf-8") as handle:
        for row in assignments:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "assignments": str(args.assignments), **manifest}, ensure_ascii=False))


if __name__ == "__main__":
    main()
