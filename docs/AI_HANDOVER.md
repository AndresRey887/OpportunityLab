# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-33

### Purpose

Identify new opportunities in repeated scheduled searches.

### Replaced files

- `src/scheduling/scheduled_search_result.py`
- `src/scheduling/scheduled_search_runner.py`
- `src/ui/scheduled_search_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### New files

- `scripts/test_phase2_scheduled_new_results.py`

### Behaviour

- Scheduled results compare opportunity URLs with earlier runs of that schedule.
- Each run stores the total result count and new result count.
- New opportunity buttons are marked `NEW` in scheduled history.
- Repeated URLs are retained but are not counted as new.

### Test

`python scripts\test_phase2_scheduled_new_results.py`

Expected: `Phase 2 scheduled new-result test passed.`
