#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为双飞/单清建立多模态的 GoalState 碰撞家族与数据回退边。

精细落点边无法覆盖双飞：同一“清掉两颗敌壶”的目标可有多种出手壶滚位，
且 NWNHT 同色壶缺少持久 id。本工件因此只声明可由运行时绑定的目标组合：

``两颗当前最靠按钮的对方营内壶 -> 必须出界``，失败则尝试
``一颗当前最靠按钮的对方营内壶 -> 必须出界``。

它不是历史中已追踪的固定壶号，也不强制出手壶停在一个伪精确坐标。调用方
必须枚举实际棋盘中合资格的组合，经本地规则和严格 PhysX 搜索后才能执行。
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


MIN_SUPPORT = 30


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def parse_core_state(state: str) -> dict[str, str]:
    """解析既有 runtime-safe core state；不引入比赛上下文。"""

    if not state.startswith("K") or "_CORE[" not in state:
        raise ValueError("需要 K*_CORE[...] 状态")
    values = dict(re.findall(r"([A-Za-z_]+)=([^;\]]+)", state))
    required = {
        "control", "F_house", "O_house", "F_centre_guard", "O_centre_guard", "F_wing_guard", "O_wing_guard",
    }
    if required - values.keys():
        raise ValueError("core state 缺少特征: %s" % sorted(required - values.keys()))
    values["K"] = state.split("_", 1)[0]
    return values


def macro_collision_state(state: str) -> str:
    """只保留会影响双飞目标选择的拓扑，不保留队名/比分/结果。"""

    values = parse_core_state(state)
    first_guards = "Y" if values["F_centre_guard"] != "0" or values["F_wing_guard"] != "0" else "N"
    opponent_guards = "Y" if values["O_centre_guard"] != "0" or values["O_wing_guard"] != "0" else "N"
    return (
        f"{values['K']}_COLLISION[control={values['control']};F_house={values['F_house']};"
        f"O_house={values['O_house']};F_guards={first_guards};O_guards={opponent_guards}]"
    )


def _house_count(occupancy: dict[str, int]) -> int:
    return sum(int(count) for zone, count in occupancy.items() if zone == "button" or zone.startswith("house_"))


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [
        {"value": key, "count": value, "share": round(value / total, 6)}
        for key, value in counter.most_common()
    ]


def build(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, int], dict[str, Any]] = defaultdict(lambda: {
        "support": 0,
        "precision": Counter(),
        "after_opp_house": Counter(),
        "after_self_house": Counter(),
        "active_outcomes": Counter(),
        "own_after_state": Counter(),
        "reply_state": Counter(),
        "examples": [],
    })
    input_rows = 0
    for row in rows:
        delta = row.get("observed_delta", {})
        if "opponent_house_removed_count" not in delta:
            raise ValueError("模板缺少 opponent_house_removed_count；请使用 nwnht_anonymous_goal_templates_v1 或更高版本")
        house_removed = int(delta["opponent_house_removed_count"])
        if house_removed <= 0:
            continue
        input_rows += 1
        removed = house_removed
        key = (macro_collision_state(str(row["source_state"])), removed)
        item = groups[key]
        item["support"] += 1
        item["precision"][str(row["precision"])] += 1
        own = row["after_own_occupancy"]
        item["after_opp_house"][str(_house_count(own["opponent"]))] += 1
        item["after_self_house"][str(_house_count(own["first"]))] += 1
        point = row.get("active_final_point")
        item["active_outcomes"]["UNRESOLVED_OR_OUT" if point is None else str(point["zone"])] += 1
        item["own_after_state"][str(row["expected_own_after_state"])] += 1
        item["reply_state"][str(row["expected_after_reply_state"])] += 1
        if len(item["examples"]) < 5:
            item["examples"].append(str(row["panel_key"]))

    families: list[dict[str, Any]] = []
    candidate_count = 0
    for (source, removed), item in groups.items():
        values = dict(re.findall(r"([A-Za-z_]+)=([^;\]]+)", source))
        # 只有当前宏观状态明确有足够的敌方营内壶时，才产生动态绑定请求。
        # 这避免把“清两颗守壶”误译成“清两颗营内壶”。
        choose_count = 2 if removed >= 2 else 1
        bindable_targets = (
            (choose_count == 2 and values.get("O_house") == "2P")
            or (choose_count == 1 and values.get("O_house") in {"1", "2P"})
        )
        candidate = item["support"] >= MIN_SUPPORT and bindable_targets
        candidate_count += int(candidate)
        binding = None if not bindable_targets else {
            "binding_kind": "OPPONENT_HOUSE_SET",
            "owner": "opponent",
            "source_region": "house",
            "choose_count": choose_count,
            "combination_order": "try all combinations; prioritize combinations containing the closest-to-button stone",
            "required_disposition": "OUT_OF_PLAY",
            "identity_note": "Dynamic current-board roles, not historical fixed stone ids.",
        }
        families.append({
            "schema": "nwnht_collision_goal_family_v2",
            "collision_family_id": f"{source}|remove={removed}",
            "source_collision_state": source,
            "observed_opponent_house_removed_count": removed,
            "support": item["support"],
            "historical_precision": dict(sorted(item["precision"].items())),
            "dynamic_binding_request": binding,
            "goal_constraints": [] if binding is None else [
                f"selected {choose_count} opponent house stone(s) must be OUT_OF_PLAY",
                "apply local free-guard-zone rule before accepting a path",
                "do not require a unique active-stone endpoint; evaluate each PhysX result against the selected pair-out constraint",
            ],
            "observed_after_own_opponent_house_count": _distribution(item["after_opp_house"]),
            "observed_after_own_self_house_count": _distribution(item["after_self_house"]),
            "observed_active_final_outcomes": _distribution(item["active_outcomes"]),
            "observed_own_after_states": _distribution(item["own_after_state"]),
            "observed_after_reply_states": _distribution(item["reply_state"]),
            "physx_search_required": True,
            "runtime_candidate_for_physx_screen": candidate,
            "not_runtime_candidate_reasons": [] if candidate else (
                ([f"support<{MIN_SUPPORT}"] if item["support"] < MIN_SUPPORT else [])
                + ([] if bindable_targets else ["source_state_does_not_guarantee_required_opponent_house_targets"])
            ),
            "examples": item["examples"],
            "evidence_status": "HISTORICAL_COLLISION_FAMILY",
            "warning": "Observed multi-removal family; does not prove that a selected runtime pair was the historical removed pair or that any route is PhysX-feasible.",
        })
    families.sort(key=lambda row: (-int(row["support"]), str(row["collision_family_id"])))
    manifest = {
        "schema": "nwnht_collision_goal_family_manifest_v2",
        "input_rows_with_opponent_house_removal": input_rows,
        "family_count": len(families),
        "runtime_candidate_for_physx_screen_count": candidate_count,
        "min_support": MIN_SUPPORT,
        "binding_policy": "only observed opponent-house removal contributes evidence; one target requires O_house=1/2P, two targets requires O_house=2P; dynamic slots are chosen at runtime",
        "warning": "Candidates require current-board role binding, rule validation, strict PhysX feasibility, and opponent reply search before use.",
    }
    return families, manifest


def main() -> int:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_anonymous_goal_templates_v1.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_collision_goal_families_v2.json")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_collision_goal_families_v2_manifest.json")
    args = parser.parse_args()
    families, manifest = build(read_jsonl(args.input))
    args.output.write_text(json.dumps(families, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("碰撞 GoalState 家族：%d 条；待 PhysX 筛选候选：%d 条。" % (manifest["family_count"], manifest["runtime_candidate_for_physx_screen_count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
