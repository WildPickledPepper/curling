import copy
import gzip
import json
from pathlib import Path
import tempfile
import unittest

from training_research.compact_pairs import iter_pairs, references_for_requests, request_fingerprint


class CompactPairingTests(unittest.TestCase):
    def write_pair(self, directory, stem, goal_x, shot):
        request = {"record_id": "reused-id", "scene_key": "board", "active_index": 1,
                   "stones": [{"index": 0, "x": 2., "y": 4., "yaw": .1}],
                   "selection": {"tactic": "achieved_goal", "goal": {"stones": {
                       "1": {"type": "IN_REGION", "x": goal_x, "y": 4.8, "radius": .15}}}}}
        reference = {"record_id": "reused-id", "shot": shot, "physics_seed": 7}
        for kind, row in (("inputs", request), ("references", reference)):
            with gzip.open(directory/(stem+"."+kind+".jsonl.gz"), "wt", encoding="utf-8") as stream:
                stream.write(json.dumps(row)+"\n")
        return request

    def test_reused_ids_are_resolved_by_their_exact_original_requests(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            a = self.write_pair(data, "a", 2., [3., 0., 0.])
            b = self.write_pair(data, "b", 3., [4., .2, 5.])
            pairs = list(iter_pairs(data))
            self.assertEqual([p[1]["shot"] for p in pairs], [[3., 0., 0.], [4., .2, 5.]])
            found = references_for_requests(data, [a, b])
            self.assertEqual(found[request_fingerprint(a)]["shot"], [3., 0., 0.])
            self.assertEqual(found[request_fingerprint(b)]["shot"], [4., .2, 5.])
            seeds = references_for_requests(data, [a, b], seeds_only=True)
            self.assertTrue(all(set(r) == {"physics_seed", "paired_location"} for r in seeds.values()))
            derived = copy.deepcopy(a)
            derived["task_key"] = "derived"
            derived["stones"][0]["yaw_source"] = "supplied"
            self.assertEqual(request_fingerprint(derived), request_fingerprint(a))

    def test_unmatched_rows_are_rejected_instead_of_silently_truncated(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            self.write_pair(data, "a", 2., [3., 0., 0.])
            with gzip.open(data/"a.references.jsonl.gz", "at", encoding="utf-8") as stream:
                stream.write(json.dumps({"record_id": "extra"})+"\n")
            with self.assertRaisesRegex(ValueError, "different lengths"):
                list(iter_pairs(data))


if __name__ == "__main__":
    unittest.main()
