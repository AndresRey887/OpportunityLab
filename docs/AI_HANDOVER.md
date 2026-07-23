# OpportunityLab AI Handover

## Current build

- Version: 0.22.0
- Package: Package-022A-07
- Build: 7
- Codename: Pathfinder
- Phase 4: In progress

## Package-022A-07

This package adds a decision-review dashboard.

- Pipeline now provides a **Review** action.
- Summary cards show tracked opportunities, completed outcomes, success rate,
  recommendation accuracy, and duplicate-family count.
- Recommendation accuracy is based on Helpful and Not Helpful feedback.
- Strong Patterns identifies high-performing sources, keywords, and opportunity
  types.
- Weak Patterns identifies low ratings and unsuccessful recorded patterns.
- Evidence Gaps explains exactly where more tracking, outcomes, or feedback is
  needed.
- Lessons gathers the newest lessons learned from completed outcomes.
- All calculations are derived from existing persistent Phase 4 data.

## New files

- `src/review/__init__.py`
- `src/review/decision_pattern.py`
- `src/review/decision_review_service.py`
- `src/ui/decision_review_window.py`
- `scripts/test_phase4_decision_review.py`

## Replaced files

- `src/ui/main_window.py`
- `src/ui/pipeline_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Complete Phase 4 with a consolidated Pathfinder verification, learning-data
export, and final interface checks.
