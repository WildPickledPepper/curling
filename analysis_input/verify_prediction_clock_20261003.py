"""Execute original TimeManager WAT functions against the Python clock."""
import hashlib,json,random,re,struct,sys
from pathlib import Path
import wasmtime
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_simulator.unity_prediction import UnityPredictionClock

def main():
    sources=[]
    for index in (79750,77913,80140):
        path=ROOT/f'analysis_input/scheduler_functions_20261003/f{index}.wat'
        sources.append(re.sub(r'\(type \$t\d+\) ', '', path.read_text()))
    wat='(module (memory (export "memory") 74)'+''.join(sources)+'''
    (export "frame" (func $f79750)) (export "fixed" (func $f77913)))'''
    engine=wasmtime.Engine();store=wasmtime.Store(engine)
    module=wasmtime.Module(engine,wasmtime.wat2wasm(wat))
    instance=wasmtime.Instance(store,module,[]);exports=instance.exports(store)
    memory=exports['memory'];ptr=1024
    memory.write(store,struct.pack('<I',ptr),4782140+7*4)
    rng=random.Random(20261003);checks=0;counts=[]
    intervals=[.33]*100+[0.,1e-7,1e-5,.01,.02,.33000003,1.,.002]*10
    intervals += [rng.uniform(0,.6) for _ in range(250)]
    for scale in (96.,16.,4.,1.,1.0000005,0.):
        memory.write(store,bytes(1100),ptr)
        clock=UnityPredictionClock(time_scale=scale)
        for offset,value in ((56,clock.fixed_dt),(236,clock.time_scale),(240,clock.maximum_delta)):
            memory.write(store,struct.pack('<f',value),ptr+offset)
        for elapsed in intervals:
            clock.begin_frame(elapsed)
            exports['frame'](store,ptr,clock.realtime)
            native_count=0
            while exports['fixed'](store):native_count+=1
            local_count=0
            while clock.take_fixed_step():local_count+=1
            assert native_count==local_count,(scale,elapsed,native_count,local_count)
            for offset,value in ((80,clock.frame_time),(32,clock.fixed_time),(208,clock.time_offset)):
                actual=bytes(memory.read(store,ptr+offset,ptr+offset+8))
                assert actual==struct.pack('<d',value),(scale,elapsed,offset,actual.hex(),struct.pack('<d',value).hex())
            checks+=1
            if scale==96. and len(counts)<8:counts.append(local_count)
    result=dict(sourceWasmSha256=hashlib.sha256((ROOT/'analysis_input/unity_20260930.wasm').read_bytes()).hexdigest(),
                functions=[dict(index=i,sha256=hashlib.sha256((ROOT/f'analysis_input/scheduler_functions_20261003/f{i}.wat').read_bytes()).hexdigest()) for i in (79750,77913,80140)],
                framesCompared=checks,fieldsComparedBitwise=['frameTime@80','fixedTime@32','timeOffset@208'],
                fixedCountsMatched=True,initialSaturatedFrameCounts=counts,
                scope='Same initial running/unpaused clock inputs; original WAT arithmetic executed by wasmtime. No assertion about unsampled browser wall-clock history.')
    path=ROOT/'analysis_input/prediction_clock_validation_20261003.json'
    path.write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
