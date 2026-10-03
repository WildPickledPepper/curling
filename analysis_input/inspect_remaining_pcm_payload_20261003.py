import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'research_archive/unity_reverse/evidence/log/a0_actor_cache_20260711/unity_runtime_probe_20260711_191604/events.jsonl'
for line in p.open(encoding='utf8'):
    if 'PxcPCMContactConvexConvex' not in line:continue
    e=json.loads(line)
    if e['type'] not in ('physx.native.before','physx.native.after') or e['data']['hook']['wasm']!='func70576':continue
    d=e['data'];pcm=next(x for x in d['extraDumps'] if x['label'].endswith('.pcmInputs'))
    def brief(x):
        if isinstance(x,dict):return {k:brief(v) for k,v in x.items() if k not in ('hexPreview','u32Preview','f32Preview','pointerTargets')}
        if isinstance(x,list):return dict(length=len(x),first=x[:20]) if len(x)>100 and not isinstance(x[0],dict) else [brief(v) for v in x]
        return x
    print(json.dumps(dict(type=e['type'],data={k:brief(pcm[k]) for k in ('transform0','transform1','narrowPhaseParams','cache','contactBuffer')}),indent=2)[:17000])
    if e['type']=='physx.native.before':
        (ROOT/'analysis_input/remaining_pcm_first_input_20261003.json').write_text(json.dumps(pcm),encoding='utf8')
