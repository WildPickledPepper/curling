#!/usr/bin/env python3
"""Build an interleaved endpoint-distribution plan for the 20 collision cases.

Every round contains each configuration once.  The start point rotates by one
case per round so a configuration alternates between the two legal active-stone
parities instead of always reusing the same physical stone object.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.calibration.build_controlled_sampling_plan import build_plan


CATEGORIES = {
    "collision_headon",
    "collision_glancing",
    "collision_double",
    "collision_with_sweep",
}


def build_distribution_plan(repeats_per_case: int) -> list[dict]:
    if repeats_per_case < 1:
        raise ValueError("repeats_per_case must be positive")
    cases = [row for row in build_plan() if row.get("category") in CATEGORIES]
    if len(cases) != 20:
        raise ValueError(f"expected 20 collision cases, got {len(cases)}")

    rows: list[dict] = []
    for repeat_index in range(repeats_per_case):
        for ordinal in range(len(cases)):
            case_index = (repeat_index + ordinal) % len(cases)
            source = cases[case_index]
            row = dict(source)
            row["sample_id"] = len(rows) + 1
            row["source_sample_id"] = source["sample_id"]
            row["config_index"] = case_index
            row["repeat_index"] = repeat_index
            row["label"] = f"{source['label']}_dist_r{repeat_index:03d}"
            row["notes"] = (
                "endpoint-distribution sample; complete position/velocity/rotation reset before this shot; "
                f"source_sample_id={source['sample_id']}; repeat_index={repeat_index}"
            )
            rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats-per-case", type=int, default=100)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("config/unity_collision_distribution_20x100_20260714.json"),
    )
    args = parser.parse_args()
    rows = build_distribution_plan(args.repeats_per_case)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} shots ({args.repeats_per_case} per each of 20 cases) -> {args.output}")


if __name__ == "__main__":
    main()
