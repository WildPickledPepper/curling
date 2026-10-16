"""Verified inline boolean simplification in the bundled Windows CP39 PhysX.

Installed once, before constructing scenes. All floating comparisons and their
order remain unchanged. The original function's stack and unwind data apply.
"""
from __future__ import annotations

import ctypes
import hashlib
import json
from pathlib import Path
import platform

KERNEL_SHA256 = '7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'
ASSET_SHA256 = '2df8260eda2850145cc71798166d77f4b9dd630b8669cd26838173371d5280bf'
ASSET = Path(__file__).resolve().parent/'runtime/physx_core_boolean_20261004.json'


class NativeCoreOptimization:
    """Toggle only before starting simulation or between quiescent requests."""

    def __init__(self, extension_path: Path):
        asset = ASSET.read_bytes()
        if hashlib.sha256(asset).hexdigest() != ASSET_SHA256:
            raise RuntimeError('PhysX core optimization asset hash mismatch')
        config = json.loads(asset)
        if config['kernel_sha256'] != KERNEL_SHA256:
            raise RuntimeError('PhysX core optimization kernel identity mismatch')
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
        kernel.GetModuleHandleW.restype = ctypes.c_void_p
        kernel.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32,
                                         ctypes.POINTER(ctypes.c_uint32)]
        kernel.VirtualProtect.restype = ctypes.c_int
        kernel.GetCurrentProcess.argtypes = []
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.FlushInstructionCache.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
        kernel.FlushInstructionCache.restype = ctypes.c_int
        base = kernel.GetModuleHandleW(str(extension_path))
        if not base:
            raise RuntimeError('Verified PhysX kernel is not loaded')
        self.kernel = kernel
        self.site = base+int(config['patch_start_rva'], 16)
        self.original = bytes.fromhex(config['original_hex'])
        self.replacement = bytes.fromhex(config['replacement_hex'])
        if len(self.original) != len(self.replacement):
            raise RuntimeError('PhysX core optimization length mismatch')
        if ctypes.string_at(self.site, len(self.original)) != self.original:
            raise RuntimeError('Loaded PhysX core instructions differ from verified original')
        self.enabled = False
        self.set_enabled(True)

    def set_enabled(self, enabled: bool) -> None:
        if self.enabled == enabled:
            return
        expected = self.replacement if self.enabled else self.original
        if ctypes.string_at(self.site, len(expected)) != expected:
            raise RuntimeError('Loaded PhysX core instructions changed unexpectedly')
        replacement = self.replacement if enabled else self.original
        previous = ctypes.c_uint32()
        if not self.kernel.VirtualProtect(self.site, len(replacement), 0x40, ctypes.byref(previous)):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            ctypes.memmove(self.site, replacement, len(replacement))
            self.enabled = bool(enabled)
        finally:
            unused = ctypes.c_uint32()
            if not self.kernel.VirtualProtect(self.site, len(replacement), previous.value, ctypes.byref(unused)):
                raise ctypes.WinError(ctypes.get_last_error())
        if not self.kernel.FlushInstructionCache(self.kernel.GetCurrentProcess(), self.site, len(replacement)):
            raise ctypes.WinError(ctypes.get_last_error())


def install_core_optimization(extension_path: Path):
    """Unknown platforms/ABIs/kernels retain their original instructions."""
    if platform.system() != 'Windows' or ctypes.sizeof(ctypes.c_void_p) != 8:
        return None
    if hashlib.sha256(extension_path.read_bytes()).hexdigest() != KERNEL_SHA256:
        return None
    return NativeCoreOptimization(extension_path)
