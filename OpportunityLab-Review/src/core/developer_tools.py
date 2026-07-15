"""Read-only developer diagnostics for OpportunityLab.

Package-019B-07 adds a small diagnostics helper without changing the
application architecture or runtime behaviour.
"""

from __future__ import annotations

import importlib.util
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.version import VERSION_INFO


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class DiagnosticCheck:
    name: str
    passed: bool
    detail: str

    @property
    def status(self) -> str:
        return "PASS" if self.passed else "FAIL"


REQUIRED_PATHS = (
    "src",
    "src/ui/main_window.py",
    "src/core/app_logger.py",
    "src/core/task_manager.py",
    "src/version.py",
    "scripts",
    "config",
)

REQUIRED_IMPORTS = (
    "src.version",
    "src.core.app_logger",
    "src.core.task_manager",
    "src.ai.ai_controller",
    "src.ui.main_window",
)


def check_required_paths(
    project_root: Path = PROJECT_ROOT,
    required_paths: Iterable[str] = REQUIRED_PATHS,
) -> list[DiagnosticCheck]:
    checks: list[DiagnosticCheck] = []

    for relative_path in required_paths:
        path = project_root / relative_path
        checks.append(
            DiagnosticCheck(
                name=f"Path: {relative_path}",
                passed=path.exists(),
                detail=str(path),
            )
        )

    return checks


def check_required_imports(
    module_names: Iterable[str] = REQUIRED_IMPORTS,
) -> list[DiagnosticCheck]:
    checks: list[DiagnosticCheck] = []

    for module_name in module_names:
        try:
            module_spec = importlib.util.find_spec(module_name)
        except Exception as error:
            checks.append(
                DiagnosticCheck(
                    name=f"Import path: {module_name}",
                    passed=False,
                    detail=f"{type(error).__name__}: {error}",
                )
            )
            continue

        checks.append(
            DiagnosticCheck(
                name=f"Import path: {module_name}",
                passed=module_spec is not None,
                detail=(
                    str(module_spec.origin)
                    if module_spec is not None
                    else "Module not found"
                ),
            )
        )

    return checks


def collect_diagnostics() -> list[DiagnosticCheck]:
    checks = [
        DiagnosticCheck(
            name="Python version",
            passed=sys.version_info >= (3, 10),
            detail=platform.python_version(),
        ),
        DiagnosticCheck(
            name="Project root",
            passed=PROJECT_ROOT.exists(),
            detail=str(PROJECT_ROOT),
        ),
    ]

    checks.extend(check_required_paths())
    checks.extend(check_required_imports())
    return checks


def format_report(checks: Iterable[DiagnosticCheck]) -> str:
    check_list = list(checks)
    passed_count = sum(check.passed for check in check_list)
    failed_count = len(check_list) - passed_count

    lines = [
        "OpportunityLab Developer Diagnostics",
        VERSION_INFO.full_label,
        "=" * 72,
    ]

    for check in check_list:
        lines.append(f"[{check.status}] {check.name}")
        lines.append(f"       {check.detail}")

    lines.extend(
        [
            "=" * 72,
            f"Passed: {passed_count}",
            f"Failed: {failed_count}",
        ]
    )

    return "\n".join(lines)


def run_diagnostics() -> int:
    checks = collect_diagnostics()
    print(format_report(checks))
    return 0 if all(check.passed for check in checks) else 1
