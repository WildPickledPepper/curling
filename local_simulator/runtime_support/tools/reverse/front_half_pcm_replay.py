#!/usr/bin/env python3
"""Reusable BESTSHOT -> first-PCM front-half replay helpers.

The functions here are pure offline helpers: they do not start Unity and they do
not depend on pyphysx. They wrap the recovered CurlingMotion kernel so analysis
scripts and the future local simulator use the same front-half state advance.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.reverse.recovered_curling_motion import (  # noqa: E402
    BASE_FRICTION,
    SWEEP_FRICTION,
    STEP,
    B2Vec2,
    RecoveredUnityRandom,
    newfrictionstep,
    unity_friction,
)
from tools.reverse.replay_bestshot_seeded import (  # noqa: E402
    DEFAULT_RELEASE_X,
    DEFAULT_RELEASE_Y,
    Bestshot,
    ProtocolState,
    clamp_bestshot,
)


BESTSHOT_RE = re.compile(r"\bBESTSHOT\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)")
MOTIONINFO_RE = re.compile(
    r"\bMOTIONINFO\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+"
    r"([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)"
)

FORMAL_STONE_RADIUS = 0.140875
UNITY_CONTACT_OFFSET = 0.01
FIRST_PCM_CENTER_DISTANCE = 2.0 * FORMAL_STONE_RADIUS + 2.0 * UNITY_CONTACT_OFFSET
UNITY_FIXED_TIMESTEP = 0.01


def norm_angle(angle: float) -> float:
    value = float(angle)
    while value > math.pi:
        value -= 2.0 * math.pi
    while value <= -math.pi:
        value += 2.0 * math.pi
    return value


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


def event_shot_groups(events: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
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
                "motioninfo": None,
            }
            groups.append(current)
            continue
        if current is None:
            continue
        motion_match = MOTIONINFO_RE.search(text)
        if motion_match and current["motioninfo"] is None:
            current["motioninfo"] = {
                "t": float(event.get("t") or 0.0),
                "values": [float(value) for value in motion_match.groups()],
                "text": text,
            }
        noise = friction_value(event)
        if noise is not None:
            current["friction"].append({"t": float(event.get("t") or 0.0), "noise": noise})
    return groups


def canonical_yaw_from_unity_quat(q: Sequence[float]) -> float:
    if len(q) < 4:
        return 0.0
    x, y, z, w = [float(value) for value in q[:4]]
    if w < 0.0:
        x, y, z, w = -x, -y, -z, -w
    return norm_angle(2.0 * math.atan2(y, w))


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


def motioninfo_state(
    motioninfo: Sequence[float],
    *,
    yaw: float = 0.0,
    steps: int = 0,
) -> dict[str, Any]:
    """Create a replay state from protocol x/y/vx/vy/w MOTIONINFO values."""

    if len(motioninfo) < 5:
        raise ValueError("motioninfo must contain x, y, vx, vy, w")
    x, y, vx, vy, w = [float(value) for value in motioninfo[:5]]
    return state_dict(
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        w=w,
        yaw=yaw,
        steps=steps,
        frictions_used=0,
        source="motioninfo",
    )


def state_dict(
    *,
    x: float,
    y: float,
    vx: float,
    vy: float,
    w: float,
    yaw: float,
    steps: float,
    frictions_used: int,
    source: str,
    **extra: Any,
) -> dict[str, Any]:
    out = {
        "x": float(x),
        "y": float(y),
        "vx": float(vx),
        "vy": float(vy),
        "w": float(w),
        "yaw": norm_angle(float(yaw)),
        "steps": steps,
        "frictionsUsed": int(frictions_used),
        "source": source,
    }
    out.update(extra)
    return out


def replay_bestshot_with_noises(
    v0: float,
    h0: float,
    w0: float,
    noises: Sequence[float],
    *,
    fallback_friction: float = BASE_FRICTION,
    initial_yaw: float = 0.0,
) -> dict[str, Any]:
    state = local_initial_state(v0, h0, w0)
    x, y, vx, vy, w = state.x, state.y, state.vx, state.vy, state.w
    yaw = float(initial_yaw)
    used = 0
    for noise in noises:
        if math.hypot(vx, vy) <= 0.01:
            break
        used += 1
        friction = unity_friction(fallback_friction == SWEEP_FRICTION, noise=float(noise))
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        yaw += w * UNITY_FIXED_TIMESTEP
        x += vx * UNITY_FIXED_TIMESTEP
        y += vy * UNITY_FIXED_TIMESTEP
    return state_dict(
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        w=w,
        yaw=yaw,
        steps=used,
        frictions_used=used,
        source="bestshot_noise_replay",
    )


def replay_bestshot_constant(
    v0: float,
    h0: float,
    w0: float,
    steps: int,
    *,
    initial_yaw: float = 0.0,
) -> dict[str, Any]:
    return replay_bestshot_with_noises(
        v0,
        h0,
        w0,
        [0.0] * int(steps),
        initial_yaw=initial_yaw,
    )


def interpolate_state(
    previous: dict[str, Any],
    current: dict[str, Any],
    alpha: float,
    *,
    source: str,
    **extra: Any,
) -> dict[str, Any]:
    alpha = max(0.0, min(1.0, float(alpha)))

    def lerp(key: str) -> float:
        return float(previous[key]) + (float(current[key]) - float(previous[key])) * alpha

    return state_dict(
        x=lerp("x"),
        y=lerp("y"),
        vx=lerp("vx"),
        vy=lerp("vy"),
        w=lerp("w"),
        yaw=lerp("yaw"),
        steps=lerp("steps"),
        frictions_used=int(current.get("frictionsUsed", 0)),
        source=source,
        interpolationAlpha=alpha,
        **extra,
    )


def advance_until_center_distance(
    initial: dict[str, Any],
    noises: Sequence[float],
    *,
    target_x: float,
    target_y: float,
    threshold: float = FIRST_PCM_CENTER_DISTANCE,
    fallback_friction: float = BASE_FRICTION,
    interpolate: bool = False,
) -> dict[str, Any]:
    """Advance one active stone to the first stone-stone PCM distance shell.

    Unity/PhysX consumes the post-FixedUpdate state at a discrete scene tick, so
    interpolation is intentionally disabled by default.  It remains available
    for geometric diagnostics only.
    """

    x = float(initial["x"])
    y = float(initial["y"])
    vx = float(initial["vx"])
    vy = float(initial["vy"])
    w = float(initial["w"])
    yaw = float(initial.get("yaw") or 0.0)
    initial_steps = float(initial.get("steps") or 0.0)
    previous = state_dict(
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        w=w,
        yaw=yaw,
        steps=initial_steps,
        frictions_used=0,
        source=str(initial.get("source") or "initial"),
        distance=math.hypot(x - target_x, y - target_y),
        threshold=threshold,
    )
    if float(previous["distance"]) <= threshold:
        previous["source"] = "center_distance_initial"
        return previous

    best = previous
    for used, noise in enumerate(noises, 1):
        if math.hypot(vx, vy) <= 0.01:
            break
        friction = unity_friction(fallback_friction == SWEEP_FRICTION, noise=float(noise))
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        yaw += w * UNITY_FIXED_TIMESTEP
        x += vx * UNITY_FIXED_TIMESTEP
        y += vy * UNITY_FIXED_TIMESTEP
        current = state_dict(
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            w=w,
            yaw=yaw,
            steps=initial_steps + used,
            frictions_used=used,
            source="center_distance_tick",
            distance=math.hypot(x - target_x, y - target_y),
            threshold=threshold,
        )
        if float(current["distance"]) < float(best["distance"]):
            best = current
        previous_delta = float(previous["distance"]) - threshold
        current_delta = float(current["distance"]) - threshold
        if current_delta <= 0.0:
            if interpolate and previous_delta * current_delta <= 0.0:
                denom = float(current["distance"]) - float(previous["distance"])
                alpha = 0.0 if abs(denom) < 1e-12 else (threshold - float(previous["distance"])) / denom
                return interpolate_state(
                    previous,
                    current,
                    alpha,
                    source="interpolated_center_distance_threshold",
                    distance=threshold,
                    threshold=threshold,
                )
            current["source"] = "center_distance_threshold_tick"
            return current
        previous = current

    best = dict(best)
    best["source"] = "center_distance_threshold_missed_best_distance"
    best["missedThreshold"] = True
    return best


def advance_until_first_pcm(
    initial: dict[str, Any],
    noises: Iterable[float],
    targets: Sequence[dict[str, Any]],
    *,
    threshold: float = FIRST_PCM_CENTER_DISTANCE,
    fallback_friction: float = BASE_FRICTION,
    max_steps: int = 5000,
) -> dict[str, Any]:
    """Advance until one or more existing stones enter the PCM contact shell.

    Each target must contain x/y and may contain an index.  All targets inside
    the shell on the first discrete tick are returned because PhysX can create
    more than one shape pair during the same scene step.
    """

    normalized_targets = [
        {
            "index": int(target.get("index", index)),
            "x": float(target["x"]),
            "y": float(target["y"]),
            "yaw": float(target.get("yaw") or 0.0),
        }
        for index, target in enumerate(targets)
    ]
    if not normalized_targets:
        raise ValueError("at least one active target is required")

    x = float(initial["x"])
    y = float(initial["y"])
    vx = float(initial["vx"])
    vy = float(initial["vy"])
    w = float(initial["w"])
    yaw = float(initial.get("yaw") or 0.0)
    initial_steps = float(initial.get("steps") or 0.0)

    def annotate(state: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        distances = [
            {
                **target,
                "distance": math.hypot(
                    float(state["x"]) - target["x"],
                    float(state["y"]) - target["y"],
                ),
            }
            for target in normalized_targets
        ]
        distances.sort(key=lambda item: (float(item["distance"]), int(item["index"])))
        contacts = [item for item in distances if float(item["distance"]) <= threshold]
        state["nearestTarget"] = distances[0]
        state["nearestDistance"] = float(distances[0]["distance"])
        state["threshold"] = float(threshold)
        state["pcmTargets"] = contacts
        state["pcmTargetIndices"] = [int(item["index"]) for item in contacts]
        return state, contacts

    current, contacts = annotate(
        state_dict(
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            w=w,
            yaw=yaw,
            steps=initial_steps,
            frictions_used=0,
            source=str(initial.get("source") or "initial"),
        )
    )
    best = current
    last = current
    if contacts:
        current["source"] = "first_pcm_initial"
        return current

    used = 0
    for noise in noises:
        if used >= max_steps:
            break
        if math.hypot(vx, vy) <= 0.01:
            break
        used += 1
        friction = unity_friction(fallback_friction == SWEEP_FRICTION, noise=float(noise))
        speed = newfrictionstep(friction, B2Vec2(vx, vy), w, STEP)
        vx, vy, w = speed.v.x, speed.v.y, speed.angle
        yaw += w * UNITY_FIXED_TIMESTEP
        x += vx * UNITY_FIXED_TIMESTEP
        y += vy * UNITY_FIXED_TIMESTEP
        current, contacts = annotate(
            state_dict(
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                w=w,
                yaw=yaw,
                steps=initial_steps + used,
                frictions_used=used,
                source="first_pcm_search_tick",
            )
        )
        last = current
        if float(current["nearestDistance"]) < float(best["nearestDistance"]):
            best = current
        if contacts:
            current["source"] = "first_pcm_discrete_tick"
            return current

    result = dict(last)
    result["source"] = "first_pcm_not_reached"
    result["missedThreshold"] = True
    result["nearestApproach"] = {
        "x": float(best["x"]),
        "y": float(best["y"]),
        "steps": float(best["steps"]),
        "nearestTarget": best["nearestTarget"],
        "nearestDistance": float(best["nearestDistance"]),
    }
    return result


def replay_bestshot_until_center_distance(
    v0: float,
    h0: float,
    w0: float,
    noises: Sequence[float],
    *,
    target_x: float,
    target_y: float,
    threshold: float = FIRST_PCM_CENTER_DISTANCE,
    fallback_friction: float = BASE_FRICTION,
    interpolate: bool = False,
    initial_yaw: float = 0.0,
) -> dict[str, Any]:
    state = local_initial_state(v0, h0, w0)
    initial = state_dict(
        x=state.x,
        y=state.y,
        vx=state.vx,
        vy=state.vy,
        w=state.w,
        yaw=initial_yaw,
        steps=0,
        frictions_used=0,
        source="bestshot_release",
    )
    return advance_until_center_distance(
        initial,
        noises,
        target_x=target_x,
        target_y=target_y,
        threshold=threshold,
        fallback_friction=fallback_friction,
        interpolate=interpolate,
    )


def replay_motioninfo_until_center_distance(
    motioninfo: Sequence[float],
    noises: Sequence[float],
    *,
    target_x: float,
    target_y: float,
    threshold: float = FIRST_PCM_CENTER_DISTANCE,
    fallback_friction: float = BASE_FRICTION,
    interpolate: bool = False,
    yaw: float = 0.0,
    steps: int = 0,
) -> dict[str, Any]:
    """Advance a protocol MOTIONINFO row to first stone-stone PCM entrance."""

    return advance_until_center_distance(
        motioninfo_state(motioninfo, yaw=yaw, steps=steps),
        noises,
        target_x=target_x,
        target_y=target_y,
        threshold=threshold,
        fallback_friction=fallback_friction,
        interpolate=interpolate,
    )


def friction_noises_after_motioninfo(event_group: dict[str, Any]) -> list[float]:
    """Return captured Random.Range noise values strictly after MOTIONINFO."""

    motioninfo = event_group.get("motioninfo")
    if not isinstance(motioninfo, dict):
        raise ValueError("event group has no MOTIONINFO event")
    motion_t = float(motioninfo["t"])
    return [
        float(item["noise"])
        for item in event_group.get("friction") or []
        if float(item["t"]) > motion_t
    ]


def unity_seed_friction_noises(
    seed: int,
    count: int,
    *,
    skip: int = 0,
    sweeping: bool = False,
) -> list[float]:
    """Generate Random.Range noise values from the recovered Unity RNG."""

    rng = RecoveredUnityRandom.from_seed(int(seed))
    for _ in range(max(0, int(skip))):
        unity_friction(sweeping, rng=rng, noise=None)
    base = SWEEP_FRICTION if sweeping else BASE_FRICTION
    return [
        unity_friction(sweeping, rng=rng, noise=None) - base
        for _ in range(max(0, int(count)))
    ]


def iter_unity_friction_noises(
    rng: RecoveredUnityRandom,
    *,
    sweeping: bool = False,
) -> Iterator[float]:
    """Yield noise lazily so unused fixed ticks do not consume global RNG."""

    base = SWEEP_FRICTION if sweeping else BASE_FRICTION
    while True:
        yield unity_friction(sweeping, rng=rng, noise=None) - base


def to_pyphysx_zup_state(
    state: dict[str, Any],
    *,
    center_height: float = 0.115,
) -> dict[str, Any]:
    """Convert protocol state to the z-up pose convention used by local pyphysx."""

    yaw = norm_angle(float(state.get("yaw") or 0.0))
    half_yaw = 0.5 * yaw
    return {
        "position": [-float(state["y"]), -float(state["x"]), float(center_height)],
        "quaternionWxyz": [math.cos(half_yaw), 0.0, 0.0, math.sin(half_yaw)],
        "linearVelocity": [-float(state["vy"]), -float(state["vx"]), 0.0],
        "angularVelocity": [0.0, 0.0, float(state["w"])],
        "coordinateMode": "pyphysx-zup-from-protocol",
    }


def error_to_unity(local: dict[str, Any], unity: dict[str, Any]) -> dict[str, float]:
    dx = float(local["x"]) - float(unity["x"])
    dy = float(local["y"]) - float(unity["y"])
    yaw_delta = norm_angle(float(local.get("yaw") or 0.0) - float(unity.get("yaw") or 0.0))
    return {
        "dx": dx,
        "dy": dy,
        "positionError": math.hypot(dx, dy),
        "yawDelta": yaw_delta,
    }
