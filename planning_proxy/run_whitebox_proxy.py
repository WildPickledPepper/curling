#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运行 P1 白盒代理，快速筛出值得严格 PhysX 复核的攻击路线。

示例（不需要 pyphysx）：

    python planning_proxy\\run_whitebox_proxy.py --top-k 12

传入自己的局面 JSON：

    python planning_proxy\\run_whitebox_proxy.py --board board.json --top-k 12

board.json 是一个数组，每项含 index、owner（self/opponent）、x、y，enabled 可省略。
输出只是“严格复核候选清单”，不能直接发送给比赛服务器。
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Optional, Sequence

from whitebox_proxy import Stone, rank_attack_candidates, regular_shot_grid


DEFAULT_BOARD = (
    # 一个己方前置守壶、两个敌方营内壶的示例；index 0 留给本次出手壶。
    Stone(2, "self", 2.05, 7.25),
    Stone(1, "opponent", 2.55, 5.45),
    Stone(3, "opponent", 2.75, 4.72),
)


def load_board(path: Optional[Path]) -> Sequence[Stone]:
    if path is None:
        return DEFAULT_BOARD
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("board JSON 顶层必须是数组")
    return tuple(
        Stone(
            index=int(item["index"]), owner=str(item["owner"]), x=float(item["x"]), y=float(item["y"]),
            enabled=bool(item.get("enabled", True)),
        )
        for item in raw
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", type=Path, default=None, help="局面 JSON；默认使用一个内置多壶示例。")
    parser.add_argument("--top-k", type=int, default=12, help="输出前几条严格复核候选。")
    parser.add_argument("--output", type=Path, default=None, help="可选 JSON 报告路径。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.top_k < 1:
        raise SystemExit("--top-k 至少为 1")
    stones = load_board(args.board)
    start = time.perf_counter()
    candidates = list(regular_shot_grid())
    ranked = rank_attack_candidates(candidates, stones)
    candidate_count = len(candidates)
    source = "direct_formula_development_baseline"
    elapsed = time.perf_counter() - start
    selected = ranked[: args.top_k]
    print("P1 白盒粗筛：%d 条候选，%.3f 秒；以下仅供严格 PhysX 复核。" % (candidate_count, elapsed))
    for rank, item in enumerate(selected, 1):
        print(
            "%2d. BESTSHOT %.3f %.3f %.3f | %.1f | first=%s/%s | %s"
            % (
                rank, item.shot.v0, item.shot.h0, item.shot.w0, item.proxy_score,
                item.first_hit_owner, item.first_hit_index, "；".join(item.notes),
            )
        )
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(
                {
                    "schema": "whitebox_attack_proxy_p1_v1",
                    "warning": "只做自由滑行首撞筛选；任何候选均须由严格 PhysX 复核。",
                    "source": source,
                    "board": [stone.__dict__ for stone in stones],
                    "candidateCount": candidate_count,
                    "elapsedSeconds": elapsed,
                    "top": [item.to_json() for item in selected],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print("report=%s" % args.output)


if __name__ == "__main__":
    main()
