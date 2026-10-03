#!/usr/bin/env python3
"""Launch the local Unity WebGL client with the runtime probe pre-injected."""

from __future__ import annotations

import argparse
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_URL = "http://127.0.0.1:9007/?connectkey=localtest"
DEFAULT_PROBE = PROJECT_ROOT / "tools" / "reverse" / "unity_webgl_runtime_probe.js"
DEFAULT_LOG_ROOT = PROJECT_ROOT / "log"


def _safe_evaluate(page: Any, expression: str) -> Any:
    try:
        return page.evaluate(expression)
    except PlaywrightError as exc:
        return {"error": str(exc)}


def _write_json_atomic(path: Path, payload: Any) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_path.replace(path)


class EventSinkState:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()
        self.event_count = 0
        self.type_counts: dict[str, int] = {}
        self.installed_hook_names: set[str] = set()
        self.native_hooks_installed = False
        self.sliding_hooks_installed = False
        self.game_object_activation_hook_installed = False
        # The WebGL client creates two independent game WebSockets.  The
        # in-canvas "ready" button is not actionable until both have received
        # CONNECTED; a blind time delay can click it during the native-splash
        # / waiting-room transition and permanently strand the TCP players.
        self.unity_protocol_connected_count = 0
        self.last_event: dict[str, Any] | None = None

    def append(self, event: dict[str, Any]) -> None:
        line = json.dumps(event, ensure_ascii=False)
        event_type = str(event.get("type") or "")
        data = event.get("data") if isinstance(event.get("data"), dict) else {}
        with self.lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
            self.event_count += 1
            self.type_counts[event_type] = self.type_counts.get(event_type, 0) + 1
            if event_type == "table_hook.installed":
                name = data.get("name")
                if isinstance(name, str):
                    self.installed_hook_names.add(name)
            if event_type == "physx.native.hooks_installed":
                self.native_hooks_installed = True
            if event_type == "sliding.hooks_installed":
                self.sliding_hooks_installed = True
            if event_type == "table_hook.installed" and data.get("name") == "UnityEngine.GameObject.SetActive":
                self.game_object_activation_hook_installed = True
            if event_type == "websocket.recv" and str(data.get("textPreview") or "").strip() == "CONNECTED":
                self.unity_protocol_connected_count += 1
            self.last_event = event

    def summary(self) -> dict[str, Any]:
        with self.lock:
            return {
                "streamedEventCount": self.event_count,
                "streamedTypeCounts": dict(sorted(self.type_counts.items())),
                "installedHookNames": sorted(self.installed_hook_names),
                "nativeHooksInstalled": self.native_hooks_installed,
                "slidingHooksInstalled": self.sliding_hooks_installed,
                "gameObjectActivationHookInstalled": self.game_object_activation_hook_installed,
                "unityProtocolConnectedCount": self.unity_protocol_connected_count,
                "lastStreamedEvent": self.last_event,
            }


def _start_event_sink(path: Path) -> tuple[ThreadingHTTPServer, EventSinkState, str]:
    state = EventSinkState(path)

    class Handler(BaseHTTPRequestHandler):
        def _cors(self) -> None:
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "content-type")

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(204)
            self._cors()
            self.end_headers()

        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length") or "0")
            raw = self.rfile.read(length)
            try:
                event = json.loads(raw.decode("utf-8"))
                if isinstance(event, dict):
                    state.append(event)
                    self.send_response(204)
                elif isinstance(event, list) and all(isinstance(item, dict) for item in event):
                    for item in event:
                        state.append(item)
                    self.send_response(204)
                else:
                    self.send_response(400)
            except Exception:
                self.send_response(400)
            self._cors()
            self.end_headers()

        def log_message(self, format: str, *args: Any) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_address[1]}/event"
    return server, state, url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--log-root", type=Path, default=DEFAULT_LOG_ROOT)
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--width", type=int, default=1500)
    parser.add_argument("--height", type=int, default=950)
    parser.add_argument("--headless", action="store_true", help="Run a diagnostic capture without a visible browser window.")
    parser.add_argument("--no-known-hooks", action="store_true")
    parser.add_argument(
        "--a0-fixed-tick-resolver-hook",
        action="store_true",
        help="Passively install the A0 controller/velocity-write resolver; it does not enable native solver dumps.",
    )
    parser.add_argument(
        "--rng-seed-on-first-friction",
        type=int,
        default=None,
        help=(
            "Diagnostic mutation: immediately before the first -0.0002..0.0002 friction draw "
            "seen by the A0 resolver, call Unity Random.InitState with this signed int32 seed. "
            "Use one controlled shot per browser session and record the emitted rng.seed_applied event."
        ),
    )
    parser.add_argument(
        "--rng-friction-manifest-events",
        type=Path,
        default=None,
        help=(
            "Diagnostic mutation: extract sliding.random_range.friction values from this JSONL "
            "event log and return them only for the recovered DCP friction Range call. "
            "This is the strict replay alternative to --rng-seed-on-first-friction."
        ),
    )
    parser.add_argument(
        "--a2-static-trace",
        action="store_true",
        help="With the A0 resolver, retain one compact moving stone solver-body state per stone-ice tick until first stone PCM.",
    )
    parser.add_argument(
        "--a8-static-window",
        action="store_true",
        help="With the A0 resolver, emit static-contact before/after state for the first eight release ticks only.",
    )
    parser.add_argument(
        "--a9-snapshot-window",
        action="store_true",
        help="With the A0 resolver, emit the native Rigidbody byte deltas caused by angular-velocity setter calls in the first eight release ticks.",
    )
    parser.add_argument(
        "--a10-release-orientation",
        action="store_true",
        help=(
            "With the A0 resolver, record the native moving-stone quaternion before the first angular setter "
            "of every BESTSHOT; use this as strict persistent-scene reset-yaw truth."
        ),
    )
    parser.add_argument(
        "--a12-dense-release-serial",
        type=int,
        default=None,
        help="Read-only per-setter native pose/getter trace for this controlled BESTSHOT protocol serial.",
    )
    parser.add_argument("--a12-dense-write-limit", type=int, default=2000,
                        help="Maximum dense setter ordinals retained by the passive A12 observer.")
    parser.add_argument("--a12-phase-ordinal-min", type=int, default=2)
    parser.add_argument("--a12-phase-ordinal-max", type=int, default=22)
    parser.add_argument("--a12-static-phase-trace", action="store_true")
    parser.add_argument("--pcm-call-trace-manifest", type=Path)
    parser.add_argument("--pcm-geometry-scale-trace", action="store_true")
    parser.add_argument(
        "--reset-all-stone-rotations",
        action="store_true",
        help=(
            "Sampling-only mutation: capture every stone's initial native quaternion on the first "
            "RESETPOSITION, then restore that quaternion after every later RESETPOSITION. "
            "This keeps the same Unity scene and protocol connections alive."
        ),
    )
    parser.add_argument(
        "--c03-first-writeback",
        action="store_true",
        help="With the A0 resolver, capture only the first dynamic-dynamic solver consume/writeback frame after the first stone-stone PCM.",
    )
    parser.add_argument(
        "--c03-target-native-x",
        type=float,
        help="Optional native rigid-core X selector; arm C03 only for a pair containing this target position.",
    )
    parser.add_argument(
        "--c03-target-native-z",
        type=float,
        help="Optional native rigid-core Z selector; used with --c03-target-native-x.",
    )
    parser.add_argument(
        "--c03-target-native-tolerance",
        type=float,
        default=0.05,
        help="Native X/Z selector tolerance in metres (default: 0.05).",
    )
    parser.add_argument(
        "--c03-active-speed-min",
        type=float,
        help="Optional native horizontal speed lower bound for the non-target core when arming C03.",
    )
    parser.add_argument(
        "--c04-dynamic-window",
        action="store_true",
        help="With C03, capture a short consecutive dynamic-solver window after the first stone-stone manager appears.",
    )
    parser.add_argument(
        "--c04-dynamic-window-limit",
        type=int,
        default=12,
        help="Maximum solverSetupSolve frames retained by --c04-dynamic-window (1-2048).",
    )
    parser.add_argument(
        "--c31-compact-core-trace",
        action="store_true",
        help=(
            "With C03/C04, retain only decoded active/target P/Q/v/w core snapshots for a long "
            "post-contact truth trace; no raw memory or solver/cache payloads are recorded."
        ),
    )
    parser.add_argument(
        "--c31-compact-core-raw-frame-limit",
        type=int,
        default=2048,
        help="With C31, retain raw solver blocks for only this many initial C04 frames; later frames keep compact cores only.",
    )
    parser.add_argument(
        "--c54-intercall-static",
        action="store_true",
        help=(
            "With C04, retain read-only static-contact regular solve/writeback descriptor and solver-body "
            "windows in exact inter-call order."
        ),
    )
    parser.add_argument(
        "--c26-target-static",
        action="store_true",
        help="Capture only the selected C04 frame's target static writeback boundaries.",
    )
    parser.add_argument(
        "--c26-target-static-frame",
        type=int,
        default=3,
        help="C04 solverSetupSolve frame index for --c26-target-static (default: 3).",
    )
    parser.add_argument(
        "--c05-pcm-window",
        action="store_true",
        help="With C03, capture a short post-contact convex-convex PCM cache/ContactBuffer window.",
    )
    parser.add_argument(
        "--c05-pcm-window-limit",
        type=int,
        default=6,
        help="Maximum PCM calls retained by --c05-pcm-window (1-12).",
    )
    parser.add_argument(
        "--c25-history-pcm",
        action="store_true",
        help="Retain a bounded read-only record for every positive stone-stone PCM across a multi-shot session.",
    )
    parser.add_argument(
        "--c25-history-pcm-limit",
        type=int,
        default=32,
        help="Maximum all-call records retained by --c25-history-pcm (1-64).",
    )
    parser.add_argument(
        "--game-object-activation-hook",
        action="store_true",
        help="Passively hook UnityEngine.GameObject.SetActive for native activation lifecycle auditing.",
    )
    parser.add_argument(
        "--mesh-collider-activation-hook",
        action="store_true",
        help="Passively hook MeshCollider slots 42/43/44 before/after state.",
    )
    parser.add_argument(
        "--overlap-created-hook",
        action="store_true",
        help="Passively hook ScScene.OnOverlapCreatedTask for ShapeInteraction creation order.",
    )
    parser.add_argument(
        "--cooked-hull-hook",
        action="store_true",
        help="Install the PhysX func72915 cooked-hull desc hook once the wasm table is captured.",
    )
    parser.add_argument(
        "--physx-native-hooks",
        action="store_true",
        help="Install ContactBuffer / solver-row PhysX native table hooks once the wasm table is captured.",
    )
    parser.add_argument(
        "--physx-native-names",
        default="",
        help="Comma-separated native hook names to install; empty installs the configured set.",
    )
    parser.add_argument(
        "--physx-native-always-names",
        default="",
        help="Comma-separated hook names that dump even when global capture mode is armed.",
    )
    parser.add_argument(
        "--c108-static-target-native-x",
        type=float,
        help=(
            "Read-only C108 selector: retain PxcPCMContactConvexMesh only when one "
            "input transform has this native X. Requires --c108-static-target-native-z."
        ),
    )
    parser.add_argument(
        "--c108-static-target-native-z",
        type=float,
        help="Read-only C108 selector native Z paired with --c108-static-target-native-x.",
    )
    parser.add_argument(
        "--c108-static-target-native-tolerance",
        type=float,
        default=0.002,
        help="C108 native X/Z selector tolerance in metres (default: 0.002).",
    )
    parser.add_argument(
        "--physx-native-arm-only-names",
        default="",
        help="Comma-separated hook names that arm native capture without writing their own payload.",
    )
    parser.add_argument(
        "--physx-native-dynamic-dynamic-only-names",
        default="",
        help="Comma-separated finalizer hook names restricted to dynamic-dynamic contact descriptors.",
    )
    parser.add_argument(
        "--physx-native-dynamic-dynamic-task-only-names",
        default="",
        help="Comma-separated task hook names dumped only once a manager has two rigid cores.",
    )
    parser.add_argument(
        "--physx-native-rigid-core-windows",
        action="store_true",
        help="Attach compact raw PxsRigidCore windows to selected contact-manager task dumps.",
    )
    parser.add_argument(
        "--physx-native-rigid-core-bytes",
        type=int,
        default=160,
        help="Bytes stored for each opt-in PxsRigidCore window.",
    )
    parser.add_argument(
        "--physx-native-max-dumps",
        type=int,
        default=16,
        help="Maximum native-state dumps per PhysX hook.",
    )
    parser.add_argument(
        "--physx-native-arm-ms",
        type=int,
        default=2000,
        help="Milliseconds to capture finalizer/solver hooks after a stone-stone PCM hit arms the probe.",
    )
    parser.add_argument(
        "--physx-native-window-bytes",
        type=int,
        default=8192,
        help="Bytes to dump from each pointer-looking PhysX hook argument.",
    )
    parser.add_argument(
        "--physx-native-max-pointer-args",
        type=int,
        default=12,
        help="Maximum pointer-looking arguments dumped for each native hook call.",
    )
    parser.add_argument(
        "--physx-native-solver-constraint-bytes",
        type=int,
        default=4096,
        help="Bytes to dump from each decoded PxSolverConstraintDesc.constraint pointer.",
    )
    parser.add_argument(
        "--physx-native-solver-desc-records",
        type=int,
        default=4,
        help="Maximum PxSolverConstraintDesc records to decode from a contactDesc.desc pointer.",
    )
    parser.add_argument(
        "--physx-native-solver-body-bytes",
        type=int,
        default=256,
        help="Bytes to dump from each decoded PxSolverConstraintDesc.bodyA/bodyB pointer.",
    )
    parser.add_argument(
        "--physx-native-geometry-bytes",
        type=int,
        default=96,
        help="Bytes to dump from each PCM GeometryUnion argument.",
    )
    parser.add_argument(
        "--physx-native-hull-data-bytes",
        type=int,
        default=512,
        help="Bytes to dump from decoded convex hull-data pointers in PCM GeometryUnion arguments.",
    )
    parser.add_argument(
        "--physx-native-cache-bytes",
        type=int,
        default=64,
        help="Bytes to dump from each PCM contact cache argument.",
    )
    parser.add_argument(
        "--physx-native-manifold-bytes",
        type=int,
        default=2048,
        help="Bytes to dump from decoded PCM persistent-manifold cachedData pointers.",
    )
    parser.add_argument(
        "--physx-native-shape-interaction-bytes",
        type=int,
        default=1024,
        help="Bytes to dump from decoded createFinalizeSolverContacts shapeInteraction pointers.",
    )
    parser.add_argument(
        "--physx-native-nested-raw",
        dest="physx_native_nested_raw",
        action="store_true",
        default=True,
        help=(
            "Also store raw bytes for nested pointer previews. Enabled by default because "
            "ConvexHullData/BigConvex support-map arrays live behind nested pointers."
        ),
    )
    parser.add_argument(
        "--no-physx-native-nested-raw",
        dest="physx_native_nested_raw",
        action="store_false",
        help="Disable nested raw byte dumps when intentionally making a lightweight native log.",
    )
    parser.add_argument(
        "--physx-native-capture-mode",
        choices=("armed", "always"),
        default="armed",
        help="Use 'always' to dump configured native hooks without waiting for ConvexConvex arming.",
    )
    parser.add_argument(
        "--sliding-trace-hooks",
        action="store_true",
        help="Install front-half sliding trace hooks for Random friction noise and optional FixedUpdate phase markers.",
    )
    parser.add_argument(
        "--sliding-trace-max-random-events",
        type=int,
        default=20000,
        help="Maximum Random hook events to stream during front-half sliding tracing.",
    )
    parser.add_argument(
        "--sliding-trace-max-fixed-events",
        type=int,
        default=8000,
        help="Maximum FixedUpdate enter/exit events to stream during front-half sliding tracing.",
    )
    parser.add_argument(
        "--sliding-trace-log-other-random-range",
        action="store_true",
        help="Also log Random.Range calls that are not the friction-noise range.",
    )
    parser.add_argument(
        "--sliding-trace-log-random-value",
        action="store_true",
        help="Also log Random.value calls. Off by default to keep traces focused.",
    )
    parser.add_argument(
        "--stream-events",
        action="store_true",
        help="Stream probe events from the page to a local HTTP sink instead of relying only on page.evaluate export.",
    )
    parser.add_argument(
        "--stream-no-store",
        action="store_true",
        help="When streaming events, avoid storing raw events in the browser-side probe.events array.",
    )
    parser.add_argument(
        "--no-poll-events",
        action="store_true",
        help="Do not pull probe.events through Playwright; useful for heavy native dumps during physics.",
    )
    parser.add_argument(
        "--auto-infinite-ui",
        action="store_true",
        help=(
            "Opt in to viewport-native Playwright clicks for infinite mode, ready, then start; "
            "used by controlled runtime sampling when desktop DPI makes watcher clicks unreliable."
        ),
    )
    parser.add_argument(
        "--auto-ui-protocol-ready-file",
        type=Path,
        help=(
            "With --auto-infinite-ui, defer only the start-match click until this marker is "
            "written by the two-player 7788 sampler handshake.  The ready click itself "
            "causes the server to issue that handshake."
        ),
    )
    parser.add_argument(
        "--unity-protocol-connected-file",
        type=Path,
        help="Write this marker once Unity has opened both game WebSockets.",
    )
    parser.add_argument(
        "--auto-ui-tcp-connected-file",
        type=Path,
        help="With --auto-infinite-ui, defer the Ready click until both raw sampler TCP slots connected.",
    )
    args = parser.parse_args()
    rng_friction_manifest: list[float] | None = None
    rng_friction_manifest_sha256: str | None = None
    if args.rng_friction_manifest_events is not None:
        source = args.rng_friction_manifest_events
        raw = source.read_bytes()
        rng_friction_manifest_sha256 = hashlib.sha256(raw).hexdigest()
        rng_friction_manifest = []
        for line_number, line in enumerate(raw.decode("utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("type") != "sliding.random_range.friction":
                continue
            data = event.get("data")
            if not isinstance(data, dict) or not isinstance(data.get("value"), (int, float)):
                raise ValueError(
                    f"{source}:{line_number}: friction event lacks numeric data.value"
                )
            rng_friction_manifest.append(float(data["value"]))
        if not rng_friction_manifest:
            raise ValueError(f"{source}: no sliding.random_range.friction events found")
    physx_native_names = [
        value.strip() for value in str(args.physx_native_names).split(",") if value.strip()
    ]
    physx_native_always_names = [
        value.strip() for value in str(args.physx_native_always_names).split(",") if value.strip()
    ]
    physx_native_arm_only_names = [
        value.strip() for value in str(args.physx_native_arm_only_names).split(",") if value.strip()
    ]
    physx_native_dynamic_dynamic_only_names = [
        value.strip()
        for value in str(args.physx_native_dynamic_dynamic_only_names).split(",")
        if value.strip()
    ]
    physx_native_dynamic_dynamic_task_only_names = [
        value.strip()
        for value in str(args.physx_native_dynamic_dynamic_task_only_names).split(",")
        if value.strip()
    ]
    if (args.c108_static_target_native_x is None) != (args.c108_static_target_native_z is None):
        raise ValueError("C108 static selector requires both --c108-static-target-native-x and --c108-static-target-native-z")
    pcm_call_trace_manifest = None
    if args.pcm_call_trace_manifest is not None:
        pcm_call_trace_manifest = json.loads(args.pcm_call_trace_manifest.read_text(encoding="utf-8"))
        patched_path = Path(pcm_call_trace_manifest["patched"])
        patched_bytes = patched_path.read_bytes()
        if hashlib.sha256(patched_bytes).hexdigest() != pcm_call_trace_manifest["patchedSha256"]:
            raise ValueError("PCM trace patched Wasm hash mismatch")
    a2_static_trace_options = json.dumps({
        "a2StaticTrace": bool(args.a2_static_trace),
        "a8StaticWindow": bool(args.a8_static_window),
        "a9SnapshotWindow": bool(args.a9_snapshot_window),
        "a10ReleaseOrientation": bool(args.a10_release_orientation),
        "a12DenseReleaseSerial": args.a12_dense_release_serial,
        "a12DenseWriteLimit": args.a12_dense_write_limit,
        "a12PhaseOrdinalMin": args.a12_phase_ordinal_min,
        "a12PhaseOrdinalMax": args.a12_phase_ordinal_max,
        "a12StaticPhaseTrace": args.a12_static_phase_trace,
        "pcmCallTraceManifest": pcm_call_trace_manifest,
        "pcmGeometryScaleTrace": args.pcm_geometry_scale_trace,
        "resetAllStoneRotations": bool(args.reset_all_stone_rotations),
        "rngSeedOnFirstFriction": args.rng_seed_on_first_friction,
        "rngFrictionManifest": rng_friction_manifest,
        "rngFrictionManifestSource": (
            str(args.rng_friction_manifest_events)
            if args.rng_friction_manifest_events is not None else None
        ),
        "c03FirstWriteback": bool(args.c03_first_writeback),
        "c03TargetNativeX": args.c03_target_native_x,
        "c03TargetNativeZ": args.c03_target_native_z,
        "c03TargetNativeTolerance": float(args.c03_target_native_tolerance),
        "c03ActiveSpeedMin": args.c03_active_speed_min,
        "c04DynamicWindow": bool(args.c04_dynamic_window),
        "c04DynamicWindowLimit": int(args.c04_dynamic_window_limit),
        "c31CompactCoreTrace": bool(args.c31_compact_core_trace),
        "c31CompactCoreRawFrameLimit": int(args.c31_compact_core_raw_frame_limit),
        "c54IntercallStatic": bool(args.c54_intercall_static),
        "c26TargetStatic": bool(args.c26_target_static),
        "c26TargetStaticFrame": int(args.c26_target_static_frame),
        "c05PcmWindow": bool(args.c05_pcm_window),
        "c05PcmWindowLimit": int(args.c05_pcm_window_limit),
        "c25HistoryPcm": bool(args.c25_history_pcm),
        "c25HistoryPcmLimit": int(args.c25_history_pcm_limit),
    })

    run_id = datetime.now().strftime("unity_runtime_probe_%Y%m%d_%H%M%S")
    output_dir = args.log_root / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    latest_path = output_dir / "events.latest.json"
    events_jsonl_path = output_dir / "events.jsonl"
    final_path = output_dir / "events.final.json"
    meta_path = output_dir / "meta.json"
    console_path = output_dir / "console.log"
    sink_server = None
    sink_state = None
    event_sink_url = None
    if args.stream_events:
        sink_server, sink_state, event_sink_url = _start_event_sink(events_jsonl_path)

    meta = {
        "url": args.url,
        "probe": str(args.probe),
        "pcm_call_trace_manifest": pcm_call_trace_manifest,
        "output_dir": str(output_dir),
        "events_jsonl": str(events_jsonl_path),
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "known_hooks": not args.no_known_hooks,
        "game_object_activation_hook": args.game_object_activation_hook,
        "cooked_hull_hook": args.cooked_hull_hook,
        "physx_native_hooks": args.physx_native_hooks,
        "physx_native_names": physx_native_names,
        "physx_native_always_names": physx_native_always_names,
        "physx_native_arm_only_names": physx_native_arm_only_names,
        "physx_native_dynamic_dynamic_only_names": physx_native_dynamic_dynamic_only_names,
        "physx_native_dynamic_dynamic_task_only_names": physx_native_dynamic_dynamic_task_only_names,
        "physx_native_rigid_core_windows": args.physx_native_rigid_core_windows,
        "physx_native_rigid_core_bytes": args.physx_native_rigid_core_bytes,
        "sliding_trace_hooks": args.sliding_trace_hooks,
        "a0_fixed_tick_resolver_hook": args.a0_fixed_tick_resolver_hook,
        "rng_seed_on_first_friction": args.rng_seed_on_first_friction,
        "rng_friction_manifest_events": (
            str(args.rng_friction_manifest_events) if args.rng_friction_manifest_events else None
        ),
        "rng_friction_manifest_draw_count": (
            len(rng_friction_manifest) if rng_friction_manifest is not None else None
        ),
        "rng_friction_manifest_source_sha256": rng_friction_manifest_sha256,
        "a2_static_trace": args.a2_static_trace,
        "a10_release_orientation": args.a10_release_orientation,
        "reset_all_stone_rotations": args.reset_all_stone_rotations,
        "c03_first_writeback": args.c03_first_writeback,
        "sliding_trace_options": {
            "maxRandomEvents": args.sliding_trace_max_random_events,
            "maxFixedUpdateEvents": args.sliding_trace_max_fixed_events,
            "logOtherRandomRange": args.sliding_trace_log_other_random_range,
            "logRandomValue": args.sliding_trace_log_random_value,
        },
        "physx_native_options": {
            "maxDumpsPerHook": args.physx_native_max_dumps,
            "armMs": args.physx_native_arm_ms,
            "argWindowBytes": args.physx_native_window_bytes,
            "maxPointerArgs": args.physx_native_max_pointer_args,
            "solverConstraintBytes": args.physx_native_solver_constraint_bytes,
            "solverDescRecords": args.physx_native_solver_desc_records,
            "solverBodyBytes": args.physx_native_solver_body_bytes,
            "geometryBytes": args.physx_native_geometry_bytes,
            "hullDataBytes": args.physx_native_hull_data_bytes,
            "cacheBytes": args.physx_native_cache_bytes,
            "manifoldBytes": args.physx_native_manifold_bytes,
            "shapeInteractionBytes": args.physx_native_shape_interaction_bytes,
            "includeNestedRawBytes": args.physx_native_nested_raw,
            "captureMode": args.physx_native_capture_mode,
        },
        "stream_events": args.stream_events,
        "stream_no_store": args.stream_no_store,
        "no_poll_events": args.no_poll_events,
        "auto_infinite_ui": args.auto_infinite_ui,
        "auto_ui_protocol_ready_file": (
            str(args.auto_ui_protocol_ready_file) if args.auto_ui_protocol_ready_file else None
        ),
        "unity_protocol_connected_file": (
            str(args.unity_protocol_connected_file) if args.unity_protocol_connected_file else None
        ),
        "auto_ui_tcp_connected_file": (
            str(args.auto_ui_tcp_connected_file) if args.auto_ui_tcp_connected_file else None
        ),
        "event_sink_url": event_sink_url,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(meta, indent=2, ensure_ascii=False), flush=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=args.headless,
            args=[
                f"--window-size={args.width},{args.height}",
                "--disable-web-security",
                "--autoplay-policy=no-user-gesture-required",
            ],
        )
        context = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            ignore_https_errors=True,
        )
        if pcm_call_trace_manifest is not None:
            def serve_pcm_trace_wasm(route: Any) -> None:
                response = route.fetch()
                body = response.body()
                raw_is_gzip = body[:2] == b"\x1f\x8b"
                source_bytes = gzip.decompress(body) if raw_is_gzip else body
                source_hash = hashlib.sha256(source_bytes).hexdigest()
                if source_hash != pcm_call_trace_manifest["sourceSha256"]:
                    print("[pcm-trace] refusing unexpected Wasm " + source_hash, flush=True)
                    route.abort()
                    return
                headers = dict(response.headers)
                headers.pop("content-length", None)
                headers.pop("content-encoding", None)
                headers.pop("etag", None)
                headers["content-type"] = "application/wasm"
                routed_bytes = gzip.compress(patched_bytes) if raw_is_gzip else patched_bytes
                route.fulfill(status=response.status, headers=headers, body=routed_bytes)
                _write_json_atomic(output_dir / "pcm_call_trace_wasm.json", {
                    "url": route.request.url, "sourceSha256": source_hash,
                    "patchedSha256": pcm_call_trace_manifest["patchedSha256"],
                    "responseBodyWasGzip": raw_is_gzip,
                    "manifest": str(args.pcm_call_trace_manifest.resolve()),
                })
            context.route("**/*.wasm*", serve_pcm_trace_wasm)
        probe_config: dict[str, Any] = {}
        if args.cooked_hull_hook:
            probe_config["autoCookedHullHook"] = True
        if rng_friction_manifest is not None:
            probe_config["rngFrictionManifest"] = rng_friction_manifest
            probe_config["rngFrictionManifestSource"] = str(args.rng_friction_manifest_events)
        if event_sink_url:
            probe_config["eventSinkUrl"] = event_sink_url
            if args.stream_no_store:
                probe_config["storeEvents"] = False
        if probe_config:
            config_script = (
                "window.__curlingProbeConfig = "
                + json.dumps(probe_config)
                + ";\n"
                + args.probe.read_text(encoding="utf-8")
            )
            context.add_init_script(script=config_script)
        else:
            context.add_init_script(path=str(args.probe))
        page = context.new_page()

        def handle_console(msg: Any) -> None:
            line = f"[browser:{msg.type}] {msg.text}"
            print(line, flush=True)
            with console_path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")

        page.on("console", handle_console)
        page.on("pageerror", lambda exc: print(f"[browser:pageerror] {exc}", flush=True))
        page.goto(args.url, wait_until="domcontentloaded")
        page.bring_to_front()

        # Browser chrome uses desktop pixels but Playwright uses the CSS
        # viewport. These coordinates were measured in the default 1500x950
        # viewport and intentionally remain opt-in.
        auto_ui_steps = (
            # Infinite mode first opens the in-canvas protocol listener, then
            # the two external sampler slots must update the waiting-room UI.
            # Leave both transitions visible before clicking the next control.
            ((475, 534), 5.0, "infinite_mode"),
            ((761, 709), 3.0, "ready"),
            ((1015, 754), 0.0, "start_match"),
        ) if args.auto_infinite_ui else ()
        auto_ui_index = 0
        auto_ui_next_at = time.monotonic()
        # This mode exists solely to make a fragile UI entry reproducible.  Keep
        # its audit trail with the runtime event summary, so a no-shot session
        # tells us whether it missed the canvas or the Unity control itself.
        auto_ui_events: list[dict[str, Any]] = []

        print(f"[probe] browser opened: {args.url}", flush=True)
        print(f"[probe] live events: {latest_path}", flush=True)

        last_count = -1
        exported_event_count = 0
        known_hooks_ready = bool(args.no_known_hooks)
        cooked_hull_ready = not args.cooked_hull_hook
        native_hooks_ready = not args.physx_native_hooks
        sliding_hooks_ready = not args.sliding_trace_hooks
        a0_fixed_tick_resolver_ready = not args.a0_fixed_tick_resolver_hook
        activation_hook_ready = not args.game_object_activation_hook
        mesh_collider_activation_hook_ready = not args.mesh_collider_activation_hook
        overlap_created_hook_ready = not args.overlap_created_hook
        auto_ui_ready = not bool(auto_ui_steps)
        auto_ui_ready_at: float | None = None
        try:
            while True:
                try:
                    if auto_ui_steps and not auto_ui_ready:
                        result = _safe_evaluate(
                            page,
                            """() => {
                              const loading = document.querySelector('#unity-loading-bar');
                              return !!loading && getComputedStyle(loading).display === 'none';
                            }""",
                        )
                        auto_ui_ready = result is True
                        if auto_ui_ready:
                            # The WebGL loader hides its HTML progress bar before
                            # Unity has finished the native splash and created the
                            # in-canvas menu.  Give that handoff a fixed, visible
                            # settle period; this only affects the opt-in UI helper.
                            auto_ui_ready_at = time.monotonic() + 4.0
                    if (
                        args.unity_protocol_connected_file is not None
                        # The server's CONNECTED reply itself can wait for
                        # the external 7788 clients.  Publish after infinite
                        # mode's own initialization delay instead of waiting
                        # for that reply, otherwise browser and sampler form
                        # a circular wait.
                        and auto_ui_index >= 1
                        and time.monotonic() >= auto_ui_next_at
                        and not args.unity_protocol_connected_file.is_file()
                    ):
                        _write_json_atomic(
                            args.unity_protocol_connected_file,
                            {"infiniteModeSettledAt": datetime.now().isoformat()},
                        )
                    if (
                        auto_ui_index < len(auto_ui_steps)
                        and known_hooks_ready
                        and sliding_hooks_ready
                        and a0_fixed_tick_resolver_ready
                        and auto_ui_ready
                        and (auto_ui_ready_at is None or time.monotonic() >= auto_ui_ready_at)
                        and time.monotonic() >= auto_ui_next_at
                        # Infinite mode asynchronously opens two game sockets.
                        # Do not spend the one-shot ready click until both
                        # players have actually entered the waiting room.
                        and (
                            auto_ui_steps[auto_ui_index][2] != "ready"
                            or args.auto_ui_tcp_connected_file is None
                            or args.auto_ui_tcp_connected_file.is_file()
                        )
                        and (
                            auto_ui_steps[auto_ui_index][2] != "start_match"
                            or args.auto_ui_protocol_ready_file is None
                            or args.auto_ui_protocol_ready_file.is_file()
                        )
                    ):
                        (x, y), delay, label = auto_ui_steps[auto_ui_index]
                        page.bring_to_front()
                        target = _safe_evaluate(
                            page,
                            f"""() => {{
                              const canvas = document.querySelector('#unity-canvas');
                              const rect = canvas ? canvas.getBoundingClientRect() : null;
                              const hit = document.elementFromPoint({x}, {y});
                              return {{
                                canvasRect: rect ? {{x: rect.x, y: rect.y, width: rect.width, height: rect.height}} : null,
                                hit: hit ? {{tag: hit.tagName, id: hit.id || null, className: hit.className || null}} : null
                              }};
                            }}""",
                        )
                        page.mouse.click(x, y)
                        screenshot_path = output_dir / f"auto_ui_{auto_ui_index:02d}_{label}.png"
                        try:
                            page.screenshot(path=str(screenshot_path))
                        except PlaywrightError as exc:
                            screenshot_path = None
                            print(f"[probe] auto_ui_screenshot_error={exc}", flush=True)
                        auto_ui_events.append({
                            "label": label,
                            "viewport": {"x": x, "y": y},
                            "target": target,
                            "screenshot": str(screenshot_path) if screenshot_path else None,
                            "atSeconds": time.monotonic(),
                        })
                        print(f"[probe] auto_ui_click={label} viewport=({x},{y})", flush=True)
                        auto_ui_index += 1
                        auto_ui_next_at = time.monotonic() + delay
                    if sink_state and args.no_poll_events:
                        stream_summary = sink_state.summary()
                        installed = set(stream_summary.get("installedHookNames") or [])
                        known_hooks_ready = known_hooks_ready or {
                            "CurlingStoneNew.OnCollisionEnter",
                            "ExtendedColliders3D.Awake",
                        }.issubset(installed)
                        native_hooks_ready = native_hooks_ready or bool(
                            stream_summary.get("nativeHooksInstalled")
                        )
                        sliding_hooks_ready = sliding_hooks_ready or bool(
                            stream_summary.get("slidingHooksInstalled")
                        )
                        activation_hook_ready = activation_hook_ready or bool(
                            stream_summary.get("gameObjectActivationHookInstalled")
                        )
                        mesh_collider_activation_hook_ready = (
                            mesh_collider_activation_hook_ready
                            or {
                                "MeshCollider.activationFlush",
                                "MeshCollider.transformRefresh",
                                "MeshCollider.stateRefresh",
                            }.issubset(set(installed))
                        )
                        if args.cooked_hull_hook:
                            cooked_hull_ready = cooked_hull_ready or (
                                "QuickHullConvexHullLib.fillConvexMeshDesc" in installed
                            )

                    if not args.no_known_hooks and not known_hooks_ready:
                        result = _safe_evaluate(
                            page,
                            """() => {
                          if (!window.__curlingProbe) return null;
                          window.__curlingProbe.scanAndHookFS();
                          if (
                            !window.__curlingProbe._knownHooksAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {
                            const installed = window.__curlingProbe.installKnownCurlingHooks();
                            window.__curlingProbe._knownHooksAttempted = true;
                            return installed;
                          }
                          return true;
                        }""",
                        )
                        if sink_state and args.no_poll_events:
                            # Readiness will be inferred from streamed table_hook.installed events.
                            pass
                        elif result and not (isinstance(result, dict) and result.get("error")):
                            known_hooks_ready = True

                    if args.cooked_hull_hook and not cooked_hull_ready:
                        result = _safe_evaluate(
                            page,
                            """() => {
                          if (!window.__curlingProbe) return null;
                          if (
                            !window.__curlingProbe._cookedHullHookAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {
                            const installed = window.__curlingProbe.installCookedHullHook();
                            window.__curlingProbe._cookedHullHookAttempted = true;
                            return !!installed;
                          }
                          return true;
                        }""",
                        )
                        if not sink_state and result:
                            cooked_hull_ready = True

                    if args.game_object_activation_hook and not activation_hook_ready:
                        result = _safe_evaluate(
                            page,
                            """() => {
                          if (!window.__curlingProbe) return null;
                          if (
                            !window.__curlingProbe._gameObjectActivationHookAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {
                            const installed = window.__curlingProbe.installGameObjectActivationHook({
                              windowBytes: 128,
                              includeRawBytes: false
                            });
                            window.__curlingProbe._gameObjectActivationHookAttempted = true;
                            return !!installed;
                          }
                          return true;
                        }""",
                        )
                        if not sink_state and result:
                            activation_hook_ready = True

                    if args.mesh_collider_activation_hook and not mesh_collider_activation_hook_ready:
                        result = _safe_evaluate(
                            page,
                            """() => {
                          if (!window.__curlingProbe) return null;
                          if (
                            !window.__curlingProbe._meshColliderActivationHookAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {
                            const installed = window.__curlingProbe.installMeshColliderPhysicsHooks({
                              componentBytes: 192,
                              backendBytes: 320,
                              includeRawBytes: true,
                              maxEvents: 96
                            });
                            window.__curlingProbe._meshColliderActivationHookAttempted = true;
                            return !!installed;
                          }
                          return true;
                        }""",
                        )
                        if not sink_state and result:
                            mesh_collider_activation_hook_ready = True

                    if args.overlap_created_hook and not overlap_created_hook_ready:
                        result = _safe_evaluate(
                            page,
                            """() => {
                          if (!window.__curlingProbe) return null;
                          if (
                            !window.__curlingProbe._overlapCreatedHookAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {
                            const installed = window.__curlingProbe.installOverlapCreatedHook({
                              maxEvents: 128,
                              maxPairs: 32
                            });
                            window.__curlingProbe._overlapCreatedHookAttempted = true;
                            return !!installed;
                          }
                          return true;
                        }""",
                        )
                        if not sink_state and result:
                            overlap_created_hook_ready = True

                    if args.sliding_trace_hooks and not sliding_hooks_ready:
                        sliding_hook_options = json.dumps(
                            {
                                "maxRandomEvents": args.sliding_trace_max_random_events,
                                "maxFixedUpdateEvents": args.sliding_trace_max_fixed_events,
                                "logOtherRandomRange": args.sliding_trace_log_other_random_range,
                                "logRandomValue": args.sliding_trace_log_random_value,
                            }
                        )
                        result = _safe_evaluate(
                            page,
                            f"""() => {{
                          if (!window.__curlingProbe) return null;
                          if (
                            !window.__curlingProbe._slidingTraceHooksAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {{
                            const installed = window.__curlingProbe.installSlidingTraceHooks({sliding_hook_options});
                            window.__curlingProbe._slidingTraceHooksAttempted = true;
                            return installed.map(h => ({{
                              index: h.index,
                              name: h.name
                            }}));
                          }}
                          return true;
                        }}""",
                        )
                        if not sink_state and result:
                            sliding_hooks_ready = True

                    if args.a0_fixed_tick_resolver_hook and not a0_fixed_tick_resolver_ready:
                        result = _safe_evaluate(
                            page,
                            """() => {
                          if (!window.__curlingProbe) return null;
                          if (
                            !window.__curlingProbe._a0FixedTickResolverAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {
                            const installed = window.__curlingProbe.installA0FixedTickResolverHook("""
                            + a2_static_trace_options
                            + """);
                            window.__curlingProbe._a0FixedTickResolverAttempted = true;
                            return installed.map(h => ({ index: h.index, name: h.name }));
                          }
                          return false;
                        }""",
                        )
                        if result and not (isinstance(result, dict) and result.get("error")):
                            a0_fixed_tick_resolver_ready = True

                    if args.physx_native_hooks and not native_hooks_ready:
                        native_hook_options = json.dumps(
                            {
                                "maxDumpsPerHook": args.physx_native_max_dumps,
                                "armMs": args.physx_native_arm_ms,
                                "includeRawBytes": True,
                                "includeNestedRawBytes": args.physx_native_nested_raw,
                                "argWindowBytes": args.physx_native_window_bytes,
                                "maxPointerArgs": args.physx_native_max_pointer_args,
                                "solverConstraintBytes": args.physx_native_solver_constraint_bytes,
                                "solverDescRecords": args.physx_native_solver_desc_records,
                                "solverBodyBytes": args.physx_native_solver_body_bytes,
                                "geometryBytes": args.physx_native_geometry_bytes,
                                "hullDataBytes": args.physx_native_hull_data_bytes,
                                "cacheBytes": args.physx_native_cache_bytes,
                                "manifoldBytes": args.physx_native_manifold_bytes,
                                "shapeInteractionBytes": args.physx_native_shape_interaction_bytes,
                                "captureMode": args.physx_native_capture_mode,
                                "names": physx_native_names,
                                "alwaysNames": physx_native_always_names,
                                "c108StaticTargetNativeX": args.c108_static_target_native_x,
                                "c108StaticTargetNativeZ": args.c108_static_target_native_z,
                                "c108StaticTargetNativeTolerance": args.c108_static_target_native_tolerance,
                                "armOnlyNames": physx_native_arm_only_names,
                                "dynamicDynamicOnlyNames": physx_native_dynamic_dynamic_only_names,
                                "dynamicDynamicTaskOnlyNames": physx_native_dynamic_dynamic_task_only_names,
                                "includeRigidCoreWindows": args.physx_native_rigid_core_windows,
                                "rigidCoreBytes": args.physx_native_rigid_core_bytes,
                            }
                        )
                        result = _safe_evaluate(
                            page,
                            f"""() => {{
                          if (!window.__curlingProbe) return null;
                          window.__curlingProbe.scanAndHookFS();
                          if (
                            !window.__curlingProbe._physxNativeHooksAttempted &&
                            window.__curlingProbe.tables &&
                            window.__curlingProbe.tables.length
                          ) {{
                            const installed = window.__curlingProbe.installPhysXNativeHooks({native_hook_options});
                            window.__curlingProbe._physxNativeHooksAttempted = true;
                            return installed.map(h => ({{
                              index: h.index,
                              name: h.name
                            }}));
                          }}
                          return true;
                        }}""",
                        )
                        if not sink_state and result:
                            native_hooks_ready = True

                    if args.no_poll_events:
                        stream_summary = sink_state.summary() if sink_state else {}
                        latest_summary = {
                            "exportedAt": datetime.now().isoformat(timespec="milliseconds"),
                            "eventsJsonl": str(events_jsonl_path),
                            "knownHooksReady": known_hooks_ready,
                            "cookedHullReady": cooked_hull_ready,
                            "meshColliderActivationHookReady": mesh_collider_activation_hook_ready,
                            "overlapCreatedHookReady": overlap_created_hook_ready,
                            "slidingHooksReady": sliding_hooks_ready,
                            "a0FixedTickResolverReady": a0_fixed_tick_resolver_ready,
                            "nativeHooksReady": native_hooks_ready,
                            "autoUiReady": auto_ui_ready,
                            "autoUiReadyAt": auto_ui_ready_at,
                            "autoUiEvents": auto_ui_events,
                            **stream_summary,
                        }
                        _write_json_atomic(latest_path, latest_summary)
                        count = int(latest_summary.get("streamedEventCount") or 0)
                        if count != last_count:
                            print(f"[probe] streamed_events={count}", flush=True)
                            last_count = count
                        time.sleep(args.interval)
                        continue

                    payload = _safe_evaluate(
                        page,
                        f"""() => {{
                      const p = window.__curlingProbe;
                      if (!p) return {{ probe_missing: true }};
                      const start = {exported_event_count};
                      const events = (p.events || []).slice(start);
                      return {{
                        installedAt: p.installedAt,
                        exportedAt: new Date().toISOString(),
                        eventCount: p.events.length,
                        exportStart: start,
                        events: events,
                        hookSummary: (p.hooks || []).map(h => ({{
                          index: h.index,
                          name: h.name,
                          calls: h.calls
                        }})),
                        physxNativeCapture: p.physxNativeCapture || null,
                        instanceCount: (p.instances || []).length,
                        memoryCount: (p.memories || []).length,
                        tableCount: (p.tables || []).length
                        ,bindingDiagnostics: {{
                          protocolMessageSerial:p.protocolMessageSerial,
                          pendingReleaseProtocol:p.pendingReleaseProtocol,
                          lastResetProtocol:p.lastResetProtocol,
                          angularWriteCount:p.a0FixedTickResolver && p.a0FixedTickResolver.a12DenseWriteCount,
                          websocketWrapperCurrent:window.WebSocket===p.webSocketWrapper,
                          changedTableHooks:(p.hooks || []).filter(h =>
                            h.installedFunction && h.tableRecord.table.get(h.index)!==h.installedFunction)
                            .map(h => ({{index:h.index,name:h.name,
                              currentFunctionName:h.tableRecord.table.get(h.index).name}}))
                        }}
                      }};
                    }}""",
                    )
                    new_events = payload.get("events") if isinstance(payload, dict) else None
                    if isinstance(new_events, list) and new_events:
                        with events_jsonl_path.open("a", encoding="utf-8") as handle:
                            for event in new_events:
                                handle.write(json.dumps(event, ensure_ascii=False) + "\n")
                        exported_event_count += len(new_events)
                    latest_summary = dict(payload) if isinstance(payload, dict) else {"payload": payload}
                    latest_summary["frameUrls"] = [frame.url for frame in page.frames]
                    latest_summary["pageUrls"] = [item.url for item in context.pages]
                    latest_summary["eventsJsonl"] = str(events_jsonl_path)
                    latest_summary["newEventCount"] = len(new_events) if isinstance(new_events, list) else 0
                    # Keep latest lightweight; all raw events are in events.jsonl.
                    latest_summary["events"] = (
                        new_events[-20:] if isinstance(new_events, list) else []
                    )
                    _write_json_atomic(latest_path, latest_summary)
                    count = int(payload.get("eventCount") or 0) if isinstance(payload, dict) else 0
                    if count != last_count:
                        print(f"[probe] events={count}", flush=True)
                        last_count = count
                except Exception as exc:
                    line = f"[probe:error] {type(exc).__name__}: {exc}"
                    print(line, flush=True)
                    with console_path.open("a", encoding="utf-8") as handle:
                        handle.write(line + "\n")
                        handle.write(traceback.format_exc() + "\n")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("[probe] stopping", flush=True)
        finally:
            payload = _safe_evaluate(
                page,
                f"""() => {{
                  const p = window.__curlingProbe;
                  if (!p) return {{ probe_missing: true }};
                  const start = {exported_event_count};
                  const events = (p.events || []).slice(start);
                  return {{
                    installedAt: p.installedAt,
                    exportedAt: new Date().toISOString(),
                    eventCount: p.events.length,
                    exportStart: start,
                    events: events,
                  hookSummary: (p.hooks || []).map(h => ({{
                    index: h.index,
                    name: h.name,
                    calls: h.calls
                  }})),
                    physxNativeCapture: p.physxNativeCapture || null,
                    instanceCount: (p.instances || []).length,
                    memoryCount: (p.memories || []).length,
                    tableCount: (p.tables || []).length
                  }};
                }}""",
            )
            new_events = payload.get("events") if isinstance(payload, dict) else None
            if isinstance(new_events, list) and new_events:
                with events_jsonl_path.open("a", encoding="utf-8") as handle:
                    for event in new_events:
                        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
            final_summary = dict(payload) if isinstance(payload, dict) else {"payload": payload}
            final_summary["eventsJsonl"] = str(events_jsonl_path)
            final_summary["newEventCount"] = len(new_events) if isinstance(new_events, list) else 0
            final_summary["events"] = new_events[-20:] if isinstance(new_events, list) else []
            _write_json_atomic(final_path, final_summary)
            context.close()
            browser.close()
            if sink_server:
                sink_server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
