# -*- coding: utf-8 -*-
"""Iterative self-play trainer with promotion gates.

This script wraps the existing search-distillation trainer instead of
duplicating the learning code.  Each cycle trains a first-player and
second-player candidate against a mixed opponent pool, then evaluates the
candidate pair against the current champion with symmetric side swapping.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional


ROOT = Path(__file__).resolve().parent
DEFAULT_FIRST = ROOT / "model" / "search_distill_tactic_policy_first.pt"
DEFAULT_SECOND = ROOT / "model" / "search_distill_tactic_policy_second.pt"


def run_command(command: list[str]) -> None:
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def train_side(
    *,
    player: str,
    cycle: int,
    args: argparse.Namespace,
    first_champion: Path,
    second_champion: Path,
    model_file: Path,
    report_file: Path,
) -> Dict[str, Any]:
    command = [
        sys.executable,
        str(ROOT / "train_search_distill.py"),
        "--player",
        player,
        "--opponent-policy",
        args.opponent_policy,
        "--games",
        str(args.games),
        "--rollouts",
        str(args.rollouts),
        "--epochs",
        str(args.epochs),
        "--batch-size",
        str(args.batch_size),
        "--eval-games",
        str(args.eval_games),
        "--search-eval-games",
        str(args.search_eval_games),
        "--seed",
        str(args.seed + cycle * 1000 + (0 if player == "first" else 100)),
        "--opponent-first-model-file",
        str(first_champion),
        "--opponent-second-model-file",
        str(second_champion),
        "--model-file",
        str(model_file),
        "--report-file",
        str(report_file),
    ]
    if args.lr is not None:
        command.extend(["--lr", str(args.lr)])
    run_command(command)
    return read_json(report_file)


def evaluate_candidate(
    *,
    cycle: int,
    args: argparse.Namespace,
    candidate_first: Path,
    candidate_second: Path,
    champion_first: Path,
    champion_second: Path,
    report_file: Path,
) -> Dict[str, Any]:
    command = [
        sys.executable,
        str(ROOT / "evaluate_head_to_head.py"),
        "--blue-policy",
        "dual_refined",
        "--red-policy",
        "dual_refined",
        "--swap-sides",
        "--games",
        str(args.head_to_head_games),
        "--trace-games",
        str(args.trace_games),
        "--blue-first-model-file",
        str(candidate_first),
        "--blue-second-model-file",
        str(candidate_second),
        "--red-first-model-file",
        str(champion_first),
        "--red-second-model-file",
        str(champion_second),
        "--top-k",
        str(args.top_k),
        "--candidates",
        str(args.candidates),
        "--rollouts",
        str(args.eval_rollouts),
        "--late-top-k",
        str(args.late_top_k),
        "--late-candidates",
        str(args.late_candidates),
        "--late-rollouts",
        str(args.late_rollouts),
        "--hammer-candidates",
        str(args.hammer_candidates),
        "--hammer-rollouts",
        str(args.hammer_rollouts),
        "--seed",
        str(args.seed + cycle * 1000 + 500),
        "--report-file",
        str(report_file),
    ]
    run_command(command)
    return read_json(report_file)


def promotion_decision(report: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    summary = report["symmetric_summary"]
    candidate_stats = summary["policy_a_action_families"]
    champion_stats = summary["policy_b_action_families"]
    avg_score = float(summary["policy_a_avg_score"])
    win_rate = float(summary["policy_a_win_rate"])
    offense_rate = float(candidate_stats["offense_rate"])
    champion_offense_rate = float(champion_stats["offense_rate"])
    passed = (
        avg_score >= args.min_avg_score
        and win_rate >= args.min_win_rate
        and offense_rate >= args.min_offense_rate
        and offense_rate + args.max_offense_regression >= champion_offense_rate
    )
    return {
        "passed": passed,
        "avg_score": avg_score,
        "win_rate": win_rate,
        "offense_rate": offense_rate,
        "champion_offense_rate": champion_offense_rate,
        "min_avg_score": args.min_avg_score,
        "min_win_rate": args.min_win_rate,
        "min_offense_rate": args.min_offense_rate,
        "max_offense_regression": args.max_offense_regression,
    }


def promote(candidate_first: Path, candidate_second: Path, champion_first: Path, champion_second: Path) -> None:
    backup_dir = ROOT / "model" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    if champion_first.exists():
        shutil.copy2(champion_first, backup_dir / f"{champion_first.stem}_{stamp}.pt")
    if champion_second.exists():
        shutil.copy2(champion_second, backup_dir / f"{champion_second.stem}_{stamp}.pt")
    shutil.copy2(candidate_first, champion_first)
    shutil.copy2(candidate_second, champion_second)


def run_cycle(cycle: int, args: argparse.Namespace, champion_first: Path, champion_second: Path) -> Dict[str, Any]:
    run_dir = ROOT / "log" / "self_play_runs" / f"cycle_{cycle:03d}"
    model_dir = ROOT / "model" / "self_play"
    run_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    candidate_first = model_dir / f"search_distill_tactic_policy_first_cycle{cycle:03d}.pt"
    candidate_second = model_dir / f"search_distill_tactic_policy_second_cycle{cycle:03d}.pt"
    first_report_file = run_dir / "train_first.json"
    second_report_file = run_dir / "train_second.json"
    h2h_report_file = run_dir / "head_to_head_candidate_vs_champion.json"

    first_report = train_side(
        player="first",
        cycle=cycle,
        args=args,
        first_champion=champion_first,
        second_champion=champion_second,
        model_file=candidate_first,
        report_file=first_report_file,
    )
    second_report = train_side(
        player="second",
        cycle=cycle,
        args=args,
        first_champion=champion_first,
        second_champion=champion_second,
        model_file=candidate_second,
        report_file=second_report_file,
    )
    h2h_report = evaluate_candidate(
        cycle=cycle,
        args=args,
        candidate_first=candidate_first,
        candidate_second=candidate_second,
        champion_first=champion_first,
        champion_second=champion_second,
        report_file=h2h_report_file,
    )
    decision = promotion_decision(h2h_report, args)
    if args.promote and decision["passed"]:
        promote(candidate_first, candidate_second, champion_first, champion_second)
        decision["promoted"] = True
    else:
        decision["promoted"] = False

    cycle_report = {
        "cycle": cycle,
        "candidate_first": str(candidate_first),
        "candidate_second": str(candidate_second),
        "champion_first": str(champion_first),
        "champion_second": str(champion_second),
        "first_training": first_report,
        "second_training": second_report,
        "head_to_head": h2h_report,
        "promotion_decision": decision,
        "elapsed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    (run_dir / "cycle_report.json").write_text(
        json.dumps(cycle_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps({"cycle": cycle, "promotion_decision": decision}, indent=2), flush=True)
    return cycle_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=1, help="0 means run until interrupted")
    parser.add_argument("--games", type=int, default=250)
    parser.add_argument("--rollouts", type=int, default=4)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--eval-games", type=int, default=250)
    parser.add_argument("--search-eval-games", type=int, default=80)
    parser.add_argument("--head-to-head-games", type=int, default=30)
    parser.add_argument(
        "--opponent-policy",
        choices=["balanced-mix", "model-mix", "scripted", "rollout", "random"],
        default="balanced-mix",
    )
    parser.add_argument("--champion-first-model-file", type=Path, default=DEFAULT_FIRST)
    parser.add_argument("--champion-second-model-file", type=Path, default=DEFAULT_SECOND)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--candidates", type=int, default=16)
    parser.add_argument("--eval-rollouts", type=int, default=1)
    parser.add_argument("--late-top-k", type=int, default=4)
    parser.add_argument("--late-candidates", type=int, default=24)
    parser.add_argument("--late-rollouts", type=int, default=2)
    parser.add_argument("--hammer-candidates", type=int, default=32)
    parser.add_argument("--hammer-rollouts", type=int, default=2)
    parser.add_argument("--trace-games", type=int, default=2)
    parser.add_argument("--min-avg-score", type=float, default=0.05)
    parser.add_argument("--min-win-rate", type=float, default=0.50)
    parser.add_argument("--min-offense-rate", type=float, default=0.08)
    parser.add_argument("--max-offense-regression", type=float, default=0.02)
    parser.add_argument("--seed", type=int, default=20260710)
    parser.add_argument("--promote", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cycle = 1
    while args.cycles == 0 or cycle <= args.cycles:
        run_cycle(
            cycle,
            args,
            args.champion_first_model_file,
            args.champion_second_model_file,
        )
        cycle += 1


if __name__ == "__main__":
    main()
