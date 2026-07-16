#!/usr/bin/env python3
"""P1.0: distil late-end strict-PhysX search records into a small policy/value model.

This script intentionally has a narrow contract:

* input is only ``strict_p0_kernel_late_end_teacher_v1`` records produced by
  :mod:`p0_kernel_end_teacher` (non-sweeping, terminal end-score labels);
* a game-level split keeps every decision of a held-out end out of training;
* the policy has a shared board encoder and separate hammer / non-hammer
  action-and-tactic heads; hammer is also an explicit input feature;
* output is a checkpoint plus a JSON report containing the exact input digest,
  split rule, configuration, and held-out teacher-fit metrics.

It is a supervised P1.0 loop, not evidence that the model wins a whole end.
Use a later strict-PhysX comparison against fixed scripts and search to make
that claim.  The source records' search budget is deliberately copied into the
report so a low-budget smoke collection is never presented as a paper-budget
teacher dataset.

Example (must use the strict runtime's Python 3.8 environment)::

    D:\\esp\\tmp\\curling_pyphysx_conda\\python.exe \
      training_research\\p1_policy_value_distill.py \
      --input training_research\\runs\\p0_kernel_late_end.json \
      --run-dir training_research\\runs\\p1_distill_500x5_v1
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SCORE_BINS = tuple(range(-8, 9))
TACTICS = ("guard_left", "guard_right", "draw_center", "takeout", "throw_out")
TACTIC_TO_INDEX = {name: index for index, name in enumerate(TACTICS)}
ACTION_SCALE = (6.0, 2.23, 15.7)
FEATURE_SIZE = 89  # 16 stones * (x, y, sin(yaw), cos(yaw), in-play) + 9 context fields


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "training_research" / "runs" / "p0_kernel_late_end.json",
        help="P0.1 strict-PhysX teacher report",
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=ROOT / "training_research" / "runs" / "p1_distill_smoke_v1",
        help="directory for the checkpoint and reproducibility report",
    )
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--hidden-size", type=int, default=128)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument(
        "--validation-modulus",
        type=int,
        default=5,
        help="a complete game is validation when game number %% modulus == 0",
    )
    parser.add_argument(
        "--max-games",
        type=int,
        default=0,
        help="optional deterministic prefix for a short pipeline smoke run; 0 keeps every game",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def normalized_action(action: Sequence[float]) -> list[float]:
    require(len(action) == 3, "teacher action must contain v0, h0, w0")
    v0, h0, w0 = (float(value) for value in action)
    return [max(0.0, min(1.0, v0 / ACTION_SCALE[0])), max(-1.0, min(1.0, h0 / ACTION_SCALE[1])), max(-1.0, min(1.0, w0 / ACTION_SCALE[2]))]


def encode_state(state: dict[str, Any]) -> list[float]:
    """Return a stable, shooter-relative feature vector from the saved state."""

    board = state["board"]
    values: list[float] = []
    for side in ("self", "opponent"):
        stones = sorted(board[side], key=lambda stone: int(stone["id"]))
        require(len(stones) == 8, "P0 state must retain eight self and eight opponent stone slots")
        for stone in stones:
            yaw = float(stone["yaw"])
            values.extend(
                (
                    float(stone["x"]) / 4.75,
                    float(stone["y"]) / 10.0,
                    math.sin(yaw),
                    math.cos(yaw),
                    1.0 if bool(stone["inPlay"]) else 0.0,
                )
            )
    turn = state["turn"]
    match = state["match"]
    leader = {"opponent": -1.0, "none": 0.0, "self": 1.0}.get(str(turn["houseLeader"]))
    require(leader is not None, "unknown house leader")
    values.extend(
        (
            float(turn["shotIndex"]) / 15.0,
            float(turn["remainingShotsInEnd"]) / 16.0,
            1.0 if bool(turn["isHammerSide"]) else 0.0,
            1.0 if bool(turn["isLastShotOfEnd"]) else 0.0,
            float(leader),
            float(turn["houseScoreForSelf"]) / 8.0,
            float(match["endIndex"]) / 10.0,
            float(match["endsRemainingAfterThis"]) / 10.0,
            float(match["scoreDifferenceForSelf"]) / 8.0,
        )
    )
    require(len(values) == FEATURE_SIZE, "unexpected feature shape")
    return values


def aggregate_tactic_weights(candidates: Iterable[dict[str, Any]]) -> list[float]:
    target = [0.0] * len(TACTICS)
    for candidate in candidates:
        tactic = str(candidate["tactic"])
        require(tactic in TACTIC_TO_INDEX, "unknown P0 tactic: %s" % tactic)
        target[TACTIC_TO_INDEX[tactic]] += max(0.0, float(candidate["searchWeight"]))
    total = sum(target)
    require(total > 0.0, "candidate weights must be positive")
    return [value / total for value in target]


def histogram_distribution(histogram: dict[str, Any]) -> list[float]:
    values = [max(0.0, float(histogram.get(str(score), 0.0))) for score in SCORE_BINS]
    total = sum(values)
    require(total > 0.0, "teacher terminal-score histogram is empty")
    return [value / total for value in values]


def load_examples(path: Path, max_games: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    require(document.get("schema") == "strict_p0_kernel_late_end_teacher_v1", "input must be strict_p0_kernel_late_end_teacher_v1")
    require(bool(document.get("trainingUsable")), "input report is not marked training-usable")
    games = list(document.get("games", []))
    if max_games:
        require(max_games > 0, "--max-games must be non-negative")
        games = games[:max_games]
    examples: list[dict[str, Any]] = []
    for game in games:
        game_number = int(game["game"])
        for decision_index, decision in enumerate(game["decisions"]):
            state = decision["state"]
            search = decision["search"]
            selected = search["selected"]
            examples.append(
                {
                    "game": game_number,
                    "decisionIndex": decision_index,
                    "shotIndex": int(state["turn"]["shotIndex"]),
                    "isHammerSide": bool(state["turn"]["isHammerSide"]),
                    "features": encode_state(state),
                    "tacticTarget": aggregate_tactic_weights(search["candidates"]),
                    "selectedTactic": TACTIC_TO_INDEX[str(selected["tactic"])],
                    "actionTarget": normalized_action(selected["action"]),
                    "scoreTarget": histogram_distribution(search["targetScoreDistributionDirect"]),
                    "searchSampleBudget": int(search["sampleBudget"]),
                    "targetRollouts": int(search["targetRollouts"]),
                }
            )
    require(examples, "input contains no teacher decisions")
    metadata = {
        "inputSchema": document["schema"],
        "inputScope": document.get("scope"),
        "inputWarning": document.get("warning"),
        "collectionConfig": document.get("collection", {}).get("config", {}),
        "gamesRead": len(games),
        "examplesRead": len(examples),
        "searchSampleBudgetCounts": dict(sorted(Counter(row["searchSampleBudget"] for row in examples).items())),
        "targetRolloutCounts": dict(sorted(Counter(row["targetRollouts"] for row in examples).items())),
    }
    return examples, metadata


def split_examples(examples: list[dict[str, Any]], modulus: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require(modulus >= 2, "--validation-modulus must be at least 2")
    train = [row for row in examples if row["game"] % modulus != 0]
    validation = [row for row in examples if row["game"] % modulus == 0]
    require(train and validation, "game-level split produced an empty train or validation set")
    return train, validation


def make_tensors(rows: list[dict[str, Any]], torch: Any) -> dict[str, Any]:
    return {
        "features": torch.tensor([row["features"] for row in rows], dtype=torch.float32),
        "hammer": torch.tensor([1 if row["isHammerSide"] else 0 for row in rows], dtype=torch.long),
        "tactic": torch.tensor([row["tacticTarget"] for row in rows], dtype=torch.float32),
        "selectedTactic": torch.tensor([row["selectedTactic"] for row in rows], dtype=torch.long),
        "action": torch.tensor([row["actionTarget"] for row in rows], dtype=torch.float32),
        "score": torch.tensor([row["scoreTarget"] for row in rows], dtype=torch.float32),
    }


def build_model(torch: Any, hidden_size: int) -> Any:
    nn = torch.nn

    class PolicyValueNet(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(FEATURE_SIZE, hidden_size), nn.ReLU(),
                nn.Linear(hidden_size, hidden_size), nn.ReLU(),
            )
            self.policy_heads = nn.ModuleList([nn.Linear(hidden_size, len(TACTICS)), nn.Linear(hidden_size, len(TACTICS))])
            self.action_heads = nn.ModuleList([nn.Linear(hidden_size, 3), nn.Linear(hidden_size, 3)])
            self.value_head = nn.Linear(hidden_size, len(SCORE_BINS))

        def forward(self, features: Any, hammer: Any) -> tuple[Any, Any, Any]:
            latent = self.encoder(features)
            policy_all = torch.stack([head(latent) for head in self.policy_heads], dim=1)
            action_all = torch.stack([head(latent) for head in self.action_heads], dim=1)
            selector = hammer.view(-1, 1, 1).expand(-1, 1, policy_all.shape[-1])
            policy = policy_all.gather(1, selector).squeeze(1)
            selector = hammer.view(-1, 1, 1).expand(-1, 1, action_all.shape[-1])
            raw_action = action_all.gather(1, selector).squeeze(1)
            action = torch.cat((torch.sigmoid(raw_action[:, :1]), torch.tanh(raw_action[:, 1:])), dim=1)
            return policy, action, self.value_head(latent)

    return PolicyValueNet()


def loss_and_metrics(model: Any, tensors: dict[str, Any], indices: Any, torch: Any) -> tuple[Any, dict[str, float]]:
    policy_logits, predicted_action, value_logits = model(tensors["features"][indices], tensors["hammer"][indices])
    tactic_target = tensors["tactic"][indices]
    action_target = tensors["action"][indices]
    score_target = tensors["score"][indices]
    policy_loss = -(tactic_target * torch.log_softmax(policy_logits, dim=1)).sum(dim=1).mean()
    action_loss = torch.nn.functional.smooth_l1_loss(predicted_action, action_target)
    value_loss = -(score_target * torch.log_softmax(value_logits, dim=1)).sum(dim=1).mean()
    total = policy_loss + action_loss + value_loss
    top_tactic = policy_logits.argmax(dim=1)
    target_tactic = tactic_target.argmax(dim=1)
    selected_tactic = tensors["selectedTactic"][indices]
    absolute_error = (predicted_action - action_target).abs().mean(dim=0)
    metric = {
        "totalLoss": float(total.detach().cpu()),
        "policyCrossEntropy": float(policy_loss.detach().cpu()),
        "actionSmoothL1": float(action_loss.detach().cpu()),
        "valueCrossEntropy": float(value_loss.detach().cpu()),
        "tacticTop1AgainstWeightArgmax": float((top_tactic == target_tactic).float().mean().detach().cpu()),
        "tacticTop1AgainstSelectedTactic": float((top_tactic == selected_tactic).float().mean().detach().cpu()),
        "actionMeanAbsoluteErrorNormalizedV0": float(absolute_error[0].detach().cpu()),
        "actionMeanAbsoluteErrorNormalizedH0": float(absolute_error[1].detach().cpu()),
        "actionMeanAbsoluteErrorNormalizedW0": float(absolute_error[2].detach().cpu()),
    }
    return total, metric


def evaluate(model: Any, tensors: dict[str, Any], torch: Any) -> dict[str, Any]:
    model.eval()
    with torch.no_grad():
        all_indices = torch.arange(tensors["features"].shape[0])
        _, aggregate = loss_and_metrics(model, tensors, all_indices, torch)
        by_role: dict[str, Any] = {}
        for hammer_value, name in ((0, "nonHammer"), (1, "hammer")):
            indices = torch.where(tensors["hammer"] == hammer_value)[0]
            if len(indices):
                _, by_role[name] = loss_and_metrics(model, tensors, indices, torch)
                by_role[name]["examples"] = int(len(indices))
    return {"all": aggregate, "byRole": by_role}


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(args.epochs > 0 and args.batch_size > 0 and args.hidden_size > 0, "epochs, batch size, and hidden size must be positive")
    require(args.learning_rate > 0.0, "learning rate must be positive")
    try:
        import torch
    except ImportError as error:
        raise RuntimeError("PyTorch is required; use D:\\esp\\tmp\\curling_pyphysx_conda\\python.exe") from error

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    examples, source_metadata = load_examples(args.input, args.max_games)
    train_rows, validation_rows = split_examples(examples, args.validation_modulus)
    train_tensors = make_tensors(train_rows, torch)
    validation_tensors = make_tensors(validation_rows, torch)
    model = build_model(torch, args.hidden_size)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    generator = torch.Generator().manual_seed(args.seed)
    history: list[dict[str, Any]] = []
    best_epoch = 0
    best_validation: dict[str, Any] | None = None
    best_state: dict[str, Any] | None = None
    last_validation: dict[str, Any] | None = None
    for epoch in range(1, args.epochs + 1):
        model.train()
        order = torch.randperm(len(train_rows), generator=generator)
        for offset in range(0, len(train_rows), args.batch_size):
            indices = order[offset : offset + args.batch_size]
            loss, _ = loss_and_metrics(model, train_tensors, indices, torch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        last_validation = evaluate(model, validation_tensors, torch)
        if best_validation is None or last_validation["all"]["totalLoss"] < best_validation["all"]["totalLoss"]:
            best_epoch = epoch
            best_validation = copy.deepcopy(last_validation)
            best_state = copy.deepcopy(model.state_dict())
        if epoch == 1 or epoch == args.epochs or epoch % 10 == 0 or epoch == best_epoch:
            history.append({"epoch": epoch, "train": evaluate(model, train_tensors, torch), "validation": last_validation})

    require(best_state is not None and best_validation is not None and last_validation is not None, "training did not produce a validation checkpoint")
    model.load_state_dict(best_state)

    run_dir = args.run_dir
    run_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = run_dir / "policy_value.pt"
    report_path = run_dir / "report.json"
    checkpoint = {
        "schema": "strict_p1_policy_value_checkpoint_v1",
        "featureSize": FEATURE_SIZE,
        "tactics": list(TACTICS),
        "scoreBins": list(SCORE_BINS),
        "actionScale": list(ACTION_SCALE),
        "hiddenSize": args.hidden_size,
        "stateDict": model.state_dict(),
    }
    torch.save(checkpoint, checkpoint_path)
    report = {
        "schema": "strict_p1_policy_value_distill_report_v1",
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "scope": "non-sweeping; strict local PhysX teacher labels; final five shots of one end; supervised teacher-fit only",
        "claimBoundary": "This report measures held-out fit to P0.1 search labels. It does not measure whole-end score, win rate, or superiority to search/fixed strategy.",
        "runtime": {"python": sys.version, "torch": str(torch.__version__), "device": "cpu", "deterministicAlgorithms": True},
        "input": {"path": str(args.input), "sha256": sha256_file(args.input), **source_metadata},
        "split": {
            "unit": "complete generated end (game)",
            "rule": "game number %% %d != 0 train; game number %% %d == 0 validation" % (args.validation_modulus, args.validation_modulus),
            "trainExamples": len(train_rows),
            "validationExamples": len(validation_rows),
            "trainGames": sorted({row["game"] for row in train_rows}),
            "validationGames": sorted({row["game"] for row in validation_rows}),
        },
        "model": {
            "featureSize": FEATURE_SIZE,
            "sharedEncoder": [FEATURE_SIZE, args.hidden_size, args.hidden_size],
            "policyHeads": "two independent heads selected by isHammerSide; isHammerSide is also an input feature",
            "tactics": list(TACTICS),
            "actionParameterOrder": ["v0", "h0", "w0"],
            "scoreBinsForCurrentShooter": list(SCORE_BINS),
        },
        "training": {"seed": args.seed, "epochs": args.epochs, "batchSize": args.batch_size, "learningRate": args.learning_rate},
        "history": history,
        "checkpointSelection": {
            "method": "lowest complete-end validation total loss",
            "selectedEpoch": best_epoch,
            "selectedValidation": best_validation,
            "lastEpochValidationBeforeSelection": last_validation,
        },
        "finalValidation": evaluate(model, validation_tensors, torch),
        "artifacts": {"checkpoint": str(checkpoint_path), "report": str(report_path)},
    }
    report_path.write_text(json.dumps(json_ready(report), ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    args = parse_args()
    report = run(args)
    metrics = report["finalValidation"]["all"]
    print("P1.0 完成：%d 训练 / %d 验证样本" % (report["split"]["trainExamples"], report["split"]["validationExamples"]))
    print("验证策略交叉熵 %.4f，动作平均绝对误差(归一化) v/h/w = %.4f / %.4f / %.4f" % (
        metrics["policyCrossEntropy"], metrics["actionMeanAbsoluteErrorNormalizedV0"], metrics["actionMeanAbsoluteErrorNormalizedH0"], metrics["actionMeanAbsoluteErrorNormalizedW0"],
    ))
    print("报告：%s" % report["artifacts"]["report"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
