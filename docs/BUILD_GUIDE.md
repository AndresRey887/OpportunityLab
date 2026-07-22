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

## Package-020A-09

### Goal

Return one structured object from a complete discovery pipeline run.

### Files to copy

Copy every file from this package into the matching location in the
OpportunityLab project. Replace existing files when prompted.

### New files

- `src/discovery/discovery_run.py`
- `scripts/test_phase2_discovery_run.py`

### Complete replacements

- `src/discovery/discovery_pipeline.py`
- `src/discovery/__init__.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

```text
python scripts\test_phase2_discovery_run.py
```

### Expected result

```text
Phase 2 discovery run test passed.
```

### Stop condition

Stop after this test and report `passed` or paste the error.
