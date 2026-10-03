"""Extract and hook actual direct callees of the first stone PCM function."""
import json
import argparse
import mmap
import re
from pathlib import Path
from instrument_pcm_calls import instrument

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--depth',type=int,default=2)
parser.add_argument('--output',type=Path,default=Path('analysis_input/unity_stone_pair_calls_20261002.wasm'))
parser.add_argument('--pair-registration',action='store_true')
opts=parser.parse_args()
wat=root/'analysis_input/unity_20260930.wat'
out=root/'analysis_input/pcm_functions_20261001'
with wat.open('rb') as handle:
    with mmap.mmap(handle.fileno(),0,access=mmap.ACCESS_READ) as data:
        def body(index):
            start=data.find(('  (func $f'+str(index)+' ').encode())
            assert start>=0,index
            end=data.find(b'\n  (func ',start+5)
            assert end>start,index
            result=data[start:end]
            (out/('f'+str(index)+'.wat')).write_bytes(result)
            return result
        ids={70576,71692} if opts.pair_registration else {70576}
        frontier=set(ids)
        for depth in range(opts.depth):
            found=set()
            for fid in frontier:
                found.update(int(i) for i in re.findall(rb'call \$f(\d+)',body(fid)))
            frontier=found-ids
            ids.update(found)
        for fid in sorted(ids):
            body(fid)
source=root/'analysis_input/unity_20260930.wasm'
patched,manifest=instrument(source.read_bytes(),sorted(ids))
target=(root/opts.output).resolve()
assert not target.exists()
target.write_bytes(patched)
manifest.update(source=str(source),patched=str(target),scope='stone-pair')
if opts.pair_registration:
    manifest['upstreamRootFunctions']=[71692]
target.with_suffix('.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'functions':sorted(ids),'patched':str(target)}))
