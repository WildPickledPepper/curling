"""One actual achieved terminal task per sampled board; no seed robustness gate."""
import argparse
import copy
from collections import Counter
import json
from pathlib import Path

from training_research.build_inverse_solved_cases import observed_pairs
from training_research.inverse_dataset.cli import file_sha, write_json
from training_research.inverse_dataset.sampling import validate_scene
from training_research.inverse_dataset.schema import digest, in_house
from training_research.inverse_dataset.selection import failure_reason

FORWARD_RUNS=("inverse_expanded_batch1_20261004","inverse_manual_boards_20261004",
    "inverse_dataset_historical_verify_20261004","inverse_dataset_grid_verify_20261004",
    "inverse_dataset_pilot_20261004","inverse_dataset_smoke_20261004")


def observed_task(record, radius=.15):
    if record.get("status")!="complete" or record.get("rule_violations") or not record.get("prediction",{}).get("settled"):
        return None
    active=record["active_index"]
    initial={s["index"]:s for s in record["before"]}
    final={s["index"]:s for s in record["physical_final"]}
    relevant=[i for i,s in initial.items() if s["enabled"] or i==active]
    goals={str(i):({"type":"IN_REGION","x":final[i]["x"],"y":final[i]["y"],"radius":radius,"required":True}
                  if final[i]["enabled"] else {"type":"OUT_OF_PLAY","required":True}) for i in relevant}
    selection={"tactic":"achieved_goal","goal":{"stones":goals}}
    pairs=observed_pairs(record)
    original=record["requested_scene"].get("selection")
    if pairs:
        targets=list(sorted(pairs)[0])
        selection.update(tactic="double_hit",first_contact_any=targets,require_single_first_contact=True,
                         required_collision_pairs=[targets])
        # Actual target endpoints remain constrained, with removal if observed.
        priority=0
    elif original and failure_reason(record,original) is None:
        selection.update({k:copy.deepcopy(v) for k,v in original.items() if k!="goal"})
        priority=1
    elif not record["prediction"].get("contact") and final[active]["enabled"]:
        selection.update(tactic="default_draw",require_no_contact=True)
        priority=2
    else:
        contacts=record["prediction"].get("firstContactTargets",[])
        if len(contacts)==1:
            selection.update(first_contact_any=contacts,require_single_first_contact=True)
            i=contacts[0]
            if i%2!=active%2 and in_house(initial[i]) and not in_house(final[i]):
                selection["tactic"]="take_out_house"
        priority=3
    if selection["tactic"]=="double_hit":
        # IN_REGION alone is not a double's required removal disposition.
        for i in selection["first_contact_any"]:
            goals[str(i)]={"type":"OUT_OF_HOUSE" if final[i]["enabled"] else "OUT_OF_PLAY","required":True}
    if failure_reason(record,selection) is not None:
        raise AssertionError("observed terminal task must accept its source")
    return selection,priority


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs",type=Path,default=Path("training_research/runs"))
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--radius",type=float,default=.15)
    args=parser.parse_args(argv)
    if not 0<args.radius<=1: parser.error("radius must be in (0,1]")
    if args.output.exists() and any(args.output.iterdir()): raise ValueError("output must be new/empty")
    args.output.mkdir(parents=True,exist_ok=True)
    chosen,hashes,counts,seen={}, {},Counter(),set()
    for name in FORWARD_RUNS:
        for path in sorted((args.runs/name/"shards").glob("*.raw.jsonl")):
            hashes[str(path.resolve())]=file_sha(path)
            with path.open(encoding="utf-8") as stream:
                for line_number,line in enumerate(stream,1):
                    record=json.loads(line); counts["raw_records"]+=1; seen.add(record["scene_key"])
                    task=observed_task(record,args.radius)
                    if task is None: counts["unusable_records"]+=1; continue
                    selection,priority=task
                    rank=(priority,digest(record["record_id"]))
                    key=record["scene_key"]
                    if key in chosen and chosen[key]["rank"]<=rank: continue
                    clean={k:v for k,v in record["requested_scene"].items() if k not in
                        ("selection","candidate_shots","shot_bounds","task_key")}
                    scene=validate_scene({**clean,"selection":selection,"scene_id":"sampled-"+key[:16]})
                    assert scene["scene_key"]==key
                    chosen[key]={"rank":rank,"scene":scene,"reference":{
                        "source":str(path.resolve()),"source_line":line_number,"record_id":record["record_id"],
                        "shot":record["shot"],"physics_seed":record["physics_seed"],
                        "physical_final":record["physical_final"],"collision_events":record["collision_events"],
                        "prediction":record["prediction"],"observed_success_count":1}}
    entries=sorted(chosen.values(),key=lambda e:(e["scene"]["selection"]["tactic"]!="double_hit",
        e["scene"]["selection"]["tactic"],e["scene"]["scene_key"]))
    write_json(args.output/"scenes.json",[e["scene"] for e in entries])
    write_json(args.output/"references.json",{e["scene"]["scene_id"]:e["reference"] for e in entries})
    report={"status":"complete","source_policy":"original_forward_samples_only","forward_run_names":list(FORWARD_RUNS),
        "counts":dict(counts),"sampled_boards":len(seen),"tested_board_catalog":len(entries),
        "boards_without_legal_settled_sample":sorted(seen-set(chosen)),
        "by_tactic":dict(Counter(e["scene"]["selection"]["tactic"] for e in entries)),
        "min_observed_successes":1,"terminal_radius":args.radius,"source_sha256":hashes,
        "builder_sha256":file_sha(Path(__file__)),
        "scope":"All usable distinct boards in the six recorded forward batches; one actually achieved terminal goal each. Double outcomes prioritised. A single observed success is sufficient; robustness is not a selection gate. References excluded from solver inputs."}
    write_json(args.output/"manifest.json",report)
    print(json.dumps({k:v for k,v in report.items() if k!="source_sha256"},ensure_ascii=False))


if __name__=="__main__": main()
