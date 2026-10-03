import unittest

from planning_proxy.competition_rules import HOUSE_X, HOUSE_Y
from planning_proxy.goal_state_tactics.proposer import propose_goal_states


K1_EMPTY = "K1_CORE[control=NONE_OR_UNCERTAIN;F_house=0;O_house=0;F_centre_guard=0;O_centre_guard=0;F_wing_guard=0;O_wing_guard=0]"
K6_DOUBLE = "K6_CORE[control=OPPONENT;F_house=0;O_house=2P;F_centre_guard=0;O_centre_guard=0;F_wing_guard=0;O_wing_guard=0]"


def fine_edge():
    return {
        "edge_id": "fine_guard", "runtime_candidate": True, "source_state": K1_EMPTY,
        "support": 50, "evidence_status": "HISTORICAL_TEMPLATE",
        "active_final_region": {"shape": "circle", "centre_x_m": 0.0, "centre_y_m": 2.2, "radius_m": 0.16},
        "stone_constraints_when_unambiguous": [],
        "after_own_occupancy": {"first": {}, "opponent": {}},
        "expected_own_after_states": [{"state": "K1_CORE[guard]", "count": 50, "share": 1.0}],
        "expected_after_reply_states": [{"state": "K2_CORE[reply]", "count": 20, "share": 0.4}],
    }


def collision_family():
    return {
        "collision_family_id": "family_double", "runtime_candidate_for_physx_screen": True,
        "source_collision_state": "K6_COLLISION[control=OPPONENT;F_house=0;O_house=2P;F_guards=N;O_guards=N]",
        "support": 35, "evidence_status": "HISTORICAL_COLLISION_FAMILY",
        "dynamic_binding_request": {"choose_count": 2},
        "observed_own_after_states": [{"value": "K6_CORE[open]", "count": 12, "share": 0.34}],
        "observed_after_reply_states": [{"value": "K7_CORE[reply]", "count": 10, "share": 0.29}],
    }


def single_collision_family():
    result = collision_family().copy()
    result["collision_family_id"] = "family_single"
    result["support"] = 90
    result["dynamic_binding_request"] = {"choose_count": 1}
    return result


def zone_fallback():
    return {
        "fallback_id": "k5_zone", "source_zone_state": "K5_6_ZONE[control=FIRST;F_house=1;O_house=0]",
        "support": 44, "evidence_status": "HISTORICAL_ZONE_FALLBACK",
        "active_final_region": {"shape": "circle", "centre_x_m": 0.0, "centre_y_m": 2.4, "radius_m": 0.32},
        "expected_own_after_states": [{"state": "K5_CORE[observed]", "count": 8, "share": 0.18}],
        "expected_after_reply_states": [{"state": "K6_CORE[observed]", "count": 7, "share": 0.16}],
    }


class GoalProposerTests(unittest.TestCase):
    def test_eighth_own_throw_marks_goal_for_mandatory_last_reply_search(self):
        eighth_zone = zone_fallback().copy()
        eighth_zone["source_zone_state"] = "K7_8_ZONE[control=NONE_OR_UNCERTAIN;F_house=0;O_house=0]"
        result = propose_goal_states([], 8, active_stone_index=14, fine_edges=[], collision_families=[], zone_fallbacks=[eighth_zone])
        self.assertEqual(len(result.proposals), 1)
        self.assertTrue(result.proposals[0].goal.require_last_reply_search)

    def test_fine_goal_translates_button_centred_region_to_local_physx(self):
        result = propose_goal_states([], 1, active_stone_index=0, fine_edges=[fine_edge()], collision_families=[], zone_fallbacks=[])
        self.assertEqual(len(result.proposals), 1)
        proposal = result.proposals[0]
        active = proposal.bound_stone_constraints[0]
        self.assertEqual(active.stone_index, 0)
        self.assertAlmostEqual(active.final_region.centre_x, HOUSE_X)
        self.assertAlmostEqual(active.final_region.centre_y, HOUSE_Y + 2.2)
        self.assertEqual([(item.owner, item.min_count, item.max_count) for item in proposal.goal.occupancy_constraints], [("self", 0, 0), ("opponent", 0, 0)])
        self.assertEqual(proposal.goal.priority, 1)

    def test_collision_goal_binds_the_actual_two_opponent_house_slots(self):
        board = [
            {"index": 4, "owner": "opponent", "x": HOUSE_X - 0.1, "y": HOUSE_Y},
            {"index": 8, "owner": "opponent", "x": HOUSE_X + 0.2, "y": HOUSE_Y + 0.1},
        ]
        result = propose_goal_states(board, 6, fine_edges=[], collision_families=[collision_family()], zone_fallbacks=[])
        self.assertEqual(result.runtime_core_state, K6_DOUBLE)
        self.assertEqual(len(result.proposals), 1)
        bound = result.proposals[0].bound_stone_constraints
        self.assertEqual({item.stone_index for item in bound}, {4, 8})
        self.assertTrue(all(item.disposition == "OUT_OF_PLAY" for item in bound))

    def test_collision_orders_double_before_historical_single_removal_fallback(self):
        board = [
            {"index": 4, "owner": "opponent", "x": HOUSE_X - 0.1, "y": HOUSE_Y},
            {"index": 8, "owner": "opponent", "x": HOUSE_X + 0.2, "y": HOUSE_Y + 0.1},
        ]
        result = propose_goal_states(board, 6, fine_edges=[], collision_families=[single_collision_family(), collision_family()], zone_fallbacks=[])
        self.assertEqual([len(item.bound_stone_constraints) for item in result.proposals], [2, 1, 1])
        self.assertEqual(
            result.proposals[0].goal.fallback_transition_ids,
            tuple(item.goal.transition_id for item in result.proposals[1:]),
        )

    def test_zone_fallback_is_available_without_precise_or_collision_edge(self):
        board = [{"index": 2, "owner": "self", "x": HOUSE_X, "y": HOUSE_Y}]
        result = propose_goal_states(board, 5, fine_edges=[], collision_families=[], zone_fallbacks=[zone_fallback()])
        self.assertEqual(result.runtime_zone_state, "K5_6_ZONE[control=FIRST;F_house=1;O_house=0]")
        self.assertEqual(len(result.proposals), 1)
        self.assertEqual(result.proposals[0].proposal_kind, "HISTORICAL_ZONE_FALLBACK")
        self.assertEqual(result.proposals[0].goal.occupancy_constraints, ())


if __name__ == "__main__":
    unittest.main()
