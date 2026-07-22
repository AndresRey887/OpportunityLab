# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-19

### Purpose

Show each opportunity's discovery source directly on its result card.

### Replaced files

- `src/ui/results_panel.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### New files

- `scripts/test_phase2_result_source_labels.py`

### Behaviour

- Every result card displays its source above the title.
- Existing score colours and click selection remain unchanged.
- Startup version display properties are retained.

### Test

`python scripts\test_phase2_result_source_labels.py`

Expected: `Phase 2 result source-label test passed.`
