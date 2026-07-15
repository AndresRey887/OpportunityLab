"""Offline Phase 1 smoke-test runner for OpportunityLab."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_FILES = (
    "scripts/test_version.py",
    "scripts/test_app_logger.py",
    "scripts/test_task_manager.py",
    "scripts/test_ai_controller.py",
    "scripts/developer_tools.py",
)


def run_test(relative_path: str) -> bool:
    print(f"\n[RUN] {relative_path}")
    completed = subprocess.run(
        [sys.executable, relative_path],
        cwd=PROJECT_ROOT,
        check=False,
    )

    if completed.returncode == 0:
        print(f"[PASS] {relative_path}")
        return True

    print(f"[FAIL] {relative_path} (exit code {completed.returncode})")
    return False


def main() -> int:
    print("OpportunityLab Phase 1 Smoke Tests")
    print("Network access is not required.")

    results = [run_test(test_file) for test_file in TEST_FILES]
    passed = sum(results)
    failed = len(results) - passed

    print("\n" + "=" * 64)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed:
        print("SMOKE TESTS FAILED")
        return 1

    print("ALL SMOKE TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
