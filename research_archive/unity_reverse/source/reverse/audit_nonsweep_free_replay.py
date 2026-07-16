#!/usr/bin/env python3
"""Strict endpoint replay for no-collision Unity shots.

Only a Unity sampler row which has a matching observed BESTSHOT event is
considered executed.  This prevents a server-rejected command from being
mistaken for a valid ``(0, 0)`` endpoint.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.reverse.diagnose_hybrid_bvh4_source_shell import _install_hybrid_module
from tools.reverse.front_half_pcm_replay import canonical_yaw_from_unity_quat, event_shot_groups, load_jsonl


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _finish_custom_sliding(scene: Any, active: int, max_steps: int = 6000) -> dict[str, Any]:
    """Finish with the normal non-sweep friction after the captured draws."""

    quiet = 0
    for step in range(1, max_steps + 1):
        scene.step_custom_sliding(active, 0.0)
        state = scene.state(active)
        moving = math.hypot(float(state["vx"]), float(state["vy"])) > 0.01 or abs(float(state["w"])) > 0.01
        quiet = 0 if moving else quiet + 1
        if quiet >= 20:
            return {"settled": True, "steps": step}
    return {"settled": False, "steps": max_steps}


def _same_shot(sample: dict[str, Any], group: dict[str, Any]) -> bool:
    requested = sample["requested"]
    return all(
        abs(float(requested[key]) - float(group[key])) <= 1e-6
        for key in ("v0", "h0", "w0")
    )


def _release_yaws(events: list[dict[str, Any]]) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for event in events:
        if event.get("type") != "a10.release_reset_orientation":
            continue
        data = event.get("data") or {}
        release = (data.get("release") or {})
        text = release.get("text")
        q = (((data.get("bridgePoseBeforeAngularSetter") or {}).get("transform") or {}).get("q"))
        if isinstance(text, str) and isinstance(q, list) and len(q) >= 4:
            result.setdefault(text, []).append(canonical_yaw_from_unity_quat(q))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    samples = _rows(args.samples)
    events = load_jsonl(args.events)
    groups = event_shot_groups(events)
    yaws = _release_yaws(events)
    _install_hybrid_module()
    from unity_front_half_physx import PersistentPhysxFrontHalfScene

    scene = PersistentPhysxFrontHalfScene(
        stone_count=16,
        ice_mesh_mode="unity-source-once",
        ice_use_fast_midphase=True,
        emulate_unity_native_angular_setter_tilt_only=True,
        emulate_unity_setactive_refilter=True,
    )
    used: set[int] = set()
    rows: list[dict[str, Any]] = []
    for group in groups:
        matches = [i for i, sample in enumerate(samples) if i not in used and _same_shot(sample, group)]
        if len(matches) != 1:
            raise ValueError("each observed BESTSHOT must map to exactly one sampler row")
        sample = samples[matches[0]]
        used.add(matches[0])
        active = int(sample["active_shot_num"])
        yaw_values = yaws.get(group["command"], [])
        if not yaw_values:
            raise ValueError("matching BESTSHOT lacks A10 release orientation")
        active_yaw = yaw_values.pop(0)
        scene.reset_positions(sample["reset_position"], yaw_overrides={active: active_yaw}, settle_steps=1)
        scene.start_bestshot(active, [float(group[key]) for key in ("v0", "h0", "w0")], yaw=active_yaw)
        for item in group["friction"]:
            scene.step_custom_sliding(active, float(item["noise"]))
        settle = _finish_custom_sliding(scene, active)
        cleared = scene.clear_out_of_play_stones() if settle["settled"] else []
        state = scene.state(active)
        unity = [float(value) for value in sample["after_position"][2 * active: 2 * active + 2]]
        unity_cleared = unity == [0.0, 0.0]
        local = [float(state["x"]), float(state["y"])]
        local_cleared = active in cleared
        rows.append({
            "label": sample["label"], "sampleId": sample["sample_id"],
            "frictionDrawCount": len(group["friction"]), "releaseYaw": active_yaw, "settle": settle,
            "unityEndpoint": unity, "localEndpoint": local,
            "unityCleared": unity_cleared, "localCleared": local_cleared,
            "endpointErrorMm": None if unity_cleared or local_cleared else 1000.0 * math.hypot(local[0] - unity[0], local[1] - unity[1]),
        })
    skipped = [{"label": sample["label"], "reason": "no matching Unity BESTSHOT event; command was not executed"} for i, sample in enumerate(samples) if i not in used]
    result = {"schema": "nonsweep_free_replay_v1", "executedRows": rows, "excludedRows": skipped}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"executed": len(rows), "excluded": len(skipped), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
