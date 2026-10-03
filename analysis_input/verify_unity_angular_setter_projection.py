"""Verify the opt-in native angular setter against two dense Unity captures."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


ROOT = Path(__file__).resolve().parent
CAPTURES = (
    ("highcurl", ROOT / "unity_12008_two_pose_setter_20260929", 1283),
    ("lowcurl", ROOT / "unity_12011_dense_setter_bridge_20260929", 911),
)


def verify(label: str, capture: Path, expected_count: int) -> dict[str, int | str]:
    event_files = list((capture / "logs").glob("*/events.jsonl"))
    if len(event_files) != 1:
        raise AssertionError(f"{label}: expected one events.jsonl, found {event_files}")
    rows: dict[int, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    tracked = {
        "a12.angular_setter_two_pose_inputs",
        "a12.dense_pre_angular_setter",
        "a12.dense_post_angular_setter",
    }
    with event_files[0].open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            if event["type"] in tracked:
                payload = event["data"]
                rows[payload["ordinal"]][event["type"]].append(payload)

    if len(rows) != expected_count:
        raise AssertionError(f"{label}: {len(rows)} setters, expected {expected_count}")
    scene = SimpleNamespace(probe=SimpleNamespace(np=np))
    exact_projection = 0
    exact_transform_reconstruction = 0
    for ordinal in sorted(rows):
        row = rows[ordinal]
        pre = row["a12.dense_pre_angular_setter"][0]
        post = row["a12.dense_post_angular_setter"][0]
        body_q = np.asarray(pre["pose"]["q"], dtype=np.float32)
        transform_q = body_q
        if ordinal >= 3:
            transform_q = body_q / np.sqrt(np.sum(body_q * body_q, dtype=np.float32))
        getter = row.get("a12.angular_setter_two_pose_inputs")
        if getter:
            captured_q = np.asarray(getter[0]["transformPose"]["q"], dtype=np.float32)
            relative_q = getter[0]["bridgePose"]["q"]
            if relative_q != [0, 0, 0, 1]:
                raise AssertionError(f"{label} setter {ordinal}: relative quaternion is not identity")
            if np.array_equal(transform_q, captured_q):
                exact_transform_reconstruction += 1
            else:
                raise AssertionError(f"{label} setter {ordinal}: Transform quaternion differs")
        projected = PersistentPhysxFrontHalfScene._unity_project_locked_angular_velocity(
            scene, tuple(transform_q), pre["setterAngular"][1]
        )
        if projected == post["bridge164"]:
            exact_projection += 1
        else:
            raise AssertionError(f"{label} setter {ordinal}: {projected} != {post['bridge164']}")
    return {
        "capture": label,
        "setters": len(rows),
        "exact_projection": exact_projection,
        "exact_transform_reconstruction": exact_transform_reconstruction,
    }


if __name__ == "__main__":
    print(json.dumps([verify(*item) for item in CAPTURES], indent=2))
