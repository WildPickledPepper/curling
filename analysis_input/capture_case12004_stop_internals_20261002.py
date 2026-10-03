"""Read-only focused observation at the first free-stop divergence."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
WORK=BASE/'multi_case_validation_20261002'


def main():
    manifest=json.loads((BASE/'unity_sample11009_step1383_capture_v2_20261002/capture_manifest.json').read_text())
    manifest['velocityGetterMaxOrdinal']=5000
    manifest['releaseTailTraceSolverLimit']=4
    manifest['wakeFunctionWindow']=dict(minOrdinal=3168,maxOrdinal=3170,maxSolverSerial=4)
    manifest['tailCoreWindow']=dict(minOrdinal=3168,maxOrdinal=5000,allStoneCores=True,
                                  maxSolverSteps=5,activationMinOrdinal=3168)
    path=WORK/'case12004_stop_internal_manifest.json'
    path.write_text(json.dumps(manifest,indent=2),encoding='utf8')
    dest=WORK/'case12004_stop_internal_unity'
    subprocess.run([sys.executable,str(BASE/'capture_12011_first_solver.py'),
        '--plan',str(WORK/'full12004_run1_plan.json'),
        '--events',str(WORK/'full12004_run1_friction.jsonl'),
        '--dense-release-serial','2','--dense-write-limit','5000','--output',str(dest),
        '--expected-release-count','1','--expected-friction-count','3168',
        '--expected-dense-count','3169','--expected-c03-count','0',
        '--expected-reset-core-count','256','--expected-tail-boundary-steps','5',
        '--reset-settle-seconds','2','--phase-ordinal-min','3168','--phase-ordinal-max','3170',
        '--static-phase-trace','--export-wait-seconds','180',
        '--pcm-call-trace-manifest',str(path)],cwd=ROOT,check=True)
    (dest/'capture_manifest.json').write_bytes(path.read_bytes())
    (dest/'observer_source.js').write_bytes((ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js').read_bytes())


if __name__=='__main__':main()
