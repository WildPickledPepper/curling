"""Audit startup before accepting any release-to-collision bit-exact prefix.

Compare mapped numerical fields, never allocator addresses, padding, or two
different platform ABIs as whole byte buffers. Report uncovered boundaries.
"""
import hashlib
import json
from pathlib import Path
import struct

from verify_pcm_internal_trace import events, rows_of
from verify_11005_angular_gap_20261002 import unchanged
from instrument_pcm_calls import Reader, sections

ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bits(v):
    return list(struct.unpack('<%dI' % len(v), struct.pack('<%df' % len(v), *v)))


def memory(call, edge, argument):
    return bytes.fromhex(next(s['hex'] for s in call[edge] if s['argument'] == argument))


def word_comparison(u, n):
    return {'unityBits': '0x%08x' % u, 'nativeBits': '0x%08x' % n, 'equal': u == n,
            'unityValue': struct.unpack('<f', struct.pack('<I', u))[0],
            'nativeValue': struct.unpack('<f', struct.pack('<I', n))[0]}


def wasm_bodies(p):
    section = dict(sections(p.read_bytes()))[10]
    r = Reader(section)
    return [r.take(r.uint()) for _ in range(r.uint())]


def main():
    directory = ROOT/'analysis_input/unity_scene_chain_from_start_20261002'
    capture, unity_path = events(directory)
    base_dir = ROOT/'analysis_input/unity_11005_step486_pcm_20261001'
    base, base_path = events(base_dir)
    unchanged(capture, directory, base, base_dir)
    manifest_path = ROOT/'analysis_input/unity_chain_from_start_20261002.json'
    manifest = json.loads(manifest_path.read_text())
    original_wasm = ROOT/'analysis_input/unity_20260930.wasm'
    patched_wasm = ROOT/'analysis_input/unity_chain_from_start_20261002.wasm'
    assert sha(original_wasm) == manifest['sourceSha256']
    assert sha(patched_wasm) == manifest['patchedSha256']
    original_bodies, patched_bodies = wasm_bodies(original_wasm), wasm_bodies(patched_wasm)
    imported = manifest['importedFunctions']
    for item in manifest['functions']:
        assert original_bodies[item['functionIndex']-imported] == patched_bodies[item['rawFunctionIndex']-imported]
    native_path = ROOT/'analysis_input/native_scene_chain_from_start_20261002/calls.json'
    native = json.loads(native_path.read_text())
    assert native['callStackReliable'] and not native['dropped'] and not native['unfinished']
    native_module = Path(native['request']['module'])
    assert sha(native_module) == native['moduleSha256']
    native_dir = native_path.parent
    observer_report = json.loads((native_dir/'alignment.json').read_text())
    baseline_report = json.loads((ROOT/'analysis_input/c131_getter_gap_closed_20261002.json').read_text())
    assert observer_report['aggregate'] == baseline_report['aggregate']
    assert observer_report['rows'] == baseline_report['rows']
    calls = rows_of(capture, 'a12.pcm_internal_call')
    unity_constructors = sorted((c for c in calls if c['functionIndex'] == 71726), key=lambda c:c['callId'])
    native_constructors = [c for c in native['calls'] if c['functionRva'] == '0x214bd0']
    assert len(unity_constructors) == 50 and len(native_constructors) == 42
    # Identify the 16 stones by the common 19.1 kg mass, not by assuming
    # that scene props cannot be interleaved in the constructor sequence.
    # Extra scene bodies are not silently treated as corresponding stones.
    names = {16:'q.x',20:'q.y',24:'q.z',28:'q.w',32:'P.x',36:'P.y',40:'P.z',
             80:'v.x',84:'v.y',88:'v.z',96:'w.x',100:'w.y',104:'w.z',
             112:'maxAngularVelocitySq',116:'maxLinearVelocitySq',120:'linearDamping',124:'angularDamping',
             128:'inverseInertia.x',132:'inverseInertia.y',136:'inverseInertia.z',140:'inverseMass'}
    # Additional words belong to the common numeric prefix, not opaque ABI headers.
    offsets = list(range(16,44,4)) + list(range(48,160,4))
    unity_stones = [c for c in unity_constructors[:26]
                    if struct.unpack_from('<I', memory(c,'before',2),140)[0] == 0x3d567344]
    native_stones = [c for c in native_constructors[:18]
                     if struct.unpack_from('<I', memory(c,'before',2),140)[0] == 0x3d567344]
    assert len(unity_stones) == len(native_stones) == 16
    registration = []
    for index in range(16):
        u, n = unity_stones[index], native_stones[index]
        ub, nb = memory(u,'before',2), memory(n,'before',2)
        assert struct.unpack_from('<I', ub, 140)[0] == struct.unpack_from('<I', nb, 140)[0] == 0x3d567344
        words = [{'coreArgumentOffset': off, 'field': names.get(off,'numericWordAt%d'%off),
                  **word_comparison(struct.unpack_from('<I',ub,off)[0], struct.unpack_from('<I',nb,off)[0])}
                 for off in offsets]
        diffs = [w for w in words if not w['equal']]
        assert len(diffs) == 8
        registration.append({'stoneCreationIndex':index, 'unityCallId':u['callId'],
                             'nativeCallId':n['callId'], 'unityOrdinal':u['ordinal'],
                             'words': words, 'differenceCount':len(diffs), 'firstDifference':diffs[0]})
    fresh_path = ROOT/'analysis_input/native_initial_chain_readonly_20261002.json'
    fresh = json.loads(fresh_path.read_text())
    asset_path = ROOT/'local_simulator/assets/unity_runtime_hull.json'
    asset = json.loads(asset_path.read_text())
    hull_unity, hull_native = bytes(asset['hull_raw_bytes']), bytes(fresh['hull']['raw_bytes'])
    assert hull_unity == hull_native and len(hull_unity) == 4008
    # Full inertia input, including off-diagonals. Prior mass verification only
    # establishes the final diagonal tensor on the observed identity path.
    mass_dir = ROOT/'analysis_input/unity_11005_mass_properties_v2_20261002'
    mass_capture, mass_path = events(mass_dir)
    unchanged(mass_capture, mass_dir, base, base_dir)
    mass_calls = rows_of(mass_capture,'a12.pcm_internal_call')
    u_matrices = []
    for parent in (c for c in mass_calls if c['functionIndex'] == 72776):
        first = min((c for c in mass_calls if c['functionIndex'] == 72779 and c['parentCallId'] == parent['callId']), key=lambda c:c['callId'])
        u_matrices.append((first, struct.unpack_from('<9I', memory(first,'before',1))))
    assert len(u_matrices) == 98 and len({m for _,m in u_matrices}) == 1
    local_mass = fresh['massInformation']
    n_matrix = bits([v for col in local_mass['local_inertia_column_major'] for v in col])
    matrix = [{'columnMajorIndex':i, **word_comparison(u,n)} for i,(u,n) in enumerate(zip(u_matrices[0][1], n_matrix))]
    assert sum(not c['equal'] for c in matrix) == 6
    reset_rows = rows_of(capture,'a10.release_reset_orientation')
    reset = []
    for u, n in zip(reset_rows, fresh['resets']):
        u = u['release']['reset']
        assert u['text'] == n['text']
        positions = [float(v) for v in u['text'].split()[1:]]
        initial_writes = u['positionWrites'][:16]
        assert len({w['transformManagedPtr'] for w in initial_writes}) == 16
        for idx, uw in enumerate(initial_writes):
            nw = next(w for w in n['positionWrites'] if w['index'] == idx)
            assert idx == uw['writeOrdinal'] == nw['index']
            if positions[2*idx] == positions[2*idx+1] == 0:
                continue  # Hidden/inactive stone placements are different semantics too.
            uv, nv = uw['sourceVector'], nw['nativeAfterWrite']['physxPosition']
            reset.append({'resetSerial':u['serial'],'stoneIndex':idx,
                          'unityLayer':'Transform position input','nativeLayer':'PxRigidDynamic pose after reset position write',
                          'components':[word_comparison(a,b) for a,b in zip(bits(uv),bits(nv))]})
    assert len(reset) == 12 and all(not c['components'][1]['equal'] for c in reset)
    result = {
        'scope':'Startup, all 16 curling stones, and reset target position inputs before accepting a release-time prefix.',
        'comparison':'Raw IEEE754 binary32 words, including signed zero; matched semantic boundaries only.',
        'globallyProvenEarliestArithmeticFork':False,
        'completePrefixVerified':False,
        'firstObservedComparableCallBoundary':{'unityFunctionIndex':71726,'nativeFunctionRva':'0x214bd0',
            'name':'Sc::RigidSim constructor input','phase':'startup before reset/release/physics ordinal 1',
            'stoneCount':16,'allStoneInputsDiffer':True,'earlierFactoryAndCookingCallsFullyCompared':False},
        'registration':registration,
        'runtimeHullAsset':{'bytes':4008,'byteExact':True,'sha256':hashlib.sha256(hull_unity).hexdigest(),
            'scope':'Production uses captured Unity hull bytes; this does not prove the two cooking algorithms are bit-exact.'},
        'rawConvexInertiaInput':{'unityFunctionIndex':72779,'argument':1,'matrixOffset':0,
            'observedCalls':98,'unityFirstCallId':u_matrices[0][0]['callId'],'words':matrix,
            'fullMatrixExact':False,'finalInertiaDiagonalPriorVerificationExact':True,
            'scope':'Unity runtime mass-update input versus native cooked mass metadata, not a synchronized cooking output capture.'},
        'resetTargetPositionInputs':reset,
        'startupActorConstructorCounts':{'unity':26,'native':18,
            'scope':'Rosters differ; only corresponding curling stones and physical ice mapped, no full actor-creation equivalence claimed.'},
        'observerValidation':{'unityOriginalFunctionBodiesByteIdentical':True,
            'unityFrictionDraws':15580,'unityDenseSetterPairs':1023,'unityDynamicCoreFrames':40,'unityShotEndpoints':12,
            'unityObservableSequenceUnchanged':True,'nativeReplayRowsAndAggregateUnchanged':True,
            'nativeReplayScope':'Recorded reset rotations/friction and release quaternion are present after startup. This replay cannot certify a from-head prefix.',
            'freshNativeInitialStateInjection':False},
        'uncovered':'Mesh generation/cooking call sequence, complete scene roster, initialization Transform synchronization, and reset settling/sleep outputs are not yet a closed prefix.',
        'nextBoundary':'Align and audit initialization lifecycle and its actual writes; do not skip to collision or inject target pose to conceal the differences.',
        'moduleSha256':{'unity':sha(original_wasm),'unityInstrumented':sha(patched_wasm),'native':sha(native_module)},
        'evidenceSha256':{str(p.relative_to(ROOT)):sha(p) for p in (unity_path,native_path,fresh_path,asset_path,mass_path,base_path)},
        'sourceSha256':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'local_simulator/unity_physx.py',
            ROOT/'local_simulator/runtime_support/tools/reverse/recovered_stone_mass.py',
            ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js')},
    }
    output = ROOT/'analysis_input/scene_from_start_bits_20261002.json'
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print('registration:',len(registration),'stones,',sum(r['differenceCount'] for r in registration),'different numeric words')
    print('runtime hull:',len(hull_unity),'bytes exact; raw inertia: 6/9 words different; reset target Y:',len(reset),'different writes')
    print('global prefix verified:',result['completePrefixVerified'],'; report:',output)


if __name__ == '__main__':
    main()
