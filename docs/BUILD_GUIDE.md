# OpportunityLab Build Guide

## Package 100B-04 test

```powershell
python scripts/test_text_size_settings.py
```

Expected: `Text size settings test passed.`

## Package 100B-03 test

```powershell
python scripts/test_ollama_profile_drafts.py
```

Expected: `Ollama profile draft test passed.`

## Package 100B-02A test

```powershell
python scripts/test_gemini_response_parsing.py
```

Expected: `Gemini response parsing test passed.`

## Package 100B-02 test

```powershell
python scripts/test_sender_profiles.py
```

Expected: `Sender profiles test passed.`

## Package 100B-01 test

```powershell
python scripts/test_gemini_key_switching.py
```

Expected: `Gemini key switching test passed.`

Configure `config\secrets.py` with:

```python
GEMINI_API_KEY_PRIMARY = "your primary key"
GEMINI_API_KEY_ALTERNATE = "your alternate key"
```

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
