"""Verify 11005's first raw-pose divergence using captured Unity/native data."""
from __future__ import annotations
import json
import sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene as Scene


def read_rows(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def main():
    out = ROOT / "analysis_input"
    archive = ROOT / "research_archive/unity_reverse/evidence"
    capture = out / "unity_11005_normalize_writer_20260930"
    events = read_rows(next((capture / "logs").glob("*/events.jsonl")))
    old_events = read_rows(archive / "log/c131_strict_yaw_r00_20260714/collision_unique_targets_batch_r00/unity_runtime_probe_20260714_173341/events.jsonl")
    noise = lambda rows: [e["data"]["value"] for e in rows if e["type"] == "sliding.random_range.friction"]
    assert noise(events) == noise(old_events) and len(noise(events)) == 15580
    old_samples = read_rows(archive / "data/calibration/c131_strict_yaw_r00_20260714/collision_unique_targets_batch_r00.jsonl")
    samples = read_rows(capture / "collision_unique_targets_batch_r00.jsonl")
    assert len(samples) == len(old_samples) == 12
    assert all(a["sample_id"] == b["sample_id"] and a["after_position"] == b["after_position"] for a, b in zip(samples, old_samples))
    pre = [e["data"] for e in events if e["type"] == "a12.dense_pre_angular_setter"]
    post = [e["data"] for e in events if e["type"] == "a12.dense_post_angular_setter"]
    phases = [e["data"] for e in events if e["type"] == "a12.early_phase_core"]
    local = json.loads((out / "c131_full-q_20260930.json").read_text(encoding="utf-8"))["releaseBoundary"][5]
    assert len(pre) == len(post) == len(local["setters"]) == 1023
    first_q = next(i for i, (u, l) in enumerate(zip(pre, local["setters"])) if u["pose"]["q"] != l["rawQuaternion"])
    first_w = next(i for i, (u, l) in enumerate(zip(post, local["setters"])) if u["bridge164"] != l["result"])
    assert first_q == first_w == 5
    tick = local["ticks"][3]
    local_exit = tick["solverPhases"][-1]["body_data"][0]["body2world"]["q"]
    phase = lambda name, edge: next(p for p in phases if p["ordinal"] == 5 and p["phase"] == name and p["edge"] == edge)
    solve_exit = phase("PxsDynamics.solverSetupSolve", "exit")["core"]["q"]
    writer_enter = phase("normalizeCandidate.121708", "enter")["core"]["q"]
    writer_exit = phase("normalizeCandidate.121708", "exit")["core"]["q"]
    assert local_exit == solve_exit == writer_enter == local["setters"][5]["rawQuaternion"]
    assert writer_exit == pre[5]["pose"]["q"]
    f = np.float32
    x, y, z, w = map(f, writer_enter)
    norm2 = f(f(f(f(x*x) + f(y*y)) + f(z*z)) + f(w*w))
    inv = f(f(1) / f(np.sqrt(norm2)))
    normalized = [float(f(v * inv)) for v in (x, y, z, w)]
    assert normalized == writer_exit
    # The historical diagnostic state() performs cast_transformation, hiding
    # the actual raw q difference. It is not a raw-body equality assertion.
    hidden = local["setters"][5]["before"]["quaternionWxyz"]
    assert [hidden[j] for j in (1, 2, 3, 0)] == writer_exit
    dummy = SimpleNamespace(probe=SimpleNamespace(np=np))
    q = np.asarray(writer_exit, dtype=np.float32)
    transform = q / np.sqrt(np.sum(q*q, dtype=np.float32))
    angular = pre[5]["setterAngular"][1]
    assert f(local["setters"][5]["scriptY"]) == f(angular)
    assert Scene._unity_project_locked_angular_velocity(dummy, transform, angular) == post[5]["bridge164"]
    synced = json.loads((out / "c131_full-q_sync_always_20260930.json").read_text(encoding="utf-8"))
    synced_trace = synced["releaseBoundary"][5]["setters"]
    synced_first = next(i for i, (u, l) in enumerate(zip(post, synced_trace)) if u["bridge164"] != l["result"])
    assert synced_first == 487
    row = next(r for r in synced["rows"] if r["sampleId"] == 11005)
    result = {
        "sample": 11005, "sameHistoricalEndpoints": 12, "sameHistoricalFrictionValues": 15580,
        "firstRawQuaternionMismatchSetterOrdinal": first_q + 1,
        "firstNativeAngularOutputMismatchSetterOrdinal": first_w + 1,
        "physicsStepProducingBoundary": 4,
        "unityWriter": "table[121708] -> wasm f72606",
        "sharedSolverExitQuaternion": solve_exit, "unityPostWriterQuaternion": writer_exit,
        "normalizationSquaredNorm": float(norm2), "normalizationInverseLength": float(inv),
        "localOldNativeAngularOutput": local["setters"][5]["result"],
        "unityNativeAngularOutput": post[5]["bridge164"],
        "oldStateReaderHidesRawDifference": True,
        "diagnosticPoseSyncFirstAngularOutputMismatchOrdinal": synced_first + 1,
        "diagnosticPoseSync11005EndpointErrorM": row["endpointErrorM"],
        "scope": "First divergence verified; diagnostic initial quaternion truth and pose-write replay are not an end-to-end solver repair.",
    }
    (out / "11005_first_divergence_verified_20260930.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
