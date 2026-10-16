import unittest

from training_research.contact_modes import parents


class ContactModeTests(unittest.TestCase):
    def test_second_parent_rotates_routes_even_when_best_candidates_share_one(self):
        selection = {"first_contact_any": [0], "require_single_first_contact": True,
                     "goal": {"stones": {"0": {"type": "SURVIVE"}}}}
        def candidate(value, chain, first=0):
            return {"loss": value, "shot": (3., value/100., 0.),
                    "record": {"prediction": {"firstContactTargets": [first], "settled": True},
                               "physical_final": [{"index": i, "enabled": True} for i in range(16)],
                               "rule_violations": [],
                               "collision_events": [{"stones": pair} for pair in chain]}}
        same = [candidate(i/100., [(0, 5)]) for i in range(12)]
        second = candidate(2., [(0, 5), (0, 2)])
        third = candidate(3., [(0, 5), (2, 5)])
        invalid = candidate(.001, [(1, 5)], first=1)
        ordered = sorted(same+[second, third, invalid], key=lambda x: x["loss"])
        visits = {}
        selected, count = parents(ordered, selection, visits)
        self.assertEqual(count, 3)
        self.assertIs(selected[0], same[0])
        self.assertIs(selected[1], second)
        selected, count = parents(ordered, selection, visits)
        self.assertIs(selected[0], same[0])
        self.assertIs(selected[1], third)


if __name__ == "__main__":
    unittest.main()
