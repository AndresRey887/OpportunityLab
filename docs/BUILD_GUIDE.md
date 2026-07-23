# OpportunityLab Build Guide

## Phase 3

Version: 0.21.0  
Codename: Catalyst  
Focus: Turn discovered opportunities into actions.

## Package-021A-01

### Goal

Add persistent opportunity tracking and its complete first UI workflow.

### New files

- `src/tracking/__init__.py`
- `src/tracking/tracked_opportunity.py`
- `src/tracking/tracking_store.py`
- `src/tracking/tracking_service.py`
- `src/ui/tracking_window.py`
- `scripts/test_phase3_opportunity_tracking.py`

### Complete replacements

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase3_opportunity_tracking.py`

### Expected result

`Phase 3 opportunity tracking test passed.`

Stop after this test and report `passed` or paste the error.
