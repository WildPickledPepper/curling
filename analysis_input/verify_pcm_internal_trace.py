"""Verify instrumentation against original Unity truth and matched-input PCM."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "analysis_input/unity_11005_step486_pcm_20261001"


def events(directory):
    paths = list(directory.glob("logs/*/events.jsonl"))
    if len(paths) != 1:
        raise ValueError(f"expected one event log in {directory}")
    return [json.loads(line) for line in paths[0].read_text(encoding="utf-8").splitlines()], paths[0]


def rows_of(rows, kind):
    return [row["data"] for row in rows if row["type"] == kind]


def geometry_points(buffer):
    return [{"point": p["point"], "normal": p["normal"], "separation": p["separation"],
             "internal_face_index1": p["internalFaceIndex1"]} for p in buffer["contactsPreview"]]


def verify_capture(directory):
    baseline, _ = events(BASELINE)
    captured, path = events(directory)
    errors = [row for row in captured if "failed" in row["type"]]
    assert not errors, errors[:2]
    friction = rows_of(captured, "sliding.random_range.friction")
    assert len(friction) == 15580
    assert friction == rows_of(baseline, "sliding.random_range.friction")
    for kind in ("a12.dense_pre_angular_setter", "a12.dense_post_angular_setter"):
        actual, expected = rows_of(captured, kind), rows_of(baseline, kind)
        assert len(actual) == len(expected) == 1023
        def strip_addresses(row):
            return {key: value for key, value in row.items() if key not in ("nativePtr", "bridgePtr", "tickSerial")}
        assert [strip_addresses(r) for r in actual] == [strip_addresses(r) for r in expected]
    phases = rows_of(captured, "a12.early_phase_core")
    old_phases = rows_of(baseline, "a12.early_phase_core")
    for row in phases:
        expected = next(r for r in old_phases if all(r[k] == row[k] for k in ("ordinal", "phase", "edge")))
        assert {k: v for k, v in row["core"].items() if k != "ptr"} == {
            k: v for k, v in expected["core"].items() if k != "ptr"}
    pcm = rows_of(captured, "a12.pcm_convex_mesh")
    old_pcm = rows_of(baseline, "a12.pcm_convex_mesh")
    for row in pcm:
        expected = next(r for r in old_pcm if r["ordinal"] == row["ordinal"])
        for edge in ("before", "after"):
            for key in ("transform0", "transform1"):
                assert row[edge][key] == expected[edge][key]
        assert row["after"]["contactBuffer"]["count"] == expected["after"]["contactBuffer"]["count"]
        assert geometry_points(row["after"]["contactBuffer"]) == geometry_points(expected["after"]["contactBuffer"])
    sample_path = next(directory.glob("collision*.jsonl"))
    baseline_sample_path = next(BASELINE.glob("collision*.jsonl"))
    samples = [json.loads(line) for line in sample_path.read_text(encoding="utf-8").splitlines()]
    old_samples = [json.loads(line) for line in baseline_sample_path.read_text(encoding="utf-8").splitlines()]
    assert len(samples) == len(old_samples) == 12
    physical_keys = ("sample_id", "after_position", "final_xy", "target_moves", "requested", "collision_observed")
    assert [{key: row[key] for key in physical_keys} for row in samples] == [
        {key: row[key] for key in physical_keys} for row in old_samples]
    return {"events": str(path), "eventsSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "frictionValuesEqual": 15580, "setterPairsEqual": 1023, "endpointsEqual": 12,
            "internalCallCount": len(rows_of(captured, "a12.pcm_internal_call")),
            "geometryScaleRecords": len(rows_of(captured, "a12.pcm_geometry_scale")),
            "geometryWriteRecords": len(rows_of(captured, "a12.geometry_write"))}


def raw_argument(row, arg, edge):
    return bytes.fromhex(next(r["hex"] for r in row[edge] if r["argument"] == arg))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--captures", nargs="+", type=Path, default=[
        ROOT / "analysis_input/unity_11005_pcm_internal_calls_20261001",
        ROOT / "analysis_input/unity_11005_pcm_candidate_calls_20261001",
        ROOT / "analysis_input/unity_pcm_geometry_scales_20261001",
        ROOT / "analysis_input/unity_geometry_writers_20261001"])
    parser.add_argument("--output", type=Path, default=ROOT / "analysis_input/pcm_internal_trace_verified_20261001.json")
    opts = parser.parse_args()
    validations = [verify_capture(directory) for directory in opts.captures]
    unity, _ = events(ROOT / "analysis_input/unity_11005_pcm_candidate_calls_20261001")
    unity_calls = rows_of(unity, "a12.pcm_internal_call")
    native_file = ROOT / "analysis_input/native_pcm_interceptor_20261001/calls.json"
    native = json.loads(native_file.read_text(encoding="utf-8"))
    assert native["callStackReliable"] and not native["unfinished"] and not native["dropped"]
    assert not any(row.get("stackMismatch") for row in native["calls"])
    native_report = json.loads(native_file.with_name("alignment.json").read_text(encoding="utf-8"))
    local_baseline = json.loads((ROOT / "analysis_input/c131_full-q_pcm_direct_verified_20261001.json").read_text(encoding="utf-8"))
    assert native_report["aggregate"] == local_baseline["aggregate"]
    assert native_report["rows"] == local_baseline["rows"]
    unity_geometry = next(r for r in unity_calls if r["functionIndex"] == 70031)
    native_geometry = next(r for r in native["calls"] if r["functionRva"] == "0x3beef0")
    unity_scale = list(struct.unpack_from("<3f", raw_argument(unity_geometry, 0, "before"), 4))
    native_scale = list(struct.unpack_from("<3f", raw_argument(native_geometry, 0, "before"), 4))
    assert unity_scale == [0.11270000040531158, 0.11500000208616257, 0.11270000040531158]
    assert native_scale == [0.11270000785589218, 0.11500000208616257, 0.11270000785589218]
    corrected_report = json.loads((ROOT / "analysis_input/c131_matched_geometry_input_20261001.json").read_text(encoding="utf-8"))
    assert corrected_report["aggregate"] == local_baseline["aggregate"]
    assert corrected_report["rows"] == local_baseline["rows"]
    boundary = next(r for r in corrected_report["releaseBoundary"] if r["sampleId"] == 11005)
    old_unity, _ = events(BASELINE)
    for query in boundary["directContacts"]:
        ordinal = query["ordinal"]
        truth = next(r for r in rows_of(old_unity, "a12.pcm_convex_mesh") if r["ordinal"] == ordinal)
        expected = geometry_points(truth["after"]["contactBuffer"])
        actual = [{key: point[key] for key in expected[0]}
                  for point in query["matchedInputGeometryProbe"]["points"]]
        assert actual == expected, ordinal
        assert query["result"]["input_transform0"] == query["matchedInputGeometryProbe"]["input_transform0"]
        assert query["result"]["input_transform1"] == query["matchedInputGeometryProbe"]["input_transform1"]
    scale_events, _ = events(ROOT / "analysis_input/unity_pcm_geometry_scales_20261001")
    active_scales = [r for r in rows_of(scale_events, "a12.pcm_geometry_scale") if r["transform0"]["p"][0] < -90]
    assert len(active_scales) == 12
    result = {"captureValidations": validations,
              "nativeModuleSha256": native["moduleSha256"], "nativeInternalCalls": len(native["calls"]),
              "unityScale": unity_scale, "nativeScale": native_scale,
              "matchedInputQueriesGeometricFieldsExact": [r["ordinal"] for r in boundary["directContacts"]],
              "mainSceneTrajectoryUnchanged": True,
              "activeScalePerRelease": [{"sampleId": 11000 + r["releaseSerial"] // 2 - 1,
                                         "scale": r["scale"], "initialQuaternion": r["transform0"]["q"]}
                                        for r in active_scales],
              "limitation": "This verifies identical-input PCM geometry, not trajectory alignment. The scale writer and calculation are separately verified in recovered_transform_scale_verified_20261001.json; live shape refresh is pending."}
    opts.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"capturesVerified": len(validations), "nativeCalls": len(native["calls"]),
                      "matchedInputOrdinals": result["matchedInputQueriesGeometricFieldsExact"],
                      "observedActiveScales": len(Counter(tuple(r["scale"]) for r in active_scales))}))


if __name__ == "__main__":
    main()
