#!/usr/bin/env python3
"""Verify that this handoff package can load its matching strict PhysX ABI."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    from local_simulator.runtime_loader import install_bundled_pyphysx

    module = install_bundled_pyphysx()
    if not hasattr(module, "curling_new_friction_step"):
        raise SystemExit("扩展不是新版：缺少 curling_new_friction_step")
    if not hasattr(module.Scene, "simulate_until_quiet"):
        raise SystemExit("扩展不是新版：缺少 simulate_until_quiet")
    if not hasattr(module.Scene, "simulate_curling_until_first_contact"):
        raise SystemExit("扩展不是新版：缺少 simulate_curling_until_first_contact")
    print(
        "OK: bundled pyphysx native training loops are ready "
        f"(CPython {sys.version_info.major}.{sys.version_info.minor})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
