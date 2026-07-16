#!/usr/bin/env python3
"""Print one recovered CurlingMotion spin update for positive and negative turns.

Run from the DCCourse directory with the bundled CPython 3.8 environment:
    & 'D:\\esp\\tmp\\curling_pyphysx_conda\\python.exe' local_simulator\\examples\\inspect_spin_step.py
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from local_simulator.runtime_support.tools.reverse.recovered_curling_motion import (
    B2Vec2,
    STEP,
    newfrictionstep,
    unity_friction,
)


def main() -> int:
    friction = unity_friction(sweeping=False, noise=0.0)
    before = B2Vec2(0.10, 3.20)
    print(f"non_sweeping_friction={friction:.9f}; one fixed tick={STEP * 10.0:.3f}s")
    for angular_velocity in (5.0, -5.0):
        after = newfrictionstep(friction, before, angular_velocity, STEP)
        print(
            f"w={angular_velocity:+.3f} -> "
            f"vx={after.v.x:+.12f}, vy={after.v.y:+.12f}, w_next={after.angle:+.12f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
