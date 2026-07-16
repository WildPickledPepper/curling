#!/usr/bin/env python3
"""Extract PxSolverContactDesc / friction patch / solver constraint evidence."""

from __future__ import annotations

import argparse
import json
import math
import struct
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


CONTACT_DESC_OFFSETS = {
    "descPtr": 16,
    "body0": 20,
    "body1": 24,
    "data0": 28,
    "data1": 32,
    "shapeInteraction": 112,
    "contactsPtr": 116,
    "numContacts": 120,
    "hasMaxImpulse": 124,
    "disableStrongFriction": 125,
    "hasForceThresholds": 126,
    "restDistance": 128,
    "maxCCDSeparation": 132,
    "frictionPtr": 136,
    "frictionCount": 140,
    "contactForcesPtr": 144,
    "startFrictionPatchIndex": 148,
    "numFrictionPatches": 152,
    "startContactPatchIndex": 156,
    "numContactPatches": 160,
    "axisConstraintCount": 162,
}


def iter_windows(windows: Any) -> Iterable[dict[str, Any]]:
    if not isinstance(windows, list):
        return
    for window in windows:
        if not isinstance(window, dict):
            continue
        yield window
        yield from iter_windows(window.get("pointerTargets"))


def finite_vec(value: Any, size: int = 3) -> bool:
    return (
        isinstance(value, list)
        and len(value) == size
        and all(isinstance(x, (int, float)) and math.isfinite(x) for x in value)
    )


def raw_bytes(window: dict[str, Any]) -> bytes:
    raw = window.get("rawBytes")
    if not isinstance(raw, list):
        return b""
    return bytes(int(x) & 0xFF for x in raw)


def read_u8(raw: bytes, offset: int) -> int | None:
    return raw[offset] if 0 <= offset < len(raw) else None


def read_u16(raw: bytes, offset: int) -> int | None:
    if offset < 0 or offset + 2 > len(raw):
        return None
    return struct.unpack_from("<H", raw, offset)[0]


def read_u32(raw: bytes, offset: int) -> int | None:
    if offset < 0 or offset + 4 > len(raw):
        return None
    return struct.unpack_from("<I", raw, offset)[0]


def read_f32(raw: bytes, offset: int) -> float | None:
    if offset < 0 or offset + 4 > len(raw):
        return None
    value = struct.unpack_from("<f", raw, offset)[0]
    return value if math.isfinite(value) else None


def preview_f32(window: dict[str, Any] | None, index: int) -> float | None:
    if not isinstance(window, dict):
        return None
    values = window.get("f32Preview")
    if not isinstance(values, list) or index < 0 or index >= len(values):
        return None
    value = values[index]
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        return None
    return float(value)


def preview_u32(window: dict[str, Any] | None, index: int) -> int | None:
    if not isinstance(window, dict):
        return None
    values = window.get("u32Preview")
    if not isinstance(values, list) or index < 0 or index >= len(values):
        return None
    value = values[index]
    if not isinstance(value, int):
        return None
    return int(value)


def preview_vec3(window: dict[str, Any] | None, start: int) -> list[float | None]:
    return [preview_f32(window, start), preview_f32(window, start + 1), preview_f32(window, start + 2)]


def preview_quat(window: dict[str, Any] | None, start: int) -> dict[str, float | None]:
    return {
        "x": preview_f32(window, start),
        "y": preview_f32(window, start + 1),
        "z": preview_f32(window, start + 2),
        "w": preview_f32(window, start + 3),
    }


def preview_transform(window: dict[str, Any] | None, start_float: int) -> dict[str, Any] | None:
    if not isinstance(window, dict):
        return None
    quat = preview_quat(window, start_float)
    pos = preview_vec3(window, start_float + 4)
    if all(value is None for value in quat.values()) and all(value is None for value in pos):
        return None
    return {"q": quat, "p": pos}


def finite_float(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def usable_vec3(value: Any) -> bool:
    return finite_vec(value, 3)


def vec_sub(a: list[float], b: list[float]) -> list[float]:
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def vec_dot(a: list[float], b: list[float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vec_cross(a: list[float], b: list[float]) -> list[float]:
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def mat33_mul_vec(columns: dict[str, Any], vec: list[float]) -> list[float] | None:
    c0 = columns.get("column0") if isinstance(columns, dict) else None
    c1 = columns.get("column1") if isinstance(columns, dict) else None
    c2 = columns.get("column2") if isinstance(columns, dict) else None
    if not (usable_vec3(c0) and usable_vec3(c1) and usable_vec3(c2)):
        return None
    return [
        float(c0[0]) * vec[0] + float(c1[0]) * vec[1] + float(c2[0]) * vec[2],
        float(c0[1]) * vec[0] + float(c1[1]) * vec[1] + float(c2[1]) * vec[2],
        float(c0[2]) * vec[0] + float(c1[2]) * vec[1] + float(c2[2]) * vec[2],
    ]


def first_contact(candidate: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(candidate, dict):
        return None
    contacts = candidate.get("contactsPreview")
    if isinstance(contacts, list) and contacts and isinstance(contacts[0], dict):
        return contacts[0]
    return None


def classify_contact(contact: dict[str, Any] | None) -> str:
    if not contact:
        return "no_contact"
    normal = contact.get("normal")
    dyn = contact.get("dynamicFriction")
    restitution = contact.get("restitution")
    if restitution == 1 and isinstance(dyn, (int, float)) and dyn >= 0.3:
        return "stone_stone"
    if finite_vec(normal) and abs(float(normal[1])) > 0.75:
        return "stone_rink"
    return "unknown_pair"


def find_direct_child(window: dict[str, Any], source_offset: int) -> dict[str, Any] | None:
    targets = window.get("pointerTargets")
    if not isinstance(targets, list):
        return None
    for child in targets:
        if isinstance(child, dict) and child.get("sourceOffset") == source_offset:
            return child
    return None


def find_top_arg(windows: Any, arg_index: int) -> dict[str, Any] | None:
    if not isinstance(windows, list):
        return None
    for window in windows:
        if isinstance(window, dict) and window.get("argIndex") == arg_index:
            return window
    return None


def find_windows_by_ptr(event: dict[str, Any], ptr: int | None) -> list[dict[str, Any]]:
    if not isinstance(ptr, int) or ptr <= 0:
        return []
    data = event.get("data") or {}
    return [window for window in iter_windows(data.get("pointerWindows")) if window.get("ptr") == ptr]


def first_extra_contact_desc(event: dict[str, Any]) -> dict[str, Any] | None:
    data = event.get("data") or {}
    extras = data.get("extraDumps")
    if not isinstance(extras, list):
        return None
    for extra in extras:
        if isinstance(extra, dict) and extra.get("label") == "createFinalizeSolverContacts.contactDesc":
            return extra
    for extra in extras:
        if isinstance(extra, dict) and str(extra.get("label") or "").endswith(".contactDesc"):
            return extra
    return None


def first_extra_with_label_suffix(event: dict[str, Any], suffix: str) -> dict[str, Any] | None:
    data = event.get("data") or {}
    extras = data.get("extraDumps")
    if not isinstance(extras, list):
        return None
    for extra in extras:
        if isinstance(extra, dict) and str(extra.get("label") or "").endswith(suffix):
            return extra
    return None


def extra_window(extra: dict[str, Any] | None, key: str) -> dict[str, Any] | None:
    if not isinstance(extra, dict):
        return None
    value = extra.get(key)
    return value if isinstance(value, dict) else None


def decode_f32_array(window: dict[str, Any] | None, max_count: int = 64) -> list[float | None]:
    raw = raw_bytes(window) if isinstance(window, dict) else b""
    if not raw:
        return []
    count = min(len(raw) // 4, max_count)
    return [read_f32(raw, index * 4) for index in range(count)]


def decode_solver_body_data(window: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(window, dict):
        return None
    return {
        "ptr": window.get("ptr"),
        "rawBytesAvailable": bool(window.get("rawBytes")),
        "linearVelocity": preview_vec3(window, 0),
        "invMass": preview_f32(window, 3),
        "angularVelocity": preview_vec3(window, 4),
        "reportThreshold": preview_f32(window, 7),
        "sqrtInvInertia": {
            "column0": preview_vec3(window, 8),
            "column1": preview_vec3(window, 11),
            "column2": preview_vec3(window, 14),
        },
        "penBiasClamp": preview_f32(window, 17),
        "nodeIndex": preview_u32(window, 18),
        "maxContactImpulse": preview_f32(window, 19),
        "body2World": preview_transform(window, 20),
        "lockFlags": (preview_u32(window, 27) or 0) & 0xFFFF if preview_u32(window, 27) is not None else None,
    }


def _decoded_child(extra: dict[str, Any] | None, key: str) -> dict[str, Any] | None:
    if not isinstance(extra, dict):
        return None
    child = extra.get(key)
    if not isinstance(child, dict):
        return None
    decoded = child.get("decoded")
    return decoded if isinstance(decoded, dict) else None


def _child_window_presence(extra: dict[str, Any] | None, key: str) -> dict[str, Any]:
    if not isinstance(extra, dict):
        return {"present": False, "rawBytesAvailable": False}
    child = extra.get(key)
    if not isinstance(child, dict):
        return {"present": False, "rawBytesAvailable": False}
    window = child.get("window")
    if isinstance(window, dict):
        return {
            "present": True,
            "ptr": window.get("ptr"),
            "rawBytesAvailable": bool(window.get("rawBytes")),
        }
    return {"present": True, "rawBytesAvailable": False}


def _raw_window_summary(window: Any) -> dict[str, Any]:
    if not isinstance(window, dict):
        return {"present": False, "rawBytesAvailable": False}
    raw = window.get("rawBytes")
    return {
        "present": True,
        "ptr": window.get("ptr"),
        "bytes": window.get("byteLength"),
        "rawBytesAvailable": isinstance(raw, list),
        "rawByteCount": len(raw) if isinstance(raw, list) else None,
    }


def _bigconvex_arrays_summary(runtime: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(runtime, dict):
        return {"present": False, "completeRawArrays": False}
    arrays = runtime.get("bigConvexRawDataArrays")
    if not isinstance(arrays, dict):
        return {"present": False, "completeRawArrays": False}
    samples = _raw_window_summary(arrays.get("samplesWindow"))
    valencies = _raw_window_summary(arrays.get("valenciesWindow"))
    adjacent = _raw_window_summary(arrays.get("adjacentVertsWindow"))
    return {
        "present": True,
        "samples": samples,
        "valencies": valencies,
        "adjacentVerts": adjacent,
        "completeRawArrays": (
            samples["rawBytesAvailable"]
            and valencies["rawBytesAvailable"]
            and adjacent["rawBytesAvailable"]
        ),
    }


def _hull_runtime_summary(shape: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(shape, dict):
        return {"present": False}
    hull_data = shape.get("hullData") if isinstance(shape.get("hullData"), dict) else None
    runtime = shape.get("hullRuntime") if isinstance(shape.get("hullRuntime"), dict) else None
    runtime_window = (
        runtime.get("runtimeBufferWindow")
        if isinstance(runtime, dict) and isinstance(runtime.get("runtimeBufferWindow"), dict)
        else None
    )
    big_window = (
        runtime.get("bigConvexRawDataWindow")
        if isinstance(runtime, dict) and isinstance(runtime.get("bigConvexRawDataWindow"), dict)
        else None
    )
    big_arrays = _bigconvex_arrays_summary(runtime)
    return {
        "present": isinstance(runtime, dict),
        "hullData": hull_data,
        "vertexRefCount": runtime.get("vertexRefCount") if isinstance(runtime, dict) else None,
        "byteLayout": runtime.get("byteLayout") if isinstance(runtime, dict) else None,
        "runtimeBufferWindowPresent": isinstance(runtime_window, dict),
        "runtimeBufferRawBytesAvailable": bool((runtime_window or {}).get("rawBytes")),
        "runtimeBufferBytes": (runtime_window or {}).get("byteLength"),
        "runtimeBufferPtr": (runtime_window or {}).get("ptr"),
        "bigConvexRawDataWindowPresent": isinstance(big_window, dict),
        "bigConvexRawDataRawBytesAvailable": bool((big_window or {}).get("rawBytes")),
        "bigConvexRawDataBytes": (big_window or {}).get("byteLength"),
        "bigConvexRawDataPtr": (big_window or {}).get("ptr"),
        "bigConvexRawDataArraysPresent": big_arrays["present"],
        "bigConvexRawDataArraysComplete": big_arrays["completeRawArrays"],
        "bigConvexRawDataArrays": big_arrays,
    }


def summarize_pcm_extra(event: dict[str, Any]) -> dict[str, Any] | None:
    extra = first_extra_with_label_suffix(event, ".pcmInputs")
    if not isinstance(extra, dict):
        return None
    contact_buffer = extra.get("contactBuffer") if isinstance(extra.get("contactBuffer"), dict) else {}
    contact_candidate = contact_buffer.get("decoded") if isinstance(contact_buffer, dict) else None
    first = first_contact(contact_candidate if isinstance(contact_candidate, dict) else None)
    cache = _decoded_child(extra, "cache") or {}
    shape0 = _decoded_child(extra, "shape0")
    shape1 = _decoded_child(extra, "shape1")
    return {
        "label": extra.get("label"),
        "ptrs": {
            "shape0": extra.get("shape0Ptr"),
            "shape1": extra.get("shape1Ptr"),
            "transform0": extra.get("transform0Ptr"),
            "transform1": extra.get("transform1Ptr"),
            "params": extra.get("paramsPtr"),
            "cache": extra.get("cachePtr"),
            "contactBuffer": extra.get("contactBufferPtr"),
        },
        "shape0": {
            "decoded": shape0,
            "window": _child_window_presence(extra, "shape0"),
            "hullDataWindowPresent": isinstance(
                (extra.get("shape0") or {}).get("hullDataWindow")
                if isinstance(extra.get("shape0"), dict)
                else None,
                dict,
            ),
            "hullRuntime": _hull_runtime_summary(
                extra.get("shape0") if isinstance(extra.get("shape0"), dict) else None
            ),
        },
        "shape1": {
            "decoded": shape1,
            "window": _child_window_presence(extra, "shape1"),
            "hullDataWindowPresent": isinstance(
                (extra.get("shape1") or {}).get("hullDataWindow")
                if isinstance(extra.get("shape1"), dict)
                else None,
                dict,
            ),
            "hullRuntime": _hull_runtime_summary(
                extra.get("shape1") if isinstance(extra.get("shape1"), dict) else None
            ),
        },
        "transform0": _decoded_child(extra, "transform0"),
        "transform1": _decoded_child(extra, "transform1"),
        "narrowPhaseParams": _decoded_child(extra, "narrowPhaseParams"),
        "cache": {
            "decoded": cache,
            "window": _child_window_presence(extra, "cache"),
            "manifoldWindowPresent": isinstance(
                (extra.get("cache") or {}).get("manifoldWindow")
                if isinstance(extra.get("cache"), dict)
                else None,
                dict,
            ),
            "manifoldRawBytesAvailable": bool(
                (((extra.get("cache") or {}).get("manifoldWindow") or {}).get("rawBytes"))
            )
            if isinstance(extra.get("cache"), dict)
            else False,
        },
        "contactBuffer": {
            "window": _child_window_presence(extra, "contactBuffer"),
            "candidate": contact_candidate,
            "firstContact": first,
            "pairClass": classify_contact(first),
        },
    }


def compute_normal_rows(
    contact_candidate: dict[str, Any] | None,
    contact_desc: dict[str, Any],
    solver_body_data: dict[str, Any],
    args: list[Any],
) -> list[dict[str, Any]]:
    contacts = contact_candidate.get("contactsPreview") if isinstance(contact_candidate, dict) else None
    if not isinstance(contacts, list):
        return []
    data0 = solver_body_data.get("data0") if isinstance(solver_body_data, dict) else None
    data1 = solver_body_data.get("data1") if isinstance(solver_body_data, dict) else None
    frame0 = contact_desc.get("bodyFrame0")
    frame1 = contact_desc.get("bodyFrame1")
    if not (isinstance(data0, dict) and isinstance(data1, dict) and isinstance(frame0, dict) and isinstance(frame1, dict)):
        return []
    p0 = frame0.get("p")
    p1 = frame1.get("p")
    if not (usable_vec3(p0) and usable_vec3(p1)):
        return []
    lin0 = data0.get("linearVelocity")
    lin1 = data1.get("linearVelocity")
    ang0 = data0.get("angularVelocity")
    ang1 = data1.get("angularVelocity")
    if not (usable_vec3(lin0) and usable_vec3(lin1) and usable_vec3(ang0) and usable_vec3(ang1)):
        return []

    inv_dt = float(args[3]) if len(args) > 3 and finite_float(args[3]) else 100.0
    bounce_threshold = float(args[4]) if len(args) > 4 and finite_float(args[4]) else -0.05
    solver_offset_slop = float(args[7]) if len(args) > 7 and finite_float(args[7]) else 0.0
    inv_dt_p8 = inv_dt * 0.8
    rest_distance = float(contact_desc.get("restDistance") or 0.0)
    ccd_max_separation = float(contact_desc.get("maxCCDSeparation") or 0.0)
    d0 = float((contact_desc.get("invMassScales") or {}).get("linear0") or 1.0)
    d1 = float((contact_desc.get("invMassScales") or {}).get("linear1") or 1.0)
    ang_d0 = float((contact_desc.get("invMassScales") or {}).get("angular0") or 1.0)
    ang_d1 = float((contact_desc.get("invMassScales") or {}).get("angular1") or 1.0)
    inv_mass0 = float(data0.get("invMass") or 0.0)
    inv_mass1 = float(data1.get("invMass") or 0.0)
    max_pen_bias = max(float(data0.get("penBiasClamp") or 0.0), float(data1.get("penBiasClamp") or 0.0))

    rows: list[dict[str, Any]] = []
    for index, contact in enumerate(contacts):
        if not isinstance(contact, dict):
            continue
        normal = contact.get("normal")
        point = contact.get("point")
        target_vel = contact.get("targetVel") or [0.0, 0.0, 0.0]
        separation = contact.get("separation")
        restitution = contact.get("restitution")
        max_impulse = contact.get("maxImpulse")
        if not (
            usable_vec3(normal)
            and usable_vec3(point)
            and usable_vec3(target_vel)
            and finite_float(separation)
            and finite_float(restitution)
        ):
            continue
        normal_f = [float(v) for v in normal]
        point_f = [float(v) for v in point]
        target_vel_f = [float(v) for v in target_vel]
        ra = vec_sub(point_f, [float(v) for v in p0])
        rb = vec_sub(point_f, [float(v) for v in p1])
        ra_x_n = vec_cross(ra, normal_f)
        rb_x_n = vec_cross(rb, normal_f)
        if solver_offset_slop > 0:
            ra_x_n = [0.0 if abs(v) < solver_offset_slop else v for v in ra_x_n]
            rb_x_n = [0.0 if abs(v) < solver_offset_slop else v for v in rb_x_n]
        ra_solver = mat33_mul_vec(data0.get("sqrtInvInertia") or {}, ra_x_n)
        rb_solver = mat33_mul_vec(data1.get("sqrtInvInertia") or {}, rb_x_n)
        if not (usable_vec3(ra_solver) and usable_vec3(rb_solver)):
            continue
        normal_len_sq = vec_dot(normal_f, normal_f)
        inv_mass_nor0 = inv_mass0 * d0 * normal_len_sq
        # PhysX passes invMassNorLenSq1 as -invMass1*d1*|n|^2, then subtracts it.
        inv_mass_nor1_negative = -inv_mass1 * d1 * normal_len_sq
        resp0 = inv_mass_nor0 + vec_dot(ra_solver, ra_solver) * ang_d0
        resp1 = vec_dot(rb_solver, rb_solver) * ang_d1 - inv_mass_nor1_negative
        unit_response = resp0 + resp1
        vel_multiplier = 1.0 / unit_response if unit_response > 0 else 0.0
        nor_vel = vec_dot(normal_f, vec_sub([float(v) for v in lin0], [float(v) for v in lin1]))
        vrel = nor_vel + vec_dot(ra_x_n, [float(v) for v in ang0]) - vec_dot(rb_x_n, [float(v) for v in ang1])
        penetration = float(separation) - rest_distance
        penetration_inv_dt = penetration * inv_dt
        penetration_inv_dt_p8 = max(max_pen_bias, penetration * inv_dt_p8)
        scaled_bias = vel_multiplier * penetration_inv_dt_p8
        bounce = (
            float(restitution) > 0.0
            and bounce_threshold > vrel
            and -vrel > penetration_inv_dt
            and ccd_max_separation >= penetration
        )
        if bounce:
            scaled_bias = 0.0
        c_target_vel = vec_dot(normal_f, target_vel_f)
        target_velocity = c_target_vel + ((-vrel) * float(restitution) if bounce else 0.0)
        target_velocity -= vrel
        biased_err = target_velocity * vel_multiplier - scaled_bias
        unbiased_err = target_velocity * vel_multiplier - (0.0 if bounce else max(scaled_bias, 0.0))
        rows.append(
            {
                "index": index,
                "source": "computed from ContactBuffer + PxSolverBodyData using DyContactPrepShared.constructContactConstraint",
                "ra": ra,
                "rb": rb,
                "rawRaXn": ra_x_n,
                "rawRbXn": rb_x_n,
                "raXn": ra_solver,
                "rbXn": rb_solver,
                "normalVelocity": nor_vel,
                "relativeNormalVelocity": vrel,
                "unitResponse": unit_response,
                "velMultiplier": vel_multiplier,
                "penetration": penetration,
                "scaledBias": scaled_bias,
                "bounce": bounce,
                "biasedErr": biased_err,
                "unbiasedErr": unbiased_err,
                "maxImpulse": float(max_impulse) if finite_float(max_impulse) else max_impulse,
            }
        )
    return rows


def decode_contact_desc(window: dict[str, Any]) -> dict[str, Any]:
    raw = raw_bytes(window)
    out: dict[str, Any] = {
        "ptr": window.get("ptr"),
        "rawBytesAvailable": bool(raw),
    }
    if not raw:
        return out

    out.update(
        {
            "invMassScales": {
                "linear0": read_f32(raw, 0),
                "angular0": read_f32(raw, 4),
                "linear1": read_f32(raw, 8),
                "angular1": read_f32(raw, 12),
            },
            "descPtr": read_u32(raw, CONTACT_DESC_OFFSETS["descPtr"]),
            "body0": read_u32(raw, CONTACT_DESC_OFFSETS["body0"]),
            "body1": read_u32(raw, CONTACT_DESC_OFFSETS["body1"]),
            "data0": read_u32(raw, CONTACT_DESC_OFFSETS["data0"]),
            "data1": read_u32(raw, CONTACT_DESC_OFFSETS["data1"]),
            "bodyFrame0": preview_transform(window, 9),
            "bodyFrame1": preview_transform(window, 16),
            "bodyState0": read_u32(raw, 92),
            "bodyState1": read_u32(raw, 96),
            "shapeInteraction": read_u32(raw, CONTACT_DESC_OFFSETS["shapeInteraction"]),
            "contactsPtr": read_u32(raw, CONTACT_DESC_OFFSETS["contactsPtr"]),
            "numContacts": read_u32(raw, CONTACT_DESC_OFFSETS["numContacts"]),
            "hasMaxImpulse": bool(read_u8(raw, CONTACT_DESC_OFFSETS["hasMaxImpulse"]) or 0),
            "disableStrongFriction": bool(read_u8(raw, CONTACT_DESC_OFFSETS["disableStrongFriction"]) or 0),
            "hasForceThresholds": bool(read_u8(raw, CONTACT_DESC_OFFSETS["hasForceThresholds"]) or 0),
            "restDistance": read_f32(raw, CONTACT_DESC_OFFSETS["restDistance"]),
            "maxCCDSeparation": read_f32(raw, CONTACT_DESC_OFFSETS["maxCCDSeparation"]),
            "frictionPtr": read_u32(raw, CONTACT_DESC_OFFSETS["frictionPtr"]),
            "frictionCount": read_u8(raw, CONTACT_DESC_OFFSETS["frictionCount"]),
            "contactForcesPtr": read_u32(raw, CONTACT_DESC_OFFSETS["contactForcesPtr"]),
            "startFrictionPatchIndex": read_u32(raw, CONTACT_DESC_OFFSETS["startFrictionPatchIndex"]),
            "numFrictionPatches": read_u32(raw, CONTACT_DESC_OFFSETS["numFrictionPatches"]),
            "startContactPatchIndex": read_u32(raw, CONTACT_DESC_OFFSETS["startContactPatchIndex"]),
            "numContactPatches": read_u16(raw, CONTACT_DESC_OFFSETS["numContactPatches"]),
            "axisConstraintCount": read_u16(raw, CONTACT_DESC_OFFSETS["axisConstraintCount"]),
        }
    )
    return out


def decode_solver_constraint_descs(desc_window: dict[str, Any] | None, event: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(desc_window, dict):
        return []
    words = desc_window.get("u32Preview")
    if not isinstance(words, list):
        return []

    rows: list[dict[str, Any]] = []
    for index in range(0, min(len(words) // 8, 8)):
        base = index * 8
        body_a = words[base]
        body_b = words[base + 1]
        links = words[base + 2]
        packed_lengths = words[base + 5]
        constraint_ptr = words[base + 6]
        writeback_ptr = words[base + 7]
        if index > 0 and body_a == 0 and body_b == 0 and constraint_ptr == 0:
            break
        constraint_len_over16 = (int(packed_lengths) >> 16) & 0xFFFF
        writeback_len_over4 = int(packed_lengths) & 0xFFFF
        matching_windows = find_windows_by_ptr(event, int(constraint_ptr))
        raw_window = next((window for window in matching_windows if raw_bytes(window)), None)
        rows.append(
            {
                "index": index,
                "bodyA": body_a,
                "bodyB": body_b,
                "linkIndexA": int(links) & 0xFFFF,
                "linkIndexB": (int(links) >> 16) & 0xFFFF,
                "bodyADataIndex": words[base + 3],
                "bodyBDataIndex": words[base + 4],
                "writeBackLengthOver4": writeback_len_over4,
                "constraintLengthOver16": constraint_len_over16,
                "expectedConstraintBytes": constraint_len_over16 * 16,
                "constraintPtr": constraint_ptr,
                "writeBackPtr": writeback_ptr,
                "constraintWindowPresent": bool(matching_windows),
                "constraintWindowLabels": [w.get("label") for w in matching_windows[:4]],
                "constraintRawBytesAvailable": any(bool(w.get("rawBytes")) for w in matching_windows),
                "decodedConstraint": decode_solver_contact_block(raw_window),
            }
        )
    return rows


def decode_friction_patch(window: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(window, dict):
        return None
    words = window.get("u32Preview")
    floats = window.get("f32Preview")
    if not isinstance(words, list) or not words:
        return None
    if not isinstance(floats, list):
        floats = []

    first = int(words[0])

    def vec3(start: int) -> list[Any] | None:
        if len(floats) < start + 3:
            return None
        return floats[start : start + 3]

    return {
        "ptr": window.get("ptr"),
        "sourceOffset": window.get("sourceOffset"),
        "layout": "Dy::FrictionPatch preview",
        "rawBytesAvailable": bool(window.get("rawBytes")),
        "broken": first & 0xFF,
        "materialFlags": (first >> 8) & 0xFF,
        "anchorCount": (first >> 16) & 0xFFFF,
        "restitution": floats[1] if len(floats) > 1 else None,
        "staticFriction": floats[2] if len(floats) > 2 else None,
        "dynamicFriction": floats[3] if len(floats) > 3 else None,
        "body0Normal": vec3(4),
        "body1Normal": vec3(7),
        "body0Anchors": [vec3(10), vec3(13)],
        "body1Anchors": [vec3(16), vec3(19)],
        "relativeQuat": floats[22:26] if len(floats) >= 26 else None,
        "u32Preview": words[:32],
        "f32Preview": floats[:32],
    }


def decode_solver_contact_block(
    window: dict[str, Any] | None,
    *,
    pointer_bytes: int = 4,
) -> dict[str, Any] | None:
    """Decode a PhysX 4.1 scalar contact block.

    Unity WebGL stores 32-bit pointers, so its ``SolverContactHeader`` is
    64 bytes.  The local pyphysx replay is a native x64 build where the two
    pointer fields expand the same header to 80 bytes.  Constraint rows begin
    immediately after that header; treating an x64 dump as wasm shifts every
    row by 16 bytes and produces a plausible-but-false semantic comparison.
    """
    if not isinstance(window, dict):
        return None
    if pointer_bytes not in (4, 8):
        raise ValueError("pointer_bytes must be 4 (wasm) or 8 (native x64)")
    raw = raw_bytes(window)
    header_size = 64 if pointer_bytes == 4 else 80
    if len(raw) < header_size:
        return None

    header = {
        "type": read_u8(raw, 0),
        "flags": read_u8(raw, 1),
        "numNormalConstr": read_u8(raw, 2),
        "numFrictionConstr": read_u8(raw, 3),
        "angDom0": read_f32(raw, 4),
        "angDom1": read_f32(raw, 8),
        "invMass0": read_f32(raw, 12),
        "staticFriction": read_f32(raw, 16),
        "dynamicFriction": read_f32(raw, 20),
        "dominance0": read_f32(raw, 24),
        "dominance1": read_f32(raw, 28),
        "normal": [read_f32(raw, 32), read_f32(raw, 36), read_f32(raw, 40)],
        "minAppliedImpulseForFriction": read_f32(raw, 44),
        "invMass1": read_f32(raw, 48),
        "broken": read_u32(raw, 52),
        "frictionBrokenWritebackByte": (
            read_u32(raw, 56) if pointer_bytes == 4 else int.from_bytes(bytes(raw[56:64]), "little")
        ),
        "shapeInteraction": (
            read_u32(raw, 60) if pointer_bytes == 4 else int.from_bytes(bytes(raw[64:72]), "little")
        ),
        "pointerBytes": pointer_bytes,
        "headerBytes": header_size,
    }

    cursor = header_size
    normal_rows: list[dict[str, Any]] = []
    for index in range(int(header.get("numNormalConstr") or 0)):
        if cursor + 48 > len(raw):
            break
        normal_rows.append(
            {
                "index": index,
                "raXn": [read_f32(raw, cursor), read_f32(raw, cursor + 4), read_f32(raw, cursor + 8)],
                "rbXn": [
                    read_f32(raw, cursor + 16),
                    read_f32(raw, cursor + 20),
                    read_f32(raw, cursor + 24),
                ],
                "velMultiplier": read_f32(raw, cursor + 32),
                "biasedErr": read_f32(raw, cursor + 36),
                "unbiasedErr": read_f32(raw, cursor + 40),
                "maxImpulse": read_f32(raw, cursor + 44),
            }
        )
        cursor += 48

    force_count = (int(header.get("numNormalConstr") or 0) + 3) & ~3
    applied_normal_forces = []
    for index in range(force_count):
        if cursor + 4 > len(raw):
            break
        applied_normal_forces.append(read_f32(raw, cursor))
        cursor += 4

    friction_rows: list[dict[str, Any]] = []
    for index in range(int(header.get("numFrictionConstr") or 0)):
        if cursor + 64 > len(raw):
            break
        friction_rows.append(
            {
                "index": index,
                "normal": [read_f32(raw, cursor), read_f32(raw, cursor + 4), read_f32(raw, cursor + 8)],
                "appliedForce": read_f32(raw, cursor + 12),
                "raXn": [
                    read_f32(raw, cursor + 16),
                    read_f32(raw, cursor + 20),
                    read_f32(raw, cursor + 24),
                ],
                "velMultiplier": read_f32(raw, cursor + 28),
                "rbXn": [
                    read_f32(raw, cursor + 32),
                    read_f32(raw, cursor + 36),
                    read_f32(raw, cursor + 40),
                ],
                "bias": read_f32(raw, cursor + 44),
                "targetVel": read_f32(raw, cursor + 48),
            }
        )
        cursor += 64

    return {
        "layout": "Dy::SolverContactHeader/Point/Friction",
        "ptr": window.get("ptr"),
        "rawByteLength": len(raw),
        "header": header,
        "normalRows": normal_rows,
        "appliedNormalForces": applied_normal_forces,
        "frictionRows": friction_rows,
        "decodedBytes": cursor,
    }


def decode_extra_dump_constraints(event: dict[str, Any]) -> list[dict[str, Any]]:
    data = event.get("data") or {}
    extras = data.get("extraDumps")
    if not isinstance(extras, list):
        return []
    rows: list[dict[str, Any]] = []
    for extra in extras:
        if not isinstance(extra, dict):
            continue
        for desc in extra.get("solverConstraintDescs") or []:
            if not isinstance(desc, dict):
                continue
            window = desc.get("constraintWindow")
            writeback_window = desc.get("writeBackWindow")
            body_a_window = desc.get("bodyAWindow")
            body_b_window = desc.get("bodyBWindow")
            decoded = decode_solver_contact_block(window)
            rows.append(
                {
                    "extraLabel": extra.get("label"),
                    "index": desc.get("index"),
                    "desc": desc.get("desc"),
                    "constraintWindowPresent": isinstance(window, dict),
                    "constraintRawBytesAvailable": isinstance(window, dict) and bool(window.get("rawBytes")),
                    "constraintWindow": window,
                    "decodedConstraint": decoded,
                    "writeBackWindowPresent": isinstance(writeback_window, dict),
                    "writeBackRawBytesAvailable": isinstance(writeback_window, dict)
                    and bool(writeback_window.get("rawBytes")),
                    "writeBackWindow": writeback_window,
                    "decodedWriteBackF32": decode_f32_array(writeback_window),
                    "bodyAWindowPresent": isinstance(body_a_window, dict),
                    "bodyARawBytesAvailable": isinstance(body_a_window, dict)
                    and bool(body_a_window.get("rawBytes")),
                    "bodyAWindow": body_a_window,
                    "bodyAF32Preview": (body_a_window or {}).get("f32Preview")
                    if isinstance(body_a_window, dict)
                    else None,
                    "bodyAU32Preview": (body_a_window or {}).get("u32Preview")
                    if isinstance(body_a_window, dict)
                    else None,
                    "bodyBWindowPresent": isinstance(body_b_window, dict),
                    "bodyBRawBytesAvailable": isinstance(body_b_window, dict)
                    and bool(body_b_window.get("rawBytes")),
                    "bodyBWindow": body_b_window,
                    "bodyBF32Preview": (body_b_window or {}).get("f32Preview")
                    if isinstance(body_b_window, dict)
                    else None,
                    "bodyBU32Preview": (body_b_window or {}).get("u32Preview")
                    if isinstance(body_b_window, dict)
                    else None,
                }
            )
    return rows


def first_decoded_constraint(constraints: list[dict[str, Any]]) -> dict[str, Any] | None:
    for row in constraints:
        decoded = row.get("decodedConstraint") if isinstance(row, dict) else None
        if isinstance(decoded, dict) and decoded.get("normalRows"):
            return decoded
    return None


def vector_delta(a: Any, b: Any) -> list[float | None] | None:
    if not (usable_vec3(a) and usable_vec3(b)):
        return None
    return [float(a[i]) - float(b[i]) for i in range(3)]


def scalar_delta(a: Any, b: Any) -> float | None:
    if not (finite_float(a) and finite_float(b)):
        return None
    return float(a) - float(b)


def compare_raw_and_computed_rows(
    contact: dict[str, Any] | None,
    computed_rows: list[dict[str, Any]],
    solver_descs: list[dict[str, Any]],
    extra_constraints: list[dict[str, Any]],
) -> dict[str, Any] | None:
    decoded = first_decoded_constraint(extra_constraints) or first_decoded_constraint(solver_descs)
    if not isinstance(decoded, dict):
        return None
    raw_rows = decoded.get("normalRows")
    if not isinstance(raw_rows, list) or not raw_rows or not computed_rows:
        return None
    raw_row = raw_rows[0]
    computed = computed_rows[0]
    header = decoded.get("header") if isinstance(decoded.get("header"), dict) else {}
    normal = contact.get("normal") if isinstance(contact, dict) else None
    return {
        "source": "Unity raw SolverContact block minus locally reconstructed row",
        "headerNormalMinusContactNormal": vector_delta(header.get("normal"), normal),
        "normalRow0": {
            "raXnDelta": vector_delta(raw_row.get("raXn"), computed.get("raXn")),
            "rbXnDelta": vector_delta(raw_row.get("rbXn"), computed.get("rbXn")),
            "velMultiplierDelta": scalar_delta(
                raw_row.get("velMultiplier"), computed.get("velMultiplier")
            ),
            "biasedErrDelta": scalar_delta(raw_row.get("biasedErr"), computed.get("biasedErr")),
            "unbiasedErrDelta": scalar_delta(
                raw_row.get("unbiasedErr"), computed.get("unbiasedErr")
            ),
            "maxImpulseDelta": scalar_delta(raw_row.get("maxImpulse"), computed.get("maxImpulse")),
        },
        "rawHeader": header,
        "rawAppliedNormalForces": decoded.get("appliedNormalForces"),
    }


SOLVER_CONSUME_HOOKS = {
    "solveContactBlock",
    "solveContact_BStaticBlock",
    "solveContact4Block",
    "solveContact4StaticBlock",
    "solveContactBlockWithWriteback",
    "solveContact_BStaticBlockWithWriteback",
    "solveContact4BlockWithWriteback",
    "solveContact4StaticBlockWithWriteback",
    "solveContactConcludeBlock",
    "solveContact_BStaticConcludeBlock",
    "solveContact4ConcludeBlock",
    "solveContact4StaticConcludeBlock",
}

PCM_CONTACT_HOOKS = {
    "PxcPCMContactConvexConvex",
    "PxcPCMContactConvexMesh",
}

WITH_WRITEBACK_HOOKS = {
    "solveContactBlockWithWriteback",
    "solveContact_BStaticBlockWithWriteback",
    "solveContact4BlockWithWriteback",
    "solveContact4StaticBlockWithWriteback",
}


def summarize_solver_consume_constraints(constraints: list[dict[str, Any]]) -> dict[str, Any]:
    decoded = first_decoded_constraint(constraints)
    header = decoded.get("header") if isinstance(decoded, dict) else None
    normal_rows = decoded.get("normalRows") if isinstance(decoded, dict) else None
    friction_rows = decoded.get("frictionRows") if isinstance(decoded, dict) else None
    return {
        "constraintCount": len(constraints),
        "rawConstraintCount": sum(1 for row in constraints if row.get("constraintRawBytesAvailable")),
        "bodyWindowCount": sum(
            1
            for row in constraints
            if row.get("bodyAWindowPresent") or row.get("bodyBWindowPresent")
        ),
        "firstHeader": header,
        "firstNormalRows": normal_rows[:4] if isinstance(normal_rows, list) else None,
        "firstFrictionRows": friction_rows[:4] if isinstance(friction_rows, list) else None,
    }


def build_capture_readiness(
    rows: list[dict[str, Any]],
    solver_consume_rows: list[dict[str, Any]],
    pcm_contact_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    stone_stone = [row for row in rows if row.get("pairClass") == "stone_stone"]
    stone_stone_after = [row for row in stone_stone if row.get("phase") == "after"]
    with_writeback = [row for row in solver_consume_rows if row.get("hook") in WITH_WRITEBACK_HOOKS]
    pcm_convex = [row for row in pcm_contact_rows if row.get("hook") == "PxcPCMContactConvexConvex"]
    pcm_convex_after = [row for row in pcm_convex if row.get("phase") == "after"]

    def has_extra_presence(row: dict[str, Any], key: str) -> bool:
        presence = row.get("exactExtraDumpPresence")
        return isinstance(presence, dict) and bool(presence.get(key))

    def has_constraint_raw(row: dict[str, Any]) -> bool:
        for dump in row.get("extraConstraintDumps") or []:
            if isinstance(dump, dict) and dump.get("constraintRawBytesAvailable"):
                return True
        return False

    def has_body_windows(row: dict[str, Any]) -> bool:
        for dump in row.get("extraConstraintDumps") or []:
            if not isinstance(dump, dict):
                continue
            if dump.get("bodyAWindowPresent") or dump.get("bodyBWindowPresent"):
                return True
        return False

    with_writeback_by_hook: dict[str, dict[str, int]] = {}
    for row in with_writeback:
        hook = str(row.get("hook"))
        bucket = with_writeback_by_hook.setdefault(
            hook,
            {
                "before": 0,
                "after": 0,
                "withConstraintRaw": 0,
                "withBodyWindows": 0,
                "withWriteBackWindow": 0,
            },
        )
        phase = str(row.get("phase"))
        if phase in {"before", "after"}:
            bucket[phase] += 1
        if has_constraint_raw(row):
            bucket["withConstraintRaw"] += 1
        if has_body_windows(row):
            bucket["withBodyWindows"] += 1
        for dump in row.get("extraConstraintDumps") or []:
            if isinstance(dump, dict) and dump.get("writeBackWindowPresent"):
                bucket["withWriteBackWindow"] += 1
                break

    return {
        "target": (
            "Runtime-native state for same-shot comparison: ContactBuffer/FrictionPatch/"
            "PxSolverBodyData at finalizer plus with-writeback pre/post body windows."
        ),
        "stoneStoneFinalizerAfterCount": len(stone_stone_after),
        "stoneStoneHasContactBufferWindow": any(
            has_extra_presence(row, "contactBufferWindow") for row in stone_stone_after
        ),
        "stoneStoneHasFrictionWindow": any(
            has_extra_presence(row, "frictionWindow") for row in stone_stone_after
        ),
        "stoneStoneHasBodyDataWindows": any(
            has_extra_presence(row, "data0Window") and has_extra_presence(row, "data1Window")
            for row in stone_stone_after
        ),
        "stoneStoneHasShapeInteractionWindow": any(
            has_extra_presence(row, "shapeInteractionWindow") for row in stone_stone_after
        ),
        "stoneStoneHasRawSolverRows": any(has_constraint_raw(row) for row in stone_stone_after),
        "pcmConvexConvexPairCount": len(pcm_convex),
        "pcmConvexConvexAfterCount": len(pcm_convex_after),
        "pcmConvexConvexHasGeometryAndTransforms": any(
            bool(((row.get("pcmInputs") or {}).get("shape0") or {}).get("decoded"))
            and bool(((row.get("pcmInputs") or {}).get("shape1") or {}).get("decoded"))
            and bool((row.get("pcmInputs") or {}).get("transform0"))
            and bool((row.get("pcmInputs") or {}).get("transform1"))
            for row in pcm_convex
        ),
        "pcmConvexConvexHasCacheManifoldWindow": any(
            bool((((row.get("pcmInputs") or {}).get("cache") or {}).get("manifoldWindowPresent")))
            for row in pcm_convex
        ),
        "pcmConvexConvexHasContactBufferAfter": any(
            isinstance(((row.get("pcmInputs") or {}).get("contactBuffer") or {}).get("candidate"), dict)
            for row in pcm_convex_after
        ),
        "withWritebackPairCount": len(with_writeback),
        "withWritebackByHook": dict(sorted(with_writeback_by_hook.items())),
        "withWritebackHasBodyWindows": any(has_body_windows(row) for row in with_writeback),
        "withWritebackHasRawSolverRows": any(has_constraint_raw(row) for row in with_writeback),
        "readyForFieldDiff": (
            bool(stone_stone_after)
            and any(has_extra_presence(row, "contactBufferWindow") for row in stone_stone_after)
            and any(has_extra_presence(row, "frictionWindow") for row in stone_stone_after)
            and any(
                has_extra_presence(row, "data0Window") and has_extra_presence(row, "data1Window")
                for row in stone_stone_after
            )
            and any(has_constraint_raw(row) for row in stone_stone_after)
            and bool(with_writeback)
            and any(has_body_windows(row) for row in with_writeback)
        ),
        "readyForContactGenerationDiff": (
            bool(pcm_convex)
            and any(
                bool(((row.get("pcmInputs") or {}).get("shape0") or {}).get("decoded"))
                and bool(((row.get("pcmInputs") or {}).get("shape1") or {}).get("decoded"))
                and bool((row.get("pcmInputs") or {}).get("transform0"))
                and bool((row.get("pcmInputs") or {}).get("transform1"))
                and bool((row.get("pcmInputs") or {}).get("narrowPhaseParams"))
                and bool((row.get("pcmInputs") or {}).get("cache"))
                for row in pcm_convex
            )
        ),
        "missingIfFalse": [
            "stone-stone createFinalizeSolverContacts.after with exact contactBufferWindow/frictionWindow/data0Window/data1Window",
            "stone-stone raw SolverContactHeader/Point/Friction block",
            "solveContact*WithWriteback before/after rows with bodyA/bodyB windows",
            "PxcPCMContactConvexConvex before/after with shape GeometryUnion, transforms, NarrowPhaseParams, cache/manifold, and ContactBuffer",
        ],
    }


def extract(payload: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    solver_consume_rows: list[dict[str, Any]] = []
    pcm_contact_rows: list[dict[str, Any]] = []
    class_counts: Counter[str] = Counter()
    solver_consume_counts: Counter[str] = Counter()
    pcm_contact_counts: Counter[str] = Counter()
    constraint_presence: Counter[str] = Counter()

    for event in payload.get("events", []):
        if event.get("type") not in {"physx.native.before", "physx.native.after"}:
            continue
        data = event.get("data") or {}
        hook = str((data.get("hook") or {}).get("name") or "unknown")
        if hook in PCM_CONTACT_HOOKS:
            pcm_inputs = summarize_pcm_extra(event)
            pcm_contact_counts[f"{hook}.{data.get('phase')}"] += 1
            pair_class = (
                (((pcm_inputs or {}).get("contactBuffer") or {}).get("pairClass"))
                if isinstance(pcm_inputs, dict)
                else "no_contact"
            )
            pcm_contact_rows.append(
                {
                    "t": event.get("t"),
                    "phase": data.get("phase"),
                    "hook": hook,
                    "callIndex": data.get("callIndex"),
                    "dumpIndex": data.get("dumpIndex"),
                    "dumpId": data.get("dumpId"),
                    "armSerial": data.get("armSerial"),
                    "args": data.get("args"),
                    "pairClass": pair_class,
                    "pcmInputs": pcm_inputs,
                }
            )
            continue
        if hook in SOLVER_CONSUME_HOOKS:
            extra_constraints = decode_extra_dump_constraints(event)
            solver_consume_counts[f"{hook}.{data.get('phase')}"] += 1
            solver_consume_rows.append(
                {
                    "t": event.get("t"),
                    "phase": data.get("phase"),
                    "hook": hook,
                    "callIndex": data.get("callIndex"),
                    "dumpIndex": data.get("dumpIndex"),
                    "dumpId": data.get("dumpId"),
                    "armSerial": data.get("armSerial"),
                    "args": data.get("args"),
                    "summary": summarize_solver_consume_constraints(extra_constraints),
                    "extraConstraintDumps": extra_constraints,
                }
            )
            continue
        if hook != "createFinalizeSolverContacts":
            continue

        arg0 = find_top_arg(data.get("pointerWindows"), 0)
        if not arg0:
            continue
        extra = first_extra_contact_desc(event)
        contact_child = find_direct_child(arg0, CONTACT_DESC_OFFSETS["contactsPtr"])
        friction_child = find_direct_child(arg0, CONTACT_DESC_OFFSETS["frictionPtr"])
        solver_desc_child = find_direct_child(arg0, CONTACT_DESC_OFFSETS["descPtr"])
        data0_child = find_direct_child(arg0, CONTACT_DESC_OFFSETS["data0"])
        data1_child = find_direct_child(arg0, CONTACT_DESC_OFFSETS["data1"])
        contact_window = extra_window(extra, "contactBufferWindow") or contact_child
        friction_window = extra_window(extra, "frictionWindow") or friction_child
        data0_window = extra_window(extra, "data0Window") or data0_child
        data1_window = extra_window(extra, "data1Window") or data1_child
        contact_candidate = contact_child.get("contactBufferCandidate") if isinstance(contact_child, dict) else None
        if not isinstance(contact_candidate, dict) and isinstance(contact_window, dict):
            contact_candidate = contact_window.get("contactBufferCandidate")
        contact = first_contact(contact_candidate)
        pair_class = classify_contact(contact)
        desc = decode_contact_desc(arg0)
        body_data = {
            "data0": decode_solver_body_data(data0_window),
            "data1": decode_solver_body_data(data1_window),
        }
        solver_descs = decode_solver_constraint_descs(solver_desc_child, event)
        extra_constraints = decode_extra_dump_constraints(event)
        computed_rows = compute_normal_rows(
            contact_candidate,
            desc,
            body_data,
            data.get("args") or [],
        )
        has_constraint_raw = any(row.get("constraintRawBytesAvailable") for row in solver_descs) or any(
            row.get("constraintRawBytesAvailable") for row in extra_constraints
        )
        constraint_presence["raw_available" if has_constraint_raw else "pointer_only"] += 1
        class_counts[pair_class] += 1
        rows.append(
            {
                "t": event.get("t"),
                "phase": data.get("phase"),
                "hook": hook,
                "pairClass": pair_class,
                "contactDesc": desc,
                "contactBuffer": {
                    "ptr": contact_window.get("ptr") if isinstance(contact_window, dict) else None,
                    "sourceOffset": CONTACT_DESC_OFFSETS["contactsPtr"],
                    "candidate": contact_candidate,
                    "firstContact": contact,
                    "rawBytesAvailable": isinstance(contact_window, dict) and bool(contact_window.get("rawBytes")),
                },
                "frictionPatch": decode_friction_patch(friction_window),
                "solverBodyData": body_data,
                "computedNormalRows": computed_rows,
                "solverConstraintDescs": solver_descs,
                "extraConstraintDumps": extra_constraints,
                "rawVsComputedNormalRow": compare_raw_and_computed_rows(
                    contact,
                    computed_rows,
                    solver_descs,
                    extra_constraints,
                ),
                "exactExtraDumpPresence": {
                    "contactBufferWindow": isinstance(extra_window(extra, "contactBufferWindow"), dict),
                    "frictionWindow": isinstance(extra_window(extra, "frictionWindow"), dict),
                    "data0Window": isinstance(extra_window(extra, "data0Window"), dict),
                    "data1Window": isinstance(extra_window(extra, "data1Window"), dict),
                    "shapeInteractionWindow": isinstance(
                        extra_window(extra, "shapeInteractionWindow"), dict
                    ),
                    "solverConstraintDescCount": len(extra.get("solverConstraintDescs") or [])
                    if isinstance(extra, dict)
                    else 0,
                },
            }
        )

    stone_stone = [row for row in rows if row.get("pairClass") == "stone_stone"]
    return {
        "sourceEventCount": len(payload.get("events", [])),
        "rowCount": len(rows),
        "classCounts": dict(sorted(class_counts.items())),
        "constraintCapture": dict(sorted(constraint_presence.items())),
        "solverConsumeCounts": dict(sorted(solver_consume_counts.items())),
        "pcmContactCounts": dict(sorted(pcm_contact_counts.items())),
        "pcmContactRows": pcm_contact_rows,
        "solverConsumeRows": solver_consume_rows,
        "captureReadiness": build_capture_readiness(rows, solver_consume_rows, pcm_contact_rows),
        "currentCaptureLimitation": (
            "Raw SolverContactHeader/Point/Friction bytes and body windows are available only "
            "for events whose probe payload contains exact extraDumps.  Use captureReadiness "
            "to decide whether a run is sufficient for field-level Unity-vs-pyphysx diff."
        ),
        "firstStoneStone": stone_stone[0] if stone_stone else None,
        "stoneStoneRows": stone_stone,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.input.suffix.lower() == ".jsonl":
        events = [
            json.loads(line)
            for line in args.input.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        payload = {"events": events}
    else:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    report = extract(payload)
    output = args.output or args.input.with_suffix(".solver_state.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "rowCount": report["rowCount"],
                "classCounts": report["classCounts"],
                "constraintCapture": report["constraintCapture"],
                "solverConsumeCounts": report.get("solverConsumeCounts"),
                "pcmContactCounts": report.get("pcmContactCounts"),
                "captureReadiness": report.get("captureReadiness"),
                "firstPcmConvexConvex": next(
                    (
                        {
                            "t": row.get("t"),
                            "phase": row.get("phase"),
                            "pairClass": row.get("pairClass"),
                            "narrowPhaseParams": ((row.get("pcmInputs") or {}).get("narrowPhaseParams")),
                            "cache": (((row.get("pcmInputs") or {}).get("cache") or {}).get("decoded")),
                            "contactCount": (
                                ((((row.get("pcmInputs") or {}).get("contactBuffer") or {}).get("candidate") or {}).get("count"))
                            ),
                        }
                        for row in report.get("pcmContactRows", [])
                        if row.get("hook") == "PxcPCMContactConvexConvex"
                    ),
                    None,
                ),
                "firstStoneStone": {
                    "t": (report.get("firstStoneStone") or {}).get("t"),
                    "phase": (report.get("firstStoneStone") or {}).get("phase"),
                    "contactDesc": (report.get("firstStoneStone") or {}).get("contactDesc"),
                    "frictionPatch": (report.get("firstStoneStone") or {}).get("frictionPatch"),
                    "bodyFrame0": ((report.get("firstStoneStone") or {}).get("contactDesc") or {}).get(
                        "bodyFrame0"
                    ),
                    "bodyFrame1": ((report.get("firstStoneStone") or {}).get("contactDesc") or {}).get(
                        "bodyFrame1"
                    ),
                    "solverBodyData": (report.get("firstStoneStone") or {}).get("solverBodyData"),
                    "computedNormalRows": (report.get("firstStoneStone") or {}).get("computedNormalRows"),
                    "solverConstraintDescs": (report.get("firstStoneStone") or {}).get(
                        "solverConstraintDescs"
                    ),
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
