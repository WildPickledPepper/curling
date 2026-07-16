#!/usr/bin/env python3
"""Audit whether existing C04/C14 artifacts can locate the frame-3 target ULP.

This is intentionally a coverage audit.  It must not splice a C14 static-solver
record from another Unity run into C04's frame-3 core transition.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
C04 = ROOT / "data/calibration/c23_c04_12frame_production_14000_20260712.json"
C14 = ROOT / "data/calibration/c14_static_intercall_14000_20260712.json"
C04_EVENTS = ROOT / "log/c04_dynamic_window_20260712/unity_runtime_probe_20260712_195741/events.jsonl"
OUTPUT = ROOT / "data/calibration/c25_static_only_coverage_14000_20260713.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def event_counts(path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            name = str(row.get("type") or "")
            counts[name] = counts.get(name, 0) + 1
    return counts


def main() -> int:
    c04 = load_json(C04)
    c14 = load_json(C14)
    frame3 = (c04["comparison"]["c04Window"])[3]["target"]
    counts = event_counts(C04_EVENTS)
    dynamic_frames = int(counts.get("c04.dynamic_solver_frame", 0))
    static_frame_events = [
        name for name in counts if "static" in name.lower() and "frame" in name.lower()
    ]

    c04_tick = int(c04["unityCapture"]["tickSerial"])
    c14_tick = int(c14["unityCapture"]["tickSerial"])
    report = {
        "schema": "c25_static_only_coverage_v1",
        "boundary": "C04 frame-2 -> frame-3 target core transition",
        "single_variable": "existing artifact coverage only",
        "expected_discriminator": "same-run target static solver input/writeback/integrate fields",
        "artifacts": {"c04": str(C04), "c14": str(C14), "c04Events": str(C04_EVENTS)},
        "frame3TargetDelta": frame3,
        "c04": {
            "tickSerial": c04_tick,
            "dynamicFrameCount": dynamic_frames,
            "perFrameStaticSolverEvents": static_frame_events,
        },
        "c14": {"tickSerial": c14_tick},
        "sameRun": c04_tick == c14_tick,
        "verdict": {
            "canLocateFirstNativeStaticField": False,
            "reason": (
                "C04 has frame exits but no frame-bound target static solver records; "
                "C14 static records are from a different tick/run and cannot be joined."
            ),
            "nextRequiredEvidence": [
                "target static solver-body before",
                "target static writeback after",
                "target post-integrate core",
            ],
        },
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "sameRun": report["sameRun"], "frame3TargetDelta": frame3}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
