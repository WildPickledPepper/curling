#!/usr/bin/env python3
"""P0.1: strict-PhysX late-end kernel-search teacher (non-sweeping).

This is deliberately restricted to the final ``N`` shots of an end.  Every
candidate is rolled forward to a real end score with a fixed alternating
continuation policy, so labels are terminal end-score distributions rather
than the misleading temporary score after one shot.  The script is the first
usable source of search-distillation data; it does not train a network.

The search is a compact root-only KR-UCT-style bandit:

* tactic templates create meaningful continuous-action starting points;
* each simulated result is kernel-shared with nearby intended shots;
* UCB chooses the next sample and a lower confidence bound selects the shot;
* search output stores the full state, role fields, candidates, and terminal
  score histogram from the current shooter's perspective.

It is intentionally not called a full MCTS.  A later phase can replace the
fixed continuation policy with a policy/value model and extend to early turns.

Example (four persistent worker processes):
    python training_research\\p0_kernel_end_teacher.py --games 500 --workers 4
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import math
import multiprocessing
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import (
    HOUSE_R,
    HOUSE_X,
    HOUSE_Y,
    STONE_COUNT,
    StrictCurlingEnd,
    TACTICS,
    distance,
    score_board,
    tactic_shot,
    team_score,
)


SCORE_BINS = tuple(range(-8, 9))
HAMMER_TEAM = 1  # With indices 0..15 and alternating throws, second throws last.

# Set once per spawned process. Each worker owns two persistent native PhysX
# scenes, never sharing a scene, RNG sequence, or reset state with another.
_COLLECTION_MASTER = None
_COLLECTION_ROLLOUT = None


@dataclass(frozen=True)
class Proposal:
    tactic: str
    shot: tuple[float, float, float]
    origin: str


@dataclass(frozen=True)
class Sample:
    proposal_index: int
    episode_seed: int
    terminal_score: int
    continuation_shot_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games", type=int, default=1, help="independent seeded ends")
    parser.add_argument(
        "--first-search-shot",
        type=int,
        default=11,
        help="zero-based first searched shot; 11 means shots 12–16 and at most five remaining throws",
    )
    parser.add_argument("--search-samples", type=int, default=16, help="kernel-bandit rollouts per root")
    parser.add_argument(
        "--initial-samples-per-template",
        type=int,
        default=2,
        help="direct terminal rollouts required for each initial tactic before UCB",
    )
    parser.add_argument(
        "--target-rollouts",
        type=int,
        default=4,
        help="fresh terminal rollouts of the chosen action used for its trainable score distribution",
    )
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--confidence-z", type=float, default=1.0, help="LCB standard-error multiplier")
    parser.add_argument("--exploration", type=float, default=0.75, help="kernel-UCB exploration multiplier")
    parser.add_argument("--expand-every", type=int, default=3, help="add a local continuous proposal every N samples")
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=20,
        help="cap total tactical/continuous candidates; KR-UCT used roughly 7–30",
    )
    parser.add_argument("--workers", type=int, default=1, help="independent persistent PhysX worker processes")
    parser.add_argument(
        "--checkpoint-dir",
        type=Path,
        default=ROOT / "training_research" / "runs" / "p0_kernel_late_end_parts",
        help="one completed end per JSON file; makes interrupted collection resumable",
    )
    parser.add_argument("--no-resume", action="store_false", dest="resume", help="ignore existing completed end files")
    parser.set_defaults(resume=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "training_research" / "runs" / "p0_kernel_late_end.json",
    )
    return parser.parse_args()


def clamp_shot(shot: Sequence[float]) -> tuple[float, float, float]:
    return (
        max(0.0, min(6.0, float(shot[0]))),
        max(-2.23, min(2.23, float(shot[1]))),
        max(-15.7, min(15.7, float(shot[2]))),
    )


def state_snapshot(states: Sequence[dict[str, Any]]) -> tuple[list[float], dict[int, float]]:
    """Make a settled board independently resettable, including all retained yaw."""

    positions = [0.0] * 32
    yaws: dict[int, float] = {}
    for state in states:
        index = int(state["index"])
        yaws[index] = float(state["yaw"])
        if not bool(state["enabled"]):
            continue
        positions[index * 2] = float(state["x"])
        positions[index * 2 + 1] = float(state["y"])
    return positions, yaws


def house_status(states: Sequence[dict[str, Any]], team: int) -> tuple[str, int]:
    """Return temporary house leader and its count from the shooter's view."""

    board = score_board(states)
    if board == 0:
        return "none", 0
    leader = 0 if board > 0 else 1
    return ("self" if leader == team else "opponent"), abs(board)


def canonical_state(states: Sequence[dict[str, Any]], shot_number: int, team: int) -> dict[str, Any]:
    """Policy-ready public state plus the raw identity-bearing replay state."""

    self_stones: list[dict[str, Any]] = []
    opponent_stones: list[dict[str, Any]] = []
    raw_stones: list[dict[str, Any]] = []
    for state in states:
        index = int(state["index"])
        item = {
            "id": index,
            "owner": "first" if index % 2 == 0 else "second",
            "x": float(state["x"]),
            "y": float(state["y"]),
            "yaw": float(state["yaw"]),
            "inPlay": bool(state["enabled"]),
        }
        raw_stones.append(item)
        (self_stones if index % 2 == team else opponent_stones).append(
            {key: item[key] for key in ("id", "x", "y", "yaw", "inPlay")}
        )
    leader, count = house_status(states, team)
    return {
        "rawStones": raw_stones,
        "board": {"self": self_stones, "opponent": opponent_stones},
        "turn": {
            "shotIndex": int(shot_number),
            "remainingShotsInEnd": STONE_COUNT - int(shot_number),
            "currentShooter": "first" if team == 0 else "second",
            "isHammerSide": bool(team == HAMMER_TEAM),
            "isLastShotOfEnd": bool(shot_number == STONE_COUNT - 1),
            "houseLeader": leader,
            "houseScoreForSelf": count,
        },
        # P0.1 is an isolated end.  Retaining these fields keeps every row
        # forward-compatible with P3 rather than silently changing input shape.
        "match": {
            "endIndex": 0,
            "endsRemainingAfterThis": 0,
            "scoreDifferenceForSelf": 0,
            "mode": "single_end_p0_1",
        },
    }


def scripted_continuation_shot(states: Sequence[dict[str, Any]], shot_number: int) -> tuple[float, float, float]:
    """Fixed, deterministic continuation policy used only to complete a rollout.

    It is deliberately simple and recorded in every sample.  It must never be
    confused with the teacher or with a deployable opponent policy.
    """

    team = shot_number % 2
    enemies_in_house = [
        state
        for index, state in enumerate(states)
        if bool(state["enabled"])
        and index % 2 != team
        and distance(float(state["x"]), float(state["y"])) <= HOUSE_R + 0.145
    ]
    if enemies_in_house:
        return tactic_shot(3, states, team)  # takeout
    if shot_number < 6:
        return tactic_shot(shot_number % 2, states, team)  # alternating guards
    return tactic_shot(2, states, team)  # draw center


def initial_proposals(states: Sequence[dict[str, Any]], team: int) -> list[Proposal]:
    """One continuous start point per validated tactic template."""

    unique: dict[tuple[float, float, float], Proposal] = {}
    for tactic_index, tactic in enumerate(TACTICS):
        shot = clamp_shot(tactic_shot(tactic_index, states, team))
        unique.setdefault(shot, Proposal(tactic=tactic.name, shot=shot, origin="tactic_template"))
    return list(unique.values())


def kernel(action: Sequence[float], sampled_action: Sequence[float]) -> float:
    """Execution-scale Gaussian kernel for local continuous value sharing.

    Bandwidths are conservative engineering starting values.  They are stored
    in the output and are not claimed to be Unity's stochastic execution law.
    """

    dv = (float(action[0]) - float(sampled_action[0])) / 0.12
    dh = (float(action[1]) - float(sampled_action[1])) / 0.16
    dw = (float(action[2]) - float(sampled_action[2])) / 0.80
    return math.exp(-0.5 * (dv * dv + dh * dh + dw * dw))


def kernel_statistics(proposals: Sequence[Proposal], samples: Sequence[Sample], proposal_index: int) -> dict[str, float]:
    if not samples:
        return {"effectiveCount": 0.0, "mean": 0.0, "variance": 0.0, "standardError": math.inf}
    weights = [kernel(proposals[proposal_index].shot, proposals[sample.proposal_index].shot) for sample in samples]
    total_weight = sum(weights)
    if total_weight <= 1e-12:
        return {"effectiveCount": 0.0, "mean": 0.0, "variance": 0.0, "standardError": math.inf}
    mean = sum(weight * sample.terminal_score for weight, sample in zip(weights, samples)) / total_weight
    variance = sum(weight * (sample.terminal_score - mean) ** 2 for weight, sample in zip(weights, samples)) / total_weight
    # Correlated kernel weights reduce usable sample size.  Kish's effective N
    # prevents a broad kernel from pretending it has many independent rollouts.
    effective_count = total_weight * total_weight / sum(weight * weight for weight in weights)
    standard_error = math.sqrt(variance / max(effective_count, 1.0))
    return {
        "effectiveCount": effective_count,
        "mean": mean,
        "variance": variance,
        "standardError": standard_error,
    }


def direct_histogram(samples: Sequence[Sample], proposal_index: int) -> dict[str, int]:
    values = [sample.terminal_score for sample in samples if sample.proposal_index == proposal_index]
    return {str(score): values.count(score) for score in SCORE_BINS}


def reset_worker(worker: StrictCurlingEnd, states: Sequence[dict[str, Any]], shot_number: int, seed: int) -> None:
    positions, yaws = state_snapshot(states)
    worker.scene.reset_positions(positions, yaw_overrides=yaws)
    worker.shot_number = int(shot_number)
    worker.seed = int(seed)


def rollout_to_end(
    worker: StrictCurlingEnd,
    states: Sequence[dict[str, Any]],
    shot_number: int,
    root_team: int,
    action: Sequence[float],
    episode_seed: int,
) -> tuple[int, int]:
    """Execute one candidate, then alternating fixed-policy throws to a terminal score."""

    reset_worker(worker, states, shot_number, episode_seed)
    result = worker.play(action)
    current_states = result["states"]
    continuation_shot_count = 0
    while worker.shot_number < STONE_COUNT:
        continuation = scripted_continuation_shot(current_states, worker.shot_number)
        current_states = worker.play(continuation)["states"]
        continuation_shot_count += 1
    return int(team_score(score_board(current_states), root_team)), continuation_shot_count


def pick_next_proposal(
    proposals: Sequence[Proposal],
    samples: Sequence[Sample],
    exploration: float,
    initial_proposal_count: int,
    initial_samples_per_template: int,
) -> int:
    # Force every template to receive one direct outcome before relying on
    # kernel sharing.  This avoids a bad initial tactic being excluded merely
    # because it lies near a different tactic in parameter space.
    direct_counts = [sum(sample.proposal_index == index for sample in samples) for index in range(len(proposals))]
    for index in range(initial_proposal_count):
        if direct_counts[index] < initial_samples_per_template:
            return index

    log_total = math.log(len(samples) + 1.0)
    best_index = 0
    best_ucb = -math.inf
    for index in range(len(proposals)):
        stats = kernel_statistics(proposals, samples, index)
        effective_count = max(float(stats["effectiveCount"]), 1e-6)
        ucb = float(stats["mean"]) + exploration * math.sqrt(log_total / effective_count)
        if ucb > best_ucb:
            best_ucb = ucb
            best_index = index
    return best_index


def add_local_expansion(
    proposals: list[Proposal],
    samples: Sequence[Sample],
    rng: random.Random,
    confidence_z: float,
) -> None:
    """Add one unexplored continuous neighbour around the current best LCB."""

    if not samples:
        return
    ranked: list[tuple[float, int]] = []
    for index in range(len(proposals)):
        stats = kernel_statistics(proposals, samples, index)
        lcb = float(stats["mean"]) - confidence_z * float(stats["standardError"])
        ranked.append((lcb, index))
    _, parent_index = max(ranked)
    parent = proposals[parent_index]
    for _ in range(12):
        shot = clamp_shot(
            (
                parent.shot[0] + rng.gauss(0.0, 0.08),
                parent.shot[1] + rng.gauss(0.0, 0.10),
                parent.shot[2] + rng.gauss(0.0, 0.50),
            )
        )
        if all(sum((shot[i] - existing.shot[i]) ** 2 for i in range(3)) > 1e-8 for existing in proposals):
            proposals.append(Proposal(tactic=parent.tactic, shot=shot, origin=f"local_expand_from_{parent_index}"))
            return


def search_root(
    *,
    states: Sequence[dict[str, Any]],
    shot_number: int,
    seed: int,
    sample_budget: int,
    confidence_z: float,
    exploration: float,
    expand_every: int,
    initial_samples_per_template: int,
    target_rollouts: int,
    max_candidates: int = 20,
    worker: StrictCurlingEnd,
) -> dict[str, Any]:
    team = shot_number % 2
    proposals = initial_proposals(states, team)
    initial_proposal_count = len(proposals)
    samples: list[Sample] = []
    rng = random.Random(seed ^ 0xC0FFEE)
    for sample_index in range(sample_budget):
        if (
            sample_index >= initial_proposal_count * initial_samples_per_template
            and expand_every > 0
            and sample_index % expand_every == 0
            and (max_candidates <= 0 or len(proposals) < max_candidates)
        ):
            add_local_expansion(proposals, samples, rng, confidence_z)
        proposal_index = pick_next_proposal(
            proposals,
            samples,
            exploration,
            initial_proposal_count,
            initial_samples_per_template,
        )
        terminal_score, continuation_shot_count = rollout_to_end(
            worker,
            states,
            shot_number,
            team,
            proposals[proposal_index].shot,
            seed + sample_index * 10_007,
        )
        samples.append(Sample(proposal_index, seed + sample_index * 10_007, terminal_score, continuation_shot_count))

    # Search first chooses a root action.  It then receives fresh, independent
    # terminal rollouts so the supervised value target is a real distribution,
    # not merely whichever one-off outcomes happened to drive exploration.
    preliminary = [
        (
            kernel_statistics(proposals, samples, index)["mean"]
            - confidence_z * kernel_statistics(proposals, samples, index)["standardError"],
            index,
        )
        for index in range(len(proposals))
    ]
    selected_original_index = max(preliminary)[1]
    for target_index in range(target_rollouts):
        episode_seed = seed + (sample_budget + target_index) * 10_007
        terminal_score, continuation_shot_count = rollout_to_end(
            worker,
            states,
            shot_number,
            team,
            proposals[selected_original_index].shot,
            episode_seed,
        )
        samples.append(Sample(selected_original_index, episode_seed, terminal_score, continuation_shot_count))

    rows: list[dict[str, Any]] = []
    for index, proposal in enumerate(proposals):
        stats = kernel_statistics(proposals, samples, index)
        direct_count = sum(sample.proposal_index == index for sample in samples)
        lcb = float(stats["mean"]) - confidence_z * float(stats["standardError"])
        rows.append(
            {
                "index": index,
                "tactic": proposal.tactic,
                "origin": proposal.origin,
                "action": list(proposal.shot),
                "directEvaluationCount": direct_count,
                "directTerminalScoreHistogram": direct_histogram(samples, index),
                "effectiveEvaluationCount": float(stats["effectiveCount"]),
                "kernelMeanEndScoreForSelf": float(stats["mean"]),
                "kernelVarianceEndScore": float(stats["variance"]),
                "kernelStandardError": float(stats["standardError"]),
                "lowerConfidenceBound": lcb,
            }
        )
    rows.sort(key=lambda row: (float(row["lowerConfidenceBound"]), float(row["kernelMeanEndScoreForSelf"])), reverse=True)
    total_effective = sum(max(0.0, float(row["effectiveEvaluationCount"])) for row in rows)
    for row in rows:
        row["searchWeight"] = float(row["effectiveEvaluationCount"]) / total_effective if total_effective else 0.0
    # Do not silently change the teacher action after collecting its target
    # distribution.  ``selected`` is the action chosen by the search phase;
    # its post-search rollouts are evaluation data, not a second search round.
    selected = next(row for row in rows if int(row["index"]) == selected_original_index)
    target_histogram = {str(score): 0 for score in SCORE_BINS}
    for sample in samples:
        if sample.proposal_index == selected_original_index:
            target_histogram[str(sample.terminal_score)] += 1
    return {
        "state": canonical_state(states, shot_number, team),
        "search": {
            "method": "root_kernel_ucb_late_end_v1",
            "scoreView": "terminal end score from current shooter perspective",
            "continuationPolicy": "scripted_continuation_v1",
            "kernelBandwidth": {"v0": 0.12, "h0": 0.16, "w0": 0.80},
            "confidenceZ": confidence_z,
            "exploration": exploration,
            "sampleBudget": sample_budget,
            "initialSamplesPerTemplate": initial_samples_per_template,
            "targetRollouts": target_rollouts,
            "samples": [
                {
                    "proposalIndex": sample.proposal_index,
                    "episodeSeed": sample.episode_seed,
                    "terminalEndScoreForSelf": sample.terminal_score,
                    "continuationShotCount": sample.continuation_shot_count,
                }
                for sample in samples
            ],
            "candidates": rows,
            "selected": selected,
            "targetScoreDistributionDirect": target_histogram,
        },
    }


def prelude_to_search(master: StrictCurlingEnd, first_search_shot: int, rng: random.Random) -> list[dict[str, Any]]:
    states = master.reset()
    while master.shot_number < first_search_shot:
        team = master.shot_number % 2
        # A broad deterministic-seeded prelude gives P0.1 different late-end
        # boards without pretending this is a learned opening policy.
        tactic_index = rng.randrange(len(TACTICS))
        states = master.play(tactic_shot(tactic_index, states, team))["states"]
    return states


def _collection_config(args: argparse.Namespace) -> dict[str, Any]:
    """Pickle-safe immutable configuration for spawned worker processes."""

    return {
        "seed": int(args.seed),
        "firstSearchShot": int(args.first_search_shot),
        "searchSamples": int(args.search_samples),
        "confidenceZ": float(args.confidence_z),
        "exploration": float(args.exploration),
        "expandEvery": int(args.expand_every),
        "initialSamplesPerTemplate": int(args.initial_samples_per_template),
        "targetRollouts": int(args.target_rollouts),
        "maxCandidates": int(args.max_candidates),
    }


def _collect_one_game(
    game_index: int,
    config: dict[str, Any],
    master: StrictCurlingEnd,
    worker: StrictCurlingEnd,
) -> dict[str, Any]:
    """Collect one independent end using pre-existing persistent scenes."""

    started = time.perf_counter()
    game_seed = int(config["seed"]) + game_index * 300_007
    master.seed = game_seed
    states = prelude_to_search(master, int(config["firstSearchShot"]), random.Random(game_seed))
    decisions: list[dict[str, Any]] = []
    while master.shot_number < STONE_COUNT:
        shot_number = master.shot_number
        decision = search_root(
            states=states,
            shot_number=shot_number,
            seed=game_seed + shot_number * 20_011,
            sample_budget=int(config["searchSamples"]),
            confidence_z=float(config["confidenceZ"]),
            exploration=float(config["exploration"]),
            expand_every=int(config["expandEvery"]),
            initial_samples_per_template=int(config["initialSamplesPerTemplate"]),
            target_rollouts=int(config["targetRollouts"]),
            max_candidates=int(config["maxCandidates"]),
            worker=worker,
        )
        selected = decision["search"]["selected"]
        executed = master.play(selected["action"])
        decision["execution"] = {
            "contact": bool(executed["contact"]),
            "cleared": list(executed["cleared"]),
            "temporaryBoardScoreFirst": score_board(executed["states"]),
        }
        decisions.append(decision)
        states = executed["states"]
    return {
        "game": game_index + 1,
        "gameSeed": game_seed,
        "preludePolicy": "seeded_tactic_template_v1",
        "finalScoreFirst": score_board(states),
        "decisions": decisions,
        "collectionTiming": {
            "workerWallSeconds": time.perf_counter() - started,
            "decisionCount": len(decisions),
            "terminalPathsPerDecision": int(config["searchSamples"]) + int(config["targetRollouts"]),
        },
    }


def _init_collection_worker() -> None:
    """Build native scenes once per spawned process, rather than once per end."""

    global _COLLECTION_MASTER, _COLLECTION_ROLLOUT
    install_bundled_pyphysx()
    _COLLECTION_MASTER = StrictCurlingEnd(seed=0, training_fast=True)
    _COLLECTION_ROLLOUT = StrictCurlingEnd(seed=1, training_fast=True)


def _collect_game_in_worker(task: tuple[int, dict[str, Any]]) -> dict[str, Any]:
    global _COLLECTION_MASTER, _COLLECTION_ROLLOUT
    game_index, config = task
    if _COLLECTION_MASTER is None or _COLLECTION_ROLLOUT is None:
        _init_collection_worker()
    return _collect_one_game(game_index, config, _COLLECTION_MASTER, _COLLECTION_ROLLOUT)


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def _load_completed_part(path: Path, expected_game: int, expected_config: dict[str, Any]) -> dict[str, Any] | None:
    """Load only a checkpoint created with exactly this collection config.

    A same-named checkpoint directory must never silently mix a low-budget
    smoke collection with a later high-budget teacher run.  The game number on
    its own is insufficient because all runs start numbering at one.
    """

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        record = payload.get("game")
        if (
            payload.get("schema") == "strict_p0_kernel_late_end_part_v1"
            and payload.get("config") == expected_config
            and record
            and record.get("game") == expected_game
        ):
            return record
    except (OSError, ValueError, TypeError):
        pass
    return None


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.games < 1 or args.search_samples < 1 or args.initial_samples_per_template < 1 or args.target_rollouts < 1:
        raise ValueError("--games, --search-samples, --initial-samples-per-template and --target-rollouts must be positive")
    if not 0 <= args.first_search_shot < STONE_COUNT:
        raise ValueError("--first-search-shot must be within 0..15")
    # Terminal score labels are affordable and unambiguous only in the last
    # five shots.  Early game expansion requires a separately validated value
    # estimator and is intentionally rejected here.
    if args.first_search_shot < STONE_COUNT - 5:
        raise ValueError("P0.1 requires --first-search-shot >= 11 so every rollout reaches a real end score")
    if args.search_samples < len(TACTICS) * args.initial_samples_per_template:
        raise ValueError("--search-samples must cover every initial tactic at least --initial-samples-per-template times")
    if args.workers < 1:
        raise ValueError("--workers must be positive")

    config = _collection_config(args)
    checkpoint_dir = Path(args.checkpoint_dir)
    games_by_index: dict[int, dict[str, Any]] = {}
    pending: list[int] = []
    for game_index in range(args.games):
        part_path = checkpoint_dir / f"end_{game_index + 1:05d}.json"
        completed = _load_completed_part(part_path, game_index + 1, config) if args.resume else None
        if completed is None:
            pending.append(game_index)
        else:
            games_by_index[game_index] = completed
    if games_by_index:
        print(f"P0.1 恢复：复用 {len(games_by_index)} 个已完成 end。", flush=True)

    def save_completed(game: dict[str, Any]) -> None:
        game_index = int(game["game"]) - 1
        games_by_index[game_index] = game
        part_path = checkpoint_dir / f"end_{game_index + 1:05d}.json"
        _write_json_atomic(
            part_path,
            {"schema": "strict_p0_kernel_late_end_part_v1", "config": config, "game": game},
        )
        print(
            f"P0.1 已保存 {game['game']:05d}/{args.games} | "
            f"终局先手得分 {game['finalScoreFirst']:+d} | "
            f"worker {game['collectionTiming']['workerWallSeconds']:.1f}s | checkpoint {part_path.name}",
            flush=True,
        )

    if args.workers == 1:
        _init_collection_worker()
        for game_index in pending:
            save_completed(_collect_game_in_worker((game_index, config)))
    elif pending:
        context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(
            max_workers=args.workers,
            mp_context=context,
            initializer=_init_collection_worker,
        ) as executor:
            futures = [executor.submit(_collect_game_in_worker, (game_index, config)) for game_index in pending]
            for future in as_completed(futures):
                save_completed(future.result())

    games = [games_by_index[index] for index in sorted(games_by_index)]

    report = {
        "schema": "strict_p0_kernel_late_end_teacher_v1",
        "trainingUsable": True,
        "scope": "non-sweeping; terminal-score labels only; final five shots of a single end; strict local PhysX",
        "warning": "Teacher values are against scripted_continuation_v1 until P2 opponent-pool search is implemented.",
        "collection": {
            "workers": int(args.workers),
            "checkpointDir": str(checkpoint_dir),
            "resume": bool(args.resume),
            "config": config,
        },
        "games": games,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    args = parse_args()
    report = run(args)
    count = sum(len(game["decisions"]) for game in report["games"])
    print(f"P0.1 完成：{count} 条终局标签写入 {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
