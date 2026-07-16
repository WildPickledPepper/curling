#!/usr/bin/env python3
"""Compare local BESTSHOT sliding replay against captured Unity first-contact PCM states."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.recovered_curling_motion import (  # noqa: E402
    BASE_FRICTION,
    STEP,
    B2Vec2,
    newfrictionstep,
)
from tools.reverse.replay_bestshot_seeded import (  # noqa: E402
    DEFAULT_RELEASE_X,
    DEFAULT_RELEASE_Y,
    Bestshot,
    ProtocolState,
    clamp_bestshot,
)


DEFAULT_EVENTS = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "events.jsonl"
DEFAULT_SUMMARY = PROJECT_ROOT / "log" / "unity_runtime_probe_20260710_012403" / "front_half_pcm_summary.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "front_half_pcm_replay_compare_20260710.json"
BESTSHOT_RE = re.compile(r"\bBESTSHOT\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                item = json.loads(line)
                if isinstance(item, dict):
                    events.append(item)
    events.sort(key=lambda event: float(event.get("t") or 0.0))
    return events


def text_preview(event: dict[str, Any]) -> str:
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    text = data.get("textPreview")
    return text if isinstance(text, str) else ""


def friction_value(event: dict[str, Any]) -> float | None:
    if event.get("type") != "sliding.random_range.friction":
        return None
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    value = data.get("value")
    return float(value) if isinstance(value, (int, float)) else None


def event_shot_groups(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for event in events:
        text = text_preview(event)
        match = BESTSHOT_RE.search(text)
        if match:
            current = {
                "t": float(event.get("t") or 0.0),
                "command": text,
                "v0": float(match.group(1)),
                "h0": float(match.group(2)),
                "w0": float(match.group(3)),
                "friction": [],
            }
            groups.append(current)
            continue
        if current is None:
            continue
        noise = friction_value(event)
        if noise is not None:
            current["friction"].append({"t": float(event.get("t") or 0.0), "noise": noise})
    return groups


def canonical_yaw_from_unity_quat(q: list[float]) -> float:
    if len(q) < 4:
        return 0.0
    x, y, z, w = [float(value) for value in q[:4]]
    if w < 0.0:
        x, y, z, w = -x, -y, -z, -w
    yaw = 2.0 * math.atan2(y, w)
    while yaw > math.pi:
        yaw -= 2.0 * math.pi
    while yaw <= -math.pi:
        yaw += 2.0 * math.pi
    return yaw


def unity_protocol_transform(
    transform: dict[str, Any],
    *,
    native_to_protocol_x_const: float,
    native_to_protocol_y_const: float,
) -> dict[str, Any]:
    p = transform.get("p") or [0.0, 0.0, 0.0]
    q = transform.get("q") or [0.0, 0.0, 0.0, 1.0]
    return {
        "x": native_to_protocol_x_const - float(p[2]),
        "y": native_to_protocol_y_const - float(p[0]),
        "nativeP": p,
        "nativeQ": q,
        "yaw": canonical_yaw_from_unity_quat([float(value) for value in q[:4]]),
    }


def local_initial_state(v0: float, h0: float, w0: float) -> ProtocolState:
    shot = clamp_bestshot(Bestshot(v0, h0, w0))
    return ProtocolState(
        x=DEFAULT_RELEASE_X + shot.horizontal_offset,
        y=DEFAULT_RELEASE_Y,
        vx=0.0,
        vy=-shot.velocity,
        w=shot.rotation,
        steps=0,
    )


def replay_with_noises(
    v0: float,
    h0: float,
    w0: float,
    noises: list[float],
    *,
    fallback_friction: float = BASE_FRICTION,
) -> dict[str, Any]:
    state = local_initial_state(v0, h0, w0)
    x, y, vx, vy, w = state.x, state.y, state.vx, state.vy, state.w
    yaw = 0.0
    used = 0
    for used, noise in enumerate(noises, 1):
        if math.hypot(vx, vy) <= 0.01:
            break
        friction = fallback_friction + float(noise)
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        yaw += w * 0.01
        x += vx * 0.01
        y += vy * 0.01
    return {
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "w": w,
        "yaw": yaw,
        "steps": used,
        "frictionsUsed": len(noises),
    }


def replay_constant(v0: float, h0: float, w0: float, steps: int) -> dict[str, Any]:
    return replay_with_noises(v0, h0, w0, [0.0] * steps)


def error_to_unity(local: dict[str, Any], unity: dict[str, Any]) -> dict[str, float]:
    dx = float(local["x"]) - float(unity["x"])
    dy = float(local["y"]) - float(unity["y"])
    yaw_delta = float(local.get("yaw") or 0.0) - float(unity.get("yaw") or 0.0)
    while yaw_delta > math.pi:
        yaw_delta -= 2.0 * math.pi
    while yaw_delta <= -math.pi:
        yaw_delta += 2.0 * math.pi
    return {
        "dx": dx,
        "dy": dy,
        "positionError": math.hypot(dx, dy),
        "yawDelta": yaw_delta,
    }


from tools.reverse.front_half_pcm_replay import (  # noqa: E402
    error_to_unity,
    event_shot_groups,
    load_jsonl,
    replay_bestshot_constant as replay_constant,
    replay_bestshot_with_noises as replay_with_noises,
    unity_protocol_transform,
)


def compare(summary: dict[str, Any], event_groups: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for seq, shot in enumerate(summary.get("shots") or []):
        if seq >= len(event_groups):
            continue
        contact_before = shot.get("firstPcmWithContactsBefore") or shot.get("firstPcmBefore")
        contact_after = shot.get("firstPcmWithContactsAfter") or shot.get("firstPcmAfter")
        if not isinstance(contact_before, dict):
            continue
        plan = shot.get("plan") or {}
        target_plan = (plan.get("stones") or [{}])[0]
        target_x = float(target_plan.get("x"))
        target_y = float(target_plan.get("y"))
        transform1 = contact_before.get("transform1") or {}
        target_native_p = transform1.get("p") or [0.0, 0.0, 0.0]
        native_to_protocol_x_const = target_x + float(target_native_p[2])
        native_to_protocol_y_const = target_y + float(target_native_p[0])
        unity_active = unity_protocol_transform(
            contact_before.get("transform0") or {},
            native_to_protocol_x_const=native_to_protocol_x_const,
            native_to_protocol_y_const=native_to_protocol_y_const,
        )
        unity_target = unity_protocol_transform(
            transform1,
            native_to_protocol_x_const=native_to_protocol_x_const,
            native_to_protocol_y_const=native_to_protocol_y_const,
        )
        contact_count = None
        if isinstance(contact_after, dict):
            contact_count = ((contact_after.get("contactBuffer") or {}).get("count"))

        event_group = event_groups[seq]
        first_t = float(contact_before.get("t") or float("inf"))
        noises = [
            float(item["noise"])
            for item in event_group.get("friction") or []
            if float(item["t"]) <= first_t
        ]
        candidates: list[dict[str, Any]] = []
        v0, h0, w0 = float(shot["v0"]), float(shot["h0"]), float(shot["w0"])
        for stride in range(1, 7):
            for slot in range(stride):
                selected = noises[slot::stride]
                local = replay_with_noises(v0, h0, w0, selected)
                candidates.append(
                    {
                        "kind": "rng_subsequence",
                        "stride": stride,
                        "slot": slot,
                        "selectedNoiseCount": len(selected),
                        "local": local,
                        "error": error_to_unity(local, unity_active),
                    }
                )
        for steps in sorted({len(noises), len(noises) // 2, len(noises) // 3, len(noises) // 4, len(noises) // 5, len(noises) // 6}):
            if steps <= 0:
                continue
            local = replay_constant(v0, h0, w0, steps)
            candidates.append(
                {
                    "kind": "constant_friction",
                    "steps": steps,
                    "local": local,
                    "error": error_to_unity(local, unity_active),
                }
            )
        candidates.sort(key=lambda item: float(item["error"]["positionError"]))
        best_candidate = candidates[0] if candidates else None
        dx = float(unity_active["x"]) - float(unity_target["x"])
        dy = float(unity_active["y"]) - float(unity_target["y"])
        rows.append(
            {
                "seq": seq,
                "label": plan.get("label"),
                "command": shot.get("command"),
                "contactBoundary": "firstPcmWithContacts" if shot.get("firstPcmWithContactsBefore") else "firstPcmAny",
                "contactCount": contact_count,
                "unityActive": unity_active,
                "unityTarget": unity_target,
                "unityCenterDistance": math.hypot(dx, dy),
                "unityRelative": {"x": dx, "y": dy},
                "rawFrictionRangeCallsBeforeContact": len(noises),
                "bestPositionCandidate": best_candidate,
                "inferredInitialYawOffset": (
                    -float(best_candidate["error"]["yawDelta"]) if best_candidate else None
                ),
                "bestCandidates": candidates[:8],
                "targetYawHidden": abs(float(unity_target.get("yaw") or 0.0)) > 1e-4,
            }
        )
    best_errors = [
        float(row["bestPositionCandidate"]["error"]["positionError"])
        for row in rows
        if row.get("bestPositionCandidate")
    ]
    yaw_offsets = [
        float(row["inferredInitialYawOffset"])
        for row in rows
        if row.get("inferredInitialYawOffset") is not None
    ]
    return {
        "schema": "front_half_pcm_replay_compare_v1",
        "inputs": {
            "summary": str(DEFAULT_SUMMARY.relative_to(PROJECT_ROOT)),
            "events": str(DEFAULT_EVENTS.relative_to(PROJECT_ROOT)),
        },
        "aggregate": {
            "rowCount": len(rows),
            "positionRmseM": (
                math.sqrt(sum(value * value for value in best_errors) / len(best_errors))
                if best_errors
                else None
            ),
            "positionMaxErrorM": max(best_errors) if best_errors else None,
            "positionMeanErrorM": (
                sum(best_errors) / len(best_errors) if best_errors else None
            ),
            "hiddenTargetYawRows": [
                row["seq"] for row in rows if row.get("targetYawHidden")
            ],
            "inferredInitialYawOffsetAbsMaxRad": (
                max(abs(value) for value in yaw_offsets) if yaw_offsets else None
            ),
        },
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    events = load_jsonl(args.events)
    event_groups = event_shot_groups(events)
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    report = compare(summary, event_groups)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    compact = []
    for row in report["rows"]:
        best = row["bestCandidates"][0]
        compact.append(
            {
                "seq": row["seq"],
                "label": row["label"],
                "boundary": row["contactBoundary"],
                "contactCount": row["contactCount"],
                "rawFrictionCalls": row["rawFrictionRangeCallsBeforeContact"],
                "unityCenterDistance": row["unityCenterDistance"],
                "targetYaw": row["unityTarget"]["yaw"],
                "bestKind": best["kind"],
                "bestStride": best.get("stride"),
                "bestSlot": best.get("slot"),
                "bestSteps": best.get("steps") or best["local"].get("steps"),
                "bestPositionError": best["error"]["positionError"],
                "bestDx": best["error"]["dx"],
                "bestDy": best["error"]["dy"],
                "bestYawDelta": best["error"]["yawDelta"],
                "inferredInitialYawOffset": -best["error"]["yawDelta"],
            }
        )
    print(json.dumps(
        {"output": str(args.output), "aggregate": report["aggregate"], "rows": compact},
        indent=2,
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
