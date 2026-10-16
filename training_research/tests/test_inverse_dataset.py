from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from training_research.inverse_dataset.cli import encode_shard
from training_research.inverse_dataset.sampling import FAMILIES, load_scenes, shot_candidates, synthetic_scene, validate_scene
from training_research.inverse_dataset.schema import (
    SCHEMA, achieved_views, encode_action, encode_input, goal_met, split_for_group,
)


def board():
    states = [{"index": i, "enabled": False, "x": 0.0, "y": 0.0, "yaw": 0.0} for i in range(16)]
    for i, x in ((1, 2.1), (3, 2.7)):
        states[i].update(enabled=True, x=x, y=4.88)
    return states


def record():
    before = board()
    after = board()
    for i in (1, 3):
        after[i]["enabled"] = False
    after[4].update(enabled=True, x=2.375, y=4.88)
    return {"schema": SCHEMA, "record_id": "test:0:0", "group_id": "game-a", "family": "double_pair", "status": "complete", "active_index": 4,
            "before": before, "physical_final": after, "shot": [4.2, 0.0, 0.0], "rule_violations": [],
            "prediction": {"settled": True, "contact": True, "firstContactTargets": [1]},
            "collision_events": [{"step": 3, "stones": [1, 3]}]}


class InverseDatasetTests(unittest.TestCase):
    def test_online_encoder_slot_binding_masks_and_normalization(self):
        states = board()
        states[1].pop("yaw")
        goal = {"stones": {"1": {"type": "OUT_OF_PLAY"}, "4": {"type": "IN_REGION", "x": 2.375, "y": 4.88, "radius": .3, "required": False}}}
        encoded = encode_input(states, goal, 4, "double_hit")
        self.assertEqual(encoded["stones"].shape, (16, 14))
        self.assertEqual(encoded["yaw"][1, 2], 0)
        self.assertEqual(encoded["stones"][1, 7], 1)
        self.assertTrue(np.all(encoded["stones"][1, 10:13] == 0))
        self.assertEqual(encoded["stones"][4, 6], 1)
        self.assertEqual(encoded["stones"][4, 4], 1)
        self.assertEqual(encoded["stones"][4, 13], 0)
        self.assertTrue(np.all(encoded["stones"][4, 10:12] == 0))
        self.assertEqual(encoded["stones"][2, 5], 1)
        self.assertTrue(np.all(encoded["stones"][2, 10:14] == 0))
        np.testing.assert_array_equal(encode_action([6.0, -2.23, 15.7]), [1, -1, 1])
        with self.assertRaises(ValueError):
            encode_action([6.001, 0, 0])

    def test_house_clear_is_not_out_of_play(self):
        states = board()
        states[1]["y"] = 9.0
        self.assertTrue(goal_met(states, {"stones": {"1": {"type": "OUT_OF_HOUSE"}}}))
        self.assertFalse(goal_met(states, {"stones": {"1": {"type": "OUT_OF_PLAY"}}}))

    def test_no_false_double_or_illegal_positive_labels(self):
        raw = record()
        views = achieved_views(raw)
        self.assertIn("double_hit", [v["tactic"] for v in views])
        self.assertTrue(all(goal_met(raw["physical_final"], v["goal"]) for v in views))
        raw["collision_events"] = []
        self.assertNotIn("double_hit", [v["tactic"] for v in achieved_views(raw)])
        raw["collision_events"] = [{"stones": [1, 3]}]
        raw["physical_final"][3].update(enabled=True, x=2.7, y=4.88)
        self.assertNotIn("double_hit", [v["tactic"] for v in achieved_views(raw)])
        raw["rule_violations"] = ["protected guard removed"]
        self.assertEqual(achieved_views(raw), [])
        raw["rule_violations"] = []
        raw["prediction"]["settled"] = False
        self.assertEqual(achieved_views(raw), [])

    def test_sampling_reproducibility_separation_and_grid(self):
        families = set()
        for i in range(160):
            scene = synthetic_scene(i, 123)
            self.assertEqual(scene, synthetic_scene(i, 123))
            families.add(scene["family"])
            self.assertTrue(all(s["index"] < scene["active_index"] for s in scene["stones"]))
            shots = shot_candidates(scene, 12, 123, "mixed", [])
            self.assertEqual(shots, shot_candidates(scene, 12, 123, "mixed", []))
            for shot in shots:
                encode_action(shot["shot"])
        self.assertEqual(families, set(FAMILIES))
        grid = shot_candidates(scene, 1, 0, "grid", [[3, 6], [-1, 1], [-10, 0, 10]])
        self.assertEqual(len(grid), 12)
        self.assertEqual(len({tuple(x["shot"]) for x in grid}), 12)

    def test_import_deduplicates_and_reports_bad_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scenes.json"
            scene = {"active_index": 2, "stones": [{"index": 1, "x": 2.375, "y": 4.88}]}
            source.write_text(json.dumps([scene, scene, {"active_index": 2, "stones": [{"index": 2, "x": 2.375, "y": 4.88}]}]), encoding="utf-8")
            scenes, rejected = load_scenes([str(source)], [])
            self.assertEqual(len(scenes), 1)
            self.assertEqual(len(rejected), 1)

    def test_supplied_candidate_is_replayed_with_effective_clamp(self):
        scene = synthetic_scene(3, 99)
        scene["candidate_shots"] = [[10.0, 2.5, 20.0]]
        shots = shot_candidates(scene, 12, 123, "mixed", [])
        self.assertEqual(shots[0], {"shot": [6.0, 2.23, 15.7], "origin": "supplied_initial"})
        encode_action(shots[0]["shot"])

    def test_import_accepts_touching_stones_but_rejects_overlap(self):
        scene = {"active_index": 4, "stones": [{"index": 1, "x": 2.0, "y": 4.88}, {"index": 3, "x": 2.29, "y": 4.88}]}
        self.assertEqual(len(validate_scene(scene)["stones"]), 2)
        scene["stones"][1]["x"] = 2.1
        with self.assertRaises(ValueError):
            validate_scene(scene)

    def test_shards_no_final_state_leakage_and_group_consistent_split(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = record()
            raw2 = record()
            raw2["record_id"] = "test:1:1"
            raw2["physical_final"][4]["x"] = 2.5
            path = Path(directory) / "input.raw.jsonl"
            path.write_text("\n".join(json.dumps(r) for r in (raw, raw2)) + "\n", encoding="utf-8")
            summary = encode_shard(path, Path(directory) / "output", 8, 42)
            self.assertEqual(summary["counts"]["records"], 2)
            with np.load(Path(directory) / "output.npz", allow_pickle=False) as arrays:
                self.assertGreater(len(arrays["actions"]), 2)
                self.assertEqual(set(arrays["split"].tolist()), {split_for_group("game-a", 42)})
                # The shooter is not yet released: achieved target coordinates
                # appear only in goal columns, never current-position columns.
                self.assertTrue(np.all(arrays["stones"][:, 4, :2] == 0))
                self.assertTrue(np.all(arrays["stones"][:, 4, 2] == 0))
                self.assertNotIn("physics_seed", arrays.files)
                self.assertNotIn("physical_final", arrays.files)
                self.assertEqual(arrays["actions"].dtype, np.float32)
                self.assertEqual(arrays["stones"].shape[1:], (16, 14))


if __name__ == "__main__":
    unittest.main()
