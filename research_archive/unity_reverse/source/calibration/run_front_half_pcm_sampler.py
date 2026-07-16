#!/usr/bin/env python3
"""Run the small controlled-shot plan for front-half PCM entrance tracing."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
import argparse
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLER = PROJECT_ROOT / "tools" / "calibration" / "controlled_scene_sampler.py"
DEFAULT_PLAN = PROJECT_ROOT / "config" / "front_half_pcm_probe_20260710.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "calibration"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="Skip completed plan rows and resume at this zero-based index.",
    )
    args, extra_args = parser.parse_known_args()
    if args.start_index < 0:
        parser.error("--start-index must be non-negative")
    show_output = "-h" not in extra_args and "--help" not in extra_args
    if show_output:
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = DEFAULT_OUTPUT_DIR / (
        "front_half_pcm_samples_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".jsonl"
    )
    plan_path = DEFAULT_PLAN
    if args.start_index:
        full_plan = json.loads(DEFAULT_PLAN.read_text(encoding="utf-8"))
        remaining_plan = full_plan[args.start_index:]
        if not remaining_plan:
            parser.error("--start-index skips every row in the plan")
        plan_path = output.with_suffix(".plan.json")
        plan_path.write_text(json.dumps(remaining_plan, indent=2, ensure_ascii=False), encoding="utf-8")
    cmd = [
        sys.executable,
        str(SAMPLER),
        "--plan-file",
        str(plan_path),
        "--output-file",
        str(output),
        "--use-reset",
        "--reset-settle-seconds",
        "0.25",
        "--force-final-timeout-seconds",
        "24",
        "--timeout-seconds",
        "180",
    ]
    cmd.extend(extra_args)
    if show_output:
        print("[front-half sampler] output=" + str(output), flush=True)
        print("[front-half sampler] plan=" + str(plan_path), flush=True)
    return subprocess.call(cmd, cwd=PROJECT_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
