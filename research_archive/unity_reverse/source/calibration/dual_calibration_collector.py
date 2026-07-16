#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect official-server calibration data with both players controlled by us."""

from __future__ import annotations

import argparse
import itertools
import json
import random
import select
import socket
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Sequence


EMPTY_POSITION_PAYLOAD = " ".join("0" for _ in range(32))


@dataclass
class ShotRequest:
    sample_id: int
    v0: float
    h0: float
    w0: float


@dataclass
class SampleRecord:
    sample_id: int
    requested_v0: float
    requested_h0: float
    requested_w0: float
    connect_name: str
    player_is_init: bool
    active_shot_num: int
    round_num: int
    round_total: int
    next_shot: int
    used_reset: bool
    motion_x: Optional[float]
    motion_y: Optional[float]
    motion_vx: Optional[float]
    motion_vy: Optional[float]
    motion_w: Optional[float]
    final_x: Optional[float]
    final_y: Optional[float]
    in_play: bool
    issued_at_utc: str
    received_at_utc: str


@dataclass
class PendingShot:
    shot: ShotRequest
    active_shot_num: int
    round_num: int
    round_total: int
    next_shot: int
    motion: Optional[List[float]] = None
    waiting_final_position: bool = False
    issued_at_utc: str = ""


class ClientState:
    def __init__(self, sock: socket.socket, slot_name: str, show_msg: bool) -> None:
        self.sock = sock
        self.slot_name = slot_name
        self.show_msg = show_msg
        self.connect_name = ""
        self.player_is_init = True
        self.position: List[float] = [0.0] * 32
        self.shot_num = 0
        self.round_num = 0
        self.round_total = 0
        self.next_shot = 0
        self.pending: Optional[PendingShot] = None

    def send_msg(self, msg: str) -> None:
        if self.show_msg:
            print(f"[{self.slot_name}] >>>> {msg}", flush=True)
        self.sock.send(msg.strip().encode())

    def recv_msg(self) -> tuple[str, list[str]]:
        buffer = bytearray()
        while True:
            data = self.sock.recv(1)
            if not data or data == b"\0":
                break
            buffer.extend(data)
        msg_str = buffer.decode().strip()
        if self.show_msg:
            print(f"[{self.slot_name}] <<<< {msg_str}", flush=True)
        if not msg_str:
            return "", []
        parts = msg_str.split(" ")
        return parts[0], parts[1:]

    def apply_setstate(self, msg_list: Sequence[str]) -> None:
        self.shot_num = int(msg_list[0])
        self.round_num = int(msg_list[1])
        self.round_total = int(msg_list[2])
        self.next_shot = int(msg_list[3])

    def apply_position(self, msg_list: Sequence[str]) -> None:
        for idx in range(32):
            self.position[idx] = float(msg_list[idx])

    def own_reset_shot_num(self) -> int:
        return 0 if self.player_is_init else 1

    def final_xy(self, active_shot_num: int) -> tuple[float, float]:
        pair = active_shot_num // 2
        offset = pair * 4 + (0 if active_shot_num % 2 == 0 else 2)
        return float(self.position[offset]), float(self.position[offset + 1])


def linspace(start: float, stop: float, count: int) -> list[float]:
    if count <= 1:
        return [float(start)]
    step = (stop - start) / (count - 1)
    return [float(start + idx * step) for idx in range(count)]


def build_schedule(args: argparse.Namespace) -> list[ShotRequest]:
    rng = random.Random(args.seed)
    shots: list[ShotRequest] = []

    if args.random_samples > 0:
        for sample_id in range(args.random_samples):
            shots.append(
                ShotRequest(
                    sample_id=sample_id,
                    v0=rng.uniform(args.v_min, args.v_max),
                    h0=rng.uniform(args.h_min, args.h_max),
                    w0=rng.uniform(args.w_min, args.w_max),
                )
            )
        return shots

    grid_v = linspace(args.v_min, args.v_max, args.v_count)
    grid_h = linspace(args.h_min, args.h_max, args.h_count)
    grid_w = linspace(args.w_min, args.w_max, args.w_count)
    tuples = list(itertools.product(grid_v, grid_h, grid_w))
    if args.shuffle:
        rng.shuffle(tuples)

    sample_id = 0
    for _ in range(args.repeats):
        for v0, h0, w0 in tuples:
            shots.append(ShotRequest(sample_id=sample_id, v0=v0, h0=h0, w0=w0))
            sample_id += 1
    return shots


def connect_key_for_mode(key: str, use_reset: bool) -> str:
    if not use_reset:
        return key
    if key.endswith(":0"):
        return key
    if ":" in key.rsplit("_", 1)[-1]:
        raise ValueError("--use-reset needs debug mode; pass a plain key or a key ending in :0")
    return key + ":0"


class DualCalibrationCollector:
    def __init__(self, args: argparse.Namespace, schedule: Sequence[ShotRequest]) -> None:
        self.args = args
        self.schedule = list(schedule)
        self.schedule_index = 0
        self.samples_written = 0
        self.output_path = Path(args.output_file)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_fp = self.output_path.open("w", encoding="utf-8")
        self.clients: list[ClientState] = []
        connect_key = connect_key_for_mode(args.key, args.use_reset)

        for idx in range(2):
            sock = socket.socket()
            sock.connect((args.host, args.port))
            client = ClientState(sock=sock, slot_name=f"C{idx + 1}", show_msg=args.show_msg)
            client.send_msg("CONNECTKEY:" + connect_key)
            self.clients.append(client)

        suffix_note = " with :0 debug suffix" if connect_key != args.key else ""
        print(f"已建立2个socket连接 {args.host} {args.port}{suffix_note}", flush=True)

    def close(self) -> None:
        for client in self.clients:
            try:
                client.sock.close()
            except OSError:
                pass
        self.output_fp.close()
        print("已关闭socket连接", flush=True)

    def next_shot(self) -> Optional[ShotRequest]:
        if self.schedule_index >= len(self.schedule):
            return None
        shot = self.schedule[self.schedule_index]
        self.schedule_index += 1
        return shot

    def write_record(self, client: ClientState, pending: PendingShot) -> None:
        final_x, final_y = client.final_xy(pending.active_shot_num)
        motion = pending.motion or [None, None, None, None, None]
        record = SampleRecord(
            sample_id=pending.shot.sample_id,
            requested_v0=pending.shot.v0,
            requested_h0=pending.shot.h0,
            requested_w0=pending.shot.w0,
            connect_name=client.connect_name,
            player_is_init=client.player_is_init,
            active_shot_num=pending.active_shot_num,
            round_num=pending.round_num,
            round_total=pending.round_total,
            next_shot=pending.next_shot,
            used_reset=self.args.use_reset,
            motion_x=motion[0],
            motion_y=motion[1],
            motion_vx=motion[2],
            motion_vy=motion[3],
            motion_w=motion[4],
            final_x=final_x,
            final_y=final_y,
            in_play=(final_x > 0.0 or final_y > 0.0),
            issued_at_utc=pending.issued_at_utc,
            received_at_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        self.output_fp.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
        self.output_fp.flush()
        self.samples_written += 1
        if self.samples_written % self.args.progress_every == 0:
            print(
                f"[progress] collected {self.samples_written}/{len(self.schedule)} samples -> {self.output_path}",
                flush=True,
            )

    def arm_shot(self, client: ClientState) -> None:
        shot = self.next_shot()
        if shot is None:
            client.send_msg("BESTSHOT 3.0 0.0 0.0")
            return

        active_shot_num = client.shot_num
        if self.args.use_reset:
            active_shot_num = client.own_reset_shot_num()
            client.send_msg("RESETPOSITION " + EMPTY_POSITION_PAYLOAD)
            client.send_msg(
                f"RESETSTATE {active_shot_num} {client.round_num} {client.round_total} {client.next_shot}"
            )
            if self.args.reset_settle_seconds > 0:
                time.sleep(self.args.reset_settle_seconds)

        client.pending = PendingShot(
            shot=shot,
            active_shot_num=active_shot_num,
            round_num=client.round_num,
            round_total=client.round_total,
            next_shot=client.next_shot,
            issued_at_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        print(
            f"[sample {shot.sample_id}] {client.slot_name} BESTSHOT "
            f"{shot.v0:.3f} {shot.h0:.3f} {shot.w0:.3f}",
            flush=True,
        )
        client.send_msg(f"BESTSHOT {shot.v0} {shot.h0} {shot.w0}")

    def handle_message(self, client: ClientState, msg_code: str, msg_list: list[str]) -> None:
        if msg_code == "":
            return
        if msg_code == "CONNECTNAME":
            client.connect_name = msg_list[0]
            client.player_is_init = client.connect_name == "Player1"
            role = "玩家1，首局先手" if client.player_is_init else "玩家2，首局后手"
            print(f"[{client.slot_name}] {role}", flush=True)
            return
        if msg_code == "ISREADY":
            client.send_msg("READYOK")
            time.sleep(0.1)
            suffix = client.connect_name or client.slot_name
            client.send_msg(f"NAME {self.args.name}_{suffix}")
            print(f"[{client.slot_name}] 已准备", flush=True)
            return
        if msg_code == "NEWGAME":
            return
        if msg_code == "SETSTATE":
            client.apply_setstate(msg_list)
            return
        if msg_code == "POSITION":
            client.apply_position(msg_list)
            if client.pending and client.pending.waiting_final_position:
                self.write_record(client, client.pending)
                client.pending = None
            return
        if msg_code == "GO":
            self.arm_shot(client)
            return
        if msg_code == "MOTIONINFO":
            if client.pending:
                client.pending.motion = [float(value) for value in msg_list[:5]]
                client.pending.waiting_final_position = True
            return
        if msg_code == "CENTERLINE_VIOLATION":
            client.send_msg("CENTERLINE_CHOICE RESET")
            return
        if msg_code == "SCORE":
            print(f"[{client.slot_name}] SCORE {' '.join(msg_list)}", flush=True)
            return
        if msg_code == "TOTALSCORE":
            print(f"[{client.slot_name}] TOTALSCORE {' '.join(msg_list)}", flush=True)
            return
        if msg_code == "GAMEOVER":
            print(f"[{client.slot_name}] GAMEOVER {' '.join(msg_list)}", flush=True)
            return
        print(f"[{client.slot_name}] [warn] unhandled message: {msg_code} {msg_list}", flush=True)

    def run(self) -> None:
        try:
            while True:
                all_issued = self.schedule_index >= len(self.schedule)
                if all_issued and not any(c.pending for c in self.clients):
                    print("采样完成。", flush=True)
                    break
                ready, _, _ = select.select([c.sock for c in self.clients], [], [], 60.0)
                if not ready:
                    print("[warn] waiting for server timed out", flush=True)
                    continue
                by_sock = {client.sock: client for client in self.clients}
                for sock in ready:
                    client = by_sock[sock]
                    msg_code, msg_list = client.recv_msg()
                    self.handle_message(client, msg_code, msg_list)
        finally:
            self.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dual-player course-server calibration")
    parser.add_argument(
        "--key",
        required=True,
        help="plain key is fine; :0 is appended automatically when --use-reset is enabled",
    )
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("--name", default="DualCalib")
    parser.add_argument(
        "--output-file", default="data/calibration/local_no_sweep.jsonl"
    )
    parser.add_argument("--show-msg", action="store_true")
    parser.add_argument("--use-reset", action="store_true")
    parser.add_argument("--reset-settle-seconds", type=float, default=0.2)
    parser.add_argument("--random-samples", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260706)
    parser.add_argument("--v-min", type=float, default=2.75)
    parser.add_argument("--v-max", type=float, default=3.25)
    parser.add_argument("--v-count", type=int, default=5)
    parser.add_argument("--h-min", type=float, default=-0.45)
    parser.add_argument("--h-max", type=float, default=0.45)
    parser.add_argument("--h-count", type=int, default=5)
    parser.add_argument("--w-min", type=float, default=-1.5)
    parser.add_argument("--w-max", type=float, default=1.5)
    parser.add_argument("--w-count", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--shuffle", action="store_true")
    parser.add_argument("--progress-every", type=int, default=25)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    schedule = build_schedule(args)
    print(
        f"Prepared {len(schedule)} dual-player samples -> {args.output_file} | "
        f"reset={'on' if args.use_reset else 'off'} | "
        f"v=[{args.v_min},{args.v_max}] h=[{args.h_min},{args.h_max}] w=[{args.w_min},{args.w_max}]",
        flush=True,
    )
    collector = DualCalibrationCollector(args, schedule)
    collector.run()


if __name__ == "__main__":
    main()
