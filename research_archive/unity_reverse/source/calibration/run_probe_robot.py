#!/usr/bin/env python3
"""Run one simple socket robot for Unity runtime probing."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.protocol.AIRobot import AIRobot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", default="localtest")
    parser.add_argument("--name", default="ProbeRobot")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7788)
    parser.add_argument("--show-msg", action="store_true")
    args = parser.parse_args()

    robot = AIRobot(args.key, name=args.name, host=args.host, port=args.port, show_msg=args.show_msg)
    robot.recv_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
