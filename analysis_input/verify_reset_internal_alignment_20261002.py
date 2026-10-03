"""Compare actual Reset contact/constraint streams and validate passive observers."""
import hashlib
import json
import struct
from pathlib import Path
from instrument_pcm_calls import Reader, sections
from verify_pcm_internal_trace import events, rows_of, raw_argument

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis_input/reset_internal_alignment_verified_20261002.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(values):
    return list(struct.unpack('<%dI' % len(values), struct.pack('<%df' % len(values), *values)))


def code_bodies(path):
    reader = Reader(dict(sections(path.read_bytes()))[10])
    return [reader.take(reader.uint()) for _ in range(reader.uint())]


def validate(directory):
    rows, path = events(directory)
    old, _ = events(ROOT / 'analysis_input/unity_reset_roster_first_case_20261002')
    assert not [r for r in rows if 'failed' in r['type']]
    assert rows_of(rows, 'sliding.random_range.friction') == rows_of(old, 'sliding.random_range.friction')
    a, b = rows_of(rows, 'scene.reset_body_cores'), rows_of(old, 'scene.reset_body_cores')
    assert len(a) == len(b) == 256, 'Incomplete/moved Reset sampling window'
    # All observed core words, including wake counter and inertia, must survive
    # the observer. Pointer addresses and the corrected step label can differ.
    assert [[c['bits'] for c in r['cores']] for r in a] == [[c['bits'] for c in r['cores']] for r in b]
    sample = lambda d: json.loads(next(d.glob('*.jsonl')).read_text().splitlines()[0])
    sa, sb = sample(directory), sample(ROOT / 'analysis_input/unity_reset_roster_first_case_20261002')
    for key in ('sample_id', 'after_position', 'final_xy', 'target_moves', 'requested', 'collision_observed'):
        assert sa[key] == sb[key], key
    return rows, path, dict(frictionRecordsExact=1562, resetCoreFramesExact=256, endpointUnchanged=True)


def main():
    validations = {}
    for name in ('unity_reset_internal_first_case_20261002', 'unity_reset_anchors_first_case_20261002',
                 'unity_reset_contact_prep_first_case_20261002'):
        rows, path, checks = validate(ROOT / 'analysis_input' / name)
        validations[name] = dict(checks, eventsSha256=digest(path))
    unity, unity_path, _ = validate(ROOT / 'analysis_input/unity_reset_contact_prep_first_case_20261002')
    original = ROOT / 'analysis_input/unity_20260930.wasm'
    source_bodies = code_bodies(original)
    manifests = ('unity_reset_internal_20261002.json', 'unity_reset_anchors_20261002.json',
                 'unity_reset_contact_prep_20261002.json')
    for name in manifests:
        manifest = json.loads((ROOT / 'analysis_input' / name).read_text())
        patched = Path(manifest['patched'])
        assert digest(original) == manifest['sourceSha256']
        assert digest(patched) == manifest['patchedSha256']
        bodies = code_bodies(patched)
        for record in manifest['functions']:
            original_body = source_bodies[record['functionIndex'] - manifest['importedFunctions']]
            assert bodies[record['rawFunctionIndex'] - manifest['importedFunctions']] == original_body
    native_path = ROOT / 'analysis_input/native_reset_anchors_steps1_6_20261002/calls.json'
    native = json.loads(native_path.read_text())
    assert native['callStackReliable'] and not native['dropped'] and not native['unfinished']
    nr = [r for r in native['calls'] if r['functionRva'] == '0x2e2880']
    ur = rows_of(unity, 'a12.pcm_convex_mesh')
    assert len(nr) == len(ur) == 6
    for step, (a, b) in enumerate(zip(nr, ur), 1):
        assert b['resetPhysicsStep'] == step
        for arg, field in ((5, 'transform0'), (6, 'transform1')):
            assert list(struct.unpack_from('<7I', raw_argument(a, arg, 'before'))) == words(
                b['before'][field]['q'] + b['before'][field]['p'])
        contacts = raw_argument(a, 8, 'after')
        assert b['after']['contactBuffer']['count'] == 5
        for i, point in enumerate(b['after']['contactBuffer']['contactsPreview']):
            assert list(struct.unpack_from('<7I', contacts, i * 64)) == words(
                point['normal'] + [point['separation']] + point['point'])
    local = json.loads((ROOT / 'analysis_input/native_reset_start_friction_internal_fixed_20261002.json').read_text())
    assert local['baselineOutputsUnchanged']
    first_friction = None
    for step, frame in enumerate(local['frames'][:6], 1):
        row = next(r for r in rows_of(unity, 'a12.static_solve') if r['resetPhysicsStep'] == step)
        a = bytes(row['before']['descs'][0]['constraintWindow']['rawBytes'])
        b = bytes(frame['solve_block'][0]['constraint_bytes_before'])
        assert a[:56] == b[:56], ('contact header', step)
        assert a[64:304] == b[80:320], ('normal constraints', step)
        differences = []
        # The force-buffer padding and unused vector lanes are not arithmetic
        # fields. Native pointers enlarge the header by 16 bytes.
        for i in range(4):
            for offset in list(range(0, 32, 4)) + [44, 48]:
                x = struct.unpack_from('<I', a, 336 + i * 64 + offset)[0]
                y = struct.unpack_from('<I', b, 352 + i * 64 + offset)[0]
                if x != y:
                    differences.append(dict(row=i, offset=offset, unityBits=x, nativeBits=y))
        if differences and first_friction is None:
            first_friction = dict(step=step, fields=differences)
    assert first_friction['step'] == 6
    cache_file = ROOT / 'analysis_input/native_reset_friction_prep_steps1_6_20261002/calls.json'
    cache_native = json.loads(cache_file.read_text())
    assert cache_native['callStackReliable'] and not cache_native['unfinished']
    cache_rows = [r for r in cache_native['calls'] if r['functionRva'] == '0xdcf30']
    cache_unity = [r for r in rows_of(unity, 'a12.pcm_internal_call') if r['functionIndex'] == 71233]
    assert len(cache_rows) == len(cache_unity) == 6
    cache_inputs = []
    for step, (a, b) in enumerate(zip(cache_rows, cache_unity), 1):
        raw = raw_argument(a, 0, 'before')
        ptr, count = struct.unpack_from('<Q', raw, 160)[0], raw[168]
        assert b['args'][1:3] == [0, 0]
        assert b['resetPhysicsStep'] == step
        cache_inputs.append(dict(step=step, unityPointer=0, unityCount=0,
                                 nativePointer=hex(ptr), nativeCount=count))
    assert cache_inputs[0]['nativeCount'] == 0 and cache_inputs[1]['nativeCount'] == 1
    regression = json.loads((ROOT / 'analysis_input/native_reset_start_friction_regression_v3_20261002.json').read_text())
    old = json.loads((ROOT / 'analysis_input/native_reset_settling_regression_20261002/alignment.json').read_text())
    assert regression['releaseBoundary'][5]['setters'] == old['releaseBoundary'][5]['setters']
    result = dict(
        originalWasmSha256=digest(original), nativeModuleSha256=native['moduleSha256'],
        observerValidations=validations, relocatedOriginalBodiesByteIdentical=True,
        pcmTransformWordsExact=84, pcmContactGeometryWordsExact=210,
        normalConstraintWordsExact=6 * 60, firstFiveFrictionConstraintFieldsExact=True,
        firstDifferingFrictionConstraint=first_friction, frictionCacheInputs=cache_inputs,
        firstObservedInternalInputDifference=dict(step=2, unityFunction=71233,
            nativeFunctionRva='0xdcf30', nativeDescriptorFrictionPointerOffset=160,
            nativeDescriptorFrictionCountOffset=168),
        firstObservedPQVelocityOutputDifferenceStep=6,
        appliedFixes=['Start sets only dynamic friction to 0; Reset preserves material history.',
                      'OnCollisionEnter(Stone) restores both actual contact participants to 0.6/0.6.'],
        calibratedRegression=dict(setterPairs11005Exact=1023, aggregate=regression['aggregate']),
        limits=['No claim that every startup/cooking intermediate is aligned.',
                'The Unity writer clearing friction cache and its caller are still unclosed.',
                'Endpoint improvements validate the material repair, not cache-mechanism reconstruction.'],
        evidenceSha256={str(p.relative_to(ROOT)):digest(p) for p in (unity_path,native_path,cache_file)},
        sourceSha256={str(p.relative_to(ROOT)):digest(p) for p in
            (ROOT / 'local_simulator/unity_physx.py',ROOT / 'analysis_input/pcm_functions_20261001/f61028.wat')})
    OUT.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('All six PCM geometry/normal-row windows exact. Cache input first differs at step 2; friction rows/output at step 6.')


if __name__ == '__main__':
    main()
