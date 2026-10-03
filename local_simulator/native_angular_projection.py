"""Optional exact native version of the existing float32 angular projection."""
from __future__ import annotations
import ctypes
from functools import lru_cache
import hashlib
import platform
from .runtime_loader import RUNTIME_ROOT

DLL_SHA256='8c64e77c9c58a037c1231ac4e2ddf63a0a36bcb2d8f7e2e39727ed0b95470848'

@lru_cache(maxsize=1)
def load_angular_projection():
    path=RUNTIME_ROOT/'unity_angular_projection.dll'
    if platform.system()!='Windows' or ctypes.sizeof(ctypes.c_void_p)!=8 or not path.is_file():
        return None  # The original Python arithmetic remains available.
    if hashlib.sha256(path.read_bytes()).hexdigest()!=DLL_SHA256:
        raise RuntimeError('Unity angular projection DLL hash mismatch')
    library=ctypes.CDLL(str(path))
    function=library.unity_angular_projection
    function.argtypes=[ctypes.c_float]*5+[ctypes.c_int,ctypes.POINTER(ctypes.c_float)]
    function.restype=None
    def project(q,angular_y,normalize=False):
        output=(ctypes.c_float*3)()
        function(*q,angular_y,int(normalize),output)
        return list(output)
    project.library=library
    return project
