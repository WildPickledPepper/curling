# -*- coding: utf-8 -*-
"""Run local one-end episodes for the tactic-level DQN robot."""

from __future__ import annotations

import argparse
import random
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from tactic_dqn_robot import ACTIONS, TacticDQN, TacticDQNRobot


LEGACY_ROOT = Path(__file__).resolve().parent


def find_freeish_port(base_port: int, episode: int) -> int:
    return base_port + (episode % 100)


def run_episode(
    episode: int,
    port: int,
    key: str,
    model_file: str,
    log_file: str,
    show_server: bool,
    brain: TacticDQN,
) -> None:
    seed = random.randint(1, 2_000_000_000)
    server_cmd = [
        sys.executable,
        str(LEGACY_ROOT / "mock_curling_server.py"),
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--key",
        key,
        "--rounds",
        "1",
        "--seed",
        str(seed),
    ]
    if show_server:
        server_cmd.append("--show-messages")

    stdout = None if show_server else subprocess.DEVNULL
    stderr = None if show_server else subprocess.DEVNULL
    server = subprocess.Popen(stdout=stdout, stderr=stderr, args=server_cmd)
    try:
        time.sleep(0.35)
        robot = TacticDQNRobot(
            key=key,
            name=f"TacticDQN_{episode}",
            host="127.0.0.1",
            port=port,
            model_file=model_file,
            log_file=log_file,
            train=True,
            max_rounds=1,
            save_every=1,
            brain=brain,
        )
        robot.recv_forever()
    finally:
        try:
            server.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            server.terminate()
            try:
                server.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                server.kill()


def main() -> None:
    parser = argparse.ArgumentParser(description="Train TacticDQN against the local mock server")
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--base-port", type=int, default=7900)
    parser.add_argument("--key", default="local-train-key")
    parser.add_argument("--model-file", default="model/tactic_dqn.pth")
    parser.add_argument("--log-file", default="log/tactic_dqn_train.log")
    parser.add_argument("--show-server", action="store_true")
    args = parser.parse_args()

    Path(args.model_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.log_file).parent.mkdir(parents=True, exist_ok=True)
    brain = TacticDQN(Path(args.model_file), action_dim=len(ACTIONS), train=True)

    for episode in range(1, args.episodes + 1):
        port = find_freeish_port(args.base_port, episode)
        print(f"===== episode {episode}/{args.episodes} port={port} =====", flush=True)
        run_episode(
            episode=episode,
            port=port,
            key=args.key,
            model_file=args.model_file,
            log_file=args.log_file,
            show_server=args.show_server,
            brain=brain,
        )


if __name__ == "__main__":
    main()
