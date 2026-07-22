# OpportunityLab AI Handover

## Current Status

Phase 1 is complete.

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-15

### Purpose

Add company-website discovery using the existing Serper connection.

### New files

- `src/discovery/company_website_search_source.py`
- `scripts/test_phase2_company_website_source.py`

### Replaced files

- `src/core/search_service.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Default searches now include general web, Reddit, YouTube, and company websites.
- The new source excludes Reddit and YouTube from its own results.
- It reuses the existing Serper API key and client.
- The package test is offline and does not use an API key.

### Test

```text
python scripts\test_phase2_company_website_source.py
```

Expected: `Phase 2 company-website source test passed.`
