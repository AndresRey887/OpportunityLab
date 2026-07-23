# OpportunityLab Build Guide

## Package 100A-03 tests

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase6_system_health.py
python scripts/test_phase6_release_report.py
python scripts/test_phase6_crash_reporting.py
```

Expected result:

```text
Phase 6 system health test passed.
Phase 6 release report test passed.
Phase 6 crash reporting test passed.
```

## Run OpportunityLab

```powershell
python -m src.ui.main_window
```

Open **Data Tools**, then choose **System Health**.
