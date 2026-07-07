# -*- coding: utf-8 -*-
"""Keep two Unity physics samplers alive until enough samples are collected."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def total_samples(output_pattern: str) -> int:
    path = PROJECT_ROOT / output_pattern
    parent = path.parent
    pattern = path.name.replace("{player}", "*")
    return sum(count_lines(item) for item in parent.glob(pattern))


def sampler_command(args: argparse.Namespace, slot: int) -> list[str]:
    command = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "calibration" / "official_physics_sampler.py"),
        "--key",
        args.key,
        "-H",
        args.host,
        "-p",
        str(args.port),
        "--name",
        f"{args.name}P{slot}",
        "--output",
        args.output,
        "--max-samples",
        str(args.max_samples_per_client),
        "--collision-tolerance",
        str(args.collision_tolerance),
    ]
    if args.plan_file:
        command.extend(["--plan-file", str(args.plan_file)])
    command.extend(["--plan-offset", str(slot - 1), "--plan-stride", "2"])
    if args.show_msg:
        command.append("--show-msg")
    return command


def start_sampler(args: argparse.Namespace, slot: int, log_dir: Path) -> subprocess.Popen:
    stdout = (log_dir / f"sampler{slot}.out.log").open("a", encoding="utf-8")
    stderr = (log_dir / f"sampler{slot}.err.log").open("a", encoding="utf-8")
    command = sampler_command(args, slot)
    print(f"[supervisor] start sampler{slot}: {' '.join(command)}", flush=True)
    return subprocess.Popen(
        command,
        cwd=PROJECT_ROOT,
        stdout=stdout,
        stderr=stderr,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", default="localtest")
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("--name", default="UnitySampler")
    parser.add_argument("--output", default="data/calibration/unity_samples_{player}.jsonl")
    parser.add_argument("--plan-file", type=Path, default=PROJECT_ROOT / "config" / "unity_sampling_plan.json")
    parser.add_argument("--max-samples-per-client", type=int, default=600)
    parser.add_argument("--target-total-samples", type=int, default=1200)
    parser.add_argument("--collision-tolerance", type=float, default=0.02)
    parser.add_argument("--retry-seconds", type=float, default=5.0)
    parser.add_argument("--log-dir", type=Path, default=PROJECT_ROOT / "log" / "unity_sampling")
    parser.add_argument("--show-msg", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.log_dir.mkdir(parents=True, exist_ok=True)
    processes: dict[int, subprocess.Popen] = {}
    while total_samples(args.output) < args.target_total_samples:
        for slot in (1, 2):
            proc = processes.get(slot)
            if proc is None or proc.poll() is not None:
                if proc is not None:
                    print(f"[supervisor] sampler{slot} exited code={proc.returncode}; retrying", flush=True)
                processes[slot] = start_sampler(args, slot, args.log_dir)
        print(
            f"[supervisor] collected={total_samples(args.output)}/{args.target_total_samples}",
            flush=True,
        )
        time.sleep(args.retry_seconds)

    print("[supervisor] target reached; stopping samplers", flush=True)
    for proc in processes.values():
        if proc.poll() is None:
            proc.terminate()
    for proc in processes.values():
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
