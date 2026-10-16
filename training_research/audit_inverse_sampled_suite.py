"""Recheck sampled-suite source records and every inverse/robustness outcome."""
import argparse
from collections import Counter
import json
from pathlib import Path
import numpy as np

from training_research.inverse_dataset.cli import file_sha,write_json
from training_research.inverse_dataset.schema import encode_action
from training_research.inverse_dataset.selection import failure_reason
from training_research.benchmark_inverse_sampled_suite import summary


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(argv)
    report=json.loads(args.report.read_text(encoding="utf-8"))
    assert report["status"]=="complete" and report["affinity_restored"]
    assert len(report["rows"])==report["planned"]
    assert report["required_seed_successes"]==1 and report["robustness_seeds"]==5
    snapshot_path=args.report.parent/"source_snapshot_manifest.json"
    snapshots=json.loads(snapshot_path.read_text(encoding="utf-8")) if snapshot_path.exists() else {}
    for path,sha in report["source_sha256"].items():
        if path in snapshots:
            assert snapshots[path]["sha256"]==sha and file_sha(Path(snapshots[path]["snapshot"]))==sha
        else: assert file_sha(Path(path))==sha
    catalog=Path(report["catalog"])
    scenes=json.loads((catalog/"scenes.json").read_text(encoding="utf-8"))
    refs=json.loads((catalog/"references.json").read_text(encoding="utf-8"))
    manifest=json.loads((catalog/"manifest.json").read_text(encoding="utf-8"))
    source_audit=json.loads((catalog/"provenance_validation.json").read_text(encoding="utf-8"))
    assert source_audit["status"]=="passed" and source_audit["checked_records"]==len(scenes)
    assert manifest["source_policy"]=="original_forward_samples_only" and manifest["min_observed_successes"]==1
    assert all(file_sha(Path(path))==sha for path,sha in manifest["source_sha256"].items())
    by_id={s["scene_id"]:s for s in scenes}
    assert {r["scene_id"] for r in report["rows"]}==set(by_id)
    counts=Counter(); misses_with_reachable_navigation=[]; no_candidates=[]
    atlas_members=None
    for source,sha in report["source_sha256"].items():
        if "inverse_contact_atlas" in source and source.endswith(".npz"):
            artifact=Path(snapshots.get(source,{}).get("snapshot",source))
            with np.load(artifact,allow_pickle=False) as data:
                atlas_members=set(zip(data["scene_key"].tolist(),data["record_id"].tolist()))
    for row in report["rows"]:
        evidence=json.loads(Path(row["evidence"]).read_text(encoding="utf-8"))
        assert evidence["scene"]==by_id[row["scene_id"]]
        assert evidence["reference"]==refs[row["scene_id"]]
        selection=evidence["scene"]["selection"]
        for source in evidence["diagnostics"].get("atlas_sources",[]):
            assert atlas_members is not None
            assert source["query_scene_key"]==row["scene_key"]
            assert source["scene_key"]!=row["scene_key"]
            assert (source["scene_key"],source["record_id"]) in atlas_members
            for support in source.get("support_record_ids",[]):
                assert (source["scene_key"],support) in atlas_members
            counts["checked_other_board_atlas_seeds"]+=1
        calls=evidence["calls"]
        assert len(calls)==row["physics_calls"]<=report["max_calls"]
        shot=evidence["result"].get("bestshot")
        assert row["success"]==(shot is not None)
        assert row["shot"]==shot
        assert evidence["diagnostics"]["required_seed_successes"]==1
        if row["success"]:
            assert calls[-1]["shot"]==shot and calls[-1]["task_failure"] is None
        else:
            assert not any(r["task_failure"] is None for r in calls)
        for record in calls+evidence["holdout"]+evidence["reference_replay"]:
            assert failure_reason(record,selection)==record["task_failure"]
            if record["proposal_origin"].startswith("reference_"):
                assert record["shot"]==evidence["reference"]["shot"]
            else: encode_action(record["shot"])
            counts["checked_records"]+=1
        assert all(r["physics_seed"]==evidence["navigation_seed"] for r in calls)
        holdout=evidence["holdout"]
        assert len(holdout)==(5 if row["success"] else 0)
        assert len({r["physics_seed"] for r in holdout})==len(holdout)
        assert all(r["physics_seed"]!=evidence["navigation_seed"] and r["shot"]==shot for r in holdout)
        assert row["holdout_passed"]==sum(r["task_failure"] is None for r in holdout)
        assert row["reference_source_seed_pass"]==(evidence["reference_replay"][0]["task_failure"] is None)
        assert row["reference_navigation_seed_pass"]==(evidence["reference_replay"][1]["task_failure"] is None)
        if not row["success"] and row["reference_navigation_seed_pass"]: misses_with_reachable_navigation.append(row["scene_id"])
        if not calls: no_candidates.append(row["scene_id"])
    assert report["summary"]==summary(report["rows"])
    output={"status":"passed","distinct_boards":len(scenes),"source_records":source_audit["checked_records"],
        "counts":dict(counts),"summary":report["summary"],"no_candidate_boards":no_candidates,
        "misses_with_successful_reference_on_navigation_seed":misses_with_reachable_navigation,
        "report_sha256":file_sha(args.report),"checks":"original sample provenance, all board coverage, goal and actual collision acceptance, single-seed solve, disjoint extra seeds, reference replay after search, physical-call caps and source hashes",
        "scope":"finite sampled cases; replay differences do not imply a diagnosed physics mechanism; unsuccessful solves do not prove infeasibility"}
    write_json(args.output,output)
    print(json.dumps({k:v for k,v in output.items() if k not in ("summary","no_candidate_boards","misses_with_successful_reference_on_navigation_seed")},ensure_ascii=False))


if __name__=="__main__": main()
