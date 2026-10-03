"""Independent Unity runtime mass/inertia outputs and actual body lifecycle."""
import json
import unittest
from pathlib import Path

import numpy as np

import local_simulator.unity_physx
from tools.reverse.recovered_stone_mass import recovered_stone_inertia


class RecoveredStoneMassTest(unittest.TestCase):
    def test_inertia_matches_all_observed_mass_rebuilds(self):
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_stone_mass_20261002.json').read_text())
        self.assertEqual(len(fixture['cases']), 98)
        for case in fixture['cases']:
            with self.subTest(callId=case['callId']):
                value = recovered_stone_inertia(fixture['massInformation'], case['scale'], case['mass'])
                bits = np.asarray(value, dtype=np.float32).view(np.uint32).tolist()
                self.assertEqual(bits, case['expectedInertiaBits'])

    def test_shape_activation_recomputes_yaw_inertia_without_solver_locks(self):
        from local_simulator.runtime_loader import install_bundled_pyphysx
        install_bundled_pyphysx()
        scene = local_simulator.unity_physx.PersistentPhysxFrontHalfScene(stone_count=1)
        slot = scene.slots[0]
        # Captured 11005 release q and Unity f72777 output; fixed inertia would
        # retain 0x3e41c3a8 instead of the observed activation value 0x3e41c3a5.
        q = [6.44059525711782e-08, 0.25336310267448425,
             1.6868479946197112e-08, 0.9673712253570557]
        slot.body.set_global_pose(([1,2,3], [q[3], *q[:3]]))
        scene._refresh_unity_stone_geometry(slot)
        actual = slot.body.get_mass_space_inertia_tensor()
        self.assertEqual(np.asarray(actual, dtype=np.float32).view(np.uint32).tolist(),
                         [0, 0x3e41c3a5, 0])
        for flag in (scene.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_X,
                     scene.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_Z):
            self.assertFalse(slot.body.get_rigid_dynamic_lock_flag_value(flag))


if __name__ == '__main__':
    unittest.main()
