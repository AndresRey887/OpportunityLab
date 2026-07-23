"""Run a controlled list of OpportunityLab regression scripts."""

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RegressionResult:
    script: str
    passed: bool
    duration_seconds: float
    output: str


class RegressionRunner:
    def __init__(
        self,
        project_root: str | Path = ".",
        timeout_seconds: float = 60.0,
    ) -> None:
        self.project_root = Path(project_root)
        self.timeout_seconds = timeout_seconds

    def run(self, scripts: tuple[str, ...]) -> tuple[RegressionResult, ...]:
        return tuple(self._run_script(script) for script in scripts)

    def _run_script(self, script: str) -> RegressionResult:
        started = time.perf_counter()
        path = self.project_root / script
        if not path.is_file():
            return RegressionResult(script, False, 0.0, "Test script is missing.")
        try:
            completed = subprocess.run(
                [sys.executable, str(path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            output = "\n".join(
                part.strip()
                for part in (completed.stdout, completed.stderr)
                if part.strip()
            )
            passed = completed.returncode == 0
        except subprocess.TimeoutExpired:
            output = f"Timed out after {self.timeout_seconds:g} seconds."
            passed = False
        duration = time.perf_counter() - started
        return RegressionResult(script, passed, duration, output)
