# OpportunityLab Build Guide

## Install Package-021A-06

Copy every folder from the package ZIP into the OpportunityLab project folder.
Allow Windows to merge folders and replace existing files.

## Test

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase3_pipeline_dashboard.py
```

Expected result:

```text
Phase 3 pipeline dashboard test passed.
```

## Run

```powershell
python -m src.ui.main_window
```

Choose **Pipeline...** from the main toolbar to see stage totals, priority
views, progress, drafts, and interaction counts.
