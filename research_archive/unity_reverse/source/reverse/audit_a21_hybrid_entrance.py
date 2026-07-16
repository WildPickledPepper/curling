#!/usr/bin/env python3
"""Compare rebuilt hybrid first-PCM entrances with the captured Unity session.

This is an A21 boundary audit.  It does not run a Scene and does not inject any
Unity data.  Unity's first positive convex-convex PCM call in each BESTSHOT
interval is the consumer-side truth for P/Q; the rebuilt hybrid report provides
the corresponding local active actor state immediately before its first contact.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = ROOT / "log/unity_runtime_probe_20260710_012403/events.jsonl"
DEFAULT_SOLVER_STATE = ROOT / "data/calibration/front_half_pcm_solver_state_20260710.json"
DEFAULT_HYBRID = ROOT / "data/calibration/a21_hybrid_a19_snapshot_sixshot_14000_14005_20260712.json"
DEFAULT_OUTPUT = ROOT / "data/calibration/a21_hybrid_entrance_14000_14005_20260712.json"

BESTSHOT_RE = re.compile(r"BESTSHOT\s+[-+0-9.eE]+\s+[-+0-9.eE]+\s+[-+0-9.eE]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--solver-state", type=Path, default=DEFAULT_SOLVER_STATE)
    parser.add_argument("--hybrid", type=Path, default=DEFAULT_HYBRID)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--position-tolerance", type=float, default=1e-6)
    parser.add_argument("--quaternion-tolerance", type=float, default=6e-7)
    return parser.parse_args()


def _json(value: Path) -> Any:
    return json.loads(value.read_text(encoding="utf-8"))


def bestshot_times(path: Path) -> list[float]:
    """Read only protocol BESTSHOT records; avoid loading the 1 GiB event log."""
    values: list[float] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if "BESTSHOT" not in line:
                continue
            event = json.loads(line)
            text = str(event.get("preview") or event.get("data") or event)
            if BESTSHOT_RE.search(text):
                values.append(float(event["t"]))
    return values


def _contact_count(row: dict[str, Any]) -> int:
    buffer = (row.get("pcmInputs") or {}).get("contactBuffer") or {}
    candidate = buffer.get("candidate") or {}
    return int(candidate.get("count") or 0)


def unity_first_contacts(state: dict[str, Any], starts: list[float]) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in state["pcmContactRows"]
        if row.get("hook") == "PxcPCMContactConvexConvex"
        and row.get("phase") == "after"
        and _contact_count(row) > 0
    ]
    result: list[dict[str, Any]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else math.inf
        matching = [row for row in candidates if start <= float(row["t"]) < end]
        if not matching:
            raise RuntimeError(f"no positive Unity convex-convex PCM call in BESTSHOT interval {index}")
        result.append(min(matching, key=lambda row: float(row["t"])))
    return result


def max_component_delta(left: list[float], right: list[float]) -> float:
    return max(abs(float(a) - float(b)) for a, b in zip(left, right))


def local_quaternion_xyzw(active: dict[str, Any]) -> list[float]:
    # Hybrid report stores PhysX quaternion as [w, x, y, z].
    w, x, y, z = [float(value) for value in active["quaternionWxyz"]]
    return [x, y, z, w]


def main() -> int:
    args = parse_args()
    hybrid = _json(args.hybrid)
    state = _json(args.solver_state)
    starts = bestshot_times(args.events)
    rows = hybrid.get("rows") or []
    if len(starts) != len(rows):
        raise RuntimeError(f"BESTSHOT/hybrid row mismatch: {len(starts)} != {len(rows)}")

    unity_rows = unity_first_contacts(state, starts)
    audit_rows: list[dict[str, Any]] = []
    for local_row, unity_row in zip(rows, unity_rows):
        active = local_row["firstContactEntrance"]["active"]
        pcm = unity_row["pcmInputs"]
        unity_p = [float(value) for value in pcm["transform0"]["p"]]
        unity_q = [float(value) for value in pcm["transform0"]["q"]]
        local_p = [float(value) for value in active["physxPosition"]]
        local_q = local_quaternion_xyzw(active)
        pos_delta = max_component_delta(local_p, unity_p)
        quat_delta = max_component_delta(local_q, unity_q)
        local_count = int((local_row.get("firstContactCounts") or [0])[0])
        unity_count = _contact_count(unity_row)
        audit_rows.append(
            {
                "sampleId": int(local_row["sampleId"]),
                "label": local_row["label"],
                "unity": {
                    "pcmCallIndex": int(unity_row["callIndex"]),
                    "pcmTime": float(unity_row["t"]),
                    "position": unity_p,
                    "quaternionXyzw": unity_q,
                    "contactCount": unity_count,
                },
                "hybrid": {
                    "firstContactStep": int(local_row["firstContactStep"]),
                    "position": local_p,
                    "quaternionXyzw": local_q,
                    "linearVelocity": active["physxLinearVelocity"],
                    "angularVelocity": active["physxAngularVelocity"],
                    "contactCount": local_count,
                },
                "delta": {
                    "positionMaxComponent": pos_delta,
                    "quaternionMaxComponent": quat_delta,
                    "contactCount": local_count - unity_count,
                },
                "passesEntranceGate": bool(
                    pos_delta <= args.position_tolerance
                    and quat_delta <= args.quaternion_tolerance
                    and local_count == unity_count
                ),
            }
        )

    first_difference = next((row for row in audit_rows if not row["passesEntranceGate"]), None)
    report = {
        "schema": "a21_hybrid_first_pcm_entrance_v1",
        "purpose": "Validate that the rebuilt hybrid/x64 extension actually carries the A19 patch into first PCM entrance.",
        "scope": "P/Q/contact-count at first positive Unity convex-convex PCM per captured BESTSHOT interval. Unity PCM records do not contain same-boundary actor raw v/w, so local v/w is recorded but not treated as an equality assertion.",
        "inputs": {
            "events": str(args.events),
            "solverState": str(args.solver_state),
            "hybrid": str(args.hybrid),
        },
        "tolerances": {
            "positionMaxComponent": args.position_tolerance,
            "quaternionMaxComponent": args.quaternion_tolerance,
        },
        "allRowsPassEntranceGate": all(row["passesEntranceGate"] for row in audit_rows),
        "firstDifferentSample": None if first_difference is None else first_difference["sampleId"],
        "rows": audit_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "allRowsPassEntranceGate": report["allRowsPassEntranceGate"],
        "firstDifferentSample": report["firstDifferentSample"],
        "rows": [
            {
                "sampleId": row["sampleId"],
                "p": row["delta"]["positionMaxComponent"],
                "q": row["delta"]["quaternionMaxComponent"],
                "count": row["delta"]["contactCount"],
                "pass": row["passesEntranceGate"],
            }
            for row in audit_rows
        ],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
