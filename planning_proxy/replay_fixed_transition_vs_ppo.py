#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从一个固定的已验证 G_k 继续回放 PPO 对抗。

用途是评估“状态机选择这个目标局面后，PPO 回应会把我们带到哪里”，而不是
只看该手结束时的临时比分。输入的 fixture 是投壶前壶面；脚本先用严格
PhysX 投出 ``--shot``，再让既有状态机和确定性 PPO 继续对局。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    STONE_COUNT, StrictCurlingEnd, install_bundled_pyphysx, score_board,
)
from planning_proxy.evaluate_vs_teammate_ppo import (  # noqa: E402
    ProxyMatchPlayer, run_game, state_snapshot,
)
from training_research.opponents.teammate_ppo_adapter import TeammatePPOOpponent  # noqa: E402


def expanded_fixture(path: Path) -> list[dict[str, Any]]:
    """把只列出在场壶的 fixture 补成严格环境要求的 16 个 slot。"""

    raw = json.loads(path.read_text(encoding="utf-8"))
    states: list[dict[str, Any]] = [{"enabled": False} for _ in range(STONE_COUNT)]
    for row in raw:
        index = int(row["index"])
        if not 0 <= index < STONE_COUNT:
            raise ValueError(f"invalid stone slot: {index}")
        states[index] = {
            "enabled": bool(row.get("enabled", True)),
            "x": float(row.get("x", 0.0)),
            "y": float(row.get("y", 0.0)),
            "yaw": float(row.get("yaw", 0.0)),
        }
    return states


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", type=Path, required=True, help="固定出手前壶面 JSON")
    parser.add_argument("--shot-index", type=int, required=True, help="固定出手的零基手号")
    parser.add_argument("--shot", type=float, nargs=3, required=True, metavar=("V", "H", "W"))
    parser.add_argument("--seed", type=int, default=20260718)
    parser.add_argument("--stop-after-shot", type=int, default=9, help="包含该手之前继续；9 表示检验到 K5 完成")
    parser.add_argument("--decision-budget-seconds", type=float, default=180.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 0 <= args.shot_index < STONE_COUNT - 1:
        raise SystemExit("--shot-index 必须留下至少一手给 PPO 回应")
    if not args.shot_index + 1 < args.stop_after_shot <= STONE_COUNT:
        raise SystemExit("--stop-after-shot 必须在固定出手之后且不超过 16")

    install_bundled_pyphysx()
    states_before = expanded_fixture(args.board)
    environment = StrictCurlingEnd(seed=int(args.seed), training_fast=True)
    environment.reset()
    environment.shot_number = int(args.shot_index)
    environment.restore_settled_states(states_before)
    result = environment.play(tuple(float(value) for value in args.shot))
    states_after = state_snapshot(result["states"])

    progress_path = args.output.with_suffix(".jsonl")
    if progress_path.exists():
        progress_path.unlink()
    proxy = ProxyMatchPlayer(physics_seeds=3, parent_regions=3, decision_budget_seconds=float(args.decision_budget_seconds))
    opponent = TeammatePPOOpponent(deterministic=True)
    try:
        continuation = run_game(
            game_index=1, proxy_team=0, seed=int(args.seed), proxy=proxy, opponent=opponent,
            opponent_label="ppo", progress_path=progress_path, initial_states=states_after,
            start_shot=int(args.shot_index) + 1, stop_after_shot=int(args.stop_after_shot),
        )
    finally:
        close = getattr(opponent, "close", None)
        if callable(close):
            close()

    report = {
        "schema": "fixed_goal_transition_vs_deterministic_ppo_v1",
        "scope": "single exact strict-PhysX G_k followed by local deterministic PPO; not a win-rate proof",
        "seed": int(args.seed),
        "manualShotIndex": int(args.shot_index),
        "manualBestshot": [float(value) for value in args.shot],
        "manualStateBefore": state_snapshot(states_before),
        "manualStateAfter": states_after,
        "manualCleared": list(result["cleared"]),
        "manualScoreFirst": score_board(result["states"]),
        "continuation": continuation,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "固定 G%d 后回放至第%d手：固定后先手分=%+d，续跑后先手分=%+d；report=%s"
        % (args.shot_index // 2 + 1, args.stop_after_shot, report["manualScoreFirst"], continuation["finalScoreFirst"], args.output)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
