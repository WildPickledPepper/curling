#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从已记录的真实 K5/K6/K7/K8 壶面恢复，比较候选状态边直到终局。

它只改变指定的先手手数（K5、K6、K7 或 K8）合同，其余先手回合和 PPO 均使用当前运行时
逻辑。它会连续重放来源报告的原始 BESTSHOT 前缀，并逐槽核验重放后的 x/y/yaw 与
来源 K5/K6/K7/K8 前壶面一致；这样保留 PhysX 场景的前序接触状态，而非只恢复坐标。
它是状态边的局部对照，不是全局胜率证明。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.examples.train_policy_tree_selfplay import install_bundled_pyphysx  # noqa: E402
from planning_proxy.evaluate_ideal_state_machine_vs_ppo import PPOWorker  # noqa: E402
import planning_proxy.evaluate_vs_teammate_ppo as evaluator  # noqa: E402
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer, append_log, run_game  # noqa: E402
from planning_proxy.first_player_strategy import (  # noqa: E402
    DefenceShape,
    FirstPlayerPlan,
    HOUSE_X,
    HOUSE_Y,
    HOUSE_R,
    STONE_R,
    HOUSE_PAIR_LEFT,
    HOUSE_PAIR_RIGHT,
    K3_GUARD_ALIGNED_RECOVERY_CORRIDOR,
    K7_CLEAR_TO_HISTORICAL_CONTROL,
    is_in_house,
)


class WorkerPPOOpponent:
    def __init__(self, python: Path) -> None:
        self._worker = PPOWorker(python)

    def choose(
        self,
        position: Sequence[float],
        *,
        player_is_init: bool,
        shot_num: int,
        end_score: int = 0,
        total_ends: int = 1,
        current_player: int = 0,
    ) -> Any:
        value = self._worker.choose(
            position=[float(item) for item in position],
            player_is_init=bool(player_is_init), shot_num=int(shot_num),
            end_score=int(end_score), total_ends=int(total_ends), current_player=int(current_player),
        )
        return SimpleNamespace(
            bestshot=tuple(float(item) for item in value["bestshot"]),
            tactic=str(value["tactic"]), action_id=int(value["action_id"]),
            policy_probability=float(value["policy_probability"]), value=float(value["value"]),
            fallback=bool(value["fallback"]),
        )

    def close(self) -> None:
        self._worker.close()


def _game_from_report(report: dict[str, Any]) -> dict[str, Any]:
    """读取两种历史报告格式中的唯一对局。"""

    # 旧续局报告使用 ``games:[...]``；当前 K6/K7 回放则直接把单局置于
    # ``game``。两者的 trace 协议相同，兼容读取只影响离线复盘入口。
    if isinstance(report.get("games"), list) and report["games"]:
        return report["games"][0]
    if isinstance(report.get("game"), dict):
        return report["game"]
    raise ValueError("source report does not contain games[0] or game")


def _resolve_parent_report(reference: str, current_path: Path) -> Path:
    """解析续局报告记录的上游路径，不猜测不存在的副本。"""

    raw = Path(reference)
    choices = (raw, ROOT / raw, current_path.parent / raw)
    for candidate in choices:
        if candidate.is_file():
            return candidate.resolve()
    raise ValueError(f"上游来源报告不存在：{reference}")


def _collect_physical_prefix(
    *, report: dict[str, Any], report_path: Path, start_shot: int,
    expected_seed: int, visited: set[Path],
) -> dict[int, dict[str, Any]]:
    """递归合并已核验的父前缀，再用当前续局的同手记录覆盖。

    早期续局报告只保存本段 `game.trace`，而其 `sourceReport` 指向完整上游
    对局。若直接忽略上游，K7 续局无法作为 K8 的严格物理前缀。这里仅拼接
    已实际执行的 BESTSHOT 记录；不从坐标推测动作，也不重放或修改状态机。
    """

    resolved = report_path.resolve()
    if resolved in visited:
        raise ValueError(f"来源报告形成循环：{resolved}")
    visited.add(resolved)
    game = _game_from_report(report)
    if int(game.get("seed", -1)) != int(expected_seed):
        raise ValueError(
            f"上游来源的对局种子不一致：期望 {expected_seed}，实际 {game.get('seed')!r}"
        )
    by_shot: dict[int, dict[str, Any]] = {}
    parent_ref = report.get("sourceReport")
    if isinstance(parent_ref, str) and parent_ref.strip():
        parent_path = _resolve_parent_report(parent_ref, report_path)
        parent_report = json.loads(parent_path.read_text(encoding="utf-8"))
        by_shot.update(_collect_physical_prefix(
            report=parent_report, report_path=parent_path, start_shot=start_shot,
            expected_seed=expected_seed, visited=visited,
        ))
    saved_prefix = report.get("strictPhysicalPrefixTrace", [])
    if isinstance(saved_prefix, list):
        for item in saved_prefix:
            if isinstance(item, dict) and 1 <= int(item.get("shot", 0)) <= int(start_shot):
                by_shot[int(item["shot"])] = item
    trace = game.get("trace", [])
    if not isinstance(trace, list):
        raise ValueError("source game.trace is not a list")
    for item in trace:
        if isinstance(item, dict) and 1 <= int(item.get("shot", 0)) <= int(start_shot):
            by_shot[int(item["shot"])] = item
    return by_shot


def source_before(path: Path, start_shot: int) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    report = json.loads(path.read_text(encoding="utf-8"))
    game = _game_from_report(report)
    turn = next(item for item in game["trace"] if int(item.get("shot", 0)) == int(start_shot) + 1)
    states = turn["stateBefore"]
    if not isinstance(states, list) or len(states) < 16:
        raise ValueError("source report does not contain a complete requested stateBefore")
    # 以最接近目标壶面的续局记录覆盖同手上游记录，避免使用已被 K5/K6/K7
    # 离线候选替换过的旧动作。
    prefix_by_shot = _collect_physical_prefix(
        report=report, report_path=path, start_shot=int(start_shot),
        expected_seed=int(game["seed"]), visited=set(),
    )
    prefix = [prefix_by_shot[shot] for shot in range(1, int(start_shot) + 1) if shot in prefix_by_shot]
    if len(prefix) != int(start_shot):
        raise ValueError("source report does not contain a complete BESTSHOT prefix")
    return report, game, states, prefix


def contract_gate_decision(path: Path, *, source_seed: int, start_shot: int) -> dict[str, Any]:
    """由合同无关固定批次决定离线 K7 门槛的实际候选合同。

    这不是生产状态机：输入批次须已经在当前壶面执行过严格三物理种子
    验收。门槛的作用只有一个——避免“仅清”在完整或 repair 仍存在时
    抢占其它状态边。后续整局仍按当前逻辑推进。
    """

    payload = json.loads(path.read_text(encoding="utf-8"))
    reports = payload.get("reports")
    if not isinstance(reports, list) or len(reports) != 1 or not isinstance(reports[0], dict):
        raise ValueError("合同门报告必须恰含一个固定候选批次")
    report = reports[0]
    if int(report.get("matchSeed", -1)) != int(source_seed) or int(report.get("shot", -1)) != int(start_shot) + 1:
        raise ValueError("合同门报告的 seed 或手数与续局输入不一致")
    contracts = report.get("contracts")
    if not isinstance(contracts, dict):
        raise ValueError("合同门报告缺少 contracts")

    def count(name: str) -> int:
        value = contracts.get(name)
        if not isinstance(value, dict):
            raise ValueError(f"合同门报告缺少 {name}")
        return int(value.get("acceptedCount", 0))

    full, repair, pure, trade = (
        count("完整防御"), count("repair"), count("仅清威胁"), count("一换一留营"),
    )
    selected = "pure_clear" if full == 0 and repair == 0 and pure > 0 else "baseline"
    return {
        "fixedContractReport": str(path),
        "contractCounts": {"full": full, "repair": repair, "pure": pure, "trade": trade},
        "selectedVariant": selected,
        "rule": "only_pure_when_full_and_repair_are_both_zero_and_pure_is_positive",
    }


def override_plan(base: FirstPlayerPlan, variant: str, start_shot: int) -> FirstPlayerPlan:
    """候选均为完整状态合同，不写入生产状态机。"""

    if variant == "baseline":
        return base
    if base.target_opponent_index is None:
        raise ValueError("K7 baseline has no physical-clear target; cannot construct candidate contract")
    if variant == "pure_clear":
        payload: dict[str, Any] = {
            "phase": "pure_clear_fallback",
            "target_points": (),
            "defence_shapes": (),
            "rationale": "续局对照：只清当前威胁；严格验收仍要求物理清除与规则合法。",
        }
        if int(start_shot) == 14:
            # K8 的此候选仍是通用终局合同：保住当前已领先的己方计分锚，
            # 清唯一营内敌壶；它不再额外要求一次碰撞同时补出前营双壶。
            # 这是离线 A/B 语义，生产分类器不受影响。
            payload.update({
                "strategy_type": "CLEAR_THREAT_ONLY_PRESERVE_SCORING_ANCHOR",
                "desired_state_type": "P8_CLEAR_SINGLE_THREAT_PRESERVE_CURRENT_ANCHOR",
                "max_own_cleared": 0,
                "rationale": "K8 续局对照：保住当前最近己方锚，严格清唯一营内威胁；不强行要求同手补齐双前营层。",
            })
        return replace(
            base,
            **payload,
        )
    if int(start_shot) == 10:
        raise ValueError(f"K6 does not define variant {variant}")
    if variant == "first_anchor":
        label = "K5" if int(start_shot) == 8 else "K7"
        return replace(
            base,
            phase="clear_then_reclaim_first_inner_anchor",
            target_points=(HOUSE_PAIR_LEFT[0], HOUSE_PAIR_RIGHT[0]),
            defence_shapes=(),
            landing_region_radius_m=0.35,
            max_own_cleared=0,
            rationale=f"{label} 对照：清当前威胁并建立第一颗最近内圈锚。",
        )
    if variant == "house_repair":
        if int(start_shot) not in {12, 14}:
            raise ValueError("house_repair 只定义为 K7/K8 对照")
        # 这是完整防御形和“声明槽 repair”都找不到严格解后的第三层合同：
        # 清当前计分威胁、零自清，并让出手壶留在任意大本营区域。它不把
        # 具体 x/y 写成策略，也不宣称本手已形成双层/护门；后续 K8 必须从
        # 真实后继壶面继续求解。
        label = "K7" if int(start_shot) == 12 else "K8"
        return replace(
            base,
            phase="clear_then_repair_outer_house_layer",
            target_points=((HOUSE_X, HOUSE_Y),),
            defence_shapes=(),
            landing_region_radius_m=HOUSE_R + STONE_R,
            max_own_cleared=0,
            rationale=f"{label} 续局对照：完整防御形和声明修复槽均不可达时，清威胁并严格取得任意营内恢复锚。",
        )
    if variant == "historical_control":
        return replace(
            base,
            phase="seventh_clear_and_roll_to_historical_control",
            target_points=(K7_CLEAR_TO_HISTORICAL_CONTROL,),
            defence_shapes=(),
            landing_region_radius_m=0.10,
            # 生产执行层会把通用 ``CLEAR_THREAT_AND_ROLL_INTO_DEFENCE`` 的
            # 某些盘面提前降级为“任意营内的一换一”。这里正在检验的恰是
            # 窄内圈控制合同；沿用通用策略标识会让离线 A/B 根本不执行本
            # 变体。使用已有的、语义相同的专用标识仅阻止这一次离线合同
            # 被宽松交换抢占，生产分类器及其默认 plan 不受影响。
            strategy_type="CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL",
            desired_state_type="P7_CLEAR_AND_ROLL_TO_INNER_CONTROL",
            max_own_cleared=0,
            rationale="K7 对照：清当前威胁并进入中心控制位。",
        )
    if variant == "guard_recovery":
        if int(start_shot) != 4:
            raise ValueError("guard_recovery 当前只定义为 K3 对照")
        return replace(
            base,
            phase="third_clear_and_roll_to_guard_aligned_recovery",
            target_points=K3_GUARD_ALIGNED_RECOVERY_CORRIDOR,
            defence_shapes=(),
            landing_region_radius_m=0.30,
            rationale="K3 离线对照：清侧营内威胁后，只验收守壶对齐恢复走廊；不与侧锚候选混合排序。",
        )
    if variant == "centre_front_layer":
        # 这不是生产坐标，更不是 PPO 的反事实动作。它把最近一次连续回放
        # 中的“守壶后方前营错层”写成两个关于中线镜像的角色区域，交给
        # 严格 PhysX 在当前壶面决定哪一个实际可达。合同还要求原中线守壶
        # 保留，防止用清壶时顺带拆掉自己的屏风来伪造一次成功。
        target_points = (
            (HOUSE_X - 0.18, HOUSE_Y + 1.59),
            (HOUSE_X + 0.18, HOUSE_Y + 1.59),
        )
        shape = DefenceShape(
            "K7_中线守壶后前营错层",
            "清唯一威胁后，出手壶进入中线守壶后方的前营窄区，同时保住中线守壶。",
            target_points,
            required_inner_count=0,
            landing_region_radius_m=0.22,
            # 这里不再叠加 require_centre_guard 的固定死区：薄撞后原屏风
            # 可在其 0.35m 角色带内横移。真正的保持条件由下一字段逐槽验证。
            preserve_initial_centre_guard=True,
        )
        return replace(
            base,
            phase="seventh_clear_and_roll_to_historical_control",
            target_points=target_points,
            defence_shapes=(shape,),
            landing_region_radius_m=0.22,
            max_own_cleared=0,
            rationale="K7 离线结构对照：清威胁后建立中线守壶后方前营错层；仅用于检验该角色能否被严格物理解出。",
        )
    raise ValueError(f"unknown variant: {variant}")


class K7VariantPlayer(ProxyMatchPlayer):
    def __init__(self, *, variant: str, start_shot: int, fixed_bestshot: Sequence[float] | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.variant = str(variant)
        self.start_shot = int(start_shot)
        self.fixed_bestshot = (
            tuple(float(value) for value in fixed_bestshot)
            if fixed_bestshot is not None else None
        )

    def choose(self, states: Sequence[dict[str, Any]], *, proxy_team: int, shot_index: int, match_seed: int):
        if int(shot_index) == self.start_shot and self.variant == "fixed_witness":
            if self.fixed_bestshot is None or len(self.fixed_bestshot) != 3:
                raise ValueError("fixed_witness 需要三元 --fixed-bestshot")
            _, proxy_board = evaluator.canonical_board(states, proxy_team)
            plan = evaluator.plan_first_player_turn(proxy_board, shot_index)
            # 输入必须先在固定候选批次中由严格 PhysX 三种子验证。本分支只
            # 重放该见证动作以衡量后继状态价值，绝不属于比赛状态机。
            return self.fixed_bestshot, {
                "mode": "offline_fixed_strict_witness_action",
                "firstPlayerPlan": plan.to_json(),
                "fixedWitnessBestshot": list(self.fixed_bestshot),
                "scope": "offline strict witness continuation only; not production policy",
            }
        if int(shot_index) != self.start_shot or self.variant == "baseline":
            return super().choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        original = evaluator.plan_first_player_turn

        # K6 的生产执行层有一个“单前场守壶 + 营内威胁时优先 outdraw”的
        # 快捷分支。它在真实比赛中合理，但会在本续局工具中把传入的
        # pure-clear 合同重写回 outdraw，导致 A/B 实际上没有替换动作。
        # 这里只对这一条离线候选临时关闭该捷径；生产状态机与其他回合不变。
        bypass_k6_outdraw = self.variant == "pure_clear" and self.start_shot == 10
        if bypass_k6_outdraw:
            self._try_fast_targeted_draw = lambda **_kwargs: None  # type: ignore[method-assign]

        # S5 的生产快速路径会无条件把任何“清营内威胁”的合同改写成
        # “同侧外环滚位”。它在比赛逻辑中是正常优化，却会让 K5 的
        # first-anchor A/B 根本没有执行候选合同。这里只跳过这一个被改写的
        # 临时计划；候选随后仍走原有全局严格 PhysX 搜索，不改变生产代码。
        bypass_k5_outer_anchor = self.variant == "first_anchor" and self.start_shot == 8
        if bypass_k5_outer_anchor:
            original_fast_hit_roll = self._try_fast_targeted_hit_roll

            def skip_only_k5_outer_anchor(**call_kwargs: Any):
                candidate_plan = call_kwargs.get("tactical_plan")
                if str(getattr(candidate_plan, "phase", "")) == "fifth_clear_house_threat_roll_to_outer_anchor":
                    return None
                return original_fast_hit_roll(**call_kwargs)

            self._try_fast_targeted_hit_roll = skip_only_k5_outer_anchor  # type: ignore[method-assign]

        # 生产执行层会在“声明的 defence shape 未完整达成”时自动放宽为
        # clear_then_repair_outer_house_layer。这是线上安全回退，不是本离线
        # 实验要检验的合同；若允许它介入，会把“守壶后方错层是否可解”偷换成
        # “任意清壶后进营是否可解”。因此仅在本实验中拒绝这一种放宽。
        bypass_centre_front_relaxation = self.variant == "centre_front_layer"
        if bypass_centre_front_relaxation:
            original_fast_hit_roll = self._try_fast_targeted_hit_roll

            def skip_only_relaxed_repair(**call_kwargs: Any):
                candidate_plan = call_kwargs.get("tactical_plan")
                if str(getattr(candidate_plan, "phase", "")) == "clear_then_repair_outer_house_layer":
                    return None
                return original_fast_hit_roll(**call_kwargs)

            self._try_fast_targeted_hit_roll = skip_only_relaxed_repair  # type: ignore[method-assign]

        # 与上面的错层对照同理：K7 的 house_repair 是要检验“声明修复合同”
        # 本身，而非检验线上执行层在修复未即时命中时改写出的交换合同。
        # 该拦截仅存在于离线变体；生产的安全回退完全不受影响。
        bypass_house_repair_relaxation = self.variant == "house_repair"
        if bypass_house_repair_relaxation:
            original_fast_hit_roll = self._try_fast_targeted_hit_roll

            def skip_only_declared_house_repair(**call_kwargs: Any):
                candidate_plan = call_kwargs.get("tactical_plan")
                if str(getattr(candidate_plan, "phase", "")) == "clear_then_repair_outer_house_layer":
                    return None
                return original_fast_hit_roll(**call_kwargs)

            self._try_fast_targeted_hit_roll = skip_only_declared_house_repair  # type: ignore[method-assign]

        def temporary_plan(board: Any, current_shot: int):
            base = original(board, current_shot)
            if int(current_shot) != self.start_shot:
                return base
            # 全局对局中的前营错层实验不能把每个 K7 都强制改成同一合同。
            # 仅覆盖该合同实际定义的状态：一颗己方中线屏风、唯一敌壶在营内。
            # 续局夹具也经过同一状态门，避免“指定第七手”偷换成状态机规则。
            if self.variant == "centre_front_layer":
                own = [stone for stone in board if getattr(stone, "owner", "") == "self"]
                enemy = [stone for stone in board if getattr(stone, "owner", "") == "opponent"]
                is_single_screen = (
                    len(own) == 1
                    and abs(float(own[0].x) - HOUSE_X) <= 0.25
                    and abs(float(own[0].y) - 7.15) <= 0.60
                )
                if not (is_single_screen and len(enemy) == 1 and is_in_house(enemy[0])):
                    return base
            candidate = override_plan(base, self.variant, self.start_shot)
            if self.variant == "house_repair":
                # 生产层会按 ``strategy_type`` 把“己方壶数领先”的任何清壶
                # 合同优先改成 exchange。这里借用该层已认可的“精确状态转移”
                # 标签，只为跳过这次抢占，让下面原有的 repair 分支实际得到
                # 执行机会；phase、目标、验收条件仍是 house_repair 的原定义。
                candidate = replace(
                    candidate,
                    strategy_type="CLEAR_AND_ROLL_TO_HISTORICAL_CONTROL",
                    rationale=f"{candidate.rationale}；离线修复对照：禁止通用交换分支抢占。",
                )
            return candidate

        evaluator.plan_first_player_turn = temporary_plan
        try:
            return super().choose(states, proxy_team=proxy_team, shot_index=shot_index, match_seed=match_seed)
        finally:
            evaluator.plan_first_player_turn = original
            if bypass_k6_outdraw:
                del self._try_fast_targeted_draw
            if bypass_k5_outer_anchor:
                del self._try_fast_targeted_hit_roll
            if bypass_centre_front_relaxation:
                del self._try_fast_targeted_hit_roll


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-report", type=Path)
    parser.add_argument("--full-game-seed", type=int, default=None, help="从 K1 新开离线完整对局；与 --source-report 二选一。")
    parser.add_argument("--start-shot", type=int, choices=(4, 8, 10, 12, 14), default=12, help="4=K3，8=K5，10=K6，12=K7，14=K8")
    parser.add_argument("--variant", choices=("baseline", "pure_clear", "contract_gate", "first_anchor", "house_repair", "historical_control", "guard_recovery", "centre_front_layer", "fixed_witness"), required=True)
    parser.add_argument("--contract-report", type=Path, help="仅 contract_gate：同一壶面的合同无关固定严格候选报告。")
    parser.add_argument("--fixed-bestshot", nargs=3, type=float, metavar=("V", "H", "W"), help="仅 fixed_witness：先由固定候选严格验证的输入。")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--decision-budget-seconds", type=float, default=105.0)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument("--parent-regions", type=int, default=3)
    parser.add_argument("--torch-python", type=Path, default=Path(r"D:\anaconda3\python.exe"))
    parser.add_argument("--stop-after-shot", type=int, default=None, help="仅用于严格可达性门槛；9 即只运行 K5")
    parser.add_argument(
        "--with-ppo-rollout", action="store_true",
        help="仅离线诊断：允许 K7/K8 枚举接当前 PPO 的后续一手；绝不属于比赛状态机。",
    )
    parser.add_argument(
        "--continuation-opponent", choices=("ppo", "aggressive"), default="ppo",
        help="从候选手之后使用的离线对手；此前缀仍严格重放来源报告。",
    )
    args = parser.parse_args()

    if args.variant == "fixed_witness" and args.fixed_bestshot is None:
        raise SystemExit("fixed_witness 必须提供 --fixed-bestshot V H W")
    if args.variant == "contract_gate" and args.contract_report is None:
        raise SystemExit("contract_gate 必须提供 --contract-report")
    if int(args.start_shot) == 10 and args.variant not in {"baseline", "pure_clear", "fixed_witness"}:
        raise SystemExit("K6 当前只允许 baseline 或 pure_clear 对照")
    if int(args.start_shot) == 14 and args.variant not in {"baseline", "pure_clear", "house_repair", "fixed_witness"}:
        raise SystemExit("K8 当前只允许 baseline、pure_clear 或 house_repair 对照")
    if int(args.start_shot) == 8 and args.variant not in {"baseline", "first_anchor", "fixed_witness"}:
        raise SystemExit("K5 当前只允许 baseline 或 first_anchor 对照")
    if int(args.start_shot) == 4 and args.variant not in {"baseline", "guard_recovery", "fixed_witness"}:
        raise SystemExit("K3 当前只允许 baseline 或 guard_recovery 对照")
    if int(args.start_shot) == 12 and args.variant == "centre_front_layer":
        pass
    elif args.variant == "centre_front_layer":
        raise SystemExit("centre_front_layer 当前只允许 K7 对照")
    if args.variant == "guard_recovery" and int(args.start_shot) != 4:
        raise SystemExit("guard_recovery 当前只允许 K3 对照")
    if args.variant == "house_repair" and int(args.start_shot) not in {12, 14}:
        raise SystemExit("house_repair 当前只允许 K7/K8 对照")
    if args.with_ppo_rollout and args.continuation_opponent != "ppo":
        raise SystemExit("--with-ppo-rollout 只可与 PPO continuation opponent 一起使用")
    if (args.source_report is None) == (args.full_game_seed is None):
        raise SystemExit("必须且只能提供 --source-report 或 --full-game-seed")
    if args.source_report is not None:
        report, game, initial_states, prefix = source_before(args.source_report, int(args.start_shot))
        source_seed = int(game["seed"])
    else:
        report, game, initial_states, prefix = {}, {"seed": int(args.full_game_seed)}, None, None
        source_seed = int(args.full_game_seed)
    gate_detail: dict[str, Any] | None = None
    effective_variant = str(args.variant)
    if args.variant == "contract_gate":
        if int(args.start_shot) != 12 or args.source_report is None:
            raise SystemExit("contract_gate 当前只允许从保存的 K7 壶面续局")
        gate_detail = contract_gate_decision(
            args.contract_report, source_seed=source_seed, start_shot=int(args.start_shot),
        )
        effective_variant = str(gate_detail["selectedVariant"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    progress = args.output.with_suffix(".jsonl")
    if progress.exists():
        progress.unlink()
    install_bundled_pyphysx()
    proxy = K7VariantPlayer(
        variant=effective_variant, start_shot=int(args.start_shot), physics_seeds=int(args.physics_seeds),
        parent_regions=int(args.parent_regions), decision_budget_seconds=float(args.decision_budget_seconds),
        fixed_bestshot=args.fixed_bestshot,
    )
    if args.continuation_opponent == "ppo":
        opponent: Any = WorkerPPOOpponent(args.torch_python)
        opponent_label = "ppo"
    else:
        from training_research.opponents.aggressive_strategy_adapter import AggressiveStrategyOpponent
        opponent = AggressiveStrategyOpponent()
        opponent_label = "aggressive"
    if args.with_ppo_rollout:
        proxy.terminal_reply_opponent = opponent
    append_log(progress, {
        "type": "continuation_start", "source": str(args.source_report), "variant": args.variant,
        "effectiveVariant": effective_variant, "contractGate": gate_detail,
        "offlinePpoRollout": bool(args.with_ppo_rollout),
    })
    try:
        outcome = run_game(
            game_index=1, proxy_team=0, seed=source_seed, proxy=proxy,
            opponent=opponent, opponent_label=opponent_label, progress_path=progress,
            start_shot=0 if args.full_game_seed is not None else int(args.start_shot), prefix_trace=prefix,
            expected_start_states=initial_states,
            stop_after_shot=args.stop_after_shot,
        )
    finally:
        close = getattr(opponent, "close", None)
        if callable(close):
            close()
    candidate_plan_selected: bool | None = None
    candidate_contract_solved: bool | None = None
    if args.variant == "first_anchor":
        candidate_trace = next((
            item for item in outcome["trace"]
            if int(item.get("shot", 0)) == int(args.start_shot) + 1 and item.get("actor") == "proxy"
        ), None)
        actual_phase = (
            candidate_trace.get("detail", {}).get("firstPlayerPlan", {}).get("phase")
            if isinstance(candidate_trace, dict) else None
        )
        if actual_phase != "clear_then_reclaim_first_inner_anchor":
            raise RuntimeError(
                "候选合同未实际执行，拒绝写入可比较结果："
                f"期望 clear_then_reclaim_first_inner_anchor，实际 {actual_phase!r}"
            )
    if args.variant == "house_repair":
        candidate_trace = next((
            item for item in outcome["trace"]
            if int(item.get("shot", 0)) == int(args.start_shot) + 1 and item.get("actor") == "proxy"
        ), None)
        actual_phase = (
            candidate_trace.get("detail", {}).get("firstPlayerPlan", {}).get("phase")
            if isinstance(candidate_trace, dict) else None
        )
        if actual_phase != "clear_then_repair_outer_house_layer":
            raise RuntimeError(
                "house_repair 合同未实际执行，拒绝写入可比较结果："
                f"实际 {actual_phase!r}"
            )
    if args.variant == "centre_front_layer":
        candidate_trace = next((
            item for item in outcome["trace"]
            if int(item.get("shot", 0)) == int(args.start_shot) + 1 and item.get("actor") == "proxy"
        ), None)
        actual_plan = candidate_trace.get("detail", {}).get("firstPlayerPlan", {}) if isinstance(candidate_trace, dict) else {}
        candidate_plan_selected = bool(
            actual_plan.get("phase") == "seventh_clear_and_roll_to_historical_control"
            and actual_plan.get("defence_shapes")
        )
        candidate_detail = candidate_trace.get("detail", {}) if isinstance(candidate_trace, dict) else {}
        candidate_contract_solved = bool(
            candidate_plan_selected
            and int(candidate_detail.get("candidateCount", 0) or 0) > 0
            and not candidate_detail.get("fallbackReason")
        )
        # 对保存局面续盘，候选合同必须实际执行，否则该对照没有意义。
        # 对完整 K1--K16 回放，状态门控本来就允许它不触发；该样本应作为
        # “未适用时是否保持基线”的回归证据，而不是伪造为候选失败。
        if not candidate_contract_solved and args.full_game_seed is None:
            raise RuntimeError(
                "前营错层合同未实际执行，拒绝写入可比较结果："
                f"phase={actual_plan.get('phase')!r} shapes={bool(actual_plan.get('defence_shapes'))}"
            )
    if args.variant == "guard_recovery":
        candidate_trace = next((
            item for item in outcome["trace"]
            if int(item.get("shot", 0)) == int(args.start_shot) + 1 and item.get("actor") == "proxy"
        ), None)
        actual_phase = (
            candidate_trace.get("detail", {}).get("firstPlayerPlan", {}).get("phase")
            if isinstance(candidate_trace, dict) else None
        )
        if actual_phase != "third_clear_and_roll_to_guard_aligned_recovery":
            raise RuntimeError(
                "K3 守壶恢复合同未实际执行，拒绝写入可比较结果："
                f"实际 {actual_phase!r}"
            )
    payload = {
        "schema": "k7_continuation_variant_v1",
        "scope": (
            "one complete local strict-PhysX first-player end; not a platform-wide win-rate proof"
            if args.full_game_seed is not None
            else "strict PhysX late-end continuation from a saved real state; not full-end win-rate proof"
        ),
        "sourceReport": None if args.source_report is None else str(args.source_report), "startShot": int(args.start_shot), "variant": args.variant,
        "effectiveVariant": effective_variant, "contractGate": gate_detail,
        "sourceOpponent": report.get("opponent"), "sourceSeed": source_seed,
        "fullGame": bool(args.full_game_seed is not None),
        "candidatePlanSelected": candidate_plan_selected,
        "candidateContractSolved": candidate_contract_solved,
        "continuationOpponent": str(args.continuation_opponent),
        "plannerPhysicsSeeds": int(args.physics_seeds), "decisionBudgetSeconds": float(args.decision_budget_seconds),
        "offlinePpoRollout": bool(args.with_ppo_rollout),
        # 这是下一级续局的严格物理输入，而非单纯坐标快照。保存它使 K6->K7->K8
        # A/B 可以沿着同一条已核验的真实物理前缀继续，而不会在层级间断链。
        "strictPhysicalPrefixTrace": prefix if args.source_report is not None else [],
        "game": outcome,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    append_log(progress, {"type": "continuation_end", "report": str(args.output)})
    print(f"variant={args.variant} score={outcome['finalScoreProxy']:+d} elapsed={outcome['elapsedSeconds']:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
