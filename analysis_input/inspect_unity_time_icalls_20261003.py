import json,struct
from pathlib import Path
from instrument_pcm_calls import Reader,sections
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'analysis_input/unity_20260930.wasm').read_bytes();sec=dict(sections(src))
r=Reader(sec[11]);segments=[]
for _ in range(r.uint()):
    flag=r.uint();assert flag==0
    assert r.byte()==65;start=r.uint();assert r.byte()==11
    segments.append((start,r.take(r.uint())))
r=Reader(sec[9]);tables={}
for _ in range(r.uint()):
    assert r.uint()==0;assert r.byte()==65;start=r.uint();assert r.byte()==11
    tables.update({start+i:r.uint() for i in range(r.uint())})
for address in (319343,345824,345157,339436):
    s,raw=next((s,b) for s,b in segments if s<=address<s+len(b));i=address-s
    print(address,raw[i:raw.index(b'\0',i)].decode())
    for base,data in segments:
        pos=0
        while True:
            pos=data.find(struct.pack('<I',address),pos)
            if pos<0:break
            around=[struct.unpack_from('<I',data,j)[0] for j in range(max(0,pos-8),min(len(data)-3,pos+12),4)]
            print(dict(memoryAddress=base+pos,words=around,possibleFunctions={k:tables[k] for k in around if k in tables}));pos+=4
