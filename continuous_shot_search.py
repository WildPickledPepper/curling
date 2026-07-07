# -*- coding: utf-8 -*-
"""Small-budget continuous shot refinement for the local curling simulator."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import torch

from curling_sweep import NO_SWEEP_ACTIONS, estimate_sweep_distance
from fast_curling_env import (
    HOUSE_R,
    HOUSE_X,
    HOUSE_Y,
    STONE_R,
    FastCurlingEnv,
    Shot,
    Stone,
    SweepShot,
    clamp,
    distance,
    split_shot,
)
from tactic_dqn_robot import ACTIONS, make_state_vector
from train_search_distill import PolicyValueNet, rollout_shot, valid_indices


TACTIC_GROUPS: Dict[str, str] = {
    "draw_center": "draw",
    "occupy": "draw",
    "middle_in_center": "draw",
    "curl_left": "curl_draw",
    "curl_right": "curl_draw",
    "guard_left": "guard",
    "guard_right": "guard",
    "defense": "guard",
    "freeze": "freeze",
    "take_out": "takeout",
    "hit_roll": "takeout",
    "clear": "takeout",
    "double_hit_gote": "takeout",
    "push_in": "raise_push",
    "push_in_14": "raise_push",
    "defense_push_in": "raise_push",
}


@dataclass
class CandidateStats:
    shot: SweepShot
    mean_score: float
    std_score: float
    samples: int


@dataclass
class ShotPlan:
    action_index: int
    action_name: str
    shot: Shot
    sweep: float
    mean_score: float
    std_score: float
    explanation: str = ""
    candidates: List[CandidateStats] = field(default_factory=list)

    def swept_shot(self) -> SweepShot:
        return (self.shot[0], self.shot[1], self.shot[2], self.sweep)


def is_our_turn(shot_num: int, player_is_init: bool) -> bool:
    return (shot_num % 2 == 0) == player_is_init


def legal_options_for_player(env: FastCurlingEnv, player_is_init: bool) -> List[Optional[Shot]]:
    is_init = 0 if player_is_init else 1
    return [action.try_shot(env.state_list(), is_init, env.shot_num) for action in ACTIONS]


def score_for_player(env: FastCurlingEnv, player_is_init: bool) -> int:
    score = env.end_score()
    return score if player_is_init else -score


def own_shot_index(shot_num: int) -> int:
    return max(1, min(8, shot_num // 2 + 1))


def strategy_phase(shot_num: int, player_is_init: bool) -> str:
    own_idx = own_shot_index(shot_num)
    if own_idx <= 2:
        return "early"
    if own_idx <= 5:
        return "middle"
    if own_idx <= 7:
        return "late_setup"
    return "hammer" if not player_is_init else "final_without_hammer"


def tactic_group(action_name: str) -> str:
    return TACTIC_GROUPS.get(action_name, "other")


def _stone_is_ours(index: int, player_is_init: bool) -> bool:
    return (index % 2 == 0) == player_is_init


def board_context(env: FastCurlingEnv, player_is_init: bool) -> Dict[str, float]:
    own_best = float("inf")
    enemy_best = float("inf")
    enemy_button = 0
    enemy_guards = 0
    center_guards = 0
    for idx, stone in enumerate(env.stones):
        if not stone.in_play:
            continue
        d = distance(stone.x, stone.y, HOUSE_X, HOUSE_Y)
        if _stone_is_ours(idx, player_is_init):
            own_best = min(own_best, d)
            continue
        enemy_best = min(enemy_best, d)
        if d <= 0.75:
            enemy_button += 1
        if HOUSE_Y + HOUSE_R < stone.y < 10.61:
            enemy_guards += 1
            if abs(stone.x - HOUSE_X) <= 0.55:
                center_guards += 1
    enemy_shot = enemy_best <= HOUSE_R + STONE_R and enemy_best < own_best
    return {
        "own_best": own_best,
        "enemy_best": enemy_best,
        "enemy_shot": 1.0 if enemy_shot else 0.0,
        "enemy_button": float(enemy_button),
        "enemy_guards": float(enemy_guards),
        "center_guards": float(center_guards),
    }


def needs_offense(env: FastCurlingEnv, player_is_init: bool) -> bool:
    ctx = board_context(env, player_is_init)
    score = score_for_player(env, player_is_init)
    phase = strategy_phase(env.shot_num, player_is_init)
    return bool(
        ctx["enemy_shot"]
        or ctx["enemy_button"] > 0
        or score < 0
        or (phase in {"late_setup", "hammer", "final_without_hammer"} and score <= 0)
    )


def explain_tactic(env: FastCurlingEnv, action_name: str, player_is_init: bool) -> str:
    ctx = board_context(env, player_is_init)
    score = score_for_player(env, player_is_init)
    phase = strategy_phase(env.shot_num, player_is_init)
    group = tactic_group(action_name)
    reasons = [f"phase={phase}", f"score={score}"]
    if ctx["enemy_shot"]:
        reasons.append(f"enemy_shot={ctx['enemy_best']:.2f}m")
    if ctx["enemy_button"] > 0:
        reasons.append("enemy_button")
    if ctx["center_guards"] > 0:
        reasons.append(f"center_guards={int(ctx['center_guards'])}")
    if group == "takeout":
        reasons.append("intent=remove_or_roll")
    elif group == "raise_push":
        reasons.append("intent=raise_scoring_stone")
    elif group == "guard":
        reasons.append("intent=protect")
    else:
        reasons.append(f"intent={group}")
    return ";".join(reasons)


def strategy_prior_bonus(env: FastCurlingEnv, action_name: str, player_is_init: bool) -> float:
    """Small situational tactic prior used only for candidate ordering.

    The values are intentionally modest and dimensionless.  Callers multiply
    them by a strength in logit units, then continuous search still chooses the
    actual shot from simulated outcomes.
    """
    group = tactic_group(action_name)
    phase = strategy_phase(env.shot_num, player_is_init)
    score = score_for_player(env, player_is_init)
    bonus = 0.0

    if player_is_init:
        if phase == "early":
            bonus += {"draw": 0.30, "guard": 0.18, "curl_draw": 0.10, "takeout": -0.12}.get(group, 0.0)
        elif phase == "middle":
            bonus += {"guard": 0.18, "curl_draw": 0.14, "draw": 0.08, "freeze": 0.04}.get(group, 0.0)
        elif phase == "late_setup":
            bonus += {"guard": 0.16, "curl_draw": 0.16, "draw": 0.08, "freeze": 0.04}.get(group, 0.0)
        else:
            bonus += {"curl_draw": 0.20, "draw": 0.14, "guard": 0.06}.get(group, 0.0)
    else:
        if phase == "early":
            bonus += {"draw": 0.18, "takeout": 0.28, "curl_draw": 0.12, "freeze": 0.08, "guard": -0.08}.get(group, 0.0)
        elif phase == "middle":
            bonus += {"draw": 0.14, "curl_draw": 0.12, "guard": 0.10, "freeze": 0.08, "raise_push": 0.04}.get(group, 0.0)
        elif phase == "late_setup":
            bonus += {"draw": 0.18, "curl_draw": 0.16, "guard": 0.06, "freeze": 0.04}.get(group, 0.0)
        else:
            bonus += {"draw": 0.28, "curl_draw": 0.22, "raise_push": 0.08, "takeout": 0.06, "guard": -0.08}.get(group, 0.0)

    if score <= -2:
        bonus += {"draw": 0.12, "curl_draw": 0.14, "takeout": 0.14, "raise_push": 0.12, "freeze": 0.10, "guard": -0.14}.get(group, 0.0)
    elif score == -1:
        bonus += {"draw": 0.10, "curl_draw": 0.12, "takeout": 0.10, "freeze": 0.08, "raise_push": 0.06, "guard": -0.08}.get(group, 0.0)
    elif score == 0:
        bonus += {"draw": 0.10, "curl_draw": 0.06, "guard": 0.04}.get(group, 0.0)
    elif score == 1:
        bonus += {"guard": 0.16, "curl_draw": 0.06, "takeout": 0.06, "draw": -0.02}.get(group, 0.0)
    else:
        bonus += {"guard": 0.22, "takeout": 0.08, "curl_draw": 0.04, "draw": -0.04, "raise_push": -0.04}.get(group, 0.0)

    ctx = board_context(env, player_is_init)
    if ctx["enemy_shot"] or ctx["enemy_button"] > 0:
        bonus += {"takeout": 0.42, "freeze": 0.16, "raise_push": 0.10, "guard": -0.24, "draw": -0.08}.get(group, 0.0)
    if ctx["center_guards"] > 0 and phase != "early":
        bonus += {"takeout": 0.18, "raise_push": 0.12, "guard": -0.08}.get(group, 0.0)

    return bonus


def plan_selection_score(plan: ShotPlan, env: FastCurlingEnv, player_is_init: bool) -> float:
    score = plan.mean_score - 0.04 * plan.std_score
    group = tactic_group(plan.action_name)
    if needs_offense(env, player_is_init):
        score += {
            "takeout": 0.42,
            "raise_push": 0.24,
            "freeze": 0.16,
            "curl_draw": 0.02,
            "draw": -0.12,
            "guard": -0.18,
        }.get(group, 0.0)
    return score


def play_controlled_shot(env: FastCurlingEnv, shot: Sequence[float]) -> None:
    if env.shot_num >= 16:
        return
    env.place_stone(env.shot_num, shot)
    env.shot_num += 1


def play_uncontrolled_shot(env: FastCurlingEnv) -> None:
    if env.shot_num >= 16:
        return
    env.place_stone(env.shot_num, env.choose_opponent_shot())
    env.shot_num += 1


def finish_rollout_for_player(env: FastCurlingEnv, rng: random.Random, player_is_init: bool) -> int:
    while env.shot_num < 16:
        if is_our_turn(env.shot_num, player_is_init):
            play_controlled_shot(env, rollout_shot(env, rng))
        else:
            play_uncontrolled_shot(env)
    return score_for_player(env, player_is_init)


def env_from_position(position: Sequence[float], shot_num: int = 0, seed: Optional[int] = None) -> FastCurlingEnv:
    env = FastCurlingEnv(seed=seed)
    env.shot_num = int(max(0, min(15, shot_num)))
    for shot_idx in range(8):
        bx, by, rx, ry = position[shot_idx * 4 : shot_idx * 4 + 4]
        env.stones[shot_idx * 2] = Stone(float(bx), float(by), bool(bx or by))
        env.stones[shot_idx * 2 + 1] = Stone(float(rx), float(ry), bool(rx or ry))
    return env


def _unique_candidates(candidates: List[SweepShot]) -> List[SweepShot]:
    seen = set()
    unique: List[SweepShot] = []
    for shot in candidates:
        key = tuple(round(x, 3) for x in shot)
        if key in seen:
            continue
        seen.add(key)
        unique.append(shot)
    return unique


def _candidate_distance(candidate: SweepShot, center: SweepShot) -> float:
    cv, ch, cw, cs = center
    v, h, w, sweep = candidate
    return (
        ((v - cv) / 0.18) ** 2
        + ((h - ch) / 0.09) ** 2
        + ((w - cw) / 0.55) ** 2
        + ((sweep - cs) / 2.0) ** 2
    )


def _select_refinement_candidates(
    candidates: List[SweepShot],
    center: SweepShot,
    rng: random.Random,
    max_candidates: int,
) -> List[SweepShot]:
    unique = _unique_candidates(candidates)
    if len(unique) <= max_candidates:
        return unique

    ranked = sorted(unique, key=lambda shot: (_candidate_distance(shot, center), shot))
    core_count = min(len(ranked), max(1, int(max_candidates * 0.7)))
    selected = ranked[:core_count]
    selected_keys = {tuple(round(x, 3) for x in shot) for shot in selected}

    # Preserve some exploration so the local search can still escape a slightly
    # bad base tactic, but do not let arbitrary loop order drop the center.
    tail = [shot for shot in unique if tuple(round(x, 3) for x in shot) not in selected_keys]
    rng.shuffle(tail)
    selected.extend(tail[: max(0, max_candidates - len(selected))])
    return selected[:max_candidates]


def generate_refinement_candidates(
    base_shot: Sequence[float],
    action_name: str,
    rng: random.Random,
    max_candidates: int,
) -> List[SweepShot]:
    v0, h0, w0, _ = split_shot(base_shot)
    base_sweep = 0.0 if action_name in NO_SWEEP_ACTIONS else estimate_sweep_distance((v0, h0, w0), action_name)
    center = (
        clamp(v0, 0.0, 6.0),
        clamp(h0, -2.23, 2.23),
        clamp(w0, -15.7, 15.7),
        clamp(base_sweep, 0.0, 12.0),
    )

    if v0 >= 4.0 or action_name in NO_SWEEP_ACTIONS or action_name in {"push_in", "push_in_14"}:
        dv_values = [-0.15, 0.0, 0.15]
        dh_values = [-0.055, 0.0, 0.055]
        dw_values = [0.0]
        sweep_values = [0.0]
    else:
        dv_values = [-0.16, -0.08, 0.0, 0.08, 0.16]
        dh_values = [-0.09, -0.045, 0.0, 0.045, 0.09]
        dw_values = [-0.45, 0.0, 0.45] if abs(w0) > 0.2 else [0.0]
        sweep_values = sorted(
            {
                0.0,
                round(base_sweep, 3),
                round(clamp(base_sweep - 2.0, 0.0, 12.0), 3),
                round(clamp(base_sweep + 2.0, 0.0, 12.0), 3),
            }
        )

    candidates: List[SweepShot] = []
    for dv in dv_values:
        for dh in dh_values:
            for dw in dw_values:
                for sweep in sweep_values:
                    candidates.append(
                        (
                            clamp(v0 + dv, 0.0, 6.0),
                            clamp(h0 + dh, -2.23, 2.23),
                            clamp(w0 + dw, -15.7, 15.7),
                            clamp(sweep, 0.0, 12.0),
                        )
                    )

    while len(candidates) < max_candidates:
        speed_scale = 0.18 if v0 < 4.0 else 0.12
        h_scale = 0.10 if v0 < 4.0 else 0.06
        w_scale = 0.55 if abs(w0) > 0.2 else 0.12
        sweep_scale = 1.5 if base_sweep > 0 else 0.3
        candidates.append(
            (
                clamp(rng.gauss(v0, speed_scale), 0.0, 6.0),
                clamp(rng.gauss(h0, h_scale), -2.23, 2.23),
                clamp(rng.gauss(w0, w_scale), -15.7, 15.7),
                0.0
                if action_name in NO_SWEEP_ACTIONS
                else clamp(rng.gauss(base_sweep, sweep_scale), 0.0, 12.0),
            )
        )

    return _select_refinement_candidates(candidates, center, rng, max_candidates)


def evaluate_swept_shot(
    env: FastCurlingEnv,
    swept_shot: Sequence[float],
    rng: random.Random,
    rollouts: int,
    player_is_init: bool = True,
) -> CandidateStats:
    scores: List[int] = []
    for _ in range(max(1, rollouts)):
        sim = env.clone(seed=rng.randint(1, 2_000_000_000))
        play_controlled_shot(sim, swept_shot)
        scores.append(finish_rollout_for_player(sim, rng, player_is_init))
    return CandidateStats(
        shot=split_shot(swept_shot),
        mean_score=float(np.mean(scores)),
        std_score=float(np.std(scores)),
        samples=len(scores),
    )


def refine_shot(
    env: FastCurlingEnv,
    action_index: int,
    base_shot: Sequence[float],
    rng: random.Random,
    max_candidates: int = 24,
    rollouts: int = 3,
    player_is_init: bool = True,
) -> ShotPlan:
    action_name = ACTIONS[action_index].name if 0 <= action_index < len(ACTIONS) else "fallback"
    candidates = generate_refinement_candidates(base_shot, action_name, rng, max_candidates)
    stats = [evaluate_swept_shot(env, shot, rng, rollouts, player_is_init=player_is_init) for shot in candidates]
    best = max(stats, key=lambda item: item.mean_score - 0.04 * item.std_score)
    v0, h0, w0, sweep = best.shot
    return ShotPlan(
        action_index=action_index,
        action_name=action_name,
        shot=(v0, h0, w0),
        sweep=sweep,
        mean_score=best.mean_score,
        std_score=best.std_score,
        explanation=explain_tactic(env, action_name, player_is_init),
        candidates=sorted(stats, key=lambda item: item.mean_score - 0.04 * item.std_score, reverse=True)[:8],
    )


def scripted_index_for_player(
    env: FastCurlingEnv,
    options: Sequence[Optional[Shot]],
    player_is_init: bool = True,
) -> int:
    score = score_for_player(env, player_is_init)
    ctx = board_context(env, player_is_init)
    if needs_offense(env, player_is_init):
        priorities = [
            "take_out",
            "hit_roll",
            "double_hit_gote",
            "clear",
            "push_in",
            "push_in_14",
            "freeze" if ctx["enemy_shot"] else "draw_center",
            "draw_center",
            "curl_left",
            "curl_right",
        ]
    elif score > 0:
        priorities = [
            "guard_left",
            "guard_right",
            "defense",
            "freeze",
            "occupy",
            "draw_center",
            "curl_left",
            "curl_right",
        ]
    else:
        priorities = [
            "draw_center",
            "occupy",
            "curl_left",
            "curl_right",
            "guard_left",
            "guard_right",
            "take_out",
        ]
    name_to_idx = {action.name: idx for idx, action in enumerate(ACTIONS)}
    for name in priorities:
        idx = name_to_idx[name]
        if options[idx] is not None:
            return idx
    valid = valid_indices(options)
    return valid[0] if valid else 0


def model_action_order(
    model: PolicyValueNet,
    env: FastCurlingEnv,
    top_k: int,
    player_is_init: bool = True,
    strategy_gate_strength: float = 0.0,
) -> List[int]:
    options = legal_options_for_player(env, player_is_init)
    valid = valid_indices(options)
    if not valid:
        return [0]
    state = torch.tensor(
        make_state_vector(env.position(), env.shot_num, 0, 1, player_is_init, 0),
        dtype=torch.float32,
    ).unsqueeze(0)
    with torch.no_grad():
        logits, _ = model(state)
    scores = logits.squeeze(0).numpy()
    if strategy_gate_strength > 0:
        adjusted = {
            idx: float(scores[idx])
            + strategy_gate_strength * strategy_prior_bonus(env, ACTIONS[idx].name, player_is_init)
            for idx in valid
        }
        return sorted(valid, key=lambda idx: adjusted[idx], reverse=True)[: max(1, top_k)]
    return sorted(valid, key=lambda idx: float(scores[idx]), reverse=True)[: max(1, top_k)]


def choose_refined_plan(
    env: FastCurlingEnv,
    rng: random.Random,
    model: Optional[PolicyValueNet] = None,
    top_k: int = 3,
    max_candidates: int = 24,
    rollouts: int = 3,
    player_is_init: bool = True,
    strategy_gate_strength: float = 0.0,
) -> ShotPlan:
    options = legal_options_for_player(env, player_is_init)
    valid = valid_indices(options)
    if not valid:
        return refine_shot(
            env,
            0,
            (3.0, 0.0, 0.0),
            rng,
            max_candidates=max_candidates,
            rollouts=rollouts,
            player_is_init=player_is_init,
        )

    if model is None:
        order = [scripted_index_for_player(env, options, player_is_init)]
    else:
        order = model_action_order(
            model,
            env,
            top_k,
            player_is_init=player_is_init,
            strategy_gate_strength=strategy_gate_strength,
        )
        scripted = scripted_index_for_player(env, options, player_is_init)
        if scripted not in order:
            order.append(scripted)
    order = [idx for idx in order if idx in valid]
    if not order:
        order = [valid[0]]

    selected_order = order[: max(1, top_k)]
    if model is not None:
        scripted = scripted_index_for_player(env, options, player_is_init)
        if scripted in valid and scripted not in selected_order:
            if needs_offense(env, player_is_init):
                selected_order = [scripted] + selected_order[:-1]
            elif len(selected_order) >= max(1, top_k):
                selected_order[-1] = scripted
            else:
                selected_order.append(scripted)

    plans: List[ShotPlan] = []
    for idx in selected_order:
        shot = options[idx]
        if shot is None:
            continue
        plans.append(
            refine_shot(
                env,
                idx,
                shot,
                rng,
                max_candidates=max_candidates,
                rollouts=rollouts,
                player_is_init=player_is_init,
            )
        )
    if not plans:
        return refine_shot(
            env,
            0,
            (3.0, 0.0, 0.0),
            rng,
            max_candidates=max_candidates,
            rollouts=rollouts,
            player_is_init=player_is_init,
        )
    return max(plans, key=lambda plan: plan_selection_score(plan, env, player_is_init))
