"""Measure the delivered scene + BESTSHOT -> stopped-scene prediction path.

Run with a bundled-pyphysx compatible Python, from the repository root:
  python local_simulator/examples/benchmark_prediction_time.py --repeats 10

No profiler, Unity friction stream, or shortened simulation is used. Request
latency includes resetting the supplied scene, play(), and JSON serialization.
"""
from __future__ import annotations

import time
ENTRY_TIME = time.perf_counter()

import argparse
import hashlib
import json
import platform
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def summary(values):
    ordered = sorted(values)
    def percentile(q):
        i = (len(ordered)-1)*q
        lo = int(i)
        hi = min(lo+1,len(ordered)-1)
        return ordered[lo]+(ordered[hi]-ordered[lo])*(i-lo)
    return dict(mean=statistics.mean(values),median=statistics.median(values),
                p95=percentile(.95),min=ordered[0],max=ordered[-1])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats',type=int,default=10)
    parser.add_argument('--seed',type=int,default=20261003)
    parser.add_argument('--cpu',default=platform.processor())
    parser.add_argument('--output',type=Path,default=ROOT/'analysis_input/prediction_timing_20261003.json')
    args=parser.parse_args()
    if args.repeats<1:
        parser.error('--repeats must be positive')

    started=time.perf_counter()
    from local_simulator.runtime_loader import install_bundled_pyphysx
    install_bundled_pyphysx()
    from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
    imports_ms=(time.perf_counter()-started)*1000
    started=time.perf_counter()
    env=StrictCurlingEnd(seed=args.seed)
    initialization_ms=(time.perf_counter()-started)*1000

    defence=json.loads((ROOT/'planning_proxy/fixtures/actual_final_defence_smoke.json').read_text())
    cases=[
        dict(name='free',label='无碰撞直线',shot=[3.,0.,0.],stones=[]),
        dict(name='stone_collision',label='撞击一只目标壶',shot=[3.4,0.,0.],
             stones=[dict(index=2,x=2.375,y=5.2,yaw=0.)]),
        dict(name='wall',label='滑行至墙碰停用',shot=[4.1,0.,0.],
             stones=[dict(index=2,x=1.875,y=5.6,yaw=0.)]),
        dict(name='spin',label='高旋绕壶',shot=[3.35,.18,9.42],
             stones=[dict(index=2,x=2.375,y=6.7,yaw=0.)]),
        dict(name='four_stone_scene',label='四壶防守场景',shot=[3.35,0.,0.],stones=defence),
    ]

    def predict(case):
        # Inputs are available before the timer, as in a parsed API request.
        positions=[0.]*32
        yaws={k:0. for k in range(16)}
        for stone in case['stones']:
            k=int(stone['index'])
            positions[2*k:2*k+2]=[float(stone['x']),float(stone['y'])]
            yaws[k]=float(stone.get('yaw',0.))
        wall_start=time.perf_counter()
        cpu_start=time.process_time()
        env.scene.reset_positions(positions,yaw_overrides=yaws)
        env.shot_number=0
        reset_end=time.perf_counter()
        result=env.play(case['shot'])
        play_end=time.perf_counter()
        response=json.dumps(result,ensure_ascii=False,separators=(',',':'))
        finished=time.perf_counter()
        cpu_ms=(time.process_time()-cpu_start)*1000
        if not result['settled']:
            raise RuntimeError('incomplete prediction must not be counted as stopped')
        timing=dict(request_ms=(finished-wall_start)*1000,
                    scene_reset_ms=(reset_end-wall_start)*1000,
                    predict_and_extract_ms=(play_end-reset_end)*1000,
                    json_ms=(finished-play_end)*1000,cpu_ms=cpu_ms,
                    fixed_steps=result['fixedSteps'],friction_draws=result['frictionDraws'],
                    updates=result['updates'],contact=result['contact'],settled=result['settled'],
                    active_enabled=result['states'][0]['enabled'],response_bytes=len(response.encode()))
        return timing,result

    first_timing,first_result=predict(cases[0])
    cold_ready_ms=(time.perf_counter()-ENTRY_TIME)*1000
    rows=[]
    for case in cases:
        predict(case)  # One untimed warm-up for each scenario.
        timings=[]
        for _ in range(args.repeats):
            timing,result=predict(case)
            timings.append(timing)
        row={**case,'runs':timings,'last_final_scene':result['states'],
             'summary_ms':{key:summary([r[key] for r in timings]) for key in
                           ('request_ms','scene_reset_ms','predict_and_extract_ms','json_ms','cpu_ms')}}
        rows.append(row)
        print(json.dumps(dict(case=case['name'],request_ms=row['summary_ms']['request_ms'],
                              fixed_steps=timings[-1]['fixed_steps'],friction_draws=timings[-1]['friction_draws']),ensure_ascii=False),flush=True)

    report=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                environment=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),cpu=args.cpu),
                seed=args.seed,repeats=args.repeats,
                scope='Current exact scheduled non-sweep prediction; warm request includes scene reset, complete play, 16-stone state extraction and JSON serialization; file/network output excluded. No concurrent benchmark workers.',
                clock=dict(frame_elapsed=env.prediction_frame_elapsed,time_scale=env.prediction_time_scale),
                cold=dict(from_script_entry_to_first_response_ms=cold_ready_ms,
                          imports_and_runtime_ms=imports_ms,scene_initialization_ms=initialization_ms,
                          first_request=first_timing,first_final_scene=first_result['states']),
                implementation_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                  (ROOT/'local_simulator/unity_prediction.py',ROOT/'local_simulator/unity_physx.py',
                   ROOT/'local_simulator/examples/train_policy_tree_selfplay.py',
                   ROOT/'local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd')},cases=rows)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(dict(cold_ms=cold_ready_ms,output=str(args.output)),ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
