#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建后半局稀疏状态的历史目标区域回退边。

精细 ``state -> 0.2m 终局点`` 在 K3 以后支持度稀疏。本工件只保留：
阶段带、中心控制、双方营内层，并将出手壶终局聚成 0.6m 网格圆区。它是
``PHYSX_SEARCH_REQUIRED`` 的第三层回退，不是精细状态的替代，更不声称唯一
后继局面。
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


GRID_M = 0.60
MIN_SUPPORT = 30
MIN_RADIUS_M = 0.30
CV_TOLERANCE_M = 0.08


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def compact_zone_state(state: str) -> str:
    """只从既有 runtime-safe core state 构造区域回退状态。"""

    match = re.match(r"K(\d+)_CORE\[", state)
    if match is None:
        raise ValueError("需要 K*_CORE[...] 状态")
    k = int(match.group(1))
    values = dict(re.findall(r"([A-Za-z_]+)=([^;\]]+)", state))
    required = {"control", "F_house", "O_house"}
    if required - values.keys():
        raise ValueError("core state 缺少特征")
    phase = "K1_2" if k <= 2 else "K3_4" if k <= 4 else "K5_6" if k <= 6 else "K7_8"
    return f"{phase}_ZONE[control={values['control']};F_house={values['F_house']};O_house={values['O_house']}]"


def _grid(point: dict[str, Any]) -> tuple[int, int]:
    return (round(float(point["x_m"]) / GRID_M), round(float(point["y_m"]) / GRID_M))


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [
        {"state": key, "count": value, "share": round(value / total, 6)}
        for key, value in counter.most_common()
    ]


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))]


def _region(points: list[tuple[float, float]]) -> dict[str, Any]:
    x = sum(item[0] for item in points) / len(points)
    y = sum(item[1] for item in points) / len(points)
    distances = [math.hypot(px - x, py - y) for px, py in points]
    return {
        "shape": "circle", "centre_x_m": round(x, 6), "centre_y_m": round(y, 6),
        "radius_m": round(max(MIN_RADIUS_M, _quantile(distances, .90) + CV_TOLERANCE_M), 6),
        "point_count": len(points), "coverage": "empirical_p90_plus_0.08m_cv_tolerance",
    }


def build(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    grouped: dict[tuple[str, tuple[int, int]], dict[str, Any]] = defaultdict(lambda: {
        "support": 0, "points": [], "own_after": Counter(), "reply": Counter(), "examples": [],
    })
    eligible_rows = 0
    for row in rows:
        point = row.get("active_final_point")
        if str(row.get("observed_template_kind")) != "ACTIVE_STONE_PLACEMENT" or point is None:
            continue
        if str(point.get("zone")) == "outside_tactical_zone":
            continue
        eligible_rows += 1
        key = (compact_zone_state(str(row["source_state"])), _grid(point))
        item = grouped[key]
        item["support"] += 1
        item["points"].append((float(point["x_m"]), float(point["y_m"])))
        item["own_after"][str(row["expected_own_after_state"])] += 1
        item["reply"][str(row["expected_after_reply_state"])] += 1
        if len(item["examples"]) < 5:
            item["examples"].append(str(row["panel_key"]))
    edges: list[dict[str, Any]] = []
    by_phase: Counter[str] = Counter()
    for (source, grid), item in grouped.items():
        if item["support"] < MIN_SUPPORT:
            continue
        by_phase[source.split("_ZONE", 1)[0]] += 1
        edges.append({
            "schema": "nwnht_zone_goal_fallback_v0",
            "fallback_id": f"{source}|grid={grid[0]},{grid[1]}",
            "source_zone_state": source,
            "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES",
            "active_final_region": _region(item["points"]),
            "grid_cell": {"x": grid[0], "y": grid[1], "size_m": GRID_M},
            "support": item["support"],
            "expected_own_after_states": _distribution(item["own_after"]),
            "expected_after_reply_states": _distribution(item["reply"]),
            "physx_search_required": True,
            "evidence_status": "HISTORICAL_ZONE_FALLBACK",
            "examples": item["examples"],
            "warning": "Coarse historical target region. Do not impose a unique next fine state or hard occupancy constraint; reclassify the actual PhysX result.",
        })
    edges.sort(key=lambda item: (-int(item["support"]), str(item["fallback_id"])))
    manifest = {
        "schema": "nwnht_zone_goal_fallback_manifest_v0",
        "eligible_active_placement_rows": eligible_rows,
        "edge_count": len(edges),
        "edge_count_by_phase": dict(sorted(by_phase.items())),
        "grid_m": GRID_M, "min_support": MIN_SUPPORT,
        "warning": "Third-tier fallback after collision and exact fine goals; historical recurrence only, strict PhysX search required.",
    }
    return edges, manifest


def main() -> int:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_anonymous_goal_templates_v1.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_zone_goal_fallbacks_v0.json")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_zone_goal_fallbacks_v0_manifest.json")
    args = parser.parse_args()
    edges, manifest = build(read_jsonl(args.input))
    args.output.write_text(json.dumps(edges, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("区域 GoalState 回退边：%d 条。" % manifest["edge_count"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
