"""Store/compare all fixed-step body bytes before and after optimization."""
import argparse,base64,hashlib,json,struct,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
from local_simulator.unity_prediction import UnityPredictionDriver,UnityPredictionClock

def main():
    p=argparse.ArgumentParser();p.add_argument('--baseline',action='store_true');args=p.parse_args()
    install_bundled_pyphysx();rows=[]
    cases=[('free',[3.,0.,0.],[]),('hit',[3.4,0.,0.],[(2,2.375,5.2)]),
           ('wall',[4.1,0.,0.],[(2,1.875,5.6)]),('spin',[3.35,.18,9.42],[(2,2.375,6.7)]),
           ('dense',[3.35,0.,0.],[(1,2.375,7.15),(3,2.375,4.88),(5,1.92,6.12),(7,2.83,6.12)])]
    for name,shot,stones in cases:
        env=StrictCurlingEnd(seed=20261003);scene=env.scene
        positions=[0.]*32
        for k,x,y in stones:positions[2*k:2*k+2]=[x,y]
        scene.reset_positions(positions,yaw_overrides={k:0. for k in range(16)})
        scene.start_bestshot(0,shot,yaw=0.)
        driver=UnityPredictionDriver(scene,0,seed=20261003,motion_stepper=env.motion_stepper)
        # Subsequent versions expose the production lean path; baseline uses
        # the current audit path. Independent fixtures still validate Unity.
        if not args.baseline and hasattr(driver,'use_lean_steps'):
            driver.use_lean_steps=True
        raw=bytearray()
        def snapshot():
            for k,slot in enumerate(scene.slots):
                state=scene.raw_native_state(k);q=state['quaternionWxyz']
                raw.extend(struct.pack('<15fBB',*state['physxPosition'],*q[1:],q[0],
                    *state['physxLinearVelocity'],*state['physxAngularVelocity'],
                    slot.material.get_static_friction(),slot.material.get_dynamic_friction(),
                    slot.enabled,slot.body.is_sleeping()))
            raw.extend(struct.pack('<IIBB4I',driver.fixed_count,driver.draw_count,driver.collided,driver.ongoing,
                                   driver.rng.s0,driver.rng.s1,driver.rng.s2,driver.rng.s3))
        snapshot()
        driver.clock.begin_frame(.33)
        while driver.clock.take_fixed_step():
            driver.fixed_update();snapshot()
        driver.update();snapshot()
        assert not driver.ongoing,name
        row=dict(case=name,shot=shot,stones=stones,result=driver.result(),
                 bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),trace=base64.b64encode(zlib.compress(raw)).decode())
        rows.append(row);print(name,len(raw),row['sha256'],flush=True)
    path=ROOT/'analysis_input/prediction_optimization_baseline_20261003.json'
    if args.baseline:
        path.write_text(json.dumps(dict(rows=rows,sourceSha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
             for p in (ROOT/'local_simulator/unity_physx.py',ROOT/'local_simulator/unity_prediction.py')}),indent=2))
    else:
        old=json.loads(path.read_text());comparison=[]
        for before,after in zip(old['rows'],rows):
            assert before['case']==after['case']
            a=zlib.decompress(base64.b64decode(before['trace']));b=zlib.decompress(base64.b64decode(after['trace']))
            assert a==b,(after['case'],next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),None))
            assert before['result']==after['result'],after['case']
            comparison.append({k:after[k] for k in ('case','bytes','sha256','result')})
        (ROOT/'analysis_input/prediction_optimization_comparison_20261003.json').write_text(json.dumps(dict(allBytesMatch=True,rows=comparison),indent=2))
if __name__=='__main__':main()
