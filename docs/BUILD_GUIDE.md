# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer  
Focus: Expand discovery sources without destabilising Phase 1.

## Completed Packages

- Package-020A-01 — Discovery-source interface.
- Package-020A-02 — Source registry.
- Package-020A-03 — Multi-source execution.
- Package-020A-04 — Result aggregation.
- Package-020A-05 — Aggregation foundation update.
- Package-020A-06 — Opportunity normalization.
- Package-020A-07 — Opportunity deduplication.
- Package-020A-08 — Source registry management.
- Package-020A-09 — Structured discovery run.
- Package-020A-10 — SearchService integration.

## Package-020A-11

### Goal

Allow individual searches to choose which enabled discovery sources run.

### Files to copy

Copy every file from this package into the matching location in the
OpportunityLab project. Replace existing files when prompted.

### New file

- `scripts/test_phase2_source_selection.py`

### Complete replacements

- `src/core/search_service.py`
- `src/discovery/discovery_pipeline.py`
- `src/discovery/source_registry.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

```text
python scripts\test_phase2_source_selection.py
```

### Expected result

```text
Phase 2 source selection test passed.
```

### Stop condition

Stop after this test and report `passed` or paste the error.
