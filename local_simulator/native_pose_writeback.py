"""Expose the verified PhysX pose setter's missing ``autowake=False`` argument.

The bundled Python binding always supplies True. Unity f73070 -> f72606
supplies False after physics, even when the quaternion bits are unchanged.
Calling the actual virtual method preserves its normalization, contact-cache
invalidation and sleep behavior; no cache fields are patched here.
"""
from __future__ import annotations

import ctypes
from functools import lru_cache
import hashlib
import platform

from .runtime_loader import _resolve_bundled_extension


class _PxTransform(ctypes.Structure):
    _fields_ = [(name, ctypes.c_float) for name in ('qx', 'qy', 'qz', 'qw', 'px', 'py', 'pz')]


@lru_cache(maxsize=1)
def _verified_setter():
    extension = _resolve_bundled_extension()
    # The CP38/CP313 instruction streams and referenced arithmetic constants
    # are identical to CP39 after resolving address relocations (ABI report
    # analysis_input/native_pose_setter_abi_comparison_20261002.json).
    kernels = {
        '2564abec4fa3f358e67259b105c4b88d49eae28510611c8a0e2f11b7671888df': 0x1acb60,
        '7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38': 0x1acb60,
        '2a2dbc19f42388239bc27c47ff90d1aef4ae4554f762afad09d13a209ae5b6f0': 0x1a3870,
        '44729fb97df143374a6c01d1a6bae59f11dd302ff8035d0432ec9a7c04c168f5': 0x1aae40,
    }
    setter_rva = kernels.get(hashlib.sha256(extension.read_bytes()).hexdigest())
    if (platform.system() != 'Windows' or ctypes.sizeof(ctypes.c_void_p) != 8
            or setter_rva is None):
        raise RuntimeError('Unity pose writeback requires a verified Windows PhysX kernel or an explicit no-autowake binding')
    kernel = ctypes.windll.kernel32
    kernel.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
    kernel.GetModuleHandleW.restype = ctypes.c_void_p
    base = kernel.GetModuleHandleW(str(extension))
    if not base:
        raise RuntimeError('Verified PhysX kernel is not loaded')
    address = base + setter_rva
    signature = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(_PxTransform), ctypes.c_bool)
    return address, signature(address)


def writeback_pose_without_autowake(body, pose):
    """Write raw PxTransform through the verified setter, normalizing once."""
    explicit = getattr(body, 'set_global_pose_without_autowake', None)
    if explicit is not None:
        explicit(pose)
        return
    address, setter = _verified_setter()
    actor = body.get_physx_address()
    vtable = ctypes.c_void_p.from_address(actor).value
    # Live RigidDynamic vtable slot 19 is the traced setGlobalPose entry.
    if ctypes.c_void_p.from_address(vtable + 19 * 8).value != address:
        raise RuntimeError('Unexpected PhysX RigidDynamic pose-setter vtable')
    position, q = pose
    transform = _PxTransform(q.x, q.y, q.z, q.w, *position)
    setter(actor, ctypes.byref(transform), False)
