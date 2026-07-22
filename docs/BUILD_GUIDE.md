# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-22 — Discovery, filtering, and reporting.
- Package-020A-23 through Package-020A-34 — Scheduled searches and notifications.

## Package-020A-35

### Goal

Add opportunity grouping by source and website.

### New files

- `src/grouping/__init__.py`
- `src/grouping/opportunity_group.py`
- `src/grouping/opportunity_grouper.py`
- `scripts/test_phase2_opportunity_grouping.py`

### Complete replacements

- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_opportunity_grouping.py`

### Expected result

`Phase 2 opportunity grouping test passed.`

Stop after this test and report `passed` or paste the error.
