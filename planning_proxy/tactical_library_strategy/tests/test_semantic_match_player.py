import unittest

from planning_proxy.first_player_strategy import GUARD_TARGET, OPENING_CENTRE_GUARD_SHOT
from planning_proxy.tactical_library_strategy.semantic_match_player import SemanticTacticalMatchPlayer


class SemanticMatchPlayerTests(unittest.TestCase):
    class _Fallback:
        def choose(self, states, *, proxy_team, shot_index, match_seed):
            return (3.0, 0.0, 0.0), {"mode": "baseline_late_state_machine"}

    def test_k1_empty_is_always_the_calibrated_centre_guard(self):
        # K1 直接返回，故无需加载数据 MDP、检索器或 PhysX 资产。
        player = SemanticTacticalMatchPlayer.__new__(SemanticTacticalMatchPlayer)
        shot, detail = player.choose([], proxy_team=0, shot_index=0, match_seed=20260718)

        self.assertEqual(shot, OPENING_CENTRE_GUARD_SHOT)
        self.assertEqual(detail["mode"], "semantic_tactical_library_fixed_opening_centre_guard")
        self.assertEqual(detail["semanticMdp"]["goal_id"], "LOCAL_RULE_FIXED_CENTRE_GUARD")
        self.assertEqual(detail["target"], list(GUARD_TARGET))

    def test_k2_local_anchor_only_has_its_own_state(self):
        state = SemanticTacticalMatchPlayer._local_k2_state([
            {"owner": "first", "x_m": 0.0, "y_m": 2.27},
        ])
        self.assertEqual(state, "S2_LOCAL_ANCHOR_ONLY")

    def test_k2_without_a_centre_anchor_does_not_use_local_conditioned_state(self):
        state = SemanticTacticalMatchPlayer._local_k2_state([
            {"owner": "first", "x_m": 0.4, "y_m": 2.27},
        ])
        self.assertIsNone(state)

    def test_k7_and_k8_defer_to_the_current_board_late_state_machine(self):
        player = SemanticTacticalMatchPlayer.__new__(SemanticTacticalMatchPlayer)
        player.fallback = self._Fallback()
        for shot_index in (12, 14):
            shot, detail = player.choose([], proxy_team=0, shot_index=shot_index, match_seed=20260718)
            self.assertEqual(shot, (3.0, 0.0, 0.0))
            self.assertEqual(detail["mode"], "baseline_late_state_machine")
            self.assertEqual(detail["semanticMdp"]["status"], "DEFER_TO_LATE_GAME_STATE_MACHINE")

    def test_k6_two_own_house_stones_defer_to_current_board_state_machine(self):
        player = SemanticTacticalMatchPlayer.__new__(SemanticTacticalMatchPlayer)
        player.fallback = self._Fallback()
        states = [
            {"enabled": True, "x": 2.32, "y": 5.02},
            {"enabled": False, "x": 0.0, "y": 0.0},
            {"enabled": True, "x": 1.92, "y": 4.97},
        ]
        shot, detail = player.choose(states, proxy_team=0, shot_index=10, match_seed=20260718)
        self.assertEqual(shot, (3.0, 0.0, 0.0))
        self.assertEqual(detail["mode"], "baseline_late_state_machine")
        self.assertEqual(detail["semanticMdp"]["reason"], "k6_own_house_cluster_requires_current_board_clear_or_repair")
        self.assertEqual(detail["semanticMdp"]["ownInHouse"], 2)

    def test_k6_single_centre_guard_vs_one_house_threat_defers_to_outdraw_gate(self):
        player = SemanticTacticalMatchPlayer.__new__(SemanticTacticalMatchPlayer)
        player.fallback = self._Fallback()
        states = [
            {"enabled": True, "x": 2.375, "y": 7.13},
            {"enabled": True, "x": 3.22, "y": 5.94},
        ]
        shot, detail = player.choose(states, proxy_team=0, shot_index=10, match_seed=20260718)
        self.assertEqual(shot, (3.0, 0.0, 0.0))
        self.assertEqual(detail["semanticMdp"]["reason"], "k6_single_centre_guard_vs_house_threat_requires_outdraw_gate")
        self.assertEqual(detail["semanticMdp"]["ownInHouse"], 0)
