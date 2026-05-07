from __future__ import annotations

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

import pystray
from PIL import Image, ImageDraw, ImageFont

import config as cfg_mod
from leetcode import LeetCodeClient
from monitor import current_status_label, monitor_loop

LEETCODE_PROBLEMSET = "https://leetcode.com/problemset/"
MENU_REFRESH_SECONDS = 30
API_ERROR_NOTIFY_COOLDOWN = 120.0


def _make_icon_image() -> Image.Image:
    size = 64
    img = Image.new("RGB", (size, size), color=(26, 26, 32))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [6, 6, size - 6, size - 6], radius=8, outline=(220, 220, 230), width=3
    )
    try:
        font = ImageFont.truetype("segoeui.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
    text = "L"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        ((size - tw) // 2, (size - th) // 2 - 2),
        text,
        fill=(245, 245, 250),
        font=font,
    )
    return img


def main() -> None:
    try:
        cfg = cfg_mod.load()
    except ValueError as e:
        print(f"Config error: {e}", file=sys.stderr)
        raise SystemExit(1) from e

    lc = LeetCodeClient(cfg)
    stop = threading.Event()

    api_notify_lock = threading.Lock()
    last_api_notify = 0.0
    icon_holder: dict[str, pystray.Icon | None] = {"icon": None}

    def notify_api_error() -> None:
        nonlocal last_api_notify
        ico = icon_holder["icon"]
        if ico is None:
            return
        now = time.monotonic()
        with api_notify_lock:
            if now - last_api_notify < API_ERROR_NOTIFY_COOLDOWN:
                return
            last_api_notify = now
        try:
            ico.notify(
                "GoofyAhhGate",
                "LeetCode unreachable — DAW allowed (fail-open).",
            )
        except Exception:
            pass

    def status_text(_item: pystray.MenuItem) -> str:
        return current_status_label(cfg, lc)

    def on_refresh(icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        lc.invalidate()
        icon.update_menu()

    def on_open_lc(_icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        webbrowser.open(LEETCODE_PROBLEMSET)

    def on_quit(icon: pystray.Icon, _item: pystray.MenuItem) -> None:
        stop.set()
        icon.stop()

    menu = pystray.Menu(
        pystray.MenuItem(status_text, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Refresh now", on_refresh),
        pystray.MenuItem("Open LeetCode", on_open_lc),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", on_quit),
    )

    icon = pystray.Icon(
        "GoofyAhhGate",
        _make_icon_image(),
        "GoofyAhhGate — LeetCode before DAW",
        menu,
    )
    icon_holder["icon"] = icon

    monitor_thread = threading.Thread(
        target=monitor_loop,
        args=(cfg, lc, stop),
        kwargs={"on_fail_open_api_error": notify_api_error},
        daemon=True,
    )
    monitor_thread.start()

    def menu_refresher() -> None:
        while not stop.is_set():
            if stop.wait(MENU_REFRESH_SECONDS):
                break
            try:
                icon.update_menu()
            except Exception:
                pass

    threading.Thread(target=menu_refresher, daemon=True).start()

    icon.run()


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parent)
    main()
