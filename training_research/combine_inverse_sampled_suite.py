"""Merge only zero-candidate retries, retaining stage/version provenance."""
import argparse
import json
from pathlib import Path

from training_research.inverse_dataset.cli import file_sha,write_json
from training_research.benchmark_inverse_sampled_suite import summary


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initial-report",type=Path,required=True)
    parser.add_argument("--retry-report",type=Path,required=True)
    parser.add_argument("--initial-audit",type=Path,required=True)
    parser.add_argument("--retry-audit",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(argv)
    reports=[]; audits=[]
    for rp,ap in ((args.initial_report,args.initial_audit),(args.retry_report,args.retry_audit)):
        r=json.loads(rp.read_text(encoding="utf-8")); a=json.loads(ap.read_text(encoding="utf-8"))
        assert r["status"]=="complete" and r["affinity_restored"]
        assert a["status"]=="passed" and a["report_sha256"]==file_sha(rp)
        assert a["distinct_boards"]==r["planned"]
        reports.append(r);audits.append(a)
    initial,retry=reports
    assert all(initial[k]==retry[k] for k in ("required_seed_successes","budget_seconds","max_calls","cpu","robustness_seeds"))
    replacements={r["scene_id"]:r for r in retry["rows"]}
    assert set(replacements)=={r["scene_id"] for r in initial["rows"] if r["physics_calls"]==0}
    rows=[]
    for old in initial["rows"]:
        new=replacements.get(old["scene_id"],old)
        if old["scene_id"] in replacements:
            a=json.loads(Path(old["evidence"]).read_text(encoding="utf-8"))
            b=json.loads(Path(new["evidence"]).read_text(encoding="utf-8"))
            assert all(a[k]==b[k] for k in ("scene","navigation_seed","reference"))
        assert new["physics_calls"]>0
        rows.append({**new,"stage":"unanchored_retry" if old["scene_id"] in replacements else "initial_full_run"})
    assert len(rows)==len({r["scene_key"] for r in rows})==initial["planned"]
    misses=[r for r in rows if not r["success"]]
    output={"status":"complete","planned":len(rows),"required_seed_successes":1,
        "budget_seconds":initial["budget_seconds"],"max_calls":initial["max_calls"],
        "scope":"All sampled boards: original full run plus exact-goal replacement of zero-candidate requests after adding unanchored proposals. Two source versions retained; other misses not retried; no reference-action initialisation.",
        "reports":{str(p.resolve()):file_sha(p) for p in (args.initial_report,args.retry_report)},
        "audits":{str(p.resolve()):file_sha(p) for p in (args.initial_audit,args.retry_audit)},
        "checked_records_including_superseded_reference_replays":sum(a["counts"]["checked_records"] for a in audits),
        "summary":summary(rows),"rows":rows,"zero_physics_call_boards":0,"stage2_replaced_requests":len(replacements),
        "misses_with_reference_navigation_seed_success":[r["scene_id"] for r in misses if r["reference_navigation_seed_pass"]],
        "misses_without_reference_navigation_seed_success":[r["scene_id"] for r in misses if not r["reference_navigation_seed_pass"]],
        "merger_sha256":file_sha(Path(__file__))}
    write_json(args.output,output)
    write_json(args.output.with_name("inverse_sampled_suite_misses_20261004.json"),{"count":len(misses),"requests":misses})
    print(json.dumps({"status":"passed","boards":len(rows),"solved":output["summary"]["all"]["solved"],
        "checked_records":output["checked_records_including_superseded_reference_replays"],"retried_zero_candidate_requests":len(replacements)}))


if __name__=="__main__": main()
