import json
import tempfile
import unittest
from pathlib import Path

from tools.calibration.build_controlled_sampling_plan import build_plan
from tools.calibration.build_fresh_collision_plans import (
    build_fresh_plan_files,
    build_unique_active_target_probe_files,
    build_unique_target_batch_files,
    select_collision_cases,
)


class BuildFreshCollisionPlansTest(unittest.TestCase):
    def test_selects_no_sweep_single_collision_cases(self):
        cases = select_collision_cases(build_plan())

        self.assertGreater(len(cases), 0)
        self.assertTrue(all(row["category"] in {"collision_headon", "collision_glancing"} for row in cases))
        self.assertTrue(all(row["sweep"] == 0.0 for row in cases))
        self.assertTrue(all(row["stones"] for row in cases))

    def test_writes_one_shot_plans_and_manifest(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)

        manifest = build_fresh_plan_files(
            output_dir=root / "plans",
            manifest_path=root / "manifest.json",
            repeats=2,
            start_sample_id=500,
        )

        self.assertGreater(len(manifest), 0)
        self.assertTrue((root / "manifest.json").exists())
        self.assertTrue(all(row["requires_fresh_page"] for row in manifest))
        self.assertEqual(len({row["sample_id"] for row in manifest}), len(manifest))

        first_plan = Path(manifest[0]["plan_file"])
        payload = json.loads(first_plan.read_text(encoding="utf-8"))
        self.assertEqual(len(payload), 1)
        self.assertIn("source_sample_id", payload[0])
        self.assertIn("fresh_r00", payload[0]["label"])

    def test_writes_unique_target_batch_plans(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)

        manifest = build_unique_target_batch_files(
            output_dir=root / "batches",
            manifest_path=root / "batch_manifest.json",
            repeats=2,
            start_sample_id=700,
        )

        self.assertEqual(len(manifest), 2)
        self.assertTrue(all(row["requires_fresh_page_before_batch"] for row in manifest))
        self.assertTrue(all(row["requires_unique_target_indices"] for row in manifest))

        first_plan = Path(manifest[0]["plan_file"])
        payload = json.loads(first_plan.read_text(encoding="utf-8"))
        target_indices = [row["stones"][0]["index"] for row in payload]
        self.assertEqual(len(payload), len(select_collision_cases(build_plan())))
        self.assertEqual(len(target_indices), len(set(target_indices)))
        self.assertTrue(all(index >= 2 for index in target_indices))
        self.assertEqual(payload[0]["sample_id"], 700)
        self.assertIn("unique_t", payload[0]["label"])

    def test_writes_unique_active_target_probe_plans(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)

        manifest = build_unique_active_target_probe_files(
            output_dir=root / "role_probe",
            manifest_path=root / "role_manifest.json",
            repeats=1,
            start_sample_id=900,
        )

        self.assertEqual(len(manifest), 1)
        self.assertTrue(manifest[0]["requires_use_plan_active_index"])
        first_plan = Path(manifest[0]["plan_file"])
        payload = json.loads(first_plan.read_text(encoding="utf-8"))
        active_indices = [row["active_index"] for row in payload]
        target_indices = [row["stones"][0]["index"] for row in payload]

        self.assertEqual(len(active_indices), len(set(active_indices)))
        self.assertEqual(len(target_indices), len(set(target_indices)))
        self.assertFalse(set(active_indices) & set(target_indices))
        self.assertEqual(payload[0]["sample_id"], 900)
        self.assertEqual(payload[0]["assigned_active_index"], payload[0]["active_index"])
        self.assertEqual(payload[0]["assigned_target_index"], payload[0]["stones"][0]["index"])


if __name__ == "__main__":
    unittest.main()
