# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer  
Focus: Expand discovery sources without destabilising Phase 1.

## Package-020A-01

Discovery-source interface foundation. Passed.

## Package-020A-02

Source registry and enable/disable control. Passed.

## Package-020A-03

Multi-source execution pipeline. Passed.

## Package-020A-04

### Goal

Add discovery result aggregation and source execution statistics.

### Files to copy

Copy every file from this package into the matching location in the OpportunityLab project. Replace existing files when prompted.

### New files

- `src/discovery/discovery_result.py`
- `src/discovery/result_aggregator.py`
- `scripts/test_phase2_result_aggregation.py`

### Complete replacements

- `src/discovery/__init__.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

```text
python scripts\test_phase2_result_aggregation.py
```

### Expected result

```text
Phase 2 result aggregation test passed.
```

### Stop condition

Stop after this test and report `passed` or paste the error.
