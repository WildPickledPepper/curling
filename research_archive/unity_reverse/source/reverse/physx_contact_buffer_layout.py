#!/usr/bin/env python3
"""Print PhysX ContactPoint/ContactBuffer layouts for 32-bit WebGL."""

from __future__ import annotations

import ctypes


class ContactPoint(ctypes.Structure):
    _fields_ = [
        ("normal_x", ctypes.c_float),
        ("normal_y", ctypes.c_float),
        ("normal_z", ctypes.c_float),
        ("separation", ctypes.c_float),
        ("point_x", ctypes.c_float),
        ("point_y", ctypes.c_float),
        ("point_z", ctypes.c_float),
        ("maxImpulse", ctypes.c_float),
        ("targetVel_x", ctypes.c_float),
        ("targetVel_y", ctypes.c_float),
        ("targetVel_z", ctypes.c_float),
        ("staticFriction", ctypes.c_float),
        ("materialFlags", ctypes.c_uint8),
        ("_pad0", ctypes.c_uint8),
        ("forInternalUse", ctypes.c_uint16),
        ("internalFaceIndex1", ctypes.c_uint32),
        ("dynamicFriction", ctypes.c_float),
        ("restitution", ctypes.c_float),
    ]


class ContactBuffer(ctypes.Structure):
    _fields_ = [
        ("contacts", ContactPoint * 64),
        ("count", ctypes.c_uint32),
        ("pad", ctypes.c_uint32 * 3),
    ]


STRUCTS = [ContactPoint, ContactBuffer]


def main() -> int:
    for struct in STRUCTS:
        print(f"{struct.__name__}: size={ctypes.sizeof(struct)} align={ctypes.alignment(struct)}")
        for name, _type in struct._fields_:
            print(f"  {getattr(struct, name).offset:4d} {name}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
