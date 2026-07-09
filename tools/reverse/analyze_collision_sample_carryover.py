#!/usr/bin/env python3
"""Analyze whether controlled collision samples reuse hidden stone state.

The sampler can reset protocol positions between shots, but the Unity reset path
does not currently prove that Transform.rotation/cooked contact history is also
reset. This script joins the controlled JSONL samples with an existing PhysX
probe result and reports target-stone reuse order against endpoint error.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "unity_controlled_samples_20260707.jsonl"
DEFAULT_BASELINE_PROBE = (
    PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_multiply_unityframe_dt0010.json"
)
DEFAULT_SCAN_PROBE = (
    PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_all_restitution_fine_fast_dt0010.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_state_carryover_report_20260708.json"
UNITY_ZERO_EPS = 1e-9


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _xy(values: Sequence[float], index: int) -> List[float]:
    return [float(values[2 * index]), float(values[2 * index + 1])]


def _is_zero_xy(xy: Sequence[float]) -> bool:
    return abs(float(xy[0])) <= UNITY_ZERO_EPS and abs(float(xy[1])) <= UNITY_ZERO_EPS


def _distance(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1]))


def _controlled_collision_samples(samples: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for sample in samples:
        if not sample.get("collision_observed"):
            continue
        if sample.get("sent_sweep") is not False:
            continue
        if not str(sample.get("category", "")).startswith("collision"):
            continue
        if len(sample.get("target_indices") or []) != 1:
            continue
        rows.append(sample)
    rows.sort(key=lambda item: int(item["sample_id"]))
    return rows


def _best_result_set(payload: Dict[str, Any], preferred_index: Optional[int]) -> Dict[str, Any]:
    result_sets = payload.get("result_sets") or []
    if not result_sets:
        raise ValueError("probe file has no result_sets")
    if preferred_index is not None:
        return result_sets[preferred_index]

    def score(item: Dict[str, Any]) -> float:
        summary = item.get("summary") or {}
        value = summary.get("combined_rmse_m")
        return float("inf") if value is None else float(value)

    return min(result_sets, key=score)


def _rows_by_sample_id(result_set: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    return {int(row["sample_id"]): row for row in result_set.get("rows") or []}


def _describe_sequence(samples: List[Dict[str, Any]], probe_rows: Dict[int, Dict[str, Any]]) -> List[Dict[str, Any]]:
    target_history: Dict[int, List[int]] = {}
    session_target_history: Dict[str, Dict[int, List[int]]] = {}
    sequence = []
    for sample in samples:
        sample_id = int(sample["sample_id"])
        target_index = int(sample["target_indices"][0])
        active_index = int(sample["active_move"]["index"])
        plan_metadata = sample.get("plan_metadata") or {}
        session_key = _session_key(sample)
        previous = list(target_history.get(target_index, []))
        target_history.setdefault(target_index, []).append(sample_id)
        previous_in_session = list(session_target_history.setdefault(session_key, {}).get(target_index, []))
        session_target_history[session_key].setdefault(target_index, []).append(sample_id)

        reset_target_xy = _xy(sample["reset_position"], target_index)
        server_before_target_xy = _xy(sample["server_position_before_reset"], target_index)
        unity_target_xy = _xy(sample["after_position"], target_index)
        probe_row = probe_rows.get(sample_id, {})
        target_error = probe_row.get("target_error")
        active_error = probe_row.get("active_error")
        target_move = (sample.get("target_moves") or [{}])[0]

        sequence.append(
            {
                "sample_id": sample_id,
                "label": sample.get("label"),
                "category": sample.get("category"),
                "plan_metadata": plan_metadata,
                "session_key": session_key,
                "active_index": active_index,
                "target_index": target_index,
                "target_reuse_ordinal": len(previous) + 1,
                "prior_target_samples": previous,
                "target_reuse_ordinal_in_session": len(previous_in_session) + 1,
                "prior_target_samples_in_session": previous_in_session,
                "reset_target_xy": reset_target_xy,
                "server_before_reset_target_xy": server_before_target_xy,
                "server_before_reset_target_was_zero_2d": _is_zero_xy(server_before_target_xy),
                "unity_target_xy": unity_target_xy,
                "unity_target_cleared": _is_zero_xy(unity_target_xy),
                "unity_target_move_m": float(target_move.get("distance", 0.0)),
                "baseline_active_error_m": None if active_error is None else float(active_error),
                "baseline_target_error_m": None if target_error is None else float(target_error),
            }
        )
    return sequence


def _session_key(sample: Dict[str, Any]) -> str:
    metadata = sample.get("plan_metadata") or {}
    if "batch_repeat_index" in metadata:
        return f"batch:{metadata['batch_repeat_index']}"
    if "fresh_repeat_index" in metadata:
        return f"fresh-shot:{sample.get('sample_id')}"
    return "single-session"


def _group_by_target(sequence: Iterable[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for row in sequence:
        groups.setdefault(str(row["target_index"]), []).append(row)
    return groups


def _headon_error_progression(sequence: Iterable[Dict[str, Any]], target_index: int) -> List[Dict[str, Any]]:
    rows = []
    for row in sequence:
        if int(row["target_index"]) != target_index:
            continue
        if row.get("category") != "collision_headon":
            continue
        rows.append(
            {
                "sample_id": row["sample_id"],
                "target_reuse_ordinal": row["target_reuse_ordinal"],
                "unity_target_cleared": row["unity_target_cleared"],
                "baseline_target_error_m": row["baseline_target_error_m"],
            }
        )
    return rows


def _target_error_stats(rows: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    values = [
        float(row["baseline_target_error_m"])
        for row in rows
        if row.get("baseline_target_error_m") is not None
    ]
    if not values:
        return {"count": 0, "rmse_m": None, "mean_m": None, "max_m": None}
    return {
        "count": len(values),
        "rmse_m": math.sqrt(sum(value * value for value in values) / len(values)),
        "mean_m": sum(values) / len(values),
        "max_m": max(values),
    }


def _scan_floor(scan_payload: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if scan_payload is None:
        return None
    result_sets = scan_payload.get("result_sets") or []
    if not result_sets:
        return None

    best_global = _best_result_set(scan_payload, None)
    per_sample: Dict[int, Dict[str, Any]] = {}
    for result_set in result_sets:
        config = result_set.get("config") or {}
        for row in result_set.get("rows") or []:
            if "target_error" not in row:
                continue
            sample_id = int(row["sample_id"])
            target_error = float(row["target_error"])
            current = per_sample.get(sample_id)
            if current is None or target_error < current["target_error_m"]:
                per_sample[sample_id] = {
                    "sample_id": sample_id,
                    "label": row.get("label"),
                    "target_index": row.get("target_index"),
                    "target_error_m": target_error,
                    "active_error_m": row.get("active_error"),
                    "config": config,
                }
    per_sample_rows = [per_sample[key] for key in sorted(per_sample)]
    over_2cm = [row for row in per_sample_rows if row["target_error_m"] > 0.02]
    return {
        "best_global_config": best_global.get("config"),
        "best_global_summary": best_global.get("summary"),
        "per_sample_best_target_errors": per_sample_rows,
        "per_sample_best_target_error_count_over_2cm": len(over_2cm),
        "per_sample_best_target_error_over_2cm_sample_ids": [row["sample_id"] for row in over_2cm],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--baseline-probe", type=Path, default=DEFAULT_BASELINE_PROBE)
    parser.add_argument("--baseline-result-index", type=int, default=0)
    parser.add_argument("--scan-probe", type=Path, default=DEFAULT_SCAN_PROBE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    samples = _controlled_collision_samples(_read_jsonl(args.samples))
    baseline_payload = _read_json(args.baseline_probe)
    baseline_result_set = _best_result_set(baseline_payload, args.baseline_result_index)
    baseline_rows = _rows_by_sample_id(baseline_result_set)
    sequence = _describe_sequence(samples, baseline_rows)
    groups = _group_by_target(sequence)

    scan_payload = _read_json(args.scan_probe) if args.scan_probe.exists() else None
    report = {
        "samples": str(args.samples),
        "baseline_probe": str(args.baseline_probe),
        "baseline_config": baseline_result_set.get("config"),
        "baseline_summary": baseline_result_set.get("summary"),
        "collision_sample_count": len(samples),
        "sequence": sequence,
        "groups_by_target_index": groups,
        "baseline_target_error_stats": _target_error_stats(sequence),
        "parameter_scan_floor": _scan_floor(scan_payload),
        "evidence_flags": {
            "same_session_target_reuse_detected": any(
                row["target_reuse_ordinal_in_session"] > 1 for row in sequence
            ),
            "2d_positions_are_reset_before_reused_target_shots": all(
                row["server_before_reset_target_was_zero_2d"]
                for row in sequence
                if row["target_reuse_ordinal"] > 1
            ),
            "headon_target2_error_progression": _headon_error_progression(sequence, 2),
            "headon_target3_cleared_then_large_inplay_error": _headon_error_progression(sequence, 3),
            "all_target3_reuse_rows": [
                {
                    "sample_id": row["sample_id"],
                    "category": row["category"],
                    "target_reuse_ordinal": row["target_reuse_ordinal"],
                    "unity_target_cleared": row["unity_target_cleared"],
                    "baseline_target_error_m": row["baseline_target_error_m"],
                }
                for row in groups.get("3", [])
            ],
        },
        "interpretation": {
            "controlled_collision_samples_are_clean_gold_set": False,
            "reason": (
                "The protocol position reset makes reused target stones look zeroed in 2D before later shots, "
                "but target errors grow with reuse and the Unity reset path has not shown a rotation reset."
            ),
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "collision_sample_count": report["collision_sample_count"],
                "baseline_target_error_stats": report["baseline_target_error_stats"],
                "evidence_flags": report["evidence_flags"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
