"""Preserve actual observed contact routes during local-start selection."""
from __future__ import annotations


def signature(record, selection):
    chain = []
    for event in record.get("collision_events", []):
        pair = tuple(sorted(event["stones"]))
        if pair not in chain:
            chain.append(pair)
    states = {s["index"]: s for s in record["physical_final"]}
    live = tuple((int(i), bool(states[int(i)]["enabled"]))
                 for i, g in sorted(selection["goal"]["stones"].items())
                 if g["type"] != "ANY" and g.get("required", True))
    return tuple(record["prediction"].get("firstContactTargets", [])), tuple(chain), live


def parents(ordered, selection, visits):
    """Keep the best viable mode and rotate a second, less-explored mode.

    This does not know any reference route. Viability uses requested first
    contact and required in-region/surviving stones only. Endpoints are ranked
    by the existing exact-goal loss within every observed mode.
    """
    leaders = {}
    for item in ordered:
        record = item["record"]
        contacts = record["prediction"].get("firstContactTargets", [])
        if record.get("rule_violations") or not record["prediction"].get("settled"):
            continue
        if "first_contact_any" in selection and (not contacts or not set(contacts) <= set(selection["first_contact_any"])):
            continue
        if selection.get("require_single_first_contact") and len(contacts) != 1:
            continue
        if selection.get("require_no_contact") and record["prediction"].get("contact"):
            continue
        states = {s["index"]: s for s in record["physical_final"]}
        if any(not states[int(i)]["enabled"] for i, g in selection["goal"]["stones"].items()
               if g["type"] in ("IN_REGION", "SURVIVE") and g.get("required", True)):
            continue
        key = signature(record, selection)
        leaders.setdefault(key, item)
    if not leaders:
        return [], 0
    selected = [min(leaders, key=lambda key: leaders[key]["loss"])]
    others = [key for key in leaders if key not in selected]
    if others:
        selected.append(min(others, key=lambda key: (visits.get(key, 0), leaders[key]["loss"])))
    for key in selected:
        visits[key] = visits.get(key, 0)+1
    return [leaders[key] for key in selected], len(leaders)
