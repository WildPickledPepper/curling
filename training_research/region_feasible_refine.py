"""Linearise endpoint positions, then satisfy goal disks as inequalities.

The inner model proposes an action only. It never moves physical stones or
accepts its own predicted endpoints; the original forward predicate certifies.
"""
from __future__ import annotations

import numpy as np


def _positions(record, goals):
    states = {s["index"]: s for s in record["physical_final"]}
    return np.asarray([[(states[index]["x"]-goal["x"])/goal["radius"],
                        (states[index]["y"]-goal["y"])/goal["radius"]]
                       for index, goal in goals])


def _mode(record, selection):
    states = {s["index"]: s for s in record["physical_final"]}
    pairs = []
    for event in record.get("collision_events", []):
        pair = tuple(sorted(event["stones"]))
        if pair not in pairs:
            pairs.append(pair)
    return (tuple(record["prediction"].get("firstContactTargets", [])), tuple(pairs),
            tuple((int(i), states[int(i)]["enabled"]) for i, g in sorted(selection["goal"]["stones"].items())
                  if g["type"] != "ANY"))


def fit(current, trial, selection, *, iterations=4, allowance=48):
    from scipy.optimize import minimize
    goals = [(int(i), g) for i, g in sorted(selection["goal"]["stones"].items())
             if g["type"] == "IN_REGION"]
    if not goals:
        return current, False
    best = current
    used = 0
    scale = np.asarray((.1, .005, 1.))
    trust = 1.

    def merit(item):
        p = _positions(item["record"], goals)
        return max(0., float(np.max(np.linalg.norm(p, axis=1)))-.985)

    def evaluate(shot, phase):
        nonlocal used, best
        item = trial(shot, phase)
        used += 1
        if item is not None and item["loss"] < best["loss"]:
            best = item
        return item

    for iteration in range(iterations):
        if used+7 > allowance:
            break
        origin = current
        origin_mode = _mode(origin["record"], selection)
        # This local model cannot cross enable/disable or contact predicates.
        # Other search branches remain responsible for those transitions.
        if not all(s["enabled"] for s in origin["record"]["physical_final"] if s["index"] in {i for i, g in goals}):
            break
        positions = _positions(origin["record"], goals)
        columns = []
        for axis, delta in enumerate((.001, .0001, .003)):
            samples = []
            for sign in (1., -1.):
                shot = np.asarray(origin["shot"]).copy()
                shot[axis] += sign*delta*(.5 if iteration % 2 else 1.)
                item = evaluate(shot, "region_jacobian")
                if item is None or item["success"]:
                    return best, item
                actual = (item["shot"][axis]-origin["shot"][axis])/scale[axis]
                if _mode(item["record"], selection) == origin_mode and abs(actual) > 1e-12:
                    samples.append((actual, _positions(item["record"], goals)))
            if len(samples) == 2:
                columns.append((samples[0][1]-samples[1][1])/(samples[0][0]-samples[1][0]))
            elif samples:
                columns.append((samples[0][1]-positions)/samples[0][0])
            else:
                columns.append(np.zeros_like(positions))
        jacobian = np.stack(columns, axis=-1)
        action = np.asarray(origin["shot"])
        lower = np.maximum(-trust, (np.asarray((.2, -2.23, -15.7))-action)/scale)
        upper = np.minimum(trust, (np.asarray((6., 2.23, 15.7))-action)/scale)
        # Convex epigraph subproblem: minimise the worst squared disk violation
        # with a small minimum-step regulariser. Already satisfied goals remain
        # inequalities, so their available interior is not frozen at zero delta.
        def constraints(z):
            predicted = positions+np.einsum("ijk,k->ij", jacobian, z[:3])
            return .985**2+z[3]-np.sum(predicted**2, axis=1)
        def constraint_jacobian(z):
            predicted = positions+np.einsum("ijk,k->ij", jacobian, z[:3])
            return np.column_stack((-2.*np.einsum("ij,ijk->ik", predicted, jacobian), np.ones(len(goals))))
        initial = np.array((0., 0., 0., max(0., float(np.max(np.sum(positions**2, axis=1)))-.985**2)))
        model = minimize(lambda z: z[3]+1e-5*float(z[:3]@z[:3]), initial,
                         jac=lambda z: np.r_[2e-5*z[:3], 1.], method="SLSQP",
                         bounds=list(zip(lower, upper))+[(0., None)],
                         constraints={"type": "ineq", "fun": constraints, "jac": constraint_jacobian},
                         options={"maxiter": 80, "ftol": 1e-10})
        if not np.isfinite(model.x).all():
            break
        accepted = False
        for alpha in (1., .5, .25):
            if used >= allowance:
                break
            item = evaluate(action+alpha*model.x[:3]*scale, "region_feasible_step")
            if item is None or item["success"]:
                return best, item
            if _mode(item["record"], selection) == origin_mode and merit(item) < merit(current)-1e-6:
                current = item
                accepted = True
                break
        if not accepted:
            current = best
        trust = min(2., trust*1.5) if accepted else trust*.35
        if trust < .01:
            break
    return best, False
