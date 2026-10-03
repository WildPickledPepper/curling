import unittest
from collections import Counter

from training_data.nwnht_curling.causal_state_machine.assess_state_homogeneity import _counter_without


class StateHomogeneityTests(unittest.TestCase):
    def test_counter_without_retains_only_positive_remainder(self):
        self.assertEqual(_counter_without(Counter({"a": 4, "b": 2}), Counter({"a": 3, "b": 2})), Counter({"a": 1}))


if __name__ == "__main__":
    unittest.main()
