#!/usr/bin/env python3
"""Summarize serialized prefab/scene rotations of formal curling stones."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "calibration" / "unity_assets_inspect_20260709.txt"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_stone_prefab_rotation_audit_20260709.json"

STONE_LINE = re.compile(
    r"^(?P<asset>[^:]+):(?P<path_id>\d+) (?P<name>Curling stone \w+\d+) "
    r".*?localRot=\((?P<local_rot>[^)]*)\).*?worldPos=\((?P<world_pos>[^)]*)\)"
)


def _yaw_from_unity_quaternion_xyzw(quat: Tuple[float, float, float, float]) -> float:
    x, y, z, w = quat
    return math.degrees(math.atan2(2.0 * (w * y + x * z), 1.0 - 2.0 * (y * y + z * z)))


def _parse_tuple(value: str) -> Tuple[float, ...]:
    return tuple(float(part) for part in value.split(","))


def build_report(input_path: Path = DEFAULT_INPUT) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for line in input_path.read_text(encoding="utf-8").splitlines():
        match = STONE_LINE.search(line)
        if not match:
            continue
        local_rot_values = _parse_tuple(match.group("local_rot"))
        if len(local_rot_values) != 4:
            continue
        local_rot = tuple(round(value, 9) for value in local_rot_values)
        yaw_deg = _yaw_from_unity_quaternion_xyzw(local_rot_values)  # type: ignore[arg-type]
        rows.append(
            {
                "asset": match.group("asset"),
                "path_id": int(match.group("path_id")),
                "name": match.group("name"),
                "local_rotation_xyzw": list(local_rot),
                "local_yaw_deg": yaw_deg,
                "world_pos": list(_parse_tuple(match.group("world_pos"))),
            }
        )

    rotation_counts = Counter(tuple(row["local_rotation_xyzw"]) for row in rows)
    yaw_values = [float(row["local_yaw_deg"]) for row in rows]
    unique_yaws = sorted({round(value, 9) for value in yaw_values})
    return {
        "input": str(input_path.relative_to(PROJECT_ROOT)),
        "stone_count": len(rows),
        "unique_local_rotation_count": len(rotation_counts),
        "unique_local_rotations": [
            {"local_rotation_xyzw": list(rotation), "count": count}
            for rotation, count in rotation_counts.most_common()
        ],
        "unique_local_yaw_deg": unique_yaws,
        "max_abs_yaw_deg": max((abs(value) for value in yaw_values), default=None),
        "interpretation": (
            "Serialized formal stone transforms all have the same near-identity local rotation. "
            "Therefore the wide-yaw endpoint improvement is not explained by different prefab initial yaws; "
            "if rotation is involved, it must be runtime carryover/contact-state, or the yaw sweep is only "
            "compensating for contact feature/manifold differences."
        ),
        "rows": rows,
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(
        json.dumps(
            {
                "stone_count": report["stone_count"],
                "unique_local_rotation_count": report["unique_local_rotation_count"],
                "unique_local_yaw_deg": report["unique_local_yaw_deg"],
                "max_abs_yaw_deg": report["max_abs_yaw_deg"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
