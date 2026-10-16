"""Extract original forward samples into solver inputs and separate references.

python -m training_research.export_solver_samples --output training_research/datasets/forward_samples_20261004
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
import gzip
import io
import json
from pathlib import Path

from training_research.build_inverse_sampled_suite import FORWARD_RUNS, observed_task
from training_research.inverse_dataset.cli import file_sha
from training_research.inverse_dataset.sampling import validate_scene


def extract(record):
    """Return exactly a public solver request and its offline reference."""
    task = observed_task(record)
    if task is None:
        return None
    selection, _ = task
    source = record["requested_scene"]
    scene = validate_scene({"active_index": record["active_index"],
        "stones": source["stones"], "selection": selection})
    if scene["scene_key"] != record["scene_key"]:
        raise ValueError("source board identity changed during extraction")
    request = {"record_id": record["record_id"], "scene_key": scene["scene_key"],
        "active_index": scene["active_index"],
        "stones": [{k: s[k] for k in ("index", "x", "y", "yaw")} for s in scene["stones"]],
        "selection": selection}
    relevant = {s["index"] for s in scene["stones"]} | {scene["active_index"]}
    reference = {"record_id": record["record_id"], "shot": record["shot"],
        "physics_seed": record["physics_seed"], "physical_final": [
            {k: s[k] for k in ("index", "enabled", "x", "y", "yaw")}
            for s in record["physical_final"] if s["index"] in relevant]}
    return request, reference


@contextmanager
def compressed_jsonl(path):
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=6) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as stream:
                yield stream


def export(runs, output):
    files = {name: sorted((runs/name/"shards").glob("*.raw.jsonl")) for name in FORWARD_RUNS}
    if any(not paths for paths in files.values()):
        raise ValueError("all six original forward batches are required")
    output.mkdir(parents=True, exist_ok=False)
    batches = []
    boards = set()
    for name, paths in files.items():
        request_path = output/(name+".inputs.jsonl.gz")
        reference_path = output/(name+".references.jsonl.gz")
        counts = Counter()
        sources = []
        with compressed_jsonl(request_path) as inputs, compressed_jsonl(reference_path) as references:
            for source in paths:
                before = source.stat()
                source_hash = file_sha(source)
                with source.open(encoding="utf-8") as stream:
                    for line_number, line in enumerate(stream, 1):
                        record = json.loads(line)
                        counts["raw_records"] += 1
                        pair = extract(record)
                        if pair is None:
                            reason = ("not_complete" if record.get("status") != "complete" else
                                "rule_violation" if record.get("rule_violations") else "not_settled")
                            counts["excluded_"+reason] += 1
                            continue
                        request, reference = pair
                        reference.update(source_shard=source.relative_to(runs/name).as_posix(),
                                         source_line=line_number)
                        a, b = [json.dumps(r, ensure_ascii=False, separators=(",", ":"), allow_nan=False)+"\n"
                                for r in (request, reference)]
                        inputs.write(a)
                        references.write(b)
                        counts["records"] += 1
                        counts["inputs_uncompressed_bytes"] += len(a.encode("utf-8"))
                        counts["references_uncompressed_bytes"] += len(b.encode("utf-8"))
                        boards.add(request["scene_key"])
                after = source.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    raise RuntimeError("source changed during extraction: "+str(source))
                sources.append({"path": (Path(name)/source.relative_to(runs/name)).as_posix(),
                    "bytes": before.st_size, "sha256": source_hash})
        batch = {"name": name, "counts": dict(counts), "sources": sources,
            "inputs": {"file": request_path.name, "bytes": request_path.stat().st_size, "sha256": file_sha(request_path)},
            "references": {"file": reference_path.name, "bytes": reference_path.stat().st_size, "sha256": file_sha(reference_path)}}
        batches.append(batch)
        print(json.dumps({"batch": name, "records": counts["records"],
            "gzip_bytes": batch["inputs"]["bytes"]+batch["references"]["bytes"]}), flush=True)
    totals = Counter()
    for batch in batches:
        totals.update(batch["counts"])
    manifest = {"schema": "compact_forward_solver_samples_v1", "status": "complete",
        "source_policy": "original_forward_samples_only", "counts": dict(totals),
        "distinct_boards": len(boards), "source_bytes": sum(s["bytes"] for b in batches for s in b["sources"]),
        "compressed_bytes": sum(b[k]["bytes"] for b in batches for k in ("inputs", "references")),
        "batches": batches, "extractor_sha256": file_sha(Path(__file__)),
        "scope": "All legal settled records in the six original forward batches; no search certificates. Inputs are direct BudgetedShotSolver requests. References, source action, seed and actual final poses are separate and must not initialize search. Goals use actual achieved terminal regions at 0.15 m and retain observed-task collision/rule acceptance. Input coordinates are original reset inputs; final coordinates are observed outputs. No numeric rounding. This is extraction, not a new solve-rate measurement."}
    (output/"manifest.json").write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2)+"\n").encode("utf-8"))
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=Path("training_research/runs"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = export(args.runs, args.output)
    print(json.dumps({k: report[k] for k in ("counts", "distinct_boards", "source_bytes", "compressed_bytes")}))


if __name__ == "__main__":
    main()
