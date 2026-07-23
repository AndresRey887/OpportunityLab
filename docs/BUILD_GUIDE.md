# OpportunityLab Build Guide

## Install Package-021A-07

Copy every folder from the package ZIP into the OpportunityLab project folder.
Allow Windows to merge folders and replace existing files.

## Test

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase3_exports.py
```

Expected result:

```text
Phase 3 export test passed.
```

## Run

```powershell
python -m src.ui.main_window
```

Open **Pipeline...**, then choose **Export CSV** for the current view or
**Report** beside an opportunity.
