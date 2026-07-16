#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate and summarize controlled Unity sampling outputs."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


EXPECTED_SWEEP_DISTANCES = [0.0, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: JSONL row must be an object")
            rows.append(row)
    return rows


def read_plan(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("plan file must contain a JSON list")
    return payload


def label_set(rows: list[dict[str, Any]]) -> set[str]:
    return {str(row.get("label", "")) for row in rows if row.get("label") not in (None, "")}


def category_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(Counter(str(row.get("category", "missing")) for row in rows))


def requested_sweep(row: dict[str, Any]) -> float | None:
    requested = row.get("requested")
    if isinstance(requested, dict) and "sweep" in requested:
        return float(requested["sweep"])
    if "sweep" in row:
        return float(row["sweep"])
    return None


def summarize_controlled(
    plan_rows: list[dict[str, Any]],
    sample_rows: list[dict[str, Any]],
    collision_tolerance: float,
) -> dict[str, Any]:
    plan_labels = label_set(plan_rows)
    sample_labels = label_set(sample_rows)
    duplicate_labels = [
        label
        for label, count in Counter(str(row.get("label", "")) for row in sample_rows).items()
        if label and count > 1
    ]
    no_collision_rows = [row for row in sample_rows if row.get("category") in {"repeat", "no_collision", "sweep_window", "boundary"}]
    collision_rows = [row for row in sample_rows if str(row.get("category", "")).startswith("collision")]
    collision_observed = [row for row in collision_rows if bool(row.get("collision_observed"))]
    no_collision_contaminated = [
        row
        for row in no_collision_rows
        if float(row.get("max_non_active_move", 0.0) or 0.0) > collision_tolerance
    ]
    sweep_rows = [row for row in sample_rows if row.get("category") == "sweep_window"]
    sweep_distances = sorted({requested_sweep(row) for row in sweep_rows if requested_sweep(row) is not None})
    motion_missing = [row for row in sample_rows if row.get("motioninfo") is None]
    by_category_missing_motion: dict[str, int] = defaultdict(int)
    for row in motion_missing:
        by_category_missing_motion[str(row.get("category", "missing"))] += 1

    return {
        "planned_count": len(plan_rows),
        "sample_count": len(sample_rows),
        "missing_labels": sorted(plan_labels - sample_labels),
        "extra_labels": sorted(sample_labels - plan_labels),
        "duplicate_labels": sorted(duplicate_labels),
        "plan_categories": category_counts(plan_rows),
        "sample_categories": category_counts(sample_rows),
        "sweep_distances": sweep_distances,
        "missing_sweep_distances": [value for value in EXPECTED_SWEEP_DISTANCES if value not in sweep_distances],
        "motioninfo_missing_count": len(motion_missing),
        "motioninfo_missing_by_category": dict(sorted(by_category_missing_motion.items())),
        "collision_rows": len(collision_rows),
        "collision_observed": len(collision_observed),
        "no_collision_contaminated": len(no_collision_contaminated),
        "no_collision_contaminated_labels": [str(row.get("label")) for row in no_collision_contaminated[:20]],
    }


def summarize_autodcp(rows: list[dict[str, Any]]) -> dict[str, Any]:
    seeded = [row for row in rows if row.get("randseed") is not None]
    trace_rows = [row for row in rows if int(row.get("trace_frames") or 0) > 0 or row.get("trace")]
    sweep_rows = [row for row in rows if row.get("sweep_distance") is not None]
    archive_paths = sorted({str(row.get("archive_path")) for row in rows if row.get("archive_path")})
    return {
        "record_count": len(rows),
        "seeded_count": len(seeded),
        "trace_count": len(trace_rows),
        "sweep_count": len(sweep_rows),
        "archive_file_count": len(archive_paths),
    }


def strict_failures(controlled: dict[str, Any], autodcp: dict[str, Any] | None) -> list[str]:
    failures: list[str] = []
    if controlled["sample_count"] < controlled["planned_count"]:
        failures.append("controlled samples are incomplete")
    if controlled["missing_labels"]:
        failures.append("controlled samples are missing planned labels")
    if controlled["duplicate_labels"]:
        failures.append("controlled samples contain duplicate labels")
    if controlled["missing_sweep_distances"]:
        failures.append("sweep-window grid is incomplete")
    if controlled["collision_rows"] > 0 and controlled["collision_observed"] == 0:
        failures.append("no collision rows observed target movement")
    if autodcp is None or autodcp["record_count"] == 0:
        failures.append("AutoDCP .save JSONL was not captured")
    elif autodcp["seeded_count"] == 0:
        failures.append("AutoDCP records contain no RANDSEED")
    return failures


def print_summary(controlled: dict[str, Any], autodcp: dict[str, Any] | None) -> None:
    print("controlled:")
    print(f"  planned/sample: {controlled['planned_count']}/{controlled['sample_count']}")
    print(f"  categories: {controlled['sample_categories']}")
    print(f"  missing labels: {len(controlled['missing_labels'])}")
    print(f"  duplicate labels: {len(controlled['duplicate_labels'])}")
    print(f"  sweep distances: {controlled['sweep_distances']}")
    print(f"  missing sweep distances: {controlled['missing_sweep_distances']}")
    print(
        "  collision observed: "
        f"{controlled['collision_observed']}/{controlled['collision_rows']}"
    )
    print(f"  no-collision contaminated: {controlled['no_collision_contaminated']}")
    print(f"  motioninfo missing: {controlled['motioninfo_missing_count']} {controlled['motioninfo_missing_by_category']}")

    if autodcp is None:
        print("autodcp: missing")
    else:
        print("autodcp:")
        print(f"  records: {autodcp['record_count']}")
        print(f"  seeded: {autodcp['seeded_count']}")
        print(f"  trace: {autodcp['trace_count']}")
        print(f"  sweep: {autodcp['sweep_count']}")
        print(f"  archive files: {autodcp['archive_file_count']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-file", type=Path, default=Path("config/unity_controlled_sampling_plan_20260707.json"))
    parser.add_argument(
        "--samples",
        type=Path,
        action="append",
        default=None,
        help="controlled JSONL file; can be repeated",
    )
    parser.add_argument("--autodcp-jsonl", type=Path, default=Path("data/calibration/autodcp_records_20260707.jsonl"))
    parser.add_argument("--collision-tolerance", type=float, default=0.02)
    parser.add_argument("--summary-json", type=Path, default=None)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_rows = read_plan(args.plan_file)
    sample_paths = args.samples or [Path("data/calibration/unity_controlled_samples_20260707.jsonl")]
    sample_rows: list[dict[str, Any]] = []
    for path in sample_paths:
        sample_rows.extend(read_jsonl(path))
    controlled = summarize_controlled(plan_rows, sample_rows, args.collision_tolerance)
    autodcp = summarize_autodcp(read_jsonl(args.autodcp_jsonl)) if args.autodcp_jsonl.exists() else None

    summary = {"controlled": controlled, "autodcp": autodcp}
    if args.summary_json:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        args.summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print_summary(controlled, autodcp)

    failures = strict_failures(controlled, autodcp) if args.strict else []
    if failures:
        print("strict failures:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
