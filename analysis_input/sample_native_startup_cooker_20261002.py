"""Pause around the first actual production stone construction for native reads."""
import ctypes
import json
from pathlib import Path
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx, _resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from tools.reverse import probe_physx_collision_alignment as probe


def main():
    directory=Path(sys.argv[1])
    original=probe._make_stone
    armed=False
    def wait(name):
        deadline=time.monotonic()+90
        while not (directory/name).exists():
            if time.monotonic()>deadline: raise TimeoutError(name)
            time.sleep(.02)
    def observed(*args,**kwargs):
        nonlocal armed
        if armed:return original(*args,**kwargs)
        armed=True
        (directory/'arm.json').write_text(json.dumps(dict(pid=os.getpid(),threadId=ctypes.windll.kernel32.GetCurrentThreadId(),
            module=str(_resolve_bundled_extension()))))
        wait('go')
        result=original(*args,**kwargs)
        (directory/'done').write_text('done')
        wait('resume')
        return result
    probe._make_stone=observed
    try:scene=PersistentPhysxFrontHalfScene(stone_count=16)
    finally:probe._make_stone=original
    (directory/'output.json').write_text(json.dumps(scene.slots[0].shape.get_convex_mesh_runtime_hull_data()))


if __name__=='__main__':main()
