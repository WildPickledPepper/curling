"""Versioned public input/output contract, independent of PhysX and Torch."""
from __future__ import annotations

import hashlib
import json
import math
from itertools import combinations
from typing import Any, Mapping, Sequence

import numpy as np

SCHEMA = "inverse_shot_dataset_v1"
HOUSE_X, HOUSE_Y, HOUSE_R, STONE_R = 2.375, 4.88, 1.830, 0.145
X_SCALE, Y_SCALE = 2.375, 10.525
ACTION_SCALE = np.array([6.0, 2.23, 15.7], dtype=np.float32)
GOAL_TYPES = ("ANY", "IN_REGION", "OUT_OF_PLAY", "OUT_OF_HOUSE", "SURVIVE")
# Preserve the deployed PPO IDs; ID 41 denotes a relabelled geometric goal.
TACTICS = tuple("occupy middle_in_center defense defense_push_in take_out hit_roll push_in push_in_14 freeze clear double_hit double_push_in default_draw draw_button draw_top4 draw_back4 center_guard corner_guard_left corner_guard_right come_around_left come_around_right take_out_house take_out_guard hit_and_stay peel_guard hit_roll_left hit_roll_right freeze_no1 freeze_no2 guard_my_shot center_guard_high center_guard_low corner_guard_left_high corner_guard_right_high tap_back raise_takeout runback_takeout around_guard_takeout_left around_guard_takeout_right around_guard_draw_left around_guard_draw_right achieved_goal".split())
FEATURES = ("x", "y", "enabled", "own", "shooter", *["goal_" + x.lower() for x in GOAL_TYPES], "goal_x", "goal_y", "goal_radius", "required")


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def split_for_group(group_id: str, split_seed: int) -> int:
    """0=train, 1=validation, 2=test; independent of worker/shard order."""
    bucket = int(digest([split_seed, group_id])[:12], 16) % 100
    return 0 if bucket < 80 else (1 if bucket < 90 else 2)


def indexed_states(states: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    if len(states) != 16:
        raise ValueError("scene must contain exactly 16 explicit slots")
    by_index = {int(s["index"]): s for s in states}
    if set(by_index) != set(range(16)):
        raise ValueError("stone indices must be unique and cover 0..15")
    return [by_index[i] for i in range(16)]


def in_house(state: Mapping[str, Any]) -> bool:
    return bool(state["enabled"]) and math.hypot(float(state["x"]) - HOUSE_X, float(state["y"]) - HOUSE_Y) <= HOUSE_R + STONE_R


def goal_met(states: Sequence[Mapping[str, Any]], goal: Mapping[str, Any]) -> bool:
    board = indexed_states(states)
    for key, item in goal["stones"].items():
        index = int(key)
        if not 0 <= index < 16:
            raise ValueError("goal index outside 0..15")
        kind = str(item["type"])
        if kind not in GOAL_TYPES:
            raise ValueError("unknown goal type: " + kind)
        stone = board[index]
        if kind == "ANY":
            continue
        if kind == "IN_REGION":
            radius = float(item["radius"])
            if radius <= 0 or not math.isfinite(radius):
                raise ValueError("region radius must be finite and positive")
            if not stone["enabled"] or math.hypot(float(stone["x"]) - float(item["x"]), float(stone["y"]) - float(item["y"])) > radius:
                return False
        elif kind == "OUT_OF_PLAY" and stone["enabled"]:
            return False
        elif kind == "OUT_OF_HOUSE" and in_house(stone):
            return False
        elif kind == "SURVIVE" and not stone["enabled"]:
            return False
    return True


def encode_input(states: Sequence[Mapping[str, Any]], goal: Mapping[str, Any], active_index: int, tactic: str = "achieved_goal") -> dict[str, np.ndarray]:
    """Same encoder for data preparation and future online PPO requests.

    Unknown yaw is masked rather than fabricated. Network input never contains
    realised final states, friction seeds, or collision reports.
    """
    board = indexed_states(states)
    if not 0 <= active_index < 16 or tactic not in TACTICS:
        raise ValueError("invalid active index or tactic")
    goal_indices = {int(k) for k in goal["stones"]}
    if any(i < 0 or i >= 16 for i in goal_indices) or len(goal_indices) != len(goal["stones"]):
        raise ValueError("invalid or duplicated goal slots")
    stones = np.zeros((16, 14), dtype=np.float32)
    # [sin(yaw), cos(yaw), known]; separate from the agreed 14-column contract.
    yaw = np.zeros((16, 3), dtype=np.float32)
    for i, state in enumerate(board):
        enabled = bool(state["enabled"])
        if enabled:
            stones[i, :2] = ((float(state["x"]) - HOUSE_X) / X_SCALE, (float(state["y"]) - HOUSE_Y) / Y_SCALE)
            if state.get("yaw") is not None:
                angle = float(state["yaw"])
                yaw[i] = (math.sin(angle), math.cos(angle), 1.0)
        stones[i, 2:5] = (enabled, i % 2 == active_index % 2, i == active_index)
        item = goal["stones"].get(str(i), goal["stones"].get(i, {"type": "ANY"}))
        kind = str(item["type"])
        if kind not in GOAL_TYPES:
            raise ValueError("unknown goal type: " + kind)
        stones[i, 5 + GOAL_TYPES.index(kind)] = 1.0
        if kind == "IN_REGION":
            radius = float(item["radius"])
            if radius <= 0:
                raise ValueError("region radius must be positive")
            stones[i, 10:13] = ((float(item["x"]) - HOUSE_X) / X_SCALE, (float(item["y"]) - HOUSE_Y) / Y_SCALE, radius / X_SCALE)
        stones[i, 13] = bool(item.get("required", True)) if kind != "ANY" else 0.0
    tactic_vector = np.zeros(len(TACTICS), dtype=np.float32)
    tactic_vector[TACTICS.index(tactic)] = 1.0
    context = np.array([active_index / 15.0, active_index % 2], dtype=np.float32)
    if not all(np.isfinite(a).all() for a in (stones, yaw, context)):
        raise ValueError("non-finite network input")
    return {"stones": stones, "yaw": yaw, "tactic": tactic_vector, "context": context}


def encode_action(shot: Sequence[float]) -> np.ndarray:
    action = np.asarray(shot, dtype=np.float32)
    if action.shape != (3,) or not np.isfinite(action).all():
        raise ValueError("shot must contain three finite values")
    if not (float(np.float32(0.0001)) <= float(action[0]) <= float(ACTION_SCALE[0])
            and abs(float(action[1])) <= float(ACTION_SCALE[1])
            and abs(float(action[2])) <= float(ACTION_SCALE[2])):
        raise ValueError("shot must already be inside the predictor BESTSHOT limits")
    return action / ACTION_SCALE


def achieved_views(record: Mapping[str, Any], max_views: int = 8) -> list[dict[str, Any]]:
    """Only stopped, legal observed outcomes produce positive inverse labels.

    Named double views additionally need the observed target-target collision;
    merely moving two stones out is not proof of the legacy double chain.
    """
    if max_views < 1 or record.get("status") != "complete" or record.get("rule_violations"):
        return []
    if not record["prediction"]["settled"]:
        return []
    before, after = indexed_states(record["before"]), indexed_states(record["physical_final"])
    active = int(record["active_index"])
    radius = float(record.get("goal_radius", 0.15))
    def disposition(i: int) -> dict[str, Any]:
        s = after[i]
        return {"type": "IN_REGION", "x": s["x"], "y": s["y"], "radius": radius, "required": True} if s["enabled"] else {"type": "OUT_OF_PLAY", "required": True}
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    def add(name: str, goals: dict[str, Any], tactic: str = "achieved_goal") -> None:
        goal = {"stones": goals}
        key = digest([goal, tactic])
        if key not in seen and goals and goal_met(after, goal):
            seen.add(key)
            result.append({"view": name, "goal": goal, "tactic": tactic})
    if record.get("selected_task"):
        task = record["selected_task"]
        add("selected_task", task["goal"]["stones"], task["tactic"])
    relevant = [i for i in range(16) if before[i]["enabled"] or i == active]
    changed = [i for i in relevant if i != active and (not after[i]["enabled"] or math.hypot(float(after[i]["x"]) - float(before[i]["x"]), float(after[i]["y"]) - float(before[i]["y"])) > 0.03)]
    opponents = [i for i in relevant if i != active and i % 2 != active % 2 and in_house(before[i]) and not in_house(after[i])]
    contacts = set(record["prediction"].get("firstContactTargets", ()))
    collision_pairs = {frozenset(e["stones"]) for e in record.get("collision_events", ())}
    # Put rarer validated tactical views before generic masks.
    for a, b in combinations(opponents, 2):
        if len(contacts) == 1 and contacts <= {a, b} and frozenset((a, b)) in collision_pairs:
            add("double_house_clear", {str(i): {"type": "OUT_OF_HOUSE", "required": True} for i in (a, b)}, "double_hit")
    for i in opponents:
        if contacts == {i}:
            add("takeout", {str(i): {"type": "OUT_OF_HOUSE", "required": True}}, "take_out_house")
    add("shooter", {str(active): disposition(active)})
    if after[active]["enabled"] and not record["prediction"].get("contact"):
        add("draw", {str(active): disposition(active)}, "default_draw")
    for i in changed:
        add("affected_" + str(i), {str(i): disposition(i)})
    add("shooter_and_affected", {str(i): disposition(i) for i in [active, *changed]})
    add("full_terminal", {str(i): disposition(i) for i in relevant})
    survivors = {str(i): {"type": "SURVIVE", "required": True} for i in relevant if after[i]["enabled"]}
    add("survivors", survivors)
    return result[:max_views]
