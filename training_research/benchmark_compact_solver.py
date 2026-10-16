"""Reproducible, answer-isolated research on compact forward-sampled requests.

One observed task per physical board, selected without opening references.
The default baseline uses the public application, including its timed proposals.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import statistics
import sys
import time


DATA = Path(__file__).resolve().parent / "datasets/forward_samples_20261004"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ordered_requests(data, per_tactic=False):
    """Prefer labelled observed tactics, then stable record hash, per board."""
    chosen = {}
    for path in sorted(data.glob("*.inputs.jsonl.gz")):
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                request = json.loads(line)
                tactic = request["selection"]["tactic"]
                priority = 0 if tactic == "double_hit" else 2 if tactic == "default_draw" else 3 if tactic == "achieved_goal" else 1
                rank = (priority, hashlib.sha256(request["record_id"].encode()).hexdigest())
                key = (request["scene_key"], tactic) if per_tactic else request["scene_key"]
                if key not in chosen or rank < chosen[key][0]:
                    chosen[key] = (rank, request)
    groups = defaultdict(list)
    for _, request in chosen.values():
        groups[request["selection"]["tactic"]].append(request)
    for items in groups.values():
        items.sort(key=lambda r: hashlib.sha256(r["scene_key"].encode()).hexdigest())
    # Round robin makes bounded development subsets cover the observed tactics.
    return [r for group in itertools.zip_longest(*(groups[k] for k in sorted(groups))) for r in group if r is not None]


def summarize(rows):
    def one(items):
        solved = [r for r in items if r["success"]]
        times = sorted(r["elapsed_ms"] for r in solved)
        return {"tested": len(items), "solved": len(solved),
                "initial_solved": sum(r["initial_success"] for r in items),
                "refinement_solved": sum(r["refinement_success"] for r in items),
                "within_10s": sum(r["success"] and r["elapsed_ms"] <= 10000 for r in items),
                "physics_calls": sum(r["physics_calls"] for r in items),
                "solved_median_ms": statistics.median(times) if times else None,
                "solved_p95_ms": times[min(len(times)-1, int(.95*len(times)))] if times else None,
                "max_ms": max((r["elapsed_ms"] for r in items), default=None),
                "initial_generation_total_ms": sum(r["initial_generation_ms"] for r in items)}
    groups = defaultdict(list)
    for r in rows:
        groups[r["tactic"]].append(r)
    return {"all": one(rows), "by_tactic": {k: one(v) for k, v in groups.items()}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--profile", default="baseline")
    parser.add_argument("--selection-mode", choices=("board", "board_tactic"), default="board")
    parser.add_argument("--world-mode", choices=("navigation", "source_seed"), default="navigation")
    parser.add_argument("--scene-mode", choices=("persistent", "fresh", "fresh_mature"), default="persistent")
    parser.add_argument("--budget-seconds", type=float, default=10.)
    parser.add_argument("--holdout-seeds", type=int, default=0)
    parser.add_argument("--cpu", type=int, default=4)
    parser.add_argument("--replay-references", action="store_true")
    args = parser.parse_args(argv)
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    cpu_info = None
    if sys.platform == "win32":
        import atexit
        import ctypes as C
        from tools.cpu_telemetry import CpuTelemetry
        telemetry = CpuTelemetry()
        cpu_info = next(c for c in telemetry.topology if c["group"] == 0 and c["logical"] == args.cpu)
        if cpu_info["efficiency"] != max(c["efficiency"] for c in telemetry.topology):
            raise ValueError("benchmark CPU must be a performance core")
        kernel = C.WinDLL("kernel32", use_last_error=True)
        execution_state = kernel.SetThreadExecutionState
        execution_state.argtypes = (C.c_uint32,)
        execution_state.restype = C.c_uint32
        if not execution_state(0x80000001):
            raise C.WinError(C.get_last_error())
        atexit.register(execution_state, 0x80000000)
        kernel.GetCurrentProcess.restype = C.c_void_p
        kernel.SetProcessAffinityMask.argtypes = (C.c_void_p, C.c_size_t)
        if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
            raise C.WinError(C.get_last_error())
        telemetry.close()
    if args.output.exists():
        raise ValueError("output must be a new directory")
    requests = json.loads(args.catalog.read_text(encoding="utf-8")) if args.catalog else ordered_requests(args.data, per_tactic=args.selection_mode=="board_tactic")
    if args.limit:
        requests = requests[:args.limit]
    args.output.mkdir(parents=True)
    (args.output/"catalog.json").write_text(json.dumps(requests, ensure_ascii=False, indent=2), encoding="utf-8")
    from training_research.shot_solver import BudgetedShotSolver
    from training_research.inverse_dataset.cli import simulate_record, make_environment
    from training_research.inverse_dataset.sampling import validate_scene
    from training_research.inverse_dataset.selection import failure_reason
    from training_research.inverse_goal_search import loss
    from training_research.compact_pairs import request_fingerprint, references_for_requests
    world_seeds = {}
    if args.world_mode == "source_seed":
        seed_references = references_for_requests(args.data, requests, seeds_only=True)
        world_seeds = {key: row["physics_seed"] for key, row in seed_references.items()}
    mature_context = None
    warming_up = True
    def controlled_forward(env, scene, proposal, navigation_seed, record_id, config):
        started = time.perf_counter()
        current_env = make_environment() if args.scene_mode != "persistent" else env
        if mature_context is not None:
            from training_research.isolated_evaluation import restore_context
            restore_context(current_env, mature_context["slots"])
        creation_ms = (time.perf_counter()-started)*1000
        key = request_fingerprint(scene)
        if not world_seeds or warming_up:  # Fixed warmup fixture, outside measured tasks.
            actual_seed = navigation_seed
        else:
            offset = navigation_seed-(20261004+scene["active_index"]*7919)
            actual_seed = (world_seeds[key]+offset) & 0xffffffff
        record = simulate_record(current_env, scene, proposal, actual_seed, record_id, config)
        record["simulation_seconds"] = record["seconds"]
        record["environment_creation_ms"] = creation_ms
        del current_env
        record["seconds"] = time.perf_counter()-started
        if world_seeds:
            record["physics_seed"] = None  # The search receives no source-seed value.
            record["random_input_policy"] = "opaque original per-shot seed in forward backend"
        return record
    # Initialise the bundled native binding before importing optional SciPy /
    # pandas dependencies: the opposite order crashes extension initialisation
    # on the CP39 Windows payload in this environment.
    solver = BudgetedShotSolver(search_profile=args.profile,
                               forward_simulator=controlled_forward if world_seeds or args.scene_mode!="persistent" else None)
    if args.scene_mode == "fresh_mature":
        from training_research.isolated_evaluation import observed_mature_context
        mature_context = observed_mature_context()
    # Initialise native environment and imports once, as in a persistent service.
    solver.solve(json.loads((Path(__file__).parent/"fixtures/sampled_goal_draw.json").read_text(encoding="utf-8")), budget_seconds=10.)
    warming_up = False
    report = {"status": "running", "profile": args.profile, "budget_seconds": args.budget_seconds,
              "selection_mode": "external_catalog" if args.catalog else args.selection_mode,
              "world_mode": args.world_mode,
              "reference_pairing": "matching gzip stem and row; external requests resolved by full request fingerprint",
              "scene_mode": args.scene_mode,
              "world_policy": "normal independently generated navigation seed" if not world_seeds else
                              "Only benchmark forward backend receives original per-shot seed; no reference action or seed is given to proposal/refinement code. Full Unity/native-history identity is not asserted.",
              "planned": len(requests), "python": sys.version, "platform": platform.platform(),
              "cpu": platform.processor(), "catalog_sha256": sha(args.output/"catalog.json"),
              "affinity": cpu_info,
              "source_sha256": {}, "holdout_seeds": args.holdout_seeds,
              "scope": "Source-forward tasks, one per board or per (board,tactic), depending on selection_mode; stable record hash tie-break. Round-robin tactic subset if limited. Atlas excludes entire tested physical board. Multiple goals on one board are not independent boards. Warm persistent process, request proposals included in timing. Reference actions used only after all timed searches; source_seed mode extracts world seeds beforehand only in the opaque forward backend. No new forward samples mixed with source data.",
              "rows": []}
    if mature_context is not None:
        report["observed_activation_context"] = mature_context
        report["observed_activation_context_sha256"] = hashlib.sha256(json.dumps(mature_context["slots"], sort_keys=True).encode()).hexdigest()
    runtime = Path("local_simulator/runtime")
    payloads = [runtime/"pyphysx/_pyphysx.cp39-win_amd64.pyd",
                Path("training_research/assets/inverse_contact_atlas_v6_20261004.npz")]
    payloads.extend(runtime.glob("physx_*_20261004.json"))
    report["runtime_sha256"] = {str(p): sha(p) for p in payloads if p.is_file()}
    report["data_sha256"] = {str(p): sha(p) for p in sorted(args.data.glob("*.jsonl.gz"))}
    report["numerical_versions"] = {k: getattr(sys.modules[k], "__version__", None)
                                    for k in ("numpy", "scipy", "dfols", "pandas") if k in sys.modules}
    snapshot = args.output/"source_snapshot"
    snapshot.mkdir()
    for path in sorted(Path("training_research").glob("*.py")):
        if path.name.startswith(("inverse_", "solver_", "shot_solver", "benchmark_compact", "legacy_inverse", "contact_seed_forest", "constrained_refine", "goal_geometry_initials", "micro_terminal_refine", "population_search", "isolated_evaluation", "region_feasible_refine", "contact_modes", "contact_distribution_prior", "compact_pairs", "full_contact_prior")):
            report["source_sha256"][str(path)] = sha(path)
            (snapshot/path.name).write_bytes(path.read_bytes())
    if args.profile in ("learned_dfols", "impact_learned", "distribution_dfols", "full_distribution", "full_augmented"):
        from training_research.contact_seed_forest import DEFAULT, IMPACT
        if args.profile in ("full_distribution", "full_augmented"):
            from training_research.full_contact_prior import DEFAULT as model_path
        elif args.profile == "distribution_dfols":
            from training_research.contact_distribution_prior import DEFAULT as model_path
        else:
            model_path = IMPACT if args.profile=="impact_learned" else DEFAULT
        report["learned_model_sha256"] = {str(p): sha(p) for p in sorted(model_path.glob("*")) if p.is_file()}
    def save():
        report["summary"] = summarize(report["rows"])
        (args.output/"report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    save()
    for i, request in enumerate(requests):
        started = time.perf_counter()
        result = solver.solve(request, budget_seconds=args.budget_seconds, include_records=True)
        outer_ms = (time.perf_counter()-started)*1000
        records = result.pop("records")
        diag = result["diagnostics"]
        assert all(r["task_failure"] == failure_reason(r, request["selection"]) for r in records)
        if result["success"]:
            assert any(r["shot"] == result["shot"] and r["task_failure"] is None for r in records)
        calls = [{"shot": r["shot"], "phase": r["search_phase"], "seconds": r["seconds"],
                  "environment_creation_ms": r.get("environment_creation_ms", 0.),
                  "failure": r["task_failure"], "loss": loss(r, request["selection"]),
                  "final": r.get("physical_final"), "prediction": r.get("prediction"),
                  "collision_events": r.get("collision_events"), "rule_violations": r.get("rule_violations")}
                 for r in records]
        evidence = {"request": request, "result": result, "calls": calls}
        with gzip.open(args.output/("%03d.json.gz" % i), "wt", encoding="utf-8") as stream:
            json.dump(evidence, stream, ensure_ascii=False)
        best_initial = min((c["loss"] for c in calls if c["phase"] in ("geometry_initial", "quick_initial")), default=None)
        row = {"index": i, "record_id": request["record_id"], "request_fingerprint": request_fingerprint(request), "scene_key": request["scene_key"],
               "tactic": request["selection"]["tactic"], "stones": len(request["stones"]),
               "success": result["success"], "shot": result["shot"], "elapsed_ms": outer_ms,
               "search_ms": result["elapsed_ms"], "physics_calls": len(calls),
               "initial_success": diag.get("initial_success", False),
               "refinement_success": diag.get("refinement_success", False),
               "initial_generation_ms": diag.get("initial_generation_ms", 0.),
               "environment_creation_total_ms": sum(c["environment_creation_ms"] for c in calls),
               "certified_final_sha256": next((hashlib.sha256(json.dumps(r["physical_final"], sort_keys=True).encode()).hexdigest()
                                                 for r in records if r["shot"]==result["shot"] and r["task_failure"] is None), None),
               "best_initial_loss": best_initial, "best_loss": min((c["loss"] for c in calls), default=None),
               "failure_counts": dict(Counter(c["failure"] for c in calls if c["failure"])),
               "phase_calls": dict(Counter(c["phase"] for c in calls)),
               "phase_ms": {p: 1000*sum(c["seconds"] for c in calls if c["phase"]==p) for p in {c["phase"] for c in calls}}}
        report["rows"].append(row)
        save()
        print(json.dumps({"done": i+1, "total": len(requests), "tactic": row["tactic"], "ok": row["success"],
                          "ms": round(outer_ms), "calls": len(calls), "loss": row["best_loss"]}), flush=True)
    if world_seeds:
        (args.output/"controlled_world_seeds.json").write_text(json.dumps(world_seeds, indent=2), encoding="utf-8")
    # Separate diagnostic pass, so a known action cannot affect later searches.
    if args.replay_references or args.holdout_seeds:
        refs = {}
        if args.replay_references:
            refs = references_for_requests(args.data, requests)
        for request, row in zip(requests, report["rows"]):
            scene = validate_scene(request)
            scene.update(scene_id=scene["scene_key"], family=scene["selection"]["tactic"])
            seed = 20261004+scene["active_index"]*7919
            def replay(shot, seed, name):
                replay_env = make_environment() if args.scene_mode != "persistent" else solver.environment
                if mature_context is not None:
                    from training_research.isolated_evaluation import restore_context
                    restore_context(replay_env, mature_context["slots"])
                r = simulate_record(replay_env, scene, {"shot": shot, "origin": name}, seed, name,
                                    {"goal_radius": .15, "config_hash": "compact-research-v1"})
                return {"failure": failure_reason(r, scene["selection"]), "loss": loss(r, scene["selection"]),
                        "physical_final": r.get("physical_final")}
            replayed = {}
            if row["success"] and args.scene_mode != "persistent":
                replay_seed = world_seeds[request_fingerprint(request)] if world_seeds else seed
                replayed["same_input"] = replay(row["shot"], replay_seed, "same_input_replay")
                row["same_input_replay_pass"] = replayed["same_input"]["failure"] is None
                row["same_input_bitwise"] = hashlib.sha256(json.dumps(replayed["same_input"]["physical_final"], sort_keys=True).encode()).hexdigest()==row["certified_final_sha256"]
            if args.replay_references:
                ref = refs[request_fingerprint(request)]
                row["reference_paired_location"] = ref["paired_location"]
                for name, replay_seed in (("source", ref["physics_seed"]), ("navigation", seed)):
                    replayed[name] = replay(ref["shot"], replay_seed, "reference_"+name)
                    row["reference_"+name+"_pass"] = replayed[name]["failure"] is None
            if row["success"] and args.holdout_seeds:
                holdout_base = world_seeds[request_fingerprint(request)] if world_seeds else seed
                replayed["holdout"] = [replay(row["shot"], (holdout_base+104729*(100+k)) & 0xffffffff, "holdout") for k in range(args.holdout_seeds)]
                row["holdout_passed"] = sum(r["failure"] is None for r in replayed["holdout"])
            (args.output/("%03d_replay.json" % row["index"])).write_text(json.dumps(replayed), encoding="utf-8")
        save()
    report["status"] = "complete"
    save()
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
