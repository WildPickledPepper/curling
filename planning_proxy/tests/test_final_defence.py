import unittest

from planning_proxy.validate_final_defence import ACTIVE_INDEX, _seed_is_safe


class FinalDefenceAcceptanceTests(unittest.TestCase):
    def test_last_stone_in_button_is_a_breach(self):
        safe, reason, _, _ = _seed_is_safe(
            {1: 0.30, ACTIVE_INDEX: 0.10}, {1}, {ACTIVE_INDEX},
        )
        self.assertFalse(safe)
        self.assertIn("按钮区", reason)

    def test_surviving_old_opponent_is_part_of_actual_end_state(self):
        """真实末手验收不能忽略第八颗后仍留在场上的敌壶。"""

        safe, reason, opponent_distance, own_distance = _seed_is_safe(
            {1: 0.40, 3: 0.25, ACTIVE_INDEX: 0.80}, {1}, {3, ACTIVE_INDEX},
        )
        self.assertFalse(safe)
        self.assertIn("残留壶", reason)
        self.assertEqual(opponent_distance, 0.25)
        self.assertEqual(own_distance, 0.40)

    def test_last_stone_out_is_safe_only_when_old_opponents_are_not_closer(self):
        safe, _, _, _ = _seed_is_safe({1: 0.35}, {1}, {ACTIVE_INDEX})
        self.assertTrue(safe)


if __name__ == "__main__":
    unittest.main()
