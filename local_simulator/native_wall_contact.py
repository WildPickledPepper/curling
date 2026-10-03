"""Enable actual PhysX contact reports for the scene's static Wall shapes.

The bundled filter reports only dynamic/dynamic pairs. A hash-checked relay
adds notification flags for a tagged Wall filter-data word and then resumes
the original filter. Solver and contact-modification flags are unchanged.
"""
from __future__ import annotations

import ctypes
import hashlib
import platform
import struct
import threading

from .runtime_loader import _resolve_bundled_extension

_KERNELS = {
    # filter site, RigidStatic::getShapes, NpShape::setSimulationFilterData
    '7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38': (0x25d23, 0x1b0520, 0x1aafd0),
    '2a2dbc19f42388239bc27c47ff90d1aef4ae4554f762afad09d13a209ae5b6f0': (0x25073, 0x1a7230, 0x1a1ce0),
    '44729fb97df143374a6c01d1a6bae59f11dd302ff8035d0432ec9a7c04c168f5': (0x25d43, 0x1ae800, 0x1a92b0),
}
_WALL_MARKER = 0x57414c4c
_ORIGINAL = bytes.fromhex('80e30f80fb01752a4080e50f403aeb7521b81c020000660906')
_LOCK = threading.Lock()
_INSTALLED = None
_KEEPALIVE = None


def install_wall_contact_notifications():
    """Extend the verified reporting filter without changing collision response."""
    global _INSTALLED, _KEEPALIVE
    with _LOCK:
        if _INSTALLED is not None:
            return dict(_INSTALLED)
        extension = _resolve_bundled_extension()
        digest = hashlib.sha256(extension.read_bytes()).hexdigest()
        sites = _KERNELS.get(digest)
        if platform.system() != 'Windows' or ctypes.sizeof(ctypes.c_void_p) != 8 or sites is None:
            raise RuntimeError('Wall contact reporting requires a verified Windows x64 PhysX kernel')
        k = ctypes.WinDLL('kernel32', use_last_error=True)
        k.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
        k.GetModuleHandleW.restype = ctypes.c_void_p
        k.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
        k.VirtualAlloc.restype = ctypes.c_void_p
        k.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong]
        k.VirtualFree.restype = ctypes.c_int
        k.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
        k.VirtualProtect.restype = ctypes.c_int
        k.GetCurrentProcess.restype = ctypes.c_void_p
        k.FlushInstructionCache.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
        k.FlushInstructionCache.restype = ctypes.c_int
        base = k.GetModuleHandleW(str(extension))
        site = base + sites[0] if base else 0
        if not base or ctypes.string_at(site, len(_ORIGINAL)) != _ORIGINAL:
            raise RuntimeError('Unexpected PhysX contact-filter instruction bytes')
        relay = None
        aligned = base & ~0xffff
        for distance in range(0x1000000, 0x70000000, 0x10000):
            for hint in (aligned + distance, aligned - distance):
                if hint > 0 and -2**31 <= hint-(site+5) < 2**31:
                    relay = k.VirtualAlloc(hint, 4096, 0x3000, 0x04)
                    if relay:
                        break
            if relay:
                break
        if not relay:
            raise RuntimeError('Cannot allocate the static Wall notification relay')
        # Original shader saved FilterData0 at rsp+0x50 and FilterData1 at
        # rsp+0x40. Only word3 is marked; words0/1/2 and original filtering
        # are retained. All branches below preserve the original stack.
        code = bytearray()
        code += b'\x81\x7c\x24\x5c' + struct.pack('<I', _WALL_MARKER)
        code += b'\x74\x0a'  # matching first shape -> notification write
        code += b'\x81\x7c\x24\x4c' + struct.pack('<I', _WALL_MARKER)
        code += b'\x75\x05'  # neither shape -> original dynamic-pair test
        code += b'\x66\x81\x0e\x1c\x02'  # FOUND/PERSISTS/LOST/CONTACT_POINTS
        code += _ORIGINAL[:6]  # and bl,15; cmp bl,1
        code += b'\x0f\x85' + struct.pack('<i', (site+0x32)-(relay+len(code)+6))
        code += b'\xe9' + struct.pack('<i', (site+8)-(relay+len(code)+5))
        def protect(address, length, mode):
            old = ctypes.c_ulong()
            if not k.VirtualProtect(address, length, mode, ctypes.byref(old)):
                raise ctypes.WinError(ctypes.get_last_error())
            return old.value
        process = k.GetCurrentProcess()
        applied = False
        old_mode = None
        try:
            ctypes.memmove(relay, bytes(code), len(code))
            protect(relay, 4096, 0x20)
            if not k.FlushInstructionCache(process, relay, len(code)):
                raise ctypes.WinError(ctypes.get_last_error())
            old_mode = protect(site, 8, 0x40)
            replacement = b'\xe9' + struct.pack('<i', relay-(site+5)) + b'\x90'*3
            ctypes.memmove(site, replacement, 8)
            applied = True
            if not k.FlushInstructionCache(process, site, 8):
                raise ctypes.WinError(ctypes.get_last_error())
            protect(site, 8, old_mode)
        except Exception:
            if applied:
                protect(site, 8, 0x40)
                ctypes.memmove(site, _ORIGINAL[:8], 8)
                k.FlushInstructionCache(process, site, 8)
            if old_mode is not None:
                protect(site, 8, old_mode)
            k.VirtualFree(relay, 0, 0x8000)
            raise
        _KEEPALIVE = (k, relay)
        _INSTALLED = dict(kernelSha256=digest, filterSiteRva=hex(sites[0]),
            notificationFlags=0x21c, wallFilterDataWord3=_WALL_MARKER,
            getShapesRva=hex(sites[1]), setSimulationFilterDataRva=hex(sites[2]),
            base=base)
        return dict(_INSTALLED)


def mark_wall_shape(actor):
    """Use verified PxRigidActor/PxShape virtual methods on its single shape."""
    metadata = install_wall_contact_notifications()
    base = metadata['base']
    pointer = actor.get_physx_address()
    table = ctypes.c_void_p.from_address(pointer).value
    address = ctypes.c_void_p.from_address(table+23*8).value
    if address != base + int(metadata['getShapesRva'], 16):
        raise RuntimeError('Unexpected static actor getShapes vtable entry')
    get_shapes = ctypes.WINFUNCTYPE(ctypes.c_uint32, ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint32, ctypes.c_uint32)(address)
    shape = ctypes.c_void_p()
    if get_shapes(pointer, ctypes.byref(shape), 1, 0) != 1:
        raise RuntimeError('Wall must have exactly one BoxCollider shape')
    table = ctypes.c_void_p.from_address(shape.value).value
    address = ctypes.c_void_p.from_address(table+20*8).value
    if address != base + int(metadata['setSimulationFilterDataRva'], 16):
        raise RuntimeError('Unexpected shape simulation-filter setter vtable entry')
    data_type = ctypes.c_uint32*4
    data = data_type(0, 0, 0, _WALL_MARKER)
    setter = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(data_type))(address)
    setter(shape, ctypes.byref(data))
    getter = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p,
        ctypes.POINTER(data_type))(ctypes.c_void_p.from_address(table+21*8).value)
    result = data_type()
    getter(shape, ctypes.byref(result))
    if list(result) != list(data):
        raise RuntimeError('Wall simulation-filter-data write did not round-trip')
    return shape.value
