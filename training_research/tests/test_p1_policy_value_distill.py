from __future__ import annotations

import unittest

from training_research.p1_policy_value_distill import (
    FEATURE_SIZE,
    aggregate_tactic_weights,
    encode_state,
    histogram_distribution,
    normalized_action,
)


def state() -> dict:
    def stone(index: int) -> dict:
        return {"id": index, "x": 2.375, "y": 4.88, "yaw": 0.0, "inPlay": index == 0}
    return {
        "board": {"self": [stone(index * 2) for index in range(8)], "opponent": [stone(index * 2 + 1) for index in range(8)]},
        "turn": {"shotIndex": 15, "remainingShotsInEnd": 1, "isHammerSide": True, "isLastShotOfEnd": True, "houseLeader": "self", "houseScoreForSelf": 1},
        "match": {"endIndex": 0, "endsRemainingAfterThis": 0, "scoreDifferenceForSelf": 0},
    }


class P1PolicyValueDistillTests(unittest.TestCase):
    def test_feature_shape_and_action_normalization(self) -> None:
        self.assertEqual(len(encode_state(state())), FEATURE_SIZE)
        self.assertEqual(normalized_action([6.0, -2.23, 15.7]), [1.0, -1.0, 1.0])

    def test_targets_normalize(self) -> None:
        weights = aggregate_tactic_weights([
            {"tactic": "draw_center", "searchWeight": 2.0},
            {"tactic": "takeout", "searchWeight": 1.0},
        ])
        self.assertAlmostEqual(sum(weights), 1.0)
        self.assertAlmostEqual(weights[2], 2.0 / 3.0)
        scores = histogram_distribution({"-1": 1, "1": 3})
        self.assertAlmostEqual(sum(scores), 1.0)
        self.assertAlmostEqual(scores[7], 0.25)
        self.assertAlmostEqual(scores[9], 0.75)


if __name__ == "__main__":
    unittest.main()
