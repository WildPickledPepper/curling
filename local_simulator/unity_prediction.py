"""Autonomous non-sweep DCP driver, separate from recorded setter replay.

Clock arithmetic: original build f79750 and f77913. Controller gates:
f61107, f61030, f61097 and f61089. Evidence and limitations are recorded in
analysis_input/prediction_driver_repair_20261003.md.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import struct
from typing import Any, Iterable


def f32(value: float) -> float:
    return struct.unpack('<f', struct.pack('<f', value))[0]


@dataclass
class UnityPredictionClock:
    """Running, unpaused TimeManager path (captureFramerate == 0).

    Frame elapsed time is an input, independent of the RNG. Defaults select
    the observed infinite-mode timeScale with saturated frames, deliberately
    giving headless predictions a reproducible clock instead of CPU timing.
    Initial times can represent a captured release boundary/accumulator.
    """
    fixed_dt: float = .01
    time_scale: float = 96.
    maximum_delta: float = .33
    frame_time: float = 0.
    fixed_time: float = 0.
    realtime: float = 0.
    time_offset: float = 0.

    def __post_init__(self) -> None:
        self.fixed_dt = f32(self.fixed_dt)
        self.time_scale = f32(self.time_scale)
        self.maximum_delta = f32(self.maximum_delta)
        if (not all(math.isfinite(v) for v in (self.fixed_dt,self.maximum_delta,self.time_scale,
                                              self.frame_time,self.fixed_time,self.realtime,self.time_offset))
                or self.fixed_dt <= 0 or self.maximum_delta <= 0 or self.time_scale < 0):
            raise ValueError('invalid clock configuration')

    def begin_frame(self, elapsed: float) -> float:
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError('elapsed time must be finite and non-negative')
        self.realtime += elapsed
        candidate = self.realtime - self.time_offset
        delta = candidate - self.frame_time
        # f79750: comparisons are f64; multiplication is f32 before promotion.
        if delta > self.maximum_delta:
            candidate = self.frame_time + f32(self.maximum_delta * self.time_scale)
        elif delta < 1e-5:
            candidate = self.frame_time + f32(f32(1e-5) * self.time_scale)
        elif abs(f32(self.time_scale - f32(1.))) > f32(1e-6):
            candidate = self.frame_time + f32(f32(delta) * self.time_scale)
        self.frame_time = candidate
        self.time_offset = self.realtime - candidate
        return candidate

    def take_fixed_step(self) -> bool:
        # f77913 uses repeated f64 addition of the promoted f32 timestep.
        next_time = self.fixed_time + self.fixed_dt
        if next_time > self.frame_time:
            return False
        self.fixed_time = next_time
        return True


class UnityPredictionDriver:
    """One released shot; draws only at an eligible DCP.FixedUpdate.

    Supplying a stream supports same-input forensic checks. Stream exhaustion
    is an error, never a controller stop signal. The default RNG is lazy.
    """
    def __init__(self, scene: Any, active_index: int, *, seed: int = 0,
                 noises: Iterable[float] | None = None, motion_stepper: Any = None,
                 clock: UnityPredictionClock | None = None, use_lean_steps: bool = False) -> None:
        from tools.reverse.recovered_unity_random import RecoveredUnityRandom
        from tools.reverse.front_half_pcm_replay import iter_unity_friction_noises
        self.scene = scene
        if scene.coordinate_mode != 'unity-native-yup' or not scene.emulate_unity_setactive_no_sim:
            raise ValueError('prediction driver requires the recovered Unity activation path')
        self.active_index = active_index
        if scene._custom_sliding_index != active_index:
            raise ValueError('start the shot before constructing its driver')
        self.origin = scene._custom_sliding_release_origin
        self.clock = clock or UnityPredictionClock(fixed_dt=scene.dt)
        if f32(scene.dt) != self.clock.fixed_dt:
            raise ValueError('clock and PhysX fixed timesteps must agree')
        self.rng = RecoveredUnityRandom.from_seed(seed) if noises is None else None
        self.noises = iter(noises) if noises is not None else iter_unity_friction_noises(self.rng)
        self.motion_stepper = motion_stepper
        self.use_lean_steps = bool(use_lean_steps)
        self.ongoing = True
        self.collided = False
        self.draw_count = 0
        self.fixed_count = 0
        self.update_count = 0
        self.first_contact_targets: list[int] = []
        self.first_contact_step: int | None = None

    def fixed_update(self) -> dict[str, Any]:
        slot = self.scene.slots[self.active_index]
        if self.ongoing and not self.collided and slot.enabled:
            try:
                noise = next(self.noises)
            except StopIteration as error:
                raise RuntimeError('friction input exhausted before controller stopped') from error
            self.draw_count += 1
            step = self.scene.step_custom_sliding_lean if self.use_lean_steps else self.scene.step_custom_sliding
            result = step(
                self.active_index, noise, motion_stepper=self.motion_stepper)
            reports = result['stoneReports']
        else:
            # Suppress the recorded-replay API's implicit Update handoff here.
            self.scene._simulate_custom_sliding_step()
            reports = self.scene._stone_reports(self.scene.scene.get_contact_reports())
            result = {'stoneReports': reports, 'wallReports': self.scene._last_wall_reports}
        self.fixed_count += 1
        targets = set()
        for report in reports:
            pair = {int(report['stoneIndex0']), int(report['stoneIndex1'])}
            if self.active_index in pair and int(report.get('events') or 0) & 4:
                targets.update(pair - {self.active_index})
        if targets:
            # f61030 sets CurlingStoneNew+16 before the next FixedUpdate draw.
            self.collided = True
            self.scene._custom_sliding_index = None
            if self.first_contact_step is None:
                self.first_contact_targets = sorted(targets)
                self.first_contact_step = self.fixed_count
        return result

    def update(self) -> bool:
        self.update_count += 1
        if self.ongoing and self.scene._unity_active_stop_condition(self.active_index, self.origin):
            material = self.scene.slots[self.active_index].material
            material.set_dynamic_friction(.6)
            material.set_static_friction(.6)
            # f61089 tests enabled stones' 3D linear speed, not angular speed.
            if self.scene._unity_all_stones_stopped():
                self.ongoing = False
                self.scene._custom_sliding_index = None
                self.scene._custom_sliding_release_origin = None
        return not self.ongoing

    def run(self, *, max_steps: int = 11000, frame_elapsed: float | None = None,
            frame_intervals: Iterable[float] | None = None) -> dict[str, Any]:
        if max_steps < 1:
            raise ValueError('max_steps must be positive')
        elapsed = self.clock.maximum_delta if frame_elapsed is None else frame_elapsed
        intervals = iter(frame_intervals) if frame_intervals is not None else None
        # Bound Update-only schedules too (e.g. a deliberately paused clock).
        for _ in range(max_steps):
            if intervals is not None:
                try:
                    elapsed = next(intervals)
                except StopIteration as error:
                    raise RuntimeError('frame schedule exhausted before controller stopped') from error
            self.clock.begin_frame(elapsed)
            while self.clock.fixed_time + self.clock.fixed_dt <= self.clock.frame_time:
                if self.fixed_count >= max_steps:
                    return self.result()
                self.clock.take_fixed_step()
                self.fixed_update()
            if self.update():
                break
        return self.result()

    def result(self) -> dict[str, Any]:
        return dict(settled=not self.ongoing, contact=self.first_contact_step is not None,
                    firstContactTargets=self.first_contact_targets,
                    firstContactStep=self.first_contact_step, fixedSteps=self.fixed_count,
                    frictionDraws=self.draw_count, updates=self.update_count,
                    rngState=None if self.rng is None else
                    [self.rng.s0, self.rng.s1, self.rng.s2, self.rng.s3],
                    clock={'fixedDt': self.clock.fixed_dt, 'timeScale': self.clock.time_scale,
                           'maximumDelta': self.clock.maximum_delta,
                           'frameTime': self.clock.frame_time, 'fixedTime': self.clock.fixed_time})
