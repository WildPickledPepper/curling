#!/usr/bin/env python3
"""Summarize gravity/rink support contact diagnostics for collision probes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_support_contact_audit_20260709.json"
DEFAULT_PROBES = [
    (
        "current_best",
        PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_current_best_20260708.json",
    ),
    (
        "center_height_0.115",
        PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_centerheight115_currentbest_20260709.json",
    ),
    (
        "disable_gravity",
        PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_disable_gravity_currentbest_20260709.json",
    ),
]
SETTLE_PROBES = [
    (
        "settle_grid_zpreserve",
        PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_settle_grid_zpreserve_20260709.json",
    ),
    (
        "settle_grid_center115",
        PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_settle_grid_center115_20260709.json",
    ),
]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _mean(values: List[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _probe_summary(label: str, path: Path, snapshot_key: str) -> Dict[str, Any]:
    payload = _read_json(path)
    result_set = (payload.get("result_sets") or [{}])[0]
    config = result_set.get("config") or {}
    summary = result_set.get("summary") or {}
    z_values: List[float] = []
    vz_values: List[float] = []
    for row in result_set.get("rows") or []:
        snapshot = (row.get("snapshots") or {}).get(snapshot_key)
        if not snapshot:
            continue
        for role in ("active", "target"):
            role_snapshot = snapshot.get(role) or {}
            position = role_snapshot.get("physx_position")
            velocity = role_snapshot.get("physx_linear_velocity")
            if position and velocity:
                z_values.append(float(position[2]))
                vz_values.append(float(velocity[2]))
    return {
        "label": label,
        "file": str(path.relative_to(PROJECT_ROOT)),
        "config_excerpt": {
            key: config.get(key)
            for key in (
                "radius",
                "height",
                "center_height",
                "contact_offset",
                "disable_stone_gravity",
                "handoff_y_offset",
                "use_unity_frame",
            )
        },
        "endpoint_summary": summary,
        "snapshot_key": snapshot_key,
        "z_mean_m": _mean(z_values),
        "z_min_m": min(z_values) if z_values else None,
        "z_max_m": max(z_values) if z_values else None,
        "vz_mean_mps": _mean(vz_values),
        "vz_min_mps": min(vz_values) if vz_values else None,
        "vz_max_mps": max(vz_values) if vz_values else None,
    }


def _settle_probe_summary(label: str, path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"label": label, "file": str(path.relative_to(PROJECT_ROOT)), "status": "missing"}
    payload = _read_json(path)
    rows: List[Dict[str, Any]] = []
    for index, result_set in enumerate(payload.get("result_sets") or []):
        config = result_set.get("config") or {}
        summary = result_set.get("summary") or {}
        row12003 = next(
            (row for row in result_set.get("rows") or [] if int(row.get("sample_id", -1)) == 12003),
            {},
        )
        rows.append(
            {
                "result_index": index,
                "center_height": config.get("center_height"),
                "target_settle_time": config.get("target_settle_time"),
                "active_settle_time": config.get("active_settle_time"),
                "active_settle_backoff": config.get("active_settle_backoff"),
                "active_rmse_m": summary.get("active_rmse_m"),
                "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
                "combined_rmse_m": summary.get("combined_rmse_m"),
                "sample_12003_target_error_m": row12003.get("target_error"),
                "sample_12003_sim_target": row12003.get("sim_target"),
            }
        )
    best = min(
        (row for row in rows if row.get("target_in_play_rmse_m") is not None),
        key=lambda row: float(row["target_in_play_rmse_m"]),
        default=None,
    )
    best12003 = min(
        (row for row in rows if row.get("sample_12003_target_error_m") is not None),
        key=lambda row: float(row["sample_12003_target_error_m"]),
        default=None,
    )
    return {
        "label": label,
        "file": str(path.relative_to(PROJECT_ROOT)),
        "status": "ok",
        "best_by_target_rmse": best,
        "best_by_12003": best12003,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-key", default="0.020000")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    reports = [_probe_summary(label, path, args.snapshot_key) for label, path in DEFAULT_PROBES]
    settle_reports = [_settle_probe_summary(label, path) for label, path in SETTLE_PROBES]
    report = {
        "snapshot_key": args.snapshot_key,
        "probes": reports,
        "settle_probes": settle_reports,
        "interpretation": [
            "Unity assets show formal stones use gravity, and pyphysx Scene uses z gravity -9.81.",
            "Disabling gravity removes rink friction/support and makes endpoint errors catastrophic, so gravity/support contact is required.",
            "Starting at center_height=0.115 removes the 0.02s vertical velocity but does not improve target RMSE, so vertical settling velocity alone is not the 10cm source.",
            "Pre-settling target and/or active stones on the rink before collision does not improve the global target RMSE; the no-settle baseline remains best in the current diagnostic grids.",
            "Remaining mismatch is more likely in stone-stone contact manifold/solver rows than in gross rink support state.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for row in reports:
        endpoint = row["endpoint_summary"]
        print(
            row["label"],
            f"target_rmse={endpoint.get('target_in_play_rmse_m')}",
            f"z_mean={row['z_mean_m']}",
            f"vz_mean={row['vz_mean_mps']}",
        )
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
