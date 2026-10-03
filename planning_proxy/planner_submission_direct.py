"""Direct-file course-platform entrypoint for the current PhysX planner.

Use this when the course upload has been verified to preserve the accompanying
``local_simulator/runtime/pyphysx/_pyphysx.cp313-win_amd64.pyd`` file.  Unlike
``planner_submission.py`` it performs no zip extraction.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ENTRY = ROOT / "planning_proxy" / "unity_planner_robot.py"


def main() -> None:
    if not ENTRY.is_file():
        raise RuntimeError("缺少 planning_proxy/unity_planner_robot.py；请保持提交目录结构。")
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    defaults = {
        "--physics-seeds": "3",
        "--parent-regions": "3",
        "--decision-budget-seconds": "90",
    }
    for option, value in defaults.items():
        if option not in sys.argv:
            sys.argv.extend([option, value])
    import numpy as np
    from local_simulator.runtime_loader import install_bundled_pyphysx

    pyphysx = install_bundled_pyphysx()
    print(
        f"PLANNER_NATIVE_BOOT python={sys.version_info.major}.{sys.version_info.minor} "
        f"numpy={np.__version__} extension={getattr(pyphysx, '__file__', '')}",
        flush=True,
    )
    sys.argv[0] = str(ENTRY)
    runpy.run_path(str(ENTRY), run_name="__main__")


if __name__ == "__main__":
    main()
