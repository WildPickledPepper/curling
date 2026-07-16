#!/usr/bin/env python3
"""Extract the SetActive-to-MeshCollider bridge timeline from a runtime log.

This is a read-only parser.  It does not infer a physical parameter from contact
counts: it associates the target/active GameObject.SetActive calls with the
three recovered MeshCollider virtual entries (slots 44, 43 and 42).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = (
    PROJECT_ROOT
    / "log"
    / "mesh_collider_activation_probe_20260711"
    / "unity_runtime_probe_20260711_140850"
    / "events.jsonl"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "mesh_collider_bridge_timeline.json"

SET_ACTIVE_EVENT = "game_object.set_active.before"
BRIDGE_EVENTS = {
    "mesh_collider.activation.before": "slot44_activation",
    "mesh_collider.transform_refresh.before": "slot43_transform_refresh",
    "mesh_collider.state_refresh.before": "slot42_state_refresh",
}


def _read_events(path: Path) -> list[tuple[int, dict[str, Any]]]:
    events: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            events.append((line_number, value))
    return events


def _mesh_component(data: dict[str, Any]) -> int | None:
    native = data.get("nativeGameObject")
    if not isinstance(native, dict):
        return None
    components = native.get("components")
    if not isinstance(components, list):
        return None
    for component in components:
        if not isinstance(component, dict) or component.get("componentTypeId") != 20:
            continue
        pointer = component.get("componentPtr")
        return int(pointer) if isinstance(pointer, int) else None
    return None


def _changed_raw_bytes(before: Any, after: Any) -> list[int] | None:
    if not isinstance(before, dict) or not isinstance(after, dict):
        return None
    before_raw = before.get("rawBytes")
    after_raw = after.get("rawBytes")
    if not isinstance(before_raw, list) or not isinstance(after_raw, list):
        return None
    if len(before_raw) != len(after_raw):
        return None
    return [index for index, (left, right) in enumerate(zip(before_raw, after_raw)) if left != right]


def _bridge_record(line_number: int, event: dict[str, Any]) -> dict[str, Any]:
    data = event.get("data")
    if not isinstance(data, dict):
        return {"line": line_number, "malformed": True}
    state = data.get("state")
    if not isinstance(state, dict):
        state = data.get("before") if isinstance(data.get("before"), dict) else {}
    component = state.get("componentPtr")
    args = data.get("args")
    if isinstance(args, list) and args and isinstance(args[0], int):
        component = args[0]
    return {
        "line": line_number,
        "timeMs": event.get("t"),
        "kind": BRIDGE_EVENTS.get(event.get("type"), event.get("type")),
        "componentPtr": component,
        "gameObjectPtr": state.get("gameObjectPtr"),
        "colliderBackendPtr": state.get("colliderBackendPtr"),
        "args": args,
        "enabledBit": state.get("enabledBit"),
        "activationBit": state.get("activationBit"),
        "componentChangedOffsets": _changed_raw_bytes(
            (data.get("before") or {}).get("componentWindow"),
            (data.get("after") or {}).get("componentWindow"),
        ),
        "backendChangedOffsets": _changed_raw_bytes(
            (data.get("before") or {}).get("backendWindow"),
            (data.get("after") or {}).get("backendWindow"),
        ),
    }


def _activation_record(line_number: int, event: dict[str, Any]) -> dict[str, Any]:
    data = event["data"]
    native = data.get("nativeGameObject") or {}
    return {
        "line": line_number,
        "timeMs": event.get("t"),
        "callIndex": data.get("callIndex"),
        "active": data.get("active"),
        "managedGameObjectPtr": data.get("objectPtr"),
        "nativeGameObjectPtr": native.get("nativeGameObjectPtr"),
        "meshColliderPtr": _mesh_component(data),
    }


def _nearest_prior_activation(
    bridge: dict[str, Any], activations: list[dict[str, Any]]
) -> dict[str, Any] | None:
    component = bridge.get("componentPtr")
    time_ms = bridge.get("timeMs")
    matches = [
        item
        for item in activations
        if item.get("meshColliderPtr") == component
        and isinstance(time_ms, (int, float))
        and isinstance(item.get("timeMs"), (int, float))
        and item["timeMs"] <= time_ms
    ]
    if not matches:
        return None
    match = max(matches, key=lambda item: float(item["timeMs"]))
    # Keep the event relation acyclic: role records later attach bridgeCalls.
    return {
        key: match.get(key)
        for key in (
            "line",
            "timeMs",
            "callIndex",
            "active",
            "managedGameObjectPtr",
            "nativeGameObjectPtr",
            "meshColliderPtr",
        )
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--target-call-index",
        type=int,
        default=30,
        help="Known target SetActive(true) call in this controlled 14000 run.",
    )
    parser.add_argument(
        "--active-call-index",
        type=int,
        default=38,
        help="Known active SetActive(true) call in this controlled 14000 run.",
    )
    args = parser.parse_args()

    events = _read_events(args.events)
    activations = [
        _activation_record(line_number, event)
        for line_number, event in events
        if event.get("type") == SET_ACTIVE_EVENT
        and isinstance(event.get("data"), dict)
    ]
    bridges = [
        _bridge_record(line_number, event)
        for line_number, event in events
        if event.get("type") in BRIDGE_EVENTS
    ]
    for bridge in bridges:
        bridge["nearestPriorSetActive"] = _nearest_prior_activation(bridge, activations)

    by_call = {item.get("callIndex"): item for item in activations}
    target = by_call.get(args.target_call_index)
    active = by_call.get(args.active_call_index)
    roles = {
        "target": target,
        "active": active,
    }
    for role, activation in roles.items():
        if not isinstance(activation, dict):
            continue
        component = activation.get("meshColliderPtr")
        activation["bridgeCalls"] = [
            bridge for bridge in bridges if bridge.get("componentPtr") == component
        ]
        activation["role"] = role

    report = {
        "schema": "mesh_collider_bridge_timeline_v1",
        "events": str(args.events),
        "targetCallIndex": args.target_call_index,
        "activeCallIndex": args.active_call_index,
        "roles": roles,
        "allBridgeCalls": bridges,
        "interpretation": (
            "A missing slot44 call is not evidence of a missing collider refresh. "
            "Only the same component's slot43/slot42 records determine its actual bridge path."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
