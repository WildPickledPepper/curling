"""只读汇总历史严格全局搜索的长尾候选。

本工具不判断合同是否有解，也不修改搜索边界。它只回答：历史记录中最慢
严格候选和最终提交动作分别落在哪个输入带，以及长尾耗时分布如何。
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


LOW_SPEED_MIN = 1.0
LOW_SPEED_MAX = 1.5
HIGH_SPIN_MIN = 10.0


def action_band(action: Any) -> str:
    """返回审计分带；不是可行性或策略分类。"""
    if not isinstance(action, list) or len(action) < 3:
        return "未知"
    try:
        speed = math.hypot(float(action[0]), float(action[1]))
        spin = abs(float(action[2]))
    except (TypeError, ValueError):
        return "未知"
    if LOW_SPEED_MIN <= speed < LOW_SPEED_MAX and spin >= HIGH_SPIN_MIN:
        return "低速高旋"
    if LOW_SPEED_MIN <= speed < LOW_SPEED_MAX:
        return "低速其他旋转"
    return "其他"


def percentile(values: List[float], fraction: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(fraction * len(ordered)) - 1)]


def traces(report: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for container_name in ("game", "fullGame"):
        container = report.get(container_name)
        if not isinstance(container, dict):
            continue
        for item in container.get("trace", []):
            if isinstance(item, dict):
                yield item


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=Path("planning_proxy/runs"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows: List[Dict[str, Any]] = []
    unreadable: List[str] = []
    for path in sorted(args.runs.glob("*.json")):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            unreadable.append(path.name)
            continue
        for trace in traces(report):
            detail = trace.get("detail")
            if not isinstance(detail, dict):
                continue
            search = detail.get("strictGlobalSearch")
            if not isinstance(search, dict) or not search.get("strictEvaluationCalls", 0):
                continue
            slow = search.get("slowestStrictEvaluation")
            if not isinstance(slow, dict):
                slow = {}
            rows.append(
                {
                    "sourceReport": path.name,
                    "shot": trace.get("shot"),
                    "mode": detail.get("mode"),
                    "submittedAction": trace.get("bestshot"),
                    "submittedBand": action_band(trace.get("bestshot")),
                    "submittedFallback": detail.get("fallback"),
                    "strictEvaluationCalls": search.get("strictEvaluationCalls"),
                    "strictEvaluationSecondsTotal": search.get("strictEvaluationSecondsTotal"),
                    "strictEvaluationSecondsMax": search.get("strictEvaluationSecondsMax"),
                    "slowestAction": slow.get("bestshot"),
                    "slowestBand": action_band(slow.get("bestshot")),
                    "slowestSeconds": slow.get("elapsedSeconds"),
                }
            )

    maxima = [float(row["strictEvaluationSecondsMax"]) for row in rows
              if isinstance(row.get("strictEvaluationSecondsMax"), (int, float))]
    slow_low_high = [row for row in rows if row["slowestBand"] == "低速高旋"]
    submitted_low_high = [row for row in rows if row["submittedBand"] == "低速高旋"]
    output = {
        "schema": "strict_global_tail_audit_v1",
        "scope": {
            "runsDirectory": str(args.runs),
            "reportFilesRead": len(list(args.runs.glob("*.json"))),
            "unreadableReports": unreadable,
            "classification": {
                "lowSpeedMin": LOW_SPEED_MIN,
                "lowSpeedMaxExclusive": LOW_SPEED_MAX,
                "highSpinAbsMin": HIGH_SPIN_MIN,
            },
            "limitation": "只读历史记录；未覆盖的候选和未完成搜索不能据此断言无解。",
        },
        "summary": {
            "strictSearchRows": len(rows),
            "slowestBandCounts": dict(Counter(row["slowestBand"] for row in rows)),
            "submittedBandCounts": dict(Counter(row["submittedBand"] for row in rows)),
            "slowestLowSpeedHighSpinRows": len(slow_low_high),
            "submittedLowSpeedHighSpinRows": len(submitted_low_high),
            "strictMaxSeconds": {
                "median": percentile(maxima, 0.5),
                "p95": percentile(maxima, 0.95),
                "max": max(maxima) if maxima else None,
            },
        },
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
