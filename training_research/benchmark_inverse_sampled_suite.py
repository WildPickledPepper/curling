"""All sampled boards: one-seed solving and separate five-seed robustness."""
import argparse
from collections import Counter,defaultdict
import ctypes as C
import json
from pathlib import Path
import time

from training_research.inverse_dataset.cli import file_sha,make_environment,simulate_record,reset_environment,write_json
from training_research.inverse_dataset.selection import failure_reason
from training_research.benchmark_inverse_batch import distribution


def summary(rows):
    groups=defaultdict(list)
    for r in rows: groups[r["tactic"]].append(r)
    def one(items):
        successes=[r for r in items if r["success"]]
        return {"tested":len(items),"solved":len(successes),
            "initial_solved":sum(r["initial_success"] for r in items),
            "iterated_solved":sum(r["refinement_success"] for r in items),
            "five_extra_seeds_all_pass":sum(r["holdout_passed"]==5 for r in successes),
            "successful_ms":distribution([r["elapsed_ms"] for r in successes]),
            "missed":len(items)-len(successes),"physics_calls":sum(r["physics_calls"] for r in items),
            "reference_source_seed_pass":sum(r.get("reference_source_seed_pass",False) for r in items),
            "reference_navigation_seed_pass":sum(r.get("reference_navigation_seed_pass",False) for r in items)}
    return {"all":one(rows),"by_tactic":{k:one(v) for k,v in groups.items()}}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--budget-seconds",type=float,default=10.)
    parser.add_argument("--max-calls",type=int,default=256)
    parser.add_argument("--cpu",type=int,default=4)
    args=parser.parse_args(argv)
    if args.budget_seconds<=0 or args.max_calls<1: parser.error("invalid budget")
    if args.output.exists() and any(args.output.iterdir()): raise ValueError("output must be new/empty")
    args.output.mkdir(parents=True,exist_ok=True)
    scenes=json.loads((args.catalog/"scenes.json").read_text(encoding="utf-8"))
    from training_research.inverse_contact_atlas import DEFAULT as atlas_path
    report={"status":"running","catalog":str(args.catalog.resolve()),"planned":len(scenes),"budget_seconds":args.budget_seconds,
        "max_calls":args.max_calls,"required_seed_successes":1,"robustness_seeds":5,"cpu":args.cpu,
        "source_sha256":{str(p):file_sha(p) for p in (Path(__file__),Path("training_research/inverse_initials.py"),
            Path("training_research/inverse_goal_search.py"),Path("training_research/inverse_goal_fallback.py"),
            Path("training_research/inverse_contact_initials.py"),Path("training_research/inverse_terminal_refine.py"),
            Path("training_research/inverse_contact_atlas.py"),
            atlas_path,atlas_path.with_suffix(".json"),
            args.catalog/"scenes.json",args.catalog/"manifest.json")},
        "scope":"all distinct boards in six original forward batches; one achieved terminal goal per board; current double solver and experimental general solver; warm persistent native scene; successful one-seed solve and extra-seed robustness reported separately; reference actions never initialise search",
        "rows":[]}
    snapshots={}; snapshot_dir=args.output/"source_snapshot"; snapshot_dir.mkdir()
    for i,(name,sha) in enumerate(report["source_sha256"].items()):
        source=Path(name); target=snapshot_dir/("%d_"%i+source.name)
        target.write_bytes(source.read_bytes())
        snapshots[name]={"sha256":sha,"snapshot":str(target.resolve())}
    write_json(args.output/"source_snapshot_manifest.json",snapshots)
    from tools.cpu_telemetry import CpuTelemetry
    telemetry=CpuTelemetry()
    cpu=next(c for c in telemetry.topology if c["group"]==0 and c["logical"]==args.cpu)
    if cpu["efficiency"]!=max(c["efficiency"] for c in telemetry.topology): raise ValueError("CPU must be a high-performance core")
    kernel=C.WinDLL("kernel32",use_last_error=True)
    kernel.GetCurrentThread.restype=C.c_void_p
    kernel.SetThreadAffinityMask.argtypes=(C.c_void_p,C.c_size_t); kernel.SetThreadAffinityMask.restype=C.c_size_t
    thread=kernel.GetCurrentThread(); previous=kernel.SetThreadAffinityMask(thread,1<<args.cpu)
    if not previous: raise C.WinError(C.get_last_error())
    try:
        env=make_environment()
        reset_environment(env,scenes[0],20261004); env.play((3.,0.,0.))
        for index,scene in enumerate(scenes):
            tactic=scene["selection"]["tactic"]
            seed=20261004+scene["active_index"]*7919
            calls=[]; started=time.perf_counter()
            def evaluate(shot,seed_index,phase):
                record=simulate_record(env,scene,{"shot":list(shot),"origin":phase},seed+104729*seed_index,
                    "search:%d:%d" % (index,len(calls)),{"goal_radius":.15,"config_hash":"sampled-suite-single-v1"})
                record.update(seed_index=seed_index,search_phase=phase,task_failure=failure_reason(record,scene["selection"]))
                calls.append(record)
                return record
            if tactic=="double_hit":
                from training_research.inverse_initials import solve
            else:
                from training_research.inverse_goal_search import solve
            attempts,diag=solve(scene,evaluate=evaluate,elapsed=lambda:time.perf_counter()-started,
                budget_seconds=args.budget_seconds,max_calls=args.max_calls,required_seed_successes=1)
            elapsed=(time.perf_counter()-started)*1000
            shot=attempts[0].get("bestshot")
            assert len(calls)<=args.max_calls
            assert all(failure_reason(r,scene["selection"])==r["task_failure"] for r in calls)
            if shot is not None:
                assert any(r["shot"]==shot and r["task_failure"] is None for r in calls)
            holdout=[]
            if shot is not None:
                for offset in range(100,105):
                    record=simulate_record(env,scene,{"shot":shot,"origin":"holdout"},seed+104729*offset,
                        "holdout:%d:%d" % (index,offset),{"goal_radius":.15,"config_hash":"sampled-suite-single-v1"})
                    record["task_failure"]=failure_reason(record,scene["selection"]); holdout.append(record)
            # Open the answer file only after the timed inverse result and robustness.
            reference=json.loads((args.catalog/"references.json").read_text(encoding="utf-8"))[scene["scene_id"]]
            replay=[]
            for name,replay_seed in (("source",reference["physics_seed"]),("navigation",seed)):
                record=simulate_record(env,scene,{"shot":reference["shot"],"origin":"reference_"+name},replay_seed,
                    "reference:%d:%s" % (index,name),{"goal_radius":.15,"config_hash":"sampled-suite-single-v1"})
                record["task_failure"]=failure_reason(record,scene["selection"]); replay.append(record)
            evidence=args.output/("%03d.json" % index)
            write_json(evidence,{"scene":scene,"navigation_seed":seed,"result":attempts[0],"diagnostics":diag,
                "elapsed_ms":elapsed,"calls":calls,"holdout":holdout,"reference":reference,"reference_replay":replay})
            row={"scene_id":scene["scene_id"],"scene_key":scene["scene_key"],"group_id":scene["group_id"],
                "tactic":tactic,"source_family":scene["family"],"stones":len(scene["stones"]),"success":shot is not None,
                "shot":shot,"elapsed_ms":elapsed,"physics_calls":len(calls),"initial_success":diag.get("initial_success",False),
                "refinement_success":diag.get("refinement_success",False),
                "holdout_passed":sum(r["task_failure"] is None for r in holdout),
                "reference_source_seed_pass":replay[0]["task_failure"] is None,
                "reference_navigation_seed_pass":replay[1]["task_failure"] is None,
                "evidence":str(evidence.resolve()),"failure_counts":dict(Counter(r["task_failure"] for r in calls if r["task_failure"]))}
            report["rows"].append(row); report["summary"]=summary(report["rows"])
            write_json(args.output/"report.json",report)
            print(json.dumps({"completed":index+1,"planned":len(scenes),"tactic":tactic,"success":shot is not None,
                "ms":round(elapsed,2),"calls":len(calls),"extra_pass":row["holdout_passed"]},ensure_ascii=False),flush=True)
        report["status"]="complete"
    finally:
        if not kernel.SetThreadAffinityMask(thread,previous): raise C.WinError(C.get_last_error())
        telemetry.close()
    report["affinity_restored"]=True
    write_json(args.output/"report.json",report)
    print(json.dumps(report["summary"],ensure_ascii=False),flush=True)


if __name__=="__main__": main()
