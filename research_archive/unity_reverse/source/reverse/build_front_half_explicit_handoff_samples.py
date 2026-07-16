#!/usr/bin/env python3
"""Build collision probe samples that start from captured Unity first-contact state."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_samples_20260710_012534.jsonl"
DEFAULT_TRUTH = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_entrance_truth_20260710.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "front_half_explicit_handoff_samples_20260710.jsonl"
DEFAULT_GRAVITY_STEP_VZ = -0.0981


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


def _float_or_none(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) else None


def _float_or_default(value: Any, default: float) -> float:
    parsed = _float_or_none(value)
    return default if parsed is None else parsed


def _velocity_from_truth(row: dict[str, Any]) -> tuple[dict[str, Any], str]:
    native = row.get("native_solver_velocity")
    if isinstance(native, dict):
        active = native.get("active") if isinstance(native.get("active"), dict) else native
        vx = _float_or_none(active.get("vx"))
        vy = _float_or_none(active.get("vy"))
        w = _float_or_none(active.get("w"))
        if vx is not None and vy is not None and w is not None:
            return {
                "vx": vx,
                "vy": vy,
                "vz": _float_or_default(active.get("vz"), DEFAULT_GRAVITY_STEP_VZ),
                "wx": _float_or_default(active.get("wx"), 0.0),
                "wy": _float_or_default(active.get("wy"), 0.0),
                "w": w,
            }, "unity_native_solver_body"

    local_velocity = ((row.get("local_front_half_replay") or {}).get("velocity") or {})
    vx = _float_or_none(local_velocity.get("vx"))
    vy = _float_or_none(local_velocity.get("vy"))
    w = _float_or_none(local_velocity.get("w"))
    if vx is None or vy is None or w is None:
        local_state = ((row.get("local_front_half_replay") or {}).get("state") or {})
        vx = _float_or_none(local_state.get("vx"))
        vy = _float_or_none(local_state.get("vy"))
        w = _float_or_none(local_state.get("w"))
    if vx is None or vy is None or w is None:
        raise ValueError(f"row {row.get('seq')} lacks usable entrance velocity")
    return {
        "vx": vx,
        "vy": vy,
        "vz": DEFAULT_GRAVITY_STEP_VZ,
        "wx": 0.0,
        "wy": 0.0,
        "w": w,
    }, "local_random_range_replay_fallback"


def _local_velocity_from_truth(row: dict[str, Any]) -> tuple[dict[str, Any], str]:
    local_velocity = ((row.get("local_front_half_replay") or {}).get("velocity") or {})
    vx = _float_or_none(local_velocity.get("vx"))
    vy = _float_or_none(local_velocity.get("vy"))
    w = _float_or_none(local_velocity.get("w"))
    if vx is None or vy is None or w is None:
        local_state = ((row.get("local_front_half_replay") or {}).get("state") or {})
        vx = _float_or_none(local_state.get("vx"))
        vy = _float_or_none(local_state.get("vy"))
        w = _float_or_none(local_state.get("w"))
    if vx is None or vy is None or w is None:
        raise ValueError(f"row {row.get('seq')} lacks usable local entrance velocity")
    return {
        "vx": vx,
        "vy": vy,
        "vz": DEFAULT_GRAVITY_STEP_VZ,
        "wx": 0.0,
        "wy": 0.0,
        "w": w,
    }, "local_random_range_replay_forced"


def _target_velocity_from_truth(row: dict[str, Any]) -> tuple[dict[str, Any], str]:
    native = row.get("native_solver_velocity")
    if isinstance(native, dict) and isinstance(native.get("target"), dict):
        target = native["target"]
        vx = _float_or_none(target.get("vx"))
        vy = _float_or_none(target.get("vy"))
        w = _float_or_none(target.get("w"))
        if vx is not None and vy is not None and w is not None:
            return {
                "vx": vx,
                "vy": vy,
                "vz": _float_or_default(target.get("vz"), DEFAULT_GRAVITY_STEP_VZ),
                "wx": _float_or_default(target.get("wx"), 0.0),
                "wy": _float_or_default(target.get("wy"), 0.0),
                "w": w,
            }, "unity_native_solver_body"
    return {
        "vx": 0.0,
        "vy": 0.0,
        "vz": DEFAULT_GRAVITY_STEP_VZ,
        "wx": 0.0,
        "wy": 0.0,
        "w": 0.0,
    }, "gravity_step_fallback"


def build_samples(
    source_samples: list[dict[str, Any]],
    truth: dict[str, Any],
    *,
    velocity_mode: str,
) -> list[dict[str, Any]]:
    source_by_id = {int(sample["sample_id"]): sample for sample in source_samples}
    out: list[dict[str, Any]] = []
    for row in truth.get("rows") or []:
        sample_id = int(row["sample_id"])
        sample = copy.deepcopy(source_by_id[sample_id])
        sample["source_category"] = sample.get("category")
        sample["category"] = "collision_front_half_explicit_handoff"
        unity_state = row.get("unity_entrance_state") or {}
        active = unity_state.get("active") or {}
        target = unity_state.get("target") or {}
        local_state = ((row.get("local_front_half_replay") or {}).get("state") or {})
        if velocity_mode == "local":
            velocity, velocity_source = _local_velocity_from_truth(row)
            target_velocity, target_velocity_source = _target_velocity_from_truth({})
        else:
            velocity, velocity_source = _velocity_from_truth(row)
            target_velocity, target_velocity_source = _target_velocity_from_truth(row)

        active_yaw = float(active.get("yaw") or 0.0)
        target_yaw = float(target.get("yaw") or 0.0)
        first_contact = row.get("first_contact_pcm") or {}
        sample["handoff_state"] = {
            "source": "unity_first_contact_pcm_entrance",
            "velocity_source": velocity_source,
            "step": int(local_state.get("steps") or -1),
            "x": float(active["x"]),
            "y": float(active["y"]),
            "vx": velocity["vx"],
            "vy": velocity["vy"],
            "vz": velocity["vz"],
            "wx": velocity["wx"],
            "wy": velocity["wy"],
            "w": velocity["w"],
            "yaw": active_yaw,
            "distance": _float_or_none(first_contact.get("unity_center_distance_m")) or 0.0,
            "threshold": 0.0,
        }
        sample["target_handoff_state"] = {
            "source": "unity_first_contact_pcm_entrance",
            "velocity_source": target_velocity_source,
            "vx": target_velocity["vx"],
            "vy": target_velocity["vy"],
            "vz": target_velocity["vz"],
            "wx": target_velocity["wx"],
            "wy": target_velocity["wy"],
            "w": target_velocity["w"],
        }
        sample["active_yaw"] = active_yaw
        sample["target_yaw"] = target_yaw
        sample["unity_first_contact_entrance"] = {
            "truth_schema": truth.get("schema"),
            "seq": row.get("seq"),
            "active": active,
            "target": target,
            "first_contact_pcm": first_contact,
            "local_front_half_position_error_m": (
                (row.get("local_front_half_replay") or {}).get("position_error_vs_unity_m")
            ),
            "native_solver_velocity": row.get("native_solver_velocity"),
            "velocity_source": velocity_source,
            "target_velocity_source": target_velocity_source,
        }
        notes = sample.get("notes")
        suffix = "Explicit handoff sample starts from captured Unity first-contact PCM entrance."
        sample["notes"] = f"{notes} {suffix}" if isinstance(notes, str) and notes else suffix
        out.append(sample)
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--truth", type=Path, default=DEFAULT_TRUTH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--velocity-mode",
        choices=("native-with-local-fallback", "local"),
        default="native-with-local-fallback",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_samples = read_jsonl(args.samples)
    truth = json.loads(args.truth.read_text(encoding="utf-8"))
    rows = build_samples(source_samples, truth, velocity_mode=args.velocity_mode)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "row_count": len(rows),
                "native_velocity_rows": sum(
                    1
                    for row in rows
                    if (row.get("handoff_state") or {}).get("velocity_source")
                    == "unity_native_solver_body"
                ),
                "fallback_velocity_rows": sum(
                    1
                    for row in rows
                    if (row.get("handoff_state") or {}).get("velocity_source")
                    == "local_random_range_replay_fallback"
                ),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
