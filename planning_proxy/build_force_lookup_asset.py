#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重新生成随规划代理交付的白盒受力表资产。

仅在恢复公式或基础摩擦常数改变后运行；正常部署与比赛推理不需要运行此脚本。
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from analytic_proxy import DEFAULT_FORCE_LOOKUP_ASSET, calibrate_force_lookup  # noqa: E402


def main() -> int:
    lookup = calibrate_force_lookup(prefer_packaged=False)
    DEFAULT_FORCE_LOOKUP_ASSET.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        DEFAULT_FORCE_LOOKUP_ASSET,
        speed_nodes=lookup.speed_nodes,
        spin_nodes=lookup.spin_nodes,
        drag_mps2=lookup.drag_mps2,
        turn_rate_radps=lookup.turn_rate_radps,
        spin_decay_per_s=lookup.spin_decay_per_s,
    )
    print("已生成 %s | %s" % (DEFAULT_FORCE_LOOKUP_ASSET, lookup.metadata()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
