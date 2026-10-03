"""Fresh production replays against stored, independently observed Unity truth."""
import hashlib
import json
from pathlib import Path
import subprocess

import validate_multiple_cases_20261002 as validation
from validate_additional_cases_20261002 import compare_observed

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
OUT=BASE/'cos_repair_regression_20261003'
PY39=r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe'

def main():
    OUT.mkdir(exist_ok=True);validation.OUT=OUT
    old=json.loads((BASE/'multi_case_validation_20261002/report.json').read_text())
    jobs=[]
    for row in old['cases']:
        label=row['label']
        capture=(BASE/'multi_case_validation_20261002'/(label+'_unity') if label.startswith('full')
            else BASE/('unity_new_sample_11009_capture_20261002' if label=='local11009'
                       else 'unity_release_both_complete_activation_v2_20261002'))
        previous=json.loads((BASE/'multi_case_validation_20261002/stop_material_repair_regression'/(label+'_native.json')).read_text())
        jobs.append((label,capture,previous['plan'],row['completedStepsCompared'],False))
    for sid in (12009,12007,12005,12000):
        label=f'additional{sid}';directory=BASE/'additional_case_validation_20261002'
        plan=json.loads((directory/(label+'_plan.json')).read_text())[0]
        jobs.append((label,directory/(label+'_unity'),plan,4000,True))
    reports=[]
    for label,capture,plan,steps,additional in jobs:
        plan_path=OUT/(label+'_plan.json');plan_path.write_text(json.dumps([plan],indent=2))
        native_path=OUT/(label+'_native.json')
        command=[PY39,str(BASE/'sample_new_case_20261002.py'),'--capture',str(capture),
            '--plan',str(plan_path),'--output',str(native_path),'--steps',str(steps)]
        if additional:command.append('--exclude-non-sliding-setters')
        print('RUN',label,flush=True)
        with (OUT/(label+'.log')).open('w') as log:
            subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        native=json.loads(native_path.read_text())
        assert native['integrationCosine']['dllSha256']==validation.digest(ROOT/'local_simulator/runtime/unity_integrate_cos.dll')
        r=(compare_observed if additional else validation.compare)(capture,native_path,'cos_fixed_'+label)
        r['integrationCosine']=native['integrationCosine']
        if label=='additional12000':
            assert r['firstDifference']['kind']=='live_actor_membership'
            assert r['differingBoundaries']==0 and r['lastPreCleanupSolverExit']['bothStoneStatesByteIdentical']
        else:
            assert r['firstDifference'] is None,(label,r['firstDifference'])
            assert r['nativeBothSleepingAtLastComparedStep'] and r['unityBothMotionlessAtLastComparedStep']
        (OUT/(label+'_comparison.json')).write_text(json.dumps(r,indent=2))
        print(label,'PASS',r['completedStepsCompared'],r['firstDifference'],flush=True)
        reports.append(r)
    full=[r for r in reports if r['firstDifference'] is None]
    result=dict(cases=reports,fullTrajectoryRuns=len(full),
        completedStepsCompared=sum(r['completedStepsCompared'] for r in full),
        fullTrajectoryStateBytesCompared=sum(r['stateBytesCompared'] for r in full),
        allFullTrajectoryBytesExact=all(r['stateBytesCompared']==r['stateBytesExact'] for r in full),
        externalCleanupStillUnimplemented='additional12000: first missing active actor at completed boundary1879; solver exit1879 still exact.',
        productionEvidence={str(p.relative_to(ROOT)):validation.digest(p) for p in [ROOT/'local_simulator/unity_physx.py',
            ROOT/'local_simulator/native_integrate_cos.py',ROOT/'local_simulator/runtime/unity_integrate_cos.c',
            ROOT/'local_simulator/runtime/unity_integrate_cos.dll',Path(__file__)]},
        scope='Both actors P/Q/v/w at release and every recorded completed physics boundary. Layout, shot and recorded friction inputs only; no state or material-write injection. Existing Unity observer controls are unchanged.')
    (OUT/'report.json').write_text(json.dumps(result,indent=2))
    print('PASS',len(full),'full trajectories',result['completedStepsCompared'],'steps',result['fullTrajectoryStateBytesCompared'],'bytes',flush=True)

if __name__=='__main__':main()
