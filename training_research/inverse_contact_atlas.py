"""Other-board empirical contact seeds. Current physical board is excluded."""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np

from training_research.inverse_dataset.cli import file_sha, write_json

RUNS = Path(__file__).resolve().parent / "runs"
DEFAULT = Path(__file__).resolve().parent / "assets/inverse_contact_atlas_v6_20261004.npz"


def build(output):
    from training_research.build_inverse_sampled_suite import FORWARD_RUNS
    arrays = {k: [] for k in ("scene_key", "record_id", "shot", "first_y", "target_delta", "active_delta",
        "target_live", "active_live", "target_house", "nearby", "stones", "target_yaw", "launch_relative_x", "nearby_final", "nearby_live")}
    sources = {}; checked = 0
    for name in FORWARD_RUNS:
        for path in sorted((RUNS / name / "shards").glob("*.raw.jsonl")):
            sources[str(path.resolve())] = file_sha(path)
            with path.open(encoding="utf-8") as stream:
                for line in stream:
                    r = json.loads(line); checked += 1
                    contacts = r.get("prediction", {}).get("firstContactTargets", [])
                    if r.get("status") != "complete" or r.get("rule_violations") or not r.get("prediction", {}).get("settled") or len(contacts) != 1: continue
                    first, active = contacts[0], r["active_index"]
                    initial = {s["index"]: s for s in r["before"]}
                    final = {s["index"]: s for s in r["physical_final"]}
                    a, b, shooter = initial[first], final[first], final[active]
                    if not a["enabled"]: continue
                    others = sorted((s for i, s in initial.items() if s["enabled"] and i != first), key=lambda s:(s["x"]-a["x"])**2+(s["y"]-a["y"])**2)
                    nearby = [s[k]-a[k] for s in others[:3] for k in ("x", "y")]
                    nearby += [5.] * (6-len(nearby))
                    nearby_final=[final[s["index"]][k]-a[k] if final[s["index"]]["enabled"] else 0. for s in others[:3] for k in ("x","y")]
                    nearby_final += [0.]*(6-len(nearby_final))
                    nearby_live=[bool(final[s["index"]]["enabled"]) for s in others[:3]]
                    nearby_live += [False]*(3-len(nearby_live))
                    values = dict(scene_key=r["scene_key"], record_id=r["record_id"], shot=r["shot"], first_y=a["y"],
                        target_delta=[b["x"]-a["x"], b["y"]-a["y"]] if b["enabled"] else [0.,0.],
                        active_delta=[shooter["x"]-a["x"], shooter["y"]-a["y"]] if shooter["enabled"] else [0.,0.],
                        target_live=bool(b["enabled"]), active_live=bool(shooter["enabled"]),
                        target_house=bool(b["enabled"] and np.hypot(b["x"]-2.375,b["y"]-4.88)<=1.975),
                        nearby=nearby, stones=len(others)+1, target_yaw=a.get("yaw",0.),launch_relative_x=r["shot"][1]-a["x"],nearby_final=nearby_final,nearby_live=nearby_live)
                    for key in arrays: arrays[key].append(values[key])
    packed = {k: np.asarray(v, dtype=str if k in ("scene_key","record_id") else bool if k.endswith("live") or k=="target_house" else float) for k,v in arrays.items()}
    output.parent.mkdir(parents=True, exist_ok=True)
    assert not output.exists()
    np.savez_compressed(output, **packed)
    metadata = {"status":"complete","checked_raw_records":checked,"contact_samples":len(packed["shot"]),
        "distinct_boards":len(set(packed["scene_key"])),"source_policy":"original_forward_samples_only",
        "source_sha256":sources,"atlas_sha256":file_sha(output),"builder_sha256":file_sha(Path(__file__)),
        "scope":"Empirical proposal library only. Every query excludes ALL rows with the current physical scene_key, across all six batches; no reference file or random seeds in features. Leave-one-physical-board-out, not held-out layout-family evaluation."}
    write_json(output.with_suffix(".json"), metadata)
    print(json.dumps({k:v for k,v in metadata.items() if k!="source_sha256"},ensure_ascii=False),flush=True)


@lru_cache(maxsize=1)
def load_atlas(path=DEFAULT):
    if not path.exists(): return None
    with np.load(path,allow_pickle=False) as data: return {k:data[k] for k in data.files}


def atlas_initials(scene, elapsed, deadline, clip, limit=12):
    atlas = load_atlas()
    if atlas is None or "scene_key" not in scene: return [], []
    from training_research.inverse_initials import path_array, interpolate
    goals = scene["selection"]["goal"]["stones"]
    stones = {s["index"]:s for s in scene["stones"]}
    targets = scene["selection"].get("first_contact_any", scene.get("_proposal_targets",[]))
    raw = []
    active_goal = goals.get(str(scene["active_index"]),{})
    # Same physical board is excluded before scoring, not after taking top-k.
    excluded = atlas["scene_key"] != scene["scene_key"]
    for first in targets:
        a = stones[first]; goal = goals.get(str(first),{})
        mask = excluded.copy()
        if goal.get("type") == "IN_REGION": mask &= atlas["target_live"]
        elif goal.get("type") == "OUT_OF_PLAY": mask &= ~atlas["target_live"]
        elif goal.get("type") == "OUT_OF_HOUSE": mask &= ~atlas["target_house"]
        if active_goal.get("type") == "IN_REGION": mask &= atlas["active_live"]
        elif active_goal.get("type") == "OUT_OF_PLAY": mask &= ~atlas["active_live"]
        indices = np.flatnonzero(mask)
        if not len(indices): continue
        score = ((atlas["first_y"][indices]-a["y"])/1.5)**2
        if goal.get("type") == "IN_REGION":
            desired = np.array((goal["x"]-a["x"],goal["y"]-a["y"]))
            score += np.sum(((atlas["target_delta"][indices]-desired)/.25)**2,axis=1)
        if active_goal.get("type") == "IN_REGION":
            desired = np.array((active_goal["x"]-a["x"],active_goal["y"]-a["y"]))
            score += np.sum(((atlas["active_delta"][indices]-desired)/.25)**2,axis=1)
        others = sorted((s for i,s in stones.items() if i!=first),key=lambda s:(s["x"]-a["x"])**2+(s["y"]-a["y"])**2)
        nearby = [s[k]-a[k] for s in others[:3] for k in ("x","y")]+[5.]*(6-2*min(3,len(others)))
        score += .1*np.sum(((atlas["nearby"][indices]-nearby)/.8)**2,axis=1)
        score += .05*(atlas["stones"][indices]-len(stones))**2
        if "nearby_final" in atlas:
            for neighbour,b in enumerate(others[:3]):
                wanted=goals.get(str(b["index"]),{})
                live=atlas["nearby_live"][indices,neighbour]
                if wanted.get("type")=="IN_REGION":
                    desired=np.array((wanted["x"]-a["x"],wanted["y"]-a["y"]))
                    score += 16.*(~live)
                    score += .4*np.sum(((atlas["nearby_final"][indices,2*neighbour:2*neighbour+2]-desired)/.25)**2,axis=1)*live
                elif wanted.get("type")=="OUT_OF_PLAY":
                    score += 16.*live
        # Keep multiple speeds and rotations rather than repetitions of one action.
        families = set()
        for local in np.argsort(score):
            index = int(indices[local]); v,h,w = atlas["shot"][index]
            family = (round(v,1),round(w,0))
            if family in families: continue
            if elapsed()>=deadline: break
            path = path_array(v,w)
            source = interpolate(path,float(atlas["first_y"][index])+2*.145)
            target = interpolate(path,a["y"]+2*.145)
            if source is None or target is None: continue
            # Preserve empirical contact offset while adjusting for target height/x.
            offset = float(atlas["launch_relative_x"][index])
            adjusted_h = a["x"]+offset+float(source[0][0])-float(target[0][0])
            if abs(adjusted_h)>2.23: continue
            raw.append((float(score[local]),clip((v,adjusted_h,w)),
                {"record_id":str(atlas["record_id"][index]),"scene_key":str(atlas["scene_key"][index]),"query_scene_key":scene["scene_key"]}))
            families.add(family)
            if len(families)>=limit: break
    raw.sort(key=lambda x:x[0]); raw=raw[:limit]
    assert all(item[2]["scene_key"]!=scene["scene_key"] for item in raw)
    return [item[1] for item in raw],[item[2] for item in raw]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=RUNS / DEFAULT.name)
    args=parser.parse_args();build(args.output)


if __name__ == "__main__": main()
