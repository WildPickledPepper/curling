#!/usr/bin/env python3
"""Compare standalone-local and Unity endpoint distributions by configuration.

The two inputs are deliberately unpaired samples.  It compares empirical
centres and spread only; it never treats a local seed as the Unity run's RNG
state or injects Unity per-shot data into the local simulator.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
from pathlib import Path
from typing import Any, Iterable


def load_jsonl(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    return rows


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(float(value) for value in values)
    return ordered[round((len(ordered) - 1) * q)]


def is_cleared(point: list[float]) -> bool:
    return abs(point[0]) < 1e-12 and abs(point[1]) < 1e-12


def stats(points: list[list[float]]) -> dict[str, float | int | None]:
    total = len(points)
    cleared = sum(1 for point in points if is_cleared(point))
    points = [point for point in points if not is_cleared(point)]
    if not points:
        return {
            "nTotal": total, "n": 0, "clearedCount": cleared, "clearedRate": (cleared / total if total else None),
            "meanX": None, "meanY": None, "sigmaX": None, "sigmaY": None, "p90Radius": None,
        }
    n = len(points)
    mean_x = sum(point[0] for point in points) / n
    mean_y = sum(point[1] for point in points) / n
    sigma_x = math.sqrt(sum((point[0] - mean_x) ** 2 for point in points) / n)
    sigma_y = math.sqrt(sum((point[1] - mean_y) ** 2 for point in points) / n)
    radii = [math.hypot(point[0] - mean_x, point[1] - mean_y) for point in points]
    return {
        "nTotal": total,
        "n": n,
        "clearedCount": cleared,
        "clearedRate": cleared / total,
        "meanX": mean_x,
        "meanY": mean_y,
        "sigmaX": sigma_x,
        "sigmaY": sigma_y,
        "p50Radius": percentile(radii, 0.50),
        "p90Radius": percentile(radii, 0.90),
        "p95Radius": percentile(radii, 0.95),
        "maxRadius": max(radii),
    }


def case_key(row: dict[str, Any]) -> str:
    metadata = row.get("plan_metadata") or {}
    source = metadata.get("source_sample_id")
    if source is not None:
        return str(source)
    label = str(row.get("label") or "")
    return label.split("_dist_r", 1)[0]


def after_endpoint(row: dict[str, Any], index: int) -> list[float]:
    values = row["after_position"]
    return [float(values[2 * index]), float(values[2 * index + 1])]


def points_by_role(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = case_key(row)
        entry = result.setdefault(key, {"label": str(row.get("label") or "").split("_dist_r", 1)[0], "category": row.get("category"), "active": [], "targets": {}})
        active = int(row["active_shot_num"])
        entry["active"].append(after_endpoint(row, active))
        for ordinal, target in enumerate(row.get("target_indices") or []):
            entry["targets"].setdefault(str(ordinal), []).append(after_endpoint(row, int(target)))
    return result


def centre_delta(left: dict[str, Any], right: dict[str, Any]) -> float | None:
    if left.get("n", 0) == 0 or right.get("n", 0) == 0:
        return None
    return math.hypot(float(left["meanX"]) - float(right["meanX"]), float(left["meanY"]) - float(right["meanY"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unity", type=Path, required=True)
    parser.add_argument("--local-glob", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    unity_raw = load_jsonl([args.unity])
    local_paths = [Path(path) for path in sorted(glob.glob(args.local_glob))]
    if not local_paths:
        raise ValueError("--local-glob matched no files")
    local_raw = load_jsonl(local_paths)
    # A missed collision / missing final POSITION is not a draw from the
    # requested collision distribution.  Exclude it rather than turning an
    # acquisition failure into a physical tail point.
    unity_rows = [
        row for row in unity_raw
        if row.get("collision_observed") is True and row.get("final_source") == "position"
    ]
    local_rows = [
        row for row in local_raw
        if row.get("collision_observed") is True and (row.get("settle") or {}).get("settled") is True
    ]
    unity = points_by_role(unity_rows)
    local = points_by_role(local_rows)

    cases: list[dict[str, Any]] = []
    for key in sorted(set(unity) | set(local), key=lambda value: int(value) if value.isdigit() else value):
        u, l = unity.get(key), local.get(key)
        active_u = stats([] if u is None else u["active"])
        active_l = stats([] if l is None else l["active"])
        target_rows: list[dict[str, Any]] = []
        target_keys = set((u or {}).get("targets", {})) | set((l or {}).get("targets", {}))
        for target_key in sorted(target_keys, key=int):
            target_u = stats([] if u is None else u["targets"].get(target_key, []))
            target_l = stats([] if l is None else l["targets"].get(target_key, []))
            target_rows.append({"targetOrdinal": int(target_key), "unity": target_u, "local": target_l, "meanCentreDeltaM": centre_delta(target_u, target_l)})
        cases.append({
            "sourceSampleId": key,
            "label": (u or l)["label"],
            "category": (u or l)["category"],
            "active": {"unity": active_u, "local": active_l, "meanCentreDeltaM": centre_delta(active_u, active_l)},
            "targets": target_rows,
        })
    report = {
        "policy": "unpaired empirical distribution comparison; local samples contain no Unity per-shot input",
        "inputs": {
            "unityRowsRaw": len(unity_raw), "unityRowsValid": len(unity_rows),
            "localRowsRaw": len(local_raw), "localRowsValid": len(local_rows),
            "localFiles": [str(path) for path in local_paths],
        },
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "unityRows": len(unity_rows), "localRows": len(local_rows), "caseCount": len(cases)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
