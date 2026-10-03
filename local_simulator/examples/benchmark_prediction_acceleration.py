"""Alternate reference and optimized prediction requests in one process."""
from __future__ import annotations
import argparse,hashlib,json,platform,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from local_simulator.examples.benchmark_prediction_time import summary
from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repeats',type=int,default=10)
    parser.add_argument('--output',type=Path,default=ROOT/'analysis_input/prediction_acceleration_timing_20261003.json')
    args=parser.parse_args()
    if args.repeats<1:parser.error('--repeats must be positive')
    install_bundled_pyphysx()
    before=StrictCurlingEnd(seed=20261003,training_fast=False)
    before.scene._native_angular_projection=None
    after=StrictCurlingEnd(seed=20261003,training_fast=True)
    if after.scene._native_angular_projection is None:
        raise RuntimeError('native projection must be installed to measure both optimizations')
    cases=[('free',[3.,0.,0.],[]),('hit',[3.4,0.,0.],[(2,2.375,5.2)]),
           ('wall',[4.1,0.,0.],[(2,1.875,5.6)]),('spin',[3.35,.18,9.42],[(2,2.375,6.7)]),
           ('dense',[3.35,0.,0.],[(1,2.375,7.15),(3,2.375,4.88),(5,1.92,6.12),(7,2.83,6.12)])]
    rows=[]
    def run(env,shot,positions):
        start=time.perf_counter();cpu=time.process_time()
        env.scene.reset_positions(positions,yaw_overrides={k:0. for k in range(16)})
        env.shot_number=0
        result=env.play(shot)
        serialized=json.dumps(result,sort_keys=True,separators=(',',':'))
        duration=(time.perf_counter()-start)*1000
        cpu_duration=(time.process_time()-cpu)*1000
        assert result['settled']
        return dict(ms=duration,cpu_ms=cpu_duration,sha256=hashlib.sha256(serialized.encode()).hexdigest()),result
    for name,shot,stones in cases:
        positions=[0.]*32
        for k,x,y in stones:positions[2*k:2*k+2]=[x,y]
        for _ in range(2):
            run(before,shot,positions);run(after,shot,positions)
        samples=[]
        for index in range(args.repeats):
            if index%2:
                a,old=run(before,shot,positions);b,new=run(after,shot,positions)
            else:
                b,new=run(after,shot,positions);a,old=run(before,shot,positions)
            assert old==new,(name,index)
            samples.append(dict(before=a,after=b,speedup=a['ms']/b['ms']))
        baseline=summary([s['before']['ms'] for s in samples]);optimized=summary([s['after']['ms'] for s in samples])
        row=dict(case=name,shot=shot,stones=stones,samples=samples,before_ms=baseline,after_ms=optimized,
                 median_speedup=baseline['median']/optimized['median'],
                 paired_speedup=summary([s['speedup'] for s in samples]),final_results_identical=True,
                 fixedSteps=new['fixedSteps'],frictionDraws=new['frictionDraws'],updates=new['updates'])
        rows.append(row);print(json.dumps({k:row[k] for k in ('case','before_ms','after_ms','median_speedup')},ensure_ascii=False),flush=True)
    report=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),seed=20261003,repeats=args.repeats,
                scope='Reference: audit snapshots and Python float32 projection. Optimized: lean snapshots and exact native projection. Identical clock, native PhysX, reset and request serialization; modes alternate sequentially, no profiler or concurrent workers.',
                source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                  (ROOT/'local_simulator/unity_physx.py',ROOT/'local_simulator/unity_prediction.py',
                   ROOT/'local_simulator/runtime/unity_angular_projection.dll')},rows=rows)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(str(args.output),flush=True)
if __name__=='__main__':main()
