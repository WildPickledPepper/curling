import json
import tempfile
import unittest
from pathlib import Path

from tools.reverse.summarize_collision_alignment import build_report


def _sample(sample_id, target_index, metadata=None):
    return {
        "sample_id": sample_id,
        "label": f"sample_{sample_id}",
        "category": "collision_headon",
        "collision_observed": True,
        "sent_sweep": False,
        "target_indices": [target_index],
        "active_move": {"index": 0},
        "plan_metadata": metadata or {},
    }


class SummarizeCollisionAlignmentTest(unittest.TestCase):
    def test_report_tracks_pass_fail_cleared_and_session_reuse(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        samples_path = root / "samples.jsonl"
        probe_path = root / "probe.json"

        samples = [
            _sample(1, 2, {"batch_repeat_index": 0, "source_sample_id": 78}),
            _sample(2, 3, {"batch_repeat_index": 0, "source_sample_id": 80}),
            _sample(3, 2, {"batch_repeat_index": 0, "source_sample_id": 82}),
            _sample(4, 2, {"batch_repeat_index": 1, "source_sample_id": 78}),
        ]
        samples_path.write_text("\n".join(json.dumps(row) for row in samples) + "\n", encoding="utf-8")
        probe_path.write_text(
            json.dumps(
                {
                    "result_sets": [
                        {
                            "config": {"dt": 0.01},
                            "summary": {},
                            "rows": [
                                {
                                    "sample_id": 1,
                                    "unity_target_in_play": True,
                                    "active_error": 0.01,
                                    "target_error": 0.015,
                                },
                                {
                                    "sample_id": 2,
                                    "unity_target_in_play": True,
                                    "active_error": 0.012,
                                    "target_error": 0.03,
                                },
                                {
                                    "sample_id": 3,
                                    "unity_target_in_play": False,
                                    "active_error": 0.005,
                                },
                                {
                                    "sample_id": 4,
                                    "unity_target_in_play": True,
                                    "active_error": 0.006,
                                    "target_error": 0.007,
                                },
                            ],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )

        report = build_report(
            samples_path=samples_path,
            probe_path=probe_path,
            result_index=0,
            threshold_m=0.02,
        )

        self.assertEqual(report["summary"]["sample_count"], 4)
        self.assertEqual(report["summary"]["full_in_play_pass_count"], 2)
        self.assertEqual(report["summary"]["target_cleared_unmodeled_count"], 1)
        self.assertEqual(report["summary"]["failed_in_play_sample_ids"], [2])
        self.assertTrue(report["summary"]["same_session_target_reuse_detected"])
        self.assertEqual(report["by_session"]["batch:1"]["sample_count"], 1)
        self.assertIn("78", report["by_source_case"])


if __name__ == "__main__":
    unittest.main()
