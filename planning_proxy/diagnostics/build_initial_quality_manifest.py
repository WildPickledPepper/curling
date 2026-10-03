#!/usr/bin/env python3
"""把分层首撞审计拆成“局部收敛质量集”和“入口覆盖压力集”。

这不是新的候选生成器，也不改变生产搜索。原审计的职责是覆盖不同的
首撞拓扑；其中很远离声明落区的原始球不适合用来衡量 MADS/随机精英
在“已有可用初值”后的收敛能力。本脚本只按审计内已记录的粗代理落区
距离生成可复查的测试清单，并完整保留被分到压力集的入口。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, action="append", required=True)
    parser.add_argument(
        "--max-proxy-distance", type=float, default=1.20,
        help="进入局部收敛质量集的最大粗代理落区距离（米）",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else (ROOT / path).resolve()


def entry(audit_path: Path, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit": str(audit_path),
        "rank": int(row["rank"]),
        "rawBestshot": [float(value) for value in row["rawBestshot"]],
        "proxyDistanceToTargetM": float(row["proxyDistanceToTargetM"]),
        "stratum": [int(value) for value in row["stratum"]],
        "auditOneSeedContractMetAfterLocalSearch": bool(row["oneSeedContractMet"]),
    }


def main() -> int:
    args = parse_args()
    if args.max_proxy_distance <= 0:
        raise SystemExit("--max-proxy-distance 必须为正数")

    convergence: list[dict[str, Any]] = []
    stress: list[dict[str, Any]] = []
    source_summary: list[dict[str, Any]] = []
    for raw_path in args.audit:
        path = resolve(raw_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = list(payload.get("primaryRows", ()))
        selected = [entry(path, row) for row in rows]
        near = [row for row in selected if row["proxyDistanceToTargetM"] <= args.max_proxy_distance]
        far = [row for row in selected if row["proxyDistanceToTargetM"] > args.max_proxy_distance]
        convergence.extend(near)
        stress.extend(far)
        distances = [row["proxyDistanceToTargetM"] for row in selected]
        source_summary.append({
            "audit": str(path), "total": len(selected), "convergence": len(near), "stress": len(far),
            "minProxyDistanceM": min(distances), "maxProxyDistanceM": max(distances),
        })

    output = {
        "schema": "initial_quality_manifest_v1",
        "scope": (
            "离线测试分层；不改生产候选或严格验收。质量集用于比较已有合格拓扑附近的局部搜索，"
            "压力集用于暴露候选生成覆盖缺口。"
        ),
        "qualityRule": {
            "requires": ["来源审计已限定为首撞指定目标的原始球", "proxyDistanceToTargetM <= threshold"],
            "thresholdM": float(args.max_proxy_distance),
            "reason": "当前三个审计中，校准壶面最大距离 1.084m，两个独立难例最小距离 1.452m；阈值置于可观测间隔内。",
        },
        "sources": source_summary,
        "convergenceQualityEntries": convergence,
        "coverageStressEntries": stress,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"quality": len(convergence), "stress": len(stress), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
