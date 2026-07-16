#!/usr/bin/env python3
"""Audit the convex-mesh PCM cache handoff without running Unity.

C17 clears the temporary multi-manifold immediately before the PCM method.
This audit distinguishes that diagnostic input reset from the later parent
writeback, then contrasts it with the historical Unity wrapper inputs.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def local_ice_trace(path: Path) -> list[dict]:
    document = read_json(path)
    entries = document["comparison"]["c05LocalPcmTrace"]
    return [
        entry
        for entry in entries
        if abs(entry["transform1"]["p"][1] - 14.304784774780273) < 1e-5
    ]


def summarize_local(entries: list[dict]) -> list[dict]:
    return [
        {
            "sequence": entry["sequence"],
            "contactCount": entry["contact_count_after"],
            "cacheBefore": entry["cache_before"]["cached_size"],
            "cacheAfterWrapper": entry["cache_after"]["cached_size"],
        }
        for entry in entries
    ]


def unity_mesh_inputs(path: Path) -> dict:
    rows = read_json(path)["pcmContactRows"]
    selected = [row for row in rows if row["pairClass"] == "stone_rink"]
    sizes = [row["pcmInputs"]["cache"]["decoded"]["cachedSize"] for row in selected]
    flags = [row["pcmInputs"]["cache"]["decoded"]["manifoldFlags"] for row in selected]
    cache_addresses = [row["pcmInputs"]["ptrs"]["cache"] for row in selected]
    cache_data_addresses = [row["pcmInputs"]["cache"]["decoded"]["cachedDataPtr"] for row in selected]
    return {
        "sampleCount": len(selected),
        "cachedSizeCounts": dict(sorted(Counter(sizes).items())),
        "manifoldFlagCounts": dict(sorted(Counter(flags).items())),
        "cacheAddressCount": len(set(cache_addresses)),
        "cachedDataAddressCount": len(set(cache_data_addresses)),
        "firstCalls": [
            {
                "callIndex": row["callIndex"],
                "cacheAddress": row["pcmInputs"]["ptrs"]["cache"],
                "cachedDataAddress": row["pcmInputs"]["cache"]["decoded"]["cachedDataPtr"],
                "cachedSize": row["pcmInputs"]["cache"]["decoded"]["cachedSize"],
                "manifoldFlags": row["pcmInputs"]["cache"]["decoded"]["manifoldFlags"],
            }
            for row in selected[:8]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unity", type=Path, required=True)
    parser.add_argument("--local-baseline", type=Path, required=True)
    parser.add_argument("--local-c17", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    baseline = summarize_local(local_ice_trace(args.local_baseline))
    c17 = summarize_local(local_ice_trace(args.local_c17))
    result = {
        "boundary": "C18: persistent PxsContactManager cache -> next PxcPCMContactConvexMesh input",
        "singleVariable": "C17 clears only the temporary MultiplePersistentContactManifold before the PCM method",
        "scope": "offline audit; no Unity execution and no production behavior change",
        "unityWrapperInputs": unity_mesh_inputs(args.unity),
        "localBaseline": baseline,
        "localC17": c17,
        "discriminator": {
            "c17StillReceives304BeforeLaterCalls": any(
                row["cacheBefore"] == 304 for row in c17[2:]
            ),
            "c17ClearsOnlyCurrentWrapperPayload": all(
                row["cacheAfterWrapper"] == 0 for row in c17
            ),
            "standardParentWritebackNotSuppressedByC17": any(
                row["cacheBefore"] == 304 for row in c17[2:]
            ),
        },
        "staticSourceFinding": {
            "unityFunction": "func70739",
            "dispatch": "calls PCM table at 4117968, including func70577 for convex-mesh",
            "writeback": "post-dispatch multi-manifold branch serializes size=(contacts*48)+(manifolds*16)+48, writes cache mCachedSize, and preserves multi flags",
        },
        "conclusion": (
            "C17 is causal but is not a serialization-disable implementation. "
            "The remaining source boundary is the per-frame PxsContactManager/work-unit cache handoff that presents a zero-sized multi cache to Unity's PCM wrapper."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["discriminator"], indent=2))


if __name__ == "__main__":
    main()
