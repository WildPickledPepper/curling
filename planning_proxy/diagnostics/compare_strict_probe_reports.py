"""比较两个 strict_candidate_tail_probe 报告的严格物理结果。

用于当前扩展与候选扩展的隔离等价检查。规则、清壶、接触步数必须完全相同；
终局壶面同时报告逐壶坐标/朝向最大差，默认容差 1e-6 米/弧度。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


DISCRETE_FIELDS = (
    "scores", "enemy_cleared", "own_cleared", "active_cleared", "total_self_cleared",
    "own_in_house", "preserves_all_own", "rule_legal", "rule_violations",
    "enemy_cleared_indices", "tactical_goal_met",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left", type=Path, required=True)
    parser.add_argument("--right", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=1e-6)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "strict_candidate_tail_probe_v1":
        raise SystemExit(f"不是 strict_candidate_tail_probe_v1：{path}")
    return data


def board_rows(board: Iterable[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {int(row["index"]): row for row in board}


def main() -> None:
    args = parse_args()
    left, right = load(args.left), load(args.right)
    identity = {
        field: left.get(field) == right.get(field)
        for field in ("source", "shot", "matchSeed", "physicsSeeds", "action", "currentPlan")
    }
    failures: list[str] = [field for field, equal in identity.items() if not equal]
    left_repeats, right_repeats = left.get("repeat", []), right.get("repeat", [])
    if len(left_repeats) != len(right_repeats):
        failures.append("重复次数不同")
    max_position_delta = 0.0
    max_yaw_delta = 0.0
    repeat_results: list[dict[str, Any]] = []
    for index, (left_repeat, right_repeat) in enumerate(zip(left_repeats, right_repeats), 1):
        result: dict[str, Any] = {"repeat": index, "discreteEqual": True, "frontHalfEqual": True}
        for key in ("enemyCleared", "ownCleared", "activeCleared"):
            if left_repeat.get(key) != right_repeat.get(key):
                result["discreteEqual"] = False
                failures.append(f"第 {index} 次 {key} 不同")
        left_front, right_front = left_repeat.get("frontHalf", []), right_repeat.get("frontHalf", [])
        front_projection = lambda rows: [
            (row.get("steps"), row.get("reachedFirstContact"), row.get("nativeLoop")) for row in rows
        ]
        if front_projection(left_front) != front_projection(right_front):
            result["frontHalfEqual"] = False
            failures.append(f"第 {index} 次首次接触步数或状态不同")
        left_eval = left_repeat.get("strictEvaluation", {})
        right_eval = right_repeat.get("strictEvaluation", {})
        for field in DISCRETE_FIELDS:
            if left_eval.get(field) != right_eval.get(field):
                result["discreteEqual"] = False
                failures.append(f"第 {index} 次严格字段 {field} 不同")
        left_boards, right_boards = left_eval.get("final_boards", []), right_eval.get("final_boards", [])
        if len(left_boards) != len(right_boards):
            failures.append(f"第 {index} 次终局种子数量不同")
        for seed_index, (left_board, right_board) in enumerate(zip(left_boards, right_boards), 1):
            a, b = board_rows(left_board), board_rows(right_board)
            if set(a) != set(b):
                failures.append(f"第 {index} 次第 {seed_index} 个种子终局壶集合不同")
                continue
            for stone_index in a:
                if bool(a[stone_index].get("enabled")) != bool(b[stone_index].get("enabled")):
                    failures.append(f"第 {index} 次第 {seed_index} 个种子壶 {stone_index} 在场状态不同")
                max_position_delta = max(
                    max_position_delta,
                    abs(float(a[stone_index]["x"]) - float(b[stone_index]["x"])),
                    abs(float(a[stone_index]["y"]) - float(b[stone_index]["y"])),
                )
                max_yaw_delta = max(max_yaw_delta, abs(float(a[stone_index]["yaw"]) - float(b[stone_index]["yaw"])))
        repeat_results.append(result)
    semantic_equal = not failures and max_position_delta <= args.tolerance and max_yaw_delta <= args.tolerance
    output = {
        "schema": "strict_probe_equivalence_v1",
        "left": str(args.left),
        "right": str(args.right),
        "tolerance": args.tolerance,
        "identityEqual": all(identity.values()),
        "repeatResults": repeat_results,
        "maxPositionDelta": max_position_delta,
        "maxYawDelta": max_yaw_delta,
        "semanticEqual": semantic_equal,
        "differences": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: output[key] for key in ("semanticEqual", "maxPositionDelta", "maxYawDelta", "differences")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
