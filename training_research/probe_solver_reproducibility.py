"""Read native initial fields and compare identical forward inputs by history.

Uses only recorded forward boards/actions for diagnosis. No physics setters,
compensation, or solver changes are introduced by the observer.
"""
from __future__ import annotations

import argparse
import ctypes as C
import gzip
import hashlib
import json
from pathlib import Path
import time


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--indices", default="0,1,2,5,6")
    args = parser.parse_args(argv)
    if args.output.exists():
        raise ValueError("output must be new")
    k = C.WinDLL("kernel32", use_last_error=True)
    k.GetCurrentProcess.restype = C.c_void_p
    k.SetProcessAffinityMask.argtypes = (C.c_void_p, C.c_size_t)
    if not k.SetProcessAffinityMask(k.GetCurrentProcess(), 16):
        raise C.WinError(C.get_last_error())
    k.SetThreadExecutionState(C.c_uint32(0x80000001))
    from training_research.inverse_dataset.cli import make_environment, simulate_record
    from training_research.inverse_dataset.sampling import validate_scene
    from training_research.inverse_dataset.selection import failure_reason
    all_cases = json.loads(args.catalog.read_text(encoding="utf-8"))
    cases = [all_cases[int(i)] for i in args.indices.split(",")]
    data = Path(__file__).parent/"datasets/forward_samples_20261004"
    from training_research.compact_pairs import references_for_requests, request_fingerprint
    references = references_for_requests(data, all_cases)
    report = {"scope": "Same original per-shot seed, original board/action, normal simulator. Pose/velocity and material getters only. History dependence is measured; no unobserved internal mechanism is inferred.",
              "runtime_sha256": hashlib.sha256(Path("local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd").read_bytes()).hexdigest(),
              "cpu": 4, "cases": []}
    kept_environments = []
    def environment():
        env = make_environment()
        kept_environments.append(env)
        return env
    def evaluate(env, raw, name, observe=True):
        scene = validate_scene(raw)
        scene.update(scene_id=raw["record_id"], family=raw["selection"]["tactic"])
        ref = references[request_fingerprint(raw)]
        original_play = env.play
        native_start = []
        def observed_play(shot):
            for slot in env.scene.slots:
                native_start.append({"index": slot.index, "enabled": slot.enabled,
                    "unity_constraints": slot.unity_constraints, "in_scene": slot.in_scene,
                    "static_friction": float(slot.material.get_static_friction()),
                    "dynamic_friction": float(slot.material.get_dynamic_friction()),
                    "restitution": float(slot.material.get_restitution())})
            return original_play(shot)
        if observe:
            env.play = observed_play
        cpu = time.process_time()
        try:
            record = simulate_record(env, scene, {"shot": ref["shot"], "origin": name}, ref["physics_seed"], name,
                                     {"goal_radius": .15, "config_hash": "reproducibility-observer-v1"})
        finally:
            env.play = original_play
        record.update(process_seconds=time.process_time()-cpu, native_start=native_start,
                      initial_pose_hash=digest(record["before"]),
                      initial_material_hash=digest(native_start), final_hash=digest(record.get("physical_final")),
                      failure=failure_reason(record, scene["selection"]))
        return record
    for raw in cases:
        env = environment()
        repeated = [evaluate(env, raw, "repeated_%d" % i) for i in range(4)]
        changed = environment()
        history = [evaluate(changed, raw, "history_initial")]
        for i, other in enumerate(cases):
            if other["scene_key"] == raw["scene_key"]:
                continue
            evaluate(changed, other, "preceding_%d" % i)
            history.append(evaluate(changed, raw, "history_after_%d" % i))
        fresh = [evaluate(environment(), raw, "fresh_%d" % i) for i in range(3)]
        unobserved = evaluate(environment(), raw, "fresh_without_observer", observe=False)
        groups = {"repeated": repeated, "different_preceding_boards": history, "fresh_worlds": fresh}
        row = {"record_id": raw["record_id"], "scene_key": raw["scene_key"],
               "groups": groups, "fresh_without_observer": unobserved,
               "observer_equivalence_to_fresh_first": fresh[0]["final_hash"] == unobserved["final_hash"],
               "summary": {name: {"runs": len(rows),
                    "distinct_before": len({r["initial_pose_hash"] for r in rows}),
                    "distinct_materials": len({r["initial_material_hash"] for r in rows}),
                    "distinct_finals": len({r["final_hash"] for r in rows}),
                    "goal_passed": sum(r["failure"] is None for r in rows),
                    "median_seconds": sorted(r["seconds"] for r in rows)[len(rows)//2]} for name, rows in groups.items()}}
        report["cases"].append(row)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"record": raw["record_id"], "summary": row["summary"],
                          "observer_same": row["observer_equivalence_to_fresh_first"]}), flush=True)
    k.SetThreadExecutionState(C.c_uint32(0x80000000))


if __name__ == "__main__":
    main()
