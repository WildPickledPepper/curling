"""Audit local endpoint errors against repeated fresh-Unity distributions.

Each input is an output directory produced by
``run_unity_collision_batch_matrix.py``.  A body is a deterministic-model
candidate only when it is observed in every fresh session, is outside the
Unity 2-D restart envelope, and its error exceeds the configured threshold in
every session.  Cleared Unity stones are excluded rather than interpreted as
the physical coordinate (0, 0).
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


def canonical_label(label: str) -> str:
    return re.sub(r"_r\d\d$", "", label)


def is_cleared(point: Any) -> bool:
    return isinstance(point, list) and len(point) == 2 and point == [0.0, 0.0]


def distance_outside_box(point: list[float], points: list[list[float]]) -> float:
    lower = [min(item[axis] for item in points) for axis in range(2)]
    upper = [max(item[axis] for item in points) for axis in range(2)]
    delta = [max(lower[axis] - point[axis], 0.0, point[axis] - upper[axis]) for axis in range(2)]
    return math.hypot(*delta)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=Path, action="append", required=True, help="Matrix output root; repeat once per fresh Unity process.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--threshold-m", type=float, default=0.020)
    args = parser.parse_args()

    by_label: dict[str, dict[str, Any]] = {}
    session_names: list[str] = []
    for root in args.session:
        summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
        batch = next(item for item in summary["batches"] if item.get("status") == "ok")
        audit = json.loads(Path(batch["endpointAudit"]).read_text(encoding="utf-8"))["rows"]
        samples = [json.loads(line) for line in Path(batch["sample"]).read_text(encoding="utf-8").splitlines() if line.strip()]
        name = root.name
        session_names.append(name)
        for sample, row in zip(samples, audit):
            label = canonical_label(row["label"])
            entry = by_label.setdefault(label, {"label": label, "category": sample["category"], "bodies": {}})
            for body in ("active", "target"):
                unity = row["unityEndpoint"].get(body)
                local = row["localEndpoint"].get(body)
                error = row["endpointErrorM"].get(body)
                if unity is None or local is None or error is None or is_cleared(unity):
                    continue
                entry["bodies"].setdefault(body, []).append({"session": name, "unity": unity, "local": local, "error_m": error})

    candidates: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for label, entry in by_label.items():
        for body, observations in entry["bodies"].items():
            unity_points = [item["unity"] for item in observations]
            outside = [distance_outside_box(item["local"], unity_points) for item in observations]
            errors = [item["error_m"] for item in observations]
            result = {
                "label": label,
                "category": entry["category"],
                "body": body,
                "validSessions": len(observations),
                "unityRestartRangeM": max(math.dist(left, right) for index, left in enumerate(unity_points) for right in unity_points[index:]),
                "localErrorMinM": min(errors),
                "localErrorMaxM": max(errors),
                "localOutsideUnityEnvelopeMaxM": max(outside),
                "persistentDeterministicCandidate": (
                    len(observations) == len(session_names)
                    and min(errors) > args.threshold_m
                    and max(outside) > args.threshold_m
                ),
            }
            rows.append(result)
            if result["persistentDeterministicCandidate"]:
                candidates.append(result)

    result = {
        "schema": "restart_endpoint_distribution_audit_v1",
        "sessions": session_names,
        "thresholdM": args.threshold_m,
        "criterion": "valid in every session AND every local error above threshold AND local endpoint outside Unity restart envelope above threshold",
        "rows": rows,
        "persistentDeterministicCandidates": candidates,
        "accepted": not candidates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"accepted": result["accepted"], "candidateCount": len(candidates), "rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
