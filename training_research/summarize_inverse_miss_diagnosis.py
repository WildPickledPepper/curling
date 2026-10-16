"""Audit miss diagnosis and keep oracle experiments out of online results."""
import json
from pathlib import Path

from training_research.inverse_dataset.cli import file_sha, write_json
from training_research.inverse_dataset.schema import encode_action
from training_research.inverse_dataset.selection import failure_reason
from training_research.benchmark_inverse_sampled_suite import summary
from training_research.diagnose_inverse_misses import recorded_trace
from training_research.inverse_goal_search import clip, loss


def main():
    root = Path("training_research/runs")
    old_path = root / "inverse_sampled_suite_combined_20261004.json"
    fixed_path = root / "inverse_miss_no_contact_initial_fix_20261004/report.json"
    audit_path = root / "inverse_miss_no_contact_initial_fix_validation_20261004.json"
    diag_path = root / "inverse_collision_miss_diagnosis_20261004/report.json"
    old, fixed, audit, diag = [json.loads(p.read_text(encoding="utf-8")) for p in
                              (old_path, fixed_path, audit_path, diag_path)]
    assert old["status"] == fixed["status"] == diag["status"] == "complete"
    assert audit["status"] == "passed" and audit["report_sha256"] == file_sha(fixed_path)
    for p, sha in diag["source_sha256"].items():
        source = Path(diag.get("source_snapshots", {}).get(p, p))
        assert file_sha(source) == sha
    for p, sha in diag.get("resume_source_sha256", {}).items(): assert file_sha(Path(p)) == sha
    by_id = {r["scene_id"]: r for r in old["rows"]}
    missed = {r["scene_id"] for r in old["rows"] if not r["success"]}
    assert len(missed) == 98 and len(fixed["rows"]) == 59 and len(diag["rows"]) == 39
    fixed_ids = {r["scene_id"] for r in fixed["rows"]}
    diag_ids = {r["scene_id"] for r in diag["rows"]}
    assert fixed_ids.isdisjoint(diag_ids) and fixed_ids | diag_ids == missed
    for r in fixed["rows"]:
        e = json.loads(Path(r["evidence"]).read_text(encoding="utf-8"))
        orig = json.loads(Path(by_id[r["scene_id"]]["evidence"]).read_text(encoding="utf-8"))
        assert e["scene"] == orig["scene"] and e["navigation_seed"] == orig["navigation_seed"]
        assert e["reference"] == orig["reference"] and e["scene"]["selection"]["require_no_contact"]
        assert r["success"] and r["initial_success"] and r["holdout_passed"] == 5
    checked = 0
    details = []
    for r in diag["rows"]:
        e = json.loads(Path(r["evidence"]).read_text(encoding="utf-8"))
        orig = json.loads(Path(e["original_evidence"]).read_text(encoding="utf-8"))
        assert e["scene"] == orig["scene"]
        assert not e["scene"]["selection"].get("require_no_contact")
        assert e["recorded_trace"] == recorded_trace(orig)
        selection = e["scene"]["selection"]
        for name in ("reference_navigation_before", "reference_before", "reference_after"):
            record = e[name]
            assert record["shot"] == orig["reference"]["shot"]
            assert failure_reason(record, selection) == record["task_failure"]
            checked += 1
        assert e["reference_before"]["task_failure"] is None and e["reference_after"]["task_failure"] is None
        near, normal, fine = e["arms"]
        ref = orig["reference"]["shot"]
        assert near["start_shot"] == list(clip((ref[0]+.12, ref[1]+.06, ref[2]+.8)))
        assert normal["start_shot"] == fine["start_shot"] == orig["diagnostics"]["best_effort_shot"]
        assert normal["physics_seed"] == fine["physics_seed"] == orig["navigation_seed"]
        assert normal["budget_seconds"] == fine["budget_seconds"] == 3.
        assert normal["max_calls"] == fine["max_calls"] == 48
        assert near["physics_seed"] == e["reference_before"]["physics_seed"] == e["reference_after"]["physics_seed"]
        for arm in e["arms"]:
            assert len(arm["calls"]) <= arm["max_calls"]
            assert len(arm["calls"]) == arm["diagnostics"]["search_physics_calls"]
            for record in arm["calls"]:
                assert record["status"] == "complete"
                assert record["physics_seed"] == arm["physics_seed"]
                assert failure_reason(record, selection) == record["task_failure"]
                encode_action(record["shot"])
                checked += 1
            assert arm["success"] == any(c["task_failure"] is None for c in arm["calls"])
            if arm["success"]:
                assert arm["result"]["bestshot"] == arm["calls"][-1]["shot"]
            assert arm["diagnostics"]["best_loss"] == min(loss(c, selection) for c in arm["calls"])
        same = all(normal["calls"][0][k] == fine["calls"][0][k] for k in
                   ("before", "physical_final", "prediction", "collision_events", "rule_violations"))
        details.append({**r, "same_own_best_start_outputs": same,
                        "fine_only_same_start": same and fine["success"] and not normal["success"],
                        "original_only_same_start": same and normal["success"] and not fine["success"]})
    pair_dir = diag_path.parent / "fresh_pairs"
    pairs = []
    pair_checked = 0
    for path in sorted(pair_dir.glob("*_original.json")):
        fine_path = path.with_name(path.name.replace("_original", "_fine"))
        original, fine = [json.loads(p.read_text(encoding="utf-8")) for p in (path, fine_path)]
        assert original["scene"] == fine["scene"]
        assert original["original_evidence_sha256"] == fine["original_evidence_sha256"] == file_sha(Path(original["original_evidence"]))
        a, b = original["arm"], fine["arm"]
        assert a["start_shot"] == b["start_shot"] and a["physics_seed"] == b["physics_seed"]
        assert a["budget_seconds"] == b["budget_seconds"] == 3. and a["max_calls"] == b["max_calls"] == 48
        for payload in (original, fine):
            for source, sha in payload["source_sha256"].items(): assert file_sha(Path(source)) == sha
            arm = payload["arm"]
            assert len(arm["calls"]) <= 48
            assert arm["success"] == any(c["task_failure"] is None for c in arm["calls"])
            for c in arm["calls"]:
                encode_action(c["shot"])
                assert failure_reason(c, payload["scene"]["selection"]) == c["task_failure"]
                assert c["physics_seed"] == arm["physics_seed"]
                pair_checked += 1
        same = all(a["calls"][0][key] == b["calls"][0][key] for key in
                   ("before", "physical_final", "prediction", "collision_events", "rule_violations"))
        assert same
        pairs.append({"scene_id": original["scene_id"], "same_start_outputs": same,
            "original_success": a["success"], "fine_success": b["success"],
            "original_calls": len(a["calls"]), "fine_calls": len(b["calls"]),
            "evidence_sha256": {str(p.resolve()): file_sha(p) for p in (path, fine_path)}})
    expected_pairs = {r["scene_id"] for r in details if r["own_best_original_success"] != r["own_best_fine_success"]}
    assert len(pairs) == 6 and {r["scene_id"] for r in pairs} == expected_pairs
    output = {"status": "passed", "inputs_sha256": {str(p.resolve()): file_sha(p) for p in
        (old_path, fixed_path, audit_path, diag_path)}, "original_misses": 98, "fixed_initial_branch": 59,
        "fixed_initial_direct_success": 59, "fixed_extra_five_all_pass": 59,
        "collision_diagnosis": {**diag["summary"], "same_best_start_outputs": sum(r["same_own_best_start_outputs"] for r in details),
            "fine_only_same_start": sum(r["fine_only_same_start"] for r in details),
            "original_only_same_start": sum(r["original_only_same_start"] for r in details),
            "near_iterated_success": sum(r["near_original_poll_success"] and not r["near_start_pass"] for r in details),
            "near_nav_seed_iterated_success": sum(r["near_original_poll_success"] and not r["near_start_pass"] and r["navigation_reference_pass"] for r in details),
            "own_best_either_success": sum(r["own_best_original_success"] or r["own_best_fine_success"] for r in details)},
        "checked_diagnostic_physical_records": checked, "rows": details,
        "fresh_process_pairs": {"tested": len(pairs), "same_start_outputs": len(pairs),
            "fine_only_success": sum(r["fine_success"] and not r["original_success"] for r in pairs),
            "original_only_success": sum(r["original_success"] and not r["fine_success"] for r in pairs),
            "both_success": sum(r["original_success"] and r["fine_success"] for r in pairs),
            "checked_physical_records": pair_checked, "rows": pairs,
            "scope": "Targeted follow-up of the six discordant reused-scene pairs, not an independent six-case test set. Separate fresh processes per arm and equal budgets; all first outputs identical."},
        "scope": "59 repaired online requests plus 39 offline diagnostic requests. Oracle-neighbour results are excluded from online counts; continuation arms extend original search and are not a new within-ten-second production benchmark."}
    write_json(root / "inverse_miss_diagnosis_summary_20261004.json", output)
    merged = []
    fixes = {r["scene_id"]: r for r in fixed["rows"]}
    for r in old["rows"]:
        item = dict(fixes.get(r["scene_id"], r))
        item["result_stage"] = "no_contact_initial_branch_fix" if r["scene_id"] in fixes else "previous_verified_combined"
        merged.append(item)
    write_json(root / "inverse_sampled_suite_after_initial_branch_fix_20261004.json", {
        "status": "complete", "planned": 306, "rows": merged, "summary": summary(merged),
        "inputs_sha256": output["inputs_sha256"],
        "scope": "Historical verified results plus replacement of exact 59 initially missed no-contact requests. Multiple source versions, no full 306-case rerun. Oracle diagnostics and additional-budget continuation results excluded."})
    print(json.dumps({k: v for k, v in output.items() if k not in ("rows", "inputs_sha256")}, ensure_ascii=False))


if __name__ == "__main__": main()
