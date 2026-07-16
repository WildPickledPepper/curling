#!/usr/bin/env python3
"""Summarize one controlled GameObject.SetActive to first-pair lifecycle run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.extract_pair_lifecycle_timeline import _compact_task_row, _manager_from_finalizer, _native_extra


DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260711_122659" / "events.jsonl"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_setactive_pair_lifecycle_20260711.json"


def _events(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                yield line_number, json.loads(line)


def _text(event: dict[str, Any]) -> str:
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    return str(data.get("textPreview") or "")


def _activation(event: dict[str, Any]) -> dict[str, Any]:
    data = event["data"]
    preview = ((data.get("gameObjectWindowAfter") or {}).get("u32Preview") or [])
    native = data.get("nativeGameObjectAfter") or {}
    components = native.get("components") if isinstance(native, dict) else None
    return {
        "line": event["line"],
        "t": event["t"],
        "callIndex": data.get("callIndex"),
        "managedGameObject": data.get("objectPtr"),
        # func79964 (GameObject::GetCachedPtr) returns managedObject[2].
        "nativeGameObject": (
            native.get("nativeGameObjectPtr")
            if isinstance(native, dict)
            else (preview[2] if len(preview) > 2 else None)
        ),
        "active": data.get("active"),
        "nativeComponentEntries": native.get("componentEntriesPtr") if isinstance(native, dict) else None,
        "nativeComponentCount": native.get("componentCount") if isinstance(native, dict) else None,
        "activationRegistry": native.get("activationRegistryPtr") if isinstance(native, dict) else None,
        "activationResolverProvider": native.get("activationResolverProvider") if isinstance(native, dict) else None,
        "activationResolverTableIndex": native.get("activationResolverTableIndex") if isinstance(native, dict) else None,
        "components": [
            {
                "entryIndex": component.get("entryIndex"),
                "typeId": component.get("componentTypeId"),
                "typeKey": component.get("componentTypeKey"),
                "componentPtr": component.get("componentPtr"),
                "vtablePtr": component.get("vtablePtr"),
                "activationCallbackTableIndex": component.get("activationCallbackTableIndex"),
            }
            for component in components
            if isinstance(component, dict)
        ]
        if isinstance(components, list)
        else [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    reset_time: float | None = None
    bestshot_time: float | None = None
    reset_activations: list[dict[str, Any]] = []
    bestshot_activations: list[dict[str, Any]] = []
    tasks: list[tuple[int, float, dict[str, Any]]] = []
    finalizers: list[tuple[int, float, int, dict[str, Any]]] = []

    for line, event in _events(args.events):
        event["line"] = line
        data = event.get("data") if isinstance(event.get("data"), dict) else {}
        event_type = event.get("type")
        if event_type == "websocket.recv":
            text = _text(event)
            if text.startswith("RESETPOSITION "):
                reset_time = float(event["t"])
                bestshot_time = None
            elif text.startswith("BESTSHOT "):
                bestshot_time = float(event["t"])
        elif event_type == "game_object.set_active.after":
            row = _activation(event)
            if bestshot_time is not None and row["t"] >= bestshot_time:
                bestshot_activations.append(row)
            elif reset_time is not None and row["t"] >= reset_time:
                reset_activations.append(row)
        elif event_type == "physx.native.before" and (data.get("hook") or {}).get("name") == "PxsContext.contactManagerDiscreteUpdate":
            task = _native_extra(data, "PxsContext.contactManagerDiscreteUpdate.task").get("task") or {}
            tasks.append((line, float(event["t"]), task))
        elif event_type == "physx.native.after" and (data.get("hook") or {}).get("name") == "createFinalizeSolverContacts":
            manager = _manager_from_finalizer(data)
            if manager is not None:
                finalizers.append((line, float(event["t"]), manager, data))

    if bestshot_time is None:
        raise ValueError("no BESTSHOT message found")
    first_finalizer = next((item for item in finalizers if item[1] >= bestshot_time), None)
    if first_finalizer is None:
        raise ValueError("no stone-stone finalizer found after BESTSHOT")
    final_line, final_time, manager_ptr, final_data = first_finalizer
    appearances: list[dict[str, Any]] = []
    for line, timestamp, task in tasks:
        if not (bestshot_time <= timestamp <= final_time):
            continue
        for manager in task.get("managers") or []:
            if manager.get("contactManagerPtr") == manager_ptr:
                appearances.append({"line": line, "t": timestamp, "state": _compact_task_row(manager)})

    desc = _native_extra(final_data, "createFinalizeSolverContacts.contactDesc")
    report = {
        "schema": "unity_setactive_pair_lifecycle_v1",
        "purpose": "Prove the runtime order from reset/activation through the first new-list pair.",
        "events": str(args.events),
        "resetActivationEvents": reset_activations,
        "bestshotActivationEvents": bestshot_activations,
        "firstFinalizer": {
            "line": final_line,
            "t": final_time,
            "contactManager": manager_ptr,
            "shapeInteraction": desc.get("shapeInteractionPtr"),
            "contactCount": desc.get("numContacts"),
        },
        "managerTaskAppearances": appearances,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), **report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
