# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-22 — Discovery, filtering, and reporting.
- Package-020A-23 through Package-020A-27 — Scheduled-search foundation and integration.

## Package-020A-28

### Goal

Add a visible window for managing scheduled searches.

### New files

- `src/ui/scheduled_search_window.py`
- `scripts/test_phase2_schedule_window.py`

### Complete replacements

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_schedule_window.py`

### Expected result

`Phase 2 schedule window test passed.`

Stop after this test and report `passed` or paste the error.
