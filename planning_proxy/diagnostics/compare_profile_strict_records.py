"""Compare every strict candidate outcome in two chooser-profile reports.

Timing is intentionally excluded.  The tool is diagnostic-only and never
loads the planner or writes production state-machine code.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _key(record: Dict[str, Any]) -> str:
    return json.dumps(
        {
            "contract": record.get("contract"),
            "bestshot": record.get("bestshot"),
            "physicsSeeds": record.get("physicsSeeds"),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _outcome(record: Dict[str, Any]) -> str:
    return json.dumps(
        record.get("outcome"), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _records(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("strictEvaluationSummary")
    if not isinstance(records, list):
        raise ValueError(f"{path}: missing strictEvaluationSummary")
    return records


def _group(records: Iterable[Dict[str, Any]]) -> Dict[str, List[str]]:
    grouped: Dict[str, List[str]] = defaultdict(list)
    for record in records:
        grouped[_key(record)].append(_outcome(record))
    for values in grouped.values():
        values.sort()
    return dict(grouped)


def main() -> None:
    parser = argparse.ArgumentParser(description="逐条比较两份完整选择器报告中的严格候选物理结果。")
    parser.add_argument("--left", required=True)
    parser.add_argument("--right", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    left_path, right_path = Path(args.left), Path(args.right)
    left, right = _group(_records(left_path)), _group(_records(right_path))
    keys = sorted(set(left) | set(right))
    missing_left = [key for key in keys if key not in left]
    missing_right = [key for key in keys if key not in right]
    different = [
        {"key": json.loads(key), "leftOutcomes": left[key], "rightOutcomes": right[key]}
        for key in keys
        if key in left and key in right and Counter(left[key]) != Counter(right[key])
    ]
    result = {
        "schema": "chooser_profile_strict_record_comparison_v1",
        "left": str(left_path),
        "right": str(right_path),
        "leftRecordCount": sum(len(values) for values in left.values()),
        "rightRecordCount": sum(len(values) for values in right.values()),
        "leftUniqueCandidateCount": len(left),
        "rightUniqueCandidateCount": len(right),
        "semanticEqual": not missing_left and not missing_right and not different,
        "missingOnLeft": [json.loads(key) for key in missing_left],
        "missingOnRight": [json.loads(key) for key in missing_right],
        "differentOutcomes": different,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"semanticEqual": result["semanticEqual"], "leftRecords": result["leftRecordCount"], "rightRecords": result["rightRecordCount"], "differences": len(different), "missingLeft": len(missing_left), "missingRight": len(missing_right)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
