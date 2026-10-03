"""Verify the actual cosf branch, original Wasm arithmetic and step-313 effect."""
import hashlib
import json
from pathlib import Path
import re
import struct

import pefile
import wasmtime

import validate_multiple_cases_20261002 as validation
from verify_pcm_internal_trace import raw_argument
from replay_integrate_wat_stages_20261003 import replay,bits

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
WORK=BASE/'additional_case_validation_20261002'


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def xmm(row,register):return struct.unpack_from('<f',bytes.fromhex(row['xmmHex']),register*16)[0]


def main():
    v=validation
    focused=BASE/'case12009_step313_unity_integrate_20261003'
    manifest_path=focused/'capture_manifest.json'
    manifest=json.loads(manifest_path.read_text())
    events=v.event_path(focused)
    baseline_events=v.event_path(WORK/'additional12009_unity')
    native_path=WORK/'additional12009_native_sliding_only.json'
    observer=v.observer_check(focused,WORK/'additional12009_original_control',manifest,native_path)
    def boundaries(path):
        return {r['solverSerial']:[v.pose_first(next(c for c in r['cores'] if c['corePtr']==r['mainCorePtr'])['bits']),
            v.pose_first(next(c for c in r['cores'] if c['corePtr']!=r['mainCorePtr'])['bits'])]
            for r in v.rows(path,'a12.tail_phase_core') if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter'}
    observed,baseline=boundaries(events),boundaries(baseline_events)
    assert observed==baseline and sorted(observed)==list(range(4001))
    calls=list(v.rows(events,'a12.pcm_internal_call'))
    cos=next(r for r in calls if r['functionIndex']==33062)
    sin=next(r for r in calls if r['functionIndex']==18890)
    integral=next(r for r in calls if r['callId']==cos['parentCallId'])
    assert integral['functionIndex']==71198 and integral['ordinal']==314
    assert sin['parentCallId']==integral['callId']
    trace_dir=BASE/'case12009_step313_native_registers_v5_20261003'
    native_trace_path=trace_dir/'calls.json'
    n=json.loads(native_trace_path.read_text())
    assert not n['dropped'] and not n['unfinished'] and not n['unhookedTargets']
    assert len(n['calls'])==18
    by={r['functionRva']:r for r in n['calls']}
    local=json.loads((trace_dir/'alignment.json').read_text())
    unobserved=json.loads(native_path.read_text())
    assert local['states']==unobserved['states'][:3000] and local['releaseBits']==unobserved['releaseBits']
    entry=by['0x2049c7']
    unity_body=raw_argument(integral,3,'before')[:112]
    native_body=bytes.fromhex(entry['bodyDataHex'])
    different_words=[i for i,(a,b) in enumerate(zip(struct.unpack('<28I',unity_body),struct.unpack('<28I',native_body))) if a!=b]
    assert different_words==[18] # Actor roster integer at byte offset 72.
    for argument,native_offset in ((0,0),(1,16)):
        assert raw_argument(integral,argument,'before')[:12]==bytes.fromhex(entry['solverBodyHex'])[native_offset:native_offset+12]
    for offset in (0,4,8,16,20,24):
        assert raw_argument(integral,2,'before')[offset:offset+4]==bytes.fromhex(entry['motionBodyHex'])[offset:offset+4]
    theta=cos['args'][0]
    assert bits(theta)==bits(sin['args'][0])==bits(xmm(by['0x204cc3'],15))==0x3bd59dea
    assert bits(sin['result'])==bits(xmm(by['0x204ccc'],0))==0x3bd59d87
    assert bits(cos['result'])==0x3f7ffe9c
    assert bits(xmm(by['0x204d1b'],0))==bits(xmm(by['0xa7855'],0))==0x3f7ffe9b
    assert bits(xmm(by['0xa77e0'],0))==0x3bd59dea
    native_double=struct.unpack_from('<d',bytes.fromhex(by['0xa7851']['xmmHex']))[0]
    assert native_double==1.0-.5*theta*theta
    crt=Path(next(r for r in n['module']['trigImports'] if r['name']=='cosf')['implementationModule'])
    pe=pefile.PE(str(crt))
    for imp in n['module']['trigImports']:
        assert bytes.fromhex(imp['runtimeCodeHex'])==pe.get_data(int(imp['implementationRva'],16),256)
    # Original cosine kernel, with one passive store before f32 demotion.
    cosine_path=BASE/'pcm_functions_20261001/f18889.wat'
    original=re.sub(r'\(type \$t\d+\)','',cosine_path.read_text(),count=1)
    marked=original.replace('(local $l1 f64)','(local $l1 f64) (local $probe f64)')
    marked=marked.replace('    f32.demote_f64','    local.tee $probe\n    i32.const 1024\n    local.get $probe\n    f64.store\n    f32.demote_f64')
    def cosine_kernel(body):
        engine=wasmtime.Engine();store=wasmtime.Store(engine)
        kernel=wasmtime.wat2wasm('(module (memory (export "memory") 1) '+body+' (export "cos" (func $f18889)))')
        instance=wasmtime.Instance(store,wasmtime.Module(engine,kernel),[])
        value=instance.exports(store)['cos'](store,theta)
        pre=struct.unpack('<d',instance.exports(store)['memory'].read(store,1024,1032))[0]
        return value,pre,kernel
    value,_,plain_cos=cosine_kernel(original)
    traced,unity_double,marked_cos=cosine_kernel(marked)
    assert bits(value)==bits(traced)==bits(cos['result'])
    (BASE/'case12009_cos_original_kernel_20261003.wasm').write_bytes(plain_cos)
    (BASE/'case12009_cos_traced_kernel_20261003.wasm').write_bytes(marked_cos)
    lower,upper=(struct.unpack('<f',struct.pack('<I',word))[0] for word in (0x3f7ffe9b,0x3f7ffe9c))
    midpoint=(lower+upper)/2
    assert native_double<midpoint<unity_double
    # Reexecute the verbatim original integrateCore function on its actual inputs.
    solver=raw_argument(integral,0,'before')[:32]
    motion=raw_argument(integral,2,'before')[:32]
    dt=integral['args'][4]
    full,plain,traced_kernel=replay(unity_body,solver,motion,sin['result'],cos['result'],dt)
    assert bytes.fromhex(full['outputHex'])==raw_argument(integral,3,'after')[:112]
    native_cos,_,_=replay(unity_body,solver,motion,sin['result'],xmm(by['0x204d1b'],0),dt)
    diagnostic=bytes.fromhex(native_cos['outputHex']);native_final=bytes.fromhex(by['0x204e02']['bodyDataHex'])
    assert diagnostic[:72]+diagnostic[76:]==native_final[:72]+native_final[76:]
    (BASE/'case12009_integrate_unity_original_20261003.wasm').write_bytes(plain)
    (BASE/'case12009_integrate_unity_traced_20261003.wasm').write_bytes(traced_kernel)
    stages=[dict(watLine=a['originalWatLine'],instruction=a['instruction'],
        unityBits=a['resultBits'],nativeCosReplayBits=b['resultBits'])
        for a,b in zip(full['stages'],native_cos['stages']) if a['resultBits']!=b['resultBits']]
    assert stages[0]['instruction']=='call $f33062'
    stage_path=BASE/'case12009_cos_causal_stages_20261003.json'
    stage_path.write_text(json.dumps(dict(unity=full,nativeCosDiagnostic=native_cos,differingStages=stages),indent=2),encoding='utf8')
    original_wasm=BASE/'unity_20260930.wasm'
    binary=ROOT/'local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd'
    assert digest(binary)==n['moduleSha256']==unobserved['moduleSha256']
    assert digest(ROOT/'local_simulator/unity_physx.py')==unobserved['sourceSha256']
    evidence=[events,baseline_events,native_trace_path,trace_dir/'alignment.json',manifest_path,
        original_wasm,binary,crt,cosine_path,BASE/'pcm_functions_20261001/f33062.wat',
        BASE/'pcm_functions_20261001/f71198.wat',BASE/'case12009_ucrt_cosf_small_disassembly_20261003.txt',
        BASE/'case12009_integrate_disassembly_20261003.txt',stage_path,Path(__file__),
        BASE/'trace_native_integrate_registers_20261003.js',BASE/'capture_case12009_integrate_20261003.py']
    result=dict(sampleId=12009,physicsTick=313,integrateSetterOrdinal=314,
        firstConfirmedInternalDifference=dict(stage='integrateCore -> cosine return',
            unityFunctionIndex=33062,unityCosKernelFunctionIndex=18889,unityIntegrateFunctionIndex=71198,
            unityCallId=cos['callId'],unityIntegrateCallId=integral['callId'],
            nativeIntegrateCosCallRva='0x204d16',nativeCosImportThunkRva='0x450480',
            nativeCosImplementation=str(crt),nativeCosEntryRva='0xa77e0',
            observedNativeBranchRvas=['0xa7840','0xa7848','0xa7851','0xa7855'],
            inputBits='0x3bd59dea',unityResultBits='0x3f7ffe9c',nativeResultBits='0x3f7ffe9b',
            nativeObservedCalculation='f64 promotion; multiply by 0.5; fused 1 - (x/2)*x; demote to f32',
            unityObservedCalculation='f33062 small-angle branch -> original f18889 double polynomial -> f32 demotion'),
        sineInputAndReturnByteIdentical=True,integrateBodyDataWordsExactExcludingRosterInteger=27,
        solverDeltaAndMotionDeltaFloatWordsExact=12,
        rounding=dict(nativePreDemoteDouble=native_double,unityPreDemoteDouble=unity_double,
            float32Midpoint=midpoint,nativeMinusMidpoint=native_double-midpoint,unityMinusMidpoint=unity_double-midpoint),
        actualUnityIntegrateOutputBytesReproduced=112,
        nativeCosDiagnosticReproducesAllNativeIntegrateOutputExceptRosterInteger=True,
        differingWatStages=stages,observer=dict(observer,completedBoundaryBytesUnchanged=4001*104,
            nativeObservedStepsUnchanged=3000,nativeInstructionSnapshots=18),
        productionCodeChanged=False,nativeModuleChanged=False,
        productionSourceSha256=unobserved['sourceSha256'],nativeModuleSha256=n['moduleSha256'],
        originalWasmSha256=digest(original_wasm),ucrtBaseSha256=digest(crt),
        limits=['Diagnosis uses the exact observed small-angle path on this Windows runtime.',
                'No production cosine replacement or full-trajectory repair has been made.',
                'The separate 12000 external cleanup boundary is not diagnosed by this report.'],
        evidenceSha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):digest(p) for p in evidence})
    target=BASE/'case12009_cos_cause_verified_20261003.json'
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:result[k] for k in ('sampleId','physicsTick','firstConfirmedInternalDifference','rounding',
        'actualUnityIntegrateOutputBytesReproduced','nativeCosDiagnosticReproducesAllNativeIntegrateOutputExceptRosterInteger',
        'productionCodeChanged')},ensure_ascii=False))


if __name__=='__main__':main()
