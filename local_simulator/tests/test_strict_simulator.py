import inspect
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

# Importing the packaged modules installs ``runtime_support`` on sys.path.
# The remaining ``tools.reverse`` imports therefore resolve to the bundle
# carried by local_simulator, never to a repository-level checkout.
from local_simulator.unity_front_half import UnityFrontHalfSimulator
from local_simulator.unity_physx import (
    DEFAULT_RUNTIME_ICE_MESH,
    PersistentPhysxFrontHalfScene,
    load_unity_builtin_plane_source,
    load_unity_runtime_ice_face_remap,
    load_unity_runtime_ice_mesh,
)
from tools.reverse.front_half_pcm_replay import event_shot_groups, to_pyphysx_zup_state
from tools.reverse.recovered_curling_motion import B2Vec2, Speed


class UnityFrontHalfSimulatorTest(unittest.TestCase):
    def test_physx_front_half_defaults_to_tilt_only_native_angular_setter(self):
        parameter = inspect.signature(PersistentPhysxFrontHalfScene).parameters[
            "emulate_unity_native_angular_setter_rotation"
        ]
        self.assertFalse(parameter.default)
        tilt_parameter = inspect.signature(PersistentPhysxFrontHalfScene).parameters[
            "emulate_unity_native_angular_setter_tilt_only"
        ]
        self.assertTrue(tilt_parameter.default)

    def test_runtime_ice_mesh_uses_captured_unity_topology(self):
        vertices, triangles, meta = load_unity_runtime_ice_mesh(
            Path(DEFAULT_RUNTIME_ICE_MESH), np
        )

        self.assertEqual(vertices.shape, (121, 3))
        self.assertEqual(triangles.shape, (200, 3))
        self.assertEqual(meta["indexWidth"], 2)
        self.assertEqual(triangles[0].tolist(), [11, 22, 23])
        self.assertAlmostEqual(float(vertices[0, 0]), -60.99604034423828)
        self.assertAlmostEqual(float(vertices[0, 2]), 60.54441833496094)

    def test_builtin_plane_source_preserves_unity_scale_pose_and_cell_order(self):
        vertices, triangles, scale, position, quaternion, meta = load_unity_builtin_plane_source(
            Path(DEFAULT_RUNTIME_ICE_MESH), np
        )

        self.assertEqual(vertices.shape, (121, 3))
        self.assertEqual(triangles.shape, (200, 3))
        self.assertEqual(triangles[:4].tolist(), [[11, 22, 23], [11, 23, 12], [0, 11, 12], [0, 12, 1]])
        self.assertEqual(scale, [4.997991561889648, 1.0160000324249268, 0.9956802725791931])
        self.assertEqual(position, [-85.98600006103516, 14.304784774780273, 55.566017150878906])
        self.assertEqual(quaternion, [1.0, 0.0, 0.0, 0.0])
        self.assertEqual(
            meta["sourceInputTriangleOrder"],
            "captured Unity Gu::TriangleMesh.mTriangles reused directly",
        )

    def test_runtime_ice_face_remap_is_complete_permutation(self):
        face_remap = load_unity_runtime_ice_face_remap(Path(DEFAULT_RUNTIME_ICE_MESH))

        self.assertEqual(len(face_remap), 200)
        self.assertEqual(sorted(face_remap), list(range(200)))
        self.assertEqual(face_remap[:4], [171, 178, 179, 180])

    def test_protocol_reset_preserves_hidden_yaw(self):
        sim = UnityFrontHalfSimulator(stone_count=2)
        sim.sync_actor_from_scene(1, x=1.0, y=2.0, yaw=0.75, vx=0.3, active=True)

        sim.reset_positions([0.0, 0.0, 2.2, 6.2])

        target = sim.stones[1]
        self.assertEqual((target.x, target.y), (2.2, 6.2))
        self.assertAlmostEqual(target.yaw, 0.75)
        self.assertEqual((target.vx, target.vy, target.w), (0.0, 0.0, 0.0))
        self.assertTrue(target.active)

    def test_motioninfo_stops_on_discrete_first_pcm_tick(self):
        sim = UnityFrontHalfSimulator(stone_count=3)
        sim.sync_actor_from_scene(0, x=0.0, y=0.0, yaw=0.25, active=False)
        sim.sync_actor_from_scene(1, x=2.0, y=2.0, yaw=0.4, active=True)
        sim.sync_actor_from_scene(2, x=2.0, y=2.0, yaw=-0.3, active=True)

        def unchanged(_friction: float, vec: B2Vec2, angle: float, _step: float) -> Speed:
            return Speed(vec, angle)

        with patch("tools.reverse.front_half_pcm_replay.newfrictionstep", side_effect=unchanged):
            result = sim.motioninfo_to_first_pcm(
                0,
                [2.0, 3.0, 0.0, -1.0, 0.2],
                noises=[0.0] * 60,
                threshold=0.5001,
            )

        self.assertEqual(result["steps"], 50.0)
        self.assertEqual(result["pcmTargetIndices"], [1, 2])
        self.assertEqual(result["source"], "first_pcm_discrete_tick")
        self.assertAlmostEqual(result["y"], 2.5)
        self.assertAlmostEqual(result["yaw"], 0.35)
        self.assertAlmostEqual(result["targetStates"][0]["yaw"], 0.4)

    def test_pcm_material_restore_waits_for_current_shell_pose(self):
        active = {"x": 0.0, "y": 0.0, "vx": 1.0, "vy": 0.0}
        targets = {"8": {"x": 0.302, "y": 0.0, "vx": 0.0, "vy": 0.0}}

        self.assertTrue(PersistentPhysxFrontHalfScene._reaches_pcm_shell_this_tick(active, targets))
        self.assertFalse(PersistentPhysxFrontHalfScene._is_inside_pcm_shell(active, targets))

    def test_pyphysx_payload_uses_unity_axis_mapping(self):
        converted = to_pyphysx_zup_state(
            {"x": 2.0, "y": 5.0, "vx": 0.1, "vy": -1.2, "w": 0.5, "yaw": 0.0}
        )

        self.assertEqual(converted["position"], [-5.0, -2.0, 0.115])
        self.assertEqual(converted["linearVelocity"], [1.2, -0.1, 0.0])
        self.assertEqual(converted["angularVelocity"], [0.0, 0.0, 0.5])
        self.assertEqual(converted["quaternionWxyz"], [1.0, 0.0, 0.0, 0.0])

    def test_event_group_records_motioninfo_boundary(self):
        events = [
            {"t": 1.0, "data": {"textPreview": "BESTSHOT 3.4 0 0"}},
            {"t": 2.0, "data": {"textPreview": "MOTIONINFO 2.3 21.5 0 -2.1 0.2"}},
            {
                "t": 3.0,
                "type": "sliding.random_range.friction",
                "data": {"value": 0.0001},
            },
        ]

        groups = event_shot_groups(events)

        self.assertEqual(groups[0]["motioninfo"]["values"], [2.3, 21.5, 0.0, -2.1, 0.2])
        self.assertEqual(groups[0]["friction"][0]["noise"], 0.0001)


if __name__ == "__main__":
    unittest.main()
