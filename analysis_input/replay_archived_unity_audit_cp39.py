"""Run the archived endpoint audit against the current CP39 simulator.

The archived audit has a CP38-only loader and imports from the old project
layout. This adapter changes those imports in memory; its replay logic stays
unchanged. It never modifies the archived source or production simulator.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from local_simulator.runtime_loader import _resolve_bundled_extension, install_bundled_pyphysx


SOURCE = ROOT / "research_archive/unity_reverse/source/reverse/audit_hybrid_p6_endpoint_sixshot.py"
REPLACEMENT = """    from tools.reverse.front_half_pcm_replay import event_shot_groups, load_jsonl
    from local_simulator.unity_physx import NativePyphysxMotionStepper, PersistentPhysxFrontHalfScene
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("samples", "events", "orientation-manifest", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)

    extension = _resolve_bundled_extension()
    install_bundled_pyphysx()
    import local_simulator.unity_physx  # noqa: F401

    source = SOURCE.read_text(encoding="utf-8")
    start_marker = "    if sys.version_info[:2] != (3, 8)"
    end_marker = "    samples = _load_jsonl"
    if source.count(start_marker) != 1 or source.count(end_marker) != 1:
        raise RuntimeError("Archived audit changed; review the adapter")
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    source = source[:start] + REPLACEMENT + source[end:]

    sys.argv = [
        str(SOURCE),
        "--samples", str(args.samples.resolve()),
        "--events", str(args.events.resolve()),
        "--orientation-manifest", str(args.orientation_manifest.resolve()),
        "--require-orientation-truth",
        "--motion-kernel", "native-pyphysx",
        "--pyphysx-extension", str(extension),
        "--output", str(args.output.resolve()),
    ]
    namespace = {"__name__": "archived_alignment_audit", "__file__": str(SOURCE)}
    print("extension_sha256", hashlib.sha256(extension.read_bytes()).hexdigest(), flush=True)
    exec(compile(source, str(SOURCE), "exec"), namespace)
    namespace["main"]()


if __name__ == "__main__":
    main()
