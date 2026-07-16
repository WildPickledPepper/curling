#!/usr/bin/env python3
"""Summarize whether Unity's first-contact PhysX native state is proven equal.

This is an audit ledger, not another parameter fit.  It joins the existing
collision reports and records which native-state fields are already matched,
which are only inferred, and which are known gaps before we can claim that the
state Unity gives PhysX is identical to the local replay state.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_native_state_equivalence_audit_20260709.json"
)

ORACLE_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_oracle_hypothesis_audit_20260709.json"
IMPULSE_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_impulse_residual_refresh_20260709.json"
PAIR_IMPULSE_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_pair_impulse_residual_refresh_20260709.json"
IMPULSE_FEASIBILITY_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_impulse_feasibility_refresh_20260709.json"
)
LOCAL_IMPULSE_TRACE_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_local_impulse_trace_20260709.json"
FRICTION_OFFSET_REPORT = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_current_best_friction_offset_refresh_20260709.json"
)
TAIL_REPLAY_002_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_tail_replay_oracle_002s_20260709.json"
TAIL_REPLAY_020_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_tail_replay_oracle_020s_20260709.json"
SOLVER_ROW_DELTA_002_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_solver_row_delta_from_tail_oracle_20260709.json"
)
SOLVER_ROW_DELTA_020_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_solver_row_delta_from_tail_oracle_020s_20260709.json"
)
ROW_CORRECTION_MODELS_002_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_row_correction_models_20260709.json"
)
ROW_CORRECTION_MODELS_020_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_row_correction_models_020s_20260709.json"
)
CONTACT_FRAME_QUANTIZATION_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_contact_frame_quantization_20260709.json"
)
FEATURE_PHASE_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_feature_phase_audit_20260709.json"
ROTATION_RESET_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_rotation_reset_audit_20260709.json"
INTEGRATED_ACTIVE_YAW_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_integrated_active_yaw_audit_20260709.json"
)
SUPPORT_REPORT = PROJECT_ROOT / "data" / "calibration" / "unity_collision_support_contact_audit_20260709.json"
STONE_GEOMETRY_INPUT_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_stone_geometry_input_audit_20260709.json"
)
STONE_PREFAB_ROTATION_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_stone_prefab_rotation_audit_20260709.json"
)
HANDOFF_THRESHOLD_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_handoff_threshold_audit_20260709.json"
)
LOCK_CONSTRAINTS_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_lock_constraints_audit_20260709.json"
)
CONTACT_REPORT_VS_ROW_DELTA_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_contact_report_vs_row_delta_20260709.json"
)
HANDOFF_XOFFSET_Y0_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_unique_role_xoffset_y0_20260709.json"
)
HANDOFF_12003_XYOFFSET_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_physx_collision_probe_12003_contact_xyoffset_wide_20260709.json"
)
HANDOFF_XY_ORACLE_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_handoff_xy_oracle_20260709.json"
)
ORACLE_GENERALIZATION_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_oracle_generalization_20260709.json"
)
ANGULAR_HANDOFF_REPORT = (
    PROJECT_ROOT / "data" / "calibration" / "unity_collision_angular_handoff_diagnostic_20260709.json"
)
RINK_MESH_REPORT = (
    PROJECT_ROOT
    / "data"
    / "calibration"
    / "unity_physx_collision_probe_unique_role_rink_mesh_currentbest_winding_20260709.json"
)


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _pyphysx_capabilities() -> Dict[str, Any]:
    try:
        import pyphysx  # type: ignore
    except ImportError as exc:
        return {"available": False, "error": str(exc)}

    shape_methods = [name for name in dir(pyphysx.Shape) if not name.startswith("_")]
    rigid_static_methods = [name for name in dir(pyphysx.RigidStatic) if not name.startswith("_")]
    scene_methods = [name for name in dir(pyphysx.Scene) if not name.startswith("_")]
    mesh_shape_methods = [
        name
        for name in shape_methods
        if "mesh" in name.lower() or "triangle" in name.lower() or "convex" in name.lower()
    ]
    return {
        "available": True,
        "shape_mesh_methods": mesh_shape_methods,
        "rigid_static_create_methods": [
            name
            for name in rigid_static_methods
            if "create" in name.lower() or "plane" in name.lower()
        ],
        "has_triangle_mesh_shape_creation": any(
            "triangle" in name.lower() and "create" in name.lower() for name in shape_methods
        ),
        "has_contact_report_dump": "get_contact_reports" in scene_methods,
        "scene_contact_report_methods": [
            name for name in scene_methods if "contact" in name.lower() or "report" in name.lower()
        ],
    }


def _requirement(
    group: str,
    field: str,
    unity_state: str,
    local_state: str,
    status: str,
    evidence: List[str],
    impact: str,
) -> Dict[str, Any]:
    return {
        "group": group,
        "field": field,
        "unity_state": unity_state,
        "local_pyphysx_state": local_state,
        "status": status,
        "evidence": evidence,
        "impact": impact,
    }


def _friction_offset_summary(report: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    result_sets = report.get("result_sets") or []
    if not result_sets:
        return None

    rows = []
    for result_set in result_sets:
        config = result_set.get("config") or {}
        summary = result_set.get("summary") or {}
        row12003 = None
        for row in result_set.get("rows") or []:
            if row.get("sample_id") == 12003:
                row12003 = row
                break
        rows.append(
            {
                "friction_offset_threshold": config.get("friction_offset_threshold"),
                "active_rmse_m": summary.get("active_rmse_m"),
                "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
                "sample_12003_target_error_m": (row12003 or {}).get("target_error"),
                "sample_12003_sim_target": (row12003 or {}).get("sim_target"),
            }
        )

    best = min(
        (row for row in rows if row.get("target_in_play_rmse_m") is not None),
        key=lambda row: row["target_in_play_rmse_m"],
        default=None,
    )
    baseline_like = [
        row
        for row in rows
        if row.get("target_in_play_rmse_m") == (best or {}).get("target_in_play_rmse_m")
        and row.get("sample_12003_target_error_m") == (best or {}).get("sample_12003_target_error_m")
    ]
    return {
        "best_by_target_rmse": best,
        "rows": rows,
        "interpretation": (
            "frictionOffsetThreshold is not the current missing lever: thresholds >=0.005 reproduce "
            "the current-best endpoint errors exactly, while 0.001 worsens target RMSE."
        ),
        "baseline_like_thresholds": [
            row.get("friction_offset_threshold") for row in baseline_like
        ],
    }


def _row_correction_models_summary(report: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    models = report.get("models") or []
    if not models:
        return None

    compact = []
    for model in models:
        summary = model.get("summary") or {}
        compact.append(
            {
                "model": model.get("model"),
                "endpoint_rmse_m": summary.get("endpoint_rmse_m"),
                "endpoint_over_2cm_count": summary.get("endpoint_over_2cm_count"),
                "impulse_residual_rmse_Ns": summary.get("impulse_residual_rmse_Ns"),
            }
        )
    non_oracle = [row for row in compact if row.get("model") != "per_sample_oracle"]
    best_non_oracle = min(
        (row for row in non_oracle if row.get("endpoint_rmse_m") is not None),
        key=lambda row: row["endpoint_rmse_m"],
        default=None,
    )
    oracle = next((row for row in compact if row.get("model") == "per_sample_oracle"), None)
    return {
        "best_model": (report.get("summary") or {}).get("best_model"),
        "oracle": oracle,
        "best_non_oracle": best_non_oracle,
        "top_models": compact[:6],
        "interpretation": (
            "Only the per-sample oracle reaches 2cm. Even the deliberately generous global 2x2 "
            "contact-frame transform remains around 10cm RMSE, so a single global row correction "
            "cannot explain the residual."
        ),
    }


def _handoff_offset_summary(
    global_x_report: Dict[str, Any], sample_xy_report: Dict[str, Any]
) -> Dict[str, Any]:
    def _result_set_key_target(result_set: Dict[str, Any]) -> float:
        summary = result_set.get("summary") or {}
        value = summary.get("target_in_play_rmse_m")
        return float(value) if value is not None else float("inf")

    def _result_set_key_combined(result_set: Dict[str, Any]) -> float:
        summary = result_set.get("summary") or {}
        value = summary.get("combined_rmse_m")
        return float(value) if value is not None else float("inf")

    def _compact_result_set(result_set: Dict[str, Any]) -> Dict[str, Any]:
        config = result_set.get("config") or {}
        summary = result_set.get("summary") or {}
        return {
            "handoff_x_offset": config.get("handoff_x_offset"),
            "handoff_y_offset": config.get("handoff_y_offset"),
            "active_rmse_m": summary.get("active_rmse_m"),
            "target_in_play_rmse_m": summary.get("target_in_play_rmse_m"),
            "combined_rmse_m": summary.get("combined_rmse_m"),
        }

    global_sets = global_x_report.get("result_sets") or []
    sample_sets = sample_xy_report.get("result_sets") or []
    baseline = next(
        (
            _compact_result_set(result_set)
            for result_set in global_sets
            if (result_set.get("config") or {}).get("handoff_x_offset") == 0
        ),
        None,
    )
    best_global = (
        _compact_result_set(min(global_sets, key=_result_set_key_target))
        if global_sets
        else None
    )

    per_sample_best: Dict[str, Dict[str, Any]] = {}
    for result_set in global_sets:
        config = result_set.get("config") or {}
        x_offset = config.get("handoff_x_offset")
        for row in result_set.get("rows") or []:
            active_error = row.get("active_error")
            target_error = row.get("target_error")
            if active_error is None or target_error is None:
                continue
            score = max(float(active_error), float(target_error))
            sample_key = str(row.get("sample_id"))
            current = per_sample_best.get(sample_key)
            if current is None or score < current["max_endpoint_error_m"]:
                per_sample_best[sample_key] = {
                    "sample_id": row.get("sample_id"),
                    "label": row.get("label"),
                    "handoff_x_offset": x_offset,
                    "active_error_m": active_error,
                    "target_error_m": target_error,
                    "max_endpoint_error_m": score,
                }

    best_12003 = None
    if sample_sets:
        best_set = min(sample_sets, key=_result_set_key_combined)
        config = best_set.get("config") or {}
        row = (best_set.get("rows") or [{}])[0]
        first_report = (row.get("stone_stone_contact_reports") or [{}])[0]
        first_point = (first_report.get("points") or [{}])[0]
        best_12003 = {
            "handoff_x_offset": config.get("handoff_x_offset"),
            "handoff_y_offset": config.get("handoff_y_offset"),
            "active_error_m": row.get("active_error"),
            "target_error_m": row.get("target_error"),
            "combined_rmse_m": (best_set.get("summary") or {}).get("combined_rmse_m"),
            "first_contact_time": row.get("first_stone_stone_contact_time"),
            "first_contact_point_count": first_report.get("contact_count"),
            "first_contact_normal": first_point.get("normal"),
            "first_contact_impulse": first_point.get("impulse"),
        }

    return {
        "global_x_y0_baseline": baseline,
        "global_x_y0_best_by_target_rmse": best_global,
        "per_sample_best_y0_by_max_endpoint_error": dict(sorted(per_sample_best.items())),
        "sample_12003_xy_best_by_combined_rmse": best_12003,
        "interpretation": (
            "A single global handoff-x offset does not explain the collision residual: the y=0 sweep "
            "slightly improves active RMSE but leaves target RMSE at about the baseline 11cm level. "
            "However, sample 12003 is highly sensitive to a sample-specific x/y handoff perturbation, "
            "which points at first-contact native input/manifold differences rather than a global coordinate constant."
        ),
    }


def build_report() -> Dict[str, Any]:
    oracle = _read_json(ORACLE_REPORT) or {}
    impulse = _read_json(IMPULSE_REPORT) or {}
    pair_impulse = _read_json(PAIR_IMPULSE_REPORT) or {}
    impulse_feasibility = _read_json(IMPULSE_FEASIBILITY_REPORT) or {}
    local_impulse_trace = _read_json(LOCAL_IMPULSE_TRACE_REPORT) or {}
    friction_offset = _read_json(FRICTION_OFFSET_REPORT) or {}
    tail_replay_002 = _read_json(TAIL_REPLAY_002_REPORT) or {}
    tail_replay_020 = _read_json(TAIL_REPLAY_020_REPORT) or {}
    solver_row_delta_002 = _read_json(SOLVER_ROW_DELTA_002_REPORT) or {}
    solver_row_delta_020 = _read_json(SOLVER_ROW_DELTA_020_REPORT) or {}
    row_correction_models_002 = _read_json(ROW_CORRECTION_MODELS_002_REPORT) or {}
    row_correction_models_020 = _read_json(ROW_CORRECTION_MODELS_020_REPORT) or {}
    contact_frame_quantization = _read_json(CONTACT_FRAME_QUANTIZATION_REPORT) or {}
    feature_phase = _read_json(FEATURE_PHASE_REPORT) or {}
    rotation_reset = _read_json(ROTATION_RESET_REPORT) or {}
    integrated_active_yaw = _read_json(INTEGRATED_ACTIVE_YAW_REPORT) or {}
    support = _read_json(SUPPORT_REPORT) or {}
    stone_geometry_input = _read_json(STONE_GEOMETRY_INPUT_REPORT) or {}
    stone_prefab_rotation = _read_json(STONE_PREFAB_ROTATION_REPORT) or {}
    handoff_threshold = _read_json(HANDOFF_THRESHOLD_REPORT) or {}
    lock_constraints = _read_json(LOCK_CONSTRAINTS_REPORT) or {}
    contact_report_vs_row_delta = _read_json(CONTACT_REPORT_VS_ROW_DELTA_REPORT) or {}
    handoff_xoffset_y0 = _read_json(HANDOFF_XOFFSET_Y0_REPORT) or {}
    handoff_12003_xyoffset = _read_json(HANDOFF_12003_XYOFFSET_REPORT) or {}
    handoff_xy_oracle = _read_json(HANDOFF_XY_ORACLE_REPORT) or {}
    oracle_generalization = _read_json(ORACLE_GENERALIZATION_REPORT) or {}
    angular_handoff = _read_json(ANGULAR_HANDOFF_REPORT) or {}
    rink_mesh = _read_json(RINK_MESH_REPORT) or {}
    pyphysx_caps = _pyphysx_capabilities()

    current_best = None
    for item in impulse.get("results", []):
        if item.get("label") == "unique_role_current_best":
            current_best = item
            break
    if current_best is None and impulse.get("results"):
        current_best = impulse["results"][0]

    current_target_rmse = None
    current_active_rmse = None
    impulse_summary = None
    if current_best:
        probe_summary = current_best.get("probe_summary", {})
        current_target_rmse = probe_summary.get("target_in_play_rmse_m")
        current_active_rmse = probe_summary.get("active_rmse_m")
        impulse_summary = current_best.get("summary")

    requirements = [
        _requirement(
            "scene",
            "fixed timestep",
            "fixedDeltaTime=0.01s",
            "probe dt=0.01s",
            "matched",
            ["docs/unity_reverse/10_simulator_alignment_strategy.zh.md", "probe config"],
            "Wrong dt was already shown to create meter-level drift; this item is not the current collision gap.",
        ),
        _requirement(
            "scene",
            "gravity",
            "PhysicsManager gravity=(0,-9.81,0), formal stones use gravity",
            "pyphysx scene z gravity=-9.81, gravity enabled by default",
            "matched_for_main_probe",
            ["data/calibration/unity_collision_support_contact_audit_20260709.json"],
            "Disabling gravity is catastrophic, but removing vertical settling does not fix the 10cm target error.",
        ),
        _requirement(
            "scene",
            "contact generation and friction type",
            "contactsGeneration=1 selects PCM; frictionType=0 selects patch friction",
            "pyphysx Scene defaults include PCM; patch friction is the PhysX default path used in probes",
            "mostly_matched",
            ["docs/unity_reverse/05_physx_contact_generation.zh.md", "docs/unity_reverse/06_physx_solver.zh.md"],
            "The code path is known; equality of the actual contact cache/manifold is still not proven.",
        ),
        _requirement(
            "static_geometry",
            "rink collider geometry",
            "static MeshCollider triangle mesh, Unity default Plane mesh, m_CookingOptions=30",
            "probe now supports both historical PxPlane and a Unity-Plane-like 10x10 triangle mesh",
            "binding_available_not_main_cause",
            [
                "docs/unity_reverse/00_overview_assets.zh.md",
                "tools/reverse/probe_physx_collision_alignment.py",
                "data/calibration/unity_physx_collision_probe_unique_role_rink_mesh_currentbest_winding_20260709.json",
            ],
            "The historical PxPlane probe is not a strict native-state match, but replacing it with a triangle mesh did not reduce the target error.",
        ),
        _requirement(
            "dynamic_actor",
            "Rigidbody scalar properties",
            "mass=19.1, drag=0, angularDrag=0.05, constraints FreezeRotationX|FreezeRotationZ",
            "probe sets mass=19.1, linear damping=0, angular damping=0.05; lock-upright replay maps Unity X/Z locks to PhysX X/Y locks",
            "tested_non_main_cause",
            [
                "docs/unity_reverse/00_overview_assets.zh.md",
                "tools/reverse/probe_physx_collision_alignment.py",
                "data/calibration/unity_collision_lock_constraints_audit_20260709.json",
            ],
            "The lock-axis mismatch is real in the historical baseline, but a locked replay suppresses horizontal angular velocity and still leaves about 11.37cm target RMSE.",
        ),
        _requirement(
            "dynamic_actor",
            "first-contact pose and velocity",
            "Unity true PxRigidDynamic pose/velocity at the frame entering PhysX",
            "reconstructed from MOTIONINFO plus Newfrictionstep or console-derived handoff_state",
            "inferred_not_captured",
            ["tools/reverse/merge_console_handoff_into_samples.py", "data/calibration/unity_physx_collision_probe_unique_role_current_best_20260708.json"],
            "A small velocity or yaw error at contact is amplified over 3-4m of post-collision sliding.",
        ),
        _requirement(
            "shape",
            "formal stone cooked convex stream",
            "runtime MeshCollider cooked PxConvexMesh/CLHL/GAUS/VALE for the actual match stone",
            "offline pyphysx cook of recovered formal mesh under recovered Unity flags",
            "inferred_not_captured",
            ["data/calibration/pyphysx_cooked_stone_hull_probe_unity_flags_rebuilt_raw_20260708.json", "docs/unity_reverse/12_physx_convex_cooking.zh.md"],
            "The offline hull is structurally strong evidence, but not a byte-level proof of Unity's runtime stream.",
        ),
        _requirement(
            "shape",
            "shape local pose, geometry scale, wrapper",
            "Unity PxShape local pose/scale after MeshCollider rebuild",
            "probe exposes common shape_local x/y/z/yaw sweeps; identity is assumed by default",
            "not_proven",
            [
                "data/calibration/unity_physx_collision_probe_unique_role_shape_local_xyz_grid_20260709.json",
                "data/calibration/unity_collision_feature_phase_audit_20260709.json",
            ],
            "Simple common offsets/yaw, actor yaw, and stone face count do not fix the hard 12003 error, but the exact Unity shape wrapper is still not directly captured.",
        ),
        _requirement(
            "material",
            "first-contact material timing",
            "Bouncy/Ice material values plus OnCollisionEnter managed timing",
            "probe tested pre/post/never material switches",
            "tested_non_main_cause",
            ["data/calibration/unity_collision_material_timing_audit_20260709.json"],
            "The timing variants do not move the oracle floor enough; this is probably not the main mismatch.",
        ),
        _requirement(
            "contact_manager",
            "persistent contact cache and friction anchors",
            "Unity PxsContactManager state accumulated before first stone-stone solve",
            "fresh pyphysx scene starts with no existing pair/cache/friction anchors",
            "not_proven",
            ["docs/unity_reverse/05_physx_contact_generation.zh.md", "docs/unity_reverse/06_physx_solver.zh.md"],
            "Warm-start/cache differences can change early tangent impulses without looking like a simple restitution parameter.",
        ),
        _requirement(
            "contact_manager",
            "first contact manifold",
            "actual normal, points, separation, material values and maxImpulse from Unity ContactBuffer",
            "not dumped; only endpoint and local snapshot residuals are available",
            "missing_required_proof",
            [
                "data/calibration/unity_collision_impulse_residual_20260709.json",
                "data/calibration/unity_collision_impulse_residual_refresh_20260709.json",
                "data/calibration/unity_collision_pair_impulse_residual_refresh_20260709.json",
                "data/calibration/unity_collision_impulse_feasibility_refresh_20260709.json",
                "data/calibration/unity_collision_local_impulse_trace_20260709.json",
            ],
            "Target-side endpoint-inferred velocity corrections are stable across early snapshots; this is the shortest path to prove or disprove native-state equality at the collision frame.",
        ),
        _requirement(
            "solver",
            "normal/friction solver rows and impulses",
            "Unity SolverContactHeader/Point/Friction rows and applied impulses",
            "formula and layouts are recovered, but row instances are not captured",
            "missing_required_proof",
            [
                "docs/unity_reverse/06_physx_solver.zh.md",
                "data/calibration/unity_collision_impulse_feasibility_refresh_20260709.json",
            ],
            "The observed residual splits into normal-row and tangent/friction/cache classes; the row/impulse dump would localize it directly.",
        ),
    ]

    status_counts: Dict[str, int] = {}
    for item in requirements:
        status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1

    counterexamples = [
        "The historical current-best probe uses PxPlane for the rink while Unity uses a non-convex MeshCollider triangle mesh; a new 10x10 triangle-mesh A/B test did not improve the target RMSE.",
        "The formal match-stone runtime cooked convex stream has not been captured byte-for-byte; the local hull is an offline PhysX cook.",
        "Unity's contact manager cache/friction anchors and first ContactBuffer/SolverContact rows have not been dumped.",
    ]
    feature_summary = feature_phase.get("summary") or {}
    if feature_summary:
        counterexamples.append(
        "Static feature-phase probes do not reach 2cm: best 12003 error across shape yaw, actor yaw, "
        f"shape offsets and stone-faces scans is {feature_summary.get('best_sample12003_error_across_feature_phase_probes_m'):.6f}m."
        )
    rotation_summary = rotation_reset.get("summary") or {}
    if rotation_summary:
        counterexamples.append(
            "Wide reset-yaw probes can bring 12003 target to "
            f"{rotation_summary.get('best_target_error_m'):.6f}m, but best pair RMSE remains "
            f"{rotation_summary.get('best_pair_rmse_m'):.6f}m and no yaw pair puts both endpoints under 2cm."
        )
        if rotation_summary.get("target_yaw_only_oracle_target_rmse_m") is not None:
            counterexamples.append(
                "Per-sample target-yaw-only probes still do not prove identity: target RMSE remains "
                f"{rotation_summary.get('target_yaw_only_oracle_target_rmse_m'):.6f}m and pair RMSE remains "
                f"{rotation_summary.get('target_yaw_only_oracle_pair_rmse_m'):.6f}m."
            )
        hard_pairs = rotation_summary.get("hard_sample_dual_yaw_best_pair_rmse_m") or {}
        if hard_pairs:
            counterexamples.append(
                "Hard-sample dual-yaw probes remain above 2cm pair RMSE: "
                + ", ".join(f"{sample}={value:.6f}m" for sample, value in sorted(hard_pairs.items()))
                + "."
            )
    if current_target_rmse is not None:
        counterexamples.append(
            f"Current unique-role replay target RMSE is {current_target_rmse:.6f}m, far above numerical epsilon."
        )
    stone_geometry_deltas = stone_geometry_input.get("deltas") or {}
    if stone_geometry_deltas:
        counterexamples.append(
            "Recovered 512-vertex formal mesh input is not the missing 10cm lever: current-best "
            "scale recovered-mesh vs ring target RMSE delta is "
            f"{stone_geometry_deltas.get('current_best_scale_recovered_minus_ring_target_rmse_m'):.6f}m, "
            "and formal recovered mesh remains "
            f"{(stone_geometry_input.get('comparisons') or {}).get('formal_params_recovered_mesh', {}).get('target_in_play_rmse_m'):.6f}m target RMSE."
        )
    if stone_prefab_rotation.get("stone_count"):
        counterexamples.append(
            "Serialized formal stone prefab/scene rotations do not explain the wide-yaw lever: "
            f"{stone_prefab_rotation.get('stone_count')} stones have "
            f"{stone_prefab_rotation.get('unique_local_rotation_count')} unique local rotation and max yaw "
            f"{stone_prefab_rotation.get('max_abs_yaw_deg'):.6f}deg."
        )
    integrated_best = integrated_active_yaw.get("best_integrated_by_target_rmse") or {}
    if integrated_best:
        counterexamples.append(
            "Deterministic BESTSHOT->handoff active yaw integration is not the missing rotation state: "
            f"best integrated target RMSE is {integrated_best.get('target_in_play_rmse_m'):.6f}m "
            f"vs baseline {(integrated_active_yaw.get('baseline') or {}).get('target_in_play_rmse_m'):.6f}m."
        )
    best_handoff = handoff_threshold.get("best_handoff_extra_plus_yoffset") or {}
    if best_handoff:
        counterexamples.append(
            "Millimeter-scale handoff threshold/placement refinement helps but does not prove identity: "
            f"best target RMSE is {best_handoff.get('target_in_play_rmse_m'):.6f}m after "
            f"{handoff_threshold.get('improvement_vs_baseline_m'):.6f}m improvement versus baseline."
        )
    lock_summary = (lock_constraints.get("lock_upright_best") or {}).get("summary") or {}
    if lock_summary:
        counterexamples.append(
            "Unity lock-axis constraints are not the missing 10cm lever: locked replay target RMSE is "
            f"{lock_summary.get('target_in_play_rmse_m'):.6f}m and target horizontal angular velocity at 0.02s is "
            f"{(lock_constraints.get('lock_upright_best') or {}).get('max_target_horizontal_angular_speed_002s'):.6f}rad/s."
        )
    contact_summary = contact_report_vs_row_delta.get("summary") or {}
    worst_contact = contact_summary.get("worst_unity_minus_contact_report_sample") or {}
    sample_12003_contact = next(
        (
            row
            for row in contact_report_vs_row_delta.get("rows") or []
            if row.get("sample_id") == 12003
        ),
        {},
    )
    if sample_12003_contact:
        counterexamples.append(
            "Local pyphysx ContactPairPoint dump confirms the hard-sample contact-frame mismatch: "
            "sample 12003 first contact report impulse angle is "
            f"{sample_12003_contact.get('target_contact_impulse_angle_deg'):.3f}deg, while Unity-implied "
            f"target impulse angle is {sample_12003_contact.get('unity_implied_impulse_angle_deg'):.3f}deg "
            f"(delta {sample_12003_contact.get('unity_minus_contact_report_angle_deg'):.3f}deg)."
        )
    handoff_offset_summary = _handoff_offset_summary(handoff_xoffset_y0, handoff_12003_xyoffset)
    global_handoff_best = handoff_offset_summary.get("global_x_y0_best_by_target_rmse") or {}
    sample_12003_xy_best = handoff_offset_summary.get("sample_12003_xy_best_by_combined_rmse") or {}
    if global_handoff_best:
        counterexamples.append(
            "A global handoff-x offset is not the missing native-state constant: the best y=0 global sweep uses "
            f"x={global_handoff_best.get('handoff_x_offset')}m and still has target RMSE "
            f"{global_handoff_best.get('target_in_play_rmse_m'):.6f}m."
        )
    if sample_12003_xy_best:
        counterexamples.append(
            "Sample 12003 is nevertheless strongly sensitive to local handoff pose: x="
            f"{sample_12003_xy_best.get('handoff_x_offset')}m, y={sample_12003_xy_best.get('handoff_y_offset')}m "
            f"reduces active/target errors to {sample_12003_xy_best.get('active_error_m'):.6f}m/"
            f"{sample_12003_xy_best.get('target_error_m'):.6f}m, so the remaining gap is contact-instance "
            "state rather than a solved field-for-field identity."
        )
    handoff_oracle_summary = handoff_xy_oracle.get("handoff_xy_oracle_summary") or {}
    handoff_active_only_summary = handoff_xy_oracle.get("handoff_xy_active_only_oracle_summary") or {}
    if handoff_oracle_summary:
        bottlenecks = handoff_oracle_summary.get("bottlenecks_over_2cm") or []
        bottleneck_text = ", ".join(
            f"{row.get('sample_id')}={row.get('max_endpoint_error_m'):.6f}m" for row in bottlenecks
        )
        if bottlenecks:
            tail = f"and bottlenecks are {bottleneck_text}."
        else:
            tail = "and all in-play target pairs are within 2cm."
        counterexamples.append(
            "A per-sample entrance-state oracle can control the existing in-play collision samples to 2cm, "
            "but only by changing sample-specific native-state proxies. "
            f"Target RMSE is {handoff_oracle_summary.get('target_in_play_rmse_m'):.6f}m, "
            f"active RMSE is {handoff_oracle_summary.get('active_rmse_m'):.6f}m, "
            f"both-endpoints-under-2cm count is {handoff_oracle_summary.get('both_endpoints_within_2cm_count')} "
            f"of {handoff_oracle_summary.get('in_play_pair_count')}, {tail}"
        )
    if handoff_active_only_summary:
        if (handoff_oracle_summary or {}).get("all_in_play_pairs_within_2cm"):
            active_tail = (
                "With the handoff angular-velocity diagnostic included, the in-play pair objective also "
                "falls under 2cm, but only under per-sample native-state proxy changes."
            )
        else:
            active_tail = (
                "That isolates active endpoint drift as mostly entrance reconstruction, but the pair objective "
                "still has a contact-instance bottleneck."
            )
        counterexamples.append(
            "Scoring only the active stone, entrance-state perturbations can put all 8 samples under 2cm "
            f"(active RMSE {handoff_active_only_summary.get('active_rmse_m'):.6f}m). "
            + active_tail
        )
    best_generalization = oracle_generalization.get("best_model_by_target_rmse") or {}
    best_generalization_summary = best_generalization.get("endpoint_summary") or {}
    if best_generalization_summary:
        counterexamples.append(
            "Visible-feature correction is not a usable substitute for native-state equality: leave-one-out "
            f"best model {best_generalization.get('name')} still has active RMSE "
            f"{best_generalization_summary.get('active_rmse_m'):.6f}m, target RMSE "
            f"{best_generalization_summary.get('target_in_play_rmse_m'):.6f}m, and "
            f"{best_generalization_summary.get('both_endpoints_within_2cm_count')} of "
            f"{best_generalization_summary.get('in_play_pair_count')} in-play pairs with both endpoints under 2cm."
        )
    angular_12005 = angular_handoff.get("sample_12005_woffset_best_by_max_endpoint") or {}
    angular_global = (angular_handoff.get("global_woffset_summary") or {}).get("best_by_target_rmse") or {}
    if angular_12005:
        counterexamples.append(
            "The 12005 angular handoff diagnostic closes that sample but is not a global angular constant: "
            f"handoff_w_offset={((angular_12005.get('config') or {}).get('handoff_w_offset'))} gives "
            f"active/target errors {angular_12005.get('active_error_m'):.6f}m/"
            f"{angular_12005.get('target_error_m'):.6f}m, while the reconstructed handoff w is only "
            f"{angular_12005.get('handoff_w'):.6f}rad/s."
        )
    if angular_global:
        counterexamples.append(
            "A global handoff_w_offset still does not solve the collision set: best global target RMSE is "
            f"{angular_global.get('target_in_play_rmse_m'):.6f}m with "
            f"{angular_global.get('bad_in_play_pair_count')} in-play pair errors over 2cm."
        )

    proof_target = [
        "Dump Unity runtime PxShape/PxConvexMeshGeometry/PxTriangleMeshGeometry for active, target and rink.",
        "Dump first stone-stone ContactBuffer after PCM narrowphase: normal, points, separation and material fields.",
        "Dump SolverContact rows or applied normal/friction impulses for the same pair.",
        "Replay from those exact dumped fields in local PhysX/C++ or pyphysx and compare the 0.02s post-contact velocity before looking at final endpoints.",
    ]

    return {
        "strong_identity_claim": "Unity first-contact native state equals local pyphysx state field-for-field",
        "strong_identity_proven": False,
        "conclusion": (
            "Not proven, and the current evidence contradicts the strong identity claim. Existing evidence supports "
            "many high-level PhysX settings, but complete native-state identity has not been demonstrated. "
            "The current replay is not a field-for-field native-state match: "
            "historical probes differed in rink geometry, the triangle-mesh A/B test did not close the gap, "
            "per-sample entrance-state perturbations materially change the hard samples, and the most "
            "contact-relevant runtime fields have not been captured."
        ),
        "current_error_evidence": {
            "unique_role_current_best_active_rmse_m": current_active_rmse,
            "unique_role_current_best_target_rmse_m": current_target_rmse,
            "unique_role_rink_mesh_target_rmse_m": (
                ((rink_mesh.get("result_sets") or [{}])[0].get("summary") or {}).get("target_in_play_rmse_m")
            ),
            "unique_role_rink_mesh_active_rmse_m": (
                ((rink_mesh.get("result_sets") or [{}])[0].get("summary") or {}).get("active_rmse_m")
            ),
            "oracle_target_only_rmse_m": (oracle.get("target_only_oracle_summary") or {}).get("rmse_m"),
            "oracle_pair_floor_rmse_m": (oracle.get("active_and_target_pair_oracle_summary") or {}).get("pair_rmse_floor_m"),
            "impulse_residual_summary": impulse_summary,
            "pair_impulse_residual_summary": pair_impulse.get("summary"),
            "impulse_feasibility_summary": impulse_feasibility.get("summary"),
            "impulse_feasibility_interpretation": impulse_feasibility.get("interpretation"),
            "local_impulse_trace_summary": local_impulse_trace.get("summary"),
            "local_impulse_trace_interpretation": local_impulse_trace.get("interpretation"),
            "friction_offset_refresh_summary": _friction_offset_summary(friction_offset),
            "tail_replay_oracle_002s_summary": tail_replay_002.get("summary"),
            "tail_replay_oracle_020s_summary": tail_replay_020.get("summary"),
            "tail_replay_oracle_interpretation": tail_replay_002.get("interpretation") or tail_replay_020.get("interpretation"),
            "solver_row_delta_002s_summary": solver_row_delta_002.get("summary"),
            "solver_row_delta_020s_summary": solver_row_delta_020.get("summary"),
            "solver_row_delta_interpretation": solver_row_delta_002.get("interpretation")
            or solver_row_delta_020.get("interpretation"),
            "row_correction_models_002s_summary": _row_correction_models_summary(row_correction_models_002),
            "row_correction_models_020s_summary": _row_correction_models_summary(row_correction_models_020),
            "contact_frame_quantization_hull_summary": contact_frame_quantization.get("hull_summary"),
            "contact_frame_quantization_summary": contact_frame_quantization.get("summary"),
            "contact_frame_quantization_interpretation": contact_frame_quantization.get("interpretation"),
            "feature_phase_summary": feature_phase.get("summary"),
            "feature_phase_evidence_notes": feature_phase.get("evidence_notes"),
            "rotation_reset_summary": rotation_reset.get("summary"),
            "rotation_reset_best_target": rotation_reset.get("best_target"),
            "rotation_reset_best_pair": rotation_reset.get("best_pair"),
            "rotation_reset_target_yaw_only_oracle": rotation_reset.get("target_yaw_only_oracle"),
            "rotation_reset_hard_sample_dual_yaw": rotation_reset.get("hard_sample_dual_yaw"),
            "integrated_active_yaw_summary": {
                "baseline": integrated_active_yaw.get("baseline"),
                "best_integrated_by_target_rmse": integrated_active_yaw.get("best_integrated_by_target_rmse"),
                "interpretation": integrated_active_yaw.get("interpretation"),
            },
            "support_contact_settle_probes": support.get("settle_probes"),
            "support_contact_interpretation": support.get("interpretation"),
            "stone_geometry_input_summary": {
                "comparisons": stone_geometry_input.get("comparisons"),
                "deltas": stone_geometry_input.get("deltas"),
                "interpretation": stone_geometry_input.get("interpretation"),
            },
            "stone_prefab_rotation_summary": {
                "stone_count": stone_prefab_rotation.get("stone_count"),
                "unique_local_rotation_count": stone_prefab_rotation.get("unique_local_rotation_count"),
                "unique_local_rotations": stone_prefab_rotation.get("unique_local_rotations"),
                "unique_local_yaw_deg": stone_prefab_rotation.get("unique_local_yaw_deg"),
                "max_abs_yaw_deg": stone_prefab_rotation.get("max_abs_yaw_deg"),
                "interpretation": stone_prefab_rotation.get("interpretation"),
            },
            "handoff_threshold_summary": {
                "baseline": handoff_threshold.get("baseline"),
                "best_handoff_extra_only": handoff_threshold.get("best_handoff_extra_only"),
                "best_handoff_extra_plus_yoffset": handoff_threshold.get("best_handoff_extra_plus_yoffset"),
                "improvement_vs_baseline_m": handoff_threshold.get("improvement_vs_baseline_m"),
                "interpretation": handoff_threshold.get("interpretation"),
            },
            "lock_constraints_summary": {
                "baseline": lock_constraints.get("baseline"),
                "lock_upright_best": lock_constraints.get("lock_upright_best"),
                "delta_vs_baseline_m": lock_constraints.get("delta_vs_baseline_m"),
                "interpretation": lock_constraints.get("interpretation"),
            },
            "contact_report_vs_row_delta_summary": {
                "summary": contact_summary,
                "sample_12003": sample_12003_contact,
                "worst_unity_minus_contact_report_sample": worst_contact,
                "interpretation": contact_report_vs_row_delta.get("interpretation"),
            },
            "handoff_offset_summary": handoff_offset_summary,
            "handoff_xy_oracle": handoff_xy_oracle,
            "oracle_generalization": {
                "question": oracle_generalization.get("question"),
                "best_model_by_target_rmse": oracle_generalization.get("best_model_by_target_rmse"),
                "interpretation": oracle_generalization.get("interpretation"),
            },
            "angular_handoff_diagnostic": angular_handoff,
        },
        "pyphysx_capabilities": pyphysx_caps,
        "requirements": requirements,
        "status_counts": status_counts,
        "known_counterexamples_or_gaps": counterexamples,
        "minimum_proof_target": proof_target,
        "source_reports": {
            "oracle": str(ORACLE_REPORT.relative_to(PROJECT_ROOT)),
            "impulse": str(IMPULSE_REPORT.relative_to(PROJECT_ROOT)),
            "pair_impulse": str(PAIR_IMPULSE_REPORT.relative_to(PROJECT_ROOT)),
            "impulse_feasibility": str(IMPULSE_FEASIBILITY_REPORT.relative_to(PROJECT_ROOT)),
            "local_impulse_trace": str(LOCAL_IMPULSE_TRACE_REPORT.relative_to(PROJECT_ROOT)),
            "friction_offset": str(FRICTION_OFFSET_REPORT.relative_to(PROJECT_ROOT)),
            "tail_replay_002s": str(TAIL_REPLAY_002_REPORT.relative_to(PROJECT_ROOT)),
            "tail_replay_020s": str(TAIL_REPLAY_020_REPORT.relative_to(PROJECT_ROOT)),
            "solver_row_delta_002s": str(SOLVER_ROW_DELTA_002_REPORT.relative_to(PROJECT_ROOT)),
            "solver_row_delta_020s": str(SOLVER_ROW_DELTA_020_REPORT.relative_to(PROJECT_ROOT)),
            "row_correction_models_002s": str(ROW_CORRECTION_MODELS_002_REPORT.relative_to(PROJECT_ROOT)),
            "row_correction_models_020s": str(ROW_CORRECTION_MODELS_020_REPORT.relative_to(PROJECT_ROOT)),
            "contact_frame_quantization": str(CONTACT_FRAME_QUANTIZATION_REPORT.relative_to(PROJECT_ROOT)),
            "feature_phase": str(FEATURE_PHASE_REPORT.relative_to(PROJECT_ROOT)),
            "rotation_reset": str(ROTATION_RESET_REPORT.relative_to(PROJECT_ROOT)),
            "integrated_active_yaw": str(INTEGRATED_ACTIVE_YAW_REPORT.relative_to(PROJECT_ROOT)),
            "support": str(SUPPORT_REPORT.relative_to(PROJECT_ROOT)),
            "stone_geometry_input": str(STONE_GEOMETRY_INPUT_REPORT.relative_to(PROJECT_ROOT)),
            "stone_prefab_rotation": str(STONE_PREFAB_ROTATION_REPORT.relative_to(PROJECT_ROOT)),
            "handoff_threshold": str(HANDOFF_THRESHOLD_REPORT.relative_to(PROJECT_ROOT)),
            "lock_constraints": str(LOCK_CONSTRAINTS_REPORT.relative_to(PROJECT_ROOT)),
            "contact_report_vs_row_delta": str(CONTACT_REPORT_VS_ROW_DELTA_REPORT.relative_to(PROJECT_ROOT)),
            "handoff_xoffset_y0": str(HANDOFF_XOFFSET_Y0_REPORT.relative_to(PROJECT_ROOT)),
            "handoff_12003_xyoffset": str(HANDOFF_12003_XYOFFSET_REPORT.relative_to(PROJECT_ROOT)),
            "handoff_xy_oracle": str(HANDOFF_XY_ORACLE_REPORT.relative_to(PROJECT_ROOT)),
            "oracle_generalization": str(ORACLE_GENERALIZATION_REPORT.relative_to(PROJECT_ROOT)),
            "angular_handoff_diagnostic": str(ANGULAR_HANDOFF_REPORT.relative_to(PROJECT_ROOT)),
            "rink_mesh": str(RINK_MESH_REPORT.relative_to(PROJECT_ROOT)),
        },
    }


def main() -> None:
    report = build_report()
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"strong_identity_proven={report['strong_identity_proven']}")
    print("status_counts=" + json.dumps(report["status_counts"], ensure_ascii=False, sort_keys=True))
    print("known gaps:")
    for gap in report["known_counterexamples_or_gaps"]:
        print(f"- {gap}")


if __name__ == "__main__":
    main()
