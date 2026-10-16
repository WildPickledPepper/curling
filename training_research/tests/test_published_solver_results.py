"""Published claims must agree with the frozen requests and recorded outcomes."""
import gzip
import hashlib
import json
from pathlib import Path
import statistics
import unittest

from training_research.compact_pairs import request_fingerprint
from training_research.inverse_dataset.selection import failure_reason


ROOT = Path(__file__).resolve().parents[1]


class PublishedSolverResultsTests(unittest.TestCase):
    def test_frozen_catalogues_and_disjoint_partitions(self):
        root = ROOT / 'benchmarks'
        manifest = json.loads((root / 'catalogs/manifest_20261016.json').read_text(encoding='utf-8'))
        catalogs = {}
        for name, item in manifest['catalogs'].items():
            compressed = (root / item['file']).read_bytes()
            self.assertEqual(hashlib.sha256(compressed).hexdigest(), item['gzip_sha256'])
            raw = gzip.decompress(compressed)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item['uncompressed_sha256'])
            requests = json.loads(raw)
            keys = {request_fingerprint(r) for r in requests}
            self.assertEqual(len(keys), item['tasks'])
            self.assertEqual(len({r['scene_key'] for r in requests}), item['physical_boards'])
            self.assertTrue(all('shot' not in r and 'physics_seed' not in r for r in requests))
            catalogs[name] = keys
        a, b = catalogs['development306_20261016'], catalogs['additional398_20261016']
        self.assertFalse(a & b)
        self.assertEqual(a | b, catalogs['development704_20261016'])
        self.assertTrue(catalogs['hard23_20261016'] <= a | b)
        self.assertFalse(catalogs['validation1024_20261016'] & (a | b))

    def test_all_published_successes_satisfy_the_original_complete_contract(self):
        root = ROOT / 'benchmarks'
        catalog = json.loads(gzip.decompress((root / 'catalogs/development704_20261016.json.gz').read_bytes()))
        cases = [
            ('wide_dfols704_20261016', 'compact_search_20261016_fullrequest_audit_summary.json', 'corrected_combined_metrics'),
            ('full_augmented704_20261016', 'compact_search_full_augmented704_paired_20261016_summary.json', 'metrics'),
        ]
        for name, summary_file, metric_key in cases:
            with self.subTest(profile=name):
                metadata = json.loads((root / ('certificates/'+name+'_manifest.json')).read_text(encoding='utf-8'))
                compressed = (root / metadata['file']).read_bytes()
                self.assertEqual(hashlib.sha256(compressed).hexdigest(), metadata['gzip_sha256'])
                rows = [json.loads(line) for line in gzip.decompress(compressed).decode().splitlines()]
                self.assertEqual(len(rows), 704)
                self.assertEqual([r['request_fingerprint'] for r in rows], [request_fingerprint(r) for r in catalog])
                for row in rows:
                    self.assertEqual(row['request_fingerprint'], request_fingerprint(row['request']))
                    if row['success']:
                        self.assertEqual(len(row['shot']), 3)
                        self.assertIsNone(failure_reason(row['certified_record'], row['request']['selection']))
                    else:
                        self.assertIsNone(row['shot'])
                        self.assertNotIn('certified_record', row)
                solved = [r for r in rows if r['success']]
                expected = json.loads((ROOT / 'results' / summary_file).read_text(encoding='utf-8'))[metric_key]
                self.assertEqual(len(solved), expected['solved'])
                self.assertEqual(len(solved), metadata['solved'])
                self.assertEqual(sum(r['elapsed_ms'] <= 10000 for r in solved), expected['within_10s'])
                self.assertEqual(sum(r['elapsed_ms'] <= 10000 for r in solved), metadata['within_10s'])
                self.assertAlmostEqual(statistics.median(r['elapsed_ms'] for r in solved), expected['median_solved_ms'])
                self.assertEqual(sum(r['initial_success'] for r in rows), expected['initial_solved'])
                self.assertEqual(sum(r['refinement_success'] for r in rows), expected['refinement_solved'])
                repaired = [r for r in rows if r['source_run'] == 'compact_interrupted_replay_p4_20261016']
                expected_repairs = [metadata['sleep_repair_request']] if 'sleep_repair_request' in metadata else []
                self.assertEqual([r['request_fingerprint'] for r in repaired], expected_repairs)


if __name__ == '__main__':
    unittest.main()
