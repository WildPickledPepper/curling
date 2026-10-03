"""Four new complete Unity trajectories and original-Wasm observer controls."""
import contextlib
import hashlib
import json
from pathlib import Path
import struct
import traceback

import validate_multiple_cases_20261002 as validation

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input'
OUT = BASE/'additional_case_validation_20261002'
SELECTED = (12000,12007,12009,12005)


def compare_observed(capture_dir, native_path, label):
    """Never substitute fallback zeros for an actor absent from the live core map."""
    v = validation
    path = v.event_path(capture_dir)
    native = json.loads(native_path.read_text())
    assert native['sourceSha256'] == v.digest(ROOT/'local_simulator/unity_physx.py')
    assert native['unityEventsSha256'] == v.digest(path)
    pre = list(v.rows(path,'a12.dense_pre_angular_setter'))
    post = list(v.rows(path,'a12.dense_post_angular_setter'))
    assert [r['ordinal'] for r in pre] == [r['ordinal'] for r in post] == list(range(1,len(pre)+1))
    sliding = [r for r in pre[1:] if r['tickSerial'] is not None and
               r['getterLinear'] is not None and r['getterAngular'] is not None]
    assert [r['lastFrictionNoise'] for r in sliding] == native['frictionNoises']
    tail = list(v.rows(path,'a12.tail_phase_core'))
    boundaries = [r for r in tail if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter']
    assert [r['solverSerial'] for r in boundaries] == list(range(4001))
    first = boundaries[0]
    core_order = [first['mainCorePtr']] + [c['corePtr'] for c in first['cores'] if c['corePtr']!=first['mainCorePtr']]
    assert len(core_order)==2
    first_difference = None
    missing = []
    states = {}
    exact = 0
    differing = 0
    for row in boundaries:
        tick = row['solverSerial']
        mapping = {c['corePtr']:c for c in row['cores']}
        if any(c not in mapping for c in core_order):
            missing.append(tick)
            if first_difference is None:
                first_difference = dict(physicsTick=tick,kind='live_actor_membership',
                    observedCorePointers=sorted(mapping),expectedCorePointers=core_order,
                    scope='Native physics-only harness does not replay the observed external actor cleanup calls.')
            continue
        unity = [v.pose_first(mapping[c]['bits']) for c in core_order]
        local = native['releaseBits'] if tick==0 else native['states'][tick-1]
        ub,nb = (struct.pack('<26I',*(state[0]+state[1])) for state in (unity,local))
        states[tick] = unity
        exact += sum(a==b for a,b in zip(ub,nb))
        if ub!=nb:
            differing += 1
            if first_difference is None:
                offset=next(i for i,(a,b) in enumerate(zip(ub,nb)) if a!=b)
                stone,word=divmod(offset//4,13)
                first_difference=dict(physicsTick=tick,kind='raw_state',stoneIndex=native['stoneIndices'][stone],
                    field=v.FIELDS[word],byteOffsetWithinTwoStoneState=offset,
                    unityBits=f'0x{unity[stone][word]:08x}',nativeBits=f'0x{local[stone][word]:08x}')
    last=max(states)
    report=dict(label=label,plan=native['plan'],releaseCaptured=True,
        capturedCompletedSteps=4000,completedStepsCompared=last,stateBytesCompared=len(states)*104,
        stateBytesExact=exact,differingBoundaries=differing,firstDifference=first_difference,
        fullTrajectoryExact=first_difference is None and last==4000,
        missingActiveBoundaryCount=len(missing),frictionDraws=len(native['frictionNoises']),
        excludedNonSlidingSetters=native['excludedNonSlidingSetters'],
        firstNativeContactTick=next(iter(native['stoneContactTicks']),None),
        nativeBothSleepingAtLastComparedStep=all(native['sleeping'][last-1]),
        unityBothMotionlessAtLastComparedStep=all((w&0x7fffffff)==0 for state in states[last] for w in state[7:]),
        unityLastTwentyCompletedStatesUnchanged=all(states[t]==states[last] for t in range(max(1,last-19),last+1)),
        productionSourceSha256=native['sourceSha256'],nativeModuleSha256=native['moduleSha256'],
        evidence={str(p.relative_to(ROOT)):v.digest(p) for p in (path,native_path)})
    if missing:
        tick=missing[0]
        solver=[r for r in tail if r['solverSerial']==tick and r['phase']=='PxsDynamics.solverSetupSolve' and r['edge']=='exit']
        assert len(solver)==1
        mapping={c['corePtr']:c for c in solver[0]['cores']}
        unity=[v.pose_first(mapping[c]['bits']) for c in core_order]
        report['lastPreCleanupSolverExit']=dict(physicsTick=tick,bothStoneStatesByteIdentical=unity==native['states'][tick-1],
            unityBits=unity,nativeBits=native['states'][tick-1])
        report['observedRemovalCalls']=[{k:r.get(k) for k in ('callId','functionIndex','tableIndex','ordinal','args','rigidIdBefore')}
            for r in v.rows(path,'a12.pcm_internal_call') if r['functionIndex']==71727 and r.get('ordinal',0)>1]
    return report


def check_observer(captured,control,manifest,native_path):
    """Include cleanup setter pairs, while counting actual friction draws only."""
    v=validation
    original,patched=Path(manifest['source']),Path(manifest['patched'])
    assert v.digest(original)==manifest['sourceSha256']
    assert v.digest(patched)==manifest['patchedSha256']
    a,b=v.code_bodies(original),v.code_bodies(patched)
    selected={r['functionIndex']:r for r in manifest['functions']}
    imports=manifest['importedFunctions']
    for i,body in enumerate(a):
        f=i+imports
        dest=selected[f]['rawFunctionIndex']-imports if f in selected else i
        assert body==b[dest],('Changed original calculation body',f)
    commands=json.loads((control/'commands.json').read_text())
    assert '--pcm-call-trace-manifest' not in commands['browser']
    assert '--rng-friction-manifest-events' in commands['browser']
    p,q=v.event_path(captured),v.event_path(control)
    assert not list(v.rows(q,'rng.friction_manifest_exhausted'))
    n=json.loads(native_path.read_text())
    assert [r['value'] for r in v.rows(q,'sliding.random_range.friction')]==n['frictionNoises']
    ignore={'nativePtr','bridgePtr','tickSerial','lastFrictionNoise','bridge164Bits','bridge300Bits'}
    expected=len(n['frictionNoises'])+1+len(n['excludedNonSlidingSetters'])
    for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
        x,y=list(v.rows(p,kind)),list(v.rows(q,kind))
        assert len(x)==len(y)==expected,(kind,len(x),len(y),expected)
        for u,w in zip(x,y):
            assert {k:val for k,val in u.items() if k not in ignore}=={k:val for k,val in w.items() if k not in ignore},(kind,u['ordinal'])
            for field in ('getterLinear','getterAngular','setterAngular','bridge164','bridge300'):
                if u.get(field) is not None:
                    assert struct.pack('<3f',*u[field])==struct.pack('<3f',*w[field])
            if u.get('pose'):
                assert struct.pack('<7f',*(u['pose']['p']+u['pose']['q']))==struct.pack('<7f',*(w['pose']['p']+w['pose']['q']))
    x,y=(json.loads(next(d.glob('*.jsonl')).read_text().splitlines()[0]) for d in (captured,control))
    for key in ('requested','after_position','final_xy','target_moves','collision_observed'):
        assert x[key]==y[key],key
    return dict(originalCalculationBodiesByteIdentical=True,unpatchedWasmControl=True,
        setterGetterPosePairsByteIdentical=expected,frictionInputsByteIdentical=len(n['frictionNoises']),
        protocolResultUnchanged=True,evidence={str(t.relative_to(ROOT)):v.digest(t) for t in (q,original,patched)})


def main():
    OUT.mkdir(exist_ok=True)
    validation.OUT = OUT
    source = ROOT/'research_archive/unity_reverse/evidence/config/unity_extended_collision_batches_20260714/collision_unique_targets_batch_r03.json'
    plans = json.loads(source.read_text())
    manifest_data = json.loads((BASE/'multi_case_validation_20261002/full_trajectory_manifest.json').read_text())
    manifest = OUT/'full_trajectory_manifest.json'
    manifest.write_text(json.dumps(manifest_data,indent=2),encoding='utf8')
    production_hash = validation.digest(ROOT/'local_simulator/unity_physx.py')
    results = []
    for sid in SELECTED:
        label = f'additional{sid}'
        plan = dict(next(p for p in plans if p['sample_id']==sid))
        plan.update(active_index=0,label=label,notes='Independent fresh Unity page, original local shot parameters, natural friction inputs, complete raw state capture. No body/contact/cache/material-write injection.')
        plan_path = OUT/(label+'_plan.json')
        plan_path.write_text(json.dumps([plan],indent=2),encoding='utf8')
        capture = OUT/(label+'_unity')
        print('CAPTURE',sid,plan['category'],flush=True)
        validation.capture(plan_path,capture,manifest=manifest)
        native = OUT/(label+'_native_sliding_only.json')
        validation.run([validation.PY39,str(BASE/'sample_new_case_20261002.py'),
            '--capture',str(capture),'--plan',str(plan_path),'--output',str(native),'--steps','4000',
            '--exclude-non-sliding-setters'],
            OUT/(label+'_native.log'))
        with (OUT/(label+'_compare.log')).open('w',encoding='utf8') as log:
            with contextlib.redirect_stdout(log):
                report=compare_observed(capture,native,label)
                print(json.dumps(report,ensure_ascii=False))
        print('COMPARED',sid,'firstDifference',report['firstDifference'],flush=True)
        n = json.loads(native.read_text())
        friction = OUT/(label+'_friction.jsonl')
        friction.write_text(''.join(json.dumps(dict(type='sliding.random_range.friction',data=dict(value=v)))+'\n'
                                    for v in n['frictionNoises']),encoding='utf8')
        control = OUT/(label+'_original_control')
        print('ORIGINAL_WASM_CONTROL',sid,flush=True)
        try:
            # Cleanup calls add dense setters without drawing fresh friction.
            if control.exists():
                validation.capture(plan_path,control,friction=friction)
            else:
                validation.capture(plan_path,control,friction=friction,count=len(n['frictionNoises']))
            report['observer']=check_observer(capture,control,manifest_data,native)
        except Exception as err:
            report['observer']=dict(unpatchedWasmControl=False,error=f'{type(err).__name__}: {err}',
                                    traceback=traceback.format_exc())
        (OUT/(label+'_comparison.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
        results.append(report)
        (OUT/'progress_report.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
        assert validation.digest(ROOT/'local_simulator/unity_physx.py')==production_hash
        print('DONE',sid,'bytesExact',report['stateBytesExact'],'/',report['stateBytesCompared'],flush=True)
    final = dict(cases=results,runs=len(results),distinctShotConditions=len(results),
        completedStepsCompared=sum(r['completedStepsCompared'] for r in results),
        stateBytesCompared=sum(r['stateBytesCompared'] for r in results),
        stateBytesExact=sum(r['stateBytesExact'] for r in results),
        passedRuns=sum(r['fullTrajectoryExact'] for r in results),
        failedOrIncompleteRuns=sum(not r['fullTrajectoryExact'] for r in results),
        allComparedBytesExact=all(r['differingBoundaries']==0 for r in results),
        allCompleteTrajectoriesExact=all(r['fullTrajectoryExact'] for r in results),
        allCasesObservedThroughRest=all(r['nativeBothSleepingAtLastComparedStep'] and r['unityBothMotionlessAtLastComparedStep']
                                       and r['unityLastTwentyCompletedStatesUnchanged'] for r in results),
        allOriginalWasmObserverControlsPassed=all(r['observer']['unpatchedWasmControl'] for r in results),
        productionCodeChanged=False,productionSourceSha256=production_hash,
        unityOriginalSha256=manifest_data['sourceSha256'],nativeModuleSha256=results[0]['nativeModuleSha256'],
        scope='New shot conditions from local archived parameters. Independent fresh Reset per run. Release and every completed physics step, both stones P/Q/v/w, raw26float32 words (104bytes). Recorded friction only, no post-release body/contact/cache/material-call injection.',
        planSource=str(source.relative_to(ROOT)),planSourceSha256=validation.digest(source))
    (OUT/'report.json').write_text(json.dumps(final,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:v for k,v in final.items() if k!='cases'},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
