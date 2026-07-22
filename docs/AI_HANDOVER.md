# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-25

### Purpose

Execute searches that the scheduler reports as due.

### New files

- `src/scheduling/scheduled_search_result.py`
- `src/scheduling/scheduled_search_runner.py`
- `scripts/test_phase2_scheduled_search_runner.py`

### Replaced files

- `src/scheduling/__init__.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Due schedules run through the existing SearchService interface.
- A schedule can restrict execution to named discovery sources.
- Successful runs store counts and advance the next-run time.
- One failed schedule does not stop other scheduled searches.
- No background timer or UI changes in this package.

### Test

`python scripts\test_phase2_scheduled_search_runner.py`

Expected: `Phase 2 scheduled search runner test passed.`
