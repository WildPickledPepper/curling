import unittest

from planning_proxy.first_player_strategy import (
    EDGE_DEAD_RIGHT,
    GUARD_TARGET,
    StrategyStone,
    is_edge_dead,
    plan_first_player_turn,
    score_strict_outcome,
)


def stone(index, owner, x, y, enabled=True):
    return {"index": index, "owner": owner, "x": x, "y": y, "enabled": enabled}


class FirstPlayerStrategyTests(unittest.TestCase):
    def test_first_throw_is_centre_guard(self):
        plan = plan_first_player_turn([], 0)
        self.assertEqual(plan.phase, "open_centre_guard")
        self.assertEqual(plan.target_points, (GUARD_TARGET,))

    def test_second_throw_pushes_ordinary_protected_guard_to_edge(self):
        plan = plan_first_player_turn([stone(1, "opponent", 2.90, 7.20)], 2)
        self.assertEqual(plan.phase, "process_first_enemy_and_score")
        self.assertEqual(plan.target_opponent_index, 1)
        self.assertEqual(plan.opponent_action, "push_to_edge_dead")

    def test_second_throw_does_not_attack_protected_centre_guard(self):
        plan = plan_first_player_turn([stone(1, "opponent", 2.375, 7.20)], 2)
        self.assertIsNone(plan.target_opponent_index)
        self.assertEqual(plan.opponent_action, "avoid_protected_centre_guard")

    def test_seventh_throw_repairs_missing_front_guard(self):
        board = [
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
            stone(3, "opponent", 1.20, 8.0),
        ]
        plan = plan_first_player_turn(board, 12)
        self.assertEqual(plan.phase, "repair_front_protector")

    def test_eighth_throw_reclaims_centre_before_everything_else(self):
        board = [
            stone(1, "self", 2.70, 5.20),
            stone(2, "self", 2.05, 5.30),
            stone(3, "opponent", 2.375, 4.88),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertEqual(plan.phase, "repair_closest_scoring_anchor")

    def test_edge_dead_band_is_explicit(self):
        self.assertTrue(is_edge_dead(StrategyStone(1, "opponent", sum(EDGE_DEAD_RIGHT) / 2.0, 7.0)))

    def test_strict_outcome_recognizes_opening_guard(self):
        plan = plan_first_player_turn([], 0)
        score, goal = score_strict_outcome(
            [{"enabled": True, "x": GUARD_TARGET[0], "y": GUARD_TARGET[1]}], [], 0, plan,
        )
        self.assertTrue(goal)
        self.assertGreater(score, 0.0)


if __name__ == "__main__":
    unittest.main()
