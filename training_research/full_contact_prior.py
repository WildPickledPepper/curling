"""Complete-board inverse features, with required moving stones first.

All old stones and all their requested terminal constraints are represented.
Labels are reconstructed from the previously verified original-forward-only
distribution export, with identical row ordering checked across all five folds.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

from training_research.contact_seed_forest import ROOT, FOLDS, board_fold, impact_features, _goal_features, _pack
from training_research.contact_distribution_prior import DEFAULT as BASE, conditional_weights

DEFAULT = ROOT/"runs/contact_distribution_full_v4_paired_20261016"


def full_features(request, first):
    stones = {s["index"]: s for s in request["stones"]}
    target = stones[first]
    goals = request["selection"]["goal"]["stones"]
    def needed(s):
        g = goals.get(str(s["index"]), {})
        if not g.get("required", True):
            return False
        if g.get("type") == "OUT_OF_PLAY":
            return True
        if g.get("type") == "OUT_OF_HOUSE":
            return math.hypot(s["x"]-2.375, s["y"]-4.88) <= 1.975
        return g.get("type") == "IN_REGION" and math.hypot(s["x"]-g["x"], s["y"]-g["y"]) > g["radius"]
    neighbours = sorted((s for i, s in stones.items() if i != first),
                        key=lambda s: (not needed(s), (s["x"]-target["x"])**2+(s["y"]-target["y"])**2, s["index"]))
    extra = []
    for stone in neighbours:
        yaw = stone.get("yaw", 0.)
        extra += [(stone["x"]-target["x"])/2.375, (stone["y"]-target["y"])/10.525,
                  math.sin(yaw), math.cos(yaw), float(stone["index"] % 2 == request["active_index"] % 2), 1.]
        extra += _goal_features(goals.get(str(stone["index"]), {}), target)
    extra += [0.]*(15*(15-len(neighbours)))
    result = np.r_[impact_features(request, first), np.asarray(extra, dtype=np.float32)].astype(np.float32)
    assert result.shape == (319,) and np.isfinite(result).all()
    return result


def proposals(request, *, limit=12, elapsed=None, deadline=None):
    from training_research.contact_distribution_prior import proposals as distribution
    return distribution(request, path=DEFAULT, limit=limit, feature_function=full_features,
                        elapsed=elapsed, deadline=deadline)


def _training_rows(data, base):
    parent = json.loads((base/"manifest.json").read_text(encoding="utf-8"))
    for name, digest in parent["source_sha256"].items():
        if hashlib.sha256((data/name).read_bytes()).hexdigest() != digest:
            raise ValueError("full-board model source differs from original forward export")
    if parent.get("reference_pairing") != "matching gzip stem and one-based row; record_id is not globally unique":
        raise ValueError("parent labels must use namespace-safe original pairing")
    omitted = {(r["input_file"], r["line"]) for r in parent["omitted_training_rows"]}
    features, boards = [], []
    for filename in sorted(data.glob("*.inputs.jsonl.gz")):
        with gzip.open(filename, "rt", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                row = json.loads(line)
                targets = row["selection"].get("first_contact_any", [])
                if len(targets) != 1 or row["selection"].get("require_no_contact") or (filename.name, line_number) in omitted:
                    continue
                features.append(full_features(row, targets[0]))
                boards.append(row["scene_key"])
    x, boards = np.asarray(features), np.asarray(boards)
    folds = np.asarray([board_fold(k) for k in boards])
    y = np.zeros((len(x), 3))
    if len(x) != parent["records"]:
        raise ValueError("reconstructed row count differs")
    # These two complementary training folds cover all rows. Held-out rows
    # are only used as labels for the other four models, never their own.
    for fold in range(FOLDS):
        mask = folds != fold
        info = parent["models"][str(fold)]
        filename = base/info["file"]
        if hashlib.sha256(filename.read_bytes()).hexdigest() != info["sha256"]:
            raise ValueError("parent distribution checksum mismatch")
        with np.load(filename, allow_pickle=False) as model:
            if not np.array_equal(boards[mask], model["training_row_boards"]):
                raise ValueError("reconstructed training row order differs")
            labels = model["training_y"]
            if fold == 0:
                y[mask] = labels
            elif fold == 1:
                missing = folds[mask] == 0
                y[np.flatnonzero(mask)[missing]] = labels[missing]
                if not np.array_equal(y[mask], labels):
                    raise ValueError("joint labels differ across parent folds")
            elif not np.array_equal(y[mask], labels):
                raise ValueError("joint labels differ across parent folds")
    return x, y, boards, folds, parent


def attach_examples(forest, x, y, boards):
    packed = _pack(forest)
    counts, rows = [], []
    checked = 0
    for tree in forest.estimators_:
        leaves = tree.apply(x)
        order = np.argsort(leaves, kind="stable")
        size = np.bincount(leaves, minlength=tree.tree_.node_count)
        offsets = np.r_[0, np.cumsum(size)]
        occupied = np.flatnonzero(size)
        for leaf in occupied[::max(1, len(occupied)//8)][:8]:
            selected = order[offsets[leaf]:offsets[leaf+1]]
            if not np.allclose(y[selected].mean(axis=0), tree.tree_.value[leaf, :, 0], rtol=0., atol=1e-11):
                raise AssertionError("joint leaf examples differ from training response")
            checked += 1
        counts.append(size)
        rows.append(order)
    packed.update(leaf_row_offsets=np.r_[0, np.cumsum(np.concatenate(counts))].astype(np.int32),
                  leaf_row_indices=np.concatenate(rows).astype(np.int32),
                  training_y=y, training_row_boards=boards,
                  feature_mode=np.asarray("full_board_affected_first"))
    return packed, checked


def build(data, output, base=BASE):
    if output.exists():
        raise ValueError("model output must be new")
    from training_research.inverse_dataset.cli import make_environment
    environment = make_environment()  # Initialise native payload before SciPy/sklearn.
    from sklearn.ensemble import ExtraTreesRegressor
    import sklearn
    started = time.perf_counter()
    x, y, boards, folds, parent = _training_rows(data, base)
    output.mkdir(parents=True)
    manifest = {"records": len(x), "physical_boards": len(set(boards)), "features": x.shape[1],
                "feature_policy": "full initial board and every old-stone goal; required moving stones sorted first",
                "source_policy": parent["source_policy"], "source_sha256": parent["source_sha256"],
                "reference_pairing": parent["reference_pairing"],
                "split_policy": parent["split_policy"], "omitted_training_rows": parent["omitted_training_rows"],
                "base_manifest_sha256": hashlib.sha256((base/"manifest.json").read_bytes()).hexdigest(),
                "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "sklearn": sklearn.__version__, "models": {}}
    for fold in range(FOLDS):
        mask = folds != fold
        forest = ExtraTreesRegressor(n_estimators=96, max_depth=14, min_samples_leaf=2,
                                    max_features=.8, n_jobs=1, random_state=20261016+fold)
        forest.fit(x[mask], y[mask])
        packed, checked = attach_examples(forest, x[mask], y[mask], boards[mask])
        for sample in x[~mask][:64]:
            weights = conditional_weights(packed, sample)
            if not np.isclose(weights.sum(), 1., rtol=0., atol=1e-12) or np.any(weights < 0.):
                raise AssertionError("invalid exported distribution")
        filename = output/("fold%d.npz" % fold)
        np.savez_compressed(filename, **packed)
        manifest["models"][str(fold)] = {"file": filename.name,
            "sha256": hashlib.sha256(filename.read_bytes()).hexdigest(), "bytes": filename.stat().st_size,
            "training_records": int(mask.sum()), "training_boards": sorted(set(boards[mask])),
            "excluded_boards": sorted(set(boards[~mask])), "leaf_mean_checks": checked,
            "distribution_checks": min(64, int((~mask).sum()))}
        print(json.dumps({"fold": fold, "bytes": filename.stat().st_size, "leaf_mean_checks": checked}), flush=True)
    manifest["build_seconds"] = time.perf_counter()-started
    (output/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT/"datasets/forward_samples_20261004")
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--output", type=Path, default=DEFAULT)
    args = parser.parse_args(argv)
    import os
    if os.name == "nt":
        import atexit
        import ctypes as C
        fn = C.WinDLL("kernel32", use_last_error=True).SetThreadExecutionState
        fn.argtypes = (C.c_uint32,)
        fn.restype = C.c_uint32
        if not fn(0x80000001):
            raise C.WinError(C.get_last_error())
        atexit.register(fn, 0x80000000)
    build(args.data, args.output, args.base)


if __name__ == "__main__":
    main()
