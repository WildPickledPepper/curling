"""Compare actual native registration inputs with the Unity runtime fixture."""
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


def bits(values):
    return list(struct.unpack('<%dI' % len(values), struct.pack('<%df' % len(values), *values)))


class StoneRegistrationTest(unittest.TestCase):
    def test_scene_receives_observed_default_pose_and_unit_inertia(self):
        install_bundled_pyphysx()
        import pyphysx
        original_scene = pyphysx.Scene
        observed = []

        class ObservedScene:
            def __init__(self, *args, **kwargs):
                self.native = original_scene(*args, **kwargs)

            def __getattr__(self, name):
                return getattr(self.native, name)

            def add_actor(self, body):
                if isinstance(body, pyphysx.RigidDynamic):
                    p, q = body.get_global_pose()
                    inertia = body.get_mass_space_inertia_tensor()
                    observed.append({
                        'pose': bits([q.x, q.y, q.z, q.w, *p]),
                        'velocities': bits([*body.get_linear_velocity(), *body.get_angular_velocity()]),
                        'inertia': bits(inertia),
                    })
                return self.native.add_actor(body)

        with patch.object(pyphysx, 'Scene', ObservedScene):
            scene = PersistentPhysxFrontHalfScene(stone_count=16)
        fixture = json.loads((Path(__file__).parent/'fixtures/unity_stone_registration_20261002.json').read_text())
        expected = dict(zip(fixture['offsets'], fixture['bits']))
        self.assertEqual(len(observed), 16)
        for row in observed:
            self.assertEqual(row['pose'], [expected[i] for i in range(16,44,4)])
            self.assertEqual(row['velocities'], [expected[i] for i in (80,84,88,96,100,104)])
            # Unity's registration inverse inertia is unit, so both views are unit.
            self.assertEqual(row['inertia'], [expected[i] for i in (128,132,136)])
        # Later synchronization still installs the recovered inertia.
        self.assertEqual(scene.slots[0].body.get_mass_space_inertia_tensor()[0], 0)


if __name__ == '__main__':
    unittest.main()
