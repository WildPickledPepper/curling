"""Discover actual Win64 PxConvexMeshDesc inputs during production startup."""
import hashlib
import argparse
import json
from pathlib import Path
import subprocess
import frida
from trace_native_pcm_calls import wait_file, CP39
ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=ROOT/'analysis_input/native_startup_cooker_inputs_20261002')
    parser.add_argument('--baseline',type=Path,default=ROOT/'analysis_input/native_startup_geometry_audit_20261002.json')
    opts=parser.parse_args()
    directory=opts.output_dir
    directory.mkdir(exist_ok=False)
    command=[CP39,str(ROOT/'analysis_input/sample_native_startup_cooker_20261002.py'),str(directory)]
    (directory/'command.json').write_text(json.dumps(command))
    session=None
    with (directory/'stdout.log').open('w') as stdout,(directory/'stderr.log').open('w') as stderr:
        worker=subprocess.Popen(command,cwd=ROOT,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            wait_file(directory/'arm.json',worker)
            request=json.loads((directory/'arm.json').read_text())
            session=frida.attach(request['pid'])
            script=session.create_script((ROOT/'analysis_input/trace_startup_cooker_inputs_20261002.js').read_text())
            script.load(); module=script.exports_sync.arm(request['threadId'],request['module'])
            (directory/'go').write_text('go')
            wait_file(directory/'done',worker)
            trace=script.exports_sync.finish()
            trace.update(module=module,moduleSha256=hashlib.sha256(Path(request['module']).read_bytes()).hexdigest(),request=request)
            (directory/'calls.json').write_text(json.dumps(trace,indent=2))
            session.detach();session=None
            (directory/'resume').write_text('resume')
            worker.wait(timeout=90)
            assert worker.returncode==0
            native=json.loads((directory/'output.json').read_text())
            plain=json.loads(opts.baseline.read_text())['observations'][0]['after']
            assert native==plain, 'Native tracing changed final initialized hull'
            assert trace['descriptors'], 'No actual native descriptor observed'
            print('PASS: actual native cooker input descriptors',len(trace['descriptors']),'unique call targets',len(trace['sites']))
        finally:
            if session:session.detach()
            if worker.poll() is None:
                worker.terminate();worker.wait(timeout=10)


if __name__=='__main__':main()
