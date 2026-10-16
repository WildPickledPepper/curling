"""Reusable scene + complete terminal goal -> certified BESTSHOT application.

python -m training_research.shot_solver --scene training_research/fixtures/sampled_goal_draw.json
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import time

from training_research.inverse_dataset.cli import make_environment, simulate_record
from training_research.inverse_dataset.sampling import validate_scene
from training_research.inverse_dataset.selection import failure_reason


class BudgetedShotSolver:
    """Construct once to reuse the native scene; observations certify each shot.

    Calls on the same instance must be serial. Unknown real-world friction is
    not inferred; extra-seed robustness is a separate acceptance policy.
    """

    def __init__(self, environment=None, *, search_profile="baseline", forward_simulator=None):
        from training_research.solver_experiments import PROFILE_NAMES, profile_kwargs
        if search_profile not in PROFILE_NAMES:
            raise ValueError("unknown search_profile: " + str(search_profile))
        self.environment = make_environment() if environment is None else environment
        self.search_profile = search_profile
        self.search_options = profile_kwargs(search_profile)
        self.forward_simulator = forward_simulator

    def solve(self, scene, *, budget_seconds=10., max_calls=256, seed=20261004,
              required_seed_successes=1, include_records=False, cancelled=None):
        if not math.isfinite(budget_seconds) or budget_seconds <= 0:
            raise ValueError("budget_seconds must be finite and positive")
        if cancelled is not None and not callable(cancelled):
            raise ValueError("cancelled must be a callable")
        for name, value in (("max_calls", max_calls), ("required_seed_successes", required_seed_successes)):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(name + " must be a positive integer")
        scene = validate_scene(scene)
        scene = {**scene, "scene_id": scene.get("scene_id", "online"),
                 "family": scene.get("family", "online")}
        if "selection" not in scene:
            raise ValueError("scene needs a selection with a complete terminal goal")
        records = []
        started = time.perf_counter()

        def evaluate(shot, seed_index, phase):
            forward = simulate_record if self.forward_simulator is None else self.forward_simulator
            record = forward(self.environment, scene,
                {"shot": list(shot), "origin": phase},
                int(seed) + scene["active_index"] * 7919 + 104729 * seed_index,
                "online:%d" % len(records), {"goal_radius": .15, "config_hash": "shot-solver-app-v1"})
            record.update(seed_index=seed_index, search_phase=phase,
                          task_failure=failure_reason(record, scene["selection"]))
            if record["status"] != "complete":
                raise RuntimeError("forward simulation failed: " + record.get("error", "unknown error"))
            records.append(record)
            return record

        if scene["selection"]["tactic"] == "double_hit":
            from training_research.inverse_initials import solve
            options = {}
        else:
            from training_research.inverse_goal_search import solve
            options = self.search_options
        attempts, diagnostics = solve(scene, evaluate=evaluate,
            elapsed=lambda: budget_seconds if cancelled is not None and cancelled() else time.perf_counter()-started,
            budget_seconds=budget_seconds,
            max_calls=max_calls, required_seed_successes=required_seed_successes, **options)
        shot = attempts[0].get("bestshot")
        result = {"status": attempts[0]["status"], "success": shot is not None,
            "shot": shot, "elapsed_ms": (time.perf_counter()-started)*1000,
            "budget_seconds": budget_seconds, "physics_calls": len(records),
            "required_seed_successes": required_seed_successes, "scene_key": scene["scene_key"],
            "search_profile": self.search_profile,
            "diagnostics": diagnostics,
            "scope": "Observed search seeds only; a miss returns no executable action. Startup excluded; in-flight calls may finish beyond the budget."}
        if include_records:
            result["records"] = records
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", type=Path, required=True)
    parser.add_argument("--budget-seconds", type=float, default=10.)
    parser.add_argument("--max-calls", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--required-seed-successes", type=int, default=1)
    parser.add_argument("--include-records", action="store_true")
    from training_research.solver_experiments import PROFILE_NAMES
    parser.add_argument("--search-profile", choices=PROFILE_NAMES, default="baseline")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.output and args.output.exists():
        parser.error("output already exists; choose a new path")
    result = BudgetedShotSolver(search_profile=args.search_profile).solve(json.loads(args.scene.read_text(encoding="utf-8")),
        budget_seconds=args.budget_seconds, max_calls=args.max_calls, seed=args.seed,
        required_seed_successes=args.required_seed_successes, include_records=args.include_records)
    serialized = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized+"\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
