"""Guarded dead-channel optimization with chained Windows unwind metadata."""
from __future__ import annotations
import ctypes
import hashlib
import json
from pathlib import Path
import platform
import struct

KERNEL_SHA256 = '7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'
ASSET_SHA256 = '5579131a622e0eb6437ef9af261d4372b6f375cd79729e5923fee1d3e1bf1da4'
ASSET = Path(__file__).resolve().parent/'runtime/physx_dead_fourth_20261004.json'
_KEEPALIVE = []  # Windows retains pointers to the registered function table.

class _RuntimeFunction(ctypes.Structure):
    _fields_ = [('BeginAddress',ctypes.c_uint32),('EndAddress',ctypes.c_uint32),('UnwindData',ctypes.c_uint32)]

class _Unavailable(RuntimeError):
    pass

class NativeVertexBoundsOptimization:
    """Install before simulation; toggle only between quiescent requests."""

    def __init__(self,extension_path: Path,*,_asset_path: Path = ASSET,
                 _asset_sha256: str = ASSET_SHA256,_name: str = 'PhysX vertex bounds'):
        self.label = _name
        blob = _asset_path.read_bytes()
        if hashlib.sha256(blob).hexdigest()!=_asset_sha256:
            raise RuntimeError(f'{self.label} asset hash mismatch')
        config = json.loads(blob)
        if config['kernel_sha256']!=KERNEL_SHA256:
            raise RuntimeError(f'{self.label} kernel identity mismatch')
        kernel = ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
        kernel.GetModuleHandleW.restype = ctypes.c_void_p
        kernel.VirtualAlloc.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.c_uint32]
        kernel.VirtualAlloc.restype = ctypes.c_void_p
        kernel.VirtualFree.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32]
        kernel.VirtualFree.restype = ctypes.c_int
        kernel.VirtualProtect.argtypes = [ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32)]
        kernel.VirtualProtect.restype = ctypes.c_int
        kernel.FlushInstructionCache.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
        kernel.FlushInstructionCache.restype = ctypes.c_int
        kernel.GetCurrentProcess.argtypes = []
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.RtlAddFunctionTable.argtypes = [ctypes.POINTER(_RuntimeFunction),ctypes.c_uint32,ctypes.c_uint64]
        kernel.RtlAddFunctionTable.restype = ctypes.c_ubyte
        kernel.RtlDeleteFunctionTable.argtypes = [ctypes.POINTER(_RuntimeFunction)]
        kernel.RtlDeleteFunctionTable.restype = ctypes.c_ubyte
        base = kernel.GetModuleHandleW(str(extension_path))
        if not base:
            raise RuntimeError('Verified PhysX kernel is not loaded')
        self.kernel,self.base = kernel,base
        self.site = base+int(config['patch_start_rva'],16)
        self.original = bytes.fromhex(config['original_hex'])
        if ctypes.string_at(self.site,len(self.original))!=self.original:
            raise RuntimeError(f'Loaded {self.label} instructions differ from verified original')
        code = bytes.fromhex(config['simd_hex'])
        unwind = bytes.fromhex(config['unwind_chain_hex'])
        self.code_size = len(code)
        self.unwind_offset = (len(code)+15)&~15
        self.allocation_size = self.unwind_offset+len(unwind)
        # All dynamic RVAs share the original module's base, including the
        # original chained function entry. Allocate an unused nearby page.
        self.memory = None
        for step in range(256):
            hint = base+0x600000+step*0x10000
            address = kernel.VirtualAlloc(hint,self.allocation_size,0x3000,4)
            if address:
                self.memory = address
                break
        if not self.memory:
            raise _Unavailable(f'No nearby page available for verified {self.label} code')
        if not 0<=self.memory-base<0x100000000-self.allocation_size:
            kernel.VirtualFree(self.memory,0,0x8000)
            raise RuntimeError(f'Dynamic {self.label} code is outside the unwind RVA range')
        for fixup in config['relative_targets']:
            offset = fixup['offset']
            displacement = base+int(fixup['target_rva'],16)-(self.memory+offset+4)
            code = code[:offset]+struct.pack('<i',displacement)+code[offset+4:]
        self.payload = code
        ctypes.memmove(self.memory,code,len(code))
        ctypes.memmove(self.memory+self.unwind_offset,unwind,len(unwind))
        previous = ctypes.c_uint32()
        if not kernel.VirtualProtect(self.memory,self.allocation_size,0x20,ctypes.byref(previous)):
            kernel.VirtualFree(self.memory,0,0x8000)
            raise ctypes.WinError(ctypes.get_last_error())
        self.table = _RuntimeFunction(self.memory-base,self.memory-base+len(code),self.memory-base+self.unwind_offset)
        if not kernel.RtlAddFunctionTable(ctypes.byref(self.table),1,base):
            kernel.VirtualFree(self.memory,0,0x8000)
            raise _Unavailable(f'Cannot register {self.label} unwind information')
        # Preserve ECX; integer flags are dead here until the loop counter.
        # A forced conditional branch avoids the unwinder's tail-call heuristic
        # at the original entry redirect as well as at both generated returns.
        displacement = self.memory-(self.site+8)
        self.replacement = bytes.fromhex('39c90f84')+struct.pack('<i',displacement)+b'\x90'*(len(self.original)-8)
        self.enabled = False
        try:
            if not kernel.FlushInstructionCache(kernel.GetCurrentProcess(),self.memory,len(code)):
                raise ctypes.WinError(ctypes.get_last_error())
            self.set_enabled(True)
        except Exception:
            try:
                self.set_enabled(False)
            except Exception:
                # Keep code/table alive if restoring the original page fails.
                _KEEPALIVE.append(self)
                raise
            kernel.RtlDeleteFunctionTable(ctypes.byref(self.table))
            kernel.VirtualFree(self.memory,0,0x8000)
            raise
        _KEEPALIVE.append(self)

    def set_enabled(self,enabled: bool) -> None:
        if self.enabled==enabled:
            return
        expected = self.replacement if self.enabled else self.original
        if ctypes.string_at(self.site,len(expected))!=expected:
            raise RuntimeError(f'Loaded {self.label} instructions changed unexpectedly')
        replacement = self.replacement if enabled else self.original
        previous = ctypes.c_uint32()
        if not self.kernel.VirtualProtect(self.site,len(replacement),0x40,ctypes.byref(previous)):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            ctypes.memmove(self.site,replacement,len(replacement))
            self.enabled = bool(enabled)
        finally:
            unused = ctypes.c_uint32()
            if not self.kernel.VirtualProtect(self.site,len(replacement),previous.value,ctypes.byref(unused)):
                raise ctypes.WinError(ctypes.get_last_error())
        if not self.kernel.FlushInstructionCache(self.kernel.GetCurrentProcess(),self.site,len(replacement)):
            raise ctypes.WinError(ctypes.get_last_error())

def install_vertex_bounds_optimization(extension_path: Path):
    if platform.system()!='Windows' or ctypes.sizeof(ctypes.c_void_p)!=8:
        return None
    if hashlib.sha256(extension_path.read_bytes()).hexdigest()!=KERNEL_SHA256:
        return None
    try:
        return NativeVertexBoundsOptimization(extension_path)
    except _Unavailable:
        return None
