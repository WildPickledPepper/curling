#!/usr/bin/env python3
"""Audit whether first stone-stone PCM reads a stale PxsTransformCache pose.

This is intentionally narrow. It joins the first dynamic-dynamic contact-manager
task with the first PxcPCMContactConvexConvex call from the same Unity event log,
then compares the two PxsRigidCore body2World transforms with the two transforms
actually passed into PCM. It does not infer solver state or modify PhysX data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _transform_from_core(window: dict[str, Any]) -> dict[str, list[float]]:
    values = window["f32Preview"]
    return {"q": values[0:4], "p": values[4:7]}


def _delta(left: dict[str, list[float]], right: dict[str, list[float]]) -> dict[str, Any]:
    q_delta = [a - b for a, b in zip(left["q"], right["q"])]
    p_delta = [a - b for a, b in zip(left["p"], right["p"])]
    return {
        "q": q_delta,
        "p": p_delta,
        "max_abs": max(abs(value) for value in q_delta + p_delta),
    }


def _score(delta: dict[str, Any]) -> float:
    return sum(value * value for value in delta["q"] + delta["p"])


def _load_first_events(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    task_event: dict[str, Any] | None = None
    pcm_event: dict[str, Any] | None = None
    with path.open(encoding="utf-8") as source:
        for line in source:
            event = json.loads(line)
            if event.get("type") != "physx.native.before":
                continue
            data = event.get("data", {})
            hook_name = data.get("hook", {}).get("name")
            if hook_name == "PxsContext.contactManagerDiscreteUpdate" and task_event is None:
                task_event = data
            elif hook_name == "PxcPCMContactConvexConvex" and pcm_event is None:
                pcm_event = data
    if task_event is None or pcm_event is None:
        raise ValueError("expected one captured contact-manager task and one convex-convex PCM call")
    return task_event, pcm_event


def audit(events_path: Path) -> dict[str, Any]:
    task_event, pcm_event = _load_first_events(events_path)
    task_extra = next(item for item in task_event["extraDumps"] if "task" in item)
    managers = task_extra["task"]["managers"]
    dynamic = [
        row
        for row in managers
        if row.get("manager", {}).get("flags") == 611
        and row.get("rigidCore0Window")
        and row.get("rigidCore1Window")
    ]
    if len(dynamic) != 1:
        raise ValueError(f"expected exactly one dynamic-dynamic manager, found {len(dynamic)}")
    manager = dynamic[0]

    pcm = next(item for item in pcm_event["extraDumps"] if "transform0" in item)
    core0 = _transform_from_core(manager["rigidCore0Window"])
    core1 = _transform_from_core(manager["rigidCore1Window"])
    pcm0 = pcm["transform0"]["decoded"]
    pcm1 = pcm["transform1"]["decoded"]

    direct = [_delta(core0, pcm0), _delta(core1, pcm1)]
    swapped = [_delta(core0, pcm1), _delta(core1, pcm0)]
    direct_score = sum(_score(item) for item in direct)
    swapped_score = sum(_score(item) for item in swapped)
    selected = direct if direct_score <= swapped_score else swapped
    exact = all(item["max_abs"] == 0.0 for item in selected)

    return {
        "scope": "Unity controlled 14000 first dynamic-dynamic manager -> first convex-convex PCM",
        "events": str(events_path).replace("\\", "/"),
        "manager": {
            "task_index": manager["taskIndex"],
            "flags": manager["manager"]["flags"],
            "transform_cache": [
                manager["manager"]["transformCache0"],
                manager["manager"]["transformCache1"],
            ],
            "np_index": manager["manager"]["npIndex"],
        },
        "actor_core_body2world": [core0, core1],
        "pcm_consumed_transforms": [pcm0, pcm1],
        "mapping": "direct" if direct_score <= swapped_score else "swapped",
        "per_transform_delta": selected,
        "acceptance": {
            "actor_core_equals_pcm_transform_float32": exact,
            "transform_cache_staleness_as_source_of_micro_pose": "rejected" if exact else "unresolved",
        },
        "interpretation": (
            "At first stone-stone PCM, the cache-consumed transforms are exact copies of the two "
            "actor cores. A missing or late actor-to-transform-cache refresh cannot explain the "
            "observed local/Unity micro-pose delta. Its source is upstream of actor core state."
            if exact
            else "The core/cache comparison did not close; do not infer a refresh cause."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.events)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["acceptance"], ensure_ascii=False))


if __name__ == "__main__":
    main()
