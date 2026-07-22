# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-18

### Purpose

Make Filter Manager source selections control which searches execute.

### Replaced files

- `src/core/search_service.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### New files

- `scripts/test_phase2_selected_source_execution.py`

### Behaviour

- Unchecked sources are not called during a normal UI search.
- Selecting every source preserves the existing all-source search.
- Explicit programmatic `source_names` still take priority.
- Startup version display properties are retained.

### Test

`python scripts\test_phase2_selected_source_execution.py`

Expected: `Phase 2 selected-source execution test passed.`
