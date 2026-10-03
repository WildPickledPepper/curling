#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回归课程平台中曾直接退到 (3,0,0) 的后手遮挡壶面。

输入仅包含实际壶面；不读取任何历史 BESTSHOT。每条样本都必须通过当前
``ProxyMatchPlayer.choose`` 的完整后手入口，并返回严格 PhysX 验收的净空
绕屏风 draw。这个基准专门防止“最深目标壶不可直接首撞”再次退化为静态球。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer  # noqa: E402
from planning_proxy.solver_benchmark.run_draw_recall_benchmark import states_from_board  # noqa: E402


DEFAULT_DATASET = ROOT / "planning_proxy" / "solver_benchmark" / "course_backhand_screen_draw_v1.json"
DRAW_MODE = "backhand_draw_around_screen_after_unreachable_takeout"


def run_one(player: ProxyMatchPlayer, sample: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    shot, detail = player.choose(
        states_from_board(sample["board"]),
        proxy_team=int(sample["proxy_team"]),
        shot_index=int(sample["shot_index"]),
        match_seed=int(sample["match_seed"]),
    )
    elapsed = time.perf_counter() - started
    strict = detail.get("strict") or {}
    passed = bool(
        detail.get("mode") == DRAW_MODE
        and strict.get("rule_legal")
        and int(detail.get("selectedOwnInHouseWorst", 0)) >= 1
        and not bool(detail.get("plannerBudgetExceeded", False))
    )
    return {
        "id": sample["id"],
        "passed": passed,
        "elapsed_seconds": elapsed,
        "mode": detail.get("mode"),
        "bestshot": [float(value) for value in shot],
        "previous_fallback_target": sample.get("previous_fallback_target"),
        "selected_own_in_house_worst": detail.get("selectedOwnInHouseWorst"),
        "planner_budget_exceeded": detail.get("plannerBudgetExceeded"),
        "draw_solver": (detail.get("fastTargetedDraw") or {}).get("solver"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--budget-seconds", type=float, default=105.0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    dataset = args.dataset if args.dataset.is_absolute() else ROOT / args.dataset
    payload = json.loads(dataset.read_text(encoding="utf-8"))
    player = ProxyMatchPlayer(
        physics_seeds=int(payload.get("physics_seed_count", 3)),
        parent_regions=3,
        decision_budget_seconds=float(args.budget_seconds),
    )
    rows = [run_one(player, sample) for sample in payload["samples"]]
    report = {
        "schema": "planning_proxy_course_backhand_screen_draw_recall_v1",
        "dataset": str(dataset),
        "budget_seconds": float(args.budget_seconds),
        "sample_count": len(rows),
        "passed_count": sum(bool(row["passed"]) for row in rows),
        "rows": rows,
    }
    output = args.output or dataset.with_name(dataset.stem + "_recall.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "passed": report["passed_count"], "samples": len(rows)}, ensure_ascii=False))
    return 0 if report["passed_count"] == len(rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
