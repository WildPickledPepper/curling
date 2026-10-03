"""Audit the actual cache -> PCM -> static constraints -> state divergence."""
import hashlib
import json
import re
import struct
from pathlib import Path

import wasmtime
from verify_pcm_internal_trace import events, rows_of, raw_argument
from verify_release_ordinary_tail_20261002 import core_states
from verify_reset_internal_alignment_20261002 import code_bodies, words
from verify_new_sample_11009_20261002 import differences

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def floats(b): return list(struct.unpack('<%df'%(len(b)//4),b))

def main():
    capture=BASE/'unity_sample11009_step1383_capture_v2_20261002'
    unity,path=events(capture)
    baseline,baseline_path=events(BASE/'unity_new_sample_11009_capture_20261002')
    assert not [r for r in unity if 'failed' in r['type'] or 'exhausted' in r['type']]
    pack=lambda v:struct.pack('<%df'%len(v),*v)
    for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
        a,b=rows_of(unity,kind),rows_of(baseline,kind)
        assert len(a)==len(b)==1384
        for x,y in zip(a,b):
            for k in ('getterLinear','getterAngular','setterAngular','bridge164','bridge300'):
                if x.get(k) is not None: assert pack(x[k])==pack(y[k])
            if x.get('pose'): assert pack(x['pose']['p']+x['pose']['q'])==pack(y['pose']['p']+y['pose']['q'])
    assert [r['value'] for r in rows_of(unity,'sliding.random_range.friction')]==[
        r['lastFrictionNoise'] for r in rows_of(baseline,'a12.dense_pre_angular_setter')[1:]]
    a,b=rows_of(unity,'scene.reset_body_cores'),rows_of(baseline,'scene.reset_body_cores')
    assert len(a)==len(b)==256
    for x,y in zip(a,b):
        assert x['step']==y['step'] and x['edge']==y['edge']
        assert [c['bits'] for c in x['cores']]==[c['bits'] for c in y['cores']]
    sample=lambda d:json.loads(next(d.glob('*.jsonl')).read_text().splitlines()[0])
    for k in ('requested','after_position','final_xy','target_moves','collision_observed'):
        assert sample(capture)[k]==sample(BASE/'unity_new_sample_11009_capture_20261002')[k]
    manifest=json.loads((capture/'capture_manifest.json').read_text())
    source=BASE/'unity_20260930.wasm'
    assert digest(source)==manifest['sourceSha256']
    assert digest(Path(manifest['patched']))==manifest['patchedSha256']
    original,patched=code_bodies(source),code_bodies(Path(manifest['patched']))
    for f in manifest['functions']:
        assert original[f['functionIndex']-476]==patched[f['rawFunctionIndex']-476]
    bounds={r['solverSerial']:core_states(r) for r in rows_of(baseline,'a12.tail_phase_core')
            if r['phase']=='DCP.FixedUpdate.boundary'}
    for r in rows_of(unity,'a12.tail_phase_core'):
        if r['phase']=='DCP.FixedUpdate.boundary': assert core_states(r)==bounds[1381+r['solverSerial']]
    native_path=BASE/'native_sample11009_step1383_trace_20261002.json'
    native=json.loads(native_path.read_text())
    production=json.loads((BASE/'native_bestshot_offset_fixed_11009_20261002.json').read_text())
    assert native['states']==production['states'] and native['releaseBits']==production['releaseBits']
    n=native['nativePhases'][1]
    assert n['physicsTick']==1383 and n['afterNativeBits']==native['states'][1382]
    static=[]; refresh=[]; meshes=[]; serial=0
    for r in unity:
        d=r['data']
        if r['type']=='a12.tail_phase_core' and d['phase']=='PxsDynamics.solverSetupSolve' and d['edge']=='enter':
            serial=d['solverSerial']
        # Narrowphase happens before solver entry; use the preceding serial.
        if serial==1 and r['type']=='a12.pcm_convex_mesh': meshes.append(d)
        if serial==1 and r['type']=='a12.pcm_internal_call' and d['functionIndex']==69978: refresh.append(d)
        if serial==2 and r['type']=='a12.static_solve': static.append(d)
    target_x=-71.17739868164062
    pcm=next(r for r in meshes if r['before']['transform0']['p'][0]==target_x)
    assert pcm['before']['cache']['cachedSize']==pcm['after']['cache']['cachedSize']==304
    assert len(refresh)==1 and len(static)==5
    calls_path=BASE/'native_sample11009_step1383_cache_clear_20261002/calls.json'
    calls=json.loads(calls_path.read_text())
    assert calls['callStackReliable'] and not calls['unfinished'] and not calls['dropped']
    trace_output=json.loads(calls_path.with_name('alignment.json').read_text())
    assert trace_output['states']==production['states']
    clear=calls['calls'][0]
    assert clear['functionRva']=='0x330f0' and clear['returnAddressRva']=='0x28487f'
    assert clear['multiCacheBefore']['cachedSize']==304 and clear['multiCacheAfter']['cachedSize']==0
    assert struct.unpack_from('<I',bytes(clear['multiCacheBefore']['serializedBytes']),32)[0]==1
    assert struct.unpack_from('<I',bytes(clear['multiCacheAfter']['serializedBytes']),32)[0]==0
    assert not [r for r in calls['calls'] if r['functionRva']=='0x29cbe0']
    nr=next(r for r in calls['calls'] if r['functionRva']=='0x2e2880')
    for arg,k in ((5,'transform0'),(6,'transform1')):
        assert list(struct.unpack_from('<7I',raw_argument(nr,arg,'before')))==words(pcm['before'][k]['q']+pcm['before'][k]['p'])
    # Prior serialized cache and Unity refresh input have the same arithmetic
    # fields; 48-byte serialized records become 64-byte expanded records.
    previous=bytes(clear['multiCacheBefore']['serializedBytes'])
    input_contacts=raw_argument(refresh[0],1,'before')
    for i in range(5):
        for off in (0,4,8,16,20,24,32,36,40,44):
            assert previous[64+i*48+off:68+i*48+off]==input_contacts[i*64+off:i*64+off+4]
    # Execute the verbatim original WAT body, with only memory/export wrapper.
    function_path=BASE/'pcm_functions_20261001/f69978.wat'
    body=re.sub(r'\(type \$t\d+\)','',function_path.read_text(),count=1)
    kernel=wasmtime.wat2wasm('(module (memory (export "memory") 2) '+body+' (export "refresh" (func $f69978)))')
    kernel_path=BASE/'unity_pcm_refresh_numeric_kernel_20261002.wasm'
    kernel_path.write_bytes(kernel)
    engine=wasmtime.Engine(); store=wasmtime.Store(engine)
    instance=wasmtime.Instance(store,wasmtime.Module(engine,kernel),[])
    memory=instance.exports(store)['memory']; ptrs=(64,1024,2048,4096)
    for arg,size in ((1,400),(2,60),(3,4)):
        memory.write(store,raw_argument(refresh[0],arg,'before')[:size],ptrs[arg])
    instance.exports(store)['refresh'](store,*ptrs)
    output=bytes(memory.read(store,1024,1424))
    expected=raw_argument(refresh[0],1,'after')[:400]
    assert output==expected
    contact_differences=[]
    contacts=raw_argument(nr,8,'after')
    for i,p in enumerate(pcm['after']['contactBuffer']['contactsPreview']):
        a=words(p['normal']+[p['separation']]+p['point'])
        b=list(struct.unpack_from('<7I',contacts,i*64))
        assert [j for j,(x,y) in enumerate(zip(a,b)) if x!=y]==[3]
        assert a[3]==struct.unpack_from('<I',output,i*64+44)[0]
        assert b[3]==struct.unpack_from('<I',previous,64+i*48+44)[0]
        contact_differences.append(dict(contact=i,unitySeparation=p['separation'],
            nativeSeparation=struct.unpack_from('<f',contacts,i*64+12)[0],
            unityBits=hex(a[3]),nativeBits=hex(b[3])))
    target_index=next(i for i,d in enumerate(static[0]['before']['solverBodyData']) if d['bodyA']['body2World']['p'][0]==target_x)
    u=bytes(static[0]['before']['descs'][target_index]['constraintWindow']['rawBytes'])
    target_solves=[r for r in n['solve_block'] if r['constraint_type']==5 and r['data_a_before']['body2world']['p'][0]==target_x]
    assert len(target_solves)==5
    b=bytes(target_solves[0]['constraint_bytes_before'])
    assert u[:56]==b[:56]
    normal_differences=[]
    for i in range(5):
        a=struct.unpack_from('<12I',u,64+i*48); c=struct.unpack_from('<12I',b,80+i*48)
        assert [j for j,(x,y) in enumerate(zip(a,c)) if x!=y]==[9]
        normal_differences.append(dict(row=i,offsetWithinRow=36,unityBits=hex(a[9]),nativeBits=hex(c[9])))
    for i in range(4):
        for off in list(range(0,32,4))+[44,48]: assert u[336+i*64+off:340+i*64+off]==b[352+i*64+off:356+i*64+off]
    for r in n['solve_block']:
        if r['constraint_type']==1:
            assert r['body_a_before']==r['body_a_after'] and r['body_b_before']==r['body_b_after']
            assert not any(r['applied_normal_forces_after']) and not any(r['applied_friction_forces_after'])
    iterations=[]
    for i,(a,b) in enumerate(zip(static,target_solves)):
        ua=a['after']['descs'][target_index]['bodyAWindow']['rawBytes']
        nv=b['body_a_after']['raw_bytes']
        iterations.append(dict(iteration=i+1,unityDeltaVelocity=floats(bytes(ua[:12])),
            nativeDeltaVelocity=b['body_a_after']['linear_velocity'],
            unityAngularState=floats(bytes(ua[16:28])),nativeAngularState=b['body_a_after']['angular_state']))
    mismatches=[dict(physicsTick=k,differences=differences(bounds[k],production['states'][k-1]))
                for k in range(1,3001) if bounds[k]!=production['states'][k-1]]
    assert [r['physicsTick'] for r in mismatches]==[1383]
    evidence=[path,baseline_path,native_path,calls_path,calls_path.with_name('alignment.json'),
        capture/'observer_source.js',capture/'capture_manifest.json',function_path,kernel_path,
        BASE/'native_pcm_cache_clear_step1383_20261002.asm',BASE/'native_pcm_cache_handoff_step1383_20261002.asm',
        BASE/'native_pcm_mesh_step1383_20261002.asm']
    result=dict(sampleId=11009,physicsTick=1383,denseOrdinal=1384,
        hashes=dict(unityWasm=digest(source),patchedWasm=manifest['patchedSha256'],
            nativeModule=calls['moduleSha256'],productionCode=production['sourceSha256']),
        observer=dict(originalFunctionBodiesRetained=True,denseSetterPairsUnchanged=1384,
            resetCoreRowsUnchanged=256,frictionInputsUnchanged=1383,completedBoundaryTicksUnchanged=list(range(1382,1387)),
            nativeObservedTrajectoryUnchanged=3000,protocolResultUnchanged=True),
        firstConfirmedInternalDifference=dict(stage='PxcDiscreteNarrowPhasePCM entry / multi-cache lifecycle',
            nativeParentRva='0x284860',nativeClearRva='0x330f0',nativeClearCallSiteRva='0x28487a',
            nativeClearSizeStoreRva='0x332d1',unityPcmFunction=70030,unityRefreshFunction=69978,
            unityInputCachedSize=304,nativeInputCachedSizeBeforeClear=304,nativeInputCachedSizeAfterClear=0,
            nativeClearCallId=clear['callId'],unityRefreshCallId=refresh[0]['callId']),
        priorCachedContactArithmeticFieldsExact=50,pcmTransformWordsExact=14,
        contactDifferences=contact_differences,normalConstraintDifferences=normal_differences,
        frictionArithmeticFieldsExact=True,originalWasmRefreshReplayExact=True,
        originalWasmRefreshFunctionBodySha256=hashlib.sha256(original[69978-476]).hexdigest(),
        dynamicPairImpulseZeroAllFiveIterations=True,targetStaticIterations=iterations,
        completedStateMismatches=mismatches,mainCompletedStatesExactThroughTick=3000,
        targetCompletedStatesExactAfterDifferenceThroughTick=3000,
        conclusion='The native multi-cache lifecycle clears a preserved target-ice cache at tick 1383. Unity refreshes old cached contacts; native regenerates them. The differing separation values feed five normal-row bias values, then target static-solver outputs and seven completed-state words.',
        productionRepairApplied=False,
        limits=['No claim that every unobserved intermediate before tick 1383 is bitwise identical.',
            'A general replacement of the old unconditional cache-clear hook still requires tracing the actual invalidation/wake branches and regression validation.'],
        evidenceSha256={str(p.relative_to(ROOT)):digest(p) for p in evidence})
    out=BASE/'sample11009_step1383_internals_verified_20261002.json'
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:result[k] for k in ('firstConfirmedInternalDifference','contactDifferences','completedStateMismatches')},indent=2))

if __name__=='__main__': main()
