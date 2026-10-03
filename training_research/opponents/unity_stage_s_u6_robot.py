#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 Stage-S U6 PPO 接入数字冰壶 Unity 的 TCP 协议。

此文件只做协议转接；PPO 推理仍由 ``stage_s_u6_adapter`` 启动已有的
Anaconda + PyTorch worker，不改 checkpoint、不把 Torch 混进 PhysX 环境。
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from training_research.opponents.stage_s_u6_adapter import StageSU6Opponent  # noqa: E402


def recv_message(sock: socket.socket) -> tuple[str, list[str]]:
    data = bytearray()
    while True:
        item = sock.recv(1)
        if not item or item == b"\0":
            break
        data.extend(item)
    fields = data.decode(errors="replace").strip().split()
    return (fields[0], fields[1:]) if fields else ("", [])


class UnityStageSRobot:
    def __init__(self, *, host: str, port: int, key: str, name: str, log_path: Path, connected_marker: Path | None, ready_marker: Path | None, verbose: bool) -> None:
        self.host, self.port, self.key, self.name, self.verbose = host, port, key, name, verbose
        self.log_path = log_path
        self.connected_marker = connected_marker
        self.ready_marker = ready_marker
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.position = [0.0] * 32
        self.shot_index = 0
        self.end_index = 0
        self.end_total = 4
        self.next_player = 0
        self.player_is_init: bool | None = None
        self.last_end_score = 0
        self.protocol_seen = False
        self.policy = StageSU6Opponent(deterministic=True)

    def write_log(self, row: dict[str, Any]) -> None:
        row["utc"] = datetime.now(timezone.utc).isoformat()
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    def mark(self, path: Path | None, event: str) -> None:
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"event": event, "name": self.name, "utc": datetime.now(timezone.utc).isoformat()}), encoding="utf-8")

    def send(self, sock: socket.socket, message: str) -> None:
        if self.verbose:
            print(f">>>> {message}", flush=True)
        sock.sendall(message.encode())

    def play(self) -> int:
        self.protocol_seen = False
        with socket.create_connection((self.host, self.port), timeout=20) as connection:
                # 20 秒仅限制连接建立；等待 Unity 页面点击准备时不应超时退出。
                connection.settimeout(None)
                print(f"已连接 Unity 服务 {self.host}:{self.port}", flush=True)
                self.send(connection, f"CONNECTKEY:{self.key}")
                empty = 0
                while True:
                    code, fields = recv_message(connection)
                    if self.verbose:
                        print(f"<<<< {code} {' '.join(fields)}", flush=True)
                    if not code:
                        empty += 1
                        if empty >= 5:
                            return 2 if self.player_is_init is None else 0
                        continue
                    empty = 0
                    # Unity 四局制尚未把双槽交给玩家时的 Error 不算握手成功；
                    # 继续重连直到收到 CONNECTNAME。
                    if code.lower().startswith("error") and self.player_is_init is None:
                        return 2
                    self.protocol_seen = True
                    if code == "CONNECTNAME":
                        self.player_is_init = bool(fields and fields[0] == "Player1")
                        self.mark(self.connected_marker, "connectname")
                        print("本局身份：" + ("先手/蓝方" if self.player_is_init else "后手/红方"), flush=True)
                    elif code == "ISREADY":
                        self.send(connection, "READYOK")
                        self.send(connection, f"NAME {self.name}")
                        self.mark(self.ready_marker, "readyok_name")
                    elif code == "NEWGAME":
                        self.position = [0.0] * 32
                    elif code == "SETSTATE" and len(fields) >= 4:
                        self.shot_index, self.end_index, self.end_total, self.next_player = map(int, fields[:4])
                    elif code == "POSITION":
                        if len(fields) != 32:
                            raise ValueError(f"POSITION 参数数量应为 32，实际为 {len(fields)}")
                        self.position = [float(value) for value in fields]
                    elif code == "GO":
                        started = time.perf_counter()
                        try:
                            if self.player_is_init is None:
                                self.player_is_init = self.next_player == 0
                            result = self.policy.choose(
                                self.position, player_is_init=self.player_is_init,
                                shot_num=self.shot_index, end_score=self.last_end_score,
                                total_ends=max(1, self.end_total), current_player=self.next_player,
                            )
                            shot = result.bestshot
                            detail: dict[str, Any] = {
                                "tactic": result.tactic, "actionId": result.action_id,
                                "value": result.value, "fallback": result.fallback,
                                "stageSP1PeelGuard": result.stage_s_p1_peel_guard,
                                "stageSP2BlockedDraw": result.stage_s_p2_blocked_draw,
                            }
                        except Exception as error:
                            shot, detail = (3.0, 0.0, 0.0), {"mode": "exception_fallback", "error": repr(error)}
                        elapsed = time.perf_counter() - started
                        self.send(connection, "BESTSHOT %.6f %.6f %.6f" % shot)
                        self.write_log({
                            "event": "decision", "endIndex": self.end_index,
                            "shotIndex": self.shot_index, "playerIsInit": self.player_is_init,
                            "position": self.position, "bestshot": shot,
                            "elapsedSeconds": elapsed, "detail": detail,
                        })
                        print(f"第 {self.end_index + 1} 局第 {self.shot_index + 1} 壶：{shot}（{elapsed:.2f}s）", flush=True)
                    elif code == "CENTERLINE_VIOLATION":
                        self.send(connection, "CENTERLINE_CHOICE RESET")
                    elif code == "SCORE":
                        self.last_end_score = int(fields[0]) if fields else 0
                        self.write_log({"event": "score", "endIndex": self.end_index, "score": self.last_end_score})
                        if self.end_total != -1:
                            if self.last_end_score > 0:
                                self.player_is_init = True
                            elif self.last_end_score < 0:
                                self.player_is_init = False
                            elif self.player_is_init is not None:
                                self.player_is_init = not self.player_is_init
                        self.position = [0.0] * 32
                    elif code == "GAMEOVER":
                        self.write_log({"event": "gameover", "result": fields})
                        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="将 Stage-S PPO 接入本地 Unity 四局制")
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("-k", "--key", default="localtest")
    parser.add_argument("--name", default="StageSU6PPO")
    parser.add_argument("--wait-for-unity-seconds", type=float, default=300.0)
    parser.add_argument("--log", type=Path, default=ROOT / "planning_proxy" / "runs" / "unity_stage_s_u6.jsonl")
    parser.add_argument("--connected-marker", type=Path)
    parser.add_argument("--ready-marker", type=Path)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    robot = UnityStageSRobot(host=args.host, port=args.port, key=args.key, name=args.name, log_path=args.log, connected_marker=args.connected_marker, ready_marker=args.ready_marker, verbose=args.verbose)
    deadline = time.monotonic() + max(0.0, args.wait_for_unity_seconds)
    try:
        while True:
            try:
                status = robot.play()
            except OSError as error:
                status = 2
                if args.verbose:
                    print(f"等待 Unity 四局制协议：{error!r}", flush=True)
            if status != 2 or time.monotonic() >= deadline:
                return status
            time.sleep(0.5)
    finally:
        robot.policy.close()


if __name__ == "__main__":
    raise SystemExit(main())
