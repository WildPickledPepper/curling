#!/usr/bin/env python3
"""Summarize collision probe alignment against a Unity sample JSONL."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SAMPLES = PROJECT_ROOT / "data" / "calibration" / "unity_controlled_samples_20260707.jsonl"
DEFAULT_PROBE = PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_multiply_unityframe_dt0010.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_alignment_summary_20260708.json"


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _rows_by_sample_id(result_set: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    return {int(row["sample_id"]): row for row in result_set.get("rows") or []}


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _mean(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return sum(rows) / len(rows)


def _session_key(sample: Dict[str, Any]) -> str:
    metadata = sample.get("plan_metadata") or {}
    if "batch_repeat_index" in metadata:
        return f"batch:{metadata['batch_repeat_index']}"
    if "fresh_repeat_index" in metadata:
        return f"fresh-shot:{sample.get('sample_id')}"
    return "single-session"


def _source_case_id(sample: Dict[str, Any]) -> int:
    metadata = sample.get("plan_metadata") or {}
    if "source_sample_id" in metadata:
        return int(metadata["source_sample_id"])
    if "source_sample_id" in sample:
        return int(sample["source_sample_id"])
    return int(sample["sample_id"])


def _status_for_row(
    sample: Dict[str, Any],
    probe_row: Optional[Dict[str, Any]],
    threshold_m: float,
) -> Dict[str, Any]:
    sample_id = int(sample["sample_id"])
    metadata = sample.get("plan_metadata") or {}
    target_indices = sample.get("target_indices") or []
    target_index = int(target_indices[0]) if target_indices else None
    base = {
        "sample_id": sample_id,
        "label": sample.get("label"),
        "category": sample.get("category"),
        "session_key": _session_key(sample),
        "source_case_id": _source_case_id(sample),
        "plan_metadata": metadata,
        "active_index": int(sample.get("active_move", {}).get("index", -1)),
        "target_index": target_index,
    }
    if probe_row is None:
        return {
            **base,
            "status": "missing_probe_row",
            "unity_target_in_play": None,
            "active_error_m": None,
            "target_error_m": None,
            "max_evaluable_error_m": None,
            "passes_threshold_excluding_cleared_target": False,
            "passes_full_in_play_collision_threshold": False,
        }

    active_error = probe_row.get("active_error")
    target_error = probe_row.get("target_error")
    unity_target_in_play = bool(probe_row.get("unity_target_in_play"))
    errors = []
    if active_error is not None:
        errors.append(float(active_error))
    if unity_target_in_play and target_error is not None:
        errors.append(float(target_error))
    max_error = max(errors) if errors else None
    passes_available = bool(errors) and all(value <= threshold_m for value in errors)
    passes_full = unity_target_in_play and active_error is not None and target_error is not None and passes_available
    if not unity_target_in_play:
        status = "target_cleared_unmodeled"
    elif passes_full:
        status = "pass"
    else:
        status = "fail"
    return {
        **base,
        "status": status,
        "unity_target_in_play": unity_target_in_play,
        "active_error_m": None if active_error is None else float(active_error),
        "target_error_m": None if target_error is None else float(target_error),
        "max_evaluable_error_m": max_error,
        "passes_threshold_excluding_cleared_target": passes_available,
        "passes_full_in_play_collision_threshold": passes_full,
    }


def _summarize_rows(rows: List[Dict[str, Any]], threshold_m: float) -> Dict[str, Any]:
    active_errors = [row["active_error_m"] for row in rows if row.get("active_error_m") is not None]
    target_errors = [row["target_error_m"] for row in rows if row.get("target_error_m") is not None]
    all_errors = active_errors + target_errors
    max_errors = [row["max_evaluable_error_m"] for row in rows if row.get("max_evaluable_error_m") is not None]
    return {
        "sample_count": len(rows),
        "missing_probe_count": sum(1 for row in rows if row["status"] == "missing_probe_row"),
        "target_cleared_unmodeled_count": sum(1 for row in rows if row["status"] == "target_cleared_unmodeled"),
        "in_play_target_count": sum(1 for row in rows if row.get("unity_target_in_play") is True),
        "active_error_count": len(active_errors),
        "target_error_count": len(target_errors),
        "active_rmse_m": _rmse(active_errors),
        "target_rmse_m": _rmse(target_errors),
        "combined_rmse_m": _rmse(all_errors),
        "active_mean_m": _mean(active_errors),
        "target_mean_m": _mean(target_errors),
        "max_evaluable_error_m": max(max_errors) if max_errors else None,
        "threshold_m": threshold_m,
        "pass_excluding_cleared_target_count": sum(
            1 for row in rows if row["passes_threshold_excluding_cleared_target"]
        ),
        "full_in_play_pass_count": sum(1 for row in rows if row["passes_full_in_play_collision_threshold"]),
        "failed_in_play_sample_ids": [
            row["sample_id"]
            for row in rows
            if row.get("unity_target_in_play") is True
            and not row["passes_full_in_play_collision_threshold"]
        ],
    }


def _group_summary(rows: List[Dict[str, Any]], key: str, threshold_m: float) -> Dict[str, Dict[str, Any]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row.get(key)), []).append(row)
    return {group_key: _summarize_rows(group_rows, threshold_m) for group_key, group_rows in sorted(groups.items())}


def _same_session_index_reuse(rows: List[Dict[str, Any]], *, index_key: str, label: str) -> Dict[str, Any]:
    seen: Dict[str, Dict[int, List[int]]] = {}
    reuse_rows = []
    for row in rows:
        stone_index = row.get(index_key)
        if stone_index is None or int(stone_index) < 0:
            continue
        session_key = str(row["session_key"])
        prior = seen.setdefault(session_key, {}).setdefault(int(stone_index), [])
        if prior:
            reuse_rows.append(
                {
                    "session_key": session_key,
                    f"{label}_index": stone_index,
                    "sample_id": row["sample_id"],
                    "prior_sample_ids": list(prior),
                }
            )
        prior.append(row["sample_id"])
    return {
        f"same_session_{label}_reuse_detected": bool(reuse_rows),
        f"{label}_reuse_rows": reuse_rows,
    }


def build_report(
    *,
    samples_path: Path,
    probe_path: Path,
    result_index: Optional[int],
    threshold_m: float,
) -> Dict[str, Any]:
    samples = _controlled_collision_samples(_read_jsonl(samples_path))
    probe_payload = _read_json(probe_path)
    result_set = _best_result_set(probe_payload, result_index)
    probe_rows = _rows_by_sample_id(result_set)
    rows = [
        _status_for_row(sample, probe_rows.get(int(sample["sample_id"])), threshold_m)
        for sample in samples
    ]
    target_reuse = _same_session_index_reuse(rows, index_key="target_index", label="target")
    active_reuse = _same_session_index_reuse(rows, index_key="active_index", label="active")
    summary_core = _summarize_rows(rows, threshold_m)
    return {
        "samples": str(samples_path),
        "probe": str(probe_path),
        "probe_config": result_set.get("config"),
        "probe_summary": result_set.get("summary"),
        "summary": {
            **summary_core,
            **target_reuse,
            **active_reuse,
            "all_in_play_targets_within_threshold": summary_core["missing_probe_count"] == 0
            and summary_core["in_play_target_count"] > 0
            and not summary_core["failed_in_play_sample_ids"],
        },
        "by_category": _group_summary(rows, "category", threshold_m),
        "by_session": _group_summary(rows, "session_key", threshold_m),
        "by_source_case": _group_summary(rows, "source_case_id", threshold_m),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=DEFAULT_SAMPLES)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--result-index", type=int, default=0)
    parser.add_argument("--threshold-m", type=float, default=0.02)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(
        samples_path=args.samples,
        probe_path=args.probe,
        result_index=args.result_index,
        threshold_m=args.threshold_m,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "summary": report["summary"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
