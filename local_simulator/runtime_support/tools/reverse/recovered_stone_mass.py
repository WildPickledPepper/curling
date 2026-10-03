"""Mass normalization recovered from the stone branch of Unity wasm f72776.

Source SHA256 cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81.
The captured hull has identity shape/scale rotation and an explicitly zero
Rigidbody COM. f72777 therefore skips the COM shift, and f69768 returns an
identity inertia rotation. This is the formal stone path, not a general mesh
mass-property routine. See analysis_input/11005_angular_gap_closed_20261002.md.
"""
from typing import Mapping, Sequence

import numpy as np


def recovered_stone_inertia(
    mass_information: Mapping, scale: Sequence[float], mass: float,
) -> tuple[float, float, float]:
    """Return the captured principal diagonals before Unity freezes X/Z.

    Preserve the expression tree: summing three half-diagonals and multiplying
    scale factors in the original order differs from double-precision formulas.
    """
    f = np.float32
    sx, sy, sz = map(f, scale)
    inertia = mass_information["local_inertia_rows"]
    ix, iy, iz = (f(inertia[i][i]) for i in range(3))
    half = f(0.5)
    half_trace = (ix * half + iy * half) + iz * half
    # f72776: sx * (sx * (halfTrace - Ixx)), and likewise for Y/Z.
    xx = sx * (sx * (half_trace - ix))
    yy = sy * (sy * (half_trace - iy))
    zz = sz * (sz * (half_trace - iz))
    volume = (sx * sy) * sz
    scaled_mass = f(mass_information["unit_density_mass"]) * volume
    density = f(mass) / scaled_mass
    return tuple(float((volume * value) * density)
                 for value in (yy + zz, zz + xx, xx + yy))
