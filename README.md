# GoofyAhhGate (LeetCode before DAW)

Minimal Windows tray app: **block configured executables (e.g. your DAW)** until you have solved enough LeetCode problems **today** (checked via LeetCode’s public GraphQL `recentAcSubmissionList`).

## Setup

1. Python 3.11+ on Windows.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy [`.env.example`](.env.example) to `.env` and edit:
   - `LEETCODE_USERNAME` — your LeetCode username (public profile).
   - `MIN_PROBLEMS_PER_DAY` — quota (e.g. `1`).
   - `PROCESSES` — comma-separated process **names** as shown in Task Manager (e.g. `Ableton Live 12 Suite.exe`).
   - `FAIL_OPEN_ON_API_ERROR` — `true` = if LeetCode is unreachable, allow the DAW and show a tray notification (recommended).

## Run

From this folder:

```powershell
pythonw main.py
```

(`pythonw` avoids an extra console window; `python main.py` also works for debugging.)

## Autostart

```powershell
python install_autostart.py
```

Creates `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GoofyAhhGate.lnk`. **To uninstall**, delete that `.lnk` file.

## Tray menu

- Status line (solved / quota).
- **Refresh now** — clears the LeetCode cache and re-fetches.
- **Open LeetCode** — problem set in the browser.
- **Quit**.

## Manual smoke test

1. In `.env`, set `MIN_PROBLEMS_PER_DAY=999` and `PROCESSES=notepad.exe`. Save.
2. Run `python main.py`. Open **Notepad**.
3. Confirm Notepad is terminated and the **Lock in.** dialog appears (may take up to `POLL_INTERVAL_SECONDS`).
4. Set `MIN_PROBLEMS_PER_DAY=0`. Restart the app. Open Notepad — it should stay open.

## Notes

- LeetCode has **no official API**; this uses their public GraphQL endpoint. It can change without notice.
- Submissions must be **Accepted** and visible on your **public** recent activity for the count to update.
- Run from an account that is allowed to terminate your DAW processes (same user is usually fine).
