"""One-off timing smoke test for the full 4305-route planner grid."""

from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer


states = [{"enabled": False, "x": 0.0, "y": 0.0, "yaw": 0.0} for _ in range(16)]
states[1] = {"enabled": True, "x": 2.55, "y": 5.45, "yaw": 0.0}
planner = ProxyMatchPlayer(physics_seeds=3, parent_regions=3, decision_budget_seconds=90.0)
shot, detail = planner.choose(states, proxy_team=0, shot_index=2, match_seed=20260716)
print(
    "FULL_GRID_SMOKE_OK",
    shot,
    detail.get("initialCandidateCount"),
    detail.get("parentRegionCount"),
    detail.get("localContinuousCandidateCount"),
    detail.get("strictCandidateCount"),
    detail.get("plannerDecisionSeconds"),
    detail.get("plannerBudgetExceeded"),
    detail.get("mode"),
    flush=True,
)
