# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-22 — Discovery, filtering, and reporting.
- Package-020A-23 — Search schedule model and storage.

## Package-020A-24

### Goal

Manage persistent schedules and identify due searches.

### New files

- `src/scheduling/search_scheduler.py`
- `scripts/test_phase2_search_scheduler.py`

### Complete replacements

- `src/scheduling/__init__.py`
- `src/scheduling/search_schedule.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_search_scheduler.py`

### Expected result

`Phase 2 search scheduler test passed.`

Stop after this test and report `passed` or paste the error.
