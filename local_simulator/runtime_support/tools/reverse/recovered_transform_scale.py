"""Unity Transform scale arithmetic recovered from pinned WebGL functions.

Source SHA256 cbbd1ad26631837ae41df05311a87d0d9aa0a5e178a68d397046c2fa595bca81.
f78121 builds a column-major rotation/scale matrix; f78120 strips world
rotation and f72950 reads its diagonal. Every operation below rounds to f32.
This helper covers the observed stone hierarchy: one nonrotating parent
with positive scale. It does not yet update a live PhysX collision shape.
"""
from typing import Sequence

import numpy as np


def _rotation_columns(quaternion: Sequence[float]) -> tuple:
    x, y, z, w = map(np.float32, quaternion)
    zero, one, negative_two = map(np.float32, (0, 1, -2))
    tx, ty, tz = x+x, y+y, z+z
    nx, ny, nz = x*negative_two, y*negative_two, z*negative_two
    # Match the instruction order, including the final additions of zero.
    return (
        y*ny-z*tz+one, x*ty+w*tz+zero, w*ny+x*tz+zero,
        w*nz+y*tx+zero, z*nz-x*tx+one, y*tz+w*tx+zero,
        z*tx+w*ty+zero, w*nx+z*ty+zero, x*nx-y*ty+one,
    )


def _multiply_columns(left: Sequence, right: Sequence) -> tuple:
    # Wasm evaluates each dot product as a + (b + c), not (a + b) + c.
    return tuple(left[row]*right[col*3] + (
        left[row+3]*right[col*3+1] + left[row+6]*right[col*3+2])
        for col in range(3) for row in range(3))


def recovered_stone_world_matrix(
    local_quaternion_xyzw: Sequence[float],
    local_scale: Sequence[float],
    parent_scale: Sequence[float],
) -> tuple:
    """Replay f78121 for one parent with identity rotation and positive scale."""
    if len(local_scale) != 3 or len(parent_scale) != 3 or len(local_quaternion_xyzw) != 4:
        raise ValueError('Expected quaternion xyzw and two xyz scales')
    if any(float(value) <= 0 for value in parent_scale):
        raise ValueError('This recovered path requires positive parent scale')
    rotation = _rotation_columns(local_quaternion_xyzw)
    local = tuple(value*np.float32(local_scale[i//3]) for i,value in enumerate(rotation))
    parent_rotation = _rotation_columns((0,0,0,1))
    parent = tuple(value*np.float32(parent_scale[i//3]) for i,value in enumerate(parent_rotation))
    return _multiply_columns(parent, local)


def recovered_stone_scale_matrix(
    local_quaternion_xyzw: Sequence[float],
    local_scale: Sequence[float],
    parent_scale: Sequence[float],
) -> tuple:
    """Replay f78119/f78120 for the captured nonrotating parent hierarchy."""
    x,y,z,w = map(np.float32, local_quaternion_xyzw)
    inverse_rotation = _rotation_columns((-x,-y,-z,w))
    world = recovered_stone_world_matrix(local_quaternion_xyzw, local_scale, parent_scale)
    return _multiply_columns(inverse_rotation, world)


def recovered_stone_geometry_scale(
    local_quaternion_xyzw: Sequence[float],
    local_scale: Sequence[float],
    parent_scale: Sequence[float],
) -> tuple[float,float,float]:
    """Read the diagonal exactly as the observed f72950 geometry producer."""
    matrix = recovered_stone_scale_matrix(local_quaternion_xyzw,local_scale,parent_scale)
    return tuple(float(matrix[i]) for i in (0,4,8))
