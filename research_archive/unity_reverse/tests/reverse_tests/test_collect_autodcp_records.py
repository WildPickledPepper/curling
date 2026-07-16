import tempfile
import unittest
from pathlib import Path

from tools.calibration.collect_autodcp_records import (
    archive_file,
    iter_candidate_files,
    load_existing_digests,
)


class CollectAutoDcpRecordsTest(unittest.TestCase):
    def make_tempdir(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name)

    def write_record(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            """
[0000]
BESTSHOT = BESTSHOT 3.0 0.0 0.0
RANDSEED = 1234
""".strip(),
            encoding="utf-8",
        )

    def test_iter_candidate_files_skips_own_outputs(self):
        root = self.make_tempdir()
        source = root / "Records" / "fresh.save"
        archive_dir = root / "data" / "calibration" / "autodcp_records"
        archived = archive_dir / "old.save"
        jsonl = root / "data" / "calibration" / "autodcp_records.jsonl"
        self.write_record(source)
        self.write_record(archived)
        jsonl.parent.mkdir(parents=True, exist_ok=True)
        jsonl.write_text("BESTSHOT RANDSEED\n", encoding="utf-8")

        candidates = iter_candidate_files(
            [root],
            max_bytes=20_000,
            excluded_roots=[archive_dir],
            excluded_files=[jsonl],
        )

        self.assertEqual(candidates, [source.resolve()])

    def test_existing_archive_digest_prevents_rearchive_after_restart(self):
        root = self.make_tempdir()
        source = root / "Records" / "fresh.save"
        archive_dir = root / "archive"
        archived = archive_dir / "old.save"
        jsonl = root / "records.jsonl"
        self.write_record(source)
        self.write_record(archived)

        seen = load_existing_digests(archive_dir)
        with jsonl.open("a", encoding="utf-8") as handle:
            archived_new_file = archive_file(source, archive_dir, seen, handle)

        self.assertFalse(archived_new_file)
        self.assertEqual(len(list(archive_dir.iterdir())), 1)

    def test_plain_text_trace_word_is_not_a_record_candidate(self):
        root = self.make_tempdir()
        paper = root / "paper.txt"
        paper.write_text("Eligibility TRACE appears here, but this is not a Unity record.\n", encoding="utf-8")

        candidates = iter_candidate_files([root], max_bytes=20_000)

        self.assertEqual(candidates, [])


if __name__ == "__main__":
    unittest.main()
