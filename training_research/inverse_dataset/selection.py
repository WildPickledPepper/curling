"""Select observed tactical successes from fixed-board parameter scans."""
from __future__ import annotations

import copy
import math

from .schema import TACTICS, encode_input, goal_met


def validate_selection(selection, active_index):
    if selection.get("tactic") not in TACTICS:
        raise ValueError("selection needs a known tactic")
    goal = selection["goal"]
    if not goal.get("stones") or all(g["type"] == "ANY" for g in goal["stones"].values()):
        raise ValueError("selection needs at least one constrained stone")
    dummy = [{"index": i, "enabled": False, "x": 0., "y": 0.} for i in range(16)]
    encode_input(dummy, goal, active_index, selection["tactic"])
    for key in ("first_contact_any",):
        if key in selection and (not selection[key] or any(not isinstance(i, int) or not 0 <= i < active_index for i in selection[key])):
            raise ValueError("first contact targets must be earlier stone slots")
    for pair in selection.get("required_collision_pairs", []):
        if len(pair) != 2 or pair[0] == pair[1] or any(not isinstance(i, int) or not 0 <= i <= active_index for i in pair):
            raise ValueError("invalid required collision pair")
    if selection["tactic"] == "double_hit":
        pairs = selection.get("required_collision_pairs", [])
        targets = selection.get("first_contact_any", [])
        if len(targets) != 2 or len(set(targets)) != 2 or not selection.get("require_single_first_contact") or not any(set(p) == set(targets) for p in pairs):
            raise ValueError("double_hit needs two first-contact targets, single first contact and their observed collision")
        if any(i % 2 == active_index % 2 for i in targets):
            raise ValueError("double_hit targets must be opponents")
        if any(goal["stones"].get(str(i), {}).get("type") not in ("OUT_OF_PLAY", "OUT_OF_HOUSE") for i in targets):
            raise ValueError("double_hit must request both targets to leave play or house")
    return selection


def failure_reason(record, selection):
    if record.get("status") != "complete":
        return "simulation_error"
    if not record.get("prediction", {}).get("settled"):
        return "unfinished"
    if record.get("rule_violations"):
        return "rule_violation"
    if not goal_met(record["physical_final"], selection["goal"]):
        return "goal_not_met"
    contacts = set(record["prediction"].get("firstContactTargets", []))
    if selection.get("require_no_contact") and record["prediction"].get("contact"):
        return "unexpected_contact"
    if "first_contact_any" in selection and (not contacts or not contacts <= set(selection["first_contact_any"])):
        return "wrong_first_contact"
    if selection.get("require_single_first_contact") and len(contacts) != 1:
        return "multiple_or_missing_first_contact"
    pairs = {frozenset(e["stones"]) for e in record.get("collision_events", [])}
    if any(frozenset(p) not in pairs for p in selection.get("required_collision_pairs", [])):
        return "missing_collision_pair"
    return None


def select_candidate(records, selection, min_seeds=1, min_success_rate=1.):
    """Repeated seeds cannot inflate confidence; errors count as failures."""
    if not records or min_seeds < 1 or not math.isfinite(min_success_rate) or not 0 < min_success_rate <= 1:
        raise ValueError("invalid seed acceptance threshold")
    validate_selection(selection, int(records[0]["active_index"]))
    if any((r["scene_key"], r["shot"]) != (records[0]["scene_key"], records[0]["shot"]) for r in records):
        raise ValueError("candidate group mixes boards or shots")
    seeds = [r["physics_seed"] for r in records]
    if len(set(seeds)) != len(seeds):
        raise ValueError("candidate repeats a physics seed")
    reasons = [failure_reason(r, selection) for r in records]
    successful = [r for r, reason in zip(records, reasons) if reason is None]
    rate = len(successful) / len(records)
    accepted = len(successful) >= min_seeds and rate >= min_success_rate
    selected = []
    if accepted:
        for record in successful:
            item = copy.deepcopy(record)
            item["selected_task"] = copy.deepcopy(selection)
            selected.append(item)
    return selected, {"attempts": len(records), "successes": len(successful), "success_rate": rate,
                      "accepted": accepted, "failures": [r for r in reasons if r is not None],
                      "successful_seeds": [r["physics_seed"] for r in successful]}
