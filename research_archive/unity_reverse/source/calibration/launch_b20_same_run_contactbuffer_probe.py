#!/usr/bin/env python3
"""Launch the single-shot B20 same-run PCM/finalizer capture browser."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = PROJECT_ROOT / "tools" / "calibration" / "launch_unity_probe_browser.py"


def main() -> int:
    command = [
        sys.executable,
        str(LAUNCHER),
        "--stream-events",
        "--stream-no-store",
        "--no-poll-events",
        "--physx-native-hooks",
        "--physx-native-names",
        "PxcPCMContactConvexConvex,createFinalizeSolverContacts",
        "--physx-native-capture-mode",
        "armed",
        "--physx-native-dynamic-dynamic-only-names",
        "createFinalizeSolverContacts",
        "--physx-native-max-dumps",
        "8",
        "--physx-native-window-bytes",
        "128",
        "--physx-native-max-pointer-args",
        "1",
        "--physx-native-cache-bytes",
        "64",
        "--physx-native-manifold-bytes",
        "256",
        "--physx-native-shape-interaction-bytes",
        "512",
        "--no-physx-native-nested-raw",
    ]
    command.extend(sys.argv[1:])
    return subprocess.call(command, cwd=PROJECT_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
