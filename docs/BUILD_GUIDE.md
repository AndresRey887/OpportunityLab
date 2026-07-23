# OpportunityLab Build Guide

## Install Package-021A-08

Copy every folder from the package ZIP into the OpportunityLab project folder.
Allow Windows to merge folders and replace existing files.

## Test

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase3_complete.py
```

Expected result:

```text
Phase 3 complete test passed.
```

## Run

```powershell
python -m src.ui.main_window
```

Choose **Data...** to create or restore an OpportunityLab backup. Restart the
app after restoring saved data.
