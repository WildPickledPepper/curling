#!/usr/bin/env python3
"""Print PhysX 4-wide contact solver structure layouts for 32-bit WebGL."""

from __future__ import annotations

import ctypes


class Vec4(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("w", ctypes.c_float),
    ]


class SolverContactHeader4(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_uint8),
        ("numNormalConstr", ctypes.c_uint8),
        ("numFrictionConstr", ctypes.c_uint8),
        ("flag", ctypes.c_uint8),
        ("flags", ctypes.c_uint8 * 4),
        ("numNormalConstr0", ctypes.c_uint8),
        ("numNormalConstr1", ctypes.c_uint8),
        ("numNormalConstr2", ctypes.c_uint8),
        ("numNormalConstr3", ctypes.c_uint8),
        ("numFrictionConstr0", ctypes.c_uint8),
        ("numFrictionConstr1", ctypes.c_uint8),
        ("numFrictionConstr2", ctypes.c_uint8),
        ("numFrictionConstr3", ctypes.c_uint8),
        ("restitution", Vec4),
        ("staticFriction", Vec4),
        ("dynamicFriction", Vec4),
        ("invMass0D0", Vec4),
        ("invMass1D1", Vec4),
        ("angDom0", Vec4),
        ("angDom1", Vec4),
        ("normalX", Vec4),
        ("normalY", Vec4),
        ("normalZ", Vec4),
        ("shapeInteraction", ctypes.c_uint32 * 4),
    ]


class SolverContactBatchPointBase4(ctypes.Structure):
    _fields_ = [
        ("raXnX", Vec4),
        ("raXnY", Vec4),
        ("raXnZ", Vec4),
        ("velMultiplier", Vec4),
        ("scaledBias", Vec4),
        ("biasedErr", Vec4),
    ]


class SolverContactBatchPointDynamic4(ctypes.Structure):
    _fields_ = SolverContactBatchPointBase4._fields_ + [
        ("rbXnX", Vec4),
        ("rbXnY", Vec4),
        ("rbXnZ", Vec4),
    ]


class SolverFrictionSharedData4(ctypes.Structure):
    _fields_ = [
        ("broken", Vec4),
        ("frictionBrokenWritebackByte", ctypes.c_uint32 * 4),
        ("normalX", Vec4 * 2),
        ("normalY", Vec4 * 2),
        ("normalZ", Vec4 * 2),
    ]


class SolverContactFrictionBase4(ctypes.Structure):
    _fields_ = [
        ("raXnX", Vec4),
        ("raXnY", Vec4),
        ("raXnZ", Vec4),
        ("scaledBias", Vec4),
        ("velMultiplier", Vec4),
        ("targetVelocity", Vec4),
    ]


class SolverContactFrictionDynamic4(ctypes.Structure):
    _fields_ = SolverContactFrictionBase4._fields_ + [
        ("rbXnX", Vec4),
        ("rbXnY", Vec4),
        ("rbXnZ", Vec4),
    ]


STRUCTS = [
    SolverContactHeader4,
    SolverContactBatchPointBase4,
    SolverContactBatchPointDynamic4,
    SolverFrictionSharedData4,
    SolverContactFrictionBase4,
    SolverContactFrictionDynamic4,
]


def main() -> int:
    for struct in STRUCTS:
        print(f"{struct.__name__}: size={ctypes.sizeof(struct)} align={ctypes.alignment(struct)}")
        for name, _type in struct._fields_:
            print(f"  {getattr(struct, name).offset:3d} {name}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
