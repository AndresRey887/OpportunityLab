"""Verify Phase 6 release checks and safe report export."""

from __future__ import annotations

import json
import sys
import tempfile
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
        (root / "docs/AI_HANDOVER.md").write_text("# Handover\n", encoding="utf-8")
        (root / "docs/BUILD_GUIDE.md").write_text("# Guide\n", encoding="utf-8")
        (root / "scripts/test_example.py").write_text(
            "print('passed')\n",
            encoding="utf-8",
        )
        service = SystemHealthService(root, root / "data")
        report_path = root / "health-report.json"
        with patch(
            "src.health.system_health_service.importlib.util.find_spec",
            return_value=object(),
        ):
            report = service.run()
            service.export_report(report_path)

        results = {check.name: check.status for check in report.checks}
        assert results["Release Files"] == "Passed"
        assert results["Regression Tests"] == "Passed"
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        assert payload["application"] == "OpportunityLab"
        assert payload["overall_status"] in {"Healthy", "Warning"}
        assert payload["checks"]
        serialized = report_path.read_text(encoding="utf-8").lower()
        assert "api_key" not in serialized
        assert "password" not in serialized

    ui_source = (PROJECT_ROOT / "src/ui/system_health_window.py").read_text(
        encoding="utf-8"
    )
    assert "Export Report" in ui_source
    assert VERSION_INFO.package == "Package-100A-03"
    assert VERSION_INFO.build == 5
    print("Phase 6 release report test passed.")


if __name__ == "__main__":
    main()
