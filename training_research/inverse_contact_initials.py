"""Goal-directed contact proposals, not a replacement collision simulator."""
import math

from training_research.inverse_dataset.schema import STONE_R
from training_research.inverse_initials import path_array, interpolate


def contact_initials(scene, elapsed, deadline, clip):
    goals = scene["selection"]["goal"]["stones"]
    stones = {s["index"]: s for s in scene["stones"]}
    explicit = scene["selection"].get("first_contact_any")
    targets = explicit or [i for i, s in stones.items() if str(i) in goals and
        (goals[str(i)]["type"] in ("OUT_OF_PLAY", "OUT_OF_HOUSE") or
         (goals[str(i)]["type"] == "IN_REGION" and math.hypot(s["x"]-goals[str(i)]["x"], s["y"]-goals[str(i)]["y"])>.03))]
    raw = []
    active_goal = goals.get(str(scene["active_index"]), {})
    for i in targets:
        s, goal = stones[i], goals[str(i)]
        directed = []
        distance = 0.
        if goal["type"] == "IN_REGION":
            dx, dy = goal["x"]-s["x"], goal["y"]-s["y"]
            distance = math.hypot(dx, dy)
            if distance>.03 and dy < -.01:
                theta = math.atan2(dy, dx)
                directed = [(math.cos(theta+a), math.sin(theta+a), a) for a in (0., -.18, .18)]
        # Retain left/right glancing contacts even when the terminal goal is removal.
        normals = directed + [(math.sin(a), -math.cos(a), a) for a in (0., -.35, .35, -.7, .7, -1., 1.)]
        for geometry, (nx, ny, turn) in enumerate(normals):
            if ny >= -.03: continue
            aim_x, aim_y = s["x"]-2*STONE_R*nx, s["y"]-2*STONE_R*ny
            for v in (3., 3.5, 4.2, 4.8, 5.6, 6.):
                for w in (0., 5., -5., 10., -10., 15., -15.):
                    if elapsed()>=deadline: break
                    path = path_array(v, w)
                    state = interpolate(path, aim_y)
                    if state is None: continue
                    state = state[0]
                    h = aim_x-float(state[0])
                    if abs(h)>2.23: continue
                    incoming = float(state[2]), float(state[3])
                    normal_speed = incoming[0]*nx+incoming[1]*ny
                    if normal_speed <= 0.: continue
                    blocked = sum(b["y"]>aim_y+.2 and abs(b["x"]-aim_x)<2*STONE_R for j, b in stones.items() if j != i)
                    score = 8.*blocked+.008*abs(w)
                    if geometry < len(directed):
                        # Range/energy proxy inferred from this recovered mean free path.
                        speed2 = incoming[0]**2+incoming[1]**2
                        free_range = max(.05, math.hypot(float(path[-1,0])-float(state[0]), float(path[-1,1])-float(state[1])))
                        transferred_range = free_range*normal_speed**2/max(speed2, 1e-9)
                        score += abs(math.log(max(.03, transferred_range)/max(.03, distance)))+.5*abs(turn)
                    else:
                        score += .7+.02*(6.-v)+.15*abs(turn)
                    if active_goal.get("type") == "IN_REGION":
                        tx, ty = incoming[0]-normal_speed*nx, incoming[1]-normal_speed*ny
                        gx, gy = active_goal["x"]-aim_x, active_goal["y"]-aim_y
                        length = math.hypot(tx, ty)*math.hypot(gx, gy)
                        if length > .01: score += .3*(1.-(tx*gx+ty*gy)/length)
                    raw.append((score, clip((v,h,w)), (i,geometry,w)))
    result = []; families = set(); shots = set()
    for _, shot, family in sorted(raw):
        if family in families or shot in shots: continue
        result.append(shot); families.add(family); shots.add(shot)
        if len(result)==24: break
    return result
