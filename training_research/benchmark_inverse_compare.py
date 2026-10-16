"""Paired double-inverse benchmark on one owned P-core thread.

The initial boards alone enter each solver. Search seeds and holdout seeds are
identical across methods. No earlier solved action enters either method.
"""
from __future__ import annotations

import argparse
import ctypes as C
import json
from pathlib import Path
import time

from tools.cpu_telemetry import CpuTelemetry
from training_research.benchmark_inverse_batch import distribution
from training_research.benchmark_inverse_solver import main as run_scene
from training_research.inverse_dataset.cli import file_sha, make_environment, write_json
from training_research.inverse_dataset.selection import failure_reason


def validate_result(result):
    """Recheck every sampled outcome and the exact three-seed acceptance."""
    row, selection = result["rows"][0], result["goal"]
    calls = row["calls"]
    assert len(calls) == row["physics_calls"]
    for record in calls:
        assert failure_reason(record, selection) == record["task_failure"]
    shot = row.get("first_three_seed_success_shot")
    if shot is not None:
        accepted = calls[row["calls_to_first_three_seed_success"]-3:row["calls_to_first_three_seed_success"]]
        assert len(accepted) == 3
        assert all(r["shot"] == shot and r["task_failure"] is None for r in accepted)
        assert [r["physics_seed"] for r in accepted] == result["physics_seeds"]
        assert result["holdout"]["shot"] == shot
    holdout = result.get("holdout", {}).get("records", [])
    for record in holdout:
        assert failure_reason(record, selection) == record["task_failure"]
    assert len({r["physics_seed"] for r in holdout}) == len(holdout)
    assert not set(result["physics_seeds"]) & {r["physics_seed"] for r in holdout}
    if holdout:
        assert sum(r["task_failure"] is None for r in holdout) == result["holdout"]["passed"]
    assert all(1. <= r["shot"][0] <= 6. and abs(r["shot"][1]) <= 2.23 and abs(r["shot"][2]) <= 15.7 for r in calls)
    return len(calls) + len(holdout)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cpu", type=int, default=4)
    parser.add_argument("--budget-seconds", type=float, default=10.)
    parser.add_argument("--methods", default="geometry,legacy_refine")
    parser.add_argument("--previous-budget-seconds",type=float,default=5.,help="budget for initial_refine_previous only")
    args = parser.parse_args(argv)
    selected_methods = tuple(args.methods.split(","))
    if len(selected_methods) not in (1,2) or len(set(selected_methods))!=len(selected_methods) or not set(selected_methods)<= {"geometry","legacy_refine","initial_refine","initial_refine_previous","initial_refine_poll","initial_refine_probe"}:
        parser.error("methods must specify one or two distinct supported methods")
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("output must be new/empty")
    payload = json.loads(args.scene_json.read_text(encoding="utf-8"))
    catalog = payload if isinstance(payload,list) else payload["scenes"]
    scenes = [s for s in catalog if s.get("selection", {}).get("tactic") == "double_hit"]
    args.output.mkdir(parents=True, exist_ok=True)
    telemetry = CpuTelemetry()
    cpu = next(c for c in telemetry.topology if c["group"] == 0 and c["logical"] == args.cpu)
    if cpu["efficiency"] != max(c["efficiency"] for c in telemetry.topology):
        raise ValueError("selected CPU is not the observed high-performance class")
    kernel = C.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentThread.restype = C.c_void_p
    kernel.SetThreadAffinityMask.argtypes = (C.c_void_p, C.c_size_t)
    kernel.SetThreadAffinityMask.restype = C.c_size_t
    kernel.GetCurrentProcessorNumber.restype = C.c_uint32
    thread = kernel.GetCurrentThread()
    previous_affinity = kernel.SetThreadAffinityMask(thread, 1 << args.cpu)
    if not previous_affinity:
        raise C.WinError(C.get_last_error())
    report = {"status": "running", "scene_source": str(args.scene_json.resolve()),
              "scene_source_sha256": file_sha(args.scene_json), "benchmark_source_sha256": file_sha(Path(__file__)),
              "planned_scenes": len(scenes), "cpu": cpu, "budget_seconds": args.budget_seconds, "methods":selected_methods,
              "previous_budget_seconds":args.previous_budget_seconds,
              "scope": "paired interleaved methods, owned thread affinity restored; frequency observed but not locked; warm persistent simulator; generation included; holdout excluded",
              "rows": [], "validated_records": 0}
    try:
        env = make_environment()
        for index, scene in enumerate(scenes):
            methods = selected_methods if index % 2 == 0 else selected_methods[::-1]
            for method in methods:
                path = args.output / ("%03d_%s.json" % (index, method))
                telemetry.snapshot()
                cpu_before, start_cpu = kernel.GetCurrentProcessorNumber(), time.thread_time()
                budget = args.previous_budget_seconds if method=="initial_refine_previous" else args.budget_seconds
                run_scene(["--scene-json", str(args.scene_json), "--scene-id", scene["scene_id"], "--method", method,
                           "--repeats", "1", "--budget-seconds", str(budget), "--holdout-seeds", "5",
                           "--seed", "20261004", "--output", str(path)], environment=env)
                cpu_ms = (time.thread_time()-start_cpu)*1000
                sample = telemetry.snapshot()["processors"][str(args.cpu)]
                result = json.loads(path.read_text(encoding="utf-8"))
                report["validated_records"] += validate_result(result)
                row = result["rows"][0]
                diagnostics = row.get("legacy_diagnostics", {})
                report["rows"].append({"scene_id": scene["scene_id"], "group_id": scene["group_id"], "method": method,
                    "success": row["first_three_seed_success_ms"] is not None,"budget_seconds":budget,
                    "solution_ms": row["first_three_seed_success_ms"], "return_ms": row["return_ms"],
                    "physics_calls": row["physics_calls"], "initial_generation_ms": diagnostics.get("initial_generation_ms"),
                    "initial_count": diagnostics.get("retained_count"),
                    "initial_success": bool(diagnostics.get("initial_three_seed_success")),
                    "refinement_success": bool(diagnostics.get("refinement_three_seed_success")),
                    "holdout_seeds": result.get("holdout", {}).get("seeds", 0),
                    "holdout_passed": result.get("holdout", {}).get("passed", 0),
                    "thread_cpu_ms_including_warmup_and_holdout": cpu_ms,
                    "cpu_before": cpu_before, "cpu_after": kernel.GetCurrentProcessorNumber(),
                    "cpu_performance_interval": sample, "evidence": str(path.resolve())})
                write_json(args.output / "report.json", report)
        summaries = {}
        for method in selected_methods:
            rows = [r for r in report["rows"] if r["method"] == method]
            successes = [r for r in rows if r["success"]]
            summaries[method] = {"tested_scenes": len(rows), "successful_scenes": len(successes),
                "all_holdout_passed_scenes": sum(r["holdout_seeds"] == r["holdout_passed"] == 5 for r in successes),
                "initial_successful_scenes": sum(r["initial_success"] for r in rows),
                "refinement_successful_scenes": sum(r["refinement_success"] for r in rows),
                "no_initial_scenes": sum(r["initial_count"] == 0 for r in rows),
                "successful_solution_ms": distribution([r["solution_ms"] for r in successes]),
                "all_request_ms": distribution([r["return_ms"] for r in rows]),
                "total_physics_calls": sum(r["physics_calls"] for r in rows)}
        report.update(status="complete", summary=summaries, independent_layout_groups=len({s["group_id"] for s in scenes}),
                      validation="all strict goal/collision checks and seed disjointness recomputed; original forward outcomes preserved")
    finally:
        if not kernel.SetThreadAffinityMask(thread, previous_affinity):
            raise C.WinError(C.get_last_error())
        telemetry.close()
    report["affinity_restored"] = True
    write_json(args.output / "report.json", report)
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
