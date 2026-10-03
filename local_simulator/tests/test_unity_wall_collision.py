"""Wall callback and actor removal against a complete observed Unity shot."""
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


class UnityWallCollisionTest(unittest.TestCase):
    def test_autonomous_draw_gate_and_full_live_states_after_wall_removal(self):
        install_bundled_pyphysx()
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_wall_collision_12000_20261003.json').read_text())
        expected = zlib.decompress(base64.b64decode(fixture['liveActorStateBytesZlibBase64']))
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        p = fixture['plan']
        positions = [0.]*32
        for stone in p['stones']:
            positions[stone['index']*2:stone['index']*2+2] = [stone['x'],stone['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(p['active_index'],[p['v0'],p['h0'],p['w0']])
        def inputs():
            yield from fixture['frictionNoises']
            self.fail('removed GameObject must not consume another friction draw')
        driver = UnityPredictionDriver(scene,p['active_index'],noises=inputs(),use_lean_steps=True)
        offset=0
        for tick in range(fixture['completedSteps']+1):
            if tick:
                driver.fixed_update()
            self.assertEqual([scene.slots[k].enabled for k in fixture['stoneIndices']],fixture['actorMembership'][tick])
            for k in fixture['stoneIndices']:
                if scene.slots[k].enabled:
                    self.assertEqual(struct.pack('<13I',*state_words(scene,k)),expected[offset:offset+52],f'step {tick}, stone {k}')
                    offset+=52
        self.assertEqual(offset,len(expected))
        self.assertEqual(driver.draw_count,1879)
        self.assertTrue(driver.update())

    def test_static_wall_reporting_does_not_change_solver_outputs(self):
        pyphysx = install_bundled_pyphysx()
        from local_simulator.native_wall_contact import mark_wall_shape
        scenes = []
        for mark in (False, True):
            scene = pyphysx.Scene(scene_flags=[], enable_contact_report=True)
            material = pyphysx.Material(.6, .6, 0.)
            wall = pyphysx.RigidStatic()
            wall.attach_shape(pyphysx.Shape.create_box([1., 1., 1.], material))
            if mark:
                mark_wall_shape(wall)
            scene.add_actor(wall)
            body = pyphysx.RigidDynamic()
            body.attach_shape(pyphysx.Shape.create_box([1., 1., 1.], material))
            body.set_global_pose(([0., 0., .99], [1., 0., 0., 0.]))
            body.disable_gravity()
            scene.add_actor(body)
            scenes.append((scene, body, wall, material))
        for tick in range(10):
            words = []
            reports = []
            for scene, body, _wall, _material in scenes:
                scene.simulate(.01)
                p, q = body.get_global_pose()
                words.append(struct.pack('<13f', *p, q.x, q.y, q.z, q.w,
                                         *body.get_linear_velocity(), *body.get_angular_velocity()))
                reports.append(scene.get_contact_reports())
            self.assertEqual(words[0], words[1], f'notification-only step {tick}')
            self.assertFalse(reports[0])
            if tick == 0:
                self.assertTrue(any(r['events'] & 4 and r['contact_count'] > 0 for r in reports[1]))

    def test_collision_removal_and_full_live_trajectory_match_unity(self):
        pyphysx = install_bundled_pyphysx()
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_wall_collision_12000_20261003.json').read_text())
        expected = zlib.decompress(base64.b64decode(fixture['liveActorStateBytesZlibBase64']))
        self.assertEqual(hashlib.sha256(expected).hexdigest(), fixture['stateBytesSha256'])
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        plan = fixture['plan']
        positions = [0.]*32
        for stone in plan['stones']:
            positions[stone['index']*2:stone['index']*2+2] = [stone['x'], stone['y']]
        scene.reset_positions(positions)
        scene.start_bestshot(plan['active_index'], [plan['v0'], plan['h0'], plan['w0']])
        active = scene.slots[plan['active_index']]
        body_address = active.body.get_physx_address()
        offset = 0
        contacts = []
        for tick in range(fixture['completedSteps']+1):
            if tick:
                if tick <= len(fixture['frictionNoises']):
                    scene.step_custom_sliding(plan['active_index'], fixture['frictionNoises'][tick-1])
                else:
                    scene._simulate_unity_step()
            actual_alive = [scene.slots[k].enabled for k in fixture['stoneIndices']]
            physically_live = [scene.slots[k].in_scene and not scene.slots[k].body.get_actor_flag_value(
                pyphysx.ActorFlag.DISABLE_SIMULATION) for k in fixture['stoneIndices']]
            self.assertEqual(physically_live, actual_alive)
            self.assertEqual(actual_alive, fixture['actorMembership'][tick], f'membership step {tick}')
            for index, alive in zip(fixture['stoneIndices'], actual_alive):
                if alive:
                    self.assertEqual(struct.pack('<13I', *state_words(scene, index)),
                                     expected[offset:offset+52], f'live actor {index}, step {tick}')
                    offset += 52
            if scene._last_wall_reports:
                contacts.append(tick)
                self.assertEqual(scene._last_wall_reports[0]['wall'], 'bound1')
            if not active.enabled:
                self.assertEqual(state_words(scene, plan['active_index']),
                                 fixture['wallCallback']['poseWords']+[0]*6)
        self.assertEqual(offset, len(expected))
        self.assertEqual(contacts, [1879])
        self.assertIsNone(scene._custom_sliding_index)
        self.assertEqual(active.material.get_static_friction(), float(scene.probe.np.float32(.6)))
        self.assertEqual(active.material.get_dynamic_friction(), float(scene.probe.np.float32(.6)))
        # The Wall callback retains the actor. Reset can independently
        # rebuild it while changing Rigidbody constraints, as already traced.
        self.assertEqual(active.body.get_physx_address(), body_address)
        scene.reset_positions(positions)
        scene.start_bestshot(plan['active_index'], [plan['v0'], plan['h0'], plan['w0']])
        self.assertTrue(active.enabled)
        for noise in fixture['frictionNoises']:
            step = scene.step_custom_sliding(plan['active_index'], noise)
            if not active.enabled:
                self.assertTrue(step['wallReports'])
                break
        self.assertFalse(active.enabled)


if __name__ == '__main__':
    unittest.main()
