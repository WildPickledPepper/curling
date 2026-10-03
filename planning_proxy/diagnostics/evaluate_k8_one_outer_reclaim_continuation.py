#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线检验 K8“一颗外场己壶 + 一颗敌方营内壶”的第一锚合同。

只在 K8 精确状态 ``P8_ENEMY_THREAT_ONE_OWN``、己方营内为零、敌方营内恰一壶时，
把原“清壶后补完整防御形”临时换成“清壶后建立第一颗最近营内锚”。
完整前缀、严格 PhysX、求解器、物理种子和 PPO K16 均维持当前实现；不修改生产状态机。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import install_bundled_pyphysx  # noqa: E402
from planning_proxy.first_player_strategy import HOUSE_PAIR_LEFT, HOUSE_PAIR_RIGHT, is_in_house  # noqa: E402


TARGET_SITUATION = "P8_ENEMY_THREAT_ONE_OWN"
TARGET_PHASE = "clear_then_choose_defence_shape"
VARIANT_PHASE = "clear_then_reclaim_first_inner_anchor"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--torch-python", type=Path, default=Path(r"D:\anaconda3\python.exe"))
    return parser.parse_args()


def one_outer_one_house(board: Sequence[Any]) -> bool:
    own = [stone for stone in board if getattr(stone, "owner", "") == "self"]
    enemy = [stone for stone in board if getattr(stone, "owner", "") == "opponent"]
    return (
        len(own) == 1
        and len(enemy) >= 1
        and sum(is_in_house(stone) for stone in own) == 0
        and sum(is_in_house(stone) for stone in enemy) == 1
    )


class OneOuterReclaimPlayer:
    """仅将满足精确结构门槛的 K8 合同交给原选择器重新严格求解。"""

    def __init__(self, base: Any) -> None:
        self._base = base

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)

    def choose(
        self, states: Sequence[dict[str, Any]], *, proxy_team: int, shot_index: int, match_seed: int,
    ) -> tuple[tuple[float, float, float], dict[str, Any]]:
        import planning_proxy.evaluate_vs_teammate_ppo as evaluator

        if int(proxy_team) != 0 or int(shot_index) != 14:
            return self._base.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        original = evaluator.plan_first_player_turn

        def reclaim_variant(board: Any, current_shot: int) -> Any:
            plan = original(board, current_shot)
            if not (
                int(current_shot) == 14
                and str(getattr(plan, "situation_type", "")) == TARGET_SITUATION
                and str(getattr(plan, "phase", "")) == TARGET_PHASE
                and one_outer_one_house(board)
            ):
                return plan
            target = next((stone for stone in board if int(stone.index) == int(plan.target_opponent_index)), None)
            pair = HOUSE_PAIR_LEFT if target is None or float(target.x) >= 2.375 else HOUSE_PAIR_RIGHT
            return replace(
                plan,
                phase=VARIANT_PHASE,
                strategy_type="CLEAR_THREAT_AND_RECLAIM_FIRST_ANCHOR",
                desired_state_type="P8_FIRST_INNER_ANCHOR_RECLAIMED_FROM_ONE_OUTER",
                target_points=pair,
                defence_shapes=(),
                landing_region_radius_m=0.35,
                max_own_cleared=0,
                rationale=(
                    "离线 K8 合同对照：已有唯一己壶不在营内，不能要求保留不存在的内圈锚；"
                    "清当前唯一营内威胁后，先建立一颗最近营内锚。"
                ),
            )

        evaluator.plan_first_player_turn = reclaim_variant
        try:
            return self._base.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        finally:
            evaluator.plan_first_player_turn = original


def main() -> int:
    args = parse_args()
    import planning_proxy.evaluate_vs_teammate_ppo as evaluator
    from planning_proxy.evaluate_k7_continuation_variants import WorkerPPOOpponent, source_before

    source_path = args.source_report.resolve()
    _, source_game, expected_states, prefix = source_before(source_path, 14)
    install_bundled_pyphysx()
    base = evaluator.ProxyMatchPlayer(
        physics_seeds=int(args.physics_seeds),
        parent_regions=int(args.parent_regions),
        decision_budget_seconds=float(args.decision_budget_seconds),
    )
    proxy = OneOuterReclaimPlayer(base)
    opponent = WorkerPPOOpponent(args.torch_python)
    try:
        game = evaluator.run_game(
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
    plan = k8.get("detail", {}).get("firstPlayerPlan", {})
    if str(plan.get("phase")) != VARIANT_PHASE:
        raise RuntimeError("来源未实际进入一外壶一威胁合同，拒绝把不可比较结果写入报告。")
    payload = {
        "schema": "offline_k8_one_outer_reclaim_first_anchor_continuation_v1",
        "scope": "同一严格物理前缀；仅替换精确 K8 合同；完整续局至 K16；仅离线。",
        "sourceReport": str(source_path),
        "sourceSeed": int(source_game["seed"]),
        "variantK8Plan": plan,
        "game": game,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "k8Mode": k8.get("detail", {}).get("mode"),
        "k8Action": k8.get("bestshot"),
        "k8Seconds": k8.get("decisionSeconds"),
        "finalScoreProxy": game.get("finalScoreProxy"),
        "winner": game.get("winner"),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
