#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derive intermediate reverse-engineering fields from controlled samples.

The socket protocol does not expose Unity's RANDSEED.  This helper therefore
does not pretend to recover the exact random sequence.  It records the
deterministic/mean-friction replay state at Midline, including the expected
number of Newfrictionstep calls before MOTIONINFO.  Once AutoDCP .save files
with RANDSEED are available, this field is the initial rng-skip hypothesis to
verify or adjust against seeded replay.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.replay_bestshot_seeded import Bestshot, asdict, replay_until_y  # noqa: E402


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def requested_shot(row: dict[str, Any]) -> Bestshot:
    requested = row.get("requested")
    if not isinstance(requested, dict):
        raise ValueError(f"row {row.get('label')} missing requested shot")
    return Bestshot(float(requested["v0"]), float(requested["h0"]), float(requested["w0"]))


def motion_error(row: dict[str, Any], mean_state: dict[str, float | int]) -> dict[str, float] | None:
    motion = row.get("motioninfo")
    if not motion:
        return None
    dx = float(mean_state["x"]) - float(motion[0])
    dy = float(mean_state["y"]) - float(motion[1])
    dvx = float(mean_state["vx"]) - float(motion[2])
    dvy = float(mean_state["vy"]) - float(motion[3])
    dw = float(mean_state["w"]) - float(motion[4])
    return {
        "dx": dx,
        "dy": dy,
        "dvx": dvx,
        "dvy": dvy,
        "dw": dw,
        "position_error": math.hypot(dx, dy),
        "velocity_error": math.hypot(dvx, dvy),
    }


def derive_row(row: dict[str, Any]) -> dict[str, Any]:
    shot = requested_shot(row)
    mean_state = asdict(replay_until_y(shot))
    return {
        "sample_id": row.get("sample_id"),
        "label": row.get("label"),
        "category": row.get("category"),
        "requested": row.get("requested"),
        "motioninfo": row.get("motioninfo"),
        "sent_sweep": row.get("sent_sweep"),
        "final_xy": row.get("final_xy"),
        "collision_observed": row.get("collision_observed"),
        "has_randseed": row.get("randseed") is not None,
        "randseed": row.get("randseed"),
        "estimated_pre_midline_rng_draws_mean": mean_state["steps"],
        "estimated_midline_state_mean": mean_state,
        "mean_replay_vs_motioninfo": motion_error(row, mean_state),
        "exact_pre_midline_rng_draws_status": (
            "missing_randseed_save; verify with AutoDCP RANDSEED + seeded replay"
            if row.get("randseed") is None
            else "seeded_verification_not_run"
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/calibration/unity_controlled_intermediates_20260707.jsonl"))
    parser.add_argument("--summary-json", type=Path, default=Path("data/calibration/unity_controlled_intermediates_20260707.summary.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows: list[dict[str, Any]] = []
    for path in args.samples:
        rows.extend(read_jsonl(path))
    derived = [derive_row(row) for row in rows]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in derived:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    step_values = [int(row["estimated_pre_midline_rng_draws_mean"]) for row in derived]
    summary = {
        "rows": len(derived),
        "has_randseed_rows": sum(1 for row in derived if row["has_randseed"]),
        "exact_rng_draws_available": False,
        "estimated_pre_midline_rng_draws_min": min(step_values) if step_values else None,
        "estimated_pre_midline_rng_draws_max": max(step_values) if step_values else None,
        "estimated_pre_midline_rng_draws_unique": sorted(set(step_values)),
        "output": str(args.output),
    }
    args.summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
