"""Run the existing audit; bracket its second isolated geometric PCM query."""
import ctypes
import json
import os
from pathlib import Path
import runpy
import sys
import time

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from local_simulator.runtime_loader import install_bundled_pyphysx
install_bundled_pyphysx()
import pyphysx._pyphysx as native
import pyphysx

control = Path(sys.argv[1])
original = native.generate_contacts_between
count = 0


def await_file(name):
    deadline = time.monotonic() + 90
    while not (control / name).exists():
        if time.monotonic() > deadline:
            raise TimeoutError(name)
        time.sleep(0.05)


def traced_query(*args, **kwargs):
    global count
    count += 1
    if count != 2:
        return original(*args, **kwargs)
    request = {"pid": os.getpid(), "threadId": ctypes.windll.kernel32.GetCurrentThreadId(),
               "queryOrdinal": 487, "module": str(Path(native.__file__).resolve())}
    (control / "arm.json").write_text(json.dumps(request), encoding="utf-8")
    await_file("go")
    try:
        result = original(*args, **kwargs)
    finally:
        (control / "done").write_text("done", encoding="utf-8")
        await_file("resume")
    return result


native.generate_contacts_between = traced_query
pyphysx.generate_contacts_between = traced_query
sys.argv = [str(root / "analysis_input/audit_c131_alignment_20260930.py")] + sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
