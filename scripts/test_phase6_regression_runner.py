"""Verify controlled regression execution, failures, and missing scripts."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.health.regression_runner import RegressionRunner
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        scripts = root / "scripts"
        scripts.mkdir()
        (scripts / "passing.py").write_text(
            "print('sample passed')\n",
            encoding="utf-8",
        )
        (scripts / "failing.py").write_text(
            "raise RuntimeError('sample failure')\n",
            encoding="utf-8",
        )
        runner = RegressionRunner(root, timeout_seconds=10)
        results = runner.run(
            (
                "scripts/passing.py",
                "scripts/failing.py",
                "scripts/missing.py",
            )
        )

        assert results[0].passed
        assert "sample passed" in results[0].output
        assert not results[1].passed
        assert "sample failure" in results[1].output
        assert not results[2].passed
        assert results[2].output == "Test script is missing."

    release_runner = (
        PROJECT_ROOT / "scripts/run_release_checks.py"
    ).read_text(encoding="utf-8")
    assert "RELEASE_CHECKS" in release_runner
    assert "test_phase6_system_health.py" in release_runner
    assert VERSION_INFO.package == "Package-100A-08"
    assert VERSION_INFO.build == 10
    print("Phase 6 regression runner test passed.")


if __name__ == "__main__":
    main()
