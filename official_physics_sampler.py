# -*- coding: utf-8 -*-
"""Collect official-server shot samples for physics calibration.

Run two instances with the same connect key so the curling server assigns them
as Player1 and Player2. Each instance follows the same global shot schedule
based on ``shot_num`` and ``round_num``; together they cover all 16 throws in an
end while logging before/after positions.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from AIRobot import AIRobot


@dataclass
class PlannedShot:
    v0: float
    h0: float
    w0: float
    sweep: float
    label: str


def stone_offset(stone_index: int) -> int:
    pair = stone_index // 2
    return pair * 4 + (0 if stone_index % 2 == 0 else 2)


def stone_xy(position: List[float], stone_index: int) -> List[float]:
    offset = stone_offset(stone_index)
    return [float(position[offset]), float(position[offset + 1])]


def default_grid_shot(round_num: int, shot_num: int) -> PlannedShot:
    """Return a no-collision-oriented grid sample.

    Within one end, the 16 stones are spread over a 4x4 grid. Across ends, the
    whole grid is repeated with different rotation/sweep settings.
    """

    v_rows = [2.55, 2.95, 3.35, 3.75]
    h_cols = [-1.70, -0.55, 0.55, 1.70]
    round_settings = [
        (0.00, 0.00, "straight_no_sweep"),
        (0.00, 1.50, "straight_sweep_1p5"),
        (0.00, 3.00, "straight_sweep_3p0"),
        (0.00, 5.00, "straight_sweep_5p0"),
        (-1.57, 0.00, "curl_neg_1p57"),
        (1.57, 0.00, "curl_pos_1p57"),
        (-3.14, 0.00, "curl_neg_3p14"),
        (3.14, 0.00, "curl_pos_3p14"),
        (-1.57, 2.00, "curl_neg_1p57_sweep_2p0"),
        (1.57, 2.00, "curl_pos_1p57_sweep_2p0"),
        (-3.14, 2.00, "curl_neg_3p14_sweep_2p0"),
        (3.14, 2.00, "curl_pos_3p14_sweep_2p0"),
    ]
    row = shot_num // 4
    col = shot_num % 4
    w0, sweep, setting_label = round_settings[round_num % len(round_settings)]
    return PlannedShot(
        v0=v_rows[row],
        h0=h_cols[col],
        w0=w0,
        sweep=sweep,
        label=f"{setting_label}_r{row}_c{col}",
    )


def parse_plan_file(path: Path) -> List[PlannedShot]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("plan file must contain a JSON list")
    shots: List[PlannedShot] = []
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"plan entry {idx} must be an object")
        shots.append(
            PlannedShot(
                v0=float(item["v0"]),
                h0=float(item["h0"]),
                w0=float(item["w0"]),
                sweep=float(item.get("sweep", 0.0)),
                label=str(item.get("label", f"plan_{idx}")),
            )
        )
    if not shots:
        raise ValueError("plan file is empty")
    return shots


def max_existing_stone_move(before: List[float], after: List[float], shot_num: int) -> float:
    max_move = 0.0
    for idx in range(shot_num):
        bx, by = stone_xy(before, idx)
        ax, ay = stone_xy(after, idx)
        move = ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
        max_move = max(max_move, move)
    return max_move


class OfficialPhysicsSampler(AIRobot):
    def __init__(
        self,
        key: str,
        name: str,
        host: str,
        port: int,
        output: str,
        max_samples: int,
        plan: Optional[List[PlannedShot]],
        collision_tolerance: float,
        show_msg: bool,
    ) -> None:
        super().__init__(key, name, host, port, show_msg=show_msg)
        self.output_template = output
        self.output_path: Optional[Path] = None
        self.max_samples = max_samples
        self.plan = plan
        self.collision_tolerance = collision_tolerance
        self.samples_written = 0
        self.connect_name = "Unknown"
        self.pending: Optional[Dict[str, object]] = None

    def resolve_output_path(self) -> Path:
        if self.output_path is None:
            path_text = self.output_template.format(
                player=self.connect_name,
                name=self.name,
                date=time.strftime("%Y%m%d"),
            )
            self.output_path = Path(path_text)
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
        return self.output_path

    def planned_shot(self) -> PlannedShot:
        if self.plan:
            sample_index = self.round_num * 16 + self.shot_num
            return self.plan[sample_index % len(self.plan)]
        return default_grid_shot(self.round_num, self.shot_num)

    def append_sample(self, sample: Dict[str, object]) -> None:
        path = self.resolve_output_path()
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(sample, ensure_ascii=False, sort_keys=True) + "\n")
        self.samples_written += 1
        collision_text = "free" if sample["collision_free"] else "collision"
        final_xy = sample["final_xy"]
        print(
            f"sample {self.samples_written}: {self.connect_name} "
            f"round={sample['round_num']} shot={sample['shot_num']} "
            f"{collision_text} final=({final_xy[0]:.4f},{final_xy[1]:.4f}) "
            f"label={sample['shot']['label']}",
            flush=True,
        )
        if self.max_samples > 0 and self.samples_written >= self.max_samples:
            self.on_line = False

    def record_after_position(self, after_position: List[float]) -> None:
        if self.pending is None:
            return
        before_position = self.pending["before_position"]
        shot_num = int(self.pending["shot_num"])
        final_xy = stone_xy(after_position, shot_num)
        max_move = max_existing_stone_move(before_position, after_position, shot_num)
        sample = {
            **self.pending,
            "after_position": list(after_position),
            "final_xy": final_xy,
            "existing_stone_max_move": max_move,
            "collision_free": max_move <= self.collision_tolerance,
            "recorded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.pending = None
        self.append_sample(sample)

    def recv_forever(self) -> None:
        ret_null_time = 0
        self.on_line = True
        time0 = time.time()

        while self.on_line:
            msg_code, msg_list = self.recv_msg()
            if msg_code == "":
                ret_null_time += 1
            if ret_null_time == 5:
                break

            if msg_code == "CONNECTNAME":
                self.connect_name = msg_list[0]
                self.player_is_init = self.connect_name == "Player1"
                side = "首局先手" if self.player_is_init else "首局后手"
                print(f"{self.connect_name}，{side}", flush=True)
                self.resolve_output_path()

            elif msg_code == "ISREADY":
                self.send_msg("READYOK")
                time.sleep(0.5)
                self.send_msg("NAME " + self.name)
                print(self.name + " 准备采样！", flush=True)

            elif msg_code == "NEWGAME":
                time0 = time.time()

            elif msg_code == "SETSTATE":
                self.recv_setstate(msg_list)

            elif msg_code == "POSITION":
                for n in range(32):
                    self.position[n] = float(msg_list[n])
                self.record_after_position(list(self.position))

            elif msg_code == "GO":
                shot = self.planned_shot()
                self.pending = {
                    "player": self.connect_name,
                    "name": self.name,
                    "round_num": self.round_num,
                    "round_total": getattr(self, "round_total", None),
                    "shot_num": self.shot_num,
                    "next_shot": getattr(self, "next_shot", None),
                    "player_is_init": self.player_is_init,
                    "before_position": list(self.position),
                    "shot": asdict(shot),
                    "motioninfo": None,
                }
                print(
                    f"planned {self.connect_name} round={self.round_num} "
                    f"shot={self.shot_num}: {shot}",
                    flush=True,
                )
                self.send_msg(f"BESTSHOT {shot.v0} {shot.h0} {shot.w0}")

            elif msg_code == "MOTIONINFO":
                for n in range(5):
                    self.motioninfo[n] = float(msg_list[n])
                if self.pending is not None:
                    self.pending["motioninfo"] = list(self.motioninfo)
                shot = PlannedShot(**self.pending["shot"]) if self.pending else None
                if shot is not None and shot.sweep > 0:
                    self.send_msg("SWEEP " + str(shot.sweep))

            elif msg_code == "CENTERLINE_VIOLATION":
                self.send_msg("CENTERLINE_CHOICE RESET")

            elif msg_code == "SCORE":
                elapsed = time.time() - time0
                score = int(msg_list[0])
                print(
                    f"{time.strftime('[%Y/%m/%d %H:%M:%S]')} "
                    f"{self.name}第{self.round_num + 1}局耗时{elapsed:.1f}秒 "
                    f"SCORE {score}",
                    flush=True,
                )
                time0 = time.time()

            elif msg_code == "GAMEOVER":
                print("GAMEOVER " + " ".join(msg_list), flush=True)
                break

        self.ai_sock.close()
        print("已关闭socket连接", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect official curling physics samples")
    parser.add_argument("--key", required=True)
    parser.add_argument("-H", "--host", required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("--name", default="PhysicsSampler")
    parser.add_argument("--output", default="log/official_physics_samples_{player}.jsonl")
    parser.add_argument("--max-samples", type=int, default=0, help="0 means run until the server stops")
    parser.add_argument("--plan-file", type=Path, default=None, help="optional JSON list of {v0,h0,w0,sweep,label}")
    parser.add_argument("--collision-tolerance", type=float, default=0.02)
    parser.add_argument("--show-msg", action="store_true")
    args = parser.parse_args()

    plan = parse_plan_file(args.plan_file) if args.plan_file else None
    sampler = OfficialPhysicsSampler(
        key=args.key,
        name=args.name,
        host=args.host,
        port=args.port,
        output=args.output,
        max_samples=args.max_samples,
        plan=plan,
        collision_tolerance=args.collision_tolerance,
        show_msg=args.show_msg,
    )
    sampler.recv_forever()


if __name__ == "__main__":
    main()
