#!/usr/bin/env python3
"""Summarize one front-half sliding-to-first-PCM runtime capture."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = PROJECT_ROOT / "config" / "front_half_pcm_probe_20260710.json"


BESTSHOT_RE = re.compile(r"\bBESTSHOT\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: {exc}") from exc
            if isinstance(event, dict):
                events.append(event)
    events.sort(key=lambda item: float(item.get("t") or 0.0))
    return events


def load_plan(path: Path | None) -> list[dict[str, Any]]:
    if not path:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"plan must be a JSON list: {path}")
    return [item for item in payload if isinstance(item, dict)]


def text_preview(event: dict[str, Any]) -> str:
    data = event.get("data")
    if not isinstance(data, dict):
        return ""
    value = data.get("textPreview")
    return value if isinstance(value, str) else ""


def short_socket_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "t": event.get("t"),
        "type": event.get("type"),
        "text": text_preview(event),
    }


def find_pcm_inputs(data: dict[str, Any]) -> dict[str, Any] | None:
    for extra in data.get("extraDumps") or []:
        if isinstance(extra, dict) and str(extra.get("label") or "").endswith(".pcmInputs"):
            return extra
    return None


def decoded_at(payload: dict[str, Any], *path: str) -> Any:
    cursor: Any = payload
    for key in path:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(key)
    return cursor


def pcm_summary(event: dict[str, Any]) -> dict[str, Any]:
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    pcm = find_pcm_inputs(data)
    summary: dict[str, Any] = {
        "t": event.get("t"),
        "phase": data.get("phase"),
        "hook": decoded_at(data, "hook", "name"),
        "callIndex": data.get("callIndex"),
        "dumpIndex": data.get("dumpIndex"),
        "dumpId": data.get("dumpId"),
        "armSerial": data.get("armSerial"),
    }
    if not pcm:
        summary["pcmInputsFound"] = False
        return summary
    summary.update(
        {
            "pcmInputsFound": True,
            "shape0": {
                "ptr": pcm.get("shape0Ptr"),
                "geometry": decoded_at(pcm, "shape0", "decoded"),
                "hullData": decoded_at(pcm, "shape0", "hullData"),
            },
            "shape1": {
                "ptr": pcm.get("shape1Ptr"),
                "geometry": decoded_at(pcm, "shape1", "decoded"),
                "hullData": decoded_at(pcm, "shape1", "hullData"),
            },
            "transform0": decoded_at(pcm, "transform0", "decoded"),
            "transform1": decoded_at(pcm, "transform1", "decoded"),
            "narrowPhaseParams": decoded_at(pcm, "narrowPhaseParams", "decoded"),
            "cache": decoded_at(pcm, "cache", "decoded"),
            "contactBuffer": decoded_at(pcm, "contactBuffer", "decoded"),
        }
    )
    return summary


def friction_sample(event: dict[str, Any]) -> dict[str, Any]:
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    return {
        "t": event.get("t"),
        "callIndex": data.get("callIndex"),
        "randomRangeCalls": data.get("randomRangeCalls"),
        "frictionRangeCalls": data.get("frictionRangeCalls"),
        "value": data.get("value"),
        "inferredNoSweepFriction": data.get("inferredNoSweepFriction"),
        "inferredSweepFriction": data.get("inferredSweepFriction"),
    }


def summarize(events: list[dict[str, Any]], plan: list[dict[str, Any]]) -> dict[str, Any]:
    groups: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    last_reset: dict[str, Any] | None = None
    recent_socket: list[dict[str, Any]] = []
    first_pcm_after_by_dump: dict[str, dict[str, Any]] = {}
    pcm_pairs_by_dump: dict[str, dict[str, dict[str, Any]]] = {}

    counts: dict[str, int] = {}
    for event in events:
        event_type = str(event.get("type") or "")
        counts[event_type] = counts.get(event_type, 0) + 1
        text = text_preview(event)

        if event_type.startswith("websocket."):
            short = short_socket_event(event)
            recent_socket.append(short)
            if len(recent_socket) > 20:
                recent_socket = recent_socket[-20:]
            if text.startswith("RESETPOSITION") or text.startswith("RESETSTATE"):
                last_reset = short
            match = BESTSHOT_RE.search(text)
            if match:
                seq = len(groups)
                shot = {
                    "t": event.get("t"),
                    "seq": seq,
                    "command": text,
                    "v0": float(match.group(1)),
                    "h0": float(match.group(2)),
                    "w0": float(match.group(3)),
                    "plan": plan[seq] if seq < len(plan) else None,
                    "lastReset": last_reset,
                    "socketAroundShot": list(recent_socket),
                    "frictionEvents": [],
                    "fixedUpdateEnterCount": 0,
                    "firstPcmBefore": None,
                    "firstPcmAfter": None,
                    "firstPcmWithContactsBefore": None,
                    "firstPcmWithContactsAfter": None,
                    "pcmDumpIds": [],
                    "socketAfterShot": [],
                }
                groups.append(shot)
                current = shot
            elif current is not None:
                current["socketAfterShot"].append(short)
                if len(current["socketAfterShot"]) > 20:
                    current["socketAfterShot"] = current["socketAfterShot"][-20:]

        if current is not None and event_type == "sliding.random_range.friction":
            current["frictionEvents"].append(friction_sample(event))

        if current is not None and event_type == "sliding.fixed_update.enter":
            current["fixedUpdateEnterCount"] += 1

        if event_type == "physx.native.after":
            data = event.get("data") if isinstance(event.get("data"), dict) else {}
            if decoded_at(data, "hook", "name") == "PxcPCMContactConvexConvex":
                dump_id = data.get("dumpId")
                if isinstance(dump_id, str):
                    summary = pcm_summary(event)
                    first_pcm_after_by_dump.setdefault(dump_id, summary)
                    pcm_pairs_by_dump.setdefault(dump_id, {})["after"] = summary
            continue

        if event_type != "physx.native.before":
            continue
        data = event.get("data") if isinstance(event.get("data"), dict) else {}
        if decoded_at(data, "hook", "name") != "PxcPCMContactConvexConvex":
            continue
        if current is None:
            current = {
                "t": None,
                "seq": len(groups),
                "command": None,
                "plan": None,
                "lastReset": last_reset,
                "socketAroundShot": list(recent_socket),
                "frictionEvents": [],
                "fixedUpdateEnterCount": 0,
                "firstPcmBefore": None,
                "firstPcmAfter": None,
                "firstPcmWithContactsBefore": None,
                "firstPcmWithContactsAfter": None,
                "pcmDumpIds": [],
                "socketAfterShot": [],
            }
            groups.append(current)
        summary = pcm_summary(event)
        dump_id = summary.get("dumpId")
        if isinstance(dump_id, str):
            current["pcmDumpIds"].append(dump_id)
            pcm_pairs_by_dump.setdefault(dump_id, {})["before"] = summary
        if current["firstPcmBefore"] is None:
            current["firstPcmBefore"] = summary

    for group in groups:
        before = group.get("firstPcmBefore")
        if isinstance(before, dict):
            dump_id = before.get("dumpId")
            if isinstance(dump_id, str):
                group["firstPcmAfter"] = first_pcm_after_by_dump.get(dump_id)
        for dump_id in group.get("pcmDumpIds") or []:
            if not isinstance(dump_id, str):
                continue
            pair = pcm_pairs_by_dump.get(dump_id) or {}
            after = pair.get("after") or {}
            count = decoded_at(after, "contactBuffer", "count")
            if isinstance(count, int) and count > 0:
                group["firstPcmWithContactsBefore"] = pair.get("before")
                group["firstPcmWithContactsAfter"] = after
                break
        friction = group.pop("frictionEvents")
        group["frictionRangeCountBeforeFirstPcm"] = len(friction)
        group["frictionRangeFirst5"] = friction[:5]
        group["frictionRangeLast5"] = friction[-5:]
        first_pcm = group.get("firstPcmBefore")
        if isinstance(first_pcm, dict) and group.get("t") is not None:
            group["shotToFirstPcmMs"] = float(first_pcm.get("t") or 0.0) - float(group["t"])
        else:
            group["shotToFirstPcmMs"] = None

    return {
        "eventCount": len(events),
        "typeCounts": dict(sorted(counts.items())),
        "shotGroupCount": len(groups),
        "shotsWithFirstPcm": sum(1 for group in groups if group.get("firstPcmBefore")),
        "shotsWithFirstContactPcm": sum(
            1 for group in groups if group.get("firstPcmWithContactsBefore")
        ),
        "shotsMissingFirstPcm": [
            {
                "seq": group.get("seq"),
                "command": group.get("command"),
                "planLabel": decoded_at(group, "plan", "label"),
                "frictionRangeCountBeforeFirstPcm": group.get("frictionRangeCountBeforeFirstPcm"),
            }
            for group in groups
            if not group.get("firstPcmBefore")
        ],
        "shots": groups,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events_jsonl", type=Path)
    parser.add_argument("--plan-file", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    events = load_jsonl(args.events_jsonl)
    plan = load_plan(args.plan_file)
    summary = summarize(events, plan)
    output = args.output or args.events_jsonl.with_name("front_half_pcm_summary.json")
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "events": len(events),
        "shotGroupCount": summary["shotGroupCount"],
        "shotsWithFirstPcm": summary["shotsWithFirstPcm"],
        "shotsWithFirstContactPcm": summary["shotsWithFirstContactPcm"],
        "missingFirstPcm": summary["shotsMissingFirstPcm"],
        "output": str(output),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
