#!/usr/bin/env python3
"""Extract first dynamic-pair manager-task state for the six controlled shots."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCES = (
    (
        (14000,),
        PROJECT_ROOT / "log" / "unity_runtime_probe_20260711_114806" / "events.jsonl",
    ),
    (
        (14001, 14002, 14003, 14004, 14005),
        PROJECT_ROOT / "log" / "unity_runtime_probe_20260711_115331" / "events.jsonl",
    ),
)
OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_pair_lifecycle_timeline_20260711.json"


def _native_extra(data: dict[str, Any], label: str) -> dict[str, Any]:
    for item in data.get("extraDumps") or []:
        if isinstance(item, dict) and item.get("label") == label:
            return item
    return {}


def _manager_from_finalizer(data: dict[str, Any]) -> int | None:
    desc = _native_extra(data, "createFinalizeSolverContacts.contactDesc")
    raw = ((desc.get("shapeInteractionWindow") or {}).get("rawBytes") or [])
    if len(raw) < 60:
        return None
    return int.from_bytes(bytes(int(value) & 0xFF for value in raw[56:60]), "little")


def _compact_task_row(row: dict[str, Any]) -> dict[str, Any]:
    manager = row.get("manager") or {}
    cache = row.get("cache") or {}
    manifold = cache.get("persistentManifoldCandidate") or {}
    np_index = int(manager.get("npIndex") or 0)
    return {
        "taskIndex": row.get("taskIndex"),
        "contactManager": row.get("contactManagerPtr"),
        "flags": manager.get("flags"),
        "statusFlags": manager.get("statusFlags"),
        "frictionPatchCount": manager.get("frictionPatchCount"),
        "managerIndex": manager.get("index"),
        "transformCache": [manager.get("transformCache0"), manager.get("transformCache1")],
        "edgeIndex": manager.get("edgeIndex"),
        "npIndex": np_index,
        "isNewList": bool(np_index & 0x80000000),
        "npSlot": np_index & 0x7FFFFFFF,
        "cache": {
            "cachedDataPtr": cache.get("cachedDataPtr"),
            "manifoldFlags": cache.get("manifoldFlags"),
            "numContacts": manifold.get("numContacts"),
            "numWarmStartPoints": manifold.get("numWarmStartPoints"),
            "aIndices": manifold.get("aIndices"),
            "bIndices": manifold.get("bIndices"),
        },
    }


def _iter_events(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                yield line_number, json.loads(line)


def _extract_source(sample_ids: tuple[int, ...], path: Path) -> list[dict[str, Any]]:
    shots: list[dict[str, Any]] = []
    tasks: list[dict[str, Any]] = []
    finalizers: list[dict[str, Any]] = []
    for line_number, event in _iter_events(path):
        data = event.get("data") if isinstance(event.get("data"), dict) else {}
        text = str(data.get("textPreview") or "")
        if event.get("type") == "websocket.recv" and text.startswith("BESTSHOT"):
            shots.append({"line": line_number, "t": event.get("t"), "text": text})
            continue
        hook = (data.get("hook") or {}).get("name")
        if event.get("type") == "physx.native.before" and hook == "PxsContext.contactManagerDiscreteUpdate":
            task = _native_extra(data, "PxsContext.contactManagerDiscreteUpdate.task").get("task") or {}
            tasks.append({"line": line_number, "t": event.get("t"), "task": task})
        elif event.get("type") == "physx.native.after" and hook == "createFinalizeSolverContacts":
            manager = _manager_from_finalizer(data)
            desc = _native_extra(data, "createFinalizeSolverContacts.contactDesc")
            if manager:
                finalizers.append(
                    {
                        "line": line_number,
                        "t": event.get("t"),
                        "manager": manager,
                        "shapeInteraction": desc.get("shapeInteractionPtr"),
                        "contactCount": desc.get("numContacts"),
                    }
                )

    if len(shots) != len(sample_ids):
        raise ValueError(f"{path}: expected {len(sample_ids)} BESTSHOT events, got {len(shots)}")
    rows: list[dict[str, Any]] = []
    for index, (sample_id, shot) in enumerate(zip(sample_ids, shots)):
        next_t = shots[index + 1]["t"] if index + 1 < len(shots) else float("inf")
        finals = [
            value for value in finalizers if shot["t"] <= value["t"] < next_t
        ]
        if not finals:
            rows.append(
                {
                    "sampleId": sample_id,
                    "bestshot": shot,
                    "error": "no dynamic-dynamic finalizer captured",
                }
            )
            continue
        first_final = finals[0]
        appearances: list[dict[str, Any]] = []
        for task_event in tasks:
            if not (shot["t"] <= task_event["t"] <= first_final["t"]):
                continue
            for manager in task_event["task"].get("managers") or []:
                if manager.get("contactManagerPtr") == first_final["manager"]:
                    appearances.append(
                        {
                            "line": task_event["line"],
                            "t": task_event["t"],
                            "state": _compact_task_row(manager),
                        }
                    )
        rows.append(
            {
                "sampleId": sample_id,
                "bestshot": shot,
                "firstFinalizer": first_final,
                "finalizerCountInShot": len(finals),
                "taskAppearancesBeforeFirstFinalizer": appearances,
                "firstTaskAppearance": appearances[0] if appearances else None,
            }
        )
    return rows


def main() -> int:
    rows: list[dict[str, Any]] = []
    for sample_ids, path in SOURCES:
        if not path.exists():
            raise FileNotFoundError(path)
        rows.extend(_extract_source(sample_ids, path))
    report = {
        "schema": "unity_pair_lifecycle_timeline_v1",
        "purpose": (
            "Locate the first PxsCMDiscreteUpdateTask appearance of each controlled "
            "stone-stone contact manager without inferring lifecycle from endpoint data."
        ),
        "sources": [str(path) for _ids, path in SOURCES],
        "rows": rows,
        "summary": [
            {
                "sampleId": row["sampleId"],
                "manager": (row.get("firstFinalizer") or {}).get("manager"),
                "firstTaskState": (row.get("firstTaskAppearance") or {}).get("state"),
                "appearanceCount": len(row.get("taskAppearancesBeforeFirstFinalizer") or []),
                "finalizerCount": row.get("finalizerCountInShot"),
                "error": row.get("error"),
            }
            for row in rows
        ],
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "summary": report["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
