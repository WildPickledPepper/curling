"""Capture the first Reset's actual convex hull and startup cooker calls."""
import hashlib
import argparse
import json
from pathlib import Path
import subprocess
import sys
from instrument_pcm_calls import instrument

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--suffix', default='')
    opts = parser.parse_args()
    assert opts.suffix in ('','_inputs_v2'), 'Use a fixed capture identity'
    previous = json.loads((ROOT / 'analysis_input/unity_reset_contact_prep_20261002.json').read_text())
    source = ROOT / 'analysis_input/unity_20260930.wasm'
    stem = ROOT / ('analysis_input/unity_startup_geometry_audit_20261002' + opts.suffix)
    functions = list(dict.fromkeys([r['functionIndex'] for r in previous['functions']] + [72908, 72910, 72915]))
    patched, manifest = instrument(source.read_bytes(), functions)
    for key in ('actorLifecycleTrace', 'chainFromStartTrace', 'resetCoreTrace',
                'rigidbodyLifecycleTrace', 'resetInternalTrace', 'resetInternalRootFunctions'):
        manifest[key] = previous[key]
    manifest.update(source=str(source), patched=str(stem.with_suffix('.wasm')),
                    sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    patchedSha256=hashlib.sha256(patched).hexdigest(), startupGeometryAudit=True,
                    startupCookerInputAudit=bool(opts.suffix),
                    upstreamRootFunctions=previous['upstreamRootFunctions'] + [72908, 72910, 72915])
    assert not stem.with_suffix('.wasm').exists(), 'Preserve captures: use a new name for another run'
    stem.with_suffix('.wasm').write_bytes(patched)
    stem.with_suffix('.json').write_text(json.dumps(manifest, indent=2))
    output = ROOT / ('analysis_input/unity_startup_geometry_audit_capture_20261002' + opts.suffix)
    subprocess.run([sys.executable, str(ROOT / 'analysis_input/capture_12011_first_solver.py'),
                    '--dense-release-serial', '2', '--output', str(output),
                    '--plan', 'analysis_input/reset_first_case_20261002.json',
                    '--events', 'research_archive/unity_reverse/evidence/log/c131_strict_yaw_r00_20260714/collision_unique_targets_batch_r00/unity_runtime_probe_20260714_173341/events.jsonl',
                    '--expected-release-count', '1', '--expected-friction-count', '1562',
                    '--expected-dense-count', '1563', '--expected-c03-count', '0',
                    '--expected-reset-core-count', '256', '--reset-settle-seconds', '2',
                    '--phase-ordinal-min', '1', '--phase-ordinal-max', '4',
                    '--export-wait-seconds', '180', '--static-phase-trace',
                    '--pcm-call-trace-manifest', str(stem.with_suffix('.json'))], cwd=ROOT, check=True)
    (output / 'capture_manifest.json').write_text(json.dumps(manifest, indent=2))
    (output / 'observer_source.js').write_bytes((ROOT / 'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js').read_bytes())


if __name__ == '__main__':
    main()
