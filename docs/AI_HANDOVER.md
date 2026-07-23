# OpportunityLab AI Handover

## Current Status

Phase 1 is complete.  
Phase 2 is complete.  
Phase 3 is in development.

## Current Version

Version: 0.21.0  
Codename: Catalyst  
Package: Package-021A-01

## Package-021A-01

### Purpose

Deliver the first complete opportunity-tracking workflow.

### New files

- `src/tracking/__init__.py`
- `src/tracking/tracked_opportunity.py`
- `src/tracking/tracking_store.py`
- `src/tracking/tracking_service.py`
- `src/ui/tracking_window.py`
- `scripts/test_phase3_opportunity_tracking.py`

### Replaced files

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Selected search results can be added to tracking.
- Tracking records persist in `data/tracked_opportunities.json`.
- Duplicate URLs are not added twice.
- Tracked opportunities support status, 0–5 rating, notes, and follow-up date.
- The main toolbar opens the Tracked Opportunities window.
- Tracked records can be filtered, opened, updated, and removed.

### Test

`python scripts\test_phase3_opportunity_tracking.py`

Expected: `Phase 3 opportunity tracking test passed.`
