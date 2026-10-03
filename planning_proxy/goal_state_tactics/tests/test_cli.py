import json
import tempfile
import unittest
from pathlib import Path

from planning_proxy.goal_state_tactics.cli import load_board


class GoalStateCliTests(unittest.TestCase):
    def test_load_board_accepts_wrapped_board(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "board.json"
            path.write_text(json.dumps({"board": [{"index": 1, "owner": "opponent", "x": 2.0, "y": 3.0}]}), encoding="utf-8")
            self.assertEqual(load_board(path)[0]["index"], 1)

    def test_load_board_rejects_missing_runtime_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "board.json"
            path.write_text(json.dumps([{"index": 1, "owner": "opponent"}]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "x/y"):
                load_board(path)


if __name__ == "__main__":
    unittest.main()
