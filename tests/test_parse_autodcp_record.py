import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.reverse.parse_autodcp_record import parse_record
from tools.reverse.recovered_curling_motion import RecoveredUnityRandom, unity_friction


class ParseAutoDcpRecordTest(unittest.TestCase):
    def make_record(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "sample.save"
        path.write_text(
            """
[LASTSTATE]
LASTSTATE = 0001

[0000]
BESTSHOT = BESTSHOT 3.1 -0.2 4.5
RANDSEED = 12345
SWEEP = SWEEP 4.25
POSITION = POSITION 0 0 1.2 3.4
SETSTATE = SETSTATE 0 0 1 0
SCORE = SCORE 1 -1
TRACE = 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63

[0001]
BESTSHOT = BESTSHOT 2.8 0 0
RANDSEED = 67890
""".strip(),
            encoding="utf-8",
        )
        return path

    def test_parse_record_extracts_replay_fields(self):
        record = parse_record(self.make_record())

        self.assertEqual(record.last_state, "0001")
        self.assertEqual(len(record.shots), 2)

        first = record.shots[0]
        self.assertEqual(first.section, "0000")
        self.assertEqual(first.end, 0)
        self.assertEqual(first.shot, 0)
        self.assertEqual(first.bestshot_velocity, 3.1)
        self.assertEqual(first.bestshot_offset, -0.2)
        self.assertEqual(first.bestshot_rotation, 4.5)
        self.assertEqual(first.randseed, 12345)
        self.assertEqual(first.sweep_distance, 4.25)
        self.assertEqual(first.position, [0.0, 0.0, 1.2, 3.4])
        self.assertEqual(first.setstate, [0, 0, 1, 0])
        self.assertEqual(first.score, [1, -1])
        self.assertIsNotNone(first.trace)
        self.assertEqual(first.trace_frames, 2)
        self.assertEqual(first.trace[0], [float(value) for value in range(32)])
        self.assertEqual(first.trace[1], [float(value) for value in range(32, 64)])
        self.assertTrue(first.has_replay_seed)

    def test_parse_record_rejects_incomplete_trace_frame(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "bad_trace.save"
        path.write_text(
            """
[0000]
BESTSHOT = BESTSHOT 3.1 -0.2 4.5
RANDSEED = 12345
TRACE = 1 2 3
""".strip(),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "32 floats per frame"):
            parse_record(path)

    def test_cli_jsonl_includes_recovered_friction_preview(self):
        path = self.make_record()
        result = subprocess.run(
            [
                sys.executable,
                "tools/reverse/parse_autodcp_record.py",
                str(path),
                "--jsonl",
                "--friction-preview",
                "2",
            ],
            check=True,
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            capture_output=True,
        )
        first = json.loads(result.stdout.splitlines()[0])
        rng = RecoveredUnityRandom.from_seed(12345)
        expected = [unity_friction(False, rng=rng, noise=None) for _ in range(2)]

        self.assertEqual(first["section"], "0000")
        self.assertEqual(first["randseed"], 12345)
        self.assertEqual(first["friction_preview"], expected)


if __name__ == "__main__":
    unittest.main()
