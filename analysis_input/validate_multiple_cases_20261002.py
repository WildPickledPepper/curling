"""Reuse complete local truth and fill missing full trajectories for archived cases.

No pose, velocity, quaternion or cache state is injected. Native replay consumes
only the shot, Reset positions and Unity's recorded per-step friction inputs.
"""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

from verify_first_release_chain_20261002 import pose_first
from verify_reset_internal_alignment_20261002 import code_bodies

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input'
OUT = BASE/'multi_case_validation_20261002'
PY39 = r'C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe'
FIELDS = ['px','py','pz','qx','qy','qz','qw','vx','vy','vz','wx','wy','wz']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path, kind):
    for line in path.open(encoding='utf8'):
        if kind not in line:
            continue
        row = json.loads(line)
        if row['type'] == kind:
            yield row['data']


def event_path(capture):
    paths = list(capture.glob('logs/*/events.jsonl'))
    assert len(paths) == 1
    return paths[0]


def run(command, log):
    print('RUN', log.name, flush=True)
    with log.open('w', encoding='utf8') as handle:
        subprocess.run(command, cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT,
                       check=True, creationflags=subprocess.CREATE_NO_WINDOW)


def capture(plan, dest, manifest=None, friction=None, count=None):
    if dest.exists():
        path=event_path(dest)
        pre=list(rows(path,'a12.dense_pre_angular_setter'))
        post=list(rows(path,'a12.dense_post_angular_setter'))
        assert len(pre)==len(post)>0, 'Existing capture has truncated dense inputs'
        assert [r['ordinal'] for r in pre]==[r['ordinal'] for r in post]==list(range(1,len(pre)+1))
        assert not list(rows(path,'rng.friction_manifest_exhausted'))
        assert len(list(dest.glob('*.jsonl')))==1
        if manifest:
            tails=[r['solverSerial'] for r in rows(path,'a12.tail_phase_core')
                   if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter']
            assert max(tails)==4000
        if count is not None:
            assert len(pre)==count+1
        print('REUSE',dest.name,flush=True)
        return
    command = [sys.executable, str(BASE/'capture_12011_first_solver.py'),
        '--plan', str(plan), '--dense-release-serial', '2', '--dense-write-limit', '5000', '--output', str(dest),
        '--expected-release-count','1','--expected-friction-count',str(count or 0),
        '--expected-dense-count',str(count+1 if count is not None else 1),
        '--expected-c03-count','0','--reset-settle-seconds','2',
        '--phase-ordinal-min','1','--phase-ordinal-max','4',
        '--export-wait-seconds','180']
    if manifest:
        command += ['--pcm-call-trace-manifest',str(manifest),
                    '--expected-reset-core-count','256','--expected-tail-boundary-steps','4000']
    if friction:
        command += ['--events',str(friction)]
    else:
        command += ['--natural-friction']
    run(command, OUT/(dest.name+'.log'))
    if manifest:
        (dest/'capture_manifest.json').write_bytes(manifest.read_bytes())
    (dest/'observer_source.js').write_bytes(
        (ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js').read_bytes())


def compare(capture_dir, native_path, label):
    path = event_path(capture_dir)
    native = json.loads(native_path.read_text())
    assert native['sourceSha256'] == digest(ROOT/'local_simulator/unity_physx.py')
    assert native['unityEventsSha256'] == digest(path)
    pre=list(rows(path,'a12.dense_pre_angular_setter'))
    post=list(rows(path,'a12.dense_post_angular_setter'))
    assert [r['ordinal'] for r in pre]==[r['ordinal'] for r in post]==list(range(1,len(pre)+1))
    assert [r['lastFrictionNoise'] for r in pre[1:]]==native['frictionNoises']
    boundaries = {}
    for row in rows(path, 'a12.tail_phase_core'):
        if row['phase'] != 'DCP.FixedUpdate.boundary' or row['edge'] != 'enter':
            continue
        main = [c for c in row['cores'] if c['corePtr'] == row['mainCorePtr']]
        target = [c for c in row['cores'] if c['corePtr'] != row['mainCorePtr']]
        assert len(main) == len(target) == 1
        values = [pose_first(main[0]['bits']), pose_first(target[0]['bits'])]
        tick = row['solverSerial']
        if tick in boundaries:
            assert boundaries[tick] == values
        boundaries[tick] = values
    assert sorted(boundaries) == list(range(max(boundaries)+1)), 'Incomplete captured trajectory'
    assert len(native['states']) >= max(boundaries)
    comparisons = []
    if 0 in boundaries:
        comparisons.append((0, boundaries[0], native['releaseBits']))
    comparisons += [(tick, boundaries[tick], native['states'][tick-1])
                    for tick in sorted(boundaries) if tick > 0]
    first = None
    mismatches = 0
    bytes_exact = 0
    for tick, unity, local in comparisons:
        assert len(unity) == len(local) == 2
        assert all(len(a)==len(b)==13 for a,b in zip(unity,local))
        ub = struct.pack('<26I', *(unity[0]+unity[1]))
        nb = struct.pack('<26I', *(local[0]+local[1]))
        bytes_exact += sum(a==b for a,b in zip(ub,nb))
        if ub != nb:
            mismatches += 1
            if first is None:
                offset = next(i for i,(a,b) in enumerate(zip(ub,nb)) if a!=b)
                stone, word = divmod(offset//4,13)
                first = dict(physicsTick=tick, stoneIndex=native['stoneIndices'][stone],
                    field=FIELDS[word], byteOffsetWithinTwoStoneState=offset,
                    unityBits=f'0x{unity[stone][word]:08x}', nativeBits=f'0x{local[stone][word]:08x}')
    assert first is None or first['physicsTick'] >= min(boundaries)
    report = dict(label=label, validStrictReplay=True, plan=native['plan'], releaseCaptured=0 in boundaries,
        completedStepsCompared=max(boundaries), stateBytesCompared=len(comparisons)*104,
        stateBytesExact=bytes_exact, differingBoundaries=mismatches, firstDifference=first,
        frictionDraws=len(native['frictionNoises']),
        firstNativeContactTick=next(iter(native['stoneContactTicks']),None),
        nativeBothSleepingAtLastComparedStep=all(native['sleeping'][max(boundaries)-1]),
        unityBothMotionlessAtLastComparedStep=all((w & 0x7fffffff)==0 for state in boundaries[max(boundaries)] for w in state[7:]),
        unityLastTwentyCompletedStatesUnchanged=all(boundaries[t]==boundaries[max(boundaries)]
            for t in range(max(1,max(boundaries)-19),max(boundaries)+1)),
        productionSourceSha256=native['sourceSha256'], nativeModuleSha256=native['moduleSha256'],
        evidence={str(p.relative_to(ROOT)):digest(p) for p in (path,native_path)})
    (OUT/(label+'_comparison.json')).write_text(json.dumps(report, indent=2,ensure_ascii=False), encoding='utf8')
    print(json.dumps(report,ensure_ascii=False),flush=True)
    return report


def observer_check(captured, control, manifest, native):
    original = Path(manifest['source'])
    patched = Path(manifest['patched'])
    assert digest(original) == manifest['sourceSha256']
    assert digest(patched) == manifest['patchedSha256']
    a, b = code_bodies(original), code_bodies(patched)
    selected = {r['functionIndex']:r for r in manifest['functions']}
    imports = manifest['importedFunctions']
    for i, body in enumerate(a):
        f = i+imports
        dest = selected[f]['rawFunctionIndex']-imports if f in selected else i
        assert body == b[dest], ('Changed original calculation body',f)
    commands = json.loads((control/'commands.json').read_text())
    assert '--pcm-call-trace-manifest' not in commands['browser']
    assert '--rng-friction-manifest-events' in commands['browser']
    p, q = event_path(captured), event_path(control)
    assert not list(rows(q,'rng.friction_manifest_exhausted')), 'Control friction replay is incomplete'
    noises = json.loads(native.read_text())['frictionNoises']
    assert [r['value'] for r in rows(q,'sliding.random_range.friction')] == noises
    ignore = {'nativePtr','bridgePtr','tickSerial','lastFrictionNoise','bridge164Bits','bridge300Bits'}
    for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
        x,y = list(rows(p,kind)),list(rows(q,kind))
        assert len(x)==len(y)==len(noises)+1, (kind,len(x),len(y),len(noises))
        for u,v in zip(x,y):
            assert {k:val for k,val in u.items() if k not in ignore} == {k:val for k,val in v.items() if k not in ignore}, (kind,u['ordinal'])
            for field in ('getterLinear','getterAngular','setterAngular','bridge164','bridge300'):
                if u.get(field) is not None:
                    assert struct.pack('<3f',*u[field]) == struct.pack('<3f',*v[field])
            if u.get('pose'):
                assert struct.pack('<7f',*(u['pose']['p']+u['pose']['q'])) == struct.pack('<7f',*(v['pose']['p']+v['pose']['q']))
    def sample(d):
        return json.loads(next(d.glob('*.jsonl')).read_text().splitlines()[0])
    x,y=sample(captured),sample(control)
    for key in ('requested','after_position','final_xy','target_moves','collision_observed'):
        assert x[key]==y[key],key
    return dict(originalCalculationBodiesByteIdentical=True, unpatchedWasmControl=True,
        setterGetterPosePairsByteIdentical=len(noises)+1, frictionInputsByteIdentical=len(noises),
        protocolResultUnchanged=True, scope='Original-Wasm control covers the complete recorded custom sliding window and final protocol result.',
        evidence={str(t.relative_to(ROOT)):digest(t) for t in (q,original,patched)})


def main():
    OUT.mkdir(exist_ok=True)
    reports=[]
    existing=[('local11009',BASE/'unity_new_sample_11009_capture_20261002', BASE/'new_sample_11009_plan_20261002.json',3000),
              ('local11000',BASE/'unity_release_both_complete_activation_v2_20261002',BASE/'old_sample_11000_regression_plan_20261002.json',4000)]
    for label,cap,plan,steps in existing:
        native=OUT/(label+'_native.json')
        run([PY39,str(BASE/'sample_new_case_20261002.py'),'--capture',str(cap),'--plan',str(plan),
             '--output',str(native),'--steps',str(steps)],OUT/(label+'_native.log'))
        reports.append(compare(cap,native,label))
    source=ROOT/'research_archive/unity_reverse/evidence/config/unity_extended_collision_batches_20260714/collision_unique_targets_batch_r03.json'
    plans=json.loads(source.read_text())
    m=json.loads((BASE/'unity_new_sample_11009_capture_20261002/capture_manifest.json').read_text())
    m['wakeFunctionTrace']=[]
    m['wakeFunctionWindow']=dict(minOrdinal=1,maxOrdinal=4,maxSolverSerial=4)
    m['velocityGetterMaxOrdinal']=5000
    m['tailCoreWindow']=dict(minOrdinal=1,maxOrdinal=5000,allStoneCores=True,maxSolverSteps=4000)
    manifest=OUT/'full_trajectory_manifest.json'
    manifest.write_text(json.dumps(m,indent=2),encoding='utf8')
    for number,sid in enumerate((12004,12008,12011,12008),1):
        label=f'full{sid}_run{number}'
        plan=dict(next(p for p in plans if p['sample_id']==sid))
        plan['active_index']=0
        plan['label']=label
        plan['notes']='Archived shot parameters, fresh page, natural Unity friction, no state injection.'
        planpath=OUT/(label+'_plan.json')
        planpath.write_text(json.dumps([plan],indent=2),encoding='utf8')
        cap=OUT/(label+'_unity')
        capture(planpath,cap,manifest=manifest)
        native=OUT/(label+'_native.json')
        run([PY39,str(BASE/'sample_new_case_20261002.py'),'--capture',str(cap),'--plan',str(planpath),
             '--output',str(native),'--steps','4000'],OUT/(label+'_native.log'))
        report=compare(cap,native,label)
        control=OUT/(label+'_original_control')
        n=json.loads(native.read_text())
        friction=OUT/(label+'_friction.jsonl')
        friction.write_text(''.join(json.dumps(dict(type='sliding.random_range.friction',data=dict(value=v)))+'\n'
                                    for v in n['frictionNoises']),encoding='utf8')
        capture(planpath,control,friction=friction,count=len(n['frictionNoises']))
        report['observer']=observer_check(cap,control,m,native)
        (OUT/(label+'_comparison.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
        reports.append(report)
        (OUT/'progress_report.json').write_text(json.dumps(reports,indent=2,ensure_ascii=False),encoding='utf8')
    final=dict(cases=reports, runs=len(reports), distinctShotConditions=len({(r['plan']['v0'],r['plan']['h0'],r['plan']['w0'],json.dumps(r['plan']['stones'],sort_keys=True)) for r in reports}),
        completedStepsCompared=sum(r['completedStepsCompared'] for r in reports),
        stateBytesCompared=sum(r['stateBytesCompared'] for r in reports),
        allComparedBytesExact=all(r['firstDifference'] is None for r in reports),
        scope='Actual Unity raw P/Q/v/w of both stones at release and completed simulation steps. Identical captured friction inputs; no post-release state injection.',
        localInventory='analysis_input/local_unity_capture_inventory_20261002.json')
    final['passedRuns']=sum(r['firstDifference'] is None for r in reports)
    final['failedRuns']=len(reports)-final['passedRuns']
    final['allCasesObservedThroughRest']=all(r['nativeBothSleepingAtLastComparedStep'] and
        r['unityBothMotionlessAtLastComparedStep'] and r['unityLastTwentyCompletedStatesUnchanged'] for r in reports)
    repeated=[json.loads((OUT/(label+'_native.json')).read_text()) for label in ('full12008_run2','full12008_run4')]
    final['repeatedStrongCurl']=dict(runs=['full12008_run2','full12008_run4'],
        frictionDrawsPerRun=len(repeated[0]['frictionNoises']),
        differingFrictionDraws=sum(a!=b for a,b in zip(repeated[0]['frictionNoises'],repeated[1]['frictionNoises'])),
        bothCompleteTrajectoriesExact=all(r['firstDifference'] is None for r in reports if r['label'] in ('full12008_run2','full12008_run4')),
        frictionStreamSha256=[hashlib.sha256(struct.pack('<%df'%len(r['frictionNoises']),*r['frictionNoises'])).hexdigest() for r in repeated])
    final['excludedInvalidReplay']='fresh12004_run1: truncated dense inputs; apparent tick 2000 difference invalidated.'
    final['firstDivergenceEvidence']='analysis_input/multi_case_validation_20261002/case12004_first_divergence_verified.json'
    final['productionCodeChanged']=False
    (OUT/'report.json').write_text(json.dumps(final,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:v for k,v in final.items() if k!='cases'},ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
