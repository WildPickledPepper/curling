"""Verify inverse arrays against raw observations and report actual coverage."""
from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path

import numpy as np

from .schema import achieved_views, encode_action, encode_input, split_for_group
from .selection import failure_reason


def audit_dataset(directory):
    from .cli import file_sha
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "complete":
        raise ValueError("audit requires a completed dataset")
    config = manifest.get("config", manifest)
    max_views, split_seed = config["views_per_result"], config["split_seed"]
    raw_paths = sorted((directory / "shards").glob("*.raw.jsonl"))
    if not raw_paths:
        raise ValueError("no raw shards in dataset; audit a collected or selected dataset")
    expected_hashes = {s["shard_id"]: s for s in manifest["shards"]}
    for source, sha in manifest.get("source_raw_sha256", {}).items():
        if file_sha(Path(source)) != sha:
            raise ValueError("source raw data changed")
    counts, by_family, by_tactic, splits = Counter(), defaultdict(Counter), Counter(), Counter()
    family_boards, family_groups, family_successful = defaultdict(set), defaultdict(set), defaultdict(set)
    seen_records, groups, boards = set(), {}, {}
    candidates = defaultdict(lambda: {"seeds": set(), "successes": 0, "attempts": 0})
    # Candidate tables store counters only; raw data is processed one shard at a time.
    for raw_path in raw_paths:
        prefix = raw_path.with_suffix("").with_suffix("")
        shard_id = int(prefix.name)
        summary = expected_hashes[shard_id]
        for suffix, key in ((".raw.jsonl", "raw_sha256"), (".npz", "npz_sha256"), (".samples.jsonl", "samples_sha256")):
            if file_sha(prefix.with_suffix(suffix)) != summary[key]:
                raise ValueError("shard hash mismatch")
        with np.load(prefix.with_suffix(".npz"), allow_pickle=False) as packed:
            with prefix.with_suffix(".samples.jsonl").open(encoding="utf-8") as stream:
                metadata = iter(json.loads(line) for line in stream)
                sample_index = 0
                with raw_path.open(encoding="utf-8") as raw:
                    for line in raw:
                        record = json.loads(line)
                        rid, family, group = record["record_id"], record["family"], record["group_id"]
                        if rid in seen_records:
                            raise ValueError("duplicate raw record id")
                        seen_records.add(rid)
                        split = split_for_group(group, split_seed)
                        if group in groups and groups[group] != split:
                            raise ValueError("group leaks across splits")
                        if record["scene_key"] in boards and boards[record["scene_key"]] != group:
                            raise ValueError("identical board has multiple split groups")
                        groups[group] = split
                        boards[record["scene_key"]] = group
                        counts["records"] += 1
                        counts[record["status"]] += 1
                        counts["illegal"] += bool(record.get("rule_violations"))
                        by_family[family]["records"] += 1
                        family_boards[family].add(record["scene_key"])
                        family_groups[family].add(group)
                        selection = record.get("selected_task") or record.get("requested_scene", {}).get("selection")
                        if selection is not None:
                            key = rid.rsplit(":", 1)[0]
                            candidate = candidates[key]
                            seed = record["physics_seed"]
                            if seed in candidate["seeds"]:
                                raise ValueError("duplicate physics seed in candidate")
                            candidate["seeds"].add(seed)
                            candidate.update(family=family, group=group)
                            candidate["attempts"] += 1
                            success = failure_reason(record, selection) is None
                            candidate["successes"] += success
                            by_family[family]["task_successful_records"] += success
                            if success:
                                family_successful[family].add(record["scene_key"])
                            if record.get("selected_task") and not success:
                                raise ValueError("selected raw record violates requested task")
                        for view_index, view in enumerate(achieved_views(record, max_views)):
                            item = next(metadata)
                            if any(item[k] != view[k] for k in ("view", "goal", "tactic")):
                                raise ValueError("encoded metadata does not match raw task view")
                            if (item["record_id"] != rid or item["sample_id"] != rid + ":" + str(view_index)
                                    or item["group_id"] != group or item["split"] != split):
                                raise ValueError("sample metadata provenance or split mismatch")
                            inputs = encode_input(record["before"], view["goal"], record["active_index"], view["tactic"])
                            expected = {**inputs, "actions": encode_action(record["shot"]), "shots": np.asarray(record["shot"], dtype=np.float32)}
                            for name, value in expected.items():
                                if packed[name][sample_index].tobytes() != value.tobytes():
                                    raise ValueError("encoded numeric bytes differ: " + name)
                            if (packed["record_id"][sample_index] != rid or packed["sample_id"][sample_index] != rid + ":" + str(view_index)
                                    or packed["group_id"][sample_index] != group or int(packed["split"][sample_index]) != split):
                                raise ValueError("encoded provenance or split mismatch")
                            counts["samples"] += 1
                            by_tactic[view["tactic"]] += 1
                            splits[str(split)] += 1
                            sample_index += 1
                if next(metadata, None) is not None or any(len(packed[k]) != sample_index for k in packed.files):
                    raise ValueError("array/metadata row count mismatch")
    for candidate in candidates.values():
        family = candidate["family"]
        by_family[family]["candidate_parameters"] += 1
        by_family[family]["all_observed_seeds_successful_candidates"] += candidate["attempts"] == candidate["successes"]
        by_family[family]["three_or_more_seeds_all_successful_candidates"] += candidate["attempts"] >= 3 and candidate["attempts"] == candidate["successes"]
    for family in by_family:
        by_family[family].update(unique_boards=len(family_boards[family]), neighbourhood_groups=len(family_groups[family]),
                                 boards_with_task_success=len(family_successful[family]))
    return {"status": "passed", "counts": dict(counts), "by_family": {k: dict(v) for k, v in by_family.items()},
            "samples_by_tactic": dict(by_tactic), "samples_by_split": dict(splits),
            "groups_by_split": dict(Counter(str(v) for v in groups.values())),
            "unique_boards": len(boards), "numeric_arrays_rebuilt_byte_equal": True,
            "raw_and_array_hashes_verified": True, "group_leakage": False,
            "families_without_task_success": [k for k in by_family if not by_family[k]["task_successful_records"]]}
