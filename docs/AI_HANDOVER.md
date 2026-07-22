# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-27

### Purpose

Connect scheduled-search monitoring to application startup and shutdown.

### Replaced files

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### New files

- `scripts/test_phase2_schedule_monitor_integration.py`

### Behaviour

- OpportunityLab starts the scheduled-search monitor after building the UI.
- The monitor checks for due schedules once per minute.
- Scheduled searches use a separate SearchService instance.
- The monitor stops cleanly before the application closes.
- No schedule-management UI in this package.

### Test

`python scripts\test_phase2_schedule_monitor_integration.py`

Expected: `Phase 2 schedule monitor integration test passed.`
