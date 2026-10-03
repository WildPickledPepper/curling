"""Inspect every still-uncompared capture, retaining actual payload schemas."""
from collections import Counter
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
TYPE=re.compile(rb'"type"\s*:\s*"([^"\n]+)"')
NUMERIC_KEYS={'rawBytes','f32','u32','f32Preview','u32Preview','velocity','angularVelocity','rotation','position','q','p','outputBits','inputBits','hexPreview'}

def numeric_fields(value,prefix='data'):
    """Record candidate numeric evidence, without claiming the bytes are defined fields."""
    if not isinstance(value,dict):return []
    found=[]
    for key,item in value.items():
        path=prefix+'.'+key
        if key in NUMERIC_KEYS and isinstance(item,(dict,list,str)) and item:found.append(path)
        if isinstance(item,dict):found.extend(numeric_fields(item,path))
        elif isinstance(item,list):
            for i,entry in enumerate(item):
                if isinstance(entry,dict):found.extend(numeric_fields(entry,path+'['+str(i)+']'))
    return found
def schema(value,depth=0):
    if depth>3:return type(value).__name__
    if isinstance(value,dict):return {k:schema(v,depth+1) for k,v in value.items()}
    if isinstance(value,list):return dict(length=len(value),first=schema(value[0],depth+1) if value else None)
    if isinstance(value,str):return dict(type='str',length=len(value),preview=value[:120])
    return value
def main():
    report=json.loads((OUT/'report.json').read_text());review=[];total=Counter();raw=0;categories=Counter()
    for r in report['coverage']:
        if r['passedScopes']:continue
        counts=Counter();examples={};h=hashlib.sha256();numeric={};protocol=[]
        for n,line in enumerate((ROOT/r['path']).open('rb'),1):
            h.update(line);match=TYPE.search(line)
            if not match:continue
            kind=match[1].decode();counts[kind]+=1
            # Inspect all actual payloads: the first event may contain empty buffers.
            try:e=json.loads(line)
            except (ValueError,UnicodeError):continue
            if kind not in examples:
                examples[kind]=dict(line=n,payloadSchema=schema(e.get('data')))
            fields=numeric_fields(e.get('data'))
            if fields and kind not in numeric:numeric[kind]=dict(line=n,fields=fields)
            if kind in ('websocket.recv','websocket.send') and len(protocol)<4:
                protocol.append(dict(line=n,payloadSchema=schema(e.get('data'))))
        assert h.hexdigest()==r['sha256'];total.update(counts)
        has_raw=bool(r['existingRawEvidenceNeedingSpecificAdapter']);raw+=has_raw
        if has_raw:
            category='solverOrPcmAdapterOrSameCallInputsPending'
            reason='Recorded internal solver/PCM calls exist; standalone adapters or complete same-call inputs are still pending. See specific function and window exclusions.'
        elif numeric:
            category='otherNumericSnapshotsAdapterOrInputsPending'
            reason='Actual memory/vector snapshots exist; their defined fields, matching invocation inputs and simulator boundary still need a dedicated comparison. Absence of a whole trajectory is not an exclusion.'
        elif protocol:
            category='protocolOrSchedulingOnlyNoRecognizedNumericSnapshot'
            reason='Actual protocol/scheduling records inspected; no recognized internal numeric snapshot recorded. Protocol endpoints require a history-aware replay and are not marked passed.'
        else:
            category='installationOrSchedulingOnlyNoRecognizedNumericSnapshot'
            reason='Actual records inspected; no recognized numeric memory/vector window or received/sent protocol record. Installation records, pointer call arguments and empty tick counters do not prove simulator numeric equality.'
        categories[category]+=1
        review.append(dict(path=r['path'],eventsSha256=h.hexdigest(),actualEventCounts=dict(counts),
            firstActualPayloadPerType=examples,existingRawEvidenceNeedingSpecificAdapter=r['existingRawEvidenceNeedingSpecificAdapter'],
            reasonCategory=category,reason=reason,firstNumericCandidatePerType=numeric,firstProtocolRecords=protocol,
            excludedMeasuredInputWindows=r['legacyInputWindowsExcluded'],
            status='Reviewed actual payloads; no simulator numeric equality claim yet.'))
    output=dict(captures=len(review),capturesWithListedSolverPcmRawTypes=raw,
        reasonCategoryCounts=dict(categories),
        capturesOnlyProbeInstalled=sum(set(r['actualEventCounts'])=={'probe.installed'} for r in review),
        capturesWithoutThoseSpecificTypes=len(review)-raw,
        note='The latter count is not an unusable-capture count: other snapshots and protocol outputs still require their own checks.',
        actualEventCounts=dict(total),capturesInventory=review)
    (OUT/'remaining_capture_payload_review.json').write_text(json.dumps(output,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in output.items() if k!='capturesInventory'},indent=2))
if __name__=='__main__':main()
