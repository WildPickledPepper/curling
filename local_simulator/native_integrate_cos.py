"""Use Unity's observed cosine arithmetic at the two PhysX integration calls.

Evidence: analysis_input/case12009_cos_cause_20261003.md. Installation happens
before simulation, once per process. The native binding on disk is unchanged;
all other math calls still use their existing implementation.
"""
from __future__ import annotations

import ctypes
import hashlib
import platform
from pathlib import Path
import struct
import threading

from .runtime_loader import RUNTIME_ROOT, _resolve_bundled_extension

_KERNELS = {
    '7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38': (0x1fc8fd, 0x204d16),
    '2a2dbc19f42388239bc27c47ff90d1aef4ae4554f762afad09d13a209ae5b6f0': (0x1f360d, 0x1fba26),
    '44729fb97df143374a6c01d1a6bae59f11dd302ff8035d0432ec9a7c04c168f5': (0x1fabdd, 0x202ff6),
}
_DLL_SHA256 = '06324049c4151ac4f85a3484796f05df76bc73696e76fe85c56fec3a69953564'
_LOCK = threading.Lock()
_INSTALLED = None
_KEEPALIVE = None


def install_unity_integration_cosine():
    """Install verified native calls; reject unknown binaries rather than guess."""
    global _INSTALLED, _KEEPALIVE
    with _LOCK:
        if _INSTALLED is not None:
            return dict(_INSTALLED)
        extension = _resolve_bundled_extension()
        digest = hashlib.sha256(extension.read_bytes()).hexdigest()
        sites = _KERNELS.get(digest)
        if platform.system() != 'Windows' or ctypes.sizeof(ctypes.c_void_p) != 8 or sites is None:
            raise RuntimeError('Unity integration cosine requires a verified Windows x64 PhysX kernel')
        dll_path = RUNTIME_ROOT/'unity_integrate_cos.dll'
        if hashlib.sha256(dll_path.read_bytes()).hexdigest() != _DLL_SHA256:
            raise RuntimeError('Unity integration cosine DLL hash mismatch')
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
        kernel.GetModuleHandleW.restype = ctypes.c_void_p
        kernel.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
        kernel.VirtualAlloc.restype = ctypes.c_void_p
        kernel.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong]
        kernel.VirtualFree.restype = ctypes.c_int
        kernel.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
        kernel.VirtualProtect.restype = ctypes.c_int
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.FlushInstructionCache.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
        kernel.FlushInstructionCache.restype = ctypes.c_int
        base = kernel.GetModuleHandleW(str(extension))
        if not base:
            raise RuntimeError('Verified PhysX kernel must be loaded before installing integration cosine')
        expected = (bytes.fromhex('e87e3b2500'), bytes.fromhex('e865b72400'))
        for site, original in zip(sites, expected):
            if ctypes.string_at(base+site, 5) != original:
                raise RuntimeError('PhysX integration cosine call-site bytes mismatch')
        library = ctypes.CDLL(str(dll_path))
        library.unity_integrate_cosf.argtypes = [ctypes.c_float]
        library.unity_integrate_cosf.restype = ctypes.c_float
        target = ctypes.cast(library.unity_integrate_cosf, ctypes.c_void_p).value
        # A nearby 14-byte absolute jump preserves the call ABI and permits the
        # original five-byte rel32 calls regardless of DLL placement by ASLR.
        relay = None
        aligned = base & ~0xffff
        for distance in range(0x1000000, 0x70000000, 0x10000):
            for hint in (aligned+distance, aligned-distance):
                if hint <= 0:
                    continue
                if all(-2**31 <= hint-(base+s+5) < 2**31 for s in sites):
                    relay = kernel.VirtualAlloc(hint, 4096, 0x3000, 0x04)
                    if relay:
                        break
            if relay:
                break
        if not relay:
            raise RuntimeError('Cannot allocate nearby Unity integration cosine relay')
        process = kernel.GetCurrentProcess()

        def protect(address, length, mode):
            old = ctypes.c_ulong()
            if not kernel.VirtualProtect(address, length, mode, ctypes.byref(old)):
                raise ctypes.WinError(ctypes.get_last_error())
            return old.value

        def write_call(address, data):
            old = protect(address, len(data), 0x40)
            try:
                ctypes.memmove(address, data, len(data))
                if not kernel.FlushInstructionCache(process, address, len(data)):
                    raise ctypes.WinError(ctypes.get_last_error())
            finally:
                protect(address, len(data), old)

        applied = []
        try:
            jump = b'\xff\x25\x00\x00\x00\x00' + struct.pack('<Q', target)
            ctypes.memmove(relay, jump, len(jump))
            protect(relay, 4096, 0x20)
            if not kernel.FlushInstructionCache(process, relay, len(jump)):
                raise ctypes.WinError(ctypes.get_last_error())
            for site, original in zip(sites, expected):
                applied.append((base+site, original))
                write_call(base+site, b'\xe8' + struct.pack('<i', relay-(base+site+5)))
        except Exception:
            for address, original in reversed(applied):
                write_call(address, original)
            kernel.VirtualFree(relay, 0, 0x8000)
            raise
        _KEEPALIVE = (library, relay)
        _INSTALLED = dict(implementation='Unity f33062/f18889/f18888/f18176 moderate reduction',
            kernelSha256=digest, dllSha256=_DLL_SHA256,
            bridgeSourceSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            arithmeticSourceSha256=hashlib.sha256((RUNTIME_ROOT/'unity_integrate_cos.c').read_bytes()).hexdigest(),
            callSiteRvas=[hex(s) for s in sites], integrationHalfAngleLimitAtDt001=50000,
            supportedAbsInputBitsMax=1305022426)
        return dict(_INSTALLED)
