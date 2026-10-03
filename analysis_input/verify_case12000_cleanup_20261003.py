"""Verify the observed collision caller and the arithmetic-preserving probe."""
import json
from pathlib import Path
import struct
import validate_multiple_cases_20261002 as validation
from validate_additional_cases_20261002 import check_observer
from verify_pcm_internal_trace import raw_argument

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis_input'
WORK=BASE/'additional_case_validation_20261002'
CAP=BASE/'case12000_cleanup_unity_v4_20261003'

def boundaries(path):
    rows=[r for r in validation.rows(path,'a12.tail_phase_core')
        if r['phase']=='DCP.FixedUpdate.boundary' and r['edge']=='enter']
    first=rows[0];active=first['mainCorePtr']
    target=next(c['corePtr'] for c in first['cores'] if c['corePtr']!=active)
    names={active:'active',target:'target'}
    return {r['solverSerial']:{names[c['corePtr']]:c['bits'] for c in r['cores']} for r in rows}

def main():
    path=validation.event_path(CAP)
    manifest=json.loads((CAP/'capture_manifest.json').read_text())
    observer=check_observer(CAP,WORK/'additional12000_original_control',manifest,
        BASE/'cos_repair_regression_20261003/additional12000_native.json')
    a=boundaries(path);b=boundaries(validation.event_path(WORK/'additional12000_unity'))
    assert sorted(a)==list(range(1901)) and all(a[t]==b[t] for t in a)
    calls=list(validation.rows(path,'a12.pcm_internal_call'));by={r['callId']:r for r in calls}
    removal=next(r for r in calls if r['functionIndex']==71727 and r.get('ordinal',0)>1)
    chain=[removal]
    while chain[-1].get('parentCallId') is not None:
        chain.append(by[chain[-1]['parentCallId']])
    collision=next(r for r in chain if r['functionIndex']==61030)
    def ancestor(r):
        while r.get('parentCallId') is not None:
            r=by[r['parentCallId']]
            if r['callId']==collision['callId']:return True
        return False
    inside=[r for r in calls if ancestor(r)]
    tag_constants=collision['collisionTagConstants']
    assert [(r['globalAddress'],r['text']) for r in tag_constants]==[(3837100,'Stone'),(3843892,'Wall')]
    material=[r for r in inside if r['functionIndex'] in (32511,32512)]
    assert len(material)==2
    assert [r['functionIndex'] for r in material]==[32511,32512]
    assert all(struct.pack('<f',r['args'][1])==struct.pack('<f',0.6) for r in material)
    zero=[r for r in inside if r['functionIndex'] in (32521,32524)]
    assert [r['functionIndex'] for r in zero]==[32521,32524]
    assert all(raw_argument(r,1,'before')[:12]==bytes(12) for r in zero)
    activation=next(r for r in inside if r['functionIndex']==54405)
    assert activation['args'][1]==0
    assert material[-1]['callId']<zero[0]['callId']<zero[1]['callId']<activation['callId']<removal['callId']
    assert all('active' in a[t] for t in range(1879))
    assert all('active' not in a[t] for t in range(1879,1901))
    p0before=raw_argument(collision,0,'before');p0after=raw_argument(collision,0,'after')
    assert p0before[16]==0 and p0after[16]==1
    proof=dict(sampleId=12000,completedStep=1879,
        actualRemovalCallerChain=[{k:r.get(k) for k in ('callId','parentCallId','functionIndex','ordinal','args')} for r in reversed(chain)],
        observedCollisionRoot={k:collision.get(k) for k in ('callId','ordinal','functionIndex','args','collisionTagConstants')},
        branch='f61030 second tag-comparison branch: Wall. The observed zero setters and SetActive(false) are exclusive to this branch in the original WAT.',
        callbackFunctions=[{k:r.get(k) for k in ('callId','parentCallId','functionIndex','args')} for r in material+zero+[activation,removal]],
        collisionFlagBeforeAndAfter=[p0before[16],p0after[16]],
        observer=dict(observer,completedBoundarySetsAndStateWordsUnchanged=1901),
        productionChanged=False,
        invalidEarlierCaptures={'case12000_cleanup_unity_20261003':'No release/Reset physics window captured.',
            'case12000_cleanup_unity_v2_20261003':'Event export timed out at step1643; missing cleanup window, not used as cause proof.',
            'case12000_cleanup_unity_v3_20261003':'Polling stalled before release; stopped this capture tree, not used as cause proof.'},
        evidence={str(p.relative_to(ROOT)):validation.digest(p) for p in [path,CAP/'capture_manifest.json',
            CAP/'observer_source.js',BASE/'pcm_functions_20261001/f61030.wat',
            BASE/'pcm_functions_20261001/f54405.wat',BASE/'unity_20260930.wasm',Path(__file__)]})
    out=BASE/'case12000_cleanup_verified_20261003.json'
    out.write_text(json.dumps(proof,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps(proof,ensure_ascii=False))

if __name__=='__main__':main()
