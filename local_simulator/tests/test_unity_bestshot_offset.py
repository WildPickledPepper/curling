"""Nonzero BESTSHOT offset must preserve Unity's captured raw release state."""
import json
import struct
import unittest
from pathlib import Path
from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


def words(scene,index):
    s=scene.raw_native_state(index)
    q=s['quaternionWxyz']
    return list(struct.unpack('<13I',struct.pack('<13f',*(s['physxPosition']
        +q[1:]+q[:1]+s['physxLinearVelocity']+s['physxAngularVelocity']))))


class UnityBestshotOffsetTest(unittest.TestCase):
    def test_nonzero_offset_release_and_first_four_steps_match_actual_unity(self):
        install_bundled_pyphysx()
        fixture=json.loads((Path(__file__).parent/'fixtures/unity_bestshot_offset_11009_20261002.json').read_text())
        p=fixture['plan']
        scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
        positions=[0.]*32
        for target in p['stones']:
            positions[target['index']*2:target['index']*2+2]=[target['x'],target['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(0,[p['v0'],p['h0'],p['w0']])
        self.assertEqual([words(scene,k) for k in (0,11)],fixture['releaseBits'])
        for noise,expected in zip(fixture['frictionNoises'],fixture['firstFourCompletedBits']):
            scene.step_custom_sliding(0,noise)
            self.assertEqual([words(scene,k) for k in (0,11)],expected)


if __name__=='__main__':unittest.main()
