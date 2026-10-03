#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the observational S -> G -> U -> S' graph for v2 goal templates.

Only structural goal candidates from ``build_goal_library_v2`` enter this
compact graph.  The terminal end label is attached for later offline
comparison, never used as a runtime state feature or action definition.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_goal_library_v2 import _goal_id, _signature
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_goal_library_v2 import _goal_id, _signature  # type: ignore


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [{"value": value, "count": count, "share": round(count / total, 6)} for value, count in counter.most_common()]


def _outcome(margin: int) -> str:
    return "FIRST_SCORES" if margin > 0 else "OPPONENT_SCORES" if margin < 0 else "BLANK"


def build(
    transition_rows: Iterable[Mapping[str, Any]],
    templates: Iterable[Mapping[str, Any]],
    goals: Iterable[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Join source rows and templates by panel key, retaining candidate goals only."""

    by_panel = {
        f"{row['end_id']}:{row['own_global_shot_number']}": row
        for row in transition_rows
    }
    candidates = {str(goal["goal_id"]): goal for goal in goals if bool(goal["runtime_goal_candidate"])}
    grouped: dict[tuple[str, str], dict[str, Any]] = defaultdict(lambda: {
        "count": 0, "margins": [], "outcomes": Counter(), "post_own": Counter(), "reply": Counter(), "examples": [],
    })
    template_count = candidate_row_count = 0
    missing_source_rows: list[str] = []
    for template in templates:
        template_count += 1
        goal_id = _goal_id(_signature(template))
        if goal_id not in candidates:
            continue
        candidate_row_count += 1
        panel_key = str(template["panel_key"])
        source = by_panel.get(panel_key)
        if source is None:
            missing_source_rows.append(panel_key)
            continue
        key = (str(template["source_state"]), goal_id)
        item = grouped[key]
        item["count"] += 1
        margin = int(source["terminal_end_label"]["first_end_margin"])
        item["margins"].append(margin)
        item["outcomes"][_outcome(margin)] += 1
        item["post_own"][str(template["post_own_topology"])] += 1
        item["reply"][str(template["after_opponent_reply_state"])] += 1
        if len(item["examples"]) < 5:
            item["examples"].append(panel_key)
    if missing_source_rows:
        raise ValueError(f"{len(missing_source_rows)} candidate templates had no matching source row; first={missing_source_rows[:3]}")

    edges: list[dict[str, Any]] = []
    for (source_state, goal_id), item in grouped.items():
        goal = candidates[goal_id]
        support = item["count"]
        # This must match the family support: otherwise the saved template
        # file and family file were produced from different inputs.
        if support != int(goal["support"]):
            raise ValueError(f"goal support mismatch for {goal_id}: templates={support}, family={goal['support']}")
        margins = item["margins"]
        edges.append({
            "schema": "nwnht_v2_observational_state_goal_edge_v0",
            "source_state": source_state,
            "goal_id": goal_id,
            "support": support,
            "post_own_topology_distribution": _distribution(item["post_own"]),
            "after_opponent_reply_state_distribution": _distribution(item["reply"]),
            "terminal_end_result_distribution": _distribution(item["outcomes"]),
            "observed_mean_first_end_margin": round(sum(margins) / support, 6),
            "observed_first_scores_rate": round(item["outcomes"]["FIRST_SCORES"] / support, 6),
            "examples": item["examples"],
            "evidence_status": "OBSERVATIONAL_EDGE_ONLY",
            "warning": "The goal label is an observed endpoint template. These outcome statistics are associations, not causal values or a deployable action ranking.",
        })
    edges.sort(key=lambda edge: (str(edge["source_state"]), -int(edge["support"]), str(edge["goal_id"])))
    return edges, {
        "schema": "nwnht_v2_observational_state_goal_graph_manifest_v0",
        "input_transition_rows": len(by_panel),
        "input_template_rows": template_count,
        "candidate_template_rows": candidate_row_count,
        "candidate_goal_count": len(candidates),
        "state_goal_edge_count": len(edges),
        "source_state_count": len({edge["source_state"] for edge in edges}),
        "warning": "This is a compact observational subgraph. It excludes unsupported/ambiguous goal templates and does not prove that choosing an endpoint causes its observed end result.",
    }


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--goals", type=Path, default=root / "nwnht_v2_goal_template_families_v0.json")
    parser.add_argument("--output", type=Path, default=root / "nwnht_v2_observational_state_goal_graph_v0.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    goals = json.loads(args.goals.read_text(encoding="utf-8"))
    edges, manifest = build(_read_jsonl(args.transitions), _read_jsonl(args.templates), goals)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"manifest": manifest, "edges": edges}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **manifest}, ensure_ascii=False))


if __name__ == "__main__":
    main()
