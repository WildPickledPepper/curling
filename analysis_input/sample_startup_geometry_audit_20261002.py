"""Read production geometry before/after the existing runtime asset import.

The observer forwards every call unchanged. It does not select a different
cooker, replace inputs, or add a new geometry patch.
"""
import hashlib
import argparse
import json
import sys
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx, _resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
from tools.reverse import probe_physx_collision_alignment as probe


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def state(scene):
    keys = ('physxPosition', 'quaternionWxyz', 'physxLinearVelocity', 'physxAngularVelocity')
    return [{k: scene.raw_native_state(i)[k] for k in keys} for i in range(16)]


def state_bits(states):
    return [list(struct.unpack('<13I', struct.pack('<13f',
                 *(r['physxPosition'] + r['quaternionWxyz'] +
                   r['physxLinearVelocity'] + r['physxAngularVelocity'])))) for r in states]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'analysis_input/native_startup_geometry_audit_20261002.json')
    opts=parser.parse_args()
    observed = []
    construction_inputs = []
    original = probe._patch_runtime_stone_shape
    original_make = probe._make_stone

    def observed_make(*args, **kwargs):
        if kwargs.get('shared_convex_source') is None:
            points = kwargs['stone_points']
            construction_inputs.append(dict(pointCount=len(points),
                pointBits=[list(struct.unpack('<3I', struct.pack('<3f', *p))) for p in points],
                quantizedCount=kwargs['convex_quantized_count'], vertexLimit=kwargs['convex_vertex_limit'],
                quantizeInput=kwargs['quantize_input'], gpuCompatible=kwargs['gpu_compatible'],
                note='Actual Python-to-pybind call inputs; native PxCookingParams internal fields still need direct memory tracing.'))
        return original_make(*args, **kwargs)

    def read_only(shape, **kwargs):
        before = shape.get_convex_mesh_runtime_hull_data()
        mass_before = shape.get_convex_mesh_data()['mass_information']
        result = original(shape, **kwargs)
        after = shape.get_convex_mesh_runtime_hull_data()
        mass_after = shape.get_convex_mesh_data()['mass_information']
        observed.append(dict(before=before, after=after,
                             massBefore=mass_before, massAfter=mass_after,
                             originalPatchResult=result))
        return result

    probe._patch_runtime_stone_shape = read_only
    probe._make_stone = observed_make
    try:
        wrapped = PersistentPhysxFrontHalfScene(stone_count=16)
    finally:
        probe._patch_runtime_stone_shape = original
        probe._make_stone = original_make
    plain = PersistentPhysxFrontHalfScene(stone_count=16)
    assert len(observed) == 1, 'Shared mesh is cooked/imported once'
    a = wrapped.slots[0].shape.get_convex_mesh_runtime_hull_data()
    b = plain.slots[0].shape.get_convex_mesh_runtime_hull_data()
    assert a == b and state_bits(state(wrapped)) == state_bits(state(plain)), 'Observer changed startup output'
    assert wrapped._stone_mass_information == plain._stone_mass_information
    assert list(wrapped.scene.get_gravity()) == list(plain.scene.get_gravity())
    report = dict(
        productionCodeSha256=digest(ROOT / 'local_simulator/unity_physx.py'),
        nativeModuleSha256=digest(_resolve_bundled_extension()),
        samplerSha256=digest(Path(__file__)), observations=observed, constructionInputs=construction_inputs,
        startupStates=state(wrapped), startupStateBits=state_bits(state(wrapped)),
        gravity=list(wrapped.scene.get_gravity()),
        bounceThreshold=wrapped.scene.get_bounce_threshold_velocity(),
        observer=dict(plainAndWrappedHullExact=True, plainAndWrappedStartupStatesExact=True,
                      plainAndWrappedMassInformationExact=True),
        scope='Fresh default CP39 startup; passive before/after existing production convex asset import; no Reset/shot/RNG/state injection.')
    out = opts.output
    out.write_text(json.dumps(report, indent=2), encoding='utf8')
    print('PASS: passive startup observer; one shared convex cook/import; output', out)


if __name__ == '__main__':
    main()
