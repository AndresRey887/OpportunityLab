# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer  
Focus: Expand discovery sources without destabilising Phase 1.

## Completed Packages

- Package-020A-01 through Package-020A-12 — Discovery pipeline foundation.
- Package-020A-13 — Reddit discovery source.
- Package-020A-14 — YouTube discovery source.
- Package-020A-15 — Company-website discovery source.

## Package-020A-16

### Goal

Add source-based filtering without changing current default behaviour.

### New files

- `src/filters/source_filter.py`
- `scripts/test_phase2_source_filter.py`

### Complete replacements

- `src/filters/filter_engine.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

```text
python scripts\test_phase2_source_filter.py
```

### Expected result

```text
Phase 2 source filter test passed.
```

Stop after this test and report `passed` or paste the error.
