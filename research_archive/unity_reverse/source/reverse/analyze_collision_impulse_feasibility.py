#!/usr/bin/env python3
"""Classify endpoint-inferred early velocity residuals as contact impulses.

The impulse residual report gives the target delta-v needed at 0.02s to land
on Unity's endpoint.  Multiplying by mass gives an equivalent missing impulse.
This script decomposes that impulse into the contact normal/tangent frame and
checks whether the residual looks like a normal-row magnitude error, a tangent
friction-row/cache error, or a mixed contact-manifold error.

The check is diagnostic only.  A difference between two legal PhysX solves is
not itself required to sit inside a Coulomb cone, but large tangent residuals
with tiny normal residuals are strong evidence against "just restitution" or a
single scalar normal impulse mismatch.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_impulse_residual_refresh_20260709.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_impulse_feasibility_refresh_20260709.json"


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _mean(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return sum(rows) / len(rows)


def _rmse(values: Iterable[float]) -> Optional[float]:
    rows = list(values)
    if not rows:
        return None
    return math.sqrt(sum(value * value for value in rows) / len(rows))


def _dominant_axis(normal_impulse: float, tangent_impulse: float) -> str:
    abs_normal = abs(normal_impulse)
    abs_tangent = abs(tangent_impulse)
    if abs_tangent > 1.25 * abs_normal:
        return "tangent"
    if abs_normal > 1.25 * abs_tangent:
        return "normal"
    return "mixed"


def _cone_status(normal_impulse: float, tangent_impulse: float, mu: float) -> str:
    abs_normal = abs(normal_impulse)
    abs_tangent = abs(tangent_impulse)
    if abs_tangent <= mu * abs_normal + 1e-12:
        return "inside_residual_cone"
    if abs_normal <= 1e-9 and abs_tangent > 1e-9:
        return "pure_tangent_outside"
    return "outside_residual_cone"


def _normal_sign(normal_impulse: float) -> str:
    if normal_impulse > 1e-9:
        return "unity_needs_more_normal"
    if normal_impulse < -1e-9:
        return "unity_needs_less_normal"
    return "normal_neutral"


def _classify(row: Dict[str, Any], mu_multiply: float, mu_raw: float) -> str:
    normal_impulse = float(row["required_impulse_normal_Ns"])
    tangent_impulse = float(row["required_impulse_tangent_Ns"])
    dominant = _dominant_axis(normal_impulse, tangent_impulse)
    cone_multiply = _cone_status(normal_impulse, tangent_impulse, mu_multiply)
    cone_raw = _cone_status(normal_impulse, tangent_impulse, mu_raw)
    if dominant == "normal" and abs(tangent_impulse) <= mu_raw * abs(normal_impulse) + 1e-12:
        return "normal_row_plausible"
    if dominant == "tangent" and cone_raw != "inside_residual_cone":
        return "friction_row_or_cache_suspect"
    if dominant == "tangent":
        return "tangent_dominant_but_cone_plausible"
    if cone_multiply == "outside_residual_cone" and cone_raw == "inside_residual_cone":
        return "combine_mode_or_effective_mu_suspect"
    return "mixed_contact_manifold_suspect"


def _extract_current_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    results = payload.get("results") or []
    if not results:
        raise ValueError("impulse report has no results")
    for result in results:
        if result.get("label") in {"unique_role_current_best_refresh", "unique_role_current_best"}:
            return result
    return results[0]


def build_report(input_path: Path, *, mu_multiply: float, mu_raw: float) -> Dict[str, Any]:
    payload = _read_json(input_path)
    result = _extract_current_result(payload)
    rows: List[Dict[str, Any]] = []
    for source in result.get("rows", []):
        if source.get("status") != "ok":
            rows.append(
                {
                    "sample_id": source.get("sample_id"),
                    "status": source.get("status"),
                }
            )
            continue
        normal_impulse = float(source["required_impulse_normal_Ns"])
        tangent_impulse = float(source["required_impulse_tangent_Ns"])
        normal_abs = abs(normal_impulse)
        tangent_abs = abs(tangent_impulse)
        ratio = None if normal_abs <= 1e-12 else tangent_abs / normal_abs
        support_normal_multiply = tangent_abs / mu_multiply if mu_multiply > 0.0 else None
        support_normal_raw = tangent_abs / mu_raw if mu_raw > 0.0 else None
        row = {
            "sample_id": int(source["sample_id"]),
            "label": source.get("label"),
            "status": "ok",
            "target_error_m": source.get("target_error_m"),
            "endpoint_error_m": source.get("endpoint_error_m"),
            "required_delta_v_norm_mps": source.get("delta_v_required_norm_mps"),
            "required_impulse_norm_Ns": source.get("required_impulse_norm_Ns"),
            "required_impulse_normal_Ns": normal_impulse,
            "required_impulse_tangent_Ns": tangent_impulse,
            "abs_tangent_over_abs_normal": ratio,
            "normal_sign": _normal_sign(normal_impulse),
            "dominant_axis": _dominant_axis(normal_impulse, tangent_impulse),
            "cone_status_mu_multiply": _cone_status(normal_impulse, tangent_impulse, mu_multiply),
            "cone_status_mu_raw": _cone_status(normal_impulse, tangent_impulse, mu_raw),
            "normal_impulse_needed_to_support_tangent_mu_multiply_Ns": support_normal_multiply,
            "normal_impulse_needed_to_support_tangent_mu_raw_Ns": support_normal_raw,
            "support_gap_mu_multiply_Ns": None if support_normal_multiply is None else support_normal_multiply - normal_abs,
            "support_gap_mu_raw_Ns": None if support_normal_raw is None else support_normal_raw - normal_abs,
            "classification": _classify(source, mu_multiply, mu_raw),
            "tail_direction_delta_deg_required": source.get("tail_direction_delta_deg_required"),
            "tail_distance_scale_required": source.get("tail_distance_scale_required"),
            "contact_normal_to_unity_disp_deg": source.get("contact_normal_to_unity_disp_deg"),
            "early_velocity_to_contact_normal_deg": source.get("early_velocity_to_contact_normal_deg"),
        }
        rows.append(row)

    ok = [row for row in rows if row.get("status") == "ok"]
    classifications: Dict[str, int] = {}
    normal_signs: Dict[str, int] = {}
    cone_counts_multiply: Dict[str, int] = {}
    cone_counts_raw: Dict[str, int] = {}
    for row in ok:
        classifications[row["classification"]] = classifications.get(row["classification"], 0) + 1
        normal_signs[row["normal_sign"]] = normal_signs.get(row["normal_sign"], 0) + 1
        cone_counts_multiply[row["cone_status_mu_multiply"]] = cone_counts_multiply.get(row["cone_status_mu_multiply"], 0) + 1
        cone_counts_raw[row["cone_status_mu_raw"]] = cone_counts_raw.get(row["cone_status_mu_raw"], 0) + 1

    def vals(key: str) -> List[float]:
        return [float(row[key]) for row in ok if row.get(key) is not None]

    worst = sorted(ok, key=lambda row: float(row.get("endpoint_error_m") or 0.0), reverse=True)[:5]
    return {
        "input": str(input_path.relative_to(PROJECT_ROOT)),
        "source_label": result.get("label"),
        "mu_assumptions": {
            "multiply_stone_stone": mu_multiply,
            "raw_stone_material": mu_raw,
            "note": "Unity asset material is 0.6/0.6 and combine mode is Multiply in current probes, so stone-stone effective friction is expected near 0.36; raw 0.6 is kept as a generous upper bound.",
        },
        "summary": {
            "row_count": len(rows),
            "ok_count": len(ok),
            "classification_counts": classifications,
            "normal_sign_counts": normal_signs,
            "cone_counts_mu_multiply": cone_counts_multiply,
            "cone_counts_mu_raw": cone_counts_raw,
            "abs_tangent_over_abs_normal_mean": _mean(vals("abs_tangent_over_abs_normal")),
            "support_gap_mu_multiply_rmse_Ns": _rmse(vals("support_gap_mu_multiply_Ns")),
            "support_gap_mu_raw_rmse_Ns": _rmse(vals("support_gap_mu_raw_Ns")),
            "normal_impulse_rmse_Ns": _rmse(vals("required_impulse_normal_Ns")),
            "tangent_impulse_rmse_Ns": _rmse(vals("required_impulse_tangent_Ns")),
        },
        "worst_rows": worst,
        "rows": rows,
        "interpretation": [
            "normal_row_plausible points at normal row magnitude, restitution, separation bias, or contact normal.",
            "friction_row_or_cache_suspect means tangent residual dominates and exceeds even a generous residual friction cone; this points at friction anchors/cache/tangent basis/contact points rather than restitution alone.",
            "mixed_contact_manifold_suspect means normal and tangent both matter, so first ContactBuffer plus solver rows are needed.",
            "The residual impulse is a difference between Unity and local solves, so cone violations are not formal impossibility proofs; they are prioritization evidence.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--mu-multiply", type=float, default=0.36)
    parser.add_argument("--mu-raw", type=float, default=0.6)
    args = parser.parse_args()

    input_path = args.input if args.input.is_absolute() else PROJECT_ROOT / args.input
    output_path = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    report = build_report(input_path, mu_multiply=args.mu_multiply, mu_raw=args.mu_raw)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {output_path.relative_to(PROJECT_ROOT)}")
    print("classification_counts=" + json.dumps(report["summary"]["classification_counts"], sort_keys=True))
    print("cone_counts_mu_multiply=" + json.dumps(report["summary"]["cone_counts_mu_multiply"], sort_keys=True))
    print("normal_sign_counts=" + json.dumps(report["summary"]["normal_sign_counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
