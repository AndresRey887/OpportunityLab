"""Verify Windows release-build configuration without building an executable."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.version import VERSION_INFO


def main() -> None:
    spec = (PROJECT_ROOT / "OpportunityLab.spec").read_text(encoding="utf-8")
    build_script_path = PROJECT_ROOT / "scripts/build_windows_release.py"
    build_script = build_script_path.read_text(encoding="utf-8")
    requirements = (PROJECT_ROOT / "requirements.txt").read_text(
        encoding="utf-8"
    )
    build_requirements = (PROJECT_ROOT / "requirements-build.txt").read_text(
        encoding="utf-8"
    )

    ast.parse(build_script)
    assert '["src/ui/main_window.py"]' in spec
    assert 'name="OpportunityLab"' in spec
    assert 'console=False' in spec
    assert "collect_data_files(\"customtkinter\")" in spec
    assert "PyInstaller" in build_script
    assert "--clean" in build_script
    assert "customtkinter" in requirements
    assert "pyinstaller" in build_requirements.lower()
    assert VERSION_INFO.package == "Package-100A-08"
    assert VERSION_INFO.build == 10
    print("Phase 6 Windows build configuration test passed.")


if __name__ == "__main__":
    main()
