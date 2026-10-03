#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取 K7 控制槽合同壶面的可复算几何特征。

这是状态分类候选特征的只读审计工具，不模拟出手，不筛候选，也不声称可由
静态几何证明合同有解或无解。它记录目标壶、其余壶与两个对称控制槽的距离，
让不同真实 fallback 壶面可以被同一张表比较。
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
from planning_proxy.competition_rules import HOUSE_X, STONE_R  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        required=True,
        metavar="名称=报告.json",
        help="可重复。报告必须含 game.trace 与指定手的 stateBefore。",
    )
    parser.add_argument("--shot", type=int, default=13)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def parse_case(raw: str) -> tuple[str, Path]:
    name, marker, path = raw.partition("=")
    if not marker or not name or not path:
        raise SystemExit(f"--case 格式应为 名称=报告.json，收到：{raw!r}")
    return name, Path(path)


def read_turn(path: Path, shot: int) -> dict[str, Any]:
    report = json.loads(path.read_text(encoding="utf-8"))
    trace = report.get("game", {}).get("trace")
    if not isinstance(trace, list):
        raise SystemExit(f"{path} 不含 game.trace")
    row = next((item for item in trace if isinstance(item, dict) and item.get("shot") == shot), None)
    if not isinstance(row, dict) or not isinstance(row.get("stateBefore"), list):
        raise SystemExit(f"{path} 缺少第 {shot} 手 stateBefore")
    return row


def point_segment_distance(x: float, y: float, ax: float, ay: float, bx: float, by: float) -> tuple[float, float]:
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    if length2 <= 1e-12:
        return math.hypot(x - ax, y - ay), 0.0
    t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / length2))
    return math.hypot(x - (ax + t * dx), y - (ay + t * dy)), t


def control_metrics(target: dict[str, Any], others: list[dict[str, Any]], control: tuple[float, float]) -> dict[str, Any]:
    tx, ty = float(target["x"]), float(target["y"])
    cx, cy = control
    length = math.hypot(cx - tx, cy - ty)
    rows: list[dict[str, Any]] = []
    for stone in others:
        distance, segment_position = point_segment_distance(float(stone["x"]), float(stone["y"]), tx, ty, cx, cy)
        rows.append({
            "index": stone["index"],
            "owner": stone["owner"],
            "distanceToTargetControlSegment": round(distance, 6),
            "segmentPosition": round(segment_position, 6),
            "expandedSegmentClearance": round(distance - 2.0 * STONE_R, 6),
        })
    rows.sort(key=lambda item: (item["expandedSegmentClearance"], item["index"]))
    return {
        "control": [round(cx, 6), round(cy, 6)],
        "targetToControlLength": round(length, 6),
        "nearestStoneToIdealSegment": rows[0] if rows else None,
        "allStoneSegmentRelations": rows,
    }


def case_result(name: str, source: Path, shot: int) -> dict[str, Any]:
    row = read_turn(source, shot)
    detail = row.get("detail") if isinstance(row.get("detail"), dict) else {}
    plan = detail.get("firstPlayerPlan") if isinstance(detail.get("firstPlayerPlan"), dict) else {}
    target_index = plan.get("target_opponent_index")
    try:
        target_index = int(target_index)
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"{source} 第 {shot} 手缺少 target_opponent_index") from exc
    states = row["stateBefore"]
    if target_index >= len(states) or not bool(states[target_index].get("enabled", False)):
        raise SystemExit(f"{source} 目标壶 {target_index} 未启用")
    target = states[target_index]
    active = []
    for index, state in enumerate(states):
        if not bool(state.get("enabled", False)):
            continue
        active.append({
            "index": index,
            "owner": "己方" if index % 2 == 0 else "对方",
            "x": round(float(state["x"]), 6),
            "y": round(float(state["y"]), 6),
        })
    target_row = next(item for item in active if item["index"] == target_index)
    others = [item for item in active if item["index"] != target_index]
    controls = [(float(x), float(y)) for x, y in plan.get("target_points", [])]
    mirrored = [(2.0 * HOUSE_X - x, y) for x, y in controls]
    nearest = min((math.hypot(float(item["x"]) - target_row["x"], float(item["y"]) - target_row["y"]) for item in others), default=None)
    return {
        "name": name,
        "source": str(source).replace("\\", "/"),
        "shot": shot,
        "state": plan.get("situation_type"),
        "contract": plan.get("phase"),
        "targetIndex": target_index,
        "target": target_row,
        "targetOffsetFromCentreLine": round(abs(float(target["x"]) - HOUSE_X), 6),
        "nearestOtherStoneClearance": None if nearest is None else round(nearest - 2.0 * STONE_R, 6),
        "activeStones": active,
        "currentControls": [control_metrics(target_row, others, point) for point in controls],
        "mirroredControls": [control_metrics(target_row, others, point) for point in mirrored],
    }


def main() -> None:
    args = parse_args()
    cases = [case_result(name, path, int(args.shot)) for name, path in (parse_case(raw) for raw in args.case)]
    output = {
        "schema": "k7_control_geometry_audit_v1",
        "scope": "只读静态几何描述；不证明严格 PhysX 合同的有解或无解",
        "stoneRadiusMetres": STONE_R,
        "expandedClearanceDefinition": "壶心到理想线段的最短距离减去两颗壶半径；仅作几何特征",
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "caseCount": len(cases)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
