"""Require the fresh Reset fall to match actual Unity solver exits."""
import json
import struct
import unittest
from pathlib import Path
from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


def bits(values):
    return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))


class UnityResetSettlingTest(unittest.TestCase):
    def test_start_material_and_both_collision_callbacks_survive_reset(self):
        install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=2, ice_mesh_mode='unity-source-once')
        scene.activate_stationary(0, 2.375, 5.2)
        scene.activate_stationary(1, 2.375, 5.4)
        # Observed f61028 Start changes dynamic friction only; the actual
        # Reset solver header consequently contains 0.012 static / 0 dynamic.
        for slot in scene.slots:
            self.assertEqual(bits([slot.material.get_static_friction(),
                                   slot.material.get_dynamic_friction()]), [1058642330, 0])
            slot.body.wake_up()
        scene._simulate_unity_step()
        self.assertTrue(scene._stone_reports(scene.scene.get_contact_reports()))
        # f61030 OnCollisionEnter(Stone) runs on each of the two components.
        for slot in scene.slots:
            self.assertEqual(bits([slot.material.get_static_friction(),
                                   slot.material.get_dynamic_friction()]), [1058642330, 1058642330])
        scene.deactivate(1)
        scene.activate_stationary(1, 2.375, 8.0)
        self.assertEqual(bits([scene.slots[1].material.get_dynamic_friction()]), [1058642330])

    def test_fresh_reset_first_six_steps_match_runtime(self):
        install_bundled_pyphysx()
        scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
        fixture=json.loads((Path(__file__).parent/'fixtures/unity_reset_first_six_steps_20261002.json').read_text())
        states=[]
        original=scene._simulate_unity_step
        def observed():
            result=original()
            state=scene.raw_native_state(2)
            q=state['quaternionWxyz']
            states.append(bits(state['physxPosition']+q[1:]+q[:1]
                               +state['physxLinearVelocity']+state['physxAngularVelocity']))
            return result
        scene._simulate_unity_step=observed
        position=[0.0]*32
        position[4:6]=[2.375,5.2]
        scene.reset_positions(position,settle_steps=6,force_sleep_after_reset=False)
        self.assertEqual(states,fixture['firstSixSolverExitBits'])
        self.assertFalse(scene.slots[2].body.is_sleeping())
        self.assertEqual(scene.raw_native_state(0)['physxPosition'],
                         [-96.85420227050781,14.43239974975586,54.174400329589844])

    def test_pose_writeback_normalizes_once_without_waking_sleeping_body(self):
        from local_simulator.native_pose_writeback import writeback_pose_without_autowake
        from types import SimpleNamespace
        pyphysx = install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=1, ice_mesh_mode='unity-source-once')
        scene.activate_stationary(0, 2.375, 5.2)
        body = scene.slots[0].body
        body.put_to_sleep()
        # Independent source/destination from the captured f72606 arithmetic.
        q = SimpleNamespace(x=6.440262012574749e-08, y=0.2535548806190491,
                            z=1.688124839915872e-08, w=0.9673210978507996)
        writeback_pose_without_autowake(body, (body.get_global_pose()[0], q))
        actual = body.get_global_pose()[1]
        self.assertEqual(bits([actual.w, actual.x, actual.y, actual.z]), bits([
            0.96732097864151, 6.440261302032013e-08,
            0.2535548508167267, 1.6881246622801882e-08]))
        self.assertTrue(body.is_sleeping())

    def test_complete_reset_solver_and_natural_sleep_match_unity_bits(self):
        pyphysx = install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_reset_complete_20261002.json').read_text())
        states = []
        original = scene._simulate_unity_step

        def observed():
            pyphysx.clear_scene_solver_setup_trace()
            pyphysx.set_scene_solver_setup_trace_enabled(True)
            try:
                result = original()
                # Unity core sample is at solverSetupSolve.exit, before fetch
                # can sleep the actor and restore its prior pose. Use that same
                # native boundary rather than comparing two different phases.
                data = pyphysx.get_scene_solver_setup_trace(False)[-1]['body_data'][0]
                states.append(bits(data['body2world']['p']+data['body2world']['q']
                                   +data['linear_velocity']+data['angular_velocity']))
                return result
            finally:
                pyphysx.set_scene_solver_setup_trace_enabled(False)

        scene._simulate_unity_step = observed
        position = [0.] * 32
        position[4:6] = [2.375, 5.2]
        scene.reset_positions(position)
        self.assertEqual(states, fixture['solverExitBits'])
        self.assertTrue(scene.slots[2].body.is_sleeping())
        state = scene.raw_native_state(2)
        q = state['quaternionWxyz']
        self.assertEqual(bits(state['physxPosition']+q[1:]+q[:1]
                              +state['physxLinearVelocity']+state['physxAngularVelocity']),
                         fixture['sleepingAfterFetchBits'])
        # Continue the same scene into BESTSHOT without injecting any recorded
        # quaternion/pose. The default placement must use the observed height
        # and float32 world coordinate, not the settled-height conversion.
        scene.start_bestshot(0, fixture['shot'])
        active = scene.raw_native_state(0)
        q = active['quaternionWxyz']
        self.assertEqual(bits(active['physxPosition']+q[1:]+q[:1]),
                         fixture['bestshotReleasePoseBits'])

    def test_default_release_first_four_steps_match_unity_bits(self):
        install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_first_release_four_steps_20261002.json').read_text())
        position = [0.] * 32
        position[4:6] = [2.375, 5.2]
        scene.reset_positions(position)
        scene.start_bestshot(0, fixture['shot'])

        def state_words():
            state = scene.raw_native_state(0)
            q = state['quaternionWxyz']
            return bits(state['physxPosition']+q[1:]+q[:1]
                        +state['physxLinearVelocity']+state['physxAngularVelocity'])

        self.assertEqual(state_words(), fixture['releaseBits'])
        for step, (noise, expected) in enumerate(zip(fixture['frictionNoises'], fixture['afterStepBits']), 1):
            scene.step_custom_sliding(0, noise)
            # The second tick starts with gravity's nonzero vertical speed.
            # Unity constructs +0 before physics, so it must not accumulate.
            self.assertEqual(state_words(), expected, 'sliding tick %d' % step)


if __name__=='__main__':
    unittest.main()
