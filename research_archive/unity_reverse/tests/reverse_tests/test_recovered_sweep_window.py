import unittest

from tools.reverse.recovered_sweep_window import (
    HOGLINE2_PROTOCOL_Y,
    MAX_SWEEP_DISTANCE,
    MIDLINE_CENTER_PROTOCOL_Y,
    MIDLINE_TRIGGER_PROTOCOL_Y,
    is_sweeping_at_protocol_y,
    sweep_window,
)


class RecoveredSweepWindowTest(unittest.TestCase):
    def test_sweep_distance_maps_to_protocol_y_window(self):
        window = sweep_window(2.0)

        self.assertAlmostEqual(window.start_y, MIDLINE_TRIGGER_PROTOCOL_Y)
        self.assertAlmostEqual(window.end_y, MIDLINE_CENTER_PROTOCOL_Y - 2.0)
        self.assertAlmostEqual(window.capped_distance, 2.0)

    def test_sweep_window_caps_at_hogline2(self):
        window = sweep_window(999.0)

        self.assertAlmostEqual(window.capped_distance, MAX_SWEEP_DISTANCE)
        self.assertAlmostEqual(window.end_y, HOGLINE2_PROTOCOL_Y)

    def test_sweeping_active_after_midline_trigger_until_end_y(self):
        window = sweep_window(1.0)

        self.assertFalse(is_sweeping_at_protocol_y(window.start_y + 0.001, 1.0))
        self.assertTrue(is_sweeping_at_protocol_y(window.start_y, 1.0))
        self.assertTrue(is_sweeping_at_protocol_y(window.end_y + 0.001, 1.0))
        self.assertFalse(is_sweeping_at_protocol_y(window.end_y, 1.0))
        self.assertFalse(is_sweeping_at_protocol_y(window.end_y - 0.001, 1.0))
        self.assertFalse(is_sweeping_at_protocol_y(window.start_y, None))


if __name__ == "__main__":
    unittest.main()
