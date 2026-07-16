#!/usr/bin/env python3
"""Derive whether requested SWEEP commands affected the active Unity slide.

The browser receives socket data immediately, but Unity handles the message on
its main thread.  If ``Curling stop`` is logged between those two events, the
slide has already finished and the request cannot alter the captured physics.
This script turns that directly observable ordering into a small manifest that
the local and accelerated simulators can consume.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True, help="controlled sampler JSONL")
    parser.add_argument("--launcher-log", type=Path, required=True, help="Unity browser stdout log")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    requested = [row for row in _rows(args.samples) if float((row.get("requested") or {}).get("sweep") or 0.0) > 0.0]
    lines = args.launcher_log.read_text(encoding="utf-8", errors="replace").splitlines()
    received = [index for index, line in enumerate(lines) if "[JSLIB WebSocket] Received message: SWEEP " in line]
    handled = [index for index, line in enumerate(lines) if "Handle message:SWEEP " in line]
    if len(handled) > len(received) or len(received) > len(requested):
        raise ValueError(
            "invalid SWEEP event count: "
            f"requested={len(requested)} received={len(received)} handled={len(handled)}"
        )

    entries: list[dict[str, Any]] = []
    for ordinal, row in enumerate(requested):
        received_line = received[ordinal] if ordinal < len(received) else None
        handled_line = handled[ordinal] if ordinal < len(handled) else None
        if received_line is None or handled_line is None:
            effective = False
            reason = "unity_sweep_not_delivered"
        elif handled_line <= received_line:
            raise ValueError(f"invalid SWEEP event order for {row.get('label')}")
        else:
            # The terminal stop follows the handler in the same main-thread
            # work item for the observed guard slides.  A handler this late
            # cannot modify the already integrated trajectory.
            terminal_stop = any("Curling stop" in line for line in lines[handled_line : handled_line + 8])
            effective = not terminal_stop
            reason = (
                "unity_handler_on_terminal_stop" if terminal_stop
                else "unity_handler_before_curling_stop"
            )
        entries.append({
            "label": row.get("label"),
            "sample_id": row.get("sample_id"),
            "requested_sweep": float((row.get("requested") or {}).get("sweep") or 0.0),
            "effective": effective,
            "reason": reason,
            "evidence": {
                "receivedLine": None if received_line is None else received_line + 1,
                "handledLine": None if handled_line is None else handled_line + 1,
            },
        })

    result = {
        "schema": "protocol_sweep_effect_manifest_v1",
        "generatedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "inputs": {"samples": str(args.samples), "launcherLog": str(args.launcher_log)},
        "entries": entries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "entries": len(entries), "effective": sum(1 for item in entries if item["effective"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
