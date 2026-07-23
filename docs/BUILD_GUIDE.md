# OpportunityLab Build Guide

## Install Package-022A-02

Copy every folder from the package ZIP into the OpportunityLab project folder.
Allow Windows to merge folders and replace existing files.

## Test

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase4_opportunity_timeline.py
```

Expected result:

```text
Phase 4 opportunity timeline test passed.
```

## Run

```powershell
python -m src.ui.main_window
```

Open **Tracked...** or **Pipeline...**, then choose **Timeline** beside a tracked
opportunity.
