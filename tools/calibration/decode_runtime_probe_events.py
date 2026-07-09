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


def decode_events(payload: Dict[str, Any]) -> tuple[list[Dict[str, Any]], Dict[str, Any]]:
    decoded_rows: list[Dict[str, Any]] = []
    type_counts: Counter[str] = Counter()
    websocket_message_counts: Counter[str] = Counter()
    fs_counts: Counter[str] = Counter()
    physx_native_counts: Counter[str] = Counter()
    physx_contact_candidates: Counter[str] = Counter()
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
        "keyword_hits": _keyword_hits(messages),
        "instance_count": payload.get("instanceCount"),
        "memory_count": payload.get("memoryCount"),
        "table_count": payload.get("tableCount"),
        "hook_summary": payload.get("hookSummary"),
    }
    return decoded_rows, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
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
