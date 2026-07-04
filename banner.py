import sys
import os

BANNER_LINES = [
    "██████╗ ███████╗ █████╗ ████████╗ ██████╗  ██████╗ ██████╗ ███████╗",
    "██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝ ██╔═══██╗██╔══██╗██╔════╝",
    "██████╔╝█████╗  ███████║   ██║   ██║      ██║   ██║██║  ██║█████╗  ",
    "██╔══██╗██╔══╝  ██╔══██║   ██║   ██║      ██║   ██║██║  ██║██╔══╝  ",
    "██████╔╝███████╗██║  ██║   ██║   ╚██████╗ ╚██████╔╝██████╔╝███████╗",
    "╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝",
]

# Synthwave-ish top-to-bottom gradient (pink -> purple -> cyan).
BANNER_GRADIENT = [
    (255, 80, 180),
    (230, 90, 210),
    (200, 100, 230),
    (160, 130, 240),
    (110, 170, 245),
    (80, 210, 250),
]


def print_banner() -> None:
    if sys.stdout is None:
        return
    try:
        if sys.platform == "win32":
            # Poke the console so it enables ANSI VT sequences on modern Windows terminals.
            os.system("")
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

        reset = "\x1b[0m"
        dim = "\x1b[2m"

        print()
        for (r, g, b), row in zip(BANNER_GRADIENT, BANNER_LINES):
            print(f"\x1b[38;2;{r};{g};{b}m{row}{reset}")
        print(f"{dim}// LeetCode first, distractions second{reset}")
        print("running!")
        print()
    except Exception:
        pass
