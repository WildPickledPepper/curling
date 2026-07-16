#!/usr/bin/env python3
"""Summarize before/after body/writeback deltas for solver consume hooks."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def compare_lists(before: Any, after: Any) -> dict[str, Any]:
    if not isinstance(before, list) or not isinstance(after, list):
        return {"present": False}
    count = min(len(before), len(after))
    changed = []
    max_abs = 0.0
    for index in range(count):
        if not (finite_number(before[index]) and finite_number(after[index])):
            continue
        delta = float(after[index]) - float(before[index])
        if abs(delta) > 1e-9:
            changed.append(
                {
                    "index": index,
                    "before": before[index],
                    "after": after[index],
                    "delta": delta,
                }
            )
            max_abs = max(max_abs, abs(delta))
    return {
        "present": True,
        "compared": count,
        "changedCount": len(changed),
        "maxAbsDelta": max_abs,
        "firstChanges": changed[:12],
    }


def compare_raw_bytes(before_window: Any, after_window: Any) -> dict[str, Any]:
    if not isinstance(before_window, dict) or not isinstance(after_window, dict):
        return {"present": False}
    before = before_window.get("rawBytes")
    after = after_window.get("rawBytes")
    if not isinstance(before, list) or not isinstance(after, list):
        return {"present": False}
    count = min(len(before), len(after))
    changed = []
    for index in range(count):
        b = int(before[index]) & 0xFF
        a = int(after[index]) & 0xFF
        if b != a:
            changed.append({"index": index, "before": b, "after": a})
    return {
        "present": True,
        "compared": count,
        "changedCount": len(changed),
        "firstChanges": changed[:24],
    }


def first_dump(row: dict[str, Any]) -> dict[str, Any]:
    dumps = row.get("extraConstraintDumps")
    return dumps[0] if isinstance(dumps, list) and dumps and isinstance(dumps[0], dict) else {}


def pair_rows(rows: list[dict[str, Any]]) -> dict[tuple[str, int, int], dict[str, dict[str, Any]]]:
    pairs: dict[tuple[str, int, int], dict[str, dict[str, Any]]] = {}
    for row in rows:
        key = (
            str(row.get("hook")),
            int(row.get("callIndex") or -1),
            int(row.get("armSerial") or -1),
        )
        phase = str(row.get("phase"))
        pairs.setdefault(key, {})[phase] = row
    return pairs


def summarize_pair(key: tuple[str, int, int], before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_dump = first_dump(before)
    after_dump = first_dump(after)
    header = ((before_dump.get("decodedConstraint") or {}).get("header") or {})
    forces = (before_dump.get("decodedConstraint") or {}).get("appliedNormalForces")
    fields = {
        "bodyA": compare_lists(before_dump.get("bodyAF32Preview"), after_dump.get("bodyAF32Preview")),
        "bodyB": compare_lists(before_dump.get("bodyBF32Preview"), after_dump.get("bodyBF32Preview")),
        "writeBack": compare_lists(
            before_dump.get("decodedWriteBackF32"),
            after_dump.get("decodedWriteBackF32"),
        ),
    }
    raw_fields = {
        "bodyA": compare_raw_bytes(before_dump.get("bodyAWindow"), after_dump.get("bodyAWindow")),
        "bodyB": compare_raw_bytes(before_dump.get("bodyBWindow"), after_dump.get("bodyBWindow")),
        "writeBack": compare_raw_bytes(
            before_dump.get("writeBackWindow"),
            after_dump.get("writeBackWindow"),
        ),
    }
    max_delta = max(
        (field.get("maxAbsDelta") or 0.0)
        for field in fields.values()
        if isinstance(field, dict)
    )
    changed_fields = [
        name for name, field in fields.items() if int(field.get("changedCount") or 0) > 0
    ]
    return {
        "hook": key[0],
        "callIndex": key[1],
        "armSerial": key[2],
        "tBefore": before.get("t"),
        "tAfter": after.get("t"),
        "maxAbsDelta": max_delta,
        "changedFields": changed_fields,
        "firstHeader": header,
        "appliedNormalForces": forces,
        "bodyABeforeFirst16": before_dump.get("bodyAF32Preview", [])[:16]
        if isinstance(before_dump.get("bodyAF32Preview"), list)
        else None,
        "bodyBBeforeFirst16": before_dump.get("bodyBF32Preview", [])[:16]
        if isinstance(before_dump.get("bodyBF32Preview"), list)
        else None,
        "fields": fields,
        "rawFields": raw_fields,
    }


def summarize(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("solverConsumeRows") or []
    pairs = pair_rows([row for row in rows if isinstance(row, dict)])
    summaries = []
    missing = Counter()
    for key, phases in pairs.items():
        if "before" not in phases or "after" not in phases:
            missing[key[0]] += 1
            continue
        summaries.append(summarize_pair(key, phases["before"], phases["after"]))

    by_hook = Counter(row["hook"] for row in summaries)
    changed_by_hook = Counter(row["hook"] for row in summaries if row["changedFields"])
    top = sorted(summaries, key=lambda row: row["maxAbsDelta"], reverse=True)[:20]
    return {
        "input": str(path),
        "solverConsumeCounts": data.get("solverConsumeCounts"),
        "pairedCount": len(summaries),
        "missingPairCountByHook": dict(sorted(missing.items())),
        "pairCountByHook": dict(sorted(by_hook.items())),
        "changedPairCountByHook": dict(sorted(changed_by_hook.items())),
        "topDeltas": top,
        "pairs": summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solver_state_json", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    report = summarize(args.solver_state_json)
    print(
        json.dumps(
            {
                "input": report["input"],
                "solverConsumeCounts": report["solverConsumeCounts"],
                "pairedCount": report["pairedCount"],
                "pairCountByHook": report["pairCountByHook"],
                "changedPairCountByHook": report["changedPairCountByHook"],
                "topDeltas": report["topDeltas"][: args.top],
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
