"""从历史完整回放提取可复跑的 K7 状态转移测试集。

历史文件跨多个代码版本，不能作为当前策略胜率统计。本工具只使用其中真实出现过的
``stateBefore`` 壶面，按完整 live-slot 的 x/y/yaw 去重，选出同一壶面被重复试验且
至少一次走向负分的样本。它们用于当前规划器的严格合同测试，而不用于直接生成动作。
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any


TARGET_SITUATION = "P7_ENEMY_THREAT_ONE_OWN"


def state_key(states: list[dict[str, Any]]) -> tuple[tuple[int, float, float, float], ...]:
    return tuple(
        (
            int(index),
            round(float(stone["x"]), 3),
            round(float(stone["y"]), 3),
            round(float(stone.get("yaw", 0.0)), 3),
        )
        for index, stone in enumerate(states)
        if bool(stone.get("enabled", True))
    )


def live_summary(states: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "index": int(index),
            "owner": "self" if index % 2 == 0 else "opponent",
            "x": round(float(stone["x"]), 6),
            "y": round(float(stone["y"]), 6),
            "yaw": round(float(stone.get("yaw", 0.0)), 6),
        }
        for index, stone in enumerate(states)
        if bool(stone.get("enabled", True))
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, default=Path(__file__).with_name("runs") / "first_player_state_data_audit.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-repeats", type=int, default=2)
    args = parser.parse_args()

    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    rows = [
        row
        for row in audit["samples"]
        if int(row["k"]) == 7
        and str(row["opponent"]) == "ppo"
        and str(row["currentSituation"]) == TARGET_SITUATION
    ]
    grouped: dict[tuple[tuple[int, float, float, float], ...], list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        grouped[state_key(row["stateBefore"])].append(row)

    fixtures: list[dict[str, Any]] = []
    for key, members in grouped.items():
        outcomes = collections.Counter(str(member["finalResult"]) for member in members)
        if len(members) < int(args.minimum_repeats) or outcomes.get("负", 0) == 0:
            continue
        source = sorted(members, key=lambda member: str(member["source"]))[0]
        fixtures.append(
            {
                "fixtureId": f"k7_state_{len(fixtures) + 1:02d}",
                "stateKeyRounded": [list(item) for item in key],
                "stateBefore": source["stateBefore"],
                "liveStoneSummary": live_summary(source["stateBefore"]),
                "historicalRecordCount": len(members),
                "historicalOutcomeCount": dict(sorted(outcomes.items())),
                "historicalModes": dict(sorted(collections.Counter(str(member["mode"]) for member in members).items())),
                "historicalMatchSeeds": sorted({int(member["seed"]) for member in members}),
                "historicalSources": sorted(str(member["source"]) for member in members),
                "interpretation": (
                    "同一真实 K7 壶面在旧版本中被重复尝试且至少一次负分；"
                    "仅用于当前严格合同的回归测试，不表示当前胜率或推荐动作。"
                ),
            }
        )
    fixtures.sort(key=lambda item: (-int(item["historicalRecordCount"]), str(item["fixtureId"])))
    for index, fixture in enumerate(fixtures, 1):
        fixture["fixtureId"] = f"k7_state_{index:02d}"
    payload = {
        "schema": "k7_historical_transition_fixture_set_v1",
        "purpose": "当前状态机/严格规划器的离线回归输入；禁止当作跨版本胜率统计或固定动作库。",
        "selection": {
            "shot": 13,
            "opponent": "ppo",
            "currentSituation": TARGET_SITUATION,
            "minimumRepeatedHistoricalRecords": int(args.minimum_repeats),
            "requiresAtLeastOneHistoricalLoss": True,
            "deduplication": "完整 live slot 的 index/x/y/yaw，坐标和 yaw 均取 0.001m/rad 精度。",
        },
        "inputRecordCount": len(rows),
        "uniqueStateCount": len(grouped),
        "fixtureCount": len(fixtures),
        "fixtures": fixtures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
