# OpportunityLab AI Handover

## Current build

- Version: 0.21.0
- Package: Package-021A-04
- Build: 4
- Codename: Catalyst

## Package-021A-04

This package adds reusable response templates and saved draft workspaces.

- Selected results can open a Draft Response workspace.
- Tracked Opportunities provides direct Draft access.
- Three built-in templates cover enquiries, expressions of interest, and
  follow-ups.
- Template fields automatically insert the opportunity title, URL, and source.
- Subject and response body are saved separately for each opportunity.
- Drafts can be copied to the clipboard.
- Any edited draft can be saved as a reusable custom template.
- Templates are stored in `data/response_templates.json`.
- Drafts are stored in `data/opportunity_drafts.json`.

## New files

- `src/responses/__init__.py`
- `src/responses/response_template.py`
- `src/responses/opportunity_draft.py`
- `src/responses/response_store.py`
- `src/responses/response_service.py`
- `src/ui/draft_window.py`
- `scripts/test_phase3_response_drafts.py`

## Replaced files

- `src/ui/main_window.py`
- `src/ui/tracking_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Continue Phase 3 with contact records and an interaction history for each
tracked opportunity.
