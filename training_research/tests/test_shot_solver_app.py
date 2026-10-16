"""Certification and budget semantics at the reusable application boundary."""
import copy
import unittest
from unittest.mock import patch

from training_research.shot_solver import BudgetedShotSolver


class ShotSolverApplicationTests(unittest.TestCase):
    def setUp(self):
        self.scene = {"active_index": 1, "stones": [], "selection": {
            "tactic": "default_draw", "require_no_contact": True,
            "goal": {"stones": {"1": {"type": "IN_REGION", "x": 2.375, "y": 4.88, "radius": .15}}}}}
        self.record = {"status": "complete", "rule_violations": [], "collision_events": [],
            "prediction": {"settled": True, "contact": False},
            "physical_final": [{"index": i, "enabled": i == 1, "x": 2.375, "y": 4.88} for i in range(16)]}

    def run_solver(self, record, **options):
        with patch("training_research.shot_solver.simulate_record", return_value=copy.deepcopy(record)) as simulate, \
             patch("training_research.inverse_goal_search.proposals", return_value=[(0., (3., 0., 0.), "draw")]):
            result = BudgetedShotSolver(environment=object()).solve(self.scene, **options)
            return result, simulate

    def test_full_goal_is_certified_and_caller_scene_is_not_mutated(self):
        original = copy.deepcopy(self.scene)
        result, simulate = self.run_solver(self.record, seed=100, include_records=True)
        self.assertTrue(result["success"])
        self.assertEqual(result["shot"], [3., 0., 0.])
        self.assertEqual(result["physics_calls"], 1)
        self.assertEqual(simulate.call_args.args[3], 100+7919)
        self.assertIsNone(result["records"][0]["task_failure"])
        self.assertEqual(self.scene, original)
        self.assertIn("scene_key", result)

    def test_budget_miss_returns_no_executable_best_effort(self):
        record = copy.deepcopy(self.record)
        record["physical_final"][1]["x"] = 3.0
        result, simulate = self.run_solver(record, max_calls=1)
        self.assertFalse(result["success"])
        self.assertIsNone(result["shot"])
        self.assertEqual(simulate.call_count, 1)
        self.assertIsNotNone(result["diagnostics"]["best_effort_shot"])

    def test_simulation_error_is_explicit_instead_of_a_certified_shot(self):
        with self.assertRaisesRegex(RuntimeError, "forward simulation failed"):
            self.run_solver({"status": "error", "error": "unavailable kernel"})


if __name__ == "__main__":
    unittest.main()
