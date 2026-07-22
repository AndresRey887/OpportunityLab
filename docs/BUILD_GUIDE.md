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

## Package-020A-10

### Goal

Connect the complete Phase 2 discovery run to SearchService.

### Files to copy

Copy every file from this package into the matching location in the
OpportunityLab project. Replace existing files when prompted.

### New file

- `scripts/test_phase2_search_service_integration.py`

### Complete replacements

- `src/core/search_service.py`
- `src/discovery/source_registry.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

```text
python scripts\test_phase2_search_service_integration.py
```

### Expected result

```text
Phase 2 SearchService integration test passed.
```

### Stop condition

Stop after this test and report `passed` or paste the error.
