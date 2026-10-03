#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在固定 K8 壶面上，用本地对手筛选小范围的严格 PhysX 动作网格。

这是末壶局部诊断工具：每个候选先严格执行先手 K8，再让确定性本地对手执行 K16，
按多个完整物理种子的最差最终分排序。它不搜索连续空间、不替代状态机，也不把
一个种子的胜利解释为稳定胜率。
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd, install_bundled_pyphysx, score_board
from planning_proxy.evaluate_ideal_state_machine_vs_ppo import PPOWorker
from planning_proxy.evaluate_vs_teammate_ppo import state_position
from planning_proxy.replay_fixed_transition_vs_ppo import expanded_fixture


def _settled_rows(states: Sequence[dict[str, Any]]) -> list[dict[str, float | int]]:
    return [
        {
            "index": index,
            "x": float(state["x"]),
            "y": float(state["y"]),
            "yaw": float(state.get("yaw", 0.0)),
        }
        for index, state in enumerate(states)
        if bool(state.get("enabled", False))
    ]


def board_from_report(path: Path, shot: int) -> list[dict[str, Any]]:
    """读取真实完整续局保存的 K8 出手前壶面，避免手工 fixture 与来源错配。"""

    report = json.loads(path.read_text(encoding="utf-8"))
    game = report.get("game")
    if not isinstance(game, dict):
        games = report.get("games")
        game = games[0] if isinstance(games, list) and games and isinstance(games[0], dict) else None
    trace = game.get("trace") if isinstance(game, dict) else None
    if not isinstance(trace, list):
        raise SystemExit(f"{path} 不含 game.trace")
    row = next((item for item in trace if isinstance(item, dict) and int(item.get("shot", -1)) == int(shot)), None)
    states = row.get("stateBefore") if isinstance(row, dict) else None
    if not isinstance(states, list) or len(states) < 16:
        raise SystemExit(f"{path} 第 {shot} 手缺少完整 stateBefore")
    return states


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    board_source = parser.add_mutually_exclusive_group(required=True)
    board_source.add_argument("--board", type=Path, help="K8 出手前稀疏 fixture")
    board_source.add_argument("--source-report", type=Path, help="含真实 K8 stateBefore 的完整续局报告")
    parser.add_argument("--source-shot", type=int, default=15, help="仅 --source-report：读取该手的 stateBefore")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shot-index", type=int, default=14)
    parser.add_argument("--seeds", nargs="+", type=int, default=(20260718, 20260719, 20260720))
    parser.add_argument("--v-values", nargs="+", type=float, default=(5.45, 5.60, 5.75))
    parser.add_argument("--h-values", nargs="+", type=float, default=(-1.60, -1.43, -1.26))
    parser.add_argument("--w-values", nargs="+", type=float, default=(8.50, 10.00, 11.50))
    parser.add_argument(
        "--torch-python", type=Path, default=Path(r"D:\anaconda3\python.exe"),
        help="带 PyTorch 的 PPO 子进程解释器；严格 PhysX 仍留在当前 CP39 进程。",
    )
    parser.add_argument(
        "--opponent", choices=("ppo", "aggressive"), default="ppo",
        help="仅用于 K16 反击验证；不影响 K8 候选网格或生产状态机。",
    )
    parser.add_argument(
        "--candidates-from-report", type=Path, default=None,
        help="复核先前报告中标为 all_seeds_nonloss 的候选；保留原动作三元组，不做笛卡尔积。",
    )
    args = parser.parse_args()
    if int(args.shot_index) != 14:
        raise SystemExit("此工具只用于先手 K8（--shot-index 14）后接本地对手 K16。")

    if args.board is not None:
        board = expanded_fixture(args.board)
        input_board: dict[str, Any] = {"kind": "fixture", "path": str(args.board)}
    else:
        board = board_from_report(args.source_report, int(args.source_shot))
        input_board = {"kind": "real_report_state_before", "path": str(args.source_report), "shot": int(args.source_shot)}
    if args.candidates_from_report is None:
        shots = list(itertools.product(args.v_values, args.h_values, args.w_values))
    else:
        source = json.loads(args.candidates_from_report.read_text(encoding="utf-8"))
        shots = [
            tuple(float(value) for value in row["bestshot"])
            for row in source["ranked_candidates"]
            if bool(row.get("all_seeds_nonloss", False))
        ]
        if not shots:
            raise SystemExit("--candidates-from-report 中没有 all_seeds_nonloss 候选。")
    install_bundled_pyphysx()
    # CP39 严格 PhysX 解释器不安装 Torch；PPO 始终在独立子进程中推理，
    # 这样不尝试跨 ABI 加载原生扩展。激进对手复用交付策略库的本地适配器。
    if args.opponent == "ppo":
        opponent: Any = PPOWorker(args.torch_python)
        opponent_label = "ppo"
    else:
        from training_research.opponents.aggressive_strategy_adapter import AggressiveStrategyOpponent

        opponent = AggressiveStrategyOpponent()
        opponent_label = "aggressive"
    rows: list[dict[str, Any]] = []
    try:
        for shot in shots:
            seed_rows: list[dict[str, Any]] = []
            for seed in args.seeds:
                environment = StrictCurlingEnd(seed=int(seed), training_fast=True)
                environment.reset()
                environment.shot_number = int(args.shot_index)
                states = environment.restore_settled_states(board)
                own = environment.play(tuple(float(value) for value in shot))
                own_states = own["states"]
                own_score = int(score_board(own_states))
                reply = opponent.choose(
                    position=state_position(own_states), player_is_init=False, shot_num=15,
                    end_score=own_score, total_ends=1, current_player=1,
                )
                reply_shot = reply["bestshot"] if isinstance(reply, dict) else reply.bestshot
                reply_tactic = reply["tactic"] if isinstance(reply, dict) else reply.tactic
                opponent_result = environment.play(tuple(float(value) for value in reply_shot))
                seed_rows.append({
                    "seed": int(seed),
                    "score_after_k8": own_score,
                    "score_after_k16": int(score_board(opponent_result["states"])),
                    "k8_cleared": [int(index) for index in own["cleared"]],
                    "k8_final_board": _settled_rows(own_states),
                    "opponent_tactic": str(reply_tactic),
                    "opponent_bestshot": [float(value) for value in reply_shot],
                    "k16_cleared": [int(index) for index in opponent_result["cleared"]],
                })
            final_scores = [int(row["score_after_k16"]) for row in seed_rows]
            rows.append({
                "bestshot": [float(value) for value in shot],
                "worst_final_score": min(final_scores),
                "mean_final_score": sum(final_scores) / len(final_scores),
                "all_seeds_nonloss": all(score >= 0 for score in final_scores),
                "seeds": seed_rows,
            })
    finally:
        close = getattr(opponent, "close", None)
        if callable(close):
            close()

    rows.sort(key=lambda row: (int(row["worst_final_score"]), float(row["mean_final_score"])), reverse=True)
    report = {
        "schema": "k8_local_grid_vs_deterministic_opponent_v2",
        "scope": (
            "fixed K8 board, finite local action grid, strict PhysX then deterministic local K16 opponent; "
            "not continuous-search or match-win proof"
        ),
        "opponent": opponent_label,
        "board": input_board,
        "seeds": [int(seed) for seed in args.seeds],
        "grid": {"v": list(args.v_values), "h": list(args.h_values), "w": list(args.w_values)},
        "candidatesFromReport": None if args.candidates_from_report is None else str(args.candidates_from_report),
        "candidate_count": len(rows),
        "all_seeds_nonloss_count": sum(bool(row["all_seeds_nonloss"]) for row in rows),
        "ranked_candidates": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows[:10]:
        print(json.dumps({
            "bestshot": row["bestshot"], "worst_final_score": row["worst_final_score"],
            "mean_final_score": row["mean_final_score"], "all_seeds_nonloss": row["all_seeds_nonloss"],
        }, ensure_ascii=False))
    print("all_seeds_nonloss_count=%d/%d" % (report["all_seeds_nonloss_count"], len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
