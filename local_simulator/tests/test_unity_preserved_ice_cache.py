"""Keep Unity's actual sleeping-target contact cache at the wake boundary."""
import json
import struct
import unittest
from pathlib import Path

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from local_simulator.tests.test_unity_target_activation import state_words


class UnityPreservedIceCacheTest(unittest.TestCase):
    def test_target_cache_and_contact_rows_match_unity_when_target_wakes(self):
        pyphysx=install_bundled_pyphysx()
        fixture=json.loads((Path(__file__).parent/'fixtures/unity_preserved_ice_cache_11009_20261002.json').read_text())
        p=fixture['plan']
        scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
        positions=[0.]*32
        for target in p['stones']:
            positions[target['index']*2:target['index']*2+2]=[target['x'],target['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(p['active_index'],[p['v0'],p['h0'],p['w0']])
        target_index=p['stones'][0]['index']
        target_x=scene.raw_native_state(target_index)['physxPosition'][0]
        for tick in range(1,1387):
            traced=tick==1383
            names=('narrowphase','solve_block')
            if traced:
                self.assertTrue(scene.slots[target_index].body.is_sleeping())
                for name in names:
                    getattr(pyphysx,'clear_scene_'+name+'_trace')()
                    getattr(pyphysx,'set_scene_'+name+'_trace_enabled')(True)
            try:
                if tick<=len(fixture['frictionNoises']):
                    scene.step_custom_sliding(p['active_index'],fixture['frictionNoises'][tick-1])
                else:
                    scene._simulate_unity_step()
                if traced:
                    narrow=pyphysx.get_scene_narrowphase_trace(False)
                    contact=next(r for r in narrow if not r['after']
                        and r['actor_core0']['p'][0]==target_x and r['geom_type1']==5)
                    self.assertEqual(contact['cache']['cached_size'],304)
                    solves=pyphysx.get_scene_solve_block_trace(False)
                    support=next(r for r in solves if r['constraint_type']==5
                        and r['data_a_before']['body2world']['p'][0]==target_x)
                    # Native pointers enlarge the constraint header by 16 bytes.
                    actual=list(struct.unpack_from('<60I',bytes(support['constraint_bytes_before']),80))
                    self.assertEqual(actual,fixture['targetNormalConstraintWords'])
                    self.assertFalse(scene.slots[target_index].body.is_sleeping())
            finally:
                if traced:
                    for name in names:
                        getattr(pyphysx,'set_scene_'+name+'_trace_enabled')(False)
            if str(tick) in fixture['completedStates']:
                self.assertEqual([state_words(scene,k) for k in fixture['stoneIndices']],
                                 fixture['completedStates'][str(tick)])


if __name__=='__main__':unittest.main()
