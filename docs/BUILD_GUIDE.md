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

### Files to copy

Copy every file from this package into the matching location in the OpportunityLab project. Replace existing files when prompted.

### New files

- src/discovery/source_registry.py
- scripts/test_phase2_source_registry.py
- scripts/test_phase2_discovery_sources.py

### Complete replacements

- src/discovery/__init__.py
- src/core/search_service.py
- src/version.py
- docs/AI_HANDOVER.md
- docs/BUILD_GUIDE.md

### Test command

Run from the OpportunityLab project root with the virtual environment active:

```bat
python scripts\test_phase2_source_registry.py
```

### Expected result

```text
Phase 2 source registry test passed.
```

### Stop condition

Do not install the next package until this test passes.
