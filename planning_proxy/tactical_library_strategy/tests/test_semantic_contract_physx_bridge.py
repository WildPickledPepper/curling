import time
import unittest
from types import SimpleNamespace

from planning_proxy.tactical_library_strategy.semantic_contract_physx_bridge import (
    canonical_board_to_local,
    solve_semantic_placement_contracts,
    solve_semantic_placement_contracts_parallel,
)


def placement_contract():
    return {
        "contract_id": "G1:fine:0:binding:0", "state_id": "K1_EMPTY", "K": 1, "goal_id": "G1",
        "semantic_effect": {
            "first_house_delta": 1, "opponent_house_delta": 0,
            "opponent_removed_count": 0, "opponent_house_removed_count": 0,
        },
        "semantic_terminal_predicate": {"control": "FIRST", "macro": "FIRST_HOUSE_CONTROL"},
        "required_removed_stones": [],
        "active_final_region": {"shape": "circle", "centre_x_m": 0.0, "centre_y_m": 0.0, "radius_m": 0.15},
    }


class FakeSolver:
    def __init__(self, *, x=2.375, y=4.88):
        self.x, self.y = x, y
        self.calls = []

    def _try_fast_targeted_draw(self, **kwargs):
        self.calls.append(kwargs)
        seeds = kwargs["seeds"]
        evaluation = SimpleNamespace(
            rule_legal=True,
            final_boards=[[{"index": 0, "owner": "self", "x": self.x, "y": self.y, "enabled": True}] for _ in seeds],
            candidate=SimpleNamespace(v0=3.2, h0=0.1, w0=4.0),
        )
        return evaluation, {"solver": "fake"}


class SemanticContractPhysxBridgeTests(unittest.TestCase):
    def test_canonical_board_keeps_runtime_indices_and_converts_coordinate_frame(self):
        local = canonical_board_to_local([{"index": 7, "owner": "opponent", "x_m": -0.2, "y_m": 0.3}])
        self.assertEqual(local[0]["index"], 7)
        self.assertEqual(local[0]["owner"], "opponent")
        self.assertAlmostEqual(local[0]["x"], 2.175)
        self.assertAlmostEqual(local[0]["y"], 5.18)

    def test_certifies_the_full_semantic_contract_not_only_the_circle(self):
        solver = FakeSolver()
        attempts = solve_semantic_placement_contracts(
            [], [placement_contract()], own_throw_number=1, physics_seeds=3,
            decision_budget_seconds=1.0, solver=solver,
        )
        self.assertEqual(attempts[0].status, "CERTIFIED_SEMANTIC_CONTRACT")
        self.assertEqual(attempts[0].bestshot, (3.2, 0.1, 4.0))
        self.assertEqual(solver.calls[0]["shot_index"], 0)

    def test_rejects_a_circle_hit_when_the_complete_g_is_wrong(self):
        solver = FakeSolver(x=2.375, y=4.88)
        bad = placement_contract()
        bad["semantic_effect"] = {**bad["semantic_effect"], "first_house_delta": 0}
        attempts = solve_semantic_placement_contracts(
            [], [bad], own_throw_number=1, physics_seeds=1,
            decision_budget_seconds=1.0, solver=solver,
        )
        self.assertEqual(attempts[0].status, "REJECTED_BY_STRICT_SEMANTIC_CONTRACT")

    def test_does_not_weaken_a_removal_contract_to_a_draw(self):
        bad = placement_contract()
        bad["semantic_effect"] = {**bad["semantic_effect"], "opponent_removed_count": 1}
        attempts = solve_semantic_placement_contracts([], [bad], own_throw_number=1, solver=FakeSolver(), decision_budget_seconds=1.0)
        self.assertEqual(attempts[0].status, "UNSUPPORTED_NONPLACEMENT_CONTRACT")

    def test_parallel_interface_preserves_priority_for_independent_contracts(self):
        first, second = placement_contract(), placement_contract()
        first["contract_id"], second["contract_id"] = "unsupported-1", "unsupported-2"
        for contract in (first, second):
            contract["semantic_effect"] = {**contract["semantic_effect"], "opponent_removed_count": 1}
        attempts = solve_semantic_placement_contracts_parallel(
            [], [first, second], own_throw_number=1, physics_seeds=1,
            decision_budget_seconds=1.0, max_workers=2,
        )
        self.assertEqual([(item.contract_id, item.priority, item.status) for item in attempts], [
            ("unsupported-1", 1, "UNSUPPORTED_NONPLACEMENT_CONTRACT"),
            ("unsupported-2", 2, "UNSUPPORTED_NONPLACEMENT_CONTRACT"),
        ])


if __name__ == "__main__":
    unittest.main()
