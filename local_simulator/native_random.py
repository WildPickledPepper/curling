"""Optional exact lazy random/noise mapping; consumption stays in the driver.

The integer transition and range arithmetic are the original f82200/f82202.
This only removes Python conversions, retaining the existing noise iterator's
rounding and state visibility. The reference generator remains available.
"""
from __future__ import annotations

import ctypes
from functools import lru_cache
import hashlib
import platform

from .runtime_loader import RUNTIME_ROOT

DLL_SHA256 = '9b936a2d75cd978c186a4140b2ce1cdc6f95d9abbcc9b78de70a158da105b591'


@lru_cache(maxsize=1)
def load_random_kernel():
    path = RUNTIME_ROOT/'unity_random.dll'
    if platform.system() != 'Windows' or ctypes.sizeof(ctypes.c_void_p) != 8 or not path.is_file():
        return None
    if hashlib.sha256(path.read_bytes()).hexdigest() != DLL_SHA256:
        raise RuntimeError('Unity random DLL hash mismatch')
    library = ctypes.CDLL(str(path))
    pointer = ctypes.POINTER(ctypes.c_uint32)
    library.unity_rng_step.argtypes = [pointer]
    library.unity_rng_step.restype = ctypes.c_uint32
    library.unity_rng_range.argtypes = [pointer, ctypes.c_float, ctypes.c_float]
    library.unity_rng_range.restype = ctypes.c_float
    library.unity_rng_friction_noise.argtypes = [pointer, ctypes.c_float, ctypes.c_float]
    library.unity_rng_friction_noise.restype = ctypes.c_double
    return library


def _word(index):
    return property(lambda self: self._state[index],
                    lambda self, value: self._state.__setitem__(index, value))


class NativeUnityRandom:
    """Four observable state words and a lazy, one-draw-per-next noise stream."""
    s0, s1, s2, s3 = (_word(index) for index in range(4))

    def __init__(self, state):
        self._library = load_random_kernel()
        if self._library is None:
            raise RuntimeError('Optional native random helper is unavailable')
        self._state = (ctypes.c_uint32*4)(*state)

    @classmethod
    def from_seed(cls, seed):
        from .runtime_support.tools.reverse.recovered_unity_random import RecoveredUnityRandom
        reference = RecoveredUnityRandom.from_seed(seed)
        return cls((reference.s0, reference.s1, reference.s2, reference.s3))

    def next_u32(self):
        return self._library.unity_rng_step(self._state)

    def range_float(self, minimum, maximum):
        return self._library.unity_rng_range(self._state, minimum, maximum)

    def friction_noises(self, *, sweeping=False):
        from .runtime_support.tools.reverse.recovered_curling_motion import (
            BASE_FRICTION, SWEEP_FRICTION, FRICTION_NOISE,
        )
        base = ctypes.c_float(SWEEP_FRICTION if sweeping else BASE_FRICTION)
        amplitude = ctypes.c_float(FRICTION_NOISE)
        function = self._library.unity_rng_friction_noise
        state = self._state
        while True:
            yield function(state, base, amplitude)
