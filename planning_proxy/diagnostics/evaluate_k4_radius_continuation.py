"""从真实 K1--K3 前缀回放 K4 半径合同的离线完整续局对照。

只在指定 K4 语义状态临时替换落区半径；选择器仍自行严格搜索，随后和同一
对手完成至 K8。该脚本不修改生产状态机、原生扩展或默认运行时。
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


TARGET_SITUATION = "P4_SINGLE_INNER_ANCHOR_OPPONENT_SIDE_GUARD"
TARGET_PHASE = "clear_side_guard_and_hold_outer_roll"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--radius", type=float, required=True)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--torch-python", type=Path, default=Path(r"D:\anaconda3\python.exe"))
    parser.add_argument("--extension", type=Path, help="仅本进程临时加载候选 CP39 扩展。")
    return parser.parse_args()


class RadiusVariantPlayer:
    """将一个精确状态语义的 K4 合同半径临时替换，再委托正式选择器。"""

    def __init__(self, base: Any, *, radius: float) -> None:
        self._base = base
        self.radius = float(radius)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)

    def choose(
        self,
        states: Sequence[dict[str, Any]],
        *,
        proxy_team: int,
        shot_index: int,
        match_seed: int,
    ) -> tuple[tuple[float, float, float], dict[str, Any]]:
        import planning_proxy.evaluate_vs_teammate_ppo as evaluator

        if int(proxy_team) != 0 or int(shot_index) != 6:
            return self._base.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        original = evaluator.plan_first_player_turn

        def radius_variant(board: Any, current_shot: int) -> Any:
            plan = original(board, current_shot)
            if (
                int(current_shot) != 6
                or plan is None
                or str(plan.situation_type) != TARGET_SITUATION
                or str(plan.phase) != TARGET_PHASE
            ):
                return plan
            return replace(
                plan,
                landing_region_radius_m=self.radius,
                defence_shapes=tuple(
                    replace(shape, landing_region_radius_m=self.radius)
                    for shape in plan.defence_shapes
                ),
                rationale=f"{plan.rationale}；离线 K4 半径因果对照={self.radius:.6f}m。",
            )

        evaluator.plan_first_player_turn = radius_variant
        try:
            return self._base.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        finally:
            evaluator.plan_first_player_turn = original


def main() -> None:
    args = parse_args()
    if args.radius <= 0.0:
        raise SystemExit("--radius 必须为正数")
    from local_simulator import runtime_loader
    if args.extension is not None:
        extension = args.extension.resolve()
        if not extension.is_file():
            raise SystemExit(f"候选原生扩展不存在：{extension}")
        runtime_loader.BUNDLED_EXTENSION = extension
    runtime_loader.install_bundled_pyphysx()
    import planning_proxy.evaluate_vs_teammate_ppo as evaluator
    from planning_proxy.evaluate_k7_continuation_variants import WorkerPPOOpponent, source_before

    report, game, expected_start_states, prefix = source_before(args.source_report, 6)
    seed = int(game["seed"])
    base = evaluator.ProxyMatchPlayer(
        physics_seeds=int(args.physics_seeds),
        parent_regions=3,
        decision_budget_seconds=float(args.decision_budget_seconds),
    )
    proxy = RadiusVariantPlayer(base, radius=float(args.radius))
    opponent = WorkerPPOOpponent(args.torch_python)
    progress = args.output.with_suffix(".jsonl")
    try:
        outcome = evaluator.run_game(
            game_index=1,
            proxy_team=0,
            seed=seed,
            proxy=proxy,
            opponent=opponent,
            opponent_label="ppo",
            progress_path=progress,
            start_shot=6,
            prefix_trace=prefix,
            expected_start_states=expected_start_states,
        )
    finally:
        close = getattr(opponent, "close", None)
        if callable(close):
            close()
    k4 = next((row for row in outcome["trace"] if int(row.get("shot", 0)) == 7), None)
    plan = (k4 or {}).get("detail", {}).get("firstPlayerPlan", {})
    if not (
        isinstance(k4, dict)
        and str(plan.get("situation_type")) == TARGET_SITUATION
        and str(plan.get("phase")) == TARGET_PHASE
        and abs(float(plan.get("landing_region_radius_m")) - float(args.radius)) <= 1.0e-12
    ):
        raise RuntimeError("K4 半径候选没有实际进入指定状态合同，拒绝输出不可比较结果")
    payload = {
        "schema": "k4_radius_contract_continuation_v1",
        "scope": "同一严格物理前缀，仅替换 K4 指定状态合同半径；完整续局至终局；仅离线。",
        "sourceReport": str(args.source_report),
        "sourceSeed": seed,
        "radiusM": float(args.radius),
        "physicsSeeds": int(args.physics_seeds),
        "extension": str(getattr(runtime_loader.install_bundled_pyphysx(), "__file__", "")),
        "k4": k4,
        "game": outcome,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "k4Mode": k4.get("detail", {}).get("mode") if isinstance(k4, dict) else None,
        "k4DecisionSeconds": k4.get("decisionSeconds") if isinstance(k4, dict) else None,
        "finalScoreProxy": outcome.get("finalScoreProxy"),
        "winner": outcome.get("winner"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
