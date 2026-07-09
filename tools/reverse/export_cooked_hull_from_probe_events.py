#!/usr/bin/env python3
"""Export PhysX cooked hull desc events captured by unity_webgl_runtime_probe.js."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_ROOT = PROJECT_ROOT / "log"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "calibration" / "unity_cooked_hulls_latest.json"
COOKED_LOG_RE = re.compile(r"cooked hull desc vertices=(\d+) polygons=(\d+) indices=(\d+)")
SOURCE_MESH_RE = re.compile(r'source mesh "([^"]+)"')


def _latest_events(log_root: Path) -> Path:
    files = sorted(log_root.glob("unity_runtime_probe_*/events.latest.json"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"no events.latest.json under {log_root}")
    return files[-1]


def _bounds(vertices: list[list[float]]) -> dict[str, list[float]]:
    mins = [min(vertex[i] for vertex in vertices) for i in range(3)]
    maxs = [max(vertex[i] for vertex in vertices) for i in range(3)]
    extents = [maxs[i] - mins[i] for i in range(3)]
    center = [(mins[i] + maxs[i]) * 0.5 for i in range(3)]
    centroid = [sum(vertex[i] for vertex in vertices) / len(vertices) for i in range(3)]
    return {
        "min": mins,
        "max": maxs,
        "extents": extents,
        "center": center,
        "centroid": centroid,
    }


def _hull_hash(hull: dict[str, Any]) -> str:
    canonical = json.dumps(
        {
            "vertices": hull.get("vertices", []),
            "polygons": hull.get("polygons", []),
            "indices": hull.get("indices", []),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _infer_console_names(console_path: Path | None) -> list[dict[str, Any]]:
    if not console_path or not console_path.exists():
        return []

    cooked: list[dict[str, Any]] = []
    lines = console_path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line_index, line in enumerate(lines):
        match = COOKED_LOG_RE.search(line)
        if not match:
            continue
        item: dict[str, Any] = {
            "console_line": line_index + 1,
            "vertices": int(match.group(1)),
            "polygons": int(match.group(2)),
            "indices": int(match.group(3)),
        }
        for next_line in lines[line_index + 1 : line_index + 4]:
            source_match = SOURCE_MESH_RE.search(next_line)
            if source_match:
                item["unity_source_mesh"] = source_match.group(1)
                item["unity_warning"] = next_line
                break
            if COOKED_LOG_RE.search(next_line):
                break
        cooked.append(item)
    return cooked


def export_hulls(input_path: Path, console_path: Path | None = None) -> dict[str, Any]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    console_hints = _infer_console_names(console_path)
    all_hulls: list[dict[str, Any]] = []
    unique: OrderedDict[str, dict[str, Any]] = OrderedDict()
    hull_ordinal = 0

    for event_index, event in enumerate(data.get("events", [])):
        if event.get("type") != "physx.cooked_hull.desc":
            continue
        payload = event.get("data", {})
        if not payload.get("ok"):
            continue
        vertices = payload.get("vertices") or []
        polygons = payload.get("polygons") or []
        indices = payload.get("indices") or []
        if not vertices:
            continue

        hull = {
            "hull_ordinal": hull_ordinal,
            "event_index": event_index,
            "event_time_ms": event.get("t"),
            "header": payload.get("header"),
            "counts": {
                "vertices": len(vertices),
                "polygons": len(polygons),
                "indices": len(indices),
            },
            "bounds": _bounds(vertices),
            "vertices": vertices,
            "polygons": polygons,
            "indices": indices,
            "raw": payload.get("raw"),
        }
        digest = _hull_hash(hull)
        hull["sha256"] = digest
        hull["sha256_16"] = digest[:16]
        if hull_ordinal < len(console_hints):
            hint = console_hints[hull_ordinal]
            hull["console_hint"] = hint
            if (
                hint.get("vertices") != len(vertices)
                or hint.get("polygons") != len(polygons)
                or hint.get("indices") != len(indices)
            ):
                hull["console_hint_mismatch"] = True
        all_hulls.append(hull)

        if digest not in unique:
            unique[digest] = {
                "sha256": digest,
                "sha256_16": digest[:16],
                "first_event_index": event_index,
                "event_indices": [event_index],
                "duplicate_count": 1,
                "counts": hull["counts"],
                "bounds": hull["bounds"],
                "unity_source_meshes": [],
                "hull": hull,
            }
        else:
            unique[digest]["event_indices"].append(event_index)
            unique[digest]["duplicate_count"] += 1
        source_mesh = hull.get("console_hint", {}).get("unity_source_mesh")
        if source_mesh and source_mesh not in unique[digest]["unity_source_meshes"]:
            unique[digest]["unity_source_meshes"].append(source_mesh)
        hull_ordinal += 1

    summary = []
    for item in unique.values():
        bounds = item["bounds"]
        counts = item["counts"]
        summary.append(
            {
                "sha256_16": item["sha256_16"],
                "first_event_index": item["first_event_index"],
                "duplicate_count": item["duplicate_count"],
                "vertices": counts["vertices"],
                "polygons": counts["polygons"],
                "indices": counts["indices"],
                "unity_source_meshes": item["unity_source_meshes"],
                "extents": bounds["extents"],
                "min": bounds["min"],
                "max": bounds["max"],
                "centroid": bounds["centroid"],
            }
        )

    return {
        "source": str(input_path),
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "event_count": data.get("eventCount"),
        "hook_summary": data.get("hookSummary"),
        "console_path": str(console_path) if console_path else None,
        "console_hints": console_hints,
        "hull_count": len(all_hulls),
        "unique_hull_count": len(unique),
        "summary": summary,
        "unique_hulls": list(unique.values()),
        "all_hulls": all_hulls,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="events.latest.json/events.final.json")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--console-log", type=Path)
    parser.add_argument("--log-root", type=Path, default=DEFAULT_LOG_ROOT)
    args = parser.parse_args()

    input_path = args.input or _latest_events(args.log_root)
    console_path = args.console_log
    if console_path is None:
        candidate = input_path.parent / "console.log"
        console_path = candidate if candidate.exists() else None
    output = export_hulls(input_path, console_path=console_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"input: {input_path}")
    print(f"output: {args.output}")
    print(f"hulls: {output['hull_count']} total, {output['unique_hull_count']} unique")
    for item in output["summary"]:
        ext = item["extents"]
        print(
            f"event={item['first_event_index']:3d} dup={item['duplicate_count']:2d} "
            f"hash={item['sha256_16']} v={item['vertices']:3d} "
            f"p={item['polygons']:3d} i={item['indices']:3d} "
            f"ext=({ext[0]:.6f},{ext[1]:.6f},{ext[2]:.6f}) "
            f"source={','.join(item['unity_source_meshes']) or '-'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
