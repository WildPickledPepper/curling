#!/usr/bin/env python3
"""Run independent local simulator samples concurrently without changing physics.

Each worker is a separate Python/PhysX process and invokes the existing
``sample_local_collision_distribution.py`` runner on a disjoint, contiguous
plan-index range.  Fresh-state episodes can therefore run concurrently without
changing their seed, fixed timestep or output schema.  The parent concatenates
successful worker shards in plan order.

The real Unity protocol preserves a stone quaternion across RESETPOSITION.
That makes one long session stateful across plan rows, so it is deliberately
kept sequential here.  Pass ``--reset-all-stone-rotations`` for independent
fresh-state training episodes, which is the parallel-safe training contract.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Iterable, List, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools" / "reverse" / "sample_local_collision_distribution.py"


def partition(start: int, end: int, workers: int) -> List[Tuple[int, int]]:
    """Return contiguous non-empty ranges, preserving global plan order."""

    if end < start:
        raise ValueError("end must be >= start")
    total = end - start
    if total == 0:
        return []
    count = max(1, min(int(workers), total))
    base, extra = divmod(total, count)
    result: List[Tuple[int, int]] = []
    cursor = start
    for index in range(count):
        size = base + (1 if index < extra else 0)
        result.append((cursor, cursor + size))
        cursor += size
    return result


def _run_shard(command: Sequence[str], cwd: str) -> dict[str, Any]:
    started = time.monotonic()
    completed = subprocess.run(list(command), cwd=cwd, capture_output=True, text=True)
    return {
        "returncode": int(completed.returncode),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "seconds": time.monotonic() - started,
        "command": list(command),
    }


def _line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def _append_option(command: List[str], name: str, value: Any) -> None:
    if value is None:
        return
    command.extend([name, str(value)])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-file", type=Path, required=True)
    parser.add_argument("--output-file", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--end-index", type=int)
    parser.add_argument("--labels", help="same logical/base-label filter accepted by the sequential runner")
    parser.add_argument("--seed-base", type=int, default=20260714)
    parser.add_argument("--max-friction-steps", type=int, default=2500)
    parser.add_argument("--max-settle-steps", type=int, default=6000)
    parser.add_argument("--sweep-start-delay-m", type=float, default=0.0)
    parser.add_argument(
        "--sweep-effect-manifest", type=Path,
        help="optional Unity-observed sweep dispatch manifest forwarded unchanged to every worker",
    )
    parser.add_argument(
        "--sweep-request-policy",
        choices=("protocol-late", "assume-effective"),
        default="protocol-late",
        help="default semantics for sweep requests not listed in the manifest",
    )
    parser.add_argument("--contact-tail-capture-steps", type=int, default=0)
    parser.add_argument(
        "--compact-training-output",
        action="store_true",
        help="omit pointer-bearing contact snapshots so parallel training shards are byte-stable",
    )
    parser.add_argument("--wake-target-at-current-pcm-shell", action="store_true")
    parser.add_argument("--emulate-unity-setactive-no-sim", action="store_true")
    parser.add_argument(
        "--reset-all-stone-rotations",
        action="store_true",
        help="run independent fresh-state episodes; required for workers > 1 because Unity-protocol rotation history is cross-row state",
    )
    parser.add_argument("--keep-shards", action="store_true")
    parser.add_argument("--python", type=Path, default=Path(sys.executable), help="interpreter that owns pyphysx")
    args = parser.parse_args()

    plan = json.loads(args.plan_file.read_text(encoding="utf-8"))
    if not isinstance(plan, list):
        raise ValueError("plan file must contain a JSON list")
    start = max(0, int(args.start_index))
    end = len(plan) if args.end_index is None else min(len(plan), int(args.end_index))
    ranges = partition(start, end, int(args.workers))
    if len(ranges) > 1 and not args.reset_all_stone_rotations:
        raise ValueError(
            "parallel shards would discard Unity-protocol persistent orientation history; "
            "use --workers 1 for a continuous session or --reset-all-stone-rotations for independent training episodes"
        )
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    shard_dir = args.output_file.with_name(args.output_file.name + ".shards")
    shard_dir.mkdir(parents=True, exist_ok=True)

    commands: List[Tuple[Tuple[int, int], Path, List[str]]] = []
    for ordinal, (shard_start, shard_end) in enumerate(ranges):
        shard = shard_dir / ("shard_%03d_%06d_%06d.jsonl" % (ordinal, shard_start, shard_end))
        if shard.exists():
            shard.unlink()
        command = [str(args.python), str(RUNNER), "--plan-file", str(args.plan_file), "--output-file", str(shard)]
        _append_option(command, "--start-index", shard_start)
        _append_option(command, "--end-index", shard_end)
        _append_option(command, "--labels", args.labels)
        _append_option(command, "--seed-base", args.seed_base)
        _append_option(command, "--max-friction-steps", args.max_friction_steps)
        _append_option(command, "--max-settle-steps", args.max_settle_steps)
        _append_option(command, "--sweep-start-delay-m", args.sweep_start_delay_m)
        _append_option(command, "--sweep-effect-manifest", args.sweep_effect_manifest)
        _append_option(command, "--sweep-request-policy", args.sweep_request_policy)
        _append_option(command, "--contact-tail-capture-steps", args.contact_tail_capture_steps)
        if args.compact_training_output:
            command.append("--compact-training-output")
        if args.wake_target_at_current_pcm_shell:
            command.append("--wake-target-at-current-pcm-shell")
        if args.emulate_unity_setactive_no_sim:
            command.append("--emulate-unity-setactive-no-sim")
        if args.reset_all_stone_rotations:
            command.append("--reset-all-stone-rotations")
        commands.append(((shard_start, shard_end), shard, command))

    started = time.monotonic()
    reports: List[Tuple[Tuple[int, int], Path, dict[str, Any]]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(commands) or 1) as pool:
        pending = {
            pool.submit(_run_shard, command, str(ROOT)): (bounds, shard)
            for bounds, shard, command in commands
        }
        for future in concurrent.futures.as_completed(pending):
            bounds, shard = pending[future]
            reports.append((bounds, shard, future.result()))
    reports.sort(key=lambda item: item[0])
    failed = [item for item in reports if item[2]["returncode"] != 0 or not item[1].is_file()]
    if failed:
        detail = [
            {"range": bounds, "returncode": report["returncode"], "stderr": report["stderr"][-2000:]}
            for bounds, _shard, report in failed
        ]
        raise RuntimeError("one or more local simulation workers failed: " + json.dumps(detail, ensure_ascii=False))

    temporary = args.output_file.with_name(args.output_file.name + ".tmp")
    rows = 0
    with temporary.open("w", encoding="utf-8") as target:
        for _bounds, shard, _report in reports:
            with shard.open("r", encoding="utf-8") as source:
                for line in source:
                    if line.strip():
                        target.write(line if line.endswith("\n") else line + "\n")
                        rows += 1
    temporary.replace(args.output_file)
    worker_rows = [(bounds, _line_count(shard)) for bounds, shard, _report in reports]
    if not args.keep_shards:
        for _bounds, shard, _report in reports:
            shard.unlink(missing_ok=True)
        try:
            shard_dir.rmdir()
        except OSError:
            pass
    summary = {
        "output": str(args.output_file),
        "rows": rows,
        "planIndexRange": [start, end],
        "workers": len(commands),
        "resetAllStoneRotations": bool(args.reset_all_stone_rotations),
        "sweepEffectManifest": None if args.sweep_effect_manifest is None else str(args.sweep_effect_manifest),
        "sweepRequestPolicy": args.sweep_request_policy,
        "compactTrainingOutput": bool(args.compact_training_output),
        "seconds": time.monotonic() - started,
        "workerSeconds": [
            {"range": list(bounds), "seconds": report["seconds"], "rows": shard_rows}
            for (bounds, _shard, report), (_same_bounds, shard_rows) in zip(reports, worker_rows)
        ],
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
