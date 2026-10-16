from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from training_research.inverse_dataset.cli import select_results, file_sha
from training_research.inverse_dataset.audit import audit_dataset
from training_research.inverse_dataset.sampling import load_scenes, shot_candidates
from training_research.inverse_dataset.schema import achieved_views
from training_research.inverse_dataset.selection import failure_reason, select_candidate, validate_selection
from training_research.tests.test_inverse_dataset import record


def criterion():
    return {"tactic": "double_hit", "first_contact_any": [1, 3], "require_single_first_contact": True,
            "required_collision_pairs": [[1, 3]],
            "goal": {"stones": {"1": {"type": "OUT_OF_PLAY"}, "3": {"type": "OUT_OF_PLAY"}}}}


def raw(seed, replicate, candidate=0):
    item = record()
    item.update(physics_seed=seed, scene_key="test", scene_id="manual", record_id=f"test:{candidate}:{replicate}",
                requested_scene={"selection": criterion()})
    return item


class SelectionTests(unittest.TestCase):
    def test_collision_evidence_and_actual_outcome_required(self):
        item = raw(1, 0)
        self.assertIsNone(failure_reason(item, criterion()))
        item["collision_events"] = []
        self.assertEqual(failure_reason(item, criterion()), "missing_collision_pair")
        item = raw(1, 0)
        item["physical_final"][1]["enabled"] = True
        self.assertEqual(failure_reason(item, criterion()), "goal_not_met")
        item = raw(1, 0)
        item["rule_violations"] = ["illegal"]
        self.assertEqual(failure_reason(item, criterion()), "rule_violation")
        item = raw(1, 0)
        item["prediction"]["settled"] = False
        self.assertEqual(failure_reason(item, criterion()), "unfinished")
        bad = criterion()
        bad.pop("required_collision_pairs")
        with self.assertRaises(ValueError):
            validate_selection(bad, 4)

    def test_seed_gate_counts_failures_and_preserves_requested_goal(self):
        rows = [raw(i + 1, i) for i in range(3)]
        rows[-1]["status"] = "error"
        self.assertFalse(select_candidate(rows, criterion(), 2, 1.)[0])
        chosen, evidence = select_candidate(rows, criterion(), 2, .66)
        self.assertEqual(len(chosen), 2)
        self.assertEqual(evidence["success_rate"], 2 / 3)
        view = achieved_views(chosen[0], 1)[0]
        self.assertEqual(view["view"], "selected_task")
        self.assertEqual(view["goal"], criterion()["goal"])
        self.assertNotIn("selected_task", rows[0])
        rows[1]["physics_seed"] = 1
        with self.assertRaises(ValueError):
            select_candidate(rows, criterion())

    def test_manual_boards_continuous_sampling(self):
        path = Path(__file__).parents[1] / "inverse_dataset/fixtures/manual_boards.json"
        scenes, rejected = load_scenes([str(path)], [])
        self.assertEqual(len(scenes), 4)
        self.assertFalse(rejected)
        for scene in scenes:
            shots = shot_candidates(scene, 64, 123, "uniform", [])
            self.assertEqual(shots, shot_candidates(scene, 64, 123, "uniform", []))
            self.assertEqual(len({tuple(s["shot"]) for s in shots}), 64)
            for shot in shots:
                for i, k in enumerate(("v", "h", "w")):
                    lo, hi = scene["shot_bounds"][k]
                    self.assertTrue(lo <= shot["shot"][i] <= hi)

    def test_filter_exports_one_requested_task_and_retains_source(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source"
            source.mkdir()
            path = source / "000000.raw.jsonl"
            rows = [raw(i + 1, i) for i in range(3)]
            failed = [raw(i + 1, i, 1) for i in range(3)]
            failed[-1]["status"] = "error"
            content = "".join(json.dumps(r) + "\n" for r in rows + failed)
            path.write_text(content, encoding="utf-8")
            output = Path(folder) / "selected"
            select_results(argparse.Namespace(raw_dir=source, output=output, goal_json=None, min_seeds=3,
                                              min_success_rate=1., views_per_result=1, split_seed=123))
            self.assertEqual(path.read_text(encoding="utf-8"), content)
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["selection_counts"]["accepted_candidates"], 1)
            self.assertEqual(manifest["summary"]["counts"]["samples"], 3)
            with np.load(output / "shards/000000.npz", allow_pickle=False) as packed:
                self.assertEqual(packed["stones"].shape, (3, 16, 14))
            metadata = [json.loads(s) for s in (output / "shards/000000.samples.jsonl").read_text().splitlines()]
            self.assertTrue(all(m["goal"] == criterion()["goal"] for m in metadata))
            self.assertEqual(len((output / "selected_shots.jsonl").read_text().splitlines()), 1)
            audit = audit_dataset(output)
            self.assertEqual(audit["counts"]["samples"], 3)
            self.assertTrue(audit["numeric_arrays_rebuilt_byte_equal"])
            # Recompute the archive hash after tampering: reconstruction must
            # catch the bad label even when the file checksum was updated.
            archive = output / "shards/000000.npz"
            with np.load(archive, allow_pickle=False) as packed:
                arrays = {k: packed[k].copy() for k in packed.files}
            arrays["actions"][0, 0] -= .1
            np.savez_compressed(archive, **arrays)
            manifest["shards"][0]["npz_sha256"] = file_sha(archive)
            (output / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "encoded numeric bytes differ"):
                audit_dataset(output)


if __name__ == "__main__":
    unittest.main()
