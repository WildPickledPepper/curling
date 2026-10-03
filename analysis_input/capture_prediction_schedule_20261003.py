"""Observe actual Update/FixedUpdate consumption, without changing RNG or clock."""
import hashlib,json,sys
from pathlib import Path
import capture_12011_first_solver as capture
from instrument_pcm_calls import instrument
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis_input/prediction_schedule_unity_v4_20261003'
PROBE=ROOT/'analysis_input/prediction_schedule_observer_20261003.js'
extra=r'''
  var scheduleHookTimer = global.setInterval(function installScheduleObserver() {
    if (!probe.tables.length) return;
    global.clearInterval(scheduleHookTimer);
    // Install before Unity caches script callback pointers during scene load.
    probe.installSlidingTraceHooks({maxRandomEvents:50000,maxFixedUpdateEvents:50000});
    probe.installA0FixedTickResolverHook({a10ReleaseOrientation:true,a12DenseReleaseSerial:2,a12DenseWriteLimit:5000});
    var fixedCount=0,frictionCount=0;
    function snapshot(args,edge) {
      var st=probe.a0FixedTickResolver || {}, memory=probe.memories[probe.memories.length-1];
      var view=memory && new DataView(memory.memory.buffer), ptr=Number(args[0]);
      return {edge:edge, functionIndex:61097, tableIndex:10970,controllerPtr:ptr,
        fixedCount:fixedCount, earlyFrictionCount:frictionCount,
        tickSerial:st.nextTickSerial, denseOrdinal:st.a12DenseWriteCount,
        frictionNoiseSerial:st.frictionNoiseSerial,manifestIndex:st.rngFrictionManifestIndex,
        controllerRaw:view ? Array.from(new Uint8Array(view.buffer,ptr,272)) : null};
    }
    probe.installTableHook(10970,"DCP.Update.schedule",{signature:"vii",traceCallEvent:false,
      beforeCall:function(args,record){pushEvent("controller.update.schedule",snapshot(args,"before"));},
      afterCall:function(args,result,record){pushEvent("controller.update.schedule",snapshot(args,"after"));}});
    probe.installTableHook(10968,"DCP.Awake.schedule",{signature:"vii",traceCallEvent:false,
      afterCall:function(args,result,record){pushEvent("controller.awake.schedule",snapshot(args,"after"));}});
    SCHEDULE_FUNCTIONS.forEach(function(entry){
      probe.installTableHook(entry.tableIndex,"schedule.direct.f"+entry.functionIndex,{signature:entry.signature,traceCallEvent:false,
        beforeCall:function(args,record){
          if(entry.functionIndex===61107)fixedCount++;
          if(entry.functionIndex===61097)pushEvent("controller.update.direct",snapshot(args,"before"));
        },
        afterCall:function(args,result,record){
          if(entry.functionIndex===61097)pushEvent("controller.update.direct",snapshot(args,"after"));
          if(entry.functionIndex===54300 && Math.abs(Number(args[0])+0.0002)<1e-7 && Math.abs(Number(args[1])-0.0002)<1e-7){
            frictionCount++;pushEvent("controller.friction.direct",{value:Number(result),fixedCount:fixedCount,frictionCount:frictionCount});
          }
          if(entry.functionIndex===54557)pushEvent("controller.time_scale.direct",{value:Number(args[0]),fixedCount:fixedCount});
        }});
    });
  },10);
'''
def main():
    wasm=ROOT/'analysis_input/prediction_schedule_calls_20261003.wasm'
    patched,manifest=instrument((ROOT/'analysis_input/unity_20260930.wasm').read_bytes(),[61097,61107,54300,54557])
    wasm.write_bytes(patched);manifest.update(source=str(ROOT/'analysis_input/unity_20260930.wasm'),patched=str(wasm))
    full_manifest=wasm.with_suffix('.json');full_manifest.write_text(json.dumps(manifest,indent=2),encoding='utf8')
    routed=dict(manifest);routed['functions']=[]
    route_manifest=ROOT/'analysis_input/prediction_schedule_route_20261003.json';route_manifest.write_text(json.dumps(routed,indent=2),encoding='utf8')
    original=capture.PROBE.read_text(encoding='utf8');marker='  global.__curlingProbe = probe;'
    assert original.count(marker)==1
    script='  var SCHEDULE_FUNCTIONS='+json.dumps(manifest['functions'])+';\n'+extra
    PROBE.write_text(original.replace(marker,script+'\n'+marker),encoding='utf8')
    capture.PROBE=PROBE
    sys.argv=[sys.argv[0],'--plan',str(ROOT/'analysis_input/multi_case_validation_20261002/full12004_run1_plan.json'),
      '--natural-friction','--dense-release-serial','2','--dense-write-limit','5000',
      '--output',str(OUT),'--expected-release-count','1','--expected-friction-count','1',
      '--expected-dense-count','1','--expected-c03-count','0','--reset-settle-seconds','2',
      '--export-wait-seconds','15','--pcm-call-trace-manifest',str(route_manifest)]
    capture.main()
    (OUT/'observer_manifest.json').write_text(json.dumps(dict(originalObserverSha256=hashlib.sha256(original.encode()).hexdigest(),
        observerSha256=hashlib.sha256(PROBE.read_bytes()).hexdigest(),sourceWasmSha256=hashlib.sha256((ROOT/'analysis_input/unity_20260930.wasm').read_bytes()).hexdigest(),
        patchedWasmSha256=hashlib.sha256(patched).hexdigest(),
        instrumentation='Original bodies appended byte-identically; original indices forward through observed table thunks.',
        rngOrClockStateMutation=False, timingPassivityVerified=False,
        scope='Direct controller, friction and timeScale bodies observed. Logging may alter wall-clock frame durations; frame schedule is an input, not a passivity claim.'),indent=2),encoding='utf8')
if __name__=='__main__':main()
