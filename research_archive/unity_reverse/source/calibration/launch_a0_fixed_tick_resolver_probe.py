#!/usr/bin/env python3
"""Prepare the bounded A0 actor-core versus PCM-cache probe.

The launcher captures only the first dynamic-dynamic manager's compact rigid-core
windows and the first convex-convex PCM input transforms. It intentionally avoids
always-on stone-ice and solver payloads.
"""

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
        "PxsContext.contactManagerDiscreteUpdate,PxcPCMContactConvexConvex",
        "--physx-native-always-names",
        "PxsContext.contactManagerDiscreteUpdate",
        "--physx-native-dynamic-dynamic-task-only-names",
        "PxsContext.contactManagerDiscreteUpdate",
        "--physx-native-rigid-core-windows",
        "--physx-native-rigid-core-bytes",
        "160",
        "--physx-native-max-dumps",
        "1",
        "--physx-native-window-bytes",
        "128",
        "--physx-native-max-pointer-args",
        "0",
        "--physx-native-cache-bytes",
        "64",
        "--physx-native-manifold-bytes",
        "128",
        "--no-physx-native-nested-raw",
    ]
    command.extend(sys.argv[1:])
    return subprocess.call(command, cwd=PROJECT_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
