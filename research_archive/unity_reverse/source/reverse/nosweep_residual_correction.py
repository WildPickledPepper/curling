#!/usr/bin/env python3
"""Apply no-sweep endpoint residual correction configs."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "unity_nosweep_residual_correction.controlled.json"


def load_correction(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("mode") != "no_sweep_endpoint_residual_correction":
        raise ValueError(f"unsupported correction mode: {payload.get('mode')!r}")
    return payload


def feature_value(name: str, *, motion_vx: float, motion_vy: float, motion_w: float) -> float:
    if name == "1":
        return 1.0
    if name == "motion_speed":
        return math.hypot(motion_vx, motion_vy)
    if name == "motion_vx":
        return motion_vx
    if name == "motion_w":
        return motion_w
    if name == "abs_motion_w":
        return abs(motion_w)
    if name == "motion_w2":
        return motion_w * motion_w
    if name == "motion_vx_motion_w":
        return motion_vx * motion_w
    raise KeyError(name)


def predict_residual(
    payload: dict[str, Any],
    *,
    motion_vx: float,
    motion_vy: float,
    motion_w: float,
) -> tuple[float, float]:
    features = [
        feature_value(name, motion_vx=motion_vx, motion_vy=motion_vy, motion_w=motion_w)
        for name in payload["features"]
    ]
    coef_x = payload["coefficients_dx"]
    coef_y = payload["coefficients_dy"]
    if len(features) != len(coef_x) or len(features) != len(coef_y):
        raise ValueError("feature/coefficient length mismatch")
    dx = sum(float(coef) * value for coef, value in zip(coef_x, features))
    dy = sum(float(coef) * value for coef, value in zip(coef_y, features))
    return dx, dy


def correct_endpoint(
    x: float,
    y: float,
    *,
    motion_vx: float,
    motion_vy: float,
    motion_w: float,
    payload: dict[str, Any] | None = None,
) -> tuple[float, float]:
    correction = load_correction() if payload is None else payload
    dx, dy = predict_residual(
        correction,
        motion_vx=motion_vx,
        motion_vy=motion_vy,
        motion_w=motion_w,
    )
    return x - dx, y - dy
