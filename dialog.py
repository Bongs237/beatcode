from __future__ import annotations

import random
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk

_DEBOUNCE_LOCK = threading.Lock()
_LAST_SHOWN_MONO = 0.0 # Time in seconds since the last time the dialog was shown
_DEBOUNCE_SECONDS = 3.0 # Time in seconds to debounce the dialog

LEETCODE_PROBLEMSET = "https://leetcode.com/problemset/"

def confirm_quit() -> bool:
    """Blocking 'are you SUPER DUPER sure' dialog. Returns True if the user confirms quitting."""
    confirmed = False

    root = tk.Tk()
    root.withdraw()

    top = tk.Toplevel(root)
    top.title("Wait a sec...")
    top.resizable(False, False)
    top.attributes("-topmost", True)

    msg = (
        "Are you SUPER DUPER sure you wanna quit?\n\n"
        "Your distractions will be wide open and your LeetCode grind\n"
        "goes completely unguarded. No takesies-backsies."
    )
    frame = ttk.Frame(top, padding=16)
    frame.pack(fill=tk.BOTH, expand=True)
    ttk.Label(frame, text=msg, justify=tk.CENTER).pack(pady=(0, 12))

    btn_row = ttk.Frame(frame)
    btn_row.pack()

    def shutdown() -> None:
        top.destroy()
        root.destroy()

    def do_quit() -> None:
        nonlocal confirmed
        confirmed = True
        shutdown()

    keep_btn = ttk.Button(btn_row, text="No, keep grinding", command=shutdown)
    keep_btn.pack(side=tk.LEFT, padx=4)
    ttk.Button(btn_row, text="Yeah, quit", command=do_quit).pack(side=tk.LEFT, padx=4)

    top.protocol("WM_DELETE_WINDOW", shutdown)

    top.focus()

    top.update_idletasks()
    w = max(top.winfo_reqwidth(), 380)
    h = top.winfo_reqheight()
    x = (top.winfo_screenwidth() - w) // 2
    y = (top.winfo_screenheight() - h) // 2
    top.geometry(f"{w}x{h}+{x}+{y}")
    top.grab_set()

    root.mainloop()
    return confirmed


def show_lockin_dialog(solved: int, required: int, quotes: list[str]) -> None:
    global _LAST_SHOWN_MONO
    now = time.monotonic()
    with _DEBOUNCE_LOCK:
        if now - _LAST_SHOWN_MONO < _DEBOUNCE_SECONDS:
            return
        _LAST_SHOWN_MONO = now

    def _run() -> None:
        root = tk.Tk()
        root.withdraw()

        top = tk.Toplevel(root)
        top.title("Lock in.")
        top.resizable(False, False)
        top.attributes("-topmost", True)

        msg = (
            f"You've solved {solved}/{required} LeetCode problems today.\n\n"
            + random.choice(quotes)
        )
        frame = ttk.Frame(top, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text=msg, justify=tk.CENTER).pack(pady=(0, 12))

        btn_row = ttk.Frame(frame)
        btn_row.pack()

        def shutdown() -> None:
            top.destroy()
            root.destroy()

        def open_lc() -> None:
            webbrowser.open(LEETCODE_PROBLEMSET)
            shutdown()

        ttk.Button(btn_row, text="Open LeetCode", command=open_lc).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btn_row, text="Close", command=shutdown).pack(side=tk.LEFT, padx=4)

        top.protocol("WM_DELETE_WINDOW", shutdown)

        top.update_idletasks()
        w = max(top.winfo_reqwidth(), 380)
        h = top.winfo_reqheight()
        x = (top.winfo_screenwidth() - w) // 2
        y = (top.winfo_screenheight() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")
        top.grab_set()

        root.mainloop()

    threading.Thread(target=_run, daemon=True).start()
