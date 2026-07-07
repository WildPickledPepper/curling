# -*- coding: utf-8 -*-
"""Reduced Shegelski-style free-running curling-rock simulator.

The paper integrates dry/wet friction around the running band. This module
keeps the same state variables and speed-dependent late-curl mechanism, while
using an identifiable reduced force law suitable for the official samples.
It intentionally does not model sweeping or collisions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Sequence, Tuple

import numpy as np


DEFAULT_CONFIG = Path(__file__).resolve().parent / "config" / "paper_physics_calibration.json"


@dataclass(frozen=True)
class PaperPhysicsParams:
    """Parameters of the reduced dry/wet-friction dynamics."""

    dry_decel: float = 0.075
    wet_decel: float = 0.006
    wet_exponent: float = 2.0
    curl_gain: float = 0.001
    late_curl_gain: float = 4.0
    transition_speed: float = 1.0
    transition_width: float = 0.2
    angular_drag: float = 0.025
    angular_speed_drag: float = 0.01

    def to_dict(self) -> Dict[str, float]:
        return {key: float(value) for key, value in asdict(self).items()}

    @classmethod
    def from_sequence(cls, values: Sequence[float]) -> "PaperPhysicsParams":
        return cls(*[float(value) for value in values])

    def to_array(self) -> np.ndarray:
        return np.array(list(self.to_dict().values()), dtype=float)


def _smooth_late_phase(speed: np.ndarray, transition: float, width: float) -> np.ndarray:
    """Return a smooth 0..1 low-speed phase weight."""

    z = np.clip((speed - transition) / max(width, 1e-4), -40.0, 40.0)
    return 1.0 / (1.0 + np.exp(z))


def simulate_tail_batch(
    middle_states: np.ndarray,
    params: PaperPhysicsParams,
    *,
    dt: float = 0.025,
    max_time: float = 40.0,
    stop_speed: float = 0.01,
) -> Tuple[np.ndarray, np.ndarray]:
    """Integrate MOTIONINFO states x,y,vx,vy,omega until rest."""

    state = np.asarray(middle_states, dtype=float).copy()
    if state.ndim != 2 or state.shape[1] != 5:
        raise ValueError("middle_states must have shape (n, 5)")

    n = len(state)
    active = np.hypot(state[:, 2], state[:, 3]) > stop_speed
    stopped_at = np.where(active, max_time, 0.0).astype(float)
    steps = int(np.ceil(max_time / dt))

    for step in range(steps):
        if not np.any(active):
            break

        idx = np.flatnonzero(active)
        vx = state[idx, 2]
        vy = state[idx, 3]
        omega = state[idx, 4]
        speed = np.hypot(vx, vy)
        ux = vx / np.maximum(speed, 1e-9)
        uy = vy / np.maximum(speed, 1e-9)

        # Dry friction is nearly speed independent. Wet friction follows the
        # paper's speed-power law, represented here per unit mass.
        decel = params.dry_decel + params.wet_decel * np.power(
            np.maximum(speed, 0.0), params.wet_exponent
        )

        late = _smooth_late_phase(
            speed, params.transition_speed, params.transition_width
        )
        curl_scale = params.curl_gain * (1.0 + params.late_curl_gain * late)
        # (-uy, ux) points to +x for a rock travelling toward decreasing y.
        curl_accel = curl_scale * omega * speed
        ax = -decel * ux + curl_accel * (-uy)
        ay = -decel * uy + curl_accel * ux

        old_vx = vx.copy()
        old_vy = vy.copy()
        new_vx = old_vx + ax * dt
        new_vy = old_vy + ay * dt
        new_speed = np.hypot(new_vx, new_vy)
        reversed_direction = old_vx * new_vx + old_vy * new_vy <= 0.0
        just_stopped = (new_speed <= stop_speed) | reversed_direction

        moving = ~just_stopped
        moving_idx = idx[moving]
        state[moving_idx, 0] += 0.5 * (old_vx[moving] + new_vx[moving]) * dt
        state[moving_idx, 1] += 0.5 * (old_vy[moving] + new_vy[moving]) * dt
        state[moving_idx, 2] = new_vx[moving]
        state[moving_idx, 3] = new_vy[moving]
        drag = params.angular_drag + params.angular_speed_drag * speed[moving]
        state[moving_idx, 4] *= np.exp(-drag * dt)

        stopped_idx = idx[just_stopped]
        if len(stopped_idx):
            fraction = np.clip(
                speed[just_stopped]
                / np.maximum(speed[just_stopped] + new_speed[just_stopped], 1e-9),
                0.0,
                1.0,
            )
            state[stopped_idx, 0] += old_vx[just_stopped] * dt * fraction
            state[stopped_idx, 1] += old_vy[just_stopped] * dt * fraction
            state[stopped_idx, 2:5] = 0.0
            stopped_at[stopped_idx] = (step + fraction) * dt
            active[stopped_idx] = False

    return state[:, :2], stopped_at


def simulate_tail(
    middle_state: Sequence[float],
    params: PaperPhysicsParams,
    **kwargs: float,
) -> Tuple[Tuple[float, float], float]:
    """Scalar convenience wrapper around simulate_tail_batch."""

    final, times = simulate_tail_batch(
        np.asarray([middle_state], dtype=float), params, **kwargs
    )
    return (float(final[0, 0]), float(final[0, 1])), float(times[0])


def shot_features(v0: float, h0: float, w0: float) -> np.ndarray:
    """Feature vector used by the calibrated release-to-middle mapping."""

    return np.array(
        [
            1.0,
            v0,
            h0,
            w0,
            abs(w0),
            np.tanh(w0),
            v0 * v0,
            h0 * h0,
            w0 * w0,
            v0 * h0,
            v0 * w0,
            h0 * w0,
        ],
        dtype=float,
    )


class CalibratedPaperSimulator:
    """Load a fitted release mapping and paper-inspired tail dynamics."""

    def __init__(
        self,
        params: PaperPhysicsParams,
        middle_coefficients: np.ndarray,
        *,
        dt: float = 0.025,
        direct_landing_coefficients: np.ndarray | None = None,
    ):
        coefficients = np.asarray(middle_coefficients, dtype=float)
        if coefficients.shape != (12, 5):
            raise ValueError("middle_coefficients must have shape (12, 5)")
        self.params = params
        self.middle_coefficients = coefficients
        self.dt = float(dt)
        self.direct_landing_coefficients = None
        if direct_landing_coefficients is not None:
            landing_coefficients = np.asarray(
                direct_landing_coefficients, dtype=float
            )
            if landing_coefficients.shape != (12, 2):
                raise ValueError(
                    "direct_landing_coefficients must have shape (12, 2)"
                )
            self.direct_landing_coefficients = landing_coefficients

    @classmethod
    def from_file(
        cls, path: Path | str = DEFAULT_CONFIG
    ) -> "CalibratedPaperSimulator":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("schema") != "paper_curling_physics_v1":
            raise ValueError("unsupported paper physics calibration schema")
        params = PaperPhysicsParams(
            **{key: float(value) for key, value in payload["params"].items()}
        )
        return cls(
            params,
            np.asarray(payload["middle_coefficients"], dtype=float),
            dt=float(payload.get("dt", 0.025)),
            direct_landing_coefficients=payload.get(
                "direct_landing_coefficients"
            ),
        )

    def predict_middle(self, v0: float, h0: float, w0: float) -> np.ndarray:
        return shot_features(v0, h0, w0) @ self.middle_coefficients

    def predict_landing(
        self, v0: float, h0: float, w0: float
    ) -> Tuple[Tuple[float, float], float]:
        middle = self.predict_middle(v0, h0, w0)
        return simulate_tail(middle, self.params, dt=self.dt)

    def predict_hybrid_landing(
        self, v0: float, h0: float, w0: float
    ) -> Tuple[Tuple[float, float], float]:
        """Use direct-regression x and physical-simulation y."""

        if self.direct_landing_coefficients is None:
            raise ValueError("calibration does not contain direct landing coefficients")
        features = shot_features(v0, h0, w0)
        direct = features @ self.direct_landing_coefficients
        physical, stop_time = self.predict_landing(v0, h0, w0)
        return (float(direct[0]), physical[1]), stop_time
