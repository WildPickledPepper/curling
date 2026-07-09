#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect controlled Unity samples with resettable scenes.

This sampler keeps both players connected, but before every planned throw it
uses the course-server debug reset messages to place the sheet in a known
state.  That lets us collect clean single-stone, sweep-window, boundary, and
collision samples without waiting for a natural 16-shot end.
"""

from __future__ import annotations

import argparse
import json
import select
import socket
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence


EMPTY_POSITION = [0.0] * 32


@dataclass(frozen=True)
class StonePlacement:
    x: float
    y: float
    index: int | None = None


@dataclass(frozen=True)
class ControlledShot:
    sample_id: int
    label: str
    category: str
    v0: float
    h0: float
    w0: float
    sweep: float = 0.0
    stones: list[StonePlacement] = field(default_factory=list)
    active_index: int | None = None
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PendingShot:
    shot: ControlledShot
    active_shot_num: int
    reset_position: list[float]
    target_indices: list[int]
    server_position_before_reset: list[float]
    round_num: int
    round_total: int
    next_shot: int
    motioninfo: list[float] | None = None
    waiting_final_position: bool = False
    sent_sweep: bool = False
    issued_at_utc: str = ""
    issued_monotonic: float = 0.0
    sweep_sent_at_utc: str | None = None
    final_source: str = "position"


class ClientState:
    def __init__(self, sock: socket.socket, slot_name: str, show_msg: bool) -> None:
        self.sock = sock
        self.slot_name = slot_name
        self.show_msg = show_msg
        self.connect_name = ""
        self.player_is_init = True
        self.position = [0.0] * 32
        self.shot_num = 0
        self.round_num = 0
        self.round_total = 0
        self.next_shot = 0
        self.pending: PendingShot | None = None

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
        msg_str = buffer.decode(errors="replace").strip()
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
        if len(msg_list) < 32:
            raise ValueError(f"POSITION expects 32 values, got {len(msg_list)}")
        self.position = [float(value) for value in msg_list[:32]]

    def own_reset_shot_num(self) -> int:
        return 0 if self.player_is_init else 1


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def stone_offset(stone_index: int) -> int:
    if stone_index < 0 or stone_index >= 16:
        raise ValueError(f"stone index must be in [0, 15], got {stone_index}")
    pair = stone_index // 2
    return pair * 4 + (0 if stone_index % 2 == 0 else 2)


def stone_xy(position: Sequence[float], stone_index: int) -> list[float]:
    offset = stone_offset(stone_index)
    return [float(position[offset]), float(position[offset + 1])]


def set_stone_xy(position: list[float], stone_index: int, x: float, y: float) -> None:
    offset = stone_offset(stone_index)
    position[offset] = float(x)
    position[offset + 1] = float(y)


def connect_key_for_reset(key: str, use_reset: bool) -> str:
    if not use_reset or key.endswith(":0"):
        return key
    return key + ":0"


def format_payload(values: Sequence[float]) -> str:
    if len(values) != 32:
        raise ValueError(f"RESETPOSITION expects 32 values, got {len(values)}")
    return " ".join(f"{value:.8g}" for value in values)


def parse_plan_file(path: Path) -> list[ControlledShot]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("plan file must contain a JSON list")
    shots: list[ControlledShot] = []
    known_keys = {
        "sample_id",
        "label",
        "category",
        "v0",
        "h0",
        "w0",
        "sweep",
        "stones",
        "active_index",
        "notes",
    }
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"plan entry {idx} must be an object")
        stones = [
            StonePlacement(
                x=float(stone["x"]),
                y=float(stone["y"]),
                index=None if stone.get("index") is None else int(stone["index"]),
            )
            for stone in item.get("stones", [])
        ]
        shots.append(
            ControlledShot(
                sample_id=int(item.get("sample_id", idx)),
                label=str(item.get("label", f"sample_{idx:03d}")),
                category=str(item.get("category", "uncategorized")),
                v0=float(item["v0"]),
                h0=float(item["h0"]),
                w0=float(item["w0"]),
                sweep=float(item.get("sweep", 0.0)),
                stones=stones,
                active_index=None if item.get("active_index") is None else int(item["active_index"]),
                notes=str(item.get("notes", "")),
                metadata={key: value for key, value in item.items() if key not in known_keys},
            )
        )
    if not shots:
        raise ValueError("plan file is empty")
    return shots


def reset_position_for_shot(shot: ControlledShot, active_shot_num: int) -> tuple[list[float], list[int]]:
    position = list(EMPTY_POSITION)
    target_indices: list[int] = []
    for offset, stone in enumerate(shot.stones):
        target_index = stone.index
        if target_index is None:
            target_index = active_shot_num + 2 + offset * 2
        if target_index == active_shot_num:
            raise ValueError(f"{shot.label}: target stone index conflicts with active stone {active_shot_num}")
        set_stone_xy(position, target_index, stone.x, stone.y)
        target_indices.append(target_index)
    return position, target_indices


def resolve_active_shot_num(
    shot: ControlledShot,
    default_active_shot_num: int,
    *,
    player_is_init: bool,
    connect_name: str,
    use_reset: bool,
    use_plan_active_index: bool,
) -> int:
    if not use_plan_active_index or shot.active_index is None:
        return default_active_shot_num
    if not use_reset:
        raise ValueError("--use-plan-active-index requires --use-reset")
    expected_parity = 0 if player_is_init else 1
    if shot.active_index % 2 != expected_parity:
        raise ValueError(
            f"{shot.label}: active_index {shot.active_index} does not match "
            f"{connect_name or 'client'} parity {expected_parity}"
        )
    return shot.active_index


def stone_moves(before: Sequence[float], after: Sequence[float]) -> list[dict[str, float | int]]:
    moves: list[dict[str, float | int]] = []
    for stone_index in range(16):
        bx, by = stone_xy(before, stone_index)
        ax, ay = stone_xy(after, stone_index)
        dx = ax - bx
        dy = ay - by
        distance = (dx * dx + dy * dy) ** 0.5
        moves.append(
            {
                "index": stone_index,
                "before_x": bx,
                "before_y": by,
                "after_x": ax,
                "after_y": ay,
                "dx": dx,
                "dy": dy,
                "distance": distance,
            }
        )
    return moves


class ControlledSceneSampler:
    def __init__(self, args: argparse.Namespace, schedule: Sequence[ControlledShot]) -> None:
        self.args = args
        self.schedule = list(schedule)
        self.schedule_index = 0
        self.samples_written = 0
        self.output_path = Path(args.output_file)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_fp = self.output_path.open("w", encoding="utf-8")
        self.clients: list[ClientState] = []

        key = connect_key_for_reset(args.key, args.use_reset)
        for idx in range(2):
            sock = socket.socket()
            sock.connect((args.host, args.port))
            client = ClientState(sock=sock, slot_name=f"C{idx + 1}", show_msg=args.show_msg)
            client.send_msg("CONNECTKEY:" + key)
            self.clients.append(client)
        suffix_note = " with :0 debug suffix" if key != args.key else ""
        print(f"已建立2个socket连接 {args.host} {args.port}{suffix_note}", flush=True)

    def close(self) -> None:
        for client in self.clients:
            try:
                client.sock.close()
            except OSError:
                pass
        self.output_fp.close()
        print("已关闭socket连接", flush=True)

    def next_shot(self) -> ControlledShot | None:
        if self.schedule_index >= len(self.schedule):
            return None
        shot = self.schedule[self.schedule_index]
        self.schedule_index += 1
        return shot

    def arm_shot(self, client: ClientState) -> None:
        if client.pending is not None:
            client.pending.final_source = "next_go_flush"
            print(
                f"[warn] {client.slot_name} flushing stale pending sample "
                f"{client.pending.shot.label} before arming next GO",
                flush=True,
            )
            self.write_record(client, client.pending)
            client.pending = None

        shot = self.next_shot()
        if shot is None:
            print(f"[{client.slot_name}] no more planned shots; leaving GO unanswered", flush=True)
            return

        active_shot_num = resolve_active_shot_num(
            shot,
            client.own_reset_shot_num() if self.args.use_reset else client.shot_num,
            player_is_init=client.player_is_init,
            connect_name=client.connect_name or client.slot_name,
            use_reset=self.args.use_reset,
            use_plan_active_index=self.args.use_plan_active_index,
        )
        reset_position, target_indices = reset_position_for_shot(shot, active_shot_num)
        before_reset = list(client.position)

        if self.args.use_reset:
            client.send_msg("RESETPOSITION " + format_payload(reset_position))
            client.send_msg(
                f"RESETSTATE {active_shot_num} {client.round_num} {client.round_total} {client.next_shot}"
            )
            if self.args.reset_settle_seconds > 0:
                time.sleep(self.args.reset_settle_seconds)
            client.position = list(reset_position)
        else:
            reset_position = list(client.position)

        client.pending = PendingShot(
            shot=shot,
            active_shot_num=active_shot_num,
            reset_position=reset_position,
            target_indices=target_indices,
            server_position_before_reset=before_reset,
            round_num=client.round_num,
            round_total=client.round_total,
            next_shot=client.next_shot,
            issued_at_utc=utc_now(),
            issued_monotonic=time.monotonic(),
        )
        print(
            f"[sample {shot.sample_id:03d}] {client.slot_name} {shot.category} {shot.label}: "
            f"BESTSHOT {shot.v0:.4g} {shot.h0:.4g} {shot.w0:.4g} sweep={shot.sweep:g} "
            f"targets={target_indices}",
            flush=True,
        )
        client.send_msg(f"BESTSHOT {shot.v0} {shot.h0} {shot.w0}")

    def write_record(self, client: ClientState, pending: PendingShot) -> None:
        moves = stone_moves(pending.reset_position, client.position)
        active_move = moves[pending.active_shot_num]
        non_active_moves = [move for move in moves if int(move["index"]) != pending.active_shot_num]
        target_moves = [moves[index] for index in pending.target_indices]
        max_non_active_move = max((float(move["distance"]) for move in non_active_moves), default=0.0)
        max_target_move = max((float(move["distance"]) for move in target_moves), default=0.0)
        shot = pending.shot
        record = {
            "sample_id": shot.sample_id,
            "label": shot.label,
            "category": shot.category,
            "notes": shot.notes,
            "plan_metadata": shot.metadata,
            "connect_name": client.connect_name,
            "player_is_init": client.player_is_init,
            "active_shot_num": pending.active_shot_num,
            "round_num": pending.round_num,
            "round_total": pending.round_total,
            "next_shot": pending.next_shot,
            "requested": {
                "v0": shot.v0,
                "h0": shot.h0,
                "w0": shot.w0,
                "sweep": shot.sweep,
                "active_index": shot.active_index,
                "stones": [asdict(stone) for stone in shot.stones],
            },
            "use_reset": self.args.use_reset,
            "target_indices": pending.target_indices,
            "reset_position": pending.reset_position,
            "server_position_before_reset": pending.server_position_before_reset,
            "after_position": list(client.position),
            "motioninfo": pending.motioninfo,
            "final_source": pending.final_source,
            "sent_sweep": pending.sent_sweep,
            "sweep_sent_at_utc": pending.sweep_sent_at_utc,
            "final_xy": stone_xy(client.position, pending.active_shot_num),
            "active_move": active_move,
            "target_moves": target_moves,
            "all_moves": moves,
            "max_non_active_move": max_non_active_move,
            "max_target_move": max_target_move,
            "collision_observed": max_non_active_move > self.args.collision_tolerance,
            "issued_at_utc": pending.issued_at_utc,
            "received_at_utc": utc_now(),
        }
        self.output_fp.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        self.output_fp.flush()
        self.samples_written += 1
        print(
            f"[record] {self.samples_written}/{len(self.schedule)} {shot.label} "
            f"final=({record['final_xy'][0]:.4f},{record['final_xy'][1]:.4f}) "
            f"max_target_move={max_target_move:.4f} collision={record['collision_observed']}",
            flush=True,
        )

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
        if msg_code == "SETSTATE":
            client.apply_setstate(msg_list)
            return
        if msg_code == "POSITION":
            client.apply_position(msg_list)
            if client.pending and (
                client.pending.waiting_final_position
                or time.monotonic() - client.pending.issued_monotonic >= self.args.min_final_position_seconds
            ):
                client.pending.final_source = "position"
                self.write_record(client, client.pending)
                client.pending = None
            return
        if msg_code == "GO":
            self.arm_shot(client)
            return
        if msg_code == "MOTIONINFO":
            if client.pending:
                client.pending.motioninfo = [float(value) for value in msg_list[:5]]
                client.pending.waiting_final_position = True
                if client.pending.shot.sweep > 0:
                    client.send_msg("SWEEP " + str(client.pending.shot.sweep))
                    client.pending.sent_sweep = True
                    client.pending.sweep_sent_at_utc = utc_now()
            return
        if msg_code == "CENTERLINE_VIOLATION":
            client.send_msg("CENTERLINE_CHOICE RESET")
            return
        if msg_code in {"NEWGAME", "SCORE", "TOTALSCORE", "GAMEOVER"}:
            print(f"[{client.slot_name}] {msg_code} {' '.join(msg_list)}", flush=True)
            return
        print(f"[{client.slot_name}] [warn] unhandled message: {msg_code} {msg_list}", flush=True)

    def run(self) -> None:
        try:
            while True:
                now = time.monotonic()
                for client in self.clients:
                    if (
                        client.pending is not None
                        and now - client.pending.issued_monotonic >= self.args.force_final_timeout_seconds
                    ):
                        client.pending.final_source = "timeout_flush"
                        print(
                            f"[warn] {client.slot_name} timeout flush sample {client.pending.shot.label}",
                            flush=True,
                        )
                        self.write_record(client, client.pending)
                        client.pending = None

                all_issued = self.schedule_index >= len(self.schedule)
                if all_issued and not any(client.pending for client in self.clients):
                    print("采样完成。", flush=True)
                    break
                ready, _, _ = select.select([client.sock for client in self.clients], [], [], self.args.timeout_seconds)
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", default="localtest")
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=7788)
    parser.add_argument("--name", default="ControlledSampler")
    parser.add_argument("--plan-file", type=Path, required=True)
    parser.add_argument("--output-file", default="data/calibration/unity_controlled_samples_20260707.jsonl")
    parser.add_argument("--use-reset", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--use-plan-active-index",
        action="store_true",
        help="when a plan row has active_index, pass it through RESETSTATE instead of forcing 0/1",
    )
    parser.add_argument("--reset-settle-seconds", type=float, default=0.2)
    parser.add_argument("--collision-tolerance", type=float, default=0.02)
    parser.add_argument(
        "--min-final-position-seconds",
        type=float,
        default=2.0,
        help="accept POSITION as final without MOTIONINFO only after this many seconds",
    )
    parser.add_argument(
        "--force-final-timeout-seconds",
        type=float,
        default=20.0,
        help="force-write a pending sample if Unity never sends a final POSITION",
    )
    parser.add_argument("--timeout-seconds", type=float, default=90.0)
    parser.add_argument("--show-msg", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    schedule = parse_plan_file(args.plan_file)
    categories = sorted({shot.category for shot in schedule})
    print(
        f"Prepared {len(schedule)} controlled samples -> {args.output_file} | "
        f"categories={','.join(categories)} | reset={'on' if args.use_reset else 'off'}",
        flush=True,
    )
    sampler = ControlledSceneSampler(args, schedule)
    sampler.run()


if __name__ == "__main__":
    main()
