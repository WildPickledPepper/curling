"""Budgeted MADS-style inverse search over ``(v, h, w)``."""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional, Sequence, Tuple

from .contracts import ScoreResult, ShotContract, evaluate_contract
from .seeds import ShotSeed
from .simulator import SimulationResult
from .state import CanonicalState


@dataclass(frozen=True)
class SolveConstraints:
    v_range: Tuple[float, float] = (2.0, 10.0)
    h_range: Tuple[float, float] = (-2.23, 2.23)
    w_range: Tuple[float, float] = (-10.0, 10.0)
    max_simulations: int = 96
    rounds: int = 4
    # Legacy fields remain for configuration compatibility. The production
    # local solver no longer samples Gaussian candidates or updates elites.
    candidates_per_seed: int = 6
    elite_count: int = 3
    initial_std: Tuple[float, float, float] = (0.30, 0.08, 1.00)
    minimum_std: Tuple[float, float, float] = (0.02, 0.005, 0.05)
    mads_step: Tuple[float, float, float] = (0.12, 0.12, 1.60)
    mads_mesh_min: float = 1.0 / 16.0
    mads_mesh_growth: float = 1.5
    mads_branch_count: int = 2
    # Offline A/B can disable the narrow robust-refinement branch while
    # keeping every other seed, MADS and budget setting identical.
    enable_multiseed_refinement: bool = True
    robust_samples: int = 0
    robust_jitter: Tuple[float, float, float] = (0.04, 0.012, 0.25)
    # Environment robustness is distinct from release-parameter jitter. A
    # release is valid only when every configured ice/friction sample passes.
    physics_seed_count: int = 1
    physics_seed_stride: int = 104729
    physics_seed_base: int | None = None
    random_seed: int = 20260717

    def __post_init__(self) -> None:
        if self.max_simulations < 1 or self.rounds < 0 or self.candidates_per_seed < 1:
            raise ValueError("simulation budget, rounds, and candidates-per-seed must be positive")
        if self.elite_count < 1:
            raise ValueError("elite count must be positive")
        if self.physics_seed_count < 1 or self.physics_seed_stride < 1:
            raise ValueError("physics seed count and stride must be positive")
        if self.max_simulations < self.physics_seed_count:
            raise ValueError("max_simulations must cover one complete physics-seed set")
        for lower, upper in (self.v_range, self.h_range, self.w_range):
            if lower >= upper:
                raise ValueError("each parameter range must have lower < upper")
        if any(value <= 0.0 for value in self.mads_step):
            raise ValueError("MADS step sizes must be positive")
        if not 0.0 < self.mads_mesh_min < 1.0 or self.mads_mesh_growth <= 1.0:
            raise ValueError("invalid MADS mesh parameters")
        if self.mads_branch_count < 1:
            raise ValueError("MADS branch count must be positive")


@dataclass(frozen=True)
class CandidateEvaluation:
    source: str
    shot: Tuple[float, float, float]
    simulation: SimulationResult
    score: ScoreResult
    physics_seeds: Tuple[int, ...] = ()
    physics_scores: Tuple[ScoreResult, ...] = ()


@dataclass(frozen=True)
class SolveResult:
    shot: Tuple[float, float, float]
    score: float
    success: bool
    final_state: CanonicalState
    physical_final_state: CanonicalState
    simulation_count: int
    cache_hits: int
    robustness: float
    objective_details: Dict[str, float]
    source: str
    best_effort: bool
    reason: str
    diagnostics: Dict[str, object] = field(compare=False)
    successful_candidates: Tuple[CandidateEvaluation, ...] = field(
        default=(), compare=False, repr=False,
    )


class InverseSolver:
    """Reusable local inverse solver for a forward simulator with ``simulate``.

    A candidate is never accepted merely because its coordinate loss is low:
    :func:`evaluate_contract` puts complete tactical success ahead of score,
    safety, and placement refinement.
    """

    def __init__(self, simulator) -> None:
        self.simulator = simulator
        self._cache: Dict[Tuple[object, ...], CandidateEvaluation] = {}

    def close(self) -> None:
        self.clear_cache()
        close = getattr(self.simulator, "close", None)
        if callable(close):
            close()

    def clear_cache(self) -> None:
        """Discard board-specific search results while retaining the simulator."""

        self._cache.clear()

    @staticmethod
    def _contract_key(objective: ShotContract) -> str:
        # metadata can alter the seed solver, so it must be part of cache identity.
        return repr(objective)

    def _physics_seeds(self, constraints: SolveConstraints, *, shot_num: int) -> Tuple[int, ...]:
        base = (
            int(constraints.physics_seed_base)
            if constraints.physics_seed_base is not None
            else int(getattr(self.simulator, "seed", 0)) + int(shot_num) * 7919
        )
        return tuple(
            base + offset * int(constraints.physics_seed_stride)
            for offset in range(int(constraints.physics_seed_count))
        )

    @staticmethod
    def _clip(shot: Sequence[float], constraints: SolveConstraints) -> Tuple[float, float, float]:
        values = (
            min(max(float(shot[0]), constraints.v_range[0]), constraints.v_range[1]),
            min(max(float(shot[1]), constraints.h_range[0]), constraints.h_range[1]),
            min(max(float(shot[2]), constraints.w_range[0]), constraints.w_range[1]),
        )
        return tuple(round(value, 5) for value in values)

    def _evaluate(
        self,
        state: CanonicalState,
        objective: ShotContract,
        shot: Sequence[float],
        *,
        source: str,
        shot_num: int,
        constraints: SolveConstraints,
    ) -> Tuple[CandidateEvaluation, bool]:
        clipped = self._clip(shot, constraints)
        physics_version = str(getattr(self.simulator, "physics_version", type(self.simulator).__name__))
        physics_seeds = self._physics_seeds(constraints, shot_num=int(shot_num))
        key = (
            state.fingerprint(), int(shot_num), physics_version,
            self._contract_key(objective), physics_seeds, clipped,
        )
        cached = self._cache.get(key)
        if cached is not None:
            return cached, True
        simulations = tuple(
            self.simulator.simulate(
                state,
                clipped,
                shot_num=int(shot_num),
                physics_seed=physics_seed,
            )
            for physics_seed in physics_seeds
        )
        scores = tuple(
            evaluate_contract(
                state,
                simulation.final_state,
                objective,
                shooter_index=int(shot_num),
                rule_events=simulation.rule_events,
                first_contact_indices=simulation.first_contact_indices,
                collision_events=simulation.collision_events,
            )
            for simulation in simulations
        )
        worst_index = min(range(len(scores)), key=lambda index: scores[index].score)
        worst_score = scores[worst_index]
        all_success = all(score.success for score in scores)
        components = dict(worst_score.components)
        components.update({
            "physics_seed_count": float(len(physics_seeds)),
            "physics_seed_success_count": float(sum(score.success for score in scores)),
            "worst_physics_seed": float(physics_seeds[worst_index]),
        })
        score = ScoreResult(
            score=float(worst_score.score),
            success=bool(all_success),
            components=components,
            reason=(
                f"multi_seed_{worst_score.reason}"
                if all_success else f"multi_seed_unmet_{worst_score.reason}"
            ),
        )
        evaluation = CandidateEvaluation(
            source,
            clipped,
            simulations[worst_index],
            score,
            physics_seeds=physics_seeds,
            physics_scores=scores,
        )
        self._cache[key] = evaluation
        return evaluation, False

    def solve(
        self,
        state: CanonicalState,
        objective: ShotContract,
        initial_guesses: Sequence[ShotSeed],
        constraints: SolveConstraints = SolveConstraints(),
        *,
        shot_num: int,
    ) -> SolveResult:
        if not initial_guesses:
            raise ValueError("inverse solver requires at least one initial guess")
        if state.is_active(int(shot_num)):
            raise ValueError("shot_num slot is already occupied on the supplied board")
        simulations = 0
        cache_hits = 0
        single_seed_evaluations: List[CandidateEvaluation] = []
        full_seed_evaluations: List[CandidateEvaluation] = []
        full_seed_by_shot: Dict[Tuple[float, float, float], CandidateEvaluation] = {}
        seed_cost = int(constraints.physics_seed_count)
        # MADS uses one seed to navigate the locally smooth part of a basin,
        # then spends the reserved multi-seed calls only to certify a promising
        # release. This is the same budget shape used by the main solver.
        exploration_constraints = replace(constraints, physics_seed_count=1)
        exploration_budget = max(0, int(constraints.max_simulations) - seed_cost)

        def explore(shot: Sequence[float], source: str) -> Optional[CandidateEvaluation]:
            nonlocal simulations, cache_hits
            if simulations + 1 > exploration_budget:
                return None
            evaluation, cached = self._evaluate(
                state, objective, shot, source=source, shot_num=shot_num,
                constraints=exploration_constraints,
            )
            cache_hits += int(cached)
            simulations += int(not cached)
            single_seed_evaluations.append(evaluation)
            return evaluation

        def certify_shot(shot: Sequence[float], source: str) -> Optional[CandidateEvaluation]:
            nonlocal simulations, cache_hits
            clipped = self._clip(shot, constraints)
            key = tuple(float(value) for value in clipped)
            prior = full_seed_by_shot.get(key)
            if prior is not None:
                return prior
            if simulations + seed_cost > int(constraints.max_simulations):
                return None
            verified, cached = self._evaluate(
                state, objective, clipped, source=source,
                shot_num=shot_num, constraints=constraints,
            )
            cache_hits += int(cached)
            simulations += seed_cost * int(not cached)
            full_seed_evaluations.append(verified)
            full_seed_by_shot[key] = verified
            return verified

        def certify(evaluation: CandidateEvaluation) -> Optional[CandidateEvaluation]:
            return certify_shot(evaluation.shot, evaluation.source)

        if exploration_budget < 1:
            # ``max_simulations == physics_seed_count`` is a valid public
            # configuration: there is room for exactly one complete strict
            # certification but not for a single-seed exploration plus one.
            seed = initial_guesses[0]
            evaluation, cached = self._evaluate(
                state, objective, self._clip(seed.shot, constraints), source=str(seed.source),
                shot_num=shot_num, constraints=constraints,
            )
            cache_hits += int(cached)
            simulations += seed_cost * int(not cached)
            single_seed_evaluations.append(evaluation)
            full_seed_evaluations.append(evaluation)
            full_seed_by_shot[tuple(float(value) for value in evaluation.shot)] = evaluation
        else:
            for seed in initial_guesses:
                shot = self._clip(seed.shot, constraints)
                if simulations + 1 > exploration_budget:
                    break
                explore(shot, str(seed.source))

        if not single_seed_evaluations:
            raise RuntimeError("simulation budget exhausted before a candidate was evaluated")

        def directions(iteration: int) -> Tuple[Tuple[float, float, float], ...]:
            phase = (int(iteration) + 1) * 2.399963229728653
            diagonal = (
                math.cos(phase), math.sin(phase), math.cos(phase * 0.6180339887498948),
            )
            length = max(math.sqrt(sum(value * value for value in diagonal)), 1.0e-12)
            diagonal = tuple(value / length for value in diagonal)
            return (
                diagonal, tuple(-value for value in diagonal),
                (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0), (0.0, -1.0, 0.0),
                (0.0, 0.0, 1.0), (0.0, 0.0, -1.0),
            )

        # This expensive path is deliberately narrow.  It is not a second
        # search for ordinary failures: it is entered only after a release
        # satisfies the tactical contract on the navigation seed but fails
        # the real all-physics-seed certification.  In that situation the
        # main planner's smaller all-seed MADS can move from a fragile basin
        # to a nearby robust one without opening another global search.
        multiseed_refinement_triggered = False
        multiseed_refinement_iterations = 0

        def refine_multiseed(
            start: CandidateEvaluation,
        ) -> CandidateEvaluation:
            nonlocal multiseed_refinement_iterations
            current = start
            mesh = 1.0
            for iteration in range(int(constraints.rounds)):
                if current.score.success or simulations + seed_cost > int(constraints.max_simulations):
                    break
                best_trial = current
                for direction in directions(iteration):
                    if simulations + seed_cost > int(constraints.max_simulations):
                        break
                    proposal = tuple(
                        float(current.shot[index])
                        + mesh * (0.04, 0.04, 0.60)[index] * float(direction[index])
                        for index in range(3)
                    )
                    evaluation = certify_shot(proposal, current.source)
                    if evaluation is not None and evaluation.score.score > best_trial.score.score:
                        best_trial = evaluation
                multiseed_refinement_iterations += 1
                if best_trial.score.score > current.score.score:
                    current = best_trial
                    mesh = min(1.0, mesh * float(constraints.mads_mesh_growth))
                else:
                    mesh *= 0.5
                    if mesh < float(constraints.mads_mesh_min):
                        break
            return current

        branches = [
            {"current": item, "mesh": 1.0}
            for item in sorted(single_seed_evaluations, key=lambda item: item.score.score, reverse=True)[
                :min(int(constraints.mads_branch_count), len(single_seed_evaluations))
            ]
        ]
        mads_iterations = 0
        certified_success: CandidateEvaluation | None = None
        for iteration in range(int(constraints.rounds)):
            exhausted = False
            for branch in branches:
                current = branch["current"]
                if current.score.success:
                    verified = certify(current)
                    if verified is not None and verified.score.success:
                        certified_success = verified
                        exhausted = True
                        break
                    if (
                        verified is not None
                        and bool(constraints.enable_multiseed_refinement)
                        and int(constraints.physics_seed_count) > 1
                    ):
                        multiseed_refinement_triggered = True
                        refined = refine_multiseed(verified)
                        if refined.score.success:
                            certified_success = refined
                            exhausted = True
                            break
                if simulations + 1 > exploration_budget:
                    exhausted = True
                    break
                best_trial = current
                for direction in directions(iteration):
                    if simulations + 1 > exploration_budget:
                        exhausted = True
                        break
                    proposal = tuple(
                        float(current.shot[index])
                        + float(branch["mesh"]) * float(constraints.mads_step[index]) * float(direction[index])
                        for index in range(3)
                    )
                    evaluation = explore(proposal, current.source)
                    if evaluation is not None and evaluation.score.score > best_trial.score.score:
                        best_trial = evaluation
                mads_iterations += 1
                if best_trial.score.score > current.score.score:
                    branch["current"] = best_trial
                    branch["mesh"] = min(1.0, float(branch["mesh"]) * float(constraints.mads_mesh_growth))
                else:
                    branch["mesh"] = float(branch["mesh"]) * 0.5
            if exhausted or all(float(branch["mesh"]) < float(constraints.mads_mesh_min) for branch in branches):
                break

        current = max((branch["current"] for branch in branches), key=lambda item: item.score.score)

        # A single-seed success is not a submitted result. Certify the best
        # local release across every configured physical seed before returning.
        if certified_success is None and tuple(float(value) for value in current.shot) not in full_seed_by_shot:
            certify(current)
        if certified_success is not None:
            best = certified_success
        elif full_seed_evaluations:
            best = max(full_seed_evaluations, key=lambda item: item.score.score)
        else:
            best = current
        # Preserve a small ranked set of contract-valid releases for the
        # caller's higher-level role/response planner. The solver itself still
        # optimizes the tactical contract; selection among these releases is a
        # separate concern and must never consider a contract failure.
        successful_candidates = tuple(sorted(
            (item for item in full_seed_evaluations if item.score.success),
            key=lambda item: item.score.score,
            reverse=True,
        ))
        # Random jitter probes belonged to the old random-search path. The
        # replacement remains deterministic; multi-seed certification is its
        # robustness signal.
        robustness = float(best.score.success)
        best_effort = not best.score.success
        reason = best.score.reason if not best_effort else "best_effort_" + best.score.reason
        return SolveResult(
            shot=best.shot,
            score=best.score.score,
            success=best.score.success,
            final_state=best.simulation.final_state,
            physical_final_state=best.simulation.physical_final_state,
            simulation_count=simulations,
            cache_hits=cache_hits,
            robustness=robustness,
            objective_details=dict(best.score.components),
            source=best.source,
            best_effort=best_effort,
            reason=reason,
            diagnostics={
                "candidate_count": len(single_seed_evaluations) + len(full_seed_evaluations),
                "search_mode": "mads_single_seed_then_conditional_multi_seed_refine",
                "mads_iterations": int(mads_iterations),
                "multiseed_refinement_triggered": bool(multiseed_refinement_triggered),
                "multiseed_refinement_iterations": int(multiseed_refinement_iterations),
                "mads_final_mesh": min(float(branch["mesh"]) for branch in branches),
                "mads_branch_count": len(branches),
                "mads_single_seed_candidates": len(single_seed_evaluations),
                "mads_multi_seed_certifications": len(full_seed_evaluations),
                "first_contact_indices": best.simulation.first_contact_indices,
                "cleared_indices": best.simulation.cleared_indices,
                "rule_events": best.simulation.rule_events,
                "settled": best.simulation.settled,
                "replay": best.simulation.replay,
                "trajectory": best.simulation.trajectory,
                "collision_events": best.simulation.collision_events,
                "physics_seeds": best.physics_seeds,
                "physics_seed_scores": [float(score.score) for score in best.physics_scores],
                "physics_seed_successes": [bool(score.success) for score in best.physics_scores],
                "physics_seed_loss_budget_ok": [
                    bool(score.components.get("loss_budget_ok", 1.0))
                    for score in best.physics_scores
                ],
                "physics_seed_board_shape_ok": [
                    bool(score.components.get("board_shape_ok", 1.0))
                    for score in best.physics_scores
                ],
                "physics_version": best.simulation.physics_version,
            },
            successful_candidates=successful_candidates,
        )
