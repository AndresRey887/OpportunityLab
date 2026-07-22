# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-28

### Purpose

Add a visible Scheduled Searches management window.

### New files

- `src/ui/scheduled_search_window.py`
- `scripts/test_phase2_schedule_window.py`

### Replaced files

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- The main search bar includes a `Schedules...` button.
- Users can add a query, interval, and discovery sources.
- Saved schedules can be enabled, disabled, or deleted.
- Changes persist through the existing schedule store.

### Test

`python scripts\test_phase2_schedule_window.py`

Expected: `Phase 2 schedule window test passed.`
