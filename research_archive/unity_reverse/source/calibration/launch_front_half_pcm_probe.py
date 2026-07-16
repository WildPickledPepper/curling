#!/usr/bin/env python3
"""Launch Unity WebGL with the front-half sliding-to-first-PCM probe enabled."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = PROJECT_ROOT / "tools" / "calibration" / "launch_unity_probe_browser.py"


def main() -> int:
    cmd = [
        sys.executable,
        str(LAUNCHER),
        "--stream-events",
        "--stream-no-store",
        "--no-poll-events",
        "--sliding-trace-hooks",
        "--sliding-trace-max-random-events",
        "30000",
        "--sliding-trace-max-fixed-events",
        "12000",
        "--physx-native-hooks",
        "--physx-native-capture-mode",
        "armed",
        "--physx-native-max-dumps",
        "120",
        "--physx-native-arm-ms",
        "2500",
        "--physx-native-window-bytes",
        "8192",
        "--physx-native-solver-constraint-bytes",
        "4096",
        "--physx-native-solver-desc-records",
        "4",
        "--physx-native-solver-body-bytes",
        "512",
        "--physx-native-geometry-bytes",
        "128",
        "--physx-native-hull-data-bytes",
        "1024",
        "--physx-native-cache-bytes",
        "128",
        "--physx-native-manifold-bytes",
        "4096",
        "--physx-native-shape-interaction-bytes",
        "2048",
    ]
    cmd.extend(sys.argv[1:])
    return subprocess.call(cmd, cwd=PROJECT_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
