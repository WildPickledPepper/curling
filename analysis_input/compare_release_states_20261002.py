"""Sequential discrete state comparison; no tolerances or inferred equality."""
import argparse,json,sys
from pathlib import Path
from verify_pcm_internal_trace import events,rows_of
from verify_reset_internal_alignment_20261002 import words

ROOT=Path(__file__).resolve().parents[1]
def compare(native_path,capture):
    rows,path=events(capture)
    native=json.loads(native_path.read_text())
    pre={r['ordinal']:r for r in rows_of(rows,'a12.dense_pre_angular_setter')}
    post={r['ordinal']:r for r in rows_of(rows,'a12.dense_post_angular_setter')}
    getters={}
    for r in rows_of(rows,'a12.velocity_getter_native'):
        key=(r['ordinal'],r['kind'])
        if key in getters:assert getters[key]['outputBits']==r['outputBits']
        getters[key]=r
    states={i:words(p['pose']['p']+p['pose']['q'])+
        getters[(i,'velocity')]['outputBits']+getters[(i,'angularVelocity')]['outputBits']
        for i,p in pre.items() if (i,'velocity') in getters and (i,'angularVelocity') in getters}
    assert native['releaseBits']==states[2]
    noises=[r['value'] for r in rows_of(rows,'sliding.random_range.friction')]
    setters={r['ordinal']:r for r in native['setters'] if r['name']=='set_angular_velocity'}
    exact=0;first=None
    for frame in native['frames']:
        i=frame['ordinal'];tick=i-1
        assert frame['noise']==noises[tick-1]
        assert states[i]==(native['releaseBits'] if tick==1 else native['frames'][tick-2]['afterBits']),('entry',tick)
        assert setters[i]['inputBits']==post[i]['bridge164Bits'],('angular setter',tick)
        if i+1 not in states:break
        u,n=states[i+1],frame['afterBits']
        dif=[j for j,(a,b) in enumerate(zip(u,n)) if a!=b]
        if dif:
            first=dict(slidingTick=tick,denseOrdinal=i,wordIndices=dif,
                       unityWords=u,nativeWords=n,
                       differences=[dict(index=j,unity=hex(u[j]),native=hex(n[j])) for j in dif])
            break
        exact+=1
    return dict(continuousPostReleaseStateTicksExact=exact,
        continuousPostReleaseStateWordsExact=exact*13,nextConfirmedDivergence=first,
        comparedStatesAvailable=len(states),unityEvents=str(path))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True)
    p.add_argument('--capture',type=Path,default=ROOT/'analysis_input/unity_first_release_chain_complete_capture_20261002')
    p.add_argument('--output',type=Path);o=p.parse_args();r=compare(o.native,o.capture)
    if o.output:o.output.write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
