#!/usr/bin/env python3
"""Summarize the remaining gap after direct PCM/contact-prep closure."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCAL_PROBE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_native13000_pcm_hull_runtime_posefix_20260709.json"
)
DEFAULT_SOLVER_STATE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_native_solver_state_pcm_hull_runtime_20260709_171257.json"
)
DEFAULT_BRIDGE = PROJECT_ROOT / "data" / "calibration" / "unity_direct_pcm_solver_row_bridge_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_direct_pcm_scene_replay_gap_20260709.json"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _vec_norm(values: Iterable[Any]) -> float | None:
    rows = [float(value) for value in values if isinstance(value, (int, float)) and math.isfinite(value)]
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows))


def _separation_range(points: list[dict[str, Any]]) -> dict[str, float | None]:
    rows = [float(point["separation"]) for point in points if isinstance(point.get("separation"), (int, float))]
    return {
        "min": min(rows) if rows else None,
        "max": max(rows) if rows else None,
    }


def _first_report(local_row: dict[str, Any]) -> dict[str, Any]:
    reports = local_row.get("stone_stone_contact_reports") or []
    report = reports[0] if reports and isinstance(reports[0], dict) else {}
    points = report.get("points") if isinstance(report.get("points"), list) else []
    impulses = [
        _vec_norm(point.get("impulse") or [])
        for point in points
        if isinstance(point, dict) and isinstance(point.get("impulse"), list)
    ]
    impulses = [float(value) for value in impulses if value is not None]
    return {
        "time": report.get("time"),
        "contact_count": report.get("contact_count"),
        "normal0": (points[0] or {}).get("normal") if points else None,
        "separation_range": _separation_range(points),
        "impulse_norm_sum": sum(impulses) if impulses else None,
        "points_preview": points[:4],
    }


def _unity_first_stone_stone(solver_state: dict[str, Any]) -> dict[str, Any]:
    first = solver_state.get("firstStoneStone") or {}
    contacts = (((first.get("contactBuffer") or {}).get("candidate") or {}).get("contactsPreview") or [])
    raw_header = ((first.get("rawVsComputedNormalRow") or {}).get("rawHeader") or {})
    return {
        "t": first.get("t"),
        "contact_count": len(contacts),
        "normal0": contacts[0].get("normal") if contacts else None,
        "separation_range": _separation_range(contacts),
        "raw_header": raw_header,
        "contacts_preview": contacts[:4],
    }


def build_report(local_probe_path: Path, solver_state_path: Path, bridge_path: Path) -> dict[str, Any]:
    local_probe = _read_json(local_probe_path)
    solver_state = _read_json(solver_state_path)
    bridge = _read_json(bridge_path)
    result_set = (local_probe.get("result_sets") or [{}])[0]
    local_row = (result_set.get("rows") or [{}])[0]
    summary = result_set.get("summary") or {}
    local_first = _first_report(local_row)
    unity_first = _unity_first_stone_stone(solver_state)
    return {
        "question": "What remains after direct PCM contacts and ContactBuffer->solver rows match Unity?",
        "local_probe": str(local_probe_path.relative_to(PROJECT_ROOT)),
        "unity_solver_state": str(solver_state_path.relative_to(PROJECT_ROOT)),
        "direct_pcm_solver_bridge": str(bridge_path.relative_to(PROJECT_ROOT)),
        "endpoint_summary": summary,
        "endpoint_pair": {
            "local_active": local_row.get("sim_active"),
            "local_target": local_row.get("sim_target"),
            "unity_active": local_row.get("unity_active"),
            "unity_target": local_row.get("unity_target"),
            "active_error_m": local_row.get("active_error"),
            "target_error_m": local_row.get("target_error"),
        },
        "local_scene_first_contact_report": local_first,
        "unity_first_stone_stone_finalizer": unity_first,
        "direct_pcm_bridge_summary": bridge.get("summary"),
        "conclusion": (
            "Direct scene-style PCM and ContactBuffer->SolverContact row prep are closed for this capture, "
            "but pyphysx full Scene replay still enters the collision with a fresh/local PCM path: "
            f"local first report has {local_first.get('contact_count')} contacts with separation "
            f"{local_first.get('separation_range')}, while Unity finalizer has {unity_first.get('contact_count')} "
            f"contacts with separation {unity_first.get('separation_range')}. The 17:12 same-run target endpoint "
            f"error remains {local_row.get('target_error')} m, so the remaining gap is Scene replay state "
            "integration: first-collision timing, PCM cache lifetime, warm-start force buffer, friction anchors, "
            "or PxSolverBody pre-solve state."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-probe", type=Path, default=DEFAULT_LOCAL_PROBE)
    parser.add_argument("--solver-state", type=Path, default=DEFAULT_SOLVER_STATE)
    parser.add_argument("--bridge", type=Path, default=DEFAULT_BRIDGE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(args.local_probe, args.solver_state, args.bridge)
    print(json.dumps({"endpoint_summary": report["endpoint_summary"], "conclusion": report["conclusion"]}, indent=2, ensure_ascii=False))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
