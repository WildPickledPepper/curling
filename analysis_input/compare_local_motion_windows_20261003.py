"""Measured DCP getter/RNG input -> current friction kernel -> script setter."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis_input/local_partial_validation_20261003'
sys.path.insert(0,str(ROOT))
import local_simulator.unity_physx
from tools.reverse.recovered_curling_motion import B2Vec2, STEP, newfrictionstep, unity_friction

def bits(values):return list(struct.unpack('<%dI'%len(values),struct.pack('<%df'%len(values),*values)))

def controls(record):
    capture=(ROOT/record['path']).parent.parent.parent
    if capture.name=='evidence':return None
    for sample_file in sorted(capture.glob('*.jsonl')):
        try:
            samples=[json.loads(line) for line in sample_file.open(encoding='utf8') if line.strip()]
        except (ValueError,UnicodeError):continue
        if samples and all(s.get('sent_sweep') is False and
                          s.get('requested',{}).get('sweep')==0 for s in samples):
            if not any('SWEEP' in c['text'] for c in record['commands']):
                return dict(path=str(sample_file.relative_to(ROOT)),
                    sha256=hashlib.sha256(sample_file.read_bytes()).hexdigest(),
                    sampleCount=len(samples),sweepCommandsSent=False)
    return None

def main():
    inventory=json.loads((OUT/'inventory.json').read_text(encoding='utf8'))
    reports=[];totals=Counter();pending=[]
    for record in inventory['capturesInventory']:
        if not record['eventCounts'].get('a12.dense_pre_angular_setter'):continue
        control=controls(record)
        if not control:
            pending.append(dict(path=record['path'],reason='Sweep branch lacks a matched nonsweep sample manifest.'));continue
        count=exact=excluded=0;first=None
        with gzip.open(ROOT/record['selectedPath'],'rt',encoding='utf8') as f:
            for line in f:
                row=json.loads(line)
                if row['type']!='a12.dense_pre_angular_setter':continue
                d=row['data']
                if (d.get('getterLinear') is None or d.get('getterAngular') is None
                    or d.get('tickSerial') is None or d.get('lastFrictionNoise') is None):
                    excluded+=1;continue
                v=d['getterLinear'];w=d['getterAngular']
                result=newfrictionstep(unity_friction(False,noise=d['lastFrictionNoise']),
                    B2Vec2(-v[2],-v[0]),w[1],STEP)
                actual=bits([0.,result.angle,0.]);expected=bits(d['setterAngular'])
                count+=1
                if actual==expected:exact+=1
                elif first is None:
                    first=dict(line=row['line'],releaseSerial=d['releaseSerial'],ordinal=d['ordinal'],
                        nativeBits=actual,unityBits=expected,measuredGetterLinear=v,
                        measuredGetterAngular=w,measuredNoise=d['lastFrictionNoise'])
        report=dict(path=record['path'],unityEventsSha256=record['sha256'],control=control,
                    compared=count,exact=exact,different=count-exact,excludedNonSlidingSetters=excluded,
                    firstDifference=first)
        reports.append(report);totals.update(dict(compared=count,exact=exact,different=count-exact))
        print(json.dumps(dict(path=record['path'],compared=count,different=count-exact,firstDifference=first)),flush=True)
    result=dict(captures=len(reports),totals=dict(totals),capturesWithDifferences=sum(bool(r['firstDifference']) for r in reports),
        capturesInventory=reports,pendingCaptures=pending,
        sourceSha256=hashlib.sha256((ROOT/'local_simulator/runtime_support/tools/reverse/recovered_curling_motion.py').read_bytes()).hexdigest(),
        inputMappingEvidence='Original f60124: negate world z/x -> protocol vx/vy; promote world angular y; f32(base+noise), f59956, then f32-demote angle into setter.',
        scope='Only measured sliding-function inputs and sampled script angular output. No reconstructed historical scene, unobserved f64 intermediate or unrecorded linear output equality claim.')
    (OUT/'motion_windows.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(dict(captures=len(reports),totals=dict(totals),pending=len(pending)),indent=2),flush=True)

if __name__=='__main__':main()
