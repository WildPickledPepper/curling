"""Recompute strict acceptance and aggregate paired inverse-search reports."""
import argparse
import json
from pathlib import Path
import statistics

from training_research.benchmark_inverse_compare import validate_result
from training_research.inverse_dataset.cli import file_sha, write_json


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports",type=Path,nargs="+",required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(argv)
    rows,checked,sets=[],0,[]
    versions={}
    for path in args.reports:
        report=json.loads(path.read_text(encoding="utf-8"))
        assert report["status"]=="complete" and report["affinity_restored"]
        assert len(report["rows"])==report["planned_scenes"]*len(report["methods"])
        boards={}
        for row in report["rows"]:
            result=json.loads(Path(row["evidence"]).read_text(encoding="utf-8"))
            checked+=validate_result(result)
            diagnostics=result["rows"][0].get("legacy_diagnostics",{})
            assert row["cpu_before"]==row["cpu_after"]==report["cpu"]["logical"]
            assert result["scene"]["scene_key"]==boards.setdefault(result["scene"]["scene_id"],result["scene"]["scene_key"])
            assert all(len(c["initial_state"])==16 for c in result["rows"][0]["calls"])
            if row["method"].startswith("initial_refine"):
                if "max_physics_calls" in diagnostics:
                    assert row["physics_calls"]<=diagnostics["max_physics_calls"]
                    assert diagnostics["conservative_iterations"]<=2*diagnostics["conservative_round_limit"]
                    assert diagnostics["local_iterations"]<=3*diagnostics["local_round_limit"]
                hashes={key.replace("\\","/"):value for key,value in result["source_sha256"].items()}
                source=hashes["training_research/inverse_initials.py"]
                versions.setdefault(source,[]).append(str(row["evidence"]))
            rows.append({**row,"report":str(path.resolve()),"budget_seconds":row.get("budget_seconds",report["budget_seconds"]),
                         "search_limits":{k:diagnostics.get(k) for k in ("max_physics_calls","conservative_round_limit","local_round_limit")}})
        sets.append(set(boards.values()))
    assert all(not a & b for i,a in enumerate(sets) for b in sets[i+1:])
    summaries={}
    for method in {r["method"] for r in rows}:
        selected=[r for r in rows if r["method"]==method]
        successful=[r for r in selected if r["success"]]
        times=[r["solution_ms"] for r in successful]
        summaries[method]={"tested_scenes":len(selected),"successful_scenes":len(successful),
            "profiles":[json.loads(profile) for profile in sorted({json.dumps({"budget_seconds":r["budget_seconds"],**r["search_limits"]},sort_keys=True) for r in selected})],
            "call_limit_reached_scenes":sum(r["physics_calls"]==r["search_limits"]["max_physics_calls"] for r in selected),
            "five_holdout_passed_scenes":sum(r["holdout_passed"]==r["holdout_seeds"]==5 for r in selected),
            "direct_initial_successful_scenes":sum(r["initial_success"] for r in selected),
            "iterated_successful_scenes":sum(r["refinement_success"] for r in selected),
            "successful_ms":{"min":min(times),"median":statistics.median(times),"max":max(times)} if times else None,
            "all_request_median_ms":statistics.median(r["return_ms"] for r in selected),
            "max_request_ms":max(r["return_ms"] for r in selected),
            "max_budget_overrun_ms":max(max(0.,r["return_ms"]-1000*r["budget_seconds"]) for r in selected),
            "total_physics_calls":sum(r["physics_calls"] for r in selected)}
    assert len(versions)==1,"final reports must use one unchanged optimizer source"
    output={"status":"passed","checked_forward_records":checked,"summary":summaries,
        "reports":{str(p.resolve()):file_sha(p) for p in args.reports},
        "optimizer_source_sha256":next(iter(versions)),"distinct_scene_keys":len(set().union(*sets)),
        "distinct_layout_groups":len({r["group_id"] for r in rows}),
        "checks":"full goals, actual collision chains, complete three-search-seed certificates, disjoint holdout seeds, parameter bounds, source version, CPU affinity boundaries, explicit reset states",
        "scope":"finite observed outcomes; successful latency excludes later holdout tests; deadline checks before calls permit one in-flight simulation to finish"}
    write_json(args.output,output)
    print(json.dumps(output,ensure_ascii=False))


if __name__=="__main__":
    main()
