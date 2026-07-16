import unittest

import numpy as np

from planning_proxy.analytic_proxy import make_initial_candidates


class AnalyticProxyCandidateTests(unittest.TestCase):
    def test_legacy_grid_is_reproducible(self):
        self.assertEqual(len(make_initial_candidates()), 5 * 25 * 9)

    def test_expanded_grid_has_the_configured_coverage(self):
        shots = make_initial_candidates(velocity_count=7, lateral_count=41, spin_count=15)
        self.assertEqual(len(shots), 7 * 41 * 15)
        np.testing.assert_allclose(shots[0], (3.2, -2.2, -15.0))
        np.testing.assert_allclose(shots[-1], (5.6, 2.2, 15.0))


if __name__ == "__main__":
    unittest.main()
