import json
from pathlib import Path
from verify_pcm_internal_trace import raw_argument

p = next(Path('analysis_input/case12000_cleanup_unity_v4_20261003/logs').glob('*/events.jsonl'))
for line in p.open():
    row = json.loads(line)
    if row['type'] != 'a12.pcm_internal_call':
        continue
    r = row['data']
    if 175 <= r['callId'] <= 205:
        print(r['callId'], r['functionIndex'], r.get('parentCallId'), r['args'])
        if r['functionIndex'] == 72606:
            import struct
            print('POSE', struct.unpack('<7f', raw_argument(r, 1, 'before')[:28]))
            if r['callId'] == 192:
                q, position = raw_argument(r, 1, 'before')[:16], raw_argument(r, 1, 'before')[16:28]
                Path('analysis_input/case12000_callback_pose_20261003.json').write_text(json.dumps(dict(
                    callId=192, functionIndex=72606, parentCallId=r['parentCallId'],
                    poseWords=list(struct.unpack('<7I', position+q)),
                    eventsPath=str(p)), indent=2))
