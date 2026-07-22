# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-12 — Discovery pipeline foundation.
- Package-020A-13 — Reddit discovery source.
- Package-020A-14 — YouTube discovery source.
- Package-020A-15 — Company-website discovery source.
- Package-020A-16 — Source filter engine.

## Package-020A-17

### Goal

Add source-selection controls to the Filter Manager.

### New files

- `scripts/test_phase2_source_filter_ui.py`

### Complete replacements

- `src/ui/filter_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_source_filter_ui.py`

### Expected result

`Phase 2 source filter UI test passed.`

Stop after this test and report `passed` or paste the error.
