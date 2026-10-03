"""JSON-lines Torch worker for ``CurrentStageCU6Opponent``."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from pathlib import Path

import torch


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from training_research.opponents.current_stagec_u6_adapter import CurrentStageCU6Opponent


def _decision_json(decision, pending: dict) -> dict:
    return {
        "ok": True,
        "bestshot": list(decision.bestshot),
        "tactic": decision.tactic,
        "action_id": decision.action_id,
        "policy_probability": decision.policy_probability,
        "value": decision.value,
        "fallback": decision.fallback,
        "legal_tactics": list(decision.legal_tactics),
        "stage_s_p1_peel_guard": decision.stage_s_p1_peel_guard,
        "stage_s_p2_blocked_draw": decision.stage_s_p2_blocked_draw,
        # The CP39 strict selector receives exactly the state/mask used for
        # this decision; it must not rebuild them with a different context.
        "state": list(pending.get("state", ())),
        "action_mask": list(pending.get("action_mask", ())),
        # The CP39 selector must rank the same history-adjusted distribution
        # as the Torch worker's first PPO choice.
        "historical_k5_k7_prior": dict(pending.get("historical_k5_k7_prior", {})),
    }


def _head_json(model, request: dict) -> dict:
    operation = str(request["operation"])
    state = request["state"]
    if operation == "rank":
        mask = list(request["mask"])
        bias = list(request.get("bias", [0.0] * len(mask)))
        if len(bias) != len(mask):
            bias = [0.0] * len(mask)
        with torch.no_grad():
            distribution, _ = model.distribution(
                torch.as_tensor(state, dtype=torch.float32).unsqueeze(0),
                action_mask=torch.as_tensor(mask, dtype=torch.bool).unsqueeze(0),
                action_logit_bias=torch.as_tensor(bias, dtype=torch.float32).unsqueeze(0),
            )
            probabilities = distribution.probs[0]
            ranked = probabilities.argsort(descending=True).tolist()
        return {
            "ok": True,
            "ranked": [
                [int(action), float(probabilities[int(action)].item())]
                for action in ranked if bool(mask[int(action)])
            ][:int(request.get("top_k", len(mask)))],
        }
    action_id = int(request["action_id"])
    if operation == "target":
        value, log_prob = model.act_target(
            state, target_mask=list(request["mask"]), action_id=action_id,
            deterministic=True, use_d5_residual=bool(request.get("use_d5_residual", False)),
            legacy_target_id=request.get("legacy_target_id"),
        )
    elif operation == "relay":
        value, log_prob = model.act_relay(
            state, middle_mask=list(request["mask"]), action_id=action_id,
            target_index=int(request["target_index"]), deterministic=True,
        )
    elif operation == "double":
        value, log_prob = model.act_double(
            state, second_target_mask=list(request["mask"]), action_id=action_id,
            target_index=int(request["target_index"]), deterministic=True,
        )
    else:
        raise ValueError(f"unknown selector operation: {operation}")
    return {"ok": True, "value": int(value), "log_prob": float(log_prob)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--deterministic", action="store_true")
    parser.add_argument("--stochastic", action="store_true")
    parser.add_argument("--rule-aware-early-hit-mask", action="store_true")
    parser.add_argument("--historical-k5-k7-prior", action="store_true")
    args = parser.parse_args()
    bot = CurrentStageCU6Opponent(
        args.checkpoint,
        deterministic=bool(args.deterministic and not args.stochastic),
        force_local=True,
        rule_aware_early_hit_mask=bool(args.rule_aware_early_hit_mask),
        historical_k5_k7_prior=bool(args.historical_k5_k7_prior),
    )
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if request.get("close"):
                return 0
            operation = str(request.get("operation", "decision"))
            if operation in {"rank", "target", "relay", "double"}:
                response = _head_json(bot._robot.model, request)
                print(json.dumps(response, ensure_ascii=False), flush=True)
                continue
            if operation != "decision":
                raise ValueError(f"unknown operation: {operation}")
            # Live Stage-C emits a readable diagnostic line for every turn;
            # the parent protocol reserves stdout for exactly one JSON reply.
            with contextlib.redirect_stdout(io.StringIO()):
                decision = bot.choose(
                    request["position"],
                    player_is_init=bool(request["player_is_init"]),
                    shot_num=int(request["shot_num"]),
                    end_score=int(request.get("end_score", 0)),
                    total_ends=int(request.get("total_ends", 1)),
                    current_player=int(request.get("current_player", 0)),
                )
            response = _decision_json(decision, bot._robot.pending_transition or {})
        except Exception as exc:
            response = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
