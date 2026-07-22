# OpportunityLab AI Handover

## Current Status

Phase 1 is complete.

OpportunityLab is a Python desktop application using CustomTkinter.

## Current Phase

Phase 2 — Discovery Expansion

Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-13

### Purpose

Add Reddit as the first additional live discovery source.

### New files

- `src/discovery/reddit_search_source.py`
- `scripts/test_phase2_reddit_source.py`

### Replaced files

- `src/core/search_service.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Default searches now run the existing general Serper search and a Reddit-specific search.
- Reddit discovery reuses the existing Serper API key and client.
- Injected sources and registries keep their previous behaviour.
- Failed sources remain isolated by the discovery pipeline.
- The package test is offline and does not use an API key.

### Test

```text
python scripts\test_phase2_reddit_source.py
```

Expected:

```text
Phase 2 Reddit source test passed.
```
