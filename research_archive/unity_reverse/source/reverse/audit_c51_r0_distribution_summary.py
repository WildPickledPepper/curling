#!/usr/bin/env python3
"""Summarize R0 fixtures without conflating front-handoff and C04-tail error."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


DEFAULT_ROWS = [
    {
        "id": "c36_fixed_manifest",
        "front": "data/calibration/c42a_manifest_handoff_baseline_14000_20260713.json",
        "sample": "data/calibration/c36_manifest_replay_fixed_a_14000_20260713.jsonl",
        "tail": "data/calibration/c38_manifest_post_c04_settle_14000_20260713.json",
        "frontTailDraws": 0,
    },
    {
        "id": "c49_raw_rng_a",
        "front": "data/calibration/c49b_r0_front_half_waterfall_drop1_14000_20260713.json",
        "sample": "data/calibration/c49_r0_distribution_a_14000_20260713.jsonl",
        "tail": None,
        "frontTailDraws": 1,
    },
    {
        "id": "c50_raw_rng_b",
        "front": "data/calibration/c50b_r0_front_half_waterfall_14000_20260713.json",
        "sample": "data/calibration/c50_r0_distribution_b_14000_20260713.jsonl",
        "tail": "data/calibration/c50_c04_tail_settle_14000_20260713.json",
        "frontTailDraws": 0,
    },
    {
        "id": "c52_raw_rng_c",
        "front": "data/calibration/c52_r0_front_half_waterfall_14000_20260713.json",
        "sample": "data/calibration/c52_r0_distribution_c_14000_20260713.jsonl",
        "tail": "data/calibration/c52_c04_c05_tail_settle_14000_20260713.json",
        "frontTailDraws": 0,
    },
    {
        "id": "c54_raw_rng_d",
        "front": "data/calibration/c54_r0_front_half_waterfall_14000_20260713.json",
        "sample": "data/calibration/c54_r0_intercall_static_14000_20260713.jsonl",
        "tail": "data/calibration/c54_c04_tail_settle_14000_20260713.json",
        "frontTailDraws": 0,
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_sample(path: Path) -> dict[str, Any]:
    return json.loads(next(line for line in path.read_text(encoding="utf-8").splitlines() if line))


def distance_mm(local: list[float], unity: list[float]) -> float:
    return math.hypot(local[0] - unity[0], local[1] - unity[1]) * 1000.0


def tail_endpoint_mm(tail: dict[str, Any], sample: dict[str, Any]) -> dict[str, float]:
    endpoint = tail["comparison"]["endpointState"]
    return {
        "active": distance_mm(
            [endpoint["active"]["x"], endpoint["active"]["y"]],
            sample["final_xy"],
        ),
        "target": distance_mm(
            [endpoint["target"]["x"], endpoint["target"]["y"]],
            [sample["target_moves"][0]["after_x"], sample["target_moves"][0]["after_y"]],
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=Path, help="Optional JSON array overriding built-in fixture paths.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data/calibration/c51_r0_distribution_summary_20260713.json",
    )
    args = parser.parse_args()
    rows_spec = load_json(args.rows) if args.rows else DEFAULT_ROWS
    rows: list[dict[str, Any]] = []
    for spec in rows_spec:
        front = load_json(ROOT / spec["front"])
        baseline = next(row for row in front["rows"] if row["cumulativeTruthFill"] == "baseline_no_truth")
        c03_truth = next((row for row in front["rows"] if row["cumulativeTruthFill"] == "full_c03_pqvw"), None)
        sample = load_sample(ROOT / spec["sample"])
        entry = baseline["c03EntryErrorBeforeFill"]
        row: dict[str, Any] = {
            "id": spec["id"],
            "rngEvidenceLevel": "R0_replay_grade",
            "frontTailDrawsExcluded": int(spec.get("frontTailDraws", 0)),
            "c03EntryMaxAbs": {"active": entry[0], "target": entry[1]},
            "productionEndpointMm": {
                "active": baseline["activeEndpoint"]["distanceMm"],
                "target": baseline["targetEndpoint"]["distanceMm"],
            },
            "c03TruthEndpointMm": (
                None if c03_truth is None else {
                    "active": c03_truth["activeEndpoint"]["distanceMm"],
                    "target": c03_truth["targetEndpoint"]["distanceMm"],
                }
            ),
            "c04TruthTailEndpointMm": None,
        }
        if spec.get("tail"):
            tail = load_json(ROOT / spec["tail"])
            row["c04TruthTailEndpointMm"] = tail_endpoint_mm(tail, sample)
            c04 = tail["comparison"].get("c04Window") or []
            row["c04FrameMaxAbs"] = [
                {
                    "frame": int(frame["frameIndex"]),
                    "activeW": frame["active"]["w"]["maxAbs"],
                    "targetW": frame["target"]["w"]["maxAbs"],
                    "activeV": frame["active"]["v"]["maxAbs"],
                    "targetV": frame["target"]["v"]["maxAbs"],
                }
                for frame in c04
            ]
        rows.append(row)

    tail_rows = [row["c04TruthTailEndpointMm"] for row in rows if row["c04TruthTailEndpointMm"]]
    report = {
        "schema": "c51_r0_distribution_summary_v1",
        "scope": "R0 fixture summary. Production BESTSHOT-to-endpoint and C04-truth-to-endpoint are distinct metrics; an absent C04 trace is reported as missing, never imputed.",
        "rows": rows,
        "aggregate": {
            "fixtureCount": len(rows),
            "c04TailObservedCount": len(tail_rows),
            "productionEndpointMmMean": {
                stone: mean(row["productionEndpointMm"][stone] for row in rows)
                for stone in ("active", "target")
            },
            "c04TruthTailEndpointMmRange": {
                stone: (
                    [min(row[stone] for row in tail_rows), max(row[stone] for row in tail_rows)]
                    if tail_rows else None
                )
                for stone in ("active", "target")
            },
            "c03TruthObservedCount": sum(row["c03TruthEndpointMm"] is not None for row in rows),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        tail = row["c04TruthTailEndpointMm"]
        print(
            row["id"],
            f"production={row['productionEndpointMm']['active']:.3f}/{row['productionEndpointMm']['target']:.3f}mm",
            "c03truth=" + (
                f"{row['c03TruthEndpointMm']['active']:.3f}/{row['c03TruthEndpointMm']['target']:.3f}mm"
                if row["c03TruthEndpointMm"] else "missing"
            ),
            "c04tail=" + (f"{tail['active']:.3f}/{tail['target']:.3f}mm" if tail else "missing"),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
