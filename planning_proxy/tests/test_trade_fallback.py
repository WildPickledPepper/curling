import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.strict_refine import (  # noqa: E402
    Candidate, StrictEvaluation, is_full_preserve_candidate, is_last_hammer_target_beaten, is_loss_budget_candidate,
    selection_priority,
)


def item(enemy, own, active=False, legal=True):
    return StrictEvaluation(
        candidate=Candidate(4.0, 0.0, 0.0, 1), active_index=0, scores=[0.0] * len(enemy),
        enemy_cleared=enemy, own_cleared=own, active_cleared=[active] * len(enemy),
        total_self_cleared=[value + int(active) for value in own],
        own_in_house=[1] * len(enemy),
        preserves_all_own=not any(own) and not active, rule_legal=legal,
        rule_violations=[[] for _ in enemy], enemy_cleared_indices=[[1] * value for value in enemy],
        final_center_distance_by_index=[{0: 0.2, 2: 0.4, 1: 0.5} for _ in enemy],
        mean_score=0.0, worst_score=0.0,
    )


class TradeFallbackTests(unittest.TestCase):
    def test_one_own_out_allows_equal_actual_enemy_out(self):
        self.assertTrue(is_loss_budget_candidate(item([1, 1, 1], [1, 1, 1]), 1))

    def test_two_own_out_requires_two_enemy_out_and_second_stage(self):
        trade = item([2, 2, 2], [2, 2, 2])
        self.assertFalse(is_loss_budget_candidate(trade, 1))
        self.assertTrue(is_loss_budget_candidate(trade, 2))

    def test_moved_but_not_out_cannot_buy_own_loss(self):
        self.assertFalse(is_loss_budget_candidate(item([0, 0, 0], [1, 1, 1]), 1))

    def test_rule_violation_never_passes_trade(self):
        self.assertFalse(is_loss_budget_candidate(item([2, 2, 2], [1, 1, 1], active=True), 1))
        self.assertFalse(is_loss_budget_candidate(item([2, 2, 2], [1, 1, 1], legal=False), 1))

    def test_active_stone_counts_as_one_of_the_allowed_self_outs(self):
        self.assertTrue(is_loss_budget_candidate(item([1, 1, 1], [0, 0, 0], active=True), 1))

    def test_must_clear_target_checks_actual_disabled_slot(self):
        self.assertTrue(is_loss_budget_candidate(item([1, 1, 1], [0, 0, 0]), 0, must_clear_index=1))
        missing = item([1, 1, 1], [0, 0, 0])
        missing.enemy_cleared_indices = [[], [], []]
        self.assertFalse(is_loss_budget_candidate(missing, 0, must_clear_index=1))

    def test_last_hammer_mode_accepts_target_that_stays_but_is_farther_than_self(self):
        candidate = item([0, 0, 0], [0, 0, 0])
        self.assertTrue(is_last_hammer_target_beaten(candidate, 1))
        self.assertTrue(is_loss_budget_candidate(candidate, 0, must_clear_index=1, allow_last_hammer_closer_win=True))

    def test_last_hammer_mode_rejects_tie_or_opponent_closer(self):
        candidate = item([0, 0, 0], [0, 0, 0])
        candidate.final_center_distance_by_index = [{0: 0.5, 2: 0.6, 1: 0.5}] * 3
        self.assertFalse(is_last_hammer_target_beaten(candidate, 1))

    def test_last_hammer_mode_requires_more_remaining_own_stones(self):
        candidate = item([0, 0, 0], [0, 0, 0])
        candidate.final_center_distance_by_index = [{0: 0.2, 1: 0.5}] * 3
        self.assertFalse(is_last_hammer_target_beaten(candidate, 1))

    def test_full_preserve_is_separate_mode(self):
        self.assertTrue(is_full_preserve_candidate(item([1, 1, 1], [0, 0, 0])))
        self.assertFalse(is_full_preserve_candidate(item([2, 2, 2], [1, 1, 1])))

    def test_more_own_stones_in_house_wins_tie_break(self):
        one = item([1, 1, 1], [0, 0, 0])
        two = item([1, 1, 1], [0, 0, 0])
        two.own_in_house = [2, 2, 2]
        self.assertGreater(selection_priority(two), selection_priority(one))


if __name__ == "__main__":
    unittest.main()
