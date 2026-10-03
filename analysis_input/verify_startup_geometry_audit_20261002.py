"""Audit current runtime convex buffers without inferring cooker equality."""
import hashlib
import argparse
import json
import struct
from pathlib import Path
from verify_reset_internal_alignment_20261002 import validate, code_bodies
from verify_pcm_internal_trace import rows_of

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'analysis_input'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(values):
    return list(struct.unpack('<%dI' % len(values), struct.pack('<%df' % len(values), *values)))


def byte_compare(a, b):
    first = next((dict(offset=i, unityByte=x, nativeByte=y)
                  for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    if first is None and len(a) != len(b):
        first = dict(offset=min(len(a), len(b)), unityLength=len(a), nativeLength=len(b))
    return dict(unityBytes=len(a), nativeBytes=len(b), exact=a == b,
                differingBytes=sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b)),
                firstDifference=first)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--suffix', default='')
    opts=parser.parse_args()
    assert opts.suffix in ('','_inputs_v2')
    directory = BASE / ('unity_startup_geometry_audit_capture_20261002' + opts.suffix)
    rows, event_path, checks = validate(directory)
    manifest = json.loads((directory / 'capture_manifest.json').read_text())
    original, patched = code_bodies(Path(manifest['source'])), code_bodies(Path(manifest['patched']))
    for r in manifest['functions']:
        assert original[r['functionIndex'] - manifest['importedFunctions']] == patched[r['rawFunctionIndex'] - manifest['importedFunctions']]
    assert digest(Path(manifest['source'])) == manifest['sourceSha256']
    assert digest(Path(manifest['patched'])) == manifest['patchedSha256']
    runtime_rows = rows_of(rows, 'a12.startup_convex_runtime')
    assert len(runtime_rows) == 1 and runtime_rows[0]['resetPhysicsStep'] == 1
    unity = runtime_rows[0]
    baseline_rows, _, _ = validate(BASE / 'unity_release_both_complete_activation_v2_20261002')
    # The release-setter manifest additionally records two bridge input vectors.
    # This startup manifest does not enable that observer; compare all shared
    # dense physical fields without treating absent optional metadata as a value.
    strip=lambda r:{k:v for k,v in r.items() if k not in ('nativePtr','bridgePtr','tickSerial','bridge164Bits','bridge300Bits')}
    for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
        assert [strip(r) for r in rows_of(rows,kind)] == [strip(r) for r in rows_of(baseline_rows,kind)]
    native_path = BASE / 'native_startup_geometry_audit_20261002.json'
    native = json.loads(native_path.read_text())
    assert native['productionCodeSha256'] == digest(ROOT / 'local_simulator/unity_physx.py')
    assert native['samplerSha256'] == digest(BASE / 'sample_startup_geometry_audit_20261002.py')
    observation = native['observations'][0]
    raw = unity['runtime']['runtimeBufferWindow']['rawBytes']
    asset = ROOT / 'local_simulator/assets/unity_runtime_hull.json'
    assert raw == json.loads(asset.read_text())['hull_raw_bytes']
    before, after = observation['before'], observation['after']
    assert raw == after['raw_bytes']
    headers = []
    for uk, nk, offset in [('aabbCenter','aabb_center',0), ('aabbExtents','aabb_extents',12),
                           ('centerOfMass','center_of_mass',24), ('internal','internal',48)]:
        u, n = unity['headerBits'][offset // 4:offset // 4 + len(after[nk])], words(after[nk])
        assert u == words(unity['hull'][uk])
        headers.append(dict(field=uk, unityOffset=offset, unityBits=u, nativeBits=n, exact=u == n,
                            differences=[dict(component=i, unityBits=hex(x), nativeBits=hex(y))
                                         for i, (x, y) in enumerate(zip(u,n)) if x != y]))
    big = unity['runtime']['bigConvexRawDataArrays']
    arrays = {}
    for uk, nk in [('samplesWindow','samples_raw_bytes'), ('valenciesWindow','valencies_raw_bytes'),
                   ('adjacentVertsWindow','adjacent_vertices_raw_bytes')]:
        arrays[nk] = byte_compare(big[uk]['rawBytes'], after['big_convex_raw_data'][nk])
    cooker_calls = [r for r in rows_of(rows,'a12.pcm_internal_call') if r['functionIndex'] in (72908,72910,72915)]
    cooked = [r for r in cooker_calls if r.get('cookedHullDesc',{}).get('ok')]
    formal_cooks = [r for r in cooked if r['cookedHullDesc']['header']['points']['count'] == 128
                    and r['cookedHullDesc']['header']['polygons']['count'] == 66]
    assert len(formal_cooks) == 16
    first_desc = formal_cooks[0]['cookedHullDesc']
    assert all(r['cookedHullDesc']['raw'] == first_desc['raw'] for r in formal_cooks)
    unity_vertices = bytes(first_desc['raw']['pointsBytes'])
    native_vertices = struct.pack('<%df' % (3 * len(before['hull_vertices'])),
                                  *(v for p in before['hull_vertices'] for v in p))
    planes = []
    for i, (u,n) in enumerate(zip(first_desc['polygons'], before['polygons'])):
        uw, nw = words(u['plane']), words(n['plane'])
        if uw != nw:
            planes.append(dict(polygonIndex=i, unityPlaneBits=uw, nativePlaneBits=nw))
    cooking_summary = [dict(callId=r['callId'], parentCallId=r['parentCallId'],
                            releaseSerial=r.get('releaseSerial'),
                            points=r['cookedHullDesc']['header']['points']['count'],
                            polygons=r['cookedHullDesc']['header']['polygons']['count']) for r in cooked]
    differences = [h for h in headers if not h['exact']]
    cooker_input=None
    additional_evidence=[]
    if opts.suffix:
        inputs=[r for r in cooker_calls if r.get('convexCookerInput',{}).get('count')==512]
        assert len(inputs)==16
        ui=inputs[0]['convexCookerInput']
        assert all(r['convexCookerInput']['pointBits']==ui['pointBits'] for r in inputs)
        input_path=BASE/'native_startup_cooker_inputs_20261002/calls.json'
        ni=json.loads(input_path.read_text())
        assert ni['moduleSha256']==native['nativeModuleSha256']
        assert len(ni['descriptors'])==3
        nd=ni['descriptors'][0]
        binding_input=native['constructionInputs'][0]
        assert all(r['pointBits']==binding_input['pointBits'] for r in ni['descriptors'])
        assert all(r['pointBits']==nd['pointBits'] for r in ni['descriptors'])
        assert all(ui[k]==nd[k] for k in ('count','stride','flags','vertexLimit','quantizedCount'))
        point_differences=[dict(vertex=i,component=j,unityBits=hex(a),nativeBits=hex(b))
                           for i,(u,n) in enumerate(zip(ui['pointBits'],nd['pointBits']))
                           for j,(a,b) in enumerate(zip(u,n)) if a!=b]
        assert point_differences[0]==dict(vertex=0,component=0,unityBits='0x0',nativeBits='0x3fa00000')
        output_path=BASE/'native_startup_cooker_inputs_20261002/output.json'
        assert json.loads(output_path.read_text())==after
        cooker_input=dict(unityFunctionIndex=72908, unityCallIds=[r['callId'] for r in inputs],
            nativeFunctionRvas=[r['functionRva'] for r in ni['descriptors']],
            matchedDescriptorFields={k:ui[k] for k in ('count','stride','flags','vertexLimit','quantizedCount')},
            all16UnityInputsBitIdentical=True, actualNativeDescriptorsMatchPythonBindingInputs=True,
            totalPointWords=1536,differentPointWords=len(point_differences),
            firstDifferentPointWord=point_differences[0],
            firstUnityPointBits=ui['pointBits'][0],firstNativePointBits=nd['pointBits'][0],
            nativeInputSource='local_simulator/assets/stone_extendedcollider_mesh_256.json -> _formal_stone_points -> Y-up conversion -> pybind -> actual PxConvexMeshDesc',
            nativeObserverFinalHullUnchanged=True)
        additional_evidence=[input_path,output_path,BASE/'capture_native_startup_cooker_20261002.py',
            BASE/'sample_native_startup_cooker_20261002.py',BASE/'trace_startup_cooker_inputs_20261002.js',
            ROOT/'local_simulator/assets/stone_extendedcollider_mesh_256.json',BASE/'pcm_functions_20261001/f72908.wat',
            BASE/'native_cooker_input_entry_disassembly_20261002.json']
    report = dict(unityWasmSha256=manifest['sourceSha256'], patchedWasmSha256=manifest['patchedSha256'],
                  nativeModuleSha256=native['nativeModuleSha256'], productionCodeSha256=native['productionCodeSha256'],
                  comparisonBoundary='Actual convex runtime input at first Reset step; native default post-import initialization',
                  actualCookerInput=cooker_input,
                  unityFunctionTableIndex=120119, unityResetSerial=unity['resetSerial'], unityResetPhysicsStep=1,
                  cookedHullBeforeImport=byte_compare(raw,before['raw_bytes']),
                  actualFormalCookerOutput=dict(unityFunctionIndex=72915, unityCallIds=[r['callId'] for r in formal_cooks],
                      all16OutputsByteIdentical=True, vertexBuffer=byte_compare(unity_vertices,native_vertices),
                      firstUnityVertexBits=words(first_desc['vertices'][0]),
                      firstNativeVertexBits=words(before['hull_vertices'][0]),
                      firstDifferentPolygonPlane=next(iter(planes),None), differingPolygonPlanes=len(planes)),
                  hullAfterImport=byte_compare(raw,after['raw_bytes']),
                  headerFields=headers, bigConvexArrays=arrays,
                  firstObservedSurvivingGeometryHeaderDifference=next(iter(differences),None),
                  observedCookedDescCalls=cooking_summary,
                  observer=dict(checks, originalFunctionBodiesRetained=True, densePairsUnchanged=1563, native=native['observer']),
                  scope='Same actual Unity binary, fresh default Windows CP39 startup, first Reset sample11000; fixed geometry asset import is explicit.',
                  limitations=['Earliest global calculation divergence is not yet established: scene creation and earlier cooker/load calls are not exhaustively compared.',
                               'Importing captured hull bytes does not verify original cooker internal inputs/branches/intermediates.',
                               'A geometry header difference does not imply a completed-step state difference in the previously verified trajectory.'],
                  evidence={str(p.relative_to(ROOT)):digest(p) for p in [event_path,native_path,asset,
                            directory/'capture_manifest.json',directory/'observer_source.js',
                            BASE/'verify_startup_geometry_audit_20261002.py',BASE/'sample_startup_geometry_audit_20261002.py',
                            BASE/'pcm_functions_20261001/f72915.wat'] + additional_evidence})
    output = BASE / ('startup_geometry_audit_verified_20261002' + opts.suffix + '.json')
    output.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    print('AUDIT: convex extra buffer %d bytes exact after import; differing header fields %s; BigConvex %s.' %
          (len(raw),[h['field'] for h in differences],{k:v['exact'] for k,v in arrays.items()}))
    if cooker_input:print('Actual cooker input: 1020/1536 point words differ, first at vertex0 X; descriptor count/stride/flags/limits exact.')


if __name__ == '__main__':
    main()
