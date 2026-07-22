# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-17

### Purpose

Add visible source-selection controls to the Filter Manager.

### Replaced files

- `src/ui/filter_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### New files

- `scripts/test_phase2_source_filter_ui.py`

### Behaviour

- Filter Manager displays Serper, Reddit, YouTube, and Company Websites.
- At least one result source must remain selected.
- Selecting every source preserves the existing show-all behaviour.
- Startup version display properties are retained.

### Test

`python scripts\test_phase2_source_filter_ui.py`

Expected: `Phase 2 source filter UI test passed.`
