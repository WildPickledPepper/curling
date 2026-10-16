"""Experimental general terminal-goal search; exact forward outcomes accept shots.

Free-flight interpolation and contact geometry propose actions only. This does
not modify the physical simulator or use reference actions from sample files.
"""
import math
import time

from training_research.inverse_dataset.schema import HOUSE_X, HOUSE_Y, HOUSE_R, STONE_R, goal_met
from training_research.inverse_initials import path_array, interpolate, clearance


def clip(shot):
    return tuple(round(min(hi,max(lo,float(value))),5) for value,lo,hi in
        zip(shot,(.2,-2.23,-15.7),(6.,2.23,15.7)))


def loss(record,selection):
    """Uncapped terminal residual ranking; acceptance remains exact."""
    from training_research.inverse_terminal_refine import residual
    values=residual(record,selection)
    return float(values @ values)


def proposals(scene,elapsed,budget):
    selection=scene["selection"]; active=scene["active_index"]
    stones={s["index"]:s for s in scene["stones"]}
    goals=selection["goal"]["stones"]
    targets=selection.get("first_contact_any",[])
    if selection.get("require_no_contact"):
        # An observed background removal is a terminal constraint, not an
        # instruction to hit it when the task explicitly forbids contact.
        targets=[]
    elif not targets:
        targets=[i for i,s in stones.items() if str(i) in goals and (goals[str(i)]["type"] in ("OUT_OF_PLAY","OUT_OF_HOUSE") or
            (goals[str(i)]["type"]=="IN_REGION" and math.hypot(s["x"]-goals[str(i)]["x"],s["y"]-goals[str(i)]["y"])>.03))]
    raw=[]
    if not targets and goals.get(str(active),{}).get("type")=="IN_REGION":
        target=goals[str(active)]
        blockers=[(s["x"],s["y"]) for s in stones.values()]
        for w in (0.,3.,-3.,7.,-7.,12.,-12.,15.,-15.):
            if elapsed()>=budget: break
            low,high=2.2,4.
            for _ in range(15):
                if elapsed()>=budget: break
                v=(low+high)/2
                if path_array(v,w)[-1,1]>target["y"]: low=v
                else: high=v
            v=(low+high)/2; path=path_array(v,w); h=target["x"]-float(path[-1,0])
            if abs(h)>2.23: continue
            gap=clearance(path,h,blockers,len(path)-1)
            raw.append((100*max(0.,2*STONE_R+.025-gap)+.001*abs(w),clip((v,h,w)),("draw",w)))
    else:
        for i in targets:
            s=stones[i]
            blockers=[b for j,b in stones.items() if j!=i]
            for v in (6.,5.6,4.8,4.2,3.5):
                for w in (0.,5.,-5.,10.,-10.,15.,-15.):
                    if elapsed()>=budget: return raw
                    state=interpolate(path_array(v,w),s["y"]+2*STONE_R)
                    if state is None: continue
                    for offset in (0.,.10,-.10,.22,-.22):
                        h=s["x"]+offset-float(state[0][0])
                        if abs(h)>2.23: continue
                        # Cheap route ranking, with exact collision validation later.
                        blocked=sum(b["y"]>s["y"]+.2 and abs(b["x"]-(s["x"]+offset))<2*STONE_R for b in blockers)
                        raw.append((10*blocked+.02*abs(w)+abs(offset)+.01*(6-v),clip((v,h,w)),(i,w,v)))
    if not raw:
        from training_research.inverse_goal_fallback import unanchored_proposals
        raw=unanchored_proposals(scene)
    return raw


def solve(scene,*,evaluate,elapsed,budget_seconds=10.,max_calls=256,required_seed_successes=1):
    if budget_seconds<=0 or not math.isfinite(budget_seconds) or max_calls<1 or required_seed_successes<1:
        raise ValueError("invalid search budget")
    cache={}; count=0; best=None
    diag={"required_seed_successes":required_seed_successes,"initial_success":False,"refinement_success":False,
          "max_physics_calls":max_calls,"initial_generation_ms":0.,"solver":"terminal_multistart_atlas_v5"}
    def trial(shot,phase):
        nonlocal count,best
        shot=clip(shot)
        if shot in cache: return cache[shot]
        records=[]
        for seed in range(required_seed_successes):
            if elapsed()>=budget_seconds or count>=max_calls: return None
            r=evaluate(shot,seed,phase); count+=1; records.append(r)
            if r["task_failure"] is not None: break
        item={"shot":shot,"loss":max(loss(r,scene["selection"]) for r in records),"record":records[0],
              "success":len(records)==required_seed_successes and all(r["task_failure"] is None for r in records),"phase":phase}
        cache[shot]=item
        if best is None or item["loss"]<best["loss"]: best=item
        return item
    def result(item=None):
        diag.update(search_physics_calls=count,evaluated_candidates=len(cache),best_loss=best["loss"] if best else None,
                    best_effort_shot=list(best["shot"]) if best else None)
        if item: diag["initial_success" if item["phase"]=="geometry_initial" else "refinement_success"]=True
        return ([{"status":"FOUND_ON_%d_OBSERVED_SEEDS" % required_seed_successes,"bestshot":list(item["shot"])}]
                if item else [{"status":"NOT_FOUND_WITHIN_BUDGET"}]),diag
    start=elapsed()
    raw=sorted(proposals(scene,elapsed,.25*budget_seconds))
    retained=[]; families=set(); shots=set()
    for _,shot,family in raw:
        if shot in shots or family in families: continue
        retained.append(shot); families.add(family); shots.add(shot)
        if len(retained)>=20: break
    collision=not scene["selection"].get("require_no_contact") and bool(scene.get("stones"))
    extra=[]
    if collision:
        from training_research.inverse_contact_initials import contact_initials
        extra=contact_initials(scene,elapsed,min(.3*budget_seconds,elapsed()+.7),clip)
    atlas=[]
    if collision:
        from training_research.inverse_contact_atlas import atlas_initials
        atlas,atlas_sources=atlas_initials(scene,elapsed,min(.3*budget_seconds,elapsed()+.8),clip,limit=8)
        diag["atlas_sources"]=atlas_sources
    # Empirical proposals exclude current-board samples; geometry remains fallback.
    pool=retained[:4]+atlas[:4]+retained[4:8]+atlas[4:]
    for index in range(max(len(extra),len(retained[8:]))):
        if index<len(extra): pool.append(extra[index])
        if index<len(retained[8:]): pool.append(retained[8:][index])
    pool=list(dict.fromkeys(pool))
    diag.update(initial_generation_ms=(elapsed()-start)*1000,retained_count=len(pool))
    evaluated=[]; cursor=0
    def initialise(n):
        nonlocal cursor
        for _ in range(n):
            if cursor>=len(pool): break
            item=trial(pool[cursor],"geometry_initial"); cursor+=1
            if item is None: return None
            evaluated.append(item)
            if item["success"]: return item
        return False
    initial=initialise(8)
    if initial is None or initial: return result(initial)
    if not evaluated: return result()
    from training_research.inverse_terminal_refine import fit,simplex_fit
    directions=((0,1,0),(0,-1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),
                (1,1,0),(-1,-1,0),(1,-1,0),(-1,1,0))
    fitted=set(); simplexes=set(); meshes={}; rounds=0; stalled=0
    while elapsed()<budget_seconds and count<max_calls:
        rounds+=1
        round_best=best["loss"]
        # Frequent coverage refresh prevents one failed contact branch consuming the budget.
        if rounds>1 and cursor<len(pool):
            initial=initialise(4)
            if initial is None or initial: return result(initial)
        ordered=sorted(cache.values(),key=lambda i:i["loss"])
        parents=[]
        for candidate in ordered:
            if all(sum(((candidate["shot"][i]-p["shot"][i])/(.12,.06,.8)[i])**2 for i in range(3))>.1 for p in parents):
                parents.append(candidate)
            if len(parents)==2: break
        progress=False
        for parent in parents:
            current=parent
            if current["loss"]<1. and current["shot"] not in simplexes:
                simplexes.add(current["shot"])
                current,success=simplex_fit(current,trial,allowance=22)
                if success is None or success: return result(success)
                progress |= current["loss"]<parent["loss"]
            if current["loss"]<80. and current["shot"] not in fitted:
                fitted.add(current["shot"])
                current,success=fit(current,trial,scene["selection"],iterations=4,allowance=20)
                if success is None or success: return result(success)
                progress |= current["loss"]<parent["loss"]
            key=parent["shot"]; mesh=meshes.get(key, .125 if current["loss"]<1. else 1.)
            start_count=count
            # Opportunistic polling saves calls for more initial contact angles.
            for direction in directions:
                item=trial([current["shot"][i]+mesh*(.12,.06,.8)[i]*direction[i] for i in range(3)],"local_refine")
                if item is None: return result()
                if item["success"]: return result(item)
                if item["loss"]<current["loss"]:
                    current=item; progress=True; break
            improved=current["loss"]<parent["loss"]
            meshes[current["shot"]]=min(1.,mesh*1.5) if improved else mesh*.5
            meshes[key]=meshes[current["shot"]]
        progress=best["loss"]<round_best
        stalled=0 if progress else stalled+1
        if not progress and cursor>=len(pool) and (stalled>=3 or all(meshes.get(p["shot"],1.)<1/512 for p in parents)):
            # Expand different impact branches instead of returning an early local failure.
            seed=ordered[(rounds//len(directions))%min(12,len(ordered))]["shot"]
            def fraction(n,base):
                value=0.; denominator=1.
                while n:
                    denominator*=base; value+=(n%base)/denominator; n//=base
                return value
            radius=(.35,.18,2.4) if rounds%3 else (.7,.28,4.8)
            item=trial([seed[i]+radius[i]*(2*fraction(rounds,(2,3,5)[i])-1) for i in range(3)],"branch_restart")
            if item is None: return result()
            if item["success"]: return result(item)
        if rounds>=1024: break
    diag["search_rounds"]=rounds
    return result()
