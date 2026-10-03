#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将当前本地棋盘 JSON 转为按优先级排列的 GoalState。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .proposer import propose_goal_states


def load_board(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    board = raw.get("board") if isinstance(raw, dict) else raw
    if not isinstance(board, list):
        raise ValueError("棋盘 JSON 必须是壶数组，或包含 board 数组")
    required = {"index", "owner", "x", "y"}
    for index, stone in enumerate(board):
        if not isinstance(stone, dict) or required - stone.keys():
            raise ValueError(f"board[{index}] 缺少 index/owner/x/y")
    return board


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board-json", type=Path, required=True, help="本地 PhysX 坐标的当前棋盘 JSON。")
    parser.add_argument("--own-throw-number", type=int, required=True, help="先手方本局第 K 次出手，范围 1..8。")
    parser.add_argument("--active-stone-index", type=int, default=None, help="本次出手壶的 PhysX slot；不传则保留 active_delivery 占位符。")
    parser.add_argument("--max-fine", type=int, default=3)
    parser.add_argument("--max-collision-pairs", type=int, default=3)
    parser.add_argument("--max-zone", type=int, default=3)
    parser.add_argument("--output", type=Path, default=None, help="可选输出 JSON 文件；默认打印到 stdout。")
    args = parser.parse_args()
    result = propose_goal_states(
        load_board(args.board_json), args.own_throw_number, active_stone_index=args.active_stone_index,
        max_fine=args.max_fine, max_collision_pairs=args.max_collision_pairs, max_zone=args.max_zone,
    )
    text = json.dumps(result.to_json(), ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
