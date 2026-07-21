# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer  
Focus: Expand discovery sources without destabilising Phase 1.

## Package-020A-01

### Goal

Introduce a common discovery-source interface while preserving the existing Serper search behaviour.

### Test result

Passed.

## Package-020A-02

### Goal

Add source registration and source enable/disable control behind the existing search workflow.

### Test result

Passed.

## Package-020A-03

### Goal

Add a multi-source execution pipeline and per-source execution statistics without changing the UI or adding another live source.

### Files to copy

Copy every file from this package into the matching location in the OpportunityLab project. Replace existing files when prompted.

### New files

- `src/discovery/execution_result.py`
- `src/discovery/discovery_pipeline.py`
- `scripts/test_phase2_multi_source_pipeline.py`

### Complete replacements

- `src/discovery/__init__.py`
- `src/core/search_service.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

Run from the OpportunityLab project root with the virtual environment active:

```bat
python scripts\test_phase2_multi_source_pipeline.py
```

### Expected result

```text
Phase 2 multi-source pipeline test passed.
```

### Stop condition

Do not install the next package until this test passes.
