"""Exact guarded identity for a dead solver product and negligible addition."""
from __future__ import annotations
import ctypes
import hashlib
from pathlib import Path
import platform
from .native_vertex_bounds import KERNEL_SHA256,NativeVertexBoundsOptimization,_Unavailable

ASSET = Path(__file__).resolve().parent/'runtime/physx_solver_product_20261004.json'
ASSET_SHA256 = 'c860b2865cd668546847f21a29cc4a50f24a991e41e4c12eb10d8a717da3e5f5'

class NativeSolverProductOptimization(NativeVertexBoundsOptimization):
    def __init__(self,extension_path: Path):
        # The generated code changes no stack layout. Use the same verified
        # near-page allocation, original-frame unwind chain and lifetime rules.
        super().__init__(extension_path,_asset_path=ASSET,_asset_sha256=ASSET_SHA256,
                         _name='PhysX solver product')

def install_solver_product_optimization(extension_path: Path):
    if platform.system()!='Windows' or ctypes.sizeof(ctypes.c_void_p)!=8:
        return None
    if hashlib.sha256(extension_path.read_bytes()).hexdigest()!=KERNEL_SHA256:
        return None
    try:
        return NativeSolverProductOptimization(extension_path)
    except _Unavailable:
        return None
