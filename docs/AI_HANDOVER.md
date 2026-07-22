# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-24

### Purpose

Manage saved schedules and identify searches that are due.

### New files

- `src/scheduling/search_scheduler.py`
- `scripts/test_phase2_search_scheduler.py`

### Replaced files

- `src/scheduling/__init__.py`
- `src/scheduling/search_schedule.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Schedules can be added, loaded, enabled, disabled, and removed.
- Due schedules are selected using UTC timestamps.
- Completed schedules receive new last-run and next-run times.
- No automatic execution or UI changes in this package.

### Test

`python scripts\test_phase2_search_scheduler.py`

Expected: `Phase 2 search scheduler test passed.`
