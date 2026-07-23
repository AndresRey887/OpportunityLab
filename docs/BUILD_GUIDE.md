# OpportunityLab Build Guide

## Phase 3

Version: 0.21.0  
Codename: Catalyst  
Focus: Turn discovered opportunities into actions.

## Completed Packages

- Package-021A-01 — Persistent opportunity tracking and tracking UI.

## Package-021A-02

### Goal

Add follow-up reminder calculation and visible reminder notices.

### New files

- `src/reminders/__init__.py`
- `src/reminders/follow_up_reminder.py`
- `src/reminders/reminder_service.py`
- `scripts/test_phase3_follow_up_reminders.py`

### Complete replacements

- `src/ui/main_window.py`
- `src/ui/tracking_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase3_follow_up_reminders.py`

### Expected result

`Phase 3 follow-up reminder test passed.`

Stop after this test and report `passed` or paste the error.
