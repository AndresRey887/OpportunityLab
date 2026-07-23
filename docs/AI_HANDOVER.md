# OpportunityLab AI Handover

## Current build

- Version: 0.21.0
- Package: Package-021A-08
- Build: 8
- Codename: Catalyst
- Phase 3: Complete

## Package-021A-08

This package completes Phase 3 with safe backup and restore tools.

- The main toolbar now provides a Data window.
- Backups include OpportunityLab JSON, SQLite, and database files from `data`.
- Backups contain a manifest with app, version, package, time, and file list.
- Restore validates the manifest, file list, paths, extensions, and total size.
- Unsafe path traversal entries and invalid archives are rejected.
- Restore replaces matching saved-data files and preserves unrelated files.
- The app clearly requests confirmation before restoring.
- A restart message is shown after a successful restore.
- The completion test covers backup, restore, safety validation, and the Phase 3
  tracking, workflow, response, contact, and pipeline foundations.

## New files

- `src/backups/__init__.py`
- `src/backups/backup_service.py`
- `src/ui/data_tools_window.py`
- `scripts/test_phase3_complete.py`

## Replaced files

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Phase 3 delivered

- Persistent opportunity tracking, ratings, status, notes, and follow-ups
- Due and upcoming reminder summaries
- Persistent action checklists and progress
- Reusable response templates and saved drafts
- Contact records and dated interaction history
- Pipeline stage totals, priority views, and quick actions
- CSV pipeline exports and complete opportunity reports
- Data backup and restore

## Next step

Open and visually verify the completed Phase 3 interface before planning the
next phase.
