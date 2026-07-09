#!/usr/bin/env python3
"""Launch the local Unity WebGL client with the runtime probe pre-injected."""

from __future__ import annotations

import argparse
import json
import time
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--probe", type=Path, default=DEFAULT_PROBE)
    parser.add_argument("--log-root", type=Path, default=DEFAULT_LOG_ROOT)
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--width", type=int, default=1500)
    parser.add_argument("--height", type=int, default=950)
    parser.add_argument("--no-known-hooks", action="store_true")
    parser.add_argument(
        "--cooked-hull-hook",
        action="store_true",
        help="Install the PhysX func72915 cooked-hull desc hook once the wasm table is captured.",
    )
    args = parser.parse_args()

    run_id = datetime.now().strftime("unity_runtime_probe_%Y%m%d_%H%M%S")
    output_dir = args.log_root / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    latest_path = output_dir / "events.latest.json"
    final_path = output_dir / "events.final.json"
    meta_path = output_dir / "meta.json"
    console_path = output_dir / "console.log"

    meta = {
        "url": args.url,
        "probe": str(args.probe),
        "output_dir": str(output_dir),
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "known_hooks": not args.no_known_hooks,
        "cooked_hull_hook": args.cooked_hull_hook,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(meta, indent=2, ensure_ascii=False), flush=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
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
        if args.cooked_hull_hook:
            config_script = (
                "window.__curlingProbeConfig = "
                + json.dumps({"autoCookedHullHook": True})
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

        print(f"[probe] browser opened: {args.url}", flush=True)
        print(f"[probe] live events: {latest_path}", flush=True)

        last_count = -1
        try:
            while True:
                if not args.no_known_hooks:
                    _safe_evaluate(
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

                if args.cooked_hull_hook:
                    _safe_evaluate(
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

                payload = _safe_evaluate(
                    page,
                    """() => {
                      const p = window.__curlingProbe;
                      if (!p) return { probe_missing: true };
                      return {
                        installedAt: p.installedAt,
                        exportedAt: new Date().toISOString(),
                        eventCount: p.events.length,
                        events: p.events,
                        hookSummary: (p.hooks || []).map(h => ({
                          index: h.index,
                          name: h.name,
                          calls: h.calls
                        })),
                        instanceCount: (p.instances || []).length,
                        memoryCount: (p.memories || []).length,
                        tableCount: (p.tables || []).length
                      };
                    }""",
                )
                latest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
                count = int(payload.get("eventCount") or 0) if isinstance(payload, dict) else 0
                if count != last_count:
                    print(f"[probe] events={count}", flush=True)
                    last_count = count
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("[probe] stopping", flush=True)
        finally:
            payload = _safe_evaluate(
                page,
                """() => {
                  const p = window.__curlingProbe;
                  if (!p) return { probe_missing: true };
                  return {
                    installedAt: p.installedAt,
                    exportedAt: new Date().toISOString(),
                    eventCount: p.events.length,
                    events: p.events,
                    hookSummary: (p.hooks || []).map(h => ({
                      index: h.index,
                      name: h.name,
                      calls: h.calls
                    })),
                    instanceCount: (p.instances || []).length,
                    memoryCount: (p.memories || []).length,
                    tableCount: (p.tables || []).length
                  };
                }""",
            )
            final_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            context.close()
            browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
