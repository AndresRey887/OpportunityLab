"""Verify Phase 6 system-health diagnostics and UI integration."""

from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.health.system_health_service import SystemHealthService
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for name in ("src", "scripts", "docs", "data"):
            (root / name).mkdir()
        (root / "requirements.txt").write_text(
            "customtkinter\n",
            encoding="utf-8",
        )
        (root / "src/version.py").write_text("# version\n", encoding="utf-8")
        (root / "docs/AI_HANDOVER.md").write_text("# handover\n", encoding="utf-8")
        (root / "docs/BUILD_GUIDE.md").write_text("# guide\n", encoding="utf-8")
        (root / "scripts/test_example.py").write_text(
            "print('passed')\n",
            encoding="utf-8",
        )

        (root / "data" / "valid.json").write_text(
            json.dumps({"status": "ready"}),
            encoding="utf-8",
        )
        (root / "data" / "invalid.json").write_text(
            "{broken",
            encoding="utf-8",
        )
        with closing(
            sqlite3.connect(root / "data" / "opportunitylab.db")
        ) as database:
            database.execute("CREATE TABLE health (status TEXT)")
            database.commit()

        service = SystemHealthService(root, root / "data")
        with patch(
            "src.health.system_health_service.importlib.util.find_spec",
            return_value=object(),
        ):
            report = service.run()
        results = {check.name: check.status for check in report.checks}

        assert results["Python Runtime"] == "Passed"
        assert results["Project Structure"] == "Passed"
        assert results["Data Storage"] == "Passed"
        assert results["Dependency: customtkinter"] == "Passed"
        assert results["JSON: valid.json"] == "Passed"
        assert results["JSON: invalid.json"] == "Failed"
        assert results["Database: opportunitylab.db"] == "Passed"
        assert report.overall_status == "Failed"

        (root / "data" / "invalid.json").unlink()
        with patch(
            "src.health.system_health_service.importlib.util.find_spec",
            return_value=object(),
        ):
            assert service.run().overall_status == "Healthy"
        (root / "data" / "opportunitylab.db").unlink()

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    data_tools = (PROJECT_ROOT / "src/ui/data_tools_window.py").read_text(
        encoding="utf-8"
    )
    health_window = (PROJECT_ROOT / "src/ui/system_health_window.py").read_text(
        encoding="utf-8"
    )
    assert "SystemHealthService" in main_window
    assert "System Health" in data_tools
    assert "Run Checks" in health_window
    assert VERSION_INFO.version == "1.0.0"
    assert VERSION_INFO.package == "Package-100A-03"
    assert VERSION_INFO.codename == "Gold Rush"

    print("Phase 6 system health test passed.")


if __name__ == "__main__":
    main()
