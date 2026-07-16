"""Flat entry point for the digital curling PPO AI.

Edit CONNECT_KEY when running this file directly in the course-platform
JupyterLab. Command-line -k/-H/-p still override these defaults when provided.
"""

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

CONNECT_KEY = "zzy_519763ad-f64d-4147-832a-0a55b7487767"
HOST = "curling-server-7788.jupyterhub.svc.cluster.local"
PORT = 7788
AI_NAME = "zzy_ppo"
AI_MODE = "ppo"
DEFAULT_CHECKPOINT = ROOT / "latest.pt"


def env_value(*names: str, default: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def parse_args():
    parser = argparse.ArgumentParser(description="Run the flat digital curling AI.")
    parser.add_argument("--mode", choices=("ppo", "tactics"), default=AI_MODE)
    parser.add_argument("-k", "--key", default=env_value("CONNECTKEY", "CURLING_KEY", default=CONNECT_KEY))
    parser.add_argument("-H", "--host", default=env_value("CURLING_HOST", default=HOST))
    parser.add_argument("-p", "--port", type=int, default=int(env_value("CURLING_PORT", default=str(PORT))))
    parser.add_argument("--name", default=env_value("CURLING_AI_NAME", default=AI_NAME))
    parser.add_argument(
        "--checkpoint",
        default=env_value("PPO_CHECKPOINT", "CURLING_CHECKPOINT", default=str(DEFAULT_CHECKPOINT)),
    )
    parser.add_argument("--stochastic", action="store_true")
    parser.add_argument("--action-logit-bias", action="append", default=[])
    parser.add_argument("--show-msg", action="store_true")
    args, unknown = parser.parse_known_args()
    if unknown:
        print("Ignoring unknown platform arguments: " + " ".join(unknown), file=sys.stderr, flush=True)
    return args


def resolve_checkpoint(requested: str) -> Path:
    candidates = []
    if requested:
        raw = Path(requested)
        candidates.append(raw)
        if not raw.is_absolute():
            candidates.append(ROOT / raw)
    candidates.append(DEFAULT_CHECKPOINT)

    seen = set()
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if path.exists():
            return path
    raise FileNotFoundError(
        "PPO checkpoint not found. Put latest.pt beside main.py, "
        "or pass --checkpoint / set PPO_CHECKPOINT."
    )


def run_ppo(args) -> None:
    from ppo_robot_flat import PPOTacticsRobot, load_model, parse_action_logit_bias

    checkpoint = resolve_checkpoint(args.checkpoint)
    print(f"Using PPO checkpoint: {checkpoint}", flush=True)
    model = load_model(str(checkpoint))
    robot = PPOTacticsRobot(
        key=args.key,
        name=args.name,
        host=args.host,
        port=args.port,
        model=model,
        deterministic=not args.stochastic,
        action_logit_bias=parse_action_logit_bias(args.action_logit_bias),
        show_msg=args.show_msg,
    )
    rollout = robot.recv_forever()
    print(
        f"PPO rollout collected: {len(rollout)} transitions, "
        f"invalid_actions={robot.invalid_action_count}, "
        f"fallback_draws={robot.fallback_draw_count}",
        flush=True,
    )


def run_tactics(args) -> None:
    from tactics_main_flat import TacticsRobot

    robot = TacticsRobot(
        key=args.key,
        name=args.name,
        host=args.host,
        port=args.port,
        show_msg=args.show_msg,
    )
    robot.recv_forever()


def main() -> None:
    args = parse_args()
    if args.mode == "ppo":
        run_ppo(args)
    else:
        run_tactics(args)


if __name__ == "__main__":
    main()
