"""Continuous goal-directed contact aims, used only to propose candidates.

Circle tangency and target displacement are geometric approximations. They
neither change PhysX nor establish a collision mechanism or success predicate.
"""
from __future__ import annotations

import math


def goal_normals(scene, first, turns=(0., -.08, .08, -.2, .2)):
    stones = {s["index"]: s for s in scene["stones"]}
    target = stones[first]
    goals = scene["selection"]["goal"]["stones"]
    active_goal = goals.get(str(scene["active_index"]), {})
    base = []
    radius = .29
    if active_goal.get("type") == "IN_REGION":
        gx, gy = active_goal["x"]-target["x"], active_goal["y"]-target["y"]
        distance = math.hypot(gx, gy)
        if distance > radius+.001:
            ux, uy = gx/distance, gy/distance
            cosine = -radius/distance
            sine = math.sqrt(max(0., 1.-cosine*cosine))
            for sign in (-1., 1.):
                nx, ny = cosine*ux-sign*sine*uy, cosine*uy+sign*sine*ux
                if ny < -.02:
                    base.append((nx, ny, "active_tangent"))
    goal = goals.get(str(first), {})
    if goal.get("type") == "IN_REGION":
        dx, dy = goal["x"]-target["x"], goal["y"]-target["y"]
        distance = math.hypot(dx, dy)
        if distance > .1 and dy < 0.:
            base.append((dx/distance, dy/distance, "target_displacement"))
    result = []
    for nx, ny, kind in base:
        for turn in turns:
            x, y = nx*math.cos(turn)-ny*math.sin(turn), nx*math.sin(turn)+ny*math.cos(turn)
            if y < -.02:
                result.append((x, y, turn, kind))
    return result


def proposals(scene, original_pool, elapsed, deadline, clip, limit=20):
    from training_research.inverse_initials import path_array, interpolate
    stones = {s["index"]: s for s in scene["stones"]}
    targets = scene["selection"].get("first_contact_any", [])
    velocity_pairs = list(dict.fromkeys((float(v), float(w)) for v, h, w in original_pool))
    velocity_pairs = velocity_pairs[:4]+[(5.5, .8), (5.5, -.8)]+velocity_pairs[4:10]+[(5., .8), (5., -.8)]
    raw = []
    for first in targets:
        if first not in stones:
            continue
        target = stones[first]
        for nx, ny, turn, kind in goal_normals(scene, first):
            aim = target["x"]-.29*nx, target["y"]-.29*ny
            for rank, (v, w) in enumerate(velocity_pairs):
                if elapsed() >= deadline:
                    break
                state = interpolate(path_array(v, w), aim[1])
                if state is None:
                    continue
                state = state[0]
                if state[2]*nx+state[3]*ny <= 0.:
                    continue
                h = aim[0]-float(state[0])
                if abs(h) <= 2.23:
                    priority = rank if turn == 0. else 4.+.5*rank+10.*abs(turn)
                    raw.append((priority+(.3 if kind=="target_displacement" else 0.),
                                clip((v, h, w))))
    return list(dict.fromkeys(shot for _, shot in sorted(raw)))[:limit]


def chain_proposals(scene, original_pool, elapsed, deadline, clip, limit=24):
    """Use other requested moving stones as possible intermediate contacts.

    Two approximate routes are considered: the first target travels toward a
    second stone, or the shooter glances off the first toward that stone. Only
    request geometry is used; actual collision chains remain forward-validated.
    """
    from training_research.inverse_initials import path_array, interpolate
    stones = {s["index"]: s for s in scene["stones"]}
    goals = scene["selection"]["goal"]["stones"]
    pairs = list(dict.fromkeys((float(v), float(w)) for v, h, w in original_pool))
    pairs = pairs[:8]+[(5.5, .8), (5.5, -.8), (5., 5.), (5., -5.)]
    raw = []
    for first in scene["selection"].get("first_contact_any", []):
        target = stones.get(first)
        if target is None:
            continue
        candidates = []
        for index, other in stones.items():
            if index == first:
                continue
            goal = goals.get(str(index), {})
            moving = goal.get("type") in ("OUT_OF_PLAY", "OUT_OF_HOUSE") or (
                goal.get("type") == "IN_REGION" and math.hypot(goal["x"]-other["x"], goal["y"]-other["y"]) > .15)
            if not moving:
                continue
            # Aim the first target toward the second stone or toward an offset
            # on its contact circle suggested by its requested displacement.
            aims = [(other["x"], other["y"])]
            if goal.get("type") == "IN_REGION":
                dx, dy = goal["x"]-other["x"], goal["y"]-other["y"]
                distance = math.hypot(dx, dy)
                if distance > .15:
                    aims.insert(0, (other["x"]-.29*dx/distance, other["y"]-.29*dy/distance))
            for x, y in aims:
                dx, dy = x-target["x"], y-target["y"]
                length = math.hypot(dx, dy)
                if length > .29 and dy < -.02:
                    candidates.append((dx/length, dy/length, "target_to_next"))
            # The pseudo-goal affects proposal geometry only, never acceptance.
            pseudo = {**scene, "selection": {**scene["selection"], "goal": {"stones": {
                str(scene["active_index"]): {"type": "IN_REGION", "x": other["x"], "y": other["y"]}}}}}
            candidates.extend((nx, ny, "shooter_to_next") for nx, ny, _, _ in goal_normals(pseudo, first, turns=(0.,)))
        for geometry, (nx, ny, kind) in enumerate(candidates):
            for rank, (v, w) in enumerate(pairs):
                if elapsed() >= deadline:
                    break
                state = interpolate(path_array(v, w), target["y"]-.29*ny)
                if state is None or state[0][2]*nx+state[0][3]*ny <= 0.:
                    continue
                h = target["x"]-.29*nx-float(state[0][0])
                if abs(h) <= 2.23:
                    raw.append((rank+.5*geometry+(.1 if kind=="shooter_to_next" else 0.), clip((v, h, w))))
    return list(dict.fromkeys(s for _, s in sorted(raw)))[:limit]
