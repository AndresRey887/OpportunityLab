# OpportunityLab AI Handover

## Current build

- Version: 0.21.0
- Package: Package-021A-03
- Build: 3
- Codename: Catalyst

## Package-021A-03

This package adds persistent action checklists to Phase 3 opportunity tracking.

- A selected search result can be tracked and opened as a checklist.
- Every new checklist starts with six practical default actions.
- Users can complete, add, and remove actions.
- Checklist progress is shown as a completed count and percentage.
- Checklists are stored in `data/opportunity_workflows.json`.
- Tracked Opportunities provides direct access to each checklist.

## New files

- `src/workflows/__init__.py`
- `src/workflows/action_item.py`
- `src/workflows/opportunity_workflow.py`
- `src/workflows/workflow_store.py`
- `src/workflows/workflow_service.py`
- `src/ui/checklist_window.py`
- `scripts/test_phase3_action_checklists.py`

## Replaced files

- `src/ui/main_window.py`
- `src/ui/tracking_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Continue Phase 3 with reusable response templates and opportunity-specific draft
workspaces.
