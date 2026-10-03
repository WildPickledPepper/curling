"""Actual PhysX shape refresh and captured f72606 writeback regressions."""
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd


class UnityShapeRefreshTest(unittest.TestCase):
    def test_setactive_replaces_actor_and_repeated_inactive_reset_stays_disabled(self):
        install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=2)
        self.assertTrue(scene.emulate_unity_setactive_no_sim)
        for position in ([0, 0, 2.375, 8], [0, 0, 2.375, 7], [2.375, 6, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]):
            # Retain old objects so allocator reuse cannot disguise replacement.
            previous = [slot.body for slot in scene.slots]
            enabled_before = [slot.enabled for slot in scene.slots]
            scene.reset_positions(position)
            for slot in scene.slots:
                if slot.enabled and not enabled_before[slot.index]:
                    self.assertIsNot(slot.body, previous[slot.index])
                else:
                    self.assertIs(slot.body, previous[slot.index])
                self.assertEqual(scene._address_to_index[int(slot.body.get_physx_address())], slot.index)
                self.assertTrue(slot.in_scene)
                self.assertEqual(slot.body.get_actor_flag_value(
                    scene.pyphysx.ActorFlag.DISABLE_SIMULATION), not slot.enabled)
                self.assertEqual(slot.shape.get_flag_value(
                    scene.pyphysx.ShapeFlag.SIMULATION_SHAPE), slot.enabled)
        scene.start_motioninfo(0, [2.375, 32, 0, -2, 0.01])
        self.assertFalse(scene.slots[0].body.get_actor_flag_value(
            scene.pyphysx.ActorFlag.DISABLE_SIMULATION))
        scene.deactivate(0)
        scene.deactivate(0)

    def test_inactive_deactivation_skips_invalid_velocity_and_sleep_apis(self):
        body = Mock()
        slot = SimpleNamespace(body=body, shape=Mock(), material=Mock(), enabled=False)
        scene = SimpleNamespace(slots=[slot], set_active_scene_membership=False,
            coordinate_mode="unity-native-yup", emulate_unity_setactive_no_sim=True,
            _set_position_preserve_orientation=Mock(),
            _custom_sliding_index=None, pyphysx=SimpleNamespace(
                ShapeFlag=SimpleNamespace(SIMULATION_SHAPE=1),
                ActorFlag=SimpleNamespace(DISABLE_SIMULATION=2)))
        PersistentPhysxFrontHalfScene.deactivate(scene, 0)
        body.set_linear_velocity.assert_not_called()
        body.set_angular_velocity.assert_not_called()
        body.put_to_sleep.assert_not_called()
        body.set_actor_flag.assert_called_once_with(2, True)

    def test_live_shapes_use_captured_scales_without_changing_body_or_hull(self):
        install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=1)
        slot = scene.slots[0]
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_transform_scale_20261001.json').read_text())
        original = slot.shape.get_convex_mesh_data()
        body_address = slot.body.get_physx_address()
        for case in fixture['cases']:
            with self.subTest(callId=case['callId']):
                x,y,z,w = case['localQuaternion']
                slot.body.set_global_pose(([1,2,3],[w,x,y,z]))
                body_before = scene.raw_native_state(0)
                previous = slot.shape
                scene._refresh_unity_stone_geometry(slot)
                self.assertIsNot(slot.shape,previous)
                mesh = slot.shape.get_convex_mesh_data()
                bits = np.asarray(mesh['scale'],dtype=np.float32).view(np.uint32).tolist()
                self.assertEqual(bits,[case['expectedMatrixBits'][i] for i in (0,4,8)])
                self.assertEqual(tuple(mesh['scale_rotation_xyzw']),(0,0,0,1))
                self.assertEqual(mesh['vertices'],original['vertices'])
                self.assertEqual(mesh['polygons'],original['polygons'])
                self.assertEqual(mesh['index_buffer'],original['index_buffer'])
                self.assertEqual(slot.body.get_physx_address(),body_address)
                self.assertEqual(scene.raw_native_state(0),body_before)
                self.assertEqual(len(slot.body.get_atached_shapes()),1)

    def test_solver_exit_is_written_back_using_captured_f72606_arithmetic(self):
        # Unity ordinal 5: source and destination are independently captured
        # before and after f72606, not produced by this implementation.
        q = SimpleNamespace(x=6.440262012574749e-08,y=0.2535548806190491,
            z=1.688124839915872e-08,w=0.9673210978507996)
        body = SimpleNamespace(is_sleeping=lambda:False,
            get_global_pose=lambda:([1,2,3],q),set_global_pose_without_autowake=Mock())
        scene = SimpleNamespace(scene=SimpleNamespace(simulate=Mock(return_value=42)),
            dt=.01,emulate_unity_body_pose_writeback=True,coordinate_mode='unity-native-yup',
            emulate_unity_setactive_no_sim=False,
            probe=SimpleNamespace(np=np),slots=[SimpleNamespace(enabled=True,body=body)])
        result = PersistentPhysxFrontHalfScene._simulate_unity_step(scene)
        self.assertEqual(result,42)
        scene.scene.simulate.assert_called_once_with(.01)
        body.set_global_pose_without_autowake.assert_called_once_with(([1,2,3],q))

    def test_settling_does_not_bypass_required_pose_writeback(self):
        native=SimpleNamespace(simulate_until_quiet=Mock(),get_contact_reports=Mock())
        body=SimpleNamespace(get_linear_velocity=lambda:[0,0,0],
                             get_angular_velocity=lambda:[0,0,0])
        scene=SimpleNamespace(scene=native,emulate_unity_body_pose_writeback=True,
            slots=[SimpleNamespace(enabled=True,body=body)],_simulate_unity_step=Mock())
        self.assertTrue(StrictCurlingEnd._settle(SimpleNamespace(scene=scene),max_steps=20))
        native.simulate_until_quiet.assert_not_called()
        self.assertEqual(scene._simulate_unity_step.call_count,20)

    def test_unity_bvh34_mesh_and_tick526_state(self):
        install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=16)
        mesh = scene.ice.get_atached_shapes()[0].get_triangle_mesh_runtime_data()
        capture = json.loads((Path(__file__).parents[1]/'assets/unity_runtime_ice_triangle_mesh.json').read_text())['captures'][0]
        self.assertEqual(mesh['midphase_id'],1)
        self.assertEqual([list(t) for t in mesh['triangles']],capture['decodedMesh']['triangles'])
        self.assertEqual(mesh['face_remap'],capture['decodedCookedInternals']['faceRemap'])
        self.assertEqual(mesh['bv4']['raw_bytes'],capture['decodedCookedInternals']['bvh4']['rawBytes'])
        self.assertEqual(mesh['bv4']['nb_nodes'],100)
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_release_tick526_20261002.json').read_text())
        def state_bits():
            s = scene.raw_native_state(0); q = s['quaternionWxyz']
            return np.asarray(s['physxPosition']+q[1:]+q[:1]+
                s['physxLinearVelocity']+s['physxAngularVelocity'],dtype=np.float32).view(np.uint32).tolist()
        scene.reset_positions(fixture['resetPositions'])
        scene.start_bestshot(0,fixture['bestshot'])
        self.assertEqual(state_bits(),fixture['releaseBits'])
        for noise in fixture['frictionInputs'][:-1]:
            scene.step_custom_sliding(0,noise)
        self.assertEqual(state_bits(),fixture['beforeBits'])
        scene.step_custom_sliding(0,fixture['frictionInputs'][-1])
        self.assertEqual(state_bits(),fixture['afterBits'])


if __name__=='__main__':
    unittest.main()
