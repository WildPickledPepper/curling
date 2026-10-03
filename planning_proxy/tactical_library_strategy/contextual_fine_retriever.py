#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retrieve fine endpoint circles from geometrically similar same-(S,G) games."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from training_data.nwnht_curling.causal_state_machine.build_goal_library_v2 import _active_region
from training_data.nwnht_curling.causal_state_machine.state_features_v2 import canonicalise_left_right


NEIGHBOUR_COUNT = 20
MAX_REGIONS = 3
CLUSTER_RADIUS_M = 0.35
UNMATCHED_STONE_PENALTY_M = 2.5


def _owner_distance(left: list[Mapping[str, Any]], right: list[Mapping[str, Any]]) -> float:
    if not left and not right:
        return 0.0
    if not left or not right:
        return UNMATCHED_STONE_PENALTY_M * max(len(left), len(right))
    def directed(source: list[Mapping[str, Any]], target: list[Mapping[str, Any]]) -> float:
        return sum(min(math.hypot(float(a["x_m"]) - float(b["x_m"]), float(a["y_m"]) - float(b["y_m"])) for b in target) for a in source)
    return (directed(left, right) + directed(right, left)) / (len(left) + len(right)) + UNMATCHED_STONE_PENALTY_M * abs(len(left) - len(right))


def board_distance(left: Iterable[Mapping[str, Any]], right: Iterable[Mapping[str, Any]]) -> float:
    """Symmetric owner-preserving coordinate distance; smaller means more alike."""

    left_board, right_board = list(left), list(right)
    return _owner_distance([x for x in left_board if x["owner"] == "first"], [x for x in right_board if x["owner"] == "first"]) + _owner_distance([x for x in left_board if x["owner"] == "opponent"], [x for x in right_board if x["owner"] == "opponent"])


def _endpoint_clusters(ranked: Iterable[tuple[float, Mapping[str, Any]]]) -> list[list[tuple[float, Mapping[str, Any]]]]:
    """Greedy densest-radius clusters; avoids splitting one draw lane by grid edge."""

    remaining = [(distance, row) for distance, row in ranked if row.get("active_final_point_canonical") is not None]
    clusters: list[list[tuple[float, Mapping[str, Any]]]] = []
    while remaining and len(clusters) < MAX_REGIONS:
        def neighbourhood(seed: tuple[float, Mapping[str, Any]]) -> list[tuple[float, Mapping[str, Any]]]:
            point = seed[1]["active_final_point_canonical"]
            return [
                item for item in remaining
                if math.hypot(float(item[1]["active_final_point_canonical"]["x_m"]) - float(point["x_m"]), float(item[1]["active_final_point_canonical"]["y_m"]) - float(point["y_m"])) <= CLUSTER_RADIUS_M
            ]
        candidates = [neighbourhood(seed) for seed in remaining]
        best = min(
            candidates,
            key=lambda group: (-len(group), sum(distance for distance, _ in group) / len(group), str(group[0][1]["panel_key"])),
        )
        clusters.append(best)
        used = {str(row["panel_key"]) for _, row in best}
        remaining = [item for item in remaining if str(item[1]["panel_key"]) not in used]
    return clusters


class ContextualFineRetriever:
    """Frozen same-(S,G) exemplar index.  Does not choose semantic G."""

    def __init__(self, artifact: Mapping[str, Any]) -> None:
        self.examples = {str(goal): [dict(row) for row in rows] for goal, rows in artifact["examples_by_goal_id"].items()}
        self.manifest = dict(artifact.get("manifest", {}))

    @classmethod
    def load(cls, path: Path) -> "ContextualFineRetriever":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def retrieve(self, board: Iterable[Mapping[str, Any]], candidate: Mapping[str, Any], *, exclude_match_id: int | None = None) -> dict[str, Any]:
        goal_id = str(candidate["goal_id"])
        k = int(candidate["K"])
        canonical_board, mirrored = canonicalise_left_right(board)
        examples = [row for row in self.examples.get(goal_id, []) if exclude_match_id is None or int(row["match_id"]) != int(exclude_match_id)]
        ranked = sorted(
            ((board_distance(canonical_board, row["before_board_canonical"]), row) for row in examples),
            key=lambda item: (item[0], int(item[1]["match_id"]), str(item[1]["panel_key"])),
        )[:NEIGHBOUR_COUNT]
        regions = []
        for members in _endpoint_clusters(ranked):
            points = [(float(row["active_final_point_canonical"]["x_m"]), float(row["active_final_point_canonical"]["y_m"])) for _, row in members]
            region = _active_region(points)
            if region is None:
                continue
            if mirrored:
                region["centre_x_m"] = -float(region["centre_x_m"])
            regions.append({
                "active_final_region": region,
                "neighbour_support": len(members),
                "mean_pre_shot_board_distance_m": round(sum(distance for distance, _ in members) / len(members), 6),
                "source_match_count": len({int(row["match_id"]) for _, row in members}),
                "examples": [str(row["panel_key"]) for _, row in members[:5]],
            })
        regions.sort(key=lambda item: (-int(item["neighbour_support"]), float(item["mean_pre_shot_board_distance_m"])))
        return {
            "state_id": str(candidate["source_state"]), "K": k, "goal_id": goal_id,
            "retrieval_status": "CONTEXTUAL_FINE_REGIONS_AVAILABLE" if regions else "NO_CONTEXTUAL_ACTIVE_ENDPOINT_EXEMPLAR",
            "runtime_orientation_mirrored": mirrored,
            "nearest_exemplar_count": len(ranked),
            "regions": regions[:MAX_REGIONS],
            "warning": "Nearest historical geometry retrieves candidate fine regions only; it does not alter G ranking or prove reachability.",
        }


def contextual_regions_as_fine_options(retrieval: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Adapt retrieved circles to ``instantiate_goal_contracts`` input."""

    return [{
        "active_final_region": dict(region["active_final_region"]),
        "stone_constraints_when_unambiguous": [],
        "dynamic_house_removal_binding_request": None,
        "after_own_occupancy": {},
        "neighbour_support": int(region["neighbour_support"]),
        "historical_support": int(region["neighbour_support"]),
    } for region in retrieval.get("regions", [])]


def load_default() -> ContextualFineRetriever:
    root = Path(__file__).resolve().parents[2] / "training_data" / "nwnht_curling" / "causal_state_machine" / "artifacts"
    return ContextualFineRetriever.load(root / "nwnht_v2_contextual_fine_exemplars_v2_physx_admissible.json")
