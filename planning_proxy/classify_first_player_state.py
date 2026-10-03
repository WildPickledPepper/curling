#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只分类先手壶面，不运行粗筛或 PhysX。

当比赛端已经收到 POSITION 时，可先调用本程序（或直接调用同名 Python
函数）立即得到离散策略类型；连续的 v/h/w 仍由后续的粗代理和严格 PhysX
求解。

示例：

    python planning_proxy\\classify_first_player_state.py --board board.json --shot-index 6

也可直接读取项目的多场景 fixture：

    python planning_proxy\\classify_first_player_state.py \
        --board planning_proxy\\fixtures\\rule_and_safety_scenarios_v1.json \
        --scenario-id 08_early_centre_guard --shot-index 2
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from planning_proxy.first_player_strategy import plan_first_player_turn  # noqa: E402


def load_board(path: Path, scenario_id: str | None = None) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and isinstance(raw.get("scenarios"), list):
        if not scenario_id:
            raise ValueError("此文件包含多个 scenarios；请提供 --scenario-id")
        selected = next((row for row in raw["scenarios"] if isinstance(row, dict) and row.get("id") == scenario_id), None)
        if selected is None:
            raise ValueError(f"找不到 scenario-id={scenario_id}")
        raw = selected.get("board")
    if not isinstance(raw, list):
        raise ValueError("--board 必须是 JSON 数组")
    board: list[dict[str, Any]] = []
    for row in raw:
        if not isinstance(row, dict):
            raise ValueError("board 的每一项必须是对象")
        if not bool(row.get("enabled", True)):
            continue
        if str(row.get("owner")) not in {"self", "opponent"}:
            raise ValueError("每颗有效壶必须标注 owner=self 或 opponent")
        for field in ("index", "x", "y"):
            if field not in row:
                raise ValueError(f"有效壶缺少 {field}")
        board.append(row)
    return board


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", required=True, type=Path, help="当前静止壶面 JSON 数组")
    parser.add_argument("--scenario-id", default=None, help="当 --board 是多场景 fixture 时选择其中一行")
    parser.add_argument("--shot-index", required=True, type=int, help="当前全局零基手数；先手只能是 0,2,...,14")
    args = parser.parse_args()
    try:
        plan = plan_first_player_turn(load_board(args.board, args.scenario_id), args.shot_index)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法分类先手壶面：{exc}") from exc
    print(json.dumps(plan.to_json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
