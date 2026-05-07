# GoofyAhhGate (LeetCode before DAW)

Minimal Windows tray app: **block configured executables (e.g. your DAW)** until you have solved enough LeetCode problems **today** (checked via LeetCode’s public GraphQL `recentAcSubmissionList`).

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Windows. Dependencies are declared in [`pyproject.toml`](pyproject.toml).

1. Sync the environment (creates `.venv` and installs everything from `pyproject.toml` / `uv.lock`):

   ```powershell
   uv sync
   ```

2. Copy [`.env.example`](.env.example) to `.env` and edit:
   - `LEETCODE_USERNAME` — your LeetCode username (public profile).
   - `MIN_PROBLEMS_PER_DAY` — quota (e.g. `1`).
   - `PROCESSES` — comma-separated process **names** as shown in Task Manager (e.g. `Ableton Live 12 Suite.exe`).
   - `FAIL_OPEN_ON_API_ERROR` — `true` = if LeetCode is unreachable, allow the DAW and show a tray notification (recommended).

## Run

From this folder:

```powershell
uv run pythonw main.py
```

(`pythonw` avoids an extra console window; `uv run python main.py` also works for debugging.)

## Autostart

```powershell
uv run python install_autostart.py
```

Creates `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GoofyAhhGate.lnk`. **To uninstall**, delete that `.lnk` file.

> The shortcut points at the `pythonw.exe` inside `.venv` (resolved via `sys.executable`), so `uv` is not required at login — just don’t move/delete the project’s `.venv`. If you ever recreate the venv, re-run `install_autostart.py`.

## Tray menu

- Status line (solved / quota).
- **Refresh now** — clears the LeetCode cache and re-fetches.
- **Open LeetCode** — problem set in the browser.
- **Quit**.

## Manual smoke test

1. In `.env`, set `MIN_PROBLEMS_PER_DAY=999` and `PROCESSES=notepad.exe`. Save.
2. Run `uv run python main.py`. Open **Notepad**.
3. Confirm Notepad is terminated and the **Lock in.** dialog appears (may take up to `POLL_INTERVAL_SECONDS`).
4. Set `MIN_PROBLEMS_PER_DAY=0`. Restart the app. Open Notepad — it should stay open.

## Notes

- LeetCode has **no official API**; this uses their public GraphQL endpoint. It can change without notice.
- Submissions must be **Accepted** and visible on your **public** recent activity for the count to update.
- Run from an account that is allowed to terminate your DAW processes (same user is usually fine).
- `from __future__ import annotations` has been deprecated starting Python 3.14, but like, AI generated this slop and I'm too lazy to change it, so I'm keeping it in for now. Also, backwards compatibility!! Am I right?
