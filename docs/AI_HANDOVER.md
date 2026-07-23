# OpportunityLab AI Handover

## Current build

- Version: 0.21.0
- Package: Package-021A-05
- Build: 5
- Codename: Catalyst

## Package-021A-05

This package adds contact records and interaction histories.

- Every tracked opportunity can have a named contact and organisation.
- Email, phone, website, and contact notes are saved persistently.
- Interaction history supports Email, Phone, Meeting, Application, Note, and
  Other entries.
- Every history entry includes a date and summary.
- History is displayed newest first and entries can be removed.
- Selected results and Tracked Opportunities both provide direct access.
- Contacts are stored in `data/opportunity_contacts.json`.
- History is stored in `data/interaction_history.json`.

## New files

- `src/contacts/__init__.py`
- `src/contacts/contact_record.py`
- `src/contacts/interaction_entry.py`
- `src/contacts/contact_store.py`
- `src/contacts/contact_service.py`
- `src/ui/contact_history_window.py`
- `scripts/test_phase3_contacts_history.py`

## Replaced files

- `src/ui/main_window.py`
- `src/ui/tracking_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Continue Phase 3 with an opportunity pipeline dashboard, stage totals, and
priority views.
