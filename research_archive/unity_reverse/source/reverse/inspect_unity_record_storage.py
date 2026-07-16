#!/usr/bin/env python3
"""Inspect where Unity WebGL record files would be stored.

The curling build is WebGL/IL2CPP.  Unity code refers to logical paths such as
``Records/4Games`` while the browser persists ``Application.persistentDataPath``
through Emscripten IDBFS under the browser profile's IndexedDB directory.

This script is intentionally read-only.  It scans the Unity build, native-looking
project directories, and common Chromium profile IndexedDB origins for record
fields such as BESTSHOT/RANDSEED/TRACE.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BUILD_RELATIVE_FILES = (
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "web" / "Build" / "build.data.gz",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "web" / "Build" / "build.wasm.gz",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "web" / "Build" / "build.framework.js.gz",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "web" / "Build" / "build.loader.js",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "web" / "index.html",
)

NATIVE_RELATIVE_DIRS = (
    Path("Records"),
    Path("Records") / "4Games",
    Path("Records") / "8Games",
    Path("AutoGame"),
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "Records",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "Records" / "4Games",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "Records" / "8Games",
    Path("数字冰壶单机版_win") / "数字冰壶单机版" / "AutoGame",
)

BUILD_PATTERNS = (
    b"Records",
    b"4Games/",
    b"8Games/",
    b"AutoGame",
    b"rank.csv",
    b"autoGame.save",
    b"Record Files(*.save)",
    b"*.save",
    b"BESTSHOT",
    b"RANDSEED",
    b"TRACE",
    b"SWEEP",
    b"POSITION",
    b"LASTSTATE",
    b"persistentDataPath",
    b"Application.persistentDataPath",
    b"IDBFS",
    b"/idbfs",
    b"FS.syncfs",
    b"autoSyncPersistentDataPath",
)

RUNTIME_PATTERNS = (
    b"Records",
    b"4Games",
    b"8Games",
    b"AutoGame",
    b"rank.csv",
    b"autoGame.save",
    b".save",
    b"BESTSHOT",
    b"RANDSEED",
    b"TRACE",
    b"SWEEP",
    b"POSITION",
    b"SETSTATE",
    b"LASTSTATE",
    b"/idbfs",
    b"PlayerPrefs",
)


@dataclass(frozen=True)
class Hit:
    path: str
    pattern: str
    count: int
    offsets: list[int]
    context: str


@dataclass(frozen=True)
class FileInfo:
    path: str
    size: int
    mtime: float


@dataclass(frozen=True)
class NativeDirInfo:
    path: str
    exists: bool
    files: list[FileInfo]


def _read_maybe_gzip(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.suffix == ".gz":
        return gzip.decompress(raw)
    return raw


def _printable(raw: bytes) -> str:
    return "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in raw)


def _scan_blob(path: Path, data: bytes, patterns: tuple[bytes, ...], max_offsets: int) -> list[Hit]:
    hits: list[Hit] = []
    for pattern in patterns:
        offsets: list[int] = []
        start = 0
        while True:
            idx = data.find(pattern, start)
            if idx < 0:
                break
            offsets.append(idx)
            start = idx + 1
            if len(offsets) >= max_offsets:
                break
        if not offsets:
            continue
        first = offsets[0]
        lo = max(0, first - 120)
        hi = min(len(data), first + len(pattern) + 180)
        hits.append(
            Hit(
                path=str(path),
                pattern=pattern.decode("utf-8", errors="replace"),
                count=len(offsets),
                offsets=offsets,
                context=_printable(data[lo:hi]),
            )
        )
    return hits


def scan_build(root: Path, max_offsets: int) -> list[Hit]:
    hits: list[Hit] = []
    for relative in BUILD_RELATIVE_FILES:
        path = root / relative
        if not path.exists():
            continue
        hits.extend(_scan_blob(path, _read_maybe_gzip(path), BUILD_PATTERNS, max_offsets))
    return hits


def scan_native_dirs(root: Path) -> list[NativeDirInfo]:
    results: list[NativeDirInfo] = []
    for relative in NATIVE_RELATIVE_DIRS:
        path = root / relative
        files: list[FileInfo] = []
        if path.exists():
            paths = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()]
            for item in sorted(paths):
                try:
                    stat = item.stat()
                except OSError:
                    continue
                files.append(FileInfo(str(item), stat.st_size, stat.st_mtime))
        results.append(NativeDirInfo(str(path), path.exists(), files))
    return results


def default_browser_indexeddb_roots() -> list[Path]:
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    candidates = [
        local / "Microsoft" / "Edge" / "User Data" / "Default" / "IndexedDB",
        local / "Google" / "Chrome" / "User Data" / "Default" / "IndexedDB",
    ]
    return [path for path in candidates if path.exists()]


def iter_origin_dirs(indexeddb_roots: list[Path]) -> list[Path]:
    origins: list[Path] = []
    for indexeddb_root in indexeddb_roots:
        if not indexeddb_root.exists():
            continue
        for item in indexeddb_root.iterdir():
            if item.is_dir() and item.name.endswith(".indexeddb.leveldb"):
                origins.append(item)
    return sorted(origins)


def scan_browser_origins(indexeddb_roots: list[Path], origin_filter: str, max_offsets: int) -> list[Hit]:
    hits: list[Hit] = []
    for origin in iter_origin_dirs(indexeddb_roots):
        if origin_filter and origin_filter not in origin.name:
            continue
        for item in origin.rglob("*"):
            if not item.is_file():
                continue
            try:
                data = item.read_bytes()
            except OSError:
                continue
            hits.extend(_scan_blob(item, data, RUNTIME_PATTERNS, max_offsets))
    return hits


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--indexeddb-root", action="append", type=Path, default=None)
    parser.add_argument("--origin-filter", default="9007")
    parser.add_argument("--max-offsets", type=int, default=6)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    indexeddb_roots = args.indexeddb_root or default_browser_indexeddb_roots()
    report = {
        "root": str(root),
        "build_hits": [asdict(hit) for hit in scan_build(root, args.max_offsets)],
        "native_dirs": [asdict(info) for info in scan_native_dirs(root)],
        "indexeddb_roots": [str(path) for path in indexeddb_roots],
        "browser_hits": [
            asdict(hit) for hit in scan_browser_origins(indexeddb_roots, args.origin_filter, args.max_offsets)
        ],
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    print(f"root: {report['root']}")
    print("\n== Unity build hits ==")
    for hit in report["build_hits"]:
        print(f"{hit['pattern']}: {hit['path']} offsets={hit['offsets']}")
        print(f"  {hit['context']}")

    print("\n== Native-looking record dirs ==")
    for info in report["native_dirs"]:
        print(f"{info['path']} exists={info['exists']} files={len(info['files'])}")
        for file_info in info["files"][:20]:
            print(f"  {file_info['path']} size={file_info['size']}")

    print("\n== Browser IndexedDB hits ==")
    print("indexeddb roots:")
    for path in report["indexeddb_roots"]:
        print(f"  {path}")
    for hit in report["browser_hits"]:
        print(f"{hit['pattern']}: {hit['path']} offsets={hit['offsets']}")
        print(f"  {hit['context']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
