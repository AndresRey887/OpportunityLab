# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-22 — Discovery, filtering, and reporting.
- Package-020A-23 through Package-020A-30 — Scheduled-search execution, UI, and history.

## Package-020A-31

### Goal

Run a saved schedule immediately from the UI.

### New files

- `scripts/test_phase2_schedule_run_now.py`

### Complete replacements

- `src/scheduling/scheduled_search_runner.py`
- `src/ui/scheduled_search_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_schedule_run_now.py`

### Expected result

`Phase 2 schedule Run Now test passed.`

Stop after this test and report `passed` or paste the error.
