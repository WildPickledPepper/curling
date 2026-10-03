"""Check that the targeted Unity capture and local boundary replay are comparable.

Read-only; exits nonzero if the recorded causal argument no longer holds.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_SAMPLES = ROOT / "research_archive/unity_reverse/evidence/data/calibration/extended_collision_validation_20260715_ordered/collision_unique_targets_batch_r03.jsonl"
OLD_EVENTS = ROOT / "research_archive/unity_reverse/evidence/log/extended_collision_validation_20260715_ordered/collision_unique_targets_batch_r03/unity_runtime_probe_20260715_125420/events.jsonl"
NEW = ROOT / "analysis_input/unity_12011_first_solver_poll_long_20260929"
BASE = ROOT / "analysis_input/simulator_alignment_12011_trace_audit_20260929_frame12_none_pre_none.json"
CHECKPOINT = ROOT / "analysis_input/simulator_alignment_12011_trace_audit_20260929_frame12_none_pre_all.json"
TRACE = ROOT / "analysis_input/simulator_alignment_12011_local_tail_20260929.json"
PRE = ROOT / "analysis_input/simulator_alignment_12011_local_tail_20260929_precontact.json"
DENSE = ROOT / "analysis_input/unity_12011_dense_setter_bridge_20260929"
ALIGNED = ROOT / "analysis_input/simulator_alignment_12011_trace_audit_20260929_frame12_none_pre_none_a10_all_production_alignment.json"
NO_ORACLE = ROOT / "analysis_input/simulator_alignment_12011_trace_audit_20260929_frame12_none_pre_none_production_alignment.json"
ALIGNED_INPUTS = ROOT / "analysis_input/simulator_alignment_12011_local_tail_20260929_a10_all_production_alignment_inputs.json"
ALIGNED_SETTERS = ROOT / "analysis_input/simulator_alignment_12011_local_tail_20260929_a10_all_production_alignment_setters.json"
BASE_RELEASE = ROOT / "analysis_input/simulator_alignment_12011_local_tail_20260929_release.json"


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def shot(report: Path) -> dict:
    return next(row for row in json.loads(report.read_text(encoding="utf-8"))["rows"]
                if row["sampleId"] == 12011)


def main() -> None:
    new_events = next((NEW / "logs").glob("*/events.jsonl"))
    old = rows(OLD_EVENTS)
    new = rows(new_events)
    old_friction = [e["data"]["value"] for e in old if e["type"] == "sliding.random_range.friction"]
    new_friction = [e["data"]["value"] for e in new if e["type"] == "sliding.random_range.friction"]
    assert len(old_friction) == len(new_friction) == 21538
    assert old_friction == new_friction
    old_samples, new_samples = rows(OLD_SAMPLES), rows(NEW / OLD_SAMPLES.name)
    assert len(old_samples) == len(new_samples) == 12
    assert all(x["sample_id"] == y["sample_id"] and
               x["after_position"] == y["after_position"]
               for x, y in zip(old_samples, new_samples))
    frames = [e["data"] for e in new if e["type"] == "c04.dynamic_solver_frame"]
    assert len(frames) == 40
    assert sum(e["type"] == "c03.first_dynamic_writeback" for e in new) == 1

    pre = json.loads(PRE.read_text(encoding="utf-8"))
    tail = json.loads(TRACE.read_text(encoding="utf-8"))
    assert len(pre) == 910 and len(tail) == 300
    u899 = frames[0]["exitCores"][1]["decodedCandidate"]
    l899 = pre[898]
    dx_m = l899["physxPosition"][0] - u899["p"][0]
    assert dx_m == 7.62939453125e-6
    assert l899["physxLinearVelocity"][0] == u899["linearVelocity"][0]
    u13_active = frames[13]["exitCores"][1]["decodedCandidate"]
    u13_target = frames[13]["exitCores"][0]["decodedCandidate"]
    l13 = tail[1]
    assert math.isclose(l13["active"]["physxLinearVelocity"][0] -
                        u13_active["linearVelocity"][0], -0.0004322528839111328,
                        rel_tol=0, abs_tol=1e-12)
    assert math.isclose(l13["target"]["physxAngularVelocity"][1] -
                        u13_target["angularVelocity"][1], 0.010856732726097107,
                        rel_tol=0, abs_tol=1e-12)

    base, corrected = shot(BASE), shot(CHECKPOINT)
    assert base["firstContactStep"] == corrected["firstContactStep"] == 910
    assert base["endpointErrorM"]["active"] > 0.019
    assert corrected["endpointErrorM"]["active"] < 0.00005
    assert corrected["endpointErrorM"]["target"] < 0.00005

    dense_events = rows(next((DENSE / "logs").glob("*/events.jsonl")))
    dense_pre = [e["data"] for e in dense_events if e["type"] == "a12.dense_pre_angular_setter"][1:]
    dense_post = [e["data"] for e in dense_events if e["type"] == "a12.dense_post_angular_setter"][1:]
    assert len(dense_pre) == len(dense_post) == 910
    aligned_inputs = json.loads(ALIGNED_INPUTS.read_text(encoding="utf-8"))
    aligned_setters = json.loads(ALIGNED_SETTERS.read_text(encoding="utf-8"))
    assert len(aligned_inputs) == len(aligned_setters) == 910
    original_release = json.loads(BASE_RELEASE.read_text(encoding="utf-8"))[0]
    unity_release = dense_pre[0]["pose"]["p"]
    assert original_release["physxPosition"][0] - unity_release[0] == 7.62939453125e-6
    assert math.isclose(original_release["physxPosition"][1] - unity_release[1],
                        -0.012615203857421875, abs_tol=1e-12)
    assert all(local["physxPosition"] == unity["pose"]["p"]
               for local, unity in zip(aligned_inputs, dense_pre))
    assert all(local["physxAngularVelocity"] == unity["bridge164"]
               for local, unity in zip(aligned_setters[:7], dense_post[:7]))
    assert aligned_setters[7]["physxAngularVelocity"][0] != dense_post[7]["bridge164"][0]
    aligned = shot(ALIGNED)
    no_oracle = shot(NO_ORACLE)
    assert aligned["endpointErrorM"]["active"] < 0.00005
    assert aligned["endpointErrorM"]["target"] < 0.00005
    assert no_oracle["endpointErrorM"]["active"] < 0.0005
    print(json.dumps({
        "sameFrictionCount": len(new_friction), "sameEndpointSamples": len(new_samples),
        "firstExactFrameStep": 899, "precontactNativeXDifferenceM": dx_m,
        "baselineErrorMm": {k: v * 1000 for k, v in base["endpointErrorM"].items()},
        "checkpointErrorMm": {k: v * 1000 for k, v in corrected["endpointErrorM"].items()},
        "checkpointIsDiagnosticOnly": True,
        "densePrecontactTicks": len(dense_pre),
        "positionExactTicksWithVerifiedInputs": sum(local["physxPosition"] == unity["pose"]["p"]
                                               for local, unity in zip(aligned_inputs, dense_pre)),
        "firstResidual": "tick 8 bridge angular X, 2.77555756e-17 rad/s",
        "verifiedInputEndpointErrorMm": {k: v * 1000 for k, v in aligned["endpointErrorM"].items()},
        "noOracle12011EndpointErrorMm": {k: v * 1000 for k, v in no_oracle["endpointErrorM"].items()},
        "a10OrientationTruthUsedByVerifiedInputReplay": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
