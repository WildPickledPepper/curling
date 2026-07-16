#!/usr/bin/env python3
"""Summarize local feature-phase probes for the hard collision sample.

The goal is to separate static hull/pose/topology explanations from the
remaining runtime contact-manifold/cache explanation.  The script only reads
existing local pyphysx probe outputs; it does not sample Unity.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION = PROJECT_ROOT / "data" / "calibration"
DEFAULT_OUTPUT = CALIBRATION / "unity_collision_feature_phase_audit_20260709.json"

REPORTS = {
    "common_shape_local_yaw": CALIBRATION
    / "unity_physx_collision_probe_unique_role_shape_local_yaw_grid_20260709.json",
    "sample12003_shape_local_yaw_fine": CALIBRATION
    / "unity_physx_collision_probe_12003_shape_local_yaw_fine_20260709.json",
    "sample12003_actor_yaw_grid": CALIBRATION
    / "unity_physx_collision_probe_12003_actor_yaw_grid_20260709.json",
    "sample12003_stone_faces_grid": CALIBRATION
    / "unity_physx_collision_probe_12003_stone_faces_grid_20260709.json",
    "common_shape_local_xyz": CALIBRATION
    / "unity_physx_collision_probe_unique_role_shape_local_xyz_grid_20260709.json",
}


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _rad_to_deg(value: Any) -> Optional[float]:
    if value is None:
        return None
    return float(value) * 180.0 / math.pi


def _sample_row(result_set: Dict[str, Any], sample_id: int) -> Optional[Dict[str, Any]]:
    for row in result_set.get("rows") or []:
        if int(row.get("sample_id", -1)) == sample_id:
            return row
    return None


def _compact_config(config: Dict[str, Any]) -> Dict[str, Any]:
    keys = [
        "shape_local_x",
        "shape_local_y",
        "shape_local_z",
        "shape_local_yaw",
        "active_yaw",
        "target_yaw",
        "stone_faces",
        "radius",
        "height",
        "center_height",
        "contact_offset",
        "rest_offset",
        "convex_quantized_count",
        "convex_vertex_limit",
        "solver_position_iterations",
        "solver_velocity_iterations",
    ]
    compact = {key: config.get(key) for key in keys if key in config}
    for key in ("shape_local_yaw", "active_yaw", "target_yaw"):
        if key in compact:
            compact[f"{key}_deg"] = _rad_to_deg(compact[key])
    return compact


def _best_by(rows: Iterable[Dict[str, Any]], key: str) -> Optional[Dict[str, Any]]:
    candidates = [row for row in rows if row.get(key) is not None]
    if not candidates:
        return None
    return min(candidates, key=lambda row: float(row[key]))


def _summarize_probe(path: Path, sample_id: int = 12003) -> Dict[str, Any]:
    payload = _read_json(path)
    if payload is None:
        return {"path": str(path.relative_to(PROJECT_ROOT)), "status": "missing"}

    rows: List[Dict[str, Any]] = []
    for index, result_set in enumerate(payload.get("result_sets") or []):
        config = result_set.get("config") or {}
        summary = result_set.get("summary") or {}
        sample = _sample_row(result_set, sample_id)
        rows.append(
            {
                "result_index": index,
                "config": _compact_config(config),
                "active_rmse_m": summary.get("active_rmse_m"),
                "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
                "combined_rmse_m": summary.get("combined_rmse_m"),
                f"sample{sample_id}_target_error_m": None if sample is None else sample.get("target_error"),
                f"sample{sample_id}_active_error_m": None if sample is None else sample.get("active_error"),
                f"sample{sample_id}_sim_target": None if sample is None else sample.get("sim_target"),
            }
        )

    sample_key = f"sample{sample_id}_target_error_m"
    return {
        "path": str(path.relative_to(PROJECT_ROOT)),
        "status": "ok",
        "result_set_count": len(rows),
        "best_by_global_target_rmse": _best_by(rows, "target_in_play_rmse_m"),
        f"best_by_sample{sample_id}_target_error": _best_by(rows, sample_key),
        "top_by_sample_target_error": sorted(
            [row for row in rows if row.get(sample_key) is not None],
            key=lambda row: float(row[sample_key]),
        )[:12],
    }


def build_report() -> Dict[str, Any]:
    probes = {name: _summarize_probe(path) for name, path in REPORTS.items()}

    bests = {}
    for name, report in probes.items():
        bests[name] = report.get("best_by_sample12003_target_error")

    best_error_values = [
        float(row["sample12003_target_error_m"])
        for row in bests.values()
        if row and row.get("sample12003_target_error_m") is not None
    ]
    best_seen = min(best_error_values) if best_error_values else None

    return {
        "sample_id": 12003,
        "summary": {
            "best_sample12003_error_across_feature_phase_probes_m": best_seen,
            "reaches_2cm": bool(best_seen is not None and best_seen <= 0.02),
            "interpretation": (
                "Static hull phase, actor yaw, simple shape-local offsets, and input stone face count "
                "do not explain the hard 12003 residual. The best local static feature probe remains "
                "around 19cm, far above the 2cm target. This supports a runtime contact-manifold, "
                "friction-anchor/cache, or solver-row instance difference rather than a single static "
                "shape phase or topology knob."
            ),
        },
        "probes": probes,
        "evidence_notes": [
            "common shape-local yaw +/- half side step improves 12003 only to about 20cm and leaves global target RMSE around 12cm.",
            "sample12003 fine shape-local yaw does not reveal a hidden phase valley near 2cm.",
            "sample12003 active/target actor yaw over +/-11.25deg also bottoms around 20cm.",
            "sample12003 stone-faces sweep changes contact behavior but bottoms around 19cm.",
            "These are local pyphysx probes only; they rule out static replay knobs, not the need for Unity runtime ContactBuffer/solver-row capture.",
        ],
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
