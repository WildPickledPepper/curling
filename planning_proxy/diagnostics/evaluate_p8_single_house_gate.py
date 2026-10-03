#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线检验：P8 外环滚位合同仅适用于唯一敌方营内壶。

不修改生产状态机。工具从来源报告连续重放 K1--K7 的真实 BESTSHOT，且只在
K8 临时把分类器的 ``P8_*_TWO_OWN_OUTER_ROLL`` 门槛收紧为“敌方营内壶恰为一颗”。
其余 K8 求解器、摩擦种子、PPO 对手和 K16 结算均保持当前实现，用于同前缀因果对照。
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import install_bundled_pyphysx  # noqa: E402
import planning_proxy.evaluate_vs_teammate_ppo as evaluator  # noqa: E402
from planning_proxy.evaluate_k7_continuation_variants import WorkerPPOOpponent, source_before  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer, run_game  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--torch-python", type=Path, default=Path(r"D:\anaconda3\python.exe"))
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    return parser.parse_args()


def gated_planner_module() -> types.ModuleType:
    """在独立模块中加载唯一的一行分类门槛变化，绝不改源文件。"""

    source_path = ROOT / "planning_proxy" / "first_player_strategy.py"
    source = source_path.read_text(encoding="utf-8")
    needle = "        and own_inner == 0\n        and own_live == 2\n        and (\n"
    replacement = "        and own_inner == 0\n        and own_live == 2\n        and opponent_house == 1\n        and (\n"
    if source.count(needle) != 1:
        raise RuntimeError("找不到唯一的 P8 外环滚位分类门槛，拒绝运行不确定的离线对照。")
    module = types.ModuleType("_offline_p8_single_house_gate")
    module.__file__ = str(source_path)
    sys.modules[module.__name__] = module
    exec(compile(source.replace(needle, replacement), str(source_path), "exec"), module.__dict__)
    return module


class SingleHouseGatePlayer(ProxyMatchPlayer):
    """仅在第 15 手临时替换分类函数；其余正式求解路径原样调用。"""

    def __init__(self, *, gated_module: types.ModuleType, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._gated_module = gated_module

    def choose(
        self, states: Sequence[dict[str, Any]], *, proxy_team: int, shot_index: int, match_seed: int,
    ):
        if int(proxy_team) != 0 or int(shot_index) != 14:
            return super().choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        original = evaluator.plan_first_player_turn

        def temporary_plan(board: Any, current_shot: int):
            if int(current_shot) == 14:
                return self._gated_module.plan_first_player_turn(board, current_shot)
            return original(board, current_shot)

        evaluator.plan_first_player_turn = temporary_plan
        try:
            return super().choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        finally:
            evaluator.plan_first_player_turn = original


def main() -> int:
    args = parse_args()
    source_path = args.source_report.resolve()
    report, source_game, expected_states, prefix = source_before(source_path, 14)
    install_bundled_pyphysx()
    gated = gated_planner_module()
    proxy = SingleHouseGatePlayer(
        gated_module=gated,
        physics_seeds=int(args.physics_seeds),
        parent_regions=int(args.parent_regions),
        decision_budget_seconds=float(args.decision_budget_seconds),
    )
    opponent = WorkerPPOOpponent(args.torch_python)
    try:
        game = run_game(
            game_index=1,
            proxy_team=0,
            seed=int(source_game["seed"]),
            proxy=proxy,
            opponent=opponent,
            opponent_label="ppo",
            progress_path=args.output.with_suffix(".jsonl"),
            start_shot=14,
            prefix_trace=prefix,
            expected_start_states=expected_states,
        )
    finally:
        opponent.close()
    k8 = next(item for item in game["trace"] if int(item.get("shot", -1)) == 15)
    payload = {
        "schema": "offline_p8_single_enemy_house_gate_continuation_v1",
        "scope": (
            "same strict physical prefix; only K8 classifier gate changes from outer-roll to requiring exactly one "
            "opponent house stone. Diagnostic only; not production policy."
        ),
        "sourceReport": str(source_path),
        "sourceSeed": int(source_game["seed"]),
        "sourceK8Plan": next(item for item in (source_game.get("trace") or []) if int(item.get("shot", -1)) == 15).get("detail", {}).get("firstPlayerPlan"),
        "variantK8Plan": k8.get("detail", {}).get("firstPlayerPlan"),
        "game": game,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "k8Mode": k8.get("detail", {}).get("mode"),
        "k8Plan": k8.get("detail", {}).get("firstPlayerPlan", {}).get("situation_type"),
        "k8Seconds": k8.get("decisionSeconds"),
        "finalScoreProxy": game.get("finalScoreProxy"),
        "winner": game.get("winner"),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
