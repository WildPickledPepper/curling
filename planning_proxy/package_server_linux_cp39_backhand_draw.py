#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成不覆盖旧包的课程平台 Linux CP39 后手绕屏风修复包。"""

from __future__ import annotations

from pathlib import Path

import package_server_linux_cp39_notebook as base


base.NAME = "server_linux_cp39_physx_state_machine_20260721_backhand_draw"
base.OUT = Path(base.PROXY) / base.NAME
base.ARCHIVE = Path(base.PROXY) / f"{base.NAME}.zip"
base.build()
