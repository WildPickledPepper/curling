#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract v2-state-conditioned historical GoalState template families.

The output answers a narrow question: from a recognised state, what *terminal
board constraints* recur in the recorded S -> U transition?  It does not claim
that an observed endpoint was the player's intended target, that it is causal,
or that a local inverse solver can reach it.

Same-colour NWNHT stones have no persistent identity.  The exporter therefore
creates a stone selector only when identity is logically recoverable; otherwise
it emits region/occupancy constraints or abstains.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .extract_anonymous_goal_templates import extract_template, zone_of
    from .partition_states_v2 import classify_runtime_state, macro_type
    from .state_features_v2 import state_features
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.extract_anonymous_goal_templates import extract_template, zone_of  # type: ignore
    from causal_state_machine.partition_states_v2 import classify_runtime_state, macro_type  # type: ignore
    from causal_state_machine.state_features_v2 import state_features  # type: ignore


GRID_M = 0.20
MIN_GOAL_SUPPORT = 30
MIN_DOMINANT_POST_OWN_SHARE = 0.70
MIN_REGION_RADIUS_M = 0.12
CV_TOLERANCE_M = 0.06


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _grid_key(point: Mapping[str, Any] | None) -> tuple[int, int] | None:
    if point is None:
        return None
    return (round(float(point["x_m"]) / GRID_M), round(float(point["y_m"]) / GRID_M))


def _feature_topology(k: int, board: list[dict[str, Any]]) -> str:
    """A post-own topology label, not a decision state and not an action."""

    features = state_features(k, board)
    compact = ";".join(
        f"{name}={features[name]}" for name in (
            "control", "F_BUTTON", "F_HOUSE_FRONT_LEFT", "F_HOUSE_FRONT_RIGHT",
            "F_HOUSE_BACK_LEFT", "F_HOUSE_BACK_RIGHT", "O_BUTTON",
            "O_HOUSE_FRONT_LEFT", "O_HOUSE_FRONT_RIGHT", "O_HOUSE_BACK_LEFT",
            "O_HOUSE_BACK_RIGHT", "F_protected_house", "O_protected_house",
        )
    )
    return f"K{k}_POST_OWN[{compact};macro={macro_type(features)}]"


def _binding_request(source_features: Mapping[str, Any], observed_house_removed: int) -> dict[str, Any] | None:
    """Describe only a runtime role binding; never claim historical identity."""

    available = int(source_features["O_house_exact"])
    if observed_house_removed < 1 or observed_house_removed > 2 or available < observed_house_removed:
        return None
    return {
        "binding_kind": "OPPONENT_HOUSE_SET",
        "owner": "opponent",
        "source_region": "house",
        "choose_count": observed_house_removed,
        "combination_order": "try all current combinations; prioritize the combination containing the closest-to-button opponent stone",
        "required_disposition": "OUT_OF_PLAY",
        "identity_note": "Dynamic current-board roles. NWNHT did not preserve same-colour stone identities across frames.",
    }


def _mirror_zone_name(zone: str) -> str:
    """Reflect a named historical zone without touching non-lateral zones."""

    marker = "__SIDE_SWAP__"
    return zone.replace("_left", marker).replace("_right", "_left").replace(marker, "_right")


def _mirror_occupancy(occupancy: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for owner, zones in occupancy.items():
        mirrored: dict[str, Any] = {}
        for zone, count in zones.items():
            mirrored[_mirror_zone_name(str(zone))] = count
        result[str(owner)] = dict(sorted(mirrored.items()))
    return result


def _canonicalise_observed_template(raw: Mapping[str, Any], *, source_was_mirrored: bool) -> dict[str, Any]:
    """Express S->U endpoint constraints in the source state's canonical frame."""

    result = dict(raw)
    if not source_was_mirrored:
        return result
    point = raw.get("active_final_point")
    if point is not None:
        mirrored_point = dict(point)
        mirrored_point["x_m"] = round(-float(point["x_m"]), 6)
        mirrored_point["zone"] = zone_of(mirrored_point)
        result["active_final_point"] = mirrored_point
    result["after_own_occupancy"] = _mirror_occupancy(raw["after_own_occupancy"])
    result["after_reply_occupancy"] = _mirror_occupancy(raw["after_reply_occupancy"])
    constraints = []
    for selector in raw["stone_constraints_when_unambiguous"]:
        updated = dict(selector)
        if "historical_source_zone" in updated:
            updated["historical_source_zone"] = _mirror_zone_name(str(updated["historical_source_zone"]))
        constraints.append(updated)
    result["stone_constraints_when_unambiguous"] = constraints
    return result


def extract_v2_template(row: Mapping[str, Any], partition: Mapping[str, Any]) -> dict[str, Any]:
    """Attach a conservative anonymous endpoint template to one v2 source state."""

    k = int(row["own_throw_number"])
    source = classify_runtime_state(partition, k, row["s_before_own"])
    raw = _canonicalise_observed_template(
        extract_template(dict(row)),
        source_was_mirrored=bool(source["mirrored_from_runtime_board"]),
    )
    if k == 8:
        next_state: dict[str, Any] = {"state_id": "END", "status": "TERMINAL"}
    else:
        next_state = classify_runtime_state(partition, k + 1, row["s_after_opponent_reply"])
    delta = dict(raw["observed_delta"])
    return {
        "schema": "nwnht_v2_goal_template_row_v0",
        "panel_key": str(raw["panel_key"]),
        "K": k,
        "source_state": source["state_id"],
        "source_state_status": source["status"],
        "coordinate_frame": "NWNHT_BUTTON_CENTRED_METRES_CANONICAL_LEFT_RIGHT",
        "observed_template_kind": raw["observed_template_kind"],
        "precision": raw["precision"],
        "observed_delta": delta,
        "active_final_point": raw["active_final_point"],
        "stone_constraints_when_unambiguous": raw["stone_constraints_when_unambiguous"],
        "dynamic_house_removal_binding_request": _binding_request(source["features"], int(delta["opponent_house_removed_count"])),
        "after_own_occupancy": raw["after_own_occupancy"],
        "post_own_topology": _feature_topology(k, list(row["u_after_own"])),
        "after_opponent_reply_state": next_state["state_id"],
        "after_opponent_reply_status": next_state["status"],
        "abstention_reason": raw["abstention_reason"],
        "warning": "Observed endpoint template only. It is not an intended action label, causal effect, winning claim or PhysX-feasible command.",
    }


def _distribution(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [{"value": value, "count": count, "share": round(count / total, 6)} for value, count in counter.most_common()]


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))]


def _active_region(points: list[tuple[float, float]]) -> dict[str, Any] | None:
    if not points:
        return None
    centre_x = sum(x for x, _ in points) / len(points)
    centre_y = sum(y for _, y in points) / len(points)
    distances = [math.hypot(x - centre_x, y - centre_y) for x, y in points]
    return {
        "shape": "circle",
        "centre_x_m": round(centre_x, 6),
        "centre_y_m": round(centre_y, 6),
        "radius_m": round(max(MIN_REGION_RADIUS_M, _quantile(distances, 0.90) + CV_TOLERANCE_M), 6),
        "point_count": len(points),
        "coverage": "empirical_p90_plus_0.06m_cv_tolerance",
    }


def _signature(row: Mapping[str, Any]) -> tuple[Any, ...]:
    """Do not include opponent reply: it describes a consequence, not the goal."""

    delta = row["observed_delta"]
    return (
        str(row["source_state"]), str(row["observed_template_kind"]), str(row["precision"]),
        int(delta["opponent_removed_count"]), int(delta["opponent_house_removed_count"]),
        _canonical(row["stone_constraints_when_unambiguous"]),
        _canonical(row["dynamic_house_removal_binding_request"]),
        _canonical(row["after_own_occupancy"]), _grid_key(row["active_final_point"]),
    )


def _goal_id(signature: tuple[Any, ...]) -> str:
    return "nwnht_v2_goal_" + hashlib.sha256(repr(signature).encode("utf-8")).hexdigest()[:16]


def aggregate_templates(rows: Iterable[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    grouped: dict[tuple[Any, ...], dict[str, Any]] = defaultdict(lambda: {
        "count": 0, "post_own": Counter(), "reply_state": Counter(), "points": [], "examples": [],
        "source_supported": True,
    })
    input_count = 0
    for row in rows:
        input_count += 1
        signature = _signature(row)
        item = grouped[signature]
        item["count"] += 1
        item["source_supported"] = item["source_supported"] and row["source_state_status"] == "DATA_SUPPORTED_STATE"
        item["post_own"][str(row["post_own_topology"])] += 1
        item["reply_state"][str(row["after_opponent_reply_state"])] += 1
        point = row["active_final_point"]
        if point is not None:
            item["points"].append((float(point["x_m"]), float(point["y_m"])))
        if len(item["examples"]) < 5:
            item["examples"].append(str(row["panel_key"]))

    goals: list[dict[str, Any]] = []
    for signature, item in grouped.items():
        (
            source_state, kind, precision, opponent_removed, opponent_house_removed,
            selector_json, binding_json, occupancy_json, grid,
        ) = signature
        post_own = _distribution(item["post_own"])
        active_region = _active_region(item["points"])
        selectors = json.loads(selector_json)
        binding = json.loads(binding_json)
        reasons: list[str] = []
        if item["count"] < MIN_GOAL_SUPPORT:
            reasons.append(f"support<{MIN_GOAL_SUPPORT}")
        if not item["source_supported"]:
            reasons.append("source_state_not_data_supported")
        if precision != "ROLE_AND_REGION":
            reasons.append("no_role_and_region_precision")
        if active_region is None and not selectors and binding is None:
            reasons.append("no_runtime_bindable_terminal_constraint")
        if post_own[0]["share"] < MIN_DOMINANT_POST_OWN_SHARE:
            reasons.append(f"post_own_mode_share<{MIN_DOMINANT_POST_OWN_SHARE:.2f}")
        candidate = not reasons
        goals.append({
            "schema": "nwnht_v2_goal_template_family_v0",
            "goal_id": _goal_id(signature),
            "source_state": source_state,
            "observed_template_kind": kind,
            "precision": precision,
            "observed_opponent_removed_count": opponent_removed,
            "observed_opponent_house_removed_count": opponent_house_removed,
            "stone_constraints_when_unambiguous": selectors,
            "dynamic_house_removal_binding_request": binding,
            "after_own_occupancy": json.loads(occupancy_json),
            "active_final_region": active_region,
            "active_region_grid_cell": None if grid is None else {"x": grid[0], "y": grid[1], "size_m": GRID_M},
            "support": item["count"],
            "post_own_topology_distribution": post_own,
            "after_opponent_reply_state_distribution": _distribution(item["reply_state"]),
            "runtime_goal_candidate": candidate,
            "not_runtime_goal_candidate_reasons": reasons,
            "unranked_structural_fallback_goal_ids": [],
            "examples": item["examples"],
            "evidence_status": "HISTORICAL_GOAL_TEMPLATE",
            "warning": "Candidate means only source/geometry/support gates passed. It is not a causal or winning recommendation and needs later state-edge scoring plus local rule/PhysX screening.",
        })

    # Double-house-removal may structurally fall back to a single removal in
    # the same state.  Do not rank these fallbacks by frequency: value scoring
    # happens in the next stage.
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for goal in goals:
        by_source[str(goal["source_state"])].append(goal)
    for goal in goals:
        if int(goal["observed_opponent_house_removed_count"]) < 2:
            continue
        goal["unranked_structural_fallback_goal_ids"] = [
            str(other["goal_id"]) for other in by_source[str(goal["source_state"])]
            if other["runtime_goal_candidate"] and int(other["observed_opponent_house_removed_count"]) == 1
        ]
    goals.sort(key=lambda item: (-int(item["support"]), str(item["goal_id"])))
    return goals, {
        "schema": "nwnht_v2_goal_template_manifest_v0",
        "input_template_rows": input_count,
        "goal_family_count": len(goals),
        "runtime_goal_candidate_count": sum(bool(goal["runtime_goal_candidate"]) for goal in goals),
        "gates": {
            "min_goal_support": MIN_GOAL_SUPPORT,
            "required_precision": "ROLE_AND_REGION",
            "min_dominant_post_own_share": MIN_DOMINANT_POST_OWN_SHARE,
        },
        "fallback_policy": "Only same-source double-house-removal -> single-house-removal structural fallbacks are linked here. They are intentionally unranked.",
        "warning": "All families are observational endpoint templates, not pre-shot action labels or causal policies.",
    }


def _read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    root = Path(__file__).resolve().parent / "artifacts"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "nwnht_first_player_causal_transitions_v0.jsonl")
    parser.add_argument("--partition", type=Path, default=root / "nwnht_first_player_state_partition_v2.json")
    parser.add_argument("--template-output", type=Path, default=root / "nwnht_v2_goal_templates_v0.jsonl")
    parser.add_argument("--goal-output", type=Path, default=root / "nwnht_v2_goal_template_families_v0.json")
    parser.add_argument("--manifest-output", type=Path, default=root / "nwnht_v2_goal_template_families_v0_manifest.json")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N records for a smoke check.")
    args = parser.parse_args()
    for path in (args.template_output, args.goal_output, args.manifest_output):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite {path}; choose a new output path.")
    partition = json.loads(args.partition.read_text(encoding="utf-8"))
    rows: Iterable[dict[str, Any]] = _read_jsonl(args.input)
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be positive")
        rows = (row for _, row in zip(range(args.limit), rows))
    templates = [extract_v2_template(row, partition) for row in rows]
    goals, manifest = aggregate_templates(templates)
    args.template_output.parent.mkdir(parents=True, exist_ok=True)
    with args.template_output.open("w", encoding="utf-8") as handle:
        for row in templates:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    args.goal_output.write_text(json.dumps(goals, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.manifest_output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"templates": len(templates), "goal_output": str(args.goal_output), **manifest}, ensure_ascii=False))


if __name__ == "__main__":
    main()
