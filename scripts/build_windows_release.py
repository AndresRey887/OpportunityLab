"""Build the OpportunityLab Windows application folder with PyInstaller."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC_FILE = PROJECT_ROOT / "OpportunityLab.spec"


def main() -> int:
    if sys.platform != "win32":
        print("Windows release builds must be created on Windows.")
        return 1
    if importlib.util.find_spec("PyInstaller") is None:
        print(
            "PyInstaller is not installed. Run: "
            "python -m pip install -r requirements-build.txt"
        )
        return 1
    if not SPEC_FILE.is_file():
        print("OpportunityLab.spec is missing.")
        return 1

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        str(SPEC_FILE),
    ]
    completed = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    if completed.returncode:
        print("Windows release build failed.")
        return completed.returncode
    print("Windows release created in dist\\OpportunityLab")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
