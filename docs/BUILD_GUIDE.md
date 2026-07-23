# OpportunityLab Build Guide

## Install Package-021A-05

Copy every folder from the package ZIP into the OpportunityLab project folder.
Allow Windows to merge folders and replace existing files.

## Test

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase3_contacts_history.py
```

Expected result:

```text
Phase 3 contacts and history test passed.
```

## Run

```powershell
python -m src.ui.main_window
```

Select an opportunity and choose **Contacts & History**, or open **Tracked
Opportunities** and choose **Contacts** beside an existing record.
