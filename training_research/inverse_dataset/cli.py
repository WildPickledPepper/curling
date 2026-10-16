"""Collect exact accelerated forward results and encode inverse-shot shards.

python -m training_research.inverse_dataset.cli collect --help
python -m training_research.inverse_dataset.cli encode --help
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from datetime import datetime, timezone
import hashlib
import json
from itertools import groupby
import multiprocessing
from pathlib import Path
import platform
import sys
import time
from typing import Any

import numpy as np

from .sampling import FAMILIES, deduplicate_scenes, load_scenes, shot_candidates, synthetic_scene, task_rng
from .schema import (ACTION_SCALE, FEATURES, GOAL_TYPES, SCHEMA, TACTICS, X_SCALE, Y_SCALE,
                     achieved_views, digest, encode_action, encode_input, split_for_group)

ROOT = Path(__file__).resolve().parents[2]
_ENV = None


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    temporary.replace(path)


def file_sha(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def make_environment():
    """Observe the driver's already-produced reports; never drain PhysX twice."""
    from local_simulator.runtime_loader import install_bundled_pyphysx
    install_bundled_pyphysx()
    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
    from local_simulator.unity_prediction import UnityPredictionClock, UnityPredictionDriver

    class RecordingDriver(UnityPredictionDriver):
        def fixed_update(self):
            result = super().fixed_update()
            for report in result["stoneReports"]:
                if int(report.get("events") or 0) & 4:
                    self.scene._dataset_collision_events.append({
                        "step": self.fixed_count,
                        "stones": sorted((int(report["stoneIndex0"]), int(report["stoneIndex1"]))),
                    })
            return result

    class RecordingEnd(StrictCurlingEnd):
        def _run_prediction(self, active_index, shot, noises, *, friction_seed=None):
            self.scene._dataset_collision_events = []
            self.scene.start_bestshot(active_index, shot, yaw=0.0)
            driver = RecordingDriver(
                self.scene, active_index, seed=0 if friction_seed is None else friction_seed,
                noises=noises, motion_stepper=self.motion_stepper, use_lean_steps=self.training_fast,
                native_random=self.prediction_native_random, native_steps=self.prediction_native_steps,
                merge_steps=self.prediction_merged_steps, native_scene_steps=self.prediction_native_scene_steps,
                clock=UnityPredictionClock(fixed_dt=self.scene.dt, time_scale=self.prediction_time_scale),
            )
            return driver.run(frame_elapsed=self.prediction_frame_elapsed)

    return RecordingEnd(seed=0, training_fast=True)


def initialize_worker():
    global _ENV
    _ENV = make_environment()


def reset_environment(env, scene: dict[str, Any], physics_seed: int):
    positions = [0.0] * 32
    yaws = {i: 0.0 for i in range(16)}
    for stone in scene["stones"]:
        i = int(stone["index"])
        positions[2*i:2*i+2] = [stone["x"], stone["y"]]
        yaws[i] = stone["yaw"]
    env.scene.reset_positions(positions, yaw_overrides=yaws)
    env.shot_number = int(scene["active_index"])
    # play() derives this exact per-shot seed, using its lazy recovered RNG.
    env.seed = int(physics_seed) - env.shot_number * 7919
    return env.states()


def simulate_record(env, scene, proposal, physics_seed, record_id, config):
    from planning_proxy.competition_rules import RuleBoardStone, free_guard_rule_violations
    active = int(scene["active_index"])
    record = {"schema": SCHEMA, "record_id": record_id, "scene_id": scene["scene_id"],
              "scene_key": scene["scene_key"], "group_id": scene["group_id"], "family": scene["family"],
              "active_index": active, "requested_scene": scene, "shot": proposal["shot"],
              "proposal_origin": proposal["origin"], "physics_seed": int(physics_seed),
              "goal_radius": config["goal_radius"], "config_hash": config["config_hash"],
              "status": "error"}
    start = time.perf_counter()
    try:
        before = reset_environment(env, scene, physics_seed)
        record["before"] = before
        result = env.play(proposal["shot"])
        if not result["settled"]:
            raise RuntimeError("predictor returned an unfinished scene")
        physical = result.pop("states")
        initial_rule_board = [RuleBoardStone(i, "self" if i % 2 == active % 2 else "opponent", float(s["x"]), float(s["y"])) for i, s in enumerate(before) if s["enabled"]]
        violations = free_guard_rule_violations(initial_rule_board, physical, shot_index=active)
        record.update(status="complete", physical_final=physical,
                      # This is a local rule-check view, not an official server ruling.
                      rules_final=before if violations else physical,
                      rule_violations=violations, prediction=result,
                      collision_events=list(env.scene._dataset_collision_events))
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
    record["seconds"] = time.perf_counter() - start
    return record


def encode_shard(raw_path: Path, output_prefix: Path, max_views: int, split_seed: int) -> dict[str, Any]:
    arrays = {k: [] for k in ("stones", "yaw", "tactic", "context", "actions", "shots", "split", "record_id", "sample_id", "group_id")}
    stats = Counter()
    groups, families, tactics = Counter(), Counter(), Counter()
    metadata_path = output_prefix.with_suffix(".samples.jsonl")
    metadata_tmp = metadata_path.with_suffix(metadata_path.suffix + ".tmp")
    with raw_path.open(encoding="utf-8") as raw, metadata_tmp.open("w", encoding="utf-8") as output:
        for line in raw:
            record = json.loads(line)
            if record.get("schema") != SCHEMA:
                raise ValueError("unsupported raw schema")
            stats["records"] += 1
            stats[record["status"]] += 1
            stats["illegal"] += bool(record.get("rule_violations"))
            families[record["family"]] += 1
            split = split_for_group(record["group_id"], split_seed)
            for view_index, view in enumerate(achieved_views(record, max_views)):
                encoded = encode_input(record["before"], view["goal"], record["active_index"], view["tactic"])
                action = encode_action(record["shot"])
                sample_id = record["record_id"] + ":" + str(view_index)
                for key, value in encoded.items():
                    arrays[key].append(value)
                for key, value in (("actions", action), ("shots", record["shot"]), ("split", split), ("record_id", record["record_id"]), ("sample_id", sample_id), ("group_id", record["group_id"])):
                    arrays[key].append(value)
                output.write(json.dumps({"sample_id": sample_id, "record_id": record["record_id"], "group_id": record["group_id"], "split": split, **view}, ensure_ascii=False, allow_nan=False) + "\n")
                stats["samples"] += 1
                groups[str(split)] += 1
                tactics[view["tactic"]] += 1
    shapes = {"stones": (16, 14), "yaw": (16, 3), "tactic": (len(TACTICS),), "context": (2,), "actions": (3,), "shots": (3,)}
    packed = {}
    for key, values in arrays.items():
        if key in shapes:
            packed[key] = np.asarray(values, dtype=np.float32).reshape((-1, *shapes[key]))
        elif key == "split":
            packed[key] = np.asarray(values, dtype=np.uint8)
        else:
            packed[key] = np.asarray(values, dtype=str)
    target = output_prefix.with_suffix(".npz")
    temporary = target.with_suffix(".npz.tmp")
    with temporary.open("wb") as stream:
        np.savez_compressed(stream, **packed)
    temporary.replace(target)
    metadata_tmp.replace(metadata_path)
    return {"counts": dict(stats), "samples_by_split": dict(groups), "records_by_family": dict(families), "samples_by_tactic": dict(tactics), "raw_sha256": file_sha(raw_path), "npz_sha256": file_sha(target), "samples_sha256": file_sha(metadata_path)}


def collect_chunk(task):
    output_dir, shard_id, scenes, config = task
    global _ENV
    if _ENV is None:
        initialize_worker()
    prefix = Path(output_dir) / "shards" / ("%06d" % shard_id)
    raw_path = prefix.with_suffix(".raw.jsonl")
    temporary = raw_path.with_suffix(raw_path.suffix + ".tmp")
    started = time.perf_counter()
    with temporary.open("w", encoding="utf-8") as stream:
        for scene in scenes:
            candidates = shot_candidates(scene, config["shots_per_scene"], config["seed"], config["sampling"], config["grid"], config["v_min"], config["v_max"])
            # Same ice seed per scene/replicate across all candidates.
            seeds = [task_rng(config["seed"], "ice", scene["scene_key"], r).randrange(2**32) for r in range(config["physics_seeds"])]
            for shot_index, proposal in enumerate(candidates):
                for replicate, physics_seed in enumerate(seeds):
                    record_id = f"{scene.get('task_key', scene['scene_key'])}:{shot_index}:{replicate}"
                    record = simulate_record(_ENV, scene, proposal, physics_seed, record_id, config)
                    stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                    stream.flush()
    temporary.replace(raw_path)
    summary = encode_shard(raw_path, prefix, config["views_per_result"], config["split_seed"])
    summary.update(shard_id=shard_id, config_hash=config["config_hash"], seconds=time.perf_counter() - started)
    write_json(prefix.with_suffix(".done.json"), summary)
    return summary


def provenance():
    from local_simulator.runtime_loader import _resolve_bundled_extension
    paths = set((ROOT / "local_simulator").glob("*.py"))
    paths.add(ROOT / "local_simulator/examples/train_policy_tree_selfplay.py")
    paths.update((ROOT / "local_simulator/assets").glob("*.json"))
    paths.update((ROOT / "local_simulator/runtime").glob("*.dll"))
    paths.update((ROOT / "local_simulator/runtime").glob("*.json"))
    paths.update((ROOT / "local_simulator/runtime_support/tools/reverse").glob("*.py"))
    paths.update(Path(__file__).parent.glob("*.py"))
    paths.add(ROOT / "planning_proxy/competition_rules.py")
    paths.add(_resolve_bundled_extension())
    return {str(p.relative_to(ROOT)): file_sha(p) for p in sorted(paths)}


def array_contract():
    return {"schema": SCHEMA, "features": FEATURES, "goal_types": GOAL_TYPES, "tactics": TACTICS,
            "normalization": {"x_origin": 2.375, "y_origin": 4.88, "x_scale": X_SCALE, "y_scale": Y_SCALE, "radius_scale": X_SCALE, "action_scale": ACTION_SCALE.tolist()},
            "arrays": {"stones": "float32 [N,16,14]", "yaw": "float32 [N,16,3]: sin,cos,known", "tactic": f"float32 [N,{len(TACTICS)}] one-hot", "context": "float32 [N,2]: active_index/15, shooter_team", "actions": "float32 [N,3] normalized v,h,w", "shots": "float32 [N,3] physical v,h,w", "split": "uint8 [N]: 0 train,1 validation,2 test", "record_id": "unicode [N]", "sample_id": "unicode [N]", "group_id": "unicode [N]"}}


def parse_axis(value):
    try:
        result = [float(v) for v in value.split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("grid axis must be comma-separated numbers") from exc
    if not result or not np.isfinite(result).all():
        raise argparse.ArgumentTypeError("grid axis must contain finite numbers")
    return result


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    from .task_boards import TASK_FAMILIES
    plan = sub.add_parser("plan", help="expand hand-authored tactical layouts into varied task boards")
    plan.add_argument("--output", type=Path, required=True, help="new JSON scene catalog")
    plan.add_argument("--layouts-per-family", type=int, default=100)
    plan.add_argument("--variants-per-layout", type=int, default=2)
    plan.add_argument("--max-background", type=int, default=8)
    plan.add_argument("--families", default=",".join(TASK_FAMILIES))
    plan.add_argument("--seed", type=int, default=20261004)
    plan.add_argument("--split-seed", type=int, default=20261004)
    audit = sub.add_parser("audit", help="reconstruct every sample byte-for-byte and report actual coverage")
    audit.add_argument("--dataset-dir", type=Path, required=True)
    audit.add_argument("--output", type=Path, help="default: dataset-dir/coverage.json")
    collect = sub.add_parser("collect", help="accelerated exact simulation + raw records + encoded arrays")
    collect.add_argument("--output", type=Path, required=True)
    collect.add_argument("--scenes", type=int, default=1000, help="synthetic scene count; 0 imports only")
    collect.add_argument("--families", default=",".join(FAMILIES))
    collect.add_argument("--scene-json", action="append", default=[], help="JSON list of active_index/stones scenes")
    collect.add_argument("--scene-log", action="append", default=[], help="local SERVER_TELEMETRY log; initial positions only")
    collect.add_argument("--shots-per-scene", type=int, default=32)
    collect.add_argument("--sampling", choices=("mixed", "grid", "uniform"), default="mixed")
    collect.add_argument("--v-min", type=float, default=2.4, help="mixed sampling speed minimum; lower speeds can be much slower")
    collect.add_argument("--v-max", type=float, default=6.0)
    collect.add_argument("--v-grid", type=parse_axis, default=[2.7, 3.0, 3.4, 4.2, 6.0])
    collect.add_argument("--h-grid", type=parse_axis, default=[-1.5, -0.5, 0.0, 0.5, 1.5])
    collect.add_argument("--w-grid", type=parse_axis, default=[-10.0, 0.0, 10.0])
    collect.add_argument("--physics-seeds", type=int, default=2)
    collect.add_argument("--workers", type=int, default=1)
    collect.add_argument("--scenes-per-shard", type=int, default=8)
    collect.add_argument("--seed", type=int, default=20261004)
    collect.add_argument("--resume", action="store_true")
    encode = sub.add_parser("encode", help="re-encode existing raw shards without running physics")
    encode.add_argument("--raw-dir", type=Path, required=True)
    encode.add_argument("--output", type=Path, required=True)
    select = sub.add_parser("select", help="filter actual outcomes against manual goals; retain source raw data")
    select.add_argument("--raw-dir", type=Path, required=True)
    select.add_argument("--output", type=Path, required=True)
    select.add_argument("--goal-json", type=Path, help="override embedded per-board selection with this criterion")
    select.add_argument("--min-seeds", type=int, default=1, help="minimum distinct successful seeds per parameter set")
    select.add_argument("--min-success-rate", type=float, default=1.0)
    for command in (collect, encode, select):
        command.add_argument("--views-per-result", type=int, default=8)
        command.add_argument("--split-seed", type=int, default=20261004)
    select.set_defaults(views_per_result=1)
    collect.add_argument("--goal-radius", type=float, default=0.15)
    args = parser.parse_args(argv)
    if args.command in ("plan", "audit"):
        return args
    if args.views_per_result < 1:
        parser.error("views-per-result must be positive")
    if args.command == "select" and (args.min_seeds < 1 or not np.isfinite(args.min_success_rate) or not 0 < args.min_success_rate <= 1):
        parser.error("min-seeds must be positive; success rate must be in (0,1]")
    if args.command == "collect":
        if args.scenes < 0 or any(getattr(args, k) < 1 for k in ("shots_per_scene", "physics_seeds", "workers", "scenes_per_shard")):
            parser.error("counts must be positive; scenes may be zero")
        if not np.isfinite(args.goal_radius) or args.goal_radius <= 0:
            parser.error("goal-radius must be finite and positive")
        if not 0.0001 <= args.v_min <= args.v_max <= 6.0:
            parser.error("velocity bounds must satisfy 0.0001 <= v-min <= v-max <= 6")
        families = args.families.split(",")
        if not families or any(f not in FAMILIES for f in families):
            parser.error("unknown scene family")
        for values in __import__("itertools").product(args.v_grid, args.h_grid, args.w_grid):
            try:
                encode_action(values)
            except ValueError as exc:
                parser.error(str(exc))
    return args


def totals(shards):
    result = {}
    for key in ("counts", "samples_by_split", "records_by_family", "samples_by_tactic"):
        counter = Counter()
        for item in shards:
            counter.update(item[key])
        result[key] = dict(counter)
    return result


def collect(args):
    imported, rejected = load_scenes(args.scene_json, args.scene_log)
    scenes = imported + [synthetic_scene(i, args.seed, args.families.split(",")) for i in range(args.scenes)]
    scenes = deduplicate_scenes(scenes)
    if not scenes:
        raise ValueError("no valid scenes to simulate")
    hashes = provenance()
    config = {k: getattr(args, k) for k in ("seed", "shots_per_scene", "sampling", "v_min", "v_max", "physics_seeds", "views_per_result", "goal_radius", "split_seed", "scenes_per_shard")}
    config.update(grid=[args.v_grid, args.h_grid, args.w_grid], schema=SCHEMA, scene_keys=[s["scene_key"] for s in scenes], scene_groups=[s["group_id"] for s in scenes], scenes_sha256=digest(scenes), implementation_sha256=hashes,
                  physics_policy={"training_fast": True, "frame_elapsed": 0.33, "time_scale": 96.0, "per_request_reset": "reset_positions; native sleep boundary; all yaw inputs explicit", "sweeping": False})
    config["config_hash"] = digest(config)
    output = args.output.resolve()
    manifest_path = output / "manifest.json"
    if manifest_path.exists():
        if not args.resume:
            raise ValueError("output already exists; use --resume with identical configuration")
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        if previous["config"]["config_hash"] != config["config_hash"]:
            raise ValueError("resume configuration/code/runtime differs from existing dataset")
    elif output.exists() and any(output.iterdir()):
        raise ValueError("output directory must be empty for a new dataset")
    (output / "shards").mkdir(parents=True, exist_ok=True)
    write_json(output / "encoding.json", array_contract())
    write_json(output / "scenes.json", scenes)
    write_json(output / "rejected_scenes.json", rejected)
    candidates_per_scene = int(np.prod([len(axis) for axis in config["grid"]])) if args.sampling == "grid" else args.shots_per_scene
    manifest = {"schema": SCHEMA, "status": "running", "config": config, "python": sys.version, "platform": platform.platform(), "started_utc": datetime.now(timezone.utc).isoformat(), "unique_scenes": len(scenes), "planned_records": len(scenes) * candidates_per_scene * args.physics_seeds, "shards": []}
    worker_config = {k: config[k] for k in ("seed", "shots_per_scene", "sampling", "v_min", "v_max", "physics_seeds", "views_per_result", "goal_radius", "split_seed", "grid", "config_hash")}
    tasks, summaries = [], []
    for start in range(0, len(scenes), args.scenes_per_shard):
        shard_id = start // args.scenes_per_shard
        prefix = output / "shards" / ("%06d" % shard_id)
        done = prefix.with_suffix(".done.json")
        if done.exists():
            item = json.loads(done.read_text(encoding="utf-8"))
            if item["config_hash"] != config["config_hash"]:
                raise ValueError("shard configuration mismatch")
            for suffix, key in ((".raw.jsonl", "raw_sha256"), (".npz", "npz_sha256"), (".samples.jsonl", "samples_sha256")):
                if file_sha(prefix.with_suffix(suffix)) != item[key]:
                    raise ValueError("completed shard hash mismatch")
            summaries.append(item)
        else:
            tasks.append((str(output), shard_id, scenes[start:start+args.scenes_per_shard], worker_config))
    def checkpoint():
        manifest.update(shards=sorted(summaries, key=lambda s: s["shard_id"]), summary=totals(summaries))
        write_json(manifest_path, manifest)
    checkpoint()
    try:
        if args.workers == 1:
            initialize_worker()
            for task in tasks:
                summaries.append(collect_chunk(task))
                checkpoint()
                print(json.dumps({"completed_shards": len(summaries), **manifest["summary"]}, ensure_ascii=False), flush=True)
        elif tasks:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn"), initializer=initialize_worker) as pool:
                iterator = iter(tasks)
                pending = set()
                exhausted = False
                while pending or not exhausted:
                    while not exhausted and len(pending) < args.workers * 2:
                        try:
                            pending.add(pool.submit(collect_chunk, next(iterator)))
                        except StopIteration:
                            exhausted = True
                    if not pending:
                        break
                    finished, pending = wait(pending, timeout=10, return_when=FIRST_COMPLETED)
                    for future in finished:
                        summaries.append(future.result())
                        checkpoint()
                        print(json.dumps({"completed_shards": len(summaries), **manifest["summary"]}, ensure_ascii=False), flush=True)
        manifest.update(status="complete", finished_utc=datetime.now(timezone.utc).isoformat())
        checkpoint()
    except BaseException:
        manifest["status"] = "interrupted"
        checkpoint()
        raise
    print(json.dumps({"output": str(output), "status": manifest["status"], **manifest["summary"]}, ensure_ascii=False), flush=True)


def reencode(args):
    paths = sorted((args.raw_dir / "shards").glob("*.raw.jsonl"))
    if not paths:
        paths = sorted(args.raw_dir.glob("*.raw.jsonl"))
    if not paths:
        raise ValueError("no raw shards found")
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("encoding output must be a new/empty directory")
    (output / "shards").mkdir(parents=True, exist_ok=True)
    write_json(output / "encoding.json", array_contract())
    summaries = []
    for i, path in enumerate(paths):
        summary = encode_shard(path, output / "shards" / ("%06d" % i), args.views_per_result, args.split_seed)
        summary["source_raw"] = str(path.resolve())
        summaries.append(summary)
    report = {"schema": SCHEMA, "status": "complete", "mode": "encoding_only", "split_seed": args.split_seed, "views_per_result": args.views_per_result, "shards": summaries, "summary": totals(summaries)}
    write_json(output / "manifest.json", report)
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)


def select_results(args):
    from .selection import select_candidate
    paths = sorted((args.raw_dir / "shards").glob("*.raw.jsonl")) or sorted(args.raw_dir.glob("*.raw.jsonl"))
    if not paths:
        raise ValueError("no raw shards found")
    override = json.loads(args.goal_json.read_text(encoding="utf-8")) if args.goal_json else None
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("selection output must be a new/empty directory")
    (output / "shards").mkdir(parents=True, exist_ok=True)
    write_json(output / "encoding.json", array_contract())
    stats, failures, summaries, source_hashes, seen = Counter(), Counter(), [], {}, set()
    report = {"schema": SCHEMA, "status": "running", "mode": "selected_outcomes", "min_seeds": args.min_seeds,
              "min_success_rate": args.min_success_rate, "goal_override": override, "split_seed": args.split_seed,
              "views_per_result": args.views_per_result,
              "implementation_sha256": {p.name: file_sha(p) for p in sorted(Path(__file__).parent.glob("*.py"))}}
    write_json(output / "manifest.json", report)
    with (output / "selected_shots.jsonl").open("w", encoding="utf-8") as shot_output:
        for shard_id, path in enumerate(paths):
            source_hashes[str(path.resolve())] = file_sha(path)
            prefix = output / "shards" / ("%06d" % shard_id)
            raw_output = prefix.with_suffix(".raw.jsonl")
            with path.open(encoding="utf-8") as stream, raw_output.open("w", encoding="utf-8") as selected_output:
                # Collector keeps every seed replicate of one candidate together.
                for key, rows in groupby((json.loads(line) for line in stream), lambda r: r["record_id"].rsplit(":", 1)[0]):
                    if key in seen:
                        raise ValueError("candidate is duplicated or split across source shards")
                    seen.add(key)
                    records = list(rows)
                    selection = override or records[0].get("requested_scene", {}).get("selection")
                    stats["candidates"] += 1
                    stats["records"] += len(records)
                    if selection is None:
                        stats["candidates_without_goal"] += 1
                        continue
                    chosen, evidence = select_candidate(records, selection, args.min_seeds, args.min_success_rate)
                    stats["candidates_with_goal"] += 1
                    stats["accepted_candidates"] += bool(chosen)
                    stats["selected_records"] += len(chosen)
                    failures.update(evidence.pop("failures"))
                    for record in chosen:
                        selected_output.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
                    if chosen:
                        shot_output.write(json.dumps({"candidate_id": key, "scene_id": chosen[0]["scene_id"], "scene_key": chosen[0]["scene_key"],
                            "shot": chosen[0]["shot"], "selection": selection, "source_raw": str(path.resolve()),
                            "record_ids": [r["record_id"] for r in chosen], **evidence}, ensure_ascii=False, allow_nan=False) + "\n")
            summary = encode_shard(raw_output, prefix, args.views_per_result, args.split_seed)
            summary.update(shard_id=shard_id, source_raw=str(path.resolve()))
            summaries.append(summary)
    if not stats["candidates_with_goal"]:
        raise ValueError("no selection goals found; supply --goal-json or scene.selection")
    report.update(status="complete", selection_counts=dict(stats), failure_counts=dict(failures), source_raw_sha256=source_hashes,
                  selected_shots_sha256=file_sha(output / "selected_shots.jsonl"), shards=summaries, summary=totals(summaries))
    write_json(output / "manifest.json", report)
    print(json.dumps({"output": str(output), "selection_counts": dict(stats), "summary": report["summary"]}, ensure_ascii=False), flush=True)


def main(argv=None):
    args = parse_args(argv)
    if args.command == "plan":
        plan_boards(args)
    elif args.command == "audit":
        from .audit import audit_dataset
        report = audit_dataset(args.dataset_dir)
        write_json(args.output or args.dataset_dir / "coverage.json", report)
        print(json.dumps(report, ensure_ascii=False), flush=True)
    elif args.command == "collect":
        collect(args)
    elif args.command == "encode":
        reencode(args)
    else:
        select_results(args)


def plan_boards(args):
    from .task_boards import task_boards
    if args.output.exists():
        raise ValueError("scene catalog already exists; choose a new output")
    scenes = task_boards(args.layouts_per_family, args.variants_per_layout, args.seed, args.max_background, args.families.split(","))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {"schema": SCHEMA, "mode": "task_board_catalog", "seed": args.seed, "layouts_per_family": args.layouts_per_family,
              "variants_per_layout": args.variants_per_layout, "max_background": args.max_background,
              "scenes_sha256": digest(scenes), "families": dict(Counter(s["family"] for s in scenes)),
              "scene_splits": dict(Counter(str(split_for_group(s["group_id"], args.split_seed)) for s in scenes)),
              "split_seed": args.split_seed,
              "implementation_sha256": {p.name: file_sha(p) for p in sorted(Path(__file__).parent.glob("*.py"))}, "scenes": scenes}
    write_json(args.output, report)
    print(json.dumps({"output": str(args.output.resolve()), "scenes": len(scenes), "families": report["families"], "scene_splits": report["scene_splits"]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
