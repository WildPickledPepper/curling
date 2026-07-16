# -*- coding: utf-8 -*-
"""Best-effort UI watcher for the standalone Unity curling page.

It watches screenshots and clicks the visible buttons needed to start the
infinite training match once the desktop is unlocked and the Unity page is
visible.  This is intentionally conservative: it only clicks when enough visual
evidence is present.
"""

from __future__ import annotations

import argparse
import ctypes
import time
from pathlib import Path
from typing import Callable, Optional, Tuple

from PIL import ImageGrab


def enable_dpi_awareness() -> None:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except Exception:
        pass
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def activate_edge() -> bool:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    enum_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def title(hwnd: int) -> str:
        n = user32.GetWindowTextLengthW(hwnd)
        if not n:
            return ""
        buf = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, buf, n + 1)
        return buf.value

    # Do not accept a broad "curling" title match by itself.  The development
    # workspace regularly has source tabs such as `curling_pyphysx_hybrid`, and
    # the old matcher could therefore foreground VS Code, screenshot it, and
    # leave the actual Chromium Unity canvas untouched.  The launched page has
    # the stable prefix `Unity WebGL Player` in its native window title.
    windows: list[tuple[int, int]] = []

    def callback(hwnd: int, _: int) -> bool:
        if user32.IsWindowVisible(hwnd):
            text = title(hwnd)
            if "Unity WebGL Player" in text:
                windows.append((0, hwnd))
            elif "curling" in text and (
                "Google Chrome" in text or "Microsoft Edge" in text or "Chromium" in text
            ):
                # A conservative compatibility fallback for a browser build
                # that omits the Unity prefix.  It still excludes editors.
                windows.append((1, hwnd))
        return True

    user32.EnumWindows(enum_proc(callback), 0)
    if not windows:
        return False

    windows.sort(key=lambda item: item[0])
    hwnd = windows[0][1]
    user32.ShowWindow(hwnd, 9)
    time.sleep(0.1)
    fg = user32.GetForegroundWindow()
    current_thread = kernel32.GetCurrentThreadId()
    fg_thread = user32.GetWindowThreadProcessId(fg, None)
    target_thread = user32.GetWindowThreadProcessId(hwnd, None)
    user32.AttachThreadInput(current_thread, fg_thread, True)
    user32.AttachThreadInput(current_thread, target_thread, True)
    user32.BringWindowToTop(hwnd)
    user32.SetActiveWindow(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(current_thread, target_thread, False)
    user32.AttachThreadInput(current_thread, fg_thread, False)
    return True


def click(x: int, y: int) -> None:
    user32 = ctypes.windll.user32
    user32.SetCursorPos(x, y)
    time.sleep(0.05)
    user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.08)
    user32.mouse_event(4, 0, 0, 0, 0)


def image_contains_ui(img) -> bool:
    # Look for the characteristic strong blue panel used by the curling Unity UI.
    small = img.resize((192, 120))
    pixels = list(small.getdata())
    blue_count = sum(1 for r, g, b in pixels if b > 120 and r < 80 and g < 110)
    return blue_count > 1000


def locate_color_components(
    img,
    predicate: Callable[[int, int, int], bool],
    *,
    y_min_ratio: float = 0.1,
    y_max_ratio: float = 0.95,
    x_min_ratio: float = 0.05,
    x_max_ratio: float = 0.95,
    step: int = 4,
    min_points: int = 20,
) -> list[dict[str, int]]:
    width, height = img.size
    pixels = img.load()
    selected: set[tuple[int, int]] = set()
    y0 = int(height * y_min_ratio)
    y1 = int(height * y_max_ratio)
    x0 = int(width * x_min_ratio)
    x1 = int(width * x_max_ratio)
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            r, g, b = pixels[x, y][:3]
            if predicate(r, g, b):
                selected.add((x, y))

    components: list[dict[str, int]] = []
    while selected:
        seed = selected.pop()
        stack = [seed]
        points = [seed]
        while stack:
            x, y = stack.pop()
            for dx in (-step, 0, step):
                for dy in (-step, 0, step):
                    if dx == 0 and dy == 0:
                        continue
                    nxt = (x + dx, y + dy)
                    if nxt in selected:
                        selected.remove(nxt)
                        stack.append(nxt)
                        points.append(nxt)
        if len(points) < min_points:
            continue
        xs = [x for x, _ in points]
        ys = [y for _, y in points]
        components.append(
            {
                "count": len(points),
                "x0": min(xs),
                "x1": max(xs),
                "y0": min(ys),
                "y1": max(ys),
                "cx": int(sum(xs) / len(points)),
                "cy": int(sum(ys) / len(points)),
            }
        )

    components.sort(key=lambda c: (c["cy"], c["cx"]))
    return components


def locate_start_buttons(
    img,
) -> Tuple[
    Optional[Tuple[int, int]],
    Optional[Tuple[int, int]],
    Optional[Tuple[int, int]],
    Optional[Tuple[int, int]],
]:
    width, height = img.size

    def red_score(r: int, g: int, b: int) -> int:
        return max(0, r - max(g, b))

    def blue_score(r: int, g: int, b: int) -> int:
        return max(0, b - max(r, g))

    red_components = locate_color_components(
        img,
        lambda r, g, b: red_score(r, g, b) > 80 and r > 140,
        y_min_ratio=0.40,
        y_max_ratio=0.90,
        x_min_ratio=0.10,
        x_max_ratio=0.90,
    )
    blue_components = locate_color_components(
        img,
        lambda r, g, b: blue_score(r, g, b) > 80 and b > 120,
        y_min_ratio=0.40,
        y_max_ratio=0.95,
        x_min_ratio=0.10,
        x_max_ratio=0.90,
    )
    upper_red_components = locate_color_components(
        img,
        lambda r, g, b: red_score(r, g, b) > 80 and r > 140,
        y_min_ratio=0.10,
        y_max_ratio=0.45,
        x_min_ratio=0.0,
        x_max_ratio=0.25,
    )

    def button_like(component: dict[str, int]) -> bool:
        width = component["x1"] - component["x0"]
        height = component["y1"] - component["y0"]
        return 80 <= width <= 360 and 20 <= height <= 90

    red_components = [c for c in red_components if button_like(c)]
    blue_components = [c for c in blue_components if button_like(c)]
    upper_red_components = [c for c in upper_red_components if button_like(c)]

    # Main menu has two lower red buttons. The left one is "无限局制".
    menu_red = [
        c
        for c in red_components
        if c["cy"] > height * 0.55 and c["cx"] < width * 0.45
    ]
    if menu_red:
        red_center = (menu_red[0]["cx"], menu_red[0]["cy"])
    elif red_components:
        red_center = (red_components[0]["cx"], red_components[0]["cy"])
    else:
        red_center = None

    # Waiting room has two lower blue buttons; the right one starts the match.
    lower_blue = [c for c in blue_components if c["cy"] > height * 0.65]
    if lower_blue:
        target = sorted(lower_blue, key=lambda c: c["cx"], reverse=True)[0]
        blue_center = (target["cx"], target["cy"])
    elif blue_components:
        target = sorted(blue_components, key=lambda c: c["cx"], reverse=True)[0]
        blue_center = (target["cx"], target["cy"])
    else:
        blue_center = None

    return_center = None
    if upper_red_components:
        target = sorted(upper_red_components, key=lambda c: c["count"], reverse=True)[0]
        return_center = (target["cx"], target["cy"])
    # The waiting room also exposes a left lower blue "main menu" control.
    # It is distinct from the right lower blue "start match" control, but the
    # original locator discarded it, preventing --recover-in-match from
    # escaping a stale ordinary game.
    waiting_room_menu_center = None
    if len(lower_blue) >= 2:
        target = sorted(lower_blue, key=lambda c: c["cx"])[0]
        waiting_room_menu_center = (target["cx"], target["cy"])
    return red_center, blue_center, return_center, waiting_room_menu_center


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", type=Path, default=Path("log/unity_sampling"))
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--max-clicks", type=int, default=40)
    parser.add_argument(
        "--recover-in-match",
        action="store_true",
        help="Opt in to clicking the visible return-to-menu control before starting a controlled infinite match.",
    )
    return parser.parse_args()


def main() -> None:
    enable_dpi_awareness()
    args = parse_args()
    args.log_dir.mkdir(parents=True, exist_ok=True)
    clicks = 0
    recovery_used = False
    while clicks < args.max_clicks:
        activated = activate_edge()
        try:
            img = ImageGrab.grab()
        except OSError:
            time.sleep(args.interval)
            continue
        img.save(args.log_dir / "ui_watcher_last.png")
        if not activated or not image_contains_ui(img):
            print("[ui_watcher] waiting for unlocked Unity page", flush=True)
            time.sleep(args.interval)
            continue

        red_center, blue_center, return_center, waiting_room_menu_center = locate_start_buttons(img)
        print(
            f"[ui_watcher] red={red_center} blue={blue_center} return={return_center} "
            f"waitingMenu={waiting_room_menu_center}",
            flush=True,
        )
        menu_infinite = (
            red_center is not None
            and red_center[0] < img.size[0] * 0.45
            and red_center[1] > img.size[1] * 0.55
        )
        if menu_infinite:
            click(*red_center)
            clicks += 1
            time.sleep(2.0)
            time.sleep(args.interval)
            continue

        # A stale previous game can leave the browser in a player-control
        # panel, where there is no protocol GO for a new sampler.  Recovery is
        # intentionally opt-in: only the dedicated runtime sampler uses it.
        if args.recover_in_match and not recovery_used and return_center is not None and not menu_infinite:
            click(*return_center)
            clicks += 1
            recovery_used = True
            time.sleep(2.0)
            time.sleep(args.interval)
            continue
        if args.recover_in_match and not recovery_used and waiting_room_menu_center is not None and not menu_infinite:
            click(*waiting_room_menu_center)
            clicks += 1
            recovery_used = True
            time.sleep(2.0)
            time.sleep(args.interval)
            continue

        # The mode menu's red buttons sit around two thirds down the canvas.
        # The ready button is in the bottom fifth, so do not mistake a menu
        # transition frame for a waiting-room control.
        if red_center and red_center[1] > img.size[1] * 0.75:
            click(*red_center)
            clicks += 1
            time.sleep(2.0)
        if blue_center and blue_center[1] > img.size[1] * 0.65:
            click(*blue_center)
            clicks += 1
            time.sleep(2.0)

        time.sleep(args.interval)

    print("[ui_watcher] max clicks reached", flush=True)


if __name__ == "__main__":
    main()
