"""Trace the actual upper-level caller of the step1879 actor removal."""
import json
from pathlib import Path
import subprocess
import sys
from instrument_pcm_calls import instrument

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
WORK=BASE/'additional_case_validation_20261002'

def main():
    old=json.loads((WORK/'full_trajectory_manifest.json').read_text())
    roots=[61029,61030]
    extra=roots+[54405]
    functions=[r['functionIndex'] for r in old['functions']]+extra
    patched,meta=instrument(Path(old['source']).read_bytes(),functions)
    wasm=BASE/'unity_case12000_cleanup_v4_20261003.wasm'
    assert not wasm.exists()
    wasm.write_bytes(patched)
    manifest={**old,**meta,'patched':str(wasm),'releaseTailTraceSolverLimit':1900,
        'tailCoreWindow':{**old['tailCoreWindow'],'maxSolverSteps':1900},
        'upstreamRootFunctions':old['upstreamRootFunctions']+roots,
        'wakeFunctionTrace':roots,'collisionTagConstantAudit':True,
        'wakeFunctionWindow':dict(minOrdinal=1879,maxOrdinal=1881,maxSolverSerial=1881)}
    path=BASE/'unity_case12000_cleanup_v4_20261003.json'
    path.write_text(json.dumps(manifest,indent=2))
    source=(ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js').read_text(encoding='utf8')
    marker='            if (upstreamRoots) row.releaseSerial = release && release.serial;'
    assert source.count(marker)==1
    observe='''            if (entry.functionIndex === 61030 && state.pcmCallTraceManifest.collisionTagConstantAudit) {
              row.collisionTagConstants = [3837100,3843892].map(function(address) {
                var ptr=view.getUint32(address,true), length=view.getInt32(ptr+8,true), text="";
                if (length < 0 || length > 64) throw new Error("invalid collision tag string length");
                for (var ci=0;ci<length;ci++) text += String.fromCharCode(view.getUint16(ptr+12+ci*2,true));
                return {globalAddress:address,stringPtr:ptr,length:length,text:text};
              });
            }
'''
    observer=BASE/'case12000_cleanup_observer_v3_20261003.js'
    observer.write_text(source.replace(marker,observe+marker),encoding='utf8')
    dest=BASE/'case12000_cleanup_unity_v4_20261003'
    subprocess.run([sys.executable,str(BASE/'capture_12000_cleanup_driver_v3_20261003.py'),
        '--plan',str(WORK/'additional12000_plan.json'),
        '--events',str(WORK/'additional12000_friction.jsonl'),
        '--dense-release-serial','2','--dense-write-limit','5000','--output',str(dest),
        '--expected-release-count','1','--expected-friction-count','1879',
        '--expected-dense-count','1881','--expected-c03-count','0',
        '--expected-reset-core-count','256','--expected-tail-boundary-steps','1900',
        '--reset-settle-seconds','2','--phase-ordinal-min','1879','--phase-ordinal-max','1880',
        '--static-phase-trace','--export-wait-seconds','600',
        '--pcm-call-trace-manifest',str(path)],cwd=ROOT,check=True)
    (dest/'capture_manifest.json').write_bytes(path.read_bytes())
    (dest/'observer_source.js').write_bytes(observer.read_bytes())

if __name__=='__main__':main()
