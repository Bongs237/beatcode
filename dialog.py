from __future__ import annotations

import random
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk

_DEBOUNCE_LOCK = threading.Lock()
_LAST_SHOWN_MONO = 0.0
_DEBOUNCE_SECONDS = 3.0

LEETCODE_PROBLEMSET = "https://leetcode.com/problemset/"

INSPIRATIONAL_QUOTES = [
    # Real-ish quotes
    '"Talk is cheap. Show me the code." ~ Linus Torvalds',
    '"Premature optimization is the root of all evil." ~ Donald Knuth',
    '"Do or do not. There is no try." ~ Yoda',
    '"Discipline equals freedom." ~ Jocko Willink',
    '"It always seems impossible until it\'s done." ~ Nelson Mandela',
    '"Whether you think you can, or you think you can\'t ~ you\'re right." ~ Henry Ford',
    '"Hard work beats talent when talent doesn\'t work hard." ~ Tim Notke',
    '"The expert in anything was once a beginner."',
    '"The greatest glory in living lies not in never falling, but in rising every time we fall." ~ Nelson Mandela',
    '"Do the best you can until you know better. Then when you know better, do better." ~ Maya Angelou',
    '"The struggle you\'re in today is developing the strength you need tomorrow." ~ Anonymous',
    '"Be not afraid of growing slowly; be afraid only of standing still." ~ Chinese Proverb',
    '"Never gonna give you up, never gonna let you down, never gonna run around and desert you." ~ Rick Astley',
    '"Embrace a growth mindset" ~ my 22c professor',

    # Certified AI-generated slop
    '"Every accepted submission is a beat you haven\'t dropped yet." ~ ChatGPT, probably',
    '"Two pointers in your code, two hands on your MIDI keys." ~ GPT-4o, after midnight',
    '"Recursion is just self-belief calling itself." ~ Claude, allegedly',
    '"Sleep is just garbage collection for the soul." ~ an LLM with too much RAM',
    '"Microwave burrito that\'s O(1), checking my phone, that\'s O(1), grinding LeetCode? That NEEDS TO BE O(1). ~ Me, 12 am',
    "",
    '"You can\'t autotune your way out of an unsolved problem." ~ Llama, 3 a.m.',
    '"The DAW is locked, but your potential is uncapped."',
    '"A bug in your solution is a bug in your soul." ~ DeepSeek, getting deep and seeking (wow)',
    '"Today\'s LeetCode is tomorrow\'s Grammy." ~ Drake, totally.',
    "'Your Spotify playlist is a queue. Data structures reference?!' ~ Me, in the car with friends, 2026",
]

def show_lockin_dialog(solved: int, required: int) -> None:
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
            + random.choice(INSPIRATIONAL_QUOTES)
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
