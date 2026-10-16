"""Joint action examples weighted by forest leaves, rather than leaf means.

Offline builder reuses the existing board-excluded impact-coordinate trees.
Online inference reads exported other-board examples only. This is a proposal
prior, inspired by conditional forest distributions (Meinshausen, JMLR 2006),
not a new forward model and not a quantile-wise recombination of action axes.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from training_research.contact_seed_forest import (ROOT, IMPACT, FOLDS, board_fold,
    impact_features, load_fold)

DEFAULT = ROOT/"runs/contact_distribution_v3_paired_20261016"


def leaf_nodes(model, x):
    nodes = model["offsets"][:-1].copy()
    for _ in range(int(model["max_depth"])+1):
        feature = model["features"][nodes]
        live = feature >= 0
        if not live.any():
            return nodes
        trees = np.flatnonzero(live)
        node = nodes[live]
        right = x[feature[live]] > model["thresholds"][node]
        nodes[live] = model["offsets"][trees]+np.where(right, model["right"][node], model["left"][node])
    raise RuntimeError("invalid exported distribution tree depth")


def conditional_weights(model, x):
    weights = np.zeros(len(model["training_y"]))
    for node in leaf_nodes(model, x):
        a, b = model["leaf_row_offsets"][node:node+2]
        rows = model["leaf_row_indices"][a:b]
        if not len(rows):
            raise RuntimeError("empty exported leaf")
        weights[rows] += 1./len(rows)
    return weights/len(model["offsets"][:-1])


@lru_cache(maxsize=128)
def _anchor(v, w, y):
    from training_research.inverse_initials import path_array, interpolate
    point = interpolate(path_array(float(v), float(w)), float(y)+.29)
    return None if point is None else float(point[0][0])


@lru_cache(maxsize=5)
def joint_groups(path, fold):
    model, _ = load_fold(path, fold)
    _, first, group = np.unique(np.round(model["training_y"], 12), axis=0,
                                return_index=True, return_inverse=True)
    return first, group


def proposals(request, *, path=DEFAULT, limit=12, feature_function=impact_features, elapsed=None, deadline=None):
    key = request["scene_key"]
    model, training_boards = load_fold(str(path), board_fold(key))
    if key in training_boards or np.any(model["training_row_boards"] == key):
        raise ValueError("current board leaked into conditional distribution")
    stones = {s["index"]: s for s in request["stones"]}
    output = []
    for first in request["selection"].get("first_contact_any", []):
        if first not in stones:
            continue
        target = stones[first]
        weights = conditional_weights(model, feature_function(request, first))
        representatives, groups = joint_groups(str(path), board_fold(key))
        mass = np.bincount(groups, weights=weights, minlength=len(representatives))
        retained = []
        for group in np.argsort(-mass, kind="stable"):
            if elapsed is not None and elapsed() >= deadline:
                break
            if mass[group] <= 0.:
                break
            row = representatives[group]
            value = model["training_y"][row]
            # Keep a joint observed response, never independent axis quantiles.
            if any(np.linalg.norm((value-other)/np.asarray((.035, .10, .08))) < .5 for other in retained):
                continue
            v, b, w = value*np.asarray((6., .29, 15.7))
            anchor = _anchor(float(v), float(w), target["y"])
            if anchor is None:
                continue
            h = target["x"]+b-anchor
            if abs(h) > 2.23:
                continue
            retained.append(value)
            output.append((float(v), float(h), float(w)))
            if len(retained) >= limit:
                break
    return list(dict.fromkeys(output))[:limit]


def _rows(data):
    sources = {}
    for filename in sorted(data.glob("*.references.jsonl.gz")):
        sources[filename.name] = hashlib.sha256(filename.read_bytes()).hexdigest()
    x, y, boards = [], [], []
    omitted = []
    for filename in sorted(data.glob("*.inputs.jsonl.gz")):
        sources[filename.name] = hashlib.sha256(filename.read_bytes()).hexdigest()
        reference_path = filename.with_name(filename.name.replace(".inputs.", ".references."))
        import itertools
        with gzip.open(filename, "rt", encoding="utf-8") as stream, gzip.open(reference_path, "rt", encoding="utf-8") as refs:
            for line_number, (line, refline) in enumerate(itertools.zip_longest(stream, refs), 1):
                if line is None or refline is None:
                    raise ValueError("paired compact files have different row counts")
                row, reference = json.loads(line), json.loads(refline)
                if row["record_id"] != reference["record_id"]:
                    raise ValueError("paired compact row IDs differ")
                targets = row["selection"].get("first_contact_any", [])
                if len(targets) != 1 or row["selection"].get("require_no_contact"):
                    continue
                target = next(s for s in row["stones"] if s["index"] == targets[0])
                v, h, w = reference["shot"]
                anchor = _anchor(v, w, target["y"])
                if anchor is None:
                    omitted.append({"input_file": filename.name, "line": line_number, "record_id": row["record_id"]})
                    continue
                x.append(impact_features(row, targets[0]))
                y.append((v/6., (h+anchor-target["x"])/.29, w/15.7))
                boards.append(row["scene_key"])
                if len(x) % 2000 == 0:
                    print(json.dumps({"prepared": len(x)}), flush=True)
    return np.asarray(x), np.asarray(y), np.asarray(boards), sources, omitted


def build(data, output, base=IMPACT):
    if output.exists():
        raise ValueError("distribution model output must be new")
    # Native mean-path binding must precede optional numerical library imports.
    from training_research.inverse_dataset.cli import make_environment
    environment = make_environment()
    started = time.perf_counter()
    x, y, boards, sources, omitted = _rows(data)
    folds = np.asarray([board_fold(k) for k in boards])
    base_manifest = json.loads((base/"manifest.json").read_text(encoding="utf-8"))
    if sources != base_manifest["source_sha256"]:
        raise ValueError("distribution source differs from original impact forest")
    if len(x) != base_manifest["records"]:
        raise ValueError("distribution training row count differs from original forest")
    output.mkdir(parents=True)
    manifest = {"coordinate_mode": "joint_impact_examples", "records": len(x),
                "physical_boards": len(set(boards)), "features": x.shape[1],
                "source_policy": "original forward labels offline only; entire query-board fold excluded",
                "reference_pairing": "matching gzip stem and one-based row; record_id is not globally unique",
                "online_policy": "request-only tree paths and jointly observed other-board actions, no reference files or query actions",
                "split_policy": base_manifest["split_policy"], "source_sha256": sources,
                "base_manifest_sha256": hashlib.sha256((base/"manifest.json").read_bytes()).hexdigest(),
                "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "omitted_training_rows": omitted, "omission_reason": "mean-path anchor unavailable; benchmark tasks never filtered",
                "models": {}}
    for fold in range(FOLDS):
        original, training_boards = load_fold(str(base), fold)
        mask = folds != fold
        bx, by, bb = x[mask], y[mask], boards[mask]
        if frozenset(bb) != training_boards:
            raise ValueError("reconstructed training boards differ from original model")
        packed = dict(original)
        counts, indices = [], []
        checked = 0
        for tree in range(len(original["offsets"])-1):
            start, end = original["offsets"][tree:tree+2]
            nodes = np.full(len(bx), start, dtype=np.int32)
            for _ in range(int(original["max_depth"])+1):
                feature = original["features"][nodes]
                live = feature >= 0
                if not live.any():
                    break
                n = nodes[live]
                right = bx[live, feature[live]] > original["thresholds"][n]
                nodes[live] = start+np.where(right, original["right"][n], original["left"][n])
            if np.any(original["features"][nodes] >= 0):
                raise RuntimeError("tree traversal did not reach leaves")
            order = np.argsort(nodes, kind="stable")
            size = np.bincount(nodes-start, minlength=end-start)
            offsets = np.r_[0, np.cumsum(size)]
            # Existing leaf means must be recovered from exactly these examples.
            leaves = np.flatnonzero(size)
            for leaf in leaves[::max(1, len(leaves)//8)][:8]:
                rows = order[offsets[leaf]:offsets[leaf+1]]
                if not np.allclose(np.mean(by[rows], axis=0), original["values"][start+leaf], rtol=0., atol=1e-11):
                    raise AssertionError("leaf examples do not recover original trained response")
                checked += 1
            counts.append(size)
            indices.append(order)
        packed.update(leaf_row_offsets=np.r_[0, np.cumsum(np.concatenate(counts))].astype(np.int32),
                      leaf_row_indices=np.concatenate(indices).astype(np.int32),
                      training_y=by, training_row_boards=bb)
        for sample in x[~mask][:64]:
            weights = conditional_weights(packed, sample)
            if np.any(weights < 0.) or not np.isclose(weights.sum(), 1., rtol=0., atol=1e-12):
                raise AssertionError("invalid conditional distribution weights")
        filename = output/("fold%d.npz" % fold)
        np.savez_compressed(filename, **packed)
        manifest["models"][str(fold)] = {"file": filename.name,
            "sha256": hashlib.sha256(filename.read_bytes()).hexdigest(),
            "training_boards": sorted(training_boards), "excluded_boards": sorted(set(boards[~mask])),
            "training_records": len(by), "leaf_mean_checks": checked, "distribution_checks": min(64, int((~mask).sum())),
            "bytes": filename.stat().st_size}
        print(json.dumps({"fold": fold, "leaf_mean_checks": checked, "bytes": filename.stat().st_size}), flush=True)
    manifest["build_seconds"] = time.perf_counter()-started
    (output/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT/"datasets/forward_samples_20261004")
    parser.add_argument("--base", type=Path, default=IMPACT)
    parser.add_argument("--output", type=Path, default=DEFAULT)
    args = parser.parse_args(argv)
    import atexit
    import os
    if os.name == "nt":
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
