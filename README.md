# BEATCODE: LeetCode first, distractions second

This program blocks a specific app or apps until you have solved a certain number of LeetCode problems today so you can **LOCK IN**.

Essentially, it's based on the psychological trick where you reward yourself after doing something lol.

This was originally designed as a very niche, personal, specific thing for me. As both a developer and music producer who got easily distracted making beats, I wanted to block my DAW (digital audio workstation) until I solved LeetCode, hence the name BEATCODE. But honestly, no matter what apps you block, you are still using this to "beat" the system...

## Setup

big shoutout to claude for writing this (I am extremely lazy)

### ⚠️ NOTE: Only Windows is currently supported (FOR NOW)
If you're not on Windows... sorry bout that 😭

#### 1. Download and install [uv](https://docs.astral.sh/uv/#installation).

#### 2. Sync the environment (creates `.venv`):
```bash
uv sync
```

#### 3. Copy [`.env.example`](.env.example) to `.env`
```bash
copy .env.example .env
```

Edit:
- `LEETCODE_USERNAME` - your LeetCode username (public profile).
- `MIN_PROBLEMS_PER_DAY` - quota (e.g. `1`).
- `PROCESSES` - **The distracting processes you want to block.** Comma-separated process names as shown in Task Manager (e.g. `notepad.exe`, `WhatsApp.Root.exe`). This will scan for the process by name and _YEET IT_
- `FAIL_OPEN_ON_API_ERROR` - `true` or `false` = if LeetCode is unreachable, allow the processes, and show a tray notification (recommended).

#### 4. RUN IT!
```bash
uv run python install_autostart.py
```
This creates a shortcut in your Windows Startup directory, and starts up the program! Whenever your computer restarts, it will automatically run this program.

**To uninstall**, delete the `.lnk` file.

> The shortcut points at the `pythonw.exe` inside `.venv`. Just don’t move/delete the project’s `.venv`. If you ever recreate the venv, re-run `install_autostart.py`.

## For development

When developing or debugging, you'll want to see print statements, errors, and logs in the console.

For development, run the app like this:
```bash
uv run python main.py
```

This runs the main program using the standard Python interpreter (not `pythonw`), so any output (including debug or error messages) appears in your terminal.

## Notes

- LeetCode has **no official API**; this uses their public GraphQL endpoint. It can change without notice.
- Submissions must be **Accepted** and visible on your **public** recent activity for the count to update.
- Run from an account that is allowed to terminate your distraction processes (same user is usually fine).
- `from __future__ import annotations` has been deprecated starting Python 3.14, but like, AI generated this slop and I'm too lazy to change it, so I'm keeping it in for now. Also, backwards compatibility!! Am I right?
