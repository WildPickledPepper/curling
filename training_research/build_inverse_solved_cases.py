"""Mine locally observed double solutions; keep robustness and labels separate."""
import argparse
import copy
from collections import Counter, defaultdict
from itertools import combinations, groupby
import json
from pathlib import Path

from training_research.inverse_dataset.cli import file_sha, write_json
from training_research.inverse_dataset.sampling import validate_scene
from training_research.inverse_dataset.schema import digest, in_house
from training_research.inverse_dataset.selection import failure_reason


def observed_pairs(record):
    if record.get("status") != "complete" or record.get("rule_violations") or not record.get("prediction", {}).get("settled"):
        return []
    active = record["active_index"]
    before = {s["index"]:s for s in record["before"]}
    after = {s["index"]:s for s in record["physical_final"]}
    opponents = [i for i,s in before.items() if i < active and i%2 != active%2 and in_house(s) and not in_house(after[i])]
    contacts = set(record["prediction"].get("firstContactTargets", []))
    pairs = {frozenset(e["stones"]) for e in record.get("collision_events", [])}
    return [pair for pair in combinations(opponents,2) if len(contacts)==1 and contacts <= set(pair) and frozenset(pair) in pairs]


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs",type=Path,default=Path("training_research/runs"))
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--terminal-radius",type=float,help="also constrain every other initial/shooter slot to observed terminal state")
    parser.add_argument("--include-search-certificates",action="store_true",help="explicitly include later inverse-search successes; default uses original forward samples only")
    parser.add_argument("--min-observed-seeds",type=int,default=1,help="one observed success proves reachability; multi-seed evidence is a separate robustness statistic")
    args=parser.parse_args(argv)
    if args.min_observed_seeds < 1:
        parser.error("min-observed-seeds must be positive")
    if args.terminal_radius is not None and not 0 < args.terminal_radius <= 1:
        parser.error("terminal-radius must be in (0,1]")
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("output must be new/empty")
    args.output.mkdir(parents=True,exist_ok=True)
    cases,source_hashes,counts={}, {},Counter()

    def add(scene, selection, shot, records, source, origin):
        scene=validate_scene({k:v for k,v in scene.items() if k not in ("candidate_shots","selection","task_key")})
        passed=[r for r in records if failure_reason(r,selection) is None]
        if len({r["physics_seed"] for r in passed})<args.min_observed_seeds:
            return
        if args.terminal_radius is not None:
            selection=copy.deepcopy(selection)
            terminal={s["index"]:s for s in passed[0]["physical_final"]}
            for i in sorted({s["index"] for s in scene["stones"]}|{scene["active_index"]}):
                if str(i) in selection["goal"]["stones"]:
                    continue
                stone=terminal[i]
                selection["goal"]["stones"][str(i)]={"type":"IN_REGION","x":stone["x"],"y":stone["y"],"radius":args.terminal_radius,"required":True} if stone["enabled"] else {"type":"OUT_OF_PLAY","required":True}
            passed=[r for r in passed if failure_reason(r,selection) is None]
            if len({r["physics_seed"] for r in passed})<args.min_observed_seeds:
                counts["terminal_goal_certificates_rejected"]+=1
                return
        case=validate_scene({**scene,"selection":selection})
        key=case["task_key"]
        case["scene_id"]="solved-double-"+key[:16]
        entry=cases.setdefault(key,{"scene":case,"references":[]})
        if not any(r["shot"]==list(shot) for r in entry["references"]):
            entry["references"].append({"shot":list(shot),"physics_seeds":sorted({r["physics_seed"] for r in passed}),
                "source":str(source.resolve()),"origin":origin,
                "record_ids":[r.get("record_id") for r in passed]})

    names=("inverse_expanded_batch1_20261004","inverse_manual_boards_20261004",
           "inverse_dataset_historical_verify_20261004","inverse_dataset_grid_verify_20261004",
           "inverse_dataset_pilot_20261004","inverse_dataset_smoke_20261004")
    for name in names:
        for path in sorted((args.runs/name/"shards").glob("*.raw.jsonl")):
            source_hashes[str(path.resolve())]=file_sha(path)
            with path.open(encoding="utf-8") as stream:
                records=(json.loads(line) for line in stream)
                for _,group in groupby(records,key=lambda r:(r["scene_key"],tuple(r["shot"]))):
                    rows=list(group); counts["raw_records_checked"]+=len(rows)
                    scene,shot=rows[0]["requested_scene"],rows[0]["shot"]
                    selection=scene.get("selection")
                    if selection and selection["tactic"]=="double_hit":
                        add(scene,selection,shot,rows,path,"embedded_full_goal")
                    pairs=set(pair for r in rows for pair in observed_pairs(r))
                    for pair in sorted(pairs):
                        selection={"tactic":"double_hit","first_contact_any":list(pair),"require_single_first_contact":True,
                            "required_collision_pairs":[list(pair)],"goal":{"stones":{str(i):{"type":"OUT_OF_HOUSE","required":True} for i in pair}}}
                        add(scene,selection,shot,rows,path,"observed_double_house_clear")
    # Search successes must not silently replace the original forward sample set.
    search_reports = sorted(args.runs.glob("inverse*/report.json")) if args.include_search_certificates else []
    for path in search_reports:
        report=json.loads(path.read_text(encoding="utf-8"))
        for row in report.get("rows",[]):
            if not row.get("success") or "evidence" not in row:
                continue
            evidence=Path(row["evidence"])
            if not evidence.exists():
                continue
            result=json.loads(evidence.read_text(encoding="utf-8"))
            if "scene" not in result or result.get("goal",{}).get("tactic")!="double_hit":
                continue
            source_hashes[str(evidence.resolve())]=file_sha(evidence)
            for attempt in result["rows"]:
                shot=attempt.get("first_three_seed_success_shot")
                if shot is not None:
                    records=[r for r in attempt["calls"] if r["shot"]==shot]
                    add(result["scene"],result["goal"],shot,records,evidence,"strict_search_certificate")
    # Keep the most constrained known goal for each physical board / target pair.
    selected={}
    for entry in cases.values():
        scene=entry["scene"]
        key=(scene["scene_key"],tuple(sorted(scene["selection"]["first_contact_any"])))
        current=selected.get(key)
        if current is None or len(scene["selection"]["goal"]["stones"])>len(current["scene"]["selection"]["goal"]["stones"]):
            selected[key]=entry
    entries=sorted(selected.values(),key=lambda e:e["scene"]["task_key"])
    for e in entries:
        counts["reference_actions"]+=len(e["references"])
        counts["reference_actions_outside_previous_spin_domain"]+=sum(abs(r["shot"][2])>10 for r in e["references"])
    write_json(args.output/"scenes.json",[e["scene"] for e in entries])
    write_json(args.output/"references.json",{e["scene"]["scene_id"]:e["references"] for e in entries})
    report={"status":"complete","terminal_radius":args.terminal_radius,
        "source_policy":"forward_samples_and_search_certificates" if args.include_search_certificates else "original_forward_samples_only",
        "forward_run_names":list(names),"include_search_certificates":args.include_search_certificates,
        "min_observed_seeds":args.min_observed_seeds,
        "counts":dict(counts),"cases":len(entries),
        "distinct_boards":len({e["scene"]["scene_key"] for e in entries}),
        "layout_groups":len({e["scene"]["group_id"] for e in entries}),
        "origin_counts":dict(Counter(r["origin"] for e in entries for r in e["references"])),
        "source_sha256":source_hashes,"builder_sha256":file_sha(Path(__file__)),
        "scope":"At least the configured number of observed successful seeds per reference; one success establishes finite-input reachability, multiple successes provide separate robustness evidence. Labels never passed to online solver."}
    write_json(args.output/"manifest.json",report)
    print(json.dumps({k:v for k,v in report.items() if k!="source_sha256"},ensure_ascii=False))


if __name__=="__main__":
    main()
