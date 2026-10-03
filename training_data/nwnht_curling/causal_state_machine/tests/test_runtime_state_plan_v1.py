import unittest

from training_data.nwnht_curling.causal_state_machine.runtime_state_plan_v1 import _unmirror_target


class RuntimeStatePlanV1Tests(unittest.TestCase):
    def test_unmirror_reflects_targets_without_changing_next_state_ids(self):
        option = {
            "tactical_target_zone": "HOUSE_FRONT_LEFT",
            "expected_next_state_distribution": [{"value": "K2_V2_FIRST_HOUSE_CONTROL_3", "share": 1.0}],
            "target_region": {"kind": "HOUSE_SECTOR", "x_relation": "<0"},
            "fine_goal_options": [{
                "active_final_region": {"shape": "circle", "centre_x_m": -0.2},
                "after_own_occupancy": {"first": {"house_front_left": 1}, "opponent": {}},
                "stone_constraints_when_unambiguous": [{"historical_source_zone": "house_front_left"}],
            }],
        }
        mirrored = _unmirror_target(option)
        self.assertEqual(mirrored["tactical_target_zone"], "HOUSE_FRONT_RIGHT")
        self.assertEqual(mirrored["target_region"]["x_relation"], ">=0")
        self.assertEqual(mirrored["fine_goal_options"][0]["active_final_region"]["centre_x_m"], 0.2)
        self.assertIn("house_front_right", mirrored["fine_goal_options"][0]["after_own_occupancy"]["first"])
        self.assertEqual(mirrored["expected_next_state_distribution"][0]["value"], "K2_V2_FIRST_HOUSE_CONTROL_3")


if __name__ == "__main__":
    unittest.main()
