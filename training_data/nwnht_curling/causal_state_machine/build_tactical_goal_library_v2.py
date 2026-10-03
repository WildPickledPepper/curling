#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build v2 tactical actions before fine-grid support is applied.

``v1`` could only merge the 112 fine GoalStates that had already passed a
per-grid-cell support gate.  This leaves many well-observed board states with
no action at all.  ``v2`` moves that support gate to the parent action layer:

* ``A`` records the state-conditioned tactical result type: placement/removal,
  removal cardinality, and semantic target zone;
* ``G`` keeps the narrow point, exact occupancy, and any dynamic stone binding.

Thus a collision's incidental exact occupancy does not fragment ``A``.  It is
still retained in every ``G`` child and is never silently discarded at
execution time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_goal_library_v2 import _active_region, _distribution, _goal_id, _signature
    from .build_tactical_goal_library_v1 import tactical_target_zone
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_goal_library_v2 import _active_region, _distribution, _goal_id, _signature  # type: ignore
    from causal_state_machine.build_tactical_goal_library_v1 import tactical_target_zone  # type: ignore


MIN_PARENT_ACTION_SUPPORT = 30
MAX_FINE_OPTIONS_PER_PARENT = 100


def _parent_id(signature: tuple[Any, ...]) -> str:
    return "nwnht_v2_tactical_action_" + hashlib.sha256(repr(signature).encode("utf-8")).hexdigest()[:16]


def _parent_signature(template: Mapping[str, Any]) -> tuple[Any, ...]:
    """Action semantics only; exact endpoint/binding belongs to fine child G."""

    delta = template["observed_delta"]
    return (
        str(template["source_state"]),
        str(template["observed_template_kind"]),
        int(delta["opponent_removed_count"]),
        int(delta["opponent_house_removed_count"]),
        tactical_target_zone(template.get("active_final_point")),
    )


def _is_expressible(template: Mapping[str, Any]) -> bool:
    return (
        str(template["source_state_status"]) == "DATA_SUPPORTED_STATE"
        and str(template["precision"]) == "ROLE_AND_REGION"
        and (
            template.get("active_final_point") is not None
            or bool(template["stone_constraints_when_unambiguous"])
            or template.get("dynamic_house_removal_binding_request") is not None
        )
    )


def _fine_payload(template: Mapping[str, Any], item: Mapping[str, Any]) -> dict[str, Any]:
    point_rows = item["points"]
    return {
        "goal_id": _goal_id(_signature(template)),
        "assigned_support": int(item["count"]),
        "observed_template_kind": template["observed_template_kind"],
        "precision": template["precision"],
        "active_final_region": _active_region(point_rows),
        "stone_constraints_when_unambiguous": template["stone_constraints_when_unambiguous"],
        "dynamic_house_removal_binding_request": template["dynamic_house_removal_binding_request"],
        "after_own_occupancy": template["after_own_occupancy"],
        "post_own_topology_distribution": _distribution(item["post"]),
        "examples": item["examples"],
    }


def build(
    templates: Iterable[Mapping[str, Any]],
    *,
    min_parent_action_support: int = MIN_PARENT_ACTION_SUPPORT,
    max_fine_options_per_parent: int = MAX_FINE_OPTIONS_PER_PARENT,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[Any, ...], dict[str, Any]] = defaultdict(lambda: {
        "count": 0, "post": Counter(), "reply": Counter(), "examples": [], "fine": {},
    })
    input_rows = expressible_rows = 0
    for template in templates:
        input_rows += 1
        if not _is_expressible(template):
            continue
        expressible_rows += 1
        signature = _parent_signature(template)
        parent_id = _parent_id(signature)
        group = groups[signature]
        group["count"] += 1
        group["post"][str(template["post_own_topology"])] += 1
        group["reply"][str(template["after_opponent_reply_state"])] += 1
        if len(group["examples"]) < 5:
            group["examples"].append(str(template["panel_key"]))
        fine_id = _goal_id(_signature(template))
        fine = group["fine"].setdefault(fine_id, {
            "template": dict(template), "count": 0, "points": [], "post": Counter(), "examples": [], "rows": [],
        })
        fine["count"] += 1
        point = template.get("active_final_point")
        if point is not None:
            fine["points"].append((float(point["x_m"]), float(point["y_m"])))
        fine["post"][str(template["post_own_topology"])] += 1
        if len(fine["examples"]) < 5:
            fine["examples"].append(str(template["panel_key"]))
        fine["rows"].append((
            str(template["panel_key"]), str(template["post_own_topology"]), str(template["after_opponent_reply_state"]),
        ))

    admitted = {signature for signature, item in groups.items() if int(item["count"]) >= min_parent_action_support}
    parents: list[dict[str, Any]] = []
    assignments: list[dict[str, Any]] = []
    for signature in admitted:
        source_state, kind, removed, house_removed, target_zone = signature
        item = groups[signature]
        fine_options = [
            _fine_payload(fine["template"], fine)
            for fine in item["fine"].values()
        ]
        fine_options.sort(key=lambda row: (-int(row["assigned_support"]), str(row["goal_id"])))
        retained_fine = fine_options[:max_fine_options_per_parent]
        retained_ids = {str(row["goal_id"]) for row in retained_fine}
        parent_id = _parent_id(signature)
        parents.append({
            "schema": "nwnht_v2_tactical_action_family_v2",
            "goal_id": parent_id,
            "source_state": source_state,
            "observed_template_kind": kind,
            "precision": "PARENT_ACTION_WITH_FINE_CHILDREN",
            "tactical_target_zone": target_zone,
            "observed_opponent_removed_count": removed,
            "observed_opponent_house_removed_count": house_removed,
            "stone_constraints_when_unambiguous": [],
            "dynamic_house_removal_binding_request": None,
            "after_own_occupancy": {"first": {}, "opponent": {}},
            "active_final_region": None,
            "fine_goal_options": retained_fine,
            "fine_goal_count_all": len(fine_options),
            "fine_goal_count_retained": len(retained_fine),
            "support": int(item["count"]),
            "post_own_topology_distribution": _distribution(item["post"]),
            "after_opponent_reply_state_distribution": _distribution(item["reply"]),
            "runtime_goal_candidate": True,
            "examples": item["examples"],
            "evidence_status": "HIERARCHICAL_ACTION_BEFORE_FINE_GRID_GATE",
            "warning": "Parent action deliberately omits exact binding and occupancy. The later executor must choose one retained fine_goal_option; parent action alone is never a physical target.",
        })
        # Keep all admitted rows for action-value estimation, even if their
        # particular fine child fell below the retained top-N list.  The action
        # transition is defined by all its observed realisations.
        for fine in item["fine"].values():
            template = fine["template"]
            for panel_key, post, reply in fine.get("rows", []):
                assignments.append({
                    "schema": "nwnht_v2_tactical_action_assignment_v2",
                    "panel_key": panel_key,
                    "K": int(template["K"]),
                    "source_state": source_state,
                    "tactical_goal_id": parent_id,
                    "fine_goal_id": _goal_id(_signature(template)),
                    "fine_goal_retained": _goal_id(_signature(template)) in retained_ids,
                    "post_own_topology": post,
                    "after_opponent_reply_state": reply,
                })

    parents.sort(key=lambda row: (str(row["source_state"]), -int(row["support"]), str(row["goal_id"])))
    assignments.sort(key=lambda row: (str(row["source_state"]), str(row["tactical_goal_id"]), str(row["panel_key"])))
    manifest = {
        "schema": "nwnht_v2_tactical_action_library_manifest_v2",
        "input_template_rows": input_rows,
        "expressible_template_rows_before_fine_grid_gate": expressible_rows,
        "parent_action_count": len(parents),
        "assignment_rows": len(assignments),
        "gates": {"min_parent_action_support": min_parent_action_support, "max_fine_options_per_parent": max_fine_options_per_parent},
        "warning": "Action support is deliberately assessed before fine-grid support. Exact endpoint/binding requirements stay in child GoalStates and require their own cross-fold screen.",
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
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_tactical_action_families_v2.json")
    parser.add_argument("--assignments", type=Path, default=root / "nwnht_v2_tactical_action_assignments_v2.jsonl")
    args = parser.parse_args()
    if args.output.exists() or args.assignments.exists():
        raise SystemExit("Refusing to overwrite tactical v2 artifacts; choose new output paths.")
    rows = list(_read_jsonl(args.templates))
    parents, assignments, manifest = build(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"manifest": manifest, "families": parents}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with args.assignments.open("w", encoding="utf-8") as handle:
        for row in assignments:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "assignments": str(args.assignments), **manifest}, ensure_ascii=False))


if __name__ == "__main__":
    main()
