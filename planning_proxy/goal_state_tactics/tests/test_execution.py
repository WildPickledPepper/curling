import unittest

from planning_proxy.goal_state_tactics.execution import (
    SearchAttempt,
    StrictGoalSolution,
    accept_bound_goal,
    rank_same_state_k8_by_reply_pressure,
    rank_k8_proposal_set_by_reply_pressure,
    screen_all_strict_goals,
    solve_strict_goal_with_fallback,
    solve_with_fallback,
)
from planning_proxy.goal_state_tactics.last_reply import board_fingerprint, receipt_from_final_defence_reports
from planning_proxy.goal_state_tactics.last_reply import LastReplySearchReceipt
from planning_proxy.goal_state_tactics.models import CircleRegion, GoalState, OccupancyConstraint
from planning_proxy.goal_state_tactics.proposer import BoundStoneConstraint, GoalProposalSet, ProposedGoal


def proposal(identifier, *, require_last_reply_search=False, last_reply_policy="REQUIRE_SEARCH_RECORD"):
    goal = GoalState(
        identifier, 1, "S", "U", None,
        require_last_reply_search=require_last_reply_search,
        last_reply_policy=last_reply_policy,
    )
    return ProposedGoal(goal, (), "TEST", 1, "HISTORICAL_TEMPLATE", (), identifier)


def reply_report(board, *, screened_safe, counterexamples):
    return {
        "fixture": {"stones": board},
        "strictCandidateCount": 8,
        "counterexampleCandidateCount": counterexamples,
        "screenedSafe": screened_safe,
    }


class GoalExecutionTests(unittest.TestCase):
    def test_acceptance_requires_every_seed_to_satisfy_bound_constraints(self):
        region = CircleRegion("target", 2.0, 3.0, 0.2)
        constraints = (
            BoundStoneConstraint("active", 0, "self", "IN_REGION", region),
            BoundStoneConstraint("enemy", 3, "opponent", "OUT_OF_PLAY"),
        )
        accepted = accept_bound_goal(
            [[{"index": 0, "x": 2.05, "y": 3.05, "enabled": True}], [{"index": 0, "x": 2.02, "y": 3.01, "enabled": True}]],
            constraints, rule_legal=True,
        )
        self.assertTrue(accepted.accepted)
        rejected = accept_bound_goal(
            [[{"index": 0, "x": 2.05, "y": 3.05, "enabled": True}], [{"index": 0, "x": 2.02, "y": 3.01, "enabled": True}, {"index": 3, "x": 1.0, "y": 1.0, "enabled": True}]],
            constraints, rule_legal=True,
        )
        self.assertFalse(rejected.accepted)
        self.assertIn("enemy:still_in_play", rejected.failures_by_seed[1])

    def test_fallback_advances_after_no_solution(self):
        first, second = proposal("first"), proposal("second")
        proposal_set = GoalProposalSet(1, "S", "C", (first, second))
        result = solve_with_fallback(proposal_set, lambda item: None if item.goal.transition_id == "first" else "solution")
        self.assertEqual(result.selected.goal.transition_id, "second")
        self.assertEqual(result.solution, "solution")
        self.assertEqual(result.attempted_transition_ids, ("first", "second"))
        self.assertEqual(result.attempts[0].status, "NOT_FOUND_WITHIN_CURRENT_SEARCH_BUDGET")
        self.assertEqual(result.attempts[1].status, "ACCEPTED")

    def test_explicit_goal_rejection_is_not_mislabeled_as_search_failure(self):
        first, second = proposal("first"), proposal("second")
        proposal_set = GoalProposalSet(1, "S", "C", (first, second))
        result = solve_with_fallback(
            proposal_set,
            lambda item: SearchAttempt("REJECTED_BY_GOAL_GATE") if item.goal.transition_id == "first"
            else SearchAttempt("ACCEPTED", "solution"),
        )
        self.assertEqual(result.selected.goal.transition_id, "second")
        self.assertEqual([item.status for item in result.attempts], ["REJECTED_BY_GOAL_GATE", "ACCEPTED"])

    def test_explicit_safety_goal_rejects_reply_counterexample_then_uses_fallback(self):
        first = proposal(
            "first", require_last_reply_search=True, last_reply_policy="REQUIRE_NO_COUNTERPLAY",
        )
        second = proposal("second")
        proposal_set = GoalProposalSet(1, "S", "C", (first, second))
        final_board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        solution = StrictGoalSolution({"bestshot": [3.0, 0.0, 0.0]}, final_board, True)
        counterexample = receipt_from_final_defence_reports(
            final_board, [reply_report(final_board[0], screened_safe=False, counterexamples=1)],
            physics_seeds_per_candidate=3,
        )
        result = solve_strict_goal_with_fallback(
            proposal_set,
            lambda _proposal: SearchAttempt("ACCEPTED", solution),
            screen_last_reply=lambda _proposal, _solution: counterexample,
        )
        self.assertEqual(result.selected.goal.transition_id, "second")
        self.assertEqual(result.attempts[0].status, "REJECTED_BY_GOAL_GATE")
        self.assertEqual(result.attempts[1].status, "ACCEPTED")

    def test_default_k8_goal_records_counterplay_without_claiming_absolute_safety(self):
        first = proposal("first", require_last_reply_search=True)
        proposal_set = GoalProposalSet(1, "S", "C", (first,))
        final_board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        solution = StrictGoalSolution({}, final_board, True)
        counterexample = receipt_from_final_defence_reports(
            final_board, [reply_report(final_board[0], screened_safe=False, counterexamples=1)],
            physics_seeds_per_candidate=3,
        )
        result = solve_strict_goal_with_fallback(
            proposal_set,
            lambda _proposal: SearchAttempt("ACCEPTED", solution),
            screen_last_reply=lambda _proposal, _solution: counterexample,
        )
        self.assertEqual(result.selected.goal.transition_id, "first")
        self.assertEqual(result.solution.last_reply_receipt.status, "COUNTERPLAY_FOUND")

    def test_strict_executor_never_accepts_final_throw_without_reply_runner(self):
        first = proposal("first", require_last_reply_search=True)
        proposal_set = GoalProposalSet(1, "S", "C", (first,))
        final_board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        result = solve_strict_goal_with_fallback(
            proposal_set,
            lambda _proposal: SearchAttempt("ACCEPTED", StrictGoalSolution({}, final_board, True)),
        )
        self.assertIsNone(result.selected)
        self.assertEqual(result.attempts[0].status, "REJECTED_BY_GOAL_GATE")

    def test_k8_pressure_rank_requires_same_state_and_complete_receipts(self):
        first = proposal("first", require_last_reply_search=True)
        second = proposal("second", require_last_reply_search=True)
        quiet = LastReplySearchReceipt(
            "COUNTERPLAY_FOUND", strict_candidate_count=100, counterexample_count=12,
            stable_counterexample_count=12, direct_counterexample_count=0,
            impact_counterexample_count=12, complete_search=True,
        )
        direct = LastReplySearchReceipt(
            "COUNTERPLAY_FOUND", strict_candidate_count=100, counterexample_count=12,
            stable_counterexample_count=12, direct_counterexample_count=4,
            impact_counterexample_count=8, complete_search=True,
        )
        empty_board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        ranks = rank_same_state_k8_by_reply_pressure((
            (second, StrictGoalSolution({}, empty_board, True, direct)),
            (first, StrictGoalSolution({}, empty_board, True, quiet)),
        ))
        self.assertEqual([item.proposal.goal.transition_id for item in ranks], ["first", "second"])
        other_state = ProposedGoal(
            GoalState("third", 1, "OTHER", "U", None, require_last_reply_search=True),
            (), "TEST", 1, "HISTORICAL_TEMPLATE", (), "third",
        )
        with self.assertRaisesRegex(ValueError, "同一 source_state"):
            rank_same_state_k8_by_reply_pressure(((first, StrictGoalSolution({}, empty_board, True, quiet)), (other_state, StrictGoalSolution({}, empty_board, True, quiet))))

    def test_screen_all_keeps_multiple_k8_results_for_later_pressure_ranking(self):
        first, second = proposal("first", require_last_reply_search=True), proposal("second", require_last_reply_search=True)
        proposal_set = GoalProposalSet(8, "S", "C", (first, second))
        board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        fingerprints = (board_fingerprint(board[0]),)
        quiet = LastReplySearchReceipt(
            "COUNTERPLAY_FOUND", final_board_fingerprints=fingerprints, strict_candidate_count=100, counterexample_count=2,
            stable_counterexample_count=2, impact_counterexample_count=2, complete_search=True,
        )
        direct = LastReplySearchReceipt(
            "COUNTERPLAY_FOUND", final_board_fingerprints=fingerprints, strict_candidate_count=100, counterexample_count=2,
            stable_counterexample_count=2, direct_counterexample_count=1,
            impact_counterexample_count=1, complete_search=True,
        )
        screened = screen_all_strict_goals(
            proposal_set,
            lambda _: SearchAttempt("ACCEPTED", StrictGoalSolution({}, board, True)),
            screen_last_reply=lambda proposal, _: quiet if proposal.goal.transition_id == "first" else direct,
        )
        self.assertEqual(len(screened), 2)
        accepted = tuple((item.proposal, item.attempt.solution) for item in screened if item.attempt.status == "ACCEPTED")
        ranks = rank_same_state_k8_by_reply_pressure(accepted)
        self.assertEqual([item.proposal.goal.transition_id for item in ranks], ["first", "second"])
        proposal_ranks = rank_k8_proposal_set_by_reply_pressure(proposal_set, screened)
        self.assertEqual([item.proposal.goal.transition_id for item in proposal_ranks], ["first", "second"])

    def test_rule_violation_rejects_even_when_geometric_goal_matches(self):
        constraint = BoundStoneConstraint("active", 0, "self", "SURVIVE")
        verdict = accept_bound_goal([[{"index": 0, "x": 2.0, "y": 3.0, "enabled": True}]], (constraint,), rule_legal=False)
        self.assertFalse(verdict.accepted)
        self.assertIn("free_guard_or_other_rule_violation", verdict.failures_by_seed[0])

    def test_final_throw_goal_cannot_be_accepted_without_reply_search(self):
        constraint = BoundStoneConstraint("active", 0, "self", "SURVIVE")
        board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        blocked = accept_bound_goal(
            board, (constraint,), rule_legal=True,
            require_last_reply_search=True,
        )
        self.assertFalse(blocked.accepted)
        self.assertIn("last_reply_search_not_completed", blocked.failures_by_seed[0])
        receipt = receipt_from_final_defence_reports(
            board,
            [reply_report(board[0], screened_safe=True, counterexamples=0)],
            physics_seeds_per_candidate=3,
        )
        accepted = accept_bound_goal(
            board, (constraint,), rule_legal=True,
            require_last_reply_search=True, last_reply_receipt=receipt,
        )
        self.assertTrue(accepted.accepted)
        self.assertEqual(accepted.last_reply_search_status, "SCREENED_NO_COUNTERPLAY_WITHIN_CURRENT_SEARCH_BUDGET")

    def test_final_throw_records_counterplay_by_default_and_rejects_it_for_a_safety_goal(self):
        constraint = BoundStoneConstraint("active", 0, "self", "SURVIVE")
        board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        counter = receipt_from_final_defence_reports(
            board,
            [reply_report(board[0], screened_safe=False, counterexamples=1)],
            physics_seeds_per_candidate=3,
        )
        screened = accept_bound_goal(
            board, (constraint,), rule_legal=True,
            require_last_reply_search=True, last_reply_receipt=counter,
        )
        self.assertTrue(screened.accepted)
        self.assertEqual(screened.last_reply_search_status, "COUNTERPLAY_FOUND")
        rejected = accept_bound_goal(
            board, (constraint,), rule_legal=True,
            require_last_reply_search=True, last_reply_policy="REQUIRE_NO_COUNTERPLAY",
            last_reply_receipt=counter,
        )
        self.assertFalse(rejected.accepted)
        self.assertIn("last_reply_counterplay_found", rejected.failures_by_seed[0])
        other_board = [[{"index": 0, "owner": "self", "x": 2.1, "y": 3.0, "enabled": True}]]
        mismatched = accept_bound_goal(
            other_board, (constraint,), rule_legal=True,
            require_last_reply_search=True, last_reply_receipt=counter,
        )
        self.assertFalse(mismatched.accepted)
        self.assertIn("last_reply_search_board_mismatch", mismatched.failures_by_seed[0])

    def test_receipt_rejects_a_report_from_another_final_board(self):
        board = [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]]
        old_board = [{"index": 0, "owner": "self", "x": 2.1, "y": 3.0, "enabled": True}]
        receipt = receipt_from_final_defence_reports(
            board, [reply_report(old_board, screened_safe=True, counterexamples=0)],
            physics_seeds_per_candidate=3,
        )
        self.assertEqual(receipt.status, "SEARCH_ERROR")

    def test_occupancy_constraint_rejects_wrong_final_house_count(self):
        house = CircleRegion("house", 2.0, 3.0, 1.0)
        verdict = accept_bound_goal(
            [[{"index": 0, "owner": "self", "x": 2.0, "y": 3.0, "enabled": True}]], (),
            rule_legal=True, occupancy_constraints=(OccupancyConstraint("self", house, min_count=0, max_count=0),),
        )
        self.assertFalse(verdict.accepted)
        self.assertIn("occupancy:self:house:above_max", verdict.failures_by_seed[0])


if __name__ == "__main__":
    unittest.main()
    rank_same_state_k8_by_reply_pressure,
