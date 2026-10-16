"""Run one local-search arm in a fresh process/native scene for a paired probe."""
import argparse
import ctypes as C
import json
from pathlib import Path

from training_research.diagnose_inverse_misses import run_arm
from training_research.inverse_dataset.cli import file_sha, make_environment, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fine", action="store_true")
    args = parser.parse_args()
    assert not args.output.exists()
    old = json.loads(args.evidence.read_text(encoding="utf-8"))
    kernel = C.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentThread.restype = C.c_void_p
    kernel.SetThreadAffinityMask.argtypes = (C.c_void_p, C.c_size_t)
    kernel.SetThreadAffinityMask.restype = C.c_size_t
    thread = kernel.GetCurrentThread()
    previous = kernel.SetThreadAffinityMask(thread, 1 << 4)
    if not previous: raise C.WinError(C.get_last_error())
    try:
        env = make_environment()
        arm = run_arm(env, old["scene"], old["navigation_seed"], old["diagnostics"]["best_effort_shot"],
            "fresh_own_best_fine" if args.fine else "fresh_own_best_original", 3., 48, fine=args.fine)
    finally:
        kernel.SetThreadAffinityMask(thread, previous)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.output, {"scene_id": old["scene"]["scene_id"], "scene": old["scene"], "arm": arm,
        "original_evidence": str(args.evidence.resolve()), "original_evidence_sha256": file_sha(args.evidence),
        "source_sha256": {str(p.resolve()): file_sha(p) for p in (Path(__file__), Path("training_research/diagnose_inverse_misses.py"), Path("training_research/inverse_goal_search.py"))},
        "scope": "Fresh process and fresh native environment per arm, identical own-best start/nav seed, 3 seconds/48 calls; only starting/restart mesh differs. Compare actual first outputs before attributing outcome to mesh."})
    print(json.dumps({"scene_id": old["scene"]["scene_id"], "fine": args.fine, "success": arm["success"],
        "calls": len(arm["calls"]), "initial_loss": arm["calls"][0]["task_failure"], "best_loss": arm["diagnostics"]["best_loss"]}), flush=True)


if __name__ == "__main__": main()
