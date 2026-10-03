"""Fresh curled glancing shot: actual Unity RNG, no trajectory state injection."""
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]


def main():
    old=ROOT/'research_archive/unity_reverse/evidence/data/calibration/c131_strict_yaw_r00_20260714/collision_unique_targets_batch_r00.jsonl'
    sample=next(json.loads(l) for l in old.open(encoding='utf8') if json.loads(l)['sample_id']==11009)
    r=sample['requested']
    plan=[dict(sample_id=11009,label='fresh_11009_curl_right_20261002',category=sample['category'],
        v0=r['v0'],h0=r['h0'],w0=r['w0'],sweep=0.,active_index=0,stones=r['stones'],
        notes='Fresh Unity page; same shot parameters as historical11009; no previous shots, pose injection or RNG override.')]
    plan_path=ROOT/'analysis_input/new_sample_11009_plan_20261002.json'
    plan_path.write_text(json.dumps(plan,indent=2))
    original=ROOT/'analysis_input/unity_release_both_complete_activation_v2_20261002/capture_manifest.json'
    manifest=json.loads(original.read_text())
    manifest['releaseTailTraceSolverLimit']=5
    manifest['velocityGetterMaxOrdinal']=4000
    manifest['tailCoreWindow']=dict(minOrdinal=1,maxOrdinal=4000,allStoneCores=True,maxSolverSteps=3000)
    m=ROOT/'analysis_input/unity_new_sample_11009_manifest_20261002.json'
    m.write_text(json.dumps(manifest,indent=2))
    out=ROOT/'analysis_input/unity_new_sample_11009_capture_20261002'
    subprocess.run([sys.executable,str(ROOT/'analysis_input/capture_12011_first_solver.py'),
        '--plan',str(plan_path),'--natural-friction','--dense-release-serial','2','--output',str(out),
        '--expected-release-count','1','--expected-friction-count','0','--expected-dense-count','1',
        '--expected-c03-count','0','--expected-reset-core-count','256','--expected-tail-boundary-steps','3000',
        '--reset-settle-seconds','2','--phase-ordinal-min','1','--phase-ordinal-max','4',
        '--static-phase-trace','--export-wait-seconds','180','--pcm-call-trace-manifest',str(m)],cwd=ROOT,check=True)
    (out/'capture_manifest.json').write_text(json.dumps(manifest,indent=2))
    (out/'observer_source.js').write_bytes((ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js').read_bytes())


if __name__=='__main__':main()
