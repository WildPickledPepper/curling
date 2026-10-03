"""Verify the continuous state prefix and first confirmed release/sliding divergence."""
import hashlib
import json
from pathlib import Path
import struct
from instrument_pcm_calls import Reader, sections, uleb
from verify_pcm_internal_trace import rows_of
from verify_reset_internal_alignment_20261002 import validate, words

ROOT=Path(__file__).resolve().parents[1]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def bodies(path):
    r=Reader(dict(sections(path.read_bytes()))[10])
    return [r.take(r.uint()) for _ in range(r.uint())]

def core_words(c):return words(c['p']+c['q']+c['linearVelocity']+c['angularVelocity'])

def pose_first(core_bits):
    # Observer snapshots are q,p,v,w; native state snapshots are p,q,v,w.
    return core_bits[4:7]+core_bits[:4]+core_bits[7:]

def main():
    directory=ROOT/'analysis_input/unity_first_release_chain_complete_capture_20261002'
    rows,path,validation=validate(directory)
    source=ROOT/'analysis_input/unity_20260930.wasm'
    served=json.loads((path.parent/'pcm_call_trace_wasm.json').read_text())
    manifest_path=directory/'capture_manifest.json'
    manifest=json.loads(manifest_path.read_text())
    assert manifest['patchedSha256']==served['patchedSha256']
    assert manifest['sourceSha256']==served['sourceSha256']
    original=bodies(source)
    patched=bodies(Path(manifest['patched']))
    imports=manifest['importedFunctions']
    selected={r['functionIndex']:r for r in manifest['functions']}
    for function,record in selected.items():
        raw=original[function-imports]
        assert raw==patched[record['rawFunctionIndex']-imports]
        assert hashlib.sha256(raw).hexdigest()==record['originalBodySha256']
    for i,body in enumerate(original):
        if i+imports not in selected:assert body==patched[i]
    assert digest(source)==manifest['sourceSha256']
    assert digest(Path(manifest['patched']))==manifest['patchedSha256']

    untraced_path=ROOT/'analysis_input/native_first_release_chain_untraced_20261002.json'
    traced_path=ROOT/'analysis_input/native_first_release_chain_traced_20261002.json'
    local=json.loads(traced_path.read_text());base=json.loads(untraced_path.read_text())
    for key in ('release','releaseBits','setters','frames'):assert local[key]==base[key],key
    assert local['moduleSha256']=='7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'
    setters=rows_of(rows,'a12.pcm_internal_call')
    linear=[r for r in setters if r['functionIndex']==73034 and r['setterInputBits'][0]!=0]
    angular=[r for r in setters if r['functionIndex']==73035 and r['callId']>linear[0]['callId']]
    local_linear=[r for r in local['setters'] if r['name']=='set_linear_velocity']
    local_angular=[r for r in local['setters'] if r['name']=='set_angular_velocity']
    comparisons=[]
    for label,i in [('release',0),('first sliding tick',1)]:
        for u,n,kind in [(linear[i],local_linear[i],'linear setter'),
                         (angular[i],local_angular[i],'angular setter')]:
            assert pose_first(u['setterCoreBeforeBits'])==n['beforeBits'],(label,kind,'before')
            assert pose_first(u['setterCoreAfterBits'])==n['afterBits'],(label,kind,'after')
            if kind=='linear setter':assert u['setterInputBits']==n['inputBits']
            else:assert u['setterCoreAfterBits'][10:13]==n['inputBits']
            comparisons.append(dict(boundary=label+' '+kind,beforeStateWordsExact=13,
                                    afterStateWordsExact=13,unityCallId=u['callId']))
    assert pose_first(angular[0]['setterCoreAfterBits'])==local['releaseBits']
    # The next setter's raw input state is the previous fetch/writeback output.
    assert pose_first(linear[2]['setterCoreBeforeBits'])==local['frames'][0]['afterBits']
    phases=rows_of(rows,'a12.early_phase_core')
    first_exit=next(r for r in phases if r['ordinal']==2 and r['edge']=='exit'
                    and r['phase']=='PxsDynamics.solverSetupSolve')
    data=local['native'][0]['solver_setup'][-1]['body_data'][0]
    assert words(data['body2world']['p']+data['body2world']['q']+
                 data['linear_velocity']+data['angular_velocity'])==core_words(first_exit['core'])
    u,n=linear[2],local_linear[2]
    assert pose_first(u['setterCoreBeforeBits'])==n['beforeBits']
    differences=[i for i,(a,b) in enumerate(zip(u['setterInputBits'],n['inputBits'])) if a!=b]
    assert differences==[1]
    assert u['setterInputBits'][1]==0 and n['inputBits'][1]==0xbdc8e8a7
    after_diff=[i for i,(a,b) in enumerate(zip(pose_first(u['setterCoreAfterBits']),n['afterBits'])) if a!=b]
    assert after_diff==[8]

    # Resolve the FixedUpdate function from the ORIGINAL binary table segment.
    element=Reader(dict(sections(source.read_bytes()))[9])
    assert element.uint()==1 and element.uint()==0 and element.byte()==0x41
    start=element.uint();assert element.byte()==0x0b
    table=[element.uint() for _ in range(element.uint())]
    assert table[11105-start]==60124 and table[129352-start]==82501
    function=original[60124-imports]
    # local.get 1; i32.const 0; i32.store align=4 offset=124.
    literal_zero=b'\x20\x01\x41\x00\x36\x02'+uleb(124)
    zero_offset=function.find(literal_zero)
    assert zero_offset>=0 and function.count(literal_zero)==1
    next_call=function.find(b'\x10'+uleb(32521),zero_offset)
    assert 0<next_call-zero_offset<64
    # f82501 explicitly calls the observed actual native f73034.
    assert b'\x10'+uleb(73034) in original[82501-imports]
    code=(ROOT/'local_simulator/unity_physx.py').read_text(encoding='utf-8')
    # This verifier replays historical pre-repair captures. The live default
    # can change after the confirmed difference is repaired.
    assert '0.0 if self.custom_sliding_zero_vertical_setter else float(current["vz"])' in code
    report=dict(unityWasmSha256=digest(source),nativeModuleSha256=local['moduleSha256'],
        observer=dict(validation,nativeFirstFourFramesAndSettersUnchanged=True,
                      selectedWasmBodiesByteIdentical=len(selected),unselectedWasmBodiesByteIdentical=True),
        scope='sample 11000, fresh default Windows CP39 scene; controlled recorded friction inputs',
        matchedStateBoundaries=comparisons,
        firstPhysicsSolverExitWordsExact=13,firstPhysicsFetchWritebackWordsExact=13,
        firstConfirmedDivergence=dict(phase='second sliding tick, linear velocity construction/write',
            denseOrdinal=3,releaseSerial=2,unityCallId=u['callId'],unityFunctionIndex=73034,
            unityBeforeStateWordsExact=13,
            unityInputWords=u['setterInputBits'],nativeInputWords=n['inputBits'],
            field='native world-Y linear velocity',unityValue=0.0,
            nativeValue=struct.unpack('<f',struct.pack('<I',n['inputBits'][1]))[0],
            unityHex='0x00000000',nativeHex='0xbdc8e8a7',
            firstChangedStateWordIndex=8),
        mechanism=dict(function=60124,tableIndex=11105,
            functionBodySha256=hashlib.sha256(function).hexdigest(),
            literalZeroStoreBodyByteOffset=zero_offset,velocitySetterCallBodyByteOffset=next_call,
            bytesFromZeroStoreThroughCall=function[zero_offset:next_call+len(b'\x10'+uleb(32521))].hex(),
            observedChain=[60124,32521,82501,73034],
            nativeCause='default custom_sliding_zero_vertical_setter=False retains current vz'),
        historicalPreRepairCapture=True,sourceSha256AtNativeCapture=local['unityPhysxSha256'],
        productionCodeChangedSinceCapture=digest(ROOT/'local_simulator/unity_physx.py')!=local['unityPhysxSha256'],
        limitations=['State words and sampled setter boundaries verified; not every f64 sliding arithmetic intermediate audited.',
                     'Later frames are outside the continuous prefix once second-tick velocity diverges.',
                     'Friction draws were controlled identically; this does not close Unity RNG state generation.'],
        evidence={str(p.relative_to(ROOT)):digest(p) for p in [path,manifest_path,
                    directory/'observer_source.js',traced_path,untraced_path,
                    ROOT/'local_simulator/unity_physx.py',
                    ROOT/'analysis_input/pcm_functions_20261001/f60124.wat',
                    ROOT/'analysis_input/pcm_functions_20261001/f82501.wat',
                    ROOT/'analysis_input/pcm_functions_20261001/f73034.wat']})
    out=ROOT/'analysis_input/first_release_chain_verified_20261002.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print('PASS: release and first sliding/physics state boundaries exact.')
    print('First confirmed divergence: second sliding tick, vertical linear setter 00000000 vs bdc8e8a7.')

if __name__=='__main__':main()
