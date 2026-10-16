import unittest

from training_research.inverse_dataset.selection import failure_reason
from training_research.inverse_goal_search import loss
from training_research.solver_experiments import precise_clip
from training_research.region_feasible_refine import fit


class RegionFeasibleTests(unittest.TestCase):
    def test_can_move_a_satisfied_goal_within_its_remaining_region(self):
        selection = {"goal": {"stones": {
            "0": {"type": "IN_REGION", "x": 2.2, "y": 4.8, "radius": .25},
            "5": {"type": "IN_REGION", "x": 2.5, "y": 4.88, "radius": .1}}}}
        calls = []
        def trial(shot, phase):
            shot = precise_clip(shot)
            v, h, w = shot
            states = [{"index": i, "enabled": i in (0, 5), "x": 0., "y": 0.} for i in range(16)]
            states[0].update(x=2.2+v-3., y=4.8+h)
            states[5].update(x=2.2+v-3., y=4.88+.05*w)
            record = {"status": "complete", "physical_final": states, "collision_events": [],
                      "rule_violations": [], "prediction": {"settled": True, "contact": False}}
            failure = failure_reason(record, selection)
            item = {"shot": shot, "loss": loss(record, selection), "record": record,
                    "success": failure is None, "phase": phase}
            calls.append(item)
            return item
        initial = trial((3., 0., 0.), "initial")
        calls.clear()
        best, success = fit(initial, trial, selection, allowance=24)
        self.assertTrue(success)
        self.assertIsNone(failure_reason(success["record"], selection))
        self.assertGreater(success["shot"][0], 3.2)
        self.assertLess(success["shot"][0], 3.25)
        self.assertLessEqual(len(calls), 24)

    def test_a_feasible_inner_prediction_cannot_certify_missing_collision(self):
        selection = {"goal": {"stones": {"0": {
            "type": "IN_REGION", "x": 2., "y": 4., "radius": .15}}},
            "required_collision_pairs": [[0, 5]]}
        record = {"status": "complete", "physical_final": [{"index": i, "enabled": True, "x": 2., "y": 4.} for i in range(16)],
                  "prediction": {"settled": True, "contact": False}, "collision_events": [], "rule_violations": []}
        def trial(shot, phase):
            return {"shot": precise_clip(shot), "loss": loss(record, selection), "record": record,
                    "success": False, "phase": phase}
        initial = trial((3., 0., 0.), "initial")
        best, success = fit(initial, trial, selection, allowance=12)
        self.assertFalse(success)
        self.assertEqual(failure_reason(best["record"], selection), "missing_collision_pair")


if __name__ == "__main__":
    unittest.main()
