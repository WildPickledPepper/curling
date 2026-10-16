"""Offline initial-versus-poll diagnosis on actual failed sampled requests.

Reference-neighbour starts are diagnostic oracles, never online search inputs.
The two best-effort restart arms use only the original solver's own output.
Neither arm changes physics, goals, acceptance or random generation.
"""
import argparse
import ctypes as C
import inspect
import json
from pathlib import Path
import sys
import time

from training_research.inverse_dataset.cli import file_sha, make_environment, simulate_record, write_json
from training_research.inverse_dataset.selection import failure_reason
from training_research import inverse_goal_search as search


def poll_trace():
    lines, start = inspect.getsourcelines(search.solve)
    checkpoint = start + next(i for i, line in enumerate(lines) if "original=p[" in line)
    rows = []
    def trace(frame, event, arg):
        if frame.f_code is search.solve.__code__ and event == "line" and frame.f_lineno == checkpoint:
            p = frame.f_locals["p"]
            rows.append({"iteration": frame.f_locals["iteration"], "mesh": p["mesh"],
                         "shot": list(p["current"]["shot"]), "loss": p["current"]["loss"]})
        return trace if frame.f_code is search.solve.__code__ else None
    return rows, trace


def recorded_trace(evidence):
    """Re-run control flow against recorded outputs, checking every requested shot."""
    calls = evidence["calls"]
    initials = [r["shot"] for r in calls if r["search_phase"] == "geometry_initial"]
    saved = search.proposals
    search.proposals = lambda *args: [(i, tuple(s), (i,)) for i, s in enumerate(initials)]
    used = 0
    def evaluate(shot, seed, phase):
        nonlocal used
        r = calls[used]
        assert list(shot) == r["shot"], (used, shot, r["shot"])
        assert phase == r["search_phase"]
        used += 1
        return r
    rows, trace = poll_trace()
    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        result, diag = search.solve(evidence["scene"], evaluate=evaluate,
            elapsed=lambda: 10. if used == len(calls) else 0., max_calls=128)
    finally:
        sys.settrace(previous)
        search.proposals = saved
    assert used == len(calls), (used, len(calls))
    groups = {}
    for p in rows:
        groups.setdefault(p["iteration"], []).append(p)
    duplicates = [i for i, ps in groups.items() if len(ps) == 2 and ps[0]["shot"] == ps[1]["shot"]]
    return {"checked_call_prefix": used, "polls": rows, "duplicate_parent_iterations": duplicates,
            "best_loss": diag["best_loss"]}


def run_arm(env, scene, seed, start_shot, label, budget, max_calls, fine=False):
    saved = search.proposals
    search.proposals = lambda *args: [(0., tuple(start_shot), (label,))]
    fn = search.solve
    if fine:
        # Same source loop and directions; only the starting/restart mesh is smaller.
        source = inspect.getsource(search.solve).replace('"mesh":1.', '"mesh":.125').replace('"mesh":.5', '"mesh":.125')
        namespace = dict(search.__dict__)
        exec(compile(source, "<diagnostic-fine-mesh>", "exec"), namespace)
        fn = namespace["solve"]
    calls = []
    started = time.perf_counter()
    def evaluate(shot, seed_index, phase):
        r = simulate_record(env, scene, {"shot": list(shot), "origin": label + ":" + phase},
            seed, label + ":" + str(len(calls)), {"goal_radius": .15, "config_hash": "miss-diagnosis-v1"})
        r.update(task_failure=failure_reason(r, scene["selection"]), search_phase=phase)
        calls.append(r)
        return r
    try:
        result, diag = fn(scene, evaluate=evaluate, elapsed=lambda: time.perf_counter()-started,
            budget_seconds=budget, max_calls=max_calls, required_seed_successes=1)
    finally:
        search.proposals = saved
    return {"label": label, "physics_seed": seed, "start_shot": list(start_shot), "budget_seconds": budget,
            "max_calls": max_calls, "result": result[0], "success": "bestshot" in result[0],
            "elapsed_ms": (time.perf_counter()-started)*1000, "diagnostics": diag, "calls": calls}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--misses", type=Path, default=Path("training_research/runs/inverse_miss_collision_distance_20261004.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cpu", type=int, default=4)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args(argv)
    if args.output.exists() and any(args.output.iterdir()) and not args.resume:
        raise ValueError("output must be new/empty")
    args.output.mkdir(parents=True, exist_ok=True)
    misses = json.loads(args.misses.read_text(encoding="utf-8"))
    report = {"status": "running", "planned": len(misses), "rows": [],
              "source_sha256": {str(p.resolve()): file_sha(p) for p in (Path(__file__), Path(search.__file__), args.misses)},
              "scope": "Offline diagnosis. Reference-neighbour arm is oracle-assisted and is NOT an online solve. Best-effort arms use original search output only, each with 3 seconds/48 calls. Exact scenes and acceptance retained; native scene reused, reset between calls; before/after reference feasibility controls retained, not bit-identical native history."}
    if args.resume:
        report = json.loads((args.output / "report.json").read_text(encoding="utf-8"))
        report["resume_source_sha256"] = {str(Path(__file__).resolve()): file_sha(Path(__file__))}
        report["resume_native_scene_is_new"] = True
    kernel = C.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentThread.restype = C.c_void_p
    kernel.SetThreadAffinityMask.argtypes = (C.c_void_p, C.c_size_t)
    kernel.SetThreadAffinityMask.restype = C.c_size_t
    thread = kernel.GetCurrentThread()
    previous = kernel.SetThreadAffinityMask(thread, 1 << args.cpu)
    if not previous: raise C.WinError(C.get_last_error())
    try:
        env = make_environment()
        for index, item in enumerate(misses):
            if index < len(report["rows"]): continue
            old = json.loads(Path(item["evidence"]).read_text(encoding="utf-8"))
            scene = old["scene"]
            assert not scene["selection"].get("require_no_contact")
            def control(seed, label):
                r = simulate_record(env, scene, {"shot": old["reference"]["shot"], "origin": label}, seed, label,
                    {"goal_radius": .15, "config_hash": "miss-diagnosis-v1"})
                r["task_failure"] = failure_reason(r, scene["selection"])
                return r
            nav_seed = old["navigation_seed"]
            nav_control = control(nav_seed, "reference_navigation_before")
            known_seed = nav_seed if nav_control["task_failure"] is None else old["reference"]["physics_seed"]
            before = control(known_seed, "reference_known_feasible_before")
            ref = old["reference"]["shot"]
            perturbed = search.clip((ref[0]+.12, ref[1]+.06, ref[2]+.8))
            near = run_arm(env, scene, known_seed, perturbed, "oracle_neighbour_original_poll", 10., 128)
            best = old["diagnostics"]["best_effort_shot"]
            normal = run_arm(env, scene, nav_seed, best, "own_best_original_mesh", 3., 48)
            fine = run_arm(env, scene, nav_seed, best, "own_best_fine_mesh", 3., 48, fine=True)
            after = control(known_seed, "reference_known_feasible_after")
            trace = recorded_trace(old)
            evidence = args.output / ("%03d.json" % index)
            write_json(evidence, {"scene": scene, "original_evidence": item["evidence"], "recorded_trace": trace,
                "reference_navigation_before": nav_control, "reference_before": before, "reference_after": after,
                "arms": [near, normal, fine]})
            row = {"scene_id": scene["scene_id"], "tactic": item["tactic"], "evidence": str(evidence.resolve()),
                "navigation_reference_pass": nav_control["task_failure"] is None, "near_reference_seed": known_seed,
                "before_reference_pass": before["task_failure"] is None, "after_reference_pass": after["task_failure"] is None,
                "near_start_pass": near["calls"][0]["task_failure"] is None,
                "near_original_poll_success": near["success"], "near_calls": len(near["calls"]),
                "own_best_original_success": normal["success"], "own_best_fine_success": fine["success"],
                "original_duplicate_parent_iterations": trace["duplicate_parent_iterations"]}
            report["rows"].append(row)
            report["summary"] = {"tested": len(report["rows"]), **{k: sum(r[k] for r in report["rows"]) for k in
                ("navigation_reference_pass", "before_reference_pass", "after_reference_pass", "near_start_pass", "near_original_poll_success", "own_best_original_success", "own_best_fine_success")},
                "duplicate_parent_cases": sum(bool(r["original_duplicate_parent_iterations"]) for r in report["rows"])}
            write_json(args.output / "report.json", report)
            print(json.dumps({"completed": index+1, "planned": len(misses), **row}, ensure_ascii=False), flush=True)
        report["status"] = "complete"
    finally:
        kernel.SetThreadAffinityMask(thread, previous)
    write_json(args.output / "report.json", report)
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
