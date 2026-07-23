"""Complete OpportunityLab health report."""

from __future__ import annotations

from dataclasses import dataclass

from src.health.health_check import HealthCheck


@dataclass(frozen=True)
class HealthReport:
    checks: tuple[HealthCheck, ...]

    @property
    def passed(self) -> int:
        return sum(check.status == "Passed" for check in self.checks)

    @property
    def warnings(self) -> int:
        return sum(check.status == "Warning" for check in self.checks)

    @property
    def failed(self) -> int:
        return sum(check.status == "Failed" for check in self.checks)

    @property
    def overall_status(self) -> str:
        if self.failed:
            return "Failed"
        if self.warnings:
            return "Warning"
        return "Healthy"

    def to_dict(self) -> dict:
        return {
            "overall_status": self.overall_status,
            "passed": self.passed,
            "warnings": self.warnings,
            "failed": self.failed,
            "checks": [check.to_dict() for check in self.checks],
        }
