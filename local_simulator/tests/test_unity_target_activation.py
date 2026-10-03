"""Actual Unity frames around island activation, without injected body states."""
import json
import struct
import unittest
from pathlib import Path

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from local_simulator.unity_prediction import UnityPredictionDriver


def state_words(scene, index):
    s = scene.raw_native_state(index)
    q = s['quaternionWxyz']
    values = s['physxPosition'] + q[1:] + q[:1] + s['physxLinearVelocity'] + s['physxAngularVelocity']
    return list(struct.unpack('<13I', struct.pack('<13f', *values)))


class UnityTargetActivationTest(unittest.TestCase):
    def setUp(self):
        install_bundled_pyphysx()
        self.fixture = json.loads((Path(__file__).parent / 'fixtures/unity_target_activation_20261002.json').read_text())
        self.scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
        positions = [0.0] * 32
        positions[4:6] = [2.375, 5.2]
        self.scene.reset_positions(positions)

    def assert_frame(self, tick):
        self.assertEqual([state_words(self.scene, k) for k in (0, 2)],
                         self.fixture['completedStates'][str(tick)])

    def test_default_does_not_wake_target_one_step_before_contact(self):
        self.scene.start_bestshot(0, [3.4, 0, 0])
        for tick, noise in enumerate(self.fixture['frictionNoises'], 1):
            step = self.scene.step_custom_sliding(0, noise)
            if tick >= 1561:
                self.assert_frame(tick)
                self.assertEqual(self.scene.slots[2].body.is_sleeping(), tick < 1562)
                self.assertFalse(step['wakesTargetsForPcm'])
        self.scene._simulate_unity_step()
        self.assert_frame(1563)

    def test_training_replay_uses_the_same_natural_activation(self):
        result = self.scene.run_bestshot_to_first_contact_training(
            0, [3.4, 0, 0], self.fixture['frictionNoises'], target_indices=[2])
        self.assertTrue(result['reachedFirstContact'])
        self.assertEqual(result['steps'], 1562)
        self.assert_frame(1562)
        self.scene._simulate_unity_step()
        self.assert_frame(1563)

    def test_autonomous_draw_gate_stops_on_actual_collision_before_update(self):
        self.scene.start_bestshot(0,[3.4,0,0])
        def inputs():
            yield from self.fixture['frictionNoises']
            self.fail('collision must block the next RNG draw')
        driver=UnityPredictionDriver(self.scene,0,noises=inputs(),use_lean_steps=True)
        for tick in range(1,1564):
            driver.fixed_update()
            if tick>=1561:
                self.assert_frame(tick)
        self.assertEqual(driver.draw_count,1562)
        self.assertEqual(driver.first_contact_step,1562)
        self.assertEqual(driver.first_contact_targets,[2])
        self.assertEqual(driver.update_count,0)


if __name__ == '__main__':
    unittest.main()
