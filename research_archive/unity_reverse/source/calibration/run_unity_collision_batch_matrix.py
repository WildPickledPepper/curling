# -*- coding: utf-8 -*-
"""Run collision validation as 12 throws per Unity session, then restart.

The batch plans intentionally reset/clear the infinite-mode sheet between
throws without resetting Unity's process-level random stream.  A new browser
is launched only between batches, so this separates within-session variation
from variation due to a fresh Unity process.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import socket
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SERVER_EXE = ROOT / "数字冰壶单机版_win" / "数字冰壶单机版" / "curling_server.exe"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--batch-dir", type=Path,
        default=ROOT / "config" / "unity_unique_target_collision_batches_20260708",
    )
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--log-root", type=Path, required=True)
    parser.add_argument(
        "--hybrid-python", type=Path,
        default=Path(r"D:\esp\tmp\curling_pyphysx_conda\python.exe"),
    )
    parser.add_argument(
        "--browser-wait-seconds", type=float, default=1.0,
        help="Lead time after starting the retrying sampler and before opening the browser (default: 1s).",
    )
    parser.add_argument("--sampler-timeout-seconds", type=float, default=1200.0)
    parser.add_argument(
        "--post-sampler-drain-seconds",
        type=float,
        default=60.0,
        help="Keep the browser alive after the final POSITION so all streamed per-shot friction events flush before teardown.",
    )
    parser.add_argument(
        "--c03-target-native-x",
        type=float,
        help="Optional native X of the target stone whose collision window is captured.",
    )
    parser.add_argument(
        "--c03-target-native-z",
        type=float,
        help="Optional native Z of the target stone whose collision window is captured.",
    )
    parser.add_argument(
        "--c03-target-native-tolerance",
        type=float,
        default=0.05,
        help="Native target selector tolerance in metres.",
    )
    parser.add_argument(
        "--c03-active-speed-min",
        type=float,
        help="Optional native horizontal speed lower bound for the moving stone in a C03 capture.",
    )
    parser.add_argument(
        "--c04-dynamic-window-limit",
        type=int,
        help="Enable a lightweight C03/C04/C31 core trace with this many post-contact frames.",
    )
    parser.add_argument(
        "--c31-compact-core-raw-frame-limit",
        type=int,
        default=2048,
        help="When C04 is enabled, retain raw solver payloads for this many first frames and compact cores thereafter.",
    )
    parser.add_argument(
        "--c54-intercall-static",
        action="store_true",
        help="Also capture read-only stone--ice static solver blocks interleaved with the selected C04 frame.",
    )
    parser.add_argument(
        "--c05-pcm-window",
        action="store_true",
        help="With C03/C04, retain the selected post-contact PCM ContactBuffer window.",
    )
    parser.add_argument(
        "--c05-pcm-window-limit",
        type=int,
        default=12,
        help="Maximum post-contact PCM calls retained by --c05-pcm-window (1-12).",
    )
    parser.add_argument(
        "--rng-friction-manifest-events",
        type=Path,
        help="Diagnostic only: replay the recorded Unity friction draws from this JSONL across the batch.",
    )
    parser.add_argument(
        "--log-other-random-range",
        action="store_true",
        help="Diagnostic only: retain non-friction UnityEngine.Random.Range calls for RNG-state accounting.",
    )
    parser.add_argument(
        "--log-random-value",
        action="store_true",
        help="Diagnostic only: retain UnityEngine.Random.value calls for RNG-state accounting.",
    )
    parser.add_argument(
        "--audit-unity-material-transition",
        action="store_true",
        help="Historical A/B only: use the old material-transition diagnostic instead of production contact override.",
    )
    parser.add_argument(
        "--reset-all-stone-rotations",
        action="store_true",
        help="Diagnostic sampling mutation: restore every stone's initial quaternion after each RESETPOSITION.",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        help="Optional exact batch plan stems; useful when replacing an invalid session.",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--debug-config-url",
        default="http://127.0.0.1:9007/debug/config",
        help="Local curling-server endpoint used to create the controlled debug session.",
    )
    parser.add_argument("--debug-connect-key", default="localtest")
    parser.add_argument(
        "--server-executable", type=Path, default=DEFAULT_SERVER_EXE,
        help="local curling_server.exe restarted after a failed controlled batch",
    )
    return parser.parse_args()


def run(command: list[str], stdout: Path, stderr: Path, timeout: float | None = None) -> None:
    stdout.with_suffix(".command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")
    with stdout.open("w", encoding="utf-8") as out, stderr.open("w", encoding="utf-8") as err:
        subprocess.run(command, cwd=ROOT, stdout=out, stderr=err, check=True, timeout=timeout)


def prepare_local_debug_session(url: str, connect_key: str) -> None:
    """Create debug protocol slots before the WebGL waiting room is opened."""

    payload = json.dumps({
        "humanFirst": True,
        "robotIndex": 0,
        "connectKey": connect_key,
    }).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8", errors="replace").strip()
            if response.status != 200 or body.lower() != "ok":
                raise RuntimeError(f"debug setup returned HTTP {response.status}: {body!r}")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"cannot initialise local debug session at {url}: {exc}") from exc


def terminate_orphaned_legacy_robots() -> None:
    """Remove only the old server-spawned ``localtest`` robot clients.

    Older manual runs used a fixed connect key and the server launched a
    ``robot_0.py`` client for it.  Those processes can stay connected after a
    sampler/browser has exited, thereby consuming a legacy player slot.  They
    are not part of a fresh, per-batch controlled session, so remove just this
    precise legacy signature before starting one.  ``taskkill`` is Windows
    specific; the harness is Windows-only because it drives the local WebGL
    build.
    """

    if os.name != "nt":
        return
    script = (
        "$ErrorActionPreference='Stop'; "
        "$stale=Get-CimInstance Win32_Process | Where-Object { "
        "$_.Name -ieq 'python.exe' -and "
        "$_.CommandLine -match 'robot_0\\.py\\s+--host\\s+127\\.0\\.0\\.1\\s+--key\\s+localtest\\s+--port\\s+7788' "
        "}; "
        "if($stale){$stale | ForEach-Object {Stop-Process -Id $_.ProcessId -Force}}"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def stop_process(process: subprocess.Popen | None) -> None:
    """Terminate a child and wait so a failed batch cannot leak a socket."""

    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def restart_local_server(server_executable: Path) -> None:
    """Reset server-side player/session state after an interrupted batch."""

    executable = server_executable.resolve()
    if not executable.exists():
        raise FileNotFoundError(f"curling server executable not found: {executable}")
    # Kill only this workspace's local server; do not touch an unrelated
    # curling instance.  Its robot children exit with the server.
    escaped = str(executable).replace("'", "''")
    script = (
        "$server=Get-CimInstance Win32_Process | Where-Object { "
        "$_.Name -ieq 'curling_server.exe' -and $_.ExecutablePath -eq '"
        + escaped
        + "' }; if($server){$server | ForEach-Object {Stop-Process -Id $_.ProcessId -Force}}"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    subprocess.Popen(
        [str(executable)], cwd=executable.parent,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", 9007), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("curling_server did not reopen port 9007 after restart")


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    args = parse_args()
    output_root = args.output_root.resolve()
    log_root = args.log_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    log_root.mkdir(parents=True, exist_ok=True)
    progress = output_root / "progress.jsonl"
    prior = {row.get("batch"): row for row in read_rows(progress) if row.get("status") == "ok"}
    # The historical 12-case matrices used this filename prefix.  Diagnostic
    # manifest sessions deliberately contain a focused repeated configuration,
    # so discover every explicit JSON plan in the caller-selected directory.
    plans = sorted(args.batch_dir.resolve().glob("*.json"))
    if args.only:
        wanted = set(args.only)
        plans = [plan for plan in plans if plan.stem in wanted]
    if not plans:
        raise SystemExit(f"No batch plans in {args.batch_dir}")

    for number, plan in enumerate(plans, start=1):
        batch = plan.stem
        if args.resume and batch in prior:
            print(f"[{number}/{len(plans)}] skip {batch}", flush=True)
            continue
        session_log = log_root / batch
        session_log.mkdir(parents=True, exist_ok=True)
        sample_path = output_root / f"{batch}.jsonl"
        audit_path = output_root / f"{batch}_endpoint.json"
        protocol_ready_path = session_log / "two_player_protocol.ready.json"
        unity_protocol_connected_path = session_log / "unity_protocol_connected.ready.json"
        protocol_tcp_connected_path = session_log / "two_player_tcp_connected.ready.json"
        unity_protocol_connected_path.unlink(missing_ok=True)
        protocol_tcp_connected_path.unlink(missing_ok=True)
        # Debug PlayerMgr state is keyed by connectKey and survives a closed
        # WebGL page briefly.  Reusing localtest can therefore reconnect to a
        # stale, already-closed match.  Give every browser batch its own key.
        session_key = f"{args.debug_connect_key}-{batch}-{int(time.time() * 1000)}"
        row = {
            "batch": batch, "startedAtUtc": utc_now(), "plan": str(plan),
            "debugConnectKey": session_key,
        }
        launcher: subprocess.Popen | None = None
        sampler: subprocess.Popen | None = None
        print(f"[{number}/{len(plans)}] Unity session start: {batch} (12 configurations)", flush=True)
        try:
            # A bare 7788 TCP listener is not a usable controlled session.
            # Initialise the server-side debug PlayerMgr first; otherwise Unity
            # may show both players connected while closing their sockets before
            # READYOK/NAME.
            terminate_orphaned_legacy_robots()
            prepare_local_debug_session(args.debug_config_url, session_key)
            sampler_command = [
                sys.executable, "tools/calibration/controlled_scene_sampler.py",
                "--key", session_key,
                "--plan-file", str(plan), "--output-file", str(sample_path),
                "--use-reset", "--use-plan-active-index", "--reset-settle-seconds", "0.25",
                "--force-final-timeout-seconds", "40",
                # The reset acknowledgement itself is a POSITION message.  For
                # collision validation it must never be mistaken for a final
                # endpoint before Unity has emitted MOTIONINFO for the throw.
                "--require-motioninfo",
                "--protocol-ready-file", str(protocol_ready_path),
                "--wait-for-unity-protocol-ready-file", str(unity_protocol_connected_path),
                "--protocol-tcp-connected-file", str(protocol_tcp_connected_path),
                # The sampler must return to its pre-ready handshake check
                # before its 15s deadline, otherwise it can wait forever on
                # an infinite-mode listener that has not started the match.
                "--timeout-seconds", "5",
            ]
            sampler_stdout = session_log / "sampler.stdout.log"
            sampler_stderr = session_log / "sampler.stderr.log"
            sampler_stdout.with_suffix(".command.txt").write_text(
                " ".join(sampler_command) + "\n", encoding="utf-8"
            )
            # The sampler retries the still-closed 7788 port.  It must be
            # alive before the browser enters infinite mode, otherwise the
            # auto UI can start an empty match and no GO is ever emitted.
            with sampler_stdout.open("w", encoding="utf-8") as out, sampler_stderr.open("w", encoding="utf-8") as err:
                sampler = subprocess.Popen(
                    sampler_command, cwd=ROOT, stdout=out, stderr=err,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
            time.sleep(args.browser_wait_seconds)
            launcher_command = [
                sys.executable, "tools/calibration/launch_unity_probe_browser.py",
                "--url", f"http://127.0.0.1:9007/?connectkey={session_key}",
                "--log-root", str(session_log), "--stream-events", "--stream-no-store", "--no-poll-events",
                "--sliding-trace-hooks", "--a0-fixed-tick-resolver-hook",
                # Record reset-preserved active and target quaternions.  The
                # endpoint auditor needs them to treat a persistent batch as
                # strict rather than a statistical/non-strict replay.
                "--a10-release-orientation",
                # A batch contains twelve complete slides; retain every friction draw for replay.
                "--sliding-trace-max-random-events", "50000",
                "--sliding-trace-max-fixed-events", "50000", "--auto-infinite-ui",
                "--unity-protocol-connected-file", str(unity_protocol_connected_path),
                "--auto-ui-tcp-connected-file", str(protocol_tcp_connected_path),
                # Do not click start until both sampler sockets have completed
                # READYOK/NAME.  This is the readiness gate, not a timer.
                "--auto-ui-protocol-ready-file", str(protocol_ready_path),
            ]
            if args.log_other_random_range:
                launcher_command.append("--sliding-trace-log-other-random-range")
            if args.log_random_value:
                launcher_command.append("--sliding-trace-log-random-value")
            if args.c04_dynamic_window_limit is not None:
                if args.c03_target_native_x is None or args.c03_target_native_z is None:
                    raise ValueError("C04 capture requires both --c03-target-native-x and --c03-target-native-z")
                launcher_command.extend([
                    "--c03-first-writeback",
                    "--c03-target-native-x", str(args.c03_target_native_x),
                    "--c03-target-native-z", str(args.c03_target_native_z),
                    "--c03-target-native-tolerance", str(args.c03_target_native_tolerance),
                    "--c04-dynamic-window",
                    "--c04-dynamic-window-limit", str(args.c04_dynamic_window_limit),
                    "--c31-compact-core-trace",
                    "--c31-compact-core-raw-frame-limit", str(args.c31_compact_core_raw_frame_limit),
                ])
                if args.c03_active_speed_min is not None:
                    launcher_command.extend(["--c03-active-speed-min", str(args.c03_active_speed_min)])
                if args.c54_intercall_static:
                    launcher_command.append("--c54-intercall-static")
                if args.c05_pcm_window:
                    launcher_command.extend([
                        "--c05-pcm-window",
                        "--c05-pcm-window-limit", str(args.c05_pcm_window_limit),
                    ])
            if args.rng_friction_manifest_events is not None:
                launcher_command.extend([
                    "--rng-friction-manifest-events",
                    str(args.rng_friction_manifest_events.resolve()),
                ])
            if args.reset_all_stone_rotations:
                launcher_command.append("--reset-all-stone-rotations")
            (session_log / "launcher.command.txt").write_text(" ".join(launcher_command) + "\n", encoding="utf-8")
            with (session_log / "launcher.stdout.log").open("w", encoding="utf-8") as out, (session_log / "launcher.stderr.log").open("w", encoding="utf-8") as err:
                launcher = subprocess.Popen(
                    launcher_command, cwd=ROOT, stdout=out, stderr=err,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
            assert sampler is not None
            try:
                sampler.wait(timeout=args.sampler_timeout_seconds)
            except subprocess.TimeoutExpired:
                sampler.kill()
                sampler.wait()
                raise
            if sampler.returncode:
                raise subprocess.CalledProcessError(sampler.returncode, sampler_command)
            # The sampler's final POSITION can arrive before the HTTP event sink
            # has flushed the last shot's per-tick friction events.  Do not turn
            # that valid Unity endpoint into a truncated local replay input.
            time.sleep(args.post_sampler_drain_seconds)
        except Exception as exc:
            row.update({"status": "sampler_failed", "error": repr(exc)})
        finally:
            stop_process(sampler)
            stop_command = [
                sys.executable, "tools/calibration/stop_unity_probe_session.py",
                "--log-root", str(session_log), "--sampler-output", str(sample_path), "--stop",
            ]
            try:
                run(stop_command, session_log / "stop.stdout.log", session_log / "stop.stderr.log")
            except Exception as exc:
                row["stopError"] = repr(exc)
            stop_process(launcher)

        if row.get("status") == "sampler_failed":
            try:
                restart_local_server(args.server_executable)
                row["serverRestartedAfterFailure"] = True
            except Exception as exc:
                row["serverRestartError"] = repr(exc)

        if row.get("status") != "sampler_failed":
            try:
                events = next(session_log.rglob("events.jsonl"))
                samples = read_rows(sample_path)
                no_target_batch = samples and all(not sample.get("target_indices") for sample in samples)
                if no_target_batch:
                    audit_command = [
                        str(args.hybrid_python), "tools/reverse/audit_nonsweep_free_replay.py",
                        "--samples", str(sample_path), "--events", str(events), "--output", str(audit_path),
                    ]
                    run(audit_command, session_log / "audit.stdout.log", session_log / "audit.stderr.log")
                    generic = json.loads(audit_path.read_text(encoding="utf-8"))
                    row.update({
                        "status": "ok", "sample": str(sample_path), "endpointAudit": str(audit_path),
                        "sampleCount": len(samples), "collisionSampleCount": 0, "firstContactCount": 0,
                        "executedReplayCount": len(generic["executedRows"]),
                        "excludedReplayCount": len(generic["excludedRows"]),
                    })
                else:
                    audit_command = [
                        str(args.hybrid_python), "tools/reverse/audit_hybrid_p6_endpoint_sixshot.py",
                        "--samples", str(sample_path), "--events", str(events), "--output", str(audit_path),
                    ]
                    if args.audit_unity_material_transition:
                        audit_command.append("--unity-material-transition")
                    run(audit_command, session_log / "audit.stdout.log", session_log / "audit.stderr.log")
                    aggregate = json.loads(audit_path.read_text(encoding="utf-8"))["aggregate"]
                    row.update({
                        "status": "ok", "sample": str(sample_path), "endpointAudit": str(audit_path),
                        "sampleCount": len(samples), "collisionSampleCount": sum(
                            1 for sample in samples if sample.get("collision_observed")
                        ),
                        "firstContactCount": aggregate["reachedFirstContactCount"],
                        "activeRmseM": aggregate["activeEndpointError"]["rmseM"],
                        "targetRmseM": aggregate["targetEndpointError"]["rmseM"],
                    })
            except Exception as exc:
                row.setdefault("status", "audit_failed")
                row["error"] = repr(exc)
        row["finishedAtUtc"] = utc_now()
        with progress.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        print(f"[{number}/{len(plans)}] {batch}: {row['status']}", flush=True)

    latest = {row.get("batch"): row for row in read_rows(progress) if row.get("batch")}
    summary = {"generatedAtUtc": utc_now(), "batches": [latest[p.stem] for p in plans if p.stem in latest]}
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("batch matrix complete", flush=True)


if __name__ == "__main__":
    main()
