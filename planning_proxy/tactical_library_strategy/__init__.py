"""独立先手战术库策略包；不接管既有 first_player_strategy。"""

from planning_proxy.tactical_library_strategy.strategy import (
    TacticalLibraryPlan,
    plan_first_player_from_tactical_library,
)
from planning_proxy.tactical_library_strategy.target_regions import (
    CandidateTargetRegion,
    TacticalTargetRegionPlan,
    candidate_target_regions,
)
from planning_proxy.tactical_library_strategy.physx_goal_bridge import (
    BoundCollisionGoalRequest,
    PhysxGoalAttempt,
    bind_contract_for_runtime_state,
    bind_single_collision_contract,
    solve_single_collision_requests,
    solve_clear_path_circle_requests,
)
from planning_proxy.tactical_library_strategy.double_outcome_goal import (
    BoundDoubleTargets,
    bind_double_target_sets,
    double_outcome_contract_met,
)
from planning_proxy.tactical_library_strategy.double_mads_solver import solve_double_outcome_contract
from training_data.nwnht_curling.causal_state_machine.runtime_goal_outcome_plan_v1 import (
    RuntimeGoalOutcomePlan,
    load_default as load_goal_outcome_runtime_plan,
)
from training_data.nwnht_curling.causal_state_machine.runtime_semantic_goal_mdp_v1 import (
    RuntimeSemanticGoalMdp,
    load_default as load_semantic_goal_mdp,
)
from planning_proxy.tactical_library_strategy.semantic_goal_contract import (
    instantiate_goal_contracts,
    instantiate_recommendation,
    semantic_transition_met,
)
from planning_proxy.tactical_library_strategy.contextual_fine_retriever import (
    ContextualFineRetriever,
    contextual_regions_as_fine_options,
    load_default as load_contextual_fine_retriever,
)
from planning_proxy.tactical_library_strategy.semantic_contract_physx_bridge import (
    SemanticPhysxAttempt,
    canonical_board_to_local,
    solve_semantic_placement_contracts,
    solve_semantic_placement_contracts_parallel,
    solve_semantic_single_removal_contracts,
    solve_semantic_single_removal_contracts_parallel,
    solve_semantic_double_removal_contracts,
    solve_semantic_mixed_collision_contracts,
    solve_semantic_mixed_collision_contracts_parallel,
)

__all__ = [
    "CandidateTargetRegion",
    "TacticalLibraryPlan",
    "TacticalTargetRegionPlan",
    "candidate_target_regions",
    "plan_first_player_from_tactical_library",
    "PhysxGoalAttempt",
    "BoundCollisionGoalRequest",
    "bind_contract_for_runtime_state",
    "bind_single_collision_contract",
    "solve_clear_path_circle_requests",
    "solve_single_collision_requests",
    "BoundDoubleTargets",
    "bind_double_target_sets",
    "double_outcome_contract_met",
    "solve_double_outcome_contract",
    "RuntimeGoalOutcomePlan",
    "load_goal_outcome_runtime_plan",
    "RuntimeSemanticGoalMdp",
    "load_semantic_goal_mdp",
    "instantiate_goal_contracts",
    "instantiate_recommendation",
    "semantic_transition_met",
    "ContextualFineRetriever",
    "load_contextual_fine_retriever",
    "contextual_regions_as_fine_options",
    "SemanticPhysxAttempt",
    "canonical_board_to_local",
    "solve_semantic_placement_contracts",
    "solve_semantic_placement_contracts_parallel",
    "solve_semantic_single_removal_contracts",
    "solve_semantic_single_removal_contracts_parallel",
    "solve_semantic_double_removal_contracts",
    "solve_semantic_mixed_collision_contracts",
    "solve_semantic_mixed_collision_contracts_parallel",
]
