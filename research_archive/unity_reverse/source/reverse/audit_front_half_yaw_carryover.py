#!/usr/bin/env python3
"""Audit hidden stone yaw carryover in the front-half PCM capture."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_samples_20260710_012534.jsonl"
DEFAULT_COMPARE = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_replay_compare_20260710.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "front_half_yaw_carryover_audit_20260710.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                item = json.loads(line)
                if isinstance(item, dict):
                    rows.append(item)
    return rows


def norm_angle(angle: float) -> float:
    value = float(angle)
    while value > math.pi:
        value -= 2.0 * math.pi
    while value <= -math.pi:
        value += 2.0 * math.pi
    return value


def angle_delta(a: float, b: float) -> float:
    return norm_angle(float(a) - float(b))


def _round_or_none(value: Any, digits: int = 9) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)


def build_audit(samples: list[dict[str, Any]], compare: dict[str, Any]) -> dict[str, Any]:
    compare_rows = compare.get("rows") or []
    rows: list[dict[str, Any]] = []
    stone_history: dict[str, list[dict[str, Any]]] = {}

    for seq, (sample, row) in enumerate(zip(samples, compare_rows)):
        active_index = int(sample.get("active_shot_num"))
        target_indices = [int(value) for value in sample.get("target_indices") or []]
        target_index = target_indices[0] if target_indices else None
        unity_active = row.get("unityActive") or {}
        unity_target = row.get("unityTarget") or {}
        best = row.get("bestPositionCandidate") or {}
        best_local = best.get("local") or {}
        best_error = best.get("error") or {}
        target_yaw = float(unity_target.get("yaw") or 0.0)
        active_yaw = float(unity_active.get("yaw") or 0.0)
        local_yaw = norm_angle(float(best_local.get("yaw") or 0.0))
        inferred_initial_yaw = norm_angle(float(row.get("inferredInitialYawOffset") or 0.0))

        item = {
            "seq": seq,
            "sample_id": sample.get("sample_id"),
            "label": sample.get("label"),
            "final_source": sample.get("final_source"),
            "active_index": active_index,
            "target_index": target_index,
            "unity_active_yaw_rad": active_yaw,
            "unity_target_yaw_rad": target_yaw,
            "unity_active_yaw_deg": math.degrees(active_yaw),
            "unity_target_yaw_deg": math.degrees(target_yaw),
            "local_integrated_yaw_from_zero_rad": local_yaw,
            "inferred_initial_yaw_offset_rad": inferred_initial_yaw,
            "position_error_m": best_error.get("positionError"),
            "contact_count": row.get("contactCount"),
            "reset_position_target_xy": (
                [
                    sample["reset_position"][2 * target_index],
                    sample["reset_position"][2 * target_index + 1],
                ]
                if target_index is not None
                else None
            ),
        }
        rows.append(item)

        stone_history.setdefault(str(active_index), []).append(
            {
                "seq": seq,
                "role": "active",
                "yaw_rad": active_yaw,
                "yaw_deg": math.degrees(active_yaw),
                "label": sample.get("label"),
            }
        )
        if target_index is not None:
            stone_history.setdefault(str(target_index), []).append(
                {
                    "seq": seq,
                    "role": "target",
                    "yaw_rad": target_yaw,
                    "yaw_deg": math.degrees(target_yaw),
                    "label": sample.get("label"),
                }
            )

    history_summary: dict[str, Any] = {}
    for stone_index, history in sorted(stone_history.items(), key=lambda item: int(item[0])):
        deltas = []
        for prev, cur in zip(history, history[1:]):
            deltas.append(
                {
                    "from_seq": prev["seq"],
                    "to_seq": cur["seq"],
                    "role_transition": f"{prev['role']}->{cur['role']}",
                    "delta_yaw_rad": angle_delta(cur["yaw_rad"], prev["yaw_rad"]),
                    "delta_yaw_deg": math.degrees(angle_delta(cur["yaw_rad"], prev["yaw_rad"])),
                }
            )
        history_summary[stone_index] = {
            "occurrence_count": len(history),
            "max_abs_yaw_rad": max(abs(float(item["yaw_rad"])) for item in history),
            "max_abs_yaw_deg": max(abs(float(item["yaw_deg"])) for item in history),
            "history": history,
            "between_occurrence_deltas": deltas,
        }

    target_hidden_rows = [
        row for row in rows if row["target_index"] is not None and abs(row["unity_target_yaw_rad"]) > 1e-4
    ]
    active_offset_rows = [
        row for row in rows if abs(row["inferred_initial_yaw_offset_rad"]) > 1e-4
    ]
    position_errors = [float(row["position_error_m"]) for row in rows if row.get("position_error_m") is not None]

    return {
        "schema": "front_half_yaw_carryover_audit_v1",
        "inputs": {
            "samples": str(DEFAULT_SAMPLES.relative_to(PROJECT_ROOT)),
            "compare": str(DEFAULT_COMPARE.relative_to(PROJECT_ROOT)),
        },
        "aggregate": {
            "row_count": len(rows),
            "position_rmse_m": (
                math.sqrt(sum(value * value for value in position_errors) / len(position_errors))
                if position_errors
                else None
            ),
            "position_max_error_m": max(position_errors) if position_errors else None,
            "target_hidden_yaw_row_count": len(target_hidden_rows),
            "active_initial_yaw_offset_row_count": len(active_offset_rows),
            "reset_position_does_not_reset_target_yaw": bool(target_hidden_rows),
            "stateless_reset_sample_replay_is_invalid": bool(target_hidden_rows or active_offset_rows),
            "main_interpretation": (
                "The front-half x/y replay is centimeter-level, but RESETPOSITION does not prove "
                "stone orientation reset. Hidden active/target yaw must be treated as part of the "
                "game state and passed into scene-style PCM/solver replay."
            ),
        },
        "rows": rows,
        "stone_history": history_summary,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--compare", type=Path, default=DEFAULT_COMPARE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    samples = read_jsonl(args.samples)
    compare = json.loads(args.compare.read_text(encoding="utf-8"))
    report = build_audit(samples, compare)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    compact_rows = [
        {
            "seq": row["seq"],
            "active_index": row["active_index"],
            "target_index": row["target_index"],
            "active_yaw_deg": _round_or_none(row["unity_active_yaw_deg"], 4),
            "target_yaw_deg": _round_or_none(row["unity_target_yaw_deg"], 4),
            "initial_yaw_offset_deg": _round_or_none(
                math.degrees(row["inferred_initial_yaw_offset_rad"]), 4
            ),
            "position_error_m": _round_or_none(row["position_error_m"], 5),
        }
        for row in report["rows"]
    ]
    print(
        json.dumps(
            {
                "output": str(args.output),
                "aggregate": report["aggregate"],
                "rows": compact_rows,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
