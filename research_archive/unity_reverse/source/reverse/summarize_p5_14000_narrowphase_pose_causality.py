#!/usr/bin/env python3
"""Preserve the source-level local narrowphase causality check for 14000."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
NATURAL = PROJECT_ROOT / "data" / "calibration" / "_scratch_local_narrowphase_membership_14000.json"
ORACLE = PROJECT_ROOT / "data" / "calibration" / "_scratch_local_narrowphase_membership_oracle_pose_14000.json"
TRUTH = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_entrance_truth_20260710.json"
OUTPUT = PROJECT_ROOT / "data" / "calibration" / "p5_14000_narrowphase_pose_causality_20260711.json"


def yaw_xyzw(q: list[float]) -> float:
    x, y, z, w = (float(value) for value in q)
    return math.atan2(2.0 * (w * y + x * z), 1.0 - 2.0 * (y * y + z * z))


def main() -> int:
    natural_rows = json.loads(NATURAL.read_text(encoding="utf-8"))
    natural = next(row for row in natural_rows if not row["after"])
    oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
    unity = json.loads(TRUTH.read_text(encoding="utf-8"))["rows"][0]["unity_entrance_state"]["active"]

    natural_transform = natural["transform0"]
    oracle_transform = oracle["trace_before"]["transform0"]
    unity_p = [float(value) for value in unity["nativeP"]]
    unity_q = [float(value) for value in unity["nativeQ"]]
    report: dict[str, Any] = {
        "schema": "p5_14000_narrowphase_pose_causality_v1",
        "purpose": (
            "Test at the actual local PxcDiscreteNarrowPhasePCM boundary whether the observed "
            "activation-path transform delta causes the 4-vs-2 manifold split."
        ),
        "policy": "one measured pose correction; no parameter search; oracle is diagnostic only",
        "unityPcmInput": {"position": unity_p, "quaternionXyzw": unity_q},
        "naturalActiveToTarget": {
            "workUnit": {
                key: natural[key]
                for key in ("flags", "status_flags", "geom_type0", "geom_type1", "transform_cache0", "transform_cache1", "np_index")
            },
            "pcmInput": natural_transform,
            "positionDeltaM": [
                float(natural_transform["p"][index]) - unity_p[index] for index in range(3)
            ],
            "yawDeltaRad": yaw_xyzw(natural_transform["q"]) - yaw_xyzw(unity_q),
            "contactCount": int(natural_rows[1]["output_contacts"]),
        },
        "measuredCorrection": {"positionX": 3.0517578125e-05, "yaw": 0.0003027813457833206},
        "diagnosticExactEntrance": {
            "pcmInput": oracle_transform,
            "positionDeltaM": [
                float(oracle_transform["p"][index]) - unity_p[index] for index in range(3)
            ],
            "quaternionComponentDelta": [
                float(oracle_transform["q"][index]) - unity_q[index] for index in range(4)
            ],
            "contactCount": int(oracle["trace_after"]["output_contacts"]),
            "reports": oracle["contact_reports"],
        },
        "conclusion": (
            "The same active->target local Scene path changes from four contacts to two only when its "
            "actual PxcDiscreteNarrowPhasePCM transform-cache input is corrected to Unity. The 8.5mm "
            "solver-facing point displacement is therefore downstream of activation-path micro-pose handoff, "
            "not an independent hull, cache or solver-formula discrepancy. The correction is diagnostic and "
            "must not be used in the training backend."
        ),
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "natural": report["naturalActiveToTarget"], "diagnostic": report["diagnosticExactEntrance"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
