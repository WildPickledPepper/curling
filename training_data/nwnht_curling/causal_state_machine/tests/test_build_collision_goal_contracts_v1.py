import unittest

from training_data.nwnht_curling.causal_state_machine.build_collision_goal_contracts_v1 import build


def family(*, binding, support=40, removed=1, target_zone="BUTTON"):
    return {
        "goal_id": "A", "source_state": "K2_V2_OPPONENT_HOUSE_THREAT_1",
        "observed_template_kind": "SINGLE_OPPONENT_REMOVAL", "support": support,
        "tactical_target_zone": target_zone, "observed_opponent_removed_count": removed,
        "observed_opponent_house_removed_count": removed,
        "after_opponent_reply_state_distribution": [],
        "fine_goal_options": [{"goal_id": "G", "assigned_support": 40, "dynamic_house_removal_binding_request": binding, "stone_constraints_when_unambiguous": []}],
    }


class CollisionGoalContractTests(unittest.TestCase):
    def test_dynamic_house_binding_becomes_a_contract(self):
        result = build([family(binding={
            "binding_kind": "OPPONENT_HOUSE_SET", "owner": "opponent", "source_region": "house",
            "required_disposition": "OUT_OF_PLAY", "choose_count": 1,
        })])
        self.assertEqual(result["manifest"]["contract_count"], 1)
        contract = result["contracts"][0]
        self.assertEqual(contract["target_binding"]["binding_mode"], "DYNAMIC_OPPONENT_HOUSE_SET")
        self.assertEqual(contract["active_target_region"]["kind"], "CIRCLE")

    def test_binding_count_must_match_observed_removal_count(self):
        result = build([family(binding={
            "binding_kind": "OPPONENT_HOUSE_SET", "owner": "opponent", "source_region": "house",
            "required_disposition": "OUT_OF_PLAY", "choose_count": 2,
        })])
        self.assertFalse(result["contracts"])
        self.assertEqual(result["rejected_parents"][0]["reason"], "binding_count_disagrees_with_parent_removal_count")

    def test_no_target_region_is_not_made_executable(self):
        result = build([family(binding={
            "binding_kind": "OPPONENT_HOUSE_SET", "owner": "opponent", "source_region": "house",
            "required_disposition": "OUT_OF_PLAY", "choose_count": 1,
        }, target_zone="NO_ACTIVE_FINAL_POINT")])
        self.assertFalse(result["contracts"])
        self.assertEqual(result["rejected_parents"][0]["reason"], "no_executable_active_target_region")


if __name__ == "__main__":
    unittest.main()
