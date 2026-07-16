#!/usr/bin/env python3
"""Compare direct PCM contacts against Unity finalizer solver rows.

This is a narrow bridge audit: direct scene-style PCM has already been shown to
emit Unity's two cached contacts. This script feeds those direct contacts into
the existing ContactBuffer -> SolverContact row reconstruction and compares the
result to Unity's captured raw solver rows from the same runtime capture.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.extract_physx_native_solver_state import (
    compute_normal_rows,
    first_decoded_constraint,
    finite_float,
    scalar_delta,
    usable_vec3,
    vector_delta,
)


DEFAULT_SOLVER_STATE = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_native_solver_state_pcm_hull_runtime_20260709_171257.json"
)
DEFAULT_DIRECT_PCM = PROJECT_ROOT / "data" / "calibration" / "unity_direct_pcm_vs_immediate_audit_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_direct_pcm_solver_row_bridge_20260709.json"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _max_abs(values: Iterable[Any]) -> float | None:
    rows = [abs(float(value)) for value in values if finite_float(value)]
    return max(rows) if rows else None


def _flatten_numbers(value: Any) -> Iterable[float]:
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        yield float(value)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _flatten_numbers(item)
    elif isinstance(value, list):
        for item in value:
            yield from _flatten_numbers(item)


def _contact_delta(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    normal_delta = vector_delta(a.get("normal"), b.get("normal"))
    point_delta = vector_delta(a.get("point"), b.get("point"))
    separation_delta = scalar_delta(a.get("separation"), b.get("separation"))
    return {
        "normalDelta": normal_delta,
        "pointDelta": point_delta,
        "separationDelta": separation_delta,
        "maxAbs": _max_abs(
            list(normal_delta or [])
            + list(point_delta or [])
            + ([separation_delta] if separation_delta is not None else [])
        ),
    }


def _row_delta(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    out = {
        "raXnDelta": vector_delta(a.get("raXn"), b.get("raXn")),
        "rbXnDelta": vector_delta(a.get("rbXn"), b.get("rbXn")),
        "velMultiplierDelta": scalar_delta(a.get("velMultiplier"), b.get("velMultiplier")),
        "biasedErrDelta": scalar_delta(a.get("biasedErr"), b.get("biasedErr")),
        "unbiasedErrDelta": scalar_delta(a.get("unbiasedErr"), b.get("unbiasedErr")),
        "maxImpulseDelta": scalar_delta(a.get("maxImpulse"), b.get("maxImpulse")),
    }
    out["maxAbs"] = _max_abs(_flatten_numbers(out))
    return out


def _contacts_from_direct_case(direct_case: dict[str, Any], unity_contacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    points = ((direct_case.get("direct_pcm") or {}).get("points") or [])
    contacts: list[dict[str, Any]] = []
    for index, point in enumerate(points):
        if not isinstance(point, dict):
            continue
        template = dict(unity_contacts[index] if index < len(unity_contacts) else {})
        template.update(
            {
                "normal": point.get("normal"),
                "point": point.get("point"),
                "separation": point.get("separation"),
                "targetVel": template.get("targetVel") or [0.0, 0.0, 0.0],
                "restitution": template.get("restitution", 1.0),
                "maxImpulse": template.get("maxImpulse", 1.0000000331813535e32),
                "staticFriction": template.get("staticFriction", 0.36000001430511475),
                "dynamicFriction": template.get("dynamicFriction", 0.36000001430511475),
            }
        )
        contacts.append(template)
    return contacts


def _case_by_name(payload: dict[str, Any], name: str) -> dict[str, Any]:
    for case in payload.get("cases") or []:
        if isinstance(case, dict) and case.get("name") == name:
            return case
    raise KeyError(f"direct PCM case not found: {name}")


def _first_raw_constraint(first_stone_stone: dict[str, Any]) -> dict[str, Any] | None:
    extra = first_stone_stone.get("extraConstraintDumps")
    descs = first_stone_stone.get("solverConstraintDescs")
    if isinstance(extra, list):
        decoded = first_decoded_constraint(extra)
        if isinstance(decoded, dict):
            return decoded
    if isinstance(descs, list):
        return first_decoded_constraint(descs)
    return None


def build_report(solver_state_path: Path, direct_pcm_path: Path, case_name: str) -> dict[str, Any]:
    solver_state = _read_json(solver_state_path)
    direct_pcm = _read_json(direct_pcm_path)
    first = solver_state["firstStoneStone"]
    unity_candidate = first["contactBuffer"]["candidate"]
    unity_contacts = unity_candidate.get("contactsPreview") or []
    direct_case = _case_by_name(direct_pcm, case_name)
    direct_contacts = _contacts_from_direct_case(direct_case, unity_contacts)
    direct_candidate = dict(unity_candidate)
    direct_candidate["contactsPreview"] = direct_contacts
    direct_candidate["contactCount"] = len(direct_contacts)

    direct_rows = compute_normal_rows(
        direct_candidate,
        first["contactDesc"],
        first["solverBodyData"],
        [],
    )
    unity_rows = first.get("computedNormalRows") or []
    raw_constraint = _first_raw_constraint(first) or {}
    raw_rows = raw_constraint.get("normalRows") if isinstance(raw_constraint, dict) else []
    raw_header = raw_constraint.get("header") if isinstance(raw_constraint, dict) else {}

    contact_deltas = [
        _contact_delta(unity_contact, direct_contact)
        for unity_contact, direct_contact in zip(unity_contacts, direct_contacts)
        if isinstance(unity_contact, dict) and isinstance(direct_contact, dict)
    ]
    direct_vs_unity_rows = [
        _row_delta(unity_row, direct_row)
        for unity_row, direct_row in zip(unity_rows, direct_rows)
        if isinstance(unity_row, dict) and isinstance(direct_row, dict)
    ]
    raw_vs_direct_rows = [
        _row_delta(raw_row, direct_row)
        for raw_row, direct_row in zip(raw_rows or [], direct_rows)
        if isinstance(raw_row, dict) and isinstance(direct_row, dict)
    ]

    header_normal_delta = vector_delta(raw_header.get("normal"), direct_contacts[0].get("normal")) if direct_contacts else None
    summary = {
        "unity_contact_count": len(unity_contacts),
        "direct_contact_count": len(direct_contacts),
        "raw_normal_row_count": len(raw_rows or []),
        "direct_computed_row_count": len(direct_rows),
        "max_contact_delta": _max_abs(delta.get("maxAbs") for delta in contact_deltas),
        "max_direct_vs_unity_computed_row_delta": _max_abs(delta.get("maxAbs") for delta in direct_vs_unity_rows),
        "max_raw_vs_direct_computed_row_delta": _max_abs(delta.get("maxAbs") for delta in raw_vs_direct_rows),
        "raw_header_normal_vs_direct_contact0_max_delta": _max_abs(header_normal_delta or []),
        "bridge_closed_at_contact_prep_precision": bool(
            len(unity_contacts) == len(direct_contacts)
            and len(direct_rows) == len(unity_rows)
            and (_max_abs(delta.get("maxAbs") for delta in contact_deltas) or 1.0) < 1e-4
            and (_max_abs(delta.get("maxAbs") for delta in raw_vs_direct_rows) or 1.0) < 1e-4
        ),
    }
    return {
        "question": "Do direct scene-style PCM contacts feed the same ContactBuffer -> SolverContact row path as Unity?",
        "solver_state": str(solver_state_path.relative_to(PROJECT_ROOT)),
        "direct_pcm_report": str(direct_pcm_path.relative_to(PROJECT_ROOT)),
        "direct_pcm_case": case_name,
        "summary": summary,
        "unity_expected_from_direct_report": direct_pcm.get("unity_expected"),
        "contact_deltas_unity_minus_direct": contact_deltas,
        "direct_vs_unity_computed_rows": direct_vs_unity_rows,
        "raw_solver_rows_minus_direct_computed_rows": raw_vs_direct_rows,
        "raw_header_normal_minus_direct_contact0": header_normal_delta,
        "direct_computed_rows": direct_rows,
        "unity_computed_rows": unity_rows,
        "raw_header": raw_header,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver-state", type=Path, default=DEFAULT_SOLVER_STATE)
    parser.add_argument("--direct-pcm", type=Path, default=DEFAULT_DIRECT_PCM)
    parser.add_argument("--case-name", default="local_4776_grb_unity_native_rawseed")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(args.solver_state, args.direct_pcm, args.case_name)
    print(json.dumps({"summary": report["summary"]}, indent=2, ensure_ascii=False))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
