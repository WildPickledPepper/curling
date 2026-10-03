"""汇总当前与候选原生扩展的严格单候选探针结果。

只读取既有 ``extension_*_current_*.json`` 与对应的 candidate 报告；不执行物理、
不改状态机。这个统计用于检查候选扩展是否真正降低长尾，不能替代完整选择器、
多局或部署验证。
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable


def _quantile_nearest_rank(values: Iterable[float], percentile: float) -> float | None:
    ordered = sorted(values)
    if not ordered:
        return None
    index = max(0, math.ceil(percentile * len(ordered)) - 1)
    return ordered[index]


def _first_repeat_seconds(report: dict[str, Any]) -> float | None:
    for item in report.get("repeat", []):
        value = item.get("seconds") if isinstance(item, dict) else None
        if isinstance(value, (int, float)):
            return float(value)
    return None


def _stats(values: list[float]) -> dict[str, float | int | None]:
    return {
        "count": len(values),
        "meanSeconds": (sum(values) / len(values)) if values else None,
        "p95SecondsNearestRank": _quantile_nearest_rank(values, 0.95),
        "maxSeconds": max(values) if values else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, default=Path("planning_proxy/runs"))
    parser.add_argument("--suffix", default="20260724", help="报告文件名中的日期后缀")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    pattern = f"extension_*_current_{args.suffix}.json"
    rows: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for current_path in sorted(args.runs_dir.glob(pattern)):
        candidate_path = Path(str(current_path).replace("_current_", "_candidate_"))
        if not candidate_path.is_file():
            skipped.append({"current": str(current_path), "reason": "missing_candidate_report"})
            continue
        current = json.loads(current_path.read_text(encoding="utf-8"))
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        current_seconds = _first_repeat_seconds(current)
        candidate_seconds = _first_repeat_seconds(candidate)
        if current_seconds is None or candidate_seconds is None or candidate_seconds <= 0.0:
            skipped.append({"current": str(current_path), "reason": "missing_repeat_seconds"})
            continue
        stem = current_path.name.removeprefix("extension_").removesuffix(
            f"_current_{args.suffix}.json"
        )
        rows.append(
            {
                "case": stem,
                "currentReport": str(current_path),
                "candidateReport": str(candidate_path),
                "currentSeconds": current_seconds,
                "candidateSeconds": candidate_seconds,
                "speedup": current_seconds / candidate_seconds,
            }
        )

    current_values = [row["currentSeconds"] for row in rows]
    candidate_values = [row["candidateSeconds"] for row in rows]
    speedups = [row["speedup"] for row in rows]
    result = {
        "schema": "extension_probe_benchmark_summary_v1",
        "scope": (
            "read-only strict single-candidate probe timing summary; not a complete chooser, "
            "not a deployment decision, and not a state-machine result"
        ),
        "runsDirectory": str(args.runs_dir),
        "suffix": args.suffix,
        "cases": rows,
        "current": _stats(current_values),
        "candidate": _stats(candidate_values),
        "speedup": {
            "count": len(speedups),
            "mean": (sum(speedups) / len(speedups)) if speedups else None,
            "p95NearestRank": _quantile_nearest_rank(speedups, 0.95),
            "max": max(speedups) if speedups else None,
        },
        "skipped": skipped,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "caseCount": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
