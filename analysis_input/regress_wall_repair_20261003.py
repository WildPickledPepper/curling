"""Fresh production replays after adding real walls and collision callbacks."""
import json
from pathlib import Path
import subprocess

import validate_multiple_cases_20261002 as v
from validate_additional_cases_20261002 import compare_observed
from compare_wall_repair_20261003 import compare as compare_wall

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
OUT=BASE/'wall_repair_regression_20261003'
PY39=r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe'


def main():
    OUT.mkdir(exist_ok=True)
    v.OUT=OUT
    old=json.loads((BASE/'multi_case_validation_20261002/report.json').read_text())
    jobs=[]
    for row in old['cases']:
        label=row['label']
        capture=(BASE/'multi_case_validation_20261002'/(label+'_unity') if label.startswith('full')
            else BASE/('unity_new_sample_11009_capture_20261002' if label=='local11009'
                       else 'unity_release_both_complete_activation_v2_20261002'))
        previous=json.loads((BASE/'cos_repair_regression_20261003'/(label+'_native.json')).read_text())
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
        if label=='additional12000':command.extend(['--trace-from-step','1879'])
        print('RUN',label,flush=True)
        with (OUT/(label+'.log')).open('w') as log:
            subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        native=json.loads(native_path.read_text())
        if label=='additional12000':
            r=compare_wall(capture,native_path,label)
        else:
            r=(compare_observed if additional else v.compare)(capture,native_path,'wall_fixed_'+label)
            assert all(all(alive) for alive in native['enabled'])
            assert native['simulating']==native['enabled']
            assert native['releaseSimulating']==native['releaseEnabled']==[True,True]
            assert not native['wallContacts']
        assert r['firstDifference'] is None,(label,r['firstDifference'])
        assert r['stateBytesCompared']==r['stateBytesExact'] and r['completedStepsCompared']==steps
        r['wallContactMetadata']=native['wallContactMetadata']
        (OUT/(label+'_comparison.json')).write_text(json.dumps(r,indent=2))
        print(label,'PASS',r['completedStepsCompared'],flush=True)
        reports.append(r)
    files=[ROOT/'local_simulator/unity_physx.py',ROOT/'local_simulator/native_wall_contact.py',
        ROOT/'local_simulator/assets/unity_wall_colliders.json',ROOT/'local_simulator/examples/train_policy_tree_selfplay.py',
        Path(__file__)]
    result=dict(cases=reports,fullTrajectoryRuns=len(reports),
        completedStepsCompared=sum(r['completedStepsCompared'] for r in reports),
        fullTrajectoryStateBytesCompared=sum(r['stateBytesCompared'] for r in reports),
        allFullTrajectoryBytesExact=all(r['stateBytesCompared']==r['stateBytesExact'] for r in reports),
        allFirstDifferencesNull=all(r['firstDifference'] is None for r in reports),
        productionEvidence={str(p.relative_to(ROOT)):v.digest(p) for p in files},
        scope='Release and every captured completed boundary; raw P/Q/v/w for live actors. 12000 additionally compares all4001 actor sets, solver exit1879 before callback, retained callback pose and zero velocities. Layout/shot/recorded friction inputs only; no cleanup timing/state injection.')
    (OUT/'report.json').write_text(json.dumps(result,indent=2))
    print('PASS',len(reports),'full trajectories',result['completedStepsCompared'],'steps',
          result['fullTrajectoryStateBytesCompared'],'bytes',flush=True)


if __name__=='__main__':main()
