"""Audit an actual simultaneous four-core solver on original forward tasks."""
from __future__ import annotations

import argparse
import atexit
from collections import Counter
import gzip
import json
from pathlib import Path
import platform
import sys
import time

from training_research.benchmark_compact_solver import DATA, ordered_requests, sha, summarize


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--budget-seconds", type=float, default=10.)
    parser.add_argument("--profiles", nargs="+")
    parser.add_argument("--cpus", nargs="+", type=int)
    args = parser.parse_args(argv)
    if args.output.exists():
        raise ValueError("output must be a new directory")
    requests = json.loads(args.catalog.read_text(encoding="utf-8")) if args.catalog else ordered_requests(DATA, per_tactic=True)
    if args.limit:
        requests = requests[:args.limit]
    args.output.mkdir(parents=True)
    (args.output/"catalog.json").write_text(json.dumps(requests, ensure_ascii=False, indent=2), encoding="utf-8")
    if sys.platform == "win32":
        import ctypes as C
        execution_state = C.WinDLL("kernel32", use_last_error=True).SetThreadExecutionState
        execution_state.argtypes = (C.c_uint32,)
        execution_state.restype = C.c_uint32
        if not execution_state(0x80000001):
            raise C.WinError(C.get_last_error())
        atexit.register(execution_state, 0x80000000)
    from training_research.parallel_shot_solver import ParallelShotSolver, PROFILES, CPUS
    from training_research.inverse_dataset.selection import failure_reason
    from training_research.inverse_goal_search import loss
    from training_research.contact_seed_forest import IMPACT, DEFAULT
    started = time.perf_counter()
    profiles = tuple(args.profiles) if args.profiles else PROFILES
    cpus = tuple(args.cpus) if args.cpus else CPUS
    solver = ParallelShotSolver(profiles=profiles, cpus=cpus)
    report = {"status": "running", "profile": "parallel_portfolio",
              "planned": len(requests), "budget_seconds": args.budget_seconds,
              "catalog_sha256": sha(args.output/"catalog.json"),
              "python": sys.version, "platform": platform.platform(),
              "worker_profiles": profiles, "worker_cpus": cpus,
              "worker_pids": [p.pid for p in solver.processes],
              "startup_seconds": time.perf_counter()-started,
              "world_mode": "navigation", "scene_mode": "independent_persistent_workers",
              "scope": "Actual simultaneous searches, one distinct P-core per worker, under one common request deadline. Warm processes. All source tasks retained. Original actions and seeds never opened. Exact goal/contact/rule/settled certification. Evidence transfers/writes after timed solve returns; dispatch and stopping other workers included. Different tasks on one board are not independent boards.",
              "rows": [], "source_sha256": {},
              "data_sha256": {str(p): sha(p) for p in sorted(DATA.glob("*.jsonl.gz"))},
              "learned_model_sha256": {str(p): sha(p) for model in (IMPACT, DEFAULT) for p in sorted(model.glob("*")) if p.is_file()}}
    runtime = Path("local_simulator/runtime")
    payloads = [runtime/"pyphysx/_pyphysx.cp39-win_amd64.pyd", Path("training_research/assets/inverse_contact_atlas_v6_20261004.npz")]
    payloads.extend(runtime.glob("physx_*_20261004.json"))
    report["runtime_sha256"] = {str(p): sha(p) for p in payloads if p.is_file()}
    snapshot = args.output/"source_snapshot"
    snapshot.mkdir()
    for path in sorted(Path("training_research").glob("*.py")):
        if path.name.startswith(("inverse_", "solver_", "shot_solver", "benchmark_", "parallel_", "legacy_inverse", "contact_seed_forest", "goal_geometry_initials", "micro_terminal_refine", "population_search")):
            report["source_sha256"][str(path)] = sha(path)
            (snapshot/path.name).write_bytes(path.read_bytes())
    def save():
        report["summary"] = summarize(report["rows"])
        (args.output/"report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    save()
    try:
        for index, request in enumerate(requests):
            started = time.perf_counter()
            result = solver.solve(request, budget_seconds=args.budget_seconds)
            outer_ms = 1000*(time.perf_counter()-started)
            records = solver.collect_records()
            calls = []
            for r in records:
                assert r["task_failure"] == failure_reason(r, request["selection"])
                calls.append({"shot": r["shot"], "phase": r["search_phase"],
                              "worker_profile": r["worker_profile"], "seconds": r["seconds"],
                              "failure": r["task_failure"], "loss": loss(r, request["selection"]),
                              "final": r.get("physical_final"), "prediction": r.get("prediction"),
                              "collision_events": r.get("collision_events"), "rule_violations": r.get("rule_violations")})
            assert len(calls) == result["physics_calls"]
            if result["success"]:
                assert any(c["shot"] == result["shot"] and c["failure"] is None and
                           c["worker_profile"] == result["diagnostics"]["winning_profile"] for c in calls)
            with gzip.open(args.output/("%03d.json.gz" % index), "wt", encoding="utf-8") as stream:
                json.dump({"request": request, "result": result, "calls": calls}, stream, ensure_ascii=False)
            diag = result["diagnostics"]
            row = {"index": index, "record_id": request["record_id"], "scene_key": request["scene_key"],
                   "tactic": request["selection"]["tactic"], "success": result["success"], "shot": result["shot"],
                   "elapsed_ms": outer_ms, "internal_elapsed_ms": result["elapsed_ms"],
                   "first_success_ms": diag["first_success_ms"], "winning_profile": diag["winning_profile"],
                   "initial_success": diag["initial_success"], "refinement_success": diag["refinement_success"],
                   "initial_generation_ms": diag["initial_generation_ms"], "physics_calls": len(calls),
                   "best_loss": min((c["loss"] for c in calls), default=None),
                   "phase_calls": dict(Counter(c["phase"] for c in calls)),
                   "worker_calls": dict(Counter(c["worker_profile"] for c in calls))}
            report["rows"].append(row)
            save()
            print(json.dumps({"done": index+1, "total": len(requests), "ok": row["success"],
                              "ms": round(outer_ms), "winner": diag["winning_profile"]}), flush=True)
        report["status"] = "complete"
        save()
        print(json.dumps(report["summary"], ensure_ascii=False), flush=True)
    finally:
        solver.close()


if __name__ == "__main__":
    main()
