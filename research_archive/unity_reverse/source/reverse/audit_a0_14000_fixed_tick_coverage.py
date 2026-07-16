#!/usr/bin/env python3
"""Audit whether existing Unity 14000 logs cover the A-chain fixed-tick boundary.

This is a read-only inventory. It deliberately does not merge values from different
Unity runs: a field is useful for A2 only when the same source session captures it
with an unambiguous relation to the first stone-stone PCM boundary.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "events.jsonl"
DEFAULT_SUMMARY = DEFAULT_EVENTS.with_name("front_half_pcm_summary.json")
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "calibration" / "a0_14000_fixed_tick_coverage_20260711.json"
)


def event_name(event: dict[str, Any]) -> str:
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    hook = data.get("hook") if isinstance(data.get("hook"), dict) else {}
    return str(hook.get("name") or event.get("type") or "<unknown>")


def evidence(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "line": row["line"],
        "t": row["t"],
        "phase": row["phase"],
        "name": row["name"],
    }


def latest_before(rows: list[dict[str, Any]], t: float) -> dict[str, Any] | None:
    eligible = [row for row in rows if isinstance(row["t"], (int, float)) and row["t"] <= t]
    return max(eligible, key=lambda row: (float(row["t"]), row["line"]), default=None)


def find_sample_14000(summary: dict[str, Any]) -> dict[str, Any]:
    for shot in summary.get("shots") or []:
        plan = shot.get("plan") if isinstance(shot.get("plan"), dict) else {}
        if plan.get("sample_id") == 14000:
            return shot
    raise ValueError("front_half_pcm_summary has no sample_id=14000 shot")


def audit(events_path: Path, summary_path: Path) -> dict[str, Any]:
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    shot = find_sample_14000(summary)
    first_pcm = shot.get("firstPcmBefore")
    if not isinstance(first_pcm, dict) or not isinstance(first_pcm.get("t"), (int, float)):
        raise ValueError("sample 14000 has no firstPcmBefore timestamp")
    boundary_t = float(first_pcm["t"])

    by_name: dict[str, list[dict[str, Any]]] = {}
    type_counts: Counter[str] = Counter()
    raw_mentions: dict[str, list[dict[str, Any]]] = {
        "Newfrictionstep": [],
        "PxsTransformCache": [],
        "sliding.fixed_update": [],
    }
    with events_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            data = event.get("data") if isinstance(event.get("data"), dict) else {}
            row = {
                "line": line_number,
                "t": event.get("t"),
                "phase": data.get("phase"),
                "name": event_name(event),
            }
            by_name.setdefault(row["name"], []).append(row)
            type_counts[row["name"]] += 1
            for token in raw_mentions:
                if token in line:
                    raw_mentions[token].append(row)

    def hook_rows(name: str) -> list[dict[str, Any]]:
        return by_name.get(name, [])

    stone_ice = hook_rows("PxcPCMContactConvexMesh")
    static_writeback = hook_rows("solveContact_BStaticBlockWithWriteback")
    stone_stone = hook_rows("PxcPCMContactConvexConvex")
    friction_rng = hook_rows("sliding.random_range.friction")
    fixed_updates = [
        row
        for name, rows in by_name.items()
        if name.startswith("sliding.fixed_update")
        for row in rows
    ]
    first_stone_stone = latest_before(stone_stone, boundary_t)

    coverage = [
        {
            "field": "post_Newfrictionstep_Rigidbody_v_w",
            "status": "missing",
            "sameShotEvidence": evidence(latest_before(friction_rng, boundary_t)),
            "reason": (
                "The run records friction RNG calls, not the Newfrictionstep write or the "
                "Rigidbody linear/angular velocity after that write."
            ),
        },
        {
            "field": "last_precontact_fixed_tick_identifier",
            "status": "missing",
            "sameShotEvidence": evidence(latest_before(fixed_updates, boundary_t)),
            "reason": (
                "The summary reports fixedUpdateEnterCount=0 and the event stream contains no "
                "sliding.fixed_update enter/exit event. Hook timestamps alone cannot prove that "
                "stone-ice and static-solver calls belong to the final pre-contact fixed tick."
            ),
        },
        {
            "field": "stone_ice_PCM_input_output",
            "status": "partial",
            "sameShotEvidence": {
                "firstCaptured": evidence(stone_ice[0] if stone_ice else None),
                "count": len(stone_ice),
            },
            "reason": (
                "PxcPCMContactConvexMesh before/after hooks exist in this armed 14000 session, "
                "but no fixed-tick marker or active-body join identifies the last pre-contact call."
            ),
        },
        {
            "field": "static_solver_before_after_body_state",
            "status": "partial",
            "sameShotEvidence": {
                "firstCaptured": evidence(static_writeback[0] if static_writeback else None),
                "count": len(static_writeback),
            },
            "reason": (
                "Static with-writeback hooks and body windows exist, but the current stream does "
                "not bind a selected active-body call to the final pre-contact fixed tick."
            ),
        },
        {
            "field": "post_sim_actor_P_Q",
            "status": "missing",
            "sameShotEvidence": None,
            "reason": (
                "No actor-core post-sim pose hook or fixed-update exit pose snapshot is present. "
                "The later stone-stone PCM transform cannot prove the actor-core write boundary."
            ),
        },
        {
            "field": "first_stone_stone_PCM_transform_P_Q",
            "status": "available",
            "sameShotEvidence": evidence(first_stone_stone),
            "reason": (
                "The sample summary and convex-convex PCM before dump contain the first stone-stone "
                "PxTransform values. This is the endpoint of chain A, not proof of its producer."
            ),
        },
        {
            "field": "actor_to_PxsTransformCache_write_order",
            "status": "missing",
            "sameShotEvidence": evidence(raw_mentions["PxsTransformCache"][0] if raw_mentions["PxsTransformCache"] else None),
            "reason": (
                "No existing event names or payload text identify an actor-to-PxsTransformCache write "
                "or a cache-slot update order for the selected final tick."
            ),
        },
    ]

    missing = [row["field"] for row in coverage if row["status"] == "missing"]
    return {
        "schema": "a0_14000_fixed_tick_coverage_v1",
        "purpose": (
            "Read-only coverage audit for chain A. Do not combine different Unity sessions into a "
            "synthetic fixed-tick trace."
        ),
        "inputs": {"events": str(events_path), "summary": str(summary_path)},
        "sample": {
            "sampleId": 14000,
            "label": (shot.get("plan") or {}).get("label"),
            "firstStoneStonePcm": {
                "t": boundary_t,
                "callIndex": first_pcm.get("callIndex"),
                "transform0": first_pcm.get("transform0"),
                "transform1": first_pcm.get("transform1"),
            },
        },
        "eventCounts": dict(type_counts),
        "coverage": coverage,
        "missingFields": missing,
        "decision": {
            "a0Complete": True,
            "a2Eligible": False,
            "reason": (
                "Existing logs establish the chain endpoint and partial stone-ice/static-solver "
                "coverage, but cannot identify the first differing A-chain field in one fixed tick."
            ),
            "nextAllowedWork": (
                "Design a minimum read-only capture schema for the missing fields; do not launch Unity "
                "or change production physics until that schema is reviewed."
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = audit(args.events, args.summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "missingFields": report["missingFields"], "decision": report["decision"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
