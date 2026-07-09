#!/usr/bin/env python3
"""Build no-sweep collision plans that avoid hidden target-state carryover."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.calibration.build_controlled_sampling_plan import build_plan


DEFAULT_OUTPUT_DIR = Path("config/unity_fresh_collision_plans_20260708")
DEFAULT_MANIFEST = Path("config/unity_fresh_collision_manifest_20260708.json")
DEFAULT_BATCH_OUTPUT_DIR = Path("config/unity_unique_target_collision_batches_20260708")
DEFAULT_BATCH_MANIFEST = Path("config/unity_unique_target_collision_batch_manifest_20260708.json")
DEFAULT_ROLE_PROBE_OUTPUT_DIR = Path("config/unity_unique_role_collision_probe_20260708")
DEFAULT_ROLE_PROBE_MANIFEST = Path("config/unity_unique_role_collision_probe_manifest_20260708.json")
DEFAULT_CATEGORIES = ("collision_headon", "collision_glancing")
DEFAULT_TARGET_INDICES = tuple(range(2, 16))
DEFAULT_ROLE_PROBE_ACTIVE_INDICES = tuple(range(0, 8))
DEFAULT_ROLE_PROBE_TARGET_INDICES = tuple(range(8, 16))


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return cleaned.strip("_") or "case"


def select_collision_cases(
    plan: list[dict[str, Any]],
    categories: tuple[str, ...] = DEFAULT_CATEGORIES,
) -> list[dict[str, Any]]:
    wanted = set(categories)
    return [
        row
        for row in plan
        if row.get("category") in wanted
        and float(row.get("sweep", 0.0)) == 0.0
        and row.get("stones")
    ]


def build_fresh_plan_files(
    *,
    output_dir: Path,
    manifest_path: Path,
    repeats: int,
    categories: tuple[str, ...] = DEFAULT_CATEGORIES,
    start_sample_id: int = 10000,
) -> list[dict[str, Any]]:
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    cases = select_collision_cases(build_plan(), categories=categories)
    if not cases:
        raise ValueError("no collision cases selected")

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    next_sample_id = start_sample_id
    for case_index, source in enumerate(cases):
        for repeat_index in range(repeats):
            row = dict(source)
            row["source_sample_id"] = int(source["sample_id"])
            row["fresh_repeat_index"] = repeat_index
            row["sample_id"] = next_sample_id
            row["label"] = f"{source['label']}_fresh_r{repeat_index:02d}"
            row["notes"] = (
                f"fresh-page collision calibration; source_sample_id={source['sample_id']}; "
                "reload Unity before running this one-shot plan"
            )
            filename = f"{case_index:03d}_{_slug(source['label'])}_r{repeat_index:02d}.json"
            plan_path = output_dir / filename
            plan_path.write_text(json.dumps([row], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            manifest.append(
                {
                    "plan_file": str(plan_path),
                    "sample_id": row["sample_id"],
                    "label": row["label"],
                    "category": row["category"],
                    "source_sample_id": row["source_sample_id"],
                    "repeat_index": repeat_index,
                    "requires_fresh_page": True,
                }
            )
            next_sample_id += 1
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def _with_explicit_target_index(source: dict[str, Any], target_index: int) -> dict[str, Any]:
    stones = source.get("stones") or []
    if len(stones) != 1:
        raise ValueError(f"{source.get('label')}: unique-target batches require exactly one target stone")
    row = dict(source)
    stone = dict(stones[0])
    stone["index"] = target_index
    row["stones"] = [stone]
    return row


def build_unique_target_batch_files(
    *,
    output_dir: Path,
    manifest_path: Path,
    repeats: int,
    categories: tuple[str, ...] = DEFAULT_CATEGORIES,
    start_sample_id: int = 11000,
    target_indices: tuple[int, ...] = DEFAULT_TARGET_INDICES,
) -> list[dict[str, Any]]:
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    cases = select_collision_cases(build_plan(), categories=categories)
    if not cases:
        raise ValueError("no collision cases selected")
    if len(cases) > len(target_indices):
        raise ValueError(
            f"{len(cases)} selected cases need {len(cases)} unique target indices, "
            f"but only {len(target_indices)} were provided"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    next_sample_id = start_sample_id
    for repeat_index in range(repeats):
        rows: list[dict[str, Any]] = []
        case_entries: list[dict[str, Any]] = []
        for case_index, (source, target_index) in enumerate(zip(cases, target_indices)):
            row = _with_explicit_target_index(source, int(target_index))
            row["source_sample_id"] = int(source["sample_id"])
            row["batch_repeat_index"] = repeat_index
            row["batch_case_index"] = case_index
            row["assigned_target_index"] = int(target_index)
            row["sample_id"] = next_sample_id
            row["label"] = f"{source['label']}_unique_t{target_index:02d}_r{repeat_index:02d}"
            row["notes"] = (
                f"unique-target collision calibration; source_sample_id={source['sample_id']}; "
                f"target_index={target_index}; reload Unity before each batch file"
            )
            rows.append(row)
            case_entries.append(
                {
                    "sample_id": row["sample_id"],
                    "label": row["label"],
                    "category": row["category"],
                    "source_sample_id": row["source_sample_id"],
                    "target_index": target_index,
                    "case_index": case_index,
                }
            )
            next_sample_id += 1

        plan_path = output_dir / f"collision_unique_targets_batch_r{repeat_index:02d}.json"
        plan_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest.append(
            {
                "plan_file": str(plan_path),
                "repeat_index": repeat_index,
                "case_count": len(rows),
                "requires_fresh_page_before_batch": True,
                "requires_unique_target_indices": True,
                "target_indices": [entry["target_index"] for entry in case_entries],
                "cases": case_entries,
            }
        )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def build_unique_active_target_probe_files(
    *,
    output_dir: Path,
    manifest_path: Path,
    repeats: int,
    categories: tuple[str, ...] = DEFAULT_CATEGORIES,
    start_sample_id: int = 12000,
    active_indices: tuple[int, ...] = DEFAULT_ROLE_PROBE_ACTIVE_INDICES,
    target_indices: tuple[int, ...] = DEFAULT_ROLE_PROBE_TARGET_INDICES,
) -> list[dict[str, Any]]:
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    if len(active_indices) != len(target_indices):
        raise ValueError("active_indices and target_indices must have the same length")
    if set(active_indices) & set(target_indices):
        raise ValueError("active and target indices must be disjoint")
    cases = select_collision_cases(build_plan(), categories=categories)[: len(active_indices)]
    if len(cases) < len(active_indices):
        raise ValueError(f"need {len(active_indices)} collision cases, got {len(cases)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    next_sample_id = start_sample_id
    for repeat_index in range(repeats):
        rows: list[dict[str, Any]] = []
        case_entries: list[dict[str, Any]] = []
        for case_index, (source, active_index, target_index) in enumerate(
            zip(cases, active_indices, target_indices)
        ):
            row = _with_explicit_target_index(source, int(target_index))
            row["source_sample_id"] = int(source["sample_id"])
            row["role_probe_repeat_index"] = repeat_index
            row["role_probe_case_index"] = case_index
            row["assigned_active_index"] = int(active_index)
            row["assigned_target_index"] = int(target_index)
            row["active_index"] = int(active_index)
            row["sample_id"] = next_sample_id
            row["label"] = (
                f"{source['label']}_active_a{active_index:02d}_target_t{target_index:02d}_r{repeat_index:02d}"
            )
            row["notes"] = (
                f"unique-active-target collision probe; source_sample_id={source['sample_id']}; "
                f"active_index={active_index}; target_index={target_index}; "
                "requires controlled_scene_sampler --use-plan-active-index"
            )
            rows.append(row)
            case_entries.append(
                {
                    "sample_id": row["sample_id"],
                    "label": row["label"],
                    "category": row["category"],
                    "source_sample_id": row["source_sample_id"],
                    "active_index": active_index,
                    "target_index": target_index,
                    "case_index": case_index,
                }
            )
            next_sample_id += 1

        plan_path = output_dir / f"collision_unique_roles_probe_r{repeat_index:02d}.json"
        plan_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest.append(
            {
                "plan_file": str(plan_path),
                "repeat_index": repeat_index,
                "case_count": len(rows),
                "requires_fresh_page_before_batch": True,
                "requires_use_plan_active_index": True,
                "requires_unique_active_indices": True,
                "requires_unique_target_indices": True,
                "active_indices": [entry["active_index"] for entry in case_entries],
                "target_indices": [entry["target_index"] for entry in case_entries],
                "cases": case_entries,
            }
        )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--batch-output-dir", type=Path, default=DEFAULT_BATCH_OUTPUT_DIR)
    parser.add_argument("--batch-manifest", type=Path, default=DEFAULT_BATCH_MANIFEST)
    parser.add_argument("--role-probe-output-dir", type=Path, default=DEFAULT_ROLE_PROBE_OUTPUT_DIR)
    parser.add_argument("--role-probe-manifest", type=Path, default=DEFAULT_ROLE_PROBE_MANIFEST)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--mode",
        choices=("fresh-one-shot", "unique-target-batch", "unique-active-target-probe", "both"),
        default="fresh-one-shot",
        help="fresh-one-shot writes one case per file; unique-target-batch writes one page-safe batch per repeat.",
    )
    parser.add_argument(
        "--categories",
        default=",".join(DEFAULT_CATEGORIES),
        help="Comma-separated plan categories. Defaults to no-sweep head-on and glancing cases.",
    )
    parser.add_argument("--start-sample-id", type=int, default=10000)
    parser.add_argument("--batch-start-sample-id", type=int, default=11000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    categories = tuple(part.strip() for part in args.categories.split(",") if part.strip())
    if args.mode in {"fresh-one-shot", "both"}:
        manifest = build_fresh_plan_files(
            output_dir=args.output_dir,
            manifest_path=args.manifest,
            repeats=args.repeats,
            categories=categories,
            start_sample_id=args.start_sample_id,
        )
        print(f"wrote {len(manifest)} fresh collision one-shot plans -> {args.output_dir}")
        print(f"manifest -> {args.manifest}")
    if args.mode in {"unique-target-batch", "both"}:
        batch_manifest = build_unique_target_batch_files(
            output_dir=args.batch_output_dir,
            manifest_path=args.batch_manifest,
            repeats=args.repeats,
            categories=categories,
            start_sample_id=args.batch_start_sample_id,
        )
        case_count = sum(int(row["case_count"]) for row in batch_manifest)
        print(f"wrote {len(batch_manifest)} unique-target batch plans ({case_count} cases) -> {args.batch_output_dir}")
        print(f"batch manifest -> {args.batch_manifest}")
    if args.mode in {"unique-active-target-probe", "both"}:
        role_manifest = build_unique_active_target_probe_files(
            output_dir=args.role_probe_output_dir,
            manifest_path=args.role_probe_manifest,
            repeats=args.repeats,
            categories=categories,
        )
        role_case_count = sum(int(row["case_count"]) for row in role_manifest)
        print(
            f"wrote {len(role_manifest)} unique-active-target probe plans "
            f"({role_case_count} cases) -> {args.role_probe_output_dir}"
        )
        print(f"role probe manifest -> {args.role_probe_manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
