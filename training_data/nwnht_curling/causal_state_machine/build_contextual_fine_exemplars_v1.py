#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export pre-shot geometry exemplars for selected semantic G_k targets.

The universal MDP selects *what* G to pursue.  This exporter retains the
historical B_k -> U_k implementations of that selected G so a runtime
retriever can choose a fine endpoint conditional on the current exact board.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_universal_semantic_goal_mdp_v1 import _goal_id, _semantic_key
    from .state_features_v2 import canonicalise_left_right
except ImportError:  # pragma: no cover
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_universal_semantic_goal_mdp_v1 import _goal_id, _semantic_key  # type: ignore
    from causal_state_machine.state_features_v2 import canonicalise_left_right  # type: ignore


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def build(plan: Mapping[str, Any], templates: Iterable[Mapping[str, Any]], transitions: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    by_panel = {f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transitions}
    selected = {
        str(row["state_id"]): str(row["primary_goal"]["goal_id"])
        for row in plan["state_plans"] if row.get("primary_goal") is not None
    }
    examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in templates:
        state = str(raw["source_state"])
        goal_id = _goal_id(state, _semantic_key(raw))
        if selected.get(state) != goal_id:
            continue
        transition = by_panel.get(str(raw["panel_key"]))
        if transition is None:
            raise ValueError(f"missing transition {raw['panel_key']}")
        canonical_before, _ = canonicalise_left_right(transition["s_before_own"])
        examples[goal_id].append({
            "panel_key": str(raw["panel_key"]),
            "match_id": int(transition["match_id"]),
            "source_state": state,
            "K": int(raw["K"]),
            "before_board_canonical": canonical_before,
            "active_final_point_canonical": raw.get("active_final_point"),
            "precision": str(raw["precision"]),
            "stone_constraints_when_unambiguous": raw.get("stone_constraints_when_unambiguous", []),
            "dynamic_house_removal_binding_request": raw.get("dynamic_house_removal_binding_request"),
            "after_own_occupancy": raw.get("after_own_occupancy", {}),
            "post_own_topology": str(raw["post_own_topology"]),
        })
    for group in examples.values():
        group.sort(key=lambda row: (int(row["match_id"]), str(row["panel_key"])))
    summary = {
        "selected_goal_count": len(selected),
        "goal_with_exemplars": len(examples),
        "exemplar_count": sum(len(group) for group in examples.values()),
        "active_endpoint_exemplar_count": sum(1 for group in examples.values() for row in group if row["active_final_point_canonical"] is not None),
    }
    return {
        "manifest": {
            "schema": "nwnht_v2_contextual_fine_exemplars_v1",
            "purpose": "Same (S_k, selected G_k) historical pre-shot geometry and fine-result exemplars for nearest-neighbour endpoint retrieval.",
            "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES_CANONICAL_LEFT_RIGHT",
            "prohibition": "Exemplars must be match-held-out during offline validation. They do not prove causal effects or physical reachability.",
            **summary,
        },
        "examples_by_goal_id": dict(sorted(examples.items())),
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=root / "nwnht_v2_universal_semantic_goal_mdp_v2.json")
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_contextual_fine_exemplars_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    result = build(json.loads(args.plan.read_text(encoding="utf-8")), _read_jsonl(args.templates), _read_jsonl(args.transitions))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
