import unittest
from unittest.mock import patch

import numpy as np

from training_research.population_search import refine


class PopulationSearchTests(unittest.TestCase):
    def test_zero_rank_loss_without_certification_is_never_returned(self):
        calls = []
        initial = {"shot": (4., 0., 0.), "loss": 0., "success": False}
        def trial(shot, phase):
            calls.append(tuple(shot))
            return {"shot": tuple(shot), "loss": 0., "success": False}
        with patch("training_research.solver_experiments.dfols_fit", side_effect=lambda current, *a, **kw: (current, False)):
            result = refine({"stones": [], "selection": {}}, trial, [initial],
                            lambda: len(calls), 25., {})
        self.assertIsNone(result)
        self.assertLessEqual(len(calls), 25)

    def test_population_finds_a_distant_feasible_basin_within_call_limit(self):
        initial = {"shot": (5.8, 2., 14.), "loss": 200., "success": False}
        calls = []
        target = np.array((3.2, -.4, -2.))
        def trial(shot, phase):
            distance = np.linalg.norm((np.asarray(shot)-target)/np.array((.4, .3, 2.)))
            item = {"shot": tuple(shot), "loss": distance**2, "success": distance < .4}
            calls.append(item)
            return item
        with patch("training_research.solver_experiments.dfols_fit", side_effect=lambda current, *a, **kw: (current, False)):
            result = refine({"stones": [], "selection": {}}, trial, [initial],
                            lambda: len(calls), 256., {})
        self.assertTrue(result["success"])
        self.assertIn(result, calls)
        self.assertLessEqual(len(calls), 256)


if __name__ == "__main__":
    unittest.main()
