"""Compare an audited full rerun with historical exact-scene results."""
import argparse
import json
from pathlib import Path

from training_research.inverse_dataset.cli import file_sha, write_json
from training_research.benchmark_inverse_batch import distribution


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old",type=Path,required=True)
    parser.add_argument("--new",type=Path,required=True)
    parser.add_argument("--audit",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    old,new,audit=[json.loads(p.read_text(encoding="utf-8")) for p in (args.old,args.new,args.audit)]
    assert old["status"]==new["status"]=="complete" and audit["status"]=="passed"
    assert audit["report_sha256"]==file_sha(args.new)
    previous={r["scene_id"]:r for r in old["rows"]}
    assert set(previous)=={r["scene_id"] for r in new["rows"]}
    improved=[]; regressed=[]; remaining=[]; successes=[]
    for row in new["rows"]:
        before=previous[row["scene_id"]]
        assert row["scene_key"]==before["scene_key"] and row["tactic"]==before["tactic"]
        a,b=[json.loads(Path(r["evidence"]).read_text(encoding="utf-8")) for r in (before,row)]
        assert a["scene"]==b["scene"] and a["navigation_seed"]==b["navigation_seed"]
        if row["success"]: successes.append(row)
        if row["success"] and not before["success"]: improved.append(row)
        if before["success"] and not row["success"]: regressed.append(row)
        if not row["success"]: remaining.append(row)
    original_misses=[r for r in old["rows"] if not r["success"]]
    result={"status":"passed","tested":len(new["rows"]),"old_solved":old["summary"]["all"]["solved"],
        "new_solved":new["summary"]["all"]["solved"],"old_missed":len(original_misses),
        "original_misses_now_solved":len(improved),"original_misses_still_missed":len(original_misses)-len(improved),
        "previous_successes_now_missed":len(regressed),"total_missed":len(remaining),
        "new_successful_ms":distribution([r["elapsed_ms"] for r in successes]),
        "newly_solved_ms":distribution([r["elapsed_ms"] for r in improved]),
        "five_extra_seeds_all_pass":new["summary"]["all"]["five_extra_seeds_all_pass"],
        "double_hit":new["summary"]["by_tactic"]["double_hit"],
        "improved":improved,"regressed":regressed,"remaining":remaining,
        "inputs_sha256":{str(p.resolve()):file_sha(p) for p in (args.old,args.new,args.audit)},
        "scope":"Full single-version rerun, same physical scenes, exact goals and navigation seeds. Historical baseline includes earlier verified source versions. Ten-second budget retained; physical-call ceiling raised from 128 to 256. Atlas excludes current physical board, across every original forward batch; leave-one-board-out, not held-out layout families. No union of best results across tuning versions."}
    write_json(args.output,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ("improved","regressed","remaining","inputs_sha256","double_hit")},ensure_ascii=False))


if __name__=="__main__":main()
