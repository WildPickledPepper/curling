"""Optional first-player runtime adapter: semantic MDP first, legacy planner fallback.

This module intentionally does not alter ``first_player_strategy.py`` or the
baseline ``ProxyMatchPlayer``.  It is used only by the local evaluation flag
so PPO comparisons can report exactly which shots were certified by the new
data-derived semantic contracts and which fell back to the existing planner.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

from planning_proxy.competition_rules import FRONT_HOG_Y, HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R
from planning_proxy.first_player_strategy import GUARD_TARGET, OPENING_CENTRE_GUARD_SHOT

from .contextual_fine_retriever import ContextualFineRetriever, contextual_regions_as_fine_options, load_default as load_retriever
from .semantic_contract_physx_bridge import (
    solve_semantic_double_removal_contracts, solve_semantic_placement_contracts_parallel,
    solve_semantic_mixed_collision_contracts_parallel,
    solve_semantic_single_removal_contracts_parallel,
)
from .semantic_goal_contract import instantiate_goal_contracts
from training_data.nwnht_curling.causal_state_machine.runtime_semantic_goal_mdp_v1 import RuntimeSemanticGoalMdp, load_default as load_mdp


def load_local_k2_anchor_plans() -> dict[str, dict[str, Any]]:
    """Load the rule-conditioned K2 plans following a K1 centre anchor."""

    root = Path(__file__).resolve().parents[2] / "training_data" / "nwnht_curling" / "causal_state_machine" / "artifacts"
    artifact = json.loads((root / "nwnht_local_k1_anchor_k2_goals_v5.json").read_text(encoding="utf-8"))
    return {str(row["state_id"]): dict(row) for row in artifact["state_plans"]}


class SemanticTacticalMatchPlayer:
    """First-side semantic contracts with an unchanged baseline fallback."""

    def __init__(
        self, fallback: Any, *, contract_budget_seconds: float = 10.0,
        max_workers: int = 3, max_contracts: int = 3, mdp: RuntimeSemanticGoalMdp | None = None,
        retriever: ContextualFineRetriever | None = None, local_k2_plans: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> None:
        self.fallback = fallback
        # ``run_game`` records this public budget for every planner-like
        # object.  Semantic search is additional diagnostic work; a failed
        # contract still delegates to the baseline's unchanged per-shot budget.
        self.decision_budget_seconds = float(fallback.decision_budget_seconds)
        self.physics_seeds = int(fallback.physics_seeds)
        self.contract_budget_seconds = float(contract_budget_seconds)
        self.max_workers = int(max_workers)
        self.max_contracts = int(max_contracts)
        self.mdp = mdp or load_mdp()
        self.retriever = retriever or load_retriever()
        self.local_k2_plans = {str(key): dict(value) for key, value in (local_k2_plans or load_local_k2_anchor_plans()).items()}

    @staticmethod
    def _canonical_board(states: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "index": index, "owner": "first" if index % 2 == 0 else "opponent",
                "x_m": float(state["x"]) - HOUSE_X, "y_m": float(state["y"]) - HOUSE_Y,
                "yaw": float(state.get("yaw", 0.0)),
            }
            for index, state in enumerate(states) if bool(state.get("enabled", False))
        ]

    @staticmethod
    def _is_centre_fgz_guard(stone: Mapping[str, Any]) -> bool:
        return (
            str(stone["owner"]) == "first"
            and 0.0 <= float(stone["y_m"]) <= FRONT_HOG_Y - HOUSE_Y
            and math.hypot(float(stone["x_m"]), float(stone["y_m"])) > HOUSE_R + STONE_R
            and abs(float(stone["x_m"])) <= STONE_R
        )

    @staticmethod
    def _is_in_house(stone: Mapping[str, Any]) -> bool:
        """Return whether a stone centre is inside the scoring house.

        This is deliberately a coarse *role* test, rather than an exact
        historical-board comparison.  The late-game decision still receives
        the full physical state from the fallback planner.
        """

        return math.hypot(float(stone["x_m"]), float(stone["y_m"])) <= HOUSE_R

    @classmethod
    def _local_k2_state(cls, board: Sequence[Mapping[str, Any]]) -> str | None:
        """Classify only the local-rule-conditioned K1-centre-anchor states."""

        if not any(cls._is_centre_fgz_guard(stone) for stone in board):
            return None
        opponents = [stone for stone in board if str(stone["owner"]) == "opponent"]
        if not opponents:
            return "S2_LOCAL_ANCHOR_ONLY"
        if any(math.hypot(float(stone["x_m"]), float(stone["y_m"])) <= HOUSE_R + STONE_R for stone in opponents):
            return "S2_LOCAL_ANCHOR_OPPONENT_HOUSE"
        if any(0.0 <= float(stone["y_m"]) <= FRONT_HOG_Y - HOUSE_Y and math.hypot(float(stone["x_m"]), float(stone["y_m"])) > HOUSE_R + STONE_R and abs(float(stone["x_m"])) <= STONE_R for stone in opponents):
            return "S2_LOCAL_ANCHOR_OPPONENT_CENTRE_GUARD"
        if any(0.0 <= float(stone["y_m"]) <= FRONT_HOG_Y - HOUSE_Y and math.hypot(float(stone["x_m"]), float(stone["y_m"])) > HOUSE_R + STONE_R for stone in opponents):
            return "S2_LOCAL_ANCHOR_OPPONENT_SIDE_GUARD"
        return "S2_LOCAL_ANCHOR_OPPONENT_OTHER_IN_PLAY"

    def choose(self, states: Sequence[dict[str, Any]], *, proxy_team: int, shot_index: int, match_seed: int):
        # The learned state machine is explicitly first-side only.  Preserve
        # the legacy behaviour when the evaluation swaps the proxy to second.
        if int(proxy_team) != 0 or int(shot_index) % 2:
            return self.fallback.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        k = int(shot_index) // 2 + 1
        board = self._canonical_board(states)
        # K1 空场不是要由历史平均值自由选择的分叉。当前本地规则下，经过
        # 严格 PhysX 空场标定的中线守壶能保留自由防守区压力；直接使用这组
        # 出手参数，不让“营内占位”这个历史关联更高的 G1 抢占首手。
        if k == 1 and not board:
            return OPENING_CENTRE_GUARD_SHOT, {
                "mode": "semantic_tactical_library_fixed_opening_centre_guard",
                "semanticMdp": {
                    "state_id": "K1_V2_EMPTY_1",
                    "goal_id": "LOCAL_RULE_FIXED_CENTRE_GUARD",
                    "K": 1,
                    "route": "DIRECT_CALIBRATED_OPENING_GUARD",
                },
                "target": list(GUARD_TARGET),
                "strictCalibration": {
                    "physicsSeeds": list(range(9)),
                    "maxLandingErrorM": 0.05174,
                    "meanLandingErrorM": 0.02854,
                },
            }
        # K6 是历史候选与残局防御交界。复盘显示：若当前已在营内有两颗己方
        # 壶，再照历史落区追加一颗，容易把它们排为一次双清的目标；这不是
        # 对某个 PPO 动作的预测，而是当前盘面的通用“营内堆叠”风险。此类
        # 局面交回完整壶面的主状态机，让它清威胁或补门。营内至多一颗时，
        # K6 的历史低位锚仍可作为严格 PhysX 认证的候选。
        own_in_house = sum(
            1 for stone in board
            if str(stone["owner"]) == "first" and self._is_in_house(stone)
        )
        own_stones = [stone for stone in board if str(stone["owner"]) == "first"]
        opponent_house_stones = [
            stone for stone in board
            if str(stone["owner"]) == "opponent" and self._is_in_house(stone)
        ]
        opponent_house_count = len(opponent_house_stones)
        k6_single_guard_outdraw_state = (
            k == 6
            and own_in_house == 0
            and len(own_stones) == 1
            and self._is_centre_fgz_guard(own_stones[0])
            and opponent_house_count == 1
            # 接近按钮中线的敌壶可在下一手被直接压入/撞向按钮，不能把
            # “绕开它占按钮”误当作同一种安全状态。只有明显侧向的威胁
            # 才走 outdraw；阈值按大本营半径表达，而非某局绝对坐标。
            and abs(float(opponent_house_stones[0]["x_m"])) >= HOUSE_R * 0.35
        )
        if k >= 7 or (k == 6 and own_in_house >= 2) or k6_single_guard_outdraw_state:
            shot, detail = self.fallback.choose(
                states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed,
            )
            return shot, {
                **detail,
                "semanticMdp": {
                    "status": "DEFER_TO_LATE_GAME_STATE_MACHINE",
                    "K": k,
                    "reason": (
                        "late_defence_requires_current_board_gate_and_reply_pressure_roles"
                        if k >= 7 else "k6_own_house_cluster_requires_current_board_clear_or_repair"
                        if own_in_house >= 2 else "k6_single_centre_guard_vs_house_threat_requires_outdraw_gate"
                    ),
                    "ownInHouse": int(own_in_house),
                },
            }
        local_state = self._local_k2_state(board) if k == 2 else None
        local_plan = self.local_k2_plans.get(str(local_state)) if local_state is not None else None
        if isinstance(local_plan, Mapping) and local_plan.get("recommendation_status") == "CONDITIONAL_G2_AVAILABLE":
            recommendation = {"state_id": str(local_state), "K": 2, "primary_goal": local_plan.get("primary_goal")}
            local_conditional = True
        else:
            recommendation = self.mdp.recommend(k, board)
            local_conditional = False
        primary = recommendation.get("primary_goal")
        if not isinstance(primary, Mapping):
            shot, detail = self.fallback.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
            return shot, {**detail, "semanticMdp": {"status": "NO_SEMANTIC_GOAL", "state_id": recommendation.get("state_id")}}
        retrieval = (
            {"state_id": recommendation["state_id"], "K": k, "goal_id": primary["goal_id"],
             "retrieval_status": "LOCAL_RULE_CONDITIONED_FINE_OPTIONS", "regions": [],
             "warning": "Use the rule-conditioned G2 artifact's own fine circles; no global exemplar override."}
            if local_conditional else self.retriever.retrieve(board, primary)
        )
        envelope = instantiate_goal_contracts(
            board, primary,
            fine_options_override=None if local_conditional else contextual_regions_as_fine_options(retrieval),
        )
        contracts = envelope["contracts"][:self.max_contracts]
        effect = primary["goal_state"]["semantic_effect"]
        removed = int(effect["opponent_removed_count"])
        if removed == 0:
            attempts = solve_semantic_placement_contracts_parallel(
                board, contracts, own_throw_number=k, physics_seeds=int(self.fallback.physics_seeds),
                match_seed=int(match_seed), decision_budget_seconds=self.contract_budget_seconds, max_workers=self.max_workers,
            )
            route = "PLACEMENT_PARALLEL_NEWTON_MADS_WITH_K8_REPLY_SCREEN" if k == 8 else "PLACEMENT_PARALLEL_NEWTON_MADS"
        elif removed == 1:
            attempts = solve_semantic_single_removal_contracts_parallel(
                board, contracts, own_throw_number=k, physics_seeds=int(self.fallback.physics_seeds),
                match_seed=int(match_seed), decision_budget_seconds=self.contract_budget_seconds, max_workers=self.max_workers,
            )
            route = "SINGLE_REMOVAL_PARALLEL_MADS_WITH_K8_REPLY_SCREEN" if k == 8 else "SINGLE_REMOVAL_PARALLEL_MADS"
        elif removed == 2:
            attempts = solve_semantic_double_removal_contracts(
                board, contracts, own_throw_number=k, physics_seeds=int(self.fallback.physics_seeds),
                match_seed=int(match_seed), decision_budget_seconds=self.contract_budget_seconds,
            )
            route = "DOUBLE_REMOVAL_MADS_WITH_K8_REPLY_SCREEN" if k == 8 else "DOUBLE_REMOVAL_MADS"
        else:
            attempts = solve_semantic_mixed_collision_contracts_parallel(
                board, contracts, own_throw_number=k, physics_seeds=int(self.fallback.physics_seeds),
                match_seed=int(match_seed), decision_budget_seconds=self.contract_budget_seconds, max_workers=self.max_workers,
            )
            route = "MIXED_COLLISION_MADS_WITH_K8_REPLY_SCREEN" if k == 8 else "MIXED_COLLISION_MADS"
        certified = next((attempt for attempt in attempts if attempt.status == "CERTIFIED_SEMANTIC_CONTRACT"), None)
        if certified is not None and certified.bestshot is not None:
            return certified.bestshot, {
                "mode": "semantic_tactical_library_certified",
                "semanticMdp": {"state_id": recommendation["state_id"], "goal_id": primary["goal_id"], "K": k, "route": route, "localRuleConditioned": local_conditional},
                "retrieval": retrieval, "contractEnvelopeStatus": envelope["contract_status"],
                "attempts": [attempt.to_json() for attempt in attempts],
            }
        shot, detail = self.fallback.choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        return shot, {
            **detail,
            "semanticMdp": {"state_id": recommendation["state_id"], "goal_id": primary["goal_id"], "K": k, "route": route, "status": "FALLBACK_NO_CERTIFIED_SEMANTIC_CONTRACT", "localRuleConditioned": local_conditional},
            "retrieval": retrieval, "contractEnvelopeStatus": envelope["contract_status"],
            "attempts": [attempt.to_json() for attempt in attempts],
        }
