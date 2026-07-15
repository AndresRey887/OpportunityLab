# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer  
Focus: Expand discovery sources without destabilising Phase 1.

## Package-020A-01

### Goal

Introduce a common discovery-source interface while preserving the existing Serper search behaviour.

### Files to copy

Copy every file from this package into the matching location in the OpportunityLab project. Replace existing files when prompted.

### New files

- src/discovery/__init__.py
- src/discovery/search_source.py
- src/discovery/serper_search_source.py
- scripts/test_phase2_discovery_sources.py
- docs/BUILD_GUIDE.md

### Complete replacements

- src/core/search_service.py
- src/version.py
- docs/AI_HANDOVER.md

### Test command

Run from the OpportunityLab project root with the virtual environment active:

```bat
python scripts\test_phase2_discovery_sources.py
```

### Expected result

```text
Phase 2 discovery-source foundation test passed.
```

### Stop condition

Do not install the next package until this test passes.
