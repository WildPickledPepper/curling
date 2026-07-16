# -*- coding: utf-8 -*-
"""Unity-aligned BESTSHOT/MOTIONINFO to first stone-stone PCM progression.

This module owns protocol-level actor state.  It deliberately stops at the
first PCM entrance; a persistent pyphysx Scene must consume the returned pose
and write the post-collision state back through ``sync_actor_from_scene``.
"""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

# The reverse-engineered equations ship with this package.  Put this bundled
# support root ahead of the project checkout so a hand-off copy runs by itself.
RUNTIME_SUPPORT_ROOT = Path(__file__).resolve().parent / "runtime_support"
if str(RUNTIME_SUPPORT_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SUPPORT_ROOT))

from tools.reverse.front_half_pcm_replay import (
    FIRST_PCM_CENTER_DISTANCE,
    RecoveredUnityRandom,
    advance_until_first_pcm,
    iter_unity_friction_noises,
    local_initial_state,
    motioninfo_state,
    state_dict,
    to_pyphysx_zup_state,
)
from tools.reverse.recovered_curling_motion import BASE_FRICTION, SWEEP_FRICTION


@dataclass
class StoneActorState:
    """State that survives protocol position resets for one Unity stone actor."""

    index: int
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    w: float = 0.0
    active: bool = False

    def reset_position(self, x: float, y: float, *, active: Optional[bool] = None) -> None:
        """Mirror SetStonesByBody: move/stop the actor without clearing yaw."""

        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.w = 0.0
        self.active = bool(self.x or self.y) if active is None else bool(active)

    def cold_reset(self, x: float = 0.0, y: float = 0.0, *, active: bool = False) -> None:
        """Reset a newly created match, including orientation."""

        self.yaw = 0.0
        self.reset_position(x, y, active=active)

    def sync(
        self,
        *,
        x: float,
        y: float,
        yaw: float,
        vx: float = 0.0,
        vy: float = 0.0,
        w: float = 0.0,
        active: Optional[bool] = None,
    ) -> None:
        """Write a post-Scene actor state back into the persistent game state."""

        self.x = float(x)
        self.y = float(y)
        self.yaw = float(yaw)
        self.vx = float(vx)
        self.vy = float(vy)
        self.w = float(w)
        if active is not None:
            self.active = bool(active)

    def replay_state(self, *, source: str) -> dict[str, Any]:
        return state_dict(
            x=self.x,
            y=self.y,
            vx=self.vx,
            vy=self.vy,
            w=self.w,
            yaw=self.yaw,
            steps=0,
            frictions_used=0,
            source=source,
        )


class UnityFrontHalfSimulator:
    """Track stable stone identities and advance the active stone to first PCM."""

    def __init__(self, *, stone_count: int = 16, unity_seed: Optional[int] = None):
        if stone_count <= 0:
            raise ValueError("stone_count must be positive")
        self.stones = [StoneActorState(index=index) for index in range(stone_count)]
        self.rng = (
            RecoveredUnityRandom.from_seed(int(unity_seed))
            if unity_seed is not None
            else None
        )

    def set_unity_seed(self, seed: int) -> None:
        self.rng = RecoveredUnityRandom.from_seed(int(seed))

    def cold_reset(self) -> None:
        for stone in self.stones:
            stone.cold_reset()

    def reset_positions(self, position: Sequence[float]) -> None:
        """Apply protocol x/y slots while preserving every actor orientation."""

        expected = 2 * len(self.stones)
        if len(position) < expected:
            raise ValueError(f"position must contain at least {expected} values")
        for index, stone in enumerate(self.stones):
            stone.reset_position(position[2 * index], position[2 * index + 1])

    def sync_actor_from_scene(
        self,
        index: int,
        *,
        x: float,
        y: float,
        yaw: float,
        vx: float = 0.0,
        vy: float = 0.0,
        w: float = 0.0,
        active: Optional[bool] = None,
    ) -> None:
        self.stones[index].sync(
            x=x,
            y=y,
            yaw=yaw,
            vx=vx,
            vy=vy,
            w=w,
            active=active,
        )

    def _targets(
        self,
        active_index: int,
        target_indices: Optional[Sequence[int]],
    ) -> list[dict[str, Any]]:
        allowed = None if target_indices is None else {int(index) for index in target_indices}
        return [
            {
                "index": stone.index,
                "x": stone.x,
                "y": stone.y,
                "yaw": stone.yaw,
            }
            for stone in self.stones
            if stone.index != active_index
            and stone.active
            and (allowed is None or stone.index in allowed)
        ]

    def _noises(
        self,
        noises: Optional[Iterable[float]],
        *,
        sweeping: bool,
    ) -> Iterable[float]:
        if noises is not None:
            return noises
        if self.rng is None:
            raise ValueError("provide friction noises or initialize a Unity RNG seed")
        return iter_unity_friction_noises(self.rng, sweeping=sweeping)

    def _finish_entrance(
        self,
        active_index: int,
        initial_yaw: float,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        active = self.stones[active_index]
        active.sync(
            x=float(result["x"]),
            y=float(result["y"]),
            yaw=float(result["yaw"]),
            vx=float(result["vx"]),
            vy=float(result["vy"]),
            w=float(result["w"]),
            active=True,
        )
        payload = dict(result)
        reached_first_pcm = bool(result.get("pcmTargetIndices")) and not bool(
            result.get("missedThreshold")
        )
        payload.update(
            {
                "activeIndex": active_index,
                "activeInitialYaw": initial_yaw,
                "activePyphysxState": to_pyphysx_zup_state(result),
                "targetStates": [
                    asdict(self.stones[int(index)])
                    for index in result.get("pcmTargetIndices") or []
                ],
                "reachedFirstPcm": reached_first_pcm,
                "requiresPersistentScene": reached_first_pcm,
            }
        )
        return payload

    def bestshot_to_first_pcm(
        self,
        active_index: int,
        shot: Sequence[float],
        *,
        noises: Optional[Iterable[float]] = None,
        target_indices: Optional[Sequence[int]] = None,
        threshold: float = FIRST_PCM_CENTER_DISTANCE,
        sweeping: bool = False,
        max_steps: int = 5000,
    ) -> dict[str, Any]:
        """Release one stable actor and advance it to the first PCM scene tick."""

        if len(shot) < 3:
            raise ValueError("shot must contain velocity, horizontal offset, rotation")
        targets = self._targets(active_index, target_indices)
        if not targets:
            raise ValueError("no active target stones are available")
        v0, h0, w0 = [float(value) for value in shot[:3]]
        release = local_initial_state(v0, h0, w0)
        active = self.stones[active_index]
        initial_yaw = active.yaw
        initial = state_dict(
            x=release.x,
            y=release.y,
            vx=release.vx,
            vy=release.vy,
            w=release.w,
            yaw=initial_yaw,
            steps=0,
            frictions_used=0,
            source="bestshot_release",
        )
        result = advance_until_first_pcm(
            initial,
            self._noises(noises, sweeping=sweeping),
            targets,
            threshold=threshold,
            fallback_friction=SWEEP_FRICTION if sweeping else BASE_FRICTION,
            max_steps=max_steps,
        )
        return self._finish_entrance(active_index, initial_yaw, result)

    def motioninfo_to_first_pcm(
        self,
        active_index: int,
        motioninfo: Sequence[float],
        *,
        noises: Optional[Iterable[float]] = None,
        target_indices: Optional[Sequence[int]] = None,
        yaw_at_motioninfo: Optional[float] = None,
        threshold: float = FIRST_PCM_CENTER_DISTANCE,
        sweeping: bool = False,
        max_steps: int = 5000,
    ) -> dict[str, Any]:
        """Continue from MOTIONINFO while retaining the tracked actor yaw."""

        targets = self._targets(active_index, target_indices)
        if not targets:
            raise ValueError("no active target stones are available")
        active = self.stones[active_index]
        initial_yaw = active.yaw if yaw_at_motioninfo is None else float(yaw_at_motioninfo)
        initial = motioninfo_state(motioninfo, yaw=initial_yaw)
        result = advance_until_first_pcm(
            initial,
            self._noises(noises, sweeping=sweeping),
            targets,
            threshold=threshold,
            fallback_friction=SWEEP_FRICTION if sweeping else BASE_FRICTION,
            max_steps=max_steps,
        )
        return self._finish_entrance(active_index, initial_yaw, result)

    def snapshot(self) -> list[dict[str, Any]]:
        return [asdict(stone) for stone in self.stones]
