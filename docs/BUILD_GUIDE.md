# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-22 — Discovery, filtering, and reporting.
- Package-020A-23 through Package-020A-34 — Scheduled searches and notifications.
- Package-020A-35 through Package-020A-38 — Result grouping controls.

## Package-020A-39

### Goal

Sort grouped results by score or title.

### New files

- `scripts/test_phase2_result_sorting.py`

### Complete replacements

- `src/ui/main_window.py`
- `src/ui/results_panel.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_result_sorting.py`

### Expected result

`Phase 2 result sorting test passed.`

Stop after this test and report `passed` or paste the error.
