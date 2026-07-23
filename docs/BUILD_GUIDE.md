# OpportunityLab Build Guide

## Install Package-022A-07

Copy every folder from the package ZIP into the OpportunityLab project folder.
Allow Windows to merge folders and replace existing files.

## Test

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase4_decision_review.py
```

Expected result:

```text
Phase 4 decision review test passed.
```

## Run

```powershell
python -m src.ui.main_window
```

Open **Pipeline...** and choose **Review** to see accuracy, strong and weak
patterns, evidence gaps, and recorded lessons.
