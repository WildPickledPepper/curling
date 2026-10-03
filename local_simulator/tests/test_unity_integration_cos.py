"""The formerly divergent strong-curl shot must match every Unity state byte."""
import base64
import hashlib
import json
from pathlib import Path
import struct
import unittest
import zlib

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from local_simulator.tests.test_unity_target_activation import state_words


class UnityIntegrationCosTest(unittest.TestCase):
    def test_strong_curl_complete_trajectory_matches_unity(self):
        install_bundled_pyphysx()
        fixture=json.loads((Path(__file__).parent/'fixtures/unity_integration_cos_12009_20261003.json').read_text())
        expected=zlib.decompress(base64.b64decode(fixture['releaseAndCompletedStateBytesZlibBase64']))
        self.assertEqual(hashlib.sha256(expected).hexdigest(),fixture['stateBytesSha256'])
        self.assertEqual(len(expected),104*(fixture['completedSteps']+1))
        plan=fixture['plan']
        scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
        positions=[0.0]*32
        for stone in plan['stones']:
            positions[stone['index']*2:stone['index']*2+2]=[stone['x'],stone['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(plan['active_index'],[plan['v0'],plan['h0'],plan['w0']])

        def compare(tick):
            states=[state_words(scene,k) for k in fixture['stoneIndices']]
            self.assertEqual(struct.pack('<26I',*(states[0]+states[1])),
                expected[tick*104:(tick+1)*104],f'completed physics step {tick}')

        compare(0)
        contacts=[]
        for tick in range(1,fixture['completedSteps']+1):
            if tick<=len(fixture['frictionNoises']):
                result=scene.step_custom_sliding(plan['active_index'],fixture['frictionNoises'][tick-1])
                if result['stoneReports']:
                    contacts.append(tick)
            else:
                scene._simulate_unity_step()
            compare(tick)
        self.assertEqual(contacts[0],fixture['firstContactStep'])
        self.assertTrue(all(scene.slots[k].body.is_sleeping() for k in fixture['stoneIndices']))


if __name__=='__main__':unittest.main()
