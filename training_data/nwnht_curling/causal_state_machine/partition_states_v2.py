#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an interpretable, holdout-checked first-player state partition.

This is deliberately not k-means.  It starts from the already understood
macro topology and recursively adds only one explicit feature predicate when
that predicate changes the observed *future transition signature* in both
match-grouped train and holdout data.

The learned leaves are candidate state labels, not a policy.  ``own_effect``
in the transition signature is an observed S->U fact and must never be used as
a deployable action label.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

try:
    from .derive_action_effects import action_effect
    from .state_features_v2 import FEATURE_NAMES, build_feature_rows, canonical_orientation, state_features
except ImportError:  # pragma: no cover - direct script invocation
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from causal_state_machine.derive_action_effects import action_effect  # type: ignore
    from causal_state_machine.state_features_v2 import FEATURE_NAMES, build_feature_rows, canonical_orientation, state_features  # type: ignore


MIN_NODE_TRAIN_SUPPORT = 80
MIN_NODE_HOLDOUT_SUPPORT = 20
MIN_LEAF_TOTAL_SUPPORT = 150
MAX_SPLIT_DEPTH = 2
MIN_STABLE_TOTAL_VARIATION = 0.20
MAX_TRAIN_HOLDOUT_TV_GAP = 0.15

# These are refinements, not alternative macro labels.  K and the macro's
# defining aggregate counts are intentionally excluded from a split rule.
SPLIT_FEATURES = tuple(
    name for name in FEATURE_NAMES
    if name not in {
        "K", "control", "F_visible", "O_visible", "O_house_clear_cardinality",
        "F_visible_exact", "O_visible_exact", "F_house_exact", "O_house_exact",
        "F_nearest_depth", "O_nearest_depth",
    }
)


def _cap_2_total(features: Mapping[str, Any], prefix: str, zones: Sequence[str]) -> str:
    count = sum(2 if str(features[f"{prefix}_{zone}"]) == "2P" else int(features[f"{prefix}_{zone}"]) for zone in zones)
    return "2P" if count >= 2 else str(count)


HOUSE_ZONES = ("BUTTON", "HOUSE_FRONT_LEFT", "HOUSE_FRONT_RIGHT", "HOUSE_BACK_LEFT", "HOUSE_BACK_RIGHT")
CENTRE_GUARD_ZONES = ("GUARD_NEAR_CENTRE", "GUARD_FAR_CENTRE")
WING_GUARD_ZONES = ("GUARD_NEAR_LEFT", "GUARD_FAR_LEFT", "GUARD_NEAR_RIGHT", "GUARD_FAR_RIGHT")


def macro_type(features: Mapping[str, Any]) -> str:
    """The existing macro layer, expressed over the v2 feature vocabulary."""

    f_visible = int(features["F_visible_exact"])
    o_visible = int(features["O_visible_exact"])
    f_house = int(features["F_house_exact"])
    o_house = int(features["O_house_exact"])
    f_centre = _cap_2_total(features, "F", CENTRE_GUARD_ZONES)
    o_centre = _cap_2_total(features, "O", CENTRE_GUARD_ZONES)
    f_wing = _cap_2_total(features, "F", WING_GUARD_ZONES)
    o_wing = _cap_2_total(features, "O", WING_GUARD_ZONES)
    total_visible = f_visible + o_visible
    total_house = f_house + o_house
    if total_visible == 0:
        return "EMPTY"
    if total_visible >= 5 and total_house >= 3:
        return "CROWDED_HOUSE"
    if o_centre != "0" and o_house > 0:
        return "OPPONENT_CENTRE_CONFIGURATION"
    if f_centre != "0" and f_house > 0:
        return "FIRST_CENTRE_CONFIGURATION"
    if features["control"] == "OPPONENT" and o_house > 0:
        return "OPPONENT_HOUSE_THREAT"
    if features["control"] == "FIRST" and f_house > 0:
        return "FIRST_HOUSE_CONTROL"
    if f_house == 0 and o_house == 0 and (f_centre != "0" or o_centre != "0" or f_wing != "0" or o_wing != "0"):
        return "GUARD_EXCHANGE"
    if total_visible <= 2:
        return "SPARSE_OPEN"
    return "MIXED_CONTESTED"


def _split_for_match(match_id: int) -> str:
    """Same deterministic match-grouped split used by the existing v1 audit."""

    digest = hashlib.sha256(f"nwnht-state-abstraction:{match_id}".encode("ascii")).digest()
    return "holdout" if digest[0] % 5 == 0 else "train"


def _opponent_reply_effect(after_own: list[dict[str, Any]], after_reply: list[dict[str, Any]]) -> str:
    def swap(board: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{**stone, "owner": "opponent" if stone["owner"] == "first" else "first"} for stone in board]

    value = action_effect(swap(after_own), swap(after_reply))["primary_effect"]
    return {
        "GAIN_OWN_SCORING_CONTROL": "OPPONENT_GAINS_SCORING_CONTROL",
        "REDUCE_OPPONENT_HOUSE_LAYER": "OPPONENT_REDUCES_FIRST_HOUSE_LAYER",
        "ADD_OWN_HOUSE_LAYER": "OPPONENT_ADDS_HOUSE_LAYER",
        "ADD_PRESSURE_GUARD": "OPPONENT_ADDS_PRESSURE_GUARD",
        "REDUCE_STONE_COUNT_WITHOUT_CONTROL": "OPPONENT_REDUCES_STONE_COUNT_WITHOUT_CONTROL",
        "NO_CLASSIFIABLE_MACRO_EFFECT": "OPPONENT_NO_CLASSIFIABLE_MACRO_EFFECT",
    }[str(value)]


def _end_result(row: Mapping[str, Any]) -> str:
    margin = int(row["terminal_end_label"]["first_end_margin"])
    return "FIRST_SCORES" if margin > 0 else "OPPONENT_SCORES" if margin < 0 else "BLANK"


def _transition_token(row: Mapping[str, Any]) -> str:
    """An audit-only summary of the observed future after the current board."""

    k = int(row["own_throw_number"])
    own_effect = str(action_effect(list(row["s_before_own"]), list(row["u_after_own"]))["primary_effect"])
    reply = _opponent_reply_effect(list(row["u_after_own"]), list(row["s_after_opponent_reply"]))
    next_macro = "END" if k == 8 else macro_type(state_features(k + 1, row["s_after_opponent_reply"]))
    return "|".join((own_effect, reply, next_macro, _end_result(row)))


@dataclass(frozen=True)
class Observation:
    panel_key: str
    match_id: int
    k: int
    macro: str
    features: Mapping[str, str | int]
    token: str


@dataclass(frozen=True)
class CandidateSplit:
    feature: str
    value: str
    train_tv: float
    holdout_tv: float
    left_train: int
    right_train: int
    left_holdout: int
    right_holdout: int

    @property
    def strength(self) -> float:
        return min(self.train_tv, self.holdout_tv)


def _distribution(rows: Iterable[Observation]) -> Counter[str]:
    return Counter(row.token for row in rows)


def total_variation(left: Counter[str], right: Counter[str]) -> float | None:
    if not left or not right:
        return None
    left_total, right_total = sum(left.values()), sum(right.values())
    values = set(left) | set(right)
    return 0.5 * sum(abs(left.get(value, 0) / left_total - right.get(value, 0) / right_total) for value in values)


def _partition(rows: Sequence[Observation], feature: str, value: str) -> tuple[list[Observation], list[Observation]]:
    return ([row for row in rows if str(row.features[feature]) == value], [row for row in rows if str(row.features[feature]) != value])


def best_stable_split(
    rows: Sequence[Observation],
    *,
    split_for_match: Callable[[int], str] = _split_for_match,
    split_features: Sequence[str] = SPLIT_FEATURES,
) -> CandidateSplit | None:
    """Find the strongest one-vs-rest, holdout-replicated feature split."""

    best: CandidateSplit | None = None
    for feature in split_features:
        values = sorted({str(row.features[feature]) for row in rows})
        if len(values) < 2:
            continue
        for value in values:
            left, right = _partition(rows, feature, value)
            left_train = [row for row in left if split_for_match(row.match_id) == "train"]
            right_train = [row for row in right if split_for_match(row.match_id) == "train"]
            left_holdout = [row for row in left if split_for_match(row.match_id) == "holdout"]
            right_holdout = [row for row in right if split_for_match(row.match_id) == "holdout"]
            supports = (len(left_train), len(right_train), len(left_holdout), len(right_holdout))
            if min(supports[0], supports[1]) < MIN_NODE_TRAIN_SUPPORT or min(supports[2], supports[3]) < MIN_NODE_HOLDOUT_SUPPORT:
                continue
            train_tv = total_variation(_distribution(left_train), _distribution(right_train))
            holdout_tv = total_variation(_distribution(left_holdout), _distribution(right_holdout))
            if train_tv is None or holdout_tv is None:
                continue
            candidate = CandidateSplit(feature, value, train_tv, holdout_tv, *supports)
            if candidate.strength < MIN_STABLE_TOTAL_VARIATION or abs(train_tv - holdout_tv) > MAX_TRAIN_HOLDOUT_TV_GAP:
                continue
            if best is None or (candidate.strength, candidate.feature, candidate.value) > (best.strength, best.feature, best.value):
                best = candidate
    return best


@dataclass
class Leaf:
    k: int
    macro: str
    predicates: list[tuple[str, str, bool]]
    rows: list[Observation]
    split_history: list[CandidateSplit]


def _leaf_id(leaf: Leaf, serial: int) -> str:
    suffix = ";".join(f"{name}{'=' if equal else '!='}{value}" for name, value, equal in leaf.predicates)
    return f"K{leaf.k}_V2_{leaf.macro}_{serial}" + (f"[{suffix}]" if suffix else "")


def _split_recursively(leaf: Leaf, depth: int) -> list[Leaf]:
    if depth >= MAX_SPLIT_DEPTH:
        return [leaf]
    candidate = best_stable_split(leaf.rows)
    if candidate is None:
        return [leaf]
    left, right = _partition(leaf.rows, candidate.feature, candidate.value)
    if min(len(left), len(right)) < MIN_LEAF_TOTAL_SUPPORT:
        return [leaf]
    return _split_recursively(
        Leaf(leaf.k, leaf.macro, leaf.predicates + [(candidate.feature, candidate.value, True)], left, leaf.split_history + [candidate]), depth + 1
    ) + _split_recursively(
        Leaf(leaf.k, leaf.macro, leaf.predicates + [(candidate.feature, candidate.value, False)], right, leaf.split_history + [candidate]), depth + 1
    )


def _token_distribution(rows: Sequence[Observation]) -> list[dict[str, Any]]:
    counts = Counter(row.token for row in rows)
    total = len(rows)
    return [{"token": token, "count": count, "share": round(count / total, 6)} for token, count in counts.most_common()]


def _leaf_record(leaf: Leaf, serial: int) -> dict[str, Any]:
    train = [row for row in leaf.rows if _split_for_match(row.match_id) == "train"]
    holdout = [row for row in leaf.rows if _split_for_match(row.match_id) == "holdout"]
    return {
        "state_id": _leaf_id(leaf, serial),
        "K": leaf.k,
        "macro_state": leaf.macro,
        "rule": [
            {"feature": feature, "operator": "=" if equal else "!=", "value": value}
            for feature, value, equal in leaf.predicates
        ],
        "support_all": len(leaf.rows),
        "support_train": len(train),
        "support_holdout": len(holdout),
        "eligible_for_next_goal_stage": len(leaf.rows) >= MIN_LEAF_TOTAL_SUPPORT and len(train) >= MIN_NODE_TRAIN_SUPPORT and len(holdout) >= MIN_NODE_HOLDOUT_SUPPORT,
        "observed_transition_signature_distribution": _token_distribution(leaf.rows),
        "split_evidence": [
            {
                "feature": split.feature, "value": split.value,
                "train_total_variation": round(split.train_tv, 6),
                "holdout_total_variation": round(split.holdout_tv, 6),
                "branch_support": {
                    "left_train": split.left_train, "right_train": split.right_train,
                    "left_holdout": split.left_holdout, "right_holdout": split.right_holdout,
                },
            }
            for split in leaf.split_history
        ],
        "warning": "State split is predictive/homogeneity evidence only. The signature contains observed post-shot facts and terminal labels solely for offline partition validation, never as runtime inputs or actions.",
    }


def observations(rows: Iterable[Mapping[str, Any]]) -> list[Observation]:
    result: list[Observation] = []
    for raw in rows:
        feature_row = build_feature_rows([raw])[0]
        features = feature_row["features"]
        result.append(Observation(
            panel_key=str(feature_row["panel_key"]),
            match_id=int(feature_row["match_id"]),
            k=int(feature_row["K"]),
            macro=macro_type(features),
            features=features,
            token=_transition_token(raw),
        ))
    return result


def build(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[int, str], list[Observation]] = defaultdict(list)
    all_observations = observations(rows)
    for row in all_observations:
        grouped[(row.k, row.macro)].append(row)
    leaves: list[Leaf] = []
    for (k, macro), group in sorted(grouped.items()):
        leaves.extend(_split_recursively(Leaf(k, macro, [], group, []), 0))
    states = [_leaf_record(leaf, serial + 1) for serial, leaf in enumerate(leaves)]
    return {
        "schema": "nwnht_first_player_state_partition_v2",
        "purpose": "Holdout-checked, interpretable candidate state partition; not a tactical policy.",
        "runtime_input_contract": "Only K and current first/opponent stone coordinates. Left/right canonical orientation is recorded separately at runtime.",
        "runtime_assignment_contract": "Compute canonical v2 features and macro_state, then select the unique leaf with matching K, macro_state and every listed rule predicate. A non-eligible leaf must return SEARCH_REQUIRED rather than a learned target.",
        "feature_names": list(FEATURE_NAMES),
        "macro_layer": "Existing explainable macro topology, refined only by explicit feature predicates.",
        "transition_signature": "observed own S->U board effect | observed opponent reply effect | next macro state | terminal end result; offline validation only.",
        "thresholds": {
            "min_node_train_support": MIN_NODE_TRAIN_SUPPORT,
            "min_node_holdout_support": MIN_NODE_HOLDOUT_SUPPORT,
            "min_leaf_total_support": MIN_LEAF_TOTAL_SUPPORT,
            "max_split_depth": MAX_SPLIT_DEPTH,
            "min_stable_total_variation": MIN_STABLE_TOTAL_VARIATION,
            "max_train_holdout_tv_gap": MAX_TRAIN_HOLDOUT_TV_GAP,
        },
        "summary": {
            "input_rows": len(all_observations),
            "macro_node_count": len(grouped),
            "state_count": len(states),
            "eligible_state_count": sum(bool(state["eligible_for_next_goal_stage"]) for state in states),
        },
        "states": states,
        "limits": [
            "No score, end number, team, event, called-shot text, post-shot result or terminal label enters a runtime state rule.",
            "This partition does not identify a causal action effect or a winning policy.",
            "Rows outside a sufficiently supported state must later route to SEARCH_REQUIRED rather than nearest-state assignment.",
        ],
    }


def _matches_rule(features: Mapping[str, Any], rule: Sequence[Mapping[str, Any]]) -> bool:
    for predicate in rule:
        actual = str(features[str(predicate["feature"])])
        expected = str(predicate["value"])
        operator = str(predicate["operator"])
        if operator == "=" and actual != expected:
            return False
        if operator == "!=" and actual == expected:
            return False
        if operator not in {"=", "!="}:
            raise ValueError(f"unsupported state-rule operator {operator!r}")
    return True


def classify_runtime_state(partition: Mapping[str, Any], k: int, board: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Map a live board to exactly one v2 leaf without reading offline labels.

    A leaf can be geometrically recognised but still lack enough historical
    support.  In that case it is returned with ``SEARCH_REQUIRED``; callers
    must not substitute its nearest supported neighbour.
    """

    orientation = canonical_orientation(k, board)
    features = orientation["features"]
    macro = macro_type(features)
    matches = [
        state for state in partition["states"]
        if int(state["K"]) == k
        and str(state["macro_state"]) == macro
        and _matches_rule(features, state["rule"])
    ]
    if len(matches) != 1:
        raise ValueError(
            f"partition must map a board to exactly one leaf; K={k}, macro={macro}, matches={len(matches)}"
        )
    state = matches[0]
    return {
        "state_id": state["state_id"],
        "macro_state": macro,
        "status": "DATA_SUPPORTED_STATE" if bool(state["eligible_for_next_goal_stage"]) else "SEARCH_REQUIRED_INSUFFICIENT_STATE_SUPPORT",
        "mirrored_from_runtime_board": orientation["mirrored_from_runtime_board"],
        "features": features,
    }


def verify_runtime_assignment(partition: Mapping[str, Any], rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Check that the saved rules reproduce all source rows exactly once."""

    observed = Counter()
    row_count = 0
    for row in rows:
        runtime = classify_runtime_state(partition, int(row["own_throw_number"]), row["s_before_own"])
        observed[str(runtime["state_id"])] += 1
        row_count += 1
    declared = {str(state["state_id"]): int(state["support_all"]) for state in partition["states"]}
    differences = {
        state_id: {"declared": expected, "runtime_reclassified": observed.get(state_id, 0)}
        for state_id, expected in declared.items()
        if observed.get(state_id, 0) != expected
    }
    unknown = sorted(set(observed) - set(declared))
    return {
        "row_count": row_count,
        "state_count": len(declared),
        "exact_reproduction": not differences and not unknown,
        "support_differences": differences,
        "unknown_state_ids": unknown,
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
    parser.add_argument("--output", type=Path, default=root / "nwnht_first_player_state_partition_v2.json")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N records for a smoke check.")
    parser.add_argument("--verify-output", type=Path, default=None, help="Read an existing partition and verify its runtime assignment against --input; does not write output.")
    args = parser.parse_args()
    if args.verify_output is not None:
        partition = json.loads(args.verify_output.read_text(encoding="utf-8"))
        print(json.dumps(verify_runtime_assignment(partition, _read_jsonl(args.input)), ensure_ascii=False))
        return
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite {args.output}; choose a new output path.")
    rows: Iterable[dict[str, Any]] = _read_jsonl(args.input)
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be positive")
        rows = (row for _, row in zip(range(args.limit), rows))
    result = build(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
