"""Validate actual release arithmetic and compare repaired normal replays."""
import hashlib
import json
import struct
from pathlib import Path
from verify_pcm_internal_trace import events, rows_of, raw_argument
from verify_release_ordinary_tail_20261002 import core_states
from verify_reset_internal_alignment_20261002 import code_bodies
from verify_new_sample_11009_20261002 import differences

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'analysis_input'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    trace_dir=BASE/'unity_bestshot_position_inputs_capture_v5_20261002'
    trace,trace_path=events(trace_dir)
    original,original_path=events(BASE/'unity_new_sample_11009_capture_20261002')
    calls=rows_of(trace,'a12.pcm_internal_call')
    setter=next(r for r in calls if r['functionIndex']==32546
        and struct.unpack_from('<I',raw_argument(r,1,'before'),8)[0]==0x4257e5c9)
    release=next(r for r in calls if r['callId']==setter['parentCallId'])
    assert release['functionIndex']==61066
    getter=next(r for r in calls if r['functionIndex']==32544 and r['parentCallId']==release['callId'])
    input_bits=list(struct.unpack_from('<3I',raw_argument(getter,0,'after')))
    output_bits=list(struct.unpack_from('<3I',raw_argument(setter,1,'before')))
    assert input_bits[:2]==output_bits[:2]
    assert input_bits[2]==0x4258b296 and output_bits[2]==0x4257e5c9
    parse=next(r for r in calls if r['functionIndex']==56989 and r['parentCallId']==release['callId']
        and struct.unpack_from('<I',raw_argument(r,1,'after'))[0]==0x3e4ccccd)
    offset_bits=struct.unpack_from('<I',raw_argument(parse,1,'after'))[0]
    assert offset_bits==0x3e4ccccd
    parse_input=raw_argument(parse,0,'before')
    string_length=struct.unpack_from('<I',parse_input,8)[0]
    assert parse_input[12:12+string_length*2].decode('utf-16-le')=='0.2'
    assert not [r for r in trace if 'failed' in r['type'] or 'exhausted' in r['type']]
    assert [r['value'] for r in rows_of(trace,'sliding.random_range.friction')] == [r['lastFrictionNoise'] for r in rows_of(original,'a12.dense_pre_angular_setter')[1:]]
    sample=lambda directory:json.loads(next(directory.glob('*.jsonl')).read_text().splitlines()[0])
    a,b=sample(trace_dir),sample(BASE/'unity_new_sample_11009_capture_20261002')
    for k in ('requested','after_position','final_xy','target_moves','collision_observed'): assert a[k]==b[k]
    for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
        a,b=rows_of(trace,kind),rows_of(original,kind)
        assert len(a)==len(b)==1384
        pack=lambda v:struct.pack('<%df'%len(v),*v)
        for x,y in zip(a,b):
            for k in ('getterLinear','getterAngular','setterAngular','bridge164','bridge300'):
                if x.get(k) is not None: assert pack(x[k])==pack(y[k])
            if x.get('pose') is not None: assert pack(x['pose']['p']+x['pose']['q'])==pack(y['pose']['p']+y['pose']['q'])
    manifest_path=BASE/'unity_bestshot_position_inputs_v5_20261002.json'
    manifest=json.loads(manifest_path.read_text())
    wasm=BASE/'unity_20260930.wasm'
    assert digest(wasm)==manifest['sourceSha256']
    assert digest(Path(manifest['patched']))==manifest['patchedSha256']
    bodies,patched=code_bodies(wasm),code_bodies(Path(manifest['patched']))
    for r in manifest['functions']:
        assert bodies[r['functionIndex']-manifest['importedFunctions']]==patched[r['rawFunctionIndex']-manifest['importedFunctions']]
    native_path=BASE/'native_bestshot_offset_fixed_11009_20261002.json'
    native=json.loads(native_path.read_text())
    assert native['sourceSha256']==digest(ROOT/'local_simulator/unity_physx.py')
    bounds={r['solverSerial']:core_states(r) for r in rows_of(original,'a12.tail_phase_core')
            if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter'}
    assert sorted(bounds)==list(range(3001))
    assert native['releaseBits']==bounds[0]
    mismatches=[dict(physicsTick=k,differences=differences(bounds[k],native['states'][k-1])) for k in range(1,3001)
                if bounds[k]!=native['states'][k-1]]
    old_path=BASE/'native_bestshot_offset_fixed_11000_20261002.json'
    old=json.loads(old_path.read_text())
    assert old['sourceSha256']==native['sourceSha256']
    assert old['moduleSha256']==native['moduleSha256']
    baseline_path=BASE/'native_stone_input_fixed_plain_20261002.json'
    baseline=json.loads(baseline_path.read_text())
    assert old['releaseBits']==baseline['releaseBits'] and old['states']==baseline['states']
    old_unity,old_unity_path=events(BASE/'unity_release_both_complete_activation_v2_20261002')
    old_boundaries={r['solverSerial']:core_states(r) for r in rows_of(old_unity,'a12.tail_phase_core')
        if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter' and r['solverSerial']>=1}
    assert all(old_boundaries[k]==old['states'][k-1] for k in range(1,2001))
    report=dict(unityWasmSha256=digest(wasm),productionCodeSha256=native['sourceSha256'],nativeModuleSha256=native['moduleSha256'],
        actualArithmetic=dict(functionIndex=release['functionIndex'],callId=release['callId'],getterFunctionIndex=32544,getterCallId=getter['callId'],
            setterFunctionIndex=32546,setterCallId=setter['callId'],getterPositionBits=[hex(v) for v in input_bits],
            horizontalOffsetBits=hex(offset_bits),parseFunctionIndex=56989,parseCallId=parse['callId'],
            setterPositionBits=[hex(v) for v in output_bits],operation='native float32 position.z minus parsed float32 horizontal offset'),
        observer=dict(originalBodiesRetained=True,setterPairsUnchanged=1384,protocolResultsUnchanged=True),
        sample11009=dict(releaseWordsExact=26,completedStepsCompared=3000,
            continuousCompletedStepsExact=mismatches[0]['physicsTick']-1 if mismatches else 3000,
            firstObservedRemainingStateDifference=mismatches[0] if mismatches else None,
            differingCompletedSteps=len(mismatches),firstContactTick=native['stoneContactTicks'][0]),
        sample11000=dict(nativeRegressionStepsUnchanged=3362,unityCompletedStepsExact=2000),
        limitations=['State equality at sampled boundaries does not prove every unobserved intermediate/RNG/protocol operation.',
            'New case remains limited to fresh sample11009; old case to fresh sample11000; Windows CP39.'],
        evidence={str(p.relative_to(ROOT)):digest(p) for p in (trace_path,original_path,old_unity_path,
            native_path,old_path,baseline_path,manifest_path,BASE/f"pcm_functions_20261001/f{release['functionIndex']}.wat",
            trace_dir/'observer_source.js',
            ROOT/'local_simulator/tests/fixtures/unity_bestshot_offset_11009_20261002.json')})
    out=BASE/'bestshot_offset_repair_verified_20261002.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:report[k] for k in ('actualArithmetic','sample11009','sample11000')},indent=2,ensure_ascii=False))


if __name__=='__main__':main()
