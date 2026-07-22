# OpportunityLab AI Handover

## Current Status

Phase 1 is complete.

OpportunityLab is a Python desktop application using CustomTkinter.

## Current Phase

Phase 2 — Discovery Expansion

Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-11

### Purpose

Allow each search to use a selected subset of enabled discovery sources.

### New file

- `scripts/test_phase2_source_selection.py`

### Replaced files

- `src/core/search_service.py`
- `src/discovery/discovery_pipeline.py`
- `src/discovery/source_registry.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- `SearchService.search()` accepts optional `source_names`.
- `DiscoveryPipeline.run()` and `execute()` accept optional source names.
- Only enabled sources in the requested subset are executed.
- Duplicate source names are ignored while preserving requested order.
- Unknown source names raise `KeyError`.
- Existing searches without `source_names` continue using all enabled sources.
- No UI changes.
- No live API test required.

### Test

```text
python scripts\test_phase2_source_selection.py
```

Expected:

```text
Phase 2 source selection test passed.
```
