"""Course-platform entrypoint for the current non-sweeping PhysX planner.

Keep this file and ``planner_payload.zip`` together in the course workspace
root, then select this file as the submitted AI main script.  The payload is
ordinary zip data so the native extension survives upload; it is extracted to
the player working directory before the normal Unity socket robot starts.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "planner_payload.zip"
RUNTIME = ROOT / ".planner_runtime"
ENTRY = RUNTIME / "planning_proxy" / "unity_planner_robot.py"
MARKER = RUNTIME / ".payload_ready"


def prepare_runtime() -> Path:
    if not PAYLOAD.is_file():
        raise RuntimeError("缺少 planner_payload.zip；它必须与 planner_submission.py 放在同一目录。")
    if not MARKER.is_file() or not ENTRY.is_file():
        RUNTIME.mkdir(exist_ok=True)
        with zipfile.ZipFile(PAYLOAD) as archive:
            archive.extractall(RUNTIME)
        MARKER.write_text("ready\n", encoding="ascii")
    return ENTRY


def main() -> None:
    entry = prepare_runtime()
    if str(RUNTIME) not in sys.path:
        sys.path.insert(0, str(RUNTIME))
    # 保留 30 秒平台余量；候选空间本身使用规划器内置的 4305 条充足粗筛，
    # 不是用短秒数替代候选覆盖。
    defaults = {
        "--physics-seeds": "3",
        "--parent-regions": "3",
        "--decision-budget-seconds": "90",
    }
    for option, value in defaults.items():
        if option not in sys.argv:
            sys.argv.extend([option, value])
    # Leave unambiguous evidence in the official match log that this is the
    # real bundled PhysX runtime rather than the old fixed-shot probe.
    import numpy as np
    from local_simulator.runtime_loader import install_bundled_pyphysx

    pyphysx = install_bundled_pyphysx()
    print(
        f"PLANNER_NATIVE_BOOT python={sys.version_info.major}.{sys.version_info.minor} "
        f"numpy={np.__version__} extension={getattr(pyphysx, '__file__', '')}",
        flush=True,
    )
    # Preserve the course command-line arguments (-H/-p/-k) verbatim.
    sys.argv[0] = str(entry)
    runpy.run_path(str(entry), run_name="__main__")


if __name__ == "__main__":
    main()
