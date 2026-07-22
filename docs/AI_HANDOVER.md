# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-23

### Purpose

Add the persistent model and storage foundation for scheduled searches.

### New files

- `src/scheduling/__init__.py`
- `src/scheduling/search_schedule.py`
- `src/scheduling/search_schedule_store.py`
- `scripts/test_phase2_search_schedule.py`

### Replaced files

- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Schedules store a query, interval, enabled state, and selected sources.
- Last-run and next-run times use UTC ISO timestamps.
- Schedules persist in `data/search_schedules.json`.
- No UI or automatic execution changes in this package.

### Test

`python scripts\test_phase2_search_schedule.py`

Expected: `Phase 2 search schedule test passed.`
