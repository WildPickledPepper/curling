"""Finite-difference terminal fitting, accepted only by the exact simulator."""
import math
import numpy as np

from training_research.inverse_dataset.schema import HOUSE_X, HOUSE_Y, HOUSE_R, STONE_R


def residual(record, selection, *, center=False, margin=1.):
    board = {s["index"]: s for s in record["physical_final"]}
    values = []
    for key, goal in sorted(selection["goal"]["stones"].items(), key=lambda p: int(p[0])):
        s = board[int(key)]
        kind = goal["type"]
        if kind == "IN_REGION":
            dx, dy = s["x"]-goal["x"], s["y"]-goal["y"]
            d = math.hypot(dx, dy)
            excess = (1./goal["radius"] if center else max(0., d-margin*goal["radius"])/max(d, 1e-12)/goal["radius"])
            values.extend((dx*excess, dy*excess, 10. if not s["enabled"] else 0.))
        elif kind == "OUT_OF_PLAY":
            distance = max(0., min(s["x"]-.145, 4.605-s["x"], s["y"], 10.525-s["y"]))
            values.append(math.sqrt(10.+distance) if s["enabled"] else 0.)
        elif kind == "OUT_OF_HOUSE":
            d = math.hypot(s["x"]-HOUSE_X, s["y"]-HOUSE_Y)
            house_margin = max(0., HOUSE_R+STONE_R-d)
            values.append(math.sqrt(10.+house_margin) if s["enabled"] and d <= HOUSE_R+STONE_R else 0.)
        elif kind == "SURVIVE":
            values.append(0. if s["enabled"] else 10.)
    contacts = set(record["prediction"].get("firstContactTargets", []))
    values.append(10. if selection.get("require_no_contact") and record["prediction"].get("contact") else 0.)
    values.append(10. if "first_contact_any" in selection and (not contacts or not contacts <= set(selection["first_contact_any"])) else 0.)
    values.append(10. if selection.get("require_single_first_contact") and len(contacts) != 1 else 0.)
    pairs = {frozenset(e["stones"]) for e in record["collision_events"]}
    values.extend(10. if frozenset(p) not in pairs else 0. for p in selection.get("required_collision_pairs", []))
    values.append(math.sqrt(1000.) if record.get("rule_violations") or not record["prediction"].get("settled") else 0.)
    return np.asarray(values, dtype=float)


def fit(current, trial, selection, *, iterations=4, allowance=24):
    """Trust-limited Gauss-Newton proposals plus backtracking and exact checks."""
    scale = np.array((.12, .06, .8))
    damping = .05
    used = 0
    for iteration in range(iterations):
        if used+4 > allowance: break
        origin = current
        r = residual(origin["record"], selection, margin=.8)
        raw_origin = residual(origin["record"], selection, center=True)
        columns = []
        for axis in range(3):
            step = (.04, .025, .10)[axis] * (1. if iteration % 2 == 0 else -1.)
            shot = np.asarray(origin["shot"]).copy()
            if axis == 0 and shot[axis] >= 5.99: step = -abs(step)
            shot[axis] += scale[axis]*step
            item = trial(shot, "terminal_jacobian"); used += 1
            if item is None: return current, None
            if item["success"]: return item, item
            actual = (item["shot"][axis]-origin["shot"][axis])/scale[axis]
            columns.append((residual(item["record"], selection, center=True)-raw_origin)/actual if abs(actual)>1e-8 else np.zeros_like(r))
            if item["loss"] < current["loss"]: current = item
        jacobian = np.column_stack(columns)
        try:
            move = np.linalg.solve(jacobian.T@jacobian + damping*np.eye(3), -jacobian.T@r)
        except np.linalg.LinAlgError:
            break
        move /= max(1., float(np.max(np.abs(move)))/3.)
        accepted = False
        for alpha in (1., .5, .25):
            if used >= allowance: break
            item = trial(np.asarray(origin["shot"])+scale*move*alpha, "terminal_fit"); used += 1
            if item is None: return current, None
            if item["success"]: return item, item
            if item["loss"] < current["loss"]:
                current = item; accepted = True; break
        damping = max(.0001, damping/3) if accepted else damping*10
        if not accepted and current is origin and damping>5.: break
    return current, False


def simplex_fit(current, trial, *, allowance=24):
    """Joint three-parameter refinement without differentiating contact branches."""
    vertices = [current]
    steps = np.array((.08, .012, .5)) * (.125 if current["loss"] < .1 else 1.)
    used = 0
    for axis in range(3):
        shot = np.asarray(current["shot"]).copy()
        shot[axis] += steps[axis] * (-1. if axis == 0 and shot[axis] > 5.9 else 1.)
        item = trial(shot, "terminal_simplex"); used += 1
        if item is None: return current, None
        if item["success"]: return item, item
        vertices.append(item)
    while used < allowance:
        vertices.sort(key=lambda p: p["loss"])
        if vertices[0]["loss"] < current["loss"]: current = vertices[0]
        center = np.mean([p["shot"] for p in vertices[:3]], axis=0)
        worst = np.asarray(vertices[-1]["shot"])
        reflected = trial(2.*center-worst, "terminal_simplex"); used += 1
        if reflected is None: return current, None
        if reflected["success"]: return reflected, reflected
        if reflected["loss"] < vertices[0]["loss"] and used < allowance:
            expanded = trial(3.*center-2.*worst, "terminal_simplex"); used += 1
            if expanded is None: return current, None
            if expanded["success"]: return expanded, expanded
            vertices[-1] = expanded if expanded["loss"] < reflected["loss"] else reflected
        elif reflected["loss"] < vertices[-2]["loss"]:
            vertices[-1] = reflected
        elif used < allowance:
            contracted = trial(.5*(center+worst), "terminal_simplex"); used += 1
            if contracted is None: return current, None
            if contracted["success"]: return contracted, contracted
            if contracted["loss"] < vertices[-1]["loss"]:
                vertices[-1] = contracted
            else:
                for index in range(1, 4):
                    if used >= allowance: break
                    item = trial(.5*(np.asarray(vertices[0]["shot"])+vertices[index]["shot"]), "terminal_simplex"); used += 1
                    if item is None: return current, None
                    if item["success"]: return item, item
                    vertices[index] = item
    current = min(vertices+[current], key=lambda p: p["loss"])
    return current, False
