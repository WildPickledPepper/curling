"""Minimal runtime compatibility module for the legacy pyphysx binding.

The binding only needs a mutable object exposing w/x/y/z when it materialises
PhysX poses.  The planner already passes rotations as numeric WXYZ lists, so
shipping the full numpy-quaternion native dependency is unnecessary.
"""


class quaternion:  # noqa: N801 - legacy binding imports this exact name
    def __init__(self, w: float = 1.0, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
