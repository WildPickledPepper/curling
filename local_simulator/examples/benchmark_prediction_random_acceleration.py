"""Alternate prior fast prediction and exact native lazy RNG in one process."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
from local_simulator.examples.benchmark_prediction_time import summary
from local_simulator.native_random import load_random_kernel


def main(*, stage='random'):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats', type=int, default=10)
    phase = {'random': 2, 'steps': 3, 'merged': 4, 'scene': 5}[stage]
    date = '20261004' if phase == 5 else '20261003'
    parser.add_argument('--output', type=Path, default=ROOT/f'analysis_input/prediction_phase{phase}_timing_{date}.json')
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error('--repeats must be positive')
    install_bundled_pyphysx()
    if load_random_kernel() is None:
        raise RuntimeError('native helper required to measure the optimization')
    if stage in ('steps', 'merged', 'scene'):
        from local_simulator.native_step_bridge import load_step_bridge
        if load_step_bridge() is None:
            raise RuntimeError('verified CP39 step bridge required to measure the optimization')
    before = StrictCurlingEnd(seed=20261003, prediction_native_random=stage != 'random',
                             prediction_native_steps=stage in ('merged', 'scene'), prediction_merged_steps=stage == 'scene',
                             prediction_native_scene_steps=False)
    after = StrictCurlingEnd(seed=20261003, prediction_native_random=True,
                            prediction_native_steps=stage != 'random', prediction_merged_steps=stage in ('merged', 'scene'),
                            prediction_native_scene_steps=stage == 'scene')
    cases = [('free', [3., 0., 0.], []), ('hit', [3.4, 0., 0.], [(2, 2.375, 5.2)]),
        ('wall', [4.1, 0., 0.], [(2, 1.875, 5.6)]), ('spin', [3.35, .18, 9.42], [(2, 2.375, 6.7)]),
        ('dense', [3.35, 0., 0.], [(1, 2.375, 7.15), (3, 2.375, 4.88), (5, 1.92, 6.12), (7, 2.83, 6.12)])]
    rows = []
    def run(env, shot, positions):
        started, cpu = time.perf_counter(), time.process_time()
        env.scene.reset_positions(positions, yaw_overrides={k: 0. for k in range(16)})
        env.shot_number = 0
        result = env.play(shot)
        payload = json.dumps(result, sort_keys=True, separators=(',', ':'))
        elapsed = (time.perf_counter()-started)*1000
        cpu_ms = (time.process_time()-cpu)*1000
        assert result['settled']
        return dict(ms=elapsed, cpu_ms=cpu_ms, sha256=hashlib.sha256(payload.encode()).hexdigest()), result
    for name, shot, stones in cases:
        positions = [0.]*32
        for k, x, y in stones:
            positions[2*k:2*k+2] = [x, y]
        for _ in range(2):
            run(before, shot, positions)
            run(after, shot, positions)
        samples = []
        for index in range(args.repeats):
            if index % 2:
                a, old = run(before, shot, positions)
                b, new = run(after, shot, positions)
            else:
                b, new = run(after, shot, positions)
                a, old = run(before, shot, positions)
            assert old == new, (name, index)
            samples.append(dict(before=a, after=b))
        baseline = summary([item['before']['ms'] for item in samples])
        optimized = summary([item['after']['ms'] for item in samples])
        row = dict(case=name, before_ms=baseline, after_ms=optimized,
                   median_speedup=baseline['median']/optimized['median'],
                   paired_speedup=summary([s['before']['ms']/s['after']['ms'] for s in samples]),
                   before_cpu_ms=summary([s['before']['cpu_ms'] for s in samples]),
                   after_cpu_ms=summary([s['after']['cpu_ms'] for s in samples]),
                   final_results_identical=True, samples=samples)
        rows.append(row)
        print(json.dumps({key: row[key] for key in ('case', 'before_ms', 'after_ms', 'median_speedup')}), flush=True)
    report = dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
        seed=20261003, repeats=args.repeats,
        scope=({'scene': 'Both use merged steps; only actual native scene simulate and empty-report writeback consolidation differ. ',
                'steps': 'Only the fused setters/RNG/position reads and batch pose writeback differ; both use native RNG and lean prediction. ',
                'merged': 'Both use native RNG and the exact native step bridge; only merged per-step report/mask work, dispatch and frame loop differ. ',
                'random': 'Only RNG/noise mapping differs; both use existing lean steps and native projection. '}[stage])+
              'Alternating warm requests including scene reset, full scheduled play, 16-state extraction and JSON. No profiler/concurrent benchmark workers.',
        source_sha256={str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in
            (ROOT/'local_simulator/unity_prediction.py', ROOT/'local_simulator/native_random.py', ROOT/'local_simulator/runtime/unity_random.c', ROOT/'local_simulator/runtime/unity_random.dll',
             ROOT/'local_simulator/unity_physx.py', ROOT/'local_simulator/native_step_bridge.py', ROOT/'local_simulator/runtime/unity_step_bridge.c', ROOT/'local_simulator/runtime/unity_step_bridge.dll')}, rows=rows)
    args.output.write_text(json.dumps(report, indent=2), encoding='utf8')


if __name__ == '__main__':
    main()
