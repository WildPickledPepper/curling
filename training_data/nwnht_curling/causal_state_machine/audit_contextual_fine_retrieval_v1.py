#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Match-held-out audit for same-(S,G) nearest-geometry fine endpoint retrieval."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .build_universal_semantic_goal_mdp_v1 import _goal_id, _semantic_key
    from .state_features_v2 import canonicalise_left_right
except ImportError:  # pragma: no cover
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_universal_semantic_goal_mdp_v1 import _goal_id, _semantic_key  # type: ignore
    from causal_state_machine.state_features_v2 import canonicalise_left_right  # type: ignore

from planning_proxy.tactical_library_strategy.contextual_fine_retriever import ContextualFineRetriever


MAX_EVALUATION_MATCHES_PER_STATE = 50


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _covered(point: Mapping[str, Any], regions: Iterable[Mapping[str, Any]]) -> bool:
    return any(math.hypot(float(point["x_m"]) - float(region["active_final_region"]["centre_x_m"]), float(point["y_m"]) - float(region["active_final_region"]["centre_y_m"])) <= float(region["active_final_region"]["radius_m"]) for region in regions)


def audit(plan: Mapping[str, Any], retriever: ContextualFineRetriever, templates: Iterable[Mapping[str, Any]], transitions: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    transition_by_panel = {f"{row['end_id']}:{row['own_global_shot_number']}": row for row in transitions}
    primary = {str(row["state_id"]): dict(row["primary_goal"]) for row in plan["state_plans"] if row.get("primary_goal")}
    selected: dict[str, list[tuple[Mapping[str, Any], Mapping[str, Any]]]] = defaultdict(list)
    seen_matches: dict[str, set[int]] = defaultdict(set)
    for raw in templates:
        if raw.get("active_final_point") is None:
            continue
        state = str(raw["source_state"])
        candidate = primary.get(state)
        if candidate is None or str(candidate["goal_id"]) != _goal_id(state, _semantic_key(raw)):
            continue
        source = transition_by_panel.get(str(raw["panel_key"]))
        if source is None:
            raise ValueError(f"missing transition {raw['panel_key']}")
        match_id = int(source["match_id"])
        if match_id in seen_matches[state] or len(seen_matches[state]) >= MAX_EVALUATION_MATCHES_PER_STATE:
            continue
        seen_matches[state].add(match_id)
        selected[state].append((raw, source))
    output, total = [], Counter()
    for state, rows in sorted(selected.items()):
        stats = Counter()
        candidate = primary[state]
        for raw, source in rows:
            canonical_before, _ = canonicalise_left_right(source["s_before_own"])
            result = retriever.retrieve(canonical_before, candidate, exclude_match_id=int(source["match_id"]))
            stats["evaluated"] += 1
            if result["regions"]:
                stats["regions_available"] += 1
            if _covered(raw["active_final_point"], result["regions"]):
                stats["covered"] += 1
            static_regions = [
                {"active_final_region": option["active_final_region"]}
                for option in candidate["goal_state"].get("fine_goal_options", [])
                if option.get("active_final_region") is not None
            ]
            if _covered(raw["active_final_point"], static_regions):
                stats["static_global_covered"] += 1
        total.update(stats)
        output.append({
            "state_id": state, **dict(stats),
            "coverage": round(stats["covered"] / stats["evaluated"], 6) if stats["evaluated"] else None,
            "static_global_coverage": round(stats["static_global_covered"] / stats["evaluated"], 6) if stats["evaluated"] else None,
        })
    return {
        "manifest": {
            "schema": "nwnht_v2_contextual_fine_retrieval_audit_v1",
            "selection": "At most one active-endpoint primary-G record per match, max 50 matches per state; each query excludes its full match from neighbours.",
            "prohibition": "This measures held-out endpoint coverage, not causal quality or PhysX reachability.",
        },
        "summary": {
            **dict(total),
            "coverage": round(total["covered"] / total["evaluated"], 6) if total["evaluated"] else None,
            "static_global_coverage": round(total["static_global_covered"] / total["evaluated"], 6) if total["evaluated"] else None,
            "regions_available_rate": round(total["regions_available"] / total["evaluated"], 6) if total["evaluated"] else None,
        },
        "states": output,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=root / "nwnht_v2_universal_semantic_goal_mdp_v2.json")
    parser.add_argument("--exemplars", type=Path, default=root / "nwnht_v2_contextual_fine_exemplars_v1.json")
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_contextual_fine_retrieval_audit_v1.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    result = audit(
        json.loads(args.plan.read_text(encoding="utf-8")), ContextualFineRetriever.load(args.exemplars),
        _read_jsonl(args.templates), _read_jsonl(args.transitions),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
