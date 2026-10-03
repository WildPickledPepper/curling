import unittest
from training_data.nwnht_curling.causal_state_machine.build_causal_estimation_panel import fold_for_match


class CausalPanelTests(unittest.TestCase):
    def test_match_stays_in_one_deterministic_fold(self):
        self.assertEqual(fold_for_match(123), fold_for_match(123))
        self.assertIn(fold_for_match(123), range(5))


if __name__ == "__main__":
    unittest.main()
