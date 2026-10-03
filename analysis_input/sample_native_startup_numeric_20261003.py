"""Read-only constructor capture and an uninstrumented startup repeat."""
import argparse,ctypes,hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx,_resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
def main():
    p=argparse.ArgumentParser();p.add_argument('--native-trace-control',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    opts=p.parse_args();control=opts.native_trace_control
    def wait(name):
        deadline=time.monotonic()+90
        while not (control/name).exists():
            if time.monotonic()>deadline:raise TimeoutError(name)
            time.sleep(.05)
    (control/'arm.json').write_text(json.dumps(dict(pid=os.getpid(),threadId=ctypes.windll.kernel32.GetCurrentThreadId(),module=str(_resolve_bundled_extension()))))
    wait('go')
    scene=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
    observed=[scene.raw_native_state(i) for i in range(16)]
    (control/'done').write_text('done');wait('resume')
    plain=PersistentPhysxFrontHalfScene(stone_count=16,ice_mesh_mode='unity-source-once')
    baseline=[plain.raw_native_state(i) for i in range(16)]
    assert observed==baseline,'Constructor observation changed exposed startup state'
    result=dict(observerStartupStatesUnchanged=True,observedStates=observed,
        moduleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest(),
        productionSourceSha256=hashlib.sha256((ROOT/'local_simulator/unity_physx.py').read_bytes()).hexdigest())
    opts.output.write_text(json.dumps(result,indent=2),encoding='utf8')
    print('16 startup states equal with and without constructor hooks')
if __name__=='__main__':main()
