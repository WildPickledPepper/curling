import inspect
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from unittest.mock import Mock

import numpy as np

# Importing the packaged modules installs ``runtime_support`` on sys.path.
# The remaining ``tools.reverse`` imports therefore resolve to the bundle
# carried by local_simulator, never to a repository-level checkout.
from local_simulator.unity_front_half import UnityFrontHalfSimulator
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
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
    def test_raw_native_state_does_not_hide_pose_writeback_difference(self):
        # Real PhysX body: 11005 solver step 4 exits with a non-unit q;
        # the old state reader silently presents the normalized copy.
        from local_simulator.runtime_loader import install_bundled_pyphysx
        install_bundled_pyphysx()
        scene = PersistentPhysxFrontHalfScene(stone_count=1)
        q = [6.440262012574749e-08, 0.2535548806190491,
             1.688124839915872e-08, 0.9673210978507996]
        scene.slots[0].body.set_global_pose(([1.0, 2.0, 3.0], [q[3], *q[:3]]))
        actual = scene.raw_native_state(0)
        self.assertEqual(actual["quaternionWxyz"], [q[3], *q[:3]])
        self.assertEqual(actual["physxPosition"], [1.0, 2.0, 3.0])
        self.assertNotEqual(scene.state(0)["quaternionWxyz"], actual["quaternionWxyz"])
        self.assertEqual(scene.raw_native_state(0), actual)

    def test_native_projected_setter_matches_dense_unity_bridge(self):
        pose = SimpleNamespace(
            x=-2.4462851300199873e-08,
            y=0.9300537109375,
            z=6.192122015136192e-08,
            w=-0.3674236834049225,
        )
        scene = SimpleNamespace(probe=SimpleNamespace(np=np))
        slot = SimpleNamespace(body=SimpleNamespace(get_global_pose=lambda: (None, pose)))
        actual = PersistentPhysxFrontHalfScene._unity_native_angular_setter_vector(
            scene, slot, 0.009968042373657227
        )
        self.assertEqual(actual, [
            -8.798517470154366e-15,
            0.009968044236302376,
            1.3273107057898414e-09,
        ])

    def test_highcurl_projection_matches_unity_transform_not_body_pose(self):
        # A12 release 18, third setter: Unity Transform and PhysX body differ
        # by one float32 ULP, which is measurable after locked-axis projection.
        scene = SimpleNamespace(probe=SimpleNamespace(np=np))
        transform_q = (
            5.197146535351749e-08, -0.6250340938568115,
            -4.161447719752687e-08, 0.7805975079536438,
        )
        actual = PersistentPhysxFrontHalfScene._unity_project_locked_angular_velocity(
            scene, transform_q, 3.1206440925598145
        )
        self.assertEqual(actual, [
            1.3642420526593924e-12,
            3.1206445693969727,
            4.1554039853508584e-07,
        ])
        body_q = (
            5.197146180080381e-08, -0.6250340342521667,
            -4.161447364481319e-08, 0.780597448348999,
        )
        from_body = PersistentPhysxFrontHalfScene._unity_project_locked_angular_velocity(
            scene, body_q, 3.1206440925598145
        )
        self.assertNotEqual(from_body, actual)

    def test_sliding_setter_uses_unity_transform_float32_normalization(self):
        body_q = SimpleNamespace(
            x=5.197146180080381e-08, y=-0.6250340342521667,
            z=-4.161447364481319e-08, w=0.780597448348999,
        )
        scene = SimpleNamespace(
            probe=SimpleNamespace(np=np), _unity_angular_setter_calls={0: 2}
        )
        slot = SimpleNamespace(
            index=0, body=SimpleNamespace(get_global_pose=lambda: (None, body_q))
        )
        actual = PersistentPhysxFrontHalfScene._unity_native_angular_setter_vector(
            scene, slot, 3.1206440925598145
        )
        self.assertEqual(actual, [
            1.3642420526593924e-12,
            3.1206445693969727,
            4.1554039853508584e-07,
        ])
        self.assertEqual(scene._unity_angular_setter_calls[0], 3)

    def test_bestshot_release_pose_is_distinct_from_settled_pose(self):
        scene = SimpleNamespace(
            emulate_unity_bestshot_release_pose=True,
            coordinate_mode="unity-native-yup",
            start_motioninfo=Mock(),
            probe=SimpleNamespace(np=np),
        )
        PersistentPhysxFrontHalfScene.start_bestshot(scene, 0, [4.2, 0.0, 0.0])
        self.assertEqual(scene.start_motioninfo.call_args.kwargs["native_position_override"], [
            -96.85420227050781,
            14.43239974975586,
            54.174400329589844,
        ])

    def test_bestshot_release_pose_precedes_angular_setter_and_shape_activation(self):
        events = []
        body = SimpleNamespace(
            set_global_pose=Mock(side_effect=lambda pose: events.append(("pose", pose[0]))),
            set_linear_velocity=Mock(),
            set_angular_velocity=Mock(side_effect=lambda _value: events.append(("angular", None))),
            enable_gravity=Mock(),
            wake_up=Mock(),
        )
        shape = SimpleNamespace(set_flag=Mock(side_effect=lambda *_args: events.append(("shape", None))))
        slot = SimpleNamespace(
            body=body, shape=shape, enabled=False,
            material=SimpleNamespace(set_static_friction=Mock(), set_dynamic_friction=Mock()),
        )
        scene = SimpleNamespace(
            slots=[slot], probe=SimpleNamespace(np=np),
            coordinate_mode="unity-native-yup",
            emulate_unity_bestshot_release_pose=True,
            emulate_unity_setactive_no_sim=False,
            emulate_unity_native_angular_setter_rotation=True,
            repeat_pose_after_shape_activation=True,
            set_active_scene_membership=False,
            pyphysx=SimpleNamespace(ShapeFlag=SimpleNamespace(SIMULATION_SHAPE=1)),
            _unity_angular_setter_calls={},
            _yaw_quaternion=lambda _yaw: [1.0, 0.0, 0.0, 0.0],
            _horizontal_velocity=lambda *_args: [0.0, 0.0, 0.0],
            _unity_native_angular_setter_vector=lambda *_args: [0.0, 3.14, 0.0],
            _refresh_unity_setactive_interactions=Mock(),
            _refresh_unity_stone_geometry=Mock(),
        )
        scene.start_motioninfo = lambda *args, **kwargs: (
            PersistentPhysxFrontHalfScene.start_motioninfo(scene, *args, **kwargs)
        )
        PersistentPhysxFrontHalfScene.start_bestshot(scene, 0, [3.7, -0.25, 3.14], yaw=0.0)
        self.assertEqual([event[0] for event in events], ["pose", "angular", "shape", "pose"])
        self.assertEqual([event[1] for event in events if event[0] == "pose"], [
            [-96.85420227050781, 14.43239974975586, 54.424400329589844],
            [-96.85420227050781, 14.43239974975586, 54.424400329589844],
        ])

    def test_highcurl_reset_angular_setter_uses_locked_axis_projection(self):
        pose = SimpleNamespace(
            x=5.131396463298188e-08,
            y=-0.6371713876724243,
            z=-4.242256679276579e-08,
            w=0.7707220911979675,
        )
        body = SimpleNamespace(set_linear_velocity=Mock(), set_angular_velocity=Mock())
        slot = SimpleNamespace(body=body, material=SimpleNamespace(
            set_static_friction=Mock(), set_dynamic_friction=Mock()
        ), shape=SimpleNamespace(set_flag=Mock()), enabled=False)
        body.enable_gravity = Mock()
        body.wake_up = Mock()
        scene = SimpleNamespace(
            slots=[slot],
            _unity_angular_setter_calls={},
            emulate_unity_setactive_no_sim=False,
            emulate_unity_native_angular_setter_rotation=True,
            coordinate_mode="unity-native-yup",
            repeat_pose_after_shape_activation=False,
            set_active_scene_membership=False,
            pyphysx=SimpleNamespace(ShapeFlag=SimpleNamespace(SIMULATION_SHAPE=1)),
            probe=SimpleNamespace(np=np),
            _set_pose=Mock(),
            _horizontal_velocity=lambda *_args: [0.0, 0.0, 0.0],
            _refresh_unity_setactive_interactions=Mock(),
            _refresh_unity_stone_geometry=Mock(),
            _unity_native_angular_setter_vector=lambda _slot, value: (
                PersistentPhysxFrontHalfScene._unity_native_angular_setter_vector(
                    SimpleNamespace(probe=SimpleNamespace(np=np)),
                    SimpleNamespace(body=SimpleNamespace(get_global_pose=lambda: (None, pose))),
                    value,
                )
            ),
        )
        PersistentPhysxFrontHalfScene.start_motioninfo(
            scene, 0, [2.3506, 32.4768, 0.0, -3.7, 3.14], yaw=0.0
        )
        self.assertEqual(body.set_angular_velocity.call_args.args[0], [
            1.3784529073745944e-12,
            3.1399991512298584,
            4.18117622302816e-07,
        ])

    def test_physx_front_half_defaults_to_exact_native_angular_setter(self):
        parameter = inspect.signature(PersistentPhysxFrontHalfScene).parameters[
            "emulate_unity_native_angular_setter_rotation"
        ]
        self.assertTrue(parameter.default)
        tilt_parameter = inspect.signature(PersistentPhysxFrontHalfScene).parameters[
            "emulate_unity_native_angular_setter_tilt_only"
        ]
        self.assertFalse(tilt_parameter.default)

    def test_solver_free_slide_does_not_bypass_exact_projection(self):
        from local_simulator.runtime_loader import install_bundled_pyphysx
        from tools.reverse.recovered_unity_random import RecoveredUnityRandom
        install_bundled_pyphysx()
        environment = StrictCurlingEnd(seed=123)
        environment.reset()
        with patch.object(environment.scene,'step_custom_sliding',
                          wraps=environment.scene.step_custom_sliding) as step:
            result=environment.play((3.,0.,0.))
        self.assertTrue(result['settled'])
        self.assertEqual(result['frictionDraws'],step.call_count)
        self.assertGreater(result['frictionDraws'],2500)
        rng=RecoveredUnityRandom.from_seed(123)
        for _ in range(result['frictionDraws']):
            rng.next_u32()
        self.assertEqual(result['rngState'],[rng.s0,rng.s1,rng.s2,rng.s3])
        self.assertIsNone(environment.scene._custom_sliding_index)

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
