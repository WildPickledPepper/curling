"""Capture the actual pose-update -> contact-cache invalidation call chain."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from instrument_geometry_writes import build
from instrument_pcm_calls import instrument

ROOT = Path(__file__).resolve().parents[1]


def main():
    stem = ROOT / 'analysis_input/unity_reset_cache_lifecycle_20261002'
    previous = json.loads((ROOT / 'analysis_input/unity_reset_friction_cache_writes_20261002.json').read_text())
    functions = list(dict.fromkeys([r['functionIndex'] for r in previous['functions']]
                                  + [71461, 71729, 71632, 71596, 72606]))
    if not stem.with_suffix('.wasm').exists():
        watched, manifest = build(Path(previous['source']).read_bytes())
        patched, calls = instrument(watched, functions)
        for key in ('upstreamRootFunctions', 'actorLifecycleTrace', 'chainFromStartTrace',
                    'resetCoreTrace', 'rigidbodyLifecycleTrace', 'resetInternalTrace',
                    'frictionCacheWriteWatch'):
            manifest[key] = previous[key]
        manifest['resetInternalRootFunctions'] = [71272, 71103, 72606, 71596, 71729, 71461]
        manifest['functions'] = calls['functions']
        manifest['source'] = previous['source']
        manifest['patched'] = str(stem.with_suffix('.wasm'))
        manifest['patchedSha256'] = hashlib.sha256(patched).hexdigest()
        stem.with_suffix('.wasm').write_bytes(patched)
        stem.with_suffix('.json').write_text(json.dumps(manifest, indent=2))
        print('built', manifest['patchedSha256'], len(patched), flush=True)
    command = [sys.executable, str(ROOT / 'analysis_input/capture_12011_first_solver.py'),
               '--dense-release-serial', '12', '--output',
               str(ROOT / 'analysis_input/unity_reset_cache_lifecycle_first_case_20261002'),
               '--plan', 'analysis_input/reset_first_case_20261002.json', '--events',
               'research_archive/unity_reverse/evidence/log/c131_strict_yaw_r00_20260714/collision_unique_targets_batch_r00/unity_runtime_probe_20260714_173341/events.jsonl',
               '--expected-release-count', '1', '--expected-friction-count', '1562',
               '--expected-dense-count', '0', '--expected-c03-count', '0', '--static-phase-trace',
               '--pcm-call-trace-manifest', str(stem.with_suffix('.json'))]
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
