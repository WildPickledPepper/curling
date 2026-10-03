import unittest

from training_data.nwnht_curling.causal_state_machine.build_local_k1_anchor_k2_goals_v1 import build


TOPOLOGY = "K2_POST_OWN[control=FIRST;F_BUTTON=1;F_HOUSE_FRONT_LEFT=0;F_HOUSE_FRONT_RIGHT=0;F_HOUSE_BACK_LEFT=0;F_HOUSE_BACK_RIGHT=0;O_BUTTON=0;O_HOUSE_FRONT_LEFT=0;O_HOUSE_FRONT_RIGHT=0;O_HOUSE_BACK_LEFT=0;O_HOUSE_BACK_RIGHT=0;F_protected_house=0;O_protected_house=0;macro=FIRST_HOUSE_CONTROL]"


class LocalK1AnchorG2Tests(unittest.TestCase):
    def test_g2_is_extracted_only_from_anchor_preserving_k1_trajectory(self):
        k1 = {"end_id": 2, "own_throw_number": 1, "u_after_own": [{"owner": "first", "x_m": 0.0, "y_m": 2.27}], "s_after_opponent_reply": [{"owner": "first", "x_m": 0.0, "y_m": 2.27}, {"owner": "opponent", "x_m": 0.1, "y_m": 0.1}]}
        k2 = {"end_id": 2, "own_global_shot_number": 3, "own_throw_number": 2, "match_id": 9, "terminal_end_label": {"first_end_margin": 2}}
        template = {"panel_key": "2:3", "K": 2, "observed_template_kind": "ACTIVE_STONE_PLACEMENT", "observed_delta": {"first_house": 1, "opponent_house": 0, "opponent_removed_count": 0, "opponent_house_removed_count": 0}, "post_own_topology": TOPOLOGY, "after_opponent_reply_state": "K3_TEST", "precision": "ROLE_AND_REGION", "active_final_point": {"x_m": 0.0, "y_m": 0.0}, "stone_constraints_when_unambiguous": [], "dynamic_house_removal_binding_request": None, "after_own_occupancy": {"first": {"button": 1}, "opponent": {}}, "source_state": "OLD"}
        result = build(k1_transitions=[k1], k2_transitions=[k2], k2_templates=[template], min_direct_support=1)
        plan = result["state_plans"][0]
        self.assertEqual(plan["state_id"], "S2_LOCAL_ANCHOR_OPPONENT_HOUSE")
        self.assertEqual(plan["primary_goal"]["K"], 2)
        self.assertEqual(plan["primary_goal"]["direct_support"], 1)
