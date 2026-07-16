import unittest
from unittest.mock import patch

from tools.reverse import probe_bestshot_release_constants as probe
from tools.reverse.replay_bestshot_seeded import ProtocolState


class ProbeBestshotReleaseConstantsTest(unittest.TestCase):
    def test_frange_includes_end_with_rounding(self):
        self.assertEqual(probe.frange(1.0, 1.3, 0.1), [1.0, 1.1, 1.2, 1.3])

    def test_evaluate_reports_rmse_components(self):
        rows = [
            {
                "requested_v0": 3.0,
                "requested_h0": 0.0,
                "requested_w0": 0.0,
                "motion_x": 2.4,
                "motion_y": 21.5,
                "motion_vx": 0.1,
                "motion_vy": -2.0,
                "motion_w": 0.2,
            }
        ]

        with patch.object(
            probe,
            "replay_until_y",
            return_value=ProtocolState(2.5, 21.3, 0.4, -1.6, 0.7, 123),
        ):
            result = probe.evaluate(rows, release_x=2.35, release_y=33.0, stop_y=21.52, max_steps=5000)

        self.assertEqual(result["release_x"], 2.35)
        self.assertEqual(result["release_y"], 33.0)
        self.assertEqual(result["stop_y"], 21.52)
        self.assertEqual(result["n"], 1)
        self.assertAlmostEqual(result["pos_rmse"], (0.1**2 + (-0.2) ** 2) ** 0.5)
        self.assertAlmostEqual(result["velocity_rmse"], (0.3**2 + 0.4**2 + 0.5**2) ** 0.5)
        self.assertEqual(result["avg_steps"], 123)


if __name__ == "__main__":
    unittest.main()
