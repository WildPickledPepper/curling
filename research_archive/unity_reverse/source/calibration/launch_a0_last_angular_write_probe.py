#!/usr/bin/env python3
"""Launch the bounded A0 probe for the final script angular-velocity write."""

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
        "--a0-fixed-tick-resolver-hook",
    ]
    command.extend(sys.argv[1:])
    return subprocess.call(command, cwd=PROJECT_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
