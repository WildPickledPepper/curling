#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从完整真实回放审计 K7→对手K7→K8 的连续状态。

历史文件可来自不同状态机版本，故本工具不把它们当作可直接合并的胜率样本。
它保存每个来源、实际执行合同和真实物理后壶面，用来发现需要在同一条状态
路径上解释的反例：K7 当手严格成功却仍在 K8 回退，或 K7 后对手一手拆空。
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "planning_proxy" / "runs"
DEFAULT_OUTPUT = RUNS / "k7_k8_transition_audit.json"

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R  # noqa: E402


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return raw if isinstance(raw, dict) else None


def turn(trace: list[dict[str, Any]], shot: int) -> dict[str, Any] | None:
    return next((item for item in trace if item.get("shot") == shot), None)


def enabled(states: list[dict[str, Any]], index: int) -> dict[str, Any] | None:
    return states[index] if index < len(states) and bool(states[index].get("enabled", False)) else None


def in_house(state: dict[str, Any]) -> bool:
    return math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R


def shape(states: list[dict[str, Any]]) -> dict[str, Any]:
    house = [(i, value) for i, value in enumerate(states) if bool(value.get("enabled", False)) and in_house(value)]
    own = sum(index % 2 == 0 for index, _ in house)
    opponent = len(house) - own
    closest = None
    if house:
        index, _ = min(house, key=lambda row: math.hypot(float(row[1]["x"]) - HOUSE_X, float(row[1]["y"]) - HOUSE_Y))
        closest = "self" if index % 2 == 0 else "opponent"
    return {"ownHouse": own, "opponentHouse": opponent, "closest": closest}


def defensive_roles(states: list[dict[str, Any]]) -> dict[str, Any]:
    """以现行状态机使用的几何角色描述 K8 入局壶面。"""

    active = [(index, state) for index, state in enumerate(states) if bool(state.get("enabled", False))]
    own = [(index, state) for index, state in active if index % 2 == 0]
    centre_guard = any(
        abs(float(state["x"]) - HOUSE_X) <= 0.25 and abs(float(state["y"]) - 7.15) <= 0.60
        for _, state in own
    )
    button_anchor = any(math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y) <= 0.25 for _, state in own)
    own_inner = sum(math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y) <= 0.610 for _, state in own)
    gate_centres = (
        ((1.82, 6.42), (1.92, 6.12), (2.08, 5.92)),
        ((2.93, 6.42), (2.83, 6.12), (2.67, 5.92)),
    )
    gates = sum(any(min(math.hypot(float(state["x"]) - x, float(state["y"]) - y) for x, y in centres) <= 0.55 for _, state in own) for centres in gate_centres)
    return {
        "centreGuard": centre_guard,
        "buttonAnchor": button_anchor,
        "ownInner": own_inner,
        "sideGates": gates,
    }


def k7_threat_geometry(states: list[dict[str, Any]], target_index: Any) -> dict[str, Any] | None:
    """把 K7 主威胁按可观察的营内/前场和横向位置分桶，供统计而非直接决策。"""

    try:
        target = enabled(states, int(target_index))
    except (TypeError, ValueError):
        return None
    if target is None:
        return None
    x, y = float(target["x"]), float(target["y"])
    distance = math.hypot(x - HOUSE_X, y - HOUSE_Y)
    vertical = "内圈" if distance <= 0.610 else "营内" if distance <= HOUSE_R + STONE_R else "前场"
    offset = abs(x - HOUSE_X)
    lateral = "中线" if offset <= 0.35 else "近侧" if offset <= 0.90 else "宽侧"
    return {"class": f"{vertical}_{lateral}", "x": round(x, 3), "y": round(y, 3), "distanceToButton": round(distance, 3)}


def terminal_result(game: dict[str, Any]) -> str:
    score = game.get("finalScoreProxy", game.get("finalScoreFirst"))
    try:
        numeric = int(score)
    except (TypeError, ValueError):
        return "未知"
    return "胜" if numeric > 0 else "平" if numeric == 0 else "负"


def detail_plan(item: dict[str, Any]) -> dict[str, Any]:
    detail = item.get("detail")
    return detail.get("firstPlayerPlan", {}) if isinstance(detail, dict) else {}


def fallback(item: dict[str, Any]) -> bool:
    detail = item.get("detail")
    return bool(isinstance(detail, dict) and detail.get("fallbackReason"))


def iter_rows(path: Path) -> Iterable[dict[str, Any]]:
    report = read_json(path)
    if report is None or "ideal_state_machine" in path.name:
        return
    for game_no, game in enumerate(report.get("games", []), 1):
        if not isinstance(game, dict) or game.get("proxyTeam") != "first" or not bool(game.get("completedEnd")):
            continue
        trace = game.get("trace")
        if not isinstance(trace, list) or len(trace) < 16:
            continue
        k6_reply, k7, reply, k8, final = (turn(trace, shot) for shot in (12, 13, 14, 15, 16))
        if not all(isinstance(item, dict) for item in (k6_reply, k7, reply, k8, final)):
            continue
        k6_reply_after = k6_reply.get("stateAfter")
        k7_after = k7.get("stateAfter")
        reply_after = reply.get("stateAfter")
        k8_after = k8.get("stateAfter")
        final_after = final.get("stateAfter")
        if not all(isinstance(item, list) for item in (k6_reply_after, k7_after, reply_after, k8_after, final_after)):
            continue
        k7_plan, k8_plan = detail_plan(k7), detail_plan(k8)
        k7_active = enabled(k7_after, 12)
        reply_active = enabled(reply_after, 13)
        k7_anchor_survives = enabled(reply_after, 12) is not None
        yield {
            "source": path.name,
            "game": game_no,
            "opponent": report.get("opponent", "未知"),
            "seed": game.get("seed"),
            "finalResult": terminal_result(game),
            "finalScoreProxy": game.get("finalScoreProxy", game.get("finalScoreFirst")),
            "k7Situation": k7_plan.get("situation_type"),
            "k7Strategy": k7_plan.get("strategy_type"),
            "k7Phase": k7_plan.get("phase"),
            "k7Mode": (k7.get("detail") or {}).get("mode"),
            "k7Fallback": fallback(k7),
            "k7DecisionSeconds": k7.get("decisionSeconds"),
            "k7InputThreatGeometry": k7_threat_geometry(k7.get("stateBefore", []), k7_plan.get("target_opponent_index")),
            "afterOpponentK6": shape(k6_reply_after),
            "afterOpponentK6Roles": defensive_roles(k6_reply_after),
            "k7After": shape(k7_after),
            "k7Active": None if k7_active is None else [round(float(k7_active["x"]), 3), round(float(k7_active["y"]), 3)],
            "afterOpponentK7": shape(reply_after),
            "afterOpponentK7Roles": defensive_roles(reply_after),
            "k7AnchorSurvivesOpponentReply": k7_anchor_survives,
            "opponentK7Active": None if reply_active is None else [round(float(reply_active["x"]), 3), round(float(reply_active["y"]), 3)],
            "k8Situation": k8_plan.get("situation_type"),
            "k8Strategy": k8_plan.get("strategy_type"),
            "k8Phase": k8_plan.get("phase"),
            "k8Mode": (k8.get("detail") or {}).get("mode"),
            "k8Fallback": fallback(k8),
            "k8DecisionSeconds": k8.get("decisionSeconds"),
            "k8After": shape(k8_after),
            "finalShape": shape(final_after),
        }


def shape_key(value: dict[str, Any]) -> str:
    return f"我营{value['ownHouse']}/对营{value['opponentHouse']}/最近{value['closest'] or '无'}"


def role_key(value: dict[str, Any]) -> str:
    return f"中守{int(value['centreGuard'])}/按钮锚{int(value['buttonAnchor'])}/内圈{value['ownInner']}/侧门{value['sideGates']}"


def summary(rows: list[dict[str, Any]], group_key: str) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if group_key == "reply_shape":
            key = (shape_key(row["afterOpponentK7"]), bool(row["k7AnchorSurvivesOpponentReply"]), bool(row["k8Fallback"]))
        elif group_key == "reply_roles":
            key = (role_key(row["afterOpponentK7Roles"]), bool(row["k8Fallback"]))
        elif group_key == "k6_reply_roles":
            key = (role_key(row["afterOpponentK6Roles"]), bool(row["k7Fallback"]), bool(row["k8Fallback"]))
        elif group_key == "k7_threat_geometry":
            geometry = row.get("k7InputThreatGeometry") or {"class": "无目标"}
            key = (str(geometry["class"]), bool(row["k7Fallback"]), bool(row["k8Fallback"]))
        else:
            key = (row["k7Strategy"], row["k8Strategy"], bool(row["k7Fallback"]), bool(row["k8Fallback"]))
        groups[key].append(row)
    output: list[dict[str, Any]] = []
    for key, items in sorted(groups.items(), key=lambda item: (-len(item[1]), str(item[0]))):
        outcomes = Counter(item["finalResult"] for item in items)
        scenarios = sorted({(str(item["opponent"]), str(item["seed"])) for item in items})
        output.append({
            "group": list(key),
            "records": len(items),
            "distinctScenarioCount": len(scenarios),
            "distinctScenarios": [{"opponent": opponent, "seed": seed} for opponent, seed in scenarios],
            "wins": outcomes["胜"], "draws": outcomes["平"], "losses": outcomes["负"],
            "sources": sorted({str(item["source"]) for item in items}),
            "opponents": dict(sorted(Counter(str(item["opponent"]) for item in items).items())),
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=RUNS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = [row for path in sorted(args.runs.glob("*.json")) for row in iter_rows(path)]
    payload = {
        "schema": "k7_k8_transition_audit_v1",
        "meaning": "完整真实回放的 K7-K8 连续状态审计；跨版本记录只能作为反例与规律线索。",
        "recordCount": len(rows),
        "summaryByK7K8Contract": summary(rows, "contract"),
        "summaryByOpponentK7Shape": summary(rows, "reply_shape"),
        "summaryByOpponentK7Roles": summary(rows, "reply_roles"),
        "summaryByOpponentK6Roles": summary(rows, "k6_reply_roles"),
        "summaryByK7ThreatGeometry": summary(rows, "k7_threat_geometry"),
        "records": rows,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "recordCount": len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
