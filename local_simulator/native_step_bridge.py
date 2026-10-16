"""Optional fused setters and pose writebacks through the existing PhysX ABI.

Only the inspected CP39 kernel is enabled. Unsupported ABIs keep the ordinary
binding path. The driver still owns clock boundaries and collision callbacks.
"""
from __future__ import annotations

import ctypes
from functools import lru_cache
import hashlib
import math
import platform

from .runtime_loader import RUNTIME_ROOT, _resolve_bundled_extension
from tools.reverse.front_half_pcm_replay import FIRST_PCM_CENTER_DISTANCE

DLL_SHA256 = 'cca55bdd5e5c19e20d3ababaaf72b7d5edb8ce88498931f377593ce1ef7126b3'
KERNEL_SHA256 = '7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'
MOTION_RVA = 0x29180
METHOD_RVAS = {18: 0x1affb0, 19: 0x1acb60, 38: 0x1b02f0,
               39: 0x1ae060, 40: 0x1afb80, 41: 0x1ae0e0, 63: 0x1ae520}


class _Context(ctypes.Structure):
    _fields_ = [('motion', ctypes.c_void_p), ('actors', ctypes.c_void_p*16),
                ('positions', ctypes.c_double*32), ('scene', ctypes.c_void_p),
                ('simulate', ctypes.c_void_p)]


@lru_cache(maxsize=1)
def load_step_bridge():
    path = RUNTIME_ROOT/'unity_step_bridge.dll'
    if platform.system() != 'Windows' or ctypes.sizeof(ctypes.c_void_p) != 8 or not path.is_file():
        return None
    extension = _resolve_bundled_extension()
    if hashlib.sha256(extension.read_bytes()).hexdigest() != KERNEL_SHA256:
        return None
    if hashlib.sha256(path.read_bytes()).hexdigest() != DLL_SHA256:
        raise RuntimeError('Unity step bridge DLL hash mismatch')
    kernel = ctypes.windll.kernel32
    kernel.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
    kernel.GetModuleHandleW.restype = ctypes.c_void_p
    base = kernel.GetModuleHandleW(str(extension))
    if not base:
        raise RuntimeError('Verified PhysX kernel is not loaded')
    library = ctypes.CDLL(str(path))
    library.unity_bridge_prepare.argtypes = [ctypes.POINTER(_Context), ctypes.c_int,
        ctypes.c_uint32, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_uint32)]
    library.unity_bridge_prepare.restype = None
    library.unity_bridge_writeback.argtypes = [ctypes.POINTER(_Context), ctypes.c_uint32]
    library.unity_bridge_writeback.restype = None
    # The existing simulate binding runs while holding the Python GIL. Keep
    # that invocation behavior for the combined entry as well; a CDLL call
    # would add a release/acquire around every physics tick.
    python_library = ctypes.PyDLL(str(path))
    simulate = python_library.unity_bridge_simulate_writeback
    simulate.argtypes = [ctypes.POINTER(_Context), ctypes.c_float, ctypes.c_uint32]
    simulate.restype = ctypes.c_int
    library.unity_bridge_simulate_writeback = simulate
    library._python_library = python_library
    return library, base


class NativeStepBridge:
    def __init__(self, scene, motion_stepper, library, base):
        self.scene = scene
        self.motion_stepper = motion_stepper
        # Keep the bodies alive; activation invalidates this bridge before any
        # body is replaced. Every new driver binds the current actor pool.
        self.bodies = [slot.body for slot in scene.slots]
        actors = [body.get_physx_address() for body in self.bodies]
        for actor in actors:
            vtable = ctypes.c_void_p.from_address(actor).value
            for slot, rva in METHOD_RVAS.items():
                if ctypes.c_void_p.from_address(vtable+slot*8).value != base+rva:
                    raise RuntimeError('Unexpected PhysX RigidDynamic bridge vtable')
        self.context = _Context(base+MOTION_RVA, (ctypes.c_void_p*16)(*actors))
        self.pointer = ctypes.byref(self.context)
        self.prepare_function = library.unity_bridge_prepare
        self.writeback_function = library.unity_bridge_writeback
        self.library = library
        self.merged = scene._merge_step_work
        self.prepared_mask = 0
        self.scene_object = scene.scene
        self.native_scene = False
        from .unity_physx import PersistentPhysxFrontHalfScene
        standard_reports = (getattr(scene._stone_reports, '__func__', None)
            is PersistentPhysxFrontHalfScene._stone_reports
            and getattr(scene._wall_reports, '__func__', None)
            is PersistentPhysxFrontHalfScene._wall_reports)
        if (self.merged and scene._merge_native_scene_work and standard_reports
                and type(self.scene_object) is scene.pyphysx.Scene):
            # Use the binary's actual pybind value-holder helper. No guessed
            # CPython object layout; only the verified exact registered type.
            holder = (ctypes.c_void_p*4)()
            resolve = ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.py_object,
                ctypes.c_void_p, ctypes.c_void_p)(base+0x8210)
            if (resolve(self.scene_object, holder, None) != ctypes.addressof(holder)
                    or holder[0] != id(self.scene_object) or holder[1] is not None):
                raise RuntimeError('Unexpected native Scene holder')
            pointer = ctypes.c_void_p.from_address(holder[3]).value
            if not pointer or ctypes.c_double.from_address(pointer+0x28).value != self.scene_object.simulation_time:
                raise RuntimeError('Unexpected native Scene time')
            self.context.scene = pointer
            self.context.simulate = base+0x277e0
            self.simulate_function = library.unity_bridge_simulate_writeback
            self.native_scene = True

    def enabled_mask(self):
        return sum(1 << slot.index for slot in self.scene.slots if slot.enabled)

    def prepare(self, index, noise, random_state=None):
        if not 0 <= index < 16:
            raise IndexError('Native actor index is outside the verified pool')
        calls = self.scene._unity_angular_setter_calls
        count = calls.get(index, 0)
        mask = self.enabled_mask()
        self.prepare_function(self.pointer, index, mask, count >= 2, noise, random_state)
        calls[index] = count+1
        self.prepared_mask = mask
        if self.merged:
            targets = mask & ~(1 << index)
            if not targets:
                return False
            positions = self.context.positions
            x, y = positions[index*2], positions[index*2+1]
            # Visit the same enabled targets in ascending slot order. The
            # distance arithmetic remains the original Python math.hypot.
            while targets:
                bit = targets & -targets
                k = bit.bit_length()-1
                if math.hypot(x-positions[k*2], y-positions[k*2+1]) <= FIRST_PCM_CENTER_DISTANCE:
                    return True
                targets ^= bit
            return False
        positions = self.context.positions
        x, y = positions[index*2], positions[index*2+1]
        from tools.reverse.front_half_pcm_replay import FIRST_PCM_CENTER_DISTANCE as reference_distance
        # Retain CPython's exact hypot calculation and <= comparison, rather
        # than substituting a different CRT or squared-distance expression.
        return any(math.hypot(x-positions[k*2], y-positions[k*2+1]) <= reference_distance
                   for k in range(16) if k != index and mask & (1 << k))

    def writeback(self, enabled_mask=None):
        if enabled_mask is None:
            enabled_mask = self.enabled_mask()
        self.writeback_function(self.pointer, enabled_mask)

    def simulate_writeback(self, dt, enabled_mask=None):
        if enabled_mask is None:
            enabled_mask = self.enabled_mask()
        return bool(self.simulate_function(self.pointer, dt, enabled_mask))


def create_step_bridge(scene, motion_stepper):
    from .unity_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene
    if (not isinstance(scene, PersistentPhysxFrontHalfScene)
            or type(motion_stepper) is not NativePyphysxMotionStepper
            or len(scene.slots) != 16 or scene.coordinate_mode != 'unity-native-yup'
            or not scene.custom_sliding_zero_vertical_setter
            or not scene.emulate_unity_native_angular_setter_rotation
            or scene._native_angular_projection is None
            or scene.wake_target_at_current_pcm_shell):
        return None
    loaded = load_step_bridge()
    active = scene._custom_sliding_index
    if active is None or not 0 <= active < 16:
        return None
    return NativeStepBridge(scene, motion_stepper, *loaded) if loaded is not None else None
