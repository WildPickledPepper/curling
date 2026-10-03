"""Observe actual integrateCore inputs and sin/cos calls at ordinal 314."""
import json
from pathlib import Path
import subprocess
import sys

from instrument_pcm_calls import instrument

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
OUT=BASE/'additional_case_validation_20261002'


def main():
    old=json.loads((OUT/'full_trajectory_manifest.json').read_text())
    functions=[r['functionIndex'] for r in old['functions']]+[71198,18890,33062]
    patched,meta=instrument(Path(old['source']).read_bytes(),functions)
    wasm=BASE/'unity_case12009_integrate_20261003.wasm'
    assert not wasm.exists()
    wasm.write_bytes(patched)
    manifest={**old,**meta,'patched':str(wasm),'releaseTailTraceSolverLimit':4000,
        'upstreamRootFunctions':old['upstreamRootFunctions']+[71198],
        'wakeFunctionTrace':[71198,18890,33062],
        'wakeFunctionWindow':dict(minOrdinal=314,maxOrdinal=314,maxSolverSerial=4000)}
    path=BASE/'unity_case12009_integrate_20261003.json'
    path.write_text(json.dumps(manifest,indent=2),encoding='utf8')
    dest=BASE/'case12009_step313_unity_integrate_20261003'
    subprocess.run([sys.executable,str(BASE/'capture_12011_first_solver.py'),
        '--plan',str(OUT/'additional12009_plan.json'),
        '--events',str(OUT/'additional12009_friction.jsonl'),
        '--dense-release-serial','2','--dense-write-limit','5000','--output',str(dest),
        '--expected-release-count','1','--expected-friction-count','1275',
        '--expected-dense-count','1276','--expected-c03-count','0',
        '--expected-reset-core-count','256','--expected-tail-boundary-steps','4000',
        '--reset-settle-seconds','2','--phase-ordinal-min','314','--phase-ordinal-max','314',
        '--static-phase-trace','--export-wait-seconds','180',
        '--pcm-call-trace-manifest',str(path)],cwd=ROOT,check=True)
    (dest/'capture_manifest.json').write_bytes(path.read_bytes())
    (dest/'observer_source.js').write_bytes((ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js').read_bytes())


if __name__=='__main__':main()
