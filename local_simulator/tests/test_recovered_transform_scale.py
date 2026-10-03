"""Independent captured Unity outputs, not an implementation-derived oracle."""
import json
import unittest
from pathlib import Path

import numpy as np

import local_simulator.unity_physx  # registers the bundled tools package
from tools.reverse.recovered_transform_scale import (
    recovered_stone_geometry_scale, recovered_stone_scale_matrix, recovered_stone_world_matrix,
)


class RecoveredTransformScaleTest(unittest.TestCase):
    def test_original_unity_matrix_outputs_are_bit_exact(self):
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_transform_scale_20261001.json').read_text())
        self.assertEqual(fixture['sourceSha256'],
            'cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81')
        self.assertEqual(len(fixture['cases']),11)
        for case in fixture['cases']:
            with self.subTest(callId=case['callId']):
                args = case['localQuaternion'],case['localScale'],case['parentScale']
                for method,expected in (
                    (recovered_stone_scale_matrix,case['expectedMatrixBits']),
                    (recovered_stone_world_matrix,case['expectedWorldMatrixBits']),
                ):
                    bits = np.asarray(method(*args),dtype=np.float32).view(np.uint32).tolist()
                    self.assertEqual(bits,expected)
                scale_bits = np.asarray(recovered_stone_geometry_scale(*args),dtype=np.float32).view(np.uint32).tolist()
                self.assertEqual(scale_bits,[case['expectedMatrixBits'][i] for i in (0,4,8)])


if __name__=='__main__':
    unittest.main()
