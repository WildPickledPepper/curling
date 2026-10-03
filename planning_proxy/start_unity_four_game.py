#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在本地 Unity 四局制中同时启动规划器和 Stage-S PPO。

先在 WebGL 页面选择【四局制】，再运行本脚本；两个客户端连接完成后在
页面依次点击【准备】和【开始】即可。日志写入 planning_proxy/runs/。
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("-k", "--key", default="localtest")
    parser.add_argument("--planner-budget-seconds", type=float, default=105.0)
    args = parser.parse_args()
    runs = ROOT / "planning_proxy" / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    processes = [
        (
            "planner",
            [sys.executable, str(ROOT / "planning_proxy" / "unity_planner_robot.py"),
             "-H", args.host, "-p", str(args.port), "-k", args.key,
             "--physics-seeds", "3", "--parent-regions", "3",
             "--decision-budget-seconds", str(args.planner_budget_seconds),
             "--wait-for-unity-seconds", "300",
             "--log", str(runs / "unity_planner.jsonl")],
        ),
        (
            "stage_s_u6",
            [sys.executable, str(ROOT / "training_research" / "opponents" / "unity_stage_s_u6_robot.py"),
             "-H", args.host, "-p", str(args.port), "-k", args.key,
             "--wait-for-unity-seconds", "300",
             "--log", str(runs / "unity_stage_s_u6.jsonl")],
        ),
    ]
    for name, command in processes:
        stdout = (runs / f"unity_{name}.stdout.log").open("w", encoding="utf-8")
        stderr = (runs / f"unity_{name}.stderr.log").open("w", encoding="utf-8")
        process = subprocess.Popen(command, cwd=str(ROOT), stdout=stdout, stderr=stderr)
        print(f"{name}: PID={process.pid}")
    print("两个客户端已启动；回 Unity 页面依次点击【准备】、【开始】。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
