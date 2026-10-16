"""Archived mathematical double seeds, validated by the current simulator.

The archived geometry and trajectory proposal code is loaded unchanged under
private names. It uses the current recovered free-motion kernel, never the old
physics scene. The small MADS-style adapter below uses today's complete goal
and collision observations; it is not a reproduction of the old score contract.
"""
from __future__ import annotations

from functools import lru_cache
import importlib.util
import math
from pathlib import Path
import sys
import time

from training_research.inverse_dataset.schema import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = Path(__file__).resolve().parent / "legacy_support"
SOURCE_FILES = tuple(ARCHIVE / p for p in (
    "local_simulator/double_geometry.py",
    "local_simulator/curling_tactic_search.py",
    "local_simulator/curling_solver/seeds.py",
    "local_simulator/curling_solver/search.py",
    "ppo_framework/tactic_targets.py",
    "tacticslib/base_library.py",
    "tacticslib/strategy_library.py",
    "tacticslib/data/data.json",
))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses resolve their defining module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


@lru_cache(maxsize=1)
def legacy_modules():
    # Temporary aliases resolve the archive's absolute imports without putting
    # the archived local_simulator package ahead of the current strict engine.
    names = ("local_simulator.double_geometry", "base_library", "strategy_library")
    previous = {name: sys.modules.get(name) for name in names}
    previous_path = sys.path[:]
    try:
        geometry = _load("training_research._legacy_double_geometry", SOURCE_FILES[0])
        sys.modules[names[0]] = geometry
        search = _load("training_research._legacy_tactic_search", SOURCE_FILES[1])
        base = _load("training_research._legacy_base_library", SOURCE_FILES[5])
        sys.modules[names[1]] = base
        strategy = _load("training_research._legacy_strategy_library", SOURCE_FILES[6])
        sys.modules[names[2]] = strategy
        targets = _load("training_research._legacy_tactic_targets", SOURCE_FILES[4])
        return search, targets
    finally:
        sys.path[:] = previous_path
        for name, module in previous.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def double_initials(scene):
    """Same two-order V2 + legacy proposals and six-seed cap as old PPO."""
    search, target_library = legacy_modules()
    position = [0.] * 32
    for stone in scene["stones"]:
        i = int(stone["index"])
        position[2*i:2*i+2] = [stone["x"], stone["y"]]
    first, second = sorted(scene["selection"]["first_contact_any"])
    before = search._relative_free_flight.cache_info()._asdict()
    candidates = []
    for a, b in ((first, second), (second, first)):
        candidates.extend(search.search_double_hit_geometry(
            position, first_index=a, second_index=b,
            geometry_samples=144, geometry_limit=6, limit=8,
        ))
    candidates.sort(key=lambda item: item.score)
    proposals = [{"shot": list(c.shot), "source": "double_geometry_v2_%d" % i,
                  "score": c.score, "virtual_aim": list(c.geometry.virtual_aim_point),
                  "first_target_position": list(c.geometry.first_point),
                  "blocker_clearance": c.blocker_clearance if math.isfinite(c.blocker_clearance) else None}
                 for i, c in enumerate(candidates[:12])]
    legacy = target_library.bestshot_for_double(
        position, action_name="double_hit", player_is_first=scene["active_index"] % 2 == 0,
        target_index=first, second_target_index=second,
    )
    if legacy is not None:
        proposals.append({"shot": list(legacy), "source": "double_legacy"})
    unique, seen = [], set()
    for item in proposals:
        shot = clip(item["shot"])
        if shot not in seen:
            seen.add(shot)
            unique.append({**item, "shot": list(shot)})
        if len(unique) == 6:
            break
    return unique, {"generated_count": len(proposals), "retained_count": len(unique),
                    "free_flight_cache_before": before,
                    "free_flight_cache_after": search._relative_free_flight.cache_info()._asdict()}


def clip(shot):
    return tuple(round(min(hi, max(lo, float(x))), 5)
                 for x, lo, hi in zip(shot, (1., -2.23, -10.), (6., 2.23, 10.)))


def search_loss(record, selection):
    """Optimization ranking only. Acceptance always uses failure_reason()."""
    from local_simulator.unity_physx import UNITY_RETAINED_PROTOCOL_X, UNITY_RETAINED_PROTOCOL_Y
    from training_research.inverse_dataset.schema import goal_met
    board = {int(s["index"]): s for s in record["physical_final"]}
    failed, distance = 0, 0.
    for key, goal in selection["goal"]["stones"].items():
        stone = board[int(key)]
        if goal_met(record["physical_final"], {"stones": {key: goal}}):
            continue
        failed += 1
        kind = goal["type"]
        if kind == "OUT_OF_PLAY":
            x, y = stone["x"], stone["y"]
            distance += max(0., min(x-UNITY_RETAINED_PROTOCOL_X[0], UNITY_RETAINED_PROTOCOL_X[1]-x,
                                    y-UNITY_RETAINED_PROTOCOL_Y[0], UNITY_RETAINED_PROTOCOL_Y[1]-y))
        elif kind == "OUT_OF_HOUSE":
            distance += max(0., HOUSE_R + STONE_R - math.hypot(stone["x"]-HOUSE_X, stone["y"]-HOUSE_Y))
        elif kind == "IN_REGION":
            distance += max(0., math.hypot(stone["x"]-goal["x"], stone["y"]-goal["y"]) - goal["radius"]) if stone["enabled"] else 20.
        elif kind == "SURVIVE":
            distance += 20.
    contacts = set(record["prediction"].get("firstContactTargets", []))
    failed += int(not contacts or not contacts <= set(selection["first_contact_any"]) or len(contacts) != 1)
    pairs = {frozenset(e["stones"]) for e in record["collision_events"]}
    failed += sum(frozenset(pair) not in pairs for pair in selection["required_collision_pairs"])
    failed += int(not record["prediction"]["settled"] or bool(record["rule_violations"]))
    return failed * 1000. + distance


def solve(scene, *, evaluate, elapsed, budget_seconds, refine=True, max_calls=96):
    """Fail-fast three-seed acceptance; two-branch, six-round local poll."""
    start = time.perf_counter()
    proposals, diagnostics = double_initials(scene)
    diagnostics.update(initial_generation_ms=(time.perf_counter()-start)*1000,
                       proposals=proposals, max_physics_calls=max_calls,
                       local_search="two branches; six rounds; mesh (.12,.12,1.6); exact full-goal loss",
                       initial_three_seed_success=False, refinement_three_seed_success=False)
    cache, call_count = {}, 0
    best = None

    def trial(shot, phase):
        nonlocal call_count, best
        shot = clip(shot)
        if shot in cache:
            return cache[shot]
        records = []
        for seed_index in range(3):
            if elapsed() >= budget_seconds or call_count >= max_calls:
                return None
            record = evaluate(shot, seed_index, phase)
            call_count += 1
            records.append(record)
            if record["task_failure"] is not None:
                break
        item = {"shot": shot, "loss": max(search_loss(r, scene["selection"]) for r in records),
                "success": len(records) == 3 and all(r["task_failure"] is None for r in records), "phase": phase}
        cache[shot] = item
        if best is None or item["loss"] < best["loss"]:
            best = item
        return item

    def result(item=None):
        diagnostics.update(search_physics_calls=call_count, evaluated_candidates=len(cache),
                           best_loss=None if best is None else best["loss"],
                           best_effort_shot=None if best is None else list(best["shot"]))
        return ([{"status": "FOUND_ON_THREE_OBSERVED_SEEDS", "bestshot": list(item["shot"])}]
                if item else [{"status": "NOT_FOUND_WITHIN_LEGACY_SEARCH", "no_initials": not proposals}]), diagnostics

    initial = []
    for proposal in proposals:
        item = trial(proposal["shot"], "legacy_initial")
        if item is None:
            return result()
        initial.append(item)
        if item["success"]:
            diagnostics["initial_three_seed_success"] = True
            return result(item)
    diagnostics["initial_stage_ms"] = elapsed() * 1000
    if not refine or not initial:
        return result()
    branches = [{"current": item, "mesh": 1.} for item in sorted(initial, key=lambda item:item["loss"])[:2]]
    from planning_proxy.tactical_library_strategy.double_mads_solver import _mads_directions
    for iteration in range(6):
        for branch in branches:
            current, best_trial = branch["current"], branch["current"]
            for direction in _mads_directions(iteration):
                shot = tuple(current["shot"][i] + branch["mesh"] * (.12, .12, 1.6)[i] * float(direction[i]) for i in range(3))
                item = trial(shot, "legacy_refine")
                if item is None:
                    return result()
                if item["success"]:
                    diagnostics["refinement_three_seed_success"] = True
                    return result(item)
                if item["loss"] < best_trial["loss"]:
                    best_trial = item
            if best_trial["loss"] < current["loss"]:
                branch["current"] = best_trial
                branch["mesh"] = min(1., branch["mesh"] * 1.5)
            else:
                branch["mesh"] *= .5
        if all(branch["mesh"] < 1./16 for branch in branches):
            break
    return result()
