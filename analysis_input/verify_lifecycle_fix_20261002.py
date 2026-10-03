"""Verify source-backed startup/retirement history and the repaired first PCM."""
import hashlib
import json
import struct
from pathlib import Path

from verify_pcm_internal_trace import events, rows_of
from verify_collision_pair_sort_20261002 import read

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def pool(row):
    memory = row['rigidIdPoolBefore']
    header = bytes.fromhex(memory[0]['hex'])
    def ids(argument, offset):
        count = struct.unpack_from('<I', header, offset)[0]
        if not count:
            return []
        data = bytes.fromhex(next(b['hex'] for b in memory if b['argument'] == argument))
        return list(struct.unpack_from('<' + str(count) + 'I', data))
    return {'freeIds': ids(1, 12), 'pendingIds': ids(2, 36)}


def main():
    directory = ROOT / 'analysis_input/unity_11005_actor_lifecycle_20261002'
    captured, event_path = events(directory)
    baseline, _ = events(ROOT / 'analysis_input/unity_11005_step486_pcm_20261001')
    assert not [r for r in captured if 'failed' in r['type']]
    assert rows_of(captured, 'sliding.random_range.friction') == rows_of(baseline, 'sliding.random_range.friction')
    for kind in ('a12.dense_pre_angular_setter', 'a12.dense_post_angular_setter'):
        def stable(row):
            return {k: v for k, v in row.items() if k not in ('nativePtr', 'bridgePtr', 'tickSerial')}
        actual, expected = rows_of(captured, kind), rows_of(baseline, kind)
        assert len(actual) == len(expected) == 1023
        assert list(map(stable, actual)) == list(map(stable, expected))
    frames = rows_of(captured, 'c04.dynamic_solver_frame')
    assert len(frames) == 40
    for actual, expected in zip(frames, rows_of(baseline, 'c04.dynamic_solver_frame')):
        for edge in ('entryCores', 'exitCores'):
            def core(row):
                return {k: v for k, v in row['decodedCandidate'].items() if k != 'ptr'}
            assert list(map(core, actual[edge])) == list(map(core, expected[edge]))
    def samples(folder):
        return [json.loads(s) for s in next(folder.glob('collision*.jsonl')).read_text().splitlines()]
    fields = ('sample_id', 'after_position', 'final_xy', 'target_moves', 'requested', 'collision_observed')
    assert [{k: r[k] for k in fields} for r in samples(directory)] == [
        {k: r[k] for k in fields} for r in samples(ROOT / 'analysis_input/unity_11005_step486_pcm_20261001')]

    asset_path = ROOT / 'local_simulator/assets/unity_startup_rigid_id_pool.json'
    asset = load('local_simulator/assets/unity_startup_rigid_id_pool.json')
    assert asset['source']['eventsSha256'] == sha(event_path)
    calls = rows_of(captured, 'a12.pcm_internal_call')
    unity_ctors = [r for r in calls if r['functionIndex'] == 71726]
    assert len(unity_ctors[:26]) == 26
    ice = unity_ctors[18]
    assert list(struct.unpack('<3f', read(ice, ice['args'][2] + 32, 12))) == asset['source']['iceActorPosition']
    assert pool(unity_ctors[26])['freeIds'] == asset['observedUnityFreedRigidIds']

    lifecycle_path = ROOT / 'analysis_input/native_actor_lifecycle_fixed_v2_20261002/calls.json'
    lifecycle = json.loads(lifecycle_path.read_text())
    assert lifecycle['callStackReliable'] and not lifecycle['dropped'] and not lifecycle['unfinished']
    native_ctors = [r for r in lifecycle['calls'] if r['functionRva'] == '0x214bd0']
    assert len(native_ctors) == 18 + 24
    def actor_type(row):
        return bytes.fromhex(next(b['hex'] for b in row['before'] if b['argument'] == 2))[13]
    assert [actor_type(r) for r in native_ctors[:18]] == [0] + [1]*16 + [0]
    mapping = {i+1: v for i, v in enumerate(sorted(asset['observedUnityFreedRigidIds']))}
    # IDs differ because irrelevant scene actors differ. A strictly increasing
    # mapping preserves every comparison and verifies the entire allocator state.
    assert len(unity_ctors[26:]) == 24
    for unity, native in zip(unity_ctors[26:], native_ctors[18:]):
        assert unity['rigidIdAfter'] == mapping[native['rigidIdAfter']]
        for key in ('freeIds', 'pendingIds'):
            assert pool(unity)[key] == [mapping[i] for i in native['rigidIdPoolBefore'][key]]

    report_path = ROOT / 'analysis_input/c131_production_lifecycle_fixed_v2_20261002.json'
    report = json.loads(report_path.read_text())
    boundary = next(r for r in report['releaseBoundary'] if r['sampleId'] == 11005)
    role_orders = []
    for index, release in enumerate(report['releaseBoundary']):
        target, active = unity_ctors[26 + 2*index:28 + 2*index]
        expected = ['active', 'target'] if active['rigidIdAfter'] >= target['rigidIdAfter'] else ['target', 'active']
        actual = [['active' if i == release['activeIndex'] else 'target' for i in pair]
                  for pair in release['firstContactRoleOrder']]
        assert actual == [expected]
        role_orders.append({'sampleId': release['sampleId'], 'order': expected})
    assert report['diagnosticEffectiveConfiguration']['setActiveNoSim']
    assert [r['clearedOutOfPlay'] for r in report['rows'] if r['clearedOutOfPlay']] == [[3], [5], [12]]

    pcm = rows_of(captured, 'c05.persistent_pcm_call')[0]
    first = boundary['postDenseFrames'][0]
    local_pcm = next(r for r in first['narrowphase'] if not r['after'] and r['geom_type0'] == r['geom_type1'] == 4)
    for field in ('p', 'q'):
        assert local_pcm['transform0'][field] == pcm['before']['transform0'][field]
    assert local_pcm['transform1']['p'] == pcm['before']['transform1']['p']
    def geometry(row):
        return {k: row[k] for k in ('point', 'normal', 'separation')}
    unity_contacts = list(map(geometry, pcm['after']['contactBuffer']['contactsPreview']))
    local_contacts = list(map(geometry, first['finalizer'][0]['contacts']))
    assert len(unity_contacts) == 2 and unity_contacts == local_contacts

    pcm_calls_path = ROOT / 'analysis_input/native_stone_pair_lifecycle_fixed_20261002/calls.json'
    trace = json.loads(pcm_calls_path.read_text())
    assert trace['callStackReliable'] and not trace['dropped'] and not trace['unfinished']
    sort = next(r for r in trace['calls'] if r['functionRva'] == '0x236ed0')
    inputs = sorted(sort['pairSortInput'], key=lambda r: r['rigidId'], reverse=True)
    assert [r['rigidId'] for r in inputs] == [15, 1]
    for role, item in enumerate(inputs):
        assert list(struct.unpack_from('<3f', bytes(item['bodyCoreBytes']), 16)) == pcm['before']['transform'+str(role)]['p']
    ctor = next(r for r in trace['calls'] if r['functionRva'] == '0x27c630')
    assert ctor['args'][1:3] == [r['actorSim'] for r in inputs]
    full = next(r for r in trace['calls'] if r['functionRva'] == '0x3c5a90')
    clip = next(r for r in trace['calls'] if r['functionRva'] == '0x3cab40')
    assert clip['args'][:2] == [full['args'][1], full['args'][0]]
    assert clip['returnAddressRva'] == '0x3c868f'
    unity_clip = next(r for r in calls if r['functionIndex'] == 70076 and r.get('releaseSerial') == 12)
    for argument in (2, 3):
        plane = bytes.fromhex(next(b['hex'] for b in clip['before'] if b['argument'] == argument))[:16]
        assert plane == read(unity_clip, unity_clip['args'][argument], 16)
    # Both observers and isolated queries leave the repaired trajectory intact.
    for folder in ('native_actor_lifecycle_fixed_v2_20261002', 'native_stone_pair_lifecycle_fixed_20261002'):
        observed = load('analysis_input/' + folder + '/alignment.json')
        assert observed['rows'] == report['rows'] and observed['aggregate'] == report['aggregate']

    uc = bytes(frames[0]['dynamicSolves'][0]['before']['descs'][0]['constraintWindow']['rawBytes'])
    lc = bytes(first['solve_block'][0]['constraint_bytes_before'])
    # Header sizes differ on 32-bit Wasm and x64. Compare the first row after
    # the respective headers, excluding architecture-specific pointer slots.
    angular_coefficients = {'unity': list(struct.unpack_from('<3f', uc, 64)),
                            'local': list(struct.unpack_from('<3f', lc, 80))}
    assert angular_coefficients['unity'] != angular_coefficients['local']
    paths = [event_path, asset_path, lifecycle_path, pcm_calls_path, report_path,
             ROOT/'local_simulator/unity_physx.py',
             ROOT/'analysis_input/native_actor_id_lifecycle_20261002.asm']
    result = {'sampleId': 11005, 'physicalStep': 1022, 'setterOrdinal': 1023,
        'fixed': 'RigidID lifecycle, actual pair order, reference face and first PCM contact geometry',
        'allocatorConstructorStatesMatched': 24, 'firstContactOrdersMatched': role_orders,
        'unityRigidIds': {'active': 16, 'target': 1}, 'nativeRigidIds': {'active': 15, 'target': 1},
        'firstContactsBitExact': local_contacts,
        'remainingFirstConstraintAngularCoefficients': angular_coefficients,
        'remainingTargetQuaternion': {'unity': pcm['before']['transform1']['q'], 'local': local_pcm['transform1']['q']},
        'activeExitAngularY': {'unity': frames[0]['exitCores'][0]['decodedCandidate']['angularVelocity'][1],
                              'local': first['afterNative']['1']['physxAngularVelocity'][1]},
        'endpointErrorM': next(r['endpointErrorM'] for r in report['rows'] if r['sampleId'] == 11005),
        'aggregate': report['aggregate'],
        'transparency': {'unityFrictionValues': 15580, 'unitySetterPairs': 1023, 'unitySolverFrames': 40,
                         'unityEndpoints': 12, 'nativeObserversDoNotChangeTrajectory': True},
        'hashes': {str(p.relative_to(ROOT)): sha(p) for p in paths},
        'unityWasmSha256': asset['source']['unityWasmSha256'], 'nativeModuleSha256': trace['moduleSha256'],
        'functions': {'unityActorConstructor':71726,'unityActorDestructor':71727,'unityRetirement':71674,
                      'nativeActorConstructor':'0x214bd0','nativeActorDestructor':'0x214c50',
                      'nativeSort':'0x236ed0','nativeFullManifold':'0x3c5a90','nativeGeneratedContacts':'0x3cab40'},
        'limits': ['The fixed startup scene state is captured; a general Unity activation-queue ordering algorithm is not reconstructed.',
                   'Exact allocator/order validation covers this 16-stone scene and recorded 12-shot lifecycle.',
                   'Initial quaternion and friction replay remain the audit boundary; no post-release Unity state is injected.',
                   'Target history, solver lock flags, first-row angular coefficients and collision-tail error remain.']}
    output = ROOT/'analysis_input/11005_lifecycle_fix_verified_20261002.json'
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('fixed', 'allocatorConstructorStatesMatched', 'remainingFirstConstraintAngularCoefficients', 'endpointErrorM')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
