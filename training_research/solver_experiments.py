"""Opt-in search experiments; they do not change physics or goal acceptance."""
from __future__ import annotations

import functools
import math


PROFILE_NAMES = ("baseline", "stream", "dfols", "impact_dfols", "portfolio",
                 "safe_stream", "safe_portfolio", "wide_dfols", "learned_dfols", "cobyqa", "tangent_dfols", "tangent_micro", "contact_de", "impact_learned", "chain_dfols", "region_feasible", "region_routes", "distribution_dfols", "full_distribution", "full_augmented")


def precise_clip(shot):
    return tuple(round(min(high, max(low, float(value))), 8)
                 for value, low, high in zip(shot, (.2, -2.23, -15.7), (6., 2.23, 15.7)))


def streamed_initials(scene, elapsed, budget, clip, diagnostics):
    """Certify a cheap candidate before generating the entire proposal pool."""
    from training_research.inverse_initials import path_array, interpolate, clearance
    from training_research.inverse_dataset.schema import STONE_R
    from training_research.inverse_goal_search import proposals
    goals = scene["selection"]["goal"]["stones"]
    stones = {s["index"]: s for s in scene["stones"]}
    active_goal = goals.get(str(scene["active_index"]), {})
    no_contact = scene["selection"].get("require_no_contact")
    targets = [] if no_contact else scene["selection"].get("first_contact_any", [])
    if not no_contact and not targets:
        targets = [i for i, s in stones.items() if str(i) in goals and
                   (goals[str(i)]["type"] in ("OUT_OF_PLAY", "OUT_OF_HOUSE") or
                    (goals[str(i)]["type"] == "IN_REGION" and math.hypot(s["x"]-goals[str(i)]["x"], s["y"]-goals[str(i)]["y"]) > .03))]
    seen = set()
    def fresh(shot):
        shot = clip(shot)
        if shot not in seen:
            seen.add(shot)
            return shot
        return None
    if not targets and active_goal.get("type") == "IN_REGION":
        blockers = [(s["x"], s["y"]) for s in stones.values()]
        for w in (0., 3., -3., 7., -7., 12., -12., 15., -15.):
            if elapsed() >= budget: return
            low, high = 2.2, 4.
            for _ in range(15):
                if elapsed() >= budget: return
                v = (low+high)/2
                if path_array(v, w)[-1, 1] > active_goal["y"]: low = v
                else: high = v
            v = (low+high)/2
            path = path_array(v, w)
            h = active_goal["x"]-float(path[-1, 0])
            if abs(h) > 2.23: continue
            shot = fresh((v, h, w))
            if shot is None: continue
            # Clearance is only an approximation. A nominal near-contact must
            # not defer every real physics call until the whole grid is built.
            yield shot
        return
    for i in targets:
        s = stones[i]
        for v in (6., 5.6, 4.8, 4.2):
            if elapsed() >= budget: return
            state = interpolate(path_array(v, 0.), s["y"]+2*STONE_R)
            if state is None: continue
            h = s["x"]-float(state[0][0])
            if abs(h) > 2.23: continue
            shot = fresh((v, h, 0.))
            if shot is not None: yield shot
    if stones and not no_contact:
        from training_research.inverse_contact_atlas import atlas_initials
        atlas, sources = atlas_initials(scene, elapsed, min(budget, elapsed()+.8), clip, limit=8)
        diagnostics["atlas_sources"] = sources
        for shot in atlas:
            shot = fresh(shot)
            if shot is not None: yield shot
    raw = sorted(proposals(scene, elapsed, min(budget, elapsed()+1.2)))
    families = set()
    retained = []
    for _, shot, family in raw:
        if family in families: continue
        families.add(family)
        retained.append(shot)
        if len(retained) == 20: break
    if stones and not no_contact:
        from training_research.inverse_contact_initials import contact_initials
        extra = contact_initials(scene, elapsed, min(budget, elapsed()+.7), clip)
    else:
        extra = []
    for n in range(max(len(retained), len(extra))):
        for group in (retained, extra):
            if n < len(group):
                shot = fresh(group[n])
                if shot is not None: yield shot


def fast_first_initials(scene, elapsed, budget, clip, diagnostics):
    """One cheap certified entrance, then preserve the baseline fallback pool."""
    from training_research.inverse_goal_search import eager_initial_pool
    prefix = streamed_initials(scene, elapsed, budget, clip, diagnostics)
    seen = set()
    first = next(prefix, None)
    if first is not None:
        seen.add(first)
        yield first
    if elapsed() >= budget:
        return
    for shot in eager_initial_pool(scene, elapsed, budget, diagnostics):
        if shot not in seen:
            seen.add(shot)
            yield shot


def forest_initials(scene, elapsed, budget, clip, diagnostics, *, impact=False, distribution=False, full=False):
    """Interleave board-held-out learned proposals with the old initial pool."""
    from training_research.contact_seed_forest import learned_initials, board_fold
    from training_research.inverse_goal_search import eager_initial_pool
    seen = set()
    first = next(streamed_initials(scene, elapsed, budget, clip, diagnostics), None)
    if first is not None:
        seen.add(first)
        yield first
    learned = []
    if len(scene["selection"].get("first_contact_any", [])) == 1:
        if full:
            from training_research.full_contact_prior import proposals
            learned = proposals(scene, limit=12)
        elif distribution:
            from training_research.contact_distribution_prior import proposals
            learned = proposals(scene, limit=12)
        elif impact:
            from training_research.contact_seed_forest import IMPACT
            learned = learned_initials(scene, path=IMPACT, limit=12)
        else:
            learned = learned_initials(scene, limit=12)
        diagnostics.update(learned_fold=board_fold(scene["scene_key"]), learned_count=len(learned),
                           learned_exclusion="all rows from the current board fold excluded")
    for shot in learned[:4]:
        shot = clip(shot)
        if shot not in seen:
            seen.add(shot)
            yield shot
    if elapsed() >= budget:
        return
    original = eager_initial_pool(scene, elapsed, budget, diagnostics)
    for start in range(0, max(len(original), len(learned)-4), 4):
        for group in (original[start:start+4], learned[4+start:8+start]):
            for shot in group:
                shot = clip(shot)
                if shot not in seen:
                    seen.add(shot)
                    yield shot


def impact_learned_initials(scene, elapsed, budget, clip, diagnostics):
    yield from forest_initials(scene, elapsed, budget, clip, diagnostics, impact=True)


def distribution_initials(scene, elapsed, budget, clip, diagnostics):
    yield from forest_initials(scene, elapsed, budget, clip, diagnostics, distribution=True)


def full_distribution_initials(scene, elapsed, budget, clip, diagnostics):
    yield from forest_initials(scene, elapsed, budget, clip, diagnostics, full=True)


def augmented_initials(scene, elapsed, budget, clip, diagnostics):
    """Preserve the first 24 old candidates, then add six full-board priors."""
    source = iter(fast_first_initials(scene, elapsed, budget, clip, diagnostics))
    seen = set()
    for _ in range(24):
        shot = next(source, None)
        if shot is None:
            return
        seen.add(shot)
        yield shot
    if elapsed() >= budget:
        return
    if len(scene["selection"].get("first_contact_any", [])) == 1:
        from training_research.full_contact_prior import proposals
        extra = proposals(scene, limit=6, elapsed=elapsed, deadline=budget)
        diagnostics["full_board_seed_count"] = len(extra)
        diagnostics["augmentation_after_original_initials"] = 24
        for shot in extra:
            shot = clip(shot)
            if shot not in seen:
                seen.add(shot)
                yield shot
    for shot in source:
        if shot not in seen:
            seen.add(shot)
            yield shot


def chain_initials(scene, elapsed, budget, clip, diagnostics):
    from training_research.goal_geometry_initials import chain_proposals
    from training_research.inverse_goal_search import eager_initial_pool
    seen = set()
    first = next(streamed_initials(scene, elapsed, budget, clip, diagnostics), None)
    if first is not None:
        seen.add(first)
        yield first
    if elapsed() >= budget:
        return
    original = eager_initial_pool(scene, elapsed, budget, diagnostics)
    directed = chain_proposals(scene, original, elapsed, min(budget, elapsed()+.4), clip)
    diagnostics["chain_initial_count"] = len(directed)
    for start in range(0, max(len(original), len(directed)), 4):
        for group in (directed[start:start+4], original[start:start+4]):
            for shot in group:
                if shot not in seen:
                    seen.add(shot)
                    yield shot


def tangent_initials(scene, elapsed, budget, clip, diagnostics):
    from training_research.goal_geometry_initials import proposals
    from training_research.inverse_goal_search import eager_initial_pool
    first = next(streamed_initials(scene, elapsed, budget, clip, diagnostics), None)
    seen = set()
    if first is not None:
        seen.add(first)
        yield first
    if elapsed() >= budget:
        return
    original = eager_initial_pool(scene, elapsed, budget, diagnostics)
    directed = proposals(scene, original, elapsed, min(budget, elapsed()+.35), clip)
    diagnostics["goal_geometry_initials"] = [list(s) for s in directed]
    for start in range(0, max(len(original), len(directed)), 4):
        for group in (directed[start:start+4], original[start:start+4]):
            for shot in group:
                if shot not in seen:
                    seen.add(shot)
                    yield shot


def refinement_functions(profile):
    if profile == "region_hybrid":
        from training_research.region_feasible_refine import fit as region_fit
        def fit(current, trial, selection, **kwargs):
            if current["loss"] < 4.:
                return region_fit(current, trial, selection, **kwargs)
            kwargs["allowance"] = min(24, kwargs.get("allowance", 24))
            return dfols_fit(current, trial, selection, adaptive=True, **kwargs)
        return fit, lambda current, trial, **kwargs: (current, False)
    if profile == "region_feasible":
        from training_research.region_feasible_refine import fit
        return fit, lambda current, trial, **kwargs: (current, False)
    if profile == "micro":
        from training_research.micro_terminal_refine import fit
        return fit, lambda current, trial, **kwargs: (current, False)
    if profile == "cobyqa":
        from training_research.constrained_refine import fit
        return fit, lambda current, trial, **kwargs: (current, False)
    if profile == "portfolio":
        from training_research.inverse_terminal_refine import simplex_fit
        turn = 0
        def alternate(current, trial, selection, **kwargs):
            nonlocal turn
            impact = turn % 2 == 1
            turn += 1
            kwargs["allowance"] = min(16, kwargs.get("allowance", 16))
            return dfols_fit(current, trial, selection, impact=impact, adaptive=True, **kwargs)
        def short_simplex(current, trial, **kwargs):
            kwargs["allowance"] = min(12, kwargs.get("allowance", 12))
            return simplex_fit(current, trial, **kwargs)
        return alternate, short_simplex
    if profile in ("dfols", "impact_dfols"):
        return functools.partial(dfols_fit, impact=profile=="impact_dfols"), lambda current, trial, **kwargs: (current, False)
    raise ValueError("unknown refinement profile: "+profile)


def dfols_fit(current, trial, selection, *, iterations=4, allowance=24, impact=False, adaptive=False):
    """Bounded residual interpolation/trust-region search (DFO-LS).

    Based on Cartis et al., https://arxiv.org/abs/1804.00154.
    The complete physics predicate, rather than model accuracy, stops on success.
    """
    import dfols
    import numpy as np
    from training_research.inverse_terminal_refine import residual
    from training_research.inverse_initials import path_array, interpolate
    scale = np.asarray((.12, .06, .8))
    origin = np.asarray(current["shot"])
    lower, upper = np.asarray((.2, -2.23, -15.7)), np.asarray((6., 2.23, 15.7))
    target = None
    if impact:
        contacts = current["record"]["prediction"].get("firstContactTargets", [])
        scene = current["record"]["requested_scene"]
        if len(contacts) == 1:
            target = next((s for s in scene["stones"] if s["index"] == contacts[0]), None)
        if target:
            def path_x(v, w):
                state = interpolate(path_array(float(v), float(w)), target["y"]+.29)
                return None if state is None else float(state[0][0])
            anchor = path_x(origin[0], origin[2])
            if anchor is None:
                target = None
            else:
                origin = origin.copy()
                origin[1] += anchor-target["x"]
                scale = np.asarray((.12, .015, .8))
                lower[1], upper[1] = min(-.5, origin[1]-.1), max(.5, origin[1]+.1)
    best = current
    used = 0
    class Finished(Exception):
        def __init__(self, item):
            self.item = item
    def objective(x):
        nonlocal best, used
        if used >= allowance:
            raise Finished(False)
        shot = x*scale
        if target:
            anchor = path_x(shot[0], shot[2])
            shot[1] = current["shot"][1] if anchor is None else target["x"]+shot[1]-anchor
        item = trial(shot, "terminal_impact_dfols" if impact else "terminal_dfols")
        used += 1
        if item is None:
            raise Finished(None)
        if item["success"]:
            raise Finished(item)
        if item["loss"] < best["loss"]:
            best = item
        return residual(item["record"], selection, margin=.9)
    try:
        radius = min(1., max(.02, .5*math.sqrt(max(0., current["loss"])))) if adaptive else .25 if current["loss"] < 1. else 1.
        dfols.solve(objective, origin/scale,
                    bounds=(lower/scale, upper/scale),
                    rhobeg=radius, rhoend=.0001,
                    maxfun=allowance, do_logging=False,
                    user_params={"restarts.use_restarts": False, "slow.max_slow_iters": 4})
    except Finished as exc:
        return best, exc.item
    return best, False


def profile_kwargs(profile):
    """Create per-instance search options after the native environment exists."""
    if profile == "baseline":
        return {}
    if profile not in PROFILE_NAMES:
        raise ValueError("unknown experiment profile: "+profile)
    if profile in ("dfols", "impact_dfols", "portfolio", "safe_portfolio", "wide_dfols", "learned_dfols", "tangent_dfols", "contact_de", "impact_learned", "chain_dfols"):
        import dfols  # Initialise numerical libraries outside per-request timing.
    if profile in ("learned_dfols", "impact_learned"):
        from training_research.contact_seed_forest import DEFAULT, IMPACT, load_fold
        for fold in range(5):
            load_fold(str(IMPACT if profile=="impact_learned" else DEFAULT), fold)
    if profile == "cobyqa":
        import cobyqa
    if profile == "region_feasible":
        from scipy.optimize import minimize
        return dict(initial_provider=tangent_initials, initial_batch_size=24,
                    refinement_profile="region_feasible", fit_allowance=48, action_clip=precise_clip)
    if profile == "region_routes":
        import dfols
        from scipy.optimize import minimize
        return dict(initial_provider=tangent_initials, initial_batch_size=24,
                    refinement_profile="region_hybrid", fit_allowance=32, action_clip=precise_clip,
                    route_diversity=True, fit_loss_limit=600.)
    if profile == "distribution_dfols":
        import dfols
        from training_research.contact_distribution_prior import DEFAULT, joint_groups
        for fold in range(5):
            joint_groups(str(DEFAULT), fold)
        return dict(initial_provider=distribution_initials, initial_batch_size=24,
                    refinement_profile="dfols", fit_allowance=48, action_clip=precise_clip)
    if profile in ("full_distribution", "full_augmented"):
        import dfols
        from training_research.full_contact_prior import DEFAULT
        from training_research.contact_distribution_prior import joint_groups
        for fold in range(5):
            joint_groups(str(DEFAULT), fold)
        return dict(initial_provider=augmented_initials if profile=="full_augmented" else full_distribution_initials,
                    initial_batch_size=30 if profile=="full_augmented" else 24,
                    refinement_profile="dfols", fit_allowance=48,
                    action_clip=None if profile=="full_augmented" else precise_clip)
    if profile == "contact_de":
        from scipy.optimize import differential_evolution
        return dict(initial_provider=tangent_initials, initial_batch_size=24,
                    population_search=True, action_clip=precise_clip)
    if profile == "impact_learned":
        return dict(initial_provider=impact_learned_initials, initial_batch_size=24,
                    refinement_profile="dfols", fit_allowance=48, action_clip=precise_clip)
    if profile == "chain_dfols":
        return dict(initial_provider=chain_initials, initial_batch_size=24,
                    refinement_profile="impact_dfols", fit_allowance=48, action_clip=precise_clip)
    refinement = "micro" if profile=="tangent_micro" else "baseline" if profile in ("stream", "safe_stream") else "portfolio" if profile=="safe_portfolio" else "dfols" if profile in ("wide_dfols", "learned_dfols", "tangent_dfols") else profile
    return dict(initial_provider=tangent_initials if profile in ("tangent_dfols", "tangent_micro") else forest_initials if profile=="learned_dfols" else fast_first_initials if profile.startswith("safe_") or profile in ("wide_dfols", "cobyqa") else streamed_initials,
                refinement_profile=refinement, refresh_each_parent=refinement=="portfolio",
                initial_batch_size=24 if profile in ("wide_dfols", "learned_dfols", "cobyqa", "tangent_dfols", "tangent_micro") else 8,
                fit_allowance=48 if profile in ("wide_dfols", "learned_dfols", "cobyqa", "tangent_dfols", "tangent_micro") else 20,
                action_clip=precise_clip if profile=="tangent_micro" else None)


def install_profile(profile):
    """Compatibility for earlier isolated-process research runners."""
    import training_research.inverse_goal_search as search
    search.solve = functools.partial(search.solve, **profile_kwargs(profile))
