# OpportunityLab AI Handover

## Current build

- Version: 0.21.0
- Package: Package-021A-06
- Build: 6
- Codename: Catalyst

## Package-021A-06

This package adds an opportunity pipeline dashboard.

- The main toolbar now provides a Pipeline window.
- Stage cards show totals for New, Reviewing, Applied, Watching, and Closed.
- Pipeline results can be filtered by stage and High, Medium, or Low priority.
- Priority combines opportunity score, user rating, and due follow-ups.
- Each row shows checklist progress, saved-draft state, and interaction count.
- Quick actions open the checklist, draft, contacts, or opportunity website.
- Pipeline results are sorted by priority automatically.

## New files

- `src/pipeline/__init__.py`
- `src/pipeline/pipeline_item.py`
- `src/pipeline/pipeline_service.py`
- `src/ui/pipeline_window.py`
- `scripts/test_phase3_pipeline_dashboard.py`

## Replaced files

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Continue Phase 3 with exportable opportunity reports and CSV pipeline exports.
