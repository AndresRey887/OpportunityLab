"""Run the supported OpportunityLab Phase 6 release checks."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.health.regression_runner import RegressionRunner

RELEASE_CHECKS = (
    "scripts/test_phase6_system_health.py",
    "scripts/test_phase6_release_report.py",
    "scripts/test_phase6_crash_reporting.py",
    "scripts/test_phase6_windows_build.py",
    "scripts/test_phase6_performance_tracking.py",
    "scripts/test_phase6_shutdown.py",
    "scripts/test_phase6_release_manifest.py",
)


def main() -> int:
    results = RegressionRunner(PROJECT_ROOT, timeout_seconds=90).run(
        RELEASE_CHECKS
    )
    print("OpportunityLab Release Checks")
    print("=" * 30)
    for result in results:
        status = "PASSED" if result.passed else "FAILED"
        print(f"{status}  {result.script}  ({result.duration_seconds:.2f}s)")
        if not result.passed and result.output:
            print(result.output)
    passed = sum(result.passed for result in results)
    print(f"\nResult: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
