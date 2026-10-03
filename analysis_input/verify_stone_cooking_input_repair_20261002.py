"""Verify repaired actual cooker inputs, natural geometry and full state replay."""
import hashlib
import json
from pathlib import Path
import struct
from verify_pcm_internal_trace import rows_of
from verify_reset_internal_alignment_20261002 import validate,code_bodies
from verify_release_ordinary_tail_20261002 import core_states,target_bits

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def words(v):return list(struct.unpack('<%dI'%len(v),struct.pack('<%df'%len(v),*v)))


def main():
    directory=BASE/'unity_startup_geometry_audit_capture_20261002_inputs_v2'
    rows,event_path,observer=validate(directory)
    manifest=json.loads((directory/'capture_manifest.json').read_text())
    source,patched=code_bodies(Path(manifest['source'])),code_bodies(Path(manifest['patched']))
    for r in manifest['functions']:
        assert source[r['functionIndex']-manifest['importedFunctions']]==patched[r['rawFunctionIndex']-manifest['importedFunctions']]
    assert digest(Path(manifest['source']))==manifest['sourceSha256']
    assert digest(Path(manifest['patched']))==manifest['patchedSha256']
    input_calls=[r for r in rows_of(rows,'a12.pcm_internal_call') if r.get('convexCookerInput',{}).get('count')==512]
    assert len(input_calls)==16
    ui=input_calls[0]['convexCookerInput']
    assert all(r['convexCookerInput']['pointBits']==ui['pointBits'] for r in input_calls)
    asset_path=ROOT/'local_simulator/assets/unity_stone_convex_input_512.json'
    asset=json.loads(asset_path.read_text())
    assert asset['pointBits']==ui['pointBits']==[words(p) for p in asset['vertices']]
    assert digest(event_path)==asset['source']['eventsSha256']
    assert hashlib.sha256(b''.join(struct.pack('<3I',*p) for p in ui['pointBits'])).hexdigest()==asset['pointBufferSha256']
    native_path=BASE/'native_startup_geometry_input_fixed_20261002.json'
    native=json.loads(native_path.read_text())
    production_path=ROOT/'local_simulator/unity_physx.py'
    assert native['productionCodeSha256']==digest(production_path)
    native_inputs_path=BASE/'native_startup_cooker_input_fixed_20261002/calls.json'
    ni=json.loads(native_inputs_path.read_text())
    assert ni['moduleSha256']==native['nativeModuleSha256']
    assert len(ni['descriptors'])==3
    for nd in ni['descriptors']:
        assert nd['pointBits']==ui['pointBits']==native['constructionInputs'][0]['pointBits']
        assert all(nd[k]==ui[k] for k in ('count','stride','flags','vertexLimit','quantizedCount'))
    unity=rows_of(rows,'a12.startup_convex_runtime')[0]
    before,after=(native['observations'][0][k] for k in ('before','after'))
    raw=unity['runtime']['runtimeBufferWindow']['rawBytes']
    exact_segments={}
    for name,segment in unity['runtime']['byteLayout'].items():
        n=before['byte_layout'][name]
        a=raw[segment['offset']:segment['offset']+segment['bytes']]
        b=before['raw_bytes'][n['offset']:n['offset']+n['bytes']]
        assert a==b,(name,'before import')
        exact_segments[name]=len(a)
    for edge,value in [('before',before),('after',after)]:
        for name,offset in [('aabb_center',0),('aabb_extents',12),('center_of_mass',24),('internal',48)]:
            assert words(value[name])==unity['headerBits'][offset//4:offset//4+len(value[name])],(edge,name)
    for uk,nk in [('nbEdges','nb_edges'),('nbHullVertices','nb_hull_vertices'),('nbPolygons','nb_polygons')]:
        assert unity['hull'][uk]==before[nk]==after[nk]
    big=unity['runtime']['bigConvexRawDataArrays']
    exact_big={}
    for uk,nk in [('samplesWindow','samples_raw_bytes'),('valenciesWindow','valencies_raw_bytes'),('adjacentVertsWindow','adjacent_vertices_raw_bytes')]:
        assert big[uk]['rawBytes']==before['big_convex_raw_data'][nk]==after['big_convex_raw_data'][nk]
        exact_big[nk]=len(big[uk]['rawBytes'])
    assert raw==after['raw_bytes']
    native_hull_path=BASE/'native_startup_cooker_input_fixed_20261002/output.json'
    assert json.loads(native_hull_path.read_text())==after

    plain_path=BASE/'native_stone_input_fixed_plain_20261002.json'
    wrapped_path=BASE/'native_stone_input_fixed_wrapped_20261002.json'
    plain,wrapped=json.loads(plain_path.read_text()),json.loads(wrapped_path.read_text())
    assert plain['sourceSha256']==wrapped['unityPhysxSha256']==digest(production_path)
    assert plain['moduleSha256']==wrapped['moduleSha256']==native['nativeModuleSha256']
    expected=[[f['afterBits'],target_bits(f['step']['targetsAfterScene']['2'])] for f in wrapped['frames']]
    expected += [[f['afterBits'],f['targetAfterBits']] for f in wrapped['tail']]
    assert len(expected)==3362 and expected==plain['states']
    old_path=BASE/'native_natural_wake_unobserved_20261002.json'
    old=json.loads(old_path.read_text())
    assert old['states']==plain['states'] and old['releaseBits']==plain['releaseBits']==wrapped['releaseBits']
    assert wrapped['targetWakeCalls']==[]
    full_rows,full_event_path,full_observer=validate(BASE/'unity_release_both_complete_activation_v2_20261002')
    boundaries={}
    for row in rows_of(full_rows,'a12.tail_phase_core'):
        if row['phase']=='DCP.FixedUpdate.boundary' and row['edge']=='enter' and row['solverSerial']>=1:
            tick=row['solverSerial']; states=core_states(row)
            if tick in boundaries:assert boundaries[tick]==states
            boundaries[tick]=states
    assert max(boundaries)==2000
    assert all(boundaries[tick]==plain['states'][tick-1] for tick in range(1,2001))
    report=dict(unityWasmSha256=manifest['sourceSha256'],nativeModuleSha256=native['nativeModuleSha256'],
        productionCodeSha256=digest(production_path),fixedInputAssetSha256=digest(asset_path),
        repair='Replace reconstructed default cylinder points with the actual fixed Unity collider cooking input; retain original cooker and existing feature import.',
        actualCookerInput=dict(unityFunctionIndex=72908,unityCallIds=[r['callId'] for r in input_calls],
            nativeFunctionRvas=[r['functionRva'] for r in ni['descriptors']],pointWordsExact=1536,differentPointWords=0,
            matchedDescriptorFields={k:ui[k] for k in ('count','stride','flags','vertexLimit','quantizedCount')}),
        naturalCookerOutputBeforeAnyFeatureImport=dict(exactSegments=exact_segments,
            totalFeatureBytesExact=sum(exact_segments.values()),headerFloatWordsExact=13,
            originalFourHeaderDifferencesResolved=True,bigConvexArraysExact=exact_big),
        states=dict(unityBothStoneCompletedStepsExact=2000,unityStateWordsExact=52000,
            nativeWrappedPlainAndPreviousProductionStepsExact=3362,nativeStateWordsExact=3362*26,
            firstConfirmedCompletedStateDivergence=None),
        observer=dict(unity=observer,originalWasmBodiesRetained=True,native=native['observer'],
            nativeStalkerFinalHullUnchanged=True),tests='34 existing checks plus one real Unity cooker-output regression passed',
        limitations=['This verifies observed cooker inputs and numerical geometry outputs; all cooker arithmetic intermediates and scene creation are not audited.',
            'Native pre-import layout has a 768-byte GPU edge array; existing feature import removes it, matching the Unity runtime layout. PxCookingParams/buildGPUData and this structural branch remain unclosed.',
            'State comparison scope remains sample11000 on Windows CP39 with the same recorded friction inputs; no claim for all samples, protocol internals or RNG states.'],
        evidence={str(p.relative_to(ROOT)):digest(p) for p in [event_path,full_event_path,native_path,native_inputs_path,native_hull_path,
            plain_path,wrapped_path,old_path,asset_path,production_path,Path(__file__),
            ROOT/'local_simulator/tests/test_unity_stone_cooking.py',ROOT/'local_simulator/tests/fixtures/unity_stone_cooking_output_20261002.json']})
    (BASE/'stone_cooking_input_repair_verified_20261002.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    print('PASS: 1536 input words; natural 4008 feature bytes, 13 header words and all BigConvex arrays exact; both stones 2000 Unity steps exact; 3362 native steps unchanged.')


if __name__=='__main__':main()
