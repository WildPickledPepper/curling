"""Blind batch benchmark on previously sampled initial boards.

Only scenes.json is supplied to the solver. Forward outcome logs are consulted
after every timed solve, strictly for coverage diagnostics, never as seeds.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import groupby
import json
from pathlib import Path
import statistics
import time

from training_research.benchmark_inverse_solver import main as run_scene
from training_research.inverse_dataset.cli import file_sha, make_environment, write_json
from training_research.inverse_dataset.selection import failure_reason


def distribution(values):
    return {"min": min(values), "median": statistics.median(values), "max": max(values)} if values else None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    parser.add_argument("--budget-seconds", type=float, default=10.)
    parser.add_argument("--holdout-seeds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--method", choices=("geometry", "legacy_seeds", "legacy_refine", "initial_refine"), default="geometry")
    args = parser.parse_args(argv)
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("output must be a new/empty directory")
    source = args.dataset_dir / "scenes.json"
    scenes = [s for s in json.loads(source.read_text(encoding="utf-8")) if s.get("selection", {}).get("tactic") == "double_hit"]
    if not scenes:
        raise ValueError("no double-hit scenes in source")
    args.output.mkdir(parents=True, exist_ok=True)
    report = {"status": "running", "scene_source": str(source.resolve()), "scene_source_sha256": file_sha(source),
              "benchmark_source_sha256": file_sha(Path(__file__)), "planned_scenes": len(scenes),
              "budget_seconds_per_scene": args.budget_seconds, "seed": args.seed,
              "sampling_policy": "all double-hit initial boards in source; no outcome-based selection; both variants retained",
              "method": args.method,
              "solver_policy": "same configured method as single-scene benchmark; three-seed acceptance; no saved successful-shot warm start",
              "scope": "inverse_double_goal_batch_v1; warm persistent simulator; successes and misses both counted", "rows": []}
    init_start = time.perf_counter()
    env = make_environment()
    report["environment_setup_ms"] = (time.perf_counter()-init_start)*1000
    write_json(args.output / "report.json", report)
    for index, scene in enumerate(scenes):
        path = args.output / f"{index:03d}.json"
        run_scene(["--scene-json", str(source), "--scene-id", scene["scene_id"], "--method", args.method,
                   "--repeats", "1", "--budget-seconds", str(args.budget_seconds), "--holdout-seeds", str(args.holdout_seeds),
                   "--seed", str(args.seed), "--output", str(path)], environment=env)
        result = json.loads(path.read_text(encoding="utf-8"))
        row = result["rows"][0]
        success = row["first_three_seed_success_ms"] is not None
        targets = scene["selection"]["first_contact_any"]
        report["rows"].append({"scene_id": scene["scene_id"], "scene_key": scene["scene_key"], "group_id": scene["group_id"],
            "stones": len(scene["stones"]), "targets": [s for s in scene["stones"] if s["index"] in targets],
            "goal": scene["selection"], "success": success, "first_single_seed_ms": row["first_single_seed_success_ms"],
            "three_seed_solution_ms": row["first_three_seed_success_ms"], "return_ms": row["return_ms"],
            "candidate_count": row["candidate_count"], "physics_calls": row["physics_calls"],
            "status": row["attempts"][0]["status"], "shot": row.get("first_three_seed_success_shot"),
            "successful_phase": row.get("successful_phase"),
            "initial_generation_ms": row.get("legacy_diagnostics", {}).get("initial_generation_ms"),
            "initial_count": row.get("legacy_diagnostics", {}).get("retained_count"),
            "initial_three_seed_success": row.get("legacy_diagnostics", {}).get("initial_three_seed_success"),
            "refinement_three_seed_success": row.get("legacy_diagnostics", {}).get("refinement_three_seed_success"),
            "holdout": {k:result.get("holdout", {}).get(k) for k in ("seeds", "passed", "ms")},
            "failure_counts": dict(Counter(c["task_failure"] for c in row["calls"] if c["task_failure"] is not None)),
            "evidence": str(path.resolve())})
        write_json(args.output / "report.json", report)
        print(json.dumps({"completed_scenes": index+1, "scene_id": scene["scene_id"], "success": success,
                          "return_ms": row["return_ms"], "physics_calls": row["physics_calls"]}, ensure_ascii=False), flush=True)
    # Diagnostic pass only after all timed searches have finished.
    tested = {r["scene_key"]: r for r in report["rows"]}
    sampled_successes = Counter()
    source_hashes = {}
    for path in sorted((args.dataset_dir / "shards").glob("*.raw.jsonl")):
        with path.open(encoding="utf-8") as raw:
            for _, rows in groupby((json.loads(line) for line in raw), lambda r:r["record_id"].rsplit(":", 1)[0]):
                records = list(rows)
                if records[0]["scene_key"] not in tested:
                    continue
                source_hashes[str(path.resolve())] = file_sha(path)
                if len(records) >= 3 and all(failure_reason(r, r["requested_scene"]["selection"]) is None for r in records):
                    sampled_successes[records[0]["scene_key"]] += 1
    for row in report["rows"]:
        row["prior_sampling_three_seed_successful_candidates"] = sampled_successes[row["scene_key"]]
    successes = [r for r in report["rows"] if r["success"]]
    failed = [r for r in report["rows"] if not r["success"]]
    report.update(status="complete", outcome_log_diagnostic_sha256=source_hashes,
        summary={"tested_scenes": len(scenes), "independent_layout_groups": len({s["group_id"] for s in scenes}),
                 "successful_scenes": len(successes), "success_rate": len(successes)/len(scenes),
                 "successful_solution_ms": distribution([r["three_seed_solution_ms"] for r in successes]),
                 "all_request_ms": distribution([r["return_ms"] for r in report["rows"]]),
                 "failed_request_ms": distribution([r["return_ms"] for r in failed]),
                 "total_physics_calls": sum(r["physics_calls"] for r in report["rows"]),
                 "solved_scenes_passing_all_holdout_seeds": sum(r["holdout"]["seeds"] == r["holdout"]["passed"] and r["holdout"]["seeds"] > 0 for r in successes),
                 "failed_scenes_with_prior_sampled_success": sum(r["prior_sampling_three_seed_successful_candidates"] > 0 for r in failed),
                 "initial_successful_scenes": sum(bool(r["initial_three_seed_success"]) for r in report["rows"]),
                 "refinement_successful_scenes": sum(bool(r["refinement_three_seed_success"]) for r in report["rows"]),
                 "interpretation": "configured candidate search misses are not evidence of physical infeasibility; neighbouring variants are correlated"})
    write_json(args.output / "report.json", report)
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
