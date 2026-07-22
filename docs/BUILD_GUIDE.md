# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-22 — Discovery, filtering, and reporting.
- Package-020A-23 through Package-020A-34 — Scheduled searches and notifications.
- Package-020A-35 — Opportunity grouping foundation.
- Package-020A-36 — Grouped results UI.

## Package-020A-37

### Goal

Allow source result groups to collapse and expand.

### New files

- `scripts/test_phase2_collapsible_result_groups.py`

### Complete replacements

- `src/ui/results_panel.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_collapsible_result_groups.py`

### Expected result

`Phase 2 collapsible result-group test passed.`

Stop after this test and report `passed` or paste the error.
