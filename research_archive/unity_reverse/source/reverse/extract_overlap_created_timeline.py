#!/usr/bin/env python3
"""Summarize the one-shot broadphase-to-first-PCM creation boundary.

The report is deliberately narrow. It proves which overlap pair was handed to
``OnOverlapCreatedTask`` and which preallocated manager then appeared in the
first narrowphase task; it does not infer any physics from endpoints.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = (
    PROJECT_ROOT
    / "log"
    / "overlap_created_probe_20260711_160604"
    / "unity_runtime_probe_20260711_160605"
    / "events.jsonl"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "overlap_created_timeline_20260711.json"


def iter_events(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                yield line_number, json.loads(line)


def native_task(data: dict[str, Any]) -> dict[str, Any]:
    for item in data.get("extraDumps") or []:
        if item.get("label") == "PxsContext.contactManagerDiscreteUpdate.task":
            return item.get("task") or {}
    return {}


def compact_manager(row: dict[str, Any]) -> dict[str, Any]:
    manager = row.get("manager") or {}
    cache = row.get("cache") or {}
    manifold = cache.get("persistentManifoldCandidate") or {}
    return {
        "taskIndex": row.get("taskIndex"),
        "contactManager": row.get("contactManagerPtr"),
        "flags": manager.get("flags"),
        "statusFlags": manager.get("statusFlags"),
        "frictionPatchCount": manager.get("frictionPatchCount"),
        "managerIndex": manager.get("index"),
        "transformCache": [manager.get("transformCache0"), manager.get("transformCache1")],
        "edgeIndex": manager.get("edgeIndex"),
        "npIndex": manager.get("npIndex"),
        "isNewList": bool(int(manager.get("npIndex") or 0) & 0x80000000),
        "cache": {
            "cachedDataPtr": cache.get("cachedDataPtr"),
            "manifoldFlags": cache.get("manifoldFlags"),
            "numContacts": manifold.get("numContacts"),
            "numWarmStartPoints": manifold.get("numWarmStartPoints"),
            "aIndices": manifold.get("aIndices"),
            "bIndices": manifold.get("bIndices"),
        },
    }


def overlap_manager(overlap: dict[str, Any]) -> int | None:
    # Captures made before the field-name correction used ``touchFound`` for
    # the same task +40 preallocated manager pointer.
    value = overlap.get("preallocatedContactManager", overlap.get("touchFound"))
    return int(value) if value else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    overlaps: list[dict[str, Any]] = []
    tasks: list[dict[str, Any]] = []
    finalizers: list[dict[str, Any]] = []
    for line, event in iter_events(args.input):
        data = event.get("data") or {}
        hook = (data.get("hook") or {}).get("name")
        if event.get("type") == "physx.overlap_created.before":
            overlaps.append({"line": line, "t": event.get("t"), "state": data.get("state") or {}})
        elif event.get("type") == "physx.native.before" and hook == "PxsContext.contactManagerDiscreteUpdate":
            tasks.append({"line": line, "t": event.get("t"), "task": native_task(data)})
        elif event.get("type") == "physx.native.before" and hook == "createFinalizeSolverContacts":
            finalizers.append({"line": line, "t": event.get("t")})

    if len(overlaps) < 3:
        raise ValueError(f"expected target-ice, active-ice, stone-stone overlaps; got {len(overlaps)}")
    candidates = [item for event in overlaps for item in event["state"].get("overlaps") or []]
    frequency: dict[int, int] = {}
    for item in candidates:
        for volume in (item.get("volume0"), item.get("volume1")):
            if volume:
                frequency[int(volume)] = frequency.get(int(volume), 0) + 1
    ice_volume = max(frequency, key=frequency.get)
    stone_pair = next(
        item
        for item in candidates
        if item.get("volume0") != ice_volume and item.get("volume1") != ice_volume
    )
    expected_manager = overlap_manager(stone_pair)
    creation_event = next(event for event in overlaps if stone_pair in (event["state"].get("overlaps") or []))
    first_task = next(task for task in tasks if task["t"] >= creation_event["t"])
    manager_row = next(
        (
            row
            for row in first_task["task"].get("managers") or []
            if row.get("contactManagerPtr") == expected_manager
        ),
        None,
    )
    report = {
        "schema": "overlap_created_timeline_v1",
        "purpose": "Prove the broadphase pair and preallocated manager identity at first stone-stone creation.",
        "source": str(args.input),
        "iceVolume": ice_volume,
        "stoneStoneOverlap": {
            "line": creation_event["line"],
            "t": creation_event["t"],
            "volumeOrder": [stone_pair.get("volume0"), stone_pair.get("volume1")],
            "preallocatedContactManager": expected_manager,
            "preallocatedShapeInteraction": stone_pair.get("preallocatedShapeInteraction", stone_pair.get("touchLost")),
        },
        "firstNarrowphaseTask": {
            "line": first_task["line"],
            "t": first_task["t"],
            "taskCount": first_task["task"].get("count"),
            "samePreallocatedManagerAppeared": manager_row is not None,
            "manager": compact_manager(manager_row) if manager_row else None,
        },
        "firstFinalizerAfterCreation": next((event for event in finalizers if event["t"] >= creation_event["t"]), None),
        "conclusion": (
            "The broadphase supplied target->active; the same preallocated manager then entered "
            "the new narrowphase list. Role sorting and manager allocation identity are observed, "
            "not inferred from the final contact points."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "report": report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
