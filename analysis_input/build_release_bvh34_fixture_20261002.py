"""Save an independently captured Unity tick-526 regression, without native values."""
import hashlib,json,struct
from pathlib import Path
from verify_pcm_internal_trace import events,rows_of,raw_argument
from verify_reset_internal_alignment_20261002 import words

ROOT=Path(__file__).resolve().parents[1]
rows,path=events(ROOT/'analysis_input/unity_release_526_chain_capture_20261002')
pre={r['ordinal']:r for r in rows_of(rows,'a12.dense_pre_angular_setter')}
getters={(r['ordinal'],r['kind']):r for r in rows_of(rows,'a12.velocity_getter_native')}
def state(i):return words(pre[i]['pose']['p']+pre[i]['pose']['q'])+getters[i,'velocity']['outputBits']+getters[i,'angularVelocity']['outputBits']
export=next(r for r in rows_of(rows,'a12.pcm_internal_call') if r['functionIndex']==69979 and r.get('ordinal')==527)
buf=raw_argument(export,1,'after')
result=dict(unityWasmSha256=hashlib.sha256((ROOT/'analysis_input/unity_20260930.wasm').read_bytes()).hexdigest(),
    evidence=str(path.relative_to(ROOT)),eventsSha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    resetPositions=[0,0,0,0,2.375,5.2]+[0]*26,bestshot=[3.4,0,0],slidingTick=526,
    releaseBits=state(2),beforeBits=state(527),afterBits=state(528),
    contactFloatWords=[list(struct.unpack_from('<7I',buf,i*64)) for i in range(6)],
    frictionInputs=[r['value'] for r in rows_of(rows,'sliding.random_range.friction')][:526])
out=ROOT/'local_simulator/tests/fixtures/unity_release_tick526_20261002.json'
out.write_text(json.dumps(result,indent=2))
print(out)
