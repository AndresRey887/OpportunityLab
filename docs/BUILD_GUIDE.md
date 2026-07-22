# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-22 — Discovery, filtering, and reporting.
- Package-020A-23 through Package-020A-34 — Scheduled searches and notifications.
- Package-020A-35 through Package-020A-37 — Opportunity grouping and collapsible groups.

## Package-020A-38

### Goal

Switch result grouping between source and website.

### New files

- `scripts/test_phase2_grouping_selector.py`

### Complete replacements

- `src/ui/results_panel.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_grouping_selector.py`

### Expected result

`Phase 2 grouping selector test passed.`

Stop after this test and report `passed` or paste the error.
