#!/usr/bin/env python3
"""Identify the quaternion basis used by Unity's native angular-velocity setter.

The A11 hook records plausible PxTransform windows inside the native setter
bridge. This audit applies PhysX's float32 PxQuat::rotate formula to each
window and compares its result with the bridge vector written by the setter.
"""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path
from typing import Any


def f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


def rotate_y(q: list[float], angular_y: float) -> list[float]:
    x, y, z, w = (f32(value) for value in q)
    vx, vy, vz = f32(0.0), f32(2.0 * f32(angular_y)), f32(0.0)
    w2 = f32(f32(w * w) - f32(0.5))
    dot2 = f32(f32(f32(x * vx) + f32(y * vy)) + f32(z * vz))
    return [
        f32(f32(f32(vx * w2) + f32(f32(y * vz) - f32(z * vy)) * w) + f32(x * dot2)),
        f32(f32(f32(vy * w2) + f32(f32(z * vx) - f32(x * vz)) * w) + f32(y * dot2)),
        f32(f32(f32(vz * w2) + f32(f32(x * vy) - f32(y * vx)) * w) + f32(z * dot2)),
    ]


def max_abs_delta(left: list[float], right: list[float]) -> float:
    return max(abs(float(a) - float(b)) for a, b in zip(left, right))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    for line in args.events.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("type") != "a9.angular_setter_native_delta":
            continue
        data = event["data"]
        bridge = (data.get("bridgeAfterSetter") or [])
        candidates_by_bridge = data.get("bridgeTransformCandidatesBefore") or []
        if not bridge or not candidates_by_bridge:
            continue

        bridge_xyz = bridge[0].get("xyz")
        setter_wy = data.get("setterWy")
        if not isinstance(bridge_xyz, list) or len(bridge_xyz) != 3 or not isinstance(setter_wy, (int, float)):
            continue

        matches: list[dict[str, Any]] = []
        for group in candidates_by_bridge:
            for candidate in group.get("candidates") or []:
                transform = candidate.get("transform") or {}
                q = transform.get("q")
                if not isinstance(q, list) or len(q) != 4:
                    continue
                rotated = rotate_y(q, float(setter_wy))
                matches.append(
                    {
                        "bridge_ptr": group.get("ptr"),
                        "bridge_y_offset": group.get("yOffset"),
                        "transform_offset": candidate.get("offset"),
                        "q": q,
                        "p": transform.get("p"),
                        "rotated_xyz": rotated,
                        "max_abs_delta": max_abs_delta(rotated, bridge_xyz),
                    }
                )
        matches.sort(key=lambda row: row["max_abs_delta"])
        rows.append(
            {
                "tick_serial": data.get("tickSerial"),
                "setter_wy": setter_wy,
                "bridge_xyz": bridge_xyz,
                "best_candidates": matches[:5],
            }
        )

    exact_rows = [row for row in rows if row["best_candidates"] and row["best_candidates"][0]["max_abs_delta"] == 0.0]
    result = {
        "events": str(args.events),
        "window_count": len(rows),
        "acceptance": {
            "bridge_transform_candidates_observed": bool(rows),
            "exact_physx_rotation_basis_found": bool(exact_rows),
            "exact_basis_every_observed_tick": bool(rows) and len(exact_rows) == len(rows),
        },
        "rows": rows,
        "scope": (
            "An exact match identifies a native PxTransform candidate whose quaternion, passed through "
            "PhysX float32 PxQuat::rotate, reproduces the setter bridge vector. It does not yet prove "
            "which public/local body accessor exposes the same transform."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["acceptance"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
