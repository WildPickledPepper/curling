"""Audit completed compact benchmarks and compare identical requests.

The additional partition must be disjoint, run the same candidate source, and
is reported as another warm process, never as an independent set of boards.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import re
import statistics

from training_research.compact_pairs import request_fingerprint


def task_id(row):
    return row.get("request_fingerprint", row["record_id"])


def load_run(path):
    report = json.loads((path/"report.json").read_text(encoding="utf-8"))
    if report["status"] != "complete" or len(report["rows"]) != report["planned"]:
        raise ValueError("benchmark is not complete: "+str(path))
    requests = json.loads((path/"catalog.json").read_text(encoding="utf-8"))
    if len(requests) != len(report["rows"]):
        raise ValueError("catalog/report length differs")
    for row, request in zip(report["rows"], requests):
        key = request_fingerprint(request)
        if row.get("request_fingerprint", key) != key:
            raise ValueError("recorded request fingerprint differs")
        row["request_fingerprint"] = key
    if len({task_id(r) for r in report["rows"]}) != len(report["rows"]):
        raise ValueError("duplicate task ids")
    return report


def core_identity(report):
    cpu = report["affinity"]
    return {k: cpu[k] for k in ("group", "logical", "core", "efficiency")}


def metrics(rows):
    successes = [r for r in rows if r["success"]]
    times = sorted(r["elapsed_ms"] for r in successes)
    robustness = [r for r in successes if "holdout_passed" in r]
    return {"tasks": len(rows), "physical_boards": len({r["scene_key"] for r in rows}),
            "solved": len(successes), "solve_rate": len(successes)/len(rows) if rows else None,
            "within_10s": sum(r["elapsed_ms"] <= 10000 for r in successes),
            "within_10_1s": sum(r["elapsed_ms"] <= 10100 for r in successes),
            "initial_solved": sum(r["initial_success"] for r in rows),
            "refinement_solved": sum(r["refinement_success"] for r in rows),
            "median_solved_ms": statistics.median(times) if times else None,
            "p95_solved_ms": times[min(int(.95*len(times)), len(times)-1)] if times else None,
            "max_solved_ms": max(times, default=None),
            "max_request_ms": max((r["elapsed_ms"] for r in rows), default=None),
            "physics_calls": sum(r["physics_calls"] for r in rows),
            "reference_source_pass": sum(r.get("reference_source_pass", False) for r in rows),
            "reference_navigation_pass": sum(r.get("reference_navigation_pass", False) for r in rows),
            "reference_replays_available": sum("reference_source_pass" in r for r in rows),
            "robustness_results_available": len(robustness),
            "three_extra_seeds_all_pass": sum(r["holdout_passed"] == 3 for r in robustness)}


def audit_returned_shots(path, report):
    from training_research.inverse_dataset.selection import failure_reason
    checked = 0
    for row in report["rows"]:
        if not row["success"]:
            if row["shot"] is not None:
                raise ValueError("failed task returned an executable shot")
            continue
        with gzip.open(path/("%03d.json.gz" % row["index"]), "rt", encoding="utf-8") as stream:
            evidence = json.load(stream)
        if evidence["request"]["record_id"] != row["record_id"]:
            raise ValueError("evidence/request mismatch")
        if row.get("request_fingerprint", request_fingerprint(evidence["request"])) != request_fingerprint(evidence["request"]):
            raise ValueError("evidence/full-request mismatch")
        certified = False
        for c in evidence["calls"]:
            if c["shot"] != row["shot"]:
                continue
            record = {"status": "complete", "physical_final": c["final"],
                      "prediction": c["prediction"], "collision_events": c["collision_events"],
                      "rule_violations": c["rule_violations"]}
            if failure_reason(record, evidence["request"]["selection"]) is None:
                certified = True
                break
        if not certified:
            raise ValueError("returned shot lacks a complete valid simulation")
        checked += 1
    return checked


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--additional", type=Path)
    parser.add_argument("--interrupted-replay", type=Path)
    parser.add_argument("--sleep-evidence", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.exists():
        raise ValueError("output must be new")
    baseline, candidate = load_run(args.baseline), load_run(args.candidate)
    if baseline["catalog_sha256"] != candidate["catalog_sha256"]:
        raise ValueError("different task catalogs")
    if baseline.get("world_mode", "navigation") != candidate.get("world_mode", "navigation"):
        raise ValueError("different random-world policies")
    if baseline.get("scene_mode", "persistent") != candidate.get("scene_mode", "persistent"):
        raise ValueError("different environment-lifetime policies")
    if core_identity(baseline) != core_identity(candidate) or baseline["budget_seconds"] != candidate["budget_seconds"]:
        raise ValueError("different CPU/budget")
    old = {task_id(r): r for r in baseline["rows"]}
    new = {task_id(r): r for r in candidate["rows"]}
    assert old.keys() == new.keys()
    def changed(improved):
        return [{"record_id": r["record_id"], "request_fingerprint": key, "scene_key": r["scene_key"], "tactic": r["tactic"],
                 "baseline_ms": old[key]["elapsed_ms"], "candidate_ms": r["elapsed_ms"],
                 "candidate_best_loss": r["best_loss"]} for key, r in new.items()
                if r["success"] == improved and old[key]["success"] != improved]
    checked = audit_returned_shots(args.baseline, baseline)+audit_returned_shots(args.candidate, candidate)
    report = {"status": "passed", "baseline": str(args.baseline), "candidate": str(args.candidate),
              "profile": candidate["profile"], "baseline_metrics": metrics(baseline["rows"]),
              "candidate_metrics": metrics(candidate["rows"]),
              "improvements": changed(True), "regressions": changed(False),
              "catalog_sha256": candidate["catalog_sha256"], "affinity": candidate["affinity"],
              "source_sha256": candidate["source_sha256"], "runtime_sha256": candidate.get("runtime_sha256"),
              "scope": "Original forward samples only. Same requests and physical goal predicates in A/B. Candidate chosen on development failures; not a new held-out-family result. Atlas excludes the entire current board. Timing includes input validation; synchronous in-flight calls may exceed the budget slightly. No best-of-multiple-method score stitching."}
    groups = {r["tactic"] for r in candidate["rows"]}
    report["by_tactic"] = {t: {"baseline": metrics([r for r in baseline["rows"] if r["tactic"]==t]),
                                   "candidate": metrics([r for r in candidate["rows"] if r["tactic"]==t])} for t in sorted(groups)}
    corrected_rows = candidate["rows"]
    if args.interrupted_replay:
        if not args.sleep_evidence:
            raise ValueError("a replay requires the external sleep evidence")
        replay = load_run(args.interrupted_replay)
        for key in ("profile", "source_sha256", "runtime_sha256", "budget_seconds"):
            if replay.get(key) != candidate.get(key):
                raise ValueError("interrupted replay used a different "+key)
        if core_identity(replay) != core_identity(candidate):
            raise ValueError("interrupted replay used a different CPU")
        interrupted = {task_id(r): r for r in candidate["rows"] if r["elapsed_ms"] > 60000}
        repeats = {task_id(r): r for r in replay["rows"]}
        if interrupted.keys() != repeats.keys():
            raise ValueError("replay must contain exactly all interrupted tasks")
        events = json.loads(args.sleep_evidence.read_text(encoding="utf-8-sig"))
        deltas = [int(v) for e in events if e["ProviderName"] == "Microsoft-Windows-Kernel-General"
                  for v in re.findall(r"(\d+)\s*ms", e["Message"])]
        if not any(e["ProviderName"] == "Microsoft-Windows-Power-Troubleshooter" for e in events):
            raise ValueError("no system resume evidence")
        candidate_requests = {request_fingerprint(r): r for r in json.loads((args.candidate/"catalog.json").read_text(encoding="utf-8"))}
        replay_requests = json.loads((args.interrupted_replay/"catalog.json").read_text(encoding="utf-8"))
        for request in replay_requests:
            key = request_fingerprint(request)
            if request != candidate_requests[key]:
                raise ValueError("interrupted task input changed")
            with gzip.open(args.candidate/("%03d.json.gz" % interrupted[key]["index"]), "rt", encoding="utf-8") as stream:
                evidence = json.load(stream)
            longest_ms = max(c["seconds"] for c in evidence["calls"])*1000
            if not any(abs(longest_ms-d) < 2000 for d in deltas):
                raise ValueError("long call does not match recorded system sleep clock jump")
        checked += audit_returned_shots(args.interrupted_replay, replay)
        corrected_rows = [repeats.get(task_id(r), r) for r in candidate["rows"]]
        report["interruption_repair"] = {"records": list(interrupted), "replay": str(args.interrupted_replay),
            "sleep_evidence": str(args.sleep_evidence), "clock_jumps_ms": deltas,
            "raw_interrupted_metrics": metrics(list(interrupted.values())), "repeat_metrics": metrics(replay["rows"]),
            "corrected_candidate_metrics": metrics(corrected_rows),
            "policy": "Raw run retained above. Exactly the externally interrupted task repeated once with identical input, policy, source, runtime, core and budget in a fresh warm process. No ordinary failures were replaced."}
    if args.additional:
        extra = load_run(args.additional)
        for key in ("profile", "source_sha256", "runtime_sha256", "budget_seconds"):
            if extra.get(key) != candidate.get(key):
                raise ValueError("additional partition used a different "+key)
        if core_identity(extra) != core_identity(candidate):
            raise ValueError("additional partition used a different CPU")
        if set(new) & {task_id(r) for r in extra["rows"]}:
            raise ValueError("additional partition overlaps")
        checked += audit_returned_shots(args.additional, extra)
        combined = candidate["rows"]+extra["rows"]
        report.update(additional_metrics=metrics(extra["rows"]), combined_metrics=metrics(combined),
                      combined_by_tactic={t: metrics([r for r in combined if r["tactic"]==t]) for t in sorted({r["tactic"] for r in combined})},
                      partition_scope="Two disjoint task partitions, each in its own warm process, identical candidate policy/source/runtime. Same 306 boards can occur in both; task counts are not independent board counts.")
        if args.interrupted_replay:
            report["corrected_combined_metrics"] = metrics(corrected_rows+extra["rows"])
    report["returned_shots_rechecked"] = checked
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "baseline_metrics", "candidate_metrics", "returned_shots_rechecked")}))


if __name__ == "__main__":
    main()
