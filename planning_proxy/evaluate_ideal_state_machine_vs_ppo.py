#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用“理想合同后壶面”而非路径规划器评估先手状态机。

我方每一手先由状态机给出 ``FirstPlayerPlan``，随后直接构造一个满足该
合同的静止壶面；不调用粗代理、MADS、严格反解或我方 PhysX 出手。PPO 仍
在该壶面上用原始物理模拟出手。因此结果隔离的是“状态机目标是否合理”，
不是“连续求解器是否能找到这颗球”。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import (  # noqa: E402
    HOUSE_X, HOUSE_Y, STONE_COUNT, StrictCurlingEnd, install_bundled_pyphysx, score_board,
)
from planning_proxy.competition_rules import free_guard_rule_violations  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import rule_board, state_position, state_snapshot  # noqa: E402
from planning_proxy.first_player_strategy import (  # noqa: E402
    EDGE_DEAD_RIGHT, FRONT_GUARD_LEFT, FRONT_GUARD_RIGHT, GUARD_TARGET, FirstPlayerPlan,
    plan_first_player_turn, score_strict_outcome,
)
DEFAULT_OUTPUT = ROOT / "planning_proxy" / "runs" / "ideal_state_machine_vs_ppo.json"
DEFAULT_TORCH_PYTHON = Path(r"D:\anaconda3\python.exe")
PPO_WORKER = ROOT / "training_research" / "opponents" / "teammate_ppo_worker.py"


class PPOWorker:
    """保持 Torch/PPO 与 CP39 PhysX 分离；每次请求严格顺序执行。"""

    def __init__(self, python: Path) -> None:
        if not python.is_file():
            raise FileNotFoundError(f"找不到带 Torch 的 PPO Python：{python}")
        self.process = subprocess.Popen(
            [str(python), str(PPO_WORKER)], cwd=str(ROOT), text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def choose(self, **request: Any) -> dict[str, Any]:
        if self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("PPO worker 标准输入输出不可用")
        self.process.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            stderr = "" if self.process.stderr is None else self.process.stderr.read()
            raise RuntimeError(f"PPO worker 已退出：{stderr}")
        response = json.loads(line)
        if not response.get("ok"):
            raise RuntimeError(f"PPO worker 推理失败：{response.get('error')}")
        return response

    def close(self) -> None:
        if self.process.poll() is None and self.process.stdin is not None:
            try:
                self.process.stdin.write('{"close":true}\n')
                self.process.stdin.flush()
            except BrokenPipeError:
                pass
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()


def strategy_board(states: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """将真实 slot 壶面转成状态机验收器可读的先手视角壶面。"""

    return [
        {
            "index": int(index),
            "owner": "self" if index % 2 == 0 else "opponent",
            "x": float(state["x"]),
            "y": float(state["y"]),
            "enabled": True,
        }
        for index, state in enumerate(states)
        if bool(state.get("enabled", False))
    ]


def candidate_targets(plan: FirstPlayerPlan) -> tuple[tuple[float, float], ...]:
    """合同可接受的出手壶目标区中心；防御形槽也属于候选。"""

    points: list[tuple[float, float]] = list(plan.target_points)
    for shape in plan.defence_shapes:
        points.extend(shape.active_targets)
    if not points:
        points.append((HOUSE_X, HOUSE_Y))
    return tuple(dict.fromkeys((float(x), float(y)) for x, y in points))


def complete_ideal_shape(
    final: list[dict[str, Any]], *, active_index: int, shape: Any | None,
) -> list[int]:
    """按防御形补齐既有壶角色；这是理想状态注入，不声称一手可这样搬壶。"""

    if shape is None:
        return []
    available = [
        index for index, state in enumerate(final)
        if index != int(active_index) and index % 2 == 0 and bool(state.get("enabled", False))
    ]
    moved: list[int] = []

    def place(point: tuple[float, float]) -> None:
        if not available:
            return
        index = available.pop(0)
        final[index].update(enabled=True, x=float(point[0]), y=float(point[1]), yaw=0.0)
        moved.append(index)

    # 优先补营内层；后续守壶/护门从其余旧壶中取。若壶数不够，最终合同
    # 仍会失败并被报告，而不会凭空增加己方壶。
    for offset in range(int(shape.required_inner_count)):
        place((HOUSE_X + (-0.38 if offset % 2 == 0 else 0.38), HOUSE_Y))
    if bool(shape.require_centre_anchor):
        place((HOUSE_X, HOUSE_Y))
    if bool(shape.require_centre_guard):
        place(GUARD_TARGET)
    if bool(shape.require_front_guard):
        place(FRONT_GUARD_LEFT[0])
    for gate in range(int(shape.required_side_gate_count)):
        place((FRONT_GUARD_LEFT if gate % 2 == 0 else FRONT_GUARD_RIGHT)[0])
    return moved


def apply_ideal_contract(
    states: Sequence[dict[str, Any]], plan: FirstPlayerPlan, active_index: int, *, choice: str,
) -> tuple[list[dict[str, Any]] | None, dict[str, Any]]:
    """仅按 G 的离散语义构造一个成功后壶面，不进行任何路径或物理求解。"""

    initial = strategy_board(states)
    target_index = plan.target_opponent_index
    attempts: list[dict[str, Any]] = []
    shaped_targets = [
        (target, shape)
        for shape in plan.defence_shapes
        for target in shape.active_targets
    ]
    if not shaped_targets:
        shaped_targets = [(target, None) for target in candidate_targets(plan)]
    if choice == "front_guard":
        shaped_targets.sort(key=lambda row: not bool(row[1] is not None and row[1].require_front_guard))
    elif choice == "inner_pair":
        shaped_targets.sort(key=lambda row: bool(row[1] is not None and row[1].require_front_guard))
    accepted: list[tuple[float, list[dict[str, Any]], dict[str, Any]]] = []
    for (target_x, target_y), shape in shaped_targets:
        final = [dict(state) for state in states]
        if target_index is not None:
            target = final[int(target_index)]
            if plan.opponent_action == "physical_clear":
                target.update(enabled=False, x=0.0, y=0.0)
            elif plan.opponent_action == "push_to_edge_dead":
                target.update(enabled=True, x=float(EDGE_DEAD_RIGHT[0] + 0.05), y=float(target["y"]))
            elif plan.opponent_action == "physical_displace":
                # 理想状态下只表达“目标确实被推进”。跨中线合同用镜像位置，
                # 其余合同取足以超过 20cm 的横向位移。
                if plan.phase == "displace_side_guard_across_centre_and_hold_outer_roll":
                    target["x"] = 2.0 * HOUSE_X - float(target["x"])
                else:
                    target["x"] = float(target["x"]) + 0.30
        final[int(active_index)] = {
            "enabled": True, "x": float(target_x), "y": float(target_y), "yaw": 0.0,
        }
        moved_existing = complete_ideal_shape(final, active_index=active_index, shape=shape)
        # K8 的 certified_for_last_reply 是原规划器里“先预测最后一壶”的
        # 内部闸门；本测试改由下一手真实 PPO 回应来验收，不能在回应发生前
        # 就把所有尚未预认证的防御形判作失败。
        evaluation_plan = (
            replace(
                plan,
                defence_shapes=tuple(replace(item, certified_for_last_reply=True) for item in plan.defence_shapes),
            )
            if plan.own_throw_number == 8 and plan.defence_shapes
            else plan
        )
        score, goal = score_strict_outcome(final, initial, int(active_index), evaluation_plan)
        attempts.append({
            "target": [target_x, target_y], "shape": None if shape is None else shape.name,
            "movedExistingOwnIndices": moved_existing, "score": float(score), "goal": bool(goal),
        })
        if goal:
            accepted.append((float(score), final, {
                "contractSatisfied": True,
                "idealActiveTarget": [target_x, target_y],
                "idealContractScore": float(score),
                "idealMovedExistingOwnIndices": moved_existing,
                "k8ReplyCertificationDeferredToActualPpo": bool(plan.own_throw_number == 8 and plan.defence_shapes),
                "attempts": attempts,
            }))
            if choice != "best_score":
                break
    if accepted:
        _score, final, detail = max(accepted, key=lambda row: row[0]) if choice == "best_score" else accepted[0]
        return final, detail
    return None, {"contractSatisfied": False, "attempts": attempts}


def run_game(*, game_index: int, seed: int, ppo: PPOWorker, choice: str) -> dict[str, Any]:
    environment = StrictCurlingEnd(seed=int(seed), training_fast=True)
    environment.reset()
    states = environment.states()
    trace: list[dict[str, Any]] = []
    invalid_contract: dict[str, Any] | None = None

    while environment.shot_number < STONE_COUNT:
        shot_index = int(environment.shot_number)
        before = state_snapshot(states)
        if shot_index % 2 == 0:
            proxy_board = [
                {"index": index, "owner": "self" if index % 2 == 0 else "opponent", "x": state["x"], "y": state["y"]}
                for index, state in enumerate(states) if bool(state.get("enabled", False))
            ]
            plan = plan_first_player_turn(proxy_board, shot_index)
            ideal_states, ideal_detail = apply_ideal_contract(states, plan, shot_index, choice=choice)
            if ideal_states is None:
                invalid_contract = {
                    "shot": shot_index + 1,
                    "plan": plan.to_json(),
                    "idealContract": ideal_detail,
                }
                trace.append({
                    "shot": shot_index + 1, "actor": "ideal_state_machine",
                    "stateBefore": before, "plan": plan.to_json(),
                    "idealContract": ideal_detail, "stateAfter": before,
                })
                break
            violations = free_guard_rule_violations(rule_board(states, 0), ideal_states, shot_index=shot_index)
            if violations:
                invalid_contract = {
                    "shot": shot_index + 1,
                    "plan": plan.to_json(),
                    "idealContract": ideal_detail,
                    "ruleViolations": violations,
                }
                break
            states = environment.restore_settled_states(ideal_states)
            # 我方理想状态转移等价于已经完成本手；PPO 的下一手仍由真实 PhysX
            # 执行，故显式推进 shot_number 而不调用 environment.play。
            environment.shot_number = shot_index + 1
            trace.append({
                "shot": shot_index + 1, "actor": "ideal_state_machine",
                "stateBefore": before, "plan": plan.to_json(), "idealContract": ideal_detail,
                "temporaryScoreFirst": int(score_board(states)), "stateAfter": state_snapshot(states),
            })
            continue

        decision = ppo.choose(
            position=state_position(states), player_is_init=False, shot_num=shot_index,
            end_score=int(score_board(states)), total_ends=1, current_player=1,
        )
        rules_before = rule_board(states, 1)
        result = environment.play(tuple(float(value) for value in decision["bestshot"]))
        states = result["states"]
        violations = free_guard_rule_violations(rules_before, states, shot_index=shot_index)
        if violations:
            states = environment.restore_settled_states(before)
        trace.append({
            "shot": shot_index + 1, "actor": "ppo", "bestshot": list(decision["bestshot"]),
            "tactic": decision["tactic"], "temporaryScoreFirst": int(score_board(states)),
            "ruleViolations": violations, "stateBefore": before, "stateAfter": state_snapshot(states),
        })

    final_score = int(score_board(states))
    return {
        "game": int(game_index), "seed": int(seed), "finalScoreFirst": final_score,
        "idealChoice": choice,
        "winner": "ideal_state_machine" if final_score > 0 else "ppo" if final_score < 0 else "draw",
        "completedEnd": invalid_contract is None and int(environment.shot_number) >= STONE_COUNT,
        "invalidContract": invalid_contract, "trace": trace,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260723)
    parser.add_argument("--games", type=int, default=4)
    parser.add_argument("--ideal-choice", choices=("inner_pair", "front_guard", "best_score"), default="inner_pair")
    parser.add_argument("--torch-python", type=Path, default=DEFAULT_TORCH_PYTHON)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.games < 1:
        raise SystemExit("--games 必须为正")
    install_bundled_pyphysx()
    ppo = PPOWorker(args.torch_python)
    try:
        games = [
            run_game(game_index=index + 1, seed=int(args.seed) + 100_003 * index, ppo=ppo, choice=args.ideal_choice)
            for index in range(args.games)
        ]
    finally:
        ppo.close()
    report = {
        "schema": "ideal_state_machine_vs_ppo_v1",
        "meaning": "我方每手直接注入满足 G_k 的理想后壶面；未运行我方路径规划器或 PhysX 出手。PPO 仍通过严格 PhysX 出手。",
        "idealChoice": args.ideal_choice,
        "games": games,
        "summary": {
            "wins": sum(game["winner"] == "ideal_state_machine" for game in games),
            "draws": sum(game["winner"] == "draw" for game in games),
            "losses": sum(game["winner"] == "ppo" for game in games),
            "invalidContracts": sum(game["invalidContract"] is not None for game in games),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
