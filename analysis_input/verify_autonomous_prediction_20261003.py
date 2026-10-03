"""Prediction repeatability; not a substitute for Unity byte comparisons."""
import hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.tests.test_unity_target_activation import state_words

def main():
    install_bundled_pyphysx();rows=[]
    cases=[('free',(3.,0.,0.),[]),('hit',(3.4,0.,0.),[(2,2.375,5.2)]),
           ('wall',(4.1,0.,0.),[(2,1.875,5.6)]),('spin',(3.35,.18,9.42),[(2,2.375,6.7)])]
    for name,shot,targets in cases:
        repeats=[]
        for _ in range(2):
            env=StrictCurlingEnd(seed=20261003)
            positions=[0.]*32
            for k,x,y in targets:positions[2*k:2*k+2]=[x,y]
            env.scene.reset_positions(positions)
            result=env.play(shot)
            words=sum((state_words(env.scene,k) for k in range(16)),[])
            result.pop('states');result['stateBytesSha256']=hashlib.sha256(struct.pack('<208I',*words)).hexdigest()
            repeats.append(result)
        assert repeats[0]==repeats[1],(name,repeats)
        rows.append(dict(case=name,shot=shot,seed=20261003,repeatsMatch=True,result=repeats[0]))
    # This checks persistent 16-shot Scene progression, including collision tails.
    env=StrictCurlingEnd(seed=20261003);env.reset();game=[]
    for tick in range(16):
        result=env.play((3.1+(tick%3)*.15,(-1 if tick%2 else 1)*.12,(tick%3-1)*3.14))
        game.append({key:result[key] for key in ('settled','contact','frictionDraws','fixedSteps','updates')})
    report=dict(scope='Local autonomous repeatability and persistent-scene smoke; not Unity equivalence evidence',cases=rows,complete16ShotGame=game)
    (ROOT/'analysis_input/autonomous_prediction_validation_20261003.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
if __name__=='__main__':main()
