#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 NWNHT 匿名前后棋盘抽取可审计的终局约束模板原料。

NWNHT 每帧只给出同色壶的匿名坐标点集。故本程序不会输出历史固定壶号，
也不会把观测到的终局误称为原始意图。它只保守记录：

``S(出手前) -> observed anonymous goal template -> U(出手后) -> V(对方回应后)``

后续聚合器才能将高支持模板编译为运行时 ``GoalState``；运行时再以几何角色
绑定当前 PhysX slot。坐标保持 NWNHT 的“以按钮为原点、米”为规范坐标，尚未
转换为本地 PhysX 绝对坐标。
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

try:
    from .build_causal_state_abstraction import state_key
except ImportError:  # pragma: no cover - direct invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.build_causal_state_abstraction import state_key  # type: ignore


HOUSE_RADIUS_M = 1.8288
BUTTON_RADIUS_M = 0.6096
FRONT_GUARD_Y_MAX_M = 6.45
UNCHANGED_MATCH_TOLERANCE_M = 0.12


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def zone_of(stone: dict[str, Any]) -> str:
    """返回足以指导后续绑定的、以按钮为中心的粗几何区域。"""

    x, y = float(stone["x_m"]), float(stone["y_m"])
    distance = math.hypot(x, y)
    if distance <= BUTTON_RADIUS_M:
        return "button"
    if distance <= HOUSE_RADIUS_M:
        depth = "front" if y >= 0.0 else "back"
        side = "left" if x < 0.0 else "right"
        return f"house_{depth}_{side}"
    if y > HOUSE_RADIUS_M and y <= FRONT_GUARD_Y_MAX_M:
        if abs(x) <= 0.38:
            return "centre_guard"
        return "wing_guard_left" if x < 0.0 else "wing_guard_right"
    return "outside_tactical_zone"


def _owner_stones(board: list[dict[str, Any]], owner: str) -> list[dict[str, Any]]:
    return [stone for stone in board if str(stone["owner"]) == owner]


def zone_counts(board: list[dict[str, Any]], owner: str) -> dict[str, int]:
    counts = Counter(zone_of(stone) for stone in _owner_stones(board, owner))
    return {name: int(counts[name]) for name in sorted(counts) if name != "outside_tactical_zone"}


def house_count(occupancy: dict[str, int]) -> int:
    return sum(int(count) for zone, count in occupancy.items() if zone == "button" or zone.startswith("house_"))


def _can_match_unchanged(
    before: list[dict[str, Any]], after_without_candidate: list[dict[str, Any]],
) -> bool:
    """是否能把每颗旧壶一一匹配到 0.12m 内的终局壶。

    这是一个小二分匹配；单队单帧最多八颗壶。匹配成功只表示“足够稳定，
    可以把唯一剩余壶视为出手壶”，不尝试恢复复杂碰撞中的历史身份。
    """

    if len(before) != len(after_without_candidate):
        return False
    adjacency: list[list[int]] = []
    for old in before:
        neighbours = [
            index for index, new in enumerate(after_without_candidate)
            if math.hypot(float(old["x_m"]) - float(new["x_m"]), float(old["y_m"]) - float(new["y_m"]))
            <= UNCHANGED_MATCH_TOLERANCE_M
        ]
        if not neighbours:
            return False
        adjacency.append(neighbours)

    assigned = [-1] * len(after_without_candidate)

    def augment(old_index: int, seen: set[int]) -> bool:
        for new_index in adjacency[old_index]:
            if new_index in seen:
                continue
            seen.add(new_index)
            if assigned[new_index] == -1 or augment(assigned[new_index], seen):
                assigned[new_index] = old_index
                return True
        return False

    return all(augment(old_index, set()) for old_index in range(len(before)))


def infer_active_final_point(
    before: list[dict[str, Any]], after: list[dict[str, Any]], *, owner: str = "first",
) -> dict[str, Any] | None:
    """仅在新增壶唯一且旧同色壶可稳定匹配时，返回出手壶终局点。"""

    old = _owner_stones(before, owner)
    new = _owner_stones(after, owner)
    if len(new) != len(old) + 1:
        return None
    candidates: list[dict[str, Any]] = []
    for candidate_index, candidate in enumerate(new):
        remaining = new[:candidate_index] + new[candidate_index + 1 :]
        if _can_match_unchanged(old, remaining):
            candidates.append(candidate)
    if len(candidates) != 1:
        return None
    point = candidates[0]
    return {
        "x_m": round(float(point["x_m"]), 6),
        "y_m": round(float(point["y_m"]), 6),
        "zone": zone_of(point),
        "inference": "unique_net_added_stone_with_unchanged_old_stones",
    }


def _all_opponents_removed_selectors(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """只在场上全部对方壶均消失时，输出可运行时再绑定的角色选择器。"""

    old = _owner_stones(before, "opponent")
    new = _owner_stones(after, "opponent")
    if not old or new:
        return []
    ordered = sorted(old, key=lambda stone: math.hypot(float(stone["x_m"]), float(stone["y_m"])))
    return [
        {
            "selector_id": f"opponent_visible_rank_{rank}",
            "owner": "opponent",
            "source_region": "visible",
            "rank_by": "closest_to_button",
            "rank": rank,
            "required_disposition": "OUT_OF_PLAY",
            "historical_source_zone": zone_of(stone),
        }
        for rank, stone in enumerate(ordered, 1)
    ]


def extract_template(row: dict[str, Any]) -> dict[str, Any]:
    """把单条 accepted transition 转为匿名 GoalState 原料。"""

    k = int(row["own_throw_number"])
    before = list(row["s_before_own"])
    after_own = list(row["u_after_own"])
    after_reply = list(row["s_after_opponent_reply"])
    first_before = len(_owner_stones(before, "first"))
    first_after = len(_owner_stones(after_own, "first"))
    opponent_before = len(_owner_stones(before, "opponent"))
    opponent_after = len(_owner_stones(after_own, "opponent"))
    active_final = infer_active_final_point(before, after_own)
    opponent_removed = opponent_before - opponent_after
    self_net_change = first_after - first_before
    selectors = _all_opponents_removed_selectors(before, after_own)
    before_occupancy = {"first": zone_counts(before, "first"), "opponent": zone_counts(before, "opponent")}
    after_occupancy = {"first": zone_counts(after_own, "first"), "opponent": zone_counts(after_own, "opponent")}

    if opponent_removed >= 2:
        template_kind = "DOUBLE_OR_MULTI_OPPONENT_REMOVAL"
    elif opponent_removed == 1:
        template_kind = "SINGLE_OPPONENT_REMOVAL"
    elif active_final is not None:
        template_kind = "ACTIVE_STONE_PLACEMENT"
    elif before != after_own:
        template_kind = "MIXED_OR_UNRESOLVED_COLLISION"
    else:
        template_kind = "NO_OBSERVABLE_BOARD_CHANGE"

    if active_final is not None or selectors:
        precision = "ROLE_AND_REGION"
    elif before != after_own:
        precision = "REGION_OCCUPANCY_ONLY"
    else:
        precision = "ABSTAIN"

    return {
        "schema": "nwnht_anonymous_goal_template_row_v0",
        "panel_key": f"{row['end_id']}:{row['own_global_shot_number']}",
        "match_id": int(row["match_id"]),
        "own_throw_number": k,
        "source_state": state_key(k, before),
        "expected_own_after_state": state_key(k, after_own),
        "expected_after_reply_state": "END" if k == 8 else state_key(k + 1, after_reply),
        "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES",
        "observed_template_kind": template_kind,
        "precision": precision,
        "observed_delta": {
            "first_visible": first_after - first_before,
            "opponent_visible": opponent_after - opponent_before,
            "opponent_removed_count": opponent_removed,
            "first_house": house_count(after_occupancy["first"]) - house_count(before_occupancy["first"]),
            "opponent_house": house_count(after_occupancy["opponent"]) - house_count(before_occupancy["opponent"]),
            "opponent_house_removed_count": house_count(before_occupancy["opponent"]) - house_count(after_occupancy["opponent"]),
        },
        "active_final_point": active_final,
        "stone_constraints_when_unambiguous": selectors,
        "before_own_occupancy": before_occupancy,
        "after_own_occupancy": after_occupancy,
        "after_reply_occupancy": {
            "first": zone_counts(after_reply, "first"),
            "opponent": zone_counts(after_reply, "opponent"),
        },
        "abstention_reason": (
            None if precision != "ABSTAIN"
            else "同色壶无唯一新增终局点，且无可观测棋盘变化；不伪造终局约束"
        ),
    }


def build(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    output: list[dict[str, Any]] = []
    precision_counts: Counter[str] = Counter()
    kind_counts: Counter[str] = Counter()
    for row in rows:
        template = extract_template(row)
        output.append(template)
        precision_counts[template["precision"]] += 1
        kind_counts[template["observed_template_kind"]] += 1
    manifest = {
        "schema": "nwnht_anonymous_goal_template_manifest_v1",
        "row_count": len(output),
        "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES",
        "coordinate_transform_status": "not_yet_compiled_to_local_physx; expected translation is checked separately before runtime use",
        "identity_limit": "same-colour stones have no persistent NWNHT id; selector constraints appear only when every opponent stone is observed removed",
        "active_final_inference": "only a unique net-added first stone after all old first stones can be one-to-one matched within 0.12m",
        "precision_counts": dict(sorted(precision_counts.items())),
        "template_kind_counts": dict(sorted(kind_counts.items())),
        "house_removal_definition": "opponent_house_removed_count is exact anonymous before/after house occupancy change; it does not claim persistent same-colour stone identity.",
        "warning": "Observed S->U outcomes, not intended shots, causal effects, or validated local-PhysX goals.",
    }
    return output, manifest


def main() -> int:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--output", type=Path, default=root / "nwnht_anonymous_goal_templates_v1.jsonl")
    parser.add_argument("--manifest", type=Path, default=root / "nwnht_anonymous_goal_templates_v1_manifest.json")
    parser.add_argument("--limit", type=int, default=None, help="仅处理前 N 行，用于小样本烟雾检查。")
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    if args.limit is not None:
        if args.limit < 1:
            raise ValueError("--limit 必须为正")
        rows = (row for _, row in zip(range(args.limit), rows))
    output, manifest = build(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in output:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("匿名 GoalState 模板：%d 行；精度=%s" % (manifest["row_count"], manifest["precision_counts"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
