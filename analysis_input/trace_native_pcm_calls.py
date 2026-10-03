"""Observe the current Windows kernel's actual PCM internal calls with Frida."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

import frida

ROOT = Path(__file__).resolve().parents[1]
CP39 = r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe"


def wait_file(path, worker):
    deadline = time.monotonic() + 90
    while not path.exists():
        if worker.poll() is not None:
            raise RuntimeError(f"native worker exited {worker.returncode}")
        if time.monotonic() > deadline:
            raise TimeoutError(path)
        time.sleep(0.05)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--targets-from-discovery", type=Path)
    parser.add_argument("--stone-collision", action="store_true")
    parser.add_argument('--physics-ordinal',type=int,default=1023)
    parser.add_argument('--actor-lifecycle',action='store_true')
    parser.add_argument('--startup-only',action='store_true')
    parser.add_argument("--direct-pair", action="store_true")
    parser.add_argument("--extra-rva", action="append",default=[])
    parser.add_argument('--observer-script',type=Path,
        default=ROOT/'analysis_input/trace_native_pcm_calls.js')
    parser.add_argument("--light-discovery",action="store_true")
    parser.add_argument('--reset-step', type=int)
    parser.add_argument('--reset-through-step', type=int)
    parser.add_argument('--reset-baseline', type=Path)
    parser.add_argument('--mxcsr-probe', action='store_true')
    parser.add_argument('--release-step',type=int)
    parser.add_argument('--fresh-case-plan',type=Path)
    parser.add_argument('--fresh-case-capture',type=Path)
    parser.add_argument('--fresh-case-step',type=int,default=1383)
    parser.add_argument('--release-baseline',type=Path,
        default=ROOT/'analysis_input/native_first_release_vertical_fixed_full_20261002.json')
    opts = parser.parse_args()
    out = opts.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    report_path = out / "alignment.json"
    command = [CP39, str(ROOT / "analysis_input/trace_native_pcm_child.py"), str(out),
               "full-q", "--trace", "--sync-body-q", "--float32-body-q",
               "--solver-ordinal-min", "486", "--solver-ordinal-max", "488",
               "--trace-constraints", "--direct-contact-probe", "--output", str(report_path)]
    if opts.stone_collision:
        command = [CP39,str(ROOT/"analysis_input/audit_c131_alignment_20260930.py"),
            "full-q","--trace","--sync-body-q","--float32-body-q",
            "--solver-ordinal-min","1021","--solver-ordinal-max","1023",
            "--trace-constraints","--post-dense-trace-frames","1",
            "--native-trace-ordinal",str(opts.physics_ordinal),
            "--native-trace-control",str(out),"--output",str(report_path)]
        if opts.direct_pair:
            command.append("--native-trace-direct-pair")
    if opts.actor_lifecycle:
        command=[CP39,str(ROOT/'analysis_input/audit_c131_alignment_20260930.py'),
            'full-q','--trace','--sync-body-q','--float32-body-q',
            '--native-lifecycle-trace-control',str(out),'--output',str(report_path)]
    if opts.startup_only:
        command=[CP39,str(ROOT/'analysis_input/sample_native_startup_numeric_20261003.py'),
            '--native-trace-control',str(out),'--output',str(report_path)]
    if opts.reset_step is not None:
        command = [CP39, str(ROOT / 'analysis_input/sample_reset_internal_trace_20261002.py'),
                   '--native-trace-control', str(out), '--native-trace-step', str(opts.reset_step),
                   '--output', str(report_path)]
        if opts.reset_through_step is not None:
            command += ['--native-trace-through-step', str(opts.reset_through_step)]
        if opts.reset_baseline is not None:
            command += ['--baseline', str(opts.reset_baseline)]
    if opts.release_step is not None:
        command=[CP39,str(ROOT/'analysis_input/sample_first_release_chain_20261002.py'),
            '--trace','--trace-at-step',str(opts.release_step),'--steps',str(opts.release_step),
            '--native-trace-control',str(out),'--baseline',
            str(opts.release_baseline),
            '--output',str(report_path)]
    if opts.fresh_case_plan is not None:
        command=[CP39,str(ROOT/'analysis_input/sample_new_case_20261002.py'),
            '--plan',str(opts.fresh_case_plan),'--capture',str(opts.fresh_case_capture),
            '--trace-from-step',str(opts.fresh_case_step),
            '--steps',str(max(3000,opts.fresh_case_step+2)),
            '--native-trace-control',str(out),'--output',str(report_path)]
    (out / "command.json").write_text(json.dumps(command, indent=2), encoding="utf-8")
    session = None
    with (out / "stdout.log").open("w") as stdout, (out / "stderr.log").open("w") as stderr:
        worker = subprocess.Popen(command, cwd=ROOT, stdout=stdout, stderr=stderr,
                                  creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        try:
            wait_file(out / "arm.json", worker)
            request = json.loads((out / "arm.json").read_text(encoding="utf-8"))
            session = frida.attach(request["pid"])
            script = session.create_script(opts.observer_script.read_text(encoding="utf-8"))
            script.on("message", lambda message, data: print(message, flush=True))
            script.load()
            target_rvas = None
            if opts.targets_from_discovery is not None:
                discovery = json.loads(opts.targets_from_discovery.read_text(encoding="utf-8"))
                if hashlib.sha256(Path(request["module"]).read_bytes()).hexdigest() != discovery["moduleSha256"]:
                    raise ValueError("native discovery module hash mismatch")
                target_rvas = sorted({row["functionRva"] for row in discovery["calls"]
                                      if row.get("functionRva") and
                                      0x100000 <= int(row["functionRva"], 16) < 0x440000})
                target_rvas = sorted(set(target_rvas)|set(opts.extra_rva))
            if opts.actor_lifecycle or opts.startup_only:
                target_rvas=['0x214bd0','0x214c50','0x236ed0']
            if target_rvas is None and opts.extra_rva:
                target_rvas = opts.extra_rva
            module = script.exports_sync.arm(request["threadId"], request["module"], target_rvas, opts.light_discovery, opts.mxcsr_probe)
            print("native module", module, flush=True)
            (out / "go").write_text("go", encoding="utf-8")
            wait_file(out / "done", worker)
            trace = script.exports_sync.finish()
            trace.update(request=request, module=module,
                         mode="interceptor" if target_rvas is not None else "callsite-discovery",
                         callStackReliable=target_rvas is not None and not trace['unfinished']
                             and not any(row.get('stackMismatch') for row in trace['calls']),
                         moduleSha256=hashlib.sha256(Path(request["module"]).read_bytes()).hexdigest())
            (out / "calls.json").write_text(json.dumps(trace), encoding="utf-8")
            (out / "resume").write_text("resume", encoding="utf-8")
            worker.wait(timeout=90)
            print("worker exit", worker.returncode, "calls", len(trace["calls"]),
                  "dropped", trace["dropped"], "unfinished count", len(trace["unfinished"]), flush=True)
            if worker.returncode:
                raise RuntimeError("native audit failed; inspect stderr.log")
        finally:
            if session is not None:
                session.detach()
            if worker.poll() is None:
                worker.terminate()
                worker.wait(timeout=5)


if __name__ == "__main__":
    main()
