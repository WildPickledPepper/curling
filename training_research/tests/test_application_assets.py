"""Portable installation assets must survive Git checkout byte-for-byte."""
import hashlib
import json
from pathlib import Path
import unittest


class ApplicationAssetTests(unittest.TestCase):
    def test_native_integrity_assets_and_empirical_atlas_are_intact(self):
        from local_simulator import native_core_optimization, native_vertex_bounds, native_solver_product
        from training_research.inverse_contact_atlas import DEFAULT
        for module in (native_core_optimization, native_vertex_bounds, native_solver_product):
            with self.subTest(asset=module.ASSET):
                self.assertEqual(hashlib.sha256(module.ASSET.read_bytes()).hexdigest(), module.ASSET_SHA256)
        metadata = json.loads(DEFAULT.with_suffix(".json").read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256(DEFAULT.read_bytes()).hexdigest(), metadata["atlas_sha256"])

    def test_proposal_helpers_are_bundled_with_original_bytes(self):
        from training_research.legacy_inverse import ARCHIVE
        self.assertEqual(ARCHIVE.parent, Path(__file__).resolve().parents[1])
        for row in json.loads((ARCHIVE/"manifest.json").read_text(encoding="utf-8"))["files"]:
            with self.subTest(source=row["path"]):
                self.assertEqual(hashlib.sha256((ARCHIVE/row["path"]).read_bytes()).hexdigest(), row["sha256"])


if __name__ == "__main__":
    unittest.main()
