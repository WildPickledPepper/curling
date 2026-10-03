#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将匿名终局模板聚合为“状态 -> GoalState 原料”的高支持边。

这一步仍在 NWNHT 的按钮中心坐标系中工作。输出边记录历史终局约束、出手后
状态及对方回应状态的*分布*；它们不是已验证策略、更不是胜率证明。仅有
``runtime_candidate=true`` 的边也还必须经过坐标转换、动态角色绑定和严格
PhysX 可达性检验。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


GRID_M = 0.20
MIN_RUNTIME_SUPPORT = 30
MIN_DOMINANT_OWN_AFTER_SHARE = 0.70
MIN_REGION_RADIUS_M = 0.12
CV_TOLERANCE_M = 0.06


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _grid_key(point: dict[str, Any] | None) -> tuple[int, int] | None:
    if point is None:
        return None
    return (round(float(point["x_m"]) / GRID_M), round(float(point["y_m"]) / GRID_M))


def _signature(row: dict[str, Any]) -> tuple[Any, ...]:
    """不把对方回应纳入签名，以免把同一终局目标不必要地打碎。"""

    return (
        str(row["source_state"]),
        str(row["observed_template_kind"]),
        str(row["precision"]),
        int(row["observed_delta"]["opponent_removed_count"]),
        _canonical(row["stone_constraints_when_unambiguous"]),
        _canonical(row["after_own_occupancy"]),
        _grid_key(row.get("active_final_point")),
    )


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [
        {"state": value, "count": count, "share": round(count / total, 6)}
        for value, count in counter.most_common()
    ]


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("quantile needs at least one value")
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))
    return ordered[index]


def _active_region(points: list[tuple[float, float]]) -> dict[str, Any] | None:
    if not points:
        return None
    centre_x = sum(x for x, _ in points) / len(points)
    centre_y = sum(y for _, y in points) / len(points)
    distances = [math.hypot(x - centre_x, y - centre_y) for x, y in points]
    # 90% 历史终局点 + CV 容差；半径下限避免伪精确。
    radius = max(MIN_REGION_RADIUS_M, _quantile(distances, 0.90) + CV_TOLERANCE_M)
    return {
        "shape": "circle",
        "centre_x_m": round(centre_x, 6),
        "centre_y_m": round(centre_y, 6),
        "radius_m": round(radius, 6),
        "point_count": len(points),
        "coverage": "empirical_p90_plus_0.06m_cv_tolerance",
    }


def _edge_id(signature: tuple[Any, ...]) -> str:
    digest = hashlib.sha256(repr(signature).encode("utf-8")).hexdigest()[:16]
    return f"nwnht_goal_edge_{digest}"


def build(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    grouped: dict[tuple[Any, ...], dict[str, Any]] = defaultdict(lambda: {
        "count": 0,
        "own_after": Counter(),
        "after_reply": Counter(),
        "points": [],
        "examples": [],
    })
    row_count = 0
    for row in rows:
        row_count += 1
        signature = _signature(row)
        item = grouped[signature]
        item["count"] += 1
        item["own_after"][str(row["expected_own_after_state"])] += 1
        item["after_reply"][str(row["expected_after_reply_state"])] += 1
        point = row.get("active_final_point")
        if point is not None:
            item["points"].append((float(point["x_m"]), float(point["y_m"])))
        if len(item["examples"]) < 5:
            item["examples"].append(str(row["panel_key"]))

    edges: list[dict[str, Any]] = []
    runtime_count = 0
    for signature, item in grouped.items():
        (
            source_state, template_kind, precision, opponent_removed_count,
            selector_json, occupancy_json, grid,
        ) = signature
        own_distribution = _distribution(item["own_after"])
        reply_distribution = _distribution(item["after_reply"])
        own_dominant_share = own_distribution[0]["share"]
        active_region = _active_region(item["points"])
        reasons: list[str] = []
        if item["count"] < MIN_RUNTIME_SUPPORT:
            reasons.append(f"support<{MIN_RUNTIME_SUPPORT}")
        if precision != "ROLE_AND_REGION":
            reasons.append("no_role_and_region_precision")
        if active_region is None and not json.loads(selector_json):
            reasons.append("no_bindable_stone_or_active_final_region")
        if own_dominant_share < MIN_DOMINANT_OWN_AFTER_SHARE:
            reasons.append(f"own_after_mode_share<{MIN_DOMINANT_OWN_AFTER_SHARE:.2f}")
        runtime_candidate = not reasons
        runtime_count += int(runtime_candidate)
        edges.append({
            "schema": "nwnht_goal_state_edge_v0",
            "edge_id": _edge_id(signature),
            "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES",
            "source_state": source_state,
            "observed_template_kind": template_kind,
            "precision": precision,
            "observed_opponent_removed_count": opponent_removed_count,
            "stone_constraints_when_unambiguous": json.loads(selector_json),
            "after_own_occupancy": json.loads(occupancy_json),
            "active_final_region": active_region,
            "active_region_grid_cell": None if grid is None else {"x": grid[0], "y": grid[1], "size_m": GRID_M},
            "support": item["count"],
            "expected_own_after_states": own_distribution,
            "expected_after_reply_states": reply_distribution,
            "runtime_candidate": runtime_candidate,
            "not_runtime_candidate_reasons": reasons,
            "examples": item["examples"],
            "evidence_status": "HISTORICAL_TEMPLATE",
            "warning": "Observational recurring terminal pattern only; must be dynamically bound and validated with local strict PhysX before runtime use.",
        })
    edges.sort(key=lambda edge: (-int(edge["support"]), str(edge["edge_id"])))
    manifest = {
        "schema": "nwnht_goal_state_edge_manifest_v0",
        "input_row_count": row_count,
        "edge_count": len(edges),
        "runtime_candidate_count": runtime_count,
        "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES",
        "clustering": {
            "active_final_grid_m": GRID_M,
            "region_radius": "max(0.12m, empirical p90 distance to centroid + 0.06m CV tolerance)",
            "reply_handling": "reply is stored as a distribution and never included in the goal-edge signature",
        },
        "runtime_candidate_gate": {
            "min_support": MIN_RUNTIME_SUPPORT,
            "required_precision": "ROLE_AND_REGION",
            "min_dominant_own_after_share": MIN_DOMINANT_OWN_AFTER_SHARE,
            "additional_required_step": "local coordinate compilation, runtime slot binding, local rule check, strict PhysX feasibility and reply search",
        },
        "warning": "runtime_candidate is a data-support gate only, not a deployed policy or a winning claim.",
    }
    return edges, manifest


def main() -> int:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_anonymous_goal_templates_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_goal_state_edges_v0.json")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_goal_state_edges_v0_manifest.json")
    args = parser.parse_args()
    edges, manifest = build(read_jsonl(args.input))
    args.output.write_text(json.dumps(edges, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("GoalState 转移边：%d 条；数据支持候选：%d 条。" % (manifest["edge_count"], manifest["runtime_candidate_count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
