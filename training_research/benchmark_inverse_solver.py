"""Time the existing double solver on the current accelerated strict simulator.

No successful shot or dataset labels are used as initial guesses. Passive
observation records when a candidate first passes the specified tactical goal.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import statistics
import sys
import time

from training_research.inverse_dataset.cli import file_sha, make_environment, write_json
from training_research.inverse_dataset.sampling import validate_scene
from training_research.inverse_dataset.selection import failure_reason
from training_research.inverse_dataset.schema import HOUSE_X, STONE_R

ROOT = Path(__file__).resolve().parents[1]


def background_snapshot():
    path = ROOT / "training_research/runs/inverse_expanded_batch1_20261004/manifest.json"
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    return {"path": str(path), "status": report["status"],
            "completed_records": report.get("summary", {}).get("counts", {}).get("records", 0)}


def main(argv=None, *, environment=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene-json", type=Path, default=ROOT / "training_research/inverse_dataset/fixtures/manual_boards.json")
    parser.add_argument("--scene-id", default="manual_double_offset")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--method", choices=("existing", "geometry", "legacy_seeds", "legacy_refine", "initial_refine", "initial_refine_previous", "initial_refine_poll", "initial_refine_probe"), default="existing")
    parser.add_argument("--budget-seconds", type=float, default=20.)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--holdout-seeds", type=int, default=10, help="extra seeds after timed search; excluded from search latency")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.repeats < 1 or args.budget_seconds <= 0 or args.holdout_seeds < 0:
        parser.error("repeats and budget must be positive; holdout-seeds cannot be negative")
    payload = json.loads(args.scene_json.read_text(encoding="utf-8"))
    scenes = payload if isinstance(payload, list) else payload["scenes"]
    scene = validate_scene(next(s for s in scenes if s["scene_id"] == args.scene_id))
    selection = scene["selection"]
    if selection["tactic"] != "double_hit":
        raise ValueError("benchmark currently measures the existing double-hit solver")
    targets = tuple(sorted(selection["first_contact_any"]))
    from planning_proxy.tactical_library_strategy import double_mads_solver as solver
    from planning_proxy.tactical_library_strategy.double_outcome_goal import BoundDoubleTargets
    from training_research.inverse_dataset.cli import reset_environment

    setup_start = time.perf_counter()
    env = make_environment() if environment is None else environment
    setup_ms = (time.perf_counter() - setup_start) * 1000
    warm_start = time.perf_counter()
    reset_environment(env, scene, args.seed)
    env.play((3., 0., 0.))
    warmup_ms = (time.perf_counter() - warm_start) * 1000
    original_play, original_evaluate, original_factory = env.play, solver.evaluate_one, solver.StrictCurlingEnd
    rows, raw_calls = [], []
    started = 0.
    active_row = None
    def observed_play(shot, *positional, **keywords):
        call_start = time.perf_counter()
        result = original_play(shot, *positional, **keywords)
        record = {"shot": list(shot), "physics_seed": env.seed + scene["active_index"] * 7919,
                  "status": "complete", "rule_violations": [], "prediction": {k: v for k, v in result.items() if k != "states"},
                  "physical_final": result["states"], "collision_events": list(env.scene._dataset_collision_events)}
        if args.method != "existing":
            record["initial_state"] = env._benchmark_initial
        # This fixture is after protected-guard deliveries; the existing solver
        # also checks legality for every candidate in evaluate_one().
        if scene["active_index"] < 5:
            raise ValueError("benchmark fixture must be after protected-guard phase")
        record.update(ms=(time.perf_counter()-call_start)*1000, elapsed_ms=(time.perf_counter()-started)*1000,
                      task_failure=failure_reason(record, selection))
        raw_calls.append(record)
        if record["task_failure"] is None and active_row["first_single_seed_success_ms"] is None:
            active_row["first_single_seed_success_ms"] = record["elapsed_ms"]
        return result
    def observed_evaluate(*positional, **keywords):
        before = len(raw_calls)
        result = original_evaluate(*positional, **keywords)
        calls = raw_calls[before:]
        active_row["candidate_count"] += 1
        if (len(calls) == 3 and all(r["task_failure"] is None for r in calls) and result.rule_legal
                and active_row["first_three_seed_success_ms"] is None):
            active_row["first_three_seed_success_ms"] = (time.perf_counter()-started)*1000
            active_row["first_three_seed_success_shot"] = list(calls[0]["shot"])
            active_row["calls_to_first_three_seed_success"] = len(raw_calls)
        return result
    def geometry_search():
        """Try geometric proposals, fail fast, validate a hit on three seeds.

        These offsets express candidate sampling only. No outcome or inverse
        physical formula is assumed; exact forward observations accept them.
        """
        seeds = [args.seed + scene["active_index"]*7919 + 104729*i for i in range(3)]
        target_stones = sorted((s for s in scene["stones"] if s["index"] in targets), key=lambda s: -s["y"])
        for v in (6., 5.6, 5.2, 4.8):
            for target in target_stones:
                for offset in (0., .5*STONE_R, -.5*STONE_R, .9*STONE_R, -.9*STONE_R, 1.2*STONE_R, -1.2*STONE_R):
                    if time.perf_counter()-started >= args.budget_seconds:
                        return [{"status": "NOT_FOUND_WITHIN_BUDGET"}]
                    shot = (v, max(-2.23, min(2.23, target["x"]-HOUSE_X+offset)), 0.)
                    active_row["candidate_count"] += 1
                    before = len(raw_calls)
                    for seed in seeds:
                        env._benchmark_initial = reset_environment(env, scene, seed)
                        observed_play(shot)
                        if raw_calls[-1]["task_failure"] is not None:
                            break
                    calls = raw_calls[before:]
                    if len(calls) == 3 and all(r["task_failure"] is None for r in calls):
                        active_row["first_three_seed_success_ms"] = (time.perf_counter()-started)*1000
                        active_row["first_three_seed_success_shot"] = list(shot)
                        active_row["calls_to_first_three_seed_success"] = len(raw_calls)
                        return [{"status": "FOUND_ON_THREE_OBSERVED_SEEDS", "bestshot": list(shot)}]
        return [{"status": "NOT_FOUND_IN_GEOMETRIC_PROPOSALS"}]
    def legacy_search():
        if args.method.startswith("initial_refine"):
            from training_research.inverse_initials import solve
        else:
            from training_research.legacy_inverse import solve
        def evaluate(shot, seed_index, phase):
            if seed_index == 0:
                active_row["candidate_count"] += 1
            seed = args.seed + scene["active_index"]*7919 + 104729*seed_index
            env._benchmark_initial = reset_environment(env, scene, seed)
            observed_play(shot)
            record = raw_calls[-1]
            record.update(search_phase=phase, candidate_number=active_row["candidate_count"], seed_index=seed_index)
            if seed_index == 2 and record["task_failure"] is None:
                active_row["first_three_seed_success_ms"] = (time.perf_counter()-started)*1000
                active_row["first_three_seed_success_shot"] = list(shot)
                active_row["calls_to_first_three_seed_success"] = len(raw_calls)
                active_row["successful_phase"] = phase
            return record
        if args.method == "initial_refine_previous":
            options = {"max_calls":96,"conservative_rounds":6,"local_rounds":12}
        elif args.method == "initial_refine_poll":
            options = {"refinement_profile":"fast_poll"}
        elif args.method == "initial_refine_probe":
            options = {"initial_polish":True}
        elif args.method == "initial_refine":
            options = {}
        else:
            options = {"refine":args.method == "legacy_refine"}
        attempts, diagnostics = solve(scene, evaluate=evaluate, elapsed=lambda:time.perf_counter()-started,
                                      budget_seconds=args.budget_seconds, **options)
        active_row["legacy_diagnostics"] = diagnostics
        return attempts
    env.play = observed_play
    solver.evaluate_one = observed_evaluate
    solver.StrictCurlingEnd = lambda **kwargs: env
    board = [{**s, "owner": "opponent" if s["index"] % 2 != scene["active_index"] % 2 else "self"} for s in scene["stones"]]
    contract = {"double_goal_id": "benchmark_two_bound_targets_out", "required_opponent_removed_count": 2,
                "terminal_board_predicate": {}}
    report = {"scene": scene, "method": args.method,
              "solver": "existing solve_double_outcome_contract; default coarse grid and MADS" if args.method == "existing" else "front target first; geometric centre/edge proposals; exact fail-fast search; stop at first three-seed pass",
              "initial_shot_source": "existing analytic coarse proposals; no solved dataset shots" if args.method == "existing" else "target centres and stone-radius offsets; no solved dataset shots",
              "goal": selection, "python": sys.version, "platform": platform.platform(),
              "setup_ms": setup_ms, "warmup_ms": warmup_ms, "match_seed": args.seed,
              "physics_seeds": [args.seed + scene["active_index"]*7919 + 104729*i for i in range(3)],
              "background_at_start": background_snapshot(),
              "accelerated_flags": {key: getattr(env, key) for key in ("training_fast", "prediction_native_random", "prediction_native_steps", "prediction_merged_steps", "prediction_native_scene_steps")},
              "source_sha256": {str(p.relative_to(ROOT)): file_sha(p) for p in (Path(__file__), Path(solver.__file__), ROOT/"local_simulator/examples/train_policy_tree_selfplay.py", ROOT/"local_simulator/unity_prediction.py", ROOT/"local_simulator/unity_physx.py")}}
    if args.method.startswith("legacy_"):
        from training_research.legacy_inverse import SOURCE_FILES
        report.update(solver="archived double mathematical seeds; current full-goal MADS-style adapter" if args.method == "legacy_refine" else "archived double mathematical seeds; current exact fail-fast validation",
                      initial_shot_source="unchanged archived two-order contact geometry + curl/free-flight inverse + legacy seed; six-seed cap; no solved dataset shots",
                      scope="old initial generator reused; current recovered motion for proposal paths; old score contract not reused; strict full requested goal and observed collision chain decide acceptance")
        report["source_sha256"].update({str(p.relative_to(ROOT)): file_sha(p) for p in (*SOURCE_FILES, ROOT/"training_research/legacy_inverse.py", ROOT/"local_simulator/runtime_support/tools/reverse/recovered_curling_motion.py", ROOT/"local_simulator/runtime_support/tools/reverse/front_half_pcm_replay.py")})
    if args.method.startswith("initial_refine"):
        from training_research.legacy_inverse import SOURCE_FILES
        report.update(solver="quick straight entrances + vectorized diverse geometry + budgeted local refinement",
                      initial_shot_source="initial board geometry and cached recovered free-flight paths only; no saved successful shots",
                      scope="proposal geometry approximate; full requested goal and observed collision chain required; deadline checked before each call")
        report["source_sha256"].update({str(p.relative_to(ROOT)):file_sha(p) for p in (*SOURCE_FILES, ROOT/"training_research/legacy_inverse.py", ROOT/"training_research/inverse_initials.py")})
        if args.method=="initial_refine_probe":
            report.update(solver="current geometric initials; two-entrance axis polish (.12,.03,.4); unchanged bounded MADS and exact three-seed acceptance",
                          initial_shot_source="scene/goal geometry only; six small coordinate probes per entrance; no saved reference action")
    try:
        for repeat in range(args.repeats):
            raw_calls = []
            active_row = {"repeat": repeat, "candidate_count": 0, "first_single_seed_success_ms": None,
                          "first_three_seed_success_ms": None}
            started = time.perf_counter()
            if args.method == "existing":
                attempts = [a.to_json() for a in solver.solve_double_outcome_contract(contract, [BoundDoubleTargets(targets, 1)], board,
                    own_throw_number=scene["active_index"]//2+1, mirrored_from_runtime_board=False, physics_seeds=3,
                    match_seed=args.seed, decision_budget_seconds=args.budget_seconds, shot_index=scene["active_index"])]
            elif args.method == "geometry":
                attempts = geometry_search()
            else:
                attempts = legacy_search()
            active_row.update(return_ms=(time.perf_counter()-started)*1000, physics_calls=len(raw_calls),
                              attempts=attempts, calls=raw_calls)
            rows.append(active_row)
            report["rows"] = rows
            args.output.parent.mkdir(parents=True, exist_ok=True)
            write_json(args.output, report)
            print(json.dumps({k:v for k,v in active_row.items() if k not in ("calls", "attempts", "legacy_diagnostics")}, ensure_ascii=False), flush=True)
    finally:
        env.play, solver.evaluate_one, solver.StrictCurlingEnd = original_play, original_evaluate, original_factory
    report["background_at_end"] = background_snapshot()
    report["summary"] = {key: {"median": statistics.median(values), "min": min(values), "max": max(values)}
                         for key in ("first_single_seed_success_ms", "first_three_seed_success_ms", "return_ms")
                         if (values := [r[key] for r in rows if r[key] is not None])}
    report["success_repeats"] = sum(r["first_three_seed_success_ms"] is not None for r in rows)
    found = next((r["first_three_seed_success_shot"] for r in rows if r["first_three_seed_success_ms"] is not None), None)
    if found is not None:
        holdout_start = time.perf_counter()
        holdout = []
        for i in range(args.holdout_seeds):
            seed = args.seed + scene["active_index"]*7919 + 104729*(100+i)
            initial_state = reset_environment(env, scene, seed)
            result = env.play(found)
            record = {"physics_seed": seed, "status": "complete", "rule_violations": [], "prediction": {k:v for k,v in result.items() if k != "states"},
                      "physical_final": result["states"], "collision_events": list(env.scene._dataset_collision_events), "initial_state":initial_state}
            record["task_failure"] = failure_reason(record, selection)
            holdout.append(record)
        report["holdout"] = {"shot": found, "seeds": len(holdout), "passed": sum(r["task_failure"] is None for r in holdout),
                              "ms": (time.perf_counter()-holdout_start)*1000, "records": holdout,
                              "scope": "new seeds, same scene; outside timed search; finite-sample validation"}
    write_json(args.output, report)
    print(json.dumps({"summary": report["summary"], "success_repeats": report["success_repeats"],
                      "holdout_passed": report.get("holdout", {}).get("passed"), "output": str(args.output.resolve())}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
