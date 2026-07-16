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
        self.assertEqual(plan.phase, "clear_then_choose_defence_shape")
        self.assertEqual(plan.target_opponent_index, 3)
        self.assertEqual(plan.opponent_action, "physical_clear")
        self.assertEqual({shape.name for shape in plan.defence_shapes}, {"双壶_左侧三角", "双壶_右侧三角", "双壶_第三红圈错层"})
        self.assertGreaterEqual(len(plan.target_points), 8)

    def test_eighth_throw_reclaims_centre_before_everything_else(self):
        board = [
            stone(1, "self", 2.70, 5.20),
            stone(2, "self", 2.05, 5.30),
            stone(3, "opponent", 2.375, 4.88),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertEqual(plan.phase, "clear_then_choose_defence_shape")
        self.assertEqual({shape.name for shape in plan.defence_shapes}, {"双壶_左侧三角", "双壶_右侧三角", "双壶_第三红圈错层"})

    def test_defence_shapes_change_with_own_stone_count(self):
        one_own = plan_first_player_turn([stone(1, "self", 2.28, 4.70)], 10)
        two_own = plan_first_player_turn([
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
        ], 10)
        three_own = plan_first_player_turn([
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
            stone(3, "self", 1.92, 6.12),
        ], 10)
        self.assertEqual({shape.name for shape in one_own.defence_shapes}, {"单壶_双红圈错层", "单壶_左侧护门", "单壶_右侧护门"})
        self.assertEqual({shape.name for shape in two_own.defence_shapes}, {"双壶_左侧三角", "双壶_右侧三角", "双壶_第三红圈错层"})
        self.assertEqual({shape.name for shape in three_own.defence_shapes}, {"三壶以上_中心锚双门", "三壶以上_左侧外壳", "三壶以上_右侧外壳", "三壶以上_红圈后备"})

    def test_any_one_defence_shape_is_an_acceptable_strict_goal(self):
        board = [
            stone(1, "self", 2.28, 4.70),
            stone(2, "self", 2.67, 5.18),
            stone(3, "opponent", 1.20, 8.0),
        ]
        plan = plan_first_player_turn(board, 12)
        # 对手 3 已被清出；出手壶落入左侧三角的其中一个保护槽。
        score, goal = score_strict_outcome(
            [
                {"enabled": True, "x": 2.28, "y": 4.70},
                {"enabled": True, "x": 2.67, "y": 5.18},
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": True, "x": 1.92, "y": 6.12},
            ],
            board,
            4,
            plan,
        )
        self.assertTrue(goal)
        self.assertGreater(score, 0.0)

    def test_centre_anchor_double_gate_is_a_valid_defence_goal(self):
        board = [
            stone(1, "self", 2.375, 7.15),
            stone(2, "self", 2.375, 4.88),
            stone(3, "self", 1.92, 6.12),
        ]
        plan = plan_first_player_turn(board, 14)
        self.assertIn("三壶以上_中心锚双门", {shape.name for shape in plan.defence_shapes})
        score, goal = score_strict_outcome(
            [
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": True, "x": 2.375, "y": 7.15},
                {"enabled": True, "x": 2.375, "y": 4.88},
                {"enabled": True, "x": 1.92, "y": 6.12},
                {"enabled": True, "x": 2.83, "y": 6.12},
            ],
            board,
            4,
            plan,
        )
        self.assertTrue(goal)
        self.assertGreater(score, 0.0)

    def test_eighth_throw_does_not_certify_an_ordinary_side_shell(self):
        board = [
            stone(1, "self", 2.10, 4.52),
            stone(2, "self", 2.72, 5.15),
            stone(3, "self", 2.00, 4.70),
        ]
        plan = plan_first_player_turn(board, 14)
        _, goal = score_strict_outcome(
            [
                {"enabled": False, "x": 0.0, "y": 0.0},
                {"enabled": True, "x": 2.10, "y": 4.52},
                {"enabled": True, "x": 2.72, "y": 5.15},
                {"enabled": True, "x": 2.00, "y": 4.70},
                {"enabled": True, "x": 1.92, "y": 6.12},
            ],
            board,
            4,
            plan,
        )
        self.assertFalse(goal)

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
