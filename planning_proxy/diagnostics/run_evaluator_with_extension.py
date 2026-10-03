"""Run the full local evaluator with a temporary CP39 native extension.

The bundled runtime file is never copied, replaced, or edited.  The extension
override exists only in this Python process, then the normal evaluator is run
with its ordinary command-line arguments.

Example (PowerShell):
    & $cp39 diagnostics/run_evaluator_with_extension.py `
      --extension D:\path\_pyphysx.cp39-win_amd64.pyd -- `
      --opponent ppo --proxy-team 0 --seed 123 --output runs\trial.json
"""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVALUATOR = ROOT / "planning_proxy" / "evaluate_vs_teammate_ppo.py"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="只在当前子进程临时加载指定 CP39 pyd，再执行完整本地对局评测。"
    )
    parser.add_argument("--extension", required=True, help="指定 CP39 Windows pyd 的绝对或相对路径")
    parser.add_argument("evaluator_args", nargs=argparse.REMAINDER, help="`--` 之后原样传给 evaluate_vs_teammate_ppo.py")
    args = parser.parse_args()
    extension = Path(args.extension).expanduser().resolve()
    if not extension.is_file():
        raise FileNotFoundError(f"找不到临时扩展：{extension}")
    if not extension.name.endswith(".cp39-win_amd64.pyd"):
        raise ValueError(f"本包装器只能运行 Windows CP39 pyd：{extension.name}")
    forwarded = list(args.evaluator_args)
    if forwarded[:1] == ["--"]:
        forwarded = forwarded[1:]

    # Must happen before runpy executes evaluator imports that load pyphysx.
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from local_simulator import runtime_loader

    # Candidate build directories usually hold only the binary.  Keep the
    # bundled runtime directory on sys.path for its companion pure-Python
    # modules (notably quaternion.py); the native binary itself is still
    # loaded only from ``extension`` below.
    bundled = runtime_loader.WINDOWS_BUNDLED_EXTENSIONS[(3, 9)]
    if str(bundled.parent) not in sys.path:
        sys.path.insert(0, str(bundled.parent))
    runtime_loader.BUNDLED_EXTENSION = extension
    print(f"TEMP_EXTENSION_ONLY {extension}", flush=True)
    sys.argv = [str(EVALUATOR), *forwarded]
    runpy.run_path(str(EVALUATOR), run_name="__main__")


if __name__ == "__main__":
    main()
