import unittest

from planning_proxy.tactical_library_strategy.contextual_fine_retriever import ContextualFineRetriever, board_distance, contextual_regions_as_fine_options


class ContextualFineRetrieverTests(unittest.TestCase):
    def test_retrieves_region_from_nearest_same_goal_examples(self):
        artifact = {"examples_by_goal_id": {"G": [
            {"panel_key": "1:1", "match_id": 1, "source_state": "K4_S", "K": 4,
             "before_board_canonical": [{"owner": "opponent", "x_m": 0.0, "y_m": 0.2}],
             "active_final_point_canonical": {"x_m": 0.3, "y_m": 0.4}},
            {"panel_key": "2:1", "match_id": 2, "source_state": "K4_S", "K": 4,
             "before_board_canonical": [{"owner": "opponent", "x_m": 2.0, "y_m": 2.0}],
             "active_final_point_canonical": {"x_m": -1.2, "y_m": 0.4}},
        ]}}
        candidate = {"source_state": "K4_S", "goal_id": "G", "K": 4}
        result = ContextualFineRetriever(artifact).retrieve([{"owner": "opponent", "x_m": 0.0, "y_m": 0.2}], candidate)
        self.assertEqual(result["retrieval_status"], "CONTEXTUAL_FINE_REGIONS_AVAILABLE")
        self.assertAlmostEqual(result["regions"][0]["active_final_region"]["centre_x_m"], 0.3)
        self.assertEqual(contextual_regions_as_fine_options(result)[0]["historical_support"], 1)

    def test_distance_is_zero_for_identical_board(self):
        board = [{"owner": "first", "x_m": 0.1, "y_m": 0.2}]
        self.assertEqual(board_distance(board, board), 0.0)


if __name__ == "__main__":
    unittest.main()
