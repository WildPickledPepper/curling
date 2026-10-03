#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在不覆盖运行时 `.pyd` 的前提下，对候选原生扩展运行测试模块。

Windows 的 ``spawn`` 子进程会重新执行本文件；扩展路径通过环境变量继承，
因此可覆盖包含多进程的语义合同测试，不能从 ``python -`` 的标准输入执行。
"""

from __future__ import annotations

import argparse
import os
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OVERRIDE_ENV = "CURLING_PYPHYSX_EXTENSION_OVERRIDE"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def install_override_from_environment() -> None:
    raw = os.environ.get(OVERRIDE_ENV)
    if not raw:
        return
    extension = Path(raw)
    if not extension.is_file():
        raise RuntimeError(f"候选原生扩展不存在：{extension}")
    runtime_dir = PROJECT_ROOT / "local_simulator" / "runtime" / "pyphysx"
    if str(runtime_dir) not in sys.path:
        sys.path.insert(0, str(runtime_dir))
    from local_simulator import runtime_loader

    runtime_loader.BUNDLED_EXTENSION = extension


install_override_from_environment()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extension", type=Path, required=True)
    parser.add_argument("module", nargs="+", help="unittest 模块名")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    os.environ[OVERRIDE_ENV] = str(args.extension.resolve())
    install_override_from_environment()
    suite = unittest.defaultTestLoader.loadTestsFromNames(args.module)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    raise SystemExit(not result.wasSuccessful())


if __name__ == "__main__":
    main()
