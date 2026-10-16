"""Source fidelity and answer isolation of the compact solver dataset."""
import copy
import unittest

from training_research.export_solver_samples import extract
from training_research.inverse_dataset.sampling import validate_scene
from training_research.inverse_dataset.selection import failure_reason


class ExportSolverSampleTests(unittest.TestCase):
    def setUp(self):
        scene = validate_scene({"active_index": 5, "stones": [
            {"index": 0, "x": 2.2, "y": 4.8, "yaw": .1},
            {"index": 2, "x": 2.5, "y": 4.8, "yaw": -.2}]})
        before = [{"index": i, "enabled": i in (0, 2), "x": 2.2 if i == 0 else 2.5,
                   "y": 4.8, "yaw": .1 if i == 0 else -.2} for i in range(16)]
        final = [{"index": i, "enabled": i == 5, "x": 2.375, "y": 4.88, "yaw": .3} for i in range(16)]
        self.record = {"record_id": "test-source", "scene_key": scene["scene_key"],
            "active_index": 5, "requested_scene": scene, "before": before, "physical_final": final,
            "shot": [6., .13, 5.], "physics_seed": 999, "status": "complete", "rule_violations": [],
            "prediction": {"settled": True, "contact": True, "firstContactTargets": [0]},
            "collision_events": [{"stones": [0, 2], "step": 800}]}

    def test_source_board_and_goal_survive_without_answer_in_request(self):
        original = copy.deepcopy(self.record)
        request, reference = extract(self.record)
        self.assertEqual(validate_scene(request)["scene_key"], original["scene_key"])
        self.assertEqual(request["stones"][0]["yaw"], .1)
        for forbidden in ("shot", "physics_seed", "physical_final", "candidate_shots"):
            self.assertNotIn(forbidden, request)
        self.assertEqual(reference["shot"], original["shot"])
        self.assertEqual(reference["physics_seed"], 999)
        self.assertEqual({s["index"] for s in reference["physical_final"]}, {0, 2, 5})
        self.assertEqual(request["selection"]["tactic"], "double_hit")
        self.assertIsNone(failure_reason(original, request["selection"]))
        self.assertEqual(self.record, original)

    def test_bad_source_outcomes_cannot_become_known_solved_tasks(self):
        for change in ({"status": "error"}, {"rule_violations": ["protected_guard"]},
                       {"prediction": {"settled": False}}):
            with self.subTest(change=change):
                self.assertIsNone(extract({**self.record, **change}))

    def test_terminal_removal_without_pair_is_not_labelled_double(self):
        record = {**self.record, "collision_events": []}
        request, _ = extract(record)
        self.assertNotEqual(request["selection"]["tactic"], "double_hit")


if __name__ == "__main__":
    unittest.main()
