"""Natural-stop handoff regression against an entire captured Unity trajectory."""
import base64
import hashlib
import json
from pathlib import Path
import struct
import unittest
import zlib

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from local_simulator.unity_prediction import UnityPredictionDriver
from local_simulator.tests.test_unity_target_activation import state_words


class UnityNaturalStopTest(unittest.TestCase):
    def test_update_restores_material_but_waits_for_other_enabled_stones(self):
        install_bundled_pyphysx()
        scene=PersistentPhysxFrontHalfScene(stone_count=2,ice_mesh_mode='unity-source-once')
        scene.reset_positions([0.,0.,2.375,4.2])
        scene.start_bestshot(0,[3.,0.,0.])
        driver=UnityPredictionDriver(scene,0,seed=123)
        body=scene.slots[0].body
        origin=driver.origin
        body.set_global_pose(([origin[0]+2.,origin[1],origin[2]],body.get_global_pose()[1]))
        body.set_linear_velocity([0.,0.,0.])
        scene.slots[1].body.set_linear_velocity([.002,0.,0.])
        self.assertFalse(driver.update())
        self.assertTrue(driver.ongoing)
        self.assertEqual(scene._custom_sliding_index,0)
        self.assertEqual(scene.slots[0].material.get_dynamic_friction(),float(scene.probe.np.float32(.6)))
        scene.slots[1].body.set_linear_velocity([0.,0.,0.])
        scene.slots[1].body.set_angular_velocity([0.,1.,0.])
        self.assertTrue(driver.update())
        self.assertIsNone(scene._custom_sliding_index)
        self.assertEqual(driver.draw_count,0)

    def test_autonomous_schedule_matches_all_4000_steps_without_stream_length_stop(self):
        install_bundled_pyphysx()
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_natural_stop_12004_20261002.json').read_text())
        expected = zlib.decompress(base64.b64decode(fixture['releaseAndCompletedStateBytesZlibBase64']))
        p = fixture['plan']
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        positions = [0.]*32
        for stone in p['stones']:
            positions[stone['index']*2:stone['index']*2+2] = [stone['x'],stone['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(p['active_index'],[p['v0'],p['h0'],p['w0']])
        consumed = []
        def inputs():
            for noise in fixture['frictionNoises']:
                consumed.append(noise)
                yield noise
            self.fail('driver attempted an extra random draw')
        driver = UnityPredictionDriver(scene,p['active_index'],noises=inputs(),use_lean_steps=True)
        def compare(tick):
            words = sum((state_words(scene,k) for k in fixture['stoneIndices']),[])
            self.assertEqual(struct.pack('<26I',*words),expected[tick*104:(tick+1)*104],f'step {tick}')
        compare(0)
        # Clock inputs determine Update; neither loop uses the input length.
        for _ in range(2):
            driver.clock.begin_frame(driver.clock.maximum_delta)
            while driver.clock.take_fixed_step():
                driver.fixed_update()
                compare(driver.fixed_count)
                if driver.fixed_count == 2506:
                    self.assertTrue(scene._unity_active_stop_condition(p['active_index'],driver.origin))
                    self.assertTrue(driver.ongoing)
                if driver.fixed_count == fixture['completedSteps']:
                    break
            if driver.fixed_count == fixture['completedSteps']:
                break
            driver.update()
        self.assertFalse(driver.ongoing)
        self.assertEqual(driver.draw_count,3168)
        self.assertEqual(len(consumed),3168)
        self.assertEqual(driver.fixed_count,4000)
        self.assertEqual(driver.update_count,1)

    def test_free_stop_and_full_tail_match_all_unity_state_bytes(self):
        pyphysx = install_bundled_pyphysx()
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_natural_stop_12004_20261002.json').read_text())
        expected = zlib.decompress(base64.b64decode(fixture['releaseAndCompletedStateBytesZlibBase64']))
        self.assertEqual(hashlib.sha256(expected).hexdigest(),fixture['stateBytesSha256'])
        self.assertEqual(len(expected),104*(fixture['completedSteps']+1))
        p = fixture['plan']
        scene = PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
        positions = [0.]*32
        for stone in p['stones']:
            positions[stone['index']*2:stone['index']*2+2] = [stone['x'],stone['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(p['active_index'],[p['v0'],p['h0'],p['w0']])
        active = scene.slots[p['active_index']]

        def compare(tick):
            states = [state_words(scene,k) for k in fixture['stoneIndices']]
            self.assertEqual(struct.pack('<26I',*(states[0]+states[1])),
                             expected[tick*104:(tick+1)*104],f'completed physics step {tick}')

        compare(0)
        for tick,noise in enumerate(fixture['frictionNoises'],1):
            scene.step_custom_sliding(p['active_index'],noise)
            compare(tick)
            self.assertFalse(scene.scene.get_contact_reports())
            # Already below the stop threshold at2506: these real remaining
            # FixedUpdate calls must not trigger an earlier Update/handoff.
            if tick in (2506,fixture['naturalStopMaterialWritesAfterCompletedStep']):
                self.assertEqual(active.material.get_static_friction(),0.)
                self.assertEqual(active.material.get_dynamic_friction(),0.)
                self.assertEqual(scene._custom_sliding_index,p['active_index'])

        for tick in range(len(fixture['frictionNoises'])+1,fixture['completedSteps']+1):
            traced = tick==len(fixture['frictionNoises'])+1
            if traced:
                pyphysx.clear_scene_solve_block_trace()
                pyphysx.set_scene_solve_block_trace_enabled(True)
            try:
                scene._simulate_unity_step()
                if traced:
                    # Actual downstream contact coefficients at the first
                    # ordinary physics step, not the material setters alone.
                    first = pyphysx.get_scene_solve_block_trace(False)[0]
                    self.assertEqual(struct.unpack_from('<2I',bytes(first['constraint_bytes_before']),16),
                                     (0x3c449ba6,0x3c449ba6))
                    self.assertIsNone(scene._custom_sliding_index)
            finally:
                if traced:pyphysx.set_scene_solve_block_trace_enabled(False)
            compare(tick)
        self.assertTrue(all(scene.slots[k].body.is_sleeping() for k in fixture['stoneIndices']))

    def test_update_gate_checks_distance_and_full_three_dimensional_velocity(self):
        install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=1,ice_mesh_mode='unity-source-once')
        scene.start_bestshot(0,[3.,0.,0.])
        slot = scene.slots[0]
        origin = scene._custom_sliding_release_origin
        q = slot.body.get_global_pose()[1]
        slot.body.set_linear_velocity([0.,0.,0.])
        slot.body.set_global_pose(([origin[0]+0.5,origin[1],origin[2]],q))
        self.assertFalse(scene._restore_unity_natural_stop_material())
        slot.body.set_global_pose(([origin[0]+2.,origin[1],origin[2]],q))
        slot.body.set_linear_velocity([0.,0.002,0.])
        self.assertFalse(scene._restore_unity_natural_stop_material())
        slot.body.set_linear_velocity([0.,0.,0.])
        self.assertTrue(scene._restore_unity_natural_stop_material())
        self.assertIsNone(scene._custom_sliding_index)
        self.assertFalse(scene._restore_unity_natural_stop_material())


if __name__=='__main__':unittest.main()
