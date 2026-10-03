#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract conditional G2 libraries after the fixed local K1 centre guard.

The source state is one of the five rule-compatible, anchor-preserving S2
states from ``build_local_k1_anchor_k2_subset_v1.py``.  This module does not
reuse an old unconditioned K2 state plan: every candidate G2 comes from the
continuation of a retained K1 -> opponent reply -> K2 historical trajectory.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .build_local_k1_anchor_k2_subset_v1 import has_preserved_anchor, is_local_k1_anchor, reply_class
    from .build_universal_semantic_goal_mdp_v1 import (
        MAX_FINE_OPTIONS_PER_GOAL, MAX_GOALS_PER_STATE, SHRINKAGE_PSEUDOCOUNT,
        _distribution, _fine_options, _goal_id, _semantic_key, physically_admissible_own_shot_observation,
    )
except ImportError:  # pragma: no cover - direct script invocation
    import sys
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_local_k1_anchor_k2_subset_v1 import has_preserved_anchor, is_local_k1_anchor, reply_class  # type: ignore
    from causal_state_machine.build_universal_semantic_goal_mdp_v1 import (  # type: ignore
        MAX_FINE_OPTIONS_PER_GOAL, MAX_GOALS_PER_STATE, SHRINKAGE_PSEUDOCOUNT,
        _distribution, _fine_options, _goal_id, _semantic_key, physically_admissible_own_shot_observation,
    )


MIN_DIRECT_SUPPORT = 30


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def retained_k1_state_by_end(rows: Iterable[Mapping[str, Any]]) -> dict[int, str]:
    """Map an end to its local, anchor-preserving S2 class."""

    result: dict[int, str] = {}
    for row in rows:
        if int(row.get("own_throw_number", -1)) != 1:
            continue
        after_own = list(row.get("u_after_own", []))
        after_reply = list(row.get("s_after_opponent_reply", []))
        if any(is_local_k1_anchor(stone) for stone in after_own) and has_preserved_anchor(after_reply):
            result[int(row["end_id"])] = reply_class(after_reply)
    return result


def build(
    *, k1_transitions: Iterable[Mapping[str, Any]], k2_transitions: Iterable[Mapping[str, Any]],
    k2_templates: Iterable[Mapping[str, Any]], min_direct_support: int = MIN_DIRECT_SUPPORT,
) -> dict[str, Any]:
    source_by_end = retained_k1_state_by_end(k1_transitions)
    template_by_panel = {
        str(row["panel_key"]): dict(row)
        for row in k2_templates if int(row.get("K", -1)) == 2
    }
    grouped: dict[tuple[str, tuple[Any, ...]], list[dict[str, Any]]] = defaultdict(list)
    missing_template = rejected_physical = 0
    for transition in k2_transitions:
        if int(transition.get("own_throw_number", -1)) != 2:
            continue
        source = source_by_end.get(int(transition["end_id"]))
        if source is None:
            continue
        panel_key = f"{transition['end_id']}:{transition['own_global_shot_number']}"
        template = template_by_panel.get(panel_key)
        if template is None:
            missing_template += 1
            continue
        if not physically_admissible_own_shot_observation(template):
            rejected_physical += 1
            continue
        grouped[(source, _semantic_key(template))].append({
            **template,
            "match_id": int(transition["match_id"]),
            "margin": float(transition["terminal_end_label"]["first_end_margin"]),
            "next_state": str(template["after_opponent_reply_state"]),
            "original_unconditioned_source_state": str(template["source_state"]),
        })

    by_state: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for (state, _), rows in grouped.items():
        by_state[state].extend(rows)
    conditional_k2_observation_count = sum(len(rows) for rows in grouped.values())
    selected_g2_observation_count = 0
    plans: list[dict[str, Any]] = []
    for state, state_rows in sorted(by_state.items()):
        baseline = sum(float(row["margin"]) for row in state_rows) / len(state_rows)
        candidates: list[dict[str, Any]] = []
        for (source, key), rows in grouped.items():
            if source != state:
                continue
            _, kind, first_house, opponent_house, removed, house_removed, control, macro = key
            mean_margin = sum(float(row["margin"]) for row in rows) / len(rows)
            score = (len(rows) * mean_margin + SHRINKAGE_PSEUDOCOUNT * baseline) / (len(rows) + SHRINKAGE_PSEUDOCOUNT)
            goal_id = _goal_id(state, key)
            fine_options = _fine_options(rows)
            candidates.append({
                "source_state": state,
                "goal_id": goal_id,
                "K": 2,
                "direct_support": len(rows),
                "conditional_end_margin_mean": round(mean_margin, 6),
                "conditional_shrunk_end_margin": round(score, 6),
                "after_opponent_reply_state_distribution": _distribution(Counter(str(row["next_state"]) for row in rows)),
                "dominant_next_state": _distribution(Counter(str(row["next_state"]) for row in rows))[0]["value"],
                "goal_state": {
                    "goal_id": goal_id,
                    "source_state": state,
                    "K": 2,
                    "semantic_effect": {
                        "observed_template_kind": kind,
                        "first_house_delta": first_house,
                        "opponent_house_delta": opponent_house,
                        "opponent_removed_count": removed,
                        "opponent_house_removed_count": house_removed,
                    },
                    "semantic_terminal_predicate": {"control": control, "macro": macro},
                    "post_own_topology_distribution": _distribution(Counter(str(row["post_own_topology"]) for row in rows)),
                    "historical_direct_support": len(rows),
                    "fine_goal_options": fine_options[:MAX_FINE_OPTIONS_PER_GOAL],
                    "fine_execution_status": "HAS_HISTORICAL_FINE_IMPLEMENTATION" if fine_options else "NO_HISTORICAL_BINDABLE_FINE_IMPLEMENTATION",
                    "warning": "Conditional historical G2 after a local-rule-compatible K1 anchor. Its score is descriptive, not causal or adversarial.",
                },
            })
        candidates.sort(key=lambda item: (-float(item["conditional_shrunk_end_margin"]), -int(item["direct_support"]), str(item["goal_id"])))
        eligible = [item for item in candidates if int(item["direct_support"]) >= int(min_direct_support)]
        selected_g2_observation_count += sum(int(item["direct_support"]) for item in eligible[:MAX_GOALS_PER_STATE])
        plans.append({
            "state_id": state,
            "K": 2,
            "observed_candidate_count": len(candidates),
            "eligible_candidate_count": len(eligible),
            "recommendation_status": "CONDITIONAL_G2_AVAILABLE" if eligible else "SEARCH_REQUIRED_LOW_CONDITIONAL_SUPPORT",
            "primary_goal": eligible[0] if eligible else None,
            "fallback_goals": eligible[1:MAX_GOALS_PER_STATE],
            "runtime_contract": "Use only when the K1 anchor remains in the FGZ and touches the centre line. Reclassify the actual board after the opponent reply; the stored K3 distribution is not a forced successor.",
        })
    return {
        "manifest": {
            "schema": "nwnht_local_k1_anchor_k2_goals_v5",
            "decision_chain": "fixed G1 centre guard -> local anchor-preserving S2 -> conditional G2",
            "state_count": len(plans),
            "goal_count": sum(1 + len(row["fallback_goals"]) for row in plans if row["primary_goal"]),
            "conditional_k2_observation_count": conditional_k2_observation_count,
            "selected_g2_observation_count": selected_g2_observation_count,
            "missing_k2_template_count": missing_template,
            "rejected_physically_impossible_k2_observation_count": rejected_physical,
            "minimum_direct_support": int(min_direct_support),
            "ranking": "within-S2 direct historical end margin with 5-observation shrinkage; it is not a causal or minimax value.",
            "prohibition": "Do not route a non-anchor S2 to this artifact and do not call its ranking a proof that G2 wins.",
        },
        "state_plans": plans,
    }


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transitions", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--templates", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_local_k1_anchor_k2_goals_v5.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    result = build(
        k1_transitions=_read_jsonl(args.transitions),
        k2_transitions=_read_jsonl(args.transitions),
        k2_templates=_read_jsonl(args.templates), min_direct_support=MIN_DIRECT_SUPPORT,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["manifest"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
