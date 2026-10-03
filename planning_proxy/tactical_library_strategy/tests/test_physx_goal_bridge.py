import unittest

from planning_proxy.tactical_library_strategy.physx_goal_bridge import (
    PLACEMENT_KIND,
    bind_single_collision_contract,
    collision_plan_for_request,
    draw_plan_for_circle,
    solve_clear_path_circle_requests,
)
from planning_proxy.tactical_library_strategy.v2_circle_goal_adapter import CircleGoalRequest


def request(*, kind=PLACEMENT_KIND, priority=1):
    return CircleGoalRequest(
        request_id=f"A|G{priority}", priority=priority, source_state="K1_V2_EMPTY_1", action_id="A",
        action_precision_level="NARROW_CROSS_FOLD_GOAL", action_kind=kind,
        local_centre_x=2.375, local_centre_y=5.10, radius_m=0.17,
        coverage_status="EXACT_SEMANTIC_REGION", expected_next_state_distribution=(), evidence_note="test",
    )


class FakeSolver:
    def __init__(self):
        self.calls = []

    def _try_fast_targeted_draw(self, **kwargs):
        self.calls.append(kwargs)
        return None


class PhysxGoalBridgeTests(unittest.TestCase):
    def test_compatibility_plan_preserves_only_the_circle_constraint(self):
        plan = draw_plan_for_circle(request(), own_throw_number=1, shot_index=0)
        self.assertEqual(plan.target_points, ((2.375, 5.10),))
        self.assertEqual(plan.landing_region_radius_m, 0.17)
        self.assertEqual(plan.opponent_action, "none")
        self.assertEqual(plan.phase, "v2_terminal_circle")

    def test_non_placement_request_is_not_relabelled_as_a_draw(self):
        attempts = solve_clear_path_circle_requests(
            [request(kind="COLLISION_CLEAR")], [], own_throw_number=1, solver=FakeSolver(), decision_budget_seconds=1,
        )
        self.assertEqual(attempts[0].status, "REQUIRES_COLLISION_GOAL_CONSTRAINTS")

    def test_clear_request_reaches_existing_solver_with_k1_slot_and_target(self):
        solver = FakeSolver()
        attempts = solve_clear_path_circle_requests(
            [request()], [], own_throw_number=1, solver=solver, decision_budget_seconds=1,
        )
        self.assertEqual(attempts[0].status, "NOT_FOUND_WITHIN_BUDGET")
        self.assertEqual(len(solver.calls), 1)
        self.assertEqual(solver.calls[0]["shot_index"], 0)
        self.assertEqual(solver.calls[0]["tactical_plan"].target_points, ((2.375, 5.10),))

    def test_collision_contract_binds_nearest_current_opponent_and_keeps_exact_out_semantics(self):
        contract = {
            "collision_goal_id": "C", "source_state": "K4_S", "tactical_goal_id": "A",
            "observed_template_kind": "SINGLE_OPPONENT_REMOVAL", "required_opponent_removed_count": 1,
            "target_binding": {"binding_mode": "DYNAMIC_OPPONENT_HOUSE_SET", "choose_count": 1},
            "active_target_region": {"kind": "CIRCLE", "centre_x_m": 0.0, "centre_y_m": 0.0, "max_radius_m": 0.61},
            "expected_next_state_distribution": [],
        }
        requests = bind_single_collision_contract(contract, [
            {"index": 3, "owner": "opponent", "x": 2.95, "y": 4.88},
            {"index": 5, "owner": "opponent", "x": 2.40, "y": 4.95},
        ])
        self.assertEqual([item.target_opponent_index for item in requests], [5, 3])
        plan = collision_plan_for_request(requests[0], own_throw_number=4, shot_index=6)
        self.assertEqual(plan.target_opponent_index, 5)
        self.assertEqual(plan.opponent_action, "physical_clear")
        self.assertEqual(plan.phase, "v2_collision_terminal")

    def test_mirrored_contract_reflects_lateral_region_before_tiling(self):
        contract = {
            "collision_goal_id": "C", "source_state": "K4_S", "tactical_goal_id": "A",
            "observed_template_kind": "SINGLE_OPPONENT_REMOVAL", "required_opponent_removed_count": 1,
            "target_binding": {"binding_mode": "DYNAMIC_OPPONENT_HOUSE_SET", "choose_count": 1},
            "active_target_region": {"kind": "CIRCLE", "centre_x_m": 0.40, "centre_y_m": 0.0, "max_radius_m": 0.17},
            "expected_next_state_distribution": [],
        }
        requests = bind_single_collision_contract(contract, [
            {"index": 5, "owner": "opponent", "x": 2.40, "y": 4.95},
        ], runtime_orientation_mirrored=True)
        self.assertEqual(len(requests), 1)
        self.assertAlmostEqual(requests[0].local_centre_x, 2.375 - 0.40)


if __name__ == "__main__":
    unittest.main()
