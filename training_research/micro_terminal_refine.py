"""Small central-difference endpoint steps with sensitivity-scaled damping."""
from __future__ import annotations

import numpy as np

from training_research.inverse_terminal_refine import residual


def _branch(record, selection):
    states = {s["index"]: s for s in record["physical_final"]}
    live = tuple(states[int(i)]["enabled"] for i, g in sorted(selection["goal"]["stones"].items())
                 if g["type"] in ("IN_REGION", "SURVIVE"))
    return tuple(record["prediction"].get("firstContactTargets", [])), live


def fit(current, trial, selection, *, iterations=4, allowance=48):
    used = 0
    damping = .03
    limits = np.asarray((.4, .04, 2.))
    for iteration in range(iterations):
        if used+7 > allowance:
            break
        origin = current
        raw_origin = residual(origin["record"], selection, center=True)
        desired = residual(origin["record"], selection, margin=.98)
        origin_branch = _branch(origin["record"], selection)
        columns = []
        for axis, absolute_step in enumerate((.001, .0001, .003)):
            delta = absolute_step*(1. if iteration % 2 == 0 else .5)
            samples = []
            for sign in (1., -1.):
                shot = np.asarray(origin["shot"]).copy()
                shot[axis] += sign*delta
                item = trial(shot, "terminal_micro_jacobian")
                used += 1
                if item is None:
                    return current, None
                if item["success"]:
                    return item, item
                if item["loss"] < current["loss"]:
                    current = item
                if _branch(item["record"], selection) == origin_branch:
                    actual = item["shot"][axis]-origin["shot"][axis]
                    if abs(actual) > 1e-10:
                        samples.append((actual, residual(item["record"], selection, center=True)))
            if len(samples) == 2:
                columns.append((samples[0][1]-samples[1][1])/(samples[0][0]-samples[1][0]))
            elif samples:
                columns.append((samples[0][1]-raw_origin)/samples[0][0])
            else:
                columns.append(np.zeros_like(raw_origin))
        jacobian = np.column_stack(columns)
        normal = jacobian.T@jacobian
        diagonal = np.maximum(np.diag(normal), 1e-8)
        try:
            move = np.linalg.solve(normal+damping*np.diag(diagonal), -jacobian.T@desired)
        except np.linalg.LinAlgError:
            break
        move /= max(1., float(np.max(np.abs(move)/limits)))
        predicted = float(np.linalg.norm(jacobian@move))
        permitted = max(.2, min(3., float(np.linalg.norm(desired))))
        move /= max(1., predicted/permitted)
        accepted = False
        for alpha in (1., .5, .25):
            if used >= allowance:
                break
            item = trial(np.asarray(origin["shot"])+alpha*move, "terminal_micro_step")
            used += 1
            if item is None:
                return current, None
            if item["success"]:
                return item, item
            if item["loss"] < current["loss"]:
                current = item
                accepted = True
                break
        damping = max(.0001, damping/3.) if accepted else damping*10.
        if not accepted and current is origin and damping > 20.:
            break
    return current, False
