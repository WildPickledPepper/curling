import unittest

from training_data.nwnht_curling.discover_state_graph import (
    EndRecord,
    Frame,
    infer_colour_owners,
    make_samples,
    normalize_action,
    shot_phase,
)


class StateGraphTests(unittest.TestCase):
    def _complete_end(self) -> EndRecord:
        record = EndRecord(
            end_id=1,
            match_id=1,
            end_number=1,
            match_type="Mens_Teams",
            teams=("A", "B"),
            score_before={"A": 0, "B": 0},
            score_after={"A": 0, "B": 1},
            final_score={"A": 3, "B": 4},
        )
        record.frames[0] = Frame()
        # Red is retained by A at shot 1; yellow by B at shot 2.  Later
        # positions stay intentionally simple: this checks the transition
        # schema, not a physical collision model.
        for shot in range(1, 17):
            team = "A" if shot % 2 else "B"
            stones = []
            if shot >= 1:
                stones.append(("red", 0.0, 2.5))
            if shot >= 2:
                stones.append(("yellow", 1.0, 1.0))
            record.frames[shot] = Frame(throwing_team=team, call="Draw", rating=4, stones=stones)
        return record

    def test_complete_end_becomes_sixteen_linked_decisions(self):
        samples = make_samples(self._complete_end())
        self.assertIsNotNone(samples)
        assert samples is not None
        self.assertEqual(len(samples), 16)
        self.assertEqual(samples[0].role, "FIRST_TO_THROW")
        self.assertEqual(samples[1].role, "OPPONENT_TO_THROW")
        self.assertEqual(samples[0].phase, "FGZ_1_5")
        self.assertEqual(samples[5].phase, "BUILD_6_10")
        self.assertEqual(samples[0].board, [])
        self.assertEqual(samples[1].board[0]["owner"], "first")

    def test_conflicting_colour_ownership_is_rejected(self):
        record = self._complete_end()
        record.frames[3].stones = [("yellow", 1.0, 1.0)]  # red disappears; yellow wrongly grows on A's shot
        self.assertIsNone(make_samples(record))

    def test_action_and_phase_normalisation(self):
        self.assertEqual(normalize_action("through"), "THROUGH")
        self.assertEqual(normalize_action("made up"), "UNCLASSIFIED")
        self.assertEqual(shot_phase(5), "FGZ_1_5")
        self.assertEqual(shot_phase(15), "LAST_15_16")


if __name__ == "__main__":
    unittest.main()
