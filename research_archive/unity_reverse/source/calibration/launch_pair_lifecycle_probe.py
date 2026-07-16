#!/usr/bin/env python3
"""Launch the six-shot pair-lifecycle runtime probe.

This records only the PCM task and finalizer boundaries needed to distinguish
new contact-manager registration from a refresh. It does not drive Unity or
send gameplay commands.
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
        "--game-object-activation-hook",
        "--mesh-collider-activation-hook",
        "--overlap-created-hook",
        "--physx-native-hooks",
        "--physx-native-names",
        "PxsContext.contactManagerDiscreteUpdate,createFinalizeSolverContacts,PxcPCMContactConvexConvex",
        "--physx-native-capture-mode",
        "armed",
        "--physx-native-always-names",
        "PxsContext.contactManagerDiscreteUpdate",
        "--physx-native-arm-only-names",
        "PxcPCMContactConvexConvex",
        "--physx-native-dynamic-dynamic-only-names",
        "createFinalizeSolverContacts",
        "--physx-native-max-dumps",
        "18000",
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
