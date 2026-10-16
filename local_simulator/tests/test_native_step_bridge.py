"""Fused path against original Unity state bytes, not just another local path."""
import base64
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch
import zlib

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene
from local_simulator.unity_prediction import UnityPredictionDriver
from local_simulator.native_step_bridge import load_step_bridge
from local_simulator.tests.test_unity_target_activation import state_words


class NativeStepBridgeTest(unittest.TestCase):
    def setUp(self):
        install_bundled_pyphysx()
        if load_step_bridge() is None:
            self.skipTest('optional verified CP39 native step bridge unavailable')

    def driver(self, fixture):
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        p = fixture['plan']
        positions = [0.]*32
        for stone in p['stones']:
            positions[stone['index']*2:stone['index']*2+2] = [stone['x'], stone['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(p['active_index'], [p['v0'], p['h0'], p['w0']])
        def inputs():
            yield from fixture['frictionNoises']
            self.fail('unexpected friction draw after stop/removal gate')
        driver = UnityPredictionDriver(scene, p['active_index'], noises=inputs(),
            motion_stepper=NativePyphysxMotionStepper(scene.pyphysx), use_lean_steps=True,
            native_scene_steps=True)
        self.assertIsNotNone(scene._native_step_bridge)
        return scene, driver

    def test_full_natural_stop_unity_bytes_with_update_boundary(self):
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_natural_stop_12004_20261002.json').read_text())
        expected = zlib.decompress(base64.b64decode(fixture['releaseAndCompletedStateBytesZlibBase64']))
        scene, driver = self.driver(fixture)
        def compare(tick):
            words = sum((state_words(scene, k) for k in fixture['stoneIndices']), [])
            self.assertEqual(struct.pack('<26I', *words), expected[tick*104:(tick+1)*104], f'step {tick}')
        compare(0)
        for _ in range(2):
            driver.clock.begin_frame(driver.clock.maximum_delta)
            while driver.clock.take_fixed_step():
                driver.fixed_update()
                compare(driver.fixed_count)
                if driver.fixed_count == fixture['completedSteps']:
                    break
            if driver.fixed_count == fixture['completedSteps']:
                break
            driver.update()
        self.assertFalse(driver.ongoing)
        self.assertEqual((driver.fixed_count, driver.draw_count, driver.update_count), (4000, 3168, 1))

    def test_full_wall_unity_bytes_draw_gate_and_actor_recreation(self):
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_wall_collision_12000_20261003.json').read_text())
        expected = zlib.decompress(base64.b64decode(fixture['liveActorStateBytesZlibBase64']))
        scene, driver = self.driver(fixture)
        bridge = scene._native_step_bridge
        self.assertTrue(bridge.native_scene)
        original_simulate = bridge.simulate_function
        branches = []
        def simulate(*args):
            empty = original_simulate(*args)
            branches.append(bool(empty))
            return empty
        bridge.simulate_function = simulate
        offset = 0
        for tick in range(fixture['completedSteps']+1):
            if tick:
                driver.fixed_update()
            self.assertEqual([scene.slots[k].enabled for k in fixture['stoneIndices']], fixture['actorMembership'][tick])
            for k in fixture['stoneIndices']:
                if scene.slots[k].enabled:
                    self.assertEqual(struct.pack('<13I', *state_words(scene, k)), expected[offset:offset+52], f'step {tick}, stone {k}')
                    offset += 52
        self.assertEqual(offset, len(expected))
        self.assertEqual(driver.draw_count, 1879)
        self.assertIn(True, branches)
        self.assertIn(False, branches)
        self.assertFalse(branches[1878], 'wall contact must return to Python callbacks before writeback')
        self.assertTrue(driver.update())
        active = driver.active_index
        old_body = bridge.bodies[active]
        scene.start_bestshot(active, [3., 0., 0.])
        self.assertIsNone(scene._native_step_bridge)
        self.assertIsNot(scene.slots[active].body, old_body)
        new_driver = UnityPredictionDriver(scene, active, seed=123,
            motion_stepper=NativePyphysxMotionStepper(scene.pyphysx), use_lean_steps=True)
        current = scene._native_step_bridge
        self.assertIsNot(current, bridge)
        self.assertEqual(current.context.actors[active], scene.slots[active].body.get_physx_address())
        new_driver.fixed_update()

    def test_missing_bridge_and_negative_python_index_use_original_path(self):
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        scene.reset_positions([0.]*32)
        motion = NativePyphysxMotionStepper(scene.pyphysx)
        scene.start_bestshot(0, [3., 0., 0.])
        with patch('local_simulator.native_step_bridge.load_step_bridge', return_value=None):
            driver = UnityPredictionDriver(scene, 0, seed=123, motion_stepper=motion, use_lean_steps=True)
        self.assertIsNone(scene._native_step_bridge)
        driver.fixed_update()
        self.assertEqual(driver.draw_count, 1)
        # Python's existing list API permits -1; never forward it as a raw
        # negative actor-array index. Its original path remains available.
        scene.start_bestshot(-1, [3., 0., 0.])
        driver = UnityPredictionDriver(scene, -1, seed=123, motion_stepper=motion, use_lean_steps=True)
        self.assertIsNone(scene._native_step_bridge)
        driver.fixed_update()
        self.assertEqual(driver.draw_count, 1)

    def test_fused_wall_mask_matches_membership_before_every_writeback(self):
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_wall_collision_12000_20261003.json').read_text())
        scene, driver = self.driver(fixture)
        bridge = scene._native_step_bridge
        original = bridge.writeback
        observed = []
        def writeback(mask=None):
            actual = sum(1 << slot.index for slot in scene.slots if slot.enabled)
            effective = actual if mask is None else mask
            self.assertEqual(effective, actual, f'writeback after step {driver.fixed_count+1}')
            observed.append(effective)
            original(mask)
        with patch.object(bridge, 'writeback', side_effect=writeback):
            for _ in range(fixture['completedSteps']):
                driver.fixed_update()
        self.assertTrue(observed[1877] & (1 << driver.active_index))
        self.assertFalse(observed[1878] & (1 << driver.active_index))
        self.assertEqual(driver.draw_count, 1879)

    def test_fused_scope_restores_flags_and_pair_material_on_simulation_error(self):
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        scene.reset_positions([0.]*32)
        scene.start_bestshot(0, [3., 0., 0.])
        driver = UnityPredictionDriver(scene, 0, seed=123,
            motion_stepper=NativePyphysxMotionStepper(scene.pyphysx), use_lean_steps=True)
        with patch.object(scene, '_first_pair_zero_friction_for_step', return_value=True), \
                patch.object(scene, '_set_stone_stone_contact_friction', wraps=scene._set_stone_stone_contact_friction) as override, \
                patch.object(scene, '_simulate_unity_step', side_effect=RuntimeError('injected simulation failure')):
            with self.assertRaisesRegex(RuntimeError, 'injected simulation failure'):
                driver.fixed_update()
        self.assertFalse(scene._in_custom_sliding_step)
        self.assertEqual([call.args for call in override.call_args_list],
                         [(0., 0.), (scene.stone_stone_contact_static_friction, scene.stone_stone_contact_dynamic_friction)])

    def test_scene_proxy_and_custom_clock_keep_instrumentation(self):
        from local_simulator.unity_prediction import UnityPredictionClock
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        scene.reset_positions([0.]*32)
        scene.start_bestshot(0, [3., 0., 0.])
        class Clock(UnityPredictionClock):
            calls = 0
            def take_fixed_step(self):
                self.calls += 1
                return super().take_fixed_step()
        clock = Clock(fixed_dt=scene.dt)
        driver = UnityPredictionDriver(scene, 0, seed=123, clock=clock,
            motion_stepper=NativePyphysxMotionStepper(scene.pyphysx), use_lean_steps=True,
            native_scene_steps=True)
        self.assertTrue(scene._native_step_bridge.native_scene)
        original = scene.scene
        calls = []
        class Proxy:
            def simulate(self, dt):
                calls.append(dt)
                return original.simulate(dt)
            def __getattr__(self, key):
                return getattr(original, key)
        scene.scene = Proxy()
        driver.run(max_steps=3)
        self.assertEqual(clock.calls, 3)
        self.assertEqual(calls, [scene.dt]*3)
        self.assertEqual(driver.fixed_count, 3)
