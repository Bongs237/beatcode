from __future__ import annotations

import threading
from collections.abc import Callable

import psutil

from config import Config
from dialog import show_lockin_dialog
from leetcode import LeetCodeClient


def current_status_label(cfg: Config, lc: LeetCodeClient) -> str:
    n = cfg.min_problems_per_day
    solved = lc.solved_today_count()
    if solved is None:
        return f"?/{n} — api error"
    if solved >= n:
        return f"{solved}/{n} solved today"
    return f"{solved}/{n} — locked"


def monitor_loop(
    cfg: Config,
    lc: LeetCodeClient,
    stop: threading.Event,
    on_fail_open_api_error: Callable[[], None] | None = None,
) -> None:
    targets = {p.lower() for p in cfg.processes}

    while not stop.is_set():
        solved = lc.solved_today_count()

        if solved is None and cfg.fail_open_on_api_error:
            if on_fail_open_api_error is not None:
                on_fail_open_api_error()
        else:
            effective = solved if solved is not None else 0
            if effective < cfg.min_problems_per_day:
                killed_any = False
                for proc in psutil.process_iter(["name", "pid"]):
                    if stop.is_set():
                        break
                    name = (proc.info.get("name") or "").lower()
                    if name not in targets:
                        continue
                    try:
                        proc.kill()
                        killed_any = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                if killed_any:
                    show_lockin_dialog(effective, cfg.min_problems_per_day, cfg.quotes)

        if stop.wait(cfg.poll_interval_seconds):
            break
