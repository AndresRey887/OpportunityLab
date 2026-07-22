# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-12 — Discovery pipeline foundation.
- Package-020A-13 through Package-020A-15 — Live discovery sources.
- Package-020A-16 through Package-020A-18 — Source filtering and execution.
- Package-020A-19 — Result source labels.

## Package-020A-20

### Goal

Save filter settings between application sessions.

### New files

- `src/filters/filter_settings_store.py`
- `scripts/test_phase2_filter_persistence.py`

### Complete replacements

- `src/filters/filter_engine.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_filter_persistence.py`

### Expected result

`Phase 2 filter persistence test passed.`

Stop after this test and report `passed` or paste the error.
