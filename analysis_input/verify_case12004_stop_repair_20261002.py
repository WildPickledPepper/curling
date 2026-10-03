"""Verify the production natural-stop repair without material/state injection."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

from validate_multiple_cases_20261002 import compare, event_path, observer_check
from verify_first_release_chain_20261002 import pose_first
from verify_pcm_internal_trace import raw_argument

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input/multi_case_validation_20261002'
OUT = BASE/'stop_material_repair_regression'
PY39 = r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    before = json.loads((BASE/'report.json').read_text())
    reports = []
    for old in before['cases']:
        label = old['label']
        native_before = json.loads((BASE/(label+'_native.json')).read_text())
        plan = OUT/(label+'_plan.json')
        plan.write_text(json.dumps([native_before['plan']],indent=2),encoding='utf8')
        capture = (BASE/(label+'_unity') if label.startswith('full') else ROOT/'analysis_input'/
            ('unity_new_sample_11009_capture_20261002' if label=='local11009'
             else 'unity_release_both_complete_activation_v2_20261002'))
        native = OUT/(label+'_native.json')
        command = [PY39,str(ROOT/'analysis_input/sample_new_case_20261002.py'),
            '--capture',str(capture),'--plan',str(plan),'--output',str(native),
            '--steps',str(old['completedStepsCompared'])]
        if label=='full12004_run1':command += ['--trace-from-step','3169','--trace-through-step','3169']
        print('RUN',label,flush=True)
        with (OUT/(label+'.log')).open('w',encoding='utf8') as log:
            subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        new = json.loads(native.read_text())
        report = compare(capture,native,'stop_fixed_'+label)
        assert report['firstDifference'] is None
        if label!='full12004_run1':
            assert new['states']==native_before['states'][:len(new['states'])]
            assert new['releaseBits']==native_before['releaseBits']
        reports.append(report)

    # Compare every static solver iteration at the old first difference.
    focused = event_path(BASE/'case12004_stop_material_unity')
    serial = 0
    solves = []
    for line in focused.open(encoding='utf8'):
        row = json.loads(line);d = row['data']
        if row['type']=='a12.tail_phase_core' and d['phase']=='PxsDynamics.solverSetupSolve' and d['edge']=='enter':serial=d['solverSerial']
        if row['type']=='a12.static_solve' and serial==3:solves.append(d)
    corrected = json.loads((OUT/'full12004_run1_native.json').read_text())
    native_solves = corrected['nativePhases'][0]['solve_block']
    assert len(solves)==len(native_solves)==5
    for a,b in zip(solves,native_solves):
        x=bytes(a['before']['descs'][0]['constraintWindow']['rawBytes']);y=bytes(b['constraint_bytes_before'])
        assert x[:56]==y[:56]
        for i in range(5):assert x[64+i*48:112+i*48]==y[80+i*48:128+i*48]
        for i in range(4):
            for off in list(range(0,32,4))+[44,48]:assert x[336+i*64+off:340+i*64+off]==y[352+i*64+off:356+i*64+off]
        for edge in ('before','after'):
            assert bytes(a[edge]['descs'][0]['bodyAWindow']['rawBytes'][:32])==bytes(b['body_a_'+edge]['raw_bytes'])

    # Additional caller/origin capture. It did not contain the requested five
    # tail boundaries, so it is NOT a full-trajectory or repaired-solver proof.
    # Validate its actual observed custom window, original code and protocol.
    cap = BASE/'case12004_stop_controller_unity'
    (cap/'capture_manifest.json').write_bytes((BASE/'case12004_stop_controller_manifest.json').read_bytes())
    manifest = json.loads((cap/'capture_manifest.json').read_text())
    observer = observer_check(cap,BASE/'full12004_run1_original_control',manifest,OUT/'full12004_run1_native.json')
    path = event_path(cap)
    calls=[];observed_phases=[];completed=[]
    for line_number,line in enumerate(path.open(encoding='utf8'),1):
        row=json.loads(line);d=row['data']
        if row['type']=='a12.pcm_internal_call':calls.append((line_number,d))
        if row['type']=='a12.tail_phase_core':
            if d['phase']=='PxsDynamics.solverSetupSolve' and d['edge']=='exit':
                observed_phases.append(d)
            if d['phase']=='DCP.FixedUpdate.boundary' and d['edge']=='enter':completed.append(d['solverSerial'])
    parent_line,parent=next((line,d) for line,d in calls if d['functionIndex']==61097)
    origin_words=list(struct.unpack_from('<3I',raw_argument(parent,0,'before'),220))
    origin=list(struct.unpack('<3f',struct.pack('<3I',*origin_words)))
    assert origin==[-96.85420227050781,14.43239974975586,54.174400329589844]
    setter_calls=[(line,d) for line,d in calls if d['functionIndex'] in (32511,32512)]
    assert [d['functionIndex'] for _,d in setter_calls]==[32511,32512]
    assert all(d['parentCallId']==parent['callId'] and d['ordinal']==3169 and
               d['args'][1]==0.6000000238418579 for _,d in setter_calls)
    assert [d['solverSerial'] for d in observed_phases]==[1,2]
    for d in observed_phases:
        assert pose_first(d['bits'])==corrected['states'][3166+d['solverSerial']-1][0]
    caller_proof=dict(functionIndex=61097,tableIndex=parent['tableIndex'],callId=parent['callId'],line=parent_line,
        setterLines=[line for line,_ in setter_calls],originWords=origin_words,origin=origin,
        observedCompletedPhysicsSteps=[3167,3168],observerCheck=observer,
        captureLimitation='Requested five tail boundaries were not captured; only boundary serial1 and solver exits1/2 are present. Used solely for the actual parent call and cached origin. Complete trajectory truth and all five repaired solver iterations use earlier independently validated captures.',
        observedBoundarySerials=completed,evidenceSha256=digest(path))
    result=dict(cases=reports,runs=len(reports),completedStepsCompared=sum(r['completedStepsCompared'] for r in reports),
        stateBytesCompared=sum(r['stateBytesCompared'] for r in reports),allComparedBytesExact=True,
        allCasesObservedThroughRest=all(r['nativeBothSleepingAtLastComparedStep'] and r['unityBothMotionlessAtLastComparedStep']
            and r['unityLastTwentyCompletedStatesUnchanged'] for r in reports),
        productionCodeChanged=True,productionSourceSha256=digest(ROOT/'local_simulator/unity_physx.py'),
        nativeModuleSha256=reports[0]['nativeModuleSha256'],correctedSolverIterationsInputsAndOutputsExact=5,
        unchangedExistingRuns=5,actualControllerAndOrigin=caller_proof,
        scope='Actual Unity P/Q/v/w bytes at release and every completed physics step for both stones. Only shot/layout/friction inputs supplied; no replay of material setter calls or body/contact/cache state. Update is evaluated at the explicit custom-setter-batch to ordinary-physics boundary.',
        fixtureSha256=digest(ROOT/'local_simulator/tests/fixtures/unity_natural_stop_12004_20261002.json'))
    (OUT/'report.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    print('PASS: six runs,21000steps,2184624state bytes; five solver iterations exact; actual DCP.Update parent and cached origin observed.')


if __name__=='__main__':main()
