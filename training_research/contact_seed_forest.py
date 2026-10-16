"""Board-held-out, multi-candidate inverse priors from original forward data.

Training reads reference actions as labels. Online features take only the
current request. Every test board is excluded in its entirety via fixed folds.
Tree predictions propose actions; only the existing physical predicate accepts.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import gzip
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
DEFAULT = ROOT/"runs/contact_seed_forest_v1_paired_20261016"
IMPACT = ROOT/"runs/contact_seed_forest_impact_v2_paired_20261016"
KINDS = ("ANY", "IN_REGION", "OUT_OF_PLAY", "OUT_OF_HOUSE", "SURVIVE")
SCALE = np.asarray((6., 2.23, 15.7))
FOLDS = 5


def board_fold(scene_key):
    return int(scene_key[:16], 16) % FOLDS


def _goal_features(goal, origin):
    kind = goal.get("type", "ANY")
    result = [float(kind == k) for k in KINDS]
    result += ([(goal["x"]-origin["x"])/2.375, (goal["y"]-origin["y"])/10.525,
                goal["radius"]/2.375] if kind == "IN_REGION" else [0., 0., 0.])
    return result+[float(goal.get("required", False))]


def encode_request(request, first):
    """Pure request features: no action, final-state reference or seed access."""
    stones = {s["index"]: s for s in request["stones"]}
    target = stones[first]
    active = request["active_index"]
    goals = request["selection"]["goal"]["stones"]
    yaw = target.get("yaw", 0.)
    values = [(target["x"]-2.375)/2.375, (target["y"]-4.88)/10.525,
              math.sin(yaw), math.cos(yaw), float(first % 2 == active % 2),
              active/15., len(stones)/16.]
    values += _goal_features(goals.get(str(first), {}), target)
    values += _goal_features(goals.get(str(active), {}), target)
    neighbours = sorted((s for i, s in stones.items() if i != first),
                        key=lambda s: ((s["x"]-target["x"])**2+(s["y"]-target["y"])**2, s["index"]))
    for j in range(4):
        if j >= len(neighbours):
            values += [0.]*15
            continue
        stone = neighbours[j]
        yaw = stone.get("yaw", 0.)
        values += [(stone["x"]-target["x"])/2.375, (stone["y"]-target["y"])/10.525,
                   math.sin(yaw), math.cos(yaw), float(stone["index"] % 2 == active % 2), 1.]
        values += _goal_features(goals.get(str(stone["index"]), {}), target)
    selection = request["selection"]
    values += [float(selection.get("require_single_first_contact", False)),
               len(selection.get("required_collision_pairs", []))/4., len(goals)/16.]
    result = np.asarray(values, dtype=np.float32)
    assert result.shape == (88,) and np.isfinite(result).all()
    return result


def predict_trees(model, x):
    """NumPy-only equivalent of the exported sklearn tree paths and leaves."""
    nodes = model["offsets"][:-1].copy()
    for _ in range(int(model["max_depth"])+1):
        features = model["features"][nodes]
        live = features >= 0
        if not np.any(live):
            return model["values"][nodes]
        indices = np.flatnonzero(live)
        offsets = model["offsets"][indices]
        right = x[features[live]] > model["thresholds"][nodes[live]]
        children = np.where(right, model["right"][nodes[live]], model["left"][nodes[live]])
        nodes[live] = offsets+children
    raise RuntimeError("invalid exported tree depth")


def impact_features(request, first):
    target = next(s for s in request["stones"] if s["index"] == first)
    extra = []
    goals = request["selection"]["goal"]["stones"]
    for index in (request["active_index"], first):
        goal = goals.get(str(index), {})
        if goal.get("type") == "IN_REGION":
            dx, dy = goal["x"]-target["x"], goal["y"]-target["y"]
            distance = math.hypot(dx, dy)
            extra += [distance/10., dx/max(distance, 1e-8), dy/max(distance, 1e-8)]
        else:
            extra += [0., 0., 0.]
    return np.concatenate((encode_request(request, first), np.asarray(extra, dtype=np.float32)))


@lru_cache(maxsize=256)
def _impact_anchor(v, w, y):
    from training_research.inverse_initials import path_array, interpolate
    anchor = interpolate(path_array(v, w), y+.29)
    return None if anchor is None else float(anchor[0][0])


def impact_action(shot, target, *, decode=False):
    """Exact inverse affine h transform for fixed v,w and mean-path anchor."""
    value = np.asarray(shot, dtype=float).copy()
    anchor = _impact_anchor(float(value[0]), float(value[2]), float(target["y"]))
    if anchor is None:
        return None
    shift = anchor-target["x"]
    value[1] = value[1]*.29-shift if decode else (value[1]+shift)/.29
    return value


@lru_cache(maxsize=5)
def load_fold(path, fold):
    path = Path(path)
    manifest = json.loads((path/"manifest.json").read_text(encoding="utf-8"))
    info = manifest["models"][str(fold)]
    filename = path/info["file"]
    if hashlib.sha256(filename.read_bytes()).hexdigest() != info["sha256"]:
        raise ValueError("learned prior checksum mismatch")
    with np.load(filename, allow_pickle=False) as data:
        arrays = {k: data[k] for k in data.files}
    return arrays, frozenset(info["training_boards"])


def learned_initials(request, *, path=DEFAULT, limit=12):
    key = request["scene_key"]
    fold = board_fold(key)
    model, training_boards = load_fold(str(path), fold)
    if key in training_boards:
        raise ValueError("current board leaked into learned prior")
    stones = {s["index"]: s for s in request["stones"]}
    targets = request["selection"].get("first_contact_any", [])
    proposals = []
    for first in targets:
        if first not in stones:
            continue
        impact = str(model.get("coordinate_mode", "release")) == "impact"
        estimates = predict_trees(model, impact_features(request, first) if impact else encode_request(request, first))
        # Preserve multiple modes: a global mean plus deterministic farthest
        # starts and cluster representatives, rather than averaging every mode.
        centers = [np.mean(estimates, axis=0)]
        diversity = np.asarray((.06, .15, .08)) if impact else np.asarray((.06, .02, .08))
        for _ in range(min(limit-1, len(estimates))):
            distances = np.min([np.sum(((estimates-c)/diversity)**2, axis=1) for c in centers], axis=0)
            centers.append(estimates[int(np.argmax(distances))].copy())
        for _ in range(6):
            distance = np.asarray([np.sum(((estimates-c)/diversity)**2, axis=1) for c in centers])
            labels = np.argmin(distance, axis=0)
            for j in range(len(centers)):
                group = estimates[labels == j]
                if len(group):
                    mean = np.mean(group, axis=0)
                    centers[j] = group[int(np.argmin(np.sum((group-mean)**2, axis=1)))]
        # The ensemble mean remains an additional candidate even after clustering.
        support = np.bincount(labels, minlength=len(centers))
        ranked = sorted(range(len(centers)), key=lambda j: (-int(support[j]), j))
        for estimate in [np.mean(estimates, axis=0)]+[centers[j] for j in ranked]:
            if impact:
                shot = impact_action(estimate*np.asarray((6., 1., 15.7)), stones[first], decode=True)
                if shot is None or abs(shot[1]) > 2.23:
                    continue
            else:
                shot = estimate*SCALE
                shot[1] += stones[first]["x"]-2.375
            proposals.append(tuple(float(v) for v in shot))
    return list(dict.fromkeys(proposals))[:limit]


def _pack(forest):
    sizes = [t.tree_.node_count for t in forest.estimators_]
    return {"offsets": np.asarray([0]+list(np.cumsum(sizes)), dtype=np.int32),
            "left": np.concatenate([t.tree_.children_left for t in forest.estimators_]).astype(np.int32),
            "right": np.concatenate([t.tree_.children_right for t in forest.estimators_]).astype(np.int32),
            "features": np.concatenate([t.tree_.feature for t in forest.estimators_]).astype(np.int16),
            "thresholds": np.concatenate([t.tree_.threshold for t in forest.estimators_]),
            "values": np.concatenate([t.tree_.value[:, :, 0] for t in forest.estimators_]),
            "max_depth": np.asarray(max(t.tree_.max_depth for t in forest.estimators_))}


def train(data, output, trees=96, depth=14, coordinate_mode="release"):
    # The mean-path helper initialises the bundled native runtime. On the CP39
    # Windows payload that must happen before sklearn's SciPy/pandas imports.
    native_environment = None
    if coordinate_mode == "impact":
        from training_research.inverse_dataset.cli import make_environment
        native_environment = make_environment()
    from sklearn.ensemble import ExtraTreesRegressor
    import sklearn
    if output.exists():
        raise ValueError("model output must be new")
    sources = {}
    for filename in sorted(data.glob("*.references.jsonl.gz")):
        sources[filename.name] = hashlib.sha256(filename.read_bytes()).hexdigest()
    features, actions, boards = [], [], []
    for filename in sorted(data.glob("*.inputs.jsonl.gz")):
        sources[filename.name] = hashlib.sha256(filename.read_bytes()).hexdigest()
        reference_path = filename.with_name(filename.name.replace(".inputs.", ".references."))
        import itertools
        with gzip.open(filename, "rt", encoding="utf-8") as stream, gzip.open(reference_path, "rt", encoding="utf-8") as refs:
            for line, reference_line in itertools.zip_longest(stream, refs):
                if line is None or reference_line is None:
                    raise ValueError("paired compact files have different row counts")
                row, reference = json.loads(line), json.loads(reference_line)
                if row["record_id"] != reference["record_id"]:
                    raise ValueError("paired compact row IDs differ")
                targets = row["selection"].get("first_contact_any", [])
                if len(targets) != 1 or row["selection"].get("require_no_contact"):
                    continue
                first = targets[0]
                target = next(s for s in row["stones"] if s["index"] == first)
                shot = np.asarray(reference["shot"], dtype=float).copy()
                if coordinate_mode == "impact":
                    encoded = impact_action(shot, target)
                    if encoded is None:
                        continue
                    if not np.allclose(impact_action(encoded, target, decode=True), shot, rtol=0., atol=1e-12):
                        raise AssertionError("impact coordinate round-trip differs")
                    features.append(impact_features(row, first))
                    actions.append(encoded/np.asarray((6., 1., 15.7)))
                else:
                    shot[1] -= target["x"]-2.375
                    features.append(encode_request(row, first))
                    actions.append(shot/SCALE)
                boards.append(row["scene_key"])
    x, y, boards = np.asarray(features), np.asarray(actions), np.asarray(boards)
    folds = np.asarray([board_fold(k) for k in boards])
    output.mkdir(parents=True)
    manifest = {"source_policy": "original_forward_reference_actions_as_offline_labels_only",
                "online_feature_policy": "initial request and requested goal only; no reference outcomes, actions or seeds",
                "split_policy": "5 physical-board folds; model k excludes ALL rows from every board in fold k",
                "records": len(x), "physical_boards": len(set(boards)), "features": x.shape[1],
                "trees": trees, "max_depth": depth, "sklearn": sklearn.__version__,
                "coordinate_mode": coordinate_mode,
                "reference_pairing": "matching gzip stem and one-based row; record_id is not globally unique",
                "source_sha256": sources, "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "models": {}}
    for fold in range(FOLDS):
        mask = folds != fold
        forest = ExtraTreesRegressor(n_estimators=trees, max_depth=depth, min_samples_leaf=2,
                                    max_features=.8, random_state=20261016+fold, n_jobs=1)
        forest.fit(x[mask], y[mask])
        packed = _pack(forest)
        packed["coordinate_mode"] = np.asarray(coordinate_mode)
        checked = x[~mask][:64]
        for sample in checked:
            actual = predict_trees(packed, sample)
            expected = np.asarray([t.predict(sample[None])[0] for t in forest.estimators_])
            if not np.array_equal(actual, expected):
                raise AssertionError("exported leaf prediction differs from sklearn")
        filename = output/("fold%d.npz" % fold)
        np.savez_compressed(filename, **packed)
        train_boards, heldout_boards = sorted(set(boards[mask])), sorted(set(boards[~mask]))
        assert not set(train_boards) & set(heldout_boards)
        manifest["models"][str(fold)] = {"file": filename.name,
            "sha256": hashlib.sha256(filename.read_bytes()).hexdigest(), "bytes": filename.stat().st_size,
            "training_records": int(mask.sum()), "training_boards": train_boards,
            "excluded_boards": heldout_boards, "export_checked": len(checked)}
        print(json.dumps({"fold": fold, "training_records": int(mask.sum()), "excluded_boards": len(heldout_boards),
                          "bytes": filename.stat().st_size}), flush=True)
    (output/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT/"datasets/forward_samples_20261004")
    parser.add_argument("--output", type=Path, default=DEFAULT)
    parser.add_argument("--trees", type=int, default=96)
    parser.add_argument("--depth", type=int, default=14)
    parser.add_argument("--coordinate-mode", choices=("release", "impact"), default="release")
    args = parser.parse_args(argv)
    os.environ["OMP_NUM_THREADS"] = "1"
    execution_state = None
    if os.name == "nt":
        import ctypes as C
        execution_state = C.WinDLL("kernel32", use_last_error=True).SetThreadExecutionState
        execution_state.argtypes = (C.c_uint32,)
        execution_state.restype = C.c_uint32
        if not execution_state(0x80000001):
            raise C.WinError(C.get_last_error())
    try:
        train(args.data, args.output, args.trees, args.depth, args.coordinate_mode)
    finally:
        if execution_state:
            execution_state(0x80000000)


if __name__ == "__main__":
    main()
