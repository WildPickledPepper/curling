"""Capture the existing 12-shot Unity plan with old friction and a 12011 C03/C04 hook.

The historical launcher/sampler remain the implementation. This orchestrator
only supplies explicit paths from the archived layout and cleans up its own
local server, sampler, and probe browser processes.
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

import psutil


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "research_archive/unity_reverse"
SCRIPTS = ARCHIVE / "source/calibration"
EVIDENCE = ARCHIVE / "evidence"
PYTHON = Path(r"D:\anaconda3\python.exe")
SERVER = ROOT / "数字冰壶单机版_win/数字冰壶单机版/curling_server.exe"
PLAN = EVIDENCE / "config/unity_extended_collision_batches_20260714/collision_unique_targets_batch_r03.json"
OLD_EVENTS = EVIDENCE / "log/extended_collision_validation_20260715_ordered/collision_unique_targets_batch_r03/unity_runtime_probe_20260715_125420/events.jsonl"
PROBE = ARCHIVE / "source/reverse/unity_webgl_runtime_probe.js"
OUT = ROOT / "analysis_input/unity_12011_dense_setter_bridge_20260929"
HEADLESS = True
STREAM_MODE = False


def wait_port(port: int, seconds: float) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)
    raise TimeoutError(f"port {port} did not open")


def stop(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def event_counts(logs: Path) -> Counter:
    counts: Counter = Counter()
    for event_file in logs.rglob("events.jsonl"):
        with event_file.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    row=json.loads(line)
                    counts[row["type"]] += 1
                    if row['type']=='a12.tail_phase_core' and row['data']['phase']=='DCP.FixedUpdate.boundary':
                        counts['_max_completed_solver']=max(counts['_max_completed_solver'],row['data']['solverSerial'])
                except json.JSONDecodeError:
                    # A concurrent append may leave only the final line partial.
                    pass
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dense-release-serial", type=int, default=24)
    parser.add_argument("--dense-write-limit", type=int, default=2000)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--plan", type=Path, default=PLAN)
    parser.add_argument("--events", type=Path, default=OLD_EVENTS)
    parser.add_argument("--expected-friction-count", type=int, default=21538)
    parser.add_argument("--expected-dense-count", type=int)
    parser.add_argument("--expected-release-count", type=int, default=12)
    parser.add_argument("--expected-c03-count", type=int, default=1)
    parser.add_argument("--expected-reset-core-count", type=int, default=0)
    parser.add_argument("--reset-settle-seconds", type=float, default=0.25)
    parser.add_argument('--export-wait-seconds',type=float,default=90)
    parser.add_argument('--natural-friction',action='store_true')
    parser.add_argument('--expected-tail-boundary-steps',type=int,default=0)
    parser.add_argument("--phase-ordinal-min", type=int, default=2)
    parser.add_argument("--phase-ordinal-max", type=int, default=22)
    parser.add_argument("--static-phase-trace", action="store_true")
    parser.add_argument("--pcm-window-limit", type=int, default=0)
    parser.add_argument("--pcm-call-trace-manifest", type=Path)
    parser.add_argument("--pcm-geometry-scale-trace", action="store_true")
    parser.add_argument("--target-native-x", type=float, default=-73.37739562988281)
    parser.add_argument("--target-native-z", type=float, default=53.900001525878906)
    parser.add_argument("--target-active-speed-min", type=float)
    opts = parser.parse_args()
    capture_out = opts.output.resolve()
    if opts.natural_friction:opts.events=None
    required = (PYTHON, SERVER, opts.plan, PROBE) + ((opts.events,) if opts.events is not None else ())
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    if capture_out.exists():
        raise FileExistsError(capture_out)
    for port in (9007, 7788, 2831):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.25):
                raise RuntimeError(f"port {port} already in use; refuse to touch an existing session")
        except (ConnectionRefusedError, TimeoutError, OSError):
            pass

    capture_out.mkdir(parents=True)
    logs = capture_out / "logs"
    logs.mkdir()
    key = f"localtest-12011-first-solver-{int(time.time() * 1000)}"
    ready = capture_out / "protocol.ready.json"
    unity_ready = capture_out / "unity.ready.json"
    tcp_ready = capture_out / "tcp.ready.json"
    samples = capture_out / (opts.plan.stem + ".jsonl")
    server = sampler = browser = None
    started_at = time.time()
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        server = subprocess.Popen([str(SERVER)], cwd=SERVER.parent,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  creationflags=flags)
        wait_port(9007, 15)
        payload = json.dumps({"humanFirst": True, "robotIndex": 0, "connectKey": key}).encode()
        request = urllib.request.Request("http://127.0.0.1:9007/debug/config", data=payload,
                                         headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode().strip()
            if response.status != 200 or body.lower() != "ok":
                raise RuntimeError(f"debug session failed: {response.status} {body}")

        sampler_args = [str(PYTHON), str(SCRIPTS / "controlled_scene_sampler.py"),
                        "--key", key, "--plan-file", str(opts.plan), "--output-file", str(samples),
                        "--use-reset", "--use-plan-active-index", "--reset-settle-seconds", str(opts.reset_settle_seconds),
                        "--force-final-timeout-seconds", "40", "--require-motioninfo",
                        "--protocol-ready-file", str(ready),
                        "--wait-for-unity-protocol-ready-file", str(unity_ready),
                        "--protocol-tcp-connected-file", str(tcp_ready),
                        "--timeout-seconds", "5"]
        browser_args = [str(PYTHON), str(SCRIPTS / "launch_unity_probe_browser.py"),
                        "--url", f"http://127.0.0.1:9007/?connectkey={key}",
                        "--probe", str(PROBE), "--log-root", str(logs),
                        "--sliding-trace-hooks", "--a0-fixed-tick-resolver-hook",
                        "--a10-release-orientation", "--sliding-trace-max-random-events", "50000",
                        "--a12-dense-release-serial", str(opts.dense_release_serial),
                        "--a12-dense-write-limit", str(opts.dense_write_limit),
                        "--a12-phase-ordinal-min", str(opts.phase_ordinal_min),
                        "--a12-phase-ordinal-max", str(opts.phase_ordinal_max),
                        "--sliding-trace-max-fixed-events", "50000", "--auto-infinite-ui",
                        "--unity-protocol-connected-file", str(unity_ready),
                        "--auto-ui-tcp-connected-file", str(tcp_ready),
                        "--auto-ui-protocol-ready-file", str(ready),
                        "--c03-first-writeback", "--c03-target-native-x", str(opts.target_native_x),
                        "--c03-target-native-z", str(opts.target_native_z),
                        "--c03-target-native-tolerance", "0.05",
                        "--c04-dynamic-window", "--c04-dynamic-window-limit", "40",
                        "--c31-compact-core-trace", "--c31-compact-core-raw-frame-limit", "8"]
        if opts.events is not None:
            browser_args.extend(["--rng-friction-manifest-events", str(opts.events)])
        if opts.static_phase_trace:
            browser_args.append("--a12-static-phase-trace")
        if opts.pcm_window_limit:
            browser_args.extend(["--c05-pcm-window", "--c05-pcm-window-limit", str(opts.pcm_window_limit)])
        if opts.pcm_call_trace_manifest is not None:
            browser_args.extend(["--pcm-call-trace-manifest", str(opts.pcm_call_trace_manifest.resolve())])
        if opts.pcm_geometry_scale_trace:
            browser_args.append("--pcm-geometry-scale-trace")
        if opts.target_active_speed_min is not None:
            browser_args.extend(["--c03-active-speed-min", str(opts.target_active_speed_min)])
        if HEADLESS:
            browser_args.append("--headless")
        if STREAM_MODE:
            browser_args.extend(["--stream-events", "--stream-no-store", "--no-poll-events"])
        (capture_out / "commands.json").write_text(json.dumps({"sampler": sampler_args, "browser": browser_args}, indent=2), encoding="utf-8")
        with (capture_out / "sampler.stdout.log").open("w") as sout, (capture_out / "sampler.stderr.log").open("w") as serr, \
             (capture_out / "browser.stdout.log").open("w") as bout, (capture_out / "browser.stderr.log").open("w") as berr:
            sampler = subprocess.Popen(sampler_args, cwd=ROOT, stdout=sout, stderr=serr, creationflags=flags)
            time.sleep(1)
            browser = subprocess.Popen(browser_args, cwd=ROOT, stdout=bout, stderr=berr, creationflags=flags)
            print("started", key, "sampler", sampler.pid, "browser", browser.pid, flush=True)
            sampler.wait(timeout=240)
            print("sampler_returncode", sampler.returncode, flush=True)
            deadline = time.monotonic() + opts.export_wait_seconds
            while time.monotonic() < deadline:
                counts = event_counts(logs)
                print("capture_progress", counts["a10.release_reset_orientation"],
                      counts["sliding.random_range.friction"],
                      counts["a12.dense_pre_angular_setter"],
                      counts["c03.first_dynamic_writeback"], flush=True)
                dense_count = opts.expected_dense_count if opts.expected_dense_count is not None else (1282 if opts.dense_release_serial == 18 else 910)
                if (counts["a10.release_reset_orientation"] >= opts.expected_release_count
                        and counts["sliding.random_range.friction"] >= opts.expected_friction_count
                        and counts["a12.dense_pre_angular_setter"] >= dense_count
                        and counts["a12.dense_post_angular_setter"] >= dense_count
                        and counts["c03.first_dynamic_writeback"] >= opts.expected_c03_count
                        and counts["scene.reset_body_cores"] >= opts.expected_reset_core_count
                        and counts['_max_completed_solver'] >= opts.expected_tail_boundary_steps):
                    break
                time.sleep(5)
        if sampler.returncode:
            raise RuntimeError(f"sampler failed: {sampler.returncode}")
        if opts.expected_reset_core_count and counts['scene.reset_body_cores'] < opts.expected_reset_core_count:
            raise RuntimeError('Requested Reset core sampling window was not captured')
        if counts['_max_completed_solver'] < opts.expected_tail_boundary_steps:
            raise RuntimeError('Requested completed-step boundary window was not captured')
        print("sample_count", sum(1 for _ in samples.open(encoding="utf-8")), flush=True)
        for event_file in logs.rglob("events.jsonl"):
            print("events", event_file, event_file.stat().st_size, flush=True)
    finally:
        stop(sampler)
        if browser is not None:
            try:
                children = psutil.Process(browser.pid).children(recursive=True)
            except psutil.NoSuchProcess:
                children = []
            for child in children:
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    pass
            _gone, alive = psutil.wait_procs(children, timeout=3)
            for child in alive:
                child.kill()
        stop(browser)
        stop(server)
        for process in psutil.process_iter(["exe", "create_time"]):
            try:
                if (process.info["exe"] and Path(process.info["exe"]).resolve() == SERVER.resolve()
                        and process.info["create_time"] >= started_at - 2):
                    for child in process.children(recursive=True):
                        child.terminate()
                    process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass


if __name__ == "__main__":
    main()
