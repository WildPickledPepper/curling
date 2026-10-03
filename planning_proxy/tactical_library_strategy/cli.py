#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""命令行查看独立先手战术库的离散输出，不运行 PhysX。

示例：
    python planning_proxy\\tactical_library_strategy\\cli.py \\
      --board board.json --own-throw-number 4
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from planning_proxy.tactical_library_strategy.target_regions import candidate_target_regions  # noqa: E402


def load_board(path: Path) -> list[dict[str, object]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("--board 必须是 JSON 数组")
    board: list[dict[str, object]] = []
    for row in raw:
        if not isinstance(row, dict) or not bool(row.get("enabled", True)):
            continue
        if str(row.get("owner")) not in {"self", "opponent"}:
            raise ValueError("每颗有效壶必须标注 owner=self 或 opponent")
        if any(field not in row for field in ("index", "x", "y")):
            raise ValueError("每颗有效壶必须包含 index/x/y")
        board.append(row)
    return board


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", required=True, type=Path, help="当前静止壶面 JSON 数组")
    parser.add_argument("--own-throw-number", required=True, type=int, help="先手自己的 K1..K8")
    args = parser.parse_args()
    try:
        result = candidate_target_regions(
            load_board(args.board), args.own_throw_number,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法生成战术库策略：{exc}") from exc
    print(json.dumps(result.to_json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
