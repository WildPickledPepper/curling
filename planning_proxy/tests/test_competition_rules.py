import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.competition_rules import RuleBoardStone, free_guard_rule_violations


class FreeGuardRuleTests(unittest.TestCase):
    def test_centre_guard_cannot_leave_centre_before_sixth_throw(self):
        board = [RuleBoardStone(1, "opponent", 2.375, 7.15)]
        final = [{"enabled": False}, {"enabled": True, "x": 2.70, "y": 7.15}]
        self.assertTrue(free_guard_rule_violations(board, final, shot_index=2))

    def test_any_opponent_free_guard_cannot_be_removed_before_sixth_throw(self):
        board = [RuleBoardStone(1, "opponent", 2.75, 7.15)]
        final = [{"enabled": False}, {"enabled": False}]
        self.assertTrue(free_guard_rule_violations(board, final, shot_index=4))

    def test_protection_ends_on_sixth_throw(self):
        board = [RuleBoardStone(1, "opponent", 2.375, 7.15)]
        final = [{"enabled": False}, {"enabled": False}]
        self.assertEqual([], free_guard_rule_violations(board, final, shot_index=5))


if __name__ == "__main__":
    unittest.main()
