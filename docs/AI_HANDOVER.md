# OpportunityLab AI Handover

## Current build

- Version: 0.21.0
- Package: Package-021A-07
- Build: 7
- Codename: Catalyst

## Package-021A-07

This package adds portable pipeline and opportunity exports.

- Pipeline views can be exported as Windows-friendly UTF-8 CSV files.
- Current stage and priority filters are respected during CSV export.
- CSV rows include status, priority, rating, score, follow-up, checklist
  progress, draft state, interactions, source, URL, and notes.
- Every pipeline opportunity has a Report action.
- Text reports combine the opportunity, contact details, checklist, response
  draft, and complete interaction history.
- Export locations and filenames are selected through standard Windows dialogs.

## New files

- `src/exports/__init__.py`
- `src/exports/export_service.py`
- `scripts/test_phase3_exports.py`

## Replaced files

- `src/ui/main_window.py`
- `src/ui/pipeline_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Complete Phase 3 with backup and restore tools plus a full phase verification.
