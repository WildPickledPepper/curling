"""Stage S U6 deployment entry point.

The Deep Sets U6 checkpoint is loaded from ``latest.pt`` beside this file.
Both approved Stage S endgame guards are enabled by default.
"""

import argparse
import os
from pathlib import Path

from ppo_state_reward import FALLBACK_DRAW_PENALTY, INVALID_ACTION_PENALTY
from v2_config import V2PPOConfig
from v2_stage_c_collector import StageCRolloutRobot, load_stage_c_model


ROOT = Path(__file__).resolve().parent
CONNECT_KEY = "zzy_519763ad-f64d-4147-832a-0a55b7487767"
HOST = "curling-server-7788.jupyterhub.svc.cluster.local"
PORT = 7788
AI_NAME = "zzy_stage_s_u6"


def env_value(*names, default):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Stage S U6 curling AI.")
    parser.add_argument("-k", "--key", default=env_value("CONNECTKEY", "CURLING_KEY", default=CONNECT_KEY))
    parser.add_argument("-H", "--host", default=env_value("CURLING_HOST", default=HOST))
    parser.add_argument("-p", "--port", type=int, default=int(env_value("CURLING_PORT", default=str(PORT))))
    parser.add_argument("--name", default=env_value("CURLING_AI_NAME", default=AI_NAME))
    parser.add_argument("--checkpoint", default=env_value("PPO_CHECKPOINT", "CURLING_CHECKPOINT", default=str(ROOT / "latest.pt")))
    parser.add_argument("--stochastic", action="store_true")
    parser.add_argument("--show-msg", action="store_true")
    args, unknown = parser.parse_known_args()
    if unknown:
        print("Ignoring unknown platform arguments: " + " ".join(unknown), flush=True)
    return args


def main():
    args = parse_args()
    checkpoint = Path(args.checkpoint)
    if not checkpoint.is_absolute():
        checkpoint = ROOT / checkpoint
    if not checkpoint.exists():
        raise FileNotFoundError("U6 checkpoint not found: %s" % checkpoint)
    print("Using Stage S U6 checkpoint: %s" % checkpoint, flush=True)
    model = load_stage_c_model(checkpoint)
    robot = StageCRolloutRobot(
        key=args.key,
        name=args.name,
        host=args.host,
        port=args.port,
        model=model,
        deterministic=not args.stochastic,
        rollout_steps=0,
        trajectory_id="stage-s-deployment",
        v2_config=V2PPOConfig(
            response_aware_reward=True,
            stage_c_context_mask=True,
            complex_hit_target_mask=True,
            stage_s_p1_peel_guard=True,
            stage_s_p2_blocked_draw=True,
        ),
        invalid_penalty=INVALID_ACTION_PENALTY,
        fallback_draw_penalty=FALLBACK_DRAW_PENALTY,
        show_msg=args.show_msg,
    )
    robot.recv_forever()


if __name__ == "__main__":
    main()
