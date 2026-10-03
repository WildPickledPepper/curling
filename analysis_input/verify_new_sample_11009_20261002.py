"""Locate observed raw-state divergence and check against original-Wasm control."""
import hashlib
import json
import struct
from pathlib import Path
from verify_pcm_internal_trace import events, rows_of
from verify_release_ordinary_tail_20261002 import core_states
from verify_reset_internal_alignment_20261002 import code_bodies

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'analysis_input'
FIELDS = ['px','py','pz','qx','qy','qz','qw','vx','vy','vz','wx','wy','wz']


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def differences(unity, native):
    return [dict(stoneIndex=(0,11)[i], field=FIELDS[j], wordIndex=j,
        unityBits=f'0x{a:08x}', nativeBits=f'0x{b:08x}',
        unityFloat=struct.unpack('<f',struct.pack('<I',a))[0],
        nativeFloat=struct.unpack('<f',struct.pack('<I',b))[0])
        for i in range(2) for j,(a,b) in enumerate(zip(unity[i],native[i])) if a != b]


def main():
    capture = BASE/'unity_new_sample_11009_capture_20261002'
    control = BASE/'unity_new_sample_11009_control_20261002'
    rows, path = events(capture)
    controls, control_path = events(control)
    native_path = BASE/'native_new_sample_11009_20261002.json'
    native = json.loads(native_path.read_text())
    assert native['sourceSha256'] == digest(ROOT/'local_simulator/unity_physx.py')
    assert native['unityEventsSha256'] == digest(path)
    assert not [r for r in rows+controls if 'failed' in r['type'] or 'exhausted' in r['type']]
    manifest = json.loads((capture/'capture_manifest.json').read_text())
    original = BASE/'unity_20260930.wasm'
    assert digest(original) == manifest['sourceSha256']
    assert digest(Path(manifest['patched'])) == manifest['patchedSha256']
    bodies, patched = code_bodies(original), code_bodies(Path(manifest['patched']))
    for r in manifest['functions']:
        assert bodies[r['functionIndex']-manifest['importedFunctions']] == patched[r['rawFunctionIndex']-manifest['importedFunctions']]
    commands = json.loads((control/'commands.json').read_text())
    assert '--pcm-call-trace-manifest' not in commands['browser']
    assert '--rng-friction-manifest-events' in commands['browser']
    assert not rows_of(rows, 'rng.friction_manifest_applied')
    strip = lambda r: {k:v for k,v in r.items() if k not in ('nativePtr','bridgePtr','tickSerial')}
    for kind in ('a12.dense_pre_angular_setter','a12.dense_post_angular_setter'):
        a, b = rows_of(rows,kind), rows_of(controls,kind)
        assert len(a) == len(b) == 1384
        # The overridden control return does not populate the passive RNG
        # ring in every backend. Check draws separately; compare all poses,
        # setter inputs and getter outputs here.
        strip_control = lambda r: {k:v for k,v in strip(r).items()
            if k not in ('lastFrictionNoise','bridge164Bits','bridge300Bits')}
        assert [strip_control(r) for r in a] == [strip_control(r) for r in b]
        bits = lambda v: struct.pack('<%df'%len(v),*v)
        for x,y in zip(a,b):
            for field in ('getterLinear','getterAngular','setterAngular','bridge164','bridge300'):
                if x.get(field) is not None:
                    assert bits(x[field]) == bits(y[field])
            if x.get('pose') is not None:
                assert bits(x['pose']['p']+x['pose']['q']) == bits(y['pose']['p']+y['pose']['q'])
    draws = rows_of(controls,'sliding.random_range.friction')
    assert [r['value'] for r in draws] == native['frictionNoises']
    def sample(d): return json.loads(next(d.glob('*.jsonl')).read_text().splitlines()[0])
    a,b = sample(capture),sample(control)
    for k in ('requested','after_position','final_xy','target_moves','collision_observed'):
        assert a[k] == b[k],k
    tail = rows_of(rows,'a12.tail_phase_core')
    boundaries = {}
    for r in tail:
        if r['phase'] == 'DCP.FixedUpdate.boundary' and r['edge'] == 'enter':
            states = core_states(r)
            tick = r['solverSerial']
            if tick in boundaries: assert boundaries[tick] == states
            boundaries[tick] = states
    assert sorted(boundaries) == list(range(3001))
    release_diff = differences(boundaries[0],native['releaseBits'])
    first_release = next(r for r in tail if r['solverSerial'] == 0)
    assert differences(core_states(first_release),native['releaseBits']) == release_diff
    assert boundaries[0][1] == native['resetBits'][1]
    delta = [(tick,differences(boundaries[tick],native['states'][tick-1])) for tick in range(1,3001)]
    delta = [(tick,diff) for tick,diff in delta if diff]
    assert len(release_diff) == 1 and release_diff[0]['field'] == 'pz'
    report = dict(sampleId=11009,plan=native['plan'],unityWasmSha256=digest(original),
        productionCodeSha256=native['sourceSha256'],nativeModuleSha256=native['moduleSha256'],
        frictionDraws=1383,completedPhysicsStepsCompared=3000,
        releaseStateWordsCompared=26,releaseStateWordsExact=25,
        firstObservedDifference=dict(boundary='BESTSHOT release, before first physical step',
            physicsTick=0,phase=first_release['phase'],edge=first_release['edge'],
            differences=release_diff),firstCompletedStepDifference=dict(physicsTick=delta[0][0],differences=delta[0][1]),
        differingCompletedSteps=len(delta),nativeFirstContactTick=native['stoneContactTicks'][0],
        observer=dict(originalBodiesByteIdentical=True,originalWasmControl=True,
            controlSetterPairsEqual=1384,controlFrictionInputsEqual=1383,controlProtocolResultEqual=True,
            scope='Original-Wasm control preserves observed setter/getter/pose stream and protocol results. RNG control uses recorded return values; internal RNG state is not compared.'),
        evidenceFunction=dict(functionIndex=60092,readPositionFunctionIndex=32544,
            writePositionFunctionIndex=32546,operation='f32 load of Rigidbody position.z; p2 horizontal offset; f32.sub; store in position vector; call f32546',
            watLine=326),
        limitations=['Earliest observed release-state divergence; no claim that all earlier internal Reset/cooking/parse operations were sampled bitwise in this new case.',
            'Later state differences are measured but are not independent root causes.',
            'No production repair or injected pose was used.'],
        evidence={str(p.relative_to(ROOT)):digest(p) for p in (path,control_path,native_path,
            capture/'capture_manifest.json',capture/'observer_source.js',control/'commands.json',
            BASE/'new_sample_11009_plan_20261002.json',BASE/'pcm_functions_20261001/f60092.wat')})
    out = BASE/'new_sample_11009_verified_20261002.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({k:report[k] for k in ('firstObservedDifference','differingCompletedSteps','observer')},indent=2,ensure_ascii=False))


if __name__ == '__main__': main()
