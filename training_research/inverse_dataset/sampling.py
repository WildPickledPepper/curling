"""Deterministic scene families and grid/stratified BESTSHOT coverage."""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path
from typing import Any

from .schema import HOUSE_X, HOUSE_Y, STONE_R, digest

FAMILIES = ("empty", "single_house", "guarded_target", "double_pair", "raise_chain", "cluster", "spread", "dense")


def task_rng(seed: int, *keys: Any) -> random.Random:
    return random.Random(int(digest([seed, *keys])[:16], 16))


def validate_scene(scene: dict[str, Any]) -> dict[str, Any]:
    active = int(scene["active_index"])
    if not 0 <= active < 16:
        raise ValueError("active_index must be 0..15")
    stones = []
    seen = set()
    for item in scene.get("stones", []):
        if not item.get("enabled", True):
            continue
        index = int(item["index"])
        if index in seen or not 0 <= index < active:
            raise ValueError("present stones must be unique earlier delivery slots")
        if item.get("owner") is not None:
            expected = "self" if index % 2 == active % 2 else "opponent"
            if item["owner"] != expected:
                raise ValueError("owner conflicts with alternating delivery slot")
        x, y = float(item["x"]), float(item["y"])
        yaw = float(item.get("yaw", 0.0))
        if not all(math.isfinite(v) for v in (x, y, yaw)) or not (0.15 <= x <= 4.60 and 0.15 <= y <= 10.40):
            raise ValueError("scene coordinate outside configurable playing-scene domain")
        # Imported stopped boards can contain touching stones. Allow their
        # contact distance and protocol rounding; synthetic spacing is .34 m.
        if any(math.hypot(x - s["x"], y - s["y"]) < 2 * STONE_R - 0.005 for s in stones):
            raise ValueError("scene contains overlapping/too-close stones")
        seen.add(index)
        stones.append({"index": index, "x": x, "y": y, "yaw": yaw, "yaw_source": "supplied" if "yaw" in item else "default_zero"})
    stones.sort(key=lambda s: s["index"])
    if "selection" in scene:
        from .selection import validate_selection
        validate_selection(scene["selection"], active)
    if "shot_bounds" in scene:
        bounds = scene["shot_bounds"]
        limits = {"v": (0.0001, 6.), "h": (-2.23, 2.23), "w": (-15.7, 15.7)}
        for axis, (low, high) in limits.items():
            values = bounds[axis]
            if len(values) != 2 or not all(math.isfinite(float(v)) for v in values) or not low <= values[0] <= values[1] <= high:
                raise ValueError("invalid shot_bounds for " + axis)
    for values in scene.get("candidate_shots", []):
        if len(values) != 3 or not all(math.isfinite(float(v)) for v in values):
            raise ValueError("candidate_shots must contain finite v,h,w triples")
    key = digest([active, [[s[k] for k in ("index", "x", "y", "yaw")] for s in stones]])
    task_key = digest([key, scene.get("selection"), scene.get("shot_bounds")]) if "selection" in scene or "shot_bounds" in scene else key
    return {**scene, "active_index": active, "stones": stones, "scene_key": key, "task_key": task_key, "group_id": str(scene.get("group_id", key))}


def deduplicate_scenes(scenes):
    """Keep distinct tasks on the same board; group identical boards together.

    Union whole neighbourhood groups when an identical board links them.
    Otherwise one variant of that neighbourhood could leak across splits.
    """
    parent, boards = {}, {}
    def find(group):
        parent.setdefault(group, group)
        while parent[group] != group:
            parent[group] = parent[parent[group]]
            group = parent[group]
        return group
    for scene in scenes:
        group = scene["group_id"]
        if scene["scene_key"] in boards:
            a, b = find(group), find(boards[scene["scene_key"]])
            parent[max(a, b)] = min(a, b)
        else:
            boards[scene["scene_key"]] = group
            find(group)
    unique = {}
    for scene in scenes:
        scene = {**scene, "group_id": find(scene["group_id"])}
        key = scene.get("task_key", scene["scene_key"])
        if key in unique:
            unique[key].setdefault("candidate_shots", []).extend(scene.get("candidate_shots", []))
        else:
            unique[key] = scene
    return list(unique.values())


def synthetic_scene(scene_index: int, seed: int, families=FAMILIES) -> dict[str, Any]:
    family = families[scene_index % len(families)]
    rng = task_rng(seed, "scene", scene_index)
    minimum = {"empty": 0, "single_house": 1, "guarded_target": 3, "double_pair": 3, "raise_chain": 2, "cluster": 6, "spread": 5, "dense": 8}[family]
    active = rng.randint(minimum, 15)
    if family == "single_house" and active == 0:
        active = 1
    opponent_slots = [i for i in range(active) if i % 2 != active % 2]
    own_slots = [i for i in range(active) if i % 2 == active % 2]
    rng.shuffle(opponent_slots)
    rng.shuffle(own_slots)
    stones: list[dict[str, Any]] = []
    def place(index: int, x: float, y: float) -> None:
        stones.append({"index": index, "x": x, "y": y, "yaw": rng.uniform(-math.pi, math.pi)})
    x, y = HOUSE_X + rng.uniform(-0.65, 0.65), HOUSE_Y + rng.uniform(-0.65, 0.65)
    if family in {"single_house", "guarded_target", "double_pair", "raise_chain"}:
        place(opponent_slots[0], x, y)
        if family == "guarded_target":
            place(opponent_slots[1], x + rng.uniform(-0.1, 0.1), y + rng.uniform(1.3, 3.1))
        elif family == "double_pair":
            angle, gap = rng.uniform(-math.pi, math.pi), rng.uniform(0.34, 1.45)
            place(opponent_slots[1], x + gap * math.cos(angle), y + gap * math.sin(angle))
        elif family == "raise_chain":
            place(own_slots[0], x + rng.uniform(-0.12, 0.12), y + rng.uniform(0.4, 1.8))
    elif family in {"cluster", "spread", "dense"}:
        count = min(active, rng.randint(3, 6) if family == "cluster" else rng.randint(1 if family == "spread" else 8, active))
        slots = list(range(active))
        rng.shuffle(slots)
        for index in slots[:count]:
            for _ in range(2000):
                px = rng.uniform(0.55, 4.20)
                py = rng.uniform(3.0, 6.9) if family == "cluster" else rng.uniform(1.0, 9.8)
                if all(math.hypot(px - s["x"], py - s["y"]) >= 0.34 for s in stones):
                    place(index, px, py)
                    break
            else:
                raise RuntimeError("could not place separated synthetic stones")
    return validate_scene({"scene_id": "synthetic-%08d" % scene_index, "family": family, "active_index": active, "stones": stones})


def load_scenes(json_paths: list[str], log_paths: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    result, rejected = [], []
    for name in json_paths:
        raw = json.loads(Path(name).read_text(encoding="utf-8"))
        entries = raw if isinstance(raw, list) else raw["scenes"]
        for row, item in enumerate(entries):
            try:
                result.append(validate_scene({**item, "scene_id": item.get("scene_id", f"{Path(name).name}:{row}"), "family": item.get("family", "imported")}))
            except (ValueError, KeyError, TypeError) as exc:
                rejected.append({"source": name, "row": row, "reason": str(exc)})
    for name in log_paths:
        with Path(name).open(encoding="utf-8", errors="replace") as stream:
            for line_index, line in enumerate(stream, 1):
                if not line.startswith("SERVER_TELEMETRY "):
                    continue
                try:
                    item = json.loads(line[len("SERVER_TELEMETRY "):])
                    if item.get("record_type") != "server_physx_topk_decision":
                        continue
                    positions = item["position"]
                    if len(positions) != 32:
                        raise ValueError("telemetry position must contain 32 coordinates")
                    stones = [{"index": i, "x": positions[2*i], "y": positions[2*i+1]} for i in range(16) if positions[2*i] != 0 or positions[2*i+1] != 0]
                    candidates = [item[k] for k in ("legacy_bestshot", "executed_bestshot") if k in item]
                    result.append(validate_scene({"scene_id": f"{Path(name).name}:{line_index}", "family": "historical", "active_index": item["shot_num"], "stones": stones, "candidate_shots": candidates, "group_id": "log-game:" + str(Path(name).resolve().parent), "source": name, "source_line": line_index}))
                except (ValueError, KeyError, TypeError) as exc:
                    rejected.append({"source": name, "row": line_index, "reason": str(exc)})
    return deduplicate_scenes(result), rejected


def shot_candidates(scene: dict[str, Any], count: int, seed: int, sampling: str, grid: list[list[float]], v_min: float = 2.4, v_max: float = 6.0) -> list[dict[str, Any]]:
    if sampling == "grid":
        return [{"shot": list(values), "origin": "grid"} for values in itertools.product(*grid)]
    rng = task_rng(seed, "shots", scene["scene_key"])
    if not 0.0001 <= v_min <= v_max <= 6.0:
        raise ValueError("invalid sampling velocity bounds")
    if sampling == "uniform":
        bounds = scene.get("shot_bounds", {"v": [v_min, v_max], "h": [-2.23, 2.23], "w": [-15.7, 15.7]})
        return [{"shot": [rng.uniform(*bounds[k]) for k in ("v", "h", "w")], "origin": "continuous_uniform"} for _ in range(count)]
    result = []
    anchors = []
    preferred = []
    for values in scene.get("candidate_shots", []):
        if len(values) != 3 or not all(math.isfinite(float(v)) for v in values):
            raise ValueError("candidate_shots must contain finite v,h,w triples")
        # Actual predictor clamp; old seeds get fresh current-version labels.
        v, h, w = (float(v) for v in values)
        preferred.append([1.0 if v < 0.0001 else min(6.0, v), max(-2.23, min(2.23, h)), max(-15.7, min(15.7, w))])
    # Column-aligned entrances are sampling proposals, not a claim of an
    # inverse physical solution. Actual outcomes determine all labels.
    for stone in scene["stones"]:
        h = max(-2.23, min(2.23, stone["x"] - HOUSE_X))
        for v in (3.0, 3.4, 4.2, 6.0):
            anchors.append([v, h, 0.0])
    anchors.extend([[3.0, 0.0, 0.0], [2.7, -1.0, 0.0], [2.7, 1.0, 0.0], [3.35, 0.18, 9.42], [3.35, -0.18, -9.42]])
    rng.shuffle(anchors)
    permutations = []
    for _ in range(3):
        order = list(range(count))
        rng.shuffle(order)
        permutations.append(order)
    for i in range(count):
        if i < min(len(preferred), max(1, count // 4)):
            shot = preferred[i]
            origin = "supplied_initial"
        elif i % 3 == 0:
            shot = list(anchors[(i // 3) % len(anchors)])
            shot[0] = max(v_min, min(v_max, shot[0]))
            origin = "column_anchor"
        elif i % 3 == 1:
            base = anchors[i % len(anchors)]
            shot = [max(v_min, min(v_max, base[0] + rng.uniform(-0.35, 0.35))), max(-2.23, min(2.23, base[1] + rng.uniform(-0.16, 0.16))), rng.uniform(-3.0, 3.0)]
            origin = "anchor_neighbour"
        else:
            u = [(permutations[k][i] + rng.random()) / count for k in range(3)]
            shot = [v_min + (v_max-v_min)*u[0], -2.23 + 4.46*u[1], -15.7 + 31.4*u[2]]
            origin = "stratified_global"
        result.append({"shot": shot, "origin": origin})
    return result
