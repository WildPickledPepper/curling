import unittest

from tools.calibration.build_controlled_sampling_plan import build_plan


class BuildControlledSamplingPlanTest(unittest.TestCase):
    def test_plan_covers_required_scene_families(self):
        plan = build_plan()
        categories = {row["category"] for row in plan}

        self.assertIn("repeat", categories)
        self.assertIn("no_collision", categories)
        self.assertIn("sweep_window", categories)
        self.assertIn("collision_headon", categories)
        self.assertIn("collision_glancing", categories)
        self.assertIn("collision_double", categories)
        self.assertIn("collision_with_sweep", categories)
        self.assertIn("boundary", categories)

    def test_plan_labels_are_unique_and_sweep_grid_is_present(self):
        plan = build_plan()
        labels = [row["label"] for row in plan]
        sweeps = sorted({row["sweep"] for row in plan if row["category"] == "sweep_window"})

        self.assertEqual(len(labels), len(set(labels)))
        self.assertEqual(sweeps, [0.0, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0])

    def test_collision_rows_have_placed_stones(self):
        plan = build_plan()
        collision_rows = [row for row in plan if row["category"].startswith("collision")]

        self.assertGreater(len(collision_rows), 0)
        self.assertTrue(all(row["stones"] for row in collision_rows))


if __name__ == "__main__":
    unittest.main()
