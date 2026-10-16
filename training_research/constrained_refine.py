"""Quadratic-model feasibility search, with exact physics-only certification.

COBYQA reference: https://www.cobyqa.com/v1.1.1/ . The signed constraints
guide proposals; they never replace the original task_failure predicate.
"""
from __future__ import annotations

import math
import numpy as np


def signed_slacks(record, selection):
    states = {s["index"]: s for s in record["physical_final"]}
    values = []
    for key, goal in sorted(selection["goal"]["stones"].items(), key=lambda kv: int(kv[0])):
        stone = states[int(key)]
        kind = goal["type"]
        if kind == "IN_REGION":
            values.append(1.-math.hypot(stone["x"]-goal["x"], stone["y"]-goal["y"])/goal["radius"]
                          if stone["enabled"] else -10.)
        elif kind == "OUT_OF_PLAY":
            distance = max(0., min(stone["x"]-.145, 4.605-stone["x"], stone["y"], 10.525-stone["y"]))
            values.append(-1.-distance/2.375 if stone["enabled"] else 1.)
        elif kind == "OUT_OF_HOUSE":
            distance = math.hypot(stone["x"]-2.375, stone["y"]-4.88)
            values.append(distance/1.975-1. if stone["enabled"] else 1.)
        elif kind == "SURVIVE":
            values.append(1. if stone["enabled"] else -10.)
    prediction = record["prediction"]
    contacts = set(prediction.get("firstContactTargets", []))
    if selection.get("require_no_contact"):
        values.append(-10. if prediction.get("contact") else 1.)
    if "first_contact_any" in selection:
        values.append(1. if contacts and contacts <= set(selection["first_contact_any"]) else -10.)
    if selection.get("require_single_first_contact"):
        values.append(1. if len(contacts) == 1 else -10.)
    pairs = {frozenset(e["stones"]) for e in record["collision_events"]}
    values.extend(1. if frozenset(p) in pairs else -10. for p in selection.get("required_collision_pairs", []))
    values.append(1. if prediction.get("settled") and not record.get("rule_violations") else -10.)
    return np.asarray(values)


def fit(current, trial, selection, *, iterations=4, allowance=48):
    import cobyqa
    from scipy.optimize import Bounds, NonlinearConstraint
    from training_research.inverse_goal_search import clip
    scale = np.asarray((.12, .06, .8))
    cache = {}
    best = current
    class Finished(Exception):
        def __init__(self, item):
            self.item = item
    def constraints(x):
        nonlocal best
        shot = clip(x*scale)
        if shot not in cache:
            if len(cache) >= allowance:
                raise Finished(False)
            item = trial(shot, "terminal_cobyqa")
            if item is None:
                raise Finished(None)
            if item["success"]:
                raise Finished(item)
            cache[shot] = item
            if item["loss"] < best["loss"]:
                best = item
        return signed_slacks(cache[shot]["record"], selection)
    try:
        cobyqa.minimize(None, np.asarray(current["shot"])/scale,
                        bounds=Bounds(np.asarray((.2, -2.23, -15.7))/scale,
                                      np.asarray((6., 2.23, 15.7))/scale),
                        constraints=NonlinearConstraint(constraints, 0., np.inf),
                        options={"maxfev": allowance, "maxiter": 200,
                                 "nb_points": 10, "radius_init": .25 if current["loss"] < 1. else 1.,
                                 "radius_final": .0001, "feasibility_tol": 1e-9})
    except Finished as exc:
        return best, exc.item
    return best, False
