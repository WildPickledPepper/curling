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
from typing import Optional, Tuple

from PIL import ImageGrab


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

    windows: list[int] = []

    def callback(hwnd: int, _: int) -> bool:
        if user32.IsWindowVisible(hwnd):
            text = title(hwnd)
            if "Unity WebGL Player" in text or "curling" in text:
                windows.append(hwnd)
        return True

    user32.EnumWindows(enum_proc(callback), 0)
    if not windows:
        return False

    hwnd = windows[0]
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


def locate_start_buttons(img) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    width, height = img.size
    pixels = img.load()

    def red_score(x: int, y: int) -> int:
        r, g, b = pixels[x, y][:3]
        return max(0, r - max(g, b))

    def blue_score(x: int, y: int) -> int:
        r, g, b = pixels[x, y][:3]
        return max(0, b - max(r, g))

    red_points = []
    blue_points = []
    for y in range(int(height * 0.45), int(height * 0.95), 4):
        for x in range(int(width * 0.1), int(width * 0.9), 4):
            if red_score(x, y) > 80:
                red_points.append((x, y))
            if blue_score(x, y) > 80:
                blue_points.append((x, y))

    def center(points):
        if len(points) < 20:
            return None
        return (int(sum(x for x, _ in points) / len(points)), int(sum(y for _, y in points) / len(points)))

    red_center = center(red_points)
    blue_center = center(blue_points)

    # Return-menu button is a red rectangle in the upper-left if already in match.
    return_center = None
    upper_red = []
    for y in range(int(height * 0.1), int(height * 0.45), 4):
        for x in range(0, int(width * 0.25), 4):
            if red_score(x, y) > 80:
                upper_red.append((x, y))
    return_center = center(upper_red)
    return red_center, blue_center, return_center


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", type=Path, default=Path("log/unity_sampling"))
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--max-clicks", type=int, default=40)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.log_dir.mkdir(parents=True, exist_ok=True)
    clicks = 0
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

        red_center, blue_center, return_center = locate_start_buttons(img)
        print(
            f"[ui_watcher] red={red_center} blue={blue_center} return={return_center}",
            flush=True,
        )
        # Waiting page: red ready/start button plus lower blue start/menu buttons.
        if red_center and red_center[1] > img.size[1] * 0.45:
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
