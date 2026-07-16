"""Minimal pose object used by the CPython 3.13 pyphysx binding.

The strict curling simulator passes rotations as numeric WXYZ sequences and
only reads the returned ``w/x/y/z`` fields.  This avoids an unnecessary
numpy-quaternion binary dependency in the online Windows runtime.
"""


class quaternion:  # noqa: N801 - legacy pyphysx imports this exact name
    def __init__(self, w: float = 1.0, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
