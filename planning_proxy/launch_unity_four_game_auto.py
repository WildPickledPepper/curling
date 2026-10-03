#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键启动 Unity 四局制：服务端 + 双 AI + 自动浏览器点击。

这是把此前大采样使用的 Playwright 生命周期搬回当前对局：不依赖人工点击，
并且只在两名 AI 都实际收到 ``CONNECTNAME`` 后点击准备、两名 AI 都发送
``READYOK/NAME`` 后点击开始。
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import os
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SERVER_DIR = ROOT / "数字冰壶单机版_win" / "数字冰壶单机版"
SERVER_EXE = SERVER_DIR / "curling_server.exe"
RUNS = ROOT / "planning_proxy" / "runs"


def wait_port(port: int, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.4):
                return
        except OSError:
            time.sleep(0.2)
    raise TimeoutError(f"Unity 服务端没有在 {timeout:.0f} 秒内打开 {port} 端口")


def wait_markers(paths: list[Path], label: str, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if all(path.is_file() for path in paths):
            print(f"{label}：已就绪", flush=True)
            return
        time.sleep(0.1)
    missing = [str(path) for path in paths if not path.is_file()]
    raise TimeoutError(f"等待 {label} 超时；缺少 {missing}")


def stop_previous_unity() -> None:
    # 仅终止本项目当前启动的 Unity 服务与两种 Unity 对局客户端；不触碰正在
    # 跑的离线训练/本地评测进程。
    script = r'''
$targets = Get-CimInstance Win32_Process | Where-Object {
  $_.ProcessId -ne {PID} -and (
  $_.Name -ieq 'curling_server.exe' -or
  ($_.Name -ieq 'python.exe' -and $_.CommandLine -match 'unity_planner_robot.py|unity_stage_s_u6_robot.py|launch_unity_four_game_auto.py')
  )
}
$targets | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
'''
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script.replace("{PID}", str(os.getpid()))],
        check=False,
        capture_output=True,
    )


def prepare_debug_session(key: str) -> None:
    """注册 connectKey；这是旧自动采样流程启动浏览器前的必要步骤。"""

    payload = json.dumps({"humanFirst": True, "robotIndex": 0, "connectKey": key}).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:9007/debug/config",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        body = response.read().decode("utf-8", errors="replace").strip()
    if body.lower() != "ok":
        raise RuntimeError(f"Unity debug session 初始化失败: {body!r}")
    print(f"Unity 会话 key 已注册: {key}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", default="localtest")
    parser.add_argument("--planner-budget-seconds", type=float, default=105.0)
    parser.add_argument("--keep-existing-server", action="store_true")
    args = parser.parse_args()
    RUNS.mkdir(parents=True, exist_ok=True)
    session = RUNS / "unity_four_game_auto"
    session.mkdir(parents=True, exist_ok=True)
    markers = {
        "planner_connected": session / "planner.connected.json",
        "stage_connected": session / "stage.connected.json",
        "planner_ready": session / "planner.ready.json",
        "stage_ready": session / "stage.ready.json",
    }
    for path in markers.values():
        path.unlink(missing_ok=True)

    if not args.keep_existing_server:
        stop_previous_unity()
        time.sleep(0.8)
        server = subprocess.Popen([str(SERVER_EXE)], cwd=str(SERVER_DIR))
        print(f"curling_server PID={server.pid}", flush=True)
        wait_port(9007, 15)
    else:
        wait_port(9007, 5)
    # 保留旧流程的顺序：先为 key 建立 PlayerMgr 状态，再打开 WebGL 和两个外部 bot。
    prepare_debug_session(args.key)
    time.sleep(0.4)

    commands = [
        (
            "planner",
            [sys.executable, str(ROOT / "planning_proxy" / "unity_planner_robot.py"),
             "-H", "127.0.0.1", "-p", "7788", "-k", args.key,
             "--physics-seeds", "3", "--parent-regions", "3",
             "--decision-budget-seconds", str(args.planner_budget_seconds),
             "--wait-for-unity-seconds", "90",
             "--connected-marker", str(markers["planner_connected"]),
             "--ready-marker", str(markers["planner_ready"]),
             "--log", str(RUNS / "unity_planner.jsonl")],
        ),
        (
            "stage_s_u6",
            [sys.executable, str(ROOT / "training_research" / "opponents" / "unity_stage_s_u6_robot.py"),
             "-H", "127.0.0.1", "-p", "7788", "-k", args.key,
             "--wait-for-unity-seconds", "90",
             "--connected-marker", str(markers["stage_connected"]),
             "--ready-marker", str(markers["stage_ready"]),
             "--log", str(RUNS / "unity_stage_s_u6.jsonl")],
        ),
    ]
    players: list[subprocess.Popen] = []
    for name, command in commands:
        out = (session / f"{name}.stdout.log").open("w", encoding="utf-8")
        err = (session / f"{name}.stderr.log").open("w", encoding="utf-8")
        player = subprocess.Popen(command, cwd=str(ROOT), stdout=out, stderr=err)
        players.append(player)
        print(f"{name} PID={player.pid}", flush=True)

    trace: list[dict[str, object]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            args=["--window-size=1500,950", "--disable-web-security", "--autoplay-policy=no-user-gesture-required"],
        )
        context = browser.new_context(viewport={"width": 1500, "height": 950})
        page = context.new_page()
        page.goto(f"http://127.0.0.1:9007/?connectkey={args.key}", wait_until="domcontentloaded")
        page.bring_to_front()
        page.wait_for_function("""() => {
          const node = document.querySelector('#unity-loading-bar');
          return !!node && getComputedStyle(node).display === 'none';
        }""", timeout=120000)
        time.sleep(4.0)  # WebGL loading bar 消失到原生主菜单出现的固定切换时间。

        # 旧采样器已验证无限局制为 (475,534)。四局制按钮与其同列、上移 69 px。
        page.mouse.click(475, 465)
        page.screenshot(path=str(session / "01_four_game_clicked.png"))
        trace.append({"click": "four_games", "x": 475, "y": 465})
        wait_markers([markers["planner_connected"], markers["stage_connected"]], "双 AI TCP 连接", 45)

        page.mouse.click(761, 709)
        page.screenshot(path=str(session / "02_ready_clicked.png"))
        trace.append({"click": "ready", "x": 761, "y": 709})
        wait_markers([markers["planner_ready"], markers["stage_ready"]], "双 AI READYOK/NAME", 20)

        page.mouse.click(1015, 754)
        page.screenshot(path=str(session / "03_start_clicked.png"))
        trace.append({"click": "start", "x": 1015, "y": 754})
        (session / "ui_trace.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
        print("四局制已自动开始。浏览器保持打开，等待对局结束。", flush=True)
        while all(player.poll() is None for player in players):
            time.sleep(1)
        page.screenshot(path=str(session / "04_finished_or_client_exit.png"))
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
