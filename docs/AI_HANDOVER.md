# OpportunityLab AI Handover

## Current Status

Phase 1 is complete.  
Phase 2 is complete.  
Phase 3 is in development.

## Current Version

Version: 0.21.0  
Codename: Catalyst  
Package: Package-021A-02

## Package-021A-02

### Purpose

Add follow-up reminders and visible reminder notices to opportunity tracking.

### New files

- `src/reminders/__init__.py`
- `src/reminders/follow_up_reminder.py`
- `src/reminders/reminder_service.py`
- `scripts/test_phase3_follow_up_reminders.py`

### Replaced files

- `src/ui/main_window.py`
- `src/ui/tracking_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Follow-up dates generate overdue, due-today, and upcoming reminders.
- Closed opportunities do not generate reminders.
- The main toolbar displays the number of due reminders.
- Startup status reports due follow-ups.
- The tracking window shows due and seven-day upcoming totals.
- Each tracked card displays its follow-up date.

### Test

`python scripts\test_phase3_follow_up_reminders.py`

Expected: `Phase 3 follow-up reminder test passed.`
