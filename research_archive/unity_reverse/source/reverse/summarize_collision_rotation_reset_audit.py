#!/usr/bin/env python3
"""Summarize wide actor-yaw probes for reset-rotation uncertainty."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_rotation_reset_audit_20260709.json"
SAMPLE_12003_PROBE_FILES = [
    CALIBRATION / "unity_physx_collision_probe_12003_actor_yaw_wide_grid_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12003_actor_yaw_wide_refine_20260709.json",
    CALIBRATION / "unity_physx_collision_probe_12003_actor_yaw_wide_refine2_20260709.json",
]
HARD_SAMPLE_DUAL_YAW_FILES = {
    12003: SAMPLE_12003_PROBE_FILES,
    12004: [CALIBRATION / "unity_physx_collision_probe_12004_actor_yaw_wide_grid_20260709.json"],
    12007: [CALIBRATION / "unity_physx_collision_probe_12007_actor_yaw_wide_grid_20260709.json"],
}
TARGET_YAW_FINE_FILE = CALIBRATION / "unity_physx_collision_probe_unique_role_target_yaw_fine_grid_20260709.json"


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _deg(rad: Any) -> float:
    return float(rad) * 180.0 / math.pi


def _collect_rows(paths: Iterable[Path], sample_id: Optional[int] = None) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in paths:
        payload = _read_json(path)
        if payload is None:
            continue
        for index, result_set in enumerate(payload.get("result_sets") or []):
            config = result_set.get("config") or {}
            for row in result_set.get("rows") or []:
                row_sample_id = row.get("sample_id")
                if sample_id is not None and row_sample_id != sample_id:
                    continue
                if "active_error" not in row or "target_error" not in row:
                    continue
                if row.get("target_error") is None or row.get("active_error") is None:
                    continue
                active_error = float(row["active_error"])
                target_error = float(row["target_error"])
                rows.append(
                    {
                        "file": str(path.relative_to(PROJECT_ROOT)),
                        "result_index": index,
                        "sample_id": row_sample_id,
                        "label": row.get("label"),
                        "active_yaw_deg": _deg(config.get("active_yaw", row.get("active_yaw", 0.0))),
                        "target_yaw_deg": _deg(config.get("target_yaw", row.get("target_yaw", 0.0))),
                        "active_error_m": active_error,
                        "target_error_m": target_error,
                        "pair_rmse_m": math.sqrt((active_error * active_error + target_error * target_error) / 2.0),
                        "unity_target_in_play": row.get("unity_target_in_play"),
                        "sim_active": row.get("sim_active"),
                        "sim_target": row.get("sim_target"),
                        "unity_active": row.get("unity_active"),
                        "unity_target": row.get("unity_target"),
                    }
                )
    return rows


def _best(rows: List[Dict[str, Any]], key: str) -> Optional[Dict[str, Any]]:
    if not rows:
        return None
    return min(rows, key=lambda row: float(row[key]))


def _summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    best_target = _best(rows, "target_error_m")
    best_pair = _best(rows, "pair_rmse_m")
    best_active = _best(rows, "active_error_m")
    return {
        "row_count": len(rows),
        "best_target_error_m": None if best_target is None else best_target["target_error_m"],
        "best_pair_rmse_m": None if best_pair is None else best_pair["pair_rmse_m"],
        "best_active_error_m": None if best_active is None else best_active["active_error_m"],
        "target_within_2cm_count": sum(1 for row in rows if row["target_error_m"] <= 0.02),
        "pair_within_2cm_count": sum(1 for row in rows if row["pair_rmse_m"] <= 0.02),
        "both_endpoints_within_2cm_count": sum(
            1 for row in rows if row["active_error_m"] <= 0.02 and row["target_error_m"] <= 0.02
        ),
    }


def _target_yaw_only_oracle() -> Dict[str, Any]:
    rows = [
        row
        for row in _collect_rows([TARGET_YAW_FINE_FILE])
        if row.get("unity_target_in_play") is not False
    ]
    by_sample: Dict[int, List[Dict[str, Any]]] = {}
    for row in rows:
        sample_id = row.get("sample_id")
        if sample_id is None:
            continue
        by_sample.setdefault(int(sample_id), []).append(row)

    best_by_sample = {
        str(sample_id): _best(sample_rows, "target_error_m")
        for sample_id, sample_rows in sorted(by_sample.items())
    }
    best_rows = [row for row in best_by_sample.values() if row is not None]
    if not best_rows:
        return {
            "file": str(TARGET_YAW_FINE_FILE.relative_to(PROJECT_ROOT)),
            "sample_count": 0,
            "interpretation": "target-yaw-only probe file is missing or empty.",
        }

    target_rmse = math.sqrt(sum(row["target_error_m"] ** 2 for row in best_rows) / len(best_rows))
    active_rmse = math.sqrt(sum(row["active_error_m"] ** 2 for row in best_rows) / len(best_rows))
    pair_rmse = math.sqrt(sum(row["pair_rmse_m"] ** 2 for row in best_rows) / len(best_rows))
    return {
        "file": str(TARGET_YAW_FINE_FILE.relative_to(PROJECT_ROOT)),
        "sample_count": len(best_rows),
        "target_rmse_m": target_rmse,
        "active_rmse_m": active_rmse,
        "pair_rmse_m": pair_rmse,
        "target_over_2cm_sample_ids": [
            row["sample_id"] for row in best_rows if row["target_error_m"] > 0.02
        ],
        "pair_over_2cm_sample_ids": [
            row["sample_id"] for row in best_rows if row["pair_rmse_m"] > 0.02
        ],
        "best_by_sample": best_by_sample,
        "interpretation": (
            "Per-sample target-yaw-only oracle reduces several target endpoints, showing hidden/reset "
            "yaw is a real state lever. It still leaves hard samples above 2cm and does not close active+target pairs."
        ),
    }


def _dual_yaw_by_sample() -> Dict[str, Any]:
    summary: Dict[str, Any] = {}
    for sample_id, files in HARD_SAMPLE_DUAL_YAW_FILES.items():
        rows = _collect_rows(files, sample_id=sample_id)
        sample_summary = _summarize_rows(rows)
        sample_summary.update(
            {
                "probe_files": [str(path.relative_to(PROJECT_ROOT)) for path in files],
                "best_target": _best(rows, "target_error_m"),
                "best_pair": _best(rows, "pair_rmse_m"),
                "best_active": _best(rows, "active_error_m"),
            }
        )
        summary[str(sample_id)] = sample_summary
    return summary


def build_report() -> Dict[str, Any]:
    rows = _collect_rows(SAMPLE_12003_PROBE_FILES, sample_id=12003)
    best_target = _best(rows, "target_error_m")
    best_pair = _best(rows, "pair_rmse_m")
    best_active = _best(rows, "active_error_m")
    target_yaw_only = _target_yaw_only_oracle()
    dual_yaw_by_sample = _dual_yaw_by_sample()
    return {
        "sample_id": 12003,
        "probe_files": [str(path.relative_to(PROJECT_ROOT)) for path in SAMPLE_12003_PROBE_FILES],
        "summary": {
            "row_count": len(rows),
            "best_target_error_m": None if best_target is None else best_target["target_error_m"],
            "best_pair_rmse_m": None if best_pair is None else best_pair["pair_rmse_m"],
            "best_active_error_m": None if best_active is None else best_active["active_error_m"],
            "target_within_2cm_count": sum(1 for row in rows if row["target_error_m"] <= 0.02),
            "pair_within_2cm_count": sum(1 for row in rows if row["pair_rmse_m"] <= 0.02),
            "both_endpoints_within_2cm_count": sum(
                1 for row in rows if row["active_error_m"] <= 0.02 and row["target_error_m"] <= 0.02
            ),
            "interpretation": (
                "Large vertical yaw is a real contact-feature lever for hard sample 12003: it can bring "
                "the target endpoint to about 1.75cm, unlike the small +/-11.25deg yaw grid. However, "
                "the same yaw settings leave active around 4-7cm, and no tested yaw pair gets the pair "
                "RMSE or both endpoints under 2cm. This makes reset yaw/rotation a plausible missing "
                "runtime state, but not a complete collision alignment by itself."
            ),
            "target_yaw_only_oracle_target_rmse_m": target_yaw_only.get("target_rmse_m"),
            "target_yaw_only_oracle_pair_rmse_m": target_yaw_only.get("pair_rmse_m"),
            "hard_sample_dual_yaw_best_pair_rmse_m": {
                sample_id: item.get("best_pair_rmse_m") for sample_id, item in dual_yaw_by_sample.items()
            },
        },
        "best_target": best_target,
        "best_pair": best_pair,
        "best_active": best_active,
        "target_yaw_only_oracle": target_yaw_only,
        "hard_sample_dual_yaw": dual_yaw_by_sample,
        "top_by_target": sorted(rows, key=lambda row: row["target_error_m"])[:20],
        "top_by_pair": sorted(rows, key=lambda row: row["pair_rmse_m"])[:20],
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with DEFAULT_OUTPUT.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(json.dumps({"output": str(DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)), "summary": report["summary"]}, indent=2))


if __name__ == "__main__":
    main()
