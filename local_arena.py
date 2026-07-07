# -*- coding: utf-8 -*-
"""Manage the official standalone curling server and local robot processes."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path
from typing import Iterable, Optional

import psutil


ROOT = Path(__file__).resolve().parent
SERVER_DIR = ROOT / "数字冰壶单机版_win" / "数字冰壶单机版"
SERVER_EXE = SERVER_DIR / "curling_server.exe"
UI_URL = "http://127.0.0.1:9007/?connectkey=localtest"
HOST = "127.0.0.1"
PORT = 7788
CONNECT_KEY = "localtest"
STATE_FILE = ROOT / "log" / "local_arena_processes.json"


def process_matches(pid: int, expected: str) -> bool:
    try:
        process = psutil.Process(pid)
        command = " ".join(process.cmdline()).lower()
        executable = (process.exe() or "").lower()
    except (psutil.Error, OSError):
        return False
    marker = expected.lower()
    return marker in command or marker in executable


def read_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def write_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def find_server_pid() -> Optional[int]:
    expected = str(SERVER_EXE).lower()
    for process in psutil.process_iter(["pid", "exe"]):
        try:
            if (process.info["exe"] or "").lower() == expected:
                return int(process.info["pid"])
        except (psutil.Error, OSError):
            continue
    return None


def wait_for_port(port: int, timeout: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        for connection in psutil.net_connections(kind="tcp"):
            if connection.laddr and connection.laddr.port == port:
                if connection.status == psutil.CONN_LISTEN:
                    return True
        time.sleep(0.2)
    return False


def start_server() -> int:
    pid = find_server_pid()
    if pid is not None:
        print(f"单机服务器已运行，PID={pid}", flush=True)
        return pid
    if not SERVER_EXE.exists():
        raise FileNotFoundError(f"未找到单机服务器：{SERVER_EXE}")

    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    process = subprocess.Popen(
        [str(SERVER_EXE)],
        cwd=SERVER_DIR,
        creationflags=creation_flags,
    )
    if not wait_for_port(PORT):
        process.terminate()
        raise RuntimeError("单机服务器启动超时，TCP 7788 未监听")
    print(f"单机服务器已启动，PID={process.pid}", flush=True)
    return int(process.pid)


def refresh_connect_key() -> None:
    with urllib.request.urlopen(UI_URL, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(
                f"本地竞技场页面返回异常状态：{response.status}"
            )
        response.read(1)
    print(f"连接密钥已刷新：{CONNECT_KEY}", flush=True)


def robot_command(name: str, extra_args: Iterable[str]) -> list[str]:
    return [
        sys.executable,
        str(ROOT / "search_distill_robot.py"),
        "--key",
        CONNECT_KEY,
        "-H",
        HOST,
        "-p",
        str(PORT),
        "--name",
        name,
        *extra_args,
    ]


def start_robot(slot: int, extra_args: Iterable[str]) -> int:
    log_dir = ROOT / "log" / "local_arena"
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout = (log_dir / f"player{slot}.out.log").open("w", encoding="utf-8")
    stderr = (log_dir / f"player{slot}.err.log").open("w", encoding="utf-8")
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    process = subprocess.Popen(
        robot_command(f"LocalAI-P{slot}", extra_args),
        cwd=ROOT,
        stdout=stdout,
        stderr=stderr,
        creationflags=creation_flags,
    )
    print(f"Player{slot} 机器人已连接，PID={process.pid}", flush=True)
    return int(process.pid)


def start(args: argparse.Namespace) -> None:
    state = read_state()
    state["server"] = start_server()
    refresh_connect_key()
    if args.open_ui:
        webbrowser.open(UI_URL)
        print(f"已打开 {UI_URL}", flush=True)
    if args.robots:
        robot_args = ["--show-msg"] if args.show_msg else []
        state["player1"] = start_robot(1, robot_args)
        state["player2"] = start_robot(2, robot_args)
        print("在页面中选择双玩家/无限局并开始对局。", flush=True)
    write_state(state)


def stop_process(pid: int, expected: str) -> None:
    if not process_matches(pid, expected):
        return
    process = psutil.Process(pid)
    children = process.children(recursive=True)
    for child in children:
        child.terminate()
    process.terminate()
    _, alive = psutil.wait_procs([*children, process], timeout=5)
    for remaining in alive:
        remaining.kill()
    print(f"已停止 PID={pid}", flush=True)


def stop() -> None:
    state = read_state()
    stop_process(int(state.get("player1", 0)), "search_distill_robot.py")
    stop_process(int(state.get("player2", 0)), "search_distill_robot.py")
    server_pid = find_server_pid()
    if server_pid is not None:
        stop_process(server_pid, "curling_server.exe")
    STATE_FILE.unlink(missing_ok=True)


def status() -> None:
    state = read_state()
    server_pid = find_server_pid()
    print(f"server: {'running PID=' + str(server_pid) if server_pid else 'stopped'}")
    for slot in (1, 2):
        pid = int(state.get(f"player{slot}", 0))
        running = pid > 0 and process_matches(pid, "search_distill_robot.py")
        print(f"player{slot}: {'running PID=' + str(pid) if running else 'stopped'}")
    print(f"ui: {UI_URL}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("--robots", action="store_true")
    start_parser.add_argument("--show-msg", action="store_true")
    start_parser.add_argument(
        "--open-ui", action=argparse.BooleanOptionalAction, default=True
    )
    subparsers.add_parser("status")
    subparsers.add_parser("stop")
    subparsers.add_parser("open")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "start":
        start(args)
    elif args.command == "stop":
        stop()
    elif args.command == "status":
        status()
    elif args.command == "open":
        webbrowser.open(UI_URL)


if __name__ == "__main__":
    main()
