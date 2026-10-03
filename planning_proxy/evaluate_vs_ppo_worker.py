#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CP39 严格 PhysX 与 CP311 PPO 推理进程的完整对局评测入口。

比赛壶面、规则、摩擦和我方路径规划都只在当前 CP39 进程执行。PPO 子进程
仅返回它原本的三元出手参数，因此不会把不同 Python 的物理模拟混在一起。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import install_bundled_pyphysx  # noqa: E402
from planning_proxy.evaluate_ideal_state_machine_vs_ppo import PPOWorker  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer, append_log, run_game  # noqa: E402


class WorkerPPOOpponent:
    """把 JSON-lines PPO 子进程适配为正式评测器需要的 choose 接口。"""

    def __init__(self, python: Path) -> None:
        self._worker = PPOWorker(python)

    def choose(
        self,
        position: Sequence[float],
        *,
        player_is_init: bool,
        shot_num: int,
        end_score: int = 0,
        total_ends: int = 1,
        current_player: int = 0,
    ) -> Any:
        result = self._worker.choose(
            position=list(float(value) for value in position),
            player_is_init=bool(player_is_init), shot_num=int(shot_num),
            end_score=int(end_score), total_ends=int(total_ends), current_player=int(current_player),
        )
        return SimpleNamespace(
            bestshot=tuple(float(value) for value in result["bestshot"]),
            tactic=str(result["tactic"]), action_id=int(result["action_id"]),
            policy_probability=float(result["policy_probability"]), value=float(result["value"]),
            fallback=bool(result["fallback"]),
        )

    def close(self) -> None:
        self._worker.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    parser.add_argument("--torch-python", type=Path, default=Path(r"D:\anaconda3\python.exe"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    progress = args.output.with_suffix(".jsonl")
    if progress.exists():
        progress.unlink()

    install_bundled_pyphysx()
    proxy = ProxyMatchPlayer(
        physics_seeds=int(args.physics_seeds), parent_regions=int(args.parent_regions),
        decision_budget_seconds=float(args.decision_budget_seconds),
    )
    opponent = WorkerPPOOpponent(args.torch_python)
    append_log(progress, {"type": "match_start", "seed": int(args.seed), "opponent": "ppo_worker"})
    try:
        game = run_game(
            game_index=1, proxy_team=0, seed=int(args.seed), proxy=proxy,
            opponent=opponent, opponent_label="ppo", progress_path=progress,
        )
    finally:
        opponent.close()
    report = {
        "schema": "planning_proxy_vs_ppo_worker_v1",
        "scope": "one complete local strict-PhysX first-player end; PPO inference isolated in CP311 worker",
        "warning": "a deterministic local integration benchmark, not a platform-wide win-rate proof",
        "opponent": "ppo", "proxyTeamScope": 0,
        "plannerPhysicsSeeds": int(args.physics_seeds), "plannerParentRegions": int(args.parent_regions),
        "decisionBudgetSeconds": float(args.decision_budget_seconds), "games": [game],
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    append_log(progress, {"type": "match_end", "report": str(args.output)})
    print("先手分=%+d | 规划方分=%+d | 胜方=%s | %.1fs" % (
        game["finalScoreFirst"], game["finalScoreProxy"], game["winner"], game["elapsedSeconds"],
    ))
    print(f"report={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
