from __future__ import annotations

import sys
from pathlib import Path

try:
    import win32com.client  # type: ignore[import-untyped]
except ImportError:
    print("Install pywin32 first: pip install pywin32", file=sys.stderr)
    raise SystemExit(1) from None


def main() -> None:
    root = Path(__file__).resolve().parent
    main_py = root / "main.py"
    if not main_py.is_file():
        print(f"Could not find main.py at {main_py}", file=sys.stderr)
        raise SystemExit(1)

    shell = win32com.client.Dispatch("WScript.Shell")
    startup_dir = Path(shell.SpecialFolders("Startup"))
    shortcut_path = startup_dir / "GoofyAhhGate.lnk"

    exe = Path(sys.executable)
    if exe.name.lower() == "python.exe":
        target = exe.with_name("pythonw.exe")
    else:
        target = exe

    if not target.is_file():
        print(f"pythonw.exe not found next to {exe}; using {exe}", file=sys.stderr)
        target = exe

    sc = shell.CreateShortcut(str(shortcut_path))
    sc.TargetPath = str(target)
    sc.Arguments = f'"{main_py}"'
    sc.WorkingDirectory = str(root)
    sc.IconLocation = str(target)
    sc.Save()

    print(f"Created startup shortcut:\n  {shortcut_path}")
    print("To uninstall, delete that .lnk file.")


if __name__ == "__main__":
    main()
