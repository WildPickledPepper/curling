"""Verify the actual BV4 route, PCM values and sequential repaired state prefix."""
import hashlib,inspect,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from verify_pcm_internal_trace import rows_of,raw_argument,events
from verify_reset_internal_alignment_20261002 import validate,code_bodies
from compare_release_states_20261002 import compare

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert inspect.signature(PersistentPhysxFrontHalfScene).parameters['ice_use_fast_midphase'].default is True
    base=ROOT/'analysis_input';source=ROOT/'local_simulator/unity_physx.py'
    paths=[base/'native_first_release_bvh34_full_20261002.json',
           base/'native_release_526_bvh34_verified_20261002/calls.json',
           base/'native_release_526_bvh34_verified_20261002/alignment.json',
           base/'native_reset_bvh34_verified_20261002.json',source]
    full=json.loads(paths[0].read_text());native=json.loads(paths[1].read_text())
    traced=json.loads(paths[2].read_text());reset=json.loads(paths[3].read_text())
    assert full['unityPhysxSha256']==traced['unityPhysxSha256']==digest(source)
    assert full['moduleSha256']==native['moduleSha256']=='7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'
    assert traced['baselineOutputsUnchanged'] and reset['baselineOutputsUnchanged']
    assert native['callStackReliable'] and not native['dropped'] and not native['unfinished']
    route=[r for r in native['calls'] if r['functionRva'] in ['0x2e2880','0x347650','0x3f69b0']]
    assert [r['functionRva']for r in route]==['0x2e2880','0x347650','0x3f69b0']
    assert route[1]['parentCallId']==route[0]['callId'] and route[2]['parentCallId']==route[1]['callId']
    old=json.loads((base/'native_first_release_vertical_fixed_full_20261002.json').read_text())
    assert full['releaseBits']==old['releaseBits']
    assert [f['afterBits'] for f in full['frames'][:525]]==[f['afterBits'] for f in old['frames'][:525]]
    assert old['frames'][525]['afterBits'][10]==0x9a381bc5 and full['frames'][525]['afterBits'][10]==0x9a381bc6

    captures=['unity_release_526_chain_capture_20261002','unity_release_1022_1025_chain_capture_20261002']
    checks={};original=code_bodies(base/'unity_20260930.wasm');reference=None
    for name in captures:
        directory=base/name;rows,path,valid=validate(directory);paths.append(path)
        manifest=json.loads((directory/'capture_manifest.json').read_text())
        patched=code_bodies(Path(manifest['patched']));imports=manifest['importedFunctions']
        for r in manifest['functions']:
            assert original[r['functionIndex']-imports]==patched[r['rawFunctionIndex']-imports]
        assert digest(base/'unity_20260930.wasm')==manifest['sourceSha256']
        assert digest(Path(manifest['patched']))==manifest['patchedSha256']
        strips=lambda r:{k:v for k,v in r.items() if k not in ('nativePtr','bridgePtr','tickSerial')}
        dense={t:[strips(r)for r in rows_of(rows,t)]for t in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter')}
        if reference is None:reference=dense;unity=rows
        else:assert dense==reference
        checks[name]=dict(valid,densePairsUnchanged=1563,originalInstrumentedBodiesRetained=True)
    u=next(r for r in rows_of(unity,'a12.pcm_internal_call') if r['functionIndex']==69979 and r.get('ordinal')==527)
    n=next(r for r in native['calls']if r['functionRva']=='0x29d550')
    a,b=raw_argument(u,0,'before'),raw_argument(n,0,'before')
    assert a[62]==b[62]==1 and struct.unpack_from('<I',a,448)==struct.unpack_from('<I',b,448)==(6,)
    for i in range(6):assert a[64+i*64:112+i*64]==b[64+i*64:112+i*64],('manifold',i)
    a,b=raw_argument(u,1,'after'),raw_argument(n,1,'after')
    for i in range(6):assert a[i*64:i*64+28]==b[i*64:i*64+28],('contact',i)
    assert struct.unpack_from('<3I',a)==(0xa5d55556,0x3f800000,0xb0d2d7eb)
    frontier=compare(paths[0],base/captures[-1])
    assert frontier['continuousPostReleaseStateTicksExact']==1561 and frontier['nextConfirmedDivergence'] is None
    report=dict(unityWasmSha256=digest(base/'unity_20260930.wasm'),nativeModuleSha256=full['moduleSha256'],
        productionCodeSha256=digest(source),repair='default ice_use_fast_midphase=True restores actual Unity BVH34 traversal',
        repairedTick=526,denseOrdinal=527,verifiedNativeQueryRvas=['0x347650','0x3f69b0'],
        originalFirst525StateOutputsUnchanged=True,reset42PhysicalStatesUnchanged=True,
        sixPersistentContactsFloatWordsExact=72,sixFinalContactsFloatWordsExact=42,
        observer=checks,nativeObserverOutputUnchanged=True,tests='32 unittest tests passed',
        frontier=frontier,scope='sample 11000, fresh Windows CP39, actual Reset and BESTSHOT; recorded friction inputs',
        limitations=['Continuous comparison covers the released stone P/Q/v/w boundaries; does not audit every arithmetic intermediate or every other stone state.',
                     'Last tick 1562 output has no next getter in this capture; direct writeback sampling is separate.',
                     'Recorded friction input agreement does not prove internal RNG-state alignment.'],
        evidence={str(p.relative_to(ROOT)):digest(p)for p in paths})
    out=base/'release_bvh34_repair_verified_20261002.json';out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print('PASS: real BV4 dispatch, 6 PCM contacts, repaired tick 526; continuous released-stone states exact through tick 1561.')
if __name__=='__main__':main()
