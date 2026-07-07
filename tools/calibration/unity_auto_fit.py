# -*- coding: utf-8 -*-
"""Periodically fit Unity calibration when enough samples are available."""

from __future__ import annotations

import argparse
import json
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


def inputs_for(pattern: str) -> list[Path]:
    path = PROJECT_ROOT / pattern
    return sorted(path.parent.glob(path.name))


def total_lines(paths: list[Path]) -> int:
    return sum(count_lines(path) for path in paths)


def fit_once(args: argparse.Namespace, inputs: list[Path]) -> dict:
    command = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "calibration" / "fit_unity_samples.py"),
        *[str(path) for path in inputs],
        "--output",
        str(PROJECT_ROOT / "config" / "unity_physics_calibration.json"),
        "--eval-output",
        str(PROJECT_ROOT / "config" / "unity_physics_evaluation.json"),
        "--min-fit-samples",
        str(args.min_fit_samples),
    ]
    print("[auto_fit] " + " ".join(command), flush=True)
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)
    report_path = PROJECT_ROOT / "config" / "unity_physics_evaluation.json"
    return json.loads(report_path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-pattern", default="data/calibration/unity_v2_samples_*.jsonl")
    parser.add_argument("--min-total-lines", type=int, default=200)
    parser.add_argument("--min-fit-samples", type=int, default=80)
    parser.add_argument("--target-rmse", type=float, default=0.05)
    parser.add_argument("--interval", type=float, default=60.0)
    parser.add_argument("--once", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    while True:
        inputs = inputs_for(args.input_pattern)
        lines = total_lines(inputs)
        print(f"[auto_fit] lines={lines} threshold={args.min_total_lines}", flush=True)
        if lines >= args.min_total_lines and inputs:
            try:
                report = fit_once(args, inputs)
                val = report.get("metrics", {}).get("val", {})
                rmse = float(val.get("rmse_total", 999.0))
                print(f"[auto_fit] val_rmse={rmse:.5f} target={args.target_rmse:.5f}", flush=True)
                if rmse <= args.target_rmse:
                    print("[auto_fit] calibration is inside target", flush=True)
            except Exception as exc:
                print(f"[auto_fit] fit failed: {type(exc).__name__}: {exc}", flush=True)
        if args.once:
            return
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
