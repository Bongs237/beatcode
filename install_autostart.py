from __future__ import annotations

import sys
from pathlib import Path

try:
    import win32com.client  # type: ignore[import-untyped]
except ImportError:
    print("Install pywin32 first: pip install pywin32", file=sys.stderr)
    raise SystemExit(1) from None


def _find_interpreter(root: Path) -> Path:
    """Locate pythonw.exe, preferring the project's uv-managed .venv."""
    venv_scripts = root / ".venv" / "Scripts"
    for name in ("pythonw.exe", "python.exe"):
        candidate = venv_scripts / name
        if candidate.is_file():
            return candidate

    exe = Path(sys.executable)
    if exe.name.lower() == "python.exe":
        pyw = exe.with_name("pythonw.exe")
        if pyw.is_file():
            return pyw
    return exe


def main() -> None:
    root = Path(__file__).resolve().parent
    main_py = root / "main.py"
    if not main_py.is_file():
        print(f"Could not find main.py at {main_py}", file=sys.stderr)
        raise SystemExit(1)

    venv_dir = root / ".venv"
    if not venv_dir.is_dir():
        print(
            f"No .venv found at {venv_dir}.\n"
            "Create it first with: uv sync  (or: uv venv && uv pip install -r requirements.txt)",
            file=sys.stderr,
        )
        raise SystemExit(1)

    shell = win32com.client.Dispatch("WScript.Shell")
    startup_dir = Path(shell.SpecialFolders("Startup"))
    shortcut_path = startup_dir / "BEATCODE.lnk"

    target = _find_interpreter(root)
    if target.name.lower() == "python.exe":
        print(
            f"Warning: using {target.name} (console window may flash). "
            "Install pywin32 in the venv to get pythonw.exe.",
            file=sys.stderr,
        )

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
