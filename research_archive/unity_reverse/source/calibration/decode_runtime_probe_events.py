#!/usr/bin/env python3
"""Decode Unity runtime probe events into readable summaries."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


def _decode_hex_preview(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    parts = value.strip().split()
    if not parts:
        return ""
    try:
        raw = bytes(int(part, 16) for part in parts)
    except ValueError:
        return value
    return raw.rstrip(b"\0").decode("utf-8", errors="replace")


def _message_text(event: Dict[str, Any]) -> Optional[str]:
    data = event.get("data") or {}
    text_preview = data.get("textPreview")
    if isinstance(text_preview, str) and text_preview:
        return text_preview
    preview = data.get("dataPreview")
    if data.get("dataType") == "string":
        return preview if isinstance(preview, str) else None
    return _decode_hex_preview(preview)


def _keyword_hits(messages: Iterable[str]) -> Dict[str, int]:
    keywords = [
        "BESTSHOT",
        "MOTIONINFO",
        "POSITION",
        "SETSTATE",
        "SCORE",
        "TOTALSCORE",
        "GAMEOVER",
        "RANDSEED",
        "TRACE",
        "SAVE",
        ".save",
        "Records",
        "syncfs",
    ]
    upper_messages = [message.upper() for message in messages]
    hits: Dict[str, int] = {}
    for keyword in keywords:
        key_upper = keyword.upper()
        hits[keyword] = sum(1 for message in upper_messages if key_upper in message)
    return hits


def _iter_pointer_windows(windows: Any) -> Iterable[Dict[str, Any]]:
    if not isinstance(windows, list):
        return
    for window in windows:
        if not isinstance(window, dict):
            continue
        yield window
        yield from _iter_pointer_windows(window.get("pointerTargets"))


def _contact_candidate_example(
    event: Dict[str, Any],
    hook_name: str,
    window: Dict[str, Any],
    candidate: Dict[str, Any],
) -> Dict[str, Any]:
    contacts = candidate.get("contactsPreview")
    first_contact = contacts[0] if isinstance(contacts, list) and contacts else None
    return {
        "t": event.get("t"),
        "phase": (event.get("data") or {}).get("phase"),
        "hook": hook_name,
        "argIndex": window.get("argIndex"),
        "label": window.get("label"),
        "ptr": window.get("ptr"),
        "sourceOffset": window.get("sourceOffset"),
        "count": candidate.get("count"),
        "firstContact": first_contact,
    }


def _pcm_inputs_summary(
    event: Dict[str, Any],
    hook_name: str,
    pcm: Dict[str, Any],
) -> Dict[str, Any]:
    data = event.get("data") or {}
    contact_buffer = pcm.get("contactBuffer") if isinstance(pcm.get("contactBuffer"), dict) else {}
    cache = pcm.get("cache") if isinstance(pcm.get("cache"), dict) else {}
    return {
        "t": event.get("t"),
        "phase": data.get("phase"),
        "hook": hook_name,
        "callIndex": data.get("callIndex"),
        "dumpIndex": data.get("dumpIndex"),
        "dumpId": data.get("dumpId"),
        "shape0": (pcm.get("shape0") or {}).get("decoded") if isinstance(pcm.get("shape0"), dict) else None,
        "shape1": (pcm.get("shape1") or {}).get("decoded") if isinstance(pcm.get("shape1"), dict) else None,
        "transform0": (pcm.get("transform0") or {}).get("decoded") if isinstance(pcm.get("transform0"), dict) else None,
        "transform1": (pcm.get("transform1") or {}).get("decoded") if isinstance(pcm.get("transform1"), dict) else None,
        "narrowPhaseParams": (pcm.get("narrowPhaseParams") or {}).get("decoded")
        if isinstance(pcm.get("narrowPhaseParams"), dict)
        else None,
        "cache": cache.get("decoded") if cache else None,
        "hasCacheManifoldWindow": isinstance(cache.get("manifoldWindow"), dict) if cache else False,
        "contactCount": (contact_buffer.get("decoded") or {}).get("count")
        if isinstance(contact_buffer.get("decoded"), dict)
        else None,
        "hasContactBufferWindow": isinstance(contact_buffer.get("window"), dict) if contact_buffer else False,
        "shape0BigConvexArrays": _bigconvex_arrays_summary(pcm.get("shape0")),
        "shape1BigConvexArrays": _bigconvex_arrays_summary(pcm.get("shape1")),
    }


def _window_raw_summary(window: Any) -> Dict[str, Any]:
    if not isinstance(window, dict):
        return {"present": False, "rawBytesAvailable": False, "byteLength": None}
    raw = window.get("rawBytes")
    return {
        "present": True,
        "ptr": window.get("ptr"),
        "byteLength": window.get("byteLength"),
        "rawBytesAvailable": isinstance(raw, list),
        "rawByteCount": len(raw) if isinstance(raw, list) else None,
    }


def _bigconvex_arrays_summary(shape_window: Any) -> Dict[str, Any]:
    if not isinstance(shape_window, dict):
        return {"runtimePresent": False, "arraysPresent": False}
    runtime = shape_window.get("hullRuntime")
    if not isinstance(runtime, dict):
        return {"runtimePresent": False, "arraysPresent": False}
    arrays = runtime.get("bigConvexRawDataArrays")
    big = runtime.get("bigConvexRawData") if isinstance(runtime.get("bigConvexRawData"), dict) else {}
    if not isinstance(arrays, dict):
        return {
            "runtimePresent": True,
            "arraysPresent": False,
            "bigConvexDecoded": bool(big),
        }
    samples = _window_raw_summary(arrays.get("samplesWindow"))
    valencies = _window_raw_summary(arrays.get("valenciesWindow"))
    adjacent = _window_raw_summary(arrays.get("adjacentVertsWindow"))
    return {
        "runtimePresent": True,
        "arraysPresent": True,
        "bigConvexDecoded": bool(big),
        "samples": samples,
        "valencies": valencies,
        "adjacentVerts": adjacent,
        "completeRawArrays": (
            samples["rawBytesAvailable"]
            and valencies["rawBytesAvailable"]
            and adjacent["rawBytesAvailable"]
        ),
    }


def _pcm_readiness(pcm: Dict[str, Any]) -> Dict[str, bool]:
    cache = pcm.get("cache") if isinstance(pcm.get("cache"), dict) else {}
    contact_buffer = pcm.get("contactBuffer") if isinstance(pcm.get("contactBuffer"), dict) else {}
    readiness = {
        "has_shape0": isinstance((pcm.get("shape0") or {}).get("decoded"), dict)
        if isinstance(pcm.get("shape0"), dict)
        else False,
        "has_shape1": isinstance((pcm.get("shape1") or {}).get("decoded"), dict)
        if isinstance(pcm.get("shape1"), dict)
        else False,
        "has_transform0": isinstance((pcm.get("transform0") or {}).get("decoded"), dict)
        if isinstance(pcm.get("transform0"), dict)
        else False,
        "has_transform1": isinstance((pcm.get("transform1") or {}).get("decoded"), dict)
        if isinstance(pcm.get("transform1"), dict)
        else False,
        "has_narrow_phase_params": isinstance((pcm.get("narrowPhaseParams") or {}).get("decoded"), dict)
        if isinstance(pcm.get("narrowPhaseParams"), dict)
        else False,
        "has_cache": isinstance(cache.get("decoded"), dict) if cache else False,
        "has_cache_manifold_window": isinstance(cache.get("manifoldWindow"), dict) if cache else False,
        "has_contact_buffer": isinstance(contact_buffer.get("decoded"), dict) if contact_buffer else False,
    }
    for shape_key in ("shape0", "shape1"):
        big = _bigconvex_arrays_summary(pcm.get(shape_key))
        prefix = f"{shape_key}_"
        readiness[prefix + "has_hull_runtime"] = bool(big.get("runtimePresent"))
        readiness[prefix + "has_bigconvex_arrays"] = bool(big.get("arraysPresent"))
        readiness[prefix + "has_bigconvex_samples_raw"] = bool(
            (big.get("samples") or {}).get("rawBytesAvailable")
        )
        readiness[prefix + "has_bigconvex_valencies_raw"] = bool(
            (big.get("valencies") or {}).get("rawBytesAvailable")
        )
        readiness[prefix + "has_bigconvex_adjacent_raw"] = bool(
            (big.get("adjacentVerts") or {}).get("rawBytesAvailable")
        )
        readiness[prefix + "has_complete_bigconvex_raw_arrays"] = bool(big.get("completeRawArrays"))
    return readiness



def decode_events(payload: Dict[str, Any]) -> tuple[list[Dict[str, Any]], Dict[str, Any]]:
    decoded_rows: list[Dict[str, Any]] = []
    type_counts: Counter[str] = Counter()
    websocket_message_counts: Counter[str] = Counter()
    fs_counts: Counter[str] = Counter()
    physx_native_counts: Counter[str] = Counter()
    physx_contact_candidates: Counter[str] = Counter()
    physx_contact_candidate_examples: list[Dict[str, Any]] = []
    physx_pcm_input_counts: Counter[str] = Counter()
    physx_pcm_readiness_counts: Counter[str] = Counter()
    physx_pcm_input_examples: list[Dict[str, Any]] = []
    messages: list[str] = []

    for event in payload.get("events", []):
        event_type = str(event.get("type"))
        type_counts[event_type] += 1
        row = {
            "t": event.get("t"),
            "type": event_type,
            "data": event.get("data") or {},
        }
        if event_type.startswith("fs."):
            fs_counts[event_type] += 1
        if event_type.startswith("physx.native."):
            data = event.get("data") or {}
            hook = data.get("hook") or {}
            hook_name = str(hook.get("name") or hook.get("wasm") or hook.get("index") or "unknown")
            phase = str(data.get("phase") or "?")
            physx_native_counts[f"{event_type}:{hook_name}"] += 1
            for window in _iter_pointer_windows(data.get("pointerWindows")):
                candidate = window.get("contactBufferCandidate")
                if not isinstance(candidate, dict):
                    continue
                count = candidate.get("count")
                if not isinstance(count, int) or count <= 0:
                    continue
                arg_index = window.get("argIndex", "?")
                label = window.get("label", "")
                physx_contact_candidates[f"{hook_name}:arg{arg_index}:count={count}:{label}"] += 1
                if len(physx_contact_candidate_examples) < 24:
                    physx_contact_candidate_examples.append(
                        _contact_candidate_example(event, hook_name, window, candidate)
                    )
            for extra in data.get("extraDumps") or []:
                if not isinstance(extra, dict):
                    continue
                if not str(extra.get("label") or "").endswith(".pcmInputs"):
                    continue
                physx_pcm_input_counts[f"{hook_name}:{phase}"] += 1
                readiness = _pcm_readiness(extra)
                for key, value in readiness.items():
                    if value:
                        physx_pcm_readiness_counts[f"{hook_name}:{phase}:{key}"] += 1
                if len(physx_pcm_input_examples) < 16:
                    physx_pcm_input_examples.append(_pcm_inputs_summary(event, hook_name, extra))
        if event_type.startswith("websocket."):
            text = _message_text(event)
            if text is not None:
                row["text"] = text
                if event_type in {"websocket.send", "websocket.recv"}:
                    command = text.split(" ", 1)[0] if text else ""
                    websocket_message_counts[f"{event_type}:{command}"] += 1
                    messages.append(text)
        decoded_rows.append(row)

    summary = {
        "event_count": len(payload.get("events", [])),
        "type_counts": dict(sorted(type_counts.items())),
        "websocket_message_counts": dict(sorted(websocket_message_counts.items())),
        "fs_counts": dict(sorted(fs_counts.items())),
        "physx_native_counts": dict(sorted(physx_native_counts.items())),
        "physx_contact_candidates": dict(sorted(physx_contact_candidates.items())),
        "physx_contact_candidate_examples": physx_contact_candidate_examples,
        "physx_pcm_input_counts": dict(sorted(physx_pcm_input_counts.items())),
        "physx_pcm_readiness_counts": dict(sorted(physx_pcm_readiness_counts.items())),
        "physx_pcm_input_examples": physx_pcm_input_examples,
        "keyword_hits": _keyword_hits(messages),
        "instance_count": payload.get("instanceCount"),
        "memory_count": payload.get("memoryCount"),
        "table_count": payload.get("tableCount"),
        "hook_summary": payload.get("hookSummary"),
    }
    return decoded_rows, summary


def _load_payload(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        if parsed is not None:
            if isinstance(parsed, dict):
                return parsed
            if isinstance(parsed, list):
                return {"events": parsed}
            raise ValueError(f"Unsupported JSON root in {path}: {type(parsed).__name__}")

    events: list[Dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        event = json.loads(line)
        if not isinstance(event, dict):
            raise ValueError(f"JSONL line {line_number} is not an object: {type(event).__name__}")
        events.append(event)
    return {"events": events}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()

    payload = _load_payload(args.input)
    decoded_rows, summary = decode_events(payload)

    jsonl_path = args.jsonl or args.input.with_suffix(".decoded.jsonl")
    summary_path = args.summary or args.input.with_suffix(".summary.json")
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in decoded_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"jsonl": str(jsonl_path), "summary": str(summary_path), **summary}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
