# -*- coding: utf-8 -*-
"""Persistent PhysX backend for Unity's MOTIONINFO -> first-contact path.

The backend keeps one Scene and stable actor/shape identities.  It applies the
recovered CurlingMotion velocity update before every 0.01 second Scene step and
lets PhysX create the stone-stone PCM pair naturally.  The production path
runs in Unity's native Y-up frame so the cooked hull topology is never reflected
into a frame with the opposite handedness.  ``pyphysx`` is imported lazily so
the protocol-only simulator remains usable in the normal Python environment.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

# Resolve the packaged reverse-engineering support before any checkout-level
# ``tools`` package.  This keeps the simulator portable after the evidence is
# archived away from the project root.
RUNTIME_SUPPORT_ROOT = Path(__file__).resolve().parent / "runtime_support"
if str(RUNTIME_SUPPORT_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SUPPORT_ROOT))

from tools.reverse.recovered_curling_motion import (
    BASE_FRICTION,
    STEP,
    UNITY_FIXED_TIMESTEP,
    B2Vec2,
    newfrictionstep,
    unity_friction,
)
from tools.reverse.front_half_pcm_replay import FIRST_PCM_CENTER_DISTANCE, local_initial_state


SIMULATOR_ROOT = Path(__file__).resolve().parent
DEFAULT_RUNTIME_HULL_ASSET = SIMULATOR_ROOT / "assets" / "unity_runtime_hull.json"
DEFAULT_RUNTIME_ICE_MESH = SIMULATOR_ROOT / "assets" / "unity_runtime_ice_triangle_mesh.json"
DEFAULT_FORMAL_STONE_MESH = SIMULATOR_ROOT / "assets" / "stone_extendedcollider_mesh_256.json"
COORDINATE_MODES = ("unity-native-yup", "legacy-zup")
ICE_MESH_MODES = (
    "reconstructed",
    "unity-runtime-postcook",
    "unity-source-once",
)

# Recovered from the native target pose in the first controlled PCM capture.
# Keeping Unity's world translation also preserves the float32 phase seen by PCM.
UNITY_NATIVE_ORIGIN_X = -64.37740020751953
UNITY_NATIVE_ORIGIN_Z = 56.525001525878906
# The ice mesh is anchored at UNITY_NATIVE_ORIGIN_X above, but the managed
# ResetPosition path evaluates its sheet-to-world X expression at a slightly
# higher precision and rounds only when it reaches the native rigid pose.
# C108 bracketed the hidden base with two fresh-page truths: y=6.2 remains
# -70.5774002075 while y=8 becomes -72.3773956299.  This value is in their
# shared rounding interval.  Do not collapse it to either observed float32
# endpoint (C107 showed that a global +1 ULP shift is wrong).
UNITY_NATIVE_POSITION_X_BASE = -64.377398
UNITY_NATIVE_ICE_Y = 14.304784545898437
UNITY_STONE_BASE_X = float.fromhex("0x1.1df46ap-24")
UNITY_STONE_SCALE_XZ = 0.11270000785589218
UNITY_STONE_SCALE_Y = 0.11500000208616257
UNITY_STONE_VERTICAL_INERTIA = 0.18922292609173136
# `DCP.UpdateState` applies its ordinary retained-area test in body-space.
# POSITION/reset coordinates carry the fixed (+2.375, +4.88) presentation
# offset, so these are the equivalent bounds in this backend's public state.
UNITY_RETAINED_PROTOCOL_X = (0.145, 4.605)
UNITY_RETAINED_PROTOCOL_Y = (2.865, 10.525)


def _normalize_yaw(yaw: float) -> float:
    while yaw > math.pi:
        yaw -= 2.0 * math.pi
    while yaw <= -math.pi:
        yaw += 2.0 * math.pi
    return yaw


@dataclass
class PhysxStoneSlot:
    index: int
    body: Any
    shape: Any
    material: Any
    enabled: bool = False
    in_scene: bool = True


class NativePyphysxMotionStepper:
    """Use the compiled f64 CurlingMotion kernel exposed by this pyphysx build.

    This is deliberately only a math-step replacement: callers still read the
    current local Scene state and still execute one PhysX simulation/contact
    step per Unity fixed tick.  It therefore cannot precompute a shot or skip
    PCM lifecycle work.
    """

    def __init__(self, pyphysx: Any) -> None:
        step = getattr(pyphysx, "curling_new_friction_step", None)
        if step is None:
            raise RuntimeError(
                "pyphysx lacks curling_new_friction_step; rebuild the scalar extension "
                "from curling_pyphysx_hybrid before selecting the native motion kernel"
            )
        self._step = step

    def step(self, *, friction: float, vx: float, vy: float, angle: float) -> tuple[float, float, float]:
        result = self._step(float(friction), float(vx), float(vy), float(angle), float(STEP))
        return float(result[0]), float(result[1]), float(result[2])

    def close(self) -> None:
        """Match the wasm stepper lifecycle; the in-process kernel owns no resource."""


def load_unity_runtime_ice_mesh(path: Path, np: Any) -> tuple[Any, Any, dict[str, Any]]:
    """Load the captured Unity PxTriangleMesh source arrays in native world coordinates."""
    document = json.loads(path.read_text(encoding="utf-8"))
    captures = document.get("captures")
    if not isinstance(captures, list):
        raise ValueError(f"runtime ice mesh has no captures: {path}")
    capture = next(
        (
            item
            for item in captures
            if isinstance(item, dict) and isinstance(item.get("decodedMesh"), dict)
        ),
        None,
    )
    if capture is None:
        raise ValueError(f"runtime ice mesh contains no complete vertex/index buffers: {path}")

    mesh = capture["decodedMesh"]
    layout = mesh.get("layout") if isinstance(mesh, dict) else None
    geometry = capture.get("triangleGeometry")
    pose = capture.get("transform1")
    if not isinstance(layout, dict) or not isinstance(geometry, dict) or not isinstance(pose, dict):
        raise ValueError(f"runtime ice mesh capture is structurally incomplete: {path}")
    if layout.get("indexWidth") != 2 or layout.get("nbVertices") != 121 or layout.get("nbTriangles") != 200:
        raise ValueError(f"unexpected Unity plane topology in {path}: {layout}")
    if geometry.get("scaleRotation") != [0, 0, 0, 1] or pose.get("q") != [0, 0, 0, 1]:
        raise ValueError("captured ice mesh has a non-identity rotation; add the verified transform path first")

    source_vertices = np.asarray(mesh.get("vertices"), dtype=np.float32)
    triangles = np.asarray(mesh.get("triangles"), dtype=np.int32)
    scale = np.asarray(geometry.get("scale"), dtype=np.float32)
    translation = np.asarray(pose.get("p"), dtype=np.float32)
    if source_vertices.shape != (121, 3) or triangles.shape != (200, 3):
        raise ValueError(f"unexpected Unity plane buffer dimensions in {path}")
    if int(triangles.min()) < 0 or int(triangles.max()) >= len(source_vertices):
        raise ValueError(f"runtime ice mesh index out of range in {path}")

    # PhysX receives the mesh-local vertices through this identity-rotation scale
    # and pose.  Keep every operation float32 before cooking the local equivalent.
    world_vertices = (source_vertices * scale + translation).astype(np.float32, copy=False)
    return world_vertices, triangles, {
        "path": str(path),
        "vertexSha256": (mesh.get("sha256") or {}).get("vertices"),
        "triangleSha256": (mesh.get("sha256") or {}).get("triangles"),
        "nbVertices": int(layout["nbVertices"]),
        "nbTriangles": int(layout["nbTriangles"]),
        "indexWidth": int(layout["indexWidth"]),
        "scale": [float(value) for value in scale],
        "translation": [float(value) for value in translation],
    }


def load_unity_builtin_plane_source(
    path: Path,
    np: Any,
) -> tuple[Any, Any, list[float], list[float], list[float], dict[str, Any]]:
    """Recover the built-in Plane's pre-scale cooking input from a runtime capture.

    The captured vertices remain in Unity's native source frame and must be
    combined with the captured PxMeshScale/static pose. Reusing Unity's
    ``mTriangles`` as this cooker's input is idempotent in that native frame:
    local PhysX reproduces all 200 cooked triangle rows and the 100-node BVH34.
    The v3 capture also carries the exact face-remap/raw BV4 truth.
    """
    document = json.loads(path.read_text(encoding="utf-8"))
    captures = document.get("captures")
    if not isinstance(captures, list):
        raise ValueError(f"runtime ice mesh has no captures: {path}")
    capture = next(
        (
            item
            for item in captures
            if isinstance(item, dict)
            and isinstance(item.get("decodedMesh"), dict)
            and isinstance(item.get("triangleGeometry"), dict)
        ),
        None,
    )
    if capture is None:
        raise ValueError(f"runtime ice mesh contains no complete mesh/geometry capture: {path}")

    mesh = dict(capture["decodedMesh"])
    geometry = dict(capture["triangleGeometry"])
    vertices = np.asarray(mesh.get("vertices"), dtype=np.float32)
    layout = dict(mesh.get("layout") or {})
    if vertices.shape != (121, 3) or int(layout.get("nbTriangles") or 0) != 200:
        raise ValueError("expected Unity built-in 10x10 Plane (121 vertices, 200 triangles)")
    scale = [float(value) for value in geometry.get("scale") or []]
    if len(scale) != 3:
        raise ValueError("Unity Plane capture has no PxMeshScale")

    triangles = np.asarray(mesh.get("triangles"), dtype=np.int32)
    if triangles.shape != (200, 3):
        raise ValueError("Unity Plane capture has no complete mTriangles array")

    transform = capture.get("transform1")
    if not isinstance(transform, dict):
        raise ValueError("Unity Plane capture has no static actor PxTransform")
    position = [float(value) for value in transform.get("p") or []]
    native_quaternion = [float(value) for value in transform.get("q") or []]
    if len(position) != 3 or len(native_quaternion) != 4:
        raise ValueError("Unity Plane static actor PxTransform is incomplete")
    quaternion_wxyz = [
        native_quaternion[3],
        native_quaternion[0],
        native_quaternion[1],
        native_quaternion[2],
    ]
    return vertices, np.asarray(triangles, dtype=np.int32), scale, position, quaternion_wxyz, {
        "path": str(path),
        "mode": "unity-source-once",
        "vertexSha256": (mesh.get("sha256") or {}).get("vertices"),
        "unityCookedTriangleSha256": (mesh.get("sha256") or {}).get("triangles"),
        "sourceInputTriangleOrder": "captured Unity Gu::TriangleMesh.mTriangles reused directly",
        "scale": scale,
        "actorPosition": position,
        "actorQuaternionWxyz": quaternion_wxyz,
    }


def load_unity_runtime_ice_face_remap(path: Path) -> list[int]:
    """Load the runtime Gu::TriangleMesh face-remap truth from a v3 capture."""
    document = json.loads(path.read_text(encoding="utf-8"))
    for capture in document.get("captures") or []:
        if not isinstance(capture, dict):
            continue
        internals = capture.get("decodedCookedInternals")
        if not isinstance(internals, dict):
            continue
        values = internals.get("faceRemap")
        if isinstance(values, list) and len(values) == 200:
            return [int(value) for value in values]
    raise ValueError(f"runtime ice capture has no complete face-remap: {path}")


class PersistentPhysxFrontHalfScene:
    """One-end Scene with stable stone identities and native PCM lifecycle."""

    def __init__(
        self,
        *,
        stone_count: int = 16,
        formal_stone_mesh: Optional[Path] = None,
        runtime_hull_asset: Optional[Path] = DEFAULT_RUNTIME_HULL_ASSET,
        patch_runtime_features: bool = True,
        ice_use_fast_midphase: bool = False,
        # Unity's source, scale, cooked triangle ordering and BVH34 data are verified.
        # Keep the scalar fallback on BVH33 without returning to a hand-built plane.
        ice_mesh_mode: str = "unity-source-once",
        coordinate_mode: str = "unity-native-yup",
        require_p4_contact_hooks: bool = True,
        set_active_scene_membership: bool = False,
        restore_active_friction_at_pcm_shell: bool = False,
        enable_stone_stone_contact_friction_override: bool = True,
        stone_stone_contact_static_friction: float = 0.36,
        stone_stone_contact_dynamic_friction: float = 0.36,
        emulate_unity_first_pair_zero_friction: bool = True,
        enable_unity_pcm_task_cache_lifecycle: bool = True,
        enable_unity_pcm_multi_cache_lifecycle: bool = True,
        repeat_pose_after_shape_activation: bool = True,
        emulate_unity_setactive_refilter: bool = True,
        emulate_unity_setactive_no_sim: bool = False,
        emulate_unity_native_angular_setter_rotation: bool = False,
        emulate_unity_native_angular_setter_residual_z: bool = False,
        emulate_unity_native_angular_setter_tilt_only: bool = True,
        wake_target_at_current_pcm_shell: bool = False,
        custom_sliding_zero_vertical_setter: bool = False,
    ) -> None:
        if stone_count <= 0:
            raise ValueError("stone_count must be positive")
        if coordinate_mode not in COORDINATE_MODES:
            raise ValueError(
                f"coordinate_mode must be one of {COORDINATE_MODES}, got {coordinate_mode!r}"
            )
        if ice_mesh_mode not in ICE_MESH_MODES:
            raise ValueError(f"ice_mesh_mode must be one of {ICE_MESH_MODES}, got {ice_mesh_mode!r}")

        try:
            from tools.reverse import probe_physx_collision_alignment as probe
        except (ImportError, SystemExit) as exc:  # pragma: no cover - external environment.
            raise RuntimeError(
                "PersistentPhysxFrontHalfScene requires the rebuilt pyphysx environment"
            ) from exc

        self.probe = probe
        self.pyphysx = probe.pyphysx
        scalar_check = getattr(self.pyphysx, "is_scalar_math_enabled", None)
        if scalar_check is None or not scalar_check():
            raise RuntimeError(
                "PersistentPhysxFrontHalfScene requires the scalar PhysX build "
                "to match Unity WebGL PCM contact generation."
            )
        self.coordinate_mode = coordinate_mode
        self.set_active_scene_membership = bool(set_active_scene_membership)
        # Diagnostic-only switch: replace the local contact-modify callback with
        # the observed Unity material state before the first solver tick.
        self.restore_active_friction_at_pcm_shell = bool(restore_active_friction_at_pcm_shell)
        self.enable_stone_stone_contact_friction_override = bool(
            enable_stone_stone_contact_friction_override
        )
        self.stone_stone_contact_static_friction = float(stone_stone_contact_static_friction)
        self.stone_stone_contact_dynamic_friction = float(stone_stone_contact_dynamic_friction)
        if self.stone_stone_contact_static_friction < 0.0 or self.stone_stone_contact_dynamic_friction < 0.0:
            raise ValueError("stone--stone contact friction overrides must be non-negative")
        self.emulate_unity_first_pair_zero_friction = bool(emulate_unity_first_pair_zero_friction)
        self.enable_unity_pcm_task_cache_lifecycle = bool(
            enable_unity_pcm_task_cache_lifecycle
        )
        self.enable_unity_pcm_multi_cache_lifecycle = bool(
            enable_unity_pcm_multi_cache_lifecycle
        )
        # Diagnostic switch for the recovered MeshCollider activation order.
        # Unity executes transform/shape refresh before the collider runtime
        # refresh; the legacy local path writes the pose once more afterwards.
        self.repeat_pose_after_shape_activation = bool(repeat_pose_after_shape_activation)
        # Unity refreshes the interaction graph after its SetActive shape
        # transition.  Leaving the local pair stale produces centimetre-scale
        # glancing endpoint errors; therefore refilter is now the production
        # default.  It remains switchable for historical A/B audits.
        self.emulate_unity_setactive_refilter = bool(emulate_unity_setactive_refilter)
        # Diagnostic timing switch. The legacy local bridge wakes a stationary
        # target when the *predicted next* active pose enters the PCM shell.
        # Unity C05 shows the target core remains unchanged until the current
        # pose is in the shell, so this is kept opt-in until 14000 closes.
        self.wake_target_at_current_pcm_shell = bool(wake_target_at_current_pcm_shell)
        # Source-backed B-chain candidate: PxActorFlag::eDISABLE_SIMULATION
        # preserves the PxActor/PxShape objects while removing the internal
        # RigidSim. Re-enabling creates a new RigidSim and therefore a new
        # RigidID, which is the value PhysX uses to order a new ShapeInteraction.
        self.emulate_unity_setactive_no_sim = bool(emulate_unity_setactive_no_sim)
        if self.emulate_unity_setactive_no_sim and self.set_active_scene_membership:
            raise ValueError(
                "eDISABLE_SIMULATION SetActive emulation cannot be combined with "
                "Scene.remove_actor/add_actor"
            )
        # Unity's native angular-velocity setter rotates the script-space vector
        # through the current body quaternion before writing its internal target.
        # This is source-backed and required by the production no-oracle path.
        self.emulate_unity_native_angular_setter_rotation = bool(
            emulate_unity_native_angular_setter_rotation
        )
        self.emulate_unity_native_angular_setter_residual_z = bool(
            emulate_unity_native_angular_setter_residual_z
        )
        self.emulate_unity_native_angular_setter_tilt_only = bool(
            emulate_unity_native_angular_setter_tilt_only
        )
        if self.emulate_unity_native_angular_setter_rotation and self.emulate_unity_native_angular_setter_tilt_only:
            raise ValueError("full and tilt-only native angular setter modes are mutually exclusive")
        # Diagnostic-only until an end-to-end R0 fixture proves that DCP writes
        # Rigidbody.linearVelocity with a literal zero Y component throughout
        # the release-to-contact airborne interval.
        self.custom_sliding_zero_vertical_setter = bool(custom_sliding_zero_vertical_setter)
        self.dt = UNITY_FIXED_TIMESTEP
        self.center_height = probe.HEIGHT / 2.0
        self.combine_mode = probe._combine_mode_from_name("multiply")
        self.scene = self.pyphysx.Scene(
            scene_flags=[],
            bounce_threshold_velocity=0.05,
            enable_contact_report=True,
        )
        has_pair_modify = hasattr(self.scene, "set_stone_stone_contact_friction_override")
        has_pcm_lifecycle = hasattr(self.pyphysx, "set_scene_pcm_unity_cache_lifecycle_enabled")
        has_multi_cache_lifecycle = hasattr(
            self.pyphysx, "set_scene_narrowphase_unity_multi_cache_lifecycle_enabled"
        )
        has_remove_actor = hasattr(self.scene, "remove_actor")
        if require_p4_contact_hooks and not has_pair_modify:
            raise RuntimeError("scalar pyphysx is missing the P4 pair-contact modification binding")
        if require_p4_contact_hooks and not has_pcm_lifecycle:
            raise RuntimeError("scalar pyphysx is missing the P4 PCM cache-lifecycle binding")
        if require_p4_contact_hooks and not has_multi_cache_lifecycle:
            raise RuntimeError("scalar pyphysx is missing the C19 PCM multi-cache lifecycle binding")
        if self.set_active_scene_membership and not has_remove_actor:
            raise RuntimeError("pyphysx is missing Scene.remove_actor for SetActive semantics")
        if self.emulate_unity_setactive_refilter and not hasattr(self.scene, "reset_filtering"):
            raise RuntimeError("pyphysx is missing Scene.reset_filtering for Unity SetActive emulation")
        if self.emulate_unity_setactive_no_sim and not hasattr(self.pyphysx, "ActorFlag"):
            raise RuntimeError("pyphysx is missing PxActorFlag bindings for Unity SetActive emulation")
        # The normal post-contact stone--stone state uses 0.36/0.36.  A C04
        # capture shows the *first* dynamic solver frame is a distinct zero
        # friction handoff; that must be modeled as a one-frame transition,
        # not by changing this persistent default.  The only permitted
        # hook-free caller is the isolated BVH4 ground probe.
        if has_pair_modify:
            self.scene.set_stone_stone_contact_friction_override(
                self.enable_stone_stone_contact_friction_override,
                self.stone_stone_contact_static_friction,
                self.stone_stone_contact_dynamic_friction,
            )
        self._has_stone_stone_contact_friction_override = has_pair_modify
        if has_pcm_lifecycle:
            self.pyphysx.set_scene_pcm_unity_cache_lifecycle_enabled(
                self.enable_unity_pcm_task_cache_lifecycle
            )
        if has_multi_cache_lifecycle:
            self.pyphysx.set_scene_narrowphase_unity_multi_cache_lifecycle_enabled(
                self.enable_unity_pcm_multi_cache_lifecycle
            )

        if self.coordinate_mode == "unity-native-yup":
            self.scene.set_gravity([0.0, -9.81, 0.0])
        self._custom_sliding_index: Optional[int] = None

        ice_material = probe._make_material(
            0.02,
            0.02,
            0.0,
            combine_mode=self.combine_mode,
            disable_strong_friction=False,
            improved_patch_friction=False,
        )
        if self.coordinate_mode == "unity-native-yup":
            # The captured Gu::TriangleMesh arrays are post-cooking output.  Passing
            # them to create_triangle_mesh_from_points would cook the topology a
            # second time, so this path remains the single-cook reconstruction until
            # the Unity BV4 midphase can be imported directly.
            ice_mesh_scale: Optional[list[float]] = None
            ice_actor_position: Optional[list[float]] = None
            ice_actor_quaternion: Optional[list[float]] = None
            if ice_mesh_mode == "unity-source-once":
                (
                    vertices,
                    triangles,
                    ice_mesh_scale,
                    ice_actor_position,
                    ice_actor_quaternion,
                    captured_meta,
                ) = load_unity_builtin_plane_source(DEFAULT_RUNTIME_ICE_MESH, self.probe.np)
                self.runtime_ice_mesh_meta = {
                    **captured_meta,
                    "cookedEquivalence": "Unity raw vertices/triangles/face-remap/BVH34 nodes verified byte-for-byte",
                    "useFastMidphase": bool(ice_use_fast_midphase),
                }
            elif ice_mesh_mode == "unity-runtime-postcook":
                vertices, triangles, captured_meta = load_unity_runtime_ice_mesh(
                    DEFAULT_RUNTIME_ICE_MESH, self.probe.np
                )
                self.runtime_ice_mesh_meta = {
                    **captured_meta,
                    "mode": ice_mesh_mode,
                    "warning": "runtime mesh is post-cook output; audit only, local cooking still rebuilds BV4",
                    "useFastMidphase": bool(ice_use_fast_midphase),
                }
            else:
                vertices = []
                subdivisions = probe.UNITY_PLANE_MESH_SUBDIVISIONS
                for iy in range(subdivisions + 1):
                    protocol_y = (
                        probe.UNITY_PLANE_MESH_CENTER_Y_M
                        - 0.5 * probe.UNITY_PLANE_MESH_LENGTH_M
                        + probe.UNITY_PLANE_MESH_LENGTH_M * iy / subdivisions
                    )
                    for ix in range(subdivisions + 1):
                        protocol_x = (
                            probe.UNITY_PLANE_MESH_CENTER_X_M
                            - 0.5 * probe.UNITY_PLANE_MESH_WIDTH_M
                            + probe.UNITY_PLANE_MESH_WIDTH_M * ix / subdivisions
                        )
                        vertices.append(
                            [
                                UNITY_NATIVE_ORIGIN_X - protocol_y,
                                UNITY_NATIVE_ICE_Y,
                                UNITY_NATIVE_ORIGIN_Z - protocol_x,
                            ]
                        )
                triangles = []
                row_width = subdivisions + 1
                for iy in range(subdivisions):
                    for ix in range(subdivisions):
                        v00 = iy * row_width + ix
                        v10 = v00 + 1
                        v01 = v00 + row_width
                        v11 = v01 + 1
                        triangles.append([v00, v10, v01])
                        triangles.append([v01, v10, v11])
                self.runtime_ice_mesh_meta = {
                    "enabled": False,
                    "mode": ice_mesh_mode,
                    "reason": "captured Gu::TriangleMesh is post-cook output; direct import pending",
                    "capturedMeshPath": str(DEFAULT_RUNTIME_ICE_MESH),
                    "useFastMidphase": bool(ice_use_fast_midphase),
                }
            mesh_points = self.probe.np.asarray(vertices, dtype=self.probe.np.float32)
            mesh_triangles = self.probe.np.asarray(triangles, dtype=self.probe.np.int32)
            mesh_kwargs = {
                "is_exclusive": True,
                "weld_vertices": True,
                "disable_clean_mesh": False,
                "disable_active_edges_precompute": False,
                "force_32bit_indices": False,
                # Unity uses BVH34, but the local scalar PhysX backend cannot
                # execute BV4 (the upstream implementation excludes it when
                # PX_SIMD_DISABLED is set). Keep BVH33 as the executable
                # fallback until a scalar BV4 path is available.
                "use_fast_midphase": ice_use_fast_midphase,
                "build_gpu_data": False,
            }
            if ice_mesh_scale is None:
                ice_shape = self.pyphysx.Shape.create_triangle_mesh_from_points(
                    mesh_points,
                    mesh_triangles,
                    ice_material,
                    scale=1.0,
                    **mesh_kwargs,
                )
            else:
                ice_shape = self.pyphysx.Shape.create_triangle_mesh_from_points_with_scale(
                    mesh_points,
                    mesh_triangles,
                    ice_material,
                    scale=ice_mesh_scale,
                    **mesh_kwargs,
                )
                # The captured remap belongs to Unity's BVH34 mesh. Do not put
                # it on the scalar backend's different BVH33 fallback: face
                # IDs do not affect support physics, but this pyphysx fallback
                # expects its own remap ordering during mesh-pair reporting.
                if ice_use_fast_midphase:
                    face_remap = load_unity_runtime_ice_face_remap(DEFAULT_RUNTIME_ICE_MESH)
                    remap_patch = ice_shape.patch_triangle_mesh_face_remap_for_unity(face_remap)
                    if not remap_patch.get("ok"):
                        raise RuntimeError(f"failed to patch Unity ice face-remap: {remap_patch}")
                    self.runtime_ice_mesh_meta["faceRemapPatched"] = True
                    self.runtime_ice_mesh_meta["faceRemapCount"] = len(face_remap)
                else:
                    self.runtime_ice_mesh_meta["faceRemapPatched"] = False
                    self.runtime_ice_mesh_meta["faceRemapReason"] = "BVH33 fallback keeps its local remap"
            self.ice = self.pyphysx.RigidStatic()
            self.ice.attach_shape(ice_shape)
            if ice_actor_position is not None and ice_actor_quaternion is not None:
                self.ice.set_global_pose((ice_actor_position, ice_actor_quaternion))
        else:
            self.runtime_ice_mesh_meta = {"enabled": False, "coordinateMode": coordinate_mode}
            self.ice = self.pyphysx.RigidStatic.create_plane(
                ice_material,
                0.0,
                0.0,
                1.0,
                0.0,
            )
        for shape in self.ice.get_atached_shapes():
            shape.set_contact_offset(0.01)
            shape.set_rest_offset(0.0)
        self.scene.add_actor(self.ice)

        mesh_path = Path(formal_stone_mesh or DEFAULT_FORMAL_STONE_MESH)
        stone_points = probe._formal_stone_points(mesh_path)
        if self.coordinate_mode == "unity-native-yup":
            stone_points = stone_points[:, [0, 2, 1]]
        runtime_hull, runtime_bigconvex, runtime_meta = self._runtime_features(
            Path(runtime_hull_asset) if runtime_hull_asset is not None else None,
            patch_runtime_features,
        )
        self.runtime_feature_meta = runtime_meta

        self.slots: list[PhysxStoneSlot] = []
        self._address_to_index: dict[int, int] = {}
        for index in range(stone_count):
            body, shape, material, _patch = probe._make_stone(
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                stone_points=stone_points,
                radius=probe.RADIUS,
                height=probe.HEIGHT,
                stone_faces=256,
                inertia_model="solid-cylinder",
                inertia_radial=None,
                inertia_vertical=None,
                center_height=self.center_height,
                stone_friction=0.6,
                static_friction=0.6,
                dynamic_friction=0.6,
                stone_restitution=1.0,
                combine_mode=self.combine_mode,
                contact_offset=0.01,
                rest_offset=0.0,
                shape_local_x=0.0,
                shape_local_y=0.0,
                shape_local_z=0.0,
                shape_local_yaw=0.0,
                convex_quantized_count=255,
                convex_vertex_limit=255,
                convex_mesh_scale=(
                    [UNITY_STONE_SCALE_XZ, UNITY_STONE_SCALE_Y, UNITY_STONE_SCALE_XZ]
                    if self.coordinate_mode == "unity-native-yup"
                    else [UNITY_STONE_SCALE_XZ, UNITY_STONE_SCALE_XZ, UNITY_STONE_SCALE_Y]
                ),
                quantize_input=False,
                gpu_compatible=False,
                runtime_hull_raw_bytes=runtime_hull,
                runtime_big_convex_arrays=runtime_bigconvex,
                solver_position_iterations=6,
                solver_velocity_iterations=1,
                max_depenetration_velocity=10.0,
                lock_upright=False,
                disable_stone_gravity=False,
                disable_strong_friction=False,
                improved_patch_friction=False,
            )
            if self.coordinate_mode == "unity-native-yup":
                body.set_mass_space_inertia_tensor(
                    # Unity's first stone-stone PxSolverBodyData has zero X/Z
                    # inverse inertia and the recovered yaw-axis inertia below.
                    # PhysX lock flags alone retain X/Z solver inertia, so they
                    # cannot reproduce Unity's normal-contact rows by themselves.
                    [0.0, UNITY_STONE_VERTICAL_INERTIA, 0.0]
                )
                body.set_rigid_dynamic_lock_flag(
                    self.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_X, True
                )
                body.set_rigid_dynamic_lock_flag(
                    self.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_Z, True
                )
                body.set_global_pose(
                    (self._horizontal_position(0.0, 0.0), self._yaw_quaternion(0.0))
                )
            shape.set_flag(self.pyphysx.ShapeFlag.SIMULATION_SHAPE, False)
            body.disable_gravity()
            if self.emulate_unity_setactive_no_sim:
                body.set_actor_flag(self.pyphysx.ActorFlag.DISABLE_SIMULATION, True)
            # Unity's active stone is enabled after the already-placed target.
            # In PhysX this also gives it the later RigidID used by
            # createShapeInteraction's dynamic-dynamic sorting rule. The
            # membership diagnostic must therefore not pre-add every actor.
            in_scene = not self.set_active_scene_membership
            if in_scene:
                self.scene.add_actor(body)
            slot = PhysxStoneSlot(
                index=index,
                body=body,
                shape=shape,
                material=material,
                in_scene=in_scene,
            )
            self.slots.append(slot)
            self._address_to_index[int(body.get_physx_address())] = index

    def _runtime_features(
        self,
        hull_asset_path: Optional[Path],
        enabled: bool,
    ) -> tuple[Optional[list[int]], Optional[dict[str, list[int]]], dict[str, Any]]:
        if not enabled:
            return None, None, {"enabled": False}
        if hull_asset_path is None or not hull_asset_path.exists():
            raise FileNotFoundError(f"runtime hull asset not found: {hull_asset_path}")

        from tools.reverse.rebuild_bigconvex_from_runtime_hull import (
            _rebuild_from_runtime_hull,
        )

        bundle = json.loads(hull_asset_path.read_text(encoding="utf-8"))
        raw = [int(value) & 0xFF for value in bundle["hull_raw_bytes"]]
        source = self.probe._runtime_hull_source_from_bundle(raw, bundle)
        if self.coordinate_mode == "unity-native-yup":
            runtime_hull = raw
            rebuild_source = dict(source)
            rebuild_source["raw"] = bytes(runtime_hull)
            bigconvex_source = "rebuilt_from_native_runtime_hull_subdiv16"
        else:
            runtime_hull = self.probe._transform_runtime_hull_raw_unity_xyz_to_pyphysx_xzy(
                raw,
                layout=source["layout"],
                nb_polygons=int(source["nb_polygons"]),
                nb_vertices=int(source["nb_vertices"]),
            )
            rebuild_source = dict(source)
            rebuild_source["raw"] = bytes(runtime_hull)
            bigconvex_source = "rebuilt_from_transformed_runtime_hull_subdiv16"
        rebuilt = _rebuild_from_runtime_hull(rebuild_source, 16)
        bigconvex = self.probe._bigconvex_arrays_from_rebuild(rebuilt)
        return runtime_hull, bigconvex, {
            "enabled": True,
            "hullAsset": str(hull_asset_path),
            "coordinateMode": self.coordinate_mode,
            "hullBytes": len(runtime_hull),
            "hullSha16": self.probe._sha16_bytes(runtime_hull),
            "bigConvexSource": bigconvex_source,
        }

    def _horizontal_position(self, x: float, y: float) -> list[float]:
        if self.coordinate_mode == "unity-native-yup":
            return [
                UNITY_NATIVE_POSITION_X_BASE - float(y),
                UNITY_NATIVE_ICE_Y + self.center_height,
                UNITY_NATIVE_ORIGIN_Z - float(x),
            ]
        px, py = self.probe._to_physx_xy(float(x), float(y), True)
        return [px, py, self.center_height]

    def _horizontal_velocity(self, vx: float, vy: float, vertical: float) -> list[float]:
        if self.coordinate_mode == "unity-native-yup":
            return [-float(vy), float(vertical), -float(vx)]
        pvx, pvy = self.probe._to_physx_xy(float(vx), float(vy), True)
        return [pvx, pvy, float(vertical)]

    def _yaw_quaternion(self, yaw: float) -> list[float]:
        half_yaw = 0.5 * float(yaw)
        if self.coordinate_mode == "unity-native-yup":
            cosine = math.cos(half_yaw)
            sine = math.sin(half_yaw)
            # Asset local rotation xyzw=(base_x, 0, 0, 1), followed by Y yaw.
            return [cosine, UNITY_STONE_BASE_X * cosine, sine, UNITY_STONE_BASE_X * sine]
        return [math.cos(half_yaw), 0.0, 0.0, math.sin(half_yaw)]

    def _pose(self, index: int) -> tuple[list[float], list[float]]:
        position, quaternion = self.pyphysx.cast_transformation(
            self.slots[index].body.get_global_pose()
        )
        return (
            [float(value) for value in position],
            [
                float(getattr(quaternion, "w")),
                float(getattr(quaternion, "x")),
                float(getattr(quaternion, "y")),
                float(getattr(quaternion, "z")),
            ],
        )

    def state(self, index: int) -> dict[str, Any]:
        slot = self.slots[index]
        position, quaternion = self._pose(index)
        linear = [float(value) for value in slot.body.get_linear_velocity()]
        angular = [float(value) for value in slot.body.get_angular_velocity()]
        if self.coordinate_mode == "unity-native-yup":
            x = UNITY_NATIVE_ORIGIN_Z - position[2]
            y = UNITY_NATIVE_POSITION_X_BASE - position[0]
            z = position[1] - UNITY_NATIVE_ICE_Y
            vx = -linear[2]
            vy = -linear[0]
            vz = linear[1]
            yaw = _normalize_yaw(2.0 * math.atan2(quaternion[2], quaternion[0]))
            wx = angular[0]
            wy = angular[2]
            w = angular[1]
        else:
            x, y = self.probe._from_physx_xy(position[0], position[1], True)
            vx, vy = self.probe._from_physx_xy(linear[0], linear[1], True)
            z = position[2]
            vz = linear[2]
            yaw = _normalize_yaw(2.0 * math.atan2(quaternion[3], quaternion[0]))
            wx = angular[0]
            wy = angular[1]
            w = angular[2]
        return {
            "index": index,
            "enabled": slot.enabled,
            "x": x,
            "y": y,
            "z": z,
            "yaw": yaw,
            "vx": vx,
            "vy": vy,
            "vz": vz,
            "wx": wx,
            "wy": wy,
            "w": w,
            "physxPosition": position,
            "quaternionWxyz": quaternion,
            "physxLinearVelocity": linear,
            "physxAngularVelocity": angular,
        }

    def activation_audit_state(self, index: int) -> dict[str, Any]:
        """Return the local native fields relevant to Unity SetActive auditing."""
        slot = self.slots[index]
        body = slot.body
        shape = slot.shape
        material = slot.material
        com_position, com_quaternion = self.pyphysx.cast_transformation(
            body.get_center_of_mass_local_pose()
        )
        shape_position, shape_quaternion = self.pyphysx.cast_transformation(shape.get_local_pose())
        return {
            "index": index,
            "enabled": bool(slot.enabled),
            "inScene": bool(slot.in_scene),
            "bodyAddress": int(body.get_physx_address()),
            "globalPose": self._pose(index),
            "linearVelocity": [float(value) for value in body.get_linear_velocity()],
            "angularVelocity": [float(value) for value in body.get_angular_velocity()],
            "sleeping": bool(body.is_sleeping()),
            "mass": float(body.get_mass()),
            "massSpaceInertia": [float(value) for value in body.get_mass_space_inertia_tensor()],
            "centerOfMassLocalPose": {
                "p": [float(value) for value in com_position],
                "qWxyz": [
                    float(getattr(com_quaternion, "w")),
                    float(getattr(com_quaternion, "x")),
                    float(getattr(com_quaternion, "y")),
                    float(getattr(com_quaternion, "z")),
                ],
            },
            "solverIterations": [int(value) for value in body.get_solver_iteration_counts()],
            "maxDepenetrationVelocity": float(body.get_max_depenetration_velocity()),
            "lockFlags": {
                "angularX": bool(
                    body.get_rigid_dynamic_lock_flag_value(
                        self.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_X
                    )
                ),
                "angularY": bool(
                    body.get_rigid_dynamic_lock_flag_value(
                        self.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_Y
                    )
                ),
                "angularZ": bool(
                    body.get_rigid_dynamic_lock_flag_value(
                        self.pyphysx.RigidDynamicLockFlag.LOCK_ANGULAR_Z
                    )
                ),
            },
            "shape": {
                "simulationShape": bool(
                    shape.get_flag_value(self.pyphysx.ShapeFlag.SIMULATION_SHAPE)
                ),
                "localPose": {
                    "p": [float(value) for value in shape_position],
                    "qWxyz": [
                        float(getattr(shape_quaternion, "w")),
                        float(getattr(shape_quaternion, "x")),
                        float(getattr(shape_quaternion, "y")),
                        float(getattr(shape_quaternion, "z")),
                    ],
                },
                "contactOffset": float(shape.get_contact_offset()),
                "restOffset": float(shape.get_rest_offset()),
            },
            "material": {
                "staticFriction": float(material.get_static_friction()),
                "dynamicFriction": float(material.get_dynamic_friction()),
                "restitution": float(material.get_restitution()),
                "frictionCombine": str(material.get_friction_combine_mode()),
            },
        }

    def _set_pose(self, index: int, x: float, y: float, yaw: float) -> None:
        self.slots[index].body.set_global_pose(
            (self._horizontal_position(x, y), self._yaw_quaternion(yaw))
        )

    def _set_position_preserve_orientation(self, index: int, x: float, y: float) -> None:
        _position, quaternion = self._pose(index)
        self.slots[index].body.set_global_pose(
            (self._horizontal_position(x, y), quaternion)
        )

    def _refresh_unity_setactive_interactions(self, slot: PhysxStoneSlot) -> None:
        if self.emulate_unity_setactive_refilter:
            self.scene.reset_filtering(slot.body)

    def deactivate(self, index: int, x: float = 0.0, y: float = 0.0) -> None:
        slot = self.slots[index]
        if self.set_active_scene_membership and slot.in_scene:
            self.scene.remove_actor(slot.body)
            slot.in_scene = False
        slot.shape.set_flag(self.pyphysx.ShapeFlag.SIMULATION_SHAPE, False)
        slot.body.disable_gravity()
        slot.body.set_linear_velocity([0.0, 0.0, 0.0])
        slot.body.set_angular_velocity([0.0, 0.0, 0.0])
        self._set_position_preserve_orientation(index, x, y)
        slot.material.set_static_friction(0.6)
        slot.material.set_dynamic_friction(0.6)
        slot.body.put_to_sleep()
        if self.emulate_unity_setactive_no_sim:
            slot.body.set_actor_flag(self.pyphysx.ActorFlag.DISABLE_SIMULATION, True)
        slot.enabled = False
        if self._custom_sliding_index == index:
            self._custom_sliding_index = None

    def clear_out_of_play_stones(self) -> list[int]:
        """Apply Unity `UpdateState`'s normal out-of-play lifecycle pass.

        This only implements the ordinary rink/play-area removal.  R7's
        centre-line rule has additional turn/history and player-choice state,
        so it belongs to the match controller rather than this physics scene.
        """

        min_x, max_x = UNITY_RETAINED_PROTOCOL_X
        min_y, max_y = UNITY_RETAINED_PROTOCOL_Y
        cleared: list[int] = []
        for slot in self.slots:
            if not slot.enabled:
                continue
            state = self.state(slot.index)
            if min_x < state["x"] < max_x and min_y < state["y"] < max_y:
                continue
            self.deactivate(slot.index)
            cleared.append(slot.index)
        return cleared

    def activate_stationary(self, index: int, x: float, y: float, yaw: Optional[float] = None) -> None:
        slot = self.slots[index]
        if self.emulate_unity_setactive_no_sim:
            # PxRigidDynamic velocity/sleep APIs are invalid while no-sim is
            # raised. Restore the internal RigidSim before rebuilding state.
            slot.body.set_actor_flag(self.pyphysx.ActorFlag.DISABLE_SIMULATION, False)
        if yaw is None:
            self._set_position_preserve_orientation(index, x, y)
        else:
            self._set_pose(index, x, y, yaw)
        slot.body.set_linear_velocity([0.0, 0.0, 0.0])
        slot.body.set_angular_velocity([0.0, 0.0, 0.0])
        slot.material.set_static_friction(0.6)
        slot.material.set_dynamic_friction(0.6)
        slot.body.enable_gravity()
        slot.shape.set_flag(self.pyphysx.ShapeFlag.SIMULATION_SHAPE, True)
        if self.repeat_pose_after_shape_activation:
            if yaw is None:
                self._set_position_preserve_orientation(index, x, y)
            else:
                self._set_pose(index, x, y, yaw)
        self._refresh_unity_setactive_interactions(slot)
        if self.set_active_scene_membership and not slot.in_scene:
            self.scene.add_actor(slot.body)
            slot.in_scene = True
        slot.body.put_to_sleep()
        slot.enabled = True

    def reset_positions(
        self,
        position: Sequence[float],
        *,
        yaw_overrides: Optional[dict[int, float]] = None,
        settle_steps: int = 1,
        force_sleep_after_reset: bool = True,
    ) -> None:
        if len(position) < 2 * len(self.slots):
            raise ValueError(f"position must contain at least {2 * len(self.slots)} values")
        yaw_overrides = yaw_overrides or {}
        for index in range(len(self.slots)):
            x = float(position[2 * index])
            y = float(position[2 * index + 1])
            if x != 0.0 or y != 0.0:
                self.activate_stationary(index, x, y, yaw_overrides.get(index))
            else:
                self.deactivate(index)
        for _ in range(max(0, int(settle_steps))):
            self.scene.simulate(self.dt)
            self.scene.get_contact_reports()
        if force_sleep_after_reset:
            for slot in self.slots:
                if slot.enabled:
                    slot.body.set_linear_velocity([0.0, 0.0, 0.0])
                    slot.body.set_angular_velocity([0.0, 0.0, 0.0])
                    slot.body.put_to_sleep()

    def start_motioninfo(
        self,
        active_index: int,
        motioninfo: Sequence[float],
        *,
        yaw: Optional[float] = None,
    ) -> None:
        if len(motioninfo) < 5:
            raise ValueError("motioninfo must contain x, y, vx, vy, w")
        x, y, vx, vy, w = [float(value) for value in motioninfo[:5]]
        slot = self.slots[active_index]
        if self.emulate_unity_setactive_no_sim:
            # See activate_stationary(): make the body live before touching
            # its dynamic state, while its collision shape remains disabled.
            slot.body.set_actor_flag(self.pyphysx.ActorFlag.DISABLE_SIMULATION, False)
        if yaw is None:
            self._set_position_preserve_orientation(active_index, x, y)
        else:
            self._set_pose(active_index, x, y, yaw)
        slot.body.set_linear_velocity(self._horizontal_velocity(vx, vy, 0.0))
        if self.coordinate_mode == "unity-native-yup":
            slot.body.set_angular_velocity([0.0, w, 0.0])
        else:
            slot.body.set_angular_velocity([0.0, 0.0, w])
        slot.material.set_static_friction(0.0)
        slot.material.set_dynamic_friction(0.0)
        slot.body.enable_gravity()
        slot.shape.set_flag(self.pyphysx.ShapeFlag.SIMULATION_SHAPE, True)
        if self.repeat_pose_after_shape_activation:
            if yaw is None:
                self._set_position_preserve_orientation(active_index, x, y)
            else:
                self._set_pose(active_index, x, y, yaw)
        self._refresh_unity_setactive_interactions(slot)
        if self.set_active_scene_membership and not slot.in_scene:
            self.scene.add_actor(slot.body)
            slot.in_scene = True
        slot.body.wake_up()
        slot.enabled = True
        self._custom_sliding_index = active_index

    def start_bestshot(
        self,
        active_index: int,
        shot: Sequence[float],
        *,
        yaw: Optional[float] = None,
    ) -> None:
        if len(shot) < 3:
            raise ValueError("shot must contain velocity, horizontal offset, rotation")
        release = local_initial_state(*[float(value) for value in shot[:3]])
        self.start_motioninfo(
            active_index,
            [release.x, release.y, release.vx, release.vy, release.w],
            yaw=yaw,
        )

    def _stone_reports(self, reports: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for report in reports:
            actor0 = self._address_to_index.get(int(report.get("actor0") or 0))
            actor1 = self._address_to_index.get(int(report.get("actor1") or 0))
            if actor0 is None or actor1 is None:
                continue

            row = dict(report)
            row["stoneIndex0"] = actor0
            row["stoneIndex1"] = actor1
            result.append(row)
        return result
    @staticmethod
    def _reaches_pcm_shell_this_tick(active: dict[str, Any], targets: dict[str, dict[str, Any]]) -> bool:
        next_active_x = float(active["x"]) + float(active["vx"]) * UNITY_FIXED_TIMESTEP
        next_active_y = float(active["y"]) + float(active["vy"]) * UNITY_FIXED_TIMESTEP
        for target in targets.values():
            next_target_x = float(target["x"]) + float(target["vx"]) * UNITY_FIXED_TIMESTEP
            next_target_y = float(target["y"]) + float(target["vy"]) * UNITY_FIXED_TIMESTEP
            if math.hypot(next_active_x - next_target_x, next_active_y - next_target_y) <= FIRST_PCM_CENTER_DISTANCE:
                return True
        return False

    @staticmethod
    def _is_inside_pcm_shell(active: dict[str, Any], targets: dict[str, dict[str, Any]]) -> bool:
        """Return whether the current actor poses are already in the PCM shell.

        Target wake-up may be predictive so the next narrowphase task sees an
        awake body. Material restoration is different: doing it one physics
        tick early creates an extra stone-ice friction step before the first
        stone-stone PCM call.
        """
        for target in targets.values():
            if math.hypot(
                float(active["x"]) - float(target["x"]),
                float(active["y"]) - float(target["y"]),
            ) <= FIRST_PCM_CENTER_DISTANCE:
                return True
        return False

    def _unity_native_angular_setter_vector(
        self, slot: PhysxStoneSlot, angular_y: float
    ) -> list[float]:
        """Legacy diagnostic model of a projected angular-velocity setter.

        This was inferred from an earlier native bridge experiment. A later
        live capture of the DCP setter shows it writes the requested world
        vector directly (``[0, wy, 0]``), so production replay leaves this
        disabled. Keep it only for historical A/B reports.
        """
        _position, q_wxyz = slot.body.get_global_pose()
        f32 = self.probe.np.float32

        def rotate(q: tuple[Any, Any, Any, Any], v: tuple[Any, Any, Any]) -> tuple[Any, Any, Any]:
            x, y, z, w = q
            vx, vy, vz = (f32(f32(2.0) * component) for component in v)
            w2 = f32(f32(w * w) - f32(0.5))
            dot2 = f32(f32(f32(x * vx) + f32(y * vy)) + f32(z * vz))
            return (
                f32(f32(f32(vx * w2) + f32(f32(y * vz) - f32(z * vy)) * w) + f32(x * dot2)),
                f32(f32(f32(vy * w2) + f32(f32(z * vx) - f32(x * vz)) * w) + f32(y * dot2)),
                f32(f32(f32(vz * w2) + f32(f32(x * vy) - f32(y * vx)) * w) + f32(z * dot2)),
            )

        # pyphysx exposes the local Z quaternion component with the opposite
        # sign to Unity's native-Y-up wrapper coordinate convention.
        q = (f32(q_wxyz.x), f32(q_wxyz.y), f32(-q_wxyz.z), f32(q_wxyz.w))
        local = rotate((f32(-q[0]), f32(-q[1]), f32(-q[2]), q[3]), (f32(0.0), f32(angular_y), f32(0.0)))
        projected = rotate(q, (f32(0.0), local[1], f32(0.0)))
        return [float(component) for component in projected]

    def _unity_native_angular_setter_tilt_vector(
        self,
        slot: PhysxStoneSlot,
        angular_y: float,
    ) -> list[float]:
        """Apply the A9-observed native bridge tilt without yaw projection."""

        _position, q_wxyz = slot.body.get_global_pose()
        f32 = self.probe.np.float32
        # Same pyphysx-to-Unity Z convention as the historical wrapper.
        qx, qy, qz, qw = (
            f32(q_wxyz.x), f32(q_wxyz.y), f32(-q_wxyz.z), f32(q_wxyz.w)
        )
        half_yaw = f32(math.atan2(float(qy), float(qw)))
        s, c = f32(math.sin(float(half_yaw))), f32(math.cos(float(half_yaw)))
        # q_tilt = q * inverse(q_yaw); only its X/Z tilt is relevant.
        tx = f32(f32(qx * c) - f32(qz * s))
        tz = f32(f32(qz * c) - f32(qx * s))
        tw = f32(f32(qw * c) + f32(qy * s))
        norm = f32(math.sqrt(float(f32(f32(tx * tx) + f32(tz * tz)) + f32(tw * tw))))
        if norm > 0.0:
            tx, tz, tw = f32(tx / norm), f32(tz / norm), f32(tw / norm)
        wy = f32(angular_y)
        return [
            float(f32(f32(-2.0) * f32(tz * tw) * wy)),
            float(f32(f32(f32(tw * tw) - f32(tx * tx)) - f32(tz * tz)) * wy),
            float(f32(f32(2.0) * f32(tx * tw) * wy)),
        ]


    def _set_stone_stone_contact_friction(self, static_friction: float, dynamic_friction: float) -> None:
        if self._has_stone_stone_contact_friction_override:
            self.scene.set_stone_stone_contact_friction_override(
                self.enable_stone_stone_contact_friction_override,
                float(static_friction),
                float(dynamic_friction),
            )

    def _training_motion_state(self, index: int) -> tuple[float, float, float, float, float, float]:
        """Read only the six protocol values needed by the training hot loop.

        The audit path deliberately materialises complete pose/quaternion and
        per-target dictionaries before and after every fixed tick.  That is
        essential when comparing a tick with Unity, but it is unnecessary once
        a validated simulator is rolling out a settled game state for training.
        This helper keeps the same native reads used by :meth:`state`, without
        constructing its diagnostic payload.
        """

        body = self.slots[index].body
        position, _quaternion = body.get_global_pose()
        linear = body.get_linear_velocity()
        angular = body.get_angular_velocity()
        if self.coordinate_mode == "unity-native-yup":
            return (
                float(UNITY_NATIVE_ORIGIN_Z - position[2]),
                float(UNITY_NATIVE_POSITION_X_BASE - position[0]),
                float(-linear[2]),
                float(-linear[0]),
                float(linear[1]),
                float(angular[1]),
            )
        x, y = self.probe._from_physx_xy(float(position[0]), float(position[1]), True)
        vx, vy = self.probe._from_physx_xy(float(linear[0]), float(linear[1]), True)
        return float(x), float(y), float(vx), float(vy), float(linear[2]), float(angular[2])

    def _run_to_first_contact_training(
        self,
        active_index: int,
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        max_steps: int = 5000,
        motion_stepper: Any | None = None,
    ) -> dict[str, Any]:
        """Lean first-contact replay for *settled* self-play positions.

        It advances exactly the same custom sliding setter and PhysX scene as
        the forensic path, but omits the per-tick JSON-like audit snapshots.
        This is valid only while all targets are stationary at shot start; a
        non-settled caller transparently falls back to the audit implementation.
        """

        targets = {
            slot.index
            for slot in self.slots
            if slot.enabled and slot.index != active_index
        }
        if target_indices is not None:
            targets &= {int(index) for index in target_indices}
        if not targets:
            raise ValueError("no enabled target stones are available")

        # A legal curling turn begins after every stone settles.  Record the
        # fixed target coordinates once instead of crossing the Python/native
        # boundary for every target both before and after every tick.
        static_targets: list[tuple[int, float, float]] = []
        for index in sorted(targets):
            x, y, vx, vy, _vz, w = self._training_motion_state(index)
            if math.hypot(vx, vy) > 0.01 or abs(w) > 0.01:
                return self._run_to_first_contact(
                    active_index,
                    friction_noises,
                    target_indices=sorted(targets),
                    max_steps=max_steps,
                    motion_stepper=motion_stepper,
                )
            static_targets.append((index, x, y))

        # The bundled native extension can run this settled-target loop
        # without constructing Python state/contact dictionaries per tick.
        # It still executes every 0.01 s PhysX step and the exact recovered
        # f64 friction update.  Keep unusual diagnostic angular modes and
        # custom motion steppers on the transparent Python path below.
        native_front_half = getattr(self.scene, "simulate_curling_until_first_contact", None)
        native_angular_mode_supported = (
            not self.emulate_unity_native_angular_setter_rotation
            and not self.emulate_unity_native_angular_setter_residual_z
        )
        native_pair_override = bool(
            self._has_stone_stone_contact_friction_override
            and self.enable_stone_stone_contact_friction_override
        )
        if (
            native_front_half is not None
            and isinstance(motion_stepper, NativePyphysxMotionStepper)
            and self.coordinate_mode == "unity-native-yup"
            and native_angular_mode_supported
        ):
            noises = [float(noise) for noise in friction_noises]
            reached_first_contact, steps_used = native_front_half(
                self.slots[active_index].body,
                [self.slots[index].body for index, _x, _y in static_targets],
                noises,
                self.dt,
                UNITY_FIXED_TIMESTEP,
                UNITY_NATIVE_ORIGIN_Z,
                UNITY_NATIVE_POSITION_X_BASE,
                FIRST_PCM_CENTER_DISTANCE,
                max_steps,
                self.custom_sliding_zero_vertical_setter,
                self.emulate_unity_native_angular_setter_tilt_only,
                self.wake_target_at_current_pcm_shell,
                self.emulate_unity_first_pair_zero_friction and native_pair_override,
                self.stone_stone_contact_static_friction,
                self.stone_stone_contact_dynamic_friction,
            )
            if reached_first_contact:
                slot = self.slots[active_index]
                slot.material.set_static_friction(0.6)
                slot.material.set_dynamic_friction(0.6)
                self._custom_sliding_index = None
                return {
                    "reachedFirstContact": True,
                    "steps": int(steps_used),
                    # The training caller only consumes the contact boolean.
                    # Forensic target identity remains on the audit path.
                    "targetIndices": [],
                    "trainingFastPath": True,
                    "nativeLoop": True,
                }
            return {
                "reachedFirstContact": False,
                "steps": int(steps_used),
                "trainingFastPath": True,
                "nativeLoop": True,
            }

        steps_used = 0
        for step_index, noise in enumerate(friction_noises, 1):
            if step_index > max_steps:
                break
            steps_used = step_index
            x, y, vx, vy, vz, angular = self._training_motion_state(active_index)
            friction = unity_friction(False, noise=float(noise))
            if motion_stepper is None:
                speed = newfrictionstep(friction, B2Vec2(vx, vy), angular, STEP)
                motion_vx, motion_vy, motion_angle = speed.v.x, speed.v.y, speed.angle
            else:
                motion_vx, motion_vy, motion_angle = motion_stepper.step(
                    friction=friction, vx=vx, vy=vy, angle=angular
                )
            slot = self.slots[active_index]
            slot.body.set_linear_velocity(
                self._horizontal_velocity(
                    motion_vx,
                    motion_vy,
                    0.0 if self.custom_sliding_zero_vertical_setter else vz,
                )
            )
            if self.coordinate_mode == "unity-native-yup":
                if self.emulate_unity_native_angular_setter_rotation:
                    angular_setter = self._unity_native_angular_setter_vector(slot, motion_angle)
                elif self.emulate_unity_native_angular_setter_tilt_only:
                    angular_setter = self._unity_native_angular_setter_tilt_vector(slot, motion_angle)
                elif self.emulate_unity_native_angular_setter_residual_z:
                    # This diagnostic branch needs the native residual, so it
                    # retains its one extra getter just as the audit path does.
                    current_native_w = slot.body.get_angular_velocity()
                    z = float(current_native_w[2])
                    if abs(z) <= 1e-12:
                        z = float(self._unity_native_angular_setter_vector(slot, motion_angle)[2])
                    angular_setter = [0.0, motion_angle, z]
                else:
                    angular_setter = [0.0, motion_angle, 0.0]
                slot.body.set_angular_velocity(angular_setter)
            else:
                slot.body.set_angular_velocity([0.0, 0.0, motion_angle])

            inside_pcm_shell = any(
                math.hypot(x - target_x, y - target_y) <= FIRST_PCM_CENTER_DISTANCE
                for _index, target_x, target_y in static_targets
            )
            reaches_pcm_shell = any(
                math.hypot(
                    x + motion_vx * UNITY_FIXED_TIMESTEP - target_x,
                    y + motion_vy * UNITY_FIXED_TIMESTEP - target_y,
                ) <= FIRST_PCM_CENTER_DISTANCE
                for _index, target_x, target_y in static_targets
            )
            if self.wake_target_at_current_pcm_shell:
                reaches_pcm_shell = inside_pcm_shell
            if reaches_pcm_shell:
                for target_index, _target_x, _target_y in static_targets:
                    self.slots[target_index].body.wake_up()
            pair_zero_friction = self._first_pair_zero_friction_for_step(inside_pcm_shell)
            if pair_zero_friction:
                self._set_stone_stone_contact_friction(0.0, 0.0)
            try:
                self.scene.simulate(self.dt)
            finally:
                if pair_zero_friction:
                    self._set_stone_stone_contact_friction(
                        self.stone_stone_contact_static_friction,
                        self.stone_stone_contact_dynamic_friction,
                    )
            hit_targets: set[int] = set()
            for report in self._stone_reports(self.scene.get_contact_reports()):
                pair = {int(report["stoneIndex0"]), int(report["stoneIndex1"])}
                if active_index not in pair or int(report.get("contact_count") or 0) <= 0:
                    continue
                target = next((index for index in pair if index != active_index), None)
                if target in targets:
                    hit_targets.add(int(target))
            if hit_targets:
                slot.material.set_static_friction(0.6)
                slot.material.set_dynamic_friction(0.6)
                self._custom_sliding_index = None
                return {
                    "reachedFirstContact": True,
                    "steps": step_index,
                    "targetIndices": sorted(hit_targets),
                    "trainingFastPath": True,
                }
        return {"reachedFirstContact": False, "steps": steps_used, "trainingFastPath": True}

    def run_bestshot_to_first_contact_training(
        self,
        active_index: int,
        shot: Sequence[float],
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        yaw: Optional[float] = None,
        max_steps: int = 5000,
        motion_stepper: Any | None = None,
    ) -> dict[str, Any]:
        """Run the no-audit training hot path from a BESTSHOT command."""

        self.start_bestshot(active_index, shot, yaw=yaw)
        return self._run_to_first_contact_training(
            active_index,
            friction_noises,
            target_indices=target_indices,
            max_steps=max_steps,
            motion_stepper=motion_stepper,
        )

    def _first_pair_zero_friction_for_step(self, inside_pcm_shell: bool) -> bool:
        """Return whether this Scene step needs Unity's zero-friction handoff.

        C04 shows the stone pair has zero static/dynamic friction in the first
        dynamic solver frame.  The next physics step must return to the normal
        0.36/0.36 pair override, so this is deliberately scoped to one
        ``Scene.simulate`` call rather than a material-state change.
        """
        return bool(self.emulate_unity_first_pair_zero_friction and inside_pcm_shell)

    def step_custom_sliding(
        self,
        active_index: int,
        friction_noise: float,
        *,
        motion_override: Optional[Sequence[float]] = None,
        motion_stepper: Any | None = None,
    ) -> dict[str, Any]:
        if self._custom_sliding_index != active_index:
            raise RuntimeError(f"stone {active_index} is not in custom sliding mode")
        slot = self.slots[active_index]
        current = self.state(active_index)
        if motion_override is None:
            friction = unity_friction(False, noise=float(friction_noise))
            if motion_stepper is None:
                speed = newfrictionstep(
                    friction,
                    B2Vec2(float(current["vx"]), float(current["vy"])),
                    float(current["w"]),
                    STEP,
                )
                motion_vx, motion_vy, motion_angle = speed.v.x, speed.v.y, speed.angle
            else:
                motion_vx, motion_vy, motion_angle = motion_stepper.step(
                    friction=friction,
                    vx=float(current["vx"]),
                    vy=float(current["vy"]),
                    angle=float(current["w"]),
                )
        else:
            if len(motion_override) != 3:
                raise ValueError("motion_override must contain protocol vx, vy, angle")
            motion_vx, motion_vy, motion_angle = (float(value) for value in motion_override)
        slot.body.set_linear_velocity(
            self._horizontal_velocity(
                motion_vx,
                motion_vy,
                0.0 if self.custom_sliding_zero_vertical_setter else float(current["vz"]),
            )
        )
        if self.coordinate_mode == "unity-native-yup":
            # C122 directly captures Unity writing a pure world-Y vector.
            # Re-projecting it through the current quaternion drains spin too
            # quickly after yaw accumulates and creates a false high-curl
            # branch.
            if self.emulate_unity_native_angular_setter_rotation:
                angular_setter = self._unity_native_angular_setter_vector(slot, motion_angle)
            elif self.emulate_unity_native_angular_setter_tilt_only:
                angular_setter = self._unity_native_angular_setter_tilt_vector(slot, motion_angle)
            elif self.emulate_unity_native_angular_setter_residual_z:
                # A9 shows the native bridge retains a minute Z residual even
                # though DCP supplies [0, wy, 0].  Seed it from the same
                # native transform on the first update, then preserve the
                # bridge's own residual rather than applying the old full
                # quaternion projection every tick.
                current_native_w = current["physxAngularVelocity"]
                z = float(current_native_w[2])
                if abs(z) <= 1e-12:
                    z = float(self._unity_native_angular_setter_vector(slot, motion_angle)[2])
                angular_setter = [0.0, motion_angle, z]
            else:
                angular_setter = [0.0, motion_angle, 0.0]
            slot.body.set_angular_velocity(angular_setter)
        else:
            slot.body.set_angular_velocity([0.0, 0.0, motion_angle])
        before_scene = self.state(active_index)
        targets_before_scene = {
            str(other.index): self.state(other.index)
            for other in self.slots
            if other.enabled and other.index != active_index
        }
        inside_pcm_shell = self._is_inside_pcm_shell(before_scene, targets_before_scene)
        wakes_targets_for_pcm = (
            inside_pcm_shell
            if self.wake_target_at_current_pcm_shell
            else self._reaches_pcm_shell_this_tick(before_scene, targets_before_scene)
        )
        if wakes_targets_for_pcm:
            for target_index in targets_before_scene:
                self.slots[int(target_index)].body.wake_up()
        # Unity keeps the sliding stone's ice material at zero for the Scene
        # step that first produces the dynamic-dynamic pair.  Restoring 0.6
        # merely because the pre-sim pose is inside the PCM shell makes the
        # stone-ice solver apply one premature angular-friction impulse.  The
        # matching-contact branch in _run_to_first_contact restores it after
        # this step, ready for subsequent collision steps.
        pair_zero_friction = self._first_pair_zero_friction_for_step(inside_pcm_shell)
        if pair_zero_friction:
            self._set_stone_stone_contact_friction(0.0, 0.0)
        try:
            self.scene.simulate(self.dt)
        finally:
            if pair_zero_friction:
                self._set_stone_stone_contact_friction(
                    self.stone_stone_contact_static_friction,
                    self.stone_stone_contact_dynamic_friction,
                )
        reports = self._stone_reports(self.scene.get_contact_reports())

        after_scene = self.state(active_index)
        targets_after_scene = {
            str(other.index): self.state(other.index)
            for other in self.slots
            if other.enabled and other.index != active_index
        }
        return {
            "frictionNoise": float(friction_noise),
            "friction": unity_friction(False, noise=float(friction_noise)),
            "beforeScene": before_scene,
            "targetsBeforeScene": targets_before_scene,
            "afterScene": after_scene,
            "targetsAfterScene": targets_after_scene,
            "stoneReports": reports,
            "wakesTargetsForPcm": wakes_targets_for_pcm,
            "insidePcmShell": inside_pcm_shell,
            "restoresActiveFriction": False,
            "pairZeroFrictionForStep": pair_zero_friction,
        }

    def _run_to_first_contact(
        self,
        active_index: int,
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        max_steps: int = 5000,
        max_physics_only_tail_steps: int = 1,
        motion_overrides: Optional[Sequence[Sequence[float]]] = None,
        motion_stepper: Any | None = None,
    ) -> dict[str, Any]:
        targets = {
            slot.index
            for slot in self.slots
            if slot.enabled and slot.index != active_index
        }
        if target_indices is not None:
            targets &= {int(index) for index in target_indices}
        if not targets:
            raise ValueError("no enabled target stones are available")

        last: Optional[dict[str, Any]] = None
        steps_used = 0
        if motion_overrides is not None and len(motion_overrides) < len(friction_noises):
            raise ValueError("motion_overrides must cover every supplied friction update")
        for step_index, noise in enumerate(friction_noises, 1):
            if step_index > max_steps:
                break
            steps_used = step_index
            override = motion_overrides[step_index - 1] if motion_overrides is not None else None
            step = self.step_custom_sliding(
                active_index,
                float(noise),
                motion_override=override,
                motion_stepper=motion_stepper,
            )
            matching_reports = []
            hit_targets: set[int] = set()
            for report in step["stoneReports"]:
                pair = {int(report["stoneIndex0"]), int(report["stoneIndex1"])}
                if active_index not in pair:
                    continue
                target = next((index for index in pair if index != active_index), None)
                if target not in targets or int(report.get("contact_count") or 0) <= 0:
                    continue
                matching_reports.append(report)
                hit_targets.add(int(target))
            if matching_reports:
                slot = self.slots[active_index]
                slot.material.set_static_friction(0.6)
                slot.material.set_dynamic_friction(0.6)
                self._custom_sliding_index = None
                step.update(
                    {
                        "reachedFirstContact": True,
                        "steps": step_index,
                        "targetIndices": sorted(hit_targets),
                        "firstContactReports": matching_reports,
                        "targetBeforeScene": {
                            str(index): step["targetsBeforeScene"][str(index)]
                            for index in sorted(hit_targets)
                        },
                    }
                )
                return step
            last = step

        # A capture can end its DCP setter trace before the following fixed
        # physics steps reach PCM.  Do not manufacture another friction update:
        # only advance ordinary Scene steps.  The default remains one step for
        # historical captures; A2-backed callers may supply a larger bounded
        # tail once the real setter sequence is known.
        if max_physics_only_tail_steps < 0:
            raise ValueError("max_physics_only_tail_steps must be non-negative")
        if last is not None:
            for tail_step in range(1, max_physics_only_tail_steps + 1):
                before_scene = self.state(active_index)
                targets_before_scene = {
                    str(other.index): self.state(other.index)
                    for other in self.slots
                    if other.enabled and other.index != active_index
                }
                pair_zero_friction = self._first_pair_zero_friction_for_step(
                    self._is_inside_pcm_shell(before_scene, targets_before_scene)
                )
                if pair_zero_friction:
                    self._set_stone_stone_contact_friction(0.0, 0.0)
                try:
                    self.scene.simulate(self.dt)
                finally:
                    if pair_zero_friction:
                        self._set_stone_stone_contact_friction(
                            self.stone_stone_contact_static_friction,
                            self.stone_stone_contact_dynamic_friction,
                        )
                reports = self._stone_reports(self.scene.get_contact_reports())
                after_scene = self.state(active_index)
                targets_after_scene = {
                    str(other.index): self.state(other.index)
                    for other in self.slots
                    if other.enabled and other.index != active_index
                }
                matching_reports = []
                hit_targets: set[int] = set()
                for report in reports:
                    pair = {int(report["stoneIndex0"]), int(report["stoneIndex1"])}
                    if active_index not in pair:
                        continue
                    target = next((index for index in pair if index != active_index), None)
                    if target not in targets or int(report.get("contact_count") or 0) <= 0:
                        continue
                    matching_reports.append(report)
                    hit_targets.add(int(target))
                if matching_reports:
                    slot = self.slots[active_index]
                    slot.material.set_static_friction(0.6)
                    slot.material.set_dynamic_friction(0.6)
                    self._custom_sliding_index = None
                    return {
                        "physicsOnlyTrailingStep": True,
                        "physicsOnlyTrailingSteps": tail_step,
                        "frictionNoise": None,
                        "friction": None,
                        "beforeScene": before_scene,
                        "targetsBeforeScene": targets_before_scene,
                        "afterScene": after_scene,
                        "targetsAfterScene": targets_after_scene,
                        "stoneReports": reports,
                        "wakesTargetsForPcm": False,
                        "pairZeroFrictionForStep": pair_zero_friction,
                        "reachedFirstContact": True,
                        "steps": steps_used,
                        "targetIndices": sorted(hit_targets),
                        "firstContactReports": matching_reports,
                        "targetBeforeScene": {
                            str(index): targets_before_scene[str(index)]
                            for index in sorted(hit_targets)
                        },
                    }

        return {
            "reachedFirstContact": False,
            "steps": steps_used,
            "lastStep": last,
        }

    def run_motioninfo_to_first_contact(
        self,
        active_index: int,
        motioninfo: Sequence[float],
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        yaw: Optional[float] = None,
        max_steps: int = 5000,
        max_physics_only_tail_steps: int = 1,
        motion_overrides: Optional[Sequence[Sequence[float]]] = None,
        motion_stepper: Any | None = None,
    ) -> dict[str, Any]:
        self.start_motioninfo(active_index, motioninfo, yaw=yaw)
        return self._run_to_first_contact(
            active_index,
            friction_noises,
            target_indices=target_indices,
            max_steps=max_steps,
            max_physics_only_tail_steps=max_physics_only_tail_steps,
            motion_overrides=motion_overrides,
            motion_stepper=motion_stepper,
        )

    def run_bestshot_to_first_contact(
        self,
        active_index: int,
        shot: Sequence[float],
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        yaw: Optional[float] = None,
        max_steps: int = 5000,
        max_physics_only_tail_steps: int = 1,
        motion_overrides: Optional[Sequence[Sequence[float]]] = None,
        motion_stepper: Any | None = None,
    ) -> dict[str, Any]:
        self.start_bestshot(active_index, shot, yaw=yaw)
        return self._run_to_first_contact(
            active_index,
            friction_noises,
            target_indices=target_indices,
            max_steps=max_steps,
            max_physics_only_tail_steps=max_physics_only_tail_steps,
            motion_overrides=motion_overrides,
            motion_stepper=motion_stepper,
        )

    def _run_to_pcm_shell(
        self,
        active_index: int,
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        threshold: float = FIRST_PCM_CENTER_DISTANCE,
        max_steps: int = 5000,
    ) -> dict[str, Any]:
        targets = {
            slot.index
            for slot in self.slots
            if slot.enabled and slot.index != active_index
        }
        if target_indices is not None:
            targets &= {int(index) for index in target_indices}
        if not targets:
            raise ValueError("no enabled target stones are available")

        last: Optional[dict[str, Any]] = None
        steps_used = 0
        for step_index, noise in enumerate(friction_noises, 1):
            if step_index > max_steps:
                break
            steps_used = step_index
            step = self.step_custom_sliding(active_index, float(noise))
            active = step["afterScene"]
            distances = {
                str(index): math.hypot(
                    float(active["x"]) - float(step["targetsAfterScene"][str(index)]["x"]),
                    float(active["y"]) - float(step["targetsAfterScene"][str(index)]["y"]),
                )
                for index in sorted(targets)
            }
            hit_targets = [index for index in sorted(targets) if distances[str(index)] <= threshold]
            if hit_targets:
                step.update(
                    {
                        "reachedPcmShell": True,
                        "steps": step_index,
                        "threshold": float(threshold),
                        "targetDistances": distances,
                        "targetIndices": hit_targets,
                        "entranceState": active,
                        "targetEntranceStates": {
                            str(index): step["targetsAfterScene"][str(index)]
                            for index in hit_targets
                        },
                    }
                )
                return step
            last = step

        return {
            "reachedPcmShell": False,
            "steps": steps_used,
            "threshold": float(threshold),
            "lastStep": last,
        }

    def run_motioninfo_to_pcm_shell(
        self,
        active_index: int,
        motioninfo: Sequence[float],
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        yaw: Optional[float] = None,
        threshold: float = FIRST_PCM_CENTER_DISTANCE,
        max_steps: int = 5000,
    ) -> dict[str, Any]:
        self.start_motioninfo(active_index, motioninfo, yaw=yaw)
        return self._run_to_pcm_shell(
            active_index,
            friction_noises,
            target_indices=target_indices,
            threshold=threshold,
            max_steps=max_steps,
        )

    def run_bestshot_to_pcm_shell(
        self,
        active_index: int,
        shot: Sequence[float],
        friction_noises: Iterable[float],
        *,
        target_indices: Optional[Sequence[int]] = None,
        yaw: Optional[float] = None,
        threshold: float = FIRST_PCM_CENTER_DISTANCE,
        max_steps: int = 5000,
    ) -> dict[str, Any]:
        self.start_bestshot(active_index, shot, yaw=yaw)
        return self._run_to_pcm_shell(
            active_index,
            friction_noises,
            target_indices=target_indices,
            threshold=threshold,
            max_steps=max_steps,
        )

    def snapshot(self) -> list[dict[str, Any]]:
        return [self.state(index) for index in range(len(self.slots))]
