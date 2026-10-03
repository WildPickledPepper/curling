"""Profile original prediction hot calls without changing physics."""
import cProfile,pstats,sys,time,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx
from local_simulator.examples.train_policy_tree_selfplay import StrictCurlingEnd
install_bundled_pyphysx()
env=StrictCurlingEnd(seed=20261003);env.reset()
profile=cProfile.Profile();profile.enable()
started=time.perf_counter();result=env.play([3.,0.,0.]);elapsed=time.perf_counter()-started
profile.disable()
profile.dump_stats(str(ROOT/'analysis_input/prediction_before_optimization_20261003.prof'))
with (ROOT/'analysis_input/prediction_before_optimization_20261003.profile.txt').open('w') as stream:
    pstats.Stats(profile,stream=stream).strip_dirs().sort_stats('cumulative').print_stats(40)
print(json.dumps(dict(elapsed=elapsed,result={k:v for k,v in result.items() if k!='states'})))
