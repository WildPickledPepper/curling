# -*- coding: utf-8 -*-
"""Compatibility entrypoint for the course socket robot base class."""

from __future__ import annotations

import runpy

from tools.protocol.AIRobot import AIRobot

__all__ = ["AIRobot"]


if __name__ == "__main__":
    runpy.run_module("tools.protocol.AIRobot", run_name="__main__")
