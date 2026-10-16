"""Diverse, inexpensive initial proposals for budgeted double inverse search.

Contact geometry and free-flight paths are proposal approximations only. No
filter, ranking value, or local loss is used as a tactical success predicate.
"""
from functools import lru_cache
import math
import sys
import time

import numpy as np

from training_research.legacy_inverse import clip, legacy_modules, search_loss
from training_research.inverse_dataset.schema import HOUSE_X, STONE_R


@lru_cache(maxsize=128)
def path_array(v, w):
    search, _ = legacy_modules()
    path = search._relative_free_flight(float(v), float(w), 0., 5000)
    return np.asarray([(p.x, p.y, p.vx, p.vy) for p in path], dtype=np.float64)


def interpolate(path, y):
    # Recovered free-flight vy stays negative up to the stopping threshold.
    i = int(np.searchsorted(-path[:, 1], -y, side="left"))
    if i < 1 or i >= len(path):
        return None
    a, b = path[i-1], path[i]
    t = (y-a[1])/(b[1]-a[1])
    return a + t*(b-a), i


def clearance(path, offset, blockers, end):
    if not blockers:
        return 10.
    a, b = path[:end, :2], path[1:end+1, :2]
    delta = b-a
    length = np.maximum(np.einsum("ij,ij->i", delta, delta), 1e-20)
    minimum = math.inf
    for x, y in blockers:
        point = np.array((x-offset, y))
        ratio = np.clip(np.einsum("ij,ij->i", point-a, delta)/length, 0., 1.)
        distance = np.linalg.norm(a+ratio[:, None]*delta-point, axis=1)
        minimum = min(minimum, float(np.min(distance)))
    return minimum


def quick_initials(scene):
    targets = set(scene["selection"]["first_contact_any"])
    stones = sorted((s for s in scene["stones"] if s["index"] in targets), key=lambda s:-s["y"])
    return [{"shot": list(clip((6., s["x"]-HOUSE_X, 0.))), "source": "straight_centre",
             "family": (s["index"], "straight")} for s in stones]


def geometric_initials(scene, *, elapsed, deadline):
    search, _ = legacy_modules()
    geometry_module = sys.modules["training_research._legacy_double_geometry"]
    targets = sorted(scene["selection"]["first_contact_any"])
    stones = {s["index"]:s for s in scene["stones"]}
    blockers = [(s["x"], s["y"]) for s in scene["stones"] if s["index"] not in targets]
    raw = []
    for first, second in (targets, targets[::-1]):
        a, b = stones[first], stones[second]
        geometries = geometry_module.double_collision_geometries((a["x"], a["y"]), (b["x"], b["y"]), samples=144, limit=6)
        aims = [(g.virtual_aim_point, g.pre_second_direction, -g.score, i,
                 max(g.first_exit_distance/max(g.tangential_transfer,1e-6),
                     g.second_exit_distance/max(g.normal_transfer,1e-6))) for i,g in enumerate(geometries)]
        # A missing outward proxy route does not prove the real scene has no
        # solution. Add contact-angle proposals without that hard rejection.
        if not aims:
            theta = math.atan2(b["y"]-a["y"], b["x"]-a["x"])
            for i, turn in enumerate((0., -.15, .15, -.35, .35, -.6, .6)):
                direction = math.cos(theta+turn), math.sin(theta+turn)
                if direction[1] >= 0.:
                    continue
                aim = (a["x"]-2*STONE_R*direction[0], a["y"]-2*STONE_R*direction[1])
                aims.append((aim, direction, .2+abs(turn), i, None))
        for aim, direction, geometry_score, geometry_id, required_range in aims:
            for v in (5., 5.3, 5.6, 5.8, 6.):
                for w in (-9., -7., -5., -3., 0., 3., 5., 7., 9.):
                    if elapsed() >= deadline:
                        return diverse(raw), len(raw)
                    path = path_array(v, w)
                    contact = interpolate(path, aim[1])
                    if contact is None:
                        continue
                    state, end = contact
                    h = aim[0]-float(state[0])
                    if abs(h)>2.23:
                        continue
                    speed = math.hypot(state[2], state[3])
                    alignment = (state[2]*direction[0]+state[3]*direction[1])/max(speed, 1e-10)
                    if alignment <= 0.:
                        continue
                    gap = clearance(path, h, blockers, end)
                    score = geometry_score + .18*(1-alignment) - .025*min(gap, 1.) - .008*speed
                    # Penalize blocked candidates, but retain alternatives if
                    # every nominal path is blocked; strict simulation decides.
                    score += 4*max(0., 2*STONE_R+.025-gap)
                    proxy_valid = required_range is not None and alignment>=.35 and gap>=2*STONE_R+.025 and (speed*alignment)**2>=.55*required_range
                    raw.append({"shot": list(clip((v,h,w))), "source": "contact_geometry",
                                "score": float(score), "family": (first, geometry_id, int(w)),
                                "virtual_aim": list(aim), "clearance": gap,"proxy_valid":bool(proxy_valid)})
    return diverse(raw), len(raw)


def diverse(raw, limit=14):
    ranked = sorted(raw, key=lambda x:(not x["proxy_valid"],x["score"]))
    result, shots, families = [], set(), set()
    # Preserve the old six ranked entrances before adding diverse families.
    # Speed variants remain legitimate alternative local-search entrances.
    for item in ranked[:6]+ranked:
        shot, family = tuple(item["shot"]), tuple(item["family"])
        if shot in shots or (len(result)>=6 and family in families):
            continue
        result.append(item)
        shots.add(shot)
        families.add(family)
        if len(result)==limit:
            break
    return result


def solve(scene, *, evaluate, elapsed, budget_seconds, max_calls=128,
          conservative_rounds=8, local_rounds=16, refinement_profile="baseline", initial_polish=False,
          required_seed_successes=3):
    """Quick entrances, diverse geometry, and opportunistic local refinement."""
    for value in (max_calls,conservative_rounds,local_rounds):
        if isinstance(value,bool) or not isinstance(value,int) or value<1:
            raise ValueError("simulation and iteration limits must be positive integers")
    if not math.isfinite(budget_seconds) or budget_seconds<=0:
        raise ValueError("budget_seconds must be positive and finite")
    if refinement_profile not in ("baseline","fast_poll"):
        raise ValueError("unknown refinement profile")
    if not isinstance(initial_polish,bool):
        raise ValueError("initial_polish must be a boolean")
    if isinstance(required_seed_successes,bool) or not isinstance(required_seed_successes,int) or required_seed_successes<1:
        raise ValueError("required_seed_successes must be a positive integer")
    diagnostics = {"initial_three_seed_success":False, "refinement_three_seed_success":False,
                   "initial_success":False,"refinement_success":False,
                   "initial_generation_ms":0., "proposals":[], "max_physics_calls":max_calls,
                   "conservative_round_limit":conservative_rounds,"local_round_limit":local_rounds,
                   "conservative_iterations":0,"local_iterations":0,
                   "refinement_profile":refinement_profile,
                   "initial_polish":initial_polish,"initial_polish_physics_calls":0,
                   "required_seed_successes":required_seed_successes,
                   "deadline_policy":"check before each proposal or strict call; one in-flight call may finish after budget"}
    cache, count, best = {}, 0, None

    def trial(shot, phase, family):
        nonlocal count, best
        shot = clip(shot)
        if shot in cache:
            return cache[shot]
        records = []
        for seed in range(required_seed_successes):
            if elapsed() >= budget_seconds or count >= max_calls:
                return None
            record = evaluate(shot, seed, phase)
            count += 1
            records.append(record)
            if record["task_failure"] is not None:
                break
        item = {"shot":shot, "loss":max(search_loss(r,scene["selection"]) for r in records),
                "success":len(records)==required_seed_successes and all(r["task_failure"] is None for r in records),
                "family":family, "phase":phase}
        cache[shot] = item
        if best is None or item["loss"]<best["loss"]:
            best = item
        return item

    def result(item=None):
        diagnostics.update(search_physics_calls=count, evaluated_candidates=len(cache),
                           retained_count=len(diagnostics["proposals"]), best_loss=None if best is None else best["loss"],
                           best_effort_shot=None if best is None else list(best["shot"]))
        if item:
            phase="initial" if item["phase"] in ("quick_initial","geometry_initial") else "refinement"
            diagnostics[phase+"_success"]=True
            diagnostics[phase+"_three_seed_success"]=required_seed_successes==3
            status="FOUND_ON_THREE_OBSERVED_SEEDS" if required_seed_successes==3 else "FOUND_ON_%d_OBSERVED_SEEDS" % required_seed_successes
            return [{"status":status,"bestshot":list(item["shot"])}], diagnostics
        return [{"status":"NOT_FOUND_WITHIN_BUDGET"}], diagnostics

    candidates = []
    for proposal in quick_initials(scene):
        diagnostics["proposals"].append(proposal)
        item = trial(proposal["shot"], "quick_initial", proposal["family"])
        if item is None:
            return result()
        candidates.append(item)
        if item["success"]:
            return result(item)
    start = time.perf_counter()
    proposals, generated = geometric_initials(scene, elapsed=elapsed, deadline=min(budget_seconds, elapsed()+1.5))
    diagnostics.update(initial_generation_ms=(time.perf_counter()-start)*1000, generated_count=generated)
    conservative = [p for p in proposals if p["proxy_valid"]][:6]
    conservative_evaluations = []
    for proposal in conservative:
        diagnostics["proposals"].append(proposal)
        item = trial(proposal["shot"], "geometry_initial", proposal["family"])
        if item is None:
            return result()
        candidates.append(item)
        conservative_evaluations.append(item)
        if item["success"]:
            return result(item)
    from planning_proxy.tactical_library_strategy.double_mads_solver import _mads_directions
    # Preserve both old local entrances, including distinct speeds with the
    # same impact/spin family. Additional weak proposals must not displace them.
    parents = [{"current":c,"mesh":1.} for c in sorted(conservative_evaluations,key=lambda c:c["loss"])[:2]]
    if initial_polish:
        polish_start=count
        for parent in parents:
            current,best_trial=parent["current"],parent["current"]
            for direction in ((0.,1.,0.),(0.,-1.,0.),(1.,0.,0.),(-1.,0.,0.),(0.,0.,1.),(0.,0.,-1.)):
                shot=tuple(current["shot"][i]+(.12,.03,.4)[i]*direction[i] for i in range(3))
                item=trial(shot,"initial_polish",current["family"])
                diagnostics["initial_polish_physics_calls"]=count-polish_start
                if item is None:
                    return result()
                candidates.append(item)
                if item["success"]:
                    return result(item)
                if item["loss"]<best_trial["loss"]:
                    best_trial=item
            parent["current"]=best_trial
    conservative_deadline = (.5 if refinement_profile=="fast_poll" else .75)*budget_seconds
    conservative_call_limit = min(max_calls,64) if refinement_profile=="fast_poll" else max_calls
    diagnostics["conservative_deadline_seconds"] = conservative_deadline
    diagnostics["conservative_call_limit"] = conservative_call_limit
    for iteration in range(conservative_rounds):
        if elapsed() >= conservative_deadline or count>=conservative_call_limit:
            break
        for parent in parents:
            diagnostics["conservative_iterations"] += 1
            current, best_trial = parent["current"], parent["current"]
            directions=_mads_directions(iteration)
            step=(.12,.12,1.6)
            if refinement_profile=="fast_poll":
                directions=[(0.,1.,0.),(0.,-1.,0.),(1.,0.,0.),(-1.,0.,0.),(0.,0.,1.),(0.,0.,-1.)]+directions[:2]
                step=(.12,.06,.8)
            for direction in directions:
                if elapsed() >= conservative_deadline or count>=conservative_call_limit:
                    break
                shot = tuple(current["shot"][i]+parent["mesh"]*step[i]*float(direction[i]) for i in range(3))
                item = trial(shot,"conservative_refine",current["family"])
                if item is None:
                    return result()
                if item["success"]:
                    return result(item)
                if item["loss"] < best_trial["loss"]:
                    best_trial = item
                    if refinement_profile=="fast_poll":
                        break
            if best_trial["loss"] < current["loss"]:
                parent["current"] = best_trial
                parent["mesh"] = min(1.,parent["mesh"]*1.5)
            else:
                parent["mesh"] *= .5
        if all(p["mesh"]<1./16 for p in parents):
            break
    # The remaining budget adds route coverage instead of spending all of it
    # in a screened-out or already exhausted basin.
    for proposal in proposals:
        if tuple(proposal["shot"]) in cache:
            continue
        diagnostics["proposals"].append(proposal)
        item = trial(proposal["shot"],"geometry_initial",proposal["family"])
        if item is None:
            return result()
        candidates.append(item)
        if item["success"]:
            return result(item)
    candidates += [p["current"] for p in parents]
    ranked = sorted(candidates,key=lambda c:c["loss"])
    chosen = ranked[:2]
    for item in ranked[2:]:
        if all(item["family"]!=other["family"] for other in chosen):
            chosen.append(item)
            break
    parents = [{"current":item,"mesh":1.} for item in chosen]
    diagnostics["branch_count"] = len(parents)
    for iteration in range(local_rounds):
        for parent in parents:
            diagnostics["local_iterations"] += 1
            current = parent["current"]
            improved = False
            # Horizontal correction is cheap and often fixes impact position.
            directions = [(0.,1.,0.),(0.,-1.,0.),(1.,0.,0.),(-1.,0.,0.),(0.,0.,1.),(0.,0.,-1.)]
            directions += list(_mads_directions(iteration)[:2])
            step = (.12,.06,.8)
            for direction in directions:
                shot = tuple(current["shot"][i]+parent["mesh"]*step[i]*float(direction[i]) for i in range(3))
                item = trial(shot,"local_refine",current["family"])
                if item is None:
                    return result()
                if item["success"]:
                    return result(item)
                if item["loss"] < current["loss"]:
                    parent["current"] = item
                    parent["mesh"] = min(1., parent["mesh"]*1.5)
                    improved = True
                    break
            if not improved:
                parent["mesh"] *= .5
        if all(p["mesh"]<1./32 for p in parents):
            break
    return result()


class BudgetedDoubleSolver:
    """Reusable online entry: initial board + full goal -> certified action.

    Construct once to keep native scene startup outside subsequent requests.
    A miss returns no executable action; best_effort is diagnostic only.
    """
    def __init__(self, environment=None):
        from training_research.inverse_dataset.cli import make_environment
        self.environment = make_environment() if environment is None else environment

    def solve(self, scene, *, budget_seconds=10.0, seed=20261004,
              max_calls=128, conservative_rounds=8, local_rounds=16, refinement_profile="baseline", initial_polish=False,
              required_seed_successes=1):
        from training_research.inverse_dataset.sampling import validate_scene
        from training_research.inverse_dataset.cli import reset_environment
        from training_research.inverse_dataset.selection import failure_reason
        from planning_proxy.competition_rules import RuleBoardStone, free_guard_rule_violations
        if not math.isfinite(budget_seconds) or budget_seconds<=0:
            raise ValueError("budget_seconds must be positive and finite")
        scene = validate_scene(scene)
        if scene["selection"]["tactic"] != "double_hit":
            raise ValueError("this entry currently supports double_hit only")
        env, records = self.environment, []
        started = time.perf_counter()
        def evaluate(shot, seed_index, phase):
            physics_seed = int(seed) + scene["active_index"]*7919 + 104729*seed_index
            before = reset_environment(env,scene,physics_seed)
            output = env.play(shot)
            initial_rules = [RuleBoardStone(s["index"],"self" if s["index"]%2 == scene["active_index"]%2 else "opponent",s["x"],s["y"])
                             for s in before if s["enabled"]]
            record = {"shot":list(shot),"physics_seed":physics_seed,"seed_index":seed_index,"search_phase":phase,
                      "initial_state":before,"status":"complete","physical_final":output["states"],
                      "prediction":{k:v for k,v in output.items() if k!="states"},
                      "collision_events":list(env.scene._dataset_collision_events),
                      "rule_violations":free_guard_rule_violations(initial_rules,output["states"],shot_index=scene["active_index"])}
            record["task_failure"] = failure_reason(record,scene["selection"])
            records.append(record)
            return record
        attempts, diagnostics = solve(scene,evaluate=evaluate,elapsed=lambda:time.perf_counter()-started,budget_seconds=budget_seconds,
                                      max_calls=max_calls,conservative_rounds=conservative_rounds,local_rounds=local_rounds,
                                      refinement_profile=refinement_profile,initial_polish=initial_polish,
                                      required_seed_successes=required_seed_successes)
        shot = attempts[0].get("bestshot")
        return {"status":attempts[0]["status"],"shot":shot,"success":shot is not None,
                "elapsed_ms":(time.perf_counter()-started)*1000,"budget_seconds":budget_seconds,
                "physics_calls":len(records),"diagnostics":diagnostics,"records":records,
                "required_seed_successes":required_seed_successes,
                "scope":"configured search-seed observations; robustness evaluated separately; no saved solved-action warm start"}
