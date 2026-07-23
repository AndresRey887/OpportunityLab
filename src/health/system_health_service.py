"""Run safe startup, dependency, storage, and data-integrity diagnostics."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.health.health_check import HealthCheck
from src.health.health_report import HealthReport


class SystemHealthService:
    REQUIRED_MODULES = ("customtkinter",)
    DATA_SUFFIXES = {".json"}

    def __init__(
        self,
        project_root: str | Path = ".",
        data_directory: str | Path = "data",
    ) -> None:
        self.project_root = Path(project_root)
        self.data_directory = Path(data_directory)

    def run(self) -> HealthReport:
        checks = [
            self._python_check(),
            self._project_check(),
            self._release_files_check(),
            self._test_suite_check(),
            self._data_directory_check(),
            *self._dependency_checks(),
            *self._json_checks(),
            *self._database_checks(),
        ]
        return HealthReport(tuple(checks))

    def export_report(self, destination: str | Path) -> Path:
        """Write a safe JSON report without credentials or file contents."""
        path = Path(destination)
        report = self.run()
        payload = {
            "application": "OpportunityLab",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "python": sys.version.split()[0],
            "platform": sys.platform,
            **report.to_dict(),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def _python_check(self) -> HealthCheck:
        version = sys.version_info
        passed = version >= (3, 11)
        return HealthCheck(
            "Python Runtime",
            "Passed" if passed else "Failed",
            f"Python {version.major}.{version.minor}.{version.micro}",
            "Runtime",
        )

    def _project_check(self) -> HealthCheck:
        required = ("src", "scripts", "docs")
        missing = [
            name for name in required
            if not (self.project_root / name).exists()
        ]
        return HealthCheck(
            "Project Structure",
            "Failed" if missing else "Passed",
            (
                f"Missing: {', '.join(missing)}"
                if missing else "Required project folders are present."
            ),
            "Application",
        )

    def _release_files_check(self) -> HealthCheck:
        required = (
            "requirements.txt",
            "requirements-build.txt",
            "OpportunityLab.spec",
            "docs/AI_HANDOVER.md",
            "docs/BUILD_GUIDE.md",
            "src/version.py",
        )
        missing = [
            name for name in required
            if not (self.project_root / name).is_file()
        ]
        return HealthCheck(
            "Release Files",
            "Failed" if missing else "Passed",
            (
                f"Missing: {', '.join(missing)}"
                if missing else "Release requirements and documentation exist."
            ),
            "Release Readiness",
        )

    def _test_suite_check(self) -> HealthCheck:
        test_directory = self.project_root / "scripts"
        test_count = len(tuple(test_directory.glob("test_*.py")))
        return HealthCheck(
            "Regression Tests",
            "Passed" if test_count else "Failed",
            (
                f"{test_count} test scripts available."
                if test_count else "No regression test scripts found."
            ),
            "Release Readiness",
        )

    def _data_directory_check(self) -> HealthCheck:
        try:
            self.data_directory.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile(
                dir=self.data_directory,
                prefix="health-",
                suffix=".tmp",
                delete=True,
            ):
                pass
        except OSError as exc:
            return HealthCheck(
                "Data Storage",
                "Failed",
                f"Data directory is not writable: {exc}",
                "Storage",
            )
        return HealthCheck(
            "Data Storage",
            "Passed",
            f"Writable data directory: {self.data_directory}",
            "Storage",
        )

    def _dependency_checks(self) -> list[HealthCheck]:
        return [
            HealthCheck(
                f"Dependency: {module}",
                "Passed" if importlib.util.find_spec(module) else "Failed",
                (
                    "Installed and importable."
                    if importlib.util.find_spec(module)
                    else "Required dependency is not installed."
                ),
                "Dependencies",
            )
            for module in self.REQUIRED_MODULES
        ]

    def _json_checks(self) -> list[HealthCheck]:
        if not self.data_directory.exists():
            return []
        checks = []
        for path in sorted(self.data_directory.glob("*.json")):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                checks.append(
                    HealthCheck(
                        f"JSON: {path.name}",
                        "Failed",
                        f"Invalid JSON data: {exc}",
                        "Data Integrity",
                    )
                )
            else:
                checks.append(
                    HealthCheck(
                        f"JSON: {path.name}",
                        "Passed",
                        "Valid JSON data.",
                        "Data Integrity",
                    )
                )
        if not checks:
            checks.append(
                HealthCheck(
                    "JSON Data",
                    "Warning",
                    "No JSON data files exist yet.",
                    "Data Integrity",
                )
            )
        return checks

    def _database_checks(self) -> list[HealthCheck]:
        checks = []
        for path in sorted(self.data_directory.glob("*.db")):
            try:
                with closing(sqlite3.connect(path)) as connection:
                    result = connection.execute("PRAGMA quick_check").fetchone()
                healthy = bool(result and result[0] == "ok")
            except sqlite3.DatabaseError as exc:
                checks.append(
                    HealthCheck(
                        f"Database: {path.name}",
                        "Failed",
                        f"Database check failed: {exc}",
                        "Data Integrity",
                    )
                )
            else:
                checks.append(
                    HealthCheck(
                        f"Database: {path.name}",
                        "Passed" if healthy else "Failed",
                        "SQLite quick check passed." if healthy else str(result),
                        "Data Integrity",
                    )
                )
        return checks
