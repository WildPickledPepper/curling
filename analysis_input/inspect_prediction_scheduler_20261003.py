"""Extract exact controller/time wrappers and their callers from original WAT."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis_input/scheduler_functions_20261003'
IDS={54530,54555,54556,54557,61094,61097,61107,82288,82289,82290,82291}
IDS.update(range(78640,78701))
IDS.add(80140)
IDS.update({61089, 79750, 77913})
IDS.update(range(79745,79756))
def main():
    OUT.mkdir(exist_ok=True);src=ROOT/'analysis_input/unity_20260930.wat'
    header=re.compile(r'^  \(func \$f(\d+)\b');current=None;lines=[];callers={i:[] for i in IDS};metadata=[]
    def flush():
        if current in IDS:
            path=OUT/('f'+str(current)+'.wat');path.write_text(''.join(lines),encoding='utf8')
            metadata.append(dict(functionIndex=current,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    for n,line in enumerate(src.open(encoding='utf8'),1):
        if line.startswith('  (data') or line.startswith('  (elem'):flush();break
        match=header.match(line)
        if match:flush();current=int(match[1]);lines=[]
        if current in IDS:lines.append(line)
        match=re.search(r'\bcall \$f(\d+)\b',line)
        if match and int(match[1]) in IDS:callers[int(match[1])].append(dict(caller=current,line=n))
    result=dict(sourceWasmSha256=hashlib.sha256((ROOT/'analysis_input/unity_20260930.wasm').read_bytes()).hexdigest(),functions=metadata,callers=callers)
    (OUT/'manifest.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(callers,indent=2))
if __name__=='__main__':main()
