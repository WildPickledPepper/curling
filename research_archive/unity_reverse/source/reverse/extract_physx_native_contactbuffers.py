#!/usr/bin/env python3
"""Extract plausible ContactBuffer snapshots from Unity WebGL native probe events."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


def iter_pointer_windows(windows: Any) -> Iterable[dict[str, Any]]:
    if not isinstance(windows, list):
        return
    for window in windows:
        if not isinstance(window, dict):
            continue
        yield window
        yield from iter_pointer_windows(window.get("pointerTargets"))


def finite_vec(value: Any, size: int = 3) -> bool:
    return (
        isinstance(value, list)
        and len(value) == size
        and all(isinstance(x, (int, float)) and math.isfinite(x) for x in value)
    )


def normal_len(contact: dict[str, Any]) -> float | None:
    normal = contact.get("normal")
    if not finite_vec(normal):
        return None
    return math.sqrt(sum(float(x) * float(x) for x in normal))


def point_in_rink_world(point: Any) -> bool:
    # The Unity world rink in this build sits near x=-100..-60, y=14, z=50..60.
    return (
        finite_vec(point)
        and -140.0 <= float(point[0]) <= -40.0
        and 0.0 <= float(point[1]) <= 30.0
        and 20.0 <= float(point[2]) <= 80.0
    )


def first_contact(candidate: dict[str, Any]) -> dict[str, Any] | None:
    contacts = candidate.get("contactsPreview")
    if isinstance(contacts, list) and contacts and isinstance(contacts[0], dict):
        return contacts[0]
    return None


def plausible_candidate(candidate: dict[str, Any]) -> bool:
    contact = first_contact(candidate)
    if contact is None:
        return False
    n_len = normal_len(contact)
    separation = contact.get("separation")
    return (
        n_len is not None
        and 0.75 <= n_len <= 1.25
        and isinstance(separation, (int, float))
        and math.isfinite(separation)
        and -0.5 <= float(separation) <= 0.5
        and point_in_rink_world(contact.get("point"))
    )


def contact_material(contact: dict[str, Any]) -> dict[str, Any]:
    return {
        "staticFriction": contact.get("staticFriction"),
        "dynamicFriction": contact.get("dynamicFriction"),
        "restitution": contact.get("restitution"),
        "maxImpulse": contact.get("maxImpulse"),
    }


def classify_candidate(hook: str, phase: str, candidate: dict[str, Any]) -> str:
    contact = first_contact(candidate) or {}
    normal = contact.get("normal") or [0.0, 0.0, 0.0]
    material = contact_material(contact)
    restitution = material.get("restitution")
    dynamic_friction = material.get("dynamicFriction")
    if hook == "PxcPCMContactConvexConvex":
        return "stone_stone_narrowphase_geometry"
    if hook == "PxcPCMContactConvexMesh":
        return "stone_rink_narrowphase_geometry"
    if hook == "createFinalizeSolverContacts":
        if restitution == 1 and dynamic_friction and dynamic_friction >= 0.3:
            return "stone_stone_finalizer_contactbuffer"
        if abs(float(normal[1])) > 0.75:
            return "stone_rink_finalizer_contactbuffer"
        return "finalizer_contactbuffer_unknown_pair"
    if hook == "createFinalizeSolverContacts4":
        return "solver4_pointer_contactbuffer_candidate"
    return f"{hook}:{phase}"


def summarize_contacts(contacts: list[dict[str, Any]]) -> dict[str, Any]:
    if not contacts:
        return {}
    separations = [
        float(contact["separation"])
        for contact in contacts
        if isinstance(contact.get("separation"), (int, float)) and math.isfinite(contact["separation"])
    ]
    return {
        "contact_count": len(contacts),
        "separation_min": min(separations) if separations else None,
        "separation_max": max(separations) if separations else None,
        "first": contacts[0],
    }


def extract(payload: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for event in payload.get("events", []):
        event_type = event.get("type")
        if event_type not in {"physx.native.before", "physx.native.after"}:
            continue
        data = event.get("data") or {}
        hook = str((data.get("hook") or {}).get("name") or "unknown")
        phase = str(data.get("phase") or "")
        for window in iter_pointer_windows(data.get("pointerWindows")):
            candidate = window.get("contactBufferCandidate")
            if not isinstance(candidate, dict) or not plausible_candidate(candidate):
                continue
            contacts = candidate.get("contactsPreview") or []
            row = {
                "t": event.get("t"),
                "phase": phase,
                "hook": hook,
                "class": classify_candidate(hook, phase, candidate),
                "argIndex": window.get("argIndex"),
                "label": window.get("label"),
                "ptr": window.get("ptr"),
                "sourceOffset": window.get("sourceOffset"),
                "reportedCount": candidate.get("count"),
                "contactsPreview": contacts,
                "summary": summarize_contacts(contacts),
            }
            rows.append(row)

    class_counts = Counter(row["class"] for row in rows)
    hook_counts = Counter(row["hook"] for row in rows)
    return {
        "sourceEventCount": len(payload.get("events", [])),
        "plausibleContactBufferCount": len(rows),
        "classCounts": dict(sorted(class_counts.items())),
        "hookCounts": dict(sorted(hook_counts.items())),
        "firstStoneStoneFinalizer": next(
            (row for row in rows if row["class"] == "stone_stone_finalizer_contactbuffer"),
            None,
        ),
        "firstStoneStoneNarrowphase": next(
            (row for row in rows if row["class"] == "stone_stone_narrowphase_geometry"),
            None,
        ),
        "firstStoneRinkFinalizer": next(
            (row for row in rows if row["class"] == "stone_rink_finalizer_contactbuffer"),
            None,
        ),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    report = extract(payload)
    output = args.output or args.input.with_suffix(".contactbuffers.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "plausibleContactBufferCount": report["plausibleContactBufferCount"],
                "classCounts": report["classCounts"],
                "firstStoneStoneFinalizer": report["firstStoneStoneFinalizer"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
