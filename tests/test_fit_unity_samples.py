# -*- coding: utf-8 -*-
"""Tests for Unity calibration sample normalization."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "calibration"))

from fit_unity_samples import normalize_row


class FitUnitySamplesTest(unittest.TestCase):
    def test_requested_sweep_distance_is_used(self) -> None:
        row = normalize_row(
            {
                "requested_v0": 3.0,
                "requested_h0": 0.1,
                "requested_w0": -0.2,
                "requested_sweep_distance": 6.0,
                "final_x": 2.4,
                "final_y": 5.0,
                "in_play": True,
            }
        )

        self.assertIsNotNone(row)
        self.assertEqual(row["sweep"], 6.0)

    def test_legacy_requested_sweep_is_still_supported(self) -> None:
        row = normalize_row(
            {
                "requested_v0": 3.0,
                "requested_h0": 0.1,
                "requested_w0": -0.2,
                "requested_sweep": 2.0,
                "final_x": 2.4,
                "final_y": 5.0,
                "in_play": True,
            }
        )

        self.assertIsNotNone(row)
        self.assertEqual(row["sweep"], 2.0)


if __name__ == "__main__":
    unittest.main()
