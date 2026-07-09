#!/usr/bin/env python3
"""Infer residual sources from Unity socket sampling JSONL files.

This tool is intentionally diagnostic.  It does not treat endpoint fitting as
the physics model.  Instead it separates the sampled evidence into:

* BESTSHOT -> MOTIONINFO release/midline residuals;
* MOTIONINFO -> endpoint tail residuals;
* repeated-shot natural dispersion;
* collision sample sanity statistics.

It supports both the early flat calibration schema and the later controlled
sampling schema.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.probe_tail_residual_sources import (  # noqa: E402
    fit_constant_friction,
    simulate as simulate_tail,
)
from tools.reverse.recovered_curling_motion import BASE_FRICTION  # noqa: E402
from tools.reverse.replay_bestshot_seeded import Bestshot, replay_until_y  # noqa: E402


@dataclass(frozen=True)
class Sample:
    source: str
    sample_id: Any
    label: str
    category: str
    v0: float
    h0: float
    w0: float
    stones_key: str
    sweep_distance: float | None
    sent_sweep: bool
    motion_x: float
    motion_y: float
    motion_vx: float
    motion_vy: float
    motion_w: float
    final_x: float
    final_y: float
    collision_observed: bool
    max_target_move: float | None
    max_non_active_move: float | None


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


def _float_or_none(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def normalize_row(row: dict[str, Any], source: Path) -> Sample | None:
    requested = row.get("requested")
    if isinstance(requested, dict):
        motion = row.get("motioninfo")
        final = row.get("final_xy")
        if not motion or not final:
            return None
        sweep_distance = _float_or_none(requested.get("sweep"))
        return Sample(
            source=str(source),
            sample_id=row.get("sample_id"),
            label=str(row.get("label", row.get("sample_id", ""))),
            category=str(row.get("category", "controlled")),
            v0=float(requested["v0"]),
            h0=float(requested["h0"]),
            w0=float(requested["w0"]),
            stones_key=json.dumps(requested.get("stones", []), sort_keys=True),
            sweep_distance=sweep_distance,
            sent_sweep=bool(row.get("sent_sweep", False)),
            motion_x=float(motion[0]),
            motion_y=float(motion[1]),
            motion_vx=float(motion[2]),
            motion_vy=float(motion[3]),
            motion_w=float(motion[4]),
            final_x=float(final[0]),
            final_y=float(final[1]),
            collision_observed=bool(row.get("collision_observed", False)),
            max_target_move=_float_or_none(row.get("max_target_move")),
            max_non_active_move=_float_or_none(row.get("max_non_active_move")),
        )

    required = (
        "requested_v0",
        "requested_h0",
        "requested_w0",
        "motion_x",
        "motion_y",
        "motion_vx",
        "motion_vy",
        "motion_w",
        "final_x",
        "final_y",
    )
    if not all(row.get(field) is not None for field in required):
        return None
    if row.get("in_play") is False:
        return None
    return Sample(
        source=str(source),
        sample_id=row.get("sample_id"),
        label=str(row.get("label", row.get("sample_id", ""))),
        category=str(row.get("category", "legacy")),
        v0=float(row["requested_v0"]),
        h0=float(row["requested_h0"]),
        w0=float(row["requested_w0"]),
        stones_key=json.dumps(row.get("stones", []), sort_keys=True),
        sweep_distance=_float_or_none(row.get("requested_sweep_distance")),
        sent_sweep=bool(row.get("sent_sweep", False)),
        motion_x=float(row["motion_x"]),
        motion_y=float(row["motion_y"]),
        motion_vx=float(row["motion_vx"]),
        motion_vy=float(row["motion_vy"]),
        motion_w=float(row["motion_w"]),
        final_x=float(row["final_x"]),
        final_y=float(row["final_y"]),
        collision_observed=bool(row.get("collision_observed", False)),
        max_target_move=_float_or_none(row.get("max_target_move")),
        max_non_active_move=_float_or_none(row.get("max_non_active_move")),
    )


def load_samples(paths: list[Path]) -> list[Sample]:
    samples: list[Sample] = []
    for path in paths:
        for row in read_jsonl(path):
            sample = normalize_row(row, path)
            if sample is not None:
                samples.append(sample)
    return samples


def rms(values: list[float]) -> float | None:
    if not values:
        return None
    return math.sqrt(sum(value * value for value in values) / len(values))


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def summarize_errors(errors: list[float]) -> dict[str, float | int | None]:
    return {
        "n": len(errors),
        "rmse": rms(errors),
        "mae": (sum(errors) / len(errors)) if errors else None,
        "p50": percentile(errors, 0.50),
        "p90": percentile(errors, 0.90),
        "max": max(errors) if errors else None,
    }


def sample_as_tail_row(sample: Sample) -> dict[str, Any]:
    return {
        "sample_id": sample.sample_id,
        "motion_x": sample.motion_x,
        "motion_y": sample.motion_y,
        "motion_vx": sample.motion_vx,
        "motion_vy": sample.motion_vy,
        "motion_w": sample.motion_w,
        "final_x": sample.final_x,
        "final_y": sample.final_y,
        "sent_sweep": sample.sent_sweep,
    }


def has_active_endpoint(sample: Sample) -> bool:
    # In the Unity protocol/state array, (0, 0) is also the cleared inactive
    # stone position.  Controlled samples with final_xy == [0, 0] reached
    # Midline but were later removed/out-of-play, so they are not usable as a
    # stop-position tail target.
    return not (abs(sample.final_x) < 1e-9 and abs(sample.final_y) < 1e-9)


def release_error(sample: Sample) -> dict[str, Any]:
    state = replay_until_y(Bestshot(sample.v0, sample.h0, sample.w0))
    dx = state.x - sample.motion_x
    dy = state.y - sample.motion_y
    dvx = state.vx - sample.motion_vx
    dvy = state.vy - sample.motion_vy
    dw = state.w - sample.motion_w
    return {
        "sample_id": sample.sample_id,
        "label": sample.label,
        "category": sample.category,
        "position_error": math.hypot(dx, dy),
        "velocity_error": math.sqrt(dvx * dvx + dvy * dvy + dw * dw),
        "dx": dx,
        "dy": dy,
        "dvx": dvx,
        "dvy": dvy,
        "dw": dw,
        "steps": state.steps,
    }


def tail_error(sample: Sample, *, max_steps: int) -> dict[str, Any]:
    row = sample_as_tail_row(sample)
    sweep_distance = sample.sweep_distance if sample.sent_sweep else None
    x, y, steps, error = simulate_tail(
        row,
        BASE_FRICTION,
        dt_pos=0.010,
        max_steps=max_steps,
        sweep_distance=sweep_distance,
    )
    return {
        "sample_id": sample.sample_id,
        "label": sample.label,
        "category": sample.category,
        "sweep_distance": sweep_distance,
        "error": error,
        "dx": x - sample.final_x,
        "dy": y - sample.final_y,
        "steps": steps,
    }


def fit_tail(sample: Sample, *, max_steps: int, iterations: int) -> dict[str, Any]:
    row = sample_as_tail_row(sample)
    sweep_distance = sample.sweep_distance if sample.sent_sweep else None
    friction, fitted = fit_constant_friction(
        row,
        dt_pos=0.010,
        max_steps=max_steps,
        lo=0.0008,
        hi=0.0012,
        iterations=iterations,
        sweep_distance=sweep_distance,
    )
    return {
        "sample_id": sample.sample_id,
        "label": sample.label,
        "category": sample.category,
        "sweep_distance": sweep_distance,
        "fitted_friction": friction,
        "fitted_error": fitted[3],
        "fitted_steps": fitted[2],
    }


def key_for_repeat(sample: Sample) -> str:
    return json.dumps(
        {
            "category": sample.category,
            "v0": round(sample.v0, 6),
            "h0": round(sample.h0, 6),
            "w0": round(sample.w0, 6),
            "stones": sample.stones_key,
            "sweep": None if sample.sweep_distance is None else round(sample.sweep_distance, 6),
            "sent_sweep": sample.sent_sweep,
            "collision": sample.collision_observed,
        },
        sort_keys=True,
    )


def repeat_groups(samples: list[Sample]) -> list[dict[str, Any]]:
    buckets: dict[str, list[Sample]] = defaultdict(list)
    for sample in samples:
        buckets[key_for_repeat(sample)].append(sample)
    groups = []
    for key, rows in buckets.items():
        if len(rows) < 2:
            continue
        mean_x = statistics.fmean(row.final_x for row in rows)
        mean_y = statistics.fmean(row.final_y for row in rows)
        radii = [math.hypot(row.final_x - mean_x, row.final_y - mean_y) for row in rows]
        groups.append(
            {
                "key": json.loads(key),
                "n": len(rows),
                "labels": [row.label for row in rows],
                "mean_final": [mean_x, mean_y],
                "dispersion_rmse": rms(radii),
                "dispersion_p90": percentile(radii, 0.90),
                "dispersion_max": max(radii),
            }
        )
    return sorted(groups, key=lambda item: item["dispersion_max"], reverse=True)


def by_category(samples: list[Sample]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for sample in samples:
        counts[sample.category] += 1
    return dict(sorted(counts.items()))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-steps", type=int, default=5000)
    parser.add_argument("--fit-limit", type=int, default=20)
    parser.add_argument("--fit-iterations", type=int, default=8)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    samples = load_samples(args.inputs)
    if not samples:
        raise SystemExit("no usable samples")

    non_collision = [sample for sample in samples if not sample.collision_observed]
    no_sweep = [sample for sample in non_collision if not sample.sent_sweep]
    sweep = [sample for sample in non_collision if sample.sent_sweep]
    collision = [sample for sample in samples if sample.collision_observed]
    tail_samples = [sample for sample in non_collision if has_active_endpoint(sample)]
    no_sweep_tail = [sample for sample in tail_samples if not sample.sent_sweep]
    sweep_tail = [sample for sample in tail_samples if sample.sent_sweep]
    out_of_play = [sample for sample in non_collision if not has_active_endpoint(sample)]

    release_rows = [release_error(sample) for sample in non_collision]
    release_by_kind = {
        "no_sweep": [release_error(sample) for sample in no_sweep],
        "sweep": [release_error(sample) for sample in sweep],
    }
    tail_rows = [tail_error(sample, max_steps=args.max_steps) for sample in tail_samples]
    tail_by_kind = {
        "no_sweep": [tail_error(sample, max_steps=args.max_steps) for sample in no_sweep_tail],
        "sweep": [tail_error(sample, max_steps=args.max_steps) for sample in sweep_tail],
    }
    fit_candidates = no_sweep_tail[: args.fit_limit]
    fit_rows = [
        fit_tail(sample, max_steps=args.max_steps, iterations=args.fit_iterations)
        for sample in fit_candidates
    ]

    summary = {
        "inputs": [str(path) for path in args.inputs],
        "total_samples": len(samples),
        "category_counts": by_category(samples),
        "non_collision_count": len(non_collision),
        "no_sweep_count": len(no_sweep),
        "sweep_count": len(sweep),
        "collision_count": len(collision),
        "out_of_play_non_collision_count": len(out_of_play),
        "release_to_midline": {
            "all_non_collision_position": summarize_errors([row["position_error"] for row in release_rows]),
            "all_non_collision_velocity": summarize_errors([row["velocity_error"] for row in release_rows]),
            "no_sweep_position": summarize_errors(
                [row["position_error"] for row in release_by_kind["no_sweep"]]
            ),
            "sweep_position": summarize_errors(
                [row["position_error"] for row in release_by_kind["sweep"]]
            ),
        },
        "motioninfo_to_endpoint": {
            "all_non_collision": summarize_errors([row["error"] for row in tail_rows]),
            "no_sweep": summarize_errors(
                [row["error"] for row in tail_by_kind["no_sweep"]]
            ),
            "sweep": summarize_errors(
                [row["error"] for row in tail_by_kind["sweep"]]
            ),
        },
        "constant_friction_fit_no_sweep": {
            "fit_limit": args.fit_limit,
            "errors": summarize_errors([row["fitted_error"] for row in fit_rows]),
            "fitted_friction": summarize_errors([row["fitted_friction"] for row in fit_rows]),
            "rows": fit_rows,
        },
        "out_of_play_non_collision_labels": [sample.label for sample in out_of_play],
        "repeat_groups": repeat_groups(samples),
        "collision": {
            "observed": len(collision),
            "max_target_move": summarize_errors(
                [sample.max_target_move for sample in collision if sample.max_target_move is not None]
            ),
            "max_non_active_move": summarize_errors(
                [sample.max_non_active_move for sample in collision if sample.max_non_active_move is not None]
            ),
        },
        "worst_release_position": sorted(release_rows, key=lambda row: row["position_error"], reverse=True)[:10],
        "worst_tail": sorted(tail_rows, key=lambda row: row["error"], reverse=True)[:10],
    }

    text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
