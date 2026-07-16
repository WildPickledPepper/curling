#!/usr/bin/env python3
"""Extract compact first-any/first-contact PCM cache truth from a large runtime log."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "events.jsonl"
DEFAULT_SUMMARY = (
    PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "front_half_pcm_summary.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_cache_truth_20260710.json"


def _sha16(values: Any) -> str | None:
    if not isinstance(values, list):
        return None
    raw = bytes(int(value) & 0xFF for value in values)
    return hashlib.sha256(raw).hexdigest()[:16]


def _decoded(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    decoded = value.get("decoded")
    return decoded if isinstance(decoded, dict) else None


def _raw_bytes(value: Any) -> list[int] | None:
    if not isinstance(value, dict):
        return None
    raw = value.get("rawBytes")
    return [int(item) & 0xFF for item in raw] if isinstance(raw, list) else None


def _compact_shape(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    runtime = value.get("hullRuntime") if isinstance(value.get("hullRuntime"), dict) else {}
    big_arrays = (
        runtime.get("bigConvexRawDataArrays")
        if isinstance(runtime.get("bigConvexRawDataArrays"), dict)
        else {}
    )
    runtime_buffer = (
        runtime.get("runtimeBufferWindow")
        if isinstance(runtime.get("runtimeBufferWindow"), dict)
        else {}
    )

    def array_window(name: str) -> dict[str, Any] | None:
        window = big_arrays.get(name)
        if not isinstance(window, dict):
            return None
        raw = window.get("rawBytes")
        return {
            "byteLength": len(raw) if isinstance(raw, list) else window.get("byteLength"),
            "sha16": _sha16(raw),
        }

    return {
        "geometry": _decoded(value),
        "hullData": value.get("hullData") if isinstance(value.get("hullData"), dict) else None,
        "runtime": {
            "layout": runtime.get("layout"),
            "polygonVertexCounts": runtime.get("polygonVertexCounts"),
            "vertexRefCount": runtime.get("vertexRefCount"),
            "byteLayout": runtime.get("byteLayout"),
            "runtimeBuffer": {
                "byteLength": len(runtime_buffer.get("rawBytes") or []),
                "sha16": _sha16(runtime_buffer.get("rawBytes")),
            },
            "bigConvexRawData": runtime.get("bigConvexRawData"),
            "bigConvexArrays": {
                "samples": array_window("samplesWindow"),
                "valencies": array_window("valenciesWindow"),
                "adjacentVertices": array_window("adjacentVertsWindow"),
            },
        },
    }


def _compact_pcm_event(event: dict[str, Any]) -> dict[str, Any] | None:
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    hook = data.get("hook") if isinstance(data.get("hook"), dict) else {}
    if hook.get("name") != "PxcPCMContactConvexConvex":
        return None
    extras = data.get("extraDumps") if isinstance(data.get("extraDumps"), list) else []
    pcm = next(
        (
            item
            for item in extras
            if isinstance(item, dict) and str(item.get("label") or "").endswith(".pcmInputs")
        ),
        None,
    )
    if not isinstance(pcm, dict):
        return None

    cache = pcm.get("cache") if isinstance(pcm.get("cache"), dict) else {}
    manifold_window = (
        cache.get("manifoldWindow")
        if isinstance(cache.get("manifoldWindow"), dict)
        else {}
    )
    contact_buffer = (
        pcm.get("contactBuffer") if isinstance(pcm.get("contactBuffer"), dict) else {}
    )
    return {
        "t": event.get("t"),
        "phase": data.get("phase"),
        "callIndex": data.get("callIndex"),
        "dumpIndex": data.get("dumpIndex"),
        "dumpId": data.get("dumpId"),
        "armSerial": data.get("armSerial"),
        "shape0": _compact_shape(pcm.get("shape0")),
        "shape1": _compact_shape(pcm.get("shape1")),
        "transform0": _decoded(pcm.get("transform0")),
        "transform1": _decoded(pcm.get("transform1")),
        "narrowPhaseParams": _decoded(pcm.get("narrowPhaseParams")),
        "cache": {
            "decoded": _decoded(cache),
            "cacheWindowRaw": _raw_bytes(cache.get("window")),
            "manifoldWindowRaw": _raw_bytes(manifold_window),
            "manifoldWindowByteLength": len(manifold_window.get("rawBytes") or []),
            "manifoldWindowSha16": _sha16(manifold_window.get("rawBytes")),
        },
        "contactBuffer": {
            "decoded": _decoded(contact_buffer),
            "windowRaw": _raw_bytes(contact_buffer.get("window")),
        },
    }


def _boundary_spec(summary: dict[str, Any]) -> tuple[dict[int, list[dict[str, Any]]], list[dict[str, Any]]]:
    call_roles: dict[int, list[dict[str, Any]]] = {}
    rows: list[dict[str, Any]] = []
    for seq, shot in enumerate(summary.get("shots") or []):
        first_any = shot.get("firstPcmBefore") or {}
        first_contact = shot.get("firstPcmWithContactsBefore") or {}
        any_call = int(first_any["callIndex"])
        contact_call = int(first_contact["callIndex"])
        row = {
            "seq": seq,
            "label": (shot.get("plan") or {}).get("label"),
            "firstAnyCallIndex": any_call,
            "firstContactCallIndex": contact_call,
            "firstAnyIsFirstContact": any_call == contact_call,
        }
        rows.append(row)
        for role, call_index in (("first-any", any_call), ("first-contact", contact_call)):
            call_roles.setdefault(call_index, []).append(
                {"seq": seq, "label": row["label"], "role": role}
            )
    return call_roles, rows


def extract(events_path: Path, summary: dict[str, Any]) -> dict[str, Any]:
    call_roles, rows = _boundary_spec(summary)
    wanted_calls = set(call_roles)
    captures: dict[int, dict[str, Any]] = {
        call_index: {"roles": call_roles[call_index], "before": None, "after": None}
        for call_index in sorted(wanted_calls)
    }

    with events_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if "PxcPCMContactConvexConvex" not in line or "pcmInputs" not in line:
                continue
            event = json.loads(line)
            data = event.get("data") if isinstance(event.get("data"), dict) else {}
            call_index = data.get("callIndex")
            if not isinstance(call_index, int) or call_index not in wanted_calls:
                continue
            phase = data.get("phase")
            if phase not in {"before", "after"}:
                continue
            compact = _compact_pcm_event(event)
            if compact is None:
                continue
            compact["sourceLine"] = line_number
            captures[call_index][phase] = compact

    missing = [
        {"callIndex": call_index, "phase": phase}
        for call_index, value in captures.items()
        for phase in ("before", "after")
        if value[phase] is None
    ]
    return {
        "schema": "front_half_pcm_cache_truth_v1",
        "purpose": (
            "Compact raw Unity PCM manifold/cache truth for first-any and first-contact "
            "convex-convex calls; extracted without new sampling."
        ),
        "inputs": {
            "events": str(events_path),
            "summary": str(DEFAULT_SUMMARY),
        },
        "sampleBoundaries": rows,
        "expectedCallCount": len(wanted_calls),
        "capturedCallCount": sum(
            1 for value in captures.values() if value["before"] and value["after"]
        ),
        "missing": missing,
        "calls": {str(key): value for key, value in captures.items()},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    result = extract(args.events, summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "expectedCallCount": result["expectedCallCount"],
                "capturedCallCount": result["capturedCallCount"],
                "missing": result["missing"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if not result["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

