#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把当前 PhysX 规划器接到数字冰壶 Unity TCP 协议。

运行方式（通常由本地 ``curling_server.exe`` 自动启动）：

    python unity_planner_robot.py -H 127.0.0.1 -p 7788 -k <connect-key>

这个适配层只负责协议和棋盘坐标转换：每次收到 ``GO`` 时，调用
``ProxyMatchPlayer`` 产生 ``BESTSHOT``。它不伪造 Unity 的 yaw 或摩擦序列；
Unity 没有通过协议发送这些量，因此这里固定为本地规划器的保守预测条件，并把
每手输入、输出和耗时记录为 JSONL，供赛后按真实 Unity 落点核对。
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


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer  # noqa: E402


def recv_message(sock: socket.socket) -> tuple[str, list[str]]:
    """读取以 NUL 结尾的一条 Unity 协议消息。"""

    buffer = bytearray()
    while True:
        data = sock.recv(1)
        if not data or data == b"\0":
            break
        buffer.extend(data)
    pieces = buffer.decode(errors="replace").strip().split()
    return (pieces[0], pieces[1:]) if pieces else ("", [])


class UnityPlannerRobot:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        key: str,
        name: str,
        physics_seeds: int,
        parent_regions: int,
        decision_budget_seconds: float,
        log_path: Path,
        connected_marker: Path | None,
        ready_marker: Path | None,
        verbose: bool,
    ) -> None:
        self.host = host
        self.port = port
        self.key = key
        self.name = name
        self.verbose = verbose
        self.log_path = log_path
        self.connected_marker = connected_marker
        self.ready_marker = ready_marker
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.position = [0.0] * 32
        self.shot_index = 0
        self.end_index = 0
        self.end_total = -1
        self.next_player = 0
        self.protocol_seen = False
        self.player_is_init: bool | None = None
        self.planner = ProxyMatchPlayer(
            physics_seeds=physics_seeds,
            parent_regions=parent_regions,
            decision_budget_seconds=decision_budget_seconds,
        )

    def log(self, row: dict[str, Any]) -> None:
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

    def parse_position(self, fields: list[str]) -> None:
        if len(fields) != 32:
            raise ValueError(f"POSITION 参数数量应为 32，实际为 {len(fields)}")
        self.position = [float(value) for value in fields]

    def states(self) -> list[dict[str, Any]]:
        # Unity POSITION 的顺序正是每一手的投掷顺序；偶数槽为本局先手、
        # 奇数槽为后手。坐标 (0, 0) 表示未投或已出界。
        result: list[dict[str, Any]] = []
        for index in range(16):
            x, y = self.position[2 * index : 2 * index + 2]
            result.append({"enabled": not (x == 0.0 and y == 0.0), "x": x, "y": y, "yaw": 0.0})
        return result

    def choose(self) -> tuple[tuple[float, float, float], dict[str, Any]]:
        if self.player_is_init is None:
            # 服务端按正常顺序总会先发 CONNECTNAME；若异常缺失，使用当前
            # SETSTATE 作为安全猜测，并在日志中明确标出来。
            self.player_is_init = self.next_player == 0
            identity_source = "SETSTATE_fallback"
        else:
            identity_source = "CONNECTNAME"
        team = 0 if self.player_is_init else 1
        shot, detail = self.planner.choose(
            self.states(),
            proxy_team=team,
            shot_index=self.shot_index,
            match_seed=self.end_index * 1009,
        )
        detail["identitySource"] = identity_source
        return shot, detail

    def serve(self) -> int:
        self.protocol_seen = False
        with socket.create_connection((self.host, self.port), timeout=20) as sock:
            # ``create_connection`` 的 20 秒只用于建连；对局开始前服务端可以
            # 合法地长时间不发消息，不能把这个建连超时带进 recv 循环。
            sock.settimeout(None)
            print(f"已连接 Unity 服务 {self.host}:{self.port}", flush=True)
            self.send(sock, f"CONNECTKEY:{self.key}")
            empty_messages = 0
            while True:
                code, fields = recv_message(sock)
                if self.verbose:
                    print(f"<<<< {code} {' '.join(fields)}", flush=True)
                if not code:
                    empty_messages += 1
                    if empty_messages >= 5:
                        # WebGL 尚未进入四局制时，服务端会接受 TCP 再立刻关闭。
                        # 在收到任何协议消息前这是“早到”，交给 main 重连。
                        return 2 if self.player_is_init is None else 0
                    continue
                empty_messages = 0
                # 四局制等待页尚未完成 PlayerMgr 交接时，服务端会回 Error
                # 后主动断开。它不是有效握手；必须继续重连直到 CONNECTNAME。
                if code.lower().startswith("error") and self.player_is_init is None:
                    return 2
                self.protocol_seen = True
                if code == "CONNECTNAME":
                    self.player_is_init = bool(fields and fields[0] == "Player1")
                    self.mark(self.connected_marker, "connectname")
                    print("本局身份：" + ("先手/蓝方" if self.player_is_init else "后手/红方"), flush=True)
                elif code == "ISREADY":
                    self.send(sock, "READYOK")
                    self.send(sock, f"NAME {self.name}")
                    self.mark(self.ready_marker, "readyok_name")
                elif code == "NEWGAME":
                    self.position = [0.0] * 32
                elif code == "SETSTATE":
                    if len(fields) >= 4:
                        self.shot_index, self.end_index, self.end_total, self.next_player = map(int, fields[:4])
                elif code == "POSITION":
                    self.parse_position(fields)
                elif code == "GO":
                    started = time.perf_counter()
                    try:
                        shot, detail = self.choose()
                    except Exception as error:  # 保证单手异常不让 Unity 空等两分钟
                        shot, detail = (3.0, 0.0, 0.0), {"mode": "exception_fallback", "error": repr(error)}
                    elapsed = time.perf_counter() - started
                    v0, h0, w0 = shot
                    self.send(sock, f"BESTSHOT {v0:.6f} {h0:.6f} {w0:.6f}")
                    self.log({
                        "event": "decision",
                        "endIndex": self.end_index,
                        "shotIndex": self.shot_index,
                        "playerIsInit": self.player_is_init,
                        "nextPlayer": self.next_player,
                        "position": self.position,
                        "bestshot": [v0, h0, w0],
                        "elapsedSeconds": elapsed,
                        "detail": detail,
                    })
                    print(f"第 {self.end_index + 1} 局第 {self.shot_index + 1} 壶：{v0:.3f}, {h0:.3f}, {w0:.3f}（{elapsed:.2f}s）", flush=True)
                elif code == "CENTERLINE_VIOLATION":
                    # 规划器已在候选筛选中嵌入自由防守区约束；若 Unity 仍判罚，
                    # 用 RESET 回到犯规前而不是把错误棋盘继续带入下一手。
                    self.send(sock, "CENTERLINE_CHOICE RESET")
                    self.log({"event": "centreline_violation", "endIndex": self.end_index, "shotIndex": self.shot_index})
                elif code == "SCORE":
                    score = int(fields[0]) if fields else 0
                    self.log({"event": "score", "endIndex": self.end_index, "score": score})
                    # 与官方模板一致：得分方下一局先手；0 分换先后手。
                    if self.end_total != -1:
                        if score > 0:
                            self.player_is_init = True
                        elif score < 0:
                            self.player_is_init = False
                        elif self.player_is_init is not None:
                            self.player_is_init = not self.player_is_init
                    self.position = [0.0] * 32
                elif code == "GAMEOVER":
                    self.log({"event": "gameover", "result": fields})
                    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="将规划器接入本地 Unity 数字冰壶")
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("-k", "--key", default="")
    parser.add_argument("--name", default="PhysXPlanner")
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--wait-for-unity-seconds", type=float, default=300.0)
    parser.add_argument("--log", type=Path, default=ROOT / "planning_proxy" / "runs" / "unity_planner.jsonl")
    parser.add_argument("--connected-marker", type=Path)
    parser.add_argument("--ready-marker", type=Path)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    robot = UnityPlannerRobot(
        host=args.host, port=args.port, key=args.key, name=args.name,
        physics_seeds=args.physics_seeds, parent_regions=args.parent_regions,
        decision_budget_seconds=args.decision_budget_seconds, log_path=args.log,
        connected_marker=args.connected_marker, ready_marker=args.ready_marker,
        verbose=args.verbose,
    )
    deadline = time.monotonic() + max(0.0, args.wait_for_unity_seconds)
    while True:
        try:
            status = robot.serve()
        except OSError as error:
            status = 2
            if args.verbose:
                print(f"等待 Unity 四局制协议：{error!r}", flush=True)
        if status != 2 or time.monotonic() >= deadline:
            return status
        time.sleep(0.5)


if __name__ == "__main__":
    raise SystemExit(main())
