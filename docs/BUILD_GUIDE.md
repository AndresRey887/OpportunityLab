# OpportunityLab Build Guide

## Package 100A-08 test

From `D:\OpportunityLab` with the virtual environment active:

```powershell
python scripts/test_phase6_release_manifest.py
```

Expected result:

```text
Phase 6 release manifest test passed.

## Run all Phase 6 release checks

```powershell
python scripts/run_release_checks.py
```

## Create a Windows release

```powershell
python -m pip install -r requirements-build.txt
python scripts/build_windows_release.py
```

The application folder is created at `dist\OpportunityLab`.

Create its integrity manifest with:

```powershell
python scripts/create_release_manifest.py
```
```

## Run OpportunityLab

```powershell
python -m src.ui.main_window
```

Open **Data Tools**, then choose **System Health**.
