"""Procedural variations of hand-authored tactical layouts.

Geometry and parameter ranges are sampling proposals, never inverse-physics
solutions. Every variant must receive fresh forward simulations and labels.
"""
from __future__ import annotations

import copy
import math

from .sampling import task_rng, validate_scene
from .schema import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R, digest

TASK_FAMILIES = ("draw_button", "draw_top4", "center_guard", "corner_guard",
                 "takeout", "hit_and_stay", "hit_roll", "peel_guard",
                 "double_hit", "freeze", "raise_takeout", "around_guard_draw")


def region(x, y, radius):
    return {"type": "IN_REGION", "x": x, "y": y, "radius": radius, "required": True}


def base_board(family, layout, seed, max_background):
    rng = task_rng(seed, "task-layout", family, layout)
    active = rng.randint(6, 15)
    own = [i for i in range(active) if i % 2 == active % 2]
    opponent = [i for i in range(active) if i % 2 != active % 2]
    rng.shuffle(own)
    rng.shuffle(opponent)
    target, second, middle = opponent[0], opponent[1], own[0]
    x, y = rng.uniform(1.2, 3.55), rng.uniform(4.05, 5.65)
    radius = rng.choice((.20, .35, .50))
    stones, goals = [], {}
    selection = {"tactic": family, "goal": {"stones": goals}}
    def put(index, px, py):
        stones.append({"index": index, "x": px, "y": py, "yaw": rng.uniform(-math.pi, math.pi)})
    def first(index):
        selection.update(first_contact_any=[index], require_single_first_contact=True)
    def clear(index, kind="OUT_OF_HOUSE"):
        goals[str(index)] = {"type": kind, "required": True}
    speed = [2.4, 3.8]
    aim_x = x
    spin = [-1., 1.] if layout % 3 else [-15.7, 15.7]
    if family in ("draw_button", "draw_top4", "center_guard", "corner_guard", "around_guard_draw"):
        selection["require_no_contact"] = True
        if family == "draw_button":
            x, y = HOUSE_X + rng.uniform(-.25, .25), HOUSE_Y + rng.uniform(-.25, .25)
        elif family == "draw_top4":
            x, y = HOUSE_X + rng.uniform(-.4, .4), HOUSE_Y + rng.uniform(.2, .6)
        elif family == "center_guard":
            x, y = HOUSE_X + rng.uniform(-.10, .10), rng.uniform(7.15, 9.1)
            selection["tactic"] = "center_guard_high" if y > 8. else "center_guard_low"
        elif family == "corner_guard":
            left = rng.choice((True, False))
            x, y = rng.uniform(.8, 1.6) if left else rng.uniform(3.15, 3.95), rng.uniform(7.0, 8.9)
            selection["tactic"] = "corner_guard_left" if left else "corner_guard_right"
        else:
            x, y = rng.uniform(1.65, 3.1), rng.uniform(4.3, 5.4)
            gx, gy = x + rng.uniform(-.12, .12), rng.uniform(7.2, 8.6)
            put(target, gx, gy)
            goals[str(target)] = region(gx, gy, .10)
            selection["tactic"] = "around_guard_draw_left" if layout % 2 == 0 else "around_guard_draw_right"
            spin = [-15.7, 15.7]
        goals[str(active)] = region(x, y, radius)
        aim_x = x
        if "guard" in family and family != "around_guard_draw":
            speed = [2.4, 3.4]
    else:
        put(target, x, y)
        first(target)
        clear(target)
        speed = [3.7, 6.]
        if family == "takeout":
            selection["tactic"] = "take_out_house"
            clear(target, "OUT_OF_PLAY" if layout % 2 else "OUT_OF_HOUSE")
        elif family == "hit_and_stay":
            goals[str(active)] = region(x, y, radius)
        elif family == "hit_roll":
            direction = -1 if layout % 2 == 0 else 1
            selection["tactic"] = "hit_roll_left" if direction == -1 else "hit_roll_right"
            goals[str(active)] = region(x + direction * rng.uniform(.4, .8), y + rng.uniform(-.3, .3), radius)
        elif family == "peel_guard":
            y = rng.uniform(7.25, 9.05)
            stones[0]["y"] = y
            clear(target, "OUT_OF_PLAY")
            clear(active, "OUT_OF_PLAY")
        elif family == "double_hit":
            # Deliberately cover both offset close pairs and longer runbacks.
            dx = rng.uniform(-.55, .55)
            dy = rng.uniform(.34, .85) if layout % 2 == 0 else rng.uniform(.9, 1.8)
            # Keep both initially in the house; reject invalid geometry below.
            y = rng.uniform(3.7, 4.8)
            stones[0]["y"] = y
            put(second, x + dx, y + dy)
            if math.hypot(x + dx - HOUSE_X, y + dy - HOUSE_Y) > HOUSE_R + STONE_R - .12:
                raise ValueError("double front target outside house")
            clear(second, "OUT_OF_PLAY" if layout % 3 == 0 else "OUT_OF_HOUSE")
            clear(target, "OUT_OF_PLAY" if layout % 3 == 0 else "OUT_OF_HOUSE")
            selection.update(first_contact_any=[target, second], required_collision_pairs=[[target, second]])
            aim_x = x + dx
            speed = [4.5, 6.]
        elif family == "freeze":
            # A geometric frozen-position request with a protected target.
            goals[str(target)] = region(x, y, .10)
            goals[str(active)] = region(x, y + 2 * STONE_R + .02, .12)
            selection.pop("first_contact_any")
            selection.pop("require_single_first_contact")
            speed = [2.4, 3.8]
        elif family == "raise_takeout":
            mx, my = x + rng.uniform(-.12, .12), y + rng.uniform(.45, 1.5)
            put(middle, mx, my)
            first(middle)
            selection["required_collision_pairs"] = [[middle, target]]
            aim_x = mx
            speed = [4.2, 6.]
    used = {s["index"] for s in stones}
    remaining = [i for i in range(active) if i not in used]
    rng.shuffle(remaining)
    background_count = min(len(remaining), rng.randint(1 if max_background else 0, max_background))
    # Mix sparse and crowded boards. Do not assume background stones inert.
    for index in remaining[:background_count]:
        for _ in range(200):
            px, py = rng.uniform(.55, 4.20), rng.uniform(2.1, 9.7)
            if all(math.hypot(px-s["x"], py-s["y"]) >= .36 for s in stones) and all(
                    math.hypot(px-g["x"], py-g["y"]) >= .36 for g in goals.values() if g["type"] == "IN_REGION"):
                put(index, px, py)
                break
        else:
            raise ValueError("unable to place background stone")
    if stones and layout % 2:
        protected = [s for s in stones if s["index"] % 2 == active % 2 and s["index"] != middle]
        if protected:
            chosen = rng.choice(protected)
            goals[str(chosen["index"])] = region(chosen["x"], chosen["y"], .15)
    h_center = aim_x - HOUSE_X
    return {"scene_id": f"task-{family}-{layout:06d}", "family": family, "active_index": active, "stones": stones,
            "selection": selection, "shot_bounds": {"v": speed, "h": [max(-2.23, h_center-.45), min(2.23, h_center+.45)], "w": spin},
            "layout": {"generator": "task_boards_v1", "family": family, "layout_index": layout, "seed": seed,
                       "background_stones": len(stones)-len(used)}}


def task_boards(layouts_per_family, variants_per_layout, seed=20261004, max_background=8, families=TASK_FAMILIES):
    if layouts_per_family < 1 or variants_per_layout < 1 or not 0 <= max_background <= 13 or not families or any(f not in TASK_FAMILIES for f in families):
        raise ValueError("invalid task-board generation configuration")
    scenes = []
    for family in families:
        for layout in range(layouts_per_family):
            # Deterministic retries for boundary/overlap violations.
            for attempt in range(100):
                try:
                    case_seed = int(digest([seed, family, layout, attempt])[:12], 16)
                    base = base_board(family, layout, case_seed, max_background)
                    validate_scene(base)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError("could not generate valid layout")
            group = digest(["task-layout-v1", seed, family, layout])
            for variant in range(variants_per_layout):
                for attempt in range(100):
                    rng = task_rng(seed, family, layout, "variant", variant, attempt)
                    scene = copy.deepcopy(base)
                    dx, dy = (0., 0.) if variant == 0 else (rng.uniform(-.08, .08), rng.uniform(-.08, .08))
                    for stone in scene["stones"]:
                        stone["x"] += dx
                        stone["y"] += dy
                    for goal in scene["selection"]["goal"]["stones"].values():
                        if goal["type"] == "IN_REGION":
                            goal["x"] += dx
                            goal["y"] += dy
                    scene["shot_bounds"]["h"] = [max(-2.23, h+dx) for h in scene["shot_bounds"]["h"]]
                    scene["scene_id"] += f"-v{variant:03d}"
                    scene["group_id"] = group
                    scene["layout"].update(variant_index=variant, translation=[dx, dy], request_seed=seed)
                    try:
                        scenes.append(validate_scene(scene))
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError("could not generate valid variant")
    return scenes
