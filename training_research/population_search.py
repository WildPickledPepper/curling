"""Contact-coordinate differential evolution followed by terminal refinement.

The coordinate transform is an initial-trajectory approximation only. Success
always comes from trial's complete original forward predicate. No source
actions, reference results or source seeds are read here.
"""
from __future__ import annotations

import numpy as np


def refine(scene, trial, evaluated, elapsed, budget, diagnostics):
    from scipy.optimize import differential_evolution
    from training_research.inverse_initials import path_array, interpolate
    from training_research.solver_experiments import dfols_fit

    targets = scene["selection"].get("first_contact_any", [])
    stones = {s["index"]: s for s in scene["stones"]}
    target = stones.get(targets[0]) if len(targets) == 1 else None
    best = min(evaluated, key=lambda p: p["loss"])
    bounds = np.array(((2.4, 6.), (-.36, .36), (-15.7, 15.7))) if target else np.array(((.2, 6.), (-2.23, 2.23), (-15.7, 15.7)))

    def path_x(v, w):
        state = interpolate(path_array(float(v), float(w)), target["y"]+.29)
        return float(state[0][0]) if state is not None else None

    def encode(shot):
        out = np.asarray(shot, dtype=float).copy()
        if target:
            anchor = path_x(out[0], out[2])
            if anchor is None:
                return None
            out[1] += anchor-target["x"]
        return out

    def decode(x):
        shot = np.asarray(x, dtype=float).copy()
        if target:
            anchor = path_x(shot[0], shot[2])
            if anchor is None:
                return None
            shot[1] += target["x"]-anchor
        if not -2.23 <= shot[1] <= 2.23:
            return None
        return shot

    class Finished(Exception):
        def __init__(self, item):
            self.item = item

    def objective(x):
        nonlocal best
        if elapsed() >= budget:
            raise Finished(None)
        shot = decode(x)
        if shot is None:
            return 1e8
        item = trial(shot, "population_de")
        if item is None:
            raise Finished(None)
        if item["success"]:
            raise Finished(item)
        if item["loss"] < best["loss"]:
            best = item
        return item["loss"]

    # First retain the original local opportunity. The remaining budget moves
    # a population across modes rather than repeatedly fitting the same point.
    if best["loss"] < 80.:
        best, success = dfols_fit(best, trial, scene["selection"], allowance=24)
        if success is None or success:
            return success
    rng = np.random.RandomState(20261016)
    population = []
    scale = np.array((.4, .06, 2.))
    for item in sorted(evaluated+[best], key=lambda p: p["loss"]):
        if elapsed() >= budget:
            return None
        value = encode(item["shot"])
        if value is None or np.any(value < bounds[:, 0]) or np.any(value > bounds[:, 1]):
            continue
        if all(np.linalg.norm((value-p)/scale) > .3 for p in population):
            population.append(value)
        if len(population) == 12:
            break
    # Each dimension receives stratified coverage, independent of references.
    for j in range(8):
        value = bounds[:, 0]+(bounds[:, 1]-bounds[:, 0])*np.array(((j+.5)/8., ((3*j)%8+.5)/8., ((5*j)%8+.5)/8.))
        population.append(value)
    diagnostics["population_size"] = len(population)
    diagnostics["population_coordinates"] = "v, approximate impact offset, w" if target else "v,h,w"
    generation = 0
    last_fitted = best["shot"]

    def callback(x, convergence):
        nonlocal best, generation, last_fitted
        generation += 1
        diagnostics["population_generations"] = generation
        # A new basin gets a short local fit; no second fit of the same action.
        if generation % 3 == 0 and best["loss"] < 80. and best["shot"] != last_fitted:
            last_fitted = best["shot"]
            best, success = dfols_fit(best, trial, scene["selection"], allowance=24)
            if success is None or success:
                raise Finished(success)
        return elapsed() >= budget

    try:
        differential_evolution(objective, bounds, init=np.asarray(population),
                               seed=rng, strategy="best1bin", mutation=(.5, 1.),
                               recombination=.9, maxiter=1000, tol=0., atol=0.,
                               polish=False, updating="immediate", callback=callback)
    except Finished as exc:
        return exc.item
    return None
