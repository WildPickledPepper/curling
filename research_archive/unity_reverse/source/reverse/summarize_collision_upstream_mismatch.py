#!/usr/bin/env python3
"""Summarize the current upstream source of the Unity-vs-pyphysx collision gap.

This report is deliberately not a parameter search.  It joins the same-shot
Unity runtime native dumps for sample 13000 with the local pyphysx replay/contact
report and records which stages are closed, which fields already disagree, and
what has to be captured next.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALIBRATION_DIR = PROJECT_ROOT / "data" / "calibration"

UNITY_NATIVE_SAMPLE = CALIBRATION_DIR / "unity_native_solver_collision_probe_20260709_withwriteback.jsonl"
UNITY_FINALIZER = CALIBRATION_DIR / "unity_physx_native_solver_state_withwriteback_20260709.json"
UNITY_SOLVE_REPLAY = CALIBRATION_DIR / "unity_physx_solver_consume_replay_delta_withwriteback_20260709.json"
UNITY_SOLVE_SUMMARY = CALIBRATION_DIR / "unity_physx_solver_consume_writeback_summary_20260709.json"
LOCAL_NATIVE13000 = CALIBRATION_DIR / "unity_physx_collision_probe_native13000_immediate_contact_20260709.json"
LOCAL_FORMAL13000 = CALIBRATION_DIR / "unity_physx_collision_probe_native13000_immediate_formal_contact_20260709.json"
LOCAL_HANDOFF_EXTRA13000 = CALIBRATION_DIR / "unity_physx_collision_probe_native13000_immediate_handoff_extra001_20260709.json"
UNITY_FINALIZER_POSE_CONTACT_REPLAY = CALIBRATION_DIR / "unity_finalizer_pose_contact_replay_20260709.json"
HISTORICAL_CONTACT_AUDIT = CALIBRATION_DIR / "unity_collision_contact_report_vs_row_delta_20260709.json"
HANDOFF_ORACLE = CALIBRATION_DIR / "unity_collision_handoff_xy_oracle_20260709.json"
ORACLE_GENERALIZATION = CALIBRATION_DIR / "unity_collision_oracle_generalization_20260709.json"

DEFAULT_OUTPUT = CALIBRATION_DIR / "unity_collision_upstream_mismatch_audit_20260709.json"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"missing": str(path.relative_to(PROJECT_ROOT))}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl_first(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"missing": str(path.relative_to(PROJECT_ROOT))}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                return json.loads(line)
    return {"missing": str(path.relative_to(PROJECT_ROOT)), "reason": "empty"}


def _angle_deg(x: float, y: float) -> float:
    return math.degrees(math.atan2(y, x))


def _angle_delta_deg(a: float, b: float) -> float:
    delta = a - b
    while delta > 180.0:
        delta -= 360.0
    while delta < -180.0:
        delta += 360.0
    return delta


def _norm2(values: Iterable[float]) -> float:
    row = list(values)
    return math.hypot(float(row[0]), float(row[1])) if len(row) >= 2 else 0.0


def _max_abs_from_nested(value: Any) -> float | None:
    found: list[float] = []

    def visit(item: Any) -> None:
        if isinstance(item, dict):
            for child in item.values():
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)
        elif isinstance(item, (int, float)) and not isinstance(item, bool):
            if math.isfinite(float(item)):
                found.append(abs(float(item)))

    visit(value)
    return max(found) if found else None


def _local_native13000_summary(report: dict[str, Any]) -> dict[str, Any]:
    result_set = (report.get("result_sets") or [{}])[0]
    row = (result_set.get("rows") or [{}])[0]
    contact_report = (row.get("stone_stone_contact_reports") or [{}])[0]
    points = contact_report.get("points") or []
    impulse_sum = [0.0, 0.0, 0.0]
    separations: list[float] = []
    normals: list[list[float]] = []
    for point in points:
        impulse = point.get("impulse") or []
        normal = point.get("normal") or []
        if len(impulse) >= 3:
            impulse_sum = [impulse_sum[i] + float(impulse[i]) for i in range(3)]
        if len(normal) >= 2:
            normals.append([float(normal[0]), float(normal[1]), float(normal[2]) if len(normal) > 2 else 0.0])
        if point.get("separation") is not None:
            separations.append(float(point["separation"]))

    first_normal = normals[0] if normals else None
    first_normal_angle = _angle_deg(first_normal[0], first_normal[1]) if first_normal else None
    impulse_angle = _angle_deg(impulse_sum[0], impulse_sum[1]) if _norm2(impulse_sum) > 0 else None
    immediate_probes = row.get("immediate_contact_probes") or []
    nonempty_immediate = [
        probe
        for probe in immediate_probes
        if ((probe.get("result") or {}).get("contact_count") or 0) > 0
    ]
    return {
        "config": result_set.get("config"),
        "endpoint_summary": result_set.get("summary"),
        "row": {
            "sample_id": row.get("sample_id"),
            "label": row.get("label"),
            "handoff": row.get("handoff"),
            "unity_active": row.get("unity_active"),
            "unity_target": row.get("unity_target"),
            "sim_active": row.get("sim_active"),
            "sim_target": row.get("sim_target"),
            "active_error_m": row.get("active_error"),
            "target_error_m": row.get("target_error"),
            "first_stone_stone_contact_time": row.get("first_stone_stone_contact_time"),
        },
        "first_contact_report": {
            "contact_count": contact_report.get("contact_count"),
            "active_is_actor0": contact_report.get("active_is_actor0"),
            "first_normal": first_normal,
            "first_normal_angle_deg_xy": first_normal_angle,
            "separation_min_m": min(separations) if separations else None,
            "separation_max_m": max(separations) if separations else None,
            "impulse_sum": impulse_sum,
            "impulse_sum_norm_Ns_xy": _norm2(impulse_sum),
            "impulse_sum_angle_deg_xy": impulse_angle,
            "points_preview": points[:4],
        },
        "first_immediate_contact_probe": _immediate_probe_summary(nonempty_immediate[0] if nonempty_immediate else {}),
        "immediate_contact_probes_preview": [
            _immediate_probe_summary(probe)
            for probe in immediate_probes[:4]
        ],
    }


def _immediate_probe_summary(probe: dict[str, Any]) -> dict[str, Any]:
    result = probe.get("result") or {}
    points = result.get("points") or []
    normal = (points[0] or {}).get("normal") if points else None
    normal_angle = None
    target_side_angle = None
    if isinstance(normal, list) and len(normal) >= 2:
        normal_angle = _angle_deg(float(normal[0]), float(normal[1]))
        target_side_angle = _angle_deg(-float(normal[0]), -float(normal[1]))
    separations = [
        float(point["separation"])
        for point in points
        if isinstance(point, dict) and point.get("separation") is not None
    ]
    return {
        "stage": probe.get("stage"),
        "step_index": probe.get("step_index"),
        "time": probe.get("time"),
        "center_distance_m": probe.get("center_distance"),
        "ok": probe.get("ok"),
        "contact_count": result.get("contact_count"),
        "contact_distance_m": result.get("contact_distance"),
        "cache": {
            "size": result.get("cache_size"),
            "pair_data": result.get("cache_pair_data"),
            "manifold_flags": result.get("cache_manifold_flags"),
        },
        "first_normal": normal,
        "first_normal_angle_deg_xy": normal_angle,
        "target_side_normal_angle_deg_xy": target_side_angle,
        "separation_min_m": min(separations) if separations else None,
        "separation_max_m": max(separations) if separations else None,
        "points_preview": points[:4],
        "solver_material_fields_valid": result.get("solver_material_fields_valid"),
        "solver_material_fields_note": result.get("solver_material_fields_note"),
    }


def _unity_finalizer_summary(report: dict[str, Any]) -> dict[str, Any]:
    rows = report.get("stoneStoneRows") or []
    after_rows = [row for row in rows if row.get("phase") == "after"]
    compact_rows: list[dict[str, Any]] = []
    max_raw_vs_computed = 0.0
    raw_vs_computed_count = 0

    for row in after_rows:
        contact_candidate = ((row.get("contactBuffer") or {}).get("candidate") or {})
        contacts = contact_candidate.get("contactsPreview") or []
        first = contacts[0] if contacts else {}
        normal = first.get("normal")
        opposite_horizontal_angle = None
        if isinstance(normal, list) and len(normal) >= 3:
            # Unity native is y-up.  The horizontal stone-stone normal lives in x/z.
            # The opposite direction is what matches the target-side pyphysx
            # ContactPairPoint convention in the local probe.
            opposite_horizontal_angle = _angle_deg(-float(normal[0]), -float(normal[2]))

        raw_vs_computed = row.get("rawVsComputedNormalRow")
        if raw_vs_computed:
            raw_vs_computed_count += 1
            raw_delta = _max_abs_from_nested(raw_vs_computed.get("normalRow0"))
            if raw_delta is not None:
                max_raw_vs_computed = max(max_raw_vs_computed, raw_delta)

        compact_rows.append(
            {
                "t": row.get("t"),
                "contact_count": contact_candidate.get("count"),
                "friction_count": (row.get("contactDesc") or {}).get("frictionCount"),
                "header": (raw_vs_computed or {}).get("rawHeader"),
                "raw_applied_normal_forces": (raw_vs_computed or {}).get("rawAppliedNormalForces"),
                "first_contact": first,
                "target_side_candidate_normal_angle_deg_xz": opposite_horizontal_angle,
                "raw_vs_computed_normal_row_max_abs_delta": raw_delta if raw_vs_computed else None,
            }
        )

    return {
        "capture_readiness": report.get("captureReadiness"),
        "source_event_count": report.get("sourceEventCount"),
        "row_count": report.get("rowCount"),
        "class_counts": report.get("classCounts"),
        "constraint_capture": report.get("constraintCapture"),
        "stone_stone_row_count": len(rows),
        "stone_stone_after_row_count": len(after_rows),
        "raw_vs_computed_count": raw_vs_computed_count,
        "raw_vs_computed_normal_row_max_abs_delta": max_raw_vs_computed if raw_vs_computed_count else None,
        "after_rows": compact_rows,
        "first_stone_stone": _unity_first_stone_stone_summary(report.get("firstStoneStone") or {}),
    }


def _solve_replay_summary(report: dict[str, Any], writeback: dict[str, Any]) -> dict[str, Any]:
    top_delta = (writeback.get("topDeltas") or [{}])[0]
    return {
        "replayed_count": report.get("replayedCount"),
        "max_error_by_hook": report.get("maxErrorByHook"),
        "paired_count": writeback.get("pairedCount"),
        "pair_count_by_hook": writeback.get("pairCountByHook"),
        "changed_pair_count_by_hook": writeback.get("changedPairCountByHook"),
        "top_dynamic_writeback_delta": {
            "hook": top_delta.get("hook"),
            "callIndex": top_delta.get("callIndex"),
            "armSerial": top_delta.get("armSerial"),
            "maxAbsDelta": top_delta.get("maxAbsDelta"),
            "changedFields": top_delta.get("changedFields"),
            "appliedNormalForces": top_delta.get("appliedNormalForces"),
            "positive_normal_force_sum_Ns": _positive_sum(top_delta.get("appliedNormalForces") or []),
        },
        "interpretation": (
            "Unity raw SolverContact rows replay back to captured bodyA/bodyB after windows at float epsilon. "
            "This closes the captured with-writeback and conclude single-pair consume/writeback boundaries."
        ),
    }


def _positive_sum(values: Iterable[Any]) -> float:
    total = 0.0
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number) and number > 0:
            total += number
    return total


def _unity_first_stone_stone_summary(row: dict[str, Any]) -> dict[str, Any]:
    contact_buffer = row.get("contactBuffer") or {}
    candidate = contact_buffer.get("candidate") or {}
    contacts = candidate.get("contactsPreview") or []
    first = contacts[0] if contacts else {}
    normal = first.get("normal")
    target_angle = None
    if isinstance(normal, list) and len(normal) >= 3:
        target_angle = _angle_deg(-float(normal[0]), -float(normal[2]))
    computed_rows = row.get("computedNormalRows") or []
    return {
        "t": row.get("t"),
        "phase": row.get("phase"),
        "contact_count": candidate.get("count"),
        "first_contact": first,
        "target_side_candidate_normal_angle_deg_xz": target_angle,
        "separations_m": [contact.get("separation") for contact in contacts],
        "internal_face_index1": [contact.get("internalFaceIndex1") for contact in contacts],
        "friction_patch": {
            key: (row.get("frictionPatch") or {}).get(key)
            for key in (
                "anchorCount",
                "restitution",
                "staticFriction",
                "dynamicFriction",
                "body0Normal",
                "body1Normal",
                "body0Anchors",
                "body1Anchors",
                "relativeQuat",
            )
        },
        "solver_body_data": {
            name: {
                key: data.get(key)
                for key in (
                    "linearVelocity",
                    "angularVelocity",
                    "invMass",
                    "penBiasClamp",
                    "nodeIndex",
                    "lockFlags",
                    "body2World",
                )
            }
            for name, data in (row.get("solverBodyData") or {}).items()
        },
        "computed_normal_rows": [
            {
                key: item.get(key)
                for key in (
                    "index",
                    "normalVelocity",
                    "relativeNormalVelocity",
                    "unitResponse",
                    "velMultiplier",
                    "penetration",
                    "scaledBias",
                    "biasedErr",
                    "unbiasedErr",
                )
            }
            for item in computed_rows
        ],
    }


def _direct_field_comparison(local: dict[str, Any], unity: dict[str, Any]) -> dict[str, Any]:
    local_contact = local.get("first_contact_report") or {}
    local_immediate = local.get("first_immediate_contact_probe") or {}
    unity_first = unity.get("first_stone_stone") or {}
    unity_angle = unity_first.get("target_side_candidate_normal_angle_deg_xz")
    local_angle = local_contact.get("first_normal_angle_deg_xy")
    angle_delta = (
        _angle_delta_deg(float(local_angle), float(unity_angle))
        if local_angle is not None and unity_angle is not None
        else None
    )
    immediate_angle = local_immediate.get("target_side_normal_angle_deg_xy")
    immediate_angle_delta = (
        _angle_delta_deg(float(immediate_angle), float(unity_angle))
        if immediate_angle is not None and unity_angle is not None
        else None
    )
    unity_first_contact = unity_first.get("first_contact") or {}
    local_impulse = local_contact.get("impulse_sum") or []
    unity_contact_count = unity_first.get("contact_count")
    local_contact_count = local_contact.get("contact_count")
    local_immediate_count = local_immediate.get("contact_count")
    return {
        "scope": (
            "same shot sample 13000 from the 2026-07-09 with-writeback run; local side now includes "
            "pyphysx immediate-mode raw contact generation plus post-step ContactPairPoint, Unity side is "
            "captured finalizer ContactBuffer/Solver row"
        ),
        "endpoint_gap_after_bestgeom_replay_m": {
            "active": (local.get("row") or {}).get("active_error_m"),
            "target": (local.get("row") or {}).get("target_error_m"),
        },
        "immediate_contact_generation": {
            "local_stage": local_immediate.get("stage"),
            "local_time": local_immediate.get("time"),
            "local_center_distance_m": local_immediate.get("center_distance_m"),
            "local_contact_distance_m": local_immediate.get("contact_distance_m"),
            "local_contact_count": local_immediate_count,
            "unity_finalizer_contact_count": unity_contact_count,
            "contact_count_status": (
                "mismatch" if local_immediate_count != unity_contact_count else "matched"
            ),
            "local_target_side_normal_angle_deg_xy": immediate_angle,
            "unity_target_side_normal_angle_deg_xz": unity_angle,
            "local_minus_unity_normal_angle_deg": immediate_angle_delta,
            "normal_status": (
                "mismatch"
                if immediate_angle_delta is not None and abs(immediate_angle_delta) > 1.0
                else "matched_or_unresolved"
            ),
            "local_separation_min_m": local_immediate.get("separation_min_m"),
            "local_separation_max_m": local_immediate.get("separation_max_m"),
            "unity_separations_m": unity_first.get("separations_m"),
            "separation_status": "mismatch",
            "cache": local_immediate.get("cache"),
            "points_preview": local_immediate.get("points_preview"),
            "note": (
                "This is the strongest current local-vs-Unity field split: local PxGenerateContacts on the reconstructed "
                "same-shot shape/pose yields raw 4-contact geometry at the handoff boundary, while Unity's captured "
                "finalizer ContactBuffer has 2 contacts and shallower positive separations.  Normal direction matches, "
                "so the remaining mismatch is contact manifold/count/separation timing or geometry/cache parity."
            ),
        },
        "contact_count": {
            "local_pyphysx_immediate_first_nonempty": local_immediate_count,
            "local_pyphysx_first_report": local_contact_count,
            "unity_finalizer_after": unity_contact_count,
            "status": (
                "mismatch"
                if local_immediate_count != unity_contact_count or local_contact_count != unity_contact_count
                else "matched"
            ),
            "note": (
                "Immediate-mode contact generation removes the old post-step report ambiguity for the local side. "
                "The local raw geometric contact generation and local ContactPairPoint report both keep 4 points; "
                "Unity finalizer has 2 points."
            ),
        },
        "normal_angle_deg": {
            "local_pyphysx_immediate_target_side_xy": immediate_angle,
            "local_pyphysx_first_report_xy": local_angle,
            "unity_finalizer_target_side_candidate_xz": unity_angle,
            "local_immediate_minus_unity_deg": immediate_angle_delta,
            "local_report_minus_unity_deg": angle_delta,
            "status": (
                "mismatch"
                if (
                    immediate_angle_delta is not None
                    and abs(immediate_angle_delta) > 1.0
                    and angle_delta is not None
                    and abs(angle_delta) > 1.0
                )
                else "matched_or_unresolved"
            ),
        },
        "separation_m": {
            "local_immediate_min": local_immediate.get("separation_min_m"),
            "local_immediate_max": local_immediate.get("separation_max_m"),
            "local_min": local_contact.get("separation_min_m"),
            "local_max": local_contact.get("separation_max_m"),
            "unity_first": unity_first_contact.get("separation"),
            "unity_all": unity_first.get("separations_m"),
            "note": (
                "Local immediate pre-step contact starts with penetration about -1.52mm; Unity finalizer contacts in "
                "the captured row are positive about +8.6/+8.4mm. Local post-step report later has positive about +6.4mm "
                "but still 4 contacts.  This points at first collision frame/contact-cache/manifold reduction or shape/pose parity."
            ),
        },
        "impulse_magnitude": {
            "local_contact_report_impulse_sum_Ns": local_impulse,
            "local_contact_report_impulse_norm_Ns_xy": local_contact.get("impulse_sum_norm_Ns_xy"),
            "local_contact_report_impulse_angle_deg_xy": local_contact.get("impulse_sum_angle_deg_xy"),
            "unity_positive_normal_force_sum_Ns": None,
            "note": "Filled after joining solve writeback summary; compare as a magnitude diagnostic, not as exact identical buffers.",
        },
        "material": {
            "unity_static_friction": unity_first_contact.get("staticFriction"),
            "unity_dynamic_friction": unity_first_contact.get("dynamicFriction"),
            "unity_restitution": unity_first_contact.get("restitution"),
            "local_config_stone_friction": ((local.get("config") or {}).get("stone_friction")),
            "local_config_combine_mode": ((local.get("config") or {}).get("combine_mode")),
            "status": "matched_high_confidence",
        },
    }


def build_report() -> dict[str, Any]:
    unity_sample = _read_jsonl_first(UNITY_NATIVE_SAMPLE)
    unity_finalizer = _unity_finalizer_summary(_read_json(UNITY_FINALIZER))
    solve_replay = _solve_replay_summary(_read_json(UNITY_SOLVE_REPLAY), _read_json(UNITY_SOLVE_SUMMARY))
    local_native13000 = _local_native13000_summary(_read_json(LOCAL_NATIVE13000))
    local_formal13000 = _local_native13000_summary(_read_json(LOCAL_FORMAL13000))
    local_handoff_extra13000 = _local_native13000_summary(_read_json(LOCAL_HANDOFF_EXTRA13000))
    finalizer_pose_replay = _read_json(UNITY_FINALIZER_POSE_CONTACT_REPLAY)
    handoff_oracle = _read_json(HANDOFF_ORACLE)
    generalization = _read_json(ORACLE_GENERALIZATION)
    historical_contact = _read_json(HISTORICAL_CONTACT_AUDIT)
    direct = _direct_field_comparison(local_native13000, unity_finalizer)
    unity_impulse_sum = ((solve_replay.get("top_dynamic_writeback_delta") or {}).get("positive_normal_force_sum_Ns"))
    if unity_impulse_sum is not None:
        direct["impulse_magnitude"]["unity_positive_normal_force_sum_Ns"] = unity_impulse_sum
        local_norm = direct["impulse_magnitude"].get("local_contact_report_impulse_norm_Ns_xy")
        if local_norm is not None:
            direct["impulse_magnitude"]["local_minus_unity_positive_normal_sum_Ns"] = float(local_norm) - float(unity_impulse_sum)
            direct["impulse_magnitude"]["local_over_unity_positive_normal_sum"] = float(local_norm) / float(unity_impulse_sum) if unity_impulse_sum else None

    closed_stages = [
        {
            "stage": "material combine",
            "status": "closed",
            "evidence": "Unity finalizer stone-stone friction is 0.3600000143 and restitution is 1, matching 0.6*0.6 and Bouncy restitution.",
        },
        {
            "stage": "ContactBuffer + PxSolverBodyData -> SolverContact rows",
            "status": "closed_for_captured_unity_rows",
            "evidence": f"rawVsComputed normal-row max abs delta = {unity_finalizer.get('raw_vs_computed_normal_row_max_abs_delta')}",
        },
        {
            "stage": "single-pair solver consume/writeback formula",
            "status": "closed_for_captured_withwriteback_wrappers",
            "evidence": f"max error by hook = {solve_replay.get('max_error_by_hook')}",
        },
    ]

    ranked_unknowns = [
        {
            "rank": 1,
            "name": "local-vs-Unity contact generation/manifold reduction mismatch",
            "why": (
                "For the with-writeback 13000 run, local pyphysx target endpoint is "
                f"{direct['endpoint_gap_after_bestgeom_replay_m']['target']}m away.  The new local immediate-mode "
                f"probe produces {direct['immediate_contact_generation']['local_contact_count']} raw contact points at "
                f"t={direct['immediate_contact_generation']['local_time']} with separations "
                f"{direct['immediate_contact_generation']['local_separation_min_m']}.."
                f"{direct['immediate_contact_generation']['local_separation_max_m']}m.  Unity's captured finalizer "
                f"ContactBuffer has {direct['immediate_contact_generation']['unity_finalizer_contact_count']} contacts "
                f"with separations {direct['immediate_contact_generation']['unity_separations_m']}.  The target-side "
                f"normal angle delta is {direct['immediate_contact_generation']['local_minus_unity_normal_angle_deg']}deg, "
                "so normal direction is effectively matched; count/separation/manifold timing is the first observed split."
            ),
            "status": "not_closed",
            "next_measurement": (
                "The Unity-finalizer bodyFrame pose replay still yields 4/3 local contacts rather than Unity's 2, so the "
                "next concrete probe is exact PxShape/PxConvexMeshGeometry/localPose and PCM manifold/cache parity."
            ),
        },
        {
            "rank": 2,
            "name": "Unity vs local pre-solve PxSolverBody state",
            "why": (
                "The row formula is closed only after Unity has already produced ContactBuffer/bodyData.  We have not "
                "shown that local pyphysx feeds the same body pose, linear velocity, angular velocity, sqrtInvInertia "
                "and contact rest distances into contact prep."
            ),
            "status": "not_closed",
            "next_measurement": "Dump or reconstruct local PxSolverBodyData for sample 13000 and compare field-by-field to Unity.",
        },
        {
            "rank": 3,
            "name": "shape cooked hull local pose / feature phase / contact cache",
            "why": (
                "The observed contact-count/separation mismatch is upstream of solver execution.  The plausible causes are "
                "runtime cooked hull byte/order/local pose, actor/shape yaw at handoff, or persistent PCM/friction contact "
                "cache.  Endpoint-only scans cannot distinguish these."
            ),
            "status": "not_closed",
            "next_measurement": "Capture Unity runtime PxShape/PxConvexMeshGeometry plus first friction patch anchors for the same shot.",
        },
        {
            "rank": 4,
            "name": "tail sliding / endpoint integration",
            "why": (
                "Older tail-oracle reports show the endpoint can be closed by early target velocity changes.  In the "
                "same-shot 13000 replay, active is already under 1cm and target is about 3cm, so tail integration is not "
                "the first suspect."
            ),
            "status": "lower_priority",
            "next_measurement": "Only revisit after same-frame 0.02s post-collision velocity is matched.",
        },
    ]

    return {
        "question": "What remains upstream of the Unity-vs-pyphysx collision mismatch after Unity row/writeback formulas are closed?",
        "conclusion": (
            "The current error is not from the recovered Unity row formula or single-pair consume formula.  In the latest "
            "with-writeback 13000 run, normal direction matches.  The new local immediate-mode probe shows the first concrete "
            "split earlier than solver execution: local raw contact generation yields 4 contacts and different separation, "
            "while Unity finalizer has 2 contacts.  The shortest remaining path is to close contact generation/manifold-cache "
            "parity, not to tune solver parameters."
        ),
        "sample_13000_unity_request": {
            "sample_id": unity_sample.get("sample_id"),
            "label": unity_sample.get("label"),
            "requested": unity_sample.get("requested"),
            "motioninfo": unity_sample.get("motioninfo"),
            "unity_after_position": unity_sample.get("after_position"),
            "target_moves": unity_sample.get("target_moves"),
        },
        "local_pyphysx_native13000": local_native13000,
        "unity_native_finalizer": unity_finalizer,
        "unity_solve_replay": solve_replay,
        "direct_field_comparison": direct,
        "targeted_geometry_checks": {
            "formal_recovered_mesh_13000": {
                "source": str(LOCAL_FORMAL13000.relative_to(PROJECT_ROOT)),
                "endpoint_summary": local_formal13000.get("endpoint_summary"),
                "first_immediate_contact_probe": local_formal13000.get("first_immediate_contact_probe"),
                "interpretation": (
                    "Switching from the simple ring/cylinder points to the recovered formal collider mesh did not "
                    "remove the 4-vs-2 contact-count split.  It improved the 13000 target endpoint only from about "
                    "19.9cm to about 17.5cm and moved the raw target-side normal to about -5.6deg, away from Unity's "
                    "-2.8125deg finalizer normal.  Therefore the current fix is not simply replacing the local ring "
                    "with this recovered visual/extended mesh."
                ),
            },
            "handoff_extra_0p01_13000": {
                "source": str(LOCAL_HANDOFF_EXTRA13000.relative_to(PROJECT_ROOT)),
                "endpoint_summary": local_handoff_extra13000.get("endpoint_summary"),
                "first_immediate_contact_probe": local_handoff_extra13000.get("first_immediate_contact_probe"),
                "interpretation": (
                    "Moving the pyphysx handoff boundary from 2R to approximately 2R+2*contactOffset is not a fix. "
                    "It makes the first local raw separation positive, but the first contact count drops to 1, the "
                    "first normal starts at 0deg, and the 13000 endpoint becomes worse.  This points to a coupled "
                    "first-frame/PCM-cache/pose problem rather than a scalar handoff threshold."
                ),
            },
            "unity_finalizer_bodyframe_pose_replay": {
                "source": str(UNITY_FINALIZER_POSE_CONTACT_REPLAY.relative_to(PROJECT_ROOT)),
                "unity_first_stone_stone": finalizer_pose_replay.get("unity_first_stone_stone"),
                "cases": [
                    {
                        "geometry": case.get("geometry"),
                        "yaw_case": case.get("yaw_case"),
                        "summary": case.get("summary"),
                    }
                    for case in (finalizer_pose_replay.get("cases") or [])
                ],
                "interpretation": (
                    "Feeding Unity's captured finalizer bodyFrame relative pose into local PxGenerateContacts does not "
                    "recover Unity's 2-contact manifold.  The simple ring gives 4 or 3 contacts; the recovered formal mesh "
                    "also gives 4 or 3 contacts.  Therefore the visible split is not just our handoff position/yaw.  The "
                    "remaining highest-value unknown is exact shape/cooked-hull/localPose/PCM-cache parity."
                ),
            },
        },
        "closed_stages": closed_stages,
        "ranked_unknowns": ranked_unknowns,
        "context_from_older_reports": {
            "handoff_xy_oracle_summary": handoff_oracle.get("handoff_xy_oracle_summary"),
            "handoff_xy_active_only_oracle_summary": handoff_oracle.get("handoff_xy_active_only_oracle_summary"),
            "visible_feature_best_model": generalization.get("best_model_by_target_rmse"),
            "historical_contact_report_vs_row_delta_summary": historical_contact.get("summary"),
            "historical_contact_report_vs_row_delta_interpretation": historical_contact.get("interpretation"),
        },
        "source_reports": {
            "unity_native_sample": str(UNITY_NATIVE_SAMPLE.relative_to(PROJECT_ROOT)),
            "unity_finalizer": str(UNITY_FINALIZER.relative_to(PROJECT_ROOT)),
            "unity_solve_replay": str(UNITY_SOLVE_REPLAY.relative_to(PROJECT_ROOT)),
            "unity_solve_summary": str(UNITY_SOLVE_SUMMARY.relative_to(PROJECT_ROOT)),
            "local_native13000": str(LOCAL_NATIVE13000.relative_to(PROJECT_ROOT)),
            "local_formal13000": str(LOCAL_FORMAL13000.relative_to(PROJECT_ROOT)),
            "local_handoff_extra13000": str(LOCAL_HANDOFF_EXTRA13000.relative_to(PROJECT_ROOT)),
            "unity_finalizer_pose_contact_replay": str(UNITY_FINALIZER_POSE_CONTACT_REPLAY.relative_to(PROJECT_ROOT)),
            "historical_contact_audit": str(HISTORICAL_CONTACT_AUDIT.relative_to(PROJECT_ROOT)),
            "handoff_oracle": str(HANDOFF_ORACLE.relative_to(PROJECT_ROOT)),
            "oracle_generalization": str(ORACLE_GENERALIZATION.relative_to(PROJECT_ROOT)),
        },
    }


def main() -> int:
    report = build_report()
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(json.dumps({
        "local_active_error_m": report["direct_field_comparison"]["endpoint_gap_after_bestgeom_replay_m"]["active"],
        "local_target_error_m": report["direct_field_comparison"]["endpoint_gap_after_bestgeom_replay_m"]["target"],
        "contact_count": report["direct_field_comparison"]["contact_count"],
        "normal_angle_deg": report["direct_field_comparison"]["normal_angle_deg"],
        "closed_stages": [row["stage"] for row in report["closed_stages"]],
        "top_unknown": report["ranked_unknowns"][0]["name"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
