#!/usr/bin/env python3
"""A minimal local digital curling server for offline AI development.

This mock server follows the course protocol closely enough for the bundled
AIRobot.py client to connect and play a simplified match while the official
platform is unavailable.
"""

from __future__ import annotations

import argparse
import math
import random
import socket
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple


HOUSE_X = 2.375
HOUSE_Y = 4.88
HOUSE_R = 1.830
STONE_R = 0.145
SHEET_WIDTH = 4.75
SHEET_LENGTH = 44.5
TEE_LINE_Y = 5.0
START_Y = 32.0


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x1 - x2, y1 - y2)


@dataclass
class Stone:
    x: float = 0.0
    y: float = 0.0
    in_play: bool = False

    def as_pair(self) -> Tuple[float, float]:
        if not self.in_play:
            return (0.0, 0.0)
        return (self.x, self.y)


class LocalCurlingServer:
    def __init__(
        self,
        host: str,
        port: int,
        key: str,
        rounds: int,
        seed: Optional[int],
        connect_name: str,
        show_messages: bool,
    ) -> None:
        self.host = host
        self.port = port
        self.key = key
        self.rounds = rounds
        self.random = random.Random(seed)
        if connect_name not in {"Player1", "Player2"}:
            raise ValueError("connect_name must be Player1 or Player2")
        self.connect_name = connect_name
        self.client_is_blue = connect_name == "Player1"
        self.show_messages = show_messages
        self.blue_total = 0
        self.red_total = 0
        self.stones: List[Stone] = [Stone() for _ in range(16)]
        self.client_name = "PlayerAI"
        self.server_socket: Optional[socket.socket] = None
        self.client_socket: Optional[socket.socket] = None
        self.debug_mode = "0"

    def log(self, text: str) -> None:
        print(text, flush=True)

    def send_msg(self, msg: str) -> None:
        if self.client_socket is None:
            raise RuntimeError("No client connected")
        if self.show_messages:
            self.log(f"<<<< {msg}")
        self.client_socket.sendall(msg.encode() + b"\0")

    def recv_msg(self, timeout: float = 120.0) -> Tuple[str, List[str]]:
        if self.client_socket is None:
            raise RuntimeError("No client connected")
        sock = self.client_socket
        sock.settimeout(timeout)
        buffer = bytearray()
        try:
            while True:
                try:
                    chunk = sock.recv(1)
                except socket.timeout:
                    if buffer:
                        break
                    raise
                if not chunk:
                    break
                if chunk == b"\0":
                    break
                buffer.extend(chunk)
                # The course client sends messages without a trailing NUL.
                # Once bytes stop arriving briefly, treat the current payload as
                # one message to keep interoperability simple.
                sock.settimeout(0.03)
        finally:
            sock.settimeout(None)
        msg = buffer.decode(errors="ignore").strip()
        if self.show_messages:
            self.log(f"  >>>> {msg}")
        if not msg:
            return "", []
        parts = msg.split()
        return parts[0], parts[1:]

    def recv_optional_msg(self, timeout: float = 0.05) -> Tuple[str, List[str]]:
        try:
            return self.recv_msg(timeout=timeout)
        except socket.timeout:
            return "", []

    def position_payload(self) -> str:
        values: List[str] = []
        for shot_idx in range(8):
            blue = self.stones[shot_idx * 2].as_pair()
            red = self.stones[shot_idx * 2 + 1].as_pair()
            values.extend(f"{v:.3f}" for v in (blue[0], blue[1], red[0], red[1]))
        return "POSITION " + " ".join(values)

    def setstate_payload(self, shot_num: int, round_num: int, next_team: int) -> str:
        return f"SETSTATE {shot_num} {round_num} {self.rounds} {next_team}"

    def is_client_turn(self, shot_num: int) -> bool:
        return (shot_num % 2 == 0) == self.client_is_blue

    def score_for_client(self, blue_score: int) -> int:
        return blue_score if self.client_is_blue else -blue_score

    def reset_stones(self) -> None:
        self.stones = [Stone() for _ in range(16)]

    def apply_position_payload(self, args: List[str]) -> None:
        if len(args) != 32:
            raise RuntimeError(f"RESETPOSITION expects 32 values, got {len(args)}")
        stones: List[Stone] = []
        for shot_idx in range(8):
            blue_x = float(args[shot_idx * 4])
            blue_y = float(args[shot_idx * 4 + 1])
            red_x = float(args[shot_idx * 4 + 2])
            red_y = float(args[shot_idx * 4 + 3])
            stones.append(Stone(blue_x, blue_y, bool(blue_x or blue_y)))
            stones.append(Stone(red_x, red_y, bool(red_x or red_y)))
        self.stones = stones

    def landing_point(self, v0: float, h0: float, w0: float) -> Tuple[float, float]:
        speed_term = clamp(v0, 0.0, 6.0)
        x = HOUSE_X + h0 * 0.88 + math.tanh(w0 / 5.0) * 0.55
        y = 8.0 - speed_term * 1.02 + abs(w0) * 0.05

        # Small randomness, matching the course note that friction varies.
        x += self.random.gauss(0.0, 0.035)
        y += self.random.gauss(0.0, 0.05)

        return (
            clamp(x, STONE_R, SHEET_WIDTH - STONE_R),
            clamp(y, STONE_R, START_Y),
        )

    def simulate_motioninfo(
        self, v0: float, h0: float, w0: float, final_x: float, final_y: float
    ) -> Tuple[float, float, float, float, float]:
        mid_y = (START_Y + final_y) / 2.0
        mid_x = HOUSE_X + h0 * 0.55 + math.tanh(w0 / 5.0) * 0.25
        vx = (final_x - mid_x) * 0.8
        vy = -max(0.2, v0 * 0.55)
        return (mid_x, mid_y, vx, vy, w0)

    def apply_simple_collision(self, stone_index: int, x: float, y: float) -> Tuple[float, float]:
        nearest_idx = None
        nearest_dist = float("inf")
        for idx, stone in enumerate(self.stones):
            if idx == stone_index or not stone.in_play:
                continue
            d = distance(x, y, stone.x, stone.y)
            if d < nearest_dist:
                nearest_dist = d
                nearest_idx = idx

        if nearest_idx is None or nearest_dist > STONE_R * 2.2:
            return x, y

        target = self.stones[nearest_idx]
        dx = target.x - x
        dy = target.y - y
        mag = math.hypot(dx, dy) or 1.0
        ux, uy = dx / mag, dy / mag

        # Move the struck stone away and keep the thrown stone near contact.
        target.x = clamp(target.x + ux * 0.55, STONE_R, SHEET_WIDTH - STONE_R)
        target.y = clamp(target.y + uy * 0.75, STONE_R, START_Y)
        return (
            clamp(target.x - ux * (STONE_R * 2.05), STONE_R, SHEET_WIDTH - STONE_R),
            clamp(target.y - uy * (STONE_R * 2.05), STONE_R, START_Y),
        )

    def place_stone(
        self,
        stone_index: int,
        v0: float,
        h0: float,
        w0: float,
        landing: Optional[Tuple[float, float]] = None,
    ) -> None:
        x, y = landing if landing is not None else self.landing_point(v0, h0, w0)
        x, y = self.apply_simple_collision(stone_index, x, y)
        in_play = y < SHEET_LENGTH and 0.0 < x < SHEET_WIDTH
        self.stones[stone_index] = Stone(x=x, y=y, in_play=in_play)

    def choose_opponent_shot(self) -> Tuple[float, float, float]:
        # A simple opponent: usually draw toward the house, sometimes overshoot.
        v0 = self.random.uniform(2.7, 3.5)
        h0 = self.random.uniform(-0.9, 0.9)
        w0 = self.random.uniform(-2.2, 2.2)
        if self.random.random() < 0.18:
            v0 += 1.1
        return (v0, h0, w0)

    def end_score(self) -> int:
        in_house: List[Tuple[float, bool]] = []
        for idx, stone in enumerate(self.stones):
            if not stone.in_play:
                continue
            d = distance(stone.x, stone.y, HOUSE_X, HOUSE_Y)
            if d <= HOUSE_R + STONE_R:
                in_house.append((d, idx % 2 == 0))
        if not in_house:
            return 0

        in_house.sort(key=lambda item: item[0])
        winning_is_blue = in_house[0][1]
        losing_best = min(
            [d for d, is_blue in in_house if is_blue != winning_is_blue],
            default=float("inf"),
        )
        score = sum(
            1 for d, is_blue in in_house if is_blue == winning_is_blue and d < losing_best
        )
        return score if winning_is_blue else -score

    def handle_handshake(self) -> None:
        code, args = self.recv_msg()
        key_value = None
        if code == "CONNECTKEY" and args:
            key_value = args[0]
        elif code.startswith("CONNECTKEY:"):
            key_value = code.split(":", 1)[1]
        if key_value is None:
            raise RuntimeError(f"Unexpected connect key message: {code} {args}")

        # Course examples sometimes append :0 or :1 to enable debug/challenge
        # modes. Treat that suffix as mode metadata while validating the base
        # key, and also allow an exact key match for simpler local scripts.
        key_base, _, mode = key_value.rpartition(":")
        if key_value == self.key:
            self.debug_mode = "0"
        elif key_base == self.key:
            self.debug_mode = mode or "0"
        else:
            raise RuntimeError(f"Unexpected connect key message: {code} {args}")

        self.send_msg(f"CONNECTNAME {self.connect_name}")

        self.send_msg("ISREADY")
        ready = False
        named = False
        while not (ready and named):
            code, args = self.recv_msg()
            if code == "READYOK":
                ready = True
            elif code == "EXPMODE" and args:
                self.debug_mode = args[0]
            elif code == "NAME" and args:
                named = True
                self.client_name = args[0]
            else:
                raise RuntimeError(f"Unexpected handshake message: {code} {args}")

    def receive_bestshot(self, shot_num: int) -> Tuple[int, float, float, float]:
        active_shot_num = shot_num
        while True:
            code, args = self.recv_msg()
            if code == "RESETPOSITION":
                self.apply_position_payload(args)
                self.send_msg(self.position_payload())
            elif code == "RESETSTATE":
                if args:
                    active_shot_num = int(args[0])
                    active_shot_num = max(0, min(15, active_shot_num))
                    self.send_msg(self.setstate_payload(active_shot_num, 0, active_shot_num % 2))
            elif code == "BESTSHOT" and len(args) == 3:
                v0, h0, w0 = map(float, args)
                return active_shot_num, v0, h0, w0
            else:
                raise RuntimeError(f"Expected BESTSHOT, got {code} {args}")

    def run_round(self, round_num: int) -> None:
        self.reset_stones()
        self.send_msg("NEWGAME")

        for shot_num in range(16):
            next_team = shot_num % 2
            self.send_msg(self.setstate_payload(shot_num, round_num, next_team))
            self.send_msg(self.position_payload())

            if self.is_client_turn(shot_num):
                self.send_msg("GO")
                active_shot_num, v0, h0, w0 = self.receive_bestshot(shot_num)
                final_x, final_y = self.landing_point(v0, h0, w0)
                motion = self.simulate_motioninfo(v0, h0, w0, final_x, final_y)
                self.send_msg(
                    "MOTIONINFO " + " ".join(f"{value:.3f}" for value in motion)
                )
                code, args = self.recv_optional_msg()
                if code == "SWEEP" and args:
                    sweep_distance = clamp(float(args[0]), 0.0, 12.0)
                    final_y = clamp(final_y - sweep_distance * 0.045, STONE_R, START_Y)
                elif code:
                    raise RuntimeError(f"Unexpected post-motion message: {code} {args}")
                self.place_stone(active_shot_num, v0, h0, w0, landing=(final_x, final_y))
            else:
                v0, h0, w0 = self.choose_opponent_shot()
                self.place_stone(shot_num, v0, h0, w0)

            self.send_msg(self.position_payload())

        score = self.end_score()
        if score > 0:
            self.blue_total += score
        elif score < 0:
            self.red_total += abs(score)
        self.send_msg(f"SCORE {self.score_for_client(score)}")

    def game_result(self) -> str:
        client_total = self.blue_total if self.client_is_blue else self.red_total
        opponent_total = self.red_total if self.client_is_blue else self.blue_total
        if client_total > opponent_total:
            return "WIN"
        if client_total < opponent_total:
            return "LOSE"
        return "DRAW"

    def serve(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.log(f"Local curling server listening on {self.host}:{self.port}")
        self.log(f"ConnectKey: {self.key}")
        conn, addr = self.server_socket.accept()
        self.client_socket = conn
        self.log(f"Client connected from {addr[0]}:{addr[1]}")
        try:
            self.handle_handshake()
            for round_num in range(self.rounds):
                self.run_round(round_num)
            self.send_msg(f"TOTALSCORE {self.blue_total} {self.red_total}")
            self.send_msg(f"GAMEOVER {self.game_result()}")
            # Help the client exit its receive loop gracefully.
            for _ in range(5):
                try:
                    conn.sendall(b"\0")
                except OSError:
                    break
                time.sleep(0.02)
        finally:
            conn.close()
            self.server_socket.close()
            self.log("Server stopped")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local mock curling server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7788)
    parser.add_argument("--key", default="local-test:0")
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--connect-name", choices=["Player1", "Player2"], default="Player1")
    parser.add_argument("--show-messages", action="store_true")
    args = parser.parse_args()

    server = LocalCurlingServer(
        host=args.host,
        port=args.port,
        key=args.key,
        rounds=args.rounds,
        seed=args.seed,
        connect_name=args.connect_name,
        show_messages=args.show_messages,
    )
    server.serve()


if __name__ == "__main__":
    main()
