# OpportunityLab AI Handover

## Current build

- Version: 0.22.0
- Package: Package-022A-02
- Build: 2
- Codename: Pathfinder
- Phase 4: In progress

## Package-022A-02

This package adds a permanent chronological timeline to every tracked
opportunity.

- Tracking and tracked-detail changes create timeline events.
- Checklist creation, completion, reopening, addition, and removal are recorded.
- Applying templates and saving drafts are recorded.
- Contact updates and dated interactions are recorded.
- Saved outcomes are recorded.
- Users can add manual timeline notes.
- Timeline actions are available from Tracked Opportunities and Pipeline.
- Events are shown newest first and remain after the opportunity changes.
- Timelines are stored in `data/opportunity_timeline.json`.
- Existing backups automatically include timeline data.

## New files

- `src/timeline/__init__.py`
- `src/timeline/timeline_event.py`
- `src/timeline/timeline_store.py`
- `src/timeline/timeline_service.py`
- `src/ui/timeline_window.py`
- `scripts/test_phase4_opportunity_timeline.py`

## Replaced files

- `src/tracking/tracking_service.py`
- `src/workflows/workflow_service.py`
- `src/responses/response_service.py`
- `src/contacts/contact_service.py`
- `src/outcomes/outcome_service.py`
- `src/ui/main_window.py`
- `src/ui/tracking_window.py`
- `src/ui/pipeline_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Add duplicate clustering so related discoveries can be reviewed as one
opportunity family without losing their individual sources.
