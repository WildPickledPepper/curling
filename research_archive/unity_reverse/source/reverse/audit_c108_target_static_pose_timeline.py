"""Summarize C108's selected target--ice PCM pose timeline.

The capture selector retains only ``PxcPCMContactConvexMesh`` calls whose
input transform contains the target's expected native X/Z.  This turns the
first retained call into a boundary probe: it is the first observable native
consumer of the target pose after RESETSTATE, and precedes stone--stone PCM.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_LOCAL_RESET_X = -72.37740325927734
DEFAULT_UNITY_C04_X = -72.37739562988281


def pcm_transforms(event: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all decoded PxTransform inputs stored by the native hook."""
    transforms: list[dict[str, Any]] = []
    for extra in event.get("data", {}).get("extraDumps", []):
        if extra.get("label") != "PxcPCMContactConvexMesh.pcmInputs":
            continue
        for key in ("transform0", "transform1"):
            decoded = (extra.get(key) or {}).get("decoded")
            if decoded and decoded.get("layout") == "PxTransform":
                transforms.append(decoded)
    return transforms


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-x", type=float, default=DEFAULT_UNITY_C04_X)
    parser.add_argument("--target-z", type=float, default=54.150001525878906)
    parser.add_argument("--tolerance", type=float, default=0.002)
    parser.add_argument("--local-reset-x", type=float, default=DEFAULT_LOCAL_RESET_X)
    parser.add_argument("--unity-c04-x", type=float, default=DEFAULT_UNITY_C04_X)
    args = parser.parse_args()

    selected: list[dict[str, Any]] = []
    with args.events.open(encoding="utf-8") as fp:
        for line in fp:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "physx.native.before":
                continue
            data = event.get("data", {})
            if (data.get("hook") or {}).get("name") != "PxcPCMContactConvexMesh":
                continue
            for transform in pcm_transforms(event):
                point = transform.get("p") or []
                if len(point) < 3:
                    continue
                if abs(point[0] - args.target_x) > args.tolerance or abs(point[2] - args.target_z) > args.tolerance:
                    continue
                selected.append({
                    "event_t_ms": event.get("t"),
                    "call_index": data.get("callIndex"),
                    "dump_index": data.get("dumpIndex"),
                    "armed": data.get("armed"),
                    "p": point[:3],
                    "q": (transform.get("q") or [])[:4],
                })

    first = selected[0] if selected else None
    first_x = first["p"][0] if first else None
    result = {
        "schema": "c108_target_static_pose_timeline_v1",
        "events": str(args.events),
        "target_selector": {"x": args.target_x, "z": args.target_z, "tolerance": args.tolerance},
        "selected_static_pcm_calls": len(selected),
        "first_target_static_pcm": first,
        "reference": {
            "local_reset_x": args.local_reset_x,
            "unity_c04_target_x": args.unity_c04_x,
            "first_minus_local_reset_m": (first_x - args.local_reset_x) if first_x is not None else None,
            "first_minus_unity_c04_m": (first_x - args.unity_c04_x) if first_x is not None else None,
        },
        "interpretation": (
            "The first selected target--ice PCM input already equals the Unity C04 target X "
            "rather than the local reset X. Therefore this 7.629 um residual is present before "
            "the first observed target static-contact solve; ice support/PCM is not its producer."
            if first is not None
            else "No selected target--ice PCM input was found; capture is incomplete."
        ),
        "timeline": selected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
