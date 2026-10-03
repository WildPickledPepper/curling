import unittest

from training_data.nwnht_curling.discover_first_player_state_graph import first_decisions, topology_features
from training_data.nwnht_curling.discover_state_graph import EndRecord, Frame


class FirstPlayerStateGraphTests(unittest.TestCase):
    def _end(self):
        record = EndRecord(1, 1, 1, "Mens_Teams", ("A", "B"), {"A": 0, "B": 0}, {"A": 0, "B": 1}, {"A": 2, "B": 3})
        record.frames[0] = Frame()
        for shot in range(1, 17):
            stones = []
            if shot >= 1:
                stones.append(("red", 0.2, 2.5))
            if shot >= 2:
                stones.append(("yellow", -1.0, 1.0))
            record.frames[shot] = Frame(throwing_team="A" if shot % 2 else "B", call="Draw", rating=4, stones=stones)
        return record

    def test_extracts_only_eight_first_player_decisions_without_context_features(self):
        decisions = first_decisions(self._end())
        self.assertIsNotNone(decisions)
        assert decisions is not None
        self.assertEqual([item.own_throw_number for item in decisions], list(range(1, 9)))
        self.assertEqual(decisions[0].uid, "1:1")
        self.assertEqual(decisions[-1].uid, "1:15")
        self.assertNotIn("score_diff_first_clipped", decisions[0].features)
        self.assertNotIn("end_number_clipped", decisions[0].features)
        self.assertNotIn("shot_in_end", decisions[0].features)

    def test_left_right_mirrors_have_the_same_topology_features(self):
        left = [{"owner": "first", "x_m": -0.8, "y_m": 2.5}, {"owner": "opponent", "x_m": 1.0, "y_m": 0.4}]
        right = [{"owner": "first", "x_m": 0.8, "y_m": 2.5}, {"owner": "opponent", "x_m": -1.0, "y_m": 0.4}]
        self.assertEqual(topology_features(left), topology_features(right))


if __name__ == "__main__":
    unittest.main()
