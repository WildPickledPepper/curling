#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计真实完整对局中的 K3→对手K4 分叉。

这不是胜率评测器。历史报告来自不同版本，因此它只把每条回放保留为可追溯
证据，回答较窄的问题：在“中线守壶仍在、K2 锚被清、对手侧营内得分”的同类
K3 局面中，K3 新锚落到什么角色区，对手下一壶是否能清掉它，以及这些分叉在
已有完整对局中如何收尾。
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R  # noqa: E402


RUNS = ROOT / "planning_proxy" / "runs"
DEFAULT_OUTPUT = RUNS / "k3_k4_lineage_audit.json"


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def enabled(states: list[dict[str, Any]], index: int) -> dict[str, Any] | None:
    if index >= len(states):
        return None
    state = states[index]
    return state if bool(state.get("enabled", False)) else None


def in_house(state: dict[str, Any] | None) -> bool:
    if state is None:
        return False
    return math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R


def anchor_role(state: dict[str, Any] | None) -> str:
    """按相对中线与大本营角色分类，不使用历史动作坐标。"""

    if state is None:
        return "未留住新锚"
    x, y = float(state["x"]), float(state["y"])
    if abs(x - HOUSE_X) <= 0.28 and HOUSE_Y - 0.28 <= y <= HOUSE_Y + 0.42:
        return "中线守壶对齐锚"
    if in_house(state) and y >= HOUSE_Y - 0.05 and abs(x - HOUSE_X) > 0.28:
        return "侧前营内锚"
    if in_house(state):
        return "其它营内锚"
    return "营外/非锚落点"


def board_shape(states: list[dict[str, Any]]) -> str:
    """用状态而非动作名描述后续壶面，便于跨版本连接整条路径。"""

    house: list[tuple[int, dict[str, Any]]] = [
        (index, state)
        for index, state in enumerate(states)
        if bool(state.get("enabled", False)) and in_house(state)
    ]
    own = sum(index % 2 == 0 for index, _ in house)
    opponent = len(house) - own
    if not house:
        closest = "无"
    else:
        closest_index, _ = min(
            house,
            key=lambda item: math.hypot(float(item[1]["x"]) - HOUSE_X, float(item[1]["y"]) - HOUSE_Y),
        )
        closest = "我" if closest_index % 2 == 0 else "对"
    return f"我营{own}/对营{opponent}/最近{closest}"


def state_after(trace: list[dict[str, Any]], shot: int) -> list[dict[str, Any]] | None:
    turn = next((item for item in trace if item.get("shot") == shot), None)
    states = turn.get("stateAfter") if isinstance(turn, dict) else None
    return states if isinstance(states, list) else None


def result(game: dict[str, Any]) -> str:
    value = game.get("finalScoreProxy", game.get("finalScoreFirst"))
    try:
        score = int(value)
    except (TypeError, ValueError):
        return "未知"
    return "胜" if score > 0 else "平" if score == 0 else "负"


def first_plan(turn: dict[str, Any]) -> dict[str, Any]:
    detail = turn.get("detail")
    return detail.get("firstPlayerPlan", {}) if isinstance(detail, dict) else {}


def is_target_family(turn: dict[str, Any]) -> bool:
    plan = first_plan(turn)
    # 以当时已执行的状态机分类为主；再保留阶段名，兼容旧报告。
    return (
        plan.get("strategy_type") == "CLEAR_AND_ROLL_TO_COUNTER_INNER_ANCHOR"
        or plan.get("phase") in {
            "clear_then_repair_closest_scoring_anchor",
            "third_clear_and_roll_to_guard_aligned_recovery",
        }
    )


def iter_rows(path: Path) -> Iterable[dict[str, Any]]:
    report = read_json(path)
    if report is None or "ideal_state_machine" in path.name:
        return
    for game_no, game in enumerate(report.get("games", []), 1):
        if not isinstance(game, dict) or game.get("proxyTeam") != "first":
            continue
        trace = game.get("trace")
        if not bool(game.get("completedEnd")) or not isinstance(trace, list) or len(trace) < 16:
            continue
        # 全球 shot 5 是我方 K3，shot 6 是对手紧接的回应。
        k3 = next((item for item in trace if item.get("shot") == 5 and item.get("actor") == "proxy"), None)
        reply = next((item for item in trace if item.get("shot") == 6 and item.get("actor") != "proxy"), None)
        if not isinstance(k3, dict) or not isinstance(reply, dict) or not is_target_family(k3):
            continue
        after_k3 = k3.get("stateAfter")
        after_k4 = reply.get("stateAfter")
        before_k3 = k3.get("stateBefore")
        if not all(isinstance(states, list) for states in (before_k3, after_k3, after_k4)):
            continue
        # slot 0 中线守壶、slot 2 K2 锚、slot 3 对手壶、slot 4 K3 出手壶、
        # slot 5 对手 K4 出手壶，是这一族状态在真实回放中的固定时序角色。
        k3_anchor = enabled(after_k3, 4)
        k4_anchor = enabled(after_k4, 4)
        opponent_reply = enabled(after_k4, 5)
        later_shapes = {
            f"afterShot{shot}": board_shape(states)
            for shot in (9, 10, 11, 12, 13, 14, 15, 16)
            if (states := state_after(trace, shot)) is not None
        }
        plan = first_plan(k3)
        yield {
            "source": path.name,
            "game": game_no,
            "opponent": report.get("opponent", "未知"),
            "seed": game.get("seed"),
            "finalResult": result(game),
            "finalScoreProxy": game.get("finalScoreProxy", game.get("finalScoreFirst")),
            "historicalPhase": plan.get("phase"),
            "historicalStrategy": plan.get("strategy_type"),
            "k3BeforeCentreGuardPresent": enabled(before_k3, 0) is not None,
            "k3BeforeK2AnchorPresent": enabled(before_k3, 2) is not None,
            "k3BeforeOpponentThreatPresent": enabled(before_k3, 3) is not None,
            "k3Anchor": None if k3_anchor is None else [round(float(k3_anchor["x"]), 3), round(float(k3_anchor["y"]), 3)],
            "k3AnchorRole": anchor_role(k3_anchor),
            "k3TargetCleared": enabled(after_k3, 3) is None,
            "k4AnchorSurvives": k4_anchor is not None,
            "k4ReplyInHouse": in_house(opponent_reply),
            "k4Reply": None if opponent_reply is None else [round(float(opponent_reply["x"]), 3), round(float(opponent_reply["y"]), 3)],
            "k3DecisionSeconds": k3.get("decisionSeconds"),
            **later_shapes,
        }


def summarise(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, bool, bool], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["k3AnchorRole"], row["k4AnchorSurvives"], row["k4ReplyInHouse"])].append(row)
    output: list[dict[str, Any]] = []
    for (role, survives, reply_house), items in sorted(groups.items()):
        outcomes = Counter(row["finalResult"] for row in items)
        output.append({
            "k3AnchorRole": role,
            "k4AnchorSurvives": survives,
            "k4ReplyInHouse": reply_house,
            "records": len(items),
            "wins": outcomes["胜"], "draws": outcomes["平"], "losses": outcomes["负"],
            "opponents": dict(sorted(Counter(str(row["opponent"]) for row in items).items())),
            "sources": sorted({str(row["source"]) for row in items}),
        })
    return output


def summarise_later_shapes(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """分别查看 K5--K8 各壶后结构与终局的关联；跨版本仅作线索。"""

    result: dict[str, list[dict[str, Any]]] = {}
    for key in (f"afterShot{shot}" for shot in (9, 10, 11, 12, 13, 14, 15, 16)):
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            if key in row:
                groups[str(row[key])].append(row)
        result[key] = [
            {
                "shape": shape,
                "records": len(items),
                "wins": (outcomes := Counter(item["finalResult"] for item in items))["胜"],
                "draws": outcomes["平"],
                "losses": outcomes["负"],
                "opponents": dict(sorted(Counter(str(item["opponent"]) for item in items).items())),
            }
            for shape, items in sorted(groups.items())
        ]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=RUNS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = [row for path in sorted(args.runs.glob("*.json")) for row in iter_rows(path)]
    payload = {
        "schema": "k3_k4_lineage_audit_v1",
        "meaning": "完整真实回放的 K3→对手K4 分叉审计；跨版本记录不可直接作为因果胜率。",
        "recordCount": len(rows),
        "summary": summarise(rows),
        "laterShapeSummary": summarise_later_shapes(rows),
        "records": rows,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "recordCount": len(rows), "groups": len(payload["summary"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
