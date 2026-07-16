#!/usr/bin/env python3
"""Serve the local Unity WebGL page through a same-origin probe-injecting proxy.

Use this when the operator must interact with the system browser rather than a
Playwright-owned window. The initial HTML receives the passive Wasm probe before
Unity loads; all other requests are forwarded unchanged to the original local
course server. Probe events are persisted at ``/__curling_probe_event``.
"""

from __future__ import annotations

import argparse
import json
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urljoin


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROBE = PROJECT_ROOT / "tools" / "reverse" / "unity_webgl_runtime_probe.js"


class EventWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()
        self.count = 0

    def append(self, event: Any) -> None:
        if not isinstance(event, dict):
            raise ValueError("probe event must be an object")
        with self.lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False) + "\n")
            self.count += 1


def _header_value(headers: Any, name: str) -> str | None:
    value = headers.get(name)
    return str(value) if value is not None else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", default="http://127.0.0.1:9007/")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9010)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--events", type=Path, required=True)
    args = parser.parse_args()

    probe_source = args.probe.read_text(encoding="utf-8")
    args.events.parent.mkdir(parents=True, exist_ok=True)
    writer = EventWriter(args.events)
    upstream = args.upstream.rstrip("/") + "/"
    injected_config = json.dumps(
        {
            "eventSinkUrl": f"http://{args.host}:{args.port}/__curling_probe_event",
            "storeEvents": False,
        }
    )

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, _format: str, *_values: Any) -> None:
            return

        def _send_cors(self) -> None:
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "content-type")

        def do_OPTIONS(self) -> None:  # noqa: N802
            if self.path != "/__curling_probe_event":
                self.send_error(404)
                return
            self.send_response(204)
            self._send_cors()
            self.end_headers()

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/__curling_probe_event":
                self.send_error(405)
                return
            try:
                length = int(self.headers.get("Content-Length") or "0")
                writer.append(json.loads(self.rfile.read(length).decode("utf-8")))
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
                self.send_error(400)
                return
            self.send_response(204)
            self._send_cors()
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            target = urljoin(upstream, self.path.lstrip("/"))
            request = urllib.request.Request(
                target,
                headers={"Accept-Encoding": "identity", "User-Agent": self.headers.get("User-Agent", "")},
            )
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    body = response.read()
                    content_type = _header_value(response.headers, "Content-Type") or "application/octet-stream"
                    status = response.status
            except urllib.error.HTTPError as error:
                body = error.read()
                content_type = _header_value(error.headers, "Content-Type") or "text/plain"
                status = error.code
            except urllib.error.URLError as error:
                self.send_error(502, str(error.reason))
                return

            if "text/html" in content_type.lower():
                html = body.decode("utf-8")
                injection = (
                    "<script>window.__curlingProbeConfig="
                    + injected_config
                    + ";\n"
                    + probe_source
                    + "</script>"
                )
                marker = "</head>"
                html = html.replace(marker, injection + marker, 1) if marker in html else injection + html
                body = html.encode("utf-8")

            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        json.dumps(
            {
                "url": f"http://{args.host}:{args.port}/?connectkey=localtest",
                "events": str(args.events),
                "upstream": upstream,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
