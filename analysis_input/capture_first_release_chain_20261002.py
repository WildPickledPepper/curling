"""Passive first-release setter and physics observer; original Wasm bodies retained."""
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
    parser.add_argument('--output', type=Path, default=ROOT/'analysis_input/unity_first_release_chain_capture_20261002')
    parser.add_argument('--phase-min',type=int,default=1)
    parser.add_argument('--phase-max',type=int,default=4)
    parser.add_argument('--velocity-getter-max-ordinal',type=int,default=1023)
    parser.add_argument('--writeback-only',action='store_true')
    parser.add_argument('--tail-core-min',type=int)
    parser.add_argument('--tail-core-max',type=int)
    parser.add_argument('--tail-all-stone-cores',action='store_true')
    parser.add_argument('--tail-max-solver-steps',type=int,default=2000)
    parser.add_argument('--wake-internal',action='store_true')
    parser.add_argument('--release-tail-trace-solver-limit',type=int,default=4)
    parser.add_argument('--export-wait-seconds',type=float,default=90)
    opts = parser.parse_args()
    stem = ROOT / ('analysis_input/unity_first_release_chain_20261002' if opts.phase_max==4
        else ('analysis_input/unity_release_526_chain_20261002' if opts.phase_min==526 and opts.phase_max==528
        else 'analysis_input/unity_release_%d_%d_chain_20261002'%(opts.phase_min,opts.phase_max)))
    if opts.writeback_only:stem=stem.with_name(stem.name+'_writeback')
    if opts.wake_internal:stem=stem.with_name(stem.name+'_wake_internal_v3')
    source = ROOT / 'analysis_input/unity_20260930.wasm'
    functions = [71726,71727,73034,73035,73070,72606,71596,71729,71632,
                 61066,60092,60705,32521,32524,32511,32512,
                 70030,70031,70485,70494,69939,69978,69979,70050,70051,
                 70054,70056,69975,69976,70052,70055,70057,70058,70059,
                 70060,70061,70062,70179,69896,69972,69977,70053,
                 71103,71234,71233,71216,71217,71218,71104,71105,71272]
    if opts.writeback_only:functions=functions[:16]
    wake_functions=[71379,71381,71468,71525,71529,71555,71556,71557,71561,71661,
                    71566,71567,71570,71571,71572,71573,71575,71576,71618,71653]
    if opts.wake_internal:functions+=wake_functions
    if not stem.with_suffix('.wasm').exists():
        patched, manifest = instrument(source.read_bytes(), functions)
        manifest.update(source=str(source), patched=str(stem.with_suffix('.wasm')),
                        sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                        patchedSha256=hashlib.sha256(patched).hexdigest(),
                        upstreamRootFunctions=[73034,73035,73070,61066,60092,60705],
                        releaseSetterTrace=True, actorLifecycleTrace=True,
                        resetCoreTrace=True, velocityGetterTrace=True)
        stem.with_suffix('.wasm').write_bytes(patched)
        stem.with_suffix('.json').write_text(json.dumps(manifest, indent=2))
        print('built', manifest['patchedSha256'], flush=True)
    manifest=json.loads(stem.with_suffix('.json').read_text())
    manifest['upstreamRootFunctions']=[71726,71727,73034,73035,73070,61066,60092,60705]
    manifest['releasePhaseRootFunctions']=[71272]
    if opts.wake_internal:
        manifest['upstreamRootFunctions']+=wake_functions
        manifest['wakeFunctionTrace']=wake_functions
        manifest['releaseTailTraceSolverLimit']=opts.release_tail_trace_solver_limit
        manifest['wakeFunctionWindow']={'minOrdinal':1560,'maxOrdinal':1563}
    manifest['velocityGetterMaxOrdinal']=opts.velocity_getter_max_ordinal
    if opts.tail_core_min is not None:
        manifest['tailCoreWindow']={'minOrdinal':opts.tail_core_min,
            'maxOrdinal':opts.tail_core_max or opts.tail_core_min,
            'allStoneCores':opts.tail_all_stone_cores,'maxSolverSteps':opts.tail_max_solver_steps}
    if opts.writeback_only:manifest['chainFromStartTrace']=True
    stem.with_suffix('.json').write_text(json.dumps(manifest,indent=2))
    command=[sys.executable,str(ROOT/'analysis_input/capture_12011_first_solver.py'),
        '--dense-release-serial','2','--output',str(opts.output),
        '--plan','analysis_input/reset_first_case_20261002.json',
        '--events','research_archive/unity_reverse/evidence/log/c131_strict_yaw_r00_20260714/collision_unique_targets_batch_r00/unity_runtime_probe_20260714_173341/events.jsonl',
        '--expected-release-count','1','--expected-friction-count','1562',
        '--expected-dense-count','1563','--expected-c03-count','0',
        '--expected-reset-core-count','256','--reset-settle-seconds','2',
        '--export-wait-seconds',str(opts.export_wait_seconds),
        '--phase-ordinal-min',str(opts.phase_min),'--phase-ordinal-max',str(opts.phase_max),
        '--pcm-call-trace-manifest',str(stem.with_suffix('.json'))]
    command.append('--static-phase-trace')
    subprocess.run(command,cwd=ROOT,check=True)
    (opts.output/'capture_manifest.json').write_text(json.dumps(manifest,indent=2))
    probe=ROOT/'research_archive/unity_reverse/source/reverse/unity_webgl_runtime_probe.js'
    (opts.output/'observer_source.js').write_bytes(probe.read_bytes())

if __name__ == '__main__':
    main()
