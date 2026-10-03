#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量复现代表性真实 fallback/慢决策壶面，输出当前选择器结果。

输入样本仅来自 ``representative_failure_corpus``。每个样本在独立 CP39 子进程中
调用 ``profile_k6_search.py``，因此不会把一个样本的 PhysX 场景或计时包装泄漏到
下一个样本。它不修改状态机、不声称无解，也不执行后续对局。

默认只运行一个样本；全部 41 个历史难例必须显式传 ``--all``，以免在单 CPU 上
误启动很长的批量任务。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILE_SCRIPT = PROJECT_ROOT / "planning_proxy" / "diagnostics" / "profile_k6_search.py"
DEFAULT_CORPUS = PROJECT_ROOT / "planning_proxy" / "diagnostics" / "representative_failure_corpus_v3_20260724.json"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output", type=Path, required=True, help="批量索引报告 JSON")
    parser.add_argument("--reports-dir", type=Path, required=True, help="每个样本的 profile JSON 目录")
    parser.add_argument("--case-id", action="append", help="指定样本编号；可重复传入")
    parser.add_argument("--all", action="store_true", help="显式运行语料库中的全部样本")
    parser.add_argument("--max-cases", type=int, default=1, help="未使用 --all 时的最大样本数，默认 1")
    parser.add_argument("--budget", type=float, default=105.0)
    parser.add_argument("--physics-seeds", type=int, default=3)
    parser.add_argument(
        "--strict-tail-reserve",
        type=float,
        help="仅转交给诊断 profile 的严格候选尾部余量；不改生产常量。",
    )
    parser.add_argument("--extension", type=Path, help="只为本批临时加载候选 CP39 .pyd")
    parser.add_argument("--timeout-margin", type=float, default=25.0, help="每个子进程相对预算的额外等待秒数")
    return parser.parse_args()


def _select_cases(corpus: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    all_cases = corpus.get("candidateTestCases")
    if not isinstance(all_cases, list):
        raise SystemExit("语料库缺少 candidateTestCases")
    requested = set(args.case_id or [])
    if requested:
        selected = [case for case in all_cases if str(case.get("id")) in requested]
        found = {str(case.get("id")) for case in selected}
        missing = sorted(requested - found)
        if missing:
            raise SystemExit(f"语料库不存在样本：{', '.join(missing)}")
        return selected
    if args.all:
        return all_cases
    if args.max_cases < 1:
        raise SystemExit("--max-cases 必须大于 0")
    return all_cases[: args.max_cases]


def _last_json_line(stdout: str) -> dict[str, Any] | None:
    for line in reversed(stdout.splitlines()):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def _run_case(case: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    case_id = str(case["id"])
    source = PROJECT_ROOT / str(case["source"])
    report_path = args.reports_dir / f"case_{case_id}.json"
    record: dict[str, Any] = {
        "id": case_id,
        "source": str(source),
        "shot": int(case["shot"]),
        "semantic": case.get("semantic"),
        "historicalObservation": case.get("historicalObservation"),
        "report": str(report_path),
    }
    if not source.is_file():
        record.update(status="source_missing")
        return record
    command = [
        sys.executable,
        str(PROFILE_SCRIPT),
        "--source", str(source),
        "--shot", str(case["shot"]),
        "--budget", str(args.budget),
        "--physics-seeds", str(args.physics_seeds),
        "--summary",
        "--output", str(report_path),
    ]
    if args.extension is not None:
        command += ["--extension", str(args.extension.resolve())]
    if args.strict_tail_reserve is not None:
        command += ["--strict-tail-reserve", str(args.strict_tail_reserve)]
    try:
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            timeout=args.budget + args.timeout_margin,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        record.update(status="subprocess_timeout", timeoutSeconds=args.budget + args.timeout_margin, stdout=exc.stdout)
        return record
    summary = _last_json_line(completed.stdout)
    record.update(
        status="ok" if completed.returncode == 0 and summary is not None else "subprocess_error",
        returnCode=completed.returncode,
        stdout=completed.stdout[-2000:],
        stderr=completed.stderr[-2000:],
        summary=summary,
    )
    return record


def main() -> None:
    args = _parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    cases = _select_cases(corpus, args)
    args.reports_dir.mkdir(parents=True, exist_ok=True)
    results = [_run_case(case, args) for case in cases]
    ok = [item for item in results if item["status"] == "ok"]
    result = {
        "schema": "representative_failure_corpus_evaluation_v1",
        "scope": (
            "current strict chooser replay on historical boards; no state-machine change, no proof of solvability, "
            "and no full-game value conclusion"
        ),
        "corpus": str(args.corpus),
        "budgetSeconds": args.budget,
        "physicsSeeds": args.physics_seeds,
        "extension": str(args.extension.resolve()) if args.extension else None,
        "selectedCaseCount": len(cases),
        "okCount": len(ok),
        "statusCounts": {status: sum(item["status"] == status for item in results) for status in sorted({item["status"] for item in results})},
        "cases": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "selected": len(cases), "ok": len(ok)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
