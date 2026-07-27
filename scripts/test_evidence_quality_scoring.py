"""Offline test for actionable evidence-quality scoring."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.opportunity import Opportunity
from src.rules.evidence_quality_rule import EvidenceQualityRule
from src.version import VERSION_INFO


def main() -> None:
    rule = EvidenceQualityRule()

    official = Opportunity(
        title="Community grant applications open",
        url="https://community.vic.gov.au/grants/apply",
        snippet=(
            "Eligible charities can apply online for funding up to $25,000. "
            "Applications close 30 September."
        ),
        source="Serper",
    )
    video = Opportunity(
        title="Community grant funding tips for charities",
        url="https://www.youtube.com/watch?v=example",
        snippet="A video explaining grants, applications and sponsorship.",
        source="YouTube",
    )

    official_points = rule.evaluate(official)
    video_points = rule.evaluate(video)

    assert official_points >= 50
    assert official.metadata["evidence_quality_tier"] == "Strong Evidence"
    assert video_points <= -20
    assert video.metadata["evidence_quality_tier"] == "Weak Evidence"
    assert official_points - video_points >= 70

    details = (
        PROJECT_ROOT / "src" / "ui" / "details_panel.py"
    ).read_text(encoding="utf-8")
    results = (
        PROJECT_ROOT / "src" / "ui" / "results_panel.py"
    ).read_text(encoding="utf-8")
    assert "Evidence quality:" in details
    assert "evidence_quality_tier" in results

    assert VERSION_INFO.version == "1.2.1"
    assert VERSION_INFO.package == "Package-110A-07A"
    assert VERSION_INFO.build == 10
    print("Evidence quality scoring test passed.")


if __name__ == "__main__":
    main()
