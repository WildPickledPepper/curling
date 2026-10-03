"""提取历史中真实执行过 K6 outdraw 的正反壶面，供当前模块复验。

跨版本旧对局的胜负不作为当前胜率；它们只提供真实的 K6 输入分布。输出固定保留每个
不同 live-slot x/y/yaw 壶面及其历史正反结果，避免只围绕最近一次失败局开发策略。
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any


def state_key(states: list[dict[str, Any]]) -> tuple[tuple[int, float, float, float], ...]:
    return tuple(
        (int(index), round(float(stone["x"]), 3), round(float(stone["y"]), 3), round(float(stone.get("yaw", 0.0)), 3))
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
    args = parser.parse_args()
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    records = [
        row for row in audit["samples"]
        if int(row["k"]) == 6
        and str(row["opponent"]) == "ppo"
        and str(row["currentSituation"]) == "P6_ENEMY_THREAT_ONE_OWN"
        and str(row["mode"]) == "first_player_k6_outdraw_single_house_threat"
    ]
    groups: dict[tuple[tuple[int, float, float, float], ...], list[dict[str, Any]]] = collections.defaultdict(list)
    for record in records:
        groups[state_key(record["stateBefore"])].append(record)
    fixtures = []
    for key, members in groups.items():
        representative = sorted(members, key=lambda item: str(item["source"]))[0]
        fixtures.append(
            {
                "fixtureId": "",
                "stateKeyRounded": [list(item) for item in key],
                "stateBefore": representative["stateBefore"],
                "liveStoneSummary": live_summary(representative["stateBefore"]),
                "historicalRecordCount": len(members),
                "historicalOutcomeCount": dict(sorted(collections.Counter(str(item["finalResult"]) for item in members).items())),
                "historicalMatchSeeds": sorted({int(item["seed"]) for item in members}),
                "historicalSources": sorted(str(item["source"]) for item in members),
                "interpretation": "历史曾执行 outdraw 的真实 K6 输入；仅用于当前模块重测，禁止把旧胜负当当前胜率。",
            }
        )
    fixtures.sort(key=lambda item: (-int(item["historicalRecordCount"]), str(item["stateKeyRounded"])))
    for index, fixture in enumerate(fixtures, 1):
        fixture["fixtureId"] = f"k6_outdraw_state_{index:02d}"
    payload = {
        "schema": "k6_outdraw_transition_fixture_set_v1",
        "purpose": "K6 outdraw 前真实壶面的当前状态机回归输入；包含历史正反样本，不是策略标签。",
        "selection": {
            "shot": 11,
            "opponent": "ppo",
            "currentSituation": "P6_ENEMY_THREAT_ONE_OWN",
            "historicalMode": "first_player_k6_outdraw_single_house_threat",
            "deduplication": "完整 live slot 的 index/x/y/yaw，取 0.001 精度。",
        },
        "inputRecordCount": len(records),
        "uniqueStateCount": len(groups),
        "fixtureCount": len(fixtures),
        "fixtures": fixtures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
