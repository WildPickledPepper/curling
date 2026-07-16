#!/usr/bin/env python3
"""Compare the recovered Python motion kernel with Unity's extracted Wasm function."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl, local_initial_state
from tools.reverse.recovered_curling_motion import B2Vec2, STEP, newfrictionstep, unity_friction


DEFAULT_EVENTS = PROJECT_ROOT / "log/unity_runtime_probe_20260710_012403/events.jsonl"
DEFAULT_WASM = Path(r"D:\esp\tmp\curling_reverse_il2cpp\newfrictionstep_oracle.wasm")
DEFAULT_NODE = PROJECT_ROOT / "tools/reverse/run_newfrictionstep_wasm_rollout.js"
DEFAULT_OUTPUT = PROJECT_ROOT / "data/calibration/newfrictionstep_wasm_rollout_audit_20260710.json"


def _python_rollout(initial: Any, frictions: list[float]) -> list[dict[str, float]]:
    vx, vy, angle = float(initial.vx), float(initial.vy), float(initial.w)
    result: list[dict[str, float]] = []
    for friction in frictions:
        speed = newfrictionstep(float(friction), B2Vec2(vx, vy), angle, STEP)
        vx, vy, angle = speed.v.x, speed.v.y, speed.angle
        result.append({"vx": vx, "vy": vy, "angle": angle})
    return result


def _wasm_rollout(initial: Any, frictions: list[float], wasm: Path, runner: Path) -> list[dict[str, float]]:
    payload = {
        "vx": float(initial.vx),
        "vy": float(initial.vy),
        "angle": float(initial.w),
        "steptime": float(STEP),
        "frictions": frictions,
    }
    completed = subprocess.run(
        ["node", str(runner), str(wasm)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        {key: float(value) for key, value in row.items()}
        for row in json.loads(completed.stdout)["steps"]
    ]


def audit(events: Path, wasm: Path, runner: Path) -> dict[str, Any]:
    groups = event_shot_groups(load_jsonl(events))
    rows: list[dict[str, Any]] = []
    for sequence, group in enumerate(groups):
        initial = local_initial_state(float(group["v0"]), float(group["h0"]), float(group["w0"]))
        frictions = [
            unity_friction(False, noise=float(item["noise"]))
            for item in group["friction"]
        ]
        python_steps = _python_rollout(initial, frictions)
        wasm_steps = _wasm_rollout(initial, frictions, wasm, runner)
        deltas = [
            {
                key: float(python_row[key]) - float(wasm_row[key])
                for key in ("vx", "vy", "angle")
            }
            for python_row, wasm_row in zip(python_steps, wasm_steps)
        ]
        max_abs = {
            key: max(abs(float(delta[key])) for delta in deltas) if deltas else 0.0
            for key in ("vx", "vy", "angle")
        }
        first_difference = next(
            (
                index
                for index, delta in enumerate(deltas, 1)
                if any(value != 0.0 for value in delta.values())
            ),
            None,
        )
        rows.append(
            {
                "sequence": sequence,
                "command": group["command"],
                "stepCount": len(frictions),
                "firstDifferentStep": first_difference,
                "maxAbsDelta": max_abs,
                "pythonFinal": python_steps[-1] if python_steps else None,
                "wasmFinal": wasm_steps[-1] if wasm_steps else None,
            }
        )
    max_abs = {
        key: max(float(row["maxAbsDelta"][key]) for row in rows) if rows else 0.0
        for key in ("vx", "vy", "angle")
    }
    return {
        "schema": "newfrictionstep_wasm_rollout_audit_v1",
        "purpose": "Exclude or quantify Python-vs-Wasm motion-kernel arithmetic before first PCM.",
        "inputs": {"events": str(events), "wasm": str(wasm), "runner": str(runner)},
        "summary": {"rowCount": len(rows), "maxAbsDelta": max_abs},
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--wasm", type=Path, default=DEFAULT_WASM)
    parser.add_argument("--runner", type=Path, default=DEFAULT_NODE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = audit(args.events, args.wasm, args.runner)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "summary": result["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
