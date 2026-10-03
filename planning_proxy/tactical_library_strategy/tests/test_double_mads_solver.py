import unittest
from types import SimpleNamespace

import numpy as np

from planning_proxy.tactical_library_strategy.double_mads_solver import _pseudo_states, select_double_parent_rows


class DoubleMadsSolverTests(unittest.TestCase):
    def test_final_board_export_is_restored_as_enabled_disabled_slots(self):
        states = _pseudo_states([{"index": 2, "enabled": True, "x": 2.4, "y": 4.9}])
        self.assertFalse(states[1]["enabled"])
        self.assertTrue(states[2]["enabled"])
        self.assertAlmostEqual(states[2]["x"], 2.4)

    def test_parent_selection_reserves_a_branch_for_each_first_hit_target(self):
        # ``attack_score`` only reads these rough fields; target 1 is made much
        # more attractive so a global top-3 selector would omit target 2.
        coarse = SimpleNamespace(
            first_hit_index=np.asarray([1, 1, 1, 2]),
            first_hit_owner=np.asarray(["opponent"] * 4),
            stop_points=np.zeros((4, 2)),
            nearest_enemy=np.zeros(4),
            nearest_own=np.full(4, 99.0),
            exits_play=np.zeros(4, dtype=bool),
        )
        shots = np.asarray([[5.0, 0.0, -3.0], [5.0, 0.1, -2.0], [5.0, 0.2, -1.0], [4.0, 1.5, 4.0]])
        parents = select_double_parent_rows(coarse, shots, (1, 2), parent_limit=3)
        self.assertIn(3, parents)
        self.assertEqual(len(parents), 3)


if __name__ == "__main__":
    unittest.main()
