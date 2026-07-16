#!/usr/bin/env python3
"""Compare a Unity C05 PCM manifold with the role-reversed local PCM trace.

The WebGL C05 hook retains only a 256-byte window of the wasm
``LargePersistentContactManifold``.  That is sufficient for its 80-byte
header and up to three 48-byte contacts.  This tool deliberately compares
semantic world-space quantities instead of raw offsets: Unity's call order is
active->target, while the local persistent Scene presents target->active.

It is a read-only diagnostic.  In particular, a matching contact manifold
does not license a pose or cache-value compensation in the production scene.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path
from typing import Any, Sequence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unity-events", type=Path, required=True)
    parser.add_argument("--local-trace", type=Path, required=True)
    parser.add_argument("--c05-call-index", type=int, default=1)
    parser.add_argument("--local-pcm-index", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def f32s(raw: Sequence[int], offset: int, count: int) -> list[float]:
    return list(struct.unpack_from("<" + "f" * count, bytes(raw), offset))


def decode_manifold(raw: Sequence[int]) -> dict[str, Any]:
    if len(raw) < 80:
        raise ValueError(f"manifold raw window too short: {len(raw)}")
    count = int(raw[64])
    available = (len(raw) - 80) // 48
    if count > available:
        raise ValueError(f"manifold declares {count} contacts but window contains {available}")
    contacts = []
    for index in range(count):
        base = 80 + 48 * index
        contacts.append({
            "localPointA": f32s(raw, base, 3),
            "localPointB": f32s(raw, base + 16, 3),
            "localNormalPen": f32s(raw, base + 32, 4),
        })
    return {
        "rawBytes": len(raw),
        "relativeTransform": {"q": f32s(raw, 0, 4), "p": f32s(raw, 16, 3)},
        "quatA": f32s(raw, 32, 4),
        "quatB": f32s(raw, 48, 4),
        "numContacts": count,
        "capacity": int(raw[65]),
        "numWarmStartPoints": int(raw[66]),
        "aIndices": list(raw[67:71]),
        "bIndices": list(raw[71:75]),
        "contacts": contacts,
    }


def rotate(quaternion: Sequence[float], vector: Sequence[float]) -> list[float]:
    x, y, z, w = quaternion
    ux, uy, uz = (
        y * vector[2] - z * vector[1],
        z * vector[0] - x * vector[2],
        x * vector[1] - y * vector[0],
    )
    uux, uuy, uuz = (
        y * uz - z * uy,
        z * ux - x * uz,
        x * uy - y * ux,
    )
    return [
        vector[0] + 2.0 * (w * ux + uux),
        vector[1] + 2.0 * (w * uy + uuy),
        vector[2] + 2.0 * (w * uz + uuz),
    ]


def transform(transform_value: dict[str, Any], vector: Sequence[float]) -> list[float]:
    rotated = rotate(transform_value["q"], vector)
    return [float(transform_value["p"][i]) + rotated[i] for i in range(3)]


def max_abs_difference(left: Sequence[float], right: Sequence[float]) -> float:
    return max((abs(float(a) - float(b)) for a, b in zip(left, right)), default=0.0)


def load_events(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def compact_transform(transform_value: dict[str, Any]) -> dict[str, list[float]]:
    return {
        "p": [float(value) for value in transform_value["p"]],
        "q": [float(value) for value in transform_value["q"]],
    }


def main() -> int:
    args = parse_args()
    events = load_events(args.unity_events)
    c05_rows = [event["data"] for event in events if event.get("type") == "c05.persistent_pcm_call"]
    if not 0 <= args.c05_call_index < len(c05_rows):
        raise ValueError(f"C05 index {args.c05_call_index} outside {len(c05_rows)} calls")
    unity_row = c05_rows[args.c05_call_index]["after"]
    unity_raw = unity_row["manifold"]["rawBytes"]
    unity = decode_manifold(unity_raw)

    local_document = json.loads(args.local_trace.read_text(encoding="utf-8"))
    local_rows = local_document.get("postContactPcmTrace") or []
    if not 0 <= args.local_pcm_index < len(local_rows):
        raise ValueError(f"local PCM index {args.local_pcm_index} outside {len(local_rows)} rows")
    local_row = local_rows[args.local_pcm_index]
    local_raw = local_row["cache_after"]["manifold_raw"]
    local = decode_manifold(local_raw)

    # C05 uses (active=A, stationary=B); the local trace uses
    # (stationary=A, active=B).  A PersistentContact stores its normal in the
    # local B frame, hence the local normal must be rotated by its active pose
    # and sign-reversed to express Unity's active->stationary direction.
    unity_transform0 = compact_transform(unity_row["transform0"])
    unity_transform1 = compact_transform(unity_row["transform1"])
    local_transform0 = compact_transform(local_row["transform0"])
    local_transform1 = compact_transform(local_row["transform1"])
    rows = []
    for index, (unity_contact, local_contact) in enumerate(zip(unity["contacts"], local["contacts"])):
        unity_active_point = transform(unity_transform0, unity_contact["localPointA"])
        unity_stationary_point = transform(unity_transform1, unity_contact["localPointB"])
        local_active_point = transform(local_transform1, local_contact["localPointB"])
        local_stationary_point = transform(local_transform0, local_contact["localPointA"])
        unity_normal = rotate(unity_transform1["q"], unity_contact["localNormalPen"][:3])
        local_normal = [-value for value in rotate(local_transform1["q"], local_contact["localNormalPen"][:3])]
        rows.append({
            "contactIndex": index,
            "worldActivePointMaxAbsDifferenceM": max_abs_difference(unity_active_point, local_active_point),
            "worldStationaryPointMaxAbsDifferenceM": max_abs_difference(unity_stationary_point, local_stationary_point),
            "worldNormalMaxAbsDifference": max_abs_difference(unity_normal, local_normal),
            "penetrationAbsDifferenceM": abs(unity_contact["localNormalPen"][3] - local_contact["localNormalPen"][3]),
            "unity": {
                "activePoint": unity_active_point,
                "stationaryPoint": unity_stationary_point,
                "worldNormal": unity_normal,
                "penetration": unity_contact["localNormalPen"][3],
            },
            "localRoleReversed": {
                "activePoint": local_active_point,
                "stationaryPoint": local_stationary_point,
                "worldNormal": local_normal,
                "penetration": local_contact["localNormalPen"][3],
            },
        })

    report = {
        "schema": "c105_pcm_manifold_semantic_compare_v1",
        "scope": "read-only semantic comparison; no pose/cache values are fed back into the local simulation",
        "roleMapping": "Unity active->stationary versus local stationary->active",
        "unity": {
            "c05CallIndex": args.c05_call_index,
            "transform0Active": unity_transform0,
            "transform1Stationary": unity_transform1,
            "manifold": unity,
        },
        "local": {
            "pcmTraceIndex": args.local_pcm_index,
            "transform0Stationary": local_transform0,
            "transform1Active": local_transform1,
            "manifold": local,
        },
        "inputPoseMaxAbsDifferenceM": {
            "active": max_abs_difference(unity_transform0["p"], local_transform1["p"]),
            "stationary": max_abs_difference(unity_transform1["p"], local_transform0["p"]),
        },
        "inputQuaternionMaxAbsDifference": {
            "active": max_abs_difference(unity_transform0["q"], local_transform1["q"]),
            "stationary": max_abs_difference(unity_transform1["q"], local_transform0["q"]),
        },
        "contacts": rows,
        "interpretation": (
            "The world-space contact differences locate whether the first second-tick mismatch is already "
            "present in the consumed pose or is introduced by pair PCM.  They do not establish a production "
            "correction by themselves."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "contactCount": len(rows),
        "inputPoseMaxAbsDifferenceM": report["inputPoseMaxAbsDifferenceM"],
        "maxContactDifferenceM": max((max(row["worldActivePointMaxAbsDifferenceM"], row["worldStationaryPointMaxAbsDifferenceM"], row["penetrationAbsDifferenceM"]) for row in rows), default=0.0),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
